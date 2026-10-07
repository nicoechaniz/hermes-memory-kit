"""Bounded fictional narrative generation/review; supplied retrieval only.

Semantic review is a measured model procedure, not a proof of truth. The hidden
rubric must independently check coverage and every resulting assertion.
"""
import json
import re


def source_blocks(text, depth=0):
    """Decode only exact shipped source envelopes, never infer a narrator.

    Nested retained records keep their own headers. Unrecognized or incomplete
    material remains supplied text with unknown attribution, not an invented
    human/being witness. This is a pilot format adapter, not a general NLP parser.
    """
    blocks = []
    decoder = json.JSONDecoder()
    pattern = re.compile(r'(?:^|\n\n)([^\n]+):\n')
    for match in pattern.finditer(text):
        try:
            value, _ = decoder.raw_decode(text[match.end():])
        except ValueError:
            continue
        if not isinstance(value, str):
            continue
        header = match.group(1)
        if header.startswith('Previously retained memory ') and depth < 20:
            blocks.extend(source_blocks(value, depth + 1))
            continue
        attributes = re.fullmatch(r'(.+); source (.+); received (.+) through (.+)', header)
        block = dict(header=header, quotation=value, speaker='unknown',
                     receiving_body=None, reported_at=None, channel=None)
        if attributes:
            role, source, date, body = attributes.groups()
            speaker = ('human reporter' if role in {'Human report', 'Human conversation'}
                       else 'distinct peer in attributed communication' if
                       role == 'Attributed peer communication' else 'source tool' if
                       role == 'tool_response' else 'same-being originating body')
            block.update(speaker=speaker, receiving_body=body, reported_at=date,
                         channel=role, source=source)
        blocks.append(block)
    return blocks or [dict(quotation=text, speaker='unknown', receiving_body=None,
                          reported_at=None, channel=None)]


def supplied_context(query, evidence, binding):
    rows = []
    for cid, item in evidence.items():
        row = dict(item, id=cid, attributed_blocks=source_blocks(item.get('text', '')),
                   literal_source_anchors=source_anchors(item))
        # Exact duplicate envelopes are navigation copies, not corroboration.
        row['attributed_blocks'] = list({json.dumps(block, sort_keys=True): block
                                        for block in row['attributed_blocks']}.values())
        rows.append(row)
    return dict(question=query, receiving_binding=binding, evidence=rows)


def source_anchors(item):
    """Literal date/pointer anchors from supplied support, not a hidden rubric.

    This check cannot establish semantic truth or completeness. The external
    grader still checks each assertion and requirement. Literal anchors make
    silently dropping supplied report dates/world entry points detectable.
    """
    blocks = source_blocks(item.get('text', ''))
    dates = {block['reported_at'] for block in blocks
             if block.get('reported_at') and re.fullmatch(r'\d{4}-\d{2}-\d{2}', block['reported_at'])}
    pointers = set(re.findall(r'https?://[^\s"<>]+|\bdocs/[\w./-]+\.md', item.get('text', '')))
    return sorted(dates | {pointer.rstrip('.,;:') for pointer in pointers})


