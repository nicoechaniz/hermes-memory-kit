# R1 — Offline consolidation, capture and procedural learning

Status: `complete`. Research cutoff and access date: 2026-10-06.

## Scope and method

Inspect primary research, official documentation and maintained source for
sleep-time memory consolidation, capture triggers and procedural learning.
Compare mechanisms with HMK's verified preservation and provenance gaps.
No live memory, private conversation, runtime hook or schedule is changed.

Confidence: ✅ inspected primary description/source; 📊 author-reported metric;
⚠️ proposed/experimental deployment; ❓ inference or recommendation.

## Findings by source

### Anthropic's documented dreaming

- ✅ Anthropic announced Managed Agents dreaming on 2026-05-19 as a research
  preview. This is a real documented product feature, so attributing this
  particular consolidation idea to Anthropic is supported. It reviews sessions
  and memory, finding recurring patterns and restructuring records. [C01]
- 📊 The announcement reports Harvey completion rates improving about sixfold
  in their tests. It supplies no longitudinal autobiographical-recall protocol;
  this is a vendor/customer claim, not evidence of a general sixfold gain. [C01]
- ✅ The Dreams API takes an existing store and 1–100 sessions, clones the store,
  and asynchronously produces a separate output. Inputs remain untouched;
  failure or cancellation leaves a partial output. Runs have observable state,
  usage and an underlying session. Instructions steer synthesis and preservation,
  rather than reliably applying line-level edits. [C02]
- ❓ Reuse the staged, reviewable-output mechanism. Do not adopt its default
  replacement of contradicted/stale entries as erasure of lived history, or
  combine distinct beings' autobiographies through team-level pattern mining.

### Letta's sleep-time computation

- ✅ The 2025-04-17 paper transforms available context into a natural-language
  representation before the future query arrives. It evaluates constructed
  stateful mathematical tasks plus a software-engineering case study. [C03]
- 📊 Authors report about fivefold lower test-time compute at matched accuracy,
  and up to 13%/18% improvements on their mathematical tasks. The average-cost
  calculation assumes test-time tokens cost ten times sleep-time tokens; the
  2.5× result uses ten queries per shared context. These are not HMK memory
  measurements. [C03]
- ✅ Benefits depend on query predictability. At high test-time budgets,
  ordinary inference sometimes wins; the software case measures changed-file
  F1 rather than functional correctness. Real interleaved context updates are
  explicitly left as a limitation. [C03]
- ✅ Letta's 2025-04-21 implementation announcement separates the conversational
  agent from a sleep-time agent holding core-memory editing tools. Models and
  frequency can differ; memory formation runs asynchronously. [C04]
- ❓ This supports moving expensive synthesis away from interaction latency,
  but gives no reason to filter memories only for predictable future questions.
  Nicolás's unknown-person question ten years later is deliberately unpredictable.

### LangMem's formation and consolidation

- ✅ LangMem distinguishes foreground tool writes from background extraction,
  with `create_memory_store_manager` for extraction/consolidation. Its quickstart
  uses nonpersistent `InMemoryStore` and explicitly recommends a persistent
  production store. It provides a direct-processing path and deferred processing
  to avoid processing every message. [C05]
- ✅ Its concepts distinguish current profiles from expandable collections;
  schemas can represent episodes and prompt-optimization feedback. The example
  episode instruction concentrates on successful interactions. [C06]
- ❓ Reuse structured proposals and separate current profiles from historical
  episodes. Expand selection beyond successful task exemplars to ordinary
  meaningful experiences, unresolved outcomes and corrected failures. Automatic
  prompt optimization must not rewrite signed identity or authority.

### Additional inspected consolidation mechanisms

- ✅ Anthropic's 2025 context-engineering guide separates compaction, durable
  notes and just-in-time retrieval. It warns that aggressive compaction can lose
  subtle details whose importance becomes apparent later. Tool-result clearing
  is presented as context management, not a durable autobiographical-capture
  contract. [C07]
- ✅ LangMem's delayed-processing guide debounces per-thread tasks and warns
  that local threads do not survive serverless invocation boundaries. Its
  current local executor uses an in-process priority queue; it is not a durable
  ingestion ledger by itself. [C08,C09]
