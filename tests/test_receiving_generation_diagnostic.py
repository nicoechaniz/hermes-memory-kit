"""Diagnostic reuse is an exact-input observation, not another model call."""
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def diagnostic(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec = importlib.util.spec_from_file_location('generation_diagnostic_test',
        root/'research/agent-memory-2026-10-06/pilots/receiving_generation_diagnostic.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def packet_root(module, path, count=1):
    path.mkdir()
    packets = [dict(arm='proposed', answer_index=i, case_id='fixture', context_sha256='fixture',
        context=dict(question='Question '+str(i), evidence=[], receiving_binding={
            'receiving_body':'fixture:voice'})) for i in range(count)]
    module.api.exchange.pilot.save(path/'packets.json', packets)
    module.api.exchange.pilot.save(path/'conditions.json', dict(fictional=True,
        packets_sha256=module.api.exchange.checksum(path/'packets.json')))
    return path


def test_generation_reuse_needs_identical_actual_parameters(diagnostic, tmp_path):
    root = packet_root(diagnostic, tmp_path/'packets')
    prior = tmp_path/'prior'
    diagnostic.run(root, prior, api_key=None, max_calls=0)
    m = json.loads((prior/'manifest.json').read_text())[0]
    d = m['request_sha256']
    request = json.loads((prior/'requests'/(d+'.json')).read_text())
    receipt = prior/'receipt.json'
    diagnostic.api.exchange.pilot.save(receipt, dict(state='completed',
        parameters=diagnostic.api.parameters(request, 'deepseek')))
    diagnostic.api.exchange.pilot.save(prior/'responses'/(d+'.json'), dict(
        request_sha256=d, requested_model='deepseek-flash', dispatch_receipt=str(receipt),
        fresh_context=True, tool_calls_observed=[], content='{}'))
    result = diagnostic.run(root, tmp_path/'reused', api_key=None, references=[prior], max_calls=0)
    assert result['available_generations'] == 1 and result['attempted_calls'] == 0
    changed = json.loads(receipt.read_text()); changed['parameters']['max_tokens'] = 6000
    diagnostic.api.exchange.pilot.save(receipt, changed)
    with pytest.raises(ValueError, match='identical actual provider'):
        diagnostic.run(root, tmp_path/'bad-reuse', api_key=None, references=[prior], max_calls=0)


def test_each_failure_is_observed_and_no_unresolved_dispatch_is_repeated(diagnostic, tmp_path, monkeypatch):
    root = packet_root(diagnostic, tmp_path/'packets', count=2)
    calls = []
    def failed(request, out, *_args):
        d = request.stem
        calls.append(d)
        (out/'dispatches').mkdir(exist_ok=True)
        diagnostic.api.exchange.pilot.save(out/'dispatches'/(d+'.json'), dict(state='started', usage=None))
        raise TimeoutError('private error must not be saved')
    monkeypatch.setattr(diagnostic.api, 'dispatch', failed)
    out = tmp_path/'out'
    result = diagnostic.run(root, out, api_key='fictional-key', max_calls=2)
    assert result['attempted_calls'] == len(result['failures']) == len(result['unresolved_dispatches']) == 2
    result = diagnostic.run(root, out, api_key='fictional-key', max_calls=2)
    assert result['attempted_calls'] == 0 and len(calls) == 2
    assert 'private error' not in (out/'state.json').read_text()


def test_changed_packet_bytes_cannot_enter_existing_diagnostic(diagnostic, tmp_path):
    root = packet_root(diagnostic, tmp_path/'packets')
    diagnostic.run(root, tmp_path/'out', api_key=None, max_calls=0)
    (root/'packets.json').write_text('[]')
    with pytest.raises(ValueError, match='unchanged fictional'):
        diagnostic.run(root, tmp_path/'out', api_key=None, max_calls=0)
