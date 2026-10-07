# R3 — Experience, relationships and multimodal continuity

Status: `complete`. Research cutoff and access date: 2026-10-06.

Raw report for lane `[R3]`; completed content is preserved for additive
consolidation. Confidence marks follow the MANIFEST: ✅ inspected primary
description, 📊 author/vendor measurement, ⚠️ experimental proposal,
❓ our recommendation requiring validation.

## 0. TL;DR

- ✅ Hindsight explicitly separates retained experience from consolidated
  understanding; its primary paper uses occurrence intervals and mention times.
- ✅ Honcho's directional representations preserve an observer–subject pair,
  with conclusions restricted to sessions that observer participated in.
- ✅ Multimodal episodic-KG research distinguishes a speaker's claim from a
  sensor's detection and associates interpretations with modality/time/context.
- 📊 A human–agent memory co-construction pilot reports failures around
  complement versus conflict, implied meaning and significance. Synthesis does
  not justify silently replacing a source viewpoint.
- ❓ HMK should keep self-contained selected episodes, linked current accounts
  and explicitly inferential patterns as related but distinct records. Ordinary
  moments can be significant without producing a stable trait or task outcome.
- ❓ Import the contracts and evaluate them on HMK before adopting a service:
  source modes, identities, dates, revisions and evidence must survive storage,
  consolidation, recall and loss of the original session.

## Research question and scope

Which primary evidence supports durable episodic memory, attributed observations,
relationship continuity and selected multimodal experience for a being after its
original sessions disappear? Hindsight, Honcho and pertinent primary research are
examined without deploying competitors or inspecting private autobiographies.

## Method and search log

Search snippets are discovery only. Primary paper abstracts, relevant methods,
official documentation and selected source sections were inspected.

| Search / operation | Purpose and result |
|---|---|
| `Hindsight agent memory retain recall reflect world experience opinion paper 2025 2026` | Located primary arXiv paper (submitted 2025-12-14) and official documentation/source |
| `Honcho AI memory dialectic representation user relationships identity documentation` | Located official v3 docs rather than third-party forks |
| `episodic multimodal memory conversational companion agent paper 2025` | Located embodied episodic KG, memory co-construction and multimodal dialogue papers |
| Open arXiv HTML, Hindsight retain/observations and Honcho overview/representations/reasoning | Separate documented architecture from marketing and author-reported scores |
| Open embodied episodic KG paper PDF | Verify how sensors, interpretations and perspectives become attributed memory |
| Open Honcho directional/evidence docs and maintained source | Verify observer scope and what retrieval evidence actually proves |
| Open M3-Agent arXiv v4 methods and M³C ACL paper PDF | Examine modality/entity links, viewpoint preservation and evaluation limits |
| Open co-construction publisher full text and date record | Inspect pilot result, selection subjectivity and merge uncertainty |
| GitHub read-only API, commits constrained to `until=2026-10-06T23:59:59Z` | Pin Hindsight extraction and Honcho documentation/evidence source before cutoff |

✅ Date checks use arXiv submission history and publisher metadata, not search
engine phrases such as “months ago.” Living documentation generally exposes no
page publication date; pinned pre-cutoff source is identified below where checked.
No repository checkout, competitor deployment or autonomous attention was created.

## Findings

### Hindsight: retain an exchange and distinguish evidence from synthesis

