# R2 — Retrieval, temporal organization and history-safe updates

State: `complete`. Research cutoff and access date: 2026-10-06.

## Question

Which demonstrated mechanisms in Mem0, Zep/Graphiti, A-MEM and MemOS can improve
HMK's weak-cue retrieval, entity recognition, chronology and corrections while
preserving a being's meaningful autobiography and evidence?

## Method and confidence

Read primary papers, official documentation and maintained source. Search
snippets are discovery only. No competing system is installed or benchmark run.
✅ denotes an inspected primary description; 📊 an author/vendor measurement;
⚠️ a proposal or experimental mechanism; ❓ our inference or recommendation.

## Search log

1. Searched `Mem0 Building Production-Ready AI Agents Scalable Long-Term Memory
   2025 arxiv`, `Zep temporal knowledge graph architecture agent memory 2025
   Graphiti paper`, `A-MEM Agentic Memory LLM Agents 2025 arxiv`, and `MemOS memory
   operating system LLM 2025 arxiv` together. Opened all four arXiv records to
   verify submission/revision dates, then their versioned HTML papers.
2. Searched within papers for bi-temporal timestamps, invalidation, memory
   evolution and MemCube. Opened relevant methods sections and later pinned
   source to distinguish conceptual capabilities from implementation evidence.
3. Searched official memory-history, Graphiti episode and MemOS version/provenance
   documentation. Opened the current Mem0 REST and Graphiti ingestion pages.
   Queried public GitHub commit APIs with an explicit cutoff, then inspected
   pinned source files for Mem0 history, Graphiti edge dates, A-MEM mutations and
   MemOS metadata. Current documentation is undated; pinned code establishes
   pre-cutoff implementation evidence independently of page-update dates.
4. Discovery also found three recent primary preprints: Engram (2026-06-05),
   MoM/P-Mem (2026-09-07) and MemTrace (2026-10-04). Opened arXiv records and
   versioned HTML to verify dates; these are experimental evidence, not shipped
   guarantees. Read methods and limitations. MemTrace only informs
   repository-state/evidence boundaries.
5. Revisited Zep methods for entity resolution, incoming/outgoing source links,
   retrieval channels and benchmark caveats. Read MoM's explicit source-authority
   limitation and Engram's distinction between an observed hybrid-detail benefit
   and a controlled ablation not yet performed. No source after the cutoff was
   included. Web reference IDs were not used in this artifact; canonical source
   URLs and pinned GitHub commits avoid ambiguity from concurrent browsing.

## Findings

### Initial paper findings

- ✅ Mem0 separates extraction of salient facts from an update decision against
  similar existing memories. Its base paper specifies ADD, UPDATE, DELETE and
  NOOP; its graph variant instead invalidates obsolete relationships. This is
  a useful distinction: keeping a coherent current profile does not itself
  establish preserved life history. [S1]
- ✅ Zep separates the time an event/fact applies from ingestion/audit time and
  retains links from extracted entities/facts back to originating episodes.
  It resolves entities with both semantic and full-text candidates. [S2]
- ✅ A-MEM makes note context, keywords, tags and links evolve when new memories
  arrive. These are retrieval interpretations; evolution should not silently
  rewrite source evidence. Its limitations acknowledge dependence on the
  underlying model's organization decisions. [S3]
- ⚠️ MemOS proposes unified memory lifecycle and governance across plaintext,
  activation and parametric forms. Its abstraction is broader than HMK's
  text-memory scope; the paper alone does not establish that such an operating
  system is required for autobiographic continuity. [S4]

### Pinned implementation evidence

- ✅ Mem0 OSS actually has a separate SQLite history table with old/new content,
  operation, actor and role; update/delete paths record pre-images after changing
  the vector store, and an explicit history API exists. Therefore the base
  paper's DELETE operation must not be summarized as proof that today's
  implementation erases every copy of history. Normal semantic retrieval and a
  per-ID audit history are nevertheless different access paths. ❓ HMK can add
  queryable native revisions locally without adopting Mem0's infrastructure;
  failure atomicity across its multiple stores still requires testing. [S5,S6]
- ✅ Graphiti's pinned `EntityEdge` keeps originating episode IDs, nullable
  validity interval, expiry time and episode reference time separately. ❓ Adopt
  these date distinctions; a generated validity interval still needs uncertainty
  and source-mode annotation to avoid turning a report into established fact.
  The current ingestion documentation requires a reference time and supports
  text, conversational messages and structured JSON. [S7,S8]
- ✅ A-MEM source contains an `evolution_history` field, but the inspected normal
  `update` path sets attributes in place and replaces the index document without
  appending an old-value snapshot. The constructor also resets its Chroma
  collection. ⚠️ A field labelled history is not evidence of a reliable
  history/recovery protocol, and this research implementation should not replace
  a live autobiography merely for its linking algorithm. [S9]
- ✅ MemOS's textual metadata schema distinguishes activated/resolving/archived/
  deleted records, increments versions by contract, retains compact archived
  histories plus an optional full archived-node pointer, and permits multiple
  source-message locators/snippets including tool roles. ⚠️ These are explicit
  schema capabilities, not our demonstration that every write/restore path
  maintains them. ❓ Borrow the source envelope and state/event distinction;
  validate writer/retriever behavior before relying on the schema. [S10]

