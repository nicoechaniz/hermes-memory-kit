# Experience, supported understanding and local memory mechanisms

Reviewed on 2026-10-07. Companion to the
[portability review](lifelong-memory-portability-review.md) and the single
[durable-recall work record](durable-recall-plan.md), tracked in
[issue #11](https://github.com/nicoechaniz/hermes-memory-kit/issues/11).
The human specifically asked to learn from Hindsight independently of backend
choice, investigate related systems and check recent OpenSouls work. This review
inspects primary documentation/source. No competitor was deployed or benchmarked.

## Hindsight: transferable design, qualified preservation

Hindsight separates retained facts/experiences from accumulated observations and
query-time reflection. Useful source details are pinned to
[`9269b884`](https://github.com/vectorize-io/hindsight/tree/9269b88417ed263e5a8350f2e416ca2b322756b1).
Descriptions from current website documentation can differ from this source;
qualify the selected release before implementation.

- [Retain](https://hindsight.vectorize.io/developer/retain) describes extracting
  self-contained facts, entities and event intervals rather than retrieving only
  arbitrary transcript chunks. The source's
  [retain types](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/hindsight_api/engine/retain/types.py)
  carry context, event dates, document identity, user-supplied entities and tags.
  Replacement/reprocessing defaults need attention: source-document updates
  are not automatically immutable autobiographical revisions.
- [Observations](https://hindsight.vectorize.io/developer/observations) describes
  supported synthesis, refinement and stale-observation verification. A useful
  conceptual separation is what happened versus what the bank now understands;
  preserve the selected experience while changing its interpretation.
- The pinned [consolidation prompt](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/hindsight_api/engine/consolidation/prompts.py)
  matches the same entity/facet or event, requires source fact IDs and reasons,
  distinguishes occurrence from mention time, and protects significant events.
  It also allows deletion of some superseded observations. Its default mission
  includes notable events; the current website's default description emphasizes
  stable recurring knowledge. Neither wording is a measured selection guarantee.
- [Entity resolution](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/hindsight_api/engine/memories/pg/entity_resolver.py)
  uses names and co-occurrence context, with safeguards for differing names and
  numbers. Explicit supplied identities can bypass resolution. This is useful
  alias handling, not proof of signed membership or permission to merge two beings.
- The [history tests](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/tests/test_observation_history.py)
  verify trimming and reclamation when observations are removed. The pinned
  [configuration](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/hindsight_api/config.py)
  defaults to 50 observation-history entries; a nonpositive cap disables trimming.
  This is not an unlimited archive by default. Tests were inspected, not run here.

An evidence count is not independent corroboration: re-importing, quoting or
resummarizing the same encounter must not increase how many encounters occurred.
Preserve source-event identity and revision when testing any formation system.

## Bring mechanisms to the selected backend

The following are proposed mechanisms, not claims of shipped behavior. The
human's later October 7 decision retains HMK for this stage and brings useful
mechanisms into it under the [agreed roadmap](durable-recall-plan.md#agreed-roadmap--2026-10-07).
HMK already has selected episodes, typed links, native revision pre-images and
a finite consolidation manifest with exact episode versions. Build on those
primitives before inventing another canonical event store.

| Mechanism | Existing foothold / next smallest experiment | Acceptance question |
|---|---|---|
| Experience versus interpretation | Preserve a selected self-contained episode; keep person/project/pattern accounts linked through `supported-by` | Can a fresh body recover the encounter after three synthesis passes without the session? |
| Entity/facet matching | Link known handles, repository/issue IDs and people; retain aliases and ambiguous candidates separately | Does a weak cue find the participant without fusing two similar names? |
| Occurrence versus report time | Use native date/precision/source fields; render these in recall | Does a later report of an old event remain old, with unknown dates still unknown? |
| Evidence and counterevidence | Extend the current episode-revision manifest only if support selection needs a finer seam | Does a correction invalidate the affected conclusion while preserving the original reported experience? |
| Freshness and bounded refinement | Compare the account's support fingerprint to the current selected episode revisions | Does new contradictory evidence trigger reconciliation instead of silently serving stale understanding? |
| Multi-path retrieval | Inspect lexical, semantic and linked candidates separately, then test fusion with calibrated relevance | Does the old issue interaction survive newer plausible distractors, without admitting unrelated weak candidates? |
| Procedural learning | Derive a proposed skill from tested repeated actions, preserving source episodes and package history | Can the memory route to a body with the required capability without claiming capability in every body? |

Do not begin by copying a Postgres implementation into SQLite or activating
background dreaming. First compare insertion-only versus staged synthesis on
the existing fictional corpus, including a single meaningful encounter, a failed
or unresolved action and an ordinary shared moment. A current hypothesis and
its prior forms are authored state; do not erase them merely because they could
be regenerated differently by a future model.

## Systems working in this direction

The [completed consolidation report](../research/agent-memory-2026-10-06/agent_reports/01_consolidation.md)
already pins Anthropic dreaming, Letta sleep-time/MemFS, LangMem, LightMem and
Honcho. Its primary citations, metrics and limits remain available. In particular,
LightMem includes configurations where offline updating reduced answer accuracy;
the word dream is not itself evidence of an improvement.

| System | Useful direction | Constraint for our comparison |
|---|---|---|
| Hindsight | Supported observations over experience and entity/time retrieval | History/deletion policy and Postgres runtime remain to qualify |
| Letta | Separate formation process and git-backed memory filesystem | Native harness integration and complete recovery outside Letta |
| Honcho | Observer/subject representations and deduction/induction with sources | Social inferences are interpretations; service stack is heavier |
| LangMem / LightMem | Structured formation, staged/background updates and topic batches | Formation primitives are not a complete lifelong canonical archive |
| Basic Memory / memU | Local readable memory, connected navigation/progressive retrieval and harness seams | Episode selection and history-preserving formation still require testing |
| Soul Protocol | Companion-oriented episodes, social layers, local portable archives and explicit dreaming | Small ecosystem; implementation assumptions and complete journal transport need verification |
| OpenSelf | Local temporal/provenance store, lifecycle-aware context compilation and JSONL transport | Current export inspected below does not serialize the whole lifecycle/graph history |

Two additional independent proposals match the human's framing closely enough
to merit source inspection. Neither is OpenSouls or an adopted industry standard:

- [Soul Protocol at `b6ab6ee3`](https://github.com/qbtrix/soul-protocol/tree/b6ab6ee3bb644a6e27f08af551a155b37c7925c2),
  May 25, MIT, ships a language-independent spec and Python implementation.
  [Memory primitives](https://github.com/qbtrix/soul-protocol/blob/b6ab6ee3bb644a6e27f08af551a155b37c7925c2/src/soul_protocol/spec/memory.py)
  include open layers, participants, source, timestamp/ingestion, supersession
  and open metadata. The [.soul packer](https://github.com/qbtrix/soul-protocol/blob/b6ab6ee3bb644a6e27f08af551a155b37c7925c2/src/soul_protocol/runtime/export/pack.py)
  writes a ZIP of JSON state/memory and an optional trust chain. This code alone
  does not establish a complete backup of the separate org SQLite journal.
  [Dreaming](https://github.com/qbtrix/soul-protocol/blob/b6ab6ee3bb644a6e27f08af551a155b37c7925c2/src/soul_protocol/runtime/dream.py)
  has preview and source episode IDs, but pattern detection here is token-overlap
  heuristics, with archive/dedup/graph-pruning phases. It is not equivalent to
  Hindsight's supported model synthesis. Its personality, bonds and identity
  conventions do not replace Matrix identity or authorize access.
- [OpenSelf at `380785d2`](https://github.com/Open-Self/Open-Self/tree/380785d21d9c7b6ef1d9b1707f2d149ab4c423da),
  September 20, MIT, describes SQLite canon, temporal supersession, entities,
  provenance and bounded context compilation. Inspecting the
  [exporter](https://github.com/Open-Self/Open-Self/blob/380785d21d9c7b6ef1d9b1707f2d149ab4c423da/src/context/exporter.js)
  shows record content/source/scope/dates, but no serialized supersession links,
  graph entities/edges or complete revision ledger in that interchange path.
  Its signed JSONL export is consequently not established as full recovery.
  This is a concrete limitation in the inspected path, not a claim that its
  separate vault-backup operation has the same limitation.

## What OpenSouls has publicly changed

The [official organization](https://github.com/opensouls) exposes three repositories
at inspection. Its engine [README](https://github.com/opensouls/opensouls/blob/0eb05965117c5d46c5643ae38e01856730202137/README.md)
describes a legacy release for digital souls, with immutable WorkingMemory,
cognitive steps, persistent state and vector stores. The latest public engine
[commit](https://github.com/opensouls/opensouls/commit/0eb05965117c5d46c5643ae38e01856730202137)
is February 8, 2026: Vercel AI SDK/model updates, storage/RAG changes. No later
public release in those inspected repositories was established; this does not
rule out unpublished or differently hosted work. The website returned an error.

There are useful existing patterns:

- [Soul-wide keyed memory](https://github.com/opensouls/opensouls/blob/0eb05965117c5d46c5643ae38e01856730202137/packages/beta-docs/pages/blueprints/hooks/useSoulMemory.mdx)
  is separate from individual mental-process state.
- [Samantha's user-learning process](https://github.com/opensouls/opensouls/blob/0eb05965117c5d46c5643ae38e01856730202137/souls/examples/samantha-learns/soul/subprocesses/learnsAboutTheUser.ts)
  updates concise user notes from a recent transcript window;
  [conversation summarization](https://github.com/opensouls/opensouls/blob/0eb05965117c5d46c5643ae38e01856730202137/souls/examples/samantha-learns/soul/subprocesses/summarizeConversation.ts)
  replaces the working summary and retains a recent message tail. These examples
  do not establish a durable episode/revision/evidence contract comparable to
  Hindsight observations. The code is an example, not an upper bound on the engine.
- The current [PGlite storage](https://github.com/opensouls/opensouls/blob/0eb05965117c5d46c5643ae38e01856730202137/packages/soul-engine-cloud/src/pglite.ts)
  persists an embedded PostgreSQL/vector database in a local directory, without
  requiring a remote database. It still comes with the Soul Engine runtime rather
  than being a drop-in SQLite memory library for existing Codex/Hermes bodies.

## Next evidence, tied to the existing plan

First fix the documented HMK pilot's omitted meaningful failed action and old
weak-cue ranking failure, without reducing preservation to successful lessons.
Then compare the local shortlist and selected consolidation mechanisms with
frozen formation/recall conditions, source loss, three passes plus replay,
correction propagation, export/restore and actual second-harness reception.
Qualify semantic preservation independently of each proposed format's structural
conformance. Keep original native learned delta and the current pool recoverable.
No runtime, memory hook, timer, peer attention or live competitor is activated
by publication of this review.
