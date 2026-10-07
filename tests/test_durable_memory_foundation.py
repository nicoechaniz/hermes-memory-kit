"""Reproduced memory-loss regressions, exercised on fictional SQLite data."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import json
import sqlite3
import sys
import subprocess

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


def test_current_account_retains_searchable_history_and_links(mc):
    cid = mc.add_text('library', 'Relay account', 'We maintain the relay scheduler.')
    episode = mc.add_text('episodes', 'Mara encounter', 'Mara proposed a replay queue.')
    mc.add_link(episode, cid, 'concerns')
    uid = mc.expand(cid)['record_uid']
    assert mc.add_text('library', 'Relay account', 'We paused rollout pending calibration.') == cid
    assert mc.expand(cid)['revision'] == 2
    assert mc.expand(cid)['record_uid'] == uid
    assert mc.history(cid)[0]['raw'] == 'We maintain the relay scheduler.'
    assert mc.history_search('scheduler')[0]['record_uid'] == uid
    assert not mc.search('scheduler')  # present recall keeps historical claims separate
    assert mc.expand(episode)['neighbors'][0]['id'] == cid


def test_revision_conflict_does_not_change_current_history_or_index(mc):
    cid = mc.add_text('library', 'Relay', 'Original account')
    mc.update_chapter(cid, content='Updated with Mara', expected_revision=1)
    with pytest.raises(SystemExit, match='revision conflict'):
        mc.update_chapter(cid, content='Stale overwrite', expected_revision=1)
    assert mc.expand(cid)['raw'] == 'Updated with Mara'
    assert len(mc.history(cid)) == 1
    assert not mc.search('overwrite')
    assert mc.update_chapter(cid, content='Updated with Mara', expected_revision=2)['noop']
    assert len(mc.history(cid)) == 1


def test_provider_exposes_revision_conflicts_and_historical_recall(mc, provider_module):
    provider = provider_module.HMKMemoryProvider()
    provider.initialize(session_id='fictional-pilot')
    provider._memoryctl = mc
    added = json.loads(provider.handle_tool_call('librarian', {
        'action': 'add_text', 'shelf': 'episodes', 'title': 'Fictional meeting',
        'content': 'Mara proposed the relay.', 'metadata': {'mode': 'reported', 'source_event_id': 'fixture:meeting'}}))
    cid = added['chapter_id']
    updated = json.loads(provider.handle_tool_call('librarian', {
        'action': 'update', 'chapter_id': cid, 'content': 'Mara clarified the queue.', 'expected_revision': 1}))
    assert updated['revision'] == 2
    stale = json.loads(provider.handle_tool_call('librarian', {
        'action': 'update', 'chapter_id': cid, 'content': 'Stale claim', 'expected_revision': 1}))
    assert not stale['success']
    old = json.loads(provider.handle_tool_call('librarian', {'action': 'history_search', 'query': 'relay'}))
    assert old['items'][0]['historical']
    assert old['items'][0]['raw'] == 'Mara proposed the relay.'
    assert len(mc.history(cid)) == 1


def test_kind_date_and_attribution_survive_revision_and_unknown_date(mc):
    cid = mc.add_text('episodes', 'An encounter', 'Mara commented on the issue.',
                      event_ts=1200, actor='Mara', metadata={'mode':'reported','source_event_id':'fixture:issue:1',
                                                           'source_instance':'fixture:body:one','date_precision':'approximate'})
    first = mc.expand(cid)
    assert first['engram_type'] == 'episodic'
    assert first['origin']['source']['mode'] == 'reported'
    mc.update_chapter(cid, content='Mara clarified her proposal.', event_ts=None, expected_revision=1)
    assert mc.expand(cid)['event_ts'] is None
    assert mc.history(cid)[0]['event_ts'] == 1200
    assert mc.expand(cid)['actor'] == 'Mara'
    assert mc.expand(cid)['origin']['source']['source_instance'] == 'fixture:body:one'


def test_explicit_delete_also_removes_native_history(mc):
    cid = mc.add_text('library', 'An account', 'oldprivatemarker')
    mc.update_chapter(cid, content='newprivatemarker')
    assert mc.history_search('oldprivatemarker')
    result = mc.delete_chapter(cid)
    assert result['revisions_removed'] == 1
    assert mc.history(cid) == []
    assert mc.history_search('oldprivatemarker') == []


def test_source_metadata_cannot_impersonate_signed_origin(mc):
    with pytest.raises(ValueError, match='unsupported'):
        mc.add_text('library','Fake origin','No signed authority',metadata={'head_event_hash':'fictional'})
    assert not mc.search('authority')


def test_semantic_backfill_is_indexed_attributed_and_idempotent(mc, monkeypatch, tmp_path):
    source = mc.add_text('episodes', 'An encounter', 'Mara helped with a repair.')
    home = tmp_path / 'fixture-home'
    home.mkdir()
    fake = tmp_path / 'fake-hermes'
    fake.write_text(f"#!{sys.executable}\nprint('social | Fictional auditneedle participant helped with a repair.')\n")
    fake.chmod(0o700)
    monkeypatch.setenv('HMK_HERMES_HOME', str(home))
    monkeypatch.setenv('HMK_HERMES_BIN', str(fake))
    for _ in range(2):
        subprocess.run([sys.executable, str(SCRIPTS/'backfill-semantic.py'), '--shelf-pattern',
                        'episodes', '--limit','1','--sleep','0'], check=True, capture_output=True, text=True)
    results = mc.search('auditneedle')
    assert len(results) == 1
    assert results[0]['origin']['source']['mode'] == 'inferred'
    assert results[0]['origin']['source']['source_event_id'] == mc.expand(source)['record_uid']
    assert mc.expand(results[0]['id'])['revision'] == 1
    assert mc.expand(results[0]['id'])['neighbors'][0]['id'] == source