### Recent research: current state, historical evidence and correction

- ✅ MoM/P-Mem proposes a compact current view while retaining displaced values
  and typed support/supersession/alternative/revocation relations. It explicitly
  distinguishes changing a once-correct value from rejecting an erroneous one,
  and keeps unresolved conflicts visible. ⚠️ It is a 2026-09 preprint; most
  evaluated updates are short sentences, conflict resolution is tested mainly
  in a controlled probe, and its annotator does not weigh source authority.
  An untrusted observation can supersede trusted knowledge. 📊 Its reported
  stale-answer improvement on knowledge updates is 19.4% → 10.9%; that is not
  a production or longitudinal-continuity result. ❓ Reuse explicit status and
  predecessor semantics, with authority-aware routing, rather than its entire
  proposed graph. Its classification of Mem0 as erasing history is too broad
  for the current source inspected above. [S11]
- ✅ Engram separates a lossless episode write from later atomic-fact
  consolidation, retains superseded facts and source links, and describes
  hybrid lexical/dense/graph retrieval plus point-in-time filtering. 📊 Its
  paper reports 83.6% against 73.2% full-context on 500 LongMemEval-S questions
  with one answerer and the category-specific official judge. ⚠️ The benefit
  of facts plus raw chunks over facts alone is a development observation;
  a controlled full-set component ablation and repeated runs are future work.
  ❓ The mechanism reinforces retaining sufficient episode detail alongside
  compact current facts, but its reliance on raw histories differs from our
  requirement that original sessions may disappear. Decay may affect rank;
  it must not automatically erase selected life history. This Engram is a
  separate project from HMK's existing ENGRAM buckets. [S12]
- ✅ MemTrace seals immutable coding execution traces with repository state,
  files/symbols/tests and provenance; later corrections make new traces.
  Restoration checks current applicability before reusing evidence.
  ⚠️ This 2026-10-04 preprint concerns coding trajectories, not a being's life
  history, and competitors were not rerun here. ❓ Carry compact authored
  contribution/project memories in HMK, while detailed task traces and fresh
  test validity remain with the repository/harness. A remembered passing test
  is historical evidence and cannot assert that changed code passes now. [S13]

### What the performance evidence establishes

- 📊 Mem0 reports roughly 2% higher overall judge performance for its graph
  variant over its base on its LoCoMo protocol; that small increment does not
  establish that HMK requires a graph backend. Its paper excludes LoCoMo's
  adversarial/unanswerable category. [S1]
- 📊 Zep evaluates DMR and LongMemEval using a particular hosted implementation
  and model configuration; its paper notes that DMR's 60-message histories fit
  ordinary full context and mostly test single-fact retrieval. Several richer
  episode-provenance traversals are described but not exercised by those
  experiments. [S2]
- 📊 A-MEM's ablations report benefits from links and memory evolution on
  conversational QA. ⚠️ The paper acknowledges model-dependent organization;
  neither clustering visualizations nor QA scores demonstrate ten-year memory
  preservation, multi-body receiving or reliable update recovery. [S3]
- ❓ These results support experiments on concrete mechanisms, with the same
  corpus, answerer, context budget and judge. They do not give a comparable
  ranking among all candidates or an empirical reason to replace HMK today.

## HMK implications and limitations

The [published general-memory review](../../../docs/general-memory-review.md)
supplies source-confirmed HMK gaps and disposable diagnostic observations.
All proposals below are ❓ recommendations requiring implementation and tests.

| HMK gap | Reusable mechanism | Smallest practical HMK experiment |
|---|---|---|
| Updating a synopsis removes its former content | Mem0 pre-image history; MoM explicit current/predecessor/status; MemOS archived versions | Native revision records with stable logical IDs and atomic old/new persistence; retrieve current account by default, historical version/episode on request. Keep protected-source history in its own authority. |
| Event dates become storage dates | Graphiti nullable validity/reference/transaction dates | Distinguish occurred/reported/recorded times and precision; unknown occurrence remains null. Add event-range/as-of filtering independently of recency rank. |
| Long natural questions lose late identifiers and Unicode names | Hybrid name/fact retrieval and entity-anchored expansion | Unicode-aware full-question lexical cues plus dense candidates; explicit source IDs and evidenced aliases; bounded incoming/outgoing person/project/episode links. |
| Same-project events collapse as duplicates | Zep entity-pair scoped matching; source-linked atomic notes | Duplicate by source-event identity/version and redundant meaning; do not treat shared title prefix or semantic proximity as the same episode/person. |
| Compact recall drops origin | Graphiti episode provenance; MemOS source envelope | Preserve source, body, mode of knowing and status in all search/pack/preview paths; expand selected evidence while maintaining attribution. |
| Hybrid fails during embedding outage; quotas return weak evidence | Multi-channel candidate retrieval and evidence gate | Return explicit degraded lexical results and backend status; calibrate relevance before quotas/fusion. A result set must distinguish no evidence from unavailable search. |
| Project capsule can claim stale current details | MemTrace applicability check; current/historical separation | Store authored functions, repo and observed state date, then route concrete current questions to the repository. Preserve former contribution/outcome as history. |

