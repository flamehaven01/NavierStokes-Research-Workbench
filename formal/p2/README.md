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
| Runtime raw SHA-256 | Record actual bytes per executor; do not assume either line-ending equality or difference. |

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
P2-L2-A normalized source representation plus normalized `i = 1` positivity
P2-L2   strict normalized main-moment comparison
P2-L3   cross-multiplied template-moment comparison: k*A1 <= A0
P2-D    source-linked NSRW deltaM negativity plus two debt identities
P2-C01  positive matrix gap, main-only coefficient formula and positivity

Next formal obligations:
C02-C04 actual coefficient decomposition, eta=0/continuity, small-positive-eta sign
L4      small-positive-eta first-repair interior zero
```

The P2-L1 compile gate is satisfied by the dated
[`P2_L1_COLAB_2026-09-12.md`](../../docs/stage_receipts/P2_L1_COLAB_2026-09-12.md)
receipt. The separate P2-F1 gate is satisfied by the clean local Windows
[`P2_F1_LOCAL_WINDOWS_2026-09-13.md`](../../docs/stage_receipts/P2_F1_LOCAL_WINDOWS_2026-09-13.md)
receipt. P2-F1 confirms only the named `mainMoment c 1` positivity
proposition; it does not promote L2--L4.

The dated external [`P2_L2A_COLAB_2026-09-13.md`](../../docs/stage_receipts/P2_L2A_COLAB_2026-09-13.md)
receipt compiles the exact L2-A module against a freshly generated P2-F1
`.olean` in the same pinned executor. It confirms only
`normalizedMainMoment_log_short` and `normalizedMainMoment_one_pos`. The
strict normalized comparison is outside that historical receipt; it does not
close L2 or promote L3--L4.

The separate [`P2_L2_COLAB_2026-10-06.md`](../../docs/stage_receipts/P2_L2_COLAB_2026-10-06.md)
receipt closes strict L2 at NSRW commit `b02002b1ab954e34e7017a45e3afb338b21abfc5`.
For the F1-to-L2 import chain, use `scripts/run-p2-l2-replay.py` from a clean
checkout. It records the source build, freshly generates the external F1
`.olean`, and compiles the L2 module with that dependency in one execution.
It does not install or update dependencies. Source cache reuse is explicit.
That receipt does not promote L3, `DeltaM`, or repair geometry.

The separate [`P2_L3_COLAB_2026-10-06.md`](../../docs/stage_receipts/P2_L3_COLAB_2026-10-06.md)
receipt closes only `exp (-(3/20)*c.lam) * rowMoment (c.exponents 1)
<= rowMoment (c.exponents 0)` at execution commit
`15108c35a2e5df948ece653a7f3fcfa02f3180f8`. Use `scripts/run-p2-l3-replay.py`
from a fresh clean checkout. Its source target is
`+NavierStokes.OutgoingPulseBounds`; it generates a fresh external L3 `.olean`
and does not import external F1/L2 modules. Source cache reuse is explicit.
That historical receipt does not admit composition or downstream repair claims.

The separate [`P2_D_COLAB_2026-10-06.md`](../../docs/stage_receipts/P2_D_COLAB_2026-10-06.md)
receipt confirms `NSRW.P2.deltaM c < 0` and two source-debt identities at
execution commit `06cb400667c433b076599aabadc5d5f9d13f8f24`.
`deltaM` is NSRW shorthand assembled from pinned source objects, not an
upstream declaration name. `scripts/run-p2-d-replay.py` builds the same source
target, freshly compiles F1, strict L2, L3, and D in one execution, and confines
the external dependency search path to the new run artifacts. Source caches
are reused, not independently attested.

The separate [C01 receipt](../../docs/stage_receipts/P2_C01_COLAB_2026-10-06.md)
confirms three main-only propositions at execution commit
`304f2adc3f26310554dfa64a572329b6a7ff8cf8`: a positive exponential gap, the
exact formula `affineCoefficients c 0 1 1 = -deltaM c / gap`, and the main-only
coefficient's positivity. `scripts/run-p2-c01-replay.py` builds the source
target and freshly compiles F1, strict L2, L3, D and C01 in one run. It does
not import stale external artifacts or promote its own claims. This is not
actual `c1(0)` or `c1(eta)` positivity. Actual coefficient decomposition and
small-eta signs, then the first-repair zero bridge, remain open.

## Proof hygiene

Each module must compile without `sorry`, `admit`, or a newly introduced
axiom.  L1 also emits `#print axioms` output for its two named propositions;
that is a check for introduced proof placeholders, not a semantic proof audit.
A successful compilation establishes only the named Lean proposition under the
pinned source, toolchain, and manifest; it neither verifies the paper as a
whole nor completes P2.
