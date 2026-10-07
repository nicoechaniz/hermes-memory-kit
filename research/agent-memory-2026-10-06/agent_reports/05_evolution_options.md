# R5 — Deployment, portability and evolution options

Research cutoff and access date: 2026-10-06. Status: `complete`.

## 0. TL;DR

- ✅ The seven systems have inspectable OSS code, but licensing differs:
  Honcho's server is AGPL-3.0; HMK, Hindsight and LangMem are MIT; Graphiti,
  Mem0 and current Letta Code are Apache-2.0. Hosted functionality is separate.
- ✅ LangMem exposes storage-independent primitives; Graphiti is a temporal-graph
  library; Hindsight separates retain/recall/reflect. ❓ Compare bounded components
  before replacing canonical storage or a body harness.
- ✅ Hindsight has source-visible repeatable-read backup, whole-bank transfer,
  index rebuilding without fresh extraction and recovery test source. ⚠️ None was
  executed here; this does not prove HMK/Matrix compatibility.
- ✅ Current Mem0 automatic extraction is ADD-only; explicit update/delete/history
  APIs coexist. Hosted schema-shaped exports are not demonstrated full backups.
- ✅ Current Letta Code offers local or Cloud backends, git-tracked MemFS and local
  JSONL transcripts; its README removes the old AgentFile export/import interface.
- ❓ No inspected evidence establishes that HMK's SQLite canon must be replaced.
  Repair preservation first, then compare components on the same continuity cases.

## Question and scope

Which agent-memory components can HMK realistically adopt while preserving a
being's canonical memories, source authority and recovery, and what evidence
would justify a component or system replacement?

This lane inspects primary repositories, licenses and deployment/export
documentation. It does not deploy competitors, benchmark quality, inspect
private memory or change any runtime. Mechanisms and reported retrieval scores
belong to the other lanes. The existing HMK review supplies its baseline.

## Method and evidence limits

- Access date: 2026-10-06; external repositories were pinned to their latest
  inspectable default-branch commit at or before the cutoff.
- Search/discovery log, inspected sections and source/version dates follow below.
- ✅ means an inspected primary description or source, not successful deployment.
  📊 means an author-reported result. ⚠️ marks an experimental or unverified
  property. ❓ marks our recommendation requiring validation.
- A permissive source license does not establish hosted-service portability.
  An API listing records does not establish a complete, verified recovery export.

## Bounded comparison

Inspected: HMK, Hindsight, Honcho, Graphiti, Mem0, Letta and LangMem. These are
seven systems, not seven directly comparable full replacements.

| System | OSS license and service distinction | Local dependencies | Portable evidence and recovery | Appropriate HMK use |
|---|---|---|---|---|
| HMK | ✅ MIT; local toolkit | ✅ Python/SQLite/FTS; chosen optional embedding and ingestion packages | ✅ Inspectable SQL canon; review demonstrates unsafe migration backup/history loss; summary projections are not full backup | ❓ Repair canon writes, snapshots and extraction receipts first |
| Hindsight | ✅ MIT; optional hosted Cloud is separate | ✅ PostgreSQL + pgvector, embedded pg0 option; extraction/reflection LLM; embeddings/reranking | ✅ Consistent schema backup and whole-bank transfer documented; import regenerates embeddings without fresh extraction; tests read, not run | ❓ Read-only retrieval/consolidation comparison after HMK preservation fixes |
| Honcho | ✅ AGPL-3.0 server; managed API separate | ✅ Python ≥3.13 manifest; API + deriver + PostgreSQL/pgvector + Redis in CLI stack; source compose also adds MCP; configured LLM | ✅ Messages and observer/observed representations distinct; PostgreSQL backup/restore documented; external vector-backend completeness unverified | ❓ Study perspective scoping/queue receipts; reuse concepts before incorporating AGPL server code |
| Graphiti | ✅ Apache-2.0 library; Zep managed infrastructure is a distinct offering | ✅ Python ≥3.10; Neo4j/FalkorDB or supported alternatives; inference + embeddings; embedded FalkorDB requires Python ≥3.12 | ✅ Episode-backed temporal graph; complete cross-backend backup/restore not established by README | ❓ Candidate derived temporal/entity index, keeping authoritative source events outside the graph |
| Mem0 | ✅ Apache-2.0 library; hosted graph memory no longer part of inspected OSS graph feature | ✅ Python ≥3.10, configurable vector backend, LLM/embeddings, separate SQLite history/messages; inspected self-hosted compose has API/dashboard/PostgreSQL | ✅ Explicit correction/history APIs coexist with ADD-only extraction; hosted structured export is not a demonstrated full restore artifact | ❓ Compare extraction/retrieval adapters; retain every store for a complete-swap pilot |
| Letta Code | ✅ Apache-2.0 active harness; V1 server retired; Cloud separate | ✅ Node ≥22.19 or Bun ≥1.3.2 manifest; chosen model; local filesystem backend available, Cloud default in README | ✅ Git-tracked MemFS, source-visible JSON/JSONL local records; AgentFile import/export removed; complete restore untested | ❓ Study dreaming/history independently; a full swap also changes body integration |
| LangMem | ✅ MIT toolkit, not itself a hosted durable database | ✅ Python ≥3.10 + LangChain/LangGraph/Trustcall + chosen LLM; functional primitives permit other storage | ✅ README explicitly says `InMemoryStore` loses memories on restart and recommends a DB-backed store | ❓ Strongest bounded experiment is reusing extraction/consolidation primitives with HMK-owned persistence |

