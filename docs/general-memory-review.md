# HMK as a being's primary durable-memory surface

Reviewed on 2026-10-06 against runtime source at `3d841eb`. This review covers
the kit's storage, write paths, ingestion, curation, retrieval, projections,
publication, workspace lifecycle and evaluation. It extends the
[durable-recall plan](durable-recall-plan.md); it is not a second task tracker.
The findings below preserve that baseline observation. Repair status and
regression evidence are maintained in the plan under
[issue #13](https://github.com/nicoechaniz/hermes-memory-kit/issues/13).

HMK already has a useful general-memory foundation. Episodic/semantic/procedural
retrieval and Minecraft social, place and skill shelves show that its implemented
scope extends beyond research documents. The source does not establish why its
author originally designed it. The relevant question is which present behaviors
support a being's lifelong memory and which require changes.

The main gaps are broader than selection prompts: native history is overwritten,
temporal metadata is inconsistent, ranking contains corpus-specific assumptions,
some retrieval paths lose provenance, and maintenance can lose committed data or
acquired skills. The policy added in the first delivery is useful, but cannot
repair those behaviors by itself.

## Required meaning of primary memory

A being should recognize its own relationships, projects, contributions,
experiences and learning from any authorized body without the original session.
Recall should support both “what is this to us now?” and “what happened then?”,
including unknown names, approximate dates, reported events and open outcomes.

Primary durable recall does not make HMK the authority for every artifact:

- HMK-native memories are authored in HMK.
- Matrix-signed personal memories retain their authoritative event history;
  their HMK rows remain retrieval projections.
- Independently authored Wiki files retain their source authority.
- Native sessions preserve dialogue; project repositories preserve detailed
  operational state; maintained skills preserve executable procedures.

These boundaries are already useful. Preserve them while making all relevant
authorized experience discoverable. Do not create a second authority for the
same signed memory merely to obtain native revisions or semantic search.

## Coverage and reusable capabilities

| Area inspected | Existing capability | General-memory consequence |
|---|---|---|
| `memoryctl` storage and writes | SQLite/WAL, FTS5, chapters, importance, tags, directed links, multiple embedding sets | Reuse the core; chapters can already hold compact entity, project, episode and learning accounts |
| `ingest_any`, corpus policy | Document normalization, optional OCR, file classification and credential-pattern checks | Keep as source ingestion; significant tool communications and lived experience need their own selection step |
| `librarian` and AGENTS | Explicit query/write/expand guidance, now supplemented by experience selection | Make selection visible within each body's authorized foreground workflow |
| ENGRAM migration/backfill | Episodic/semantic/procedural taxonomy and fact extraction | Useful concepts, but current metadata and extraction paths are not a general capture contract |
| Hybrid/ENGRAM/provider | Lexical and semantic retrieval, filters, quotas, optional reranking, previews | Useful tools; weak-cue, temporal, absence and attribution cases need measured acceptance |
| Workspace/bootstrap/upgrade | Explicit paths, default installation isolation, scripts/plugins refreshed with some backups | Installation identity must be separated from being identity; acquired material must survive upgrades |
| Native continuity/legacy plugin | Native-first re-entry; legacy handoff excluded from default bootstrap | Keep session resume distinct from durable life history; handoffs must not become biography |
| Matrix projection | Scoped identity, event predecessors, classification, retraction, receipts and protected mutation paths | Reuse the source boundary; preserve its provenance throughout recall rather than copying its authority into tags |
| Obsidian export | Disposable navigation with staging/manifest and source-root separation | Keep optional; this summary projection is not a full memory backup |
| Collective publication | Explicitly selected, attributed derived artifacts and revocation | Sharing knowledge remains distinct from sharing a being's whole private autobiography |
| Existing tests/benchmarks | Mechanical storage, provider, ownership, publication and projection checks; provider A/B harness | Add lifelong-memory diagnostics and capture/answer evaluation; topical hit rate alone is insufficient |

## Findings established by synthetic diagnostics

The [diagnostic runner](benchmarks/general-memory-diagnostics.py) uses only
disposable fictional databases and workspaces. It calls no model or embedding
service. Migration, native writes, lexical search, pack, backfill persistence and
upgrade run against the actual implementation. Backend outage and ENGRAM's
relevance gate use explicit substitutes to isolate those control paths. These
observations are not a successful capture or ten-year recall evaluation.

Run from a clone:

```bash
python3 docs/benchmarks/general-memory-diagnostics.py
```

| Finding | Observed behavior | Owning code / necessary change |
|---|---|---|
| Migration backup can omit committed memories | One committed chapter was in the WAL; the pre-migration `.db` copy contained zero chapters | [`migrate-engram.py`](../scripts/migrate-engram.py#L74): use SQLite's backup API and verify the snapshot; a file copy is not enough |
| Skill upgrade can erase acquired work | A custom learned skill under the shipped `memory/` category disappeared after upgrade | [`bootstrap_agent.upgrade`](../scripts/bootstrap_agent.py#L348): preserve custom skill files and pre-images; do not replace the whole category without a recovery path |
| Native title collisions can replace distinct entities | The fictional titles `李青` and `王岚` both became `item`; adding the second removed the first account and reused its local ID | [`slugify` / `upsert_book`](../scripts/memoryctl.py#L538): handle Unicode and title collisions explicitly; names and local IDs must not silently equate identities |
| Current synopsis update loses history | After changing the project account, its former text was no longer searchable | [`update_chapter`](../scripts/memoryctl.py#L2094): preserve meaningful episodes now; define native revision/supersession support where needed without altering protected-source authority |
| Episodic metadata is not maintained by normal writes | After migration, a newly added `episodes` record had `engram_type=semantic`; an imported event with unknown date received its recording timestamp as `event_ts` | [`add_text`](../scripts/memoryctl.py#L684), [`migrate-engram.py`](../scripts/migrate-engram.py#L105): support explicit kind/date metadata and keep unknown occurrence dates unknown |
| Natural questions can lose their identifying cues | Only the first eight ASCII-derived tokens were used; the question about a replay proposal omitted `HarborMesh`; `Nicolás Echániz` became fragmented tokens | [`tokenize_query`](../scripts/memoryctl.py#L1119): evaluate Unicode-aware cue extraction beyond the opening words; do not reuse this truncated representation as a whole-record duplicate test |
| Distinct episodes can be removed from a recall pack | Two different events with identical first eight title tokens produced two lexical candidates but one packed item | [`overlap_ratio`](../scripts/memoryctl.py#L1198), [`pack`](../scripts/memoryctl.py#L1510): deduplicate redundant meaning without discarding different participants/events under a common project heading |
| Document-domain preferences affect life memories | With a research prefix configured, the episode prior was `-0.10` and a matching source prior `+0.14`; an empty prefix instead awarded `+0.14` to every non-project row | [`source_domain_prior`](../scripts/memoryctl.py#L1162): remove the empty-prefix bug and make corpus preferences explicit/optional; do not silently penalize episodic recall in general use |
| Link expansion has no incoming traversal | Episode → project was visible from the episode, while expanding the project returned zero neighbors | [`linked_neighbors`](../scripts/memoryctl.py#L1277): support bounded incoming as well as outgoing navigation where recognition begins with a project/person |
| Embedding outage prevents hybrid results | Existing lexical candidates were present, but a simulated embedding outage caused `hybrid_pack` to raise instead of returning them | [`hybrid_pack`](../scripts/memoryctl.py#L1573): provide an explicit degraded lexical result and distinguish unavailable search from grounded absence |
| ENGRAM does not enforce the requested relevance threshold | Input with score `0.001` still returned a memory and `null_retrieval=false` with threshold `0.30` | [`engram_pack`](../scripts/memoryctl.py#L1713): apply a relevance gate in the appropriate score space before quota/fusion selection; quotas must not manufacture relevant recall |
| Backfilled facts can exist outside lexical retrieval | The actual backfill writer inserted one fictional extracted fact; lexical search found zero hits for its unique marker | [`backfill-semantic.py`](../scripts/backfill-semantic.py#L172): use a supported write path that maintains FTS, provenance and embedding eligibility; make repeated extraction idempotent |

These findings affect data preservation or recoverable meaning and deserve code
changes. They are not reasons to migrate a live pool during this review. The
diagnostics intentionally report current behavior; they are not yet regression
tests asserting that these issues have been fixed.

## Additional source-confirmed gaps

**Native provenance and identity.** The native schema stores titles, text, tags,
importance and storage timestamps, with book-level source path/kind. It does not
provide a general structured record for originating body, source message/action,
mode of knowing, entity identity, alias evidence, report date or supersession.
Today those facts can be retained in text and links, but reliable updating,
filtering and concurrent curation need an explicit content/API contract. Evaluate
which metadata needs structured persistence; do not assume an entity table is
required before trying compact accounts. Chapter IDs are local references, not
portable person/being identities.

**Provenance through retrieval.** `search` and `expand` attach Matrix origin, but
`pack` and `hybrid_pack` assemble smaller item dictionaries without that origin.
`semantic_search` does not expose it either. The Hermes preview renders only
shelf/type, 140 SPR characters and a local citation. Therefore a protected source's
subject, author and classification are not consistently available in the compact
recall surface. Retain origin in machine results and show enough attribution for
the answering body; expand when necessary. Do not make signed statements
embedding-eligible by bypassing their projection policy.

**Capture and embedding freshness.** The shipped provider exposes write tools,
but does not implement turn synchronization or extraction at compression/session
end. Its add/update tools do not refresh embeddings; `update` correctly removes
stale vectors and requires an explicit refresh afterward. General-memory capture
needs an observable “selected → persisted → retrieval-ready” outcome under the
body's authorized workflow, including tool communications and embodied inputs.
This does not authorize new hooks, autonomous inbox access or Codex prefetch.

**Chronology and currentness.** ENGRAM's date columns are optional and its common
retrieval APIs do not offer event/report-date ranges or entity-centered timelines.
Ranking recency uses the last storage update with a 30-day decay, not the event
date. A synopsis edited today can outrank an old event without becoming evidence
of that event's occurrence date. Retain explicit date kinds and assess historical
queries separately from current-state questions; semantic rank is not chronology.

**Compression and modality.** SPR uses the first eight nonempty lines; plain
lines are cut to 140 characters. Embedding input includes only the first 5,000
raw characters. The core is text-oriented; document ingestion is not a general
audio/image/sensor episode pipeline. Embodied experiences can already be stored
as attributed textual accounts with selected evidence pointers. Preserve the
needed meaning early in the text, then measure whether richer summaries or
chunking are necessary. A pointer to unavailable media is not a sufficient memory.

**Navigation.** Links carry notes and custom relation types in SQLite, but the
Obsidian renderer names only six link types and classifies general library
records mainly as concepts. A person/project account is not given dedicated
navigation, and proposed relations such as `concerns` are not fully rendered.
This is an optional navigation limitation, not a reason to replace the canon with
the exported vault: exported notes contain summaries and a raw DB reference,
not the full durable account.

**Lifecycle and scale.** SQLite supports concurrent local access, but native
updates have no expected-version check; serialization alone does not resolve
two bodies editing an old synopsis. Sharing a local being-level pool and
synchronizing offline copies across machines are different problems. The latter
needs a receiving protocol in the runtime/portability layer, not a raw SQLite-file
merge. Semantic search loads all matching stored vectors/records before its
prefilter; ENGRAM performs separate bucket searches and query logs accumulate
without a retention policy here. Measure realistic corpus growth and query cost
before selecting a new vector store or deleting any durable memories.

**Recovery and configuration.** Our deployed being can have verified rolling and
portable backups outside this kit; that does not make the kit's migration copy
safe or demonstrate recovery for every installation. Define and test the required
snapshot/restore/retrieval checks as a deployment contract. Provider defaults also
drift: `memoryctl` defaults to local/BGE-M3, environment templates select NVIDIA,
and provider documentation describes three providers while code also supports
Model2Vec. Reconcile documented versus effective configuration without silently
changing anyone's selected provider or model.

## Responsibility boundaries

| HMK should own | Runtime / portability should own | Body and maintained skills should own |
|---|---|---|
| Safe native persistence, revision/update semantics, metadata APIs, indexes, bounded retrieval and provenance-bearing results | Signed being membership, authorized memory binding, source capabilities, cross-host receiving/synchronization and access policy | Selection during authorized foreground activity, sensor/tool interpretation, executable procedures and harness-specific integration |
| Consistent backup/migration primitives and diagnostic observability | Deployment backup scheduling and portable custody, when authorized | Distinguishing remembered knowledge from tools actually available in this body |

Default installation isolation remains valuable between distinct beings. Multiple
bodies of one being may use an explicitly authorized existing pool. A workspace,
model, harness or copied SOUL is not proof of membership. HMK should document that
deployment option without minting identities or opening another being's memory.

## Changes to the existing plan

Add preservation fixes ahead of the capture pilot: WAL-consistent migration
backup, acquired-skill preservation and explicit collision handling. Turn the
relevant diagnostics into regression tests when fixing each behavior.

Then address the native write/recall contract: kind and date semantics, source/body
attribution, history-safe current accounts, indexed/idempotent extraction,
relevance-gated retrieval, degraded lexical search, Unicode cues and bounded
bidirectional links. Preserve supported research workflows as optional corpus
behavior rather than a universal bias.

Use the existing selection cases to evaluate capture and answers, adding cases
for update preservation, imported unknown dates, significant identifiers late in
queries, same-project distinct episodes, embedding outages, upgrades and
multi-writer updates. Add age/distractor/scale perturbations to those scenarios;
avoid another competing corpus. Publish each coherent fix and its evidence as it
lands, before deployment or the full ten-year pilot is complete.

Live receiving acceptance and the model capture/recall pilot remain untested.
This review establishes source-supported gaps and specific synthetic behavior,
not the necessity of a wholesale database rewrite or a completed memory upgrade.