**Example acceptance target.** A fictional contributor named `Nicolás Echániz`
with known GitHub identifier comments on HarborMesh issue 42, proposes replay,
and later clarifies the proposal. From another authorized body, ten simulated
years and many unrelated memories later, the question “Who was that person who
proposed something interesting in the HarborMesh issue?” should recover the
person/identifier, proposal, why it mattered, clarification and observed outcome.
It must preserve that these were issue comments, distinguish the original
proposal from the correction and avoid merging another same-name contributor.
The original full session and external issue should be absent during evaluation.

**Update semantics need more than latest-wins.** A later report can describe an
earlier event, disagree with another source or retract an erroneous inference.
Preserve alternatives when evidence is unresolved. Distinguish `supersedes`
(was correct, changed) from `corrects` (was mistaken), `supports` and `retracts`.
Date ordering alone does not decide authority or identity. An inferred alias,
entity match or relationship remains an attributed hypothesis until supported.

**Storage decision.** SQLite chapters, FTS, metadata, revision rows and indexed
links can express these mechanisms. A separate graph service is worth trialling
only if measured entity/temporal/multi-hop retrieval remains poor after those
fixes or its bounded traversal/maintenance costs become untenable. The trial
must preserve canonical records and compare memory quality at the same budget.
Embedding/index replacement can be independent of durable-memory replacement.
Native writer history, source attribution and recovery are necessary regardless
of the selected backend; replacing a backend does not solve capture omissions.

## Limits of this lane

✅ Primary sources and selected source methods were inspected, not every
competitor file. 📊 Reported measurements were not rerun. ⚠️ Undated live docs
can change; pinned pre-cutoff commits carry implementation claims. ❓ None of
these sources independently verifies our required ten-year cross-body scenario,
private pool boundaries, embodied experiences or receiving acceptance. The
research does not authorize data migration, raw session retention, schedulers,
automatic deletion or changes to deployed bodies. No live pool was read or
modified. Ordinary meaningful episodes require enough retained detail to answer
later without an external history pointer; an extracted fact alone may be too
lossy even if its source ID survives.

## Source ledger

| ID | Primary source | Publication/version inspected | Access |
|---|---|---|---|
| S1 | [Mem0 paper](https://arxiv.org/html/2504.19413v1) | 2025-04-28, v1 | 2026-10-06 |
| S2 | [Zep paper](https://arxiv.org/html/2501.13956v1) | 2025-01-20, v1 | 2026-10-06 |
| S3 | [A-MEM paper](https://arxiv.org/html/2502.12110v11) | First 2025-02-17; v11 2025-10-08 | 2026-10-06 |
| S4 | [MemOS paper](https://arxiv.org/html/2507.03724v4) | First 2025-07-04; v4 2025-12-03 | 2026-10-06 |
| S5 | [Mem0 history source](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/storage.py) | Commit c93420c, 2026-10-05 | 2026-10-06 |
| S6 | [Mem0 write/history source](https://github.com/mem0ai/mem0/blob/c93420c49a6b14c3d446bdb156d96811908fd90a/mem0/memory/main.py) | Commit c93420c, 2026-10-05 | 2026-10-06 |
| S7 | [Graphiti edge model](https://github.com/getzep/graphiti/blob/aa5bb2706929fce502d99d8c7c4ddbb77bff4995/graphiti_core/edges.py) | Commit aa5bb27, 2026-10-06 | 2026-10-06 |
| S8 | [Graphiti adding episodes](https://help.getzep.com/graphiti/core-concepts/adding-episodes) | Current v3 docs; page date not specified, code corroborates core fields | 2026-10-06 |
| S9 | [A-MEM source](https://github.com/agiresearch/A-mem/blob/ceffb860f0712bbae97b184d440df62bc910ca8d/agentic_memory/memory_system.py) | Commit ceffb86, 2025-12-12 | 2026-10-06 |
| S10 | [MemOS textual metadata source](https://github.com/MemTensor/MemOS/blob/a7367d07e55db61099f7b4e2c1108bc5831a24f3/src/memos/memories/textual/item.py) | Commit a7367d0, 2026-09-22 | 2026-10-06 |
| S11 | [MoM/P-Mem paper](https://arxiv.org/html/2609.25054v1) | 2026-09-07, v1 | 2026-10-06 |
| S12 | [Engram paper](https://arxiv.org/html/2606.09900v1) | 2026-06-05, v1 | 2026-10-06 |
| S13 | [MemTrace paper](https://arxiv.org/html/2610.04838v1) | 2026-10-04, v1 | 2026-10-06 |

Source count: 13 sources used in this report (7 papers, 5 pinned source files,
1 official documentation page). Additional discovery pages/abstract records,
Mem0 REST docs and Graphiti quick-start were opened for orientation but are not
counted as independent supporting evidence. Final raw report is immutable;
corrections or synthesis should be additive and attributed in later artifacts.
