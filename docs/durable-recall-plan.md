# Durable recall across a being's bodies

The goal is selected, retrievable life history that survives loss of original
sessions. Ten years after an interesting proposal in a project issue, another
body should be able to recover the participant's known name/account, what they
proposed, why it mattered and what happened next. It should also recognize the
being's own projects, relationships, shared experiences and learning.

This is an improvement plan and evaluation contract. It does not claim that HMK
already provides ten-year recall, automatic experience extraction or receiving
acceptance in another body. A successful native session resume tests a different
property from durable recall without that session.

The [general-memory review](general-memory-review.md) examines the whole kit
against this use, including preservation, metadata, capture, retrieval,
workspace lifecycle and source authority. Its disposable diagnostics establish
concrete gaps beyond the selection policy.

The [2026-10-06 agent-memory investigation](../research/agent-memory-2026-10-06/README.md)
adds five primary-source research lanes on consolidation, retrieval, experience,
evaluation and evolution options. Its [synthesis](../research/agent-memory-2026-10-06/SYNTHESIS.md)
and [cross-report](../research/agent-memory-2026-10-06/CROSS_REPORT.md) support the
work sequence below. Competing systems were not deployed or benchmarked; this
evidence does not establish a necessary wholesale replacement.

The [2026-10-07 Codex addendum](codex-native-memory-review.md) incorporates the
explicitly supplied project handoff and pinned native implementation. Codex
already implements both session continuity and cross-session extraction,
consolidation and recall. Preserve useful native behavior while comparing a
complete HMK adapter with controlled coexistence in
[issue #11](https://github.com/nicoechaniz/hermes-memory-kit/issues/11). Native
local persistence and its external-memory import are not yet evidence of a
being-shared lifelong store or a configurable HMK backend.

The [2026-10-07 Mariano research comparison](mariano-memory-research-review.md)
adds inspected April/July designs from four authorized live research collections.
It connects typed memory, historical changes, coherent publication and layered
synthesis to this plan. Mounted documentation and source configuration establish
that collective-memory serves a filtered index of the live tree, including its
curated map and underlying documents; the second view retains additional material
and may also contain current work. Its name does not establish source age.
The source ledger separates document age, access and editorial status. Fixed
hardware, scoring and lifecycle recommendations require fresh evidence before
adoption.

The same comparison now checks Mariano's GitHub repositories and selected
AlterMundi repositories, including upstream memory PRs and author dates.
Collective-memory's July public source implements thematic distillation with
source fingerprints, preview, provenance, unchanged-result reuse and serialized
publication. Reuse those mechanisms for P3/P4 while retaining self-contained
episodes and actual evidence manifests. Generated synthesis cannot serve as
independent corroboration of its own sources or replace episode history.
No inspected source establishes a later Mariano autobiographical-sleep study;
inventory/search coverage is stated in the comparison rather than treated as
proof of absence.

## First delivery

The first delivery adds:

- a [selection policy](../templates/skills/memory/librarian/references/durable-memory-selection.md),
  shipped with the librarian skill, covering every authorized channel;
- short guidance in the bootstrap AGENTS template, so selection is visible
  without loading a large reference every turn;
- [synthetic evaluation cases](benchmarks/durable-recall-cases.json), with source
  material, expected retained meaning, noise to omit and later questions;
- the capture/recall protocol below, separating persistence, retrieval and answer
  quality so that a failure identifies what to improve.

These changes are in the fork's templates. Existing installations do not acquire
them merely because this file exists. Body-specific access policies, Matrix
contracts, private-memory boundaries and original sources remain authoritative.

Validation on 2026-10-06: the corpus contains 12 cases, 14 distinct retained
meanings and 16 recall questions; source IDs, expected connections and document
links were checked. The kit's smoke test passed. A disposable bootstrap/upgrade
check confirmed that the selection reference ships with the skill and that new
AGENTS guidance is present in a fresh workspace. No live pool was changed and
the model capture/recall pilot has not yet run. The Codex-only skill validator
rejects the template's existing Hermes frontmatter keys (`version`, `author`,
`prerequisites`); YAML and packaging were checked without changing that format.

## Gaps in the current implementation

