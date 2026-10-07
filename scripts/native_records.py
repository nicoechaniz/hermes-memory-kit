"""Native record revisions and attributed metadata; never signed authority."""
from __future__ import annotations

import json
import sqlite3
import time
import uuid

from sqlite_snapshot import verified_snapshot

SHELF_TYPES = {"episodes": "episodic", "mc-episodic": "episodic",
               "mc-skills": "procedural", "plans": "procedural"}
MODES = {"observed", "reported", "inferred", "generated"}
SOURCE_FIELDS = {"source_instance", "source_event_id", "source_version", "source_uri",
                 "subject", "actor", "mode", "reported_at", "event_end_ts",
                 "date_precision", "evidence", "correction_of", "selection_version"}


def metadata(value):
    if value is None:
        return {}
    if not isinstance(value, dict) or set(value) - SOURCE_FIELDS:
        raise ValueError("unsupported native source metadata")
    result = json.loads(json.dumps(value, allow_nan=False))
    if "mode" in result and result["mode"] not in MODES:
        raise ValueError("mode must be observed, reported, inferred or generated")
    for key in SOURCE_FIELDS - {"evidence", "reported_at", "event_end_ts"}:
        if key in result and not isinstance(result[key], str):
            raise ValueError(f"{key} must be a string")
    for key in ("reported_at", "event_end_ts"):
        if key in result and (not isinstance(result[key], int) or isinstance(result[key], bool)):
            raise ValueError(f"{key} must be an integer timestamp")
    if "evidence" in result and (not isinstance(result["evidence"], list)
                                 or not all(isinstance(x, str) for x in result["evidence"])):
        raise ValueError("evidence must be a list of attributed references")
    return result


def ensure_schema(con, db_path, *, snapshot=True):
    columns = {r[1] for r in con.execute("PRAGMA table_info(chapters)")}
    additions = {
        "record_uid": "TEXT",
        "revision": "INTEGER NOT NULL DEFAULT 1",
        "source_metadata_json": "TEXT NOT NULL DEFAULT '{}'",
        "engram_type": "TEXT NOT NULL DEFAULT 'semantic' CHECK (engram_type IN ('episodic','semantic','procedural'))",
        "event_ts": "INTEGER",
        "actor": "TEXT",
        "location_json": "TEXT",
    }
    missing = set(additions) - columns
    if not missing and con.execute("SELECT 1 FROM sqlite_master WHERE name='chapter_revisions'").fetchone():
        return
    con.commit()
    if snapshot and missing and con.execute("SELECT 1 FROM chapters LIMIT 1").fetchone():
        verified_snapshot(db_path, f"{db_path}.bak.prenative.{time.time_ns()}")
    con.execute("BEGIN IMMEDIATE")
    try:
        # Another writer may have completed migration while this connection
        # waited for the SQLite writer lock.
        missing = set(additions) - {r[1] for r in con.execute("PRAGMA table_info(chapters)")}
        for key, declaration in additions.items():
            if key in missing:
                con.execute(f"ALTER TABLE chapters ADD COLUMN {key} {declaration}")
        if "engram_type" in missing:
            for shelf, kind in SHELF_TYPES.items():
                con.execute("UPDATE chapters SET engram_type=? WHERE book_id IN "
                            "(SELECT b.id FROM books b JOIN shelves s ON s.id=b.shelf_id WHERE s.name=?)", (kind, shelf))
        for row in con.execute("SELECT id FROM chapters WHERE record_uid IS NULL").fetchall():
            con.execute("UPDATE chapters SET record_uid=? WHERE id=?", (str(uuid.uuid4()), row[0]))
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_chapters_record_uid ON chapters(record_uid)")
        con.execute("""CREATE TABLE IF NOT EXISTS chapter_revisions (
            id INTEGER PRIMARY KEY, record_uid TEXT NOT NULL, chapter_id INTEGER NOT NULL,
            revision INTEGER NOT NULL, snapshot_json TEXT NOT NULL,
            reason TEXT NOT NULL, archived_at INTEGER NOT NULL,
            UNIQUE(record_uid, revision))""")
        con.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS chapter_revisions_fts
            USING fts5(title, spr, raw, tags, content='', tokenize='unicode61')""")
        con.commit()
    except BaseException:
        con.rollback()
        raise


def archive(con, row, reason):
    snapshot = dict(row)
    book = con.execute("SELECT b.title AS book_title,b.source_kind,b.source_path,s.name AS shelf "
                       "FROM books b JOIN shelves s ON s.id=b.shelf_id WHERE b.id=?", (row['book_id'],)).fetchone()
    snapshot.update(dict(book))
    cursor = con.execute("INSERT INTO chapter_revisions(record_uid,chapter_id,revision,snapshot_json,reason,archived_at) "
                         "VALUES(?,?,?,?,?,?)", (row['record_uid'], row['id'], row['revision'],
                         json.dumps(snapshot, ensure_ascii=False), reason, int(time.time())))
    con.execute("INSERT INTO chapter_revisions_fts(rowid,title,spr,raw,tags) VALUES(?,?,?,?,?)",
                (cursor.lastrowid, row['title'] or '', row['spr'], row['raw'], row['tags_json']))


def forget_history(con, record_uid):
    rows = con.execute("SELECT id,snapshot_json FROM chapter_revisions WHERE record_uid=?", (record_uid,)).fetchall()
    for row in rows:
        old = json.loads(row['snapshot_json'])
        con.execute("INSERT INTO chapter_revisions_fts(chapter_revisions_fts,rowid,title,spr,raw,tags) "
                    "VALUES('delete',?,?,?,?,?)", (row['id'],old['title'] or '',old['spr'],old['raw'],old['tags_json']))
    con.execute("DELETE FROM chapter_revisions WHERE record_uid=?", (record_uid,))
    return len(rows)
