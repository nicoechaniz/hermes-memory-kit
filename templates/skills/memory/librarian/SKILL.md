---
name: librarian
description: Query and curate the local HMK library, distinguishing HMK-native authority from LLM Wiki records that HMK indexes for retrieval.
version: 2.0.0
author: Local System
license: MIT
metadata:
  hermes:
    tags: [Memory, Librarian, Retrieval, SQLite, FTS5, Local]
    related_skills: [codebase-inspection]
prerequisites:
  commands: [python3]
---

# Librarian

Use the local memory controller instead of bloating the live prompt with raw notes.

## Invocation idiom (v3 — workspace-relative)

All commands run from the **agent workspace root** (`$HMK_WORKSPACE_ROOT`, typically `~/agents/<agent-name>/`) using the `./scripts/hmk` wrapper. The wrapper cd's to the workspace, loads the agent's `.env`, and absolutizes `HMK_*` paths, so scripts never rely on hardcoded user-specific paths. Never call the underlying `.py` files directly with absolute paths — use `./scripts/hmk` always.

Paths referenced below (e.g. `agent-memory/state/NOW.md`, `wiki/index.md`) are **relative to the workspace root**. They resolve correctly for any agent bootstrapped from `hermes-memory-kit`, not just `hermes-prime`.

## When to Use

- User asks what we were previously working on
- You need legacy project roadmap or architecture context
- You need current memory-system status or design rationale
- You want to register a durable fact or document
- You need to expand one stored item without loading everything

## Rules

- Prefer `hybrid-pack` before `expand`
- Accept `null_retrieval` when returned; do not pad with weak matches
- Never write to `$HERMES_HOME/SOUL.md` through memory maintenance flows
- Do not treat `MEMORY.md` as the hot write path
- Use `expand` only for items already selected as relevant
- Treat the workspace `wiki/` as a disposable HMK projection.
- Treat `$WIKI_PATH` as a separate, authoritative LLM Wiki for its raw and
  curated files. HMK copies of those files are retrieval indexes.
- For HMK-native records and precise continuity, use `library.db`.

## Core Commands

### 1. Query a compact bundle

```bash
./scripts/hmk memoryctl.py hybrid-pack --query "USER_QUESTION" --budget 1800 --limit 4 --threshold 0.4
```

Use `--threshold 0.4` as the current pragmatic default. Raise it only when retrieval is noisy.
Fallback to plain `pack` only if the embeddings layer is unavailable or you explicitly want a lexical baseline.

### 2. Inspect raw ranked candidates

```bash
./scripts/hmk memoryctl.py search --query "USER_QUESTION" --limit 6
```

Use this when ranking looks suspicious and you need to inspect why.

### 3. Expand a stored item

```bash
./scripts/hmk memoryctl.py expand --id 17
```

This returns the full raw content plus linked neighbors.

### 4. Add a durable text memory

```bash
./scripts/hmk memoryctl.py add-text \
  --shelf episodes \
  --title "short-title" \
  --raw "durable fact or decision text" \
  --tags memory,decision \
  --importance 0.8
```

### 5. Add a file into the library

```bash
./scripts/hmk memoryctl.py add-file \
  --shelf plans \
  --path /path/to/file.md \
  --title "descriptive-title" \
  --tags plan,architecture \
  --importance 0.9
```

### 6. Check library stats

```bash
./scripts/hmk memoryctl.py stats
```

### 6b. Inspect embedding backend configuration

```bash
./scripts/hmk memoryctl.py embed-config
```

Use this when retrieval quality, provider selection, or portability of the memory stack is relevant.
Current architecture supports:
- `nvidia` as the active default
- `google` (`gemini-embedding-001`) when a Gemini/Google API key is present
- `local` as an optional backend for a compatible sentence-transformers stack

### 7. Ingest heterogeneous sources via the modular stack

```bash
./scripts/hmk ingest_any.py \
  --source /path/to/file.pdf \
  --shelf evidence \
  --title "descriptive-title" \
  --tags pdf,source \
  --importance 0.7
```

Use this for PDF, DOCX, HTML, URLs, or any source that should be normalized to markdown before entering `library.db`.

Current modular stack:
- `pdftotext` for PDF
- `trafilatura` for URLs and HTML
- `pandoc` for broad document conversion
- `mammoth` as DOCX fallback

### 8. Inspect the generated HMK projection layer

```bash
sed -n '1,200p' wiki/index.md
sed -n '1,200p' wiki/maps/project-memory-system.md
```

Use this only for navigation over HMK-native records. Do not confuse it with
the independently authored LLM Wiki at `$WIKI_PATH`.