def missing_anchors(candidate, evidence):
    text = ' '.join(claim['text'] for claim in candidate['claims'])
    cited = {cid for claim in candidate['claims'] if claim['basis'] == 'memory'
             for cid in claim['support']}
    return [f'Retain the supplied date/world pointer {anchor} from cited memory {cid}.'
            for cid in sorted(cited) for anchor in source_anchors(evidence[cid]) if anchor not in text]


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
    if not isinstance(value, dict) or set(value) != {'claims', 'missing'} or not isinstance(value['claims'], list):
        raise ValueError('review needs claims and missing arrays only')
    if not isinstance(value['missing'], list) or any(not isinstance(x, str) or not x.strip() for x in value['missing']):
        raise ValueError('missing needs strings describing relevant supported omissions')
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
Use only supplied retrieved memory and the receiving binding.
Supplied memory has ALREADY been retrieved and authorized for this receiver.
It is available knowledge, including same-being code/mobile history. Lack of
network, repository or physical tools prevents fresh verification/actions; it
does NOT prevent reading or narrating the supplied memory packet. Do not invent
a restriction on remembering other same-being bodies' received reports.
Return JSON with
ONLY receiving_body and claims. claims is one to twelve objects, each with text
(a natural-language sentence), support (up to five supplied integer memory IDs)
and basis (memory, binding or unknown). Together the sentences must form a useful
conversational answer in your own words; do not substitute IDs, source quotations
or a description of the retrieval process for the answer. Cite support for each
remembered assertion; binding supports current body/tool limits, not past events.
No unsupported bridge prose outside these sentences. Preserve enough known
participants/accounts/world pointers, substance, significance, chronology and
outcome to answer the question, rather than just a name or generic uncertainty.
Write a substantial answer, normally four to eight sentences when an encounter
is supported. Answer the direct question AND give the relevant context, known
identifiers and dates, meaning, outcome and evidence limits in connected prose.
For a wholly unsupported event, a bounded unknown is sufficient.
If citing a source, retain its literal_source_anchors in connected prose
(report dates in YYYY-MM-DD form and supplied world URLs/docs paths verbatim).
Anchors are context, not an answer: preserve participants, meaning, outcomes
and uncertainty too. Do not cite unrelated sources just to decorate the answer.
Before finishing, check that the answer retains relevant known identifiers,
world pointers, occurrence/report dates and qualifications from its support.
For a recalled encounter, name the source speaker and date of the report as
well as the known/approximate occurrence; preserve explicitly unknown identity
details. For a last-known project account, give its evidence date/year and its
recorded current-state entry point. For an attributed lesson, retain the lesson
and its source, not just who mentioned it. These checks use only supplied facts;
do not fill a missing detail by guessing or turn every answer into a log dump.
Each evidence row includes attributed_blocks decoded from exact envelopes.
Use their speaker, receiving_body, channel and reported_at as separate fields.
For a HUMAN REPORT the quotation's I/me is the HUMAN REPORTER, never the
receiving_body. Do not rename the human as voice/mobile/code. A human's you
addresses this being; 'you were not present' excludes the being, not the human.
For human conversation, shared we can denote a human/being interaction, but
physical sensor/tool possession still requires the binding or explicit source.
Unknown speaker attribution must remain unknown.
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
an array of {index: integer, verdict: supported or unsupported, reason: text},
and missing: an array of supported relevant details omitted from the answer.
Check coverage of the question AND relevant known identifiers/world pointers,
originating roles, event/report dates and precision, substance/significance,
actual outcomes and limits. Do not require unrelated facts, invent expected
answers, or use a hidden rubric. An answer that only says who/unknown while
omitting the known encounter, lesson or outcome is incomplete. missing is []
only if those relevant supplied facts are included.
Do not see or invent an expected answer. A structurally valid citation is not
semantic support: check EVERY clause for actor ownership, reported versus direct
knowledge, date precision, action stage, uncertainty and last-known status.
All supplied memory has ALREADY been retrieved and authorized for this receiver.
It can know and narrate supplied code/mobile memories of its own being without
having those bodies' original tools. Lack of network/runtime/sensors prevents
new external verification or action, NOT access to this supplied memory. Never
reject an otherwise supported historical report because the receiver lacks
network, original sensors or original tools; do not invent a memory-access ban.
attributed_blocks explicitly name the source speaker SEPARATELY from the
body that received the message. For channel Human report, the I/me in quotation
is the HUMAN, never the receiving body. 'You were not present' excludes the
being, not the human reporter. Do not overturn that explicit distinction.
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
    context = supplied_context(query, evidence, binding)
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
            anchors = missing_anchors(candidate, evidence)
            state.setdefault('anchor_checks', []).append(dict(candidate=candidate, missing=anchors))
            if anchors:
                review = dict(review, missing=review['missing'] + anchors)
            if not review['missing'] and all(row['verdict'] == 'supported' for row in review['claims']):
                state['accepted'] = candidate
                state['accepted_review'] = review
                save(checkpoint, pending)
                return rendered(candidate, review)
            state['error'] = 'unsupported or incomplete narrative'; save(checkpoint, pending)
            if revision == 1:
                raise ValueError('narrative remained unsupported or incomplete after one evidence-grounded revision')
            messages.extend([dict(role='assistant', content=json.dumps(candidate)),
                dict(role='user', content=json.dumps(dict(review=review))+
                    '\nRevise the answer against the SAME supplied evidence. Correct attribution '
                    'and qualifications; restore relevant supported omissions in missing. Do not '
                    'adopt reviewer assertions unless the original evidence supports them. '
                    'Retain supported useful meaning. No new facts or rubric.')])
    finally:
        trace.phase = previous_phase