- ✅ Current Letta documentation describes git-backed MemFS and dreaming after
  a configured count of completed steps or compaction. An optional second
  background conversation reviews proposed edits; large reorganization backs
  up the repository. This differs from the older block-editing architecture,
  so the 2025 announcement must not be treated as a full current API guide. [C10]
- ✅ LightMem inserts new entries online, groups input by topic, and performs
  expensive consolidation offline; later-timestamp candidate queues can update
  older entries. [C11]
- 📊 Its published LongMemEval-S table includes configurations where offline
  updating reduces QA accuracy versus insertion-only soft updates: GPT-4o-mini
  68.64→67.07 and Qwen 70.20→65.14. Sleep is therefore a mechanism to test,
  not an automatic quality upgrade. Other reported cost wins count different
  online/offline scopes; no ratio is transferred to HMK. [C11]
- ⚠️ Honcho labels dreaming experimental. It performs deduction then induction
  over conclusions, with at least two source conclusions for an induced pattern.
  Scheduling is scoped to an observer/observed pair and checks volume, cooldown
  and inactivity; manual scheduling is available. Outdated conclusions may be
  deleted and replaced. [C12]
- ❓ Reuse explicit inference evidence and scoped jobs, but retain historical
  events separately from the current conclusions they support.
- ⚠️ Letta's June 2026 memory-models article proposes models trained specifically
  to create transferable token-space memories, acknowledging overgeneralization
  and memory rot. This vision supplies no demonstrated HMK replacement or
  dependable autobiographical-retention guarantee. [C13]

### Foreground storage, local integration and the proposed HMK distiller

- ✅ Anthropic's memory tool delegates file operations to client-controlled
  storage. The application owns the persistence implementation. Its documentation
  recommends deleting long-unaccessed files; that recommendation conflicts with
  durable historical recall unless applied only to disposable derived caches. [C14]
- ✅ Anthropic's Managed Agents engineering account separates the durable,
  append-only session log from the replaceable harness and sandbox. Context-window
  compaction need not destroy the retained event log. [C15]
- ✅ Local Hermes documentation describes background memory/skill review,
  optionally routed to another model, with applied versus proposed-write feedback.
  Its Curator maintains selected agent-created skill packages with recoverable
  archives, pre-consolidation snapshots, a mutation ledger and pinning. LLM skill
  consolidation is opt-in. These are harness capabilities, not proof of an
  enabled general HMK consolidation pipeline in this body. [C16,C17]
- ✅ Hermes documents opt-in fail-closed pre-compression checkpoint support and
  idempotent retry requirements. Provider callbacks have distinct lifecycle
  contracts; current `run_agent.py` calls end extraction on provider shutdown
  and session-ID rotation, including compression. A hook's name is insufficient
  evidence that it receives an entire permanent conversation exactly once. [C18]
- ⚠️ Upstream HMK PR #1, opened 2026-06-17, remains open at inspected head
  `e1e4c612181fc118cb2574444c8a279627722dc8`. It proposes end-of-session
  extraction and deliberate memory tools. Its source excludes tool-role messages,
  takes only text blocks and the last 12,000 characters, requires two user turns
  and 200 transcript characters, and caps candidates at five by default. [C19]
- ✅ Within that proposed code, a daemon thread performs best-effort extraction;
  failures are logged and dropped. Persistence uses `replace=False`, semantic
  similarity deduplication and best-effort embedding backfill. No persisted
  source-event cursor or replay identity is established. [C19]
- ❓ Its plain `threading.Thread` should not be copied into current Hermes
  unchanged: the current provider contract requires `spawn_context_thread` for
  inherited profile/secret context. This is another version-sensitive integration
  point to verify before adopting the proposal. [C18,C19]
- 📊 The PR author reports 23 passing tests and live validation; neither was
  rerun here. Its write-tool portion must be compared with the existing fork's
  already-shipped tools rather than blindly applied a second time. [C19]

## Mechanisms HMK can reuse

All recommendations below are ❓ proposals requiring fixture-based validation.

