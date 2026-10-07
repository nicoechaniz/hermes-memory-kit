# Natural recall qualification procedure

This explicitly invoked fictional pilot tests whether supplied HMK memory can
support natural narration. It is not a live memory handler, proof of semantic
truth, cross-harness receiving acceptance or a completed stage-two qualification.
The owning contract remains [the durable recall plan](durable-recall-plan.md)
and [issue #13](https://github.com/nicoechaniz/hermes-memory-kit/issues/13).
Stage-one evidence remains unchanged.

The new corpus has eighteen capture cases and twenty-two receiving questions,
including human reports received through a mobile body, a declined proposal,
uncertain causal repair and an unsupported return encounter. Neither expected
meanings nor answer requirements enter capture, planning, narration or review.
Both policy arms reuse complete frozen fictional formation and use identical
receiving limits, provider/model and reasoning settings.

`--model` selects formation; `--receiving-model` explicitly selects the planner,
narrator and reviewer for both receiving arms, defaulting to the formation model.
This permits a new receiving-model comparison over unchanged formation without
changing its authorship/selection metadata or silently recapturing its sources.
The receiving selection is frozen in conditions and cannot change on resume.
Embeddings remain configured separately. This NVIDIA API selector does not add
an OpenAI adapter or authorize a fresh Codex subagent; those require their own
explicitly selected receiving setup and blind-context evidence. If planner/model
or reader changes produce different packets, do not claim an isolated model-only
comparison over identical evidence. Freeze or replay the actual supplied packets
when that narrower comparison is intended.

The external frozen-packet receiver additionally supports `--review-model` and
`--review-reasoning-effort`. `--model`/`--reasoning-effort` continue to select
generation and every revision; only atomic review uses the reviewer settings.
Defaults retain the shared-model behavior. Each selected role is frozen in the
comparison conditions; a pending reviewer or its effort cannot be replaced on
resume. A review timeout retains its generation and its repair/revision budget.
The underlying narrative procedure fingerprints a distinct reviewer while
preserving the historical shared-model fingerprint. Changed module hashes still
require a new comparison; old packets, requests, responses and checkpoints stay.
This selector adds no dispatch, independent corroboration or qualification.

Each receiving request sees only retrieved previews, bounded expansions and the
fictional binding. The source-loss database excludes capture payloads/ledgers;
retrieval actually runs with its clock advanced ten years, retaining original
record timestamps and adding recent unrelated distractors. The model cannot
open original URLs, sessions or the filesystem. A retrieval hit is not a correct
answer, and a conservative empty answer cannot satisfy a positive requirement.

## Narration and review

`--narrative` returns natural claim prose, each with visible support IDs and a
memory/binding/unknown basis. Remembered accounts cover identification, context,
meaning, outcome and limits. The adapter decodes only exact attributed source
envelopes, including retained nested envelopes. It distinguishes the source
speaker from the receiving body; unfamiliar/incomplete formats stay unknown.
It preserves the original supplied text. This is a pilot-format adapter, not a
general-purpose attribution extractor.

Report calendar dates and world pointers extracted from decoded cited support must survive
in the prose; ISO and full month-name dates preserve the same value. Missing
years, approximate dates or different years do not satisfy a full dated anchor.
This narrow mechanical check cannot verify actor ownership,
meaning, dates of occurrence, action outcomes or semantic completeness. A
separate model review decomposes each claim into assertion spans covering every
word. Each supported memory assertion must quote its actual cited source; an
unsupported clause makes the enclosing claim unsupported. The adapter validates
quote membership and decomposition, not semantic entailment. Quoting a related
passage can still be wrong, so independent grading remains mandatory. A question
asking only an unavailable detail may cite source-qualified limits without five
irrelevant filler facets; a positive remembered account still needs all five.
An answer led by a packet-scoped unknown may also retain brief cited context
from an older relevant report. That context does not establish the question's
presupposed event. This exception permits only context/limits facets after the
leading unknown; it does not replace semantic review or positive requirements.
Validation protocol `narrative-shape/v3` is frozen in the phase fingerprint, so
historical accepted or pending work cannot silently acquire new qualification.
The prior Flash procedure remains resumable with its preserved implementation
from commit `eb08e32`; its nine completed candidates and pending review are
retained separately from the corrected comparison.
The receiving API requests a closed JSON schema, with sentences bounded to 220
characters and short proof quotations (at most 400 characters each). This
reduces malformed review output and compound-claim overload without certifying
factual fidelity. The same local validators and independent semantic grading
still apply even when the provider accepts the schema. The schema hash is
recorded for each call; the frozen helper hash includes its implementation.
The explicitly selected `passages/v1` verifier receives numbered original source
headers and quotation blocks and returns `{id, passage}` references. The adapter
materializes their exact text, checks that the source is cited by the claim, and
runs the same assertion coverage, verdict and proof-membership checks. Original
model responses remain intact beside their canonical quoted review. Selecting a
valid passage is still not semantic entailment; outside grading checks that the
chosen passage actually supports the assertion. This avoids making the model
copy source punctuation without weakening factual or coverage requirements.

The legacy literal mode retains its raw response and separately records a narrow
syntax repair when a source clause's terminal semicolon was rendered as a period.
It changes no words, IDs, spans or verdicts, and cannot repair question marks or
conditional commas. Other invalid quotation text remains rejected.

`receiving_batch.py` runs at most three fictional receivers concurrently with a
finite invocation call budget and per-question phase checkpoints. Every future
is observed. Unresolved dispatches cannot be implicitly repeated; exact-parameter
response reuse retains its original receipt and incurs no new inference call.
Generation and reviewer effort are frozen separately. The direct DeepSeek
`none` option explicitly disables thinking and omits reasoning_effort; low/high
profiles remain unchanged. The four-case non-thinking reviewer smoke failed and
is not adopted. The completed Flash low trial failed. The next candidate keeps Flash initial
narration and uses native OpenAI Codex Sol low for review and corrections.
`receiving_batch.run` freezes `generation_model`, `review_model` and
`revision_model` separately. Corrections include semantic revisions and an
initial structural repair. Native roles require an explicit native dispatcher
and low effort; the direct DeepSeek adapter cannot silently route Sol through
Nous. Changing a correction role refuses the existing checkpoint.
The expanded passage instructions keep bounded unknown/binding proof empty,
require same-claim citation membership and judge significance/relevance from
supplied evidence. They do not expose expected answers or certify semantics.

Two evidence-grounded revisions are permitted. Actual candidates, reviewers,
anchor checks, phases and known provider usage remain recorded separately.
Native tools absent from the current body restrict new actions, not access to
already supplied same-being history.

Narration/review default to the selected NVIDIA model's full reasoning; formation
and planning retain low reasoning. The
[provider API](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b-infer)
defines those modes. Narration/review use a 2,048-token reasoning budget within the 12,000-token
output ceiling, leaving space for assertion/proof JSON. Formation and planning
retain the 6,000-token ceiling. Every request records effort, budget and output limit.
For a provider that rejects an explicit reasoning budget, the deliberately
selected `--narrative-reasoning-budget none` omits that parameter. It does not
silently substitute a new budget: conditions and traces record null, and both
arms still use the same output ceiling, schema, local validators and outside
grading. Output exhaustion remains an incomplete answer. A successful HTTP/schema
response is not proof that the returned content preserved its source.
An exhausted output ceiling or null content is retained as an incomplete response
with actual known usage; it is never accepted as an answer. Resumption freezes
the semantic module and backend dependency hashes, narration effort, reasoning
budget and output ceiling. Accepted resumption also fingerprints the actual
question, binding and supplied evidence. Reused formation must match sources,
guidance, model and configuration. A changed reader needs the explicit
`--reuse-with-retrieval-upgrade` comparison flag; its before/after hashes are
recorded and copied canonical records, UIDs, revisions, history and links must
remain identical across reader initialization. This is a new receiving comparison,
not retrospective qualification of the original procedure.

The receiving checkpoint now also freezes the model/prompt procedure and records
the unfinished phase, saved response, revision number, structural-repair count
and critique messages. A timeout while reviewing a saved candidate resumes that
review instead of generating the candidate again. A durable response written
before an interruption is validated without repeating the provider call.
Structural repair and the two semantic revisions retain their bounds across
restarts; terminal rejection does not reset them. Changed context/model/procedure
and historical checkpoints without the new phase cursor are rejected while
preserving their files. Historical runs must use their frozen implementation
or start a new explicitly versioned comparison, not silently migrate results.
An unobserved provider response may still require a retry; its unknown usage is
recorded as unknown, not assumed free. This persistence fix does not improve or
certify the receiving model's semantic judgment.

Rejected terminal candidates preserve pending work. `--complete-diagnostics`
additionally archives that pending state and proceeds to later questions while
labelling the actual rejected answer `operational_status: rejected`. It never
changes a rejection into successful recall. This permits a complete diagnostic
comparison rather than stopping all measurement at the first semantic failure.
Provider/plan failures still preserve resumable work. The historical exact-evidence
answer form remains the default.

## Required independent grading

The supervising agent must inspect every assertion and every hidden requirement
outside the answer pipeline. Record source/actor errors, unsupported strengthenings,
missing essentials and verifier false positives/negatives separately. Supported
citations, populated facets, anchor presence and a model's `supported` verdict
are not acceptance criteria by themselves. Grade selection, retrieval, narrative
fidelity/coverage, original/history preservation and costs separately.

Initial runs demonstrated false review denials based on missing original tools,
a human narrator misidentified as the voice body, unobserved receipt strengthened
to non-receipt, omitted source dates/context and rejection of bounded unknowns
because there was no positive source asserting absence. Those runs remain failed
evidence. Source-role framing, facet coverage, literal anchor checks and explicit
packet-scoped unknowns address distinct defects; they do not establish final
qualification. Complete final-contract recall and three consolidation passes,
replay and dependent corrections remain necessary before stage two can close.
No live memory changes, native activation, hooks, timers or autonomous attention
follow from invoking this pilot.

The complete v7 diagnostic compared all twenty-two questions in both arms but
did not qualify natural narration. Operational acceptance and correct retrieval
did not prevent participant, chronology and outcome errors. See the
[preserved diagnostic](../research/agent-memory-2026-10-06/pilots/2026-10-07-narrative-diagnostic.md).
The [completed v8 diagnostic](../research/agent-memory-2026-10-06/pilots/2026-10-07-narrative-atomic-diagnostic.md)
adds outside review of all complete claims and individual answer requirements.
It exposes both faithful paraphrases rejected for literal differences and copied
peer speech accepted with changed autobiographical ownership. It also records
the extra generation after an unfinished-review timeout that motivated the phase
cursor. The new cursor contract is not retrospectively substituted into v8.

An explicit fictional schema capability probe on the selected NVIDIA endpoint
returned HTTP 200 and correctly escaped an embedded quotation, using 269 total
provider tokens. That establishes acceptance of that request and sample output,
not universal schema enforcement or narrative quality. The probe and its cost
are separate from formation, recall and hidden-rubric grading.

[Alternative receiving probes](../research/agent-memory-2026-10-06/pilots/receiving-model-probes/README.md)
record Ultra's temporary overload, explicit-budget incompatibility and a
schema-shaped HTTP 200 response that nevertheless lost the supplied quotation.
No receiving-quality advantage is established by those capability probes.

The [blind receiving preparation](../research/agent-memory-2026-10-06/pilots/2026-10-07-blind-receiving-preparation.md)
freezes all 44 corrected-reader packets from unqueried original formation and
replays only prior question-derived plans. Its finite file exchange prepares
fresh-context requests and preserves externally observed responses without
dispatching a model or reading a rubric in the receiving process. This enables
a controlled narrative comparison on identical actual evidence; it does not
qualify a new model's planner, provide a native dispatcher or establish recall.

The [receiving API diagnostic](../research/agent-memory-2026-10-06/pilots/2026-10-07-receiving-api-diagnostic.md)
isolates an observed Ultra provider-schema failure and supplies a finite direct
text-only dispatcher with unchanged local criteria. Its actual baseline candidate
still has narrative gaps; review timed out and its explicit retry returned 503.
Raw output, unknown costs and the saved review phase remain preserved. This is
not a complete receiving comparison or stage-two qualification.
