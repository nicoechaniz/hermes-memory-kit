# Release-head independent review of PR #285

Verdict: **APPROVED** at exact head `4a5e6112c7808bcea7c3121fbd9d82fbccb91239`.

Reviewed only the two-file fixture relocation against previously approved head `c0d5e5a94db45c1c4dde603d9d2fc3766554a347`: `tests/test_dm034_memory_projection.py` and `tests/test_memory_preservation.py`. Prior reviews remain preserved.

The current-HMK test still runs under the same unittest name and exact-pin setup, now calling the offline helper through `import_module`. The helper imports the same runtime/test constants and transports; exceptions and assertions propagate directly. A targeted AST comparison confirms the complete behavior from fixture startup through evidence/report output is identical, retaining all 19 assertion calls. Source withdrawal, exact content/history verification, signature checking, earlier Git revision restoration, missing/altered dependency checks, current-head rebuild, native-record retention, bounded corpus lookup and rollback checks remain intact.

Separately confirmed byte-identical `tools/preserve_memory.py`, `.github/workflows/tests.yml` and `tools/ci_scope.py` against the previously approved head. The P1 source-ID validation fix remains intact, and CI still invokes/configures the current-HMK qualifier. No contract pin, runtime behavior, qualification requirement or acceptance assertion was relaxed. This isolates optional offline-tool imports from the typed SDK graph without reducing behavioral coverage.

Reused the supplied strict-mypy success, eight offline-tool test results, qualified fictitious 21-record/14-history corpus fixture result and frozen-check success. Ran only the structural/unchanged-file verification described above; no broad test rerun or unrelated audit. No demonstrated remaining blocker. New-head full CI was underway and remains a separate merge requirement.

This approval covers preservation and isolated qualification only; it establishes no live memory continuity, Matrix admission, receiving-body activation or deployment. No code edits, publishing, live memory/runtime/Matrix reads or model calls were performed.
