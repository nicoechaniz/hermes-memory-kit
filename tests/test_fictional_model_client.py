"""Fictional full-pipeline transport must preserve inputs, receipts and work."""
import importlib.util
import json
from pathlib import Path
import pytest


@pytest.fixture
def client_module(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec=importlib.util.spec_from_file_location('fictional_client_test',
        root/'research/agent-memory-2026-10-06/pilots/fictional_model_client.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def inputs(module,tmp_path):
    fixture=tmp_path/'fixture.json';fixture.write_text(json.dumps(dict(fictional=True,expected='SECRET_HIDDEN_RUBRIC')))
    catalog=tmp_path/'catalog.json';catalog.write_text('{"models":[]}')
    arm=tmp_path/'proposed';arm.mkdir()
    trace=module.api.exchange.pilot.Trace(arm/'trace.json');trace.phase='capture'
    messages=[dict(role='system',content='Select supplied fictional sources only.'),
              dict(role='user',content='A fictional source says no change occurred.')]
    return fixture,catalog,trace,messages


def test_operation_receipt_replay_and_hidden_fixture_stay_separate(client_module,tmp_path):
    m=client_module;fixture,catalog,trace,messages=inputs(m,tmp_path);calls=[]
    def dispatch(path,root):
        request=json.loads(path.read_text());calls.append(request)
        assert request['messages']==messages and 'SECRET_HIDDEN_RUBRIC' not in path.read_text()
        params=m.api.parameters(request,'deepseek');assert params['thinking']=={'type':'enabled'}
        receipt=root/'dispatches'/path.name;receipt.parent.mkdir();response=root/'responses'/path.name;response.parent.mkdir()
        content='{"outcome":"omitted"}'
        m.api.exchange.pilot.save(receipt,dict(state='completed',content=content,parameters=params,
            parameters_sha256=m.api.exchange.pilot.digest(params)))
        m.api.exchange.pilot.save(response,dict(request_sha256=path.stem,requested_model='deepseek-flash',
            fresh_context=True,tool_calls_observed=[],dispatch_receipt=str(receipt),content=content,usage=None))
    c=m.Client(tmp_path/'transport',fixture,'fixture-key',catalog,dispatcher=dispatch)
    assert c.chat('deepseek-flash',messages,trace)=={'outcome':'omitted'}
    assert c.chat('deepseek-flash',messages,trace)=={'outcome':'omitted'}
    assert len(calls)==len(trace)==1
    response=next((tmp_path/'transport/proposed/responses').glob('*.json'))
    data=json.loads(response.read_text());data['content']='{"outcome":"applied"}';m.api.exchange.pilot.save(response,data)
    with pytest.raises(ValueError,match='parameters/content'):
        c.chat('deepseek-flash',messages,trace)
    assert len(calls)==1


def test_changed_role_or_fixture_and_failed_dispatch_preserve_pending(client_module,tmp_path):
    m=client_module;fixture,catalog,trace,messages=inputs(m,tmp_path);calls=[]
    def fail(path,root):
        calls.append(path.stem);receipt=root/'dispatches'/path.name;receipt.parent.mkdir()
        m.api.exchange.pilot.save(receipt,dict(state='failed',usage=None))
        raise TimeoutError()
    c=m.Client(tmp_path/'transport',fixture,'fixture-key',catalog,dispatcher=fail)
    with pytest.raises(TimeoutError):c.chat('deepseek-flash',messages,trace)
    with pytest.raises(RuntimeError,match='no implicit retry'):c.chat('deepseek-flash',messages,trace)
    assert len(calls)==1
    with pytest.raises(ValueError,match='transport changed'):
        m.Client(tmp_path/'transport',fixture,'fixture-key',catalog,operation_effort='none')
    fixture.write_text('{"fictional":false}')
    with pytest.raises(ValueError,match='fictional fixture'):
        m.Client(tmp_path/'other',fixture,'fixture-key',catalog)
    request=json.loads(next((tmp_path/'transport/proposed/requests').glob('*.json')).read_text())
    request['fictional']=False
    with pytest.raises(ValueError,match='fictional text profile'):m.api.parameters(request,'deepseek')
    request['fictional']=True;request['phase']='live-memory-sync'
    with pytest.raises(ValueError,match='fictional text profile'):m.api.parameters(request,'deepseek')


def test_narrative_call_cannot_bypass_frozen_role(client_module,tmp_path):
    m=client_module;fixture,catalog,trace,messages=inputs(m,tmp_path)
    c=m.Client(tmp_path/'transport',fixture,'fixture-key',catalog,
               dispatcher=lambda *_a:pytest.fail('Unselected role dispatched'))
    trace.phase='narrative_generation'
    with pytest.raises(ValueError,match='frozen processing role'):
        c.chat('gpt-6.1-sol',messages,trace)
    trace.phase='narrative_review'
    with pytest.raises(ValueError,match='frozen processing role'):
        c.chat('deepseek-flash',messages,trace)
