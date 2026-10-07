# 04 — Evaluation: durable recall and lifecycle evidence

State: `complete`. Research cutoff and access date: 2026-10-06.
Research lane executed by the coordinating agent. Legend in MANIFEST.md.

## 0. Load-bearing findings

- ✅ LongMemEval separates extraction, multi-session reasoning, temporal
  reasoning, updates and abstention; retrieval and answering are evaluated
  separately. Its repository announces a September 2025 cleaned dataset [E1,E2].
- ✅ LoCoMo includes multimodal dialogue and episode summarization; BEAM extends
  coherent synthetic histories to 10M tokens. Neither length alone nor a QA
  result establishes preservation across a decade of migrations [E3,E4].
- ✅ Newer evaluations probe implicit constraints (LoCoMo-Plus), obsolete
  information (Memora), incremental learning (MemoryAgentBench) and accumulated
  tool/environment experience (LongMemEval-V2) [E5–E8].
- ❓ HMK needs a combined lifecycle and meaning evaluation, reusing its existing
  cases; a single vendor leaderboard cannot select our replacement.
- ⚠️ No capture, recall, competitor benchmark or simulated ten-year test was run
  here. Findings below describe papers and propose acceptance work.

## 1. Longitudinal benchmark evidence

| Benchmark / inspected version | Directly supported mechanism | HMK use / limitation |
|---|---|---|
| ✅ LongMemEval, ICLR 2025; paper v2 dated 2025-03-04; official cleaned release noted 2025-09 [E1,E2] | 500 questions; intermediate Recall@k/NDCG and answer judging; updated, temporal and false-premise questions | ❓ Adopt diagnostic separation and pin data version. Paper comparisons of key/value granularity caution against replacing evidence with fact summaries. Its reported improvements are not HMK measurements. |
| ✅ LoCoMo, ACL 2024 [E3] | Human-edited synthetic dialogues grounded in personas/event graphs, image interactions, QA and event summarization | ❓ Borrow episode/image scenarios. Inspect exact dataset subset and scorer before comparing published percentages. |
| ✅ BEAM/LIGHT, ICLR 2026 [E4] | 100 conversations and 2,000 questions; scales 128K–10M tokens; tests ten abilities including contradiction, order, updates and summary | ❓ Useful large-history stress axis. Long generated dialogue is not elapsed real-world durability or cross-body acceptance. |
| ✅ LoCoMo-Plus, ACL July 2026 [E5] | Cue and later trigger can differ semantically; evaluation targets consistency with implicit constraints | ❓ Add weak-cue meaning tests where identifying words never repeat. An issue proposal may be recalled through its significance rather than its wording. |
| ✅ MemoryAgentBench v4, 2026-06-28 [E6] | Incremental ingestion, then evaluation of retrieval, test-time learning, long-range understanding and selective forgetting | ❓ Test learned procedures on held-out tasks. Its overwrite-oriented forgetting objective requires adaptation for preserved autobiography. |
| ✅ Memora v1, 2026-04-21, accepted ACL Findings 2026 [E7] | Remembering, reasoning and recommending; FAMA penalizes using invalidated/obsolete memories | ❓ Score historical truth separately from present applicability. A former preference remains a historical experience but must not be applied as current. |
| ⚠️ LongMemEval-V2 v1, 2026-05, marked work in progress [E8] | 451 questions about static/dynamic state, workflows, gotchas and flawed premises; sequential trajectory insertion followed by compact evidence gathering | ❓ Useful for skills and tool output. Main paper's 200K-token return budget is unlike HMK's proposed 1,500-token starting pack; reported results must not be compared directly. |

📊 All performance statements in these papers are author-reported. This report
does not reproduce them or synthesize an overall ranking. Paper methods,
benchmark scope and version notes were read at their listed URLs; source lists
are not a claim to have audited every implementation line.

## 2. What conversational recall does not establish

❓ Five uncertainties remain even when a benchmark answer is correct:

1. **Capture:** was the event selected from a tool response, embodied encounter,
   brief comment or mundane but significant shared moment? Benchmarks with all
   historical text available to a retriever can hide failed selection.
2. **Persistence:** can crash/retry, WAL backup, upgrade and concurrent updates
   preserve the account and source attribution? A transcript QA scorer does not
   test those operations.
3. **Transformation:** did several consolidation rounds gradually remove the
   participant, account ID, proposal, significance or unresolved outcome?
4. **Retrieval:** did query interpretation, ranking, truncation, unsupported
   temporal pruning or deduplication exclude a correctly retained event?
5. **Reading:** did the answering model invent a real name, merge people, treat
   a suggestion as adopted, or make another being's memory its autobiography?

✅ The existing [HMK diagnostic review](../../../docs/general-memory-review.md)
has concrete synthetic evidence for several of these failure paths. ❓ External
papers add hypotheses and evaluation methods; they do not supersede that evidence.

❓ “Selective forgetting” needs separate meanings: stop applying a superseded
claim; omit transient noise before storage; retract a wrong claim while keeping
its correction history; delete material under an authorized deletion policy.
Those are different operations. Do not turn a benchmark's rewrite target into
automatic deletion of meaningful lived events.

