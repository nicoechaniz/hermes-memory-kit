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
    with pytest.raises(ValueError,match='empty initial pack'):
        pilot.recall_plan({},set(),require_refinement=True)
    assert pilot.recall_plan({'queries':['arrival evidence']},set(),require_refinement=True)=={
        'queries':['arrival evidence'],'expand_ids':[]}


def test_pipeline_accepts_typed_source_projection_and_rejects_tampered_prose(pilot):
    evidence={1:{'text':'The checks require runtime tools.'}}
    binding={'receiving_body':'voice','repository_runtime_access':False}
    candidate={'receiving_body':'voice','claims':[dict(text='The checks require runtime tools, which I lack here.',
        basis='binding',support=[],facet='limits')]}
    atoms=[dict(span='The checks require runtime tools,',basis='memory',source_fact=evidence[1]['text'],
        proof=[{'id':1,'quote':evidence[1]['text']}],binding_fields=[]),
        dict(span=' which I lack here.',basis='binding',source_fact='Current runtime access is false.',
        proof=[],binding_fields=['repository_runtime_access'])]
    for a in atoms:a.update(verdict='supported',reason='Actual supplied source.')
    review={'claims':[dict(index=0,verdict='supported',reason='Supported clauses.',assertions=atoms)],'missing':[]}
    state={'narrative':dict(accepted=candidate,accepted_review=review)}
    answer=dict(pilot.narrative_recall.supported_claims(candidate,review),used_ids=[1],
        text=candidate['claims'][0]['text'],semantic_review=review,review_is_proof=False,support_protocol='assertions/v2')
    assert pilot.verify_narrative_answer(answer,state,evidence,binding)==answer
    with pytest.raises(ValueError,match='accepted candidate/review'):
        pilot.verify_narrative_answer(answer,{},evidence,binding)
    answer['claims'][0]['text']='The checks already passed.'
    with pytest.raises(ValueError,match='accepted source projection'):
        pilot.verify_narrative_answer(answer,state,evidence,binding)


def test_temporal_metadata_preserves_native_null_and_full_expansion_precedence(pilot):
    packs=[{'items':[{'id':1,'spr':'Preview','event_ts':99,
                     'neighbors':[{'id':2,'spr':'Neighbor','event_ts':0}]}]}]
    full=[{'id':1,'raw':'Original quotation with an approximate date.','event_ts':None}]
    ordinary=pilot.answer_evidence(packs,full)
    enriched=pilot.answer_evidence(packs,full,True)
    assert all('temporal_metadata'not in row for row in ordinary.values())
    assert enriched[1]['text']==ordinary[1]['text']==full[0]['raw']
    assert enriched[1]['temporal_metadata']['native_event_ts']is None
    assert enriched[2]['temporal_metadata']['native_event_ts']==0
    assert 'Receipt order does not establish event order' in enriched[1]['temporal_metadata']['ordering']


def test_temporal_metadata_does_not_invent_an_unavailable_native_field(pilot):
    packs=[{'items':[{'id':1,'spr':'Received 2026-08-05.'}]}]
    assert 'temporal_metadata'not in pilot.answer_evidence(packs,[],True)[1]
    with pytest.raises(ValueError,match='explicit boolean'):
        pilot.answer_evidence(packs,[],'yes')


