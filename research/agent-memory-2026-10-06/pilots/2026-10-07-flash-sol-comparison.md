# Flash / Sol low first-generation comparison — 2026-10-07

The human selected DeepSeek Flash for the current HMK work, deferred Gemini/Qwen
comparisons, and retained Sol 6.1 low as a candidate if consumption is modest.
This is a bounded comparison, not a provider winner or narrative/stage-two
qualification. Earlier failed diagnostics and stage-one evidence remain intact.

Eight stateless Nous API calls requested `openai/gpt-6.1-sol` with low reasoning.
All returned HTTP 200, complete JSON and that exact model label. No native Codex
account/session, subagent, tool, private memory, source URL or hidden rubric was
used. An existing authorized inference credential was read without rotation.
The native Codex memory configuration and live HMK index remain unchanged.

Each request has **identical messages and output schema** to its corresponding
[Flash diagnostic](2026-10-07-deepseek-generation-diagnostic.md): four fixed
questions in each formation arm, same evidence, binding, instructions, JSON-object
decoding and 12,000-token generation ceiling. The explicit model/route and
vendor-specific reasoning controls differ. Actual tokenizers, caching and
internal reasoning cannot be made identical by requesting low in both APIs.

The [dispatcher](receiving_text_api.py) accepts only selected fictional
DeepSeek/Nous model profiles, with no provider fallback or implicit retry. It
retains every attempted request, usage and final text, never provider reasoning
or credentials. Review/revision dispatch is supported separately, with a frozen
32,768-token review ceiling; **this Sol probe invoked neither**. Syntax decoding
does not replace local schema checks or outside grading.

## Observed results

| Measure, eight initial answers each | Direct DeepSeek Flash low | Sol 6.1 low through Nous |
|---|---:|---:|
| Completed / attempts | 8 / 8 | 8 / 8 |
| Schema-valid answers | 8 | 8 |
| Every required literal anchor retained | 7 / 8 | 8 / 8 |
| Outside claims assessed | 140 | 62 |
| Unsupported clauses | 3 | 2 |
| Positive requirements met / assessed | 24 / 24 | 22 / 24 |
| Partial positive requirements | 0 | 2 |
| Additional basis gaps | 0 | 2 |
| Median request seconds | 24.45 | 6.73 |
| Input / completion tokens | 22,738 / 43,392 | 21,508 / 2,334 |
| Reported reasoning tokens | 38,267 | 39 |
| Generation-only cost | US$0.0285–0.0569 tariff estimate | US$0.077098 provider-reported |

These counts do not establish rates over a complete test or a held-out corpus.
Shorter responses expose fewer assertions but can omit meaning. Flash retains
why the replay proposal interested us; both Sol answers omit its fit with our
field deployments. That positive requirement is partial, not met.

The proposed Sol issue answer uses "Her" and "She" for Mara without supplied
gender. Two Jo answers combine a remembered explanation ability with current
physical restrictions under a binding-only basis. The remembered method and
absent tools are supported; the binding does not explicitly supply explanation
ability. This is recorded as a basis gap, not a nonexistent physical capability.

The earlier Flash errors remain: two report dates promoted to occurrence dates,
one narrowed known name, and one missing report-date anchor. Neither model may
be qualified by ignoring the errors, passing a conservative answer or merely
finding the correct record. Sol's comparatively natural/concise prose and lower
latency make it worth retaining as a candidate; its omissions/gender still need
correction under the complete contract.

## Evidence, costs and continuation

[Sol evidence](receiving-api-evidence/sol-low-v1/manifest.json) includes every
request, receipt and raw final answer. [Outside grading](receiving-api-evidence/sol-low-v1/outside-assessment.json)
assesses all 62 claims, all 24 positive requirements and forbidden assertions.
No grader material was supplied to either receiver.

[Sol costs](receiving-api-evidence/sol-low-v1/costs.json) sum `usage.cost`, including
the provider's cache-write accounting. Receipts identify the price source as
`openrouter_list`/`openrouter_catalog`; that is observed price metadata, not proof
of the actual upstream transport. Returned model labels and requested low effort
are recorded; effective internal compute is not independently verified.
The direct [Flash estimate](receiving-api-evidence/deepseek-flash-low-v1/costs.json)
uses [published cache/output tariffs](https://api-docs.deepseek.com/quick_start/pricing/),
with actual hit/miss and all reasoning completion tokens. These billing bases
and cache behavior differ; neither is an independently reconciled invoice.

No attempt has unknown usage, and there were no new embedding, review, repair or
consolidation calls in this comparator. Generation alone is not total workflow
cost. Do not compare Flash's later review costs against unreviewed Sol answers
as though both had completed the same workflow.

Continue the complete 44-packet Flash narration/review run under frozen settings.
Its eight earlier generations can be reused only where request, schema and actual
provider parameters match exactly; retain their original receipts and count the
original work without billing it again. Preserve pending review/revision phases.
Grade all final claims and positive requirements independently. If fidelity or
total consumption warrants it, compare Sol's complete reviewed workflow under
the same contract. A changed formation/retrieval pipeline needs a separate full
comparison before stage-two consolidation, replay and correction qualification.
