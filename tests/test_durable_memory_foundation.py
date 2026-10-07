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


def test_bootstrap_cannot_replace_an_existing_canon(mc):
    cid = mc.add_text('episodes', 'Retained encounter', 'Mara shared an irreplaceable moment.')
    mc.update_chapter(cid, content='Mara shared an irreplaceable moment and a later correction.')
    with pytest.raises(SystemExit, match='new database'):
        mc.bootstrap()
    assert mc.expand(cid)['revision'] == 2
    assert mc.history(cid)[0]['raw'] == 'Mara shared an irreplaceable moment.'
    assert mc.search('irreplaceable')[0]['id'] == cid


def test_projection_preserves_open_relation_names_and_escapes_yaml(mc):
    projection = load('durable_projection_fixture', SCRIPTS / 'export_obsidian.py')
    chapter = dict(id=1, book_id=1, shelf='episodes', tags=[], source_path=None,
                   links_out=[dict(link_type='concerns', other_id=2, other_title='Relay'),
                              dict(link_type='place: "north"', other_id=3, other_title='Canal')])
    text = projection.render_frontmatter(chapter, dict(title='Encounter',folder='episodes'), {})
    import yaml
    metadata = yaml.safe_load(text.split('---')[1])
    assert metadata['memory_links']['concerns'] == ['`mem:2` Relay']
    assert metadata['memory_links']['place: "north"'] == ['`mem:3` Canal']


def test_decision_schema_requires_no_pool_and_matches_writer_fields(tmp_path):
    import os
    env = dict(os.environ)
    for key in ('HMK_AGENT_MEMORY_BASE','HMK_DB_PATH','AGENT_MEMORY_BASE','HMK_BASE_DIR'):
        env.pop(key, None)
    result = subprocess.run([sys.executable, str(SCRIPTS/'capturectl.py'), 'decision-schema'],
                            cwd=tmp_path, env=env, capture_output=True, text=True, check=True)
    schema = json.loads(result.stdout)
    fields = schema['properties']['records']['items']['properties']
    assert fields['metadata']['properties']['reported_at']['type'] == 'integer'
    assert 'location' in fields and 'location_json' not in fields
    assert list(tmp_path.iterdir()) == []


def test_invalid_selected_link_preserves_pending_source_and_rolls_back(mc):
    capture = load('invalid_link_fixture', SCRIPTS/'capturectl.py')
    ledger = capture.CaptureLedger(mc)
    event = dict(stream_id='fixture:links', sequence=1, event_id='comment', source_version='1',
                 content='Mara proposed a replay queue.', metadata={'mode':'reported'})
    key = ledger.stage(event)['event_key']
    decision = dict(outcome='applied', reason='Lasting collaboration', selection_version='fixture:v1',
                    records=[dict(key='episode',operation='add',shelf='episodes',title='Mara proposal',raw=event['content'])],
                    links=[dict(source='episode',target='1',link_type='concerns')])
    with pytest.raises(ValueError, match='integer chapter ID'):
        ledger.assess(key,decision)
    assert not mc.search('Mara')
    assert ledger.pending(event['stream_id'])[0]['event']['content'] == event['content']
    assert ledger.pending(event['stream_id'])[0]['processed_through'] == 0


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


def test_full_unicode_question_reaches_late_name_and_raw_cue(mc):
    cid = mc.add_text('episodes', 'A significant proposal', 'Context.\n' * 150 + 'Nicolás Echániz proposed a HarborMesh replay queue.')
    question = 'Do you remember the person who once suggested something for HarborMesh, Nicolás Echániz?'
    assert 'harbormesh' in mc.tokenize_query(question)
    assert 'nicolás' in mc.tokenize_query(question)
    assert mc.search(question)[0]['id'] == cid
    assert mc.text_overlap_score('HarborMesh', mc.expand(cid)) == 1
    assert mc.pack(question, threshold=0.6, budget_tokens=1500)['items'][0]['id'] == cid
    assert mc.search('"***') == []


