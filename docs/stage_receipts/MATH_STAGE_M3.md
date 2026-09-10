# Math Stage M3 Receipt

Status: `HELD_SOURCE_INSTANCE__M4_HELD`

## Delivered

- Equation (4.6) radial-average evaluator with explicit axis extension.
- Equation (4.7) `V0` derivation from `U`, `h`, and averaged `U`.
- Equation (4.25) canonical pressure evaluator with an explicit tail integral.
- Closed `LeadingProfiles` adapter that prevents independent `V0`/`Pi` drift.
- Static paper–Lean crosswalk and machine-readable missing-link register.
- Deterministic M3 receipt and negative controls for invalid axis/tail behavior.

## Verification

- `PASS[M3:full-pytest]`: 151 tests passed.
- `PASS[M3:coverage]`: 93.71% against the configured 90% floor.
- `PASS[M3:ruff]`: all source and test checks passed.
- `PASS[M3:compile]`: all source modules compiled.
- `PASS[M3:source-contract]`: exact Fraction `h` with `0<h<1/100`; explicit
  `X=0` pressure limit; one-sided endpoint derivatives.
- `PASS[M3:closure-replay]`: radial-flux and pressure-balance samples passed;
  the receipt is byte-stable across repeated runs (SHA-256
  `6EA0A9C2E449BAB6A9FA3E8E69E526DD07C33784924FD1F64DF75E4C950519FC`).
- `PASS[M3:missing-link-regression]`: the presumed missing `V0` Lean relation
  is classified `FALSIFIED_AS_MISSING` because `SlowDivergence.radialFlux` is
  present.
- `PASS[M3:ci-replay-definition]`: CI now runs and byte-compares two M3 receipts.
- `PASS[M3R-1:compiled-target]`: the pinned Lean `4.34.0-rc2` toolchain was
  provisioned and `lake build +NavierStokes.OutgoingDilation` completed
  successfully (`2856/2856` jobs). The target `.olean` and direct compiled
  dependencies were captured in the M3R receipt.
- `PASS[M3R-1:theorem-axioms]`: six canonical declarations were checked with
  `#print axioms`; no `sorryAx` was reported.
- `ERROR[M3:default-library-build:ENV_IO/OOM]`: the broad default
  `NavierStokes` target remains environmentally unstable under parallel cache
  reads. This is kept separate from the successful scoped M4 prerequisite.
- `PASS[M3:static-theorem-dependency-surface]`: all 6/6 required declarations
  are present under static source inspection. This is not a compiled dependency
  graph or Lean proof-validity result.
- `PASS[M3:parametric-tail-witness]`: independent log-coordinate quadrature
  against source `canonicalKernel`, `Pi_canonical`, `powerTail`, and
  `E_tail_factorization` matches the parametric source pressure tail, including
  the `-1/2` pressure factor (absolute integral error
  `6.233347171757941e-13`).
- `HELD[M3R-2:source-instance-tail]`: the concrete noncomputable `TailData`
  amplitude/radius were not evaluated by Lean, so the parametric witness is not
  promoted to a source-instance closure.
- `UNVERIFIED[M3:theorem-4.6-semantic-equivalence]`: declaration presence does
  not establish the full quantitative conjunction or its source equivalence.

## Transition

M4 must not begin yet. The scoped compiled Lean prerequisite is now verified,
but the concrete source-instance tail evaluation and full paper–Lean semantic
equivalence remain open. Resolve the required source-instance boundary before
entering M4. The global Navier–Stokes claim remains `UNVERIFIED`.

Canonical evidence receipt: `outputs/m3-evidence-execution.json`, SHA-256
`3253664E2EA3A13C9678BBC7629130473309708CDA93AB574ED1CE8090985AD5`.

M3R execution receipt: `docs/M3R_EXECUTION_RECEIPT_2026-09-10.md`, SHA-256
`3C0C43EBEFCAE55A3AAD952C36E4AFBE5FD6DB57B3E3CEA3E6E2A1199B9038B9`.
