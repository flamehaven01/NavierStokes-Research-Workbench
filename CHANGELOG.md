# Changelog

All notable changes to this project are documented here. The project follows
Keep a Changelog conventions and uses semantic versioning for software
artifacts. Research claims retain their separate evidence statuses.

## [Unreleased]

### Fixed

- Reconciled public v0.2.3 status with the final tagged commit and hosted run,
  while preserving the earlier release-candidate receipt as historical evidence.

## [0.2.3] - 2026-09-12

### Added

- A shared strict-JSON and JSON-Schema admission path for M4 manifests, Lean
  build requests and receipts, migration records, provenance envelopes, and
  mutation metadata.
- A LIVE-only compiled-evidence v2 contract that binds each `.olean` artifact
  and generated dependency file by safe relative path and SHA-256.
- Fourteen committed, hashed pre-mutated M4 JSON manifests, consumed by the
  Python verifier and available to future independent implementations.
- A final hosted LIVE receipt from run `34666375341`, including runtime-derived
  provenance, three target-specific Lean records, three dependency-file
  digests, and a 14/14 applicable mutation result.

### Changed

- M3 command exit status now follows the recorded Lean result: `0` for PASS,
  `1` for an executed failure, and `2` for an execution error.
- Hosted build classification is derived from the bounded GitHub Actions
  runtime identity; local execution produces only isolated-local authority.
- Support interval boundaries and Cone dependency ordering are explicit,
  executable v3 contract fields.
- Exact rational limits are enforced independently for numerator and
  denominator, at 256 digits each.
- LIVE verification re-reads and hashes dependency files as well as `.olean`
  files; replay does not claim current local artifact presence.
- README now separates implemented capability from future research directions.
- The post-implementation closure audit is recorded in
  `docs/V0.2.2_AUDIT_PATCH_TO_V0.2.3_CLOSURE.md`.

## [0.2.2] - 2026-09-11 [NOT RELEASED]

This implementation checkpoint passed hosted run `34579077366` but was
superseded by the v0.2.3 post-implementation audit before a tag or release was
published.

### Added

- Strict bounded JSON parsing with duplicate-key/non-finite-value rejection and
  separate raw-input and canonical semantic digests.
- Versioned v3 M4-P, compiled-evidence, and run-specific provenance schemas.
- Deterministic atomic compiled-receipt writer and live-target build helper.
- A source-bound v3 replay pilot and language-neutral 14-case staged mutation
  oracle metadata with full-manifest/direct-evaluator expectations.
- An additive M3 historical tombstone for the former PATH-presence execution
  assertion.

### Changed

- M4 Support, Cone, and Moment evaluators now reject negative domains, boolean
  numerics, negative margins, duplicate labels, and empty exact identities.
- v2 remains historical replay-only; v3 uses explicit evidence-mode routing.
- README positioning now describes NSRW as an open research-lab workbench,
  while future mathematical, CFD, and SciML directions remain non-authoritative.
- Lean receipt generation, dependency normalization, observed `.olean`
  discovery, live-manifest creation, and CI provenance are owned by
  `nsrw.lean_receipt` rather than inline workflow Python.
- Relative Lean source and dependency roots are normalized before artifact and
  source paths are recorded, matching hosted checkout layouts.
- M3 compiled PASS now requires an executed subprocess with a zero exit code.

## [0.2.0] - 2026-09-11

### Added

- Public MIT-licensed repository foundation.
- Cross-platform pytest, coverage, Ruff, compilation, and deterministic replay CI.
- Dedicated Navier--Stokes validation for source traceability, scoped Lean target
  builds, parametric Support/Cone/Moment obligations, and falsification mutations.
- A secondary structural consistency check using a pinned dependency, which cannot
  override required NSRW validation.
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
  platform drift without weakening non-line-ending byte identity checks.

### Security

- Third-party GitHub Actions and the optional structural-check source dependency
  are pinned to immutable commits.

## [0.1.0] - 2026-09-10

### Added

- Initial evidence-bound Navier--Stokes research workbench.

[Unreleased]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/compare/v0.2.0...v0.2.3
[0.2.2]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/commit/447e86347a150bfa98e3bc5c6a61bc07c1c6223c
[0.2.0]: https://github.com/flamehaven01/NavierStokes-Research-Workbench/releases/tag/v0.2.0
