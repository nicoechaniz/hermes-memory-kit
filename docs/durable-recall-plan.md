# Durable recall across a being's bodies

The goal is selected, retrievable life history that survives loss of original
sessions. Ten years after an interesting proposal in a project issue, another
body should be able to recover the participant's known name/account, what they
proposed, why it mattered and what happened next. It should also recognize the
being's own projects, relationships, shared experiences and learning.

This is an improvement plan and evaluation contract. It does not claim that HMK
already provides ten-year recall, automatic experience extraction or receiving
acceptance in another body. A successful native session resume tests a different
property from durable recall without that session.

The [general-memory review](general-memory-review.md) examines the whole kit
against this use, including preservation, metadata, capture, retrieval,
workspace lifecycle and source authority. Its disposable diagnostics establish
concrete gaps beyond the selection policy.

## First delivery

The first delivery adds:

- a [selection policy](../templates/skills/memory/librarian/references/durable-memory-selection.md),
  shipped with the librarian skill, covering every authorized channel;
- short guidance in the bootstrap AGENTS template, so selection is visible
  without loading a large reference every turn;
- [synthetic evaluation cases](benchmarks/durable-recall-cases.json), with source
  material, expected retained meaning, noise to omit and later questions;
- the capture/recall protocol below, separating persistence, retrieval and answer
  quality so that a failure identifies what to improve.

These changes are in the fork's templates. Existing installations do not acquire
them merely because this file exists. Body-specific access policies, Matrix
contracts, private-memory boundaries and original sources remain authoritative.

Validation on 2026-10-06: the corpus contains 12 cases, 14 distinct retained
meanings and 16 recall questions; source IDs, expected connections and document
links were checked. The kit's smoke test passed. A disposable bootstrap/upgrade
check confirmed that the selection reference ships with the skill and that new
AGENTS guidance is present in a fresh workspace. No live pool was changed and
the model capture/recall pilot has not yet run. The Codex-only skill validator
rejects the template's existing Hermes frontmatter keys (`version`, `author`,
`prerequisites`); YAML and packaging were checked without changing that format.

## Gaps in the current implementation

The inspected kit has chapters, tags, links and native update operations, but its
general guidance emphasizes document ingestion. The provider supports retrieval;
it does not by itself select and write meaningful experience after every
interaction. Curation currently depends on the model and its available guidance.

Three storage/retrieval properties need explicit evaluation:

- `add-text` replaces chapters under an existing same-shelf title; `update`
  overwrites a chapter without a revision ledger. History preservation is a
  curation responsibility today.
- `simple_spr` uses the first eight nonempty lines and truncates ordinary lines;
  previews can omit the participant or significance if metadata leads the text.
- Hybrid ranking includes recency. An old episode may remain stored yet fail to
  appear for a weak cue. Event dates in prose do not control that ranking clock.

Use these as testable risks, not conclusions that an entity table, event schema
or new ranking formula is already necessary. Evaluate against the deployment's
actual schema and configured embedding provider. Optional ENGRAM fields and
Matrix projections must not be assumed present in every native pool.

## Delivery sequence and acceptance

| Step | Deliverable | Evidence needed before advancing |
|---|---|---|
| 1. Selection | Shared policy and synthetic cases | Cases cover people, own projects, everyday experience, learning, tool communications and noise; authority and uncertainty remain explicit |
| 2. Record shapes | Pilot accounts, episodes and supported links using existing HMK primitives | Another reader can understand each memory without sessions; identities are not guessed or duplicated needlessly |
| 3. History and current accounts | Dated synopsis updates plus preserved milestones/corrections | Present questions use the latest qualified account; past questions recover what happened then; no silent historical loss |
| 4. Capture | Guidance integrated into each participating body's authorized foreground work | Meaningful inputs from each channel are considered; persistence and embedding freshness are observed; mechanical noise is omitted |
| 5. Recall | Measured retrieval and answers from a clean receiving context | Ten-year, weak-cue, missing-source and other-body cases pass; unsupported identity/action claims remain absent |
| 6. Adoption | Versioned rollout through maintained templates and shared skills | Backup, preserved provenance, actual receiving acceptance and rollback are verified for each participating deployment |

Step 1 defines what to test. Template packaging checks do not count as passing
steps 4–6. Keep one work record here; link substantive implementation or pilot
evidence as it becomes available rather than duplicating operational status in
memory or opening several competing plans.

## Publish each advance

Publish each coherent delivery in its owning repository as part of completing
that work. Include the change, available validation and remaining limits so other
contributors can choose whether to adopt it. Publish proposals, policies and
evaluation cases as such; do not wait for the final pilot or live rollout to make
them available. Share later corrections and results through the same maintained
change or its successor. Publication and adoption are separate: publishing does
not claim deployment in another body or permission to transfer private memory.