def test_joint_projection_is_bound_to_selected_procedure_and_preserves_sources(pilot,tmp_path):
    evidence={1:{'text':'Running the remembered checks requires runtime tools.'}}
    binding={'receiving_body':'voice','repository_runtime_access':False}
    candidate={'receiving_body':'voice','claims':[dict(text='I cannot run those checks here.',basis='binding',support=[],facet='limits')]}
    raw={'claims':[dict(index=0,verdict='supported',reason='Joint premises.',assertions=[dict(
        span=candidate['claims'][0]['text'],basis='memory',source_fact='Checks need tools; current runtime is unavailable.',
        proof=[{'id':1,'passage':0}],binding_fields=['repository_runtime_access'],verdict='supported',reason='Remembered dependency plus actual capability.')])],'missing':[]}
    state={}
    def chat(_model,_messages,trace):
        return raw if trace.phase=='narrative_review' else candidate
    result=pilot.narrative_recall.answer('fixture','Can you run the checks?',evidence,binding,
        SimpleNamespace(phase='recall'),state,tmp_path/'pending.json',chat,pilot.save,
        review_protocol='assertions',allow_joint_support=True,review_effort='medium')
    assert result['claims'][0]['basis']=='mixed' and result['claims'][0]['support']==[1]
    assert result['text']==candidate['claims'][0]['text']
    assert pilot.verify_narrative_answer(result,state,evidence,binding)==result
    forged_unknown=dict(result,unknown_premises_protocol='positive-presuppositions/v1')
    with pytest.raises(ValueError,match='unknown premise support'):
        pilot.verify_narrative_answer(forged_unknown,state,evidence,binding)
    state['narrative']['unknown_premises_protocol']='positive-presuppositions/v1'
    assert pilot.verify_narrative_answer(forged_unknown,state,evidence,binding)==forged_unknown
    del state['narrative']['unknown_premises_protocol']
    forged=dict(result,joint_support_protocol='other')
    with pytest.raises(ValueError,match='accepted procedure'):
        pilot.verify_narrative_answer(forged,state,evidence,binding)


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
    value=pilot.chat('fixture-model', [], trace)
    assert value == {'_invalid_json':'not JSON'}
    saved=json.loads(path.read_text())[0]
    assert saved['usage']['total_tokens'] == 42 and saved['response_content']=='not JSON'
    with pytest.raises(ValueError):pilot.recall_plan(value,set())


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
    responses = iter([{'queries':[], 'expand_ids':[1]}, {'receiving_body':'fixture:body:voice','answer':{
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


def test_source_review_precedes_commit_and_never_sees_hidden_rubric(pilot, tmp_path, monkeypatch):
    original = pilot.memory_at
    def isolated(path):
        memory = original(path)
        memory.backfill_embeddings = lambda: {'updated':0}
        memory.semantic_search = lambda *a, **k: []
        memory.rerank_provider_default = lambda: 'none'
        return memory
    monkeypatch.setattr(pilot, 'memory_at', isolated)
    args = SimpleNamespace(out=tmp_path, resume=False, model='fictional', receiving_model='fictional-receiver', consolidate=False, review_capture=True)
    corpus = {'fixture_context':{}, 'cases':[{'id':'report', 'sources':[
        {'id':'source','originating_body':'fixture:body:voice','content':'The human reports an encounter.'}],
        'expected':{'secret':'HIDDEN_RUBRIC'},'questions':[{'query':'HIDDEN_RECALL_QUESTION'}]}]}
    candidate = {'outcome':'applied','reason':'Meaningful encounter','records':[
        {'key':'event','operation':'add','shelf':'episodes','title':'Encounter',
         'raw':'We attended the encounter.'}], 'links':[]}
    corrected = json.loads(json.dumps(candidate))
    corrected['records'][0]['raw'] = 'The human reported an encounter; the receiving voice body did not attend.'
    responses = iter([candidate, corrected, {'queries':['encounter report'],'expand_ids':[]}, {'receiving_body':'fixture:body:voice','answer':{
        'identification':'Unknown','context':'A report','meaning':'Unknown','outcome':'Reported',
        'limits':'Not directly observed'},'used_ids':[]}])
    phases=[]
    def chat(model, messages, trace):
        phases.append(trace.phase)
        assert model == ('fictional' if trace.phase.startswith('capture') else 'fictional-receiver')
        if trace.phase.startswith('capture'):
            assert 'HIDDEN_' not in json.dumps(messages)
        if trace.phase == 'capture_review':
            with isolated(tmp_path/'test/memory').connect() as con:
                assert con.execute('SELECT COUNT(*) FROM chapters').fetchone()[0] == 0
        return next(responses)
    monkeypatch.setattr(pilot,'chat',chat)
    pilot.run_variant('test','',args,corpus)
    assert phases == ['capture','capture_review','recall','recall']
    records=json.loads((tmp_path/'test/selected-canon.json').read_text())
    assert records[0]['raw'] == corrected['records'][0]['raw']


def test_inflight_attempt_is_durable_with_unknown_usage(pilot, tmp_path):
    path=tmp_path/'trace.json'
    trace=pilot.Trace(path)
    trace.phase='capture_review'
    index=trace.begin({'requested_model':'fixture'})
    saved=json.loads(path.read_text())
    assert saved[index]['state']=='started' and saved[index]['usage'] is None
    trace.finish(index,{'state':'completed','usage':{'total_tokens':42}})
    assert len(json.loads(path.read_text())) == 1


def test_source_blocks_preserve_reporter_uncertainty_and_refuse_generated_facts(pilot):
    sources=[{'id':'report','channel':'human_message','originating_body':'fixture:voice',
              'received_at':'2026-06-15','content':'I met Leto in late May, I think. You were not present.'}]
    candidate={'outcome':'applied','reason':'A meaningful report','records':[
        {'key':'event','operation':'add','shelf':'episodes','title':'Leto',
         'source_ids':['report']}],'links':[]}
    result=pilot.source_decision(candidate,sources,[])
    text=result['records'][0]['raw']
    assert 'Human report' in text and 'through fixture:voice' in text
    assert sources[0]['content'] in text
    assert 'I (voice body)' not in text
    assert 'source_ids' not in result['records'][0]
    candidate['records'][0]['raw']='I attended.'
    with pytest.raises(ValueError):pilot.source_decision(candidate,sources,[])
    candidate['records'][0].pop('raw')
    candidate['records'][0]['source_ids']=['invented']
    with pytest.raises(ValueError):pilot.source_decision(candidate,sources,[])


def test_answer_cannot_select_its_body_from_remembered_provenance(pilot):
    value={'receiving_body':'fixture:body:code','answer':dict.fromkeys(
        ('identification','context','meaning','outcome','limits'),'Unknown'),'used_ids':[]}
    with pytest.raises(ValueError,match='supplied binding'):
        pilot.grounded_answer(value,set(),'fixture:body:voice')


def test_evidence_response_preserves_failed_outcome_and_refuses_narrative(pilot):
    pack={'items':[{'id':1,'spr':'Object created.', 'origin':{'kind':'capture'}}]}
    text='Object created. Delivery failed. No access or response observed.'
    evidence=pilot.answer_evidence([pack],[{'id':1,'raw':text}])
    binding={'receiving_body':'fixture:body:voice','physical_actuators':False}
    value={'receiving_body':'fixture:body:voice','answer':dict.fromkeys(
        ('identification','context','meaning','outcome','limits'),[1]),'used_ids':[1]}
    result=pilot.supported_answer(value,evidence,binding)
    assert result['evidence'][0]['text']==text
    assert result['evidence'][0]['representation']=='expanded_record'
    assert result['receiving_binding']==binding
    value['answer']['outcome']='Recipient did not receive it.'
    with pytest.raises(ValueError):pilot.supported_answer(value,evidence,binding)
    value['answer']['outcome']=[99]
    with pytest.raises(ValueError):pilot.supported_answer(value,evidence,binding)
    value['answer']['outcome']=[1]
    value['used_ids']=[]
    with pytest.raises(ValueError):pilot.supported_answer(value,evidence,binding)


def test_only_all_empty_facet_array_has_an_unambiguous_normalization(pilot):
    binding={'receiving_body':'fixture:body:voice'}
    value={'receiving_body':binding['receiving_body'],'answer':[[],[],[],[],[]],'used_ids':[]}
    result=pilot.supported_answer(value,{},binding)
    assert set(result['answer'])=={'identification','context','meaning','outcome','limits'}
    assert all(ids==[] for ids in result['answer'].values())
    assert value['answer']==[[],[],[],[],[]]
    value['answer']=[[1],[],[],[],[]]
    with pytest.raises(ValueError):pilot.supported_answer(value,{1:{}},binding)


@pytest.mark.parametrize('content', [None, '{"claims":[]'])
@pytest.mark.parametrize('budget', [2048,None])
def test_truncated_response_preserves_usage_bytes_and_explicit_reasoning_budget(pilot,tmp_path,monkeypatch,content,budget):
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def read(self,*args):
            return json.dumps({'model':'fixture', 'usage':{'total_tokens':6000},
                'choices':[{'message':{'content':content},'finish_reason':'length'}]}).encode()
    requests=[]
    def receive(request,**kwargs):
        requests.append(json.loads(request.data));return Response()
    monkeypatch.setattr(pilot.configuration,'read_env_key',lambda key:'fictional-key')
    monkeypatch.setattr(pilot.urllib.request,'urlopen',receive)
    trace=pilot.Trace(tmp_path/'trace.json');trace.phase='narrative_review'
    trace.narrative_reasoning_effort='high';trace.narrative_reasoning_budget=budget
    messages=[{'role':'system','content':'Fictional'}, {'role':'user','content':json.dumps({'evidence':[],
        'candidate':{'claims':[{'text':'Unknown here.'}]}})}]
    value=pilot.chat('fixture',messages,trace)
    assert value=={'_invalid_json':content,'_finish_reason':'length'}
    assert requests[0].get('reasoning_budget')==budget and requests[0]['max_tokens']==12000
    if budget is None:assert 'reasoning_budget' not in requests[0]
    assert requests[0]['response_format']['type']=='json_schema'
    assert requests[0]['response_format']['json_schema']['strict'] is True
    row=json.loads(trace.path.read_text())[0]
    assert row['usage']['total_tokens']==6000 and row['response_content']==content
    assert row['parse_error']=='incomplete_response' and row['requested_reasoning_budget']==budget
    assert row['requested_max_tokens']==12000
    assert row['response_format_sha256']==pilot.digest(requests[0]['response_format'])


def test_reader_upgrade_requires_explicit_comparable_formation(pilot):
    source=dict(model='fixture',baseline_commit='old',guidance_hashes={'proposed':'fixed'},
        fixture_hash='fictional',reasoning_effort='low',embedding_config={'provider':'fixed'},
        retrieval_profile='general',rerank_provider='none',review_capture=False,source_blocks=True,
        retrieval_sha256='old-reader')
    conditions=dict(source,retrieval_sha256='new-reader')
    with pytest.raises(ValueError,match='explicit'):
        pilot.formation_compatibility(source,conditions)
    assert pilot.formation_compatibility(source,conditions,True)['explicit_upgrade'] is True
    # Receiving is a new experiment over preserved formation, not recapture.
    assert pilot.formation_compatibility(source,dict(conditions,receiving_model='different-receiver'),True)['explicit_upgrade'] is True
    with pytest.raises(ValueError,match='identical'):
        pilot.formation_compatibility(source,dict(conditions,fixture_hash='different'),True)
    with pytest.raises(ValueError,match='identical'):
        pilot.formation_compatibility(source,dict(conditions,model='different-formation'),True)


def test_resume_cannot_change_receiving_model_or_rewrite_conditions(pilot,tmp_path,monkeypatch):
    corpus=tmp_path/'corpus.json';corpus.write_text(json.dumps({'fictional':True,'cases':[]}))
    output=tmp_path/'comparison';calls=[]
    def run(name,guidance,args,corpus):
        calls.append((name,args.model,args.receiving_model));return {'variant':name}
    monkeypatch.setattr(pilot,'run_variant',run)
    argv=['pilot','--out',str(output),'--corpus',str(corpus),'--model','fictional-formation',
          '--receiving-model','receiver-one']
    monkeypatch.setattr('sys.argv',argv);pilot.main()
    original=(output/'conditions.json').read_bytes()
    conditions=json.loads(original)
    assert conditions['model']=='fictional-formation' and conditions['receiving_model']=='receiver-one'
    monkeypatch.setattr('sys.argv',argv[:-1]+['receiver-two','--resume'])
    with pytest.raises(SystemExit):pilot.main()
    assert len(calls)==2 and (output/'conditions.json').read_bytes()==original
    assert pilot.optional_reasoning_budget('none') is None
    assert pilot.optional_reasoning_budget('2048')==2048


def test_formation_preservation_includes_originals_and_history(pilot,tmp_path):
    memory=pilot.memory_at(tmp_path/'memory')
    cid=memory.add_text('episodes','A shared moment','Original meaningful source.')
    original=pilot.formation_state(memory.DB_PATH)
    memory.update_chapter(cid,content='Original source plus dated correction.')
    changed=pilot.formation_state(memory.DB_PATH)
    assert changed['chapters']!=original['chapters']
    assert changed['chapter_revisions']['rows']>original['chapter_revisions']['rows']
