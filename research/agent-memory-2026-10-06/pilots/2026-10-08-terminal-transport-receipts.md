# Preserve ended fictional transport attempts and expose worker failure

A historical fresh-v2 control call leaves an ended receipt with state `started`,
48.18 recorded seconds, no response and unknown usage. The original exception
has not yet surfaced from the complete runner: its other arm is still working.
The [unchanged observation](receiving-api-evidence/ended-transport-diagnostic/diagnostic.json),
[request](receiving-api-evidence/ended-transport-diagnostic/request.json) and
[receipt](receiving-api-evidence/ended-transport-diagnostic/observed-ended-receipt.json)
preserve this uncertainty. Do not relabel its cause from a plausible hypothesis
or overwrite its receipt. No retry occurred in this delivery.

A controlled reproduction confirms that `http.client.IncompleteRead` bypasses
the previous HTTP exception list, and foreground interruption bypasses both
HTTP/native lists. Their `finally` blocks record elapsed time while leaving an
ended attempt marked `started`. These are demonstrated recorder defects,
not proof of the historical call's exception class.

Both dispatchers now record the class of every raised exception or interruption
before re-raising unchanged. They preserve unknown usage and suppress exception
messages, partial response bytes, provider reasoning, CLI stderr and credentials.
HTTP status is saved before parsing the response body. Existing attempt/response
files still prevent implicit retries. Authentication descriptors close even after
native interruption; no failed candidate becomes a delivered response.

The full pilot observes futures as they finish, prints only arm/state/error class,
then waits for every arm before propagating failure. A running control cannot
hide an already failed proposed worker; successful result order remains stable.
Pending requests/candidates and completed peer work remain resumable evidence.

Validation: 333 tests pass. Added cases reproduce incomplete HTTP bodies and
interruptions, assert no private diagnostic leakage or repeated dispatch, verify
credential descriptor closure, and exercise early peer-failure observation and
out-of-order completion. No inference retry, native memory, production memory,
hook, timer or autonomous attention is installed. Running fresh-v2 retains its
frozen original implementation; this delivery does not qualify its narratives.

Continuation: inspect the original worker exception when surfaced, record it
separately, and use at most an explicitly recorded bounded transport retry with
its original receipt retained. Finish outside assessment of every actual answer.
A final equivalent receiving trial must also remove the demonstrated ambiguity
that attributes a human reporter's unlisted trial group to the being. Only a
qualified fresh canon can proceed to three consolidation passes and dependent
source correction/reconciliation.