def test_distinct_episodes_survive_common_openings_and_age(mc, monkeypatch):
    ids = [mc.add_text('episodes', 'A meeting about our common relay project discussion ' + name,
                       'A meeting about our common relay project discussion ' + name + ' proposed ' + idea, importance=0.9)
           for name, idea in [('Mara', 'a queue'), ('Ivo', 'a checksum')]]
    clock = mc.now_ts()
    monkeypatch.setattr(mc, 'now_ts', lambda: clock + 10 * 365 * 86400)
    result = mc.pack('relay project discussion', threshold=0.6, budget_tokens=1500)
    assert {item['id'] for item in result['items']} == set(ids)
    assert result['used_tokens_estimate'] <= 1500
    assert all(item['event_ts'] is None for item in result['items'])


def test_general_priors_are_neutral_and_research_prefix_must_be_nonempty(mc, monkeypatch):
    monkeypatch.setenv('HMK_RETRIEVAL_PROFILE', 'general')
    monkeypatch.setattr(mc, 'BIBLIOTECA_PREFIX', '/fixture/papers/')
    assert mc.source_domain_prior('coupling', {'shelf': 'episodes', 'source_path': ''}) == 0
    assert mc.source_domain_prior('coupling', {'shelf': 'evidence', 'source_path': '/fixture/papers/a'}) == 0
    monkeypatch.setenv('HMK_RETRIEVAL_PROFILE', 'research')
    assert mc.source_domain_prior('coupling', {'shelf': 'evidence', 'source_path': '/fixture/papers/a'}) == 0.14
    monkeypatch.setattr(mc, 'BIBLIOTECA_PREFIX', '')
    assert mc.source_domain_prior('coupling', {'shelf': 'library', 'source_path': '/fixture/papers/a'}) == 0


def test_project_can_recover_attributed_incoming_episode(mc):
    project = mc.add_text('library', 'HarborMesh', 'We maintain the scheduler.')
    episode = mc.add_text('episodes', 'Mara encounter', 'Mara proposed replay.',
                         metadata={'mode': 'reported', 'source_event_id': 'fixture:issue:7'})
    mc.add_link(episode, project, 'concerns', note='Proposal for this project')
    neighbor = mc.expand(project)['neighbors'][0]
    assert neighbor['id'] == episode
    assert neighbor['direction'] == 'incoming'
    assert neighbor['note'] == 'Proposal for this project'
    assert neighbor['origin']['source']['source_event_id'] == 'fixture:issue:7'


def test_hybrid_outage_uses_lexical_without_provider_substitution(mc, monkeypatch):
    cid = mc.add_text('episodes', 'HarborMesh proposal', 'Mara proposed replay.', importance=0.8,
                      metadata={'mode': 'reported', 'source_instance': 'fixture:body'})
    def unavailable(*args, **kwargs):
        raise mc.EmbeddingBackendError('synthetic outage')
    monkeypatch.setattr(mc, 'semantic_search', unavailable)
    result = mc.hybrid_pack('HarborMesh', provider='nvidia', model='fixture-model')
    assert result['items'][0]['id'] == cid
    assert result['items'][0]['origin']['source']['source_instance'] == 'fixture:body'
    assert result['retrieval_status'] == 'degraded'
    assert result['provider'] == 'nvidia' and result['model'] == 'fixture-model'
    absent = mc.hybrid_pack('absentneedle')
    assert absent['null_retrieval'] and absent['reason'] == 'backend_unavailable'
    assert absent['retrieval_status'] == 'unavailable'
    def broken(*args, **kwargs):
        raise sqlite3.DatabaseError('synthetic schema fault')
    monkeypatch.setattr(mc, 'semantic_search', broken)
    with pytest.raises(sqlite3.DatabaseError):
        mc.engram_pack('HarborMesh')


def test_threshold_applies_to_every_item_and_budget_includes_origin(mc, monkeypatch):
    first = mc.add_text('episodes', 'First', 'Relevant marker', metadata={'evidence': ['fixture:' + 'x' * 800]})
    second = mc.add_text('episodes', 'Second', 'Unrelated marker')
    rows = [dict(mc.expand(first), score=0.95), dict(mc.expand(second), score=0.01)]
    monkeypatch.setattr(mc, 'search', lambda *args, **kwargs: rows)
    result = mc.pack('marker', threshold=0.5, budget_tokens=1500)
    assert [item['id'] for item in result['items']] == [first]
    assert result['used_tokens_estimate'] == sum(mc._item_cost(item) for item in result['items'])
    exhausted = mc.pack('marker', threshold=0.5, budget_tokens=0)
    assert exhausted['null_retrieval'] and exhausted['reason'] == 'budget_exhausted'


