# Native-first manual re-entry

`continuityctl.py rehydrate` is a deprecated compatibility entry point that now
returns native Hermes session/goal guidance and `continuity.restored: false`.
It does not select a session, read shared handoffs, read native MEMORY.md/USER.md,
import memoryctl, open a database, or call a provider. Legacy retrieval flags are
accepted as no-ops with a deprecation notice. Engineering `show`/`update` remain.

Use Hermes `/resume` for the intended conversation, explicit `session_search`
for historical context, and `/goal` for the active mission. The latest human
direction wins over historical summaries. A new session is not permission to
inherit the most recent same-platform conversation.

HMK remains durable curated memory: use memoryctl for explicit recall. Native
session history is distinct from native MEMORY.md/USER.md stores and does not
require enabling those stores. This change does not alter HMK retrieval,
embedding configuration, library schemas, or automatic hooks.

This focused change does not disable or migrate an installed dialogue plugin,
change bootstrap defaults, or erase historical files. Those remain separate
operator decisions. Consumers of the retired identity/state/handoff JSON fields
must use native history or explicit durable retrieval instead. Empty
meta_context/exact_memories and null query/retrieval fields preserve a bounded
compatibility response, not a recovered conversation.

Tests run offline: `python -m pytest tests/ -q`. The two new regressions make
legacy paths directories (any accidental read fails) and exercise guidance
without HMK roots. They prove reader isolation, not model-level efficiency.
