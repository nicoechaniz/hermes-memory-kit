"""Organization pilot mechanics on isolated fake memory; no model-quality claim."""
import importlib.util
import json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


@pytest.fixture
def setup(tmp_path,monkeypatch):
    base=tmp_path/'pool';base.mkdir()
    monkeypatch.setenv('HMK_AGENT_MEMORY_BASE',str(base));monkeypatch.setenv('HMK_DB_PATH',str(base/'library.db'))
    monkeypatch.syspath_prepend(str(ROOT/'scripts'));monkeypatch.syspath_prepend(str(ROOT/'research/agent-memory-2026-10-06/pilots'))
    mc=load(ROOT/'scripts/memoryctl.py','organization_memory_fixture');mc.init_db()
    mod=load(ROOT/'research/agent-memory-2026-10-06/pilots/durable_organization_pilot.py','organization_fixture')
    return mc,mod


def test_three_passes_replay_correction_and_topological_reconciliation(setup,tmp_path):
    mc,m=setup;original=mc.add_text('episodes','Reported trial','Human report received May 3: two people tested a relay prototype successfully.')
    old=[mc._read_chapter(original)];project=None;understanding=None
    for n in range(1,4):
        for phase,kind in [('project','semantic'),('understanding','procedural')]:
            support=original if phase=='project' else project
            target=project if phase=='project' else understanding
            current=mc._read_chapter(target) if target else None
            value=dict(manifest=m.consolidationctl.preview([support],mc,profile='native'),current_account=current)
            r=dict(key='account',operation='update' if current else 'add',title=phase,raw=f'Attributed {phase} pass {n}',engram_type=kind)
            if current:r.update(chapter_id=target,expected_revision=current['revision'])
            else:r['shelf']='library'
            p=dict(decision=dict(outcome='applied',reason='Source-based understanding',records=[r],links=[]),supports_by_record={'account':[support]})
            with pytest.raises(ValueError,match='inspection hash'):
                m.reviewed_apply(mc,value,p,tmp_path/'rejected',phase=phase,pass_number=n,reviewed_sha256='wrong')
            a=m.reviewed_apply(mc,value,p,tmp_path/f'{n}-{phase}',phase=phase,pass_number=n,reviewed_sha256=m.digest(p))
            target=a['account']['id']
            if phase=='project':project=target
            else:understanding=target
            assert a['rollback_verified'] and a['receipt']==a['replay']
    report=m.preservation(mc,old,[]);assert report['originals'][0]['status']=='unchanged'
    correction=dict(fictional=True,id='correction',source=dict(id='human-correction',channel='human_message',received_at='2026-10-05',originating_body='fixture:body:code',content='Earlier success report was too broad: some readings were lost.'))
    c=m.apply_correction(mc,original,correction,[project,understanding],tmp_path/'correction')
    assert len(c['stale_dependents'])==2 and c['original_raw_prefix_retained']
    assert m.preservation(mc,old,[])['originals'][0]['status']=='original_revision_preserved'
    for phase,target,support,kind in [('project',project,original,'semantic'),('understanding',understanding,project,'procedural')]:
        current=mc._read_chapter(target)
        value=dict(manifest=m.consolidationctl.preview([support],mc,profile='native'),current_account=current)
        p=dict(decision=dict(outcome='applied',reason='Reconciled later report',records=[dict(key='account',operation='update',chapter_id=target,expected_revision=current['revision'],title=phase,raw='The later human report corrects earlier success: readings were lost.',engram_type=kind)],links=[]),supports_by_record={'account':[support]})
        m.reviewed_apply(mc,value,p,tmp_path/f'reconciled-{phase}',phase=phase,pass_number=4,reviewed_sha256=m.digest(p))
    assert all(mc._read_chapter(cid)['support_status']=='current' for cid in [project,understanding])
    assert old[0]['raw'] in mc.history(original)[0]['raw']


def test_live_or_unqualified_pool_refused_before_memory_open(setup,tmp_path,monkeypatch):
    mc,m=setup;fixture=tmp_path/'fixture.json';fixture.write_text(json.dumps({'fictional':True,'cases':[]}));q=tmp_path/'grade.json';q.write_text('{}')
    with pytest.raises(ValueError,match='qualification required'):m.scoped_memory(tmp_path,fixture,q)
    q.write_text('{"fresh_formation_qualified":true}');(tmp_path/'conditions.json').write_text(json.dumps({'fixture_hash':m.digest(json.loads(fixture.read_text()))}))
    monkeypatch.setattr(m.pilot.configuration,'BASE_DIR',tmp_path)
    with pytest.raises(ValueError,match='live pool'):m.scoped_memory(tmp_path,fixture,q)