## Evolution and replacement gates

### Patterns to bring into HMK now

❓ Preserve the canonical/derived distinction: selected episodes, meaningful
native revisions and external-source projections are primary; embeddings,
entity indexes, current-account summaries and HTML diary views can be rebuilt.
HMK's existing Matrix/Wiki authority boundaries already support this distinction.

❓ Reuse the operational pattern visible in Hindsight/Honcho: durable queued work,
explicit extraction progress, failure/retry state and a retrieval-ready receipt.
A background worker is a deployment option, not permission to add attention to
this manual Codex body. The contract should also work in finite foreground
consolidation requested by the human.

❓ Borrow Hindsight's distinction between complete recovery and rebuildable-index
migration. An HMK export should inventory authoritative records, protected-source
projections, links and all historical variants still available. Re-embedding must
not silently re-extract or reinterpret autobiography. A database change cannot
recover source history that was already lost.

### Components worth evaluating without changing authority

| Candidate | Smallest justified experiment | Evidence gate |
|---|---|---|
| LangMem functional extraction/consolidation | ❓ Adapter takes an authorized delta and selected existing memory; proposed records go through HMK's safe writer | ❓ Provenance, unknown dates, tool communications and idempotent replay survive; gains justify model/dependency cost |
| Graphiti temporal/entity retrieval | ❓ Rebuildable derived index over selected source-attributed episodes | ❓ Weak-cue entity and historical queries improve while invalidated facts/distinct events remain attributable |
| Hindsight recall/consolidation | ❓ Isolated service comparison on fictional fixtures or explicitly selected authorized records, mapped to canon | ❓ Continuity, latency/cost, source links, recovery and retraction propagation pass |
| Mem0 extraction/retrieval | ❓ Version-pinned adapter; automatic extraction distinct from correction/history APIs | ❓ Assistant assertions remain distinct from observed actions; source/effect receipts and retained old episodes survive |
| Honcho perspective modeling | ❓ Study observer/observed separation and durable reasoning queue before a scoped service pilot | ❓ Relationship modeling does not merge being identities, permissions or autobiography; conclusions remain source-bound/retractable |
| Letta dreaming/MemFS | ❓ Compare selection and versioning patterns before replacing the harness | ❓ Existing body foreground behavior, signed membership and maintained skills keep their authority |

### What would justify replacement?

- ❓ **Replace or accelerate an index** if measured scale/latency or recall failures
  persist after cue extraction, relevance gating and provenance fixes, and a
  rebuildable alternative improves the same acceptance cases within the agreed
  cost/resource budget. SQLite can remain canonical storage.
- ❓ **Replace extraction/consolidation** if another implementation retains more
  selected meaning, introduces fewer false autobiographical claims and passes
  retry/idempotency/attribution tests. Extraction quality alone does not establish
  storage safety or a migration contract.
- ❓ **Change canonical storage/architecture** only when a required behavior cannot
  reasonably be maintained in HMK—for example a measured concurrency/scale/recovery
  limit—and a candidate demonstrates lossless available-corpus migration,
  corrections, receiving scope and verified rollback. Audited write/API defects
  do not automatically disappear with another database.
- ❓ **Replace the whole system** only after passing continuity and operational
  acceptance across authorized bodies. Leaderboard position, repository
  popularity, a graph abstraction or hosted availability is insufficient.

❓ Declare critical recall cases, latency/cost/resource budgets and acceptable
restore time before comparison. Require zero lost canonical records and zero
source-authority or cross-being violations in the migration fixture. Choose
quality targets from the evaluation lane, not incompatible vendor scores.

## Migration and rollback acceptance

All steps below are ❓ proposed acceptance requirements; none was executed here.

1. **Inventory and authority map.** Record available corpus version, counts/hashes,
   durable IDs/aliases, source/body/event references, links, native history,
   corrections/retractions, date precision and mode of knowing. Mark historical
   gaps explicitly. Matrix events and independently authored Wiki files keep
   their authorities; import projections rather than competing equivalent events.
