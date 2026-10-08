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
    # The bounded semantic rejection is terminal for this frozen comparison;
    # resuming cannot quietly grant another three generation rounds.
    def unexpected_call(*args):pytest.fail('Terminal rejection repeated a provider call.')
    with pytest.raises(nr.NarrativeRejected,match='two evidence-grounded revisions'):
        nr.answer('fixture','Did Jo get it?',{1:{}},body,trace,saved,path,
                  unexpected_call,lambda p,v:p.write_text(json.dumps(v)))


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
    action=nr.supplied_context('What did we try?',{1:{'text':source('foreground_action','code')}},binding)
    assert action['evidence'][0]['attributed_blocks'][0]['speaker']=='same-being originating body'


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


@pytest.mark.parametrize('facet', ['context', 'limits'])
def test_unrecorded_return_can_retain_older_context_without_inventing_an_episode(facet):
    candidate={'receiving_body':'voice','claims':[
        dict(text='The supplied memories do not record a return or who welcomed us.',
             support=[1],basis='unknown',facet='limits'),
        dict(text='The human report received September 12 describes their earlier meeting, which I did not attend.',
             support=[1],basis='memory',facet=facet)]}
    evidence={1:{'text':'The human reported the earlier meeting. The being was absent.'}}
    assert nr.validate(candidate,evidence,{'receiving_body':'voice'})==candidate
    # Structural acceptance neither approves the prose nor removes review.
    with pytest.raises(ValueError,match='review every claim'):
        nr.review_shape({'claims':[],'missing':[]},candidate,evidence)
    # A positive occurrence cannot hide behind the leading unknown's exception.
    candidate['claims'][1]['facet']='outcome'
    with pytest.raises(ValueError,match='all five facets'):
        nr.validate(candidate,evidence,{'receiving_body':'voice'})


def test_known_account_still_requires_meaning_outcome_and_limits():
    candidate={'receiving_body':'voice','claims':[
        dict(text='Our code body met the contributor in the issue.',support=[1],
             basis='memory',facet='context')]}
    with pytest.raises(ValueError,match='all five facets'):
        nr.validate(candidate,{1:{'text':'A known interaction.'}},{'receiving_body':'voice'})


def test_changed_validation_cannot_silently_requalify_an_accepted_checkpoint(tmp_path):
    import hashlib
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    binding={'receiving_body':'voice'};checkpoint=tmp_path/'pending.json';pending={}
    def chat(model,messages,trace):
        return candidate if trace.phase=='narrative_generation' else verdict(
            'supported','Actual failure.',candidate,'Delivery failed.')
    nr.answer('fixture','What happened?',evidence,binding,SimpleNamespace(phase='recall'),
              pending,checkpoint,chat,lambda p,v:p.write_text(json.dumps(v)))
    historical=dict(model='fixture',generation=nr.GENERATION,review=nr.REVIEW,
                    protocol='receiving-phase/v1')
    pending['narrative']['procedure_sha256']=hashlib.sha256(
        json.dumps(historical,sort_keys=True).encode()).hexdigest()
    checkpoint.write_text(json.dumps(pending));original=checkpoint.read_bytes()
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('fixture','What happened?',evidence,binding,SimpleNamespace(phase='recall'),
                  pending,checkpoint,lambda *a:pytest.fail('Unexpected model call'),
                  lambda p,v:p.write_text(json.dumps(v)))
    assert checkpoint.read_bytes()==original


def test_source_clause_delimiter_repair_preserves_raw_review_and_exact_words(tmp_path):
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed; no reply observed.'}}
    raw=verdict('supported','Observed failure.',candidate,'Delivery failed.')
    calls=[];pending={}
    def chat(model,messages,trace):
        calls.append(trace.phase)
        return candidate if trace.phase=='narrative_generation' else raw
    result=nr.answer('fixture','What happened?',evidence,{'receiving_body':'voice'},
        SimpleNamespace(phase='recall'),pending,tmp_path/'pending.json',chat,
        lambda p,v:p.write_text(json.dumps(v)))
    assert calls==['narrative_generation','narrative_review']
    row=pending['narrative']['reviews'][0]
    assert row['review']==raw and row['literal_quote_repairs'][0]['original_quote']=='Delivery failed.'
    assert result['semantic_review']['claims'][0]['assertions'][0]['proof'][0]['quote']=='Delivery failed;'
    assert evidence[1]['text']=='Delivery failed; no reply observed.' and result['claims']==candidate['claims']


