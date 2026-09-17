# AGENTS.md

## Scope

This workspace uses Hermes Memory Kit as its durable memory layer.

## Memory Discipline

- HMK-native memory lives canonically in `agent-memory/library.db`
- use `./scripts/hmk memoryctl.py hybrid-pack` for durable retrieval
- use `./scripts/hmk ingest_any.py` to normalize heterogeneous sources before storage
- use the workspace `wiki/` only as an HMK-generated projection
- never point that projection at the authoritative LLM Wiki (`$WIKI_PATH`)
- LLM Wiki files are authoritative for their raw evidence and curated notes;
  their HMK chapters are rebuildable retrieval indexes
- accept `null_retrieval` instead of padding weak context

## Curation Discipline

- classify new documentation as HMK-native or LLM Wiki-authored first
- then retrieve related context
- then inspect the appropriate navigation surface if conceptual orientation is needed
- then decide whether to keep as evidence, link, distill, or project

## Token Discipline

- no periodic loops by default
- no background polling unless explicitly requested
- prefer bounded retrieval bundles over raw dumps

## Re-entry priorities

Use native Hermes session history and goal state for the matching conversation.
The latest human direction controls continuation; historical summaries do not
revive cancelled work. Retrieve HMK or the project cockpit when needed, but do
not infer current dialogue from engineering-state files or global handoffs.

`./scripts/hmk continuityctl.py rehydrate` provides an optional native-first
orientation result, not a recovered conversation or a mandatory startup ritual.
Keep retrieval metadata out of ordinary conversation unless relevant to the
user's request.