def test_engram_relevance_precedes_quota_and_rrf(mc, monkeypatch):
    cid = mc.add_text('episodes', 'Proposal', 'Mara proposed replay.')
    item = dict(mc.expand(cid), score=0.001)
    monkeypatch.setattr(mc, 'hybrid_pack', lambda *args, **kwargs: {'items': [item], 'retrieval_status': 'ok'})
    assert mc.engram_pack('unrelated', threshold=0.3)['null_retrieval']
    item['score'] = 0.9
    relevant = mc.engram_pack('proposal', threshold=0.3, quotas={})
    assert relevant['items'][0]['id'] == cid
    assert relevant['items'][0]['score'] == 0.9
    assert relevant['items'][0]['rrf_score'] < 0.3  # ordering and relevance are different spaces


def test_weak_rerank_is_not_normalized_to_perfect_relevance(mc, monkeypatch):
    cid = mc.add_text('episodes', 'A proposal', 'A marginally related marker.')
    row = mc.expand(cid)
    monkeypatch.setattr(mc, 'search', lambda *args, **kwargs: [])
    monkeypatch.setattr(mc, 'semantic_search', lambda *args, **kwargs: [dict(row, semantic_score=0.001)])
    monkeypatch.setattr(mc, 'rerank_provider_default', lambda: 'flashrank')
    monkeypatch.setattr(mc, 'flashrank_rerank', lambda *args, **kwargs: [{'id': str(cid), 'score': 0.001}])
    assert mc.hybrid_pack('Unrelated question', threshold=0.3)['null_retrieval']


def test_semantic_and_provider_keep_attribution_and_full_preview(mc, monkeypatch, provider_module):
    cid = mc.add_text('episodes', 'An account', 'A prefix ' + 'context ' * 30 + 'Mara proposed a relay.',
                      metadata={'mode': 'inferred', 'source_instance': 'fixture:body', 'source_event_id': 'fixture:event'})
    monkeypatch.setattr(mc, 'embed_texts', lambda *args, **kwargs: [[1.0, 0.0]])
    con = mc.connect()
    mc.upsert_embedding(con, cid, 'local', 'fixture-model', mc.embed_input_text(mc.expand(cid)), [1.0, 0.0])
    con.commit()
    con.close()
    row = mc.semantic_search('relay', provider='local', model='fixture-model')[0]
    assert row['origin']['source']['mode'] == 'inferred'
    result = mc.hybrid_pack('relay', provider='local', model='fixture-model', budget_tokens=1500)
    rendered = provider_module.HMKMemoryProvider()._render_items(result['items'])
    assert 'fixture:body' in rendered
    assert 'inferred' in rendered
    # Preview currently exposes the selected SPR, not an additional 140-character cut.
    assert result['items'][0]['spr'].replace('\n', ' ') in rendered
    assert 'Mara proposed a relay.' in rendered


def test_authored_summary_survives_metadata_updates_and_refreshes_vectors(mc):
    cid = mc.add_text('episodes', 'Long source', 'Context.\n' * 300 + 'Mara proposed replay.',
                      summary='Mara proposed a replay queue for HarborMesh; this is reported, outcome unknown.')
    assert 'Mara' in mc.expand(cid)['spr']
    con = mc.connect()
    mc.upsert_embedding(con, cid, 'local', 'fixture-model', mc.embed_input_text(mc.expand(cid)), [1.0])
    con.commit()
    con.close()
    mc.update_chapter(cid, metadata={'mode': 'reported'})
    assert 'Mara' in mc.expand(cid)['spr']
    changed = mc.update_chapter(cid, summary='Mara clarified that replay is a proposal, not an implemented feature.')
    assert changed['embeddings_dropped'] == 1
    assert 'outcome unknown' in mc.history(cid)[-1]['spr']


