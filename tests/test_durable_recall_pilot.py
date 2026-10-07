"""Pilot API faults retain pending evidence and cannot authorize invented IDs."""
import importlib.util
from pathlib import Path
import json
from types import SimpleNamespace

import pytest


@pytest.fixture
def pilot(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root/'scripts'))
    spec = importlib.util.spec_from_file_location('durable_pilot_test',
        root/'research/agent-memory-2026-10-06/pilots/durable_recall_pilot.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('value', [[], {'queries': None}, {'queries': ['ok', '']},
    {'queries': [{'query': 'ok', 'instruction': 'extra'}]}, {'queries': ['a','b','c']},
    {'expand_ids': ['1']}, {'expand_ids': [True]}, {'expand_ids': [99]}, {'other': 1}])
def test_invalid_plan_is_rejected_before_tools(pilot, value):
    with pytest.raises(ValueError):
        pilot.recall_plan(value, {1})


def test_equivalent_query_shapes_and_bounded_ids(pilot):
    assert pilot.recall_plan({'queries': [' relay ', {'query':'issue'}], 'expand_ids':[1,1]}, {1}) == {
        'queries':['relay','issue'], 'expand_ids':[1]}
    assert pilot.recall_plan({}, set()) == {'queries':[], 'expand_ids':[]}
    pack = {'items':[{'id':1,'neighbors':[{'id':2,'neighbors':[{'id':99}]}]}]}
    assert pilot.visible_ids(pack) == {1,2}
    assert pilot.recall_plan({'expand_ids':[2]}, pilot.visible_ids(pack))['expand_ids'] == [2]


def test_trace_survives_rejected_response(pilot, tmp_path, monkeypatch):
    path = tmp_path/'trace.json'
    trace = pilot.Trace(path)
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, *args):
            return json.dumps({'model':'fixture-model', 'usage':{'total_tokens':42},
                'choices':[{'message':{'content':'not JSON'}, 'finish_reason':'stop'}]}).encode()
    monkeypatch.setattr(pilot.configuration, 'read_env_key', lambda key: 'fictional-key')
    monkeypatch.setattr(pilot.urllib.request, 'urlopen', lambda *a, **k: Response())
    with pytest.raises(json.JSONDecodeError):
        pilot.chat('fixture-model', [], trace)
    assert json.loads(path.read_text())[0]['usage']['total_tokens'] == 42


def test_failed_plans_resume_without_losing_capture_or_pending_question(pilot, tmp_path, monkeypatch):
    original = pilot.memory_at
    def isolated(path):
        memory = original(path)
        memory.backfill_embeddings = lambda: {'updated':0}
        memory.semantic_search = lambda *a, **k: []
        memory.rerank_provider_default = lambda: 'none'
        return memory
    monkeypatch.setattr(pilot, 'memory_at', isolated)
    args = SimpleNamespace(out=tmp_path, resume=False, model='fictional', consolidate=False)
    corpus = {'fixture_context':{}, 'cases':[{'id':'encounter', 'sources':[
        {'id':'source', 'originating_body':'fixture:body', 'content':'Tavi proposed labels.'}],
        'questions':[{'query':'Who proposed labels?'}]}]}
    decision = {'outcome':'applied','reason':'Meaningful encounter', 'records':[
        {'key':'event','operation':'add','shelf':'episodes','title':'Label proposal',
         'raw':'Tavi proposed labels.', 'engram_type':'episodic'}], 'links':[]}
    responses = iter([decision, {'queries':[None]}, {'expand_ids':['1']}])
    monkeypatch.setattr(pilot, 'chat', lambda *a: next(responses))
    with pytest.raises(ValueError):
        pilot.run_variant('test', '', args, corpus)
    out = tmp_path/'test'
    pending_before = json.loads((out/'pending-recall.json').read_text())
    assert len(pending_before['plans']) == 2
    assert len(json.loads((out/'capture.json').read_text())) == 1
    args.resume = True
    responses = iter([{'queries':[], 'expand_ids':[1]}, {'answer':{
        'identification':'Tavi', 'context':'A label discussion', 'meaning':'Proposed labels',
        'outcome':'Unknown', 'limits':'No other evidence'}, 'used_ids':[1]}])
    pilot.run_variant('test', '', args, corpus)
    answer = json.loads((out/'answers.json').read_text())[0]
    assert answer['packs'] == pending_before['packs']
    assert len(answer['plan_attempts']) == 3
    assert not (out/'pending-recall.json').exists()
    assert not (out/'dream.json').exists()
    assert len(json.loads((out/'selected-canon.json').read_text())) == 1


def test_grounded_answer_requires_context_and_actual_visible_ids(pilot):
    with pytest.raises(ValueError):
        pilot.grounded_answer({'answer':'Tavi','used_ids':[1]}, {1})
    answer = {'answer':{'identification':'Unknown','context':'Unknown','meaning':'Unknown',
              'outcome':'Unknown','limits':'No supporting memory'}, 'used_ids':[]}
    assert pilot.grounded_answer(answer, set()) == answer
    answer['used_ids'] = [99]
    with pytest.raises(ValueError):
        pilot.grounded_answer(answer, {1})