### 9. Native session re-entry, separate from durable retrieval

Use Hermes `/resume` for the intended session, `session_search` for explicitly
selected history, and native `/goal` for the active mission. Native SQLite
session/goal persistence is distinct from the optional MEMORY.md/USER.md stores.
The kit defaults to HMK for durable memory with those native stores disabled.

`continuityctl.py rehydrate` is deprecated: it returns native re-entry guidance,
not recovered context, and reads no files or databases. Old retrieval/summary
flags are accepted but ignored. Use `memoryctl hybrid-pack`, `expand`, or the
`librarian` tool for explicit durable recall. `continuityctl show` and `update`
remain available for operator-maintained engineering notes only.

## Memory Topology (workspace-relative)

- `agent-memory/library.db`: curated durable HMK memory
- `agent-memory/state/NOW.md`, `ACTIVE-CONTEXT.md`: optional engineering notes
- `agent-memory/index/INDEX.md`, `plans/MEMORY-ARCHITECTURE.md`: navigation
- `hermes-home/state.db`: native sessions and goal state, managed by Hermes
- `wiki/`: generated HMK navigation, not the independently authored LLM Wiki

These are bootstrap defaults. Follow the actual deployment paths and preserve
`HMK_AGENT_MEMORY_BASE`; do not invent another memory root to match the examples.

## Retrieval Strategy

1. Use `hybrid-pack` or `librarian` for durable knowledge.
2. For lost dialogue, select the native session/history rather than searching a
   shared handoff or assuming the latest same-platform conversation is yours.
3. For conceptual orientation, inspect the appropriate navigation surface.
4. Cite chapter IDs like `[mem:17]`, then `expand` selected IDs if needed.
5. Accept `null_retrieval`; missing recall does not activate native file stores.

Current user direction outranks historical summaries, quotations and engineering
notes. Do not promote a worker result, `/new` parent ID, or stale context into a
new human request. HMK automatic prefetch and `librarian` do not depend on the
optional dialogue plugin. Do not treat retrieved chapters as a conversation log.

## Ingestion Strategy

- use `./scripts/hmk memoryctl.py add-file` for clean markdown or text already in final form
- use `./scripts/hmk ingest_any.py` for heterogeneous formats
- normalize first, then store
- do not put binary formats directly into `library.db`
- do not rely on Python `MarkItDown` on pre-AVX CPUs; it crashes (SIGILL). The host stub at `~/.local/bin/markitdown-local` explains alternatives.

## Curation Workflow For New Documentation

When new documentation enters the system, classify its authority first.

HMK-native flow:

1. normalize and ingest the source into canonical memory
2. retrieve related context with `hybrid-pack`
3. inspect the wiki only as a conceptual map layer
4. decide the curation outcome
5. write HMK first, optional isolated HMK projection second

LLM Wiki flow:

1. stage raw evidence and a curated note outside `$WIKI_PATH`
2. publish through `wiki_publish`
3. verify the HMK evidence/library indexes and `derived_from` edge
4. repair index drift from the authoritative wiki files, never the reverse

### Minimal curation loop

#### A. Normalize and ingest

```bash
./scripts/hmk ingest_any.py \
  --source /path/to/source \
  --shelf evidence \
  --title "descriptive-title" \
  --tags source,new \
  --importance 0.7
```

#### B. Retrieve related context

```bash
./scripts/hmk memoryctl.py hybrid-pack --query "topic of the new document" --budget 1800 --limit 4 --threshold 0.4
```

#### C. Inspect conceptual map if needed

```bash
sed -n '1,200p' wiki/index.md
sed -n '1,220p' wiki/maps/project-memory-system.md
```

#### D. Choose one or more outputs

- evidence only
- evidence + links
- evidence + distilled `library` note
- evidence + wiki update
- evidence + map note update
- evidence + pending-curation follow-up

### Hard rule

- `library.db` is authoritative for HMK-native records
- `$WIKI_PATH` is authoritative for LLM Wiki-authored records
- the workspace projection vault is disposable
- every artifact has one authority; follow the v1 memory ownership policy

Detailed contract: `agent-memory/plans/CURATION-PIPELINE.md` (if present in this agent)

## Anti-Patterns

- Dumping entire raw docs into the answer when SPR is enough
- Using `expand` on many items at once
- Writing scratch noise into the library
- Treating absence of results as failure instead of valid null retrieval
- Referencing absolute paths under `/home/<user>/agent-memory/...` — those are pre-v3 legacy and may not exist. Use workspace-relative paths always.
