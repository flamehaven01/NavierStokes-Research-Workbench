# Publication selections

## Current selection - 31 October 2026

P01 v0.5 and P02 v0.6 are versioned under `versions/`, each with Markdown, standalone LaTeX, PDF and a separate checksum manifest. Zenodo preprints are [P01](https://doi.org/10.5281/zenodo.23835054) and [P02](https://doi.org/10.5281/zenodo.23835112). Software v0.5.0 includes the exact-rational core-scalar prototype and public example JSON. The GitHub research site copies only the explicit allowlist in `scripts/build-research-site.py`. Original v0.4/v0.5 paper assets, historical tags and formal execution checkpoints are preserved. P03, local reviews, raw logs/metadata/binaries, credentials and private archives are excluded. The earlier selections below are historical records.


## P02 addition — 28 October 2026

The second manuscript selection is *From Source-Bound Proofs to Reproducible
Research Artifacts: An NSRW Case Study*, version 0.5. It includes only:

- `P02_SourceBound_ReproducibleResearch.md`;
- `latex/P02_SourceBound_ReproducibleResearch.tex`;
- `pdf/P02_SourceBound_ReproducibleResearch.pdf`;
- `SHA256SUMS-P02-v0.5`, identifying those three files.

The paper retains the October 12 reference replay and October 14 software-test
observations as dated evidence. Its updated distribution section identifies the
already published software/P01 assets and distinguishes the later P1 extension.
It does not supply new Lean execution, independent reproduction or a numerical
certificate. The paper uses CC BY 4.0; software remains MIT. P03 and internal
review records remain excluded. No historical software tag or P01 asset is replaced.

## First selection: NSRW software and P01

Selection date: 14 October 2026.

The first publication selects one mathematical manuscript:

1. *A First-Repair Mass Zero Without Angular-Moment Cancellation*, v0.4.

The authored P01 manuscript uses CC BY 4.0. NSRW code retains MIT. This selection
is not an upload, DOI assignment, repository release or external review.

### Included in the first candidate

- The current P01 Markdown manuscript and the manuscript license notice.
- One standalone LaTeX source, one exported PDF, and typesetting instructions.
- The reproduction guide and selected documentary development history.
- Seventeen exact committed proof/driver inputs from execution revision
  `3a50b5f50b034319a469b9de68f556be70fff02c`.
- Two unchanged post-execution receipt snapshots, each with its own identity.
- A bounded replay index, stage summary, nineteen selected axiom lines and
  the transformation inventory describing the distributed evidence subset.
- The NSRW MIT license and member checksum manifest.

The P01 PDF is compiled with Tectonic 0.17.0 using locally cached TeX resources.
Its final typesetting is checked separately from the original proof execution.
Its identity is listed separately from the Markdown and LaTeX sources in
`SHA256SUMS-P01-v0.4`.
This typesetting check is not a new Lean replay or independent mathematical review.

### Excluded from the first selection

- P02 and P03 manuscripts, which remain later publication/revision tasks.
- Internal manuscript reviews, preparation records, tool reports and local helpers.
- Raw runtime metadata/logs, compiled `.olean` files, caches and private archives.
- Unissued DOI links, unpublished asset URLs and claims of independent reproduction.

The original archive and earlier candidates are preserved. This revised package
has its own inventory and checksum; it is not silently relabeled as an earlier
candidate. Author publication authorization and content/privacy/redistribution
inspection remain separate from file-integrity checks and independent reproduction.