def test_native_upgrade_snapshot_precedes_ddl_and_recovers_legacy_record(mc):
    cid = mc.add_text('episodes', 'Legacy encounter', 'Mara proposed replay.')
    con = mc.connect()
    con.execute('DROP INDEX idx_chapters_record_uid')
    for column in ('record_uid', 'revision', 'source_metadata_json'):
        con.execute('ALTER TABLE chapters DROP COLUMN ' + column)
    con.execute('DROP TABLE chapter_revisions')
    con.execute('DROP TABLE chapter_revisions_fts')
    con.commit()
    con.close()
    mc.init_db()
    snapshots = list(mc.BASE_DIR.glob('library.db.bak.preupgrade.*'))
    assert len(snapshots) == 1
    con = sqlite3.connect(snapshots[0])
    assert 'record_uid' not in {row[1] for row in con.execute('PRAGMA table_info(chapters)')}
    assert con.execute('SELECT raw FROM chapters WHERE id=?', (cid,)).fetchone()[0] == 'Mara proposed replay.'
    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    con.close()
    assert mc.expand(cid)['record_uid']


def event(sequence=1, content='Mara proposed a replay queue.', version='1'):
    return {'stream_id': 'fixture:issue', 'sequence': sequence, 'event_id': f'comment:{sequence}',
            'source_version': version, 'content': content,
            'metadata': {'mode': 'reported', 'source_instance': 'fixture:body'}}


def selection(title='Mara encounter'):
    return {'outcome': 'applied', 'reason': 'Significant proposal in our own project',
            'selection_version': 'fixture:policy:v1', 'records': [
                {'key': 'episode', 'operation': 'add', 'shelf': 'episodes', 'title': title,
                 'raw': 'Mara proposed a replay queue for HarborMesh in an issue; it may enable offline work. Outcome unknown.',
                 'importance': 0.9}]}


def test_capture_survives_source_loss_and_replay_without_duplicate_events(mc):
    from capturectl import CaptureLedger
    ledger = CaptureLedger(mc)
    staged = ledger.stage(event())
    assert staged['state'] == 'pending' and staged['processed_through'] == 0
    # A fresh reader gets durable pending source text without the original session.
    restored = CaptureLedger(mc)
    assert restored.pending('fixture:issue')[0]['event']['content'] == event()['content']
    decision = selection()
    receipt = restored.assess(staged['event_key'], decision)
    assert receipt['processed_through'] == 1 and receipt['state'] == 'applied'
    assert receipt['records']['episode']['embedding_status'] == 'pending'
    assert receipt['records']['episode']['lexical_ready']
    assert receipt == restored.assess(staged['event_key'], decision)
    assert receipt == restored.stage(event())
    assert restored.pending('fixture:issue') == []
    assert len(mc.search('HarborMesh')) == 1
    assert mc.history(receipt['records']['episode']['chapter_id']) == []


def test_capture_does_not_skip_missing_deferred_failed_events_or_retain_noise(mc):
    from capturectl import CaptureLedger
    ledger = CaptureLedger(mc)
    later = ledger.stage(event(2))
    assert ledger.assess(later['event_key'], selection())['processed_through'] == 0
    first = ledger.stage(event(1, 'Working status'))
    omitted = {'outcome': 'omitted', 'reason': 'mechanical-status', 'selection_version': 'fixture:policy:v1'}
    assert ledger.assess(first['event_key'], omitted)['processed_through'] == 2
    con = mc.connect()
    assert con.execute('SELECT payload_json FROM capture_events WHERE event_key=?', (first['event_key'],)).fetchone()[0] is None
    con.close()
    third = ledger.stage(event(3))
    assert ledger.assess(third['event_key'], dict(omitted, outcome='deferred'))['processed_through'] == 2
    with pytest.raises(ValueError, match='different content'):
        ledger.stage(event(3, 'Different source under reused version'))
    assert len(ledger.pending('fixture:issue')) == 1


