"""Source typing must preserve prose without accepting fabricated references."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

spec = importlib.util.spec_from_file_location('assertion_fixture',
    Path(__file__).resolve().parents[1]/'research/agent-memory-2026-10-06/pilots/narrative_recall.py')
nr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nr)


def example():
    evidence = {1:{'text':'The checks need repository/runtime tools.'}}
    binding = {'receiving_body':'voice','repository_runtime_access':False}
    candidate = {'receiving_body':'voice','claims':[dict(
        text='The checks need runtime tools, which this body lacks.',
        basis='binding',support=[],facet='limits')]}
    atoms = [dict(span='The checks need runtime tools,',basis='memory',
        source_fact='The checks require repository/runtime tools.',
        proof=[{'id':1,'quote':evidence[1]['text']}],binding_fields=[]),
        dict(span=' which this body lacks.',basis='binding',
        source_fact='Current repository_runtime_access is false.',
        proof=[],binding_fields=['repository_runtime_access'])]
    for a in atoms:
        a.update(verdict='supported',reason='Supplied source supports this proposition.')
    review = {'claims':[dict(index=0,verdict='supported',reason='Both clauses have distinct support.',assertions=atoms)],'missing':[]}
    return candidate,evidence,binding,review


def test_compound_support_does_not_rewrite_prose_or_hide_its_memory_citation():
    candidate,evidence,binding,review = example()
    nr.review_shape(review,candidate,evidence,binding,'assertions')
    grounded = nr.supported_claims(candidate,review)
    assert grounded['claims'][0]['text'] == candidate['claims'][0]['text']
    assert grounded['claims'][0]['basis'] == 'mixed'
    assert grounded['claims'][0]['support'] == [1]
    assert grounded['claims'][0]['draft_basis'] == 'binding'
    assert candidate['claims'][0]['support'] == []
    evidence[1]['text'] = 'https://example.invalid/checks'
    assert nr.missing_anchors(grounded,evidence)


def test_actual_binding_and_original_source_membership_remain_required():
    candidate,evidence,binding,review = example()
    review['claims'][0]['assertions'][1]['binding_fields'] = ['invented_runtime_access']
    with pytest.raises(ValueError,match='actual supplied receiving fields'):
        nr.review_shape(review,candidate,evidence,binding,'assertions')
    candidate,evidence,binding,review = example()
    review['claims'][0]['assertions'][0]['proof'][0]['quote'] = 'Checks have already succeeded.'
    with pytest.raises(ValueError,match='verbatim'):
        nr.review_shape(review,candidate,evidence,binding,'assertions')
    candidate,evidence,binding,review = example()
    review['claims'][0]['assertions'][0]['proof'][0]['id'] = 999
    with pytest.raises(ValueError,match='supplied citations'):
        nr.review_shape(review,candidate,evidence,binding,'assertions')


def test_unknown_cannot_hide_historical_proof_and_memory_cannot_drop_proof():
    candidate,evidence,binding,review = example()
    atom = review['claims'][0]['assertions'][0]
    atom['basis'] = 'unknown'
    with pytest.raises(ValueError,match='cannot cite historical proof'):
        nr.review_shape(review,candidate,evidence,binding,'assertions')
    atom['basis'] = 'memory'
    atom['proof'] = []
    with pytest.raises(ValueError,match='require quoted source proof'):
        nr.review_shape(review,candidate,evidence,binding,'assertions')


def test_conversation_and_indirect_report_do_not_share_a_narrator_label():
    quotation = json.dumps('We talked through a speaker. A separate group tested a relay.')
    conversation = nr.source_blocks('Human conversation; source direct; received 2026-09-17 through voice:\n'+quotation)[0]
    report = nr.source_blocks('Human report; source report; received 2026-09-17 through voice:\n'+quotation)[0]
    assert conversation['speaker'] == 'human conversational participant'
    assert report['speaker'] == 'human reporter'
    assert conversation['quotation'] == report['quotation']


def test_assertion_protocol_accepts_source_relabeling_without_semantic_revision(tmp_path):
    candidate,evidence,binding,review = example()
    raw = json.loads(json.dumps(review))
    raw['claims'][0]['assertions'][0]['proof'] = [{'id':1,'passage':0}]
    pending = {}
    trace = SimpleNamespace(phase='recall')
    phases = []
    def chat(model,messages,trace):
        phases.append(trace.phase)
        if trace.phase == 'narrative_generation':return candidate
        assert json.loads(messages[1]['content'])['review_protocol'] == 'assertions/v2'
        schema = nr.response_schema(trace.phase,messages)
        assert 'basis' in schema['properties']['claims']['items']['properties']['assertions']['items']['properties']
        return raw
    save = lambda p,v:p.write_text(json.dumps(v))
    result = nr.answer('fixture','Can this body run the checks?',evidence,binding,
        trace,pending,tmp_path/'pending.json',chat,save,review_protocol='assertions')
    assert phases == ['narrative_generation','narrative_review']
    assert result['text'] == candidate['claims'][0]['text']
    assert result['used_ids'] == [1]
    assert result['review_is_proof'] is False
    assert result['support_protocol'] == 'assertions/v2'
    assert nr.answer('fixture','Can this body run the checks?',evidence,binding,
        trace,pending,tmp_path/'pending.json',lambda *a:pytest.fail('Unexpected replay call'),save,
        review_protocol='assertions') == result
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('fixture','Can this body run the checks?',evidence,binding,
            trace,pending,tmp_path/'pending.json',chat,save,review_protocol='passages')
