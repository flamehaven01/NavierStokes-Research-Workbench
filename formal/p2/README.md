# P2 Lean reproduction capsule

This directory contains external Lean modules for the narrow P2-C analysis.
It is deliberately **not** a Lean project and does not carry a `lakefile` or a
dependency manifest.  The build authority is the pinned
`openai/NavierStokesAndEuler` source checkout named below.

## Pinned environment

| Field | Required value |
| --- | --- |
| Source repository | `https://github.com/openai/NavierStokesAndEuler` |
| Source commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| `lake-manifest.json` SHA-256 | `d8d5387db4bfe8dcdd867d1c4979d2911f194dfe8dae3012463c620e19c6001f` |

Run a module from the pinned source root, not from this repository:

```bash
lake env lean /content/NavierStokes-Research-Workbench/formal/p2/P2_L1_MainPulsePositivity.lean
```

Use `scripts/run-p2-lean-colab.sh` for the fail-closed identity checks,
target-only source build, and captured stdout/stderr.  It builds only
`+NavierStokes.PulseAmplitude` before compiling the external module.  The
runner, proof file, and their shared NSRW revision must be tracked and clean.
It does not run `lake update` unless explicitly asked to bootstrap missing
dependencies, and it rejects a changed manifest.

## Current scope

`P2_L1_MainPulsePositivity.lean` proves only these source-bound facts:

1. `mainPulse z >= 0` for `z >= 0`.
2. `mainPulse (1 / 25) > 0`.

Those facts establish a positive point of the pulse.  They do **not** yet
establish the weighted integral `F1 > 0`; that requires a separate
integrability and positive-subinterval argument.  Consequently, compiling L1
does not promote the current P2 comparison or first-repair-zero claims.

The intended proof order remains:

```text
L1  pulse nonnegativity plus a positive point, then F1 > 0
L2  normalized main-moment comparison
L3  template moment-ratio comparison
L4  small-positive-eta first-repair interior zero
```

L2--L4 source files are intentionally deferred until L1 has a captured
compiled receipt.  This prevents uncompiled placeholders from being mistaken
for formalized results.

## Proof hygiene

Each module must compile without `sorry`, `admit`, or a newly introduced
axiom.  L1 also emits `#print axioms` output for its two named propositions;
that is a check for introduced proof placeholders, not a semantic proof audit.
A successful compilation establishes only the named Lean proposition under the
pinned source, toolchain, and manifest; it neither verifies the paper as a
whole nor completes P2.