The inspected kit has chapters, tags, links and native update operations, but its
general guidance emphasizes document ingestion. The provider supports retrieval;
it does not by itself select and write meaningful experience after every
interaction. Curation currently depends on the model and its available guidance.

Three storage/retrieval properties identified at review time needed repair:

- The reviewed `add-text`/`update` overwrote native accounts without a revision
  ledger. The repair delivery below now preserves native revisions and stable
  IDs; meaningful distinct encounters still need their own selected episodes.
- `simple_spr` uses the first eight nonempty lines and truncates ordinary lines;
  previews can omit the participant or significance if metadata leads the text.
- Hybrid ranking includes recency. An old episode may remain stored yet fail to
  appear for a weak cue. Event dates in prose do not control that ranking clock.

Use these as testable risks, not conclusions that an entity table, event schema
or new ranking formula is already necessary. Evaluate against the deployment's
actual schema and configured embedding provider. Optional ENGRAM fields and
Matrix projections must not be assumed present in every native pool.

## Delivery sequence and acceptance

| Step | Deliverable | Evidence needed before advancing |
|---|---|---|
| 1. Selection | Shared policy and synthetic cases | Cases cover people, own projects, everyday experience, learning, tool communications and noise; authority and uncertainty remain explicit |
| 2. Record shapes | Pilot accounts, episodes and supported links using existing HMK primitives | Another reader can understand each memory without sessions; identities are not guessed or duplicated needlessly |
| 3. History and current accounts | Dated synopsis updates plus preserved milestones/corrections | Present questions use the latest qualified account; past questions recover what happened then; no silent historical loss |
| 4. Capture | Guidance integrated into each participating body's authorized foreground work | Meaningful inputs from each channel are considered; persistence and embedding freshness are observed; mechanical noise is omitted |
| 5. Recall | Measured retrieval and answers from a clean receiving context | Ten-year, weak-cue, missing-source and other-body cases pass; unsupported identity/action claims remain absent |
| 6. Adoption | Versioned rollout through maintained templates and shared skills | Backup, preserved provenance, actual receiving acceptance and rollback are verified for each participating deployment |

Step 1 defines what to test. Template packaging checks do not count as passing
steps 4–6. Keep one work record here; link substantive implementation or pilot
evidence as it becomes available rather than duplicating operational status in
memory or opening several competing plans.

## Publish each advance

Publish each coherent delivery in its owning repository as part of completing
that work. Include the change, available validation and remaining limits so other
contributors can choose whether to adopt it. Publish proposals, policies and
evaluation cases as such; do not wait for the final pilot or live rollout to make
them available. Share later corrections and results through the same maintained
change or its successor. Publication and adoption are separate: publishing does
not claim deployment in another body or permission to transfer private memory.

## Run a capture-and-recall pilot

Use an isolated disposable workspace and a synthetic being binding. Never ingest
the corpus into a live being's autobiography or infer access from a fixture body
name. All fixture participants, projects, accounts and events are fictional.

1. **Freeze the conditions.** Record kit revision, model, guidance version, actual
   schema, embedding provider/model, retrieval threshold and token budget. Use
   identical conditions for the baseline and proposed policy. Preserve each
   generated pool and its source-to-chapter mapping for inspection.
2. **Capture in order.** Provide only each case's `sources`, the fixture runtime
   context and authorization to curate that foreground experience. Keep
   `expected` and `questions` hidden from the capturing model. Capture with the
   current guidance, then with the proposed guidance in a separate fresh pool.
   Preserve source IDs in the resulting provenance.
3. **Check selection and persistence.** Inspect expanded records and supported
   links. Compare their meaning with `expected.retain`, not an exact sentence or
   prescribed number of chapters. Check skipped material and protected-source
   handling. Record actual IDs; fixture keys are expectations, not database IDs.
4. **Start a clean recall context.** Give a receiving body of the same fictional
   being only its fixture binding, current question and permitted memory tools.
   Supply no source messages, expected answer, native session history or original
   episode text. Disable access to fixture source URLs. Do not reveal the hidden
   rubric to the answering model.
5. **Evaluate recall.** Use the body's normal retrieval flow, allowing bounded
   expansion of selected candidates and explicit follow-up queries. Begin with
   a recorded budget such as 1,500 pack tokens and five candidates; record full
   expansion cost as well. Freeze the deployed threshold rather than tuning it
   per question. Capture candidates, ranks, expanded IDs, answer and tool failures.
