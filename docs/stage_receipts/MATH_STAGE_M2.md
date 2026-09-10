# Math Stage M2 Receipt

Status: `GREEN[LOCAL_ANALYTIC_SPINE]__SOURCE_PROFILES_NOT_INSTANTIATED`

## Scope

Implemented the concentrating leading-field interface and bounded analytic obligations from
primary-PDF pages 7--9. The paper's actual constructed profiles remain uninstantiated.

## Implemented artifacts

- exact affine-in-`h` exponent ledger and generated correction orders;
- source-shaped `(E,U,V0,Pi)` profile interface;
- cylindrical-to-Cartesian leading-field and pressure evaluators;
- core membership and stress-region classification;
- sampled incompressibility and radial pressure-balance obligations;
- fixed-similarity-coordinate growth and finite residual-order diagnostics;
- wrong-exponent, wrong-pressure, non-divergence-free, and asymptotic-overclaim mutations;
- deterministic M2 CLI receipt.

## Authority boundary

- Exponent operations: `EXACT_SYMBOLIC_ALGEBRA`.
- Local PDE obligations: `SAMPLED_NUMERICAL_DIAGNOSTIC`.
- Asymptotic checks: `FINITE_ASYMPTOTIC_SAMPLE_NOT_PROOF`.
- Fixture: `MANUFACTURED_DIAGNOSTIC_NOT_SOURCE_PROFILE`.
- Source profiles: `NOT_INSTANTIATED`.
- Global claim: `NOT_ESTABLISHED`; `claim_status=UNVERIFIED`.

## Verification

- `PASS[M2:focused-pytest]`: 35 M2 tests passed.
- `PASS[M2:full-pytest]`: 115 cumulative tests passed on local Python 3.14.3.
- `PASS[M2:coverage]`: 94.74% passed the configured 90% floor; all five new runtime modules
  reached 100% coverage except the CLI guard line.
- `PASS[M2:ruff]`: all source and tests passed.
- `PASS[M2:compile]`: all source modules compiled.
- `PASS[M2:ci-yaml]`: the two-job workflow parsed after analytic replay was added.
- `PASS[M2:exponent-ledger]`: all source-inspected powers were derived from exact affine
  expressions at `h=1/200`; the axial-diffusion exponent mutation was killed.
- `PASS[M2:local-obligations]`: manufactured-profile incompressibility residual `0.0`, radial
  pressure-balance residual `-6.922160622480078e-10` under tolerance `1e-05`, and fixed-`X`
  growth-ratio absolute error `4.063416270128073e-14`.
- `PASS[M2:asymptotic-overclaim]`: the supported finite sample normalized to `3.0` under bound
  `3.01`; the stronger mutated power produced `3000000.000000001` and failed its bound.
- `PASS[M2:deterministic-replay]`: contract, M1 math, and M2 analytic receipts were each
  byte-identical across two executions. M2 receipt SHA-256:
  `EBF7A786AD2A39E356A9D8A33AFA1111BA58C7C9A59CFC6C9EE619B10446A015`.
- `PASS[M2:source-bound-regression]`: pipeline `GREEN`, claim `UNVERIFIED`, 5/5 original
  mutations killed, fingerprint
  `FD2921283E0999E04A3C103264711A410A08A2BDAE691DEF085D48765B78FAE5`.
- `PASS[M2:slop-rules]`: 18 runtime Python files analyzed; findings 0, high 0, critical 0,
  unsupported 0, weighted deficit `0.9244088181379055`.
- `UNAVAILABLE[M2:slop-ml]`: no compatible model was configured; it was not used for GREEN.
- `UNVERIFIED[M2:source-profile-obligations]`: the actual profiles constructed by the paper
  have not been extracted or evaluated.
- `UNVERIFIED[M2:global-claim]`: M2 establishes no existence, regularity, blowup, or semantic
  equivalence result.

No dependency, commit, push, Lean installation, deployment, or release was performed.