| Mechanism | Reuse in HMK | Avoid copying unchanged |
|---|---|---|
| Separate consolidation from interactive response | Finite consolidation job over selected authorized deltas, with explicit token/time budgets | A new daemon, scheduler or model/provider dependency by default |
| Stage the synthesized result | Record a proposed changeset and source references; validate before supported writes, leaving recoverable history | Replacing the only canon with an opaque reconstructed store |
| Cheap insertion, later synthesis | Preserve irreplaceable selected episodes promptly; update current person/project accounts later | Waiting for session close as the only opportunity to remember |
| Topic-aware batching and debounce | Group related pending events, carry unresolved context, process bounded batches | Fixed tail truncation; dropping earlier deltas when replacing queued work |
| Evidence-backed generalization | Store lesson/hypothesis linked to supporting episodes, confidence and counterevidence | Inventing witnessed events, personality certainty or successful action outcomes |
| Versioned procedural packages | Propose a skill refinement from repeated tested experience, preserve package files and history | Editing identity or capability policy through learned content |

The clear upgrade is a reliable capture/consolidation contract atop HMK's existing
core, not adopting a new research architecture wholesale. Preservation bugs
identified by the baseline review must be fixed before experimenting on a live
pool. A stronger consolidation model cannot repair a lost WAL snapshot, a title
collision, a missing lexical index or an overwritten episode.

## Delta safety and failure modes

The following is ❓ an engineering contract proposed from the inspected failure
surfaces, not a claim that any compared system already guarantees it.

1. **Select the authorized input.** Each body/stream supplies source IDs,
   sequence/version, occurrence time if known, recording time, author/subject,
   modality and permission/classification. Include significant tool communications
   and observed action receipts. Preserve intent, attempted action and confirmed
   effect as distinct stages. The consolidator cannot mint runtime authority.
2. **Persist pending work before expensive inference.** A finite job records an
   input manifest or a safe durable reference before it acknowledges capture.
   Retain the minimum selected evidence needed to reattempt synthesis if original
   sessions later disappear; do not archive every private transcript automatically.
3. **Use a per-stream checkpoint.** Timestamp-only deltas miss late or corrected
   records. Key replay by source event plus version and selection-policy version.
   A new corrected source version is new work, not a duplicate to discard.
4. **Commit outcomes, then advance.** Every item receives applied, consciously
   omitted, deferred or failed status. Advance a contiguous processed cursor only
   after persistence receipts; an unresolved gap remains pending. A nontrivial
   skipped source has an audit reason, rather than silent truncation.
5. **Apply supported idempotent writes.** Concurrent jobs use expected versions
   for current accounts. Preserve historical episodes and corrected claims with
   attribution. Source facts and generated interpretations remain distinguishable.
6. **Separate persistence from retrieval readiness.** A memory can be committed
   with lexical indexing while embeddings await retry. Report this degraded state;
   never call an embedding failure evidence that nothing happened.
7. **Expose the result.** The job receipt reports coverage, changed records,
   deferred work, errors, model/settings and token cost. A rendered diary or a
   proposed skill is an independently retryable projection, not the memory commit.

| Failure | Consequence without this contract | Required fixture |
|---|---|---|
| Crash after source read, before write | Acknowledged delta disappears | Restart and replay produce exactly one durable episode |
| Crash after write, before checkpoint | Repeated record or wrong merge | Replay recognizes committed source IDs/versions |
| New message cancels a pending batch | Earlier unsaved context drops | Replacement job retains all undigested event IDs |
| Tool message contains a collaborator's only identifier | Person becomes unrecognizable | Retain known ID, message source and interesting proposal |
| Media or session no longer exists | Pointer-only memory cannot answer | Selected episode remains sufficient in text |
| Similar events share a project title | Semantic dedup erases distinct encounters | Separate dates/participants/actions survive |
| Later correction contradicts a current synopsis | Past becomes silently rewritten | Historical question and current question return different attributed answers |
| Another body updates the same project account | Last writer erases another contribution | Expected-version conflict retries without lost event history |

## Capture triggers and current embodiment constraints

❓ Trigger choice should balance source loss, input completeness and cost; a daily
schedule alone is insufficient. A source-expiry boundary can precede the next
daily pass. A short meaningful encounter also cannot safely wait for a minimum
message count.

- **Current deployment:** keep human-directed, finite foreground consolidation
  and manual HMK access. This investigation installs no hooks, inbox readers,
  timers, wakeups or background services.