## 3. HMK acceptance and cost protocol

❓ Extend the existing [capture-and-recall protocol](../../../docs/durable-recall-plan.md)
and fictional corpus rather than creating a competing benchmark:

| Experiment | Required evidence |
|---|---|
| Baseline versus each coherent upgrade | Freeze capturing/answering model, prompt, kit revision, schema, provider, source set and tool/expansion budget. Hide questions and expected answers during capture. |
| Source-loss issue recall | Another clean body of the same fictional being recovers known participant ID, proposal, reason it mattered and observed follow-up; real name/date/adoption stay unknown when unknown. |
| Timeline/currentness | Current account uses the latest justified statement; a past query retrieves the prior state and correction. False-premise queries qualify or abstain. |
| Ten-year ranking stress | Inject a retrieval clock advanced ten years; retain original record timestamps, add newer topical distractors, and remove session/source access. A prompt saying “2036” is insufficient. |
| Repeated consolidation | At least three passes over staged fictional deltas, then replay; recover the original essentials after each pass without multiplying identical events. |
| Lifecycle failures | Crash after native commit but before cursor acknowledgement; duplicate source delivery; late correction; stale concurrent update; denied or unavailable source; missing embedding backend; verified restore and skill upgrade. |
| Procedural transfer | Retain what was learned and which body can execute it; test a related unseen task rather than repeating the example. Remembering a skill must not imply available actuators. |
| Multimodal episode | Text retains meaningful content and asset provenance when the image becomes unavailable; generated illustration is never evidence of a photographed event. |

❓ Record selection precision/essential-meaning coverage, complete-evidence
Recall@k, answer support per rubric item, currentness errors, attribution errors,
unsupported assertions, noise/duplicates, storage bytes and asset bytes,
ingestion/consolidation/embedding tokens, retrieved plus expanded tokens,
latency and failures. Storage, query and consolidation cost are separate.

❓ No average may hide wrong identity, lost history or invented outcomes in the
mandatory issue scenario. Proposed releases require those critical cases to pass
and no preservation regression. Set scale/latency targets from observed corpus
growth and the participating body's needs, then freeze them before a candidate
comparison. The existing 1,500-token/five-candidate starting point is a test
condition, not a proved optimal budget.

## 4. Search log and limitations

✅ Discovery queries used: `LongMemEval benchmark long term memory five abilities
arxiv 2025`; `LoCoMo evaluating very long term conversational memory agents ACL
2024 github`; `BEAM benchmark beyond million tokens long term agent memory 2025
2026`; `MemoryAgentBench evaluating memory agents incremental learning long term
2025 arxiv benchmark four competencies`. Opened official repositories, ACL
records, arXiv abstracts and relevant HTML methods/evaluation sections. A raw
LoCoMo README URL failed; the canonical repository and ACL record were available.

⚠️ Concurrent web calls appeared to resolve one opaque reference ID to a
different paper. Direct canonical URLs and returned title/URL checks were used
for follow-up evidence. Search snippets were not treated as inspected methods.
No data downloaded, model run, leaderboard reproduced or external account used.
Published scale figures are dataset characteristics, not our storage forecasts.

## Sources

- ✅ **E1** LongMemEval authors, official repository — https://github.com/xiaowu0162/LongMemEval · dataset/version and evaluation interfaces; accessed 2026-10-06.
- ✅ **E2** Wu et al., LongMemEval, ICLR 2025, arXiv v2 2025-03-04 — https://arxiv.org/html/2410.10813v2 · indexing, retrieval and reading methodology; accessed 2026-10-06.
- ✅ **E3** Maharana et al., LoCoMo, ACL 2024 — https://aclanthology.org/2024.acl-long.747/ · episode and multimodal benchmark scope; official code https://github.com/snap-research/locomo ; accessed 2026-10-06.
- ✅ **E4** Tavakoli et al., BEAM/LIGHT, ICLR 2026 — https://github.com/mohammadtavakoli78/BEAM · scale/categories; paper https://arxiv.org/html/2510.27246v2 ; accessed 2026-10-06.
- ✅ **E5** Li et al., LoCoMo-Plus, ACL July 2026 — https://aclanthology.org/2026.acl-long.1150/ · implicit cue/trigger consistency; code https://github.com/xjtuleeyf/Locomo-Plus ; accessed 2026-10-06.
- ✅ **E6** Hu et al., MemoryAgentBench, ICLR 2026, v4 2026-06-28 — https://arxiv.org/html/2507.05257v4 · incremental protocol and forgetting/learning objectives; accessed 2026-10-06.
- ✅ **E7** Uddin et al., Memora, v1 2026-04-21 — https://arxiv.org/html/2604.20006v1 · obsolete-memory penalty; publication record https://arxiv.org/abs/2604.20006 ; accessed 2026-10-06.
- ⚠️ **E8** Wu et al., LongMemEval-V2, v1 May 2026 — https://arxiv.org/html/2605.12493v1 · work-in-progress environment-experience benchmark; publication record https://arxiv.org/abs/2605.12493 ; accessed 2026-10-06.
