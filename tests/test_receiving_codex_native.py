"""Native fictional receiver isolation controls and failed-attempt accounting."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def native(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec = importlib.util.spec_from_file_location('native_receiver_test',
        root/'research/agent-memory-2026-10-06/pilots/receiving_codex_native.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def inputs(native, path):
    request = dict(format='hmk-fictional-receiving-request/v1', model='gpt-6.1-sol',
        phase='narrative_generation', reasoning_effort='low', fresh_context=True,
        tools_allowed=False, native_memory_allowed=False,
        messages=[dict(role='system', content='Fictional JSON only.'),
                  dict(role='user', content='Supplied fictional evidence.')], response_schema={'type':'object'})
    request_path = path/(native.exchange.pilot.digest(request)+'.json')
    native.exchange.pilot.save(request_path, request)
    catalog = path/'catalog.json'
    native.exchange.pilot.save(catalog, {'models':[dict(slug='gpt-6.1-sol',
        apply_patch_tool_type=None, shell_type='disabled', experimental_supported_tools=[],
        supports_search_tool=False, node_repl_disabled=True)]})
    return request_path, request, catalog


def test_native_controls_and_usage_do_not_claim_an_invoice_or_model_label(native, tmp_path):
    path, request, catalog = inputs(native, tmp_path)
    credential = tmp_path/'fixture-auth.json'; credential.write_text('{}')
    def runner(argv, **kwargs):
        assert argv[0] == 'bwrap' and '--tmpfs' in argv
        argv = argv[argv.index('--')+1:]
        assert argv[0:2] == ['codex', 'exec']
        assert '--ignore-user-config' in argv and '--ephemeral' in argv
        assert 'forced_login_method="chatgpt"' in argv and 'model_provider="openai"' in argv
        assert 'project_doc_max_bytes=0' in argv and 'orchestrator.mcp.enabled=false' in argv
        assert kwargs['input'] == request['messages'][1]['content']
        assert kwargs['timeout'] == 300
        events = [dict(type='item.completed', item=dict(type='agent_message', text='{}')),
            dict(type='turn.completed', usage=dict(input_tokens=30, output_tokens=4, cached_input_tokens=10))]
        return SimpleNamespace(returncode=0, stdout='\n'.join(map(json.dumps, events)), stderr='private stderr')
    receipt = native.dispatch(path, tmp_path, catalog, runner, credential)
    data = json.loads(receipt.read_text())
    assert data['usage']['total_tokens'] == 34 and data['native_usage']['cached_input_tokens'] == 10
    assert data['billed_cost_usd'] is None and data['actual_response_model'] is None
    assert 'private stderr' not in receipt.read_text()
    with pytest.raises(ValueError, match='no implicit retry'):
        native.dispatch(path, tmp_path, catalog, lambda *_a, **_k: pytest.fail('repeated'), credential)


def test_observed_tool_use_is_preserved_but_cannot_enter_receiving(native, tmp_path):
    path, _request, catalog = inputs(native, tmp_path)
    credential = tmp_path/'fixture-auth.json'; credential.write_text('{}')
    def runner(*_a, **_k):
        events = [dict(type='item.completed', item=dict(type='mcp_tool_call')),
            dict(type='turn.completed', usage=dict(input_tokens=8, output_tokens=2))]
        return SimpleNamespace(returncode=0, stdout='\n'.join(map(json.dumps, events)))
    with pytest.raises(ValueError, match='used tools'):
        native.dispatch(path, tmp_path, catalog, runner, credential)
    receipt = json.loads((tmp_path/'dispatches'/path.name).read_text())
    assert receipt['state'] == 'failed' and receipt['usage']['total_tokens'] == 10
    assert not (tmp_path/'responses'/path.name).exists()


def test_unsupported_model_or_tool_capable_catalog_never_dispatches(native, tmp_path):
    path, request, catalog = inputs(native, tmp_path)
    request['model'] = 'openai/gpt-6.1-sol'
    with pytest.raises(ValueError, match='native Sol low'):
        native.command(request, catalog, tmp_path, tmp_path)
    data = json.loads(catalog.read_text()); data['models'][0]['apply_patch_tool_type'] = 'freeform'
    native.exchange.pilot.save(catalog, data)
    with pytest.raises(ValueError, match='disable all'):
        native.dispatch(path, tmp_path, catalog, lambda *_a, **_k: pytest.fail('dispatched'))
