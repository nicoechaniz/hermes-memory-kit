# Receiving API diagnostic, 2026-10-07

**Narration remains unqualified.** This delivery identifies a provider-format
failure and executes one actual receiving generation, not a complete comparison
or a model-quality ranking. Stage-two passes have not begun.

## Matched provider-format experiment

The original Ultra probe returned an empty quotation with provider JSON-schema
decoding. Removing that decoder produced the quoted utterance with escaped
quotation marks. Its original instruction was ambiguous about whether to copy
the utterance or the whole source line, so the automated full-line failure is
not evidence that the utterance was lost. The
[plain probe](receiving-model-probes/provider-ultra-plain-probe.json) retains
the actual response and explicitly separates these interpretations.

The matched follow-up made the full-line task explicit. Both requests used
`nvidia/nemotron-3-ultra-550b-a55b`, identical messages, temperature zero,
reasoning `high`, and 3,000 output tokens; only `response_format` differed.

| Decoder | Actual result | Reported tokens |
|---|---|---:|
| [Provider schema](receiving-model-probes/provider-ultra-paired-schema.json) | Malformed JSON, repeated whitespace, `finish_reason: length`; full line not preserved | 3,104 |
| [Plain text](receiving-model-probes/provider-ultra-paired-plain.json) | Valid JSON with the exact complete line, including both quotation marks | 399 |

This establishes a concrete compatibility difference for these observed calls,
not a universal cause of prior semantic errors or a durable-memory advantage.
All failed output and usage remain recorded. No provider reasoning text is
stored. None of these literal-copy probes qualifies narrative fidelity.

## Direct receiving transport

[`receiving_api.py`](receiving_api.py) implements an explicitly invoked, finite
NVIDIA text-only dispatcher for the existing [blind exchange](receiving_exchange.py).
It sends one fresh HTTP request per prepared phase with only the supplied
messages and output schema. It starts no agent, native harness, memory feature,
tool execution, source database, hook, timer or autonomous attention.

Both decoder modes append the same explicit schema instruction. Plain mode omits
provider schema decoding and the previously unsupported reasoning-budget field;
it does not change local shape, evidence, anchor or semantic criteria. Model,
effort, output limit, format, actual parameters/hashes, raw final text and known
or unknown usage remain visible. The supervisor still independently grades
every assertion; a model review or a completed candidate is not proof.

Completed calls cannot be re-executed silently. A failed client request can have
one **explicit** same-parameters retry, recorded separately without erasing its
unknown server execution/usage. A started or twice-failed request cannot be
silently repeated. Transport-only adoption preserves the previous conditions;
model, effort, output limit, decoder mode and endpoint must remain equal. The
receiving exchange separately freezes its narrative procedure and packet bytes.
Thus extending a client timeout can retain a saved generation instead of
generating it again. The timeout is an HTTP transport limit, not a timer that
starts an autonomous body. All calls still require explicit finite invocation.

Length-truncated output retains its exact raw final text and `finish_reason`.
It is treated as incomplete for the existing bounded local repair even if that
partial text happens to parse as JSON. Original responses and costs stay intact.

## Actual bounded receiving diagnostic

The [manifest](receiving-api-evidence/ultra-plain-v1/manifest.json) preserves the
actual requests, receipts, raw response, pending phase, trace, old/adopted
transport conditions, costs and outside assessment. It reuses the same 44
corrected-reader packets with source loss, cold formation, actual +10-year
retrieval clocks and recent distractors; no recapture or retrieval was performed.
The new schema instruction is a disclosed provider adapter, so this diagnostic
is not claimed identical to the previous Super receiving procedure.

The first baseline generation returned HTTP 200 in 35.5 seconds with 3,968
reported tokens. It preserved Mara's known identifiers, proposal, significance,
issue pointer and prototype agreement. The
[outside assessment](receiving-api-evidence/ultra-plain-v1/outside-assessment.json)
checks all seven sentences and the three positive requirements for this one
question. It identifies omitted human-report provenance/May 3 date, an unbounded
production negative, and a claim of no recorded updates after May 2 that
contradicts the supplied May 3 update. First-person narration was also absent.
The candidate is not accepted as faithful recall.

The first review request hit the 120-second client timeout. The exact generation
and review cursor remained pending. An explicit transport-only adoption extended
the HTTP limit to 300 seconds and retried **that review**, without another
generation; the retry returned HTTP 503. There is no live request handle, returned
review or completed candidate. No proposed-arm answer has been generated. The
single retry bound is exhausted for that request; do not silently overwrite its
receipts or restart the generation to hide the failure.

The [cost ledger](receiving-api-evidence/ultra-plain-v1/costs.json) records three
HTTP dispatch attempts, one completed generation with known usage and two review
attempts without usage. Those unknown costs are not zero. Formation, the 93
packet-freezing embedding requests and literal-copy probes are separate ledgers.

## Exact continuation

Choose a stable receiving setup and run the complete independently graded
comparison over both frozen arms. The separately prepared Sol request remains
unexecuted and requires explicitly selected fresh-context native/subagent
dispatch; native memory remains disabled. Preserve this failed Ultra diagnostic
and its candidate rather than treating the provider failure as narrative success
or a passing model comparison. Any resumed external review must refer to the same
request/context and disclose its actual model/procedure, without claiming that
the failed NVIDIA request completed.

Once natural narration qualifies, execute all three consolidation passes,
replay and supported correction/dependent-account reconciliation, with recall
after each transformation. The remaining scope is unchanged.

Validation: 274 tests passed, including finite dispatch, source/rubric-free text
requests, identical instructions across decoder modes, unknown-cost preservation,
refusal of silent duplicate/started executions, one explicit failed-request retry,
transport-only adoption without model changes, and raw length-truncation handling.
The installed CLI/database is unchanged by this research delivery.
