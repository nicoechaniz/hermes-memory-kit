# Optional decoded receiving sources: conservation preflight

Receiving prompts currently ship both encoded source envelopes and their decoded,
attributed quotations. Add an explicit `source_representation='decoded'` research
option that omits the encoded copy **only** when a complete parse accounts for
all source content, including nested retained envelopes. Decoded quotations,
headers, speakers, receiving bodies, report dates, source references, world
anchors, origin and support status remain. A source-text hash binds the original;
original retrieval text and proof checks are unchanged.

Mixed prose, incomplete envelopes, excessive nesting and additional text before
or after a source keep the entire raw text. This is syntactic conservation,
not a selector, semantic compression or noise admission. Default `full` behavior
and its procedure fingerprint remain unchanged. Changing representation rejects
reuse of an accepted or pending full-format checkpoint instead of resetting it.
Existing trials retain their original implementation and inputs.

The [preflight](receiving-api-evidence/decoded-source-preflight.json) compares
11 observed initial narrator packets from the fresh-v2 trial without inference.
Attributed blocks/provenance/anchors compare equal. Source payload falls from
109,508 to 84,206 characters (23.1%). This is character reduction, not measured
provider tokens, money, latency or narrative quality. Native base instructions
and reviews have additional costs; no such saving is claimed yet.

Forty-two narrative tests pass, including complete nested-source conservation,
six mixed/malformed fallback cases and checkpoint incompatibility. The full
suite passes 328 tests. No production installation, model choice, memory or
running trial changes in this delivery. The option needs a fresh equivalent
receiving comparison before adoption. The ongoing full fresh-v2 trial retains
full-format inputs and outside grading; its attribution limitations are not
fixed or qualified by this preflight.
