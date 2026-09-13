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
| `lake-manifest.json` committed Git blob SHA-1 | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Runtime raw SHA-256 | Observational only; record per executor because Windows CRLF and Linux LF checkouts differ. |

Run a module from the pinned source root, not from this repository:

```bash
lake env lean /content/NavierStokes-Research-Workbench/formal/p2/P2_L1_MainPulsePositivity.lean
```

Use `scripts/run-p2-lean-colab.sh` for the fail-closed identity checks,
target-only source build, and captured stdout/stderr.  It builds only
`+NavierStokes.PulseAmplitude` before compiling the external module.  The
runner, proof file, and their shared NSRW revision must be tracked and clean.
It does not run `lake update` unless explicitly asked to bootstrap missing
dependencies. It fails closed on an unapproved manifest change; the sole
bounded bootstrap normalization is restored to the committed Git blob and
rechecked before compilation.

## Current scope

`P2_L1_MainPulsePositivity.lean` proves only these source-bound facts:

1. `mainPulse z >= 0` for `z >= 0`.
2. `mainPulse (1 / 25) > 0`.

Those facts establish a positive point of the pulse. They do **not by
themselves** establish the weighted integral `F1 > 0`; that required a
separate integrability and positive-subinterval argument in P2-F1.
Consequently, compiling P2-L1 does not promote the current P2 comparison or
first-repair-zero claims.

The completed and next formal obligations are deliberately named separately:

```text
Completed:
P2-L1  pulse nonnegativity plus a positive point
P2-F1  weighted main-moment positivity: `0 < mainMoment c (1 : Fin 2)`

Next formal obligations:
L2      normalized main-moment comparison
L3      template moment-ratio comparison
L4      small-positive-eta first-repair interior zero
```

The P2-L1 compile gate is satisfied by the dated
[`P2_L1_COLAB_2026-09-12.md`](../../docs/stage_receipts/P2_L1_COLAB_2026-09-12.md)
receipt. The separate P2-F1 gate is satisfied by the clean local Windows
[`P2_F1_LOCAL_WINDOWS_2026-09-13.md`](../../docs/stage_receipts/P2_F1_LOCAL_WINDOWS_2026-09-13.md)
receipt. P2-F1 confirms only the named `mainMoment c 1` positivity
proposition; it does not promote L2--L4.

`P2_L2_NormalizedMainMomentComparison.lean` is an included scaffold, not a
compiled L2 result. It has not yet received a successful external-module
compile receipt. The next execution obligation is to compile the exact L2-A
bytes against a freshly generated P2-F1 `.olean` in the same pinned executor.

## Proof hygiene

Each module must compile without `sorry`, `admit`, or a newly introduced
axiom.  L1 also emits `#print axioms` output for its two named propositions;
that is a check for introduced proof placeholders, not a semantic proof audit.
A successful compilation establishes only the named Lean proposition under the
pinned source, toolchain, and manifest; it neither verifies the paper as a
whole nor completes P2.
