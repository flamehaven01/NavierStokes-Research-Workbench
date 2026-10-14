# NSRW publication and international reproduction plan

Date: 2026-10-08 (Asia/Bangkok)
Scope: publication planning for an independently maintained research project.
This is not a proof receipt, a second claim ledger, or an execution gate.
It does not authorize account creation, uploads, outreach, deployment, or releases.

## 1. Decision and constraints

Historical scheduling decision (2026-10-08): **continue C04 -> Z first**, following C03C admission.
Updated preparation position (2026-10-12): **Z-core and bounded Z+J have separate
named-proposition admissions** from one shared exact commit-bound replay.
Updated authorization (2026-10-14): first publish NSRW software through the
author-enabled GitHub–Zenodo integration and P01 as a separate mathematical
preprint. Final inspection, path-scoped commit/push and GitHub Release are
authorized; issue the Release only after the exact commit's hosted CI succeeds.
Verify the resulting Zenodo record rather than assuming integration succeeded.
P02/P03 manuscripts, application drafts, outreach and site deployment are deferred.
Preserve the previous decision as historical chronology, not the current queue.

Use **Zenodo as the primary archival dissemination route**, the existing GitHub
repository as the executable source, and a small GitHub Pages site as the
reader-facing explanation. arXiv, Reddit, and Hacker News are outside the
current delivery plan; their availability is not a prerequisite for sharing
NSRW research. This is an operational choice, not a claim that independent
researchers are universally ineligible for those services.

The objective is to make a bounded result understandable, downloadable,
reproducible, and open to correction internationally. It is not to manufacture
academic endorsement or maximize impressions. Existing LinkedIn activity does
not establish technical engagement, but low engagement does not refute the
research either. Domestic communities are optional; no assumption about a
national audience's attitudes is needed in the public presentation.

English is the primary international-facing language. A Korean summary may
link to the same evidence rather than maintaining a second status narrative.
Use an accurate author identity and independent-researcher affiliation; do not
invent an institution, reviewer, endorsement, or collaborator.

## 2. Starting point and claim boundary

The current position must be read from the
[dated checklist](NSRW_COLAB_RESTART_TASKS_2026-10-06.md),
[claim index](E2A_RESOURCE_CLAIM_LEDGER.yaml), and exact receipts. This plan does
not update their mathematical status.

As of 2026-10-12, the [C04 receipt](stage_receipts/P2_C04_COLAB_2026-10-10.md)
admits a Profile-dependent small-positive-eta coefficient sign. Two later
receipts admit the following narrower consequences from **one shared replay**:

- [Z-core](stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md): for every fixed
  source `Profile F`, a Profile-dependent `epsilon(F)>0` exists; every
  `0<eta<epsilon(F)` has a source `Profile.M=0` at an interior first-repair radius.
- [Bounded Z+J](stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md): a conditional
  first-window local M-zero with `c1>0` implies `J>0`, and the small-positive-eta
  composition gives source `Profile.M=0` and `Profile.J>0` at the SAME point.

Checkpoint: `3a50b5f50b034319a469b9de68f556be70fff02c`;
run: `nsrw-z-phase-replay-20261012T065216884451Z`.
These are separate bounded claim reviews of one execution, **not independent
reproduction**. Original execution metadata remains `NONE / UNVERIFIED`.
The support-derived terminal zero plateau is not a separately compiled theorem.

Do not promote a development compile because its ZIP becomes public. Do not
describe an AI-assisted or same-session review as independent external
attestation. Formalization of a consequence also does not establish novelty
relative to the mathematical literature; that comparison remains separate.

## 3. Archival objects, research publications, and timing

An **archival object** preserves executable inputs and fixed evidence. A
**research publication** presents a mathematical or methodological argument.
A website is a communication entry point. These roles are complementary, not
interchangeable: depositing an artifact DOI is not publishing a mathematical
paper. A later note can cite that artifact as its computational supplement.

| Category | Object | Recommended milestone |
| --- | --- | --- |
| Archival object | Zenodo software/reproduction artifact and fixed evidence package | Local public-derivative candidate after Z-core/Z+J; deposit requires approval |
| Communication | GitHub Pages project site | Deferred pending separate approval |
| Research publication | Short mathematical technical note/preprint | Local English draft on admitted Z-core and Z+J only; no submission |
| Research publication | Fuller P2 obstruction study | Separate later decision; avoid duplicating the bounded Z/J note |
| Research publication | NSRW software/methods paper | A completed research use case and at least one documented external reproduction experience; a failed attempt can be informative and is not confirmation |
| Research publication | Equation to Artifact methods paper | NSRW case study first; an additional non-NSRW case strengthens a broader methods paper |