2. **Verified rollback first.** Obtain a consistent snapshot and validate integrity,
   metadata and representative retrieval from an isolated restore. Include
   selected assets or an explicit missing-asset manifest, required nonsecret
   configuration, learned skills and software/model versions. A summary vault,
   current-person profile or extraction-shaped export is not this recovery artifact.
3. **Versioned transport.** Export canonical text/metadata/history in a documented
   format with checksums and an old-to-new local-ID map. Preserve authoritative
   portable source IDs unchanged. Import deterministically, preserve unknown
   dates and rebuild indexes without fresh autobiography extraction.
4. **Incremental replay.** Keep one canonical write authority during comparison.
   Replicate a versioned delta/outbox with stable idempotency keys, explicit
   applied/skipped/deferred/error receipts and corrections/retractions. Independent
   model-written histories from dual-writing both systems are not replication.
   Source-event ID plus source version identify the logical encounter; policy and
   model versions identify a processing decision/job. Reprocessing under a new
   policy can extend/revise the same source account, not create a new encounter.
5. **Read-only shadow and receiving acceptance.** Query both on the same authorized
   fixture. Measure retained meaning, critical recall, provenance, null/degraded
   results, latency/cost and late/concurrent updates. Check source isolation and
   each receiving body's actual access/capabilities. Bank, peer, user, namespace
   or project IDs never establish signed being membership.
6. **Bounded cutover with rollback.** After deployment authorization, quiesce
   canonical writes or drain a verified delta, record the final checkpoint,
   recheck counts/hashes/critical queries and change reader/writer binding.
   Preserve source snapshot and rollback that accounts for new target-side writes.
   Stop if committed memory or source boundaries are lost. Leaving both old and
   new systems independently writable does not provide rollback.

❓ Local self-hosting establishes who operates storage; local inference establishes
where selected memory goes during model calls. Evaluate both independently.
Preserve the body's configured provider and real authorization rather than
silently adopting defaults from an imported package.

## Search and inspection log

- Initial read: this investigation's MANIFEST and the published HMK general-memory
  review. Existing diagnostics establish preservation gaps; their runtime fixes
  remain pending.
- Inspected pinned LICENSE, relevant README deployment/storage sections and
  dependency manifests for Hindsight, Honcho and Graphiti. GitHub tree listings
  were used to locate recovery and deployment documentation. Long README output
  was excerpted and some initial output was truncated; only the sections actually
  reopened/read support findings.
- Two web discovery queries: `site.hindsight.vectorize.io export bank backup
  database pg_dump` and `site.docs.honcho.dev self host export backup postgres`.
  Search snippets are discovery only; unrelated Procfile `honcho` exports were
  excluded. Supporting documentation was checked against pinned repository files.
- Read Hindsight's pinned admin-CLI backup/export/import/blue-green sections and
  backup-roundtrip test excerpts. Read Honcho's pinned self-hosting guide including
  its PostgreSQL backup/restore commands. Read LICENSE/README/manifest sections
  for Mem0, Letta and LangMem. No advertised benchmark scores were used to rank
  deployment suitability.
- Followed Letta's primary-source pointer to active `letta-code`, pinned by the
  same cutoff; inspected LICENSE, README, manifest and local-store/transcript/path
  excerpts. Inspected Mem0's pinned migration guide, explicit correction/history
  APIs, SQLite history/messages and hosted export cookbook.
- Search count: two web discovery queries. Source scope: seven systems; Letta
  spans historical/current repositories. Commit/tree lookups establish versions
  and locate files, not deployed behavior. No candidate deployment, private
  corpus upload or quality benchmark was performed.

## Source ledger

