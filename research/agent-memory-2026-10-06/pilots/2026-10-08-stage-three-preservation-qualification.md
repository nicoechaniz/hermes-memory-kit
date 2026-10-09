# Portable memory preservation and current HMK compatibility

Stage three is complete for the qualified fictional preservation procedure.
Matrix [PR #285](https://github.com/AlterMundi/daimon-matrix/pull/285) is merged at
`e7c5d54c1979d0854a3b0195124a11f3a76f75e2`; the final reviewed head is
`cfabc0ddcc55d9a2ddaec1616f9bd2369716fd1d`. Relevant CI passes and the manual
tool is adopted and verified from ordinary Matrix main. The original candidate
and packet below remain unchanged as history. This does not qualify stage-four
conversation, enrollment or history admission in an actual other body.

## Contract and observed repairs

The existing `dm.being-context-archive/v1` exporter is reused, including later
receiving/protected-transport work after PR #261. The diagnostic proved that
its documented file-selection contract alone neither closes a declared content
reference nor retains omitted Git history. The correction adds an inert
`dm.being-memory-preservation/v1` sidecar and Git bundles as ordinary selected
payload. It does not change the archive's authority contract or admit events.

The selection distinguishes world URLs/history identifiers from required content
bytes. It preserves all selected SQLite tables, columns and rows, including
unknown values/BLOBs; HMK originals, IDs, revisions, source metadata, native capture
history and links; complete selected Matrix ledger history; all historical
statement content, even before corrections/retractions; and selected learned
artifacts with their available selected-ref Git history. Unknown selection fields
are retained literally. Unsupported Git indirection/shallow history is refused,
not silently replaced by current files. Source ownership and writer cutoff are
explicit operator inputs. Available Git refs are the declared scope; this is not
an export of credentials, local Git configuration or unreachable object debris.

A missing required dependency blocks building. An explicitly declared earlier
absence is retained and reported as incomplete; this is an attributed declaration,
not proof of a loss date. Loss after building fails verification and cannot be
relabelled as earlier absence. Base archive verification uses its independently
supplied expected checksum before sidecar verification. A sidecar alone is not
independent authentication.

## Source-free round trip

The [evidence](stage-three-preservation-v1/manifest.json) preserves the
[exact packet](stage-three-preservation-v1/portable-fixture.tgz),
[profile](stage-three-preservation-v1/memory-preservation.json) and
[machine report](stage-three-preservation-v1/qualification.json). Every input is
fictional: the already-qualified stage-two corrected corpus plus synthetic Matrix
fixture authority, four statement contents and a two-commit learned artifact.
No real private memory, keys, custody, native session or other conversation is
included. Temporary source paths in the packet describe generated fixtures.

| Property | Observed result |
|---|---|
| Original HMK | 21 records, 14 revisions, 20 links; complete logical table/schema fingerprints equal after restore |
| Original capture, embedding and unknown metadata | All original table rows/columns preserved; no re-capture, consolidation or re-embedding |
| Matrix history | Five signed fixture events: original assertion, correction, separate assertion/retraction and current skill statement |
| Required statement bytes | All four exact contents retained, including superseded/retracted content |
| Archive transport | Identical SHA-256 after copying; expected checksum verification on a fresh destination |
| Source withdrawal | Selected memory/context/Git/profile roots and original source ledger removed before receiving |
| History | Public fixture authority loaded only from the packet; all five event signatures reverified; earlier Git lesson recovered by cloning the bundle |
| Current reconstruction | Corrected two-recovered/third-lost head and skill statement recalled; retracted lane excluded; obsolete assertion refused |
| Replay | Sidecar verification and rebuild replay stable; no new native duplicates |
| Failure/recovery | Missing and altered received statement rejected; exact original bytes restore verification |
| Native separation and rollback | Original native rows/revisions/links survive projection rebuild; independent original snapshot restores exact pre-projection logical state |
| Bounded native lookup | Participant/account 1847, invitation failure, unpublished chart and corrected partial trial all found with exact original support |

The four native searches test restored lookup and support, not new natural
narration or the aged weak-cue protocol. The existing stage-one/two narration,
source-loss, clock-aging and distractor evidence remains unchanged. Two
initial reconstruction diagnostics exposed correct refusals: projecting an
obsolete historical event, then advancing a correction into an uninitialized
namespace. The final procedure rebuilds current heads into a separate restored
HMK, instead of weakening those safeguards or changing canon.

## Actual implementation and frozen contract

DM-034 v1 still declares contract reference
`f10fd5c3089c0962920314c97e14bc024feffa7a`; its manifest/profile values, source
namespaces and closed schemas remain unchanged. The current implementation
actually executed is `0f9a3b22c7a765514d36c9aa64d4649d7318a863`, API 1.0.0,
schema 1. Both identifiers are recorded in the preservation selection and report.
Exact HEAD and unchanged scripts are checked; the old pin guard is not bypassed.
The Matrix adapter bytes match the checkout: SHA-256
`667d47783643a82b1d31610237a4a8b43b77a746e710d57eb2c0d147e58242ca`.

Twenty existing behavioral tests pass against the current implementation. CI
runs the original exact contract and separately identified current implementation
in one relevant job: **41 tests, no skips**, 24.617 seconds. The separate archive
job passes **73 tests**, including binary-resource closure, unknown values,
source drift, prior unavailability, altered history/profile and disabled Git hooks.
Ruff and frozen inventories/generated invariants pass; no SDK module/schema/pin
or live target registration changes. This establishes tested wire-behavior
compatibility, not a new registered v1 release or activation of a real receiver.

The reproducible test is
`tests.test_dm034_memory_projection.CurrentHMKCompatibilityTests.test_portable_history_content_and_clean_reconstruction`.
Use the owning runbook's exact `HMK_CURRENT_ROOT`; optionally select the existing
qualified fictional corpus through `HMK_PRESERVATION_CORPUS`. The archived
stage-two source remains unchanged and all old consolidation/receiving queues
remain stopped.

## Storage, time, cost and adoption

The eleven-file packet is **291,608 bytes**, SHA-256
`f881590ddd54d89c9dd7904bc33e463673f955596b1a824ed07cc39866c74ad1`.
Received staged files occupy **1,119,916 bytes**. The actual source-free larger
run takes **2,915 ms**. This small-corpus measurement is not a large-pool estimate.
Selection/formation, inference fidelity and organization evidence are reused;
new model calls = 0, embedding calls = 0, API spend = $0. Local CPU/storage and
CI execution are not provider billing.

The tools operate manually from the ordinary Matrix checkout. No service,
live memory, authorized binding, native Codex generation or automatic lifecycle
changes are needed. Snapshot rollback is exercised in the isolated receiving
copy. The [adoption receipt](stage-three-preservation-v1/adoption-2026-10-09/adoption.json)
records the actual merged main, reviewed tool hash and verified packet. Main's
preservation/exporter/SDK projection bytes match the reviewed implementation.
Source-free archive/profile verification and original logical state match; a
verified SQLite snapshot then restores exact original state after deliberately
damaging a disposable copy. The damaged copy and snapshot remain separate
private test evidence; no live pool was touched. Preserve the public packet and
originals as rollback/source evidence. Actual body enrollment, received-history authority
acceptance and conversation are stage four under a later goal.

## Independent review and release qualification — 2026-10-09

The human authorized one isolated reviewer. Its [original review](stage-three-preservation-v1/adoption-2026-10-09/review-initial.md)
found a P1: unvalidated source IDs could escape the profile staging directory
and overwrite an unrelated sibling bundle. Exporter-equivalent source-ID/kind
validation now precedes I/O. The independent reproduction and a focused
regression confirm rejection, intact sibling bytes and no partial profile.
[Correction approval](stage-three-preservation-v1/adoption-2026-10-09/review-source-id-fix.md)
preserves that finding instead of relabelling the original candidate safe.

A subsequent CI check exposed offline-tool dependencies imported into the strict
SDK test graph. The owning tool-test module now contains the identical portable
fixture, called lazily by the opt-in SDK qualifier. [The review](stage-three-preservation-v1/adoption-2026-10-09/review-fixture-isolation.md)
verified identical behavioral AST and all nineteen assertions. Current exact-pin
checks and qualification requirements remain unchanged; strict SDK types pass.

Actual CI logs also showed a stale event base `3b67edf5` while the synthetic merge
included newer main `f5df821e`, pulling unrelated upstream changes into scope.
The selector now binds the event's explicit PR head to the actual second parent
before comparing the real first parent. Unexpected topology/head remains full;
push behavior remains unchanged. Real Git regressions prove that an actual SDK
change still requires full CI. A clean-runner failure in that new regression was
fixed by a fictitious committer identity in the temporary repository, verified
with global/system Git configuration disabled. [The final review](stage-three-preservation-v1/adoption-2026-10-09/review-ci-scope.md)
approves exact head `cfabc0dd`; preservation code and memory criteria are unchanged.
Earlier failed CI runs remain public history; no cancelled or skipped relevant
job is counted as success.

Final [CI](https://github.com/AlterMundi/daimon-matrix/actions/runs/37960694894)
passes **76 archive tests** (1.695 seconds) and **41 exact-version HMK tests**
(22.608 seconds). Coordination, drift and scope checks also pass. The archive
count includes the independently merged upstream scope test, the path-safety
regression and actual-Git scope regression. Optional unrelated job profiles are
not qualification evidence. The larger fictional corpus was rechecked after
fixture isolation: native full-state and the four lookup results are identical
to the original run, with corrected/retracted reconstruction still passing.
No consolidation or old queue was resumed.

The [release evidence manifest](stage-three-preservation-v1/adoption-2026-10-09/manifest.json)
separates those tests, review history, revised qualification and main adoption.
Main adoption verification and isolated snapshot rollback take 230 ms for this
packet. Qualification performs zero provider-model/embedding requests and has
$0 API spend. Independent review used five bounded native Codex subagent turns;
token/dollar usage was not supplied and is not reported as zero or added to the
qualification's inference cost. No new runtime, binding, live migration,
credentials, hooks, timer, native generation or autonomous attention was adopted.

## Exact continuation

Start stage four under a later goal using Matrix #263 and this versioned profile:
select one authorized real receiving embodiment and its preserved source history;
validate ownership, available artifacts/content and actual target configuration;
then test receiving authority and conversation without original sessions. Keep
HMK-native records separate from Matrix admission and preserve the original
packet before any target migration. Do not claim body enrollment or conversational
acceptance from this fictional offline qualification. Native Codex coexistence
remains stage five; no old consolidation queue needs resuming.