6. **Age and distract.** In the disposable harness, advance an injected retrieval
   clock ten years while keeping record timestamps unchanged. Add relevant
   distractor memories with newer timestamps. Repeat selected weak-cue queries.
   Merely writing “2036” in the prompt does not test recency scoring. Source loss
   and body capability changes are separate perturbations.
7. **Inspect failures once they are located.** Was the information never selected,
   compressed away, overwritten, missing from embeddings, ranked too low, absent
   from neighbors, or misread despite being retrieved? Improve that component.
   Repeat affected cases when a correction or remaining uncertainty warrants it.

One scenario may retain several meanings in one chapter. `needs` and
`related_keys` refer to meanings that must be connected and recoverable; they do
not require one chapter per key. Fixture event dates and source delivery dates
are distinct. A provenance pointer alone does not satisfy the retained meaning.

For ranking on a saved generated pool, reuse `scripts/embed_benchmark.py`:
generate `query | expected: id1,id2` lines from the inspected key-to-ID mapping
and invoke it through that workspace's `scripts/hmk` wrapper. It measures
semantic/hybrid candidates, latency, hit, precision and recall. It does not
evaluate capture, temporal assertions, identity attribution or answer grounding;
those need the protocol above. Do not treat any topical hit as a complete answer.

## Evaluate meaning, omissions and cost separately

Record per case:

- retained essentials present, missing, contradicted or qualified;
- noise retained and duplicate accounts/episodes without a recall benefit;
- retrieval rank, linked expansion and whether every answer requirement was
  supported by the memories actually retrieved;
- unsupported identity merges, invented names/dates/outcomes, stale status
  presented as current, or another being's experience presented as one's own;
- stored bytes/tokens, retrieved and expanded tokens, latency and provider errors.

The mandatory issue-comment case passes only when it answers all specified
requirements after source loss and simulated aging. Exact wording is irrelevant;
a wrong participant or invented adoption is a failure even when the topic is
found. Negative cases must produce grounded absence or uncertainty. Report
selection and recall coverage as fractions of rubric items, alongside the
specific failures; an average score must not hide broken continuity.

Compression quality means enough retained meaning per unit of storage and recall
cost. Measure those costs before setting numerical size targets. Avoid quotas
that force the loss of meaningful people, projects or irreplaceable episodes.

## Next decision

