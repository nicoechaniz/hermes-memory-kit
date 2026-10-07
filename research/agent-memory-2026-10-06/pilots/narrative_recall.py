"""Bounded fictional narrative generation/review; supplied retrieval only.

Semantic review is a measured model procedure, not a proof of truth. The hidden
rubric must independently check coverage and every resulting assertion.
"""
import json


def validate(value, evidence, binding):
    if not isinstance(value, dict) or set(value) != {'receiving_body', 'claims'}:
        raise ValueError('return receiving_body and claims only')
    if value['receiving_body'] != binding['receiving_body']:
        raise ValueError('receiving_body must match the supplied binding')
    claims = value['claims']
    if not isinstance(claims, list) or not claims or len(claims) > 12:
        raise ValueError('claims needs one to twelve natural-language sentences')
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != {'text', 'support', 'basis'}:
            raise ValueError('each claim needs text, support and basis only')
        if not isinstance(claim['text'], str) or not claim['text'].strip():
            raise ValueError('claim text must be nonempty natural-language prose')
        if claim['basis'] not in {'memory', 'binding', 'unknown'}:
            raise ValueError('basis is memory, binding or unknown')
        ids = claim['support']
        if not isinstance(ids, list) or len(ids) > 5 or any(
                type(cid) is not int or cid not in evidence for cid in ids):
            raise ValueError('support needs at most five supplied memory IDs')
        if claim['basis'] == 'memory' and not ids:
            raise ValueError('remembered assertions need supplied evidence')
    return value


def review_shape(value, count):
    if not isinstance(value, dict) or set(value) != {'claims'} or not isinstance(value['claims'], list):
        raise ValueError('review needs a claims array only')
    if len(value['claims']) != count:
        raise ValueError('review every claim exactly once')
    indices = []
    for row in value['claims']:
        if not isinstance(row, dict) or set(row) != {'index', 'verdict', 'reason'}:
            raise ValueError('review entries need index, verdict and reason')
        if type(row['index']) is not int or row['verdict'] not in {'supported', 'unsupported'}:
            raise ValueError('review needs integer indices and supported/unsupported verdicts')
        if not isinstance(row['reason'], str) or not row['reason'].strip():
            raise ValueError('each review verdict needs a reason')
        indices.append(row['index'])
    if sorted(indices) != list(range(count)):
        raise ValueError('review indices must cover the actual claims once')
    return value


GENERATION = '''Answer as the current body of the supplied fictional being.
Use only supplied retrieved memory and the receiving binding. Return JSON with
ONLY receiving_body and claims. claims is one to twelve objects, each with text
(a natural-language sentence), support (up to five supplied integer memory IDs)
and basis (memory, binding or unknown). Together the sentences must form a useful
conversational answer in your own words; do not substitute IDs, source quotations
or a description of the retrieval process for the answer. Cite support for each
remembered assertion; binding supports current body/tool limits, not past events.
No unsupported bridge prose outside these sentences. Preserve enough known
participants/accounts/world pointers, substance, significance, chronology and
outcome to answer the question, rather than just a name or generic uncertainty.
Distinguish source speaker, body receiving a report and event participants.
A human's quoted I is the human. Another body of this being carries our shared
history, but another being's experience remains theirs. Explain which original
body participated where relevant; current abilities come only from the binding.
Receipt of a report is not physical attendance. Distinguish observation, report,
inference and intention; preserve source uncertainty and approximate/unknown
occurrence dates separately from report dates. Relative dates can be explained
relative to the dated report; do not invent an exact occurrence from import time.
Do not strengthen action stages, causal explanations or success. A created
object is not delivery, unobserved access is not proof of non-receipt, and an
attempt/intention is not agreement or attendance. State the observed failure
when supplied; qualify absence as lack of observed evidence. Dated project state
is last-known, not current: give the recorded pointer for checking present state.
Keep previous tentative attribution and later corrections distinct.
An unknown detail does not erase the known qualified encounter. Answer negative
questions with explicit scoped uncertainty, not a guessed fact or proof that an
event never happened. Do not invent simulation, deployment, causality, identities,
abilities, private access or a performed learning solely to make a smooth story.
'''