## Run a capture-and-recall pilot

Use an isolated disposable workspace and a synthetic being binding. Never ingest
the corpus into a live being's autobiography or infer access from a fixture body
name. All fixture participants, projects, accounts and events are fictional.

1. **Freeze the conditions.** Record kit revision, model, guidance version, actual
   schema, embedding provider/model, retrieval threshold and token budget. Use
   identical conditions for the baseline and proposed policy. Preserve each
   generated pool and its source-to-chapter mapping for inspection.
2. **Capture in order.** Provide only each case's `sources`, the fixture runtime
   context and authorization to curate that foreground experience. Keep
   `expected` and `questions` hidden from the capturing model. Capture with the
   current guidance, then with the proposed guidance in a separate fresh pool.
   Preserve source IDs in the resulting provenance.
3. **Check selection and persistence.** Inspect expanded records and supported
   links. Compare their meaning with `expected.retain`, not an exact sentence or
   prescribed number of chapters. Check skipped material and protected-source
   handling. Record actual IDs; fixture keys are expectations, not database IDs.
4. **Start a clean recall context.** Give a receiving body of the same fictional
   being only its fixture binding, current question and permitted memory tools.
   Supply no source messages, expected answer, native session history or original
   episode text. Disable access to fixture source URLs. Do not reveal the hidden
   rubric to the answering model.
5. **Evaluate recall.** Use the body's normal retrieval flow, allowing bounded
   expansion of selected candidates and explicit follow-up queries. Begin with
   a recorded budget such as 1,500 pack tokens and five candidates; record full
   expansion cost as well. Freeze the deployed threshold rather than tuning it
   per question. Capture candidates, ranks, expanded IDs, answer and tool failures.
6. **Age and distract.** In the disposable harness, advance an injected retrieval
   clock ten years while keeping record timestamps unchanged. Add relevant
   distractor memories with newer timestamps. Repeat selected weak-cue queries.
   Merely writing “2036” in the prompt does not test recency scoring. Source loss
   and body capability changes are separate perturbations.
7. **Inspect failures once they are located.** Was the information never selected,
   compressed away, overwritten, missing from embeddings, ranked too low, absent
   from neighbors, or misread despite being retrieved? Improve that component.
   Repeat affected cases when a correction or remaining uncertainty warrants it.

One scenario may retain several meanings in one chapter. `needs` and
`related_keys` refer to meanings that must be connected and recoverable; they do
not require one chapter per key. Fixture event dates and source delivery dates
are distinct. A provenance pointer alone does not satisfy the retained meaning.

For ranking on a saved generated pool, reuse `scripts/embed_benchmark.py`:
generate `query | expected: id1,id2` lines from the inspected key-to-ID mapping
and invoke it through that workspace's `scripts/hmk` wrapper. It measures
semantic/hybrid candidates, latency, hit, precision and recall. It does not
evaluate capture, temporal assertions, identity attribution or answer grounding;
those need the protocol above. Do not treat any topical hit as a complete answer.

## Evaluate meaning, omissions and cost separately

Record per case:

- retained essentials present, missing, contradicted or qualified;
- noise retained and duplicate accounts/episodes without a recall benefit;
- retrieval rank, linked expansion and whether every answer requirement was
  supported by the memories actually retrieved;
- unsupported identity merges, invented names/dates/outcomes, stale status
  presented as current, or another being's experience presented as one's own;
- stored bytes/tokens, retrieved and expanded tokens, latency and provider errors.

The mandatory issue-comment case passes only when it answers all specified
requirements after source loss and simulated aging. Exact wording is irrelevant;
a wrong participant or invented adoption is a failure even when the topic is
found. Negative cases must produce grounded absence or uncertainty. Report
selection and recall coverage as fractions of rubric items, alongside the
specific failures; an average score must not hide broken continuity.

Compression quality means enough retained meaning per unit of storage and recall
cost. Measure those costs before setting numerical size targets. Avoid quotas
that force the loss of meaningful people, projects or irreplaceable episodes.

## Next decision

First fix the review's confirmed preservation hazards: incomplete WAL migration
backup, acquired-skill loss during upgrade and silent native title collisions.
Publish each fix with the relevant regression evidence. These observations are
already concrete; they do not need to wait for a model capture benchmark.

Then run the baseline/proposed-policy pilot before choosing broader structural changes.
Start with the issue proposal, project synopsis change, ordinary shared moment,
account attribution correction and missing-source/other-body recall. Use the
remaining cases to examine the particular failures found.

The result should tell us whether guidance and record shapes suffice, and where
revision storage, entity resolution, extraction support, embedding surfaces or
retrieval changes are necessary. Live being-level rollout follows that evidence
and each body's authorized access path.