@pytest.mark.parametrize('boundary', ['before_commit','after_commit'])
def test_capture_failure_boundaries_are_atomic_and_replayable(mc, boundary):
    from capturectl import CaptureLedger
    ledger = CaptureLedger(mc)
    key = ledger.stage(event())['event_key']
    def crash(point):
        if point == boundary:
            raise RuntimeError('synthetic interruption')
    with pytest.raises(RuntimeError):
        ledger.assess(key, selection(), _fault_hook=crash)
    assert bool(mc.search('HarborMesh')) == (boundary == 'after_commit')
    receipt = CaptureLedger(mc).assess(key, selection())
    assert receipt['processed_through'] == 1
    assert len(mc.search('HarborMesh')) == 1


def test_capture_batch_rolls_back_prior_writes_on_stale_update(mc):
    from capturectl import CaptureLedger
    target = mc.add_text('library', 'HarborMesh', 'Current account')
    mc.update_chapter(target, content='Fresh account')
    ledger = CaptureLedger(mc)
    key = ledger.stage(event())['event_key']
    decision = selection()
    decision['records'].append({'key':'account', 'operation':'update', 'chapter_id':target,
                                'expected_revision':1, 'raw':'Stale account'})
    with pytest.raises(SystemExit, match='revision conflict'):
        ledger.assess(key, decision)
    assert not mc.search('Mara')
    assert mc.expand(target)['raw'] == 'Fresh account'
    assert len(mc.history(target)) == 1
    assert ledger.pending('fixture:issue')[0]['state'] == 'failed'
    assert ledger.pending('fixture:issue')[0]['processed_through'] == 0
    decision['records'][-1]['expected_revision'] = 2
    assert ledger.assess(key, decision)['state'] == 'applied'


def test_consolidation_preserves_full_sources_and_original_encounters(mc):
    from consolidationctl import preview, apply
    first = mc.add_text('episodes', 'First encounter', 'Context.\n' * 100 + 'Mara proposed replay for HarborMesh.', metadata={'mode':'reported'})
    second = mc.add_text('episodes', 'Second encounter', 'Ivo tested recovery and identified duplicate writes.')
    original = {cid: mc.expand(cid)['raw'] for cid in (first,second)}
    manifest = preview([first,second], mc)
    assert 'Mara proposed' in manifest['supports'][0]['raw']
    decision = {'outcome':'applied', 'reason':'Proposed supported lesson', 'records':[
        {'operation':'add','key':'lesson','shelf':'library','title':'HarborMesh recovery lesson',
         'raw':'The HarborMesh encounters suggest that replay should be idempotent; this is an inferred lesson.'}]}
    options = {'stream_id':'fixture:dream','sequence':1,'event_id':'dream:1','selection_version':'fixture:policy:v1','memory':mc}
    receipt = apply(manifest, decision, **options)
    assert receipt == apply(manifest, decision, **options)
    lesson = receipt['records']['lesson']['chapter_id']
    assert mc.expand(lesson)['origin']['source']['mode'] == 'inferred'
    assert len(mc.expand(lesson)['origin']['source']['evidence']) == 2
    assert {row['id'] for row in mc.expand(lesson)['neighbors']} == {first,second}
    assert {cid: mc.expand(cid)['raw'] for cid in original} == original
    assert all(mc.expand(cid)['revision'] == 1 for cid in original)
    assert mc.expand(lesson)['support_status'] == 'current'
    mc.update_chapter(first, content='Mara withdrew the replay proposal.')
    assert mc.pack('recovery lesson', threshold=0, budget_tokens=1500)['items'][0]['support_status'] == 'needs_reconciliation'
    assert mc.expand(lesson)['support_checks'][0]['status'] == 'changed'
    mc.delete_chapter(first)
    assert mc.expand(lesson)['support_checks'][0]['status'] == 'missing'


