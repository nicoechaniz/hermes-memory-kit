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


def test_joint_conclusion_retains_memory_and_actual_binding_without_changing_verdict():
    evidence={1:{'text':'Running these checks requires repository/runtime tools.'}}
    binding={'receiving_body':'voice','repository_runtime_access':False}
    candidate={'receiving_body':'voice','claims':[dict(text='I cannot run those checks here.',
        basis='binding',support=[],facet='limits')]}
    raw={'claims':[dict(index=0,verdict='supported',reason='Two actual premises support the conclusion.',assertions=[dict(
        span=candidate['claims'][0]['text'],basis='memory',source_fact='Checks require runtime tools and current runtime access is false.',
        proof=[{'id':1,'passage':0}],binding_fields=['repository_runtime_access'],
        verdict='supported',reason='Original dependency and actual body capability jointly entail this limit.')])],'missing':[]}
    strict=nr.passage_review(raw,candidate,evidence,'assertions')
    with pytest.raises(ValueError,match='only binding assertions'):
        nr.review_shape(strict,candidate,evidence,binding,'assertions')
    joint=nr.passage_review(raw,candidate,evidence,'assertions',True)
    nr.review_shape(joint,candidate,evidence,binding,'assertions',True)
    atom=joint['claims'][0]['assertions'][0]
    assert atom['basis']=='mixed' and raw['claims'][0]['assertions'][0]['basis']=='memory'
    assert atom['span']==candidate['claims'][0]['text']
    assert atom['proof']==[{'id':1,'quote':evidence[1]['text']}]
    assert nr.supported_claims(candidate,joint)['claims'][0]['basis']=='mixed'
    # A rejected date/actor remains rejected; normalization is not approval.
    raw['claims'][0]['verdict']=raw['claims'][0]['assertions'][0]['verdict']='unsupported'
    rejected=nr.passage_review(raw,candidate,evidence,'assertions',True)
    assert rejected['claims'][0]['verdict']=='unsupported'
    atom['binding_fields']=['invented_access']
    with pytest.raises(ValueError,match='actual supplied receiving fields'):
        nr.review_shape(joint,candidate,evidence,binding,'assertions',True)


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
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('fixture','Can this body run the checks?',evidence,binding,
            trace,pending,tmp_path/'pending.json',chat,save,review_protocol='assertions',
            preserve_citation_receipts=True)
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('fixture','Can this body run the checks?',evidence,binding,
            trace,pending,tmp_path/'pending.json',chat,save,review_protocol='assertions',
            clarify_deixis=True)
    for options in [{'allow_joint_support':True}, {'review_effort':'medium'}, {'check_unknown_premises':True}]:
        with pytest.raises(ValueError,match='procedure/model changed'):
            nr.answer('fixture','Can this body run the checks?',evidence,binding,
                trace,pending,tmp_path/'pending.json',chat,save,review_protocol='assertions',**options)


def test_report_referents_preserve_source_and_require_event_specific_membership():
    quotation = 'You helped me yesterday. I want us to remember Leto; we have not contacted the group.'
    evidence = {1: {'text': 'Human report; source report; received 2026-09-17 through code:\n'
                     + json.dumps(quotation)}}
    binding = {'receiving_body': 'voice'}
    original = nr.supplied_context('Who contacted whom?', evidence, binding, 'decoded')
    clarified = nr.supplied_context('Who contacted whom?', evidence, binding, 'decoded', True)
    block = clarified['evidence'][0]['attributed_blocks'][0]
    assert block['quotation'] == original['evidence'][0]['attributed_blocks'][0]['quotation'] == quotation
    assert block['source_referents']['receiving_being_membership'] == 'requires explicit event-specific source evidence'
    assert 'does not identify' in block['source_referents']['first_person_plural']
    assert 'source_referents' not in original['evidence'][0]['attributed_blocks'][0]
    evidence[1]['text'] = evidence[1]['text'].replace('Human report', 'Human conversation')
    direct = nr.supplied_context('What did we discuss?', evidence, binding, 'decoded', True)
    assert 'source_referents' not in direct['evidence'][0]['attributed_blocks'][0]


