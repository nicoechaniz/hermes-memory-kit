# Native Sol low versus Flash low: fictional review role

This bounded diagnostic compares four initial reviews of identical fictional
candidates and evidence. Only the requested model changes in the prepared
request: DeepSeek Flash through its direct API versus `gpt-6.1-sol` low through
OpenAI Codex. It does not qualify the full receiving or consolidation pipeline.
No hidden rubric, private memory, other conversation or external tool is supplied.
Qwen is deferred under the human's current quota constraint.

The [manifest and actual requests/responses](receiving-api-evidence/sol-review-probe-v3/manifest.json)
retain both routes. Native task instructions occupy the developer role and its
generic base remains; this harness difference is explicit. New ephemeral threads
mask the existing Codex home with a private mount namespace and expose only the
existing authentication file read-only. No credential is copied. Tools, skills,
private instructions and native memory remain disabled. Initial review requests
use the same supplied system/user text pair as narration. Future repairs can
carry an explicitly labelled transcript; that rendering needs its own observed
qualification, not an assumption of native session continuity.

## Observations

All four native reviews satisfy the local assertion/proof schema after selecting
exact original passage IDs. The local diagnostic initially unpacked the compiled
review incorrectly; correcting that local assessment reread the saved responses
and made **zero** additional inference requests. Raw reviews remain unchanged.

Both reviewers detect the unsupported claim that Mara opened issue 47: the source
credits a comment, not issue authorship. Both also distinguish packet absence
from positive historical memory. Sol detects a genuine change from talking
*through* the porch speaker to talking *about* it. It does not demand literal
copying of candidate prose as source proof. These are useful role observations,
not a measure of complete semantic recall.

Sol still requests additional project contributions/repository details when the
question asks about the old proposer, although the candidate already gives the
issue pointer, proposal, interest, agreement and later reported outcome. Those
requests need relevance adjudication. Its correction-versus-initial-report
objection also depends on whether “corrected record” denotes the entire retained
record or only its later source block. Neither objection is automatic evidence
that the remembered facts are wrong. Flash's complete passage trial separately
exhibits uncited-proof errors and overly literal significance judgments. No
provider winner or complete narrative pass is declared from these four reviews.

## Consumption and setup preservation

[Costs](receiving-api-evidence/sol-review-probe-v3/costs.json) are separated by route:

| Four initial reviews | Input tokens | Output tokens | Total | Median request seconds |
|---|---:|---:|---:|---:|
| Native OpenAI Codex Sol low | 46,396 | 8,533 | 54,929 | 45.60 |
| Direct DeepSeek Flash low | 19,511 | 63,123 | 82,634 | 63.06 |

Native generic input overhead is included. Actual billing and native subscription
quota conversion are unknown. This is not a price comparison based on the Nous
route. No embeddings, selection or consolidation calls belong to this diagnostic.
Five failed local CLI setup attempts are retained separately with unknown usage;
they exited before returning native JSON events. The demonstrated setup defect
was a relative model-catalog path interpreted after changing the native cwd.
The adapter now resolves request, output and catalog paths before dispatch.
It never retries an observed or unresolved dispatch implicitly.

Validation: four native adapter tests pass, covering isolation, actual usage,
refusal of tool effects, preservation of failures and explicit transcript roles.
Next: finish and independently grade every claim and requirement of the complete
Flash passage trial; select a complete receiving configuration from demonstrated
results, then run changed Flash formation and all stage-two transformations.
