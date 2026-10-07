# Lifelong being memory: portability and replacement review

Reviewed on 2026-10-07. This additive review responds to the human's report that
Mariano now uses native Codex memory with collective-memory, and to the clarified
goal: a being carries a shared life across bodies and years, including when
original sessions are unavailable. Keeping HMK is not itself an acceptance
criterion. The [durable-recall plan](durable-recall-plan.md) remains the work
record; [issue #11](https://github.com/nicoechaniz/hermes-memory-kit/issues/11)
owns the native/replacement comparison.

## Import exists; universal memory interchange is not established

The official [import documentation](https://learn.chatgpt.com/docs/import)
explicitly lists Claude Code project memories separately from chats and
instruction files. In installed Codex `0.160.0`, pinned to
`a956835d020762cb2b570053af06f643a11c0ecc`, the
[discovery code](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/external-agent-migration/src/memory.rs)
recursively finds Markdown under each external project's `memory/` directory.
It uses available session metadata to resolve a reliable, existing project cwd;
it does not need to import those chats as the memory content. Unresolved scope
can prevent a project's memory import. Symlinks and non-Markdown files are skipped.
Discovery here does not establish coverage for every custom memory location.

The [importer](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/external-agent-migration/src/memory_import.rs)
copies selected files into an external-memory extension, writes project scope,
and queues consolidation when the workspace changes. Its interpretation rules
preserve source frontmatter and file hierarchy, keep detailed resources apart
from the global index, and forbid fabricated native thread IDs or timestamps.
Consolidation must not edit those imported resources. Re-import can replace a
selected project's resources, so this is not an immutable migration archive.

This is an implemented, source-specific adapter. Markdown makes text readable
across tools; it does not standardize identity, episodes, revisions, corrections,
support, retention, perspectives or retrieval. Claude's
[documented auto-memory](https://code.claude.com/docs/en/memory) is a project-local
index plus topic files, read and written during interaction. Codex's background
extraction/consolidation is a different lifecycle. No inspected source establishes
a shared, lossless memory schema adopted by both products. MCP and shared agent
instructions/skills are interfaces, not evidence of such a schema.

## What native Codex stores and how it selects

The [native pipeline](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/memories/README.md)
has per-thread extractions in its local SQLite state database and consolidated
filesystem memory under the selected Codex home. V1 maintains `MEMORY.md`,
`memory_summary.md`, supporting summaries/resources and optional learned skills;
V2 has a different output contract. The
[local backend](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/ext/memories/src/local.rs)
implements list/read/search/note over files. Its
[search implementation](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/ext/memories/src/local/search.rs)
matches text with normalization and line/window modes; this inspected path is
not an embedding/vector database. Models perform extraction, consolidation and
query interpretation. A backend trait exists, but the installed extension
constructs the local backend directly; no configuration-only HMK substitution
was established.

The [extraction prompt](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/memories/write/templates/memories/stage_one_system.md)
prioritizes stable preferences, reusable procedures, reliable task maps and
future user time saved. That overlaps with the being's learned delta but does
not require preservation of each meaningful encounter without a reusable lesson.
This is a prompt-level scope finding, not an executed native capture comparison.

[State selection/pruning](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/state/src/runtime/memories.rs)
ranks usage and recency, bounds the consolidated input set and deletes stale,
unselected stage-1 outputs. Summaries outside the selection are removed. The
[V1 consolidator](https://github.com/openai/codex/blob/a956835d020762cb2b570053af06f643a11c0ecc/codex-rs/memories/write/templates/memories/consolidation.md)
instructs removal of memory supported only by deleted inputs and cleanup of
low-signal or stale content. This does not mean that all memory expires at one
fixed age. It does mean that an unused significant episode has no demonstrated
lifelong preservation guarantee. The workspace's resettable git baseline is
not a retained autobiographical revision archive.

## Mariano's accessible current setup

The human's report of Mariano's current use is new evidence; the earlier April/
July HMK proposals do not establish his present choice. Independently read on
October 7: the mounted root contract, content updated September 28, directs
Codex to consult the collective map and project submaps; relevant work goes to
project documentation/bitacoras, and a manually invoked bibliotecario compiles
the map. Its public implementation remains
[collective-memory at `ca048630`](https://github.com/Mar-IA-no/collective-memory/tree/ca0486307aea6ea8ec65f70ffd5ba32fd56b8850),
July 29, as verified again through repository metadata. The
[earlier source review](mariano-memory-research-review.md) explains its filtered
corpus, thematic synthesis and serving/index boundaries.

The accessible contract establishes Codex plus shared corpus consultation and
curation. The selected root contract, administrative-memory references,
bibliotecario runbook and published memory research do not establish a direct
native-memory-to-collective-memory bridge. The mounted project-local `.codex`
directory is empty; this is not Mariano's actual native Codex home. Its memory
settings/artifacts and a receiving restoration were not inspected. Therefore
the precise native integration and preservation behavior remain unqualified;
do not infer their absence from this bounded access.

## Candidates closer to a shared life

The closed [five-lane investigation](../research/agent-memory-2026-10-06/README.md)
already examines Hindsight, Honcho, Letta, Mem0, Graphiti and LangMem. The new
lifelong framing also warrants memU and MemOS, which were not qualified in that
seven-system deployment matrix. Descriptions below are inspected architecture,
not a competitor deployment or a cross-body acceptance result.

| Candidate | Relevant implemented/documented mechanisms | Required comparison for this being |
|---|---|---|
| HMK, repaired fork | Being-bound pool, selected records, revision pre-images, source/mode/date metadata, hybrid recall, finite capture and supported consolidation | Selection and weak-cue recall remain faulty in the partial model pilot; mechanical safety is not sufficient |
| Codex + collective-memory | Native learning plus independently maintained shared documents, map and retrieval | Establish actual publication seam, lifelong episode retention, native learned-delta backup, and access from another harness |
| Hindsight | Retained experience, entity/temporal retrieval, evidence-linked observations, bank transfer/recovery tooling | Preserve selected meaning without original transcripts, qualify historical changes/identity resolution, measure cost and actual restore |
| Honcho | Peers beyond users, observer–subject representations and attributed reasoning | Distinguish this being's autobiography from interpretations of others; qualify evidence sufficiency and historical preservation |
| Letta Code | MemFS, git-backed memory and dreaming with a persistent agent | A whole-harness swap changes body integration; memory alone must remain usable outside Letta and fully restorable |
| memU | Shared memory/skill store, host adapters, agent-authored Markdown and progressive retrieval | Qualify Linux Codex formation, significant episode selection, history, source scope and safe portability; README's integration matrix reports Linux Codex formation limitations |
| Basic Memory | Local Markdown knowledge graph, SQLite text/vector indexes, local MCP/CLI and harness integrations | Preserve immutable IDs, selected episode history and corrections beyond editable notes; qualify local reconstruction and independent receiving recall |
| MemOS | MemCube abstraction, memory lifecycle/provenance, heterogeneous memory management | Test actual available-history transport and corrections; a framework's standardized unit is not an industry-adopted format |

Additional primary sources inspected October 7:

- [Hindsight observations](https://hindsight.vectorize.io/developer/observations)
  describes support-linked consolidation and changing understanding;
  [admin CLI](https://hindsight.vectorize.io/developer/admin-cli) distinguishes
  complete backup from bank transfer, with operational history optional.
- [Honcho's directional design](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/docs/v3/documentation/core-concepts/design-patterns.mdx)
  situates peer reasoning and participation; the existing R3/R5 source pins cover
  evidence and deployment. The product overview's claims are not independent
  verification of psychological interpretation or continuity.
- [memU README at `2c050bc9`](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/README.md),
  commit September 21: agent-driven formation, local SQLite/Postgres or Cloud,
  adapters over native history and documented per-host limitations. Its proposed
  schedules and prompt-file patches are not authorized or installed here.
- [MemOS core concepts at `a7367d07`](https://github.com/MemTensor/MemOS/blob/a7367d07e55db61099f7b4e2c1108bc5831a24f3/docs/en/open_source/home/core_concepts.md),
  commit September 22, and [primary MemOS paper](https://arxiv.org/abs/2507.03724)
  describe MemCube provenance/versioning and heterogeneous memory. No inspected
  Codex/Claude importer consumes this format natively.

There is research explicitly aimed at companionship and embodied life, so the
claim that every contemporary system targets only tasks would be too broad:

- [MemoryBank](https://arxiv.org/abs/2305.10250), 2023/2024, explicitly models
  long-term companionship and selective forgetting. Its reported qualitative/
  simulated dialogue evaluation does not establish cross-body lifelong recovery.
- [LifeBench](https://arxiv.org/html/2603.03781v1), March 2026, simulates a full
  year of linked events, conversations, phone and health traces, testing temporal
  updates and inferred habits alongside episodes. It compares multiple memory
  systems; its dataset format is an evaluation format, not a migration standard.
- [LifeSide](https://arxiv.org/html/2606.04660v1), June 2026, evaluates simulated
  24–36-month companion trajectories, partial observability, evolving relations
  and user understanding. It reports shortcomings even with strong memory
  baselines. Those results cannot be transferred to our installed models or
  treated as real years of operation.
- [Hierarchical episodic memory for lifelong robots](https://arxiv.org/abs/2604.11306),
  April 2026, learns relevance from feedback and tests simulated tasks plus
  20.5 hours of real recordings. Useful embodied selection evidence; no decade
  of deployment or multi-harness memory transport is demonstrated.

These sources motivate better tests and reusable components. No inspected source
demonstrates the complete requested contract already operating for years across
authorized bodies. That is a bounded evidence statement, not proof that such a
system cannot exist elsewhere.

## Interchange proposals and maturity

These proposals were inspected as specifications/source, not installed or used
for live migration. Self-description as an open standard is not independent adoption.

| Proposal | Concrete progress | Current qualification |
|---|---|---|
| AIMEM Bundle | JSON, namespaced IDs, chunks/entities/edges, checksums, idempotent import and conformance levels; reference producer/consumer and test corpus | Individual Internet-Draft; no IETF endorsement or demonstrated native Codex/Claude support |
| MIF v2 | JSON Schema, Python/TypeScript libraries, CLI/MCP and adapters; graph/vendor metadata | Draft, first public release; useful immediate transport candidate, history-preserving real-system round trips unqualified |
| AMP (YouTale) v0.1 | Markdown nodes, links, manifest, daily notes, regenerable indexes and git/versioning spec | Reference CLI/MCP/Python and import adapters listed as planned |
| MemCube | Portable framework abstraction with heterogeneous memory and lifecycle metadata | Within MemOS; no established native Codex/Claude adoption |
| MEMORY.md | Readable indexes/supporting Markdown in several harnesses; specific Claude-to-Codex import | Shared convention, different semantics and retention; not full interchange |

[AIMEM `-00`](https://www.ietf.org/archive/id/draft-vu-aimem-bundle-00.html),
June 14, has [individual-draft status](https://datatracker.ietf.org/doc/draft-vu-aimem-bundle/),
not formal standards-process standing. The [reference server](https://github.com/memoryai-dev/aimem-reference)
explicitly covers encoding/transport, not production memory reasoning. Its
non-expiry invariant protects selected identity/preference/decision/procedure
classes and pinned chunks; an unpinned episode is not automatically protected.
Revision history, observer/source modes and occurrence-time precision need mapping.

[MIF at `2162e8e0`](https://github.com/varun29ankus/mif-spec/blob/2162e8e031b61223c61464913cd6ae16ec2f5349/spec/mif-v2.md)
requires preservation of unknown fields/types and vendor extensions on round trips.
Optional versions and graph invalidation timestamps are useful; required
content/ID/creation fields do not require full revisions or distinguish occurrence
from report time. Its `tests/round_trip.py` checks JSON serialization identity,
not restore between actual systems. Other adapter/model tests were located, not run.
The [MIF proposal to MCP, PR #2342](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2342)
was closed without merging: maintainers asked for agreement among memory
implementers before making memory format part of MCP. Transport compatibility
does not establish memory-schema compatibility.

[AMP at `5ab36049`](https://github.com/agentmemoryprotocol/agentmemoryprotocol/tree/5ab36049c6004dd7d86d5508b3293a8ca5c88c3e)
is the YouTale proposal linked by `agentmemoryprotocol.io`. Its implementation
roadmap remains future work; similarly named projects are not one adoption
community. The separate [Cromus MEMORY.md proposal](https://github.com/cromus-ai/memory-md-spec)
does not establish that Codex or Claude implement its identity/context/handoff schema.

Compare MIF and AIMEM as offline export envelopes before choosing a standard or
adding dependencies. Test all available revisions, corrections/retractions,
supporting episodes, dates/precision, source modes, body identities and unknown
fields. Keep attributed originals where semantic mapping is not demonstrably
lossless. Readable Markdown can provide navigation; embeddings can be rebuilt.
Checksums do not authenticate membership or source authority. This transport
work applies to HMK or a replacement; it does not solve memory selection itself.

## A compatible subset without discarding the being's history

The October 7 storage preference changes the evaluation order: prioritize a
being-owned directory and SQLite over a mandatory hosted API or complex service
stack. This is a deployment requirement independent of the interchange envelope.
No inspected system was established to implement MIF, AIMEM and AMP together
out of the box. Several can represent the shared content with explicit adapters;
none has passed that cross-system comparison here.

A literal intersection is small: identifiable text records, a declared kind and
creation/modification metadata, with optional connections. The proposals differ
in ID syntax, taxonomies and which fields are required. That core alone cannot
meet the being's preservation contract. Use two levels:

1. A broadly readable projection: stable logical record mapping, sufficient
   self-contained text, an open original type plus mapped destination type,
   recorded/modified dates, tags, named references and supported links where
   the destination accepts them.
2. A complete preservation package: selected episode originals, available
   revisions and retractions, source/body/perspective, occurrence/report/record
   dates and precision, references/aliases, support and counterevidence, selected
   media and hashes, original native learning, and a declared mapping/loss report.
   Keep this alongside the projection when the destination cannot preserve it.

The second level is our required profile, not a claim of consensus among the
proposals. Embeddings and search indexes are replaceable derivatives. Authored
learnings and consolidated understanding are meaningful state: preserve their
available history even when rebuilding an index or generating a new projection.

| Semantic element | MIF | AIMEM Bundle | AMP | Mapping requirement |
|---|---|---|---|---|
| Logical identity | UUID v4, optional external ID | Producer-namespaced URN; tenant UUID/URI | File/node IDs and links | Reversible ID table; never infer being authority from an ID |
| Self-contained text | `content` | Chunk `content` | Markdown body | Selected meaning must survive source/session loss |
| Kind and dates | Types, creation/update and optional metadata | Closed memory-type enum and creation date | Node types, created/modified frontmatter | Keep original type and occurrence precision when mapping |
| People and connections | Entities, related IDs, optional graph | Entities and edges | Node links/relations | Preserve known identifiers and aliases; similarity is not identity |
| Revision and evidence history | Optional version/source/metadata; unknown fields must survive | Required core does not mandate our full ledger | Versioning specification; implementation planned | Namespaced extension or untouched original package; test consumers rather than assume preservation |

Start by validating MIF and AIMEM envelopes against a fictional fixture, then
perform actual write/export/import/restore in each candidate. JSON serialization
identity, an MCP connection or readable Markdown does not qualify that cycle.
If an adapter drops a correction, unknown field or historical support, record the
loss and retain the original; do not advertise the projection as complete backup.

## Local persistence and operational cost

This is source inspection, not a resource benchmark. Local storage does not by
itself imply offline model inference; formation and retrieval providers must
be configured and measured separately.

| Candidate | Canon and local runtime | Advantage to test against HMK | Material remaining work |
|---|---|---|---|
| HMK | Python commands/provider; SQLite pool with selected records, links and native revision pre-images | Existing being bindings, protected-source routing and verified snapshots/rollback | Selection, weak-cue recall, measured consolidation and complete interchange adapters |
| Basic Memory | Markdown knowledge files; default SQLite with FTS and sqlite-vec, local MCP/CLI; local FastEmbed option | Human-readable canon, file editing/Obsidian, graph navigation and documented Codex/Hermes integrations | Durable revision policy and logical IDs through rename/edit, autobiographical selection, exact reconstruction outside its own harness |
| memU | SQLite resource/recall-file/segment models; optional Postgres/Cloud; agent-authored memory/skill tracks | Progressive retrieval and separation of memory, skills and original resources | Current documented host limitations; inspected models show created/updated timestamps but not a full immutable revision ledger |
| Letta Code local | Local JSON/JSONL agent state plus git-backed MemFS; headless mode or optional App Server | Separate formation/dreaming and versioned memory workspace | It is an agent harness; qualify use as independent memory in existing bodies and complete recovery |
| Native Codex | Local state SQLite and filesystem learning; compiled local memory backend | Built-in extraction/consolidation without another storage service | Preserve native learned delta and significant unused episodes; prove another harness can recover and use them |
| Hindsight | Postgres/pgvector; embedded pg0 for local development; Python programmatic/API modes | Entity/time-aware retained experience and evidence-linked observations | More storage/runtime machinery than SQLite; qualify full history, replacement/deletion behavior and recovery cost |
| Honcho / graph or broader memory frameworks | Locally deployable, with additional services in the inspected deployment matrix | Directional social understanding or specialized temporal graph mechanisms | Justify service stack and show benefit over local primitives before adoption |

Basic Memory was inspected at
[`53d1c466`](https://github.com/basicmachines-co/basic-memory/tree/53d1c466143b315546f5cc5338d076ce9c1328e0),
October 7, AGPL-3.0. Its [local quickstart](https://docs.basicmemory.com/start-here/quickstart-local),
[knowledge format](https://docs.basicmemory.com/concepts/knowledge-format) and
[configuration](https://docs.basicmemory.com/reference/configuration) establish
Markdown content and SQLite indexes. Redis, Postgres and Milvus are optional
for that local configuration. Local backups/history remain operator-managed;
cloud snapshot features must not be attributed to the local deployment. Custom
frontmatter offers a representation seam, not tested preservation of our profile.

memU's [SQLite models](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/src/memu/database/sqlite/models.py)
provide UUID IDs, content/resources/tracks and created/updated dates. Its
[SQLite guide](https://github.com/NevaMind-AI/memU/blob/2c050bc9681a4c0aff1af211a000e73d14f33356/docs/sqlite.md)
describes brute-force cosine retrieval and single-writer persistence; some table
descriptions retain older names, so use the pinned models for the actual shape.
A copying example is not evidence of safe backup of a live WAL database.

Letta's [local store](https://github.com/letta-ai/letta-code/blob/4b028fab07c69edaac2ddb4f7b9a43573ff20d81/src/backend/local/local-store.ts)
persists JSON agent/conversation state and JSONL transcripts. Its
[App Server documentation](https://docs.letta.com/self-hosting/app-server)
distinguishes local state from Cloud and one-shot headless execution from an
always-on server. Hindsight's [storage guide](https://hindsight.vectorize.io/developer/storage)
documents automatic local pg0 when no database URL is supplied: it does not
require Cloud or a separately managed remote Postgres by default. It still runs
Postgres/pgvector and needs a consistent cluster backup/restore procedure.

Under this preference, Basic Memory and memU are the first alternative-backend
comparisons; Letta MemFS and Hindsight are also mechanism sources. Retain native
Codex learning in the comparison, without assuming its retention policy supplies
lifelong autobiography. Prioritization is an engineering judgment from the
deployment shapes, not a measured quality ranking.

## Another architecture: portable being history and harness-native projections

The human added this route on October 7: use each harness's native memory while
preserving the being in its own portable representation. That changes the main
comparison from choosing one memory engine to qualifying preservation, formation
and projection seams. HMK may remain a retrieval/projection adapter or be
replaced; neither outcome defines the being.

The inspected Matrix source at
[`196ec721`](https://github.com/AlterMundi/daimon-matrix/tree/196ec7219f954cf4e514a1f61ae72eb3451d851e)
already contains an important part of this design:

- [Origin-retaining memory lanes](https://github.com/AlterMundi/daimon-matrix/blob/196ec7219f954cf4e514a1f61ae72eb3451d851e/specs/memory-boundaries.md)
  represent accepted assertions, corrections and retractions as immutable
  successors, with personal-experience/insight/skill categories, author/context,
  evidence and exact content references. Admission authenticates origin and
  policy; it does not establish that an inferred conclusion is true or useful.
- [DM-034](https://github.com/AlterMundi/daimon-matrix/blob/196ec7219f954cf4e514a1f61ae72eb3451d851e/docs/dm034-memory-projection.md)
  already projects accepted personal-memory heads into HMK. For those lanes,
  Matrix is canonical and HMK is a derived retrieval view. Its exact target
  contract and provenance namespace remain separate from HMK-native records.
- The ledger does not itself own the bytes named by every memory content
  reference. The projection contract explicitly treats unavailable content as
  unavailable, even after signed-event sync. A portable package must preserve
  the exact referenced bytes and available revisions, not just events/hashes.
- Existing HMK-native records and native harness learning are not automatically
  present in accepted Matrix lanes. DM-034 explicitly refuses to hide such an
  import inside projection cutover. Preserve them with original attribution;
  design the source/admission migration instead of fabricating body occurrences.

This is source/contract inspection, not a new claim of installed-runtime
capabilities or a live migration. Reuse the existing versioned Matrix contracts;
do not introduce unknown fields into their closed v1 schemas. Any richer memory
content profile, manifest or new projector needs an explicit versioned seam.

The proposed local preservation package has three related parts:

1. Accepted being history and its reference closure: memory events, exact
   content, meaningful revisions, sources, corrections, selected assets and
   applicable identity/skill history, retaining original authorship and scope.
2. Original native learned artifacts and their available history/lifecycle state,
   initially preserved as attributed originals. Selection can admit new durable
   insights or skills with links back to them; a projection cannot silently
   replace those originals.
3. Regenerable or versioned harness projections plus a reconstruction manifest:
   native indexes/topic files, HMK/SQLite views or other local retrieval engines,
   named source versions, adapters and observed reconstruction/recall results.

Credential custody and body-specific runtime bindings are separate from a
shareable memory/identity package. Restoring a new body is not copying a live
writable ledger or another body's private keys. Same-being synchronization and
foreign attributed knowledge retain their existing Matrix boundaries.

Each harness can form useful memory natively. A bounded explicit capture path
then evaluates genuinely new authored learning/experience, records attribution
and preserved originals, and produces a successor projection for other bodies.
Reading a projection must not be fed back as a new experience or supporting
source. Native cleanup affects its local view; it must not delete the only copy
of significant history. This lifecycle remains to qualify; no automatic observer
or native memory is activated here.

An archive alone is insufficient: after native pruning, a fresh body still needs
a documented path to discover and retrieve older memories. A routing summary,
topic files or a local archive query tool must recover the weak-cue encounter,
not merely make its bytes recoverable by an operator. Measure that independently
of native session resume and compare how much adapter work each harness needs.

## ResonantNetwork as associative memory and learned state

The human also supplied the earlier
[Resonant Neural Net exploration](https://hackmd.io/@nicoechaniz/ResonantNeuralNet).
Read through its public Markdown download on October 7; no private conversation
was imported. It is a dialogue exploring harmonic/phase organization, a trained
interference configuration and query-as-excitation (Jpsh!), rather than an
implemented or validated durable-memory system. Publication date is not supplied
by the retrieved text.

Later human clarification: the intended harmonic resonant system can be a
stable storage medium, not necessarily a training space. Evaluate encoding,
retention and query/readout separately from any learned-embedding experiment.
The local portable archive remains the recovery basis while that proposal is
unqualified.

This provides two distinct experimental roles:

- Associative retrieval: a partial cue activates related episodes/entities or
  concepts; return stable record IDs and evidence rather than treating a recalled
  blend as an authenticated event. Compare with existing lexical/vector/graph
  retrieval on the same old weak-cue and correction cases.
- Learned being state: if the network accumulates meaningful associations or
  structure that selected text does not fully reproduce, preserve that learned
  delta as a versioned original artifact too. Record architecture/encoding,
  baseline/version, parameters/phase state, numeric precision, update recipe and
  supported record mapping. Do not call it disposable merely because it serves
  retrieval; test reconstruction and cross-body behavioral continuity.

[Modern Hopfield networks](https://arxiv.org/abs/2008.02217) provide a concrete
primary associative-memory reference with continuous states and an attention-
equivalent update under that model. They do not validate this specific harmonic
proposal. Infinite phase capacity, instantaneous inference and general quantum
equivalence in the exploratory dialogue are not established engineering results.
The experiment must specify a finite representation, noise/precision, observable
cost, collision/ambiguity behavior and how new learning changes old recall.

The human specifically recalled interest in superadditive capacity. Keep it as
a measured hypothesis: with N independent phase coordinates and M distinguishable
values per coordinate there are M^N configurations, whose maximum information
is N log2(M) bits. Pairwise interference counts do not establish independent
stored information. A useful gain would instead be demonstrated as more
correctly retrievable associations/episodes per comparable storage and inference
budget, robust partial-cue recall, or less interference when adding new learning.
Specify the encoder, state update and readout before running a harmonic model;
compare against local vector/graph and an associative baseline on the same data.

Run this as a bounded research track after a safe archive/projection baseline.
The preservation format should permit such attributed learned-state artifacts
without requiring every body to execute the same neural substrate. When a body
cannot use it, report that capability gap and retain usable evidence/text plus
the original state. A byte round trip alone does not prove continuity of uptake.

## Decision: preserve the being's delta; qualify the backend

Native Codex-authored learning is itself part of the being's accumulated delta.
It cannot be classified as disposable merely because HMK also receives a summary.
Preserve native learned artifacts, their available history, provenance and the
state needed to resume their lifecycle independently of any selected projection.
A migration must inventory what it keeps, compresses, transforms or cannot carry.
Do not claim that one summary or an embedding is an equivalent identity backup.
Native session continuity remains a distinct surface.

The human's later October 7 decision retains HMK for this stage, brings the
researched mechanisms into it and then tests native Codex alongside it. The
[agreed roadmap](durable-recall-plan.md#agreed-roadmap--2026-10-07) makes the
remaining quality, consolidation, portable-content and receiving work explicit
before native activation. Native import or Mariano's project workflow does not
justify discarding this being's memory, and incumbent status alone does not
prove HMK is sufficient. Basic Memory and memU remain future replacement options;
a competitor deployment is not a prerequisite for the next improvements.
Hindsight, Letta, Honcho and other systems contribute mechanisms to test in HMK. The
[mechanism review](experience-consolidation-mechanisms.md) records this work,
including the current OpenSouls source and additional local proposals.

Matrix already has a [merged offline archive producer](https://github.com/AlterMundi/daimon-matrix/pull/261)
and [receiving continuity issue #263](https://github.com/AlterMundi/daimon-matrix/issues/263).
Reuse those artifacts rather than creating another exporter or continuity task.
The producer's documented original-file/SQLite preservation does not by itself
close external content references or its deferred Git-history adaptation. Those
remaining properties belong in the preservation/receiving qualification. Matrix
#262 owns a Telegram convergence pilot and is not the memory roadmap parent.

Use the same hidden-rubric fictional corpus and actual formation lifecycles.
Compare capture, historical correction, weak-cue recall after source loss,
repeated consolidation, verified export/restore and a receiving context in a
second harness. Add a meaningful failed/unresolved action, a shared ordinary
moment and a learned procedure tied to a body's real capabilities. Advance the
retrieval clock, add newer distractors, and test recall of old unused episodes.
Neither a leaderboard nor simulated age alone proves real decade-long operation.

Choose among adopting a system, adopting components, or retaining HMK from the
measured missing work and operational cost. The durable-memory contract should
survive that choice. Existing HMK records and native learned memory must remain
recoverable through any trial; no live native capture, hooks or competitor is
activated by this review.