@pytest.mark.parametrize('source,pointer', [
    ('See (https://forge.example.invalid/commons/harbormesh/issues/47).',
     'https://forge.example.invalid/commons/harbormesh/issues/47'),
    ('See [https://example.invalid/Foo_(film)].', 'https://example.invalid/Foo_(film)'),
    ('See (https://example.invalid/Foo_(film)).', 'https://example.invalid/Foo_(film)'),
    ('See https://example.invalid/part{two}.', 'https://example.invalid/part{two}'),
])
def test_world_pointers_drop_only_unmatched_prose_punctuation(source, pointer):
    evidence = {1: {'text': source}}
    assert nr.source_anchors(evidence[1]) == [pointer]
    candidate = {'claims': [dict(text='The source is '+pointer, support=[1], basis='memory')]}
    assert nr.missing_anchors(candidate, evidence) == []


def test_secondary_identifier_proof_preserves_receipts_without_another_story():
    evidence = {7: {'text': 'Human report; source tentative; received 2026-07-01 through code:\n'
        + json.dumps('The human group wanted to try the checklist.') + '\n\n'
        + 'tool_response; source identity; received 2026-07-04 through code:\n'
        + json.dumps('Mara\'s account remains 1847.')}}
    candidate = {'claims': [dict(text='Mara has account 1847.', support=[7], basis='memory')]}
    assert len(nr.missing_anchors(candidate, evidence)) == 2
    receipts = nr.receipt_context(candidate, evidence)
    assert nr.missing_anchors(candidate, evidence, receipts) == []
    assert candidate['claims'][0]['text'] == 'Mara has account 1847.'
    assert [s['reported_at'] for s in receipts[0]['sources']] == ['2026-07-01', '2026-07-04']
    assert all('quotation' not in s for s in receipts[0]['sources'])
    receipts[0]['sources'][0]['reported_at'] = '2036-07-01'
    with pytest.raises(ValueError, match='original supplied sources'):
        nr.missing_anchors(candidate, evidence, receipts)


def test_receipt_metadata_does_not_excuse_missing_world_pointer_or_wrong_claim(tmp_path):
    candidate,evidence,binding,review = example()
    candidate['claims'][0].update(basis='mixed', support=[1])
    evidence[1]['text'] = ('foreground_work; source checks; received 2026-08-05 through code:\n'
                          + json.dumps('The checks need repository/runtime tools. See docs/checks.md.'))
    receipts = nr.receipt_context(candidate, evidence)
    missing = nr.missing_anchors(candidate, evidence, receipts)
    assert len(missing) == 1 and 'docs/checks.md' in missing[0]
    # A real attribution verdict must still reject the narrative even when
    # every receipt is retained. Citation metadata is never semantic proof.
    evidence[1]['text'] = 'Only the human group wanted to try the method.'
    candidate['claims'][0].update(text='We wanted to try the method.',basis='memory',support=[1])
    bad = dict(span='We wanted to try the method.',basis='memory',source_fact=evidence[1]['text'],
               proof=[{'id':1,'passage':0}],binding_fields=[],verdict='unsupported',reason='Human group is not this being.')
    raw = dict(claims=[dict(index=0,verdict='unsupported',reason=bad['reason'],assertions=[bad])],missing=[])
    calls = []
    def chat(model,messages,trace):
        calls.append(trace.phase)
        return raw if trace.phase == 'narrative_review' else candidate
    with pytest.raises(nr.NarrativeRejected):
        nr.answer('fixture','Who wanted to try?',evidence,binding,SimpleNamespace(phase='recall'),{},
            tmp_path/'pending.json',chat,lambda p,v: p.write_text(json.dumps(v)),
            review_protocol='assertions',preserve_citation_receipts=True)
    assert calls.count('narrative_review') == 3


