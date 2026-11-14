# MB-08 source cutoff derivative bound

14 November 2026. Status `HELD[SOURCE_CUTOFF_NUMERIC_JET_UNAVAILABLE]`.
This audit concerns the original cutoff at upstream commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` and Mathlib commit
`85e3a25e006c35636f0e53b0e9296caca2685bc0`.

## What the original definition gives

`SmoothCutoffs.cutoffBump` fixes the two radii. Mathlib's
`ContDiffBump.toFun` evaluates the base returned by
`someContDiffBumpBase`, defined as `Nonempty.some hb.out`.
`HasContDiffBump` is a proposition whose field asserts that a base exists.
The inner-product instance supplies an explicit witness via
`ofInnerProductSpace`. Its use to prove nonemptiness supplies no equality
between the result of the classical choice and that witness.
[Mathlib bump interface](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/Calculus/BumpFunction/Basic.lean)
· [Inner-product witness](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/Calculus/BumpFunction/InnerProduct.lean)

The original source gives an existential derivative bound in
`cutoff_iteratedDeriv_bounded` and an existential multiplier in
`relative_first_jet_bound`. The inspected declarations give no numerical
upper bound on either witness or a source-level equality identifying the
selected cutoff. The source's `OutgoingTail.stepBound` concerns
`OutgoingSchedule.sigma`, a different function.
[Source cutoff bounds](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/SmoothCutoffs.lean)
· [Reset jet bound](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/AngularMomentReset.lean)
· [Step bound](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingTail.lean)

## Why the interface cannot give a numerical bound

Let `b(R,x)` be the explicit inner-product base on the real line. For
each positive integer `n`, the family `b_n(R,x)=b(R,x)^n` satisfies
all the base fields. Powers preserve the range, symmetry, joint smoothness
in `(R,x)`, the plateau at 1 and the exact open support. The corresponding
normalized cutoff at the original radii is
`f_n(x) = smoothTransition(2-2*abs(x))^n`.

Fix any `M>0`. Choose `0<h<min(1/2,1/(2*M))` and set
`x_0=1/2`, `x_1=1/2+h`. Then `f_n(x_0)=1`. At `x_1` the
explicit transition is strictly between 0 and 1. For sufficiently large
`n`, `f_n(x_1)<1/2`. The mean value theorem gives an interior
point with `abs(f_n')>(1/2)/h>M`. Translating and scaling this cutoff
into the first reset bump multiplies its derivative by `20/3`.
Taking coefficients `(1,0)` makes the relative perturbation equal to
that bump with coefficient norm 1. Thus no single numerical multiplier
for the reset jet follows from the base fields alone. This is a
mathematical interface argument. The derivative of the particular
classically chosen function still has some finite bound by compactness.
[Transition values and smoothness](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/SpecialFunctions/SmoothTransition.lean)

## Consequence for the fixed tuple

The prior exact budget `D ≤ 10^324/648000` is sufficient for the
jet estimate obtained from the conservative coefficient bound
`162000*lambda^28`. Tightening the debt estimate can enlarge this
budget. Any finite budget still requires a numerical estimate for the
actual chosen cutoff. Inverse and quadratic operator bounds use the
base fields and can be formalized independently of the jet estimate.
[MB-08 analytic bounds and development runs](MB08_FIXED_RESET_BOUNDS_2026-11-14.md)

An identity-preserving fixed-lambda reset would require a new quantitative
result for the exact chosen function, an applicable identity lemma, or a
different proof of the actual reset's small jets that avoids a numerical
bound for the full cutoff derivative. The explicit inner-product bump
provides a candidate for a derived construction. Its derivative bound
applies to that construction once its operator and reset equations are
bound to the explicit bump. A later amplitude proof must use the
corresponding energy polynomial and reset.

## Original quadratic operator development compile

`NSRW.P2.mb_source_quadraticCLM_norm_le_one` proves
`‖quadraticCLM lam‖ ≤ 1` for `0 ≤ lam ≤ 1/10`. The proof uses the
source bump supports and value bounds, with no cutoff derivative estimate.
It supplies the quadratic operator inequality used by the reset
construction.
[Lean module](../../formal/p2/P2_MB08_QuadraticBound.lean)

- Status `PASS[LOCAL_PROOF_COMPILE:MB08_QUADRATIC_BOUND]`
- Run `mb08-quadratic-20261114T031902113956Z` on Lean `4.34.0-rc2`
- Proof SHA-256 `eaf811f995154e45c83906321a7869252721d90dffea160051d2b6c99dd0da8e`
- Exit 0 with empty stderr. The declaration uses `propext`,
  `Classical.choice`, and `Quot.sound`.
- Colab archive `/content/mb08-quadratic-20261114T031902113956Z.zip`,
  180,503 bytes, SHA-256
  `f1f79a8ebcd5b6a29ecc2ff11dc826439daf8a55bd190f37af1b4a843bb1f5b6`.
  The runtime reopened the archive and checked CRC and the four
  input/output digests against its metadata. Drive was unmounted.
  The in-app download did not yield a verifiable local copy.
- Claim status `UNVERIFIED`.

## Original inverse operator and fixed reset development compile

`mb_source_linear_inverse_norm_le_1000` bounds the inverse of the
original `linearEquivNonneg` for `0 ≤ lam ≤ 1/10`. The proof uses
the actual exponential template moments, bounded between `3/40` and
`3/5`. Direct elimination in the two normalized matrix rows bounds the
absolute values of the inverse coordinates by `77 * ‖x‖` and
`21 * ‖x‖`, respectively, in the proof of the requested `1000 * ‖x‖`
max-norm bound. The derivation uses support and plateau properties.

`mb_fixed_reset_of_source_jet_bound` applies both source operator
bounds to the existing reset theorem. For supplied source `TailData` at
`lam = 1/10^12`, it gives `Nonempty (ResetWitness d 81162000)`
conditional on the source jet inequalities with multiplier `500`.
The cutoff decision above still applies to those inequalities. The
energy polynomial signs for the same reset remain open.
[Lean module](../../formal/p2/P2_MB08_InverseBound.lean)
· [Pre-implementation contract](MB08_INVERSE_OPERATOR_LEAN_CONTRACT_2026-11-14.md)

- Status `PASS[LOCAL_PROOF_COMPILE:MB08_INVERSE_BOUND]`.
- Source `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, manifest blob
  `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d`, Lean `4.34.0-rc2`.
- FixedReset, QuadraticBound and InverseBound all compiled with exit 0
  and empty stderr. Both new declarations printed only `propext`,
  `Classical.choice` and `Quot.sound`.
- Successful inverse proof SHA-256
  `c0bc6150d59a8b2b4f84f8dfd03b7e3a2ab713ee38a50f174c8766a0a6d67685`.
- Successful run `mb08-inverse-20261114T034159983338Z`. Original ZIP
  at `/content/mb08-inverse-20261114T034159983338Z.zip` has 13 members,
  576,191 bytes and SHA-256
  `7d7b8f46aad1367a5367889945bbf715efbc9f70245ca84913b1c921a35bc50b`.
  CRC and listed payload SHA-256 values were rechecked inside Colab.
  Durable Drive or D: preservation is unverified.
- The first inverse run and a repeat of the first input failed in
  the same absolute-value step. The successful proof gives Lean the
  explicit nonnegativity statement for the exponential gap.
- Claim status `UNVERIFIED`.