- ✅ **Hindsight source** — [repository at `9269b884`](https://github.com/vectorize-io/hindsight/tree/9269b88417ed263e5a8350f2e416ca2b322756b1), commit 2026-10-06 16:21:45 UTC. Inspected LICENSE, README Quick Start/embedded/core concepts/production table and workspace manifest; recovery guide listed separately below.
- ✅ **Honcho source** — [repository at `ae4a1575`](https://github.com/plastic-labs/honcho/tree/ae4a157578691c985154e759b968b8a2181ad929), commit 2026-10-06 21:11:09 UTC; manifest version 3.2.2. Inspected LICENSE, README local-stack/peer-representation sections and `pyproject.toml` dependencies.
- ✅ **Graphiti source** — [repository at `aa5bb270`](https://github.com/getzep/graphiti/tree/aa5bb2706929fce502d99d8c7c4ddbb77bff4995), commit 2026-10-06 20:43:26 UTC; manifest version 0.30.2. Inspected LICENSE, README Graphiti versus Zep/deployment/backend sections and `pyproject.toml`. Kuzu is explicitly deprecated at this revision; it is not a sound new embedded-backend recommendation.
- ✅ **Hindsight Admin CLI and recovery test source** — [pinned guide](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-docs/docs/developer/admin-cli.md). Same commit/date as above; inspected backup consistency/coverage, destructive restore and bank-migration rollback runbook. [Roundtrip tests](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/tests/test_admin_backup_restore.py) assert table coverage and restored IDs/text/timestamps/metadata/vectors; read, not executed. Bank transfer is PostgreSQL-only, needs a fresh target bank and regenerates embeddings; operational history is opt-in. This differs from full schema backup retaining operational tables.
- ✅ **Honcho local environment** — [pinned self-hosting guide](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/docs/v3/contributing/self-hosting.mdx). Same commit/date as above; inspected services, model requirement, deriver readiness, migrations and PostgreSQL backup/restore. README minimum Python 3.10 conflicts with package minimum 3.13; package manifest governs installability at this revision.
- ✅ **Mem0 source** — [repository at `c93420c4`](https://github.com/mem0ai/mem0/tree/c93420c49a6b14c3d446bdb156d96811908fd90a), commit 2026-10-05 15:22:59 UTC; Python package 2.2.1. Inspected LICENSE, README library/self-hosted/Cloud distinction and manifest. README describes an April-2026 ADD-only algorithm; earlier update/delete research is not automatically this version's behavior.
- ✅ **Letta historical/current-source pointer** — [README at `5bcdd177`](https://github.com/letta-ai/letta/blob/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a/README.md), commit 2026-09-10 17:59:06 UTC; LICENSE Apache-2.0. Inspected complete short README: active source is `letta-ai/letta-code`, historical V1 API server retired on `archive` branch.
- ✅ **LangMem source** — [repository at `48e3c11f`](https://github.com/langchain-ai/langmem/tree/48e3c11f5bb527282c7d5339c6a87a0b35abccfc), commit 2026-10-02 19:35:19 UTC; package 0.0.30. Inspected LICENSE, complete README and manifest; functional core versus LangGraph tools and ephemeral versus persistent-store distinction.
- ✅ **Current Letta Code source** — [repository at `4b028fab`](https://github.com/letta-ai/letta-code/tree/4b028fab07c69edaac2ddb4f7b9a43573ff20d81), commit 2026-10-05 23:06:21 UTC; package 0.34.4, Apache-2.0. Inspected README backend/MemFS/removed AgentFile sections, package manifest, [local store](https://github.com/letta-ai/letta-code/blob/4b028fab07c69edaac2ddb4f7b9a43573ff20d81/src/backend/local/local-store.ts), transcript schema/manifest and MemFS paths. Source exposes JSON/JSONL local records; neither this read nor git-tracked memory proves whole-body verified restore.
- ✅ **Mem0 versioned extraction, correction and portability** — [migration guide](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/docs/migration/oss-v2-to-v3.mdx), [memory implementation](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/main.py), [SQLite history/messages](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/storage.py) and [Platform export cookbook](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/docs/cookbooks/essentials/exporting-memories.mdx). Same pinned commit/date as above. Automatic `add` now emits ADD-only; explicit `update`/`delete`/`history` remain, reconciling current default and history APIs. Hosted schema exports may resolve conflicts and downloads expire in seven days: neither proves complete recovery. Migration guide removes OSS external graph integration and says Qdrant BM25 requires `fastembed`.
- ✅ **HMK baseline/license** — [source at `3d841eb`](https://github.com/nicoechaniz/hermes-memory-kit/tree/3d841eb97f5ab7c59d8420d3ad0652c1243da7de), [MIT LICENSE](https://github.com/nicoechaniz/hermes-memory-kit/blob/3d841eb97f5ab7c59d8420d3ad0652c1243da7de/LICENSE) and [general-memory review](../../../docs/general-memory-review.md), reviewed 2026-10-06. License/README inspected here; preservation/authority findings reused from the source-grounded review and disclosed synthetic diagnostics.

## Open questions

- ⚠️ End-to-end restore/receiving acceptance remains untested for every candidate.
  Hindsight has the clearest inspected recovery contract, but compatibility with
  HMK selected records/protected sources still requires a fixture.
- ⚠️ Hosted parity, export completeness and model-data processing depend on the
  deployment/service contract; OSS licenses cannot establish these properties.
  No hosted account was created or private corpus uploaded.
- ❓ Which measured HMK limit justifies extra services? No workload/scale result
  was generated here, so this lane supplies no replacement deadline.
- ⚠️ Honcho README/manifest disagree about Python, and README/guide examples differ
  about default providers. Check pinned package/effective configuration instead
  of relying on a remembered quickstart.
