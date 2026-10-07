# Codex native memory and being-level continuity

Reviewed on 2026-10-07 against installed Codex CLI `0.160.0`. Source pin:
[`rust-v0.160.0`](https://github.com/openai/codex/tree/rust-v0.160.0), commit
`a956835d020762cb2b570053af06f643a11c0ecc`. This supplements the closed
[2026-10-06 investigation](../research/agent-memory-2026-10-06/README.md);
it does not change its frozen raw reports or claim a model comparison.

## Codex implements both session continuity and cross-session memory

| Surface | Purpose | Implementation and limit |
|---|---|---|
| Native session history, resume and compaction | Continue a particular conversation and its work | Stored thread history, `thread/resume`, and compaction checkpoints. A successful resume does not test recall after that history disappears. |
| Local Codex memories | Carry selected preferences and reusable learning into later conversations | Background extraction, database-backed intermediate records, consolidation, generated memory files, context injection and optional dedicated memory tools. This is an implemented lifecycle. |
| Being-level durable memory | Preserve selected relationships, experiences and learning across authorized bodies and harnesses | HMK's intended role here, supplemented by source-authoritative projections. Lifelong preservation and receiving acceptance still need the existing HMK fixes and evaluation. |

The official [memory documentation](https://learn.chatgpt.com/docs/customization/memories)
describes a local store separate from ChatGPT web memory. The
[App Server interface](https://learn.chatgpt.com/docs/app-server#api-overview)
describes thread resume and stored history. These are different mechanisms.

The native [extraction prompt](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/templates/memories/stage_one_system.md)
prioritizes useful operating preferences, proven procedures, task maps and
environment/workflow knowledge. It also considers tool evidence and allows
empty output. Its selection criterion emphasizes improving future work. A
meaningful shared moment can matter to a being without changing a future coding
workflow; our selection and recall contract must cover that case explicitly.
This is a difference in intended coverage, not a measured native failure.

## What Codex contemplates for external memory

There are two distinct source-level mechanisms:

1. **An interface that anticipates a remote backend.** The public Rust
   [`MemoriesBackend` trait](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/backend.rs)
   explicitly permits a future remote implementation. It provides list, read,
   search and add-ad-hoc-note operations with relative paths, lines, token limits,
   pagination and lexical match modes. The
   [installed extension](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/extension.rs)
   constructs `LocalMemoriesBackend` directly. This is a compiled integration
   seam; no configuration-only HMK backend was established.
2. **Import of selected external-agent memory.** The
   [discovery code](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/external-agent-migration/src/memory.rs)
   discovers Markdown in an external agent's project memory directories and
   resolves project scope from its session metadata. The
   [importer](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/external-agent-migration/src/memory_import.rs)
   copies selected project resources into the native memory workspace, records
   their scope and source-specific interpretation rules, and enqueues native
   consolidation when the workspace changes. This imports material into local
   Codex memory; it does not establish a live external canonical store. Do not
   manufacture third-party session metadata to make HMK appear to be that source.

An HMK MCP tool can provide authorized retrieval independently. Installing it
does not redirect native extraction, consolidation or automatic context
injection. The native summary
[read path](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/prompts.rs)
still reads `memory_summary.md` from the selected native memory namespace.

## Native behavior to preserve and qualify

| Behavior | Source evidence | HMK integration consequence |
|---|---|---|
| Bounded background extraction | [Startup](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/start.rs), [phase 1](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/phase1.rs): root-session eligibility, pruning, quota gate, bounded source claims and stored extraction outcomes | Manual HMK retrieval alone does not replace capture. Preserve scheduling, source selection, no-op and failure/retry behavior if adapting it. |
| Serialized consolidation | [Phase 2](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/phase2.rs): global lease, selected inputs, workspace diff, consolidation agent, artifact/ownership validation and completion | Reuse this behavior when practical. A read backend does not intercept this separate database/files writer. |
| Versioned output | [Config/defaults](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/config/src/types.rs), [V1 prompt](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/templates/memories/consolidation.md), [V2 prompt](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/templates/memories/consolidation_v2.md) | V1 defaults to a searchable `MEMORY.md`, compact summary and optional learned skills; V2 uses a different summary contract. Compare the selected version; prompt requirements are not observed reliability. |
| Source-linked external resources | [Importer](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/external-agent-migration/src/memory_import.rs) preserves project hierarchy and distinct evidence pointers | A possible pattern for selected HMK indexes. A generic HMK source registration and update/retraction path remain to be qualified. |
| Retrieval and initial context | [Backend](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/backend.rs), [extension](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/extension.rs), [prompts](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/ext/memories/src/prompts.rs) | Preserve citation, path/line, namespace and truncation contracts alongside semantic retrieval. Dedicated tools have their own enablement setting. |
| Thread use and contribution controls | [Config](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/config/src/types.rs), [selection](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/state/src/runtime/memories.rs) | `generate_memories=false` disables contribution for newly created threads, not every pre-existing enabled thread. A shared native home is unsuitable for the first fictional experiment. |
| Source eligibility | [Allowed interactive sources](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/rollout/src/lib.rs), [claim call](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/phase1.rs) | Verify the actual Telegram session source. The inspected claim call supplies no signed being binding or explicit per-project allowlist. |
| External-context eligibility | [Official controls](https://learn.chatgpt.com/docs/customization/memories), [pinned defaults](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/config/src/types.rs) | `disable_on_external_context=true` excludes chats that used external context from generation; the older `no_memories_if_mcp_or_web_search` key remains an alias. Its pinned default is false. Test this explicitly with an HMK MCP adapter and external communications: excluding these chats can lose meaningful input, while allowing them requires protection against treating recalled memory as independent new evidence. |
| Worker capabilities | [Consolidator configuration](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/phase2.rs) disables MCP, plugins, native memory tools and recursive collaboration | An HMK MCP installation alone cannot connect this writer. Managed permissions restrict local writes/network; explicitly disabled or external parent permission profiles are preserved. |

## Persistence is not a lifelong preservation guarantee

Codex memories persist on disk between sessions. That does not make the native
store an immutable autobiography or a complete record of significant encounters.
In this version:

- [Phase-2 selection and pruning](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/state/src/runtime/memories.rs)
  use a configured unused-time window and bounded input set. Selection ranks
  usage count and recency; the unused-time fallback is `source_updated_at` when
  there is no `last_usage`. Pruning deletes stale unselected stage-1 outputs.
  The code is more precise than the repository README's `generated_at` wording.
- [Workspace synchronization](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/phase2.rs)
  removes summaries outside the current selection; consolidation handles the
  resulting changes. The memory
  [git workspace](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/memories/write/src/workspace.rs)
  is a resettable comparison baseline, not guaranteed retained revision history.
- Removing a native source or revising a generated current summary does not
  authorize erasing an independently retained HMK episode. Conversely, a revoked
  source must not survive by blindly copying it into another authority. Preserve
  the record's classification, consent and correction/retraction semantics.
- HMK had confirmed overwrite/history gaps at initial review. The repaired fork
  now preserves native revisions, but the partial model pilot still fails essential
  selection/weak-cue recall. See the maintained [plan](durable-recall-plan.md);
  intended scope does not establish the ten-year contract.

## Integration decision and smallest next experiment

The later [lifelong-memory review](lifelong-memory-portability-review.md)
supersedes any assumption that every native artifact must be regenerable from
HMK. Native-authored learning is part of the being's accumulated delta: preserve
its original representation, available history and provenance separately from
selected projections. Compare Codex plus collective-memory and other backends
against the same enduring-memory contract. HMK retention is not the goal.

Keep three routes open under [issue #11](https://github.com/nicoechaniz/hermes-memory-kit/issues/11):

| Route | Benefit | Qualification work |
|---|---|---|
| HMK backs native reads, capture and consolidation | One being-level canonical store while preserving native behavior | Backend selection, context contribution, writer integration, native citation/procedure semantics and HMK preserved revisions; end-to-end parity is unproven. |
| Native Codex memory coexists with HMK | Keep native workflow learning and use HMK for shared durable experience | Explicit authority per record, selected source indexes, correction propagation and scoped eligibility; first practical experimental candidate. |
| HMK plus custom hooks | Existing shared corpus remains central | Recreate and qualify whatever native extraction, consolidation, context and usage behavior would otherwise be lost. A compact hook alone is insufficient. |

For controlled coexistence, native-authored engineering learning can remain
native. HMK-authored experience remains HMK. Where both need one fact, use an
attributed, repairable index with an explicit owner, rather than independently
editing two versions of the same fact. This is an experiment proposal, not an
adapter that has been deployed.

Domain descriptions in a prompt do not establish source isolation. Qualify
thread eligibility, namespace boundaries and the external-context setting in
the actual lifecycle. Keep origin/record/version identifiers on projections;
a retrieved HMK record must not become independent corroboration of itself
when a later native pass extracts the conversation. Corrections and retractions
must update or invalidate those projections through their recorded owner.

Use the existing fictional corpus and an isolated native test home. Start with
one reusable engineering lesson, one enduring preference, one autobiographical
episode, one correction and one routine exchange. Record native version/model,
input scope, formation cost, memory outputs and answering budget. Compare native
alone with native plus selected HMK indexes through the real extraction,
consolidation and retrieval lifecycle; do not synthesize expected memory files
and call that a native baseline.

Fresh-session checks cover recall, exact evidence, corrected current claims plus
retained history, duplication, no-op selection, source deletion, source isolation,
quota/storage cost, embedding outage and restart. Add the source-loss and ten-year
perturbations from the [durable-recall plan](durable-recall-plan.md). Identify the
actual source-registration seam before attempting the smallest adapter change.
Prefer controlled coexistence if preserving parity requires a broad harness fork.
Finish that experiment with one implementation route and explicit measured limits.

The bounded continuity/candidate hook design stays in
[issue #12](https://github.com/nicoechaniz/hermes-memory-kit/issues/12).
[`PreCompact`](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/hooks/src/events/compact.rs)
is a compaction event, not an established native-consolidation-completed event.

The human's October 7 follow-up selects HMK health repairs under
[issue #13](https://github.com/nicoechaniz/hermes-memory-kit/issues/13) before the
native coexistence experiment. A later adapter may observe supported native
memory operations and submit candidates for being-level selection. Distinguish
read/use, new extraction, consolidated publication, correction and retraction;
each has a different evidence contract. Repeated reads do not create new lived
events or independent corroboration. Candidate acceptance preserves originating
record/version, body/session scope, selected sufficient evidence and uncertainty.

The official [hooks interface](https://learn.chatgpt.com/docs/hooks) exposes
`PostToolUse` for supported local tool paths, with tool identity, input and
response. The pinned [hook registry](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/hooks/src/registry.rs)
and [event modules](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/hooks/src/events/mod.rs)
do not establish a dedicated memory-consolidation-completed event. Tool coverage
also has exceptions. Qualification must prove the actual native memory path's
hook coverage; automatic context injection and the separate background writer
cannot be assumed to produce `PostToolUse`. Where no suitable event exists,
propose an explicit committed-memory notification/adapter in the owning harness,
with idempotent deltas and receiving receipts, rather than promising observation
of every memory action through a tool hook. No observer or hook is installed here.

## Receiving state and evidence limits

The human authorized enabling the Codex hooks framework in the other project
conversation; the 2026-10-07 receiving check confirms it is enabled. The check
also confirms native memories, external memory import, generation and use are
disabled, with no explicit memory version override. An October 7 follow-up
reconfirmed those settings and CLI version; the external-context option and its
older alias are unset, so the pinned false default applies. No HMK memory hook handler
was installed by this investigation. Existing manual access remains distinct
from any later qualified lifecycle integration.

This addendum reads the explicitly supplied project handoff, official docs and
pinned public implementation files. No unrelated session content was inspected
or imported, and no live memory feature was activated. No competitor, native
model baseline or HMK integration was benchmarked here. Research publication is
separate from receiving configuration and adoption.
