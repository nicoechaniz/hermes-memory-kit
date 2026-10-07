"""Blind receiving transport preserves contexts/work and cannot dispatch a model."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def exchange(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    path=root/'research/agent-memory-2026-10-06/pilots/receiving_exchange.py'
    spec=importlib.util.spec_from_file_location('receiving_exchange_test',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def packet(module):
    source='Human report; source human-report; received 2026-06-15 through fixture:body:voice:\n'+json.dumps(
        'I met Leto. I do not know their surname.')
    binding={'being':'fixture:being:ash','receiving_body':'fixture:body:voice',
             'same_being_bodies':['fixture:body:voice']}
    packs=[{'items':[{'id':1,'spr':source,'origin':{'kind':'capture'}}]}]
    question='What was Leto\'s surname?'
    evidence=module.pilot.answer_evidence(packs,[])
    return dict(arm='proposed',answer_index=0,case_id='unknown-name',question=question,
        binding=binding,packs=packs,expanded=[],context_sha256=module.pilot.digest(evidence),
        context=module.narrative.supplied_context(question,evidence,binding))


def write_packets(module,path):
    path.mkdir();module.pilot.save(path/'packets.json',[packet(module)])
    module.pilot.save(path/'conditions.json',dict(fictional=True,qualification=False,
        packets_sha256=module.checksum(path/'packets.json')))


def response(module,out,request_path,content,**changes):
    request=json.loads(request_path.read_text());key=module.pilot.digest(request)
    value=dict(request_sha256=key,requested_model=request['model'],fresh_context=True,
        tool_calls_observed=[],dispatch_receipt='fixture:actual-test-dispatch',usage=None,
        response_model=None,content=json.dumps(content))
    value.update(changes);path=out/'responses'/(key+'.json');module.pilot.save(path,value)
    return path


def test_missing_response_only_prepares_blind_request_and_does_not_call_provider(exchange,tmp_path,monkeypatch):
    monkeypatch.setattr(exchange.pilot,'chat',lambda *a:pytest.fail('Unexpected inference call'))
    root=tmp_path/'packets';write_packets(exchange,root)
    out=tmp_path/'receiving'
    result=exchange.receive(root,out,'fixture-model')
    assert result['state']=='prepared' and result['model_requests_executed_by_this_process']==0
    request=json.loads(Path(result['request']).read_text())
    assert request['messages'][1]['content']==json.dumps(packet(exchange)['context'],ensure_ascii=False)
    assert request['tools_allowed'] is False and request['native_memory_allowed'] is False
    assert not (out/'trace.json').exists() and not (out/'answers.json').exists()
    assert request['fresh_context'] is True and request['external_dispatch_required'] is True
    # Preparation alone supplies no model-selection or semantic-acceptance proof.
    assert result['qualification'] is False


def test_external_narration_and_review_resume_without_source_database_or_rubric(exchange,tmp_path,monkeypatch):
    root=tmp_path/'packets';write_packets(exchange,root);out=tmp_path/'receiving'
    first=exchange.receive(root,out,'fixture-model')
    monkeypatch.setattr(exchange.pilot,'memory_at',lambda *a:pytest.fail('Receiver opened a database'))
    monkeypatch.setattr(exchange.pilot,'chat',lambda *a:pytest.fail('Receiver called inference'))
    text="The human's June 15, 2026 report gives no surname for Leto."
    candidate={'receiving_body':'fixture:body:voice','claims':[
        dict(text=text,support=[1],basis='memory',facet='limits')]}
    response(exchange,out,Path(first['request']),candidate)
    second=exchange.receive(root,out,'fixture-model',resume=True)
    request=json.loads(Path(second['request']).read_text());assert request['phase']=='narrative_review'
    trace=json.loads((out/'trace.json').read_text());assert len(trace)==1 and trace[0]['usage'] is None
    review={'missing':[],'claims':[dict(index=0,verdict='supported',reason='Human report retains unknown surname.',
        assertions=[dict(span=text,verdict='supported',reason='Preserves reported source and date.',proof=[
            {'id':1,'quote':'received 2026-06-15'},
            {'id':1,'quote':'I met Leto. I do not know their surname.'}])])]}
    response(exchange,out,Path(second['request']),review)
    result=exchange.receive(root,out,'fixture-model',resume=True)
    assert result['state']=='candidates_complete' and result['qualification'] is False
    assert result['independent_grading_required'] is True
    assert len(json.loads((out/'trace.json').read_text()))==2
    saved=json.loads((out/'answers.json').read_text())[0]
    assert saved['answer']['claims']==candidate['claims']
    assert saved['answer']['review_is_proof'] is False
    assert saved['narrative_attempts']['generations']==[candidate]
    assert not (out/'pending.json').exists()
    # Replaying the completed exchange is not another receiving execution.
    assert exchange.receive(root,out,'fixture-model',resume=True)==result
    assert len(json.loads((out/'trace.json').read_text()))==2


@pytest.mark.parametrize('changes', [
    {'request_sha256':'wrong'}, {'requested_model':'other'}, {'fresh_context':False},
    {'tool_calls_observed':['read source']}, {'dispatch_receipt':''},
    {'usage':{'total_tokens':0}}, {'usage':{'prompt_tokens':-1,'completion_tokens':1,'total_tokens':0}}])
def test_mismatched_or_contaminated_response_preserves_work_without_acceptance(exchange,tmp_path,changes):
    root=tmp_path/'packets';write_packets(exchange,root);out=tmp_path/'receiving'
    prepared=exchange.receive(root,out,'fixture-model');checkpoint=(out/'pending.json').read_bytes()
    path=response(exchange,out,Path(prepared['request']),{},**changes)
    with pytest.raises(ValueError):exchange.receive(root,out,'fixture-model',resume=True)
    assert path.exists() and (out/'pending.json').read_bytes()==checkpoint
    assert not (out/'answers.json').exists() and not (out/'trace.json').exists()


def test_durable_response_replay_is_one_observed_call_with_unknown_usage(exchange,tmp_path):
    out=tmp_path/'out';out.mkdir();transport=exchange.FileExchange(out,'xhigh')
    trace=exchange.pilot.Trace(out/'trace.json');trace.phase='narrative_generation'
    messages=[{'role':'system','content':'Fictional'},
              {'role':'user','content':json.dumps(packet(exchange)['context'])}]
    with pytest.raises(exchange.ResponsePending) as error:transport('fixture-model',messages,trace)
    response(exchange,out,Path(str(error.value)),{'broken':'candidate'})
    assert transport('fixture-model',messages,trace)=={'broken':'candidate'}
    assert transport('fixture-model',messages,trace)=={'broken':'candidate'}
    assert len(trace)==1 and trace[0]['usage'] is None


def test_changed_model_or_frozen_packet_cannot_reuse_pending_candidate(exchange,tmp_path):
    root=tmp_path/'packets';write_packets(exchange,root);out=tmp_path/'receiving'
    exchange.receive(root,out,'fixture-model');before=(out/'pending.json').read_bytes()
    with pytest.raises(ValueError,match='conditions changed'):
        exchange.receive(root,out,'other-model',resume=True)
    assert (out/'pending.json').read_bytes()==before
    data=json.loads((root/'packets.json').read_text());data[0]['question']='A changed question'
    exchange.pilot.save(root/'packets.json',data)
    with pytest.raises(ValueError,match='bytes changed'):
        exchange.receive(root,out,'fixture-model',resume=True)
    assert (out/'pending.json').read_bytes()==before


def test_canonical_check_preserves_corrections_but_allows_only_retrieval_usage(exchange,tmp_path):
    memory=exchange.pilot.memory_at(tmp_path/'memory')
    cid=memory.add_text('episodes','Encounter','Original source.')
    original=exchange.canon(memory.DB_PATH)
    memory.expand(cid)
    assert exchange.canon(memory.DB_PATH)==original
    memory.update_chapter(cid,content='Original plus correction.')
    revised=exchange.canon(memory.DB_PATH)
    assert revised!=original and 'chapter_revisions' in revised
    with memory.connect() as con:
        con.execute('UPDATE chapters SET updated_at=updated_at+1 WHERE id=?',(cid,));con.commit()
    assert exchange.canon(memory.DB_PATH)!=revised


@pytest.mark.parametrize('warm',[False,True])
def test_packet_freeze_preserves_pre_recall_history_and_hides_rubric(exchange,tmp_path,monkeypatch,warm):
    source=tmp_path/'source';source.mkdir();output=tmp_path/'packets'
    corpus={'fictional':True,'fixture_context':{'being':'fixture:being:ash',
        'same_being_bodies':['fixture:body:voice']},'cases':[{'id':'event',
        'questions':[{'query':'Who proposed labels?'}],
        'expected':{'secret':'RUBRIC_MUST_NEVER_ENTER_RECEIVING_PACKETS'}}]}
    corpus_path=tmp_path/'corpus.json';exchange.pilot.save(corpus_path,corpus)
    exchange.pilot.save(source/'conditions.json',dict(fixture_hash=exchange.pilot.digest(corpus),
        retrieval_sha256=exchange.checksum(Path(exchange.pilot.configuration.__file__))))
    exchange.pilot.save(source/'results.json',[{'variant':arm,'retrieval_clock':2106956370}
        for arm in ('baseline','proposed')])
    original_memory_at=exchange.pilot.memory_at
    snapshots={}
    for arm in ('baseline','proposed'):
        pool=source/arm/'memory';pool.mkdir(parents=True)
        memory=original_memory_at(pool);cid=memory.add_text('episodes','Tavi labels',
            'Human report; source meeting; received 2026-06-15 through fixture:body:voice:\n'+json.dumps('Tavi proposed labels.'))
        memory.update_chapter(cid,content=memory._read_chapter(cid)['raw']+'\nNo handle was supplied.')
        exchange.pilot.CaptureLedger(memory)  # Empty original ledgers must be absent from the receiver.
        if warm:memory.expand(cid)
        snapshots[arm]=exchange.canon(memory.DB_PATH)
        exchange.pilot.save(source/arm/'answers.json',[dict(case_id='event',question='Who proposed labels?',
            plan_attempts=[{'queries':[],'expand_ids':[cid]}])])
    def isolated(pool):
        memory=original_memory_at(pool)
        def pack(query,**kwargs):
            assert memory.now_ts()==2106956370
            return dict(query=query,null_retrieval=False,retrieval_status='ok',
                items=[memory._compact_record(memory._read_chapter(1))])
        memory.hybrid_pack=pack
        return memory
    monkeypatch.setattr(exchange.pilot,'memory_at',isolated)
    monkeypatch.setattr(exchange.pilot.configuration,'BASE_DIR',None)
    if warm:
        with pytest.raises(ValueError,match='unqueried pre-recall'):exchange.freeze(source,corpus_path,output)
        return
    exchange.freeze(source,corpus_path,output)
    text=(output/'packets.json').read_text()
    assert 'RUBRIC_MUST_NEVER_ENTER_RECEIVING_PACKETS' not in text
    assert len(json.loads(text))==2
    for arm in ('baseline','proposed'):
        assert exchange.canon(source/arm/'memory/library.db')==snapshots[arm]
        assert exchange.canon(output/arm/'receiver/library.db')==snapshots[arm]
        with exchange.sqlite3.connect(output/arm/'receiver/library.db') as con:
            tables={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert not tables & {'capture_events','capture_streams'}
    assert json.loads((output/'conditions.json').read_text())['model_requests_executed']==0