Implementation now proceeds under
[health issue #13](https://github.com/nicoechaniz/hermes-memory-kit/issues/13),
which links this plan, the source reviews, research index and the later Codex
issues #11/#12. The human selected repairing HMK first, then testing native
coexistence once the baseline is healthy. This order supersedes any reading of
the earlier smallest Codex experiment as the immediate implementation task.

P0 repair on 2026-10-07: migration uses a verified standalone SQLite online
snapshot including committed WAL data; unknown occurrence time stays unknown.
Upgrades merge shipped skills and preserve custom files plus overwritten
pre-images outside skill discovery. Native titles preserve Unicode and resolve
slug collisions without replacing differently titled records; legacy exact-title
books keep their existing IDs/slugs. Thirty-two targeted regression/compatibility
tests passed, including isolated snapshot retrieval and repeated migration.
P1 adds stable native record UUIDs, searchable revision pre-images, expected-
revision writes, explicit kind/date/source metadata and native forgetting of
current/history copies. Single-chapter replacement retains ID and links;
multi-chapter replacement requires explicit updates. The CLI and provider expose
the metadata and historical lookup. Semantic backfill now uses the maintained
writer, binds inferences to source revisions and keeps FTS/eligibility consistent;
repeating identical output does not duplicate it. Source changes still require
reconciling derived claims; generic extraction excludes signed projections and
embedding-disabled records. Seventy-two targeted compatibility/regression tests
cover this delivery.

P2 repairs Unicode/full-question cues, whole-record lexical overlap, distinct
episode retention, neutral general priors (research preferences require explicit
opt-in), incoming/outgoing navigation and source-bearing semantic/compact results.
Short selected accounts keep complete recall text; long records can provide an
authored summary, which participates in revisions and embedding invalidation.
Every item passes relevance before budget/quota/RRF selection. Weak reranking
scores are no longer normalized to a perfect match. Embedding outages return
qualified lexical degradation/unavailability without changing providers; schema
errors propagate. ENGRAM reuses one query embedding and only records final picks.
Budget estimates include source and neighbor metadata. Provider previews retain
attribution and distinguish unavailable retrieval from absence.

The complete suite passes 176 tests. The original diagnostic runner now observes
preserved WAL contents, acquired skills and distinct names/events; maintained
episodic metadata, incoming links, historical lookup, indexed backfill and
qualified outage/relevance behavior. These are synthetic mechanical results.
The ten-year clock test establishes preservation/lexical retrieval under its
fixture, not model selection, semantic accuracy or another live body's acceptance.
P3/P4 now have [finite foreground capture/consolidation primitives](foreground-capture.md):
durable pending deltas, explicit outcomes, contiguous cursors and atomic native
writes/receipts with replay. Full episode manifests bind dream proposals to exact
source versions. Inferred/generated accounts preserve episodes and support links;
later changed/missing supports are exposed as needing reconciliation. This is a
mechanical foundation, not an automatic extractor or a completed dream pilot.
Model selection/answer quality, three-pass consolidation, cost comparison and
actual receiving adoption remain unqualified. No live binding or trigger changed.
The complete suite after this delivery passes 187 tests, including separate
process capture after deleting its source file and pre/post-commit failures.

Published implementation: [PR #14](https://github.com/nicoechaniz/hermes-memory-kit/pull/14),
based on the selection/research [PR #10](https://github.com/nicoechaniz/hermes-memory-kit/pull/10).
This is code/test evidence; no live being pool was migrated or deployed.

First fix the review's confirmed preservation hazards: incomplete WAL migration
backup, acquired-skill loss during upgrade and silent native title collisions.
Publish each fix with the relevant regression evidence. These observations are
already concrete; they do not need to wait for a model capture benchmark.

The research reinforces three linked products: self-contained selected episodes,
current person/project accounts and evidence-linked learnings. Correcting or
consolidating a present account must preserve the experience and its historical
attribution. The project capsule remembers authored contributions and dated
status; repositories retain detailed operational state and fresh validation.

Use this priority sequence inside the six delivery steps above; it is the same
work record, not a second program:

| Priority | Coherent change | Acceptance before adoption |
|---|---|---|
| P0 | WAL-consistent backup, learned-skill preservation, collision-safe native writes | Regression evidence for each reproduced loss and an isolated verified restore |
| P1 | Native revision/source/date contract and supported writers | Current versus past answers, unknown/approximate dates, source/body/mode preservation, maintained FTS/embedding eligibility, idempotent events and expected-version concurrent updates |
| P2 | Repair retrieval cues, deduplication, priors, provenance, links and relevance/outage behavior | Full/Unicode question cues, distinct episodes, incoming/outgoing navigation, relevance before quota/fusion, explicit null versus degraded/unavailable results |
| P3 | Finite authorized delta capture | Tool-only and brief meaningful encounters, source-loss sufficiency, durable pending work, late corrections, crash/replay and persistence/readiness receipts |
| P4 | Staged dream/consolidation pilot | Insertion-only baseline versus proposed changes; three passes plus replay; no lost essential meaning, fabricated events, identity merges or stale-current claims |
| P5 | Diary and procedural navigation | Rebuildable episode/media view, text sufficient without images, illustrations attributed; remembered skills route to actual body capabilities |
| P6 | Scale and component comparisons | Frozen quality/cost/latency conditions, source isolation, complete available-history transport, verified restore and actual receiving acceptance before replacement |

Do not postpone a confirmed preservation/indexing fix until a model pilot, or
infer that every proposed metadata field needs a new table before trying compact
records. Run the baseline/proposed-policy pilot under recorded conditions, then
isolate each implementation change. Start with the issue proposal, project
synopsis change, ordinary shared moment, attribution correction and
missing-source/other-body recall. Reuse the corpus for lifecycle and consolidation
perturbations rather than building a competing benchmark.

## Capture and consolidation contract

Initial implementation is human-directed finite foreground work. This plan does
not install hooks, timers, inbox attention, prefetch or another model/provider.
On 2026-10-07, a separate explicit human request enabled the Codex hooks
framework and established the bounded design in
[issue #12](https://github.com/nicoechaniz/hermes-memory-kit/issues/12). That later
authorization does not install a memory handler or activate native generation;
qualify the native writer, source scope and receiving contract first. Reuse
native extraction/consolidation where feasible rather than assuming every body
needs a new implementation of sleep.
Future daily, idle, step-count, compression or end triggers use the same contract
only through each body's authorized harness/runtime integration. A source-loss
boundary can occur before a daily pass; session end is an extra opportunity.

Each authorized body/source stream supplies event identity and source version.
Known participants, platform/source IDs, originating body/narrator, mode of
knowing and action stage survive selection. Occurrence interval and precision,
report time and recording/revision time are distinct; unknown occurrence stays
unknown. Similar names do not establish one actor or signed being membership.

Persist sufficient selected evidence or a durable authorized pending reference
before acknowledging work. Process ordered per-stream deltas with applied,
deliberately omitted, deferred and failed outcomes; advance the processed cursor
only after durable outcomes, retaining unresolved gaps for retry. No silent tail
truncation, minimum message count or fixed fact quota may discard meaningful
experience. Omitted mechanical noise need not become permanent autobiography.

Logical event identity stays tied to source event/version. Selection-policy and
model versions describe a processing decision; rerunning a policy can revise its
account without inventing another encounter. Current-account writes require a
version check and retained native history. Protected Matrix/Wiki sources keep
their authority, history and projection restrictions.

Dreaming produces proposed links, syntheses and learnings with supporting
episodes. Validate and apply through supported writers; preserve original
meaning and corrections. Inferred patterns, imagined possibilities and generated
illustrations remain attributed as such. Skill refinements belong in maintained
packages with relevant functional evidence; memory never grants capability.

Consolidation links supporting episodes without treating the act of summarizing
them as a factual correction. Keep meaningful encounters reachable by ordinary
past-event queries after a higher-level synthesis exists. Minimum source counts
for generalizations and cluster size for a batch are not capture prerequisites:
a single significant encounter may need immediate durable selection.

Separate durable persistence/lexical indexing from embedding readiness. Retry
vectors, skill proposals and diary rendering independently and report actual
coverage, deferred work, errors, versions and formation cost. A diary renders
canonical episodes and selected media with captions/hashes/source modes; it is
not the only memory or a source that confirms its own generated narration.

## Replacement gates

Prepare a versioned export/restore contract alongside these upgrades. Inventory
available text, metadata, logical IDs, native revisions, source references,
links, corrections/retractions, date precision and selected assets. Explicitly
record already-missing history; changing systems cannot recover it by inference.
Keep source authority and receiving scope distinct from storage IDs.

LangMem formation primitives, Graphiti temporal/entity indexing and Hindsight
recall/consolidation are bounded comparison candidates, not selected replacements.
Compare on fictional fixtures first, at the same source set, answering conditions
and total formation/recall budget. Measure relevant behavior, not vendor rankings.

Replace an index or extractor when it solves a measured limitation that remains
after the simpler repairs. Change canonical storage only when a required behavior
cannot reasonably be maintained in HMK and the candidate passes lossless
available-corpus transfer, verified restore, source/correction propagation and
receiving acceptance. A full replacement additionally preserves each body's
integration and actual capabilities.

Keep one canonical write authority during read-only shadow comparisons. Replicate
versioned deltas with receipts; do not generate independent autobiographies by
dual-writing model inferences. Before cutover, verify the final checkpoint and
critical queries, preserve rollback, and account for new writes made after it.
Live rollout follows that evidence and the existing authorization of each body.

Research delivery on 2026-10-06: five completed raw reports, cross-report,
narrative, synthesis, deduplicated bibliography and research index. Runtime
fixes, model capture/recall, consolidation, scale and live receiving acceptance
remain unexecuted. Publish every coherent implementation and correction as it
lands rather than waiting for the entire sequence.

Codex integration update on 2026-10-07: the addendum distinguishes native thread
continuity, cross-session local memory, external import and the compiled backend
seam. It incorporates the existing #11/#12 work and specifies a fictional native
versus coexistence experiment. This is source-verified integration design;
capture/consolidation measurements and live activation remain pending.