@pytest.mark.parametrize('quote,source', [
    ('Delivery succeeded.','Delivery failed; no reply observed.'),
    ('Jo received it.','Jo received it? No confirmation was supplied.'),
    ('Delivery failed.','Delivery failed, if the report is accurate.')])
def test_quote_repair_cannot_change_words_or_question_conditional_punctuation(quote,source):
    candidate=account('Delivery failed.',[1]);raw=verdict('supported','Claimed support.',candidate,quote)
    canonical,repairs=nr.literal_review_quotes(raw,candidate,{1:{'text':source}})
    assert canonical==raw and repairs==[]
    with pytest.raises(ValueError,match='verbatim'):
        nr.review_shape(canonical,candidate,{1:{'text':source}})


def test_passage_review_materializes_original_source_and_preserves_model_output(tmp_path):
    evidence={1:{'text':'tool_response; source outreach; received unknown through code:\n'+
        json.dumps('Delivery failed; no reply observed.')}}
    passages=nr.proof_passages(evidence[1])
    assert passages[1]['quote']=='Delivery failed; no reply observed.'
    candidate=account('Delivery failed.',[1]);calls=[];pending={}
    raw=verdict('supported','Observed failure.',candidate)
    raw['claims'][0]['assertions'][0]['proof']=[{'id':1,'passage':1}]
    def chat(model,messages,trace):
        calls.append(trace.phase)
        if trace.phase=='narrative_generation':return candidate
        packet=json.loads(messages[1]['content'])
        assert packet['review_protocol']=='passages/v1'
        assert packet['evidence'][0]['proof_passages']==passages
        schema=nr.response_schema(trace.phase,messages)
        proof=schema['properties']['claims']['items']['properties']['assertions']['items']['properties']['proof']['items']
        assert set(proof['properties'])=={'id','passage'}
        return raw
    result=nr.answer('fixture','What happened?',evidence,{'receiving_body':'voice'},
        SimpleNamespace(phase='recall'),pending,tmp_path/'pending.json',chat,
        lambda p,v:p.write_text(json.dumps(v)),review_protocol='passages')
    assert calls==['narrative_generation','narrative_review'] and pending['narrative']['reviews'][0]['review']==raw
    assert result['semantic_review']['claims'][0]['assertions'][0]['proof'][0]['quote']=='Delivery failed; no reply observed.'
    assert result['claims']==candidate['claims']


@pytest.mark.parametrize('ref',[{'id':1,'passage':99},{'id':2,'passage':0},
    {'id':1,'quote':'Invented source text.'}])
def test_passage_proofs_cannot_forge_text_or_redirect_to_uncited_sources(ref):
    candidate=account('Delivery failed.',[1]);raw=verdict('supported','Claimed support.',candidate)
    raw['claims'][0]['assertions'][0]['proof']=[ref]
    with pytest.raises(ValueError,match='passage'):
        nr.passage_review(raw,candidate,{1:{'text':'Delivery failed.'},2:{'text':'Delivery succeeded.'}})


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


def test_review_timeout_resumes_saved_candidate_without_another_generation(tmp_path):
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    body={'receiving_body':'voice'};trace=SimpleNamespace(phase='recall')
    checkpoint=tmp_path/'pending.json';pending={};calls=[]
    def save(path,value):path.write_text(json.dumps(value))
    def first(model,messages,trace):
        calls.append(trace.phase)
        if trace.phase=='narrative_generation':return candidate
        raise TimeoutError('Provider response unavailable; usage unknown.')
    with pytest.raises(TimeoutError):
        nr.answer('fixture','What happened?',evidence,body,trace,pending,checkpoint,first,save)
    assert trace.phase=='recall'
    saved=json.loads(checkpoint.read_text())
    assert saved['narrative']['generations']==[candidate]
    assert saved['narrative']['reviews']==[]
    def resumed(model,messages,trace):
        calls.append(trace.phase)
        assert json.loads(messages[1]['content'])['candidate']==candidate
        return verdict('supported','Actual failed delivery.',candidate,'Delivery failed.')
    result=nr.answer('fixture','What happened?',evidence,body,trace,saved,checkpoint,resumed,save)
    assert result['claims']==candidate['claims']
    assert calls==['narrative_generation','narrative_review','narrative_review']
    assert saved['narrative']['generations']==[candidate]