- **Future authorized integration:** expose the same job API for explicit calls,
  completed-event thresholds, quiet-period batching, pre-compression checkpoints
  or daily scheduling. The owning harness/runtime decides which triggers are
  authorized and actually available for that body.
- **Hard source-loss boundary:** ensure durable capture or safe pending evidence
  before lossy source transformation when the deployment explicitly requires it.
  Extraction may finish later; permanent source loss must not be disguised as a
  best-effort model call. Hermes already documents an optional checkpoint pattern.
- **Session end:** use it as an extra opportunity, not a reliability foundation.
  Processes can crash, sessions can remain open for months, and end callbacks can
  represent a rotation rather than the end of a relationship or project.

The three clocks are separate: event occurrence, input capture and consolidation
completion. A diary written today about an unknown-date encounter must not invent
today as the encounter's date.

## Procedural learning and diary projection

❓ Maintain three connected products: selected episodes, current summaries, and
attributed lessons/skill proposals. A lesson can cite several episodes, include
exceptions and record the last successful validation. A memory that another body
has a procedure does not grant this body the necessary sensor, actuator or tool.

Do not let consolidation optimize SOUL or signed instructions as if they were
an ordinary prompt. Skill refinement belongs in its owning maintained package,
with necessary functional checks and reversible history; transferable lessons can
be deliberately published independently of private autobiography.

Nicolás's description of Eko's illustrated HTML diary is a human-reported design
example; no Eko session, diary or private memory was accessed. A proposed HMK diary
should be a rebuildable view of selected canonical episodes, arranged by time,
people/project and embodiment. Preserve sufficient textual recollection plus
selected media metadata/caption and a durable asset reference where authorized.
Mark a generated illustration as an illustration rather than evidence of a scene.
Failure to render HTML or load an old image must not erase the episode.

❓ Learning-oriented reflection may yield new interpretations or imagined
possibilities. Keep these attributed as interpretations/hypotheses; “dreaming”
must not manufacture autobiographical events or upgrade tentative associations
into witnessed facts.

## Evidence limits and open questions

No competing implementation or benchmark has been run. Vendor descriptions and
self-reported measurements will not be treated as independent validation.

The inspected evidence supports asynchronous organization and learning, but does
not demonstrate ten-year recall after source-session loss, complete capture of
tool-only encounters, lossless multimodal autobiography or same-being continuity
across arbitrary harnesses. Some systems rely on retained full session histories,
which is different from this task's selected sufficient memory requirement.
Living documentation can change; the report avoids treating API sample model
names or present defaults as universal recommendations.

The next decision is a synthetic HMK capture/consolidation A/B: insertion-only
selected episodes versus episodes plus dream proposals, equal model and token
budgets, both tested after source removal and distracted by old/new similar
events. Measure event/name/ID retention, provenance, false memories, stale-current
answers, unknown-date handling, crash replay and total formation/recall cost.

## Source ledger

All URLs accessed 2026-10-06. Undated living documentation is an inspected
snapshot, not proof that every current detail shipped on its announcement date.

