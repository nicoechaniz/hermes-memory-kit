# Observed cost: receiving qualification versus daily organization

The [reader-authority closing](2026-10-08-reader-authority-closing-qualification.md)
uses 137 new physical calls to test 44 independent answers and 102 content
requirements. It is a qualification battery, not a nightly consolidation budget.
The cost is modest in dollars; additional repair/time remains a separate concern.

## Token-based reference, checked 2026-10-08

| Work | Actual new token split | Reference USD |
|---|---|---:|
| 30 direct DeepSeek calls | 74,368 cached input; 74,424 uncached input; 188,447 output | 0.12445–0.24891 |
| 107 native Codex Sol calls | 995,168 uncached input; 462,720 cached input; 265,113 output; zero cache-write tokens | 4.68774 hypothetical API Standard |
| Combined closing | Above actual token counts | 4.81219–4.93665 hypothetical combined reference |
| Preserved organization, 34 distinct Flash calls | 26,624 cached input; 116,006 uncached input; 203,778 output | 0.13975–0.27950 |

[DeepSeek's current official tariff](https://api-docs.deepseek.com/quick_start/pricing/)
for deepseek-flash (served by DeepSeek-V4.1-Flash) is USD 0.003/0.15/0.60 per million
cached-input/uncached-input/output tokens off-peak, twice those rates at peak.
The range prices every call at either extreme; it is not an observed invoice.
It includes reported output/reasoning tokens and actual input cache hits.

[Sol 6.1 API Standard](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
is USD 2 uncached input / 0.10 cached input / 10 output per million at these short
context sizes. The original native receipts expose 462,720 cached input tokens
within 1,457,888 total input tokens and zero explicit cache-write tokens. The
reference uses those counters and excludes Fast/other premiums. Reported reasoning
output is already included in output tokens and is not charged twice. The initial
conservative estimate without a cache discount was USD 5.56691 for Sol and
5.69136–5.81582 combined; the cache-aware figures above replace that reference.
**The actual Sol calls use the ChatGPT Codex subscription, not API billing.**
[Subscription/credit usage](https://learn.chatgpt.com/docs/pricing) is separate;
the API equivalent does not establish an extra charge or remaining plan allowance.
Earlier reused physical calls are not billed again in this closing estimate.

## What a daily consolidation would do

The preserved organization evidence comprises three passes updating four accounts,
plus direct/transitive correction reconciliation: fourteen applied updates, 34
physical model calls and 346,408 tokens. All generations, reviews and the actual
bounded correction are counted. The whole observed organization set is roughly
USD 0.14–0.28 at current Flash prices, independently of receiving tests.

For four affected accounts of comparable size, a reference is about 8–12 calls
and USD 0.04–0.08, extrapolated from the measured average per applied update.
This is not a measured daily workload or fixed cap. Daily volume, account count,
changed inputs and repairs determine the actual work. Selection/capture of new
experiences, embeddings and narrative answers have separate costs; the number
above covers account organization only.

A daily run should process the delta and affected accounts, reusing unchanged
source fingerprints and exact replay where valid. It should not repeat this
44-answer qualification battery or all three experimental consolidation passes.
Scheduling remains a later authorized step; this evidence installs no timer,
hook, native memory or autonomous attention.

Audit sources: [closing costs and raw audit](receiving-api-evidence/closing-reader-authority-v2)
and [organization costs and raw audit](receiving-api-evidence/organization-three-passes-v1).
Known token counts remain distinct from tariff estimates, invoices and quota.