@pytest.mark.parametrize('boundary', ['generation_validate','review_validate','assess'])
def test_persisted_response_or_assessment_is_not_called_again(tmp_path,boundary):
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    checkpoint=tmp_path/'pending.json';calls=[];interrupted=False
    def chat(model,messages,trace):
        calls.append(trace.phase)
        return candidate if trace.phase=='narrative_generation' else verdict(
            'supported','Failed delivery.',candidate,'Delivery failed.')
    def save(path,value):
        nonlocal interrupted
        path.write_text(json.dumps(value))
        if not interrupted and value['narrative']['progress']['phase']==boundary:
            interrupted=True
            raise RuntimeError('Process stopped after durable write.')
    trace=SimpleNamespace(phase='recall');body={'receiving_body':'voice'}
    with pytest.raises(RuntimeError):
        nr.answer('fixture','What happened?',evidence,body,trace,{},checkpoint,chat,save)
    assert trace.phase=='recall'
    saved=json.loads(checkpoint.read_text())
    nr.answer('fixture','What happened?',evidence,body,trace,saved,checkpoint,chat,save)
    assert calls==['narrative_generation','narrative_review']
    assert len(saved['narrative']['generations'])==len(saved['narrative']['reviews'])==1


def test_semantic_revision_retains_critique_and_its_budget_across_interruption(tmp_path):
    bad=account('Jo received it.',[1]);good=account('Delivery failed.',[1])
    evidence={1:{'text':'Delivery failed.'}};body={'receiving_body':'voice'}
    checkpoint=tmp_path/'pending.json';calls=[];interrupted=False
    def chat(model,messages,trace):
        calls.append(trace.phase)
        if trace.phase=='narrative_generation':return bad
        if trace.phase=='narrative_revision':
            assert 'Receipt unknown.' in json.dumps(messages)
            return good
        candidate=json.loads(messages[1]['content'])['candidate']
        return verdict('unsupported','Receipt unknown.',bad) if candidate==bad else verdict(
            'supported','Observed failure.',good,'Delivery failed.')
    def save(path,value):
        nonlocal interrupted
        path.write_text(json.dumps(value))
        p=value['narrative']['progress']
        if not interrupted and p['revision']==1 and p['phase']=='generation':
            interrupted=True;raise RuntimeError('Stopped before revision.')
    trace=SimpleNamespace(phase='recall')
    with pytest.raises(RuntimeError):
        nr.answer('fixture','Did Jo get it?',evidence,body,trace,{},checkpoint,chat,save)
    saved=json.loads(checkpoint.read_text())
    result=nr.answer('fixture','Did Jo get it?',evidence,body,trace,saved,checkpoint,chat,save)
    assert result['claims']==good['claims']
    assert calls==['narrative_generation','narrative_review','narrative_revision','narrative_review']
    assert saved['narrative']['generations']==[bad,good]


def test_terminal_rejection_does_not_reset_attempts_on_resume(tmp_path):
    candidate=account('Delivery failed.',[1]);checkpoint=tmp_path/'pending.json'
    responses=iter([candidate,{'bad':'review'}, {'bad':'review again'}]);calls=[]
    def chat(*args):calls.append(args[2].phase);return next(responses)
    save=lambda path,value:path.write_text(json.dumps(value))
    args=('fixture','What happened?',{1:{'text':'Delivery failed.'}},
          {'receiving_body':'voice'},SimpleNamespace(phase='recall'))
    with pytest.raises(nr.NarrativeRejected):nr.answer(*args,{},checkpoint,chat,save)
    saved=json.loads(checkpoint.read_text())
    with pytest.raises(nr.NarrativeRejected):nr.answer(*args,saved,checkpoint,chat,save)
    assert calls==['narrative_generation','narrative_review','narrative_review']
    assert len(saved['narrative']['generations'])==1 and len(saved['narrative']['reviews'])==2


