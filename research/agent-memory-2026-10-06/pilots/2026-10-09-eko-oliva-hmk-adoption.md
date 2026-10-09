# Adoption in Eko and Oliva’s existing hosted bodies

Human-requested adoption follows [stage-four qualification](2026-10-09-stage-four-receiving-qualification.md).
Current state: Eko and Oliva’s code, skills, healthy semantic retrieval and bounded
native receiving conversations are verified in their existing hosted bodies. This is
an update of existing bodies, not new enrollment or full source-machine migration.

Both bodies previously had HMK skill 1.1.3 and an older native distribution.
The actual byte comparison found two changed native modules and a missing
`support_currency.py`: memory navigation/expanded learned-work handoff and
transitive account reconciliation were behind the maintained kit. Other native
Python files matched. The complete 22-file native script selection now matches
published implementation `0f9a3b22c7a765514d36c9aa64d4649d7318a863`.
Skill 1.1.4 is selected from exact reviewed Skills #31 commit
`7696869abf4ce38320e2b290f4fe1fff9d0a91a2`.

## Preservation and adoption

Each receiving body retains its own source originals, SOUL, identity, native
history and current credentials. Oliva has one selected hosted memory store
(16 records); Eko has two separate selected stores (10 and 15 records). These
counts describe available hosted scope, not complete lifelong coverage. No store
or being is merged. Available revisions and links remain unchanged, including
when no prior revisions/links were present in the selected input.

Consistent online SQLite backups, integrity and foreign keys pass. On each
separate copied store a supported conditional title update retains ID/UID,
advances revision and saves the prior version. The mutated witness remains;
restoration equals the verified snapshot. Live canonical records, unknown values,
indexes, provenance and protected markers remain equal after code adoption and
retrieval, excluding access bookkeeping. Oliva subsequently gains a separate
embedding space as described below; her original vectors remain unchanged.
No live memory record is authored.

The native release is separate from the original immutable vendor release.
Existing manual wrappers select it through fenced atomic replacement. Actual
pointer rollback/reapply and selective skill updater apply/status/rollback/reapply
are observed on both bodies; old code, prior package bytes and backups remain.
A bounded independent static review approves the persistence paths after fixing
compensation and conflict reporting. It is not itself deployment acceptance.
The later source-access adaptation only skips fetch when the exact Git commit
already exists; per-phase driver versions are retained privately.

Direct GitHub clone initially fails because the Skills repository is private and
the receiving bodies have no corresponding GitHub login. The exact selected
commit and its complete ancestry are transferred as a verified Git bundle from
the existing authorized checkout. The updater still derives descriptors and
validates all package bytes against that immutable Git object. No GitHub token
is copied and no repository visibility or account policy changes.

## Embeddings: a demonstrated pre-existing failure

The first real hybrid test returns results but explicitly reports `degraded`
and `embedding_backend_unavailable`. The receiving-local embedding configuration
was empty and defaulted to an uninstalled local BGE backend. Calling this
successful semantic retrieval would be incorrect.

