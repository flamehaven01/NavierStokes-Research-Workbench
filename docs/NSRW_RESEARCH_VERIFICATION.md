# Research verification in NSRW

P0 defines the mathematical object, hypotheses, domain and reference inputs.
P1 chooses a check and explains which errors it can detect.
P2 registers the check with a stable identifier and revision.
P3 runs a positive control, a relevant deliberate error and the retained
research input when it is available.

The shared runner records named input digests, check revision, method,
domain, evidence class and result. A new evaluator implements
`evaluate(evidence) -> Finding` and declares its input names in a
`Verification`. Register it in the CLI's `CHECKS` table to expose it on the
command line. A changed criterion gets a new revision. When comparing
algorithm versions, supply their exact records as named inputs and keep
the test cases, tolerances and reference method fixed.

| Use | Required reference | Result scope |
| --- | --- | --- |
| Exact algebra or inverse calculation | Independently fixed system, identities or exact solution | Exact residuals within the supplied model and input |
| Interval computation | Pinned inputs, outward enclosure and a distinct arithmetic method where feasible | Containment or a certified bound at the tested inputs |
| PDE model or numerical solver | Equation, boundary and initial conditions, error measure and test domain | Analytic manufactured controls and sampled diagnostics. For solver comparisons, also record mesh, time-step refinement and the error norm |
| Lean result | Exact source, declaration, toolchain and replay evidence | Record inspection and live kernel execution have distinct evidence classes |

A common result format lets further models and algorithms use their own
mathematical checks. `FAIL` reports a mismatch. `UNRESOLVED` reports an
inconclusive mathematical check. `ENV_BLOCKED`, `NOT_RUN` and `ERROR`
identify dependency, input and execution problems. A successful report
is scoped to its evidence class and carries no claim admission authority.

## Initial applications

- **MB-08 inverse** checks nine exact rational controls, including coherent
  row and pressure-factor mutations, with the original source file pinned.
- **MB-06 ratio** tests the retained normalized factor enclosure with a
  second interval algorithm.
- **Forced shear** checks the Navier–Stokes momentum and divergence
  implementation at one point against an analytic manufactured solution.
  Removing the force changes the predicted momentum residual from zero to
  `(0.75,0,0)`.
- **P1 Lean margins** checks the retained commit-bound archive for the two
  quantitative-margin modules. It rehashes the inventory of 25 members,
  checks six recorded stages and ten declarations, and pins the printed
  signatures of the two headline theorems. A regression fixture removes
  the mass-zero hypothesis and repacks the archive with consistent hashes.
  The signature check rejects it. The recorded check runs without Lean.
  [P1 dated receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md)

All four cases passed in the local run, and repeating them reproduced
their retained JSON reports byte for byte after normalizing possible
Windows stdout line endings. The NSRW suite passed 818 tests with 3 skips,
22 passing subtests and 90.66% line coverage.

Run the installed command from the NSRW root. The inverse case additionally imports local FHVAL, and the interval
case uses the existing `mpmath==1.3.0` dependency.

```powershell
nsrw-verify forced-shear --input fixture=examples/research-verification/forced-shear.json
nsrw-verify mb06-ratio --input record=examples/research-verification/mb06-ratio-20261113.json
nsrw-verify mb08-inverse --input source=external_sources/related-repos/openai/NavierStokesAndEuler/NavierStokes/AngularMomentReset.lean
nsrw-verify p1-lean-margin --input "archive=path/to/local-P1-replay.zip"
```

Use `--output` to retain a new JSON result. The historical P1 bundle is
private evidence. A local copy with the receipt's SHA-256 is required to
run that check. New theorem or solver checks require their own reference
criteria when registered.


## Post-run input custody correction (14 November 2026)

The first generic runner passed four scoped cases, but a separate synthetic
falsification revealed that an evaluator could modify the input dictionary
before the original implementation computed its SHA-256. The engine
incorrectly reported `PASS` with a digest of the modified input rather
than the originally submitted bytes.

The engine now snapshots exact `bytes` values and computes their digests
**before** executing the checker. It provides the evaluator a read-only
mapping. Attempted mutation produces `ERROR`; wrong evidence types
cannot pass. Added regressions check original-hash preservation and
reject mutable/non-bytes evidence. Path-not-found is `NOT_RUN`;
permission/read-environment failures are `ENV_BLOCKED`.

## Execution manifests

Install the command with `python -m pip install -e ".[verification]"`.
For example:

```shell
nsrw-verify forced-shear --input fixture=examples/research-verification/forced-shear.json --output outputs/shear.json --manifest outputs/shear-manifest.json
```

The manifest binds the report digest and input digests to the selected
implementation files, observed runtime and available package metadata.
The runner compares those identities before and after executing the
check. If a required implementation file or the pinned interval
dependency identity is unavailable, the command exits with code 2
before emitting the report or manifest. The inverse checker can use
a local source checkout, whose implementation file is hashed.
A package RECORD digest identifies installed metadata and is
not a fresh integrity check of every file in that package. A manifest
records a local execution and is not an independent attestation.
CI runs the installed shear and interval checks using tracked examples.
The private Lean archive and local inverse backend have separate local
reproduction commands.
