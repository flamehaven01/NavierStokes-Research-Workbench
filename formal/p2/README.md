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
P2-C02  generic and fixed-Profile actual coefficient decomposition equalities
P2-C03  actual coefficient zero product identity, positivity at zero, continuity
P2-C04  per-Profile existential radius: 0 < eta < epsilon(F) -> actual c1(eta) > 0

P2-Z-core source-facing per-Profile small-positive-eta interior M-zero
P2-Z+J    conditional first-window local M-zero + c1>0 -> local J>0
          source-facing same-point Profile.M=0 and Profile.J>0

Compiled supporting dependency modules:
Z01–Z03 mass identities, boundary signs and conditional IVT

Next work (not another mathematical admission):
Public reproduction package / technical-note scope review; separate authorization
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
actual `c1(0)` or `c1(eta)` positivity. C02's separate
[2026-10-07 commit-bound receipt](../../docs/stage_receipts/P2_C02_COLAB_2026-10-07.md)
admits only two decomposition equalities; it does not admit a sign.

The separate [C03 receipt](../../docs/stage_receipts/P2_C03_COLAB_2026-10-08.md)
confirms the zero product identity, actual coefficient positivity at `eta = 0`,
and continuity as a function of `eta` on all `Real`, for each source `Profile`.
Its execution checkpoint is `d7e41b9b60ae7510e5b4cc67eb5d071df21bd73d`.
`scripts/run-p2-c03-replay.py` builds `+NavierStokes.OutgoingProfile` and freshly
compiles F1, strict L2, L3, D, C01, C02 and C03 in one run. The same Profile's
amplitude and `amp_contDiff` are used; angular-reset and axial coefficients
remain distinct. Metadata stays `NONE / UNVERIFIED`; the receipt records the
subsequent same-session admission, not independent attestation.
That historical C03 receipt does not admit a neighborhood-sign theorem or a
mass zero.

The separate [C04 receipt](../../docs/stage_receipts/P2_C04_COLAB_2026-10-10.md)
confirms only `NSRW.P2.actualSecondRepairCoefficient_pos_small_positive`:
for every fixed `Profile F`, there exists `epsilon(F) > 0` such that
`0 < eta < epsilon(F)` implies actual coefficient positivity. Its execution
checkpoint is `10d5a1f517b8665137f2354746d70752f8ef67fd`.
`scripts/run-p2-c04-replay.py` builds `+NavierStokes.OutgoingProfile` and freshly
compiles F1, strict L2, L3, D, C01, C02, C03 and C04 in one new clean replay.
Source caches are reused; execution and receipt review share a trust domain.
Original metadata remains `NONE / UNVERIFIED`. Neither a uniform/numerical
epsilon nor a mass zero is admitted by C04.

Status refresh 2026-10-12: the [Z-core receipt](../../docs/stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md)
admits `profileM_firstRepair_zero_small_positive`. The separate
[Z+J receipt](../../docs/stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md) admits
conditional local/source J positivity at first-window M-zeros with `c1 > 0`,
and `profileMJ_firstRepair_zero_small_positive` with the same F/eta/r/X witness.
Both use the new preserved run `nsrw-z-phase-replay-20261012T065216884451Z`
at checkpoint `3a50b5f50b034319a469b9de68f556be70fff02c`: fifteen stages exit 0,
fourteen fresh external artifacts, seventeen exact committed inputs, nineteen
Z axiom surfaces, and D: archive crosscheck. Source caches were reused; the
original metadata remains `NONE / UNVERIFIED`. Separate receipts are not
independent attestation. No uniform/numerical epsilon, first/unique zero,
simple-zero, numerical margin, Q pole/limit or application is admitted.
The earlier development records and lost old replay archive remain separate
history; they are not used to assemble the new replay's evidence.

Publication preparation update, 2026-10-13: a held local derivative packages
exact execution inputs and post-execution receipts with bounded summaries.
It does not replace raw private evidence or create a new proof receipt.
The [proposed v0.4.0 notes](../../docs/releases/v0.4.0.md) separate version/tag/
Release preparation from this capsule's immutable execution checkpoint.
Human privacy/rights/content review and public distribution are still held.

## Proof hygiene

`P2_C02_ActualCoefficientDecomposition.lean` implements two source-wrapper
equalities: generic debt-to-affine decomposition, and its second-coefficient
specialization using one fixed Profile's corrected amplitude. It does not
import external F1/L2/L3/D/C01 proof modules. The separate Colab development run
on 2026-10-07 passed `PASS[LOCAL_PROOF_COMPILE:P2_C02]` after pinned environment
restoration. Both named equalities compiled with empty stderr; the original
archive and fresh `.olean` are preserved locally. See the
[development handoff](../../colab/C02_DEVELOPMENT_2026-10-07.md).
The earlier mathlib private-artifact read failure remains debugging history.
The later C-02C replay uses `scripts/run-p2-c02-replay.py` at
`01d2deae3534cba5a035e87ac1cbe37faac470ca`: pinned source ->
`+NavierStokes.OutgoingProfile` -> fresh C02, without external F1/L2/L3/D/C01.
Its two equalities were admitted after separate archive review; no
actual-coefficient sign is promoted by C02. Both development and replay metadata
retain `claim_authority: NONE`; the dated receipt records subsequent admission.
The operational checklist separates implementation, development compile,
and commit-bound closure as C-02A/B/C.

Each module must compile without `sorry`, `admit`, or a newly introduced
axiom.  L1 also emits `#print axioms` output for its two named propositions;
that is a check for introduced proof placeholders, not a semantic proof audit.
A successful compilation establishes only the named Lean proposition under the
pinned source, toolchain, and manifest; it neither verifies the paper as a
whole nor completes P2.