HF Static Space is deferred, not a first-checkpoint deliverable. Reconsider it
only when a specific visualization improves understanding enough to justify
another maintained surface.

These are publication recommendations, not new prerequisites for C03/C04/Z.
The scheduling decision above defers writing and site work; it does not assert
that earlier admitted results are unpublishable. There is no required paper count
and no reason to split the same finding into several near-duplicate papers.

## 4. Zenodo: preservation before promotion

Zenodo accepts research objects including publications and software. It assigns
DOIs and preserves records; a deposited manuscript is a research note or
preprint unless a separate peer-review process is documented. Neither a DOI nor
community inclusion certifies the mathematical result.
[Records](https://help.zenodo.org/docs/deposit/about-records/)

Start with at most two linked objects:

1. **Archival object — NSRW software and reproduction artifact:** one fixed checkpoint, exact
   Lean inputs, bounded runners, receipts, and public execution evidence.
2. **Research publication — P2 research note:** the mathematical argument, definitions, assumptions,
   limitations, source attribution, and citations to the artifact's version DOI.

Do not mint a third governance-paper record merely to complete a publication
list. Prepare it when it has a distinct, evidenced contribution.

### Minimum bounded public derivative contents

The public derivative preserves exact reproduction inputs and selected,
provenance-linked execution evidence. It intentionally excludes raw private
logs, runtime metadata, caches and compiled binaries; it is **not an equivalent
copy of the original execution archive**. The original remains privately
preserved, unchanged and separately hashed. Reproducing the pinned inputs is
different from independently inspecting every byte of the reference execution.

- A short `README` naming the admitted propositions and explicit non-claims.
- Exact code/proof checkpoint and upstream commit/toolchain/dependency pins.
- Source files and commands needed to generate the external modules.
- Selected same-run axiom/log excerpts and an allowlisted stage-metadata summary,
  linked to original input/log/metadata digests; explicit omissions and transformations.
- File inventory, internal member checksums, external ZIP digest and exact
  post-execution receipt snapshots with their separate document lineage.
- Expected axiom output, expected failure boundaries, and approximate observed
  runtime/resource requirements, without promising identical performance.
- License and upstream attribution; redistribution rights checked for every
  included third-party component.
- Human author/contributor information and an accurate AI-assistance disclosure.

A full original-evidence package would additionally disclose the raw logs,
runtime metadata and generated artifacts, after a separate necessity/privacy/
rights decision. That broader package is not required or claimed by this bounded
derivative. Hashes of excluded bytes are provenance references, not public access
to those bytes or independent verification of them. Neither distribution form
alone establishes independent mathematical reproduction.

### One reproduction entry point

The public artifact package should have a root-level `REPRODUCE.md`. This is a
planned package entry point, not a new file to create before a checkpoint is
selected. Translate existing evidence into the external reader's execution
order rather than introducing another runner or receipt system:

1. Exact artifact version, code checkpoint, and associated receipt.
2. Upstream source/toolchain/dependency pins.
3. Environment requirements and the observed cache/build policy.
4. Exact reproduction commands and input locations.
5. Expected named propositions and explicit non-claims.
6. Expected axiom surface and the scope of that observation.
7. Expected input identities/checksums where portable.
8. Non-portable or run-dependent fields, including paths, timings, line endings,
   and generated artifact/log hashes; do not require fresh-run binary equality
   unless determinism has actually been established.
9. A failure-reporting route requesting the version, command, environment, and
   redacted error/log evidence.

Hashes verify downloaded archived bytes against their inventory; they do not
make a future run identical or establish the proposition's interpretation.

Keep `.olean` outputs as optional version-bound forensic evidence, not a
replacement for source and fresh compilation. Do not require a reviewer to
download the full dependency cache. Git-ignored local evidence is not included
in an ordinary repository snapshot; verify that the intended public evidence
files are actually present in the deposited record.

Preserve the private original archive. If publication requires removal of
personal paths, host identifiers, tokens, or notebook account details, create a
separate public derivative with its own hash and an explicit transformation
note. Never imply its digest is the original archive digest.

Published record files are not edited in place; corrected files require a new
version. Cite the **version DOI** for a specific experiment and the **concept
DOI** when referring to the evolving project.
[Record lifecycle](https://help.zenodo.org/docs/deposit/about-records/),
[DOI versioning](https://zenodo.org/help/versioning)

GitHub integration can archive a release, but enabling it is optional. Manual
deposit avoids assuming that an automatic code snapshot includes ignored
experiment evidence. Verify actual deposited contents either way.
[GitHub archival route](https://help.zenodo.org/docs/github/archive-software/github-upload/)

A relevant Zenodo community may provide another discovery route. Check its
scope and current submission policy before requesting inclusion. Curatorial
acceptance is not automatically scholarly peer review; draft submission can
lead to publication upon acceptance and must not be initiated without approval.
[Community submission](https://help.zenodo.org/docs/share/submit-for-review/)

## 5. A small international entry point

Use the existing repository's project site rather than creating a second
research repository. GitHub Pages provides static hosting for public
repositories on GitHub Free.
[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

The first site should contain only:

1. **Research:** the precise question, rejected candidate assumption, and findings.
2. **Mathematics:** definitions of `Q`, `J/M/H`, normalized moments, `deltaM`,
   and actual axial `c1(eta)`, with source locators and assumptions.
3. **Formal evidence:** named propositions linked to exact proof files and receipts.
4. **Reproduce:** a fixed checkout, commands, downloadable evidence, and expected outputs.
5. **Limits and review:** open obligations and one concrete external-review request.

Keep Equation to Artifact and Operationally Exposed explanations subordinate
to the research. Operational exposure means making an object's inputs,
assumptions, transformations, outputs, and failures inspectable; it does not
mean the object is already a practical solver or engineering product.

Link the future Verification Ledger to the same versioned evidence. Do not
maintain a second hand-edited claim-status table there. Every dated site snapshot
must identify its checkpoint and direct readers to the current checklist.

The site follows **question -> finding -> evidence link -> reproduce -> boundary**.
It must not grow into a manually maintained `L2 PASS / L3 PASS / D PASS` dashboard.
Reuse the repository's explanations and link to dated evidence; any displayed
snapshot must be explicitly dated rather than presented as live authority.

## 6. Reach by technical fit, not by audience size

The ordering below is a workload/fit judgment, not evidence that an audience
will respond. No account availability or willingness to review has been checked.

| Channel | Appropriate use | Boundary |
| --- | --- | --- |
| Lean community / Zulip | Ask for review of one exact theorem statement, source-object bridge, or reproduction failure | Follow current community rules; a conversation is not an endorsement |
| GitHub | Provide persistent source, issues, and a reproduction-report entry point | A star, CI badge, or comment is not mathematical validation |
| Zenodo | Provide citable, downloadable fixed research objects | DOI registration does not guarantee readership or peer review |
| Hugging Face Static Space | Show definitions, proof-chain navigation, or a clearly labeled illustrative visualization | Not a Lean executor or a trained model; do not mislabel evidence as a benchmark/dataset |
| LinkedIn | Send interested readers to the exact result and its reproduction package | Impressions and likes measure exposure, not correctness or technical use |
| Targeted specialist contact | After separate authorization, request one bounded review from a relevant researcher | No bulk messaging, repeated unsolicited requests, or assumed endorsement |

The Lean community identifies Zulip and GitHub as its main meeting places.
This makes it a better subject fit than a broad news feed for Lean source
questions, but response and acceptance remain unverified.
[Lean community](https://leanprover-community.github.io/)

For Lean outreach, lead with the mathematics and the exact declaration, not
an AI/governance framework or a claim to solve Navier-Stokes. A useful review
request has five parts: statement, assumptions, exact source/Lean pin,
reproduction command, and a specific uncertainty. Offer a small review target,
not an invitation to audit the entire repository. Do not file promotional
issues in unrelated upstream repositories or submit upstream PRs solely for visibility.

### First bounded review target

After the separate 2026-10-12 Z-core/Z+J receipts, the first bounded review
should focus on `NSRW.P2.profileMJ_firstRepair_zero_small_positive`.
Supply the exact source/NSRW commits, both receipts and the proposed
`REPRODUCE.md` entry point. Ask whether `Profile.M` and `Profile.J` match the
intended pinned source objects, whether their shared F/eta/r/X is preserved
by the coordinate bridge, and whether any weighted-tail hypothesis is missing.
This is a source/semantic review, **not** a request to accept the upstream PDE
theorem. A second operator's clean compile and literature/novelty evaluation
are distinct. No review has been requested or approved by this planning edit.

### Deferred: Hugging Face without arXiv

A Static Space can host a small artifact explorer without a compute service;
official documentation currently describes Static Spaces as free. Reuse the
same explanation and DOI links, with no new backend or duplicate evidence store.
[Static Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-static)

HF Paper Pages' documented indexing flow is arXiv-centered. Do not assume that
a Zenodo-only manuscript will obtain a Paper Page or Daily Papers exposure.
Use a Space with an ordinary Zenodo link instead; paper-indexing support must
be checked separately if it changes.
[Paper Pages](https://huggingface.co/docs/hub/en/paper-pages)

Do not open HF's numerical FNO/PINN lane merely to attract an audience. It
remains separate from the pinned construction's formal consequences. A browser
illustration is explanatory only unless its own narrower numerical claim has
appropriate evidence.

The first external surfaces are sufficient without HF: **GitHub = executable
source; Zenodo = fixed, versioned archive; GitHub Pages = readable entry point**.

## 7. Manuscript separation

**P2 mathematics:** explain the obstruction of a scale-invariant ratio within
a pinned construction. Distinguish source lemmas, newly derived consequences,
and literature novelty. A zero denominator does not by itself prove that a
quotient's limit diverges. No claim about the upstream theorem's failure or a
solution to the Millennium problem follows.

**NSRW software/methods:** explain how the workbench supported an actual
investigation, including failures and the rejected endpoint-first-zero
assumption. Demonstrate use, maintainability, and reproducibility rather than
listing internal terms or test counts as the contribution.

**Equation to Artifact:** start as a case study of claim transformations.
Compare against relevant provenance/reproducibility/assurance literature;
document missed errors, costs, and trust-domain limitations. General
effectiveness claims require evidence beyond one self-authored example.

Each manuscript must cite upstream work, identify human responsibility,
disclose AI assistance, and distinguish a Zenodo preprint from a peer-reviewed
publication. Present inspectable evidence rather than relying on institutional
branding. External review can strengthen assurance, but no endorsement may be
implied unless it has actually been given.

### Bounded literature and novelty review

Before a research note makes a novelty claim, compare its exact consequence
against the pinned upstream manuscript, relevant declarations, and a bounded
selection of related papers or technical discussions. Record reviewed versions,
locators, queries, access gaps, and the stopping boundary. Use these descriptions:

- `EXPLICIT_IN_SOURCE`: an exact statement is located, with a citation.
- `IMPLICIT_BUT_STANDARD`: a cited standard argument explains the consequence;
  do not assign this label solely because the result seems easy.
- `NOT_LOCATED_IN_REVIEWED_SOURCES`: no explicit statement was found within the
  declared review coverage; this is not proof of novelty or priority.
- `UNKNOWN`: coverage or interpretation is insufficient to classify it.

Prefer "a consequence we did not locate as an explicit statement in the
reviewed pinned source" over "a new result" when that is the evidence available.
This review concerns manuscript wording, not admission of compiled propositions,
artifact preservation, or permission to continue C04/Z. It is not performed by
adding this section.

## 8. Bounded preparation checklist

This checklist tracks publication preparation only. It does not replace the
mathematical restart checklist or authorize an external action.

- [x] Record the Zenodo-first route and the separation of artifact, manuscript,
  site, and community engagement (this document).
- [x] Select the named admitted claims and pin their **execution** checkpoint:
  Z-core `profileM_firstRepair_zero_small_positive`, conditional Z+J
  `angularMoment_pos_of_firstRepair_mass_zero`, and same-point
  `profileMJ_firstRepair_zero_small_positive` at `3a50b5f...fff02c`.
  The execution identity stays fixed; each derived-package revision has its own digest.
- [x] Assemble and crosscheck a **held local public derivative** (2026-10-13):
  exact inputs, two post-execution receipts, selected axiom lines, bounded stage
  summary and root-level `REPRODUCE.md`; internal member digests plus an external
  ZIP sidecar. Separate hash-check implementations share the same operator/trust
  domain and do not constitute independent attestation.
- [ ] Finish human content/privacy/redistribution-rights review of the actual
  final ZIP and its extracted links; preserve earlier candidates and the private original.
- [ ] Finish README/CHANGELOG/docs sanity and exact Git file inventory for the
  [proposed v0.4.0 milestone](releases/v0.4.0.md). Draft notes are not a created
  tag, GitHub Release or package-version bump; historical tags/notes stay unchanged.
- [ ] Before claiming novelty in a research note, perform the bounded review
  above and record one of its four classifications with evidence and access gaps.
- [ ] Finalize the local English technical-note draft after mathematical,
  factual, license, privacy and attribution review.
- [ ] Prepare citation metadata and cross-links for software, evidence, and note.
  No invented DOI or published status before the actual deposit exists.
- [x] Obtain author approval for NSRW + P01 publication (2026-10-14).
  Site deployment and external outreach remain outside that approval.
- [ ] After approved publication, verify unauthenticated download, deposited
  checksums, version DOI, and all site/repository links.
- [ ] After separate outreach approval, request one bounded source-semantic
  review of the SAME-point `Profile.M=0` / `Profile.J>0` theorem. Preserve
  counterarguments and failed reproduction reports.
- [ ] Defer HF Static Space unless it adds specific explanatory value without
  duplicating upkeep. No paid compute or account changes are authorized here.
- [ ] Review substantive engagement before expanding channels or writing more papers.

The bounded Z-core + Z+J phase is now admitted at named proposition scope.
Current preparation sequence: **preserve private originals -> build local public
candidate -> produce/redact/have separate digests for the public derivative ->
review content, rights and privacy -> commit/push and inspect the exact hosted CI
-> approve tag/GitHub Release and its evidence assets -> archive software/evidence
on Zenodo -> prepare the separate research-paper record -> GitHub Pages and
reviewed output-free Colab starter**. Each external write retains its approval
boundary. PyPI is not a target; Docker/GHCR and HF remain optional. Do not build a
new verification framework to perform this conversion. No additional Lean
proof or replay is required for the already admitted proposition scope.
Zenodo deposit, Pages deployment, external outreach, tag and release all
require subsequent explicit approval.

Publication identity confirmed by the author on 2026-10-13: **Yun Kwansub**
(family name Yun, given name Kwansub). [Software citation](../CITATION.cff)
is prepared; affiliation/ORCID were not supplied and are omitted. The research
note carries this author identity separately. Version, publication date, DOI
and cross-record identifiers must be filled only when actually established.
Citation preparation does not complete the human rights/privacy review or
authorize upload. The existing private originals and execution checkpoint stay fixed.

## 9. What counts as engagement

### Distribution observation — 2026-10-15

The earlier preparation checklist is retained as a dated planning record.
NSRW v0.4.0 was subsequently published on GitHub at software commit
`6b81fc0c672ac8d5dd6cea9a7dbe7277ba8793bc`, after all six jobs of
[the exact-commit CI run](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/runs/38601396281)
succeeded. The [Release](https://github.com/flamehaven01/NavierStokes-Research-Workbench/releases/tag/v0.4.0)
has four selected assets; GitHub digests and retrieved local hashes matched.
Author approval and assisted file inspection are not independent legal review
or external mathematical attestation.

Zenodo's repository release webhook was enabled after that publication; the
connection ping returned HTTP 202, but no release event was delivered at the
pre-patch observation. The authorized [v0.4.1 distribution patch](releases/v0.4.1.md)
updates software metadata and current documentation, preserving P01 v0.4 and
the selected assets unchanged. Do not infer a DOI from webhook activation or
from the software tag. Observe the actual Zenodo record, its archived files,
version identity and retrievable checksums before marking archival complete.
P01's separate preprint record remains a separate deposit; P02/P03 remain deferred.
The proof execution checkpoint `3a50b5f50b034319a469b9de68f556be70fff02c`
and the original receipts are not replaced by a distribution commit.

The first useful outcome is one attributable external reproduction attempt or
one technically specific correction, not a target number of views. Record:

- Which proposition and exact version someone attempted to reproduce.
- Whether the attempt succeeded, failed, or remains unresolved, with environment
  and command evidence where available.
- Whether feedback found a source-binding, assumption, proof, or packaging defect.
- Whether another research workflow actually reused an artifact.

Downloads and page views are discovery signals only; they do not identify
unique expert readers or establish reproduction. An AI-assisted check alone
does not establish independent expert review. Independent attestation requires
an appropriately separate reviewer/executor and inspectable evidence.

As a workload limit, try one small, relevant outreach round before expanding.
If no substantive response appears, improve the entry point or reduce the
reviewer's task; do not repeat generic announcements, bypass restrictions, or
interpret silence as either scientific acceptance or rejection.

## 10. Sources and unchecked matters

Official platform documents were inspected on 2026-10-08. The accompanying
[source notes](NSRW_PUBLICATION_AND_REPRODUCTION_PLAN_2026-10-08.sources.json)
separate documented capabilities from strategy recommendations. These sources
do not establish novelty, community acceptance, international demand, or future
reach. Platform rules must be rechecked before execution.

No account login, upload, message, release, or website deployment was performed
while preparing this plan. No scholarly novelty search or external mathematical
review was performed. arXiv and broad-social-channel availability were not
investigated; they are simply not dependencies of this plan.
