"""Reproduced memory-loss regressions, exercised on fictional SQLite data."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sqlite3
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def mc(tmp_path, monkeypatch):
    base = tmp_path / "memory"
    base.mkdir()
    monkeypatch.setenv("HMK_AGENT_MEMORY_BASE", str(base))
    monkeypatch.setenv("HMK_DB_PATH", str(base / "library.db"))
    monkeypatch.syspath_prepend(str(SCRIPTS))
    module = load("durable_memory_fixture", SCRIPTS / "memoryctl.py")
    module.init_db()
    return module


def test_migration_snapshot_contains_committed_wal_and_restores(mc, monkeypatch):
    holder = mc.connect()
    holder.execute("PRAGMA wal_autocheckpoint=0")
    holder.execute("PRAGMA wal_checkpoint(TRUNCATE)")
    cid = mc.add_text("episodes", "An encounter", "Mara proposed a local replay queue.")
    migration = load("migration_fixture", SCRIPTS / "migrate-engram.py")
    assert migration.main() == 0
    snapshots = list(mc.DB_PATH.parent.glob("library.db.bak.preengram.*"))
    assert len(snapshots) == 1
    with sqlite3.connect(snapshots[0]) as restored:
        assert restored.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert restored.execute("SELECT raw FROM chapters WHERE id=?", (cid,)).fetchone()[0].startswith("Mara")
        assert restored.execute("SELECT rowid FROM chapters_fts WHERE chapters_fts MATCH 'replay'").fetchone()[0] == cid
    with mc.connect() as migrated:
        assert migrated.execute("SELECT engram_type,event_ts FROM chapters WHERE id=?", (cid,)).fetchone()[:] == ("episodic", None)
    assert migration.main() == 0
    assert len(list(mc.DB_PATH.parent.glob("library.db.bak.preengram.*"))) == 2
    holder.close()


def test_snapshot_never_overwrites_a_recovery_file(mc, tmp_path):
    snapshots = load("snapshot_fixture", SCRIPTS / "sqlite_snapshot.py")
    target = tmp_path / "retained.db"
    target.write_bytes(b"previous recovery evidence")
    with pytest.raises(FileExistsError):
        snapshots.verified_snapshot(mc.DB_PATH, target)
    assert target.read_bytes() == b"previous recovery evidence"


def test_skill_upgrade_preserves_acquired_files_and_edited_preimages(tmp_path):
    bootstrap = load("bootstrap_fixture", SCRIPTS / "bootstrap_agent.py")
    workspace = tmp_path / "workspace"
    bootstrap.bootstrap(workspace, "fixture", False)
    skills = workspace / "hermes-home/skills"
    learned = skills / "memory/learned-method/SKILL.md"
    learned.parent.mkdir()
    learned.write_text("A method learned with Mara.")
    shipped = skills / "memory/librarian/SKILL.md"
    shipped.write_text("Local evolution of the librarian.")
    bootstrap.upgrade(workspace)
    assert learned.read_text() == "A method learned with Mara."
    backups = list((workspace / "hermes-home/skill-backups").glob("*/memory/librarian/SKILL.md"))
    assert len(backups) == 1
    assert backups[0].read_text() == "Local evolution of the librarian."
    assert shipped.read_text() == (bootstrap.TEMPLATES / "skills/memory/librarian/SKILL.md").read_text()


@pytest.mark.parametrize("titles", [("李青", "王岚"), ("A/B", "A B"), ("Mara", "mara"), ("!!!", "???")])
def test_distinct_native_titles_do_not_replace_each_other(mc, titles):
    first = mc.add_text("library", titles[0], "firstpersonmarker encounter")
    second = mc.add_text("library", titles[1], "secondpersonmarker encounter")
    assert first != second
    assert mc.expand(first)["title"] == titles[0]
    assert mc.expand(second)["title"] == titles[1]
    assert [r["id"] for r in mc.search("firstpersonmarker")] == [first]


def test_legacy_ascii_slug_keeps_its_existing_book(mc):
    cid = mc.add_text("library", "李青", "Earlier encounter")
    with mc.connect() as con:
        con.execute("UPDATE books SET slug='item' WHERE id=(SELECT book_id FROM chapters WHERE id=?)", (cid,))
        con.commit()
    book_id = mc.expand(cid)["book_id"]
    current = mc.add_text("library", "李青", "Updated account")
    assert mc.expand(current)["book_id"] == book_id