def test_consolidation_rejects_stale_sources_and_episode_overwrites(mc):
    from consolidationctl import preview, apply
    cid = mc.add_text('episodes', 'Mara encounter', 'Mara proposed a queue.')
    manifest = preview([cid], mc)
    mc.update_chapter(cid, content='Mara corrected the proposal.')
    decision = {'outcome':'applied','reason':'Lesson','records':[{
        'operation':'add','key':'lesson','shelf':'library','title':'A lesson','raw':'This is an inferred lesson.'}]}
    options = {'stream_id':'fixture:dream','sequence':1,'event_id':'dream:1','selection_version':'fixture:policy:v1','memory':mc}
    with pytest.raises(ValueError, match='support changed'):
        apply(manifest, decision, **options)
    assert not mc.search('lesson')
    decision['records'][0] = {'operation':'update','key':'lesson','chapter_id':cid,'expected_revision':2,'raw':'Overwrite original episode'}
    with pytest.raises(ValueError, match='cannot overwrite'):
        apply(preview([cid],mc), decision, **dict(options, sequence=2, event_id='dream:2'))
    assert mc.expand(cid)['raw'] == 'Mara corrected the proposal.'


def test_late_capture_correction_preserves_attribution_and_history(mc):
    from capturectl import CaptureLedger
    ledger = CaptureLedger(mc)
    first = ledger.stage(event())
    initial = ledger.assess(first['event_key'], selection())
    cid = initial['records']['episode']['chapter_id']
    corrected = event(2, 'The proposer was Ivo, not Mara.', version='2')
    corrected['event_id'] = event()['event_id']
    key = ledger.stage(corrected)['event_key']
    decision = {'outcome':'applied','reason':'Reported attribution correction', 'selection_version':'fixture:policy:v1', 'records':[
        {'key':'episode','operation':'update','chapter_id':cid,'expected_revision':1,
         'raw':'Ivo (@ivo-test) proposed replay for HarborMesh; Mara was an earlier, superseded attribution.',
         'metadata':{'correction_of':event()['event_id']}}]}
    ledger.assess(key, decision)
    assert mc.expand(cid)['origin']['source']['source_version'] == '2'
    assert 'Mara proposed' in mc.history(cid)[0]['raw']
    assert mc.expand(cid)['origin']['source']['mode'] == 'reported'


def test_capture_keeps_embedding_failure_separate_from_persistence(mc, monkeypatch):
    from capturectl import CaptureLedger
    ledger = CaptureLedger(mc)
    key = ledger.stage(event())['event_key']
    monkeypatch.setattr(mc, 'embeddings_runtime_config', lambda *args, **kwargs: (_ for _ in ()).throw(ValueError('synthetic config error')))
    receipt = ledger.assess(key, selection())
    assert receipt['records']['episode']['embedding_status'] == 'configuration_unavailable'
    assert receipt['records']['episode']['lexical_ready']
    assert mc.search('HarborMesh')


def test_finite_capture_cli_persists_across_processes_without_a_listener(mc, tmp_path):
    source = tmp_path / 'event.json'
    source.write_text(json.dumps(event()))
    decision = tmp_path / 'selection.json'
    decision.write_text(json.dumps(selection()))
    def command(*args):
        result = subprocess.run([sys.executable, str(SCRIPTS / 'capturectl.py'), *args], check=True,
                                capture_output=True, text=True, timeout=10)
        return json.loads(result.stdout)
    key = command('stage', '--file', str(source))['event_key']
    source.unlink()  # source/session loss before curation resumes
    assert command('pending', '--stream', 'fixture:issue')[0]['event']['content']
    receipt = command('assess', '--event-key', key, '--file', str(decision))
    assert receipt['state'] == 'applied'
    assert command('pending', '--stream', 'fixture:issue') == []
    assert mc.search('HarborMesh')


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


def test_summary_and_title_follow_embedding_eligibility_policy(mc, monkeypatch):
    monkeypatch.setattr(mc, 'scan_content_for_secrets', lambda text: 'synthetic-secret' if 'fixture-secret' in text else None)
    cid = mc.add_text('episodes','An account','Ordinary text',summary='fixture-secret')
    assert mc.expand(cid)['embed_disabled'] == 1
    cid = mc.add_text('episodes','Another account','Ordinary text')
    mc.update_chapter(cid, summary='fixture-secret')
    assert mc.expand(cid)['embed_disabled'] == 1
    cid = mc.add_text('episodes','fixture-secret','Ordinary text')
    assert mc.expand(cid)['embed_disabled'] == 1