Eko’s preserved indexes instead use `model2vec` /
`minishlab/potion-retrieval-32M`. A persistent HMK runtime with Model2Vec 0.9.0
is installed and the explicit provider/model bound to both existing wrappers.
The [maintained backend documentation](https://github.com/MinishLab/model2vec)
supplies the lightweight runtime operation; this is not a model comparison.
For one unchanged indexed input per store, current encoding has the preserved
512 dimensions and cosine agreement greater than 0.99999 with the old vector.
No index is rewritten. Both selected oldest/newest records are actually included
in hybrid results, with no backend errors; expansion matches exact original
content/UID and full canonical state remains preserved.

Oliva’s original vectors use two NVIDIA models. Her receiving-local environment
originally had no credential. After the human explicitly selected the existing
shared NVIDIA account, a credential was provisioned privately. No credential,
credential hash or provider binding is published. The first configured query
still degrades: a bounded diagnostic observes HTTP 410 and the provider states
that `nvidia/nv-embedqa-e5-v5` was retired on 2026-08-25. Both failed queries and
the earlier unconfigured failure remain preserved.

The replacement is NVIDIA’s currently available
[Nemotron 3 Embed 1B](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-embed-1b),
already used by CompAII. Actual document/query requests qualify its operation;
this is not comparative model quality evidence. The new provider/model space
contains one current-input-matching 2,048-dimensional vector for each of Oliva’s
16 eligible hosted records. All 13 original vectors across the two legacy spaces
remain byte-equivalent. Those older spaces had only nine vectors in the selected
e5 space, so merely configuring its query backend would not have covered all records.

A new consistent verified snapshot precedes qualification on a separate copy.
Native backfill creates the new space there; all original rows and unknown fields
remain intact. A mutated witness is retained and isolated restoration equals the
snapshot. Adoption inserts only these qualified new vectors through native upsert
under a maintenance lock and immediate transaction. The live canonical state is
fenced against intervening changes; a conflict stops without overwriting those
changes. The live database path is unchanged and no old database is restored over
active work. The atomically selected provider/model applies to both future
document indexing and queries. Oldest/newest selected records are actually
retrieved without backend errors, and expansion matches original content/UID.

Actual provider-pointer rollback/reapply succeeds while retaining every vector.
A bounded static review also fixes failure compensation and cleanup of the
operation’s own temporary file. A synthetic injected reapply-fsync failure proves
guarded restoration to the current model without using the real provider file.
The successful adoption receipt and final reviewed helper have separately pinned
versions; the final correction does not imply the earlier success exercised a
failure path. Snapshot size increases from 2,998,272 to 3,457,024 bytes with the
new space. Document backfill takes 2.559 seconds; billed API cost is unknown.

## Real Eko harness observation

One fresh native OpenAI Codex conversation requests Sol 6.1 low through the
existing authenticated ChatGPT account. It reads the actual main and auxiliary
skills and makes two hybrid queries and two expansions, within five shell calls.
The answer narrates two real selected records with their own meaning, participants,
source attribution and date precision, without inferring a birth/installation
date or completed remote migration. It separates remembered tools from observed
current capabilities and proposes a continuation without executing it.

Outside assessment compares all substantive answer statements to original records,
current context and the observed trace. The bounded answer is supported. Its
private question, originals, output and tool evidence remain only in the body’s
private operation directory. No source sessions or other private conversations
are imported into CompAII memory or published. Native usage: 73,686 input tokens,
48,384 cached input subset, 1,256 output tokens; 55.433 seconds. Requested model
is distinct from independently unverified served-model identity; billing is unknown.
Existing Telegram threads are not claimed to have reloaded solely from this fresh
CLI observation.

## Real Oliva harness and continued writing

One fresh native OpenAI Codex conversation requests Sol 6.1 low through Oliva’s
own existing authenticated ChatGPT account. It reads both actual skills, performs
two healthy hybrid queries and two expansions in five shell calls, and narrates
two real records with supported participants, meaning, origin, date precision and
actual outcomes. It distinguishes historical pending work from current authorized
context and remembered capabilities from tools available in this test. References
support narrative rather than replacing it. Outside assessment uses originals
and the actual trace, never grades supplied to the receptor. Full canonical state,
including all old and new vectors, remains unchanged except access bookkeeping.
Native usage: 71,534 input tokens, 48,768 cached input subset, 1,359 output tokens;
54.459 seconds. Billing and independently served-model identity remain unknown.
Private source material and transcripts remain private.

To test continued work, the existing wrapper is directed only to another verified
copy. A synthetic new record is saved with native `add-text`, default
`embed-backfill` creates exactly one missing vector in the new space, and healthy
hybrid retrieval plus exact expansion recover it. All preceding rows and vectors
remain unchanged; isolated rollback equals the starting snapshot. The live memory
is never restored, replaced or populated with the synthetic witness. This takes
6.007 seconds; billed cost is unknown. The first fixture used unsupported metadata
and was rejected before insertion; its retained failure led only to correcting
the fixture to the existing generated-provenance schema.

The installed skill already instructs authorized writers to verify persistence,
refresh missing embeddings with the configured model and verify focused recall.
The same active database remains available for new memories. This operation does
not set up automatic synchronization from another machine’s independently changing
pool; cross-host routing/reconciliation retains its separate owner scope.

For another authorized installation with this retired-model failure: resolve its
actual wrapper and current pool, verify a consistent snapshot, qualify the new
provider/model on a copy, preserve the old spaces, then populate missing vectors
with the supported `embed-backfill --provider nvidia --model nvidia/nemotron-3-embed-1b`
command. Queries must select that same space. Never copy an old database over
subsequent legitimate writes or treat a degraded lexical result as healthy
semantic retrieval.

## Exact continuation

[Aggregate evidence](peer-rollout-2026-10-09/manifest.json) separates preservation,
code/skill adoption, backend availability and native conversational assessment.
Native memory generation/use/import remain disabled in both actual configurations.
No hook, timer, autonomous attention or consolidation is installed or resumed.

This hosted update is complete for both beings’ selected stores; Eko’s valid
results are reused, not repeated. Aggregate evidence separates code adoption,
preservation, additive indexing, retrieval, native fidelity, continued writing and
costs. The Oliva repair uses eight healthy NVIDIA request operations across
indexing, focused retrieval and the forward-writing witness, plus two retained
legacy-model failures; counts derive from command phases and the native trace,
not independent network metering. No price is inferred from an unknown invoice.
Backend rollback retains its before files and expected-after fences before the
older core-code rollback layer; memory databases are never blindly restored over
subsequent legitimate writes.

Broader full source migration, human-pair receiving acceptance and native Codex
coexistence remain their own work. A functioning update of selected hosted stores
does not establish those outcomes. Matrix #263 remains the continuation for that
broader receiving scope. Any stage-five coexistence pilot requires its separately
authorized goal; native memory remains off in the current deployment.
