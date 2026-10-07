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


def verdict(status, reason, missing=None):
    return {'missing':missing or [], 'claims':[
        {'index':index,'verdict':status if index==0 else 'supported',
         'reason':reason if index==0 else 'Scoped to this test packet.'} for index in range(5)]}



def test_claim_support_and_complete_review_are_required():
    body={'receiving_body':'voice'}
    candidate=account('Jo was invited.',[1])
    assert nr.validate(candidate,{1:{}},body)==candidate
    candidate['claims'][0]['support']=[99]
    with pytest.raises(ValueError):nr.validate(candidate,{1:{}},body)
    with pytest.raises(ValueError):nr.review_shape({'missing':[], 'claims':[]},1)
    with pytest.raises(ValueError):nr.review_shape({'missing':[], 'claims':[
        {'index':0,'verdict':'supported','reason':'ok'},
        {'index':0,'verdict':'supported','reason':'ok'}]},2)


def test_false_nonreceipt_is_revised_and_cost_phases_and_originals_stay(tmp_path):
    body={'receiving_body':'voice'}
    unsupported=account('Jo did not receive it.',[1])
    corrected=account('Delivery failed; no reply was observed.',[1])
    responses=iter([unsupported,verdict('unsupported','Unobserved receipt is not non-receipt.'),
        corrected,verdict('supported','Preserves observed failure and uncertainty.')])
    phases=[];trace=SimpleNamespace(phase='recall')
    def chat(model,messages,trace):
        assert 'SECRET_RUBRIC' not in json.dumps(messages)
        phases.append(trace.phase);return next(responses)
    pending={};path=tmp_path/'pending.json'
    save=lambda path,value:path.write_text(json.dumps(value))
    value=nr.answer('fixture','Did Jo get it?',{1:{'text':'Delivery failed; no reply observed.'}},
        body,trace,pending,path,chat,save)
    assert value['text'].startswith(corrected['claims'][0]['text'])
    assert value['review_is_proof'] is False
    assert pending['narrative']['generations'][0]==unsupported
    assert phases==['narrative_generation','narrative_review','narrative_revision','narrative_review']
    assert trace.phase=='recall'
    # A crash after accepted review must not repeat model calls on resumption.
    assert nr.answer('fixture','Did Jo get it?',{1:{}},body,trace,pending,path,chat,save)==value


def test_bounded_unsupported_narrative_preserves_pending_instead_of_claiming_success(tmp_path):
    body={'receiving_body':'voice'}
    candidate=account('Jo received it.',[1])
    responses=iter([candidate,verdict('unsupported','No receipt.'),
                    candidate,verdict('unsupported','Still no receipt.'),
                    candidate,verdict('unsupported','Still no receipt.')])
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
    responses=iter([first,verdict('supported','Supported but incomplete.',['Reported connector lesson.']),
        final,verdict('supported','Includes lesson.')])
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