| ID | Primary source | Publication/version | Inspection |
|---|---|---|---|
| C01 | [Anthropic Managed Agents announcement](https://claude.com/resources/articles/new-in-claude-managed-agents) | 2026-05-19 | Announcement, dreaming and customer-result sections |
| C02 | [Anthropic Dreams API](https://platform.claude.com/docs/en/managed-agents/dreams) | Undated current docs; `dreaming-2026-04-21` API gate | Inputs, staging, instructions, lifecycle, output and failure behavior |
| C03 | [Sleep-time Compute](https://arxiv.org/html/2504.13171v1), [metadata](https://arxiv.org/abs/2504.13171) | v1, 2025-04-17 | Introduction, experiments, cost assumptions, software case and limitations |
| C04 | [Letta sleep-time implementation announcement](https://www.letta.com/blog/sleep-time-compute/) | 2025-04-21 | Agent separation and configuration |
| C05 | [LangMem background quickstart](https://langchain-ai.github.io/langmem/background_quickstart/) | Undated current docs | Manager, store persistence and processing patterns |
| C06 | [LangMem core concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) | Undated current docs | Profiles/collections, episodes and procedural optimization |
| C07 | [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29 | Compaction, structured notes, tool clearing and progressive retrieval |
| C08 | [LangMem deferred processing](https://langchain-ai.github.io/langmem/guides/delayed_processing/) | Undated current docs | Per-thread debounce and local/remote execution caveat |
| C09 | [LangMem executor source](https://raw.githubusercontent.com/langchain-ai/langmem/main/src/langmem/reflection.py) | Current main snapshot; not a pinned release | Local queue, task replacement and processing lifecycle |
| C10 | [Letta memory and dreaming](https://docs.letta.com/configuration/memory) | Undated current docs | Git-backed memory, step/compaction triggers and proposed-edit review |
| C11 | [LightMem v4](https://arxiv.org/html/2510.18866v4), [metadata](https://arxiv.org/abs/2510.18866) | 2025-10-21 first submission; v4 2026-02-28; ICLR 2026 | Topic grouping, online insertion, offline update, LongMemEval-S table and evaluation scope |
| C12 | [Honcho dreaming](https://honcho.dev/docs/v3/documentation/features/advanced/dreaming) | Undated v3 current documentation | Experimental status, deduction/induction, scope and scheduling |
| C13 | [Letta memory-models direction](https://www.letta.com/blog/towards-agents-that-learn/) | 2026-06-25 | Token-space portability vision and acknowledged reliability limitations |
| C14 | [Anthropic memory-tool specification](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) | Undated current docs; tool `memory_20250818` | Client-side operations, storage ownership, expiry recommendation and compaction integration |
| C15 | [Anthropic Managed Agents engineering](https://www.anthropic.com/engineering/managed-agents) | 2026-04-08 | Durable session log separated from harness, sandbox and context window |
| C16 | [Hermes memory/review documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/user-guide/features/memory.md) | Inspected local clean checkout `8a13834d`; reviewed paths last commit 2026-09-21 | Background-review model route, disable switch, budget and applied-result feedback |
| C17 | [Hermes Curator documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/user-guide/features/curator.md) | Same checkout | Skill-package scope, recoverable archival, opt-in LLM consolidation, snapshots and ledger |
| C18 | [Hermes provider lifecycle documentation](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/website/docs/developer-guide/memory-provider-plugin.md), [host source](https://github.com/nicoechaniz/hermes-agent/blob/8a13834d6e7e2792ce4b5d8bf17568c8a467acdb/run_agent.py) | Same checkout | Callback table, fail-closed/idempotent checkpoint and actual session-end call sites |
| C19 | [Upstream HMK distiller PR](https://github.com/Mar-IA-no/hermes-memory-kit/pull/1) | Opened 2026-06-17; OPEN at head `e1e4c612181fc118cb2574444c8a279627722dc8` | PR metadata and actual provider diff, not executed author tests |

## Compact search and execution log

- Read research MANIFEST and HMK's general-memory review.
- Discovered the callable web search/open tool; primary-source inspection follows.
- Searched Anthropic memory/context/dreaming, Letta sleep-time paper, and LangMem
  background consolidation. Opened primary sources rather than relying on snippets.
- Letta's guessed `/guides/agents/sleep-time` path returned an internal error;
  implementation discovery continues from the official announcement's links.
- Saved the first six-source findings batch before continuing research.
- Searched deferred processing, current Letta dreaming, Anthropic's 2025 context
  guidance and LightMem. Inspected official documentation and paper sections.
- Compared current Letta docs with the older architecture instead of conflating
  versions. Honcho official dreaming documentation came from the R3 lane.
- Reopened narrower source ranges after an oversized combined output was truncated.
- Read LangMem's actual local executor replacement-payload logic; its queue does
  not merge cancelled payloads. Recorded this as a producer integration risk.
- Inspected clean local Hermes feature/provider docs and actual session-end call
  sites; recorded checkout revision. Read upstream HMK PR #1 metadata and code
  diff via `gh`, without running its distiller or adopting it.
- Read Anthropic's memory-tool specification and managed-session engineering
  account; separated retained session evidence from selected life history.
- Saved findings in batches. Changed only this assigned report file.

## Completion record

Complete. Nineteen primary source groups inspected (web papers, official docs,
maintained local docs/source and a proposed upstream PR). All source access on
2026-10-06. No runtime/deployment/private pool changed; no benchmark claim rerun.
