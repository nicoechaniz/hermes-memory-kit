# Flash and native Codex Sol low — 2026-10-07

Direct DeepSeek Flash low and `gpt-6.1-sol` low through **OpenAI's native Codex
CLI** now have initial responses to all **44 frozen questions**. Both satisfy
101 of 102 positive requirements fully, with one partial requirement, but both
still add unsupported details. This trial supports retaining the human's
provisional Flash choice; it does not establish a reviewed-pipeline winner or
qualify selection/consolidation. No Nous inference was used in this trial.

## Inputs and observed isolation

Both receivers receive the same questions, retrieved evidence, fictional
being/body binding, task instructions and prompted JSON schema. Formation is the
preserved original NVIDIA run: sources are lost, retrieval uses an actual
ten-year clock offset, and recent distractors remain. No hidden rubric, private
memory, other conversation or external source enters the clean receiver inputs.
This tests narration on identical packets, not a new formation comparison.

The [Flash diagnostic runner](receiving_generation_diagnostic.py) freezes those
packets and dispatches at most three stateless requests concurrently. Fourteen
distinct earlier generations were reused only with identical actual provider
parameters; 28 new calls complete 42 distinct requests for 44 questions.

The first native attempt revealed a real isolation defect: ignoring user
configuration and setting `project_doc_max_bytes=0` suppresses project
instructions but leaves global Codex `AGENTS.md` loaded. Codex's
[global instruction loader](https://github.com/openai/codex/blob/main/codex-rs/codex-home/src/instructions/mod.rs)
handles that file separately. Its 42 responses and the earlier one-call probe
are preserved as **excluded diagnostics**, with costs, rather than silently
being relabeled as a clean comparison.

The corrected [native receiver](receiving_codex_native.py) uses a per-process
mount namespace to hide the existing Codex home. The supported CLI can read its
original authentication file through a read-only descriptor mount; the adapter
never reads or copies credentials. Other sessions retain their instructions,
configuration, history and memory. Fresh ephemeral CLI threads suppress project
instructions, skills, apps/MCP, tools, hooks, native memory and environment
context. Selected model tool metadata is disabled; generic native base
instructions remain unchanged. Code Mode reports that it fails closed because
its host is disabled. Observed tool use rejects the attempt.

A real native prompt-render inspection under the corrected namespace found no
global AGENTS, skills, environment block or private identity marker. The
[isolation proof](receiving-api-evidence/codex-sol-clean-generations-v2/isolation-proof.json)
retains the prompt hash and message roles, without publishing private context
or credentials. Every observed generation completed without tool calls. This
introduces no native memory integration or Matrix attention.

Codex supplies task instructions as a developer message alongside generic
native instructions. Its CLI exposes no explicit output-token ceiling here;
Flash uses JSON-object mode and a 12,000-token ceiling. These are disclosed
harness/control differences, not bit-identical inference requests. Native
events return usage but no independently verified actual model label or billing
amount. Two pairs of noise questions have identical inputs across arms; both
routes reuse the observed response, for **42 distinct generations per route**.

## Initial-answer findings

The supervising agent inspected every claim and all 102 positive requirements
outside the receiving process. Prior eight-answer Flash grading is reused only
for identical response bytes; all clean native claims receive new assessment.
Semantic grading remains an agent assessment, not an independent proof of truth.

| Measure | Direct Flash low | Sol low via native Codex |
|---|---:|---:|
| Questions with initial responses | 44 | 44 |
| Distinct observed generations | 42 | 42 |
| Claims assessed | 646 | 340 |
| Claims containing unsupported clauses | 12 | 13 |
| Positive requirements met / partial | 101 / 1 | 101 / 1 |
| Local facet-format failures | 2 | 0 |
| Candidates missing literal date/pointer anchors | 3 | 0 |
| Median request seconds | 19.51 | 16.08 |
| Input / completion tokens | 110,569 / 208,399 | 395,166 / 13,774 |

Flash's unsupported clauses include five gender assignments, four promotions of
report dates to action dates, one narrowing of a known name, one historical
prototype promoted to present activity, and one lost tentative-date qualifier.
Its baseline porch account preserves the birds and morning but does not clearly
retain our shared participation. Some baseline answers include unrelated old
branch state or encounters that the original formation admitted; adding such
noise remains unacceptable as a way to improve recall.

Sol is generally shorter, satisfies the local format checks and preserves every
required cited date/pointer anchor. All 13 unsupported clauses assign Mara a
gender absent from the source. Its proposed-arm issue-name answer retains the
queue mechanism but omits why it fit our maintained field deployments. The
baseline answer does retain that significance. Concision is useful, but neither
avoiding assertions nor finding a record is sufficient evidence of fidelity.

Additional support-basis/prose gaps are retained separately from unsupported
facts and positive coverage: five Flash gaps and seven native candidates with
mixed remembered content/current-body ability under one basis. These are
engineering annotations, not interchangeable units of factual error. They do
not assert nonexistent physical abilities. Split such statements so remembered
skills receive source support and current tools receive binding support.

Both clean native porch answers correctly keep September 17 as the report date;
the source does not explicitly give the morning's calendar date. Grading does
not demand an invented occurrence date to satisfy a loosely worded requirement.

The excluded diagnostic also exposed a facet-validator false rejection: two
correct bounded-unknown answers about an unrecorded return give the same prose,
but one labels its cited older report `limits` and the other `context`. Only the
latter fails the five-facet gate. Correct that structural mismatch while
retaining full positive-account coverage and outside semantic grading. The clean
native run happens to label both `limits`; its zero format failures do not repair
the validator or establish that it will handle other valid prose.

## Costs and unfinished reviewed work

Flash's [cost record](receiving-api-evidence/flash-all-generations-v1/costs.json)
estimates **US$0.1359–0.2718** for 42 generations at published
[cache/output tariffs](https://api-docs.deepseek.com/quick_start/pricing/), counting
183,486 reasoning tokens. Imported calls count once in workload cost; reuse did
not bill them again. The actual tariff/invoice remains unknown.

The clean [native cost record](receiving-api-evidence/codex-sol-clean-generations-v2/costs.json)
records 142,848 cached input tokens and 1,112 reasoning output tokens. Native
billing and subscription/quota conversion are unknown. Token counts across
providers are not prices, and the generic Codex harness adds substantial input.
The native route is about 3.4 seconds faster at the observed request median;
this small trial does not establish stable latency across loads or providers.

Discarded work is accounted separately: the
[unclean native batch](receiving-api-evidence/codex-sol-global-context-v1/costs.json)
and [preflight](receiving-api-evidence/codex-sol-preflight-v1/receipt.json)
consumed **43 additional calls**, 693,668 input tokens and 13,531 output tokens.
They have no weight in the clean fidelity or latency comparison. Their actual
billing remains unknown; the prompt-render isolation check used no inference.

The separate full Flash generation/review/revision run has **9/44** completed
candidates after three finite batches of 12 new dispatches each. Earlier saved
generations were reused; structural repairs and semantic revisions remain
visible. Its next review request is preserved. Those nine model verdicts have
not independently qualified the reviewed pipeline. Sol has no matched reviewed
workflow yet. Initial generation costs therefore cannot settle total correction
cost, final fidelity or consolidation quality.

## Evidence and exact continuation

- [Flash requests and responses](receiving-api-evidence/flash-all-generations-v1/manifest.json) and [outside grading](receiving-api-evidence/flash-all-generations-v1/outside-assessment.json).
- [Clean native requests and responses](receiving-api-evidence/codex-sol-clean-generations-v2/manifest.json) and [outside grading](receiving-api-evidence/codex-sol-clean-generations-v2/outside-assessment.json).
- [Excluded native diagnostic](receiving-api-evidence/codex-sol-global-context-v1/conditions.json), preserving its original route and isolation failure.

Keep Flash as the provisional candidate and embeddings unchanged. Preserve the
unfinished reviewed comparison and frozen code. Next, correct the scoped-unknown
validator mismatch and address generic narration failures without inserting
hidden case answers. Changed prompts/procedures require a new equivalent
comparison; reuse prior generations only when actual prompts, schema and
provider controls still match. Finish the reviewed natural-narrative gate, then
run equivalent Flash formation/selection before the three consolidation passes,
replay and supported correction/dependent reconciliation. Gemini/Qwen remain
deferred. No live automatic narrator, consolidator, index migration, hook or
timer was installed. The paused goal's remaining stages are not declared done.