def test_changed_model_and_legacy_unfinished_state_preserve_work(tmp_path):
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    checkpoint=tmp_path/'pending.json';body={'receiving_body':'voice'}
    trace=SimpleNamespace(phase='recall');save=lambda p,v:p.write_text(json.dumps(v))
    def chat(model,messages,trace):
        if trace.phase=='narrative_generation':return candidate
        raise TimeoutError('Pending review.')
    with pytest.raises(TimeoutError):
        nr.answer('fixture','What happened?',evidence,body,trace,{},checkpoint,chat,save)
    saved=json.loads(checkpoint.read_text());original=checkpoint.read_bytes()
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('different','What happened?',evidence,body,trace,saved,checkpoint,chat,save)
    assert checkpoint.read_bytes()==original
    legacy={'narrative':{'generations':[candidate],'reviews':[]}}
    with pytest.raises(ValueError,match='legacy narrative checkpoint'):
        nr.answer('fixture','What happened?',evidence,body,trace,legacy,checkpoint,chat,save)
    assert checkpoint.read_bytes()==original and legacy['narrative']['generations']==[candidate]


def test_distinct_reviewer_resumes_timeout_without_changing_narrator_or_budget(tmp_path):
    candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    body={'receiving_body':'voice'};path=tmp_path/'pending.json';pending={};calls=[]
    save=lambda p,v:p.write_text(json.dumps(v));trace=SimpleNamespace(phase='recall')
    def chat(model,messages,trace):
        calls.append((model,trace.phase))
        if trace.phase=='narrative_generation':return candidate
        if len(calls)==2:raise TimeoutError('review pending')
        return verdict('supported','Actual failure.',candidate,'Delivery failed.')
    with pytest.raises(TimeoutError):
        nr.answer('narrator','What happened?',evidence,body,trace,pending,path,chat,save,
                  review_model='reviewer')
    original=path.read_bytes();saved=json.loads(original)
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('narrator','What happened?',evidence,body,trace,saved,path,chat,save,
                  review_model='changed-reviewer')
    assert path.read_bytes()==original and len(calls)==2
    result=nr.answer('narrator','What happened?',evidence,body,trace,saved,path,chat,save,
                     review_model='reviewer')
    assert result['claims']==candidate['claims']
    assert calls==[('narrator','narrative_generation'),('reviewer','narrative_review'),
                   ('reviewer','narrative_review')]


def test_reviewer_critique_returns_revisions_to_original_narrator(tmp_path):
    bad=account('Jo received it.',[1]);good=account('Delivery failed.',[1]);calls=[]
    def chat(model,messages,trace):
        calls.append((model,trace.phase))
        if trace.phase=='narrative_generation':return bad
        if trace.phase=='narrative_revision':return good
        candidate=json.loads(messages[1]['content'])['candidate']
        return verdict('unsupported','No receipt.',candidate) if candidate==bad else verdict(
            'supported','Actual failure.',candidate,'Delivery failed.')
    value=nr.answer('narrator','What happened?',{1:{'text':'Delivery failed.'}},
        {'receiving_body':'voice'},SimpleNamespace(phase='recall'),{},tmp_path/'pending.json',
        chat,lambda p,v:p.write_text(json.dumps(v)),review_model='reviewer')
    assert value['claims']==good['claims']
    assert calls==[('narrator','narrative_generation'),('reviewer','narrative_review'),
                   ('narrator','narrative_revision'),('reviewer','narrative_review')]


