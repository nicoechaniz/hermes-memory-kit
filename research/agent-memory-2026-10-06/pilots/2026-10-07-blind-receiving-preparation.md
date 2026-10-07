# Blind receiving preparation, 2026-10-07

**This is prepared input, not qualified recall.** The finite
[`receiving_exchange.py`](receiving_exchange.py) prepares packets and transports
externally obtained responses. It dispatches no Codex session or subagent and
activates no native memory, hook, timer or autonomous attention.

The [manifest](blind-receiving-evidence/v1/manifest.json) preserves all 44 actual
packets, contexts, timestamps, replayed plans, canonical/history checks, query
embedding traces, costs and the first prepared Sol request. The receiver's
process consumes only these frozen packets; it does not read the corpus/rubric
or source databases. No expected meaning, positive requirement, forbidden claim
or previous answer/review is fed into receiving generation.

## Experiment boundary

The packets start from v8's **pre-recall formation**, not its already queried
receiver database. All original chapters have zero accesses and no last-access
timestamp. Original creation/update times and revisions remain intact; no old
usage history is reset to manufacture a cold experiment. The snapshot excludes
original capture ledgers. Retrieval actually uses the original +10-year clocks,
with the three recent unrelated distractors still present.

The recorded question-derived v8 planner outputs are replayed through the upgraded
reader. Expansion IDs must still be visible in the new initial packet, and a
null initial pack still requires a bounded refinement. This fixes retrieval
input for a **narrative comparison**; it is not an end-to-end qualification of a
new model's planning or capture. Compare receiving models over the identical
packets within each arm, and keep their actual provider/effort settings explicit.
Both policy arms use the same reader, bounds and plan-replay procedure.

| Observation | Baseline | Proposed |
|---|---:|---:|
| Questions frozen | 22 | 22 |
| Actual packs | 48 | 45 |
| Maximum estimated pack tokens, limit 1,500 | 1,415 | 1,499 |
| Query embedding calls | 48 | 45 |
| Calls without reported embedding token usage | 48 | 45 |
| Generative chat requests during freezing | 0 | 0 |
| Canonical/history values preserved | Yes | Yes |

Every observed retrieval status is `ok`. Both Ren packets now expose the retained
failure source, chapter 13, alongside the authorized attempt and known map
collaborator. This establishes available support for the actual validation
failure/unpublished link, not successful narration or receipt of the chart.
The [preservation check](blind-receiving-evidence/v1/preservation.json) excludes
only `last_access` and `access_count`, which legitimately change during retrieval;
all other canonical/history columns remain checked. The
[cost ledger](blind-receiving-evidence/v1/costs.json) distinguishes zero generative
dispatches from the 93 real query embedding requests with unknown token usage.
The freeze conditions' model-request count refers to generative dispatch only.

## External response transport

Each pending generation, review or revision becomes one self-contained request
with a model/effort selection, the actual messages and closed output schema.
`receive` prints its path and stops when the external response is unavailable.
It starts no background worker. The
[prepared Sol request](blind-receiving-evidence/v1/prepared-sol-request.json)
selects `gpt-6.1-sol`, `xhigh`; it has not been dispatched and establishes no
account availability, model quality, context isolation or receiving acceptance.

An explicitly authorized dispatcher must create a fresh context for **each**
request, pass only its supplied messages/schema, keep native memory disabled,
and prevent source/session/tool reads. Do not inherit the supervising thread
or send the corpus, previous diagnostic answers or rubric. If using a native
Codex process, [official non-interactive documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
documents schema output, JSON events and ephemeral execution; the
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents relevant controls. Those controls are not a receiving acceptance test.
Validate the actual invocation and transcript rather than assuming an empty
working directory or read-only sandbox makes all source reads impossible.
This delivery supplies a transport, not an automatically configured native worker.

The response file is named by the canonical request hash and must preserve:

- `request_sha256`, `requested_model`, and raw final-message `content`;
- `fresh_context: true`, `tool_calls_observed: []`, and an actual
  `dispatch_receipt` reference for the supervising body's independent inspection;
- `response_model`, `seconds`, and `usage` when actually observed, otherwise
  null/unknown. Known usage requires nonnegative prompt/completion/total counts.

These fields are operator evidence claims, not signed identity/capability proofs
or a guarantee of isolation. The supervisor must inspect the actual referenced
dispatch and trace. Mismatched or contaminated responses are retained and rejected.
Re-reading one saved response after interruption records one observed call,
not a new execution. Provider usage that was not supplied remains unknown.
The existing bounded phase cursor, local validators and outside grading still
apply. Completing a candidate or getting a model's supported verdict never
sets `qualification` to true.

## Exact continuation

Choose and authorize the external receiving setup, inspect its actual fresh
context/tool/native-memory boundaries, and answer the prepared request. Continue
the exchange through all 44 cases, retaining every failure, revision and cost.
Independently grade every assertion and all 51 positive requirements per arm,
plus forbidden assertions, selection and preservation. Model-only comparison
reuses these exact packets; an end-to-end planner comparison must be separately
labelled and frozen. Natural narration and the three stage-two passes remain
pending. After narration qualifies, perform organization, replay and dependent
correction/reconciliation with recall after each transformation.

Validation: 258 tests pass, including response timeout/preparation without
dispatch, preserved pending candidates, source/rubric-free response consumption,
request/model mismatches, observed tool use, missing receipt, invalid usage,
exact-context changes, cold-formation rejection, original/history preservation
and idempotent response consumption. The live CLI/database installation is
unchanged by this research delivery.
