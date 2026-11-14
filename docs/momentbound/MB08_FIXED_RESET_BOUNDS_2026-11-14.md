# MB-08 explicit bounds for the scheduled reset

14 November 2026. The bounds use the pinned outgoing construction at
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` and the Mathlib revision
`85e3a25e006c35636f0e53b0e9296caca2685bc0`.

## Operator and jet bounds

For `0 < lambda ≤ 1/10`, let `s = 1-lambda`, `p = -1-2*lambda`, and
`M(v) = moment(v)` for the source reset template. The template is bounded
by 0 and 1, supported on `[-3/20,3/20]), and equal to 1 on
`[-3/40,3/40]`. On the support, `abs(v*y) ≤ 9/50` for either slope.
The estimates `exp(9/50) ≤ 1/(1-9/50) < 2` and
`exp(-9/50) ≥ 1-9/50 > 1/2` give `3/40 ≤ M(v) ≤ 3/5`.
[Template and matrix definitions](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/AngularMomentReset.lean)

The absolute determinant of the source linear matrix is
`2*M(s)*M(p)*(exp(2*s)-exp(2*p))`. Here `exp(2*s) ≥ 1+2*s`,
`s ≥ 9/10`, and `exp(2*p)<1`. Thus the determinant exceeds `9/800`.
Using `exp(2*s) ≤ exp(2) < 9`, the adjugate row sums in absolute
value are bounded by `6/5+27/5 = 33/5) and `6/5+3/5 = 9/5`.
For the sup norm on `Fin 2 → Real`, division by the determinant gives
an inverse operator norm below `(33/5)/(9/800) < 1000`.

The pressure quadratic term has coefficients given by the weighted squared
bump integrals. The bump at zero contributes at most `(3/10)*2`. On the
support of the bump translated by 2, `p*y ≤ 0`, so it contributes at
most `3/10`. The bilinear operator norm is therefore at most `9/10 < 1`.

For a comparison jet bound, Mathlib's explicit inner-product bump is
`cutoff(x)=smoothTransition(2-2*abs(x))` after scaling by the two
radii. Set `g(t)=exp(-1/t)` for positive t and zero otherwise. For
`0<t<1`, `g'(t)=t^-2*exp(-1/t) ≤ 2` by `exp(u) ≥ u^2/2`.
The transition is `g(t)/(g(t)+g(1-t))`. Its derivative is
`(g'(t)*g(1-t)+g(t)*g'(1-t))/(g(t)+g(1-t))^2`, bounded by
`2/(g(t)+g(1-t)) ≤ 2*exp(2) < 18` since at least one argument is
at least `1/2`. The derivative is zero off the transition interval,
including its endpoints by smoothness. The reset template adds a scale
`20/3`, giving `abs(bump'(j,y)) ≤ 240` for each translate. Summing
the two terms bounds the value and derivative of the relative
perturbation by `500*norm(c)` for that explicit bump. The upstream
`ContDiffBump.toFun` instead calls `someContDiffBumpBase`, which takes a
witness using `Nonempty.some`. Its exposed support and plateau laws suffice
for the operator bounds above. An upper derivative bound for the actual
chosen bump remains open.
[Mathlib choice and bump evaluation](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/Calculus/BumpFunction/Basic.lean)
[Mathlib bump](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/Calculus/BumpFunction/InnerProduct.lean)
· [Mathlib transition](https://github.com/leanprover-community/mathlib4/blob/85e3a25e006c35636f0e53b0e9296caca2685bc0/Mathlib/Analysis/SpecialFunctions/SmoothTransition.lean)

## Fixed-lambda construction from the source solver

Use `lambda=10^-12`, `beta=1000`, `K_quad=1`, the proposed source
jet bound `D=500` as a hypothesis, and
`C=81 ≥ 3*exp(3)`. Exact rational arithmetic gives

| Quantity | Value |
| --- | --- |
| Contraction radius `r=1/(4*beta*K_quad)` | `1/4000` |
| Debt radius `epsilon=r/(4*beta)` | `1/16000000` |
| Bound `L=2*beta*(1+D)` | `1002000` |
| Witness bound `K=L*C` | `81162000` |

The checks `4*beta*K_quad*r=1`, `C*lambda^28<epsilon`, and
`K*lambda^28<lambda/4<1/2` pass exactly.

For any source `TailData` with this lambda, the source theorem
`actual_debt_first_jet_bound` controls both the debt and its derivative
for every eta. Apply `exists_smooth_solver_on_ball` to the actual
linear equivalence and quadratic map using the bounds above. If its
inverse branch is `g_inv`, compose it with
`eta ↦ debt(normalizedDebt d eta)`. The full image lies inside the
open debt ball, giving global smoothness. Applying `actual_moment_map`
to the solver identity gives both source moment equations. The solver's
norm and local Lipschitz bounds give the coefficient and eta derivative
bounds by composition with the debt. The jet estimate gives
`small_jets` using `K*lambda^28<lambda/4<1/2`. These arguments give
the fields of a source `ResetWitness d K` conditional on the three
operator estimates. The inverse and quadratic estimates are analytic
derivations. Establishing the source jet estimate remains necessary
to discharge the Lean theorem's last premise.

The analytic construction has room for a much weaker source jet bound.
The solver's tighter coefficient estimate is
`norm(coefficients eta) ≤ 162000*lambda^28`, also for the eta derivative.
For a general jet multiplier `D`, it is enough to check
`D*162000*lambda^28 ≤ lambda/4`. At the fixed lambda this allows, for
example, `D=10^318` if that bound can be justified for the chosen bump.
The current compiled wrapper takes `D=500`.
[Source solver and witness](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/UniformAngularReset.lean)

The remaining numerical amplitude task is to enclose the coefficients
of the same reset's source energy polynomial at `eta=2^-20`.
In particular the constant term must satisfy `c ≤ -1/5` to use the
source's unclamped equation, and `Q(9/10)<0` supplies the strict lower
bound on the positive root.

## Development compile and evidence

[Amplitude proofs](../../formal/p2/P2_MB08_Amplitude.lean) establish the
source sufficient-condition obstruction, its specialization to the fixed
lambda, and the positive-root sign criterion. The criterion applies to a
nonnegative threshold and uses the actual source polynomial with the clamp
inactive. It provides a route to the desired amplitude bound once the two
polynomial inequalities are proved.

[Reset proof](../../formal/p2/P2_MB08_FixedReset.lean) establishes
`Nonempty (ResetWitness d 81162000)` for the fixed lambda under the three
operator and jet hypotheses stated in the theorem. The witness provides
the smooth coefficient function and all-eta moment and derivative fields.

Both modules passed in Colab with Lean `4.34.0-rc2` at
`6a10ac8c22beadecabdbb0919c2b50214762f91d` and the pinned upstream checkout.
The four declarations used `propext`, `Classical.choice` and `Quot.sound`.
Successful runs had empty stderr and no `sorryAx`. The first amplitude
run had a tactic syntax error. The first reset run needed the chain rule
expressed for the exact lambda function in the goal. The successful proof
SHA-256 values are
`397514f2946c438acf7f491dc78748c3728ee92e500ecf83ff37d8159a5a4d34`
for amplitude and
`a72bcc32a762a86f34681368335ec957b2ba9dcdc2346a6cd1c3f5ffdbeb9946`
for reset.

All four archives were reopened in private Drive at
`MyDrive/NSRW-evidence/2026-11-14/<run-id>/<run-id>-evidence.zip`.
ZIP CRCs, file digests and the whole-file digest matched the Colab originals.
Run IDs carry the original UTC date.

| Run ID | Exit | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `mb08-dev-20261113T173810516025Z` | 1 | 2556 | `559653e429e2893c9f42f688f19f9f3e301f125c37fe2bd509102596199a9a06` |
| `mb08-dev-20261113T173936894705Z` | 0 | 124631 | `798c3b052857cf3948bce3e03891eb9d49433626ba9078c6ad5449c5aba1aaa0` |
| `mb08-reset-20261113T174113871411Z` | 1 | 3334 | `08d416b890105e88e95a9baf0d8bc6ba8f20bed0fc46cba1f6a694a137d4a074` |
| `mb08-reset-20261113T174214695879Z` | 0 | 114372 | `4acfaad689c74dd100a525a34a977a4d5c8ca7ccc713c5b73faed405a9a897ca` |

The four declarations have development evidence and remain `UNVERIFIED`
for formal admission. The fixed source instance remains open pending a
bound for the chosen bump and verification of the actual energy polynomial.