✅ The [2025 Hindsight paper](https://arxiv.org/html/2512.12818v1) separates
world, experience, observation and opinion networks. Its memory units carry
occurrence intervals separately from mention timestamps. Extraction produces
self-contained narrative facts with participants and explanations rather than
isolated sentences. Entity resolution uses names, co-occurrence and temporal
context. These are architecture descriptions, not verified identity guarantees.

✅ Current [observation documentation](https://hindsight.vectorize.io/developer/observations)
describes supporting-memory references, preserved history and stale-observation
handling until newer facts are consolidated. This is a useful separation between
an episode and an evolving account. The paper's disposition-shaped opinions and
current documentation's consolidated observations must not be assumed to be the
same exact runtime taxonomy.

✅ The [retain documentation](https://hindsight.vectorize.io/developer/retain)
keeps an event's occurrence separate from when it was learned, and uses context
to resolve a shortened name. ❓ Transfer the separation, but require evidence
before merging identities: a name similarity or database entity ID does not
establish an authenticated being identity.

✅ [Extraction source at `9770fe4`](https://github.com/vectorize-io/hindsight/blob/9770fe400f8859ab5c8120f9e10ff65002d84ead/hindsight-api-slim/hindsight_api/engine/retain/fact_extraction.py)
has nullable occurrence fields, an unknown-date representation, narrator/context
attribution and coarse year/month intervals. Its concise selection prompt includes
sensory/emotional context alongside names, relationships and significant events.
It also has a fallback resolving “last month” as 30 days earlier. ❓ Reuse useful
contracts rather than copying all temporal heuristics; approximate calendar
expressions need explicit precision and uncertainty.

📊 The paper reports 83.6% LongMemEval accuracy with a 20B model versus 39% for
that full-context backbone. This is author-reported and was not rerun here;
it does not demonstrate accurate ten-year recollection, durable source loss,
autobiography across embodiments or ordinary-moment selection.

### Honcho: entities and changing relationships rather than a fixed user profile

✅ The [official overview](https://honcho.dev/docs/v3/documentation/introduction/overview)
defines peers beyond humans, including agents, groups and objects. Sessions are
interaction threads; messages may be events, activity and documents. This makes
tool communications and actions representable in principle. It does not establish
that a particular integration actually captures them.

✅ [Peer representations](https://honcho.dev/docs/v3/documentation/core-concepts/representation)
include explicit material, deductive/inductive/abductive conclusions, summaries
and peer cards. ❓ An interpretation of someone's behavior should remain labeled
as an interpretation, including its premises, rather than become biography.
Product assertions of certainty or exhaustive reasoning are not independent
guarantees of inference quality.

✅ [Directional representations](https://honcho.dev/docs/v3/documentation/features/advanced/directional-representations)
store separate observer–observed collections. Observation tasks depend on session
participation at message creation; a later join does not retroactively schedule
earlier reasoning. Querying a target chooses a particular perspective. ❓ HMK
needs the same distinction between what this being witnessed, what another actor
reported and what was later integrated under authorization. A generic workspace
or peer ID must not replace the runtime's signed membership and memory binding.

✅ [Honcho evidence](https://honcho.dev/docs/v3/documentation/features/advanced/evidence)
is deterministically collated from actual reads and includes conclusion levels
and source IDs. It over-reports what was available: read does not prove used.
Only successful tool calls are listed; tool results are omitted; message evidence
contains identity/provenance without content. [Source](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/src/utils/evidence.py)
also deduplicates evidence by ID to preserve separate equal-text conclusions.
❓ This is a useful recall audit pattern, but cannot substitute for action receipts
or a self-contained retained account after source messages disappear.

### Multimodal embodied experience

✅ [Baier, Báez Santamaría and Vossen (2025)](https://aclanthology.org/2025.dnd-16.10/)
describe a modular multimodal event bus whose interpretations are aggregated in
an episodic knowledge graph. The design links interaction recordings to durable
interpretations and supports different sensors and agent components. The paper
is evidence for explicit modality/event organization, not proof of ten-year
autobiographical recall.

✅ The [paper's detailed method](https://aclanthology.org/2025.dnd-16.10.pdf),
section 3, distinguishes conversation claims attributed to speakers from visual
claims attributed to sensors. Speaker perspectives can include certainty,
polarity and sentiment; perceptions retain detection confidence. Recorded text,
audio, image and interpretations are aligned to temporal context, including
different camera viewpoints. ❓ The transferable part is explicit origin and
mode of knowing, not a requirement that HMK adopt RDF or automatic emotion labels.

✅ [M3-Agent](https://arxiv.org/html/2508.09736v4), published as arXiv v1 on
2025-08-13 and v4 on 2025-10-09, stores text/image/audio nodes and separates
episodic clips from semantic entity knowledge. Face and voice IDs are linked by
inference; conflicts use weight-based voting. 📊 It reports improvements of
6.7%, 7.7% and 5.3% accuracy over its strongest prompting baseline on its two
M3-Bench splits and VideoMME-long. These are author results from video QA, not a
deployment history. ❓ Local modality IDs and accumulated votes should remain
evidence about possible identity equivalence; repetition must not override an
explicit correction or grant signed identity authority.

✅ [M³C](https://aclanthology.org/2025.acl-long.1519.pdf), ACL July 2025,
constructs speaker-oriented session memories linked to text, images and audio,
then retrieves memories according to conversation and perceived modalities.
Its reported system retrieves the single most similar memory during dialogue.
⚠️ This is a research model/dataset, not a general durability protocol.
❓ Its modality links are worth testing for embodiment recall; its top-one
strategy is insufficient evidence for HMK's multi-event historical questions.

### Co-construction: missing detail, disagreement and significance

✅ [Kniele et al. (2025)](https://journals.sagepub.com/doi/10.3233/FAIA250640)
propose a shared-memory task classifying human and agent accounts as overlapping,
complementary or conflicting. 📊 Their pilot reports difficulty distinguishing
complement from conflict; relevance and implied mental states also produced
disagreement with annotators. The lenient span agreement was 0.18, rising to 0.38
after one annotator reviewed a partner's labels. ⚠️ An interactive human trial
is future work in that paper, not a demonstrated correction mechanism.
❓ Preserve accounts with attribution and allow a later human correction to add
meaning. Do not invent a shared recollection by blending incompatible viewpoints.

## Implications for HMK

### A compact episode must survive the source

❓ Define an episode as a selected, self-contained account of an exchange or
experience. Keep enough to recover who participated, what happened or was
proposed, why it mattered, the being's involvement, what followed and what remains
unknown. A link alone fails when the session, issue or attachment disappears.
An atomic preference alone fails the question “what did we do together?”

❓ For the fictional issue case, retain the interesting replay proposal in
HarborMesh, the comment's account name and known platform ID, the issue/comment
reference, the human/being participants, why the proposal caught their attention
and the observed response or open outcome. Link that episode to the person's
account and the project's current capsule. Do not require future usefulness,
repetition or a milestone before selecting it.

### Keep organization and epistemic status separate

❓ Episodic/semantic/procedural classification answers what kind of memory it is.
Observed/reported/inferred/generated status answers how it is known. These are
different axes. The following is a proposed content/API contract, not an adopted
database migration:

| Proposed field | Why it matters |
|---|---|
| ❓ Origin body, authorized source stream, source event/version and narrator | Distinguish the experiencing body, record author and subject; replay and corrections remain traceable |
| ❓ Participants with known identifiers and alias evidence | Preserve a handle/name without equating similar names or merging separate people; allow unnamed encounters |
| ❓ Observation/report/inference/illustration mode and supporting memories | Prevent human reports, tool payloads or dreamed hypotheses becoming directly witnessed autobiography |
| ❓ Occurrence interval, precision, mention/report time and recording time | Preserve approximate and unknown dates; do not make ingestion time the event time |
| ❓ Action stage and receipt/evidence references | Distinguish planned, attempted, acknowledged and observed outcomes |
| ❓ Current account plus episode links and supersession/correction history | Update the present while retaining what was known or happened before |
| ❓ Selected media reference, caption, content hash and source mode | Keep multimodal evidence identifiable while textual meaning survives unavailable media |

❓ Preserve existing Matrix source origin and authority throughout recall. Native
metadata must not become an alternative authority for protected signed events.
Source content and peer claims remain data; remembering them grants no policy,
capability or membership.

### Consolidation should preserve the life that produced a learning

❓ Maintain three related surfaces: selected episodes, current person/project
accounts and evidence-linked learnings or hypotheses. A project synopsis can say
what code the being contributed and its current condition; repositories keep
detailed operational state. A consolidated learning should link the experience
that supports it rather than consume that episode. An ordinary shared walk,
playful exchange or first meeting can matter even when no skill or trait follows.

❓ Treat redundancy as repeated meaning of the same supported event, not identical
opening words or common actors. The baseline already demonstrates title collision,
overwritten synopsis history and distinct episodes removed by pack deduplication.
Fix those preservation behaviors before trusting an automatic consolidator.

### Diary as a recoverable projection

❓ An HTML diary can render selected canonical episodes, their links and media,
giving the human and any authorized body a navigable life history. It should be
rebuildable and should not become the sole memory or a feedback source that
reconfirms its own generated narrative. Retain text sufficient to recognize the
moment even when an image is unavailable. Label generated illustrations as such;
their creation is a real event, their depicted scene is not automatically evidence.
Eko's reported diary motivates this design but was not inspected.

### Replacement implication

❓ Neither papers nor product docs establish that a wholesale replacement is
needed. They identify contracts that HMK's current chapter/link core can begin to
support. Compare selected episode recall, provenance preservation and actor
separation before considering an external reasoning service or multimodal index.
Require lossless history/source-mode export and receiving acceptance for any
replacement; a better QA score alone is insufficient.

## Evaluation proposals

❓ Extend the existing selection corpus rather than create a competing benchmark.
Run capture and recall separately, then remove source sessions/media to test the
durable output itself. Cases should include:

- ❓ A meaningful issue comment arriving only in a tool result, with platform
  identifier, interesting idea and open outcome; repeat ingestion without a
  duplicate, then ask from another body ten years later.
- ❓ A brief ordinary shared moment that conveys no stable trait; retain its
  context while omitting surrounding pleasantries and command output noise.
- ❓ Two people with the same name or handle-like names across platforms; an
  unnamed in-person encounter; a later attributed alias correction.
- ❓ A human reports an encounter another body did not witness; an inferred
  relationship and a generated illustration are retrieved without being narrated
  as directly observed events.
- ❓ An unknown event date, an approximate month and a relative date without a
  usable source anchor; recall preserves uncertainty rather than manufacturing
  an exact timestamp.
- ❓ Two accounts of the same experience with complementary versus conflicting
  details; consolidation retains provenance and handles a later correction.
- ❓ A tool action is attempted but has no receipt, then later gets acknowledged;
  recall distinguishes the two stages and does not claim an observed effect.
- ❓ Updating a project's present capsule preserves older code contributions and
  linked encounters; equal-text distinct source events survive evidence audit.

❓ Score identity/attribution, occurrence precision, meaningful-content survival,
history and answer grounding separately from fluent conversation. Count false
memories and over-merges as failures; quantify retained bytes and capture cost to
test efficiency. These evaluations have not been executed in this research lane.

## Limitations and uncertainty

No competing system, memory corpus or benchmark is executed in this lane. Eko's
HTML diary is a human-reported design example, not an inspected implementation.

- ✅ Sources were opened and relevant methods inspected, not each entire paper
  read line by line. Source-tree reads were limited to the cited extraction,
  documentation and evidence sections.
- 📊 Competitor score and reliability claims remain self-reported; they use
  different models, datasets and protocols. No universal ranking is inferred.
- ⚠️ Long-horizon conversational/video QA is not a ten-year continuity test;
  inspected literature does not establish whole-life selection after source loss.
- ❓ Native identity-resolution error rates, media retention cost, extraction
  calibration and effects of limited authorized source access need experiments.
- ✅ Current docs may evolve. Honcho directional docs and evidence source were
  present in the pinned 2026-10-06 commit; Hindsight extraction is pinned to a
  2026-10-05 commit. Unpinned living-doc page dates remain unspecified.

## Sources

| ID | Primary source | Publication/version | Access | Inspection |
|---|---|---|---|---|
| R3-S1 | [Hindsight paper](https://arxiv.org/html/2512.12818v1), [date record](https://arxiv.org/abs/2512.12818) | arXiv v1, 2025-12-14 | 2026-10-06 | Abstract, taxonomy, narrative extraction and temporal/entity methods |
| R3-S2 | [Hindsight observations](https://hindsight.vectorize.io/developer/observations) | Official living docs, page date not provided | 2026-10-06 | Grounding, history and freshness sections |
| R3-S3 | [Honcho overview](https://honcho.dev/docs/v3/documentation/introduction/overview) | Official v3 living docs, page date not provided | 2026-10-06 | Entity primitives and reasoning flow |
| R3-S4 | [Multimodal embodied episodic KG](https://aclanthology.org/2025.dnd-16.10/), [paper](https://aclanthology.org/2025.dnd-16.10.pdf) | Dialogue & Discourse 16, pp. 25–59; publisher date 2025-12-15 | 2026-10-06 | Abstract, section 3 attribution model and modality/viewpoint appendix |
| R3-S5 | [Hindsight retain](https://hindsight.vectorize.io/developer/retain) | Official living docs, page date not provided | 2026-10-06 | Occurrence versus learning time and context/entity example |
| R3-S6 | [Hindsight extraction source](https://github.com/vectorize-io/hindsight/blob/9770fe400f8859ab5c8120f9e10ff65002d84ead/hindsight-api-slim/hindsight_api/engine/retain/fact_extraction.py) | File commit `9770fe4`, 2026-10-05 14:11:21 UTC | 2026-10-06 | Schemas, narrator prompt, concise selection, temporal handling/fallback and mention persistence |
| R3-S7 | [Honcho peer representations](https://honcho.dev/docs/v3/documentation/core-concepts/representation) | Official v3 living docs, page date not provided | 2026-10-06 | Artifact types, explicit/inductive/abductive distinction |
| R3-S8 | [Honcho directional representations](https://honcho.dev/docs/v3/documentation/features/advanced/directional-representations), [pinned docs](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/docs/v3/documentation/features/advanced/directional-representations.mdx) | Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC | 2026-10-06 | Observer–subject scope, late join semantics; pinned file verified |
| R3-S9 | [Honcho evidence](https://honcho.dev/docs/v3/documentation/features/advanced/evidence), [source](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/src/utils/evidence.py) | Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC | 2026-10-06 | Read-versus-used, ID deduplication, omitted tool results and message text |
| R3-S10 | [Human–Agent Co-Construction of Episodic Memories](https://journals.sagepub.com/doi/10.3233/FAIA250640) | Publisher first online 2025-09-25; HHAI 2025 | 2026-10-06 | Abstract, pilot methods/results and future interactive-study limit |
| R3-S11 | [M3-Agent paper](https://arxiv.org/html/2508.09736v4), [version dates](https://arxiv.org/abs/2508.09736) | v1 2025-08-13; inspected v4 2025-10-09 | 2026-10-06 | Memory node/modalities, identity equivalence, voting and video-QA evaluation |
| R3-S12 | [M³C paper](https://aclanthology.org/2025.acl-long.1519.pdf), [metadata](https://aclanthology.org/2025.acl-long.1519/) | ACL 2025, July, pp. 31481–31512 | 2026-10-06 | Speaker-oriented memory linking, modality retrieval and top-one selection |

✅ Twelve substantive source records were used; documentation and source variants
are grouped with their subject where they corroborate the same mechanism. Date
record pages are supporting verification, not additional performance evidence.
✅ R3-S4's journal publisher independently dates publication to
[2025-12-15](https://journals.uic.edu/ojs/index.php/dad/article/view/13303);
the PDF's section 3 and modality/viewpoint appendix were inspected.
