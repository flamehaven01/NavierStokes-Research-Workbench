# Math Stage M1 Receipt

Status: `GREEN[LOCAL_MATH_KERNEL]__GLOBAL_CLAIM_UNVERIFIED`

## Scope

Implemented the self-similar scaling and residual kernel without modifying the three reference
repositories or the pinned OpenAI formal-source repository.

## Implemented artifacts

- exact `ScalingLaw` exponent derivation and two source-bound certificates;
- viscosity-rescaled velocity, pressure, and force callables;
- divergence, curl, Laplacian, convection, pressure gradient, and forced PDE residual;
- equation-(3.2) similarity-coordinate reconstruction;
- unforced and forced manufactured solutions;
- deterministic CLI receipt with explicit evidence authority;
- positive, boundary, and mutation tests.

## Authority boundary

- Exact exponent equality is `EXACT_EXPONENT_ALGEBRA` for the declared scaling laws.
- Finite-difference samples are `NUMERICAL_DIAGNOSTIC`.
- Similarity solving is `NUMERICAL_RECONSTRUCTION`.
- The global Navier--Stokes claim is `NOT_ESTABLISHED`; `claim_status=UNVERIFIED`.

## Verification

- `PASS[M1:focused-pytest]`: 40 math-kernel tests passed after adding the force-exponent
  mutation (39 passed in the initial focused run).
- `PASS[M1:full-pytest]`: 80 cumulative tests passed on local Python 3.14.3.
- `PASS[M1:coverage]`: 93.33% total coverage passed the configured 90% floor; the new operator,
  scaling, experiment, and manufactured-solution modules each reached 100%.
- `PASS[M1:ruff]`: all source and test files passed.
- `PASS[M1:compile]`: all source modules compiled.
- `PASS[M1:exact-scaling]`: viscosity-rescaling momentum powers all derive to `1/2`, and
  parabolic-scaling powers all derive to `3` using `Fraction` arithmetic.
- `PASS[M1:mutations]`: wrong force, wrong force exponent, and compressible-field controls were
  detected.
- `PASS[M1:manufactured-solutions]`: maximum sampled residual infinity norm
  `7.218425301935838e-09` was below the recorded `2e-06` tolerance; maximum sampled absolute
  divergence was `0.0`.
- `PASS[M1:similarity-reconstruction]`: the sample defining-equation residual was
  `-5.995204332975845e-14` with `|eta| < 1`.
- `PASS[M1:deterministic-replay]`: two independent math receipts were byte-identical; SHA-256
  `505913E2373B9B500F801D7B6335E2806AE6D486354426D9BEABEF9C7CD55DB2`.
- `PASS[M1:source-bound-regression]`: the actual PDF, Markdown, pinned Git commit, paper
  locators, and Lean declaration locators retained pipeline `GREEN`, 5/5 killed mutations, and
  the stable logical fingerprint
  `FD2921283E0999E04A3C103264711A410A08A2BDAE691DEF085D48765B78FAE5`.
- `PASS[M1:slop-rules]`: 13 runtime Python files were analyzed; findings 0, high 0, critical 0,
  unsupported 0, weighted deficit `1.2266758285131574`.
- `UNAVAILABLE[M1:slop-ml]`: no compatible ML model was configured; rule-based evidence only.
- `UNAVAILABLE[M1:lean-build]`: no local Lean/Lake toolchain was installed or claimed.
- `UNVERIFIED[M1:global-claim]`: no global existence, regularity, blowup, or source-paper
  equivalence claim follows from M1.

No commit, push, dependency installation, Lean installation, or release was part of this stage.
Generated receipts remain ignored by Git.
