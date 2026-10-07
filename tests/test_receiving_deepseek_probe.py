"""DeepSeek diagnostics preserve observed and uncertain effects without retries."""
import importlib.util
import io
import json
from pathlib import Path

import pytest


@pytest.fixture
def probe(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    monkeypatch.syspath_prepend(str(root/'research/agent-memory-2026-10-06/pilots'))
    spec = importlib.util.spec_from_file_location('deepseek_probe_test',
        root/'research/agent-memory-2026-10-06/pilots/receiving_deepseek_probe.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(probe, root, **changes):
    value = dict(format='hmk-fictional-receiving-request/v1', model='deepseek-flash',
        phase='narrative_generation', reasoning_effort='low', fresh_context=True,
        tools_allowed=False, native_memory_allowed=False,
        messages=[dict(role='system', content='Fictional JSON output.'),
                  dict(role='user', content='Supplied fictional evidence only.')],
        response_schema={'type': 'object'})
    value.update(changes)
    path = root/(probe.exchange.pilot.digest(value)+'.json')
    probe.exchange.pilot.save(path, value)
    return path


def test_final_text_usage_and_receipt_preserved_without_secret_or_reasoning(probe, tmp_path):
    path = request(probe, tmp_path)
    def opener(call, timeout):
        payload = json.loads(call.data)
        assert timeout == 300
        assert payload['thinking'] == {'type': 'enabled'}
        assert payload['reasoning_effort'] == 'low'
        assert payload['response_format'] == {'type': 'json_object'}
        assert 'temperature' not in payload and 'tools' not in payload
        result = io.StringIO(json.dumps(dict(id='fixture-response', model='deepseek-flash',
            usage={'prompt_tokens': 3, 'completion_tokens': 5, 'total_tokens': 8},
            choices=[dict(finish_reason='stop', message=dict(content='{"claims":[]}',
                reasoning_content='discard-this-reasoning'))])))
        result.status = 200
        return result
    receipt = probe.dispatch(path, tmp_path, 'fixture-secret', opener)
    saved = json.loads((tmp_path/'responses'/path.name).read_text())
    assert saved['content'] == '{"claims":[]}' and saved['usage']['total_tokens'] == 8
    assert saved['dispatch_receipt'] == str(receipt)
    assert 'fixture-secret' not in receipt.read_text()
    assert 'discard-this-reasoning' not in receipt.read_text()
    with pytest.raises(ValueError, match='no implicit retry'):
        probe.dispatch(path, tmp_path, 'fixture-secret', lambda *_a, **_k: pytest.fail('repeated call'))


def test_timeout_preserves_unknown_cost_and_disallows_repetition(probe, tmp_path):
    path = request(probe, tmp_path)
    def timeout(*_a, **_k):
        raise TimeoutError('fixture-secret must not appear in receipt')
    with pytest.raises(TimeoutError):
        probe.dispatch(path, tmp_path, 'fixture-secret', timeout)
    text = (tmp_path/'dispatches'/path.name).read_text()
    receipt = json.loads(text)
    assert receipt['state'] == 'failed' and receipt['usage'] is None
    assert 'fixture-secret' not in text and not (tmp_path/'responses'/path.name).exists()
    with pytest.raises(ValueError, match='no implicit retry'):
        probe.dispatch(path, tmp_path, 'fixture-secret', timeout)


@pytest.mark.parametrize('changes', [dict(model='another-provider'),
    dict(phase='narrative_review'), dict(native_memory_allowed=True), dict(tools_allowed=True)])
def test_other_models_review_or_native_context_cannot_dispatch(probe, tmp_path, changes):
    path = request(probe, tmp_path, **changes)
    with pytest.raises(ValueError):
        probe.dispatch(path, tmp_path, 'fixture-secret', lambda *_a, **_k: pytest.fail('API called'))
    assert not (tmp_path/'dispatches').exists()
