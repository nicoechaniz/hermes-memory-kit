"""Finite isolated batch work must retain phase state and observe each future."""
import importlib.util
import json
from pathlib import Path
import pytest


@pytest.fixture
def batch(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec=importlib.util.spec_from_file_location('receiving_batch_test',root/'research/agent-memory-2026-10-06/pilots/receiving_batch.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def packets(module,root,count=1):
    root.mkdir();body=dict(receiving_body='fixture:body:voice',same_being_bodies=['fixture:body:voice'])
    rows=[]
    for i in range(count):
        question=f'What happened in unrecorded encounter {i}?'
        rows.append(dict(arm='proposed',answer_index=i,case_id='unknown',question=question,
            binding=body,packs=[],expanded=[],context_sha256=str(i),
            context=module.api.exchange.narrative.supplied_context(question,{},body)))
    module.api.exchange.pilot.save(root/'packets.json',rows)
    module.api.exchange.pilot.save(root/'conditions.json',dict(fictional=True,
        packets_sha256=module.api.exchange.checksum(root/'packets.json')))


def successful_dispatch(module,calls):
    def dispatch(path,root,key,provider):
        request=json.loads(path.read_text());calls.append(request['phase'])
        if request['phase']=='narrative_generation':
            value=dict(receiving_body='fixture:body:voice',claims=[dict(
                text='The supplied memories do not record that encounter.',support=[],basis='unknown',facet='limits')])
        else:
            candidate=json.loads(request['messages'][1]['content'])['candidate']
            value=dict(missing=[],claims=[dict(index=0,verdict='supported',reason='Packet-scoped absence.',
                assertions=[dict(span=candidate['claims'][0]['text'],verdict='supported',reason='Absent from packet.',proof=[])])])
        receipt=root/'dispatches'/path.name;receipt.parent.mkdir(exist_ok=True);module.api.exchange.pilot.save(receipt,dict(state='completed',request_sha256=path.stem,parameters=module.api.parameters(request,'deepseek'),content=json.dumps(value)))
        module.api.exchange.pilot.save(root/'responses'/path.name,dict(
            request_sha256=path.stem,requested_model=request['model'],fresh_context=True,
            tool_calls_observed=[],dispatch_receipt=str(receipt),usage=None,content=json.dumps(value)))
        return receipt
    return dispatch


def test_budget_resumes_saved_generation_without_repeating_or_resetting(batch,tmp_path):
    source=tmp_path/'packets';out=tmp_path/'out';packets(batch,source);calls=[]
    dispatch=successful_dispatch(batch,calls)
    first=batch.run(source,out,api_key='fixture',max_calls=1,dispatcher=dispatch)
    assert first['completed_candidates']==0 and first['results'][0]['state']=='pending_budget'
    saved=json.loads((out/'proposed/0/pending.json').read_text())
    assert saved['narrative']['progress']['phase']=='review' and len(saved['narrative']['generations'])==1
    second=batch.run(source,out,api_key='fixture',max_calls=1,dispatcher=dispatch)
    assert second['completed_candidates']==1 and calls==['narrative_generation','narrative_review']
    third=batch.run(source,out,api_key='fixture',max_calls=1,dispatcher=dispatch)
    assert third['new_dispatch_attempts']==0 and calls==['narrative_generation','narrative_review']
    original=(out/'answers.json').read_bytes()
    with pytest.raises(ValueError,match='procedure changed'):
        batch.run(source,out,api_key='fixture',review_effort='high',dispatcher=dispatch)
    assert (out/'answers.json').read_bytes()==original


def test_every_failed_future_and_unresolved_dispatch_stays_observed(batch,tmp_path):
    source=tmp_path/'packets';out=tmp_path/'out';packets(batch,source,3);calls=[]
    def failing(path,root,*args):
        calls.append(path.stem);(root/'dispatches').mkdir(exist_ok=True);batch.api.exchange.pilot.save(root/'dispatches'/path.name,dict(state='failed',usage=None))
        raise TimeoutError('Provider unavailable')
    first=batch.run(source,out,api_key='fixture',max_calls=3,dispatcher=failing)
    assert len(calls)==3 and len(first['results'])==3
    assert all(r['state']=='failed' and r['error_type']=='TimeoutError' for r in first['results'])
    second=batch.run(source,out,api_key='fixture',max_calls=3,dispatcher=failing)
    assert len(calls)==3 and second['new_dispatch_attempts']==0
    assert all(r['state']=='failed' and r['error_type']=='RuntimeError' for r in second['results'])
    assert all((out/'proposed'/str(i)/'pending.json').exists() for i in range(3))


def test_changed_packets_do_not_mutate_comparison(batch,tmp_path):
    source=tmp_path/'packets';out=tmp_path/'out';packets(batch,source)
    batch.run(source,out,api_key='fixture',max_calls=0)
    original=(out/'conditions.json').read_bytes();(source/'packets.json').write_text('[]')
    with pytest.raises(ValueError,match='unchanged explicitly fictional'):
        batch.run(source,out,api_key='fixture',max_calls=0)
    assert (out/'conditions.json').read_bytes()==original


def test_generation_reuse_needs_the_actual_identical_payload_and_receipt(batch,tmp_path):
    source=tmp_path/'packets';first=tmp_path/'first';packets(batch,source);calls=[]
    dispatch=successful_dispatch(batch,calls)
    batch.run(source,first,api_key='fixture',max_calls=1,dispatcher=dispatch)
    second=batch.run(source,tmp_path/'second',api_key='fixture',max_calls=1,review_effort='none',
        generation_references=[first/'proposed/0'],dispatcher=dispatch)
    assert second['completed_candidates']==1 and second['new_dispatch_attempts']==1
    assert calls==['narrative_generation','narrative_review']
    imported=json.loads(next((tmp_path/'second/proposed/0').glob('imported-*.json')).read_text())
    assert imported['additional_inference_calls']==0
    receipt=next((first/'proposed/0/dispatches').glob('*.json'))
    value=json.loads(receipt.read_text());value['content']='tampered observed response'
    batch.api.exchange.pilot.save(receipt,value)
    third=batch.run(source,tmp_path/'third',api_key='fixture',max_calls=1,
        generation_references=[first/'proposed/0'],dispatcher=dispatch)
    assert third['results'][0]['state']=='failed' and third['new_dispatch_attempts']==0
    assert calls==['narrative_generation','narrative_review']
