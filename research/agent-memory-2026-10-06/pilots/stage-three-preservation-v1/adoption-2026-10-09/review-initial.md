# Independent review of PR #285

Verdict: **REQUEST CHANGES** at exact head `0263a4e3e5ded16277fca4a570441711f41cb2ae`, against parent `3b67edf522078d983645e44e8154996e4f4b7ee6`.

## Blocking finding

**P1 — Unvalidated source IDs allow Git bundle writes outside staging and overwrite unrelated files.** `tools/preserve_memory.py:134` accepts plan IDs without the validation performed by `tools/export_being.py:670–673`; `tools/preserve_memory.py:226–227` then uses the selected ID directly in a filesystem path and passes it to `git bundle create`.

A targeted, disposable, fictitious-repository reproduction at this exact head:

1. Initialize an ordinary Git repository with one committed `lesson.md`, then obtain a plan with `archive.discover("Fixture", [("context", source)])`.
2. Set `plan["sources"][0]["id"] = "../outside-profile"` and select `git_sources: ["../outside-profile"]` with the supported preservation-selection schema.
3. Write a pre-existing unrelated file at `output.parent / "outside-profile.bundle"`.
4. Call `preservation.build(plan, selection, output, writers_stopped=True)`.

Observed: the builder returns a successful v1 profile, the unrelated file is overwritten with a Git bundle, and the final profile directory contains only `memory-preservation.json`. The escaped bundle is absent from the advertised profile directory. The base exporter rejects the identical plan with `unsafe_relative_path`.

Validate every plan source ID with `archive.safe_name`, require a single path component and a supported source kind before any output I/O, as the base exporter does. Add a focused regression proving traversal/absolute IDs are rejected before creating or overwriting any bundle. This is an input-validation defect, independent of the declared writer cutoff or archive transport checksum.

## Reviewed behavior and evidence

Read repository `AGENTS.md`, `CONTRIBUTING.md`, the pinned foundation, and the contributions skill. Reviewed the complete seven-file diff, relevant base-exporter safety helpers, and the frozen/current HMK qualification boundary. Reused the supplied successful CI evidence: 73 archive tests and 41 frozen/current HMK tests; did not rerun broad suites.

The coherent design preserves complete selected SQLite snapshots, fingerprints unknown columns and native revisions, accounts for historical Matrix statement references, distinguishes declared prior unavailability from subsequent loss, binds the sidecar to the staged base manifest, and keeps preservation separate from admission and authority. Existing tests exercise source-free restoration, exact historical content, altered/missing dependencies, earlier Git revisions, and clean current-head reconstruction. A separate targeted Git replacement-ref experiment successfully restored the original earlier commit; it produced no finding.

The unchanged wire-contract pin remains `f10fd5c3089c0962920314c97e14bc024feffa7a`. CI separately checks out and qualifies current HMK `0f9a3b22c7a765514d36c9aa64d4649d7318a863`; the compatibility subclass verifies HEAD and tracked script drift. These are distinct implementation and contract claims.

No additional demonstrated blocker or required follow-up was found in this bounded review. Approval is withheld solely for the source-ID write escape. No code edits, publishing, model calls, live memory/runtime/Matrix reads, enrollment or deployment were performed. This review does not establish conversational continuity or a live receiving-body effect.
