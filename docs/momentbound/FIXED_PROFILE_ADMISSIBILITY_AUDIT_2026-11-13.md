# Fixed-tuple source Profile and amplitude — admissibility audit

Date: 2026-11-13 (Asia/Bangkok)
Status: `HELD[FIXED_PROFILE_NOT_CONSTRUCTED]`; **source-interface review**, no new theorem, execution or claim admission.

## Pin and admitted anchors

- Upstream: `openai/NavierStokesAndEuler` commit
  `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- `NavierStokes/OutgoingSchedule.lean`: `Parameters`, `paperParameters`.
- `NavierStokes/OutgoingTail.lean`: `TailData`.
- `NavierStokes/UniformAngularReset.lean`: `ResetWitness`,
  `exists_scheduled_reset`.
- `NavierStokes/CorrectedPulseAmplitude.lean`: `amplitude_spec`,
  `exists_corrected_amplitude`.
- `NavierStokes/OutgoingProfile.lean`: `Profile`, `Specification`,
  `exists_profile_for_data`, `exists_outgoing_profile`,
  `Profile.J_at_exp`.
- NSRW admitted: `mb_fixed_coarse_pos`,
  `mb_actualSecondRepairCoefficient_fixed_pos` (MB-05 receipt),
  `mb_normalizedAngularMoment_gt_coarse_mul_ratio` (MB-06 receipt);
  `exists_firstRepair_zero_of_secondCoeff_pos` (Z03 receipt scope).

## Exact selected tuple

```text
P = 1; m = 1
lambda = 1/1000000000000
eta = 1/1048576 (>0, eta^2<=1)
h = lambda/4 (>0, 2*h<lambda)
wait = 60 * log(1/lambda)
K/reset = NOT ASSIGNED
```

The core `Parameters` and a `TailData` with `h=lambda/4` are
*mathematically admissible elementary objects*: positive P, m and lambda,
lambda<1/10, h>0, 2h<lambda, and the paperParameters wait relation.
This document does **not** contain a newly compiled Lean construction for
that fixed `TailData`.

## Source theorem path and missing gate

`OutgoingProfile.exists_outgoing_profile` produces
`∃ lam0 C, 0<lam0 ∧ 0<C ∧ ∀ lam, 0<lam → lam<lam0 → ... ∃ Profile F`
with a matching `Specification F C`. It does **not** assert
`1/10^12 < lam0`. `exists_fixed_lambda` selects its own lambda after
lam0; it does not identify the selected lambda as `10^-12`.

The proof uses `CorrectedPulseAmplitude.exists_corrected_amplitude`,
which in turn uses `exists_scheduled_reset` and a rate threshold.
These yield existential smallness thresholds and a positive reset constant
K; they do not provide a numerical K or a lower enclosure for the common
threshold suitable for this fixed tuple.

More direct `CorrectedPulseAmplitude.amplitude_spec` requires:

```text
w : ResetWitness d K
0 < K
d.core.lam <= 1/120
d.core.wait = 60*log(1/d.core.lam)
combinedScale d K <= 1/1000
eta^2 <= 1
```

For a `Profile F`, `F.reset` is the reset tied to *that same F.data*,
and `F.amp` uses `F.reset.coefficients`. A bound for a different
reset, arbitrary `K`, or an unattached numerical sample does not
satisfy the source theorem. The fixed lambda does satisfy the elementary
`<=1/120` condition; **`combinedScale d K<=1/1000` and a matching
witness remain undischarged**.

An alternative logical route, **conditional on an existing**
`Specification F C`, is its `amplitude_bounds` field: since
`(2^-20)^2<=1`, it directly supplies
`9/10 < F.amp (2^-20)`. This is not a construction of that
Specification or Profile.

## Do not require a computed root for an existential bound

If there is an actual fixed-tuple `Profile F` and its actual amplitude
satisfies `9/10<F.amp(2^-20)`, then the *admitted* MB-05 theorem yields
`actualSecondRepairCoefficient F (2^-20)>0`.

Using `localSecondRepairCoefficient_eq_actual` and
`Z03.exists_firstRepair_zero_of_secondCoeff_pos` with `eta=2^-20>0`
gives an **existential** `r` in
`(F.data.core.lower 0, F.data.core.upper 0)` with
`localMass F eta r=0`. MB-06 can then apply at this same `r`
and `F`, with `mb_fixed_coarse_pos`, to yield the strict normalized
local-angular-moment lower bound at some point.

That composition is a **proposed short Lean wrapper**; it has not been
added, compiled or admitted as a new standalone proposition here.
It requires neither a numerically located root nor a new axiom.

If instead the target is a *numerically located* root or a numerical
source `Profile.J` at a named `X`, a validated root enclosure,
the correct `X=exp(c.pulseStart)*r` coordinate, and the remaining
positive scale `K1`/source evaluation are further obligations.
`Profile.J_at_exp` supplies the qualitative coordinate identity,
not a numerical certificate.

## Decisions and falsifiers

| Item | State | Close only with |
| --- | --- | --- |
| Exact fixed core/tail arithmetic | `CHECKABLE`, no new Lean wrapper | Source-typed construction and compile if this becomes an admitted claim |
| Fixed-lambda source Profile nonemptiness | `HELD` | An explicit, source-justified threshold proving `10^-12<lam0` or a separate valid fixed-tuple construction |
| Same-reset amplitude lower bound | `HELD` | Source witness / `Specification` for the very same `F`, or direct checked `amplitude_spec` premises |
| First-window root existence | `CONDITIONAL_DERIVABLE` | Fixed F and actual positive c1; apply Z03 with `eta>0` |
| Root numeric localization | `NOT PERFORMED` | Validated continuous-function endpoint/root enclosure for that actual F |
| Normalized local J bound | `CONFIRMED_CONDITIONAL` | The MB-06 receipt's exact hypotheses |
| Numerical `Profile.J` at a named X | `HELD` | Source instance, same-point root/coordinate and quantitative scale/evaluation |

**Do not** infer `10^-12<lam0` from “sufficiently small.”
**Do not** replace missing K/reset with a guessed finite value.
**Do not** retune lambda after a failed test without a new declared
experiment and a new fixed-rational proof/input contract.

This review does not modify upstream material, admitted proofs,
receipts, ledger or original run metadata.
