# Changelog

All notable changes to this project are documented here. The project follows
Keep a Changelog conventions and uses semantic versioning for software
artifacts. Research claims retain their separate evidence statuses.

## [Unreleased]

### Added

- Strict bounded JSON parsing with duplicate-key/non-finite-value rejection and
  separate raw-input and canonical semantic digests.
- Versioned v3 M4-P, compiled-evidence, and run-specific provenance schemas.
- Deterministic atomic compiled-receipt writer and live-target build helper.

### Changed

- M4 Support, Cone, and Moment evaluators now reject negative domains, boolean
  numerics, negative margins, duplicate labels, and empty exact identities.
- v2 remains historical replay-only; v3 uses explicit evidence-mode routing.
- README positioning now describes NSRW as a governance and guardrail workbench,
  while future mathematical/CFD/SciML lanes remain non-authoritative.

## [0.2.0] - 2026-09-11

### Added

- Public MIT-licensed repository foundation.
- Cross-platform pytest, coverage, Ruff, compilation, and deterministic replay CI.
- Dedicated Navier--Stokes research gates for source custody, scoped Lean target
  builds, parametric Support/Cone/Moment obligations, and falsification mutations.
- SPAR-backed secondary claim-drift review with an independent fail-closed NSRW gate.
- M4-P obligation manifest schema, portable pilot fixture, CLI, and receipts.
- Hosted scoped Lean evidence for OutgoingDilation, OutgoingCone, and
  NominalConeAssembly, including `.olean` hashes and dependency artifacts.
- M4 contract v2 with source-signature quantifier binding, structured compiled
  receipt verification, baseline-delta mutation verdicts, and fail-closed Cone
  relation/dependency validation. Contract v1 remains retained for replay.
- External 2-D vorticity experiment contract and Colab design surface.

### Changed

- M3 engineering status is separated from the noncomputable selected-source-instance lane.
- Local archive paths were replaced by portable relative paths and environment configuration.
- Generated outputs are excluded from version control; bounded stage receipts remain in docs.
- M4 source-locator hashes now canonicalize CRLF to LF, eliminating checkout
  platform drift without weakening non-line-ending byte custody.

### Security

- Third-party GitHub Actions and the SPAR source dependency are pinned to immutable commits.

## [0.1.0] - 2026-09-10

### Added

- Initial evidence-bound Navier--Stokes research workbench.

[Unreleased]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/releases/tag/v0.2.0
