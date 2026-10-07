# Stage 1 repair delivery — 2026-10-07

The incomplete [original pilot](2026-10-07-model-pilot.md) identified three
concrete failures. This delivery repairs their mechanisms; a new formation and
recall run must still qualify the changed guidance and retrieval together.

- Hybrid relevance now retains independent token-overlap evidence when the
  embedding is weak. This floor excludes recency, importance and relative FTS
  rank, retains the configured threshold and research prior, and does not pad
  the pack. Reranking still uses its absolute scores when explicitly enabled.
- Selection explicitly preserves a meaningful unsuccessful action with its
  observed failure and unresolved outcome. Routine retries remain noise.
- Recall plans are validated in full before follow-up retrieval: bounded query
  arrays, typed expansion IDs and pack membership. One structural repair is
  allowed without factual hints or rubrics. An unresolved failure retains its
  question, initial pack and rejected plans for foreground resumption.

The runner checkpoints every model attempt before parsing its content, includes
failed requests with unknown usage, separates capture/recall/indexing traces,
and measures actual pack estimates rather than the formerly incorrect zero-cost
field. Provider billing and embedding token usage are not available through
this client and will not be guessed. Formation conditions and retrieval source
hashes are frozen for resumption. A fresh receiving SQLite snapshot excludes
capture ledger tables; recall receives only bounded packs and expansions.
Consolidation requires an explicit `--consolidate` flag and belongs to stage 2.

The earlier proposed guide's example duplicated the issue fixture's participant
and proposal. That contamination is recorded here; the new guide uses an
independent fictional example. Earlier evidence stays available and is not
relabelled as a blind completed comparison. The new run changes guidance and
retrieval from that partial run; its baseline and proposed variants share the
same new retrieval, models, fixture order, aged clock, distractors and limits.

Verification: 204 pytest tests pass; bootstrap/upgrade smoke passes. Regression
checks cover age without timestamp edits, weak embeddings, unrelated null recall,
pack thresholds/budgets, invalid plans and resumption preserving completed
capture and the pending question, and cost persistence for rejected model JSON.
These mechanical checks are not a completed model-quality result.

## Observed correction after the first new run

The first new run recovered the old lexical encounter, but proposed selection
still omitted the failed invitation and falsely attributed that omission to the
guide. Its pending recall plans also selected IDs from supplied neighbor hints;
the validator had unnecessarily restricted them to primary rows. Both stopped
questions and all completed captures remain preserved, not reset in place.

The correction places a significance-before-success decision check at the end
of the guide and admits only IDs actually visible in primary rows or supplied
one-hop hints. Arbitrary and deeper unseen IDs remain refused. The answer
contract requests enough identifying meaning for recognition, applied equally
to both arms without case-specific facts. A new main run is required; changing
an answer prompt is not a comparable continuation of earlier answers. A separate
predeclared fictional chart-handover case and 100 repeated transport lines check
generalization and noise selection, not just the invitation wording.