def test_required_semantic_revision_keeps_observed_feedback_then_accepts_receipts(tmp_path):
    evidence = {1: {'text': 'Human report; source intent; received 2026-07-01 through code:\n'
                    + json.dumps('The human group wanted to try the method.')}}
    binding = {'receiving_body': 'voice'}
    wrong = {'receiving_body': 'voice', 'claims': [dict(text='We wanted to try the method.',
             support=[1], basis='memory', facet='limits')]}
    faithful = json.loads(json.dumps(wrong))
    faithful['claims'][0]['text'] = 'The human group wanted to try the method.'
    def chat(model,messages,trace):
        if trace.phase == 'narrative_generation':return wrong
        if trace.phase == 'narrative_revision':
            feedback = json.JSONDecoder().raw_decode(messages[-1]['content'])[0]['review']
            assert feedback['missing'] == nr.missing_anchors(wrong,evidence)
            return faithful
        packet = json.loads(messages[1]['content']); text = packet['candidate']['claims'][0]['text']
        verdict = 'supported' if text == faithful['claims'][0]['text'] else 'unsupported'
        return {'claims':[dict(index=0,verdict=verdict,reason='Check who wanted to try.',assertions=[dict(
            span=text,verdict=verdict,reason='The human group is the source actor.',basis='memory',
            source_fact='Only the human group wanted to try.',proof=[{'id':1,'passage':1}],binding_fields=[])])], 'missing':[]}
    result = nr.answer('fixture','Who wanted to try?',evidence,binding,SimpleNamespace(phase='recall'),{},
        tmp_path/'pending.json',chat,lambda p,v:p.write_text(json.dumps(v)),
        review_protocol='assertions',preserve_citation_receipts=True)
    assert result['text'] == faithful['claims'][0]['text']
    assert result['citation_receipts'][0]['sources'][0]['reported_at'] == '2026-07-01'


def test_unknown_premise_contract_changes_only_review_and_keeps_bounded_phases(tmp_path):
    candidate,evidence,binding,review=example()
    raw=json.loads(json.dumps(review))
    raw['claims'][0]['assertions'][0]['proof']=[{'id':1,'passage':0}]
    contexts=[]
    def chat(model,messages,trace):
        contexts.append((trace.phase,messages))
        return raw if trace.phase=='narrative_review' else candidate
    pending={};save=lambda p,v:p.write_text(json.dumps(v))
    result=nr.answer('fixture','Can this body run the checks?',evidence,binding,
        SimpleNamespace(phase='recall'),pending,tmp_path/'pending.json',chat,save,
        review_protocol='assertions',check_unknown_premises=True)
    assert [p for p,m in contexts]==['narrative_generation','narrative_review']
    assert contexts[1][1][0]['content']==nr.ASSERTION_REVIEW+nr.UNKNOWN_PREMISES_REVIEW
    assert nr.UNKNOWN_PREMISES_REVIEW not in contexts[0][1][0]['content']
    assert result['text']==candidate['claims'][0]['text']
    assert result['unknown_premises_protocol']=='positive-presuppositions/v1'
    assert nr.answer('fixture','Can this body run the checks?',evidence,binding,
        SimpleNamespace(phase='recall'),pending,tmp_path/'pending.json',
        lambda *a:pytest.fail('Unexpected replay call'),save,review_protocol='assertions',
        check_unknown_premises=True)==result
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('fixture','Can this body run the checks?',evidence,binding,
            SimpleNamespace(phase='recall'),pending,tmp_path/'pending.json',chat,save,
            review_protocol='assertions')
    for option in [1,'yes']:
        with pytest.raises(ValueError,match='unknown premise checks'):
            nr.answer('fixture','q',evidence,binding,SimpleNamespace(phase='recall'),{},
                tmp_path/'invalid.json',chat,save,review_protocol='assertions',
                check_unknown_premises=option)
    with pytest.raises(ValueError,match='unknown premise checks'):
        nr.answer('fixture','q',evidence,binding,SimpleNamespace(phase='recall'),{},
            tmp_path/'invalid.json',chat,save,review_protocol='passages',check_unknown_premises=True)