REVIEW = '''Review every sentence against its cited supplied memory and the
receiving binding. Candidate prose is not evidence. Return ONLY JSON with claims:
an array of {index: integer, verdict: supported or unsupported, reason: text}.
Do not see or invent an expected answer. A structurally valid citation is not
semantic support: check EVERY clause for actor ownership, reported versus direct
knowledge, date precision, action stage, uncertainty and last-known status.
Quoted human I/we remains its speaker; receiving a report does not establish
participation or a preference of the receiving body. Same-being body history
does not grant the receiver sensors/tools. Distinct peers remain distinct.
Do not accept a stronger outcome, causal explanation or invented simulation.
Unobserved receipt/access does not prove the recipient did not obtain something;
no acceptance/attendance observed is not proof no meeting occurred. Known delivery
or validation failure can be stated as the actual observed failure. Historical
corrections must not make the old uncertain attribution certain or erase it.
Unknown claims with no cited support must be scoped to supplied memory, never a
universal negative; use source-qualified unknowns when available. Binding claims
must match actual receiving abilities and cannot assert past events.
If any factual clause exceeds its support, mark that sentence unsupported and
explain the precise mismatch. Review is not independent corroboration and may
not add sources or new observations.
'''


def answer(model, query, evidence, binding, trace, pending, checkpoint, chat, save):
    state = pending.setdefault('narrative', {'generations': [], 'reviews': []})
    def rendered(candidate, review):
        return dict(candidate, text=' '.join(claim['text'] for claim in candidate['claims']),
            used_ids=list(dict.fromkeys(cid for c in candidate['claims'] for cid in c['support'])),
            semantic_review=review, review_is_proof=False)
    if 'accepted' in state:
        validate(state['accepted'], evidence, binding)
        review_shape(state['accepted_review'], len(state['accepted']['claims']))
        return rendered(state['accepted'], state['accepted_review'])
    context = dict(question=query, receiving_binding=binding, evidence=list(evidence.values()))
    messages = [dict(role='system', content=GENERATION),
                dict(role='user', content=json.dumps(context, ensure_ascii=False))]
    previous_phase = trace.phase
    try:
        for revision in range(2):
            trace.phase = 'narrative_generation' if revision == 0 else 'narrative_revision'
            for repair in range(2):
                candidate = chat(model, messages, trace)
                state['generations'].append(candidate)
                save(checkpoint, pending)
                try:
                    validate(candidate, evidence, binding)
                except ValueError as error:
                    state['error'] = str(error); save(checkpoint, pending)
                    if repair == 1: raise
                    messages.extend([dict(role='assistant', content=json.dumps(candidate)),
                        dict(role='user', content='Invalid structure: '+str(error)+
                            '. Repair API shape only; preserve supported meaning. No rubric.')])
                else: break
            trace.phase = 'narrative_review'
            review_messages = [dict(role='system', content=REVIEW), dict(role='user',
                content=json.dumps(dict(context, candidate=candidate), ensure_ascii=False))]
            for repair in range(2):
                review = chat(model, review_messages, trace)
                state['reviews'].append(dict(candidate=candidate, review=review))
                save(checkpoint, pending)
                try:
                    review_shape(review, len(candidate['claims']))
                except ValueError as error:
                    state['error'] = str(error); save(checkpoint, pending)
                    if repair == 1: raise
                    review_messages.extend([dict(role='assistant', content=json.dumps(review)),
                        dict(role='user', content='Invalid review shape: '+str(error)+'. Repair only shape.')])
                else: break
            if all(row['verdict'] == 'supported' for row in review['claims']):
                state['accepted'] = candidate
                state['accepted_review'] = review
                save(checkpoint, pending)
                return rendered(candidate, review)
            state['error'] = 'unsupported narrative claims'; save(checkpoint, pending)
            if revision == 1:
                raise ValueError('narrative remained unsupported after one evidence-grounded revision')
            messages.extend([dict(role='assistant', content=json.dumps(candidate)),
                dict(role='user', content=json.dumps(dict(review=review))+
                    '\nRevise the answer against the SAME supplied evidence. Correct attribution '
                    'and qualifications; retain supported useful meaning. No new facts or rubric.')])
    finally:
        trace.phase = previous_phase
