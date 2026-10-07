"""Narrative review must retain failed attempts and cannot fabricate support IDs."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

spec=importlib.util.spec_from_file_location('narrative_fixture',
    Path(__file__).resolve().parents[1]/'research/agent-memory-2026-10-06/pilots/narrative_recall.py')
nr=importlib.util.module_from_spec(spec);spec.loader.exec_module(nr)


def account(text, support):
    claims=[{'text':text, 'support':support, 'basis':'memory', 'facet':'outcome'}]
    for facet in ('identification','context','meaning','limits'):
        claims.append({'text':'No further detail is supplied in this test packet.',
                       'support':[], 'basis':'unknown', 'facet':facet})
    return {'receiving_body':'voice', 'claims':claims}


def verdict(status, reason, candidate, proof='', missing=None):
    return {'missing':missing or [], 'claims':[
        {'index':index,'verdict':status if index==0 else 'supported',
         'reason':reason if index==0 else 'Scoped to this test packet.',
         'assertions':[{'span':claim['text'], 'verdict':status if index==0 else 'supported',
                        'reason':reason, 'proof':[{'id':1,'quote':proof}] if index==0 and proof else []}]}
        for index,claim in enumerate(candidate['claims'])]}



def test_claim_support_and_complete_review_are_required():
    body={'receiving_body':'voice'}
    candidate=account('Jo was invited.',[1])
    assert nr.validate(candidate,{1:{}},body)==candidate
    candidate['claims'][0]['support']=[99]
    with pytest.raises(ValueError):nr.validate(candidate,{1:{}},body)
    with pytest.raises(ValueError):nr.review_shape({'missing':[], 'claims':[]},candidate,{1:{}})
    with pytest.raises(ValueError):nr.review_shape({'missing':[], 'claims':[
        {'index':0,'verdict':'supported','reason':'ok'},
        {'index':0,'verdict':'supported','reason':'ok'}]},candidate,{1:{}})


def test_false_nonreceipt_is_revised_and_cost_phases_and_originals_stay(tmp_path):
    body={'receiving_body':'voice'}
    unsupported=account('Jo did not receive it.',[1])
    corrected=account('Delivery failed; no reply was observed.',[1])
    evidence={1:{'text':'Delivery failed; no reply observed.'}}
    responses=iter([unsupported,verdict('unsupported','Unobserved receipt is not non-receipt.',unsupported),
        corrected,verdict('supported','Preserves observed failure and uncertainty.',corrected,evidence[1]['text'])])
    phases=[];trace=SimpleNamespace(phase='recall')
    def chat(model,messages,trace):
        assert 'SECRET_RUBRIC' not in json.dumps(messages)
        phases.append(trace.phase);return next(responses)
    pending={};path=tmp_path/'pending.json'
    save=lambda path,value:path.write_text(json.dumps(value))
    value=nr.answer('fixture','Did Jo get it?',evidence,
        body,trace,pending,path,chat,save)
    assert value['text'].startswith(corrected['claims'][0]['text'])
    assert value['review_is_proof'] is False
    assert pending['narrative']['generations'][0]==unsupported
    assert phases==['narrative_generation','narrative_review','narrative_revision','narrative_review']
    assert trace.phase=='recall'
    # A crash after accepted review must not repeat model calls on resumption.
    assert nr.answer('fixture','Did Jo get it?',evidence,body,trace,pending,path,chat,save)==value
    with pytest.raises(ValueError,match='context changed'):
        nr.answer('fixture','Did Jo get it?',{1:{'text':'CHANGED'}},body,trace,pending,path,chat,save)


def test_bounded_unsupported_narrative_preserves_pending_instead_of_claiming_success(tmp_path):
    body={'receiving_body':'voice'}
    candidate=account('Jo received it.',[1])
    responses=iter([candidate,verdict('unsupported','No receipt.',candidate),
                    candidate,verdict('unsupported','Still no receipt.',candidate),
                    candidate,verdict('unsupported','Still no receipt.',candidate)])
    pending={};path=tmp_path/'pending.json';trace=SimpleNamespace(phase='recall')
    with pytest.raises(ValueError,match='remained unsupported'):
        nr.answer('fixture','Did Jo get it?',{1:{}},body,trace,pending,path,
                  lambda *args:next(responses),lambda path,value:path.write_text(json.dumps(value)))
    saved=json.loads(path.read_text())
    assert len(saved['narrative']['generations'])==3
    assert 'accepted' not in saved['narrative']
    assert trace.phase=='recall'


def test_nested_envelopes_keep_human_speaker_separate_from_receiving_mobile_body():
    original='Human report; source report; received 2026-09-12 through mobile:\n'+json.dumps('I met Neri. You were not with me.')
    retained='Previously retained memory 4, revision 2:\n'+json.dumps(original)
    context=nr.supplied_context('Were we there?',{1:{'text':retained}}, {'receiving_body':'voice'})
    block=context['evidence'][0]['attributed_blocks'][0]
    assert block['speaker']=='human reporter'
    assert block['receiving_body']=='mobile'
    assert block['reported_at']=='2026-09-12'
    assert block['quotation']=='I met Neri. You were not with me.'
    # Incomplete previews cannot acquire an attributed speaker by guesswork.
    assert nr.source_blocks('Human report; ... [Incomplete preview]')[0]['speaker']=='unknown'


def test_supported_but_incomplete_answer_is_revised_without_hidden_rubric(tmp_path):
    body={'receiving_body':'voice'}
    first=account('Reed told us.',[1])
    final=account('Reed reported a reversed connector; we were not there.',[1])
    source='Reed reported a reversed connector; you were not there.'
    responses=iter([first,verdict('supported','Supported but incomplete.',first,source,['Reported connector lesson.']),
        final,verdict('supported','Includes lesson.',final,source)])
    value=nr.answer('fixture','What happened?',{1:{'text':'Reed reported a reversed connector; you were not there.'}},
        body,SimpleNamespace(phase='recall'),{},tmp_path/'pending.json',
        lambda *args:next(responses),lambda p,v:p.write_text(json.dumps(v)))
    assert value['text'].startswith(final['claims'][0]['text'])


def test_literal_source_anchors_detect_omitted_report_date_and_current_state_pointer():
    source='foreground_work; source work; received 2026-04-16 through code:\n'+json.dumps(
        'We authored the scheduler. Repository https://forge.example.invalid/p. Check docs/STATUS.md.')
    evidence={1:{'text':source}}
    candidate={'claims':[{'text':'We authored the scheduler.', 'support':[1], 'basis':'memory'}]}
    assert len(nr.missing_anchors(candidate,evidence))==3
    candidate['claims'][0]['text']='On 2026-04-16 our code body recorded scheduler authorship at https://forge.example.invalid/p, with present work to check in docs/STATUS.md.'
    assert nr.missing_anchors(candidate,evidence)==[]
    # Uncited retrieval distractors impose no fabricated coverage obligation.
    assert nr.missing_anchors({'claims':[{'text':'Unknown here.','support':[],'basis':'unknown'}]}, evidence)==[]


def test_date_values_survive_natural_prose_but_wrong_year_or_precision_fails():
    source='Human report; source report; received 2026-09-12 through mobile:\n'+json.dumps('A dated report.')
    evidence={1:{'text':source}}
    candidate={'claims':[{'text':'Reported on September 12th, 2026.', 'support':[1], 'basis':'memory'}]}
    assert nr.missing_anchors(candidate,evidence)==[]
    candidate['claims'][0]['text']='Reported on 12 September 2026.'
    assert nr.missing_anchors(candidate,evidence)==[]
    for text in ('Reported in September 2026.', 'Reported on September 12, 2036.'):
        candidate['claims'][0]['text']=text
        assert nr.missing_anchors(candidate,evidence)


def test_unknown_channels_and_unlisted_bodies_cannot_acquire_same_being_ownership():
    def source(role,body):
        return f'{role}; source event; received 2026-09-12 through {body}:\n'+json.dumps('I repaired it.')
    binding={'receiving_body':'voice','same_being_bodies':['code']}
    rows=nr.supplied_context('Who?',{1:{'text':source('surprise','code')},
        2:{'text':source('foreground_work','peer')},3:{'text':source('foreground_work','code')}},binding)['evidence']
    assert [row['attributed_blocks'][0]['speaker'] for row in rows]==[
        'unknown','attributed originating body','same-being originating body']


def test_atomic_review_cannot_hide_a_false_clause_or_forge_source_proof():
    candidate=account('Delivery failed; Jo received it.',[1])
    evidence={1:{'text':'Delivery failed.'}}
    review=verdict('unsupported','Second clause exceeds the source.',candidate)
    review['claims'][0]['assertions']=[
        {'span':'Delivery failed;', 'verdict':'supported','reason':'Observed failure.',
         'proof':[{'id':1,'quote':'Delivery failed.'}]},
        {'span':'Jo received it.','verdict':'unsupported','reason':'Receipt unknown.','proof':[]}]
    assert nr.review_shape(review,candidate,evidence)==review
    review['claims'][0]['verdict']='supported'
    with pytest.raises(ValueError,match='every assertion'):nr.review_shape(review,candidate,evidence)
    review['claims'][0]['verdict']='unsupported'
    review['claims'][0]['assertions'][0]['proof'][0]['quote']='Jo received it.'
    with pytest.raises(ValueError,match='verbatim'):nr.review_shape(review,candidate,evidence)
    review['claims'][0]['assertions']=review['claims'][0]['assertions'][1:]
    with pytest.raises(ValueError,match='every word'):nr.review_shape(review,candidate,evidence)


def test_known_uncertainty_can_be_cited_without_five_filler_facets():
    candidate={'receiving_body':'voice','claims':[{'text':'The report gives no surname.',
        'support':[1],'basis':'memory','facet':'limits'}]}
    assert nr.validate(candidate,{1:{'text':'No surname was supplied.'}},{'receiving_body':'voice'})==candidate


def test_invalid_atomic_review_retains_actual_candidate_as_rejected(tmp_path):
    candidate=account('Delivery failed.',[1])
    responses=iter([candidate,{'bad':'review'}, {'bad':'review again'}])
    pending={};path=tmp_path/'pending.json'
    with pytest.raises(nr.NarrativeRejected,match='atomic review invalid'):
        nr.answer('fixture','What happened?',{1:{'text':'Delivery failed.'}},
                  {'receiving_body':'voice'},SimpleNamespace(phase='recall'),pending,path,
                  lambda *args:next(responses),lambda p,v:p.write_text(json.dumps(v)))
    assert pending['narrative']['generations']==[candidate]
    assert len(pending['narrative']['reviews'])==2
    assert 'accepted' not in pending['narrative']


def test_json_schema_bounds_sentences_and_review_without_certifying_semantics():
    packet={'receiving_binding':{'receiving_body':'voice'},'evidence':[{'id':4}],
            'candidate':account('Delivery failed.',[4])}
    messages=[{'role':'system','content':'Fictional'}, {'role':'user','content':json.dumps(packet)}]
    generation=nr.response_schema('narrative_generation',messages)
    claim=generation['properties']['claims']['items']
    assert claim['properties']['text']['maxLength']==220
    assert claim['properties']['support']['items']['enum']==[4]
    assert generation['properties']['receiving_body']['enum']==['voice']
    review=nr.response_schema('narrative_review',messages)
    entry=review['properties']['claims']['items']
    assert review['properties']['claims']['minItems']==review['properties']['claims']['maxItems']==5
    proof=entry['properties']['assertions']['items']['properties']['proof']['items']
    assert proof['properties']['quote']['maxLength']==400
    assert proof['properties']['id']['enum']==[4]
    # API constraints supplement independent membership/meaning/coverage checks.
    with pytest.raises(ValueError,match='split compound'):
        nr.validate(account('x'*221,[4]),{4:{}},{'receiving_body':'voice'})
