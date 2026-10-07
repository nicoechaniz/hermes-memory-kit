# Mariano's memory research and lifelong HMK continuity

Reviewed on 2026-10-07. This first comparison reads seven selected documents from
four authorized research collections, plus mounted system documentation and
selected serving/index configuration. It adds source evidence to the existing
[durable-recall plan](durable-recall-plan.md). It does not replace the closed
[October investigation](../research/agent-memory-2026-10-06/README.md).

## Source access, dates and editorial status

The receiving body independently listed all four collections and read a
substantive document from each through SFTP and SSHFS using its own identity.
All four byte comparisons matched. After the second view's access repair, an
independent comparison found **66 memory-related Markdown files in each view**:
all 66 matched by SHA-256, with no files unique to either view in this selected
set at 2026-10-07T03:00:32Z. Both mounted views remained read-only; the
receiving services were active and on demand. Initial access qualification is recorded
in [the existing coordination issue](https://github.com/AlterMundi/daimon-matrix/issues/235#issuecomment-6029804744).
No private session, control database or excluded research subtree was read.

The publication exposes live original research files. Their content dates remain
April and July 2026; access in October does not update the research cutoff. The
readable catalogue was compiled on 2026-07-27T19:56:46Z. Its index, status and
collective-memory project node match byte-for-byte in both mounted views. That
historical catalogue locates work; current claims require the underlying sources.

Reading the mounted consultation guide, architecture narrative, `serve.py`,
`tier1.py` and service unit establishes the source relationship below. The index
root is the server tree exposed here as `marianos-live`; the API serves its index
and projections. It does not query the receiving SSHFS mount or the backup.

| Surface | Role established by the mounted context |
|---|---|
| `marianos-live` | Read-only receiving view of the working source tree, including its published map and underlying research |
| `collective-memory` | Consultation service over that tree's filtered index: curated map, generated syntheses and source documents, distinguished by kind/provenance |
| `marianos-backup` | Separate source view containing additional project/copy directories absent from the live tree; current work may also live here |

Curatorial status belongs to documents and publications within these surfaces;
a mount name or file modification time does not establish approval. M5 explicitly
reports a July design awaiting Mariano's review/approval. Generated synthesis,
reviewed knowledge and working evidence retain their respective provenance.
Assess freshness from each document's content, revision and dates; neither mount
name establishes age or activity. The two-view hash comparison covers the four
selected memory research collections, with unrelated Hermes research, private
context and symlinks excluded. It does not establish equality or age of the
whole trees. A bounded
HTTP `/health` request from this host timed out, so actual API receiving access
is still unqualified. Direct filesystem reads remain available for this work.

## Selected source ledger

Identifiers below name documents in the authorized research collections. Hashes
identify the bytes inspected; they do not certify the claims or an approved
release. Raw documents are not copied into this repository.

| ID | Collection and document | Document framing |
|---|---|---|
| M1 | `Sobre_Hermes/memoria-resumen.md` | April 2026 executive summary of three investigations |
| M2 | `Sobre_Hermes/memoria-v2-integrado-llm.md` | April 2026 implementation proposal for Hermes 0.10 and a CPU-only machine |
| M3 | `Sobre_Hermes/research_memoria_2026-04-24/07-recomendacion-sintesis.md` | April 24 synthesis situated in HMK 3.2 and a separate continuity plugin |
| M4 | `Agentes_y_memoria_persistente/01_MemGPT_Letta_y_Memory_OS.md` | Survey note on virtual memory, reflection and alternatives |
| M5 | `Base_de_datos_fractal_semantica/PLAN_MVP_memoria_colectiva.md` | July 4, v4 design for curated collective knowledge |
| M6 | `capitalizacion_llm_memoria_colectiva/SYNTHESIS.md` | Research synthesis on layered knowledge and discovery |
| M7 | `capitalizacion_llm_memoria_colectiva/agent_reports/05_writer_side_synthesis_y_knowledge_distillation.md` | Raw writer-side consolidation report; distinguishes findings and proposals |

| ID | SHA-256 |
|---|---|
| M1 | `9b3f1ee9e3242feb6c1fd2de947bf94e659a33a4aa457a4095e356e2ed10fbc8` |
| M2 | `9f6d55414e274e653839bd1caf787aba6de83c53fbddc039e7f1e76615cd3452` |
| M3 | `7af4e58c45eb0f91c5607c6d98c356c45abc517b05bea78d50a65d5fc6ea5ef8` |
| M4 | `639dedf31ba97d36ffdb4d4a49d0802298f0d179c2e94f2249912c64efb29a7b` |
| M5 | `f66f15b0b4f3b2063e7fa7c82cbd4d6b194af358606687675340f9b215ad4d4e` |
| M6 | `ac024222a85faa1e893b008f6958c10866a2bc536e7b81a5b328b18f13e7ca34` |
| M7 | `a1947a1da227ca8cad06f186aa179b45c1b07bb91b74a23a8d08bae75209b40c` |

Additional mounted context used to establish the source wiring:

| Artifact | Inspected scope | SHA-256 |
|---|---|---|
| `Base_de_datos_fractal_semantica/SISTEMA_MEMORIA_COLECTIVA_narrado.md` | Opening architecture and source/serving sections, dated July | `6e6fee8d1c87d40c5b59f66212a2160560ea07e73ca8e0016a42dd1fc1378202` |
| `catalogue-20260727T195646Z/GUIA_CONSULTA.md` | Consultation guide, published July 27 | `10f8941eb20685fb2f28b518f7e12d624fcd01e0529dafabf725173e09a7f055` |
| `.mapa/serve.py` | Imports, serving configuration and health/search/document handlers | `7cb0fbfe4d14b11a26525b3a86c2cce9a692bc62a7acb124f58825effa9d132a` |
| `.mapa/tier1.py` | Source/index/map root definitions | `e5de7372298250e35549470d0b0249e4ae4bc030b12a0b04e8ec1339c0f6b295` |
| `.mapa/mapa-serve.service` | Serving entry point and configured environment | `008a663b9e0a2f617f536da7e7df1f0090a27a0b0d5d3edd3df4ad090825902f` |

## Mechanisms to carry into the existing plan

The documents already address agent continuity and consolidation alongside
research indexing. M3 separates immediate working continuity from long-term
memory. M2 proposes episodic, semantic and procedural memory plus retained
historical changes. M5 describes a curator-controlled map with stable logical
IDs, content hashes, durable inputs, coherent publication and visible freshness.
M6/M7 add maintained thematic synthesis and attributed discovery. These are
useful situated designs; their examples do not establish present HMK behavior.

The following translations are proposals for this being-level use:

| Source mechanism | HMK translation | Existing work |
|---|---|---|
| Working versus long-term memory (M3/M4) | Preserve each native conversation and separately select enough durable meaning to recall without it | [Ownership contract](memory-ownership-contract.md), [Codex integration](codex-native-memory-review.md) |
| Episodic/semantic/procedural distinctions (M2/M3) | Link selected episodes, maintained person/project accounts and evidence-based learning; test compact records before requiring separate tables | P1/P3 |
| Preserved temporal changes (M2/M3) | Keep previous meanings and corrections; distinguish occurrence, report and revision time; answer both current and past questions | P1 |
| Stable IDs, hashes and coherent publication (M5) | Bind decisions to source event/version, retain pending deltas, validate proposed consolidation and publish a consistent revision | P1/P3/P4 |
| Readable source layer and freshness (M5) | Keep selected records accessible despite an unavailable embedding provider; expose indexing readiness and source/account age | P2/P3 |
| Maintained thematic synthesis (M6/M7) | Build revisable abstractions with local evidence links, provenance, qualifications and a path back to the selected episodes | P4 |
| Typed discovery with counterevidence (M6/M7) | Store proposed connections or learnings with support and uncertainty, then test their usefulness; inference retains its attribution | P4/P6 |

## Adaptations required by source loss and ten-year recall

**Episodes must survive consolidation as usable evidence.** M2's sleep proposal
creates a cluster summary, marks its episodes as superseded, and its default
search omits superseded records. That is an example's behavior, not an observed
live implementation. For HMK, a later question about an interesting issue
comment must still reach the participant, proposal, significance and outcome.
An abstraction can link and compress those episodes while keeping their selected
meaning retrievable. A factual correction and an episode summarized at a higher
level need distinct treatment; summarization does not make the encounter false.

**A source pointer has different guarantees when the source can disappear.**
M1/M2 use SPR plus a raw reference; M7 describes synthesis as regenerable from its
source corpus. Our sessions may be unavailable in another body or ten years
later. Retain self-contained selected evidence in HMK before deriving accounts
or learning from it. Generated syntheses and diary views can then be rebuilt
from that retained evidence. Detailed project state still belongs in its cockpit.

**Selection must include single significant encounters.** M2 illustrates clusters
of at least ten items; M7 proposes at least three sources for a general synthesis.
Those conditions cannot become minimum counts for remembering a person, a short
tool-delivered communication or a meaningful shared moment. Capture can persist
one encounter immediately; later consolidation may find a larger pattern.

**Recency and source status need question-specific treatment.** M1/M2 recommend
decay, while M2's consolidation discussion favors the newest conflicting fact.
An old episode remains necessary for a past-event question. A later report also
does not alone settle two incompatible accounts of an event. Preserve evidence,
time precision and disagreements, and qualify the current account. Test aging,
distractors and missing sources under the existing recall protocol.

**Style similarity is a limited continuity signal.** M2 suggests comparing
embeddings of current and baseline speech. Such a measure can flag changes in
wording. It does not establish correct autobiography, known participants,
authored contributions, preserved history or signed body membership. Test those
properties directly rather than declaring continuity from a style score.

## Recommendations that require fresh evidence

M1/M2/M3 contain fixed budgets and thresholds, model/hardware comparisons,
framework rankings, provider advice and proposed lifecycle triggers. Their
numerical and vendor claims were not revalidated in this access comparison and
are not imported as current defaults. M3 explicitly situates its CPU proposal
in a machine without AVX; retain this deployment's configured embedding provider
until a controlled component comparison justifies a change.

Use the October archive's pinned primary-source findings for the current
competitor comparison. Test relevance in the actual score space, distinguish
absence from an unavailable backend, and measure formation plus recall cost.
The [whole-kit review](general-memory-review.md) already supplies reproduced
preservation and retrieval defects; they remain the implementation priority.

The source publications do not authorize this body to install their timers,
succession hooks, startup reads or discovery director. Native session continuity,
HMK capture and staged sleep use the receiving body's established authorization
and source boundaries. Reuse the existing #11/#12 Codex work for that integration.

## Evidence and next discriminating work

This delivery verifies selected filesystem access, establishes the configured
source/index/API relationship and compares inspected designs. It does not run
their examples, benchmark models, consolidate a live pool or qualify API access.
The October raw reports and their checksum record remain unchanged.

Consult the published map and trace its conclusions to the source revisions.
Compare both readable views for current, additional and historical research;
the name `backup` must not limit a source to historical use. Keep
the current P0 preservation fixes first. For P4, compare retained
episodes plus linked syntheses against the original pool using the same recall
questions and budget; explicitly test that consolidation preserves weak-cue
access to a one-off person or event after source loss. Preserve the before/after
records, supporting links, corrections and replay evidence.
