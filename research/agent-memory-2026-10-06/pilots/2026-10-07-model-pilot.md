# Partial HMK model pilot — failures and remaining qualification

Run on 2026-10-07 using only the existing fictional
[corpus](../../../docs/benchmarks/durable-recall-cases.json). This is an additive
result, not an edit to the closed research reports or a native Codex comparison.
The [full available synthetic evidence](2026-10-07-partial-evidence.json) contains
conditions, proposals, receipts, retrieval packs, expansions, answers and trace
metadata. No real autobiography, credentials or private session is included.

## Conditions and coverage

- Kit baseline: `d58800e0d037e0d34956789b7c4c5ea670732b6f`, plus the recorded
  capture-schema/link-error and prototype runner changes. Runner hashes/resume
  revisions and guidance/fixture hashes are retained in evidence.
- Capturing/answering model: `nvidia/nemotron-3-super-120b-a12b`, temperature 0,
  low reasoning effort; actual API responses, not manually manufactured memories.
  This model was explicitly selected for the isolated pilot; the body's default
  inference configuration was not changed.
- Embeddings: the configured `nvidia/nemotron-3-embed-1b`; reranking disabled.
  Initial retrieval: threshold 0.4, budget 1,500 tokens, five candidates, followed
  by bounded model-planned queries/expansion.
- Baseline: librarian at `5926a9d1c120e2d5fcc53e0ef3dd692e2b90da5d`.
  Proposed: shipped durable selection reference. Both use the same structural
  record prompt, corpus and model, in separate fresh synthetic pools.
- All 12 cases captured in order for both variants. Expected meaning and later
  questions were hidden during formation. A visible shape-only repair can use
  the writer's validation error, without the hidden rubric.
- Fresh recall requests received only questions and permitted packs/expansions,
  with no source messages, expected answers or native history. The retrieval
  clock advanced ten years; original timestamps were retained and three newer
  fictional topical distractors inserted. Source URLs were not fetched.
- Available answers: baseline 10 of 16; proposed 16 of 16. The runner then failed
  on an invalid model recall-plan shape. Three-pass consolidation, complete
  aggregate evaluation and total-cost accounting were not completed. Model trace
  counts alone exclude earlier failed attempts and cannot establish total cost.

The [prototype runner](durable_recall_pilot.py) is published for inspection. It is
an explicit research command, not installed capture or a production benchmark.
Its JSON/error handling still needs qualification. Resume preserves frozen model,
guidance/fixture conditions and previous output; it does not turn this failed run
into a completed benchmark. No further model run was made to hide these failures.

## Mandatory weak-cue recall failed

Both variants failed the first issue question, asking for the person who proposed
something interesting in an issue on a relay project. The participant and
proposal existed in the selected canon, but retrieval returned newer unrelated
relay maintenance. Both answering requests abstained. Naming HarborMesh in the
next question recovered Mara Ibarra and the replay proposal; that does not satisfy
the deliberately weak first cue, and the proposed answer still omitted some
known identifying/qualified meaning.

A diagnostic on a separate copy of the proposed fictional pool found:

| Signal | Relevant Mara episode | New distractors |
|---|---|---|
| Lexical score for the full weak question | 0.5429 | 0.4451 / 0.4326 / 0.4242 |
| Semantic score | 0.191367 | approximately 0.303 |
| Hybrid result at threshold 0.4 | Excluded | Included |

A narrow `issue` lexical query recovered the relevant episode at 0.8. The
combined relevance gate diluted a strong lexical candidate with weak semantic
similarity and old-record ranking. This identifies a retrieval defect to isolate;
lowering the global threshold or padding packs is not a demonstrated fix. The
diagnostic was not fed back into the recorded recall model.

## Selection lost a meaningful unsuccessful action

In `intent-versus-observed-action`, the human authorized inviting an already-known
participant, Jo Vale, to a workshop. The tool created an invitation object but
delivery failed; no response or acceptance was observed. The baseline retained
the attempt and linked the previous encounter. The proposed policy omitted it,
reasoning that unsuccessful delivery created no meaningful relationship or
learning. The omitted action therefore cannot be recovered later from canon.

A meaningful attempt or unresolved action may continue an existing relationship
without establishing a new trait or reusable lesson. Selection needs to preserve
that history and the observed failure; routine retries still belong in project
state. This single observed regression does not establish a general rate, nor
that the older ingestion policy is preferable overall. Policy repair and a fresh
formation/recall test remain pending under the
[maintained plan](../../../docs/durable-recall-plan.md).

## Structural fixes and conclusions

Earlier partial attempts generated unsupported record fields, invalid metadata
types and string references to old chapter IDs. Capture correctly refused those
proposals and retained failed pending payloads. The maintained writer now exposes
`capturectl decision-schema` without opening a pool, gives actionable field/link
errors, and verifies referenced integer chapter IDs before the atomic commit.
Regression tests confirm malformed-link rollback, preserved pending work and no
cursor advancement. The complete mechanical suite passes 191 tests.

Mechanical preservation and receiving tool operation do not establish model
selection or lifelong recall. No aggregate score, native parity, competitor
superiority, cross-body conversational acceptance or successful three-pass dream
is claimed. These failures must accompany the
[backend/interchange reassessment](../../../docs/lifelong-memory-portability-review.md).
