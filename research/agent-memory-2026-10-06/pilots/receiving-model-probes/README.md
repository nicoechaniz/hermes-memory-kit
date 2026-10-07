# Receiving API probes, 2026-10-07

These bounded fictional probes check an available alternative receiving endpoint,
not durable-memory or narrative qualification. The selected embedding provider
and original formation stay unchanged. The [manifest](manifest.json) hashes
the exact request parameters and observed responses, omitting credentials and
provider reasoning text.

| Probe | Model | Outcome | Usage |
|---|---|---|---|
| [Initial request](provider-ultra-availability-probe.json) | `nvidia/nemotron-3-ultra-550b-a55b` | HTTP 503, temporarily overloaded | Unknown |
| [Bounded recheck](provider-ultra-availability-recheck.json) | Same | HTTP 400: the deployed V2 runner rejects the explicit reasoning budget | Unknown |
| [Explicit budget omission](provider-ultra-no-budget-probe.json) | Same | HTTP 200 and valid requested object shape, but the requested quotation was empty | 57 prompt + 369 completion = 426 tokens |

The successful request retained the original prompt and schema and omitted only
the server-rejected budget parameter. The prompt supplied Aro's quotation about
the speaker stopping buzzing and requested its preservation. The returned
`quotation` was the empty string. Thus availability and schema-shaped output
were observed, but source fidelity failed in this sample. These probes establish
neither a superior model nor a complete comparison. Failed requests with no
reported usage are unknown, not zero cost. They are separate from the v8 run.

The pilot now permits an explicit receiving-model selection independently of
formation, and an explicit `none` reasoning budget for compatible requests.
Those choices remain frozen and equal across both arms. They do not bypass
local validators, hidden-rubric grading or memory-preservation requirements.
No native memory, new inference credentials, subagent, hook or automatic
attention was installed by these probes.