def test_frozen_revision_role_routes_correction_without_repeating_initial_model(tmp_path):
    body={'receiving_body':'voice'}
    first=account('Jo received it.',[1])
    final=account('Delivery failed.',[1])
    evidence={1:{'text':'Delivery failed.'}}
    responses=iter([first,verdict('unsupported','Receipt unsupported.',first),
                    final,verdict('supported','Actual failure.',final,'Delivery failed.')])
    calls=[]
    def chat(model,messages,trace):
        calls.append((model,trace.phase));return next(responses)
    pending={};save=lambda p,v:p.write_text(json.dumps(v));path=tmp_path/'pending.json'
    value=nr.answer('initial','Did Jo get it?',evidence,body,SimpleNamespace(phase='recall'),
                    pending,path,chat,save,review_model='reviewer',revision_model='corrector')
    assert value['claims'][0]['text']=='Delivery failed.'
    assert calls==[('initial','narrative_generation'),('reviewer','narrative_review'),
                   ('corrector','narrative_revision'),('reviewer','narrative_review')]
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('initial','Did Jo get it?',evidence,body,SimpleNamespace(phase='recall'),
                    pending,path,chat,save,review_model='reviewer',revision_model='other')
    assert len(calls)==4


def test_decoded_context_preserves_complete_nested_sources_and_provenance():
    quote='I met Neri at the shed; you were not with me.\nNo extra handle was supplied.'
    original='Human report; source mending; received 2026-09-12 through mobile:\n'+json.dumps(quote)
    text='Previously retained memory 4, revision 1:\n'+json.dumps(original)+'\n\n'+original
    evidence={4:dict(text=text,origin={'kind':'native','source':{'mode':'reported'}},support_status='current')}
    full=nr.supplied_context('What did the human report?',evidence,{'receiving_body':'voice'})
    lean=nr.supplied_context('What did the human report?',evidence,{'receiving_body':'voice'},'decoded')
    row=lean['evidence'][0]
    assert row['attributed_blocks']==full['evidence'][0]['attributed_blocks']
    assert row['attributed_blocks'][0]['quotation']==quote
    assert row['origin']==evidence[4]['origin'] and row['support_status']=='current'
    assert row['source_text_sha256']==nr.hashlib.sha256(text.encode()).hexdigest()
    assert 'text' not in row and len(json.dumps(lean))<len(json.dumps(full))
    assert evidence[4]['text']==text  # Retrieval originals and proof checking stay unchanged.


@pytest.mark.parametrize('kind',['prefix','suffix','nested-prefix','broken'])
def test_decoded_context_keeps_every_mixed_or_malformed_source_byte(kind):
    original='Human report; source encounter; received 2026-09-12 through mobile:\n'+json.dumps('Neri proposed a method.')
    text={'prefix':'Extra significant fact.\n\n'+original,
          'suffix':original+'\n\nExtra significant fact.',
          'nested-prefix':'Previously retained memory 4, revision 1:\n'+json.dumps('Extra significant fact.\n\n'+original),
          'broken':original+'\n\nHuman report; source later:\n"incomplete'}[kind]
    assert not nr.complete_source_envelopes(text)
    result=nr.supplied_context('What happened?',{4:{'text':text}},{'receiving_body':'voice'},'decoded')
    assert result['evidence'][0]['text']==text


def test_decoded_representation_cannot_reuse_full_context_checkpoint(tmp_path):
    body={'receiving_body':'voice'};candidate=account('Delivery failed.',[1]);evidence={1:{'text':'Delivery failed.'}}
    responses=iter([candidate,verdict('supported','Actual failure.',candidate,'Delivery failed.')]);calls=[]
    def chat(model,messages,trace):calls.append(trace.phase);return next(responses)
    save=lambda p,v:p.write_text(json.dumps(v));pending={};path=tmp_path/'pending.json'
    nr.answer('model','What happened?',evidence,body,SimpleNamespace(phase='recall'),pending,path,chat,save)
    before=path.read_bytes()
    with pytest.raises(ValueError,match='procedure/model changed'):
        nr.answer('model','What happened?',evidence,body,SimpleNamespace(phase='recall'),pending,path,chat,save,source_representation='decoded')
    assert path.read_bytes()==before and len(calls)==2
