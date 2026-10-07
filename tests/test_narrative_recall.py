"""Narrative review must retain failed attempts and cannot fabricate support IDs."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

spec=importlib.util.spec_from_file_location('narrative_fixture',
    Path(__file__).resolve().parents[1]/'research/agent-memory-2026-10-06/pilots/narrative_recall.py')
nr=importlib.util.module_from_spec(spec);spec.loader.exec_module(nr)


def test_claim_support_and_complete_review_are_required():
    body={'receiving_body':'voice'}
    candidate={'receiving_body':'voice','claims':[{'text':'Jo was invited.', 'support':[1],'basis':'memory'}]}
    assert nr.validate(candidate,{1:{}},body)==candidate
    candidate['claims'][0]['support']=[99]
    with pytest.raises(ValueError):nr.validate(candidate,{1:{}},body)
    with pytest.raises(ValueError):nr.review_shape({'claims':[]},1)
    with pytest.raises(ValueError):nr.review_shape({'claims':[
        {'index':0,'verdict':'supported','reason':'ok'},
        {'index':0,'verdict':'supported','reason':'ok'}]},2)


def test_false_nonreceipt_is_revised_and_cost_phases_and_originals_stay(tmp_path):
    body={'receiving_body':'voice'}
    unsupported={'receiving_body':'voice','claims':[{'text':'Jo did not receive it.','support':[1],'basis':'memory'}]}
    corrected={'receiving_body':'voice','claims':[{'text':'Delivery failed; no reply was observed.','support':[1],'basis':'memory'}]}
    responses=iter([unsupported,{'claims':[{'index':0,'verdict':'unsupported','reason':'Unobserved receipt is not non-receipt.'}]},
        corrected,{'claims':[{'index':0,'verdict':'supported','reason':'Preserves observed failure and uncertainty.'}]}])
    phases=[];trace=SimpleNamespace(phase='recall')
    def chat(model,messages,trace):
        assert 'SECRET_RUBRIC' not in json.dumps(messages)
        phases.append(trace.phase);return next(responses)
    pending={};path=tmp_path/'pending.json'
    save=lambda path,value:path.write_text(json.dumps(value))
    value=nr.answer('fixture','Did Jo get it?',{1:{'text':'Delivery failed; no reply observed.'}},
        body,trace,pending,path,chat,save)
    assert value['text']==corrected['claims'][0]['text']
    assert value['review_is_proof'] is False
    assert pending['narrative']['generations'][0]==unsupported
    assert phases==['narrative_generation','narrative_review','narrative_revision','narrative_review']
    assert trace.phase=='recall'
    # A crash after accepted review must not repeat model calls on resumption.
    assert nr.answer('fixture','Did Jo get it?',{1:{}},body,trace,pending,path,chat,save)==value


def test_twice_unsupported_narrative_preserves_pending_instead_of_claiming_success(tmp_path):
    body={'receiving_body':'voice'}
    candidate={'receiving_body':'voice','claims':[{'text':'Jo received it.','support':[1],'basis':'memory'}]}
    responses=iter([candidate,{'claims':[{'index':0,'verdict':'unsupported','reason':'No receipt.'}]},
                    candidate,{'claims':[{'index':0,'verdict':'unsupported','reason':'Still no receipt.'}]}])
    pending={};path=tmp_path/'pending.json';trace=SimpleNamespace(phase='recall')
    with pytest.raises(ValueError,match='remained unsupported'):
        nr.answer('fixture','Did Jo get it?',{1:{}},body,trace,pending,path,
                  lambda *args:next(responses),lambda path,value:path.write_text(json.dumps(value)))
    saved=json.loads(path.read_text())
    assert len(saved['narrative']['generations'])==2
    assert 'accepted' not in saved['narrative']
    assert trace.phase=='recall'
