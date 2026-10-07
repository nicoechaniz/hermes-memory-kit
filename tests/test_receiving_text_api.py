"""Receiving dispatch keeps profiles explicit and preserves failed actual calls."""
import importlib.util
import io
import json
from pathlib import Path

import pytest


@pytest.fixture
def api(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec=importlib.util.spec_from_file_location('receiving_text_test',
        root/'research/agent-memory-2026-10-06/pilots/receiving_text_api.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def request(api,root,model='deepseek-flash',phase='narrative_generation'):
    value=dict(format='hmk-fictional-receiving-request/v1',model=model,phase=phase,
        reasoning_effort='low',fresh_context=True,tools_allowed=False,native_memory_allowed=False,
        messages=[dict(role='system',content='Fictional JSON.'),dict(role='user',content='Evidence only.')],
        response_schema={'type':'object'})
    path=root/(api.exchange.pilot.digest(value)+'.json');api.exchange.pilot.save(path,value)
    return path,value


def test_only_route_and_output_controls_differ_between_provider_profiles(api,tmp_path):
    _,value=request(api,tmp_path)
    ds=api.parameters(value,'deepseek');value['model']='openai/gpt-6.1-sol'
    sol=api.parameters(value,'nous')
    assert ds['messages']==sol['messages']
    assert ds['max_tokens']==sol['max_tokens']==12000
    assert ds['thinking']=={'type':'enabled'} and 'thinking' not in sol
    assert ds['response_format']==sol['response_format']=={'type':'json_object'}
    value['phase']='narrative_review'
    assert api.parameters(value,'nous')['max_tokens']==32768
    with pytest.raises(ValueError):api.parameters(value,'deepseek')
    value['tools_allowed']=True
    with pytest.raises(ValueError):api.parameters(value,'nous')


def test_final_output_costs_and_unknown_actual_model_remain_observed_data(api,tmp_path):
    path,_=request(api,tmp_path,model='openai/gpt-6.1-sol')
    def opener(call,timeout):
        assert call.full_url==api.ENDPOINTS['nous'] and timeout==300
        result=io.StringIO(json.dumps(dict(id='fixture',model=None,provider='fixture-route',
            usage={'prompt_tokens':3,'completion_tokens':4,'total_tokens':7,'cost':0.001},
            choices=[dict(finish_reason='stop',message={'content':'{}',
                'reasoning_content':'discard-reasoning'})])))
        result.status=200;return result
    receipt=api.dispatch(path,tmp_path,'fixture-secret','nous',opener)
    data=json.loads(receipt.read_text());saved=json.loads((tmp_path/'responses'/path.name).read_text())
    assert data['response_provider']=='fixture-route' and saved['response_model'] is None
    assert saved['usage']['cost']==0.001 and saved['content']=='{}'
    assert 'fixture-secret' not in receipt.read_text() and 'discard-reasoning' not in receipt.read_text()
    with pytest.raises(ValueError,match='no implicit retry'):
        api.dispatch(path,tmp_path,'fixture-secret','nous',lambda *_a,**_k:pytest.fail('repeated'))


def test_failed_call_has_unknown_usage_and_cannot_be_replayed_implicitly(api,tmp_path):
    path,_=request(api,tmp_path)
    def timeout(*_a,**_k):raise TimeoutError('never store this secret')
    with pytest.raises(TimeoutError):api.dispatch(path,tmp_path,'fixture-secret','deepseek',timeout)
    data=json.loads((tmp_path/'dispatches'/path.name).read_text())
    assert data['state']=='failed' and data['usage'] is None
    assert not (tmp_path/'responses'/path.name).exists()
    with pytest.raises(ValueError,match='no implicit retry'):
        api.dispatch(path,tmp_path,'fixture-secret','deepseek',timeout)


def test_explicit_deepseek_nonthinking_profile_omits_unsupported_effort(api,tmp_path):
    _,value=request(api,tmp_path,phase='narrative_review')
    old=api.parameters(value,'deepseek')
    value['reasoning_effort']='none'
    selected=api.parameters(value,'deepseek')
    assert selected['thinking']=={'type':'disabled'}
    assert 'reasoning_effort' not in selected
    assert selected['messages']==old['messages'] and selected['max_tokens']==32768
    value['model']='openai/gpt-6.1-sol'
    with pytest.raises(ValueError):api.parameters(value,'nous')
    value.update(model='deepseek-flash',reasoning_effort='low')
    assert api.parameters(value,'deepseek')==old
