# BIBLIOGRAPHY — agent memory and consolidation

Deduplicated canonical URLs from the five raw source ledgers. Date records and
code corroboration are included as verification sources, not independent
performance studies. ✅ inspected primary description; ⚠️ proposed/experimental.
All access dates: 2026-10-06. Author-reported quality is marked 📊 in reports.
Exact method/limitations live in the owning raw report; living docs may change.

## [R1] consolidation

- ✅ [Anthropic Managed Agents announcement](https://claude.com/resources/articles/new-in-claude-managed-agents) — 2026-05-19 Announcement, dreaming and customer-result sections. Owners: R1:C01.
- ✅ [Anthropic Dreams API](https://platform.claude.com/docs/en/managed-agents/dreams) — Undated current docs; `dreaming-2026-04-21` API gate Inputs, staging, instructions, lifecycle, output and failure behavior. Owners: R1:C02.
- ✅ [Sleep-time Compute](https://arxiv.org/html/2504.13171v1) — v1, 2025-04-17 Introduction, experiments, cost assumptions, software case and limitations. Owners: R1:C03.
- ✅ [metadata](https://arxiv.org/abs/2504.13171) — v1, 2025-04-17 Introduction, experiments, cost assumptions, software case and limitations. Owners: R1:C03.
- ✅ [Letta sleep-time implementation announcement](https://www.letta.com/blog/sleep-time-compute/) — 2025-04-21 Agent separation and configuration. Owners: R1:C04.
- ✅ [LangMem background quickstart](https://langchain-ai.github.io/langmem/background_quickstart/) — Undated current docs Manager, store persistence and processing patterns. Owners: R1:C05.
- ✅ [LangMem core concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) — Undated current docs Profiles/collections, episodes and procedural optimization. Owners: R1:C06.
- ✅ [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 2025-09-29 Compaction, structured notes, tool clearing and progressive retrieval. Owners: R1:C07.
- ✅ [LangMem deferred processing](https://langchain-ai.github.io/langmem/guides/delayed_processing/) — Undated current docs Per-thread debounce and local/remote execution caveat. Owners: R1:C08.
- ✅ [LangMem executor source](https://raw.githubusercontent.com/langchain-ai/langmem/main/src/langmem/reflection.py) — Current main snapshot; not a pinned release Local queue, task replacement and processing lifecycle. Owners: R1:C09.
- ✅ [Letta memory and dreaming](https://docs.letta.com/configuration/memory) — Undated current docs Git-backed memory, step/compaction triggers and proposed-edit review. Owners: R1:C10.
- ✅ [LightMem v4](https://arxiv.org/html/2510.18866v4) — 2025-10-21 first submission; v4 2026-02-28; ICLR 2026 Topic grouping, online insertion, offline update, LongMemEval-S table and evaluation scope. Owners: R1:C11.
- ✅ [metadata](https://arxiv.org/abs/2510.18866) — 2025-10-21 first submission; v4 2026-02-28; ICLR 2026 Topic grouping, online insertion, offline update, LongMemEval-S table and evaluation scope. Owners: R1:C11.
- ⚠️ [Honcho dreaming](https://honcho.dev/docs/v3/documentation/features/advanced/dreaming) — Undated v3 current documentation Experimental status, deduction/induction, scope and scheduling. Owners: R1:C12.
- ✅ [Letta memory-models direction](https://www.letta.com/blog/towards-agents-that-learn/) — 2026-06-25 Token-space portability vision and acknowledged reliability limitations. Owners: R1:C13.
- ✅ [Anthropic memory-tool specification](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) — Undated current docs; tool `memory_20250818` Client-side operations, storage ownership, expiry recommendation and compaction integration. Owners: R1:C14.
- ✅ [Anthropic Managed Agents engineering](https://www.anthropic.com/engineering/managed-agents) — 2026-04-08 Durable session log separated from harness, sandbox and context window. Owners: R1:C15.
- ✅ [Hermes memory/review documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/user-guide/features/memory.md) — Inspected local clean checkout `8a13834d`; reviewed paths last commit 2026-09-21 Background-review model route, disable switch, budget and applied-result feedback. Owners: R1:C16.
- ✅ [Hermes Curator documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/user-guide/features/curator.md) — Same checkout Skill-package scope, recoverable archival, opt-in LLM consolidation, snapshots and ledger. Owners: R1:C17.
- ✅ [Hermes provider lifecycle documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/developer-guide/memory-provider-plugin.md) — Same checkout Callback table, fail-closed/idempotent checkpoint and actual session-end call sites. Owners: R1:C18.
- ✅ [host source](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/run_agent.py) — Same checkout Callback table, fail-closed/idempotent checkpoint and actual session-end call sites. Owners: R1:C18.
- ⚠️ [Upstream HMK distiller PR](https://github.com/Mar-IA-no/hermes-memory-kit/pull/1) — Opened 2026-06-17; OPEN at head `e1e4c612181fc118cb2574444c8a279627722dc8` PR metadata and actual provider diff, not executed author tests. Owners: R1:C19.

## [R2] retrieval temporality

- ✅ [Mem0 paper](https://arxiv.org/html/2504.19413v1) — 2025-04-28, v1 Fact extraction and write decisions; author-reported LoCoMo protocol. Owners: R2:S1.
- ✅ [Zep paper](https://arxiv.org/html/2501.13956v1) — 2025-01-20, v1 Temporal graph, entity resolution and episode provenance. Owners: R2:S2.
- ✅ [A-MEM paper](https://arxiv.org/html/2502.12110v11) — First 2025-02-17; v11 2025-10-08 Contextual notes, linking and memory evolution; model-dependence limits. Owners: R2:S3.
- ✅ [MemOS paper](https://arxiv.org/html/2507.03724v4) — First 2025-07-04; v4 2025-12-03 Proposed memory lifecycle across text and model-oriented forms. Owners: R2:S4.
- ✅ [Mem0 history source](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/storage.py) — Commit c93420c, 2026-10-05 Native pre-image history schema. Owners: R2:S5, R5:Mem0 versioned extraction, correction and portability.
- ✅ [Mem0 write/history source](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/main.py) — Commit c93420c, 2026-10-05 Explicit update/delete/history paths. Owners: R2:S6, R5:Mem0 versioned extraction, correction and portability.
- ✅ [Graphiti edge model](https://github.com/getzep/graphiti/blob/aa5bb2706929fce502d99d8c7c4ddbb77bff4995/graphiti_core/edges.py) — Commit aa5bb27, 2026-10-06 Episode-backed nullable temporal fields. Owners: R2:S7.
- ✅ [Graphiti adding episodes](https://help.getzep.com/graphiti/core-concepts/adding-episodes) — Current v3 docs; page date not specified, code corroborates core fields Reference time and input types for episode ingestion. Owners: R2:S8.
- ✅ [A-MEM source](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py) — Commit ceffb86, 2025-12-12 Inspected evolution/update and collection-reset behavior. Owners: R2:S9.
- ✅ [MemOS textual metadata source](https://github.com/MemTensor/MemOS/blob/a7367d07e55db61099f7b4e2c1108bc5831a24f3/src/memos/memories/textual/item.py) — Commit a7367d0, 2026-09-22 Version/status and multi-source metadata schema. Owners: R2:S10.
- ✅ [MoM/P-Mem paper](https://arxiv.org/html/2609.25054v1) — 2026-09-07, v1 Experimental current-state/provenance design; authority limitations. Owners: R2:S11.
- ✅ [Engram paper](https://arxiv.org/html/2606.09900v1) — 2026-06-05, v1 Experimental facts/episode retrieval; ablation limits. Owners: R2:S12.
- ✅ [MemTrace paper](https://arxiv.org/html/2610.04838v1) — 2026-10-04, v1 Experimental immutable coding traces and applicability checks. Owners: R2:S13.

## [R3] experience relationships

- ✅ [Hindsight paper](https://arxiv.org/html/2512.12818v1) — arXiv v1, 2025-12-14 Abstract, taxonomy, narrative extraction and temporal/entity methods Owners: R3:R3-S1.
- ✅ [date record](https://arxiv.org/abs/2512.12818) — arXiv v1, 2025-12-14 Abstract, taxonomy, narrative extraction and temporal/entity methods Owners: R3:R3-S1.
- ✅ [Hindsight observations](https://hindsight.vectorize.io/developer/observations) — Official living docs, page date not provided Grounding, history and freshness sections Owners: R3:R3-S2.
- ✅ [Honcho overview](https://honcho.dev/docs/v3/documentation/introduction/overview) — Official v3 living docs, page date not provided Entity primitives and reasoning flow Owners: R3:R3-S3.
- ✅ [Multimodal embodied episodic KG](https://aclanthology.org/2025.dnd-16.10/) — Dialogue & Discourse 16, pp. 25–59; publisher date 2025-12-15 Abstract, section 3 attribution model and modality/viewpoint appendix Owners: R3:R3-S4.
- ✅ [paper](https://aclanthology.org/2025.dnd-16.10.pdf) — Dialogue & Discourse 16, pp. 25–59; publisher date 2025-12-15 Abstract, section 3 attribution model and modality/viewpoint appendix Owners: R3:R3-S4.
- ✅ [Hindsight retain](https://hindsight.vectorize.io/developer/retain) — Official living docs, page date not provided Occurrence versus learning time and context/entity example Owners: R3:R3-S5.
- ✅ [Hindsight extraction source](https://github.com/vectorize-io/hindsight/blob/9770fe400f8859ab5c8120f9e10ff65002d84ead/hindsight-api-slim/hindsight_api/engine/retain/fact_extraction.py) — File commit `9770fe4`, 2026-10-05 14:11:21 UTC Schemas, narrator prompt, concise selection, temporal handling/fallback and mention persistence Owners: R3:R3-S6.
- ✅ [Honcho peer representations](https://honcho.dev/docs/v3/documentation/core-concepts/representation) — Official v3 living docs, page date not provided Artifact types, explicit/inductive/abductive distinction Owners: R3:R3-S7.
- ✅ [Honcho directional representations](https://honcho.dev/docs/v3/documentation/features/advanced/directional-representations) — Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC Observer–subject scope, late join semantics; pinned file verified Owners: R3:R3-S8.
- ✅ [pinned docs](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/docs/v3/documentation/features/advanced/directional-representations.mdx) — Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC Observer–subject scope, late join semantics; pinned file verified Owners: R3:R3-S8.
- ✅ [Honcho evidence](https://honcho.dev/docs/v3/documentation/features/advanced/evidence) — Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC Read-versus-used, ID deduplication, omitted tool results and message text Owners: R3:R3-S9.
- ✅ [source](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/src/utils/evidence.py) — Official v3; inspected repository state `ae4a157`, 2026-10-06 21:11:09 UTC Read-versus-used, ID deduplication, omitted tool results and message text Owners: R3:R3-S9.
- ✅ [Human–Agent Co-Construction of Episodic Memories](https://journals.sagepub.com/doi/10.3233/FAIA250640) — Publisher first online 2025-09-25; HHAI 2025 Abstract, pilot methods/results and future interactive-study limit Owners: R3:R3-S10.
- ✅ [M3-Agent paper](https://arxiv.org/html/2508.09736v4) — v1 2025-08-13; inspected v4 2025-10-09 Memory node/modalities, identity equivalence, voting and video-QA evaluation Owners: R3:R3-S11.
- ✅ [version dates](https://arxiv.org/abs/2508.09736) — v1 2025-08-13; inspected v4 2025-10-09 Memory node/modalities, identity equivalence, voting and video-QA evaluation Owners: R3:R3-S11.
- ✅ [M³C paper](https://aclanthology.org/2025.acl-long.1519.pdf) — ACL 2025, July, pp. 31481–31512 Speaker-oriented memory linking, modality retrieval and top-one selection Owners: R3:R3-S12.
- ✅ [metadata](https://aclanthology.org/2025.acl-long.1519/) — ACL 2025, July, pp. 31481–31512 Speaker-oriented memory linking, modality retrieval and top-one selection Owners: R3:R3-S12.

## [R4] evaluation

- ✅ [E1](https://github.com/xiaowu0162/LongMemEval) — Accessed 2026-10-06; version/inspection in raw report. dataset/version and evaluation interfaces; accessed 2026-10-06. Owners: R4:E1.
- ✅ [E2](https://arxiv.org/html/2410.10813v2) — Accessed 2026-10-06; version/inspection in raw report. indexing, retrieval and reading methodology; accessed 2026-10-06. Owners: R4:E2.
- ✅ [E3](https://aclanthology.org/2024.acl-long.747/) — Accessed 2026-10-06; version/inspection in raw report. episode and multimodal benchmark scope; official code https://github.com/snap-research/locomo ; accessed 2026-10-06. Owners: R4:E3.
- ✅ [E3](https://github.com/snap-research/locomo) — Accessed 2026-10-06; version/inspection in raw report. episode and multimodal benchmark scope; official code https://github.com/snap-research/locomo ; accessed 2026-10-06. Owners: R4:E3.
- ✅ [E4](https://github.com/mohammadtavakoli78/BEAM) — Accessed 2026-10-06; version/inspection in raw report. scale/categories; paper https://arxiv.org/html/2510.27246v2 ; accessed 2026-10-06. Owners: R4:E4.
- ✅ [E4](https://arxiv.org/html/2510.27246v2) — Accessed 2026-10-06; version/inspection in raw report. scale/categories; paper https://arxiv.org/html/2510.27246v2 ; accessed 2026-10-06. Owners: R4:E4.
- ✅ [E5](https://aclanthology.org/2026.acl-long.1150/) — Accessed 2026-10-06; version/inspection in raw report. implicit cue/trigger consistency; code https://github.com/xjtuleeyf/Locomo-Plus ; accessed 2026-10-06. Owners: R4:E5.
- ✅ [E5](https://github.com/xjtuleeyf/Locomo-Plus) — Accessed 2026-10-06; version/inspection in raw report. implicit cue/trigger consistency; code https://github.com/xjtuleeyf/Locomo-Plus ; accessed 2026-10-06. Owners: R4:E5.
- ✅ [E6](https://arxiv.org/html/2507.05257v4) — Accessed 2026-10-06; version/inspection in raw report. incremental protocol and forgetting/learning objectives; accessed 2026-10-06. Owners: R4:E6.
- ✅ [E7](https://arxiv.org/html/2604.20006v1) — Accessed 2026-10-06; version/inspection in raw report. obsolete-memory penalty; publication record https://arxiv.org/abs/2604.20006 ; accessed 2026-10-06. Owners: R4:E7.
- ✅ [E7](https://arxiv.org/abs/2604.20006) — Accessed 2026-10-06; version/inspection in raw report. obsolete-memory penalty; publication record https://arxiv.org/abs/2604.20006 ; accessed 2026-10-06. Owners: R4:E7.
- ⚠️ [E8](https://arxiv.org/html/2605.12493v1) — Accessed 2026-10-06; version/inspection in raw report. work-in-progress environment-experience benchmark; publication record https://arxiv.org/abs/2605.12493 ; accessed 2026-10-06. Owners: R4:E8.
- ⚠️ [E8](https://arxiv.org/abs/2605.12493) — Accessed 2026-10-06; version/inspection in raw report. work-in-progress environment-experience benchmark; publication record https://arxiv.org/abs/2605.12493 ; accessed 2026-10-06. Owners: R4:E8.

## [R5] evolution options

- ✅ [repository at `9269b884`](https://github.com/vectorize-io/hindsight/tree/9269b88417ed263e5a8350f2e416ca2b322756b1) — Accessed 2026-10-06; version/inspection in raw report. Inspected LICENSE, README Quick Start/embedded/core concepts/production table and workspace manifest; recovery guide listed separately below. Owners: R5:Hindsight source.
- ✅ [repository at `ae4a1575`](https://github.com/plastic-labs/honcho/tree/ae4a157578691c985154e759b968b8a2181ad929) — Accessed 2026-10-06; version/inspection in raw report. Inspected LICENSE, README local-stack/peer-representation sections and `pyproject.toml` dependencies. Owners: R5:Honcho source.
- ✅ [repository at `aa5bb270`](https://github.com/getzep/graphiti/tree/aa5bb2706929fce502d99d8c7c4ddbb77bff4995) — Accessed 2026-10-06; version/inspection in raw report. Inspected LICENSE, README Graphiti versus Zep/deployment/backend sections and `pyproject.toml`. Kuzu is explicitly deprecated at this revision; it is not a sound new embedded-backend recommendation. Owners: R5:Graphiti source.
- ✅ [pinned guide](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-docs/docs/developer/admin-cli.md) — Accessed 2026-10-06; version/inspection in raw report. Same commit/date as above; inspected backup consistency/coverage, destructive restore and bank-migration rollback runbook. Roundtrip tests assert table coverage and restored IDs/text/timestamps/metadata/vectors; read, not executed.… Owners: R5:Hindsight Admin CLI and recovery test source.
- ✅ [Roundtrip tests](https://github.com/vectorize-io/hindsight/blob/9269b88417ed263e5a8350f2e416ca2b322756b1/hindsight-api-slim/tests/test_admin_backup_restore.py) — Accessed 2026-10-06; version/inspection in raw report. Same commit/date as above; inspected backup consistency/coverage, destructive restore and bank-migration rollback runbook. Roundtrip tests assert table coverage and restored IDs/text/timestamps/metadata/vectors; read, not executed.… Owners: R5:Hindsight Admin CLI and recovery test source.
- ✅ [pinned self-hosting guide](https://github.com/plastic-labs/honcho/blob/ae4a157578691c985154e759b968b8a2181ad929/docs/v3/contributing/self-hosting.mdx) — Accessed 2026-10-06; version/inspection in raw report. Same commit/date as above; inspected services, model requirement, deriver readiness, migrations and PostgreSQL backup/restore. README minimum Python 3.10 conflicts with package minimum 3.13; package manifest governs… Owners: R5:Honcho local environment.
- ✅ [repository at `c93420c4`](https://github.com/mem0ai/mem0/tree/c93420c49a6b14c3d446bdb156d96811908fd90a) — Accessed 2026-10-06; version/inspection in raw report. Inspected LICENSE, README library/self-hosted/Cloud distinction and manifest. README describes an April-2026 ADD-only algorithm; earlier update/delete research is not automatically this version's behavior. Owners: R5:Mem0 source.
- ✅ [README at `5bcdd177`](https://github.com/letta-ai/letta/blob/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a/README.md) — Accessed 2026-10-06; version/inspection in raw report. Inspected complete short README: active source is `letta-ai/letta-code`, historical V1 API server retired on `archive` branch. Owners: R5:Letta historical/current-source pointer.
- ✅ [repository at `48e3c11f`](https://github.com/langchain-ai/langmem/tree/48e3c11f5bb527282c7d5339c6a87a0b35abccfc) — Accessed 2026-10-06; version/inspection in raw report. Inspected LICENSE, complete README and manifest; functional core versus LangGraph tools and ephemeral versus persistent-store distinction. Owners: R5:LangMem source.
- ✅ [repository at `4b028fab`](https://github.com/letta-ai/letta-code/tree/4b028fab07c69edaac2ddb4f7b9a43573ff20d81) — Accessed 2026-10-06; version/inspection in raw report. Inspected README backend/MemFS/removed AgentFile sections, package manifest, local-store source, transcript schema/manifest and MemFS paths. Source exposes JSON/JSONL local records; neither this read nor git-tracked memory proves… Owners: R5:Current Letta Code source.
- ✅ [local store](https://github.com/letta-ai/letta-code/blob/4b028fab07c69edaac2ddb4f7b9a43573ff20d81/src/backend/local/local-store.ts) — Accessed 2026-10-06; version/inspection in raw report. Inspected README backend/MemFS/removed AgentFile sections, package manifest, local-store source, transcript schema/manifest and MemFS paths. Source exposes JSON/JSONL local records; neither this read nor git-tracked memory proves… Owners: R5:Current Letta Code source.
- ✅ [migration guide](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/docs/migration/oss-v2-to-v3.mdx) — Accessed 2026-10-06; version/inspection in raw report. Same pinned commit/date as above. Automatic `add` now emits ADD-only; explicit `update`/`delete`/`history` remain, reconciling current default and history APIs. Hosted schema exports may resolve conflicts and… Owners: R5:Mem0 versioned extraction, correction and portability.
- ✅ [Platform export cookbook](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/docs/cookbooks/essentials/exporting-memories.mdx) — Accessed 2026-10-06; version/inspection in raw report. Same pinned commit/date as above. Automatic `add` now emits ADD-only; explicit `update`/`delete`/`history` remain, reconciling current default and history APIs. Hosted schema exports may resolve conflicts and… Owners: R5:Mem0 versioned extraction, correction and portability.
- ✅ [source at `3d841eb`](https://github.com/nicoechaniz/hermes-memory-kit/tree/3d841eb97f5ab7c59d8420d3ad0652c1243da7de) — Accessed 2026-10-06; version/inspection in raw report. License/README inspected here; preservation/authority findings reused from the source-grounded review and disclosed synthetic diagnostics. Owners: R5:HMK baseline/license.
- ✅ [MIT LICENSE](https://github.com/nicoechaniz/hermes-memory-kit/blob/3d841eb97f5ab7c59d8420d3ad0652c1243da7de/LICENSE) — Accessed 2026-10-06; version/inspection in raw report. License/README inspected here; preservation/authority findings reused from the source-grounded review and disclosed synthetic diagnostics. Owners: R5:HMK baseline/license.

Ledger groups: 63 before cross-report URL deduplication.
Unique canonical URLs: 81. These counts describe the archive,
not independent experiments or verified competing-system deployments.
