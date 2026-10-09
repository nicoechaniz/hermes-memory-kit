# CI-scope independent review of PR #285

Verdict: **APPROVED** at exact head `12725e7a2d5498e6f668ed1ec4c813620d33d7c1`.

Reviewed only the three-file CI-scope correction against previously approved head `4a5e6112c7808bcea7c3121fbd9d82fbccb91239`: `tools/ci_scope.py`, `tests/test_ci_scope.py` and `.github/workflows/tests.yml`. Prior reports remain preserved.

For a pull request, the selector now requires a two-parent checkout whose second parent exactly matches the trusted event head before comparing the checkout to its actual first parent. Git errors, an unexpected parent count or a head mismatch select full CI. The workflow supplies the event head through a quoted environment argument. Pushes retain the existing event-base comparison; missing/zero bases retain the existing full-CI fallback. This removes unrelated upstream changes from the synthetic merge comparison without narrowing the existing file allowlists or stage requirements.

Reran only the new real-Git regression. It passed: a stale event base plus a newer unrelated main runtime change selects archive qualification for the tool-only PR; an incorrect head or unbound comparison selects full; an actual PR runtime change, including the fixture's explicit conflict resolution, selects full. Existing nine-scope-test/frozen-check results were supplied and reused; no broad rerun.

Confirmed `tools/preserve_memory.py`, `tests/test_memory_preservation.py` and `tests/test_dm034_memory_projection.py` are byte-identical to the previously approved head. The source-ID fix, relocated fixture body and all preservation/compatibility criteria remain intact. No demonstrated blocker or reduction of required criteria was found.

New-head CI was still running and remains a separate merge requirement. This review does not independently re-establish the supplied diagnosis of earlier job logs, nor establish live memory continuity, admission, activation or deployment. No code edits, publishing, live memory/runtime/Matrix reads or model calls were performed.

## Fixture-only correction approval

Verdict: **APPROVED** at exact head `cfabc0ddcc55d9a2ddaec1616f9bd2369716fd1d`.

Confirmed the entire diff from `12725e7a2d5498e6f668ed1ec4c813620d33d7c1` consists of four added lines in `tests/test_ci_scope.py`: two explanatory comments and repository-local `user.name=Fixture` / `user.email=fixture@example.invalid` configuration in the temporary Git fixture. The existing helper uses `git -C` with that fixture root; no global/system account configuration is changed. This supplies the identity required by the conflict-producing `--no-commit` merge without changing selector/workflow/runtime logic, assertions, file allowlists or qualification requirements.

Reused the supplied focused regression success with global/system Git configuration disabled, plus frozen/ruff results. No broader rerun or new audit was performed. Earlier approval and review history above remain intact. New-head archive/HMK CI was underway and remains a separate merge requirement. No demonstrated remaining blocker.
