"""Finite direct API transport records actual effects without changing recall criteria."""
import importlib.util
import io
import json
from pathlib import Path
import urllib.error

import pytest


@pytest.fixture
def api(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec = importlib.util.spec_from_file_location('receiving_api_test',
        root/'research/agent-memory-2026-10-06/pilots/receiving_api.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    monkeypatch.setattr(module.exchange.pilot.configuration, 'read_env_key', lambda _: 'fixture-secret')
    return module


def request(api, root):
    value = dict(format='hmk-fictional-receiving-request/v1', model='nvidia/fixture',
        phase='narrative_generation', fresh_context=True, tools_allowed=False,
        native_memory_allowed=False, reasoning_effort='high',
        messages=[{'role':'system','content':'Fictional output.'},
                  {'role':'user','content':'Only this supplied source.'}],
        response_schema={'type':'object'})
    path = root/(api.exchange.pilot.digest(value)+'.json')
    api.exchange.pilot.save(path, value)
    return path, value


def opener(content='{"claims":[]}', finish='stop', tools=None, observed=None):
    def open_call(call, timeout):
        assert timeout in {120,300}
        if observed is not None:observed.append(json.loads(call.data))
        stream = io.StringIO(json.dumps(dict(id='fixture-response', model='nvidia/fixture',
            usage=None, choices=[dict(finish_reason=finish,
                message=dict(content=content, tool_calls=tools))])))
        stream.status = 200
        return stream
    return open_call


def test_decoder_modes_have_identical_supplied_messages_and_local_schema(api,tmp_path):
    _, value = request(api,tmp_path)
    before = json.dumps(value)
    plain = api.parameters(value,12000,'plain'); schema = api.parameters(value,12000,'schema')
    assert plain['messages'] == schema['messages']
    assert schema['response_format']['json_schema']['schema'] == value['response_schema']
    assert 'response_format' not in plain and 'reasoning_budget' not in plain
    assert 'tools' not in plain and json.dumps(value) == before
    assert plain['max_tokens'] == schema['max_tokens'] == 12000


@pytest.mark.parametrize('changes',[{'model':'other/provider'}, {'fresh_context':False},
    {'tools_allowed':True}, {'native_memory_allowed':True}, {'format':'private-live-request'}])
def test_nonfictional_or_agent_requests_do_not_dispatch(api,tmp_path,changes):
    path,value = request(api,tmp_path);value.update(changes)
    path = tmp_path/(api.exchange.pilot.digest(value)+'.json');api.exchange.pilot.save(path,value)
    with pytest.raises(ValueError):api.dispatch(path,tmp_path,opener=lambda *_a,**_k:pytest.fail('API called'))
    assert not (tmp_path/'dispatches').exists()


def test_one_fresh_text_call_preserves_final_output_unknown_usage_and_actual_receipt(api,tmp_path):
    path,value = request(api,tmp_path);observed=[]
    receipt = api.dispatch(path,tmp_path,opener=opener(observed=observed))
    result = json.loads(receipt.read_text())
    saved = json.loads((tmp_path/'responses'/path.name).read_text())
    assert saved['content'] == result['content'] == '{"claims":[]}'
    assert saved['usage'] is None and saved['fresh_context'] is True
    assert saved['dispatch_receipt'] == str(receipt) and saved['tool_calls_observed'] == []
    assert 'fixture-secret' not in receipt.read_text()
    assert len(observed) == 1 and observed[0]['messages'][1:] == value['messages'][1:]
    with pytest.raises(ValueError,match='already observed'):
        api.dispatch(path,tmp_path,opener=lambda *_a,**_k:pytest.fail('Duplicate API execution'))


def test_timeout_keeps_actual_uncertain_attempt_and_refuses_silent_retry(api,tmp_path):
    path,_ = request(api,tmp_path)
    def fail(*_a,**_k):raise TimeoutError('fixture')
    with pytest.raises(TimeoutError):api.dispatch(path,tmp_path,opener=fail)
    receipt = json.loads((tmp_path/'dispatches'/path.name).read_text())
    assert receipt['state'] == 'failed' and receipt['usage'] is None
    assert not (tmp_path/'responses'/path.name).exists()
    with pytest.raises(ValueError,match='already observed'):api.dispatch(path,tmp_path,opener=fail)


@pytest.mark.parametrize('content,tools',[(None,None), ('{}',[{'type':'function','function':{'name':'fixture'}}])])
def test_unexpected_provider_tools_or_missing_final_text_preserved_but_not_consumed(api,tmp_path,content,tools):
    path,_ = request(api,tmp_path)
    with pytest.raises(ValueError,match='unexpected tool'):
        api.dispatch(path,tmp_path,opener=opener(content=content,tools=tools))
    receipt = json.loads((tmp_path/'dispatches'/path.name).read_text())
    assert receipt['state'] == 'completed' and receipt['content'] == content
    assert receipt['tool_calls_observed'] == (tools or [])
    assert not (tmp_path/'responses'/path.name).exists()


def test_length_truncated_output_keeps_exact_raw_bytes_for_bounded_local_repair(api,tmp_path):
    path,_ = request(api,tmp_path)
    api.dispatch(path,tmp_path,opener=opener(content='{"claims":[]}',finish='length'))
    value=json.loads((tmp_path/'responses'/path.name).read_text())
    assert value['content'] == '{"claims":[]}' and value['finish_reason']=='length'


def test_driver_is_finite_resumable_and_freezes_provider_settings(api,tmp_path,monkeypatch):
    root = tmp_path/'run';count=[]
    def receive(packet_root,out,model,effort,resume):
        if not resume:out.mkdir();api.exchange.pilot.save(out/'conditions.json',{})
        path,_=request(api,out)
        return dict(state='prepared',request=str(path),completed_candidates=0,qualification=False)
    monkeypatch.setattr(api.exchange,'receive',receive)
    monkeypatch.setattr(api,'dispatch',lambda *a,**kw:(count.append((a,kw)) or Path('fixture-receipt')))
    value=api.run(tmp_path,root,'nvidia/fixture','high',12000,'plain',2)
    assert len(count)==2 and value['new_dispatches']==2 and value['qualification'] is False
    with pytest.raises(ValueError,match='settings changed'):
        api.run(tmp_path,root,'nvidia/fixture','high',12000,'schema',2,resume=True)
    assert len(count)==2
    api.run(tmp_path,root,'nvidia/fixture','high',12000,'plain',1,resume=True)
    assert len(count)==3


def test_failed_client_request_can_retry_once_without_repeating_generation_or_erasing_unknown_cost(api,tmp_path):
    path,_ = request(api,tmp_path)
    def fail(*_a,**_k):raise TimeoutError('fixture')
    with pytest.raises(TimeoutError):api.dispatch(path,tmp_path,opener=fail,timeout=120)
    original = (tmp_path/'dispatches'/path.name).read_bytes()
    receipt = api.dispatch(path,tmp_path,opener=opener(),retry_failed=True)
    assert (tmp_path/'dispatches'/path.name).read_bytes()==original
    assert json.loads(receipt.read_text())['attempt']==2
    assert json.loads(original)['usage'] is None
    with pytest.raises(ValueError):api.dispatch(path,tmp_path,opener=opener(),retry_failed=True)


def test_started_or_twice_failed_request_cannot_be_silently_duplicated(api,tmp_path):
    path,_ = request(api,tmp_path)
    def fail(*_a,**_k):raise TimeoutError('fixture')
    for retry in (False,True):
        with pytest.raises(TimeoutError):api.dispatch(path,tmp_path,opener=fail,retry_failed=retry)
    with pytest.raises(ValueError,match='retry was already'):
        api.dispatch(path,tmp_path,opener=opener(),retry_failed=True)
    first=tmp_path/'dispatches'/path.name
    value=json.loads(first.read_text());value['state']='started';api.exchange.pilot.save(first,value)
    with pytest.raises(ValueError,match='unresolved'):
        api.dispatch(path,tmp_path,opener=opener(),retry_failed=True)


def test_transport_adoption_preserves_old_conditions_but_cannot_change_model_inputs(api,tmp_path,monkeypatch):
    root=tmp_path/'run'
    def receive(packet_root,out,model,effort,resume):
        if not resume:out.mkdir();api.exchange.pilot.save(out/'conditions.json',{})
        return dict(state='candidates_complete',qualification=False)
    monkeypatch.setattr(api.exchange,'receive',receive)
    api.run(tmp_path,root,'nvidia/fixture','high',12000,'plain',1,timeout=120)
    old=json.loads((root/'provider-conditions.json').read_text())
    api.run(tmp_path,root,'nvidia/fixture','high',12000,'plain',1,resume=True,adopt_transport=True)
    history=json.loads((root/'provider-conditions-history.json').read_text())
    assert history[0]['previous']==old and history[0]['adopted']['timeout_seconds']==300
    with pytest.raises(ValueError,match='settings changed'):
        api.run(tmp_path,root,'nvidia/other','high',12000,'plain',1,resume=True,adopt_transport=True)
    assert json.loads((root/'provider-conditions-history.json').read_text())==history
