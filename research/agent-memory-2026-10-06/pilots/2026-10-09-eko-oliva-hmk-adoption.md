# Adoption in Eko and Oliva’s existing hosted bodies

Human-requested adoption follows [stage-four qualification](2026-10-09-stage-four-receiving-qualification.md).
Current state: Eko is verified; Oliva’s code and skill are adopted, with semantic
backend configuration pending the human’s choice of embedding account. This is
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
retrieval, excluding access bookkeeping. No live memory record is authored.

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

Oliva’s original vectors use two NVIDIA models. Her hosted embedding environment
has no credential. The human has been asked whether to bind the existing shared
NVIDIA account or Ani’s account. No service credential is copied pending that
choice, no local substitute is installed and no existing vector is discarded.
Her earlier degraded query is preserved. Healthy semantic retrieval and native
receiving acceptance for this rollout remain pending, not passed.

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

## Exact continuation

[Aggregate evidence](peer-rollout-2026-10-09/manifest.json) separates preservation,
code/skill adoption, backend availability and native conversational assessment.
Native memory generation/use/import remain disabled in both actual configurations.
No hook, timer, autonomous attention or consolidation is installed or resumed.

Next: after the human selects Oliva’s NVIDIA account, provision only her
receiving-local backend, verify a preserved compatible embedding space and healthy
old/new hybrid retrieval, then run one bounded fresh native conversation and
update this report with actual receipts. Preserve Eko’s valid results; do not
repeat them. Restoring a backend uses its retained before files and expected-after
fences before the older core-code rollback layer; memory databases are not
blindly restored over subsequent legitimate writes.

Broader full source migration, human-pair receiving acceptance and native Codex
coexistence remain their own work. A functioning update of selected hosted stores
does not establish those outcomes.
