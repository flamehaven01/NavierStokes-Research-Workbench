# First conditional numerical experiment: input and error contract

Original design snapshot: 2026-10-28 (Asia/Bangkok), before arithmetic execution.
Update, 2026-10-31: the bounded exact-rational **core-scalar** experiment is now
implemented and locally recomputed. Coefficient/moment evaluation and the full
conditional-family computation remain unperformed. The historical design date
and fixed tuple below are preserved.
This contract implements the next step of the
[computational bridge plan](NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md).
It is not a numerical certificate, source-Profile construction or new receipt.

Reassessment, 2 November 2026: the [current-position document](CURRENT_POSITION_2026-11-02.md)
sets normalized main/prefix moment and coefficient enclosure as the next work.
Core scalars now also have a [separate interval-arithmetic cross-check](NSRW_CORE_SCALAR_CROSSCHECK.md).
That checker does not provide a validated quadrature method. Prefer explicit
computable analytic bounds where sufficient, and justify any remaining integral
enclosures. The tuple, unresolved source hypotheses and budget below are unchanged.

Reassessment, 12 November 2026: section 3.1 makes the analytic-first route
explicit. The first coefficient target permits justified one-sided bounds and
an exactly linked scaled q bound. It does not require accurate evaluation of
all integrals, or a full Profile evaluator. No new coefficient computation or
Lean admission is recorded by this clarification.

## 1. Selected model and first output

Select the **conditional source-family route**. Its mathematical inputs remain
the pinned source `Profile F` and exact P1 propositions. The first computation
will enclose core-dependent quantities and a proposed coefficient lower bound;
it will not identify a numerical Profile or a radius at which M vanishes.
The full-instance and restricted/toy alternatives are not silently substituted.

The proposed scalar tuple is fixed before numerical results are examined:

| Input | Exact representation | Meaning |
|---|---|---|
| P, m | 1, 1 | Positive core parameters |
| lambda | 1 / 1000000000000 | Strictly positive; below 1/120 and 1/10 |
| wait | 60 log(1000000000000) | Exact source amplitude-spec expression |
| h | lambda / 4 | Candidate TailData scalar; 0<h and 2h<lambda |
| eta | 1 / 1048576 | Positive fixed input with eta squared at most 1 |
| coefficient bound K | Unassigned | Must belong to the same Profile/reset; no fabricated value |

The positivity of wait-25 follows analytically from log(10)>1, rather than a
floating-point comparison. These elementary scalar facts do not establish a
ResetWitness, combinedScale smallness or nonemptiness of the numerical family.
This input is a proposed conditional computation, not a source-instance witness.

Source: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
Formal P1 execution: `7f29ebf0e2b894bf598144628230ae09df436c3d`.
The [dated P1 receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md)
fixes the ten exact-real statements; none is altered here.

## 2. Admissibility: established versus unresolved

| Obligation | Present disposition | Evidence still required for a numerical source claim |
|---|---|---|
| Core positive parameters and lambda bounds | Analytic scalar check | Bind exact inputs to the evaluated core |
| wait identity and eta squared bound | Analytic scalar check | Preserve expression identity, not a rounded equality |
| h inequalities | Analytic scalar check | Matching TailData and full Profile construction |
| The same F.reset supplies amplitude | Required hypothesis | A matching ResetWitness; finite sampling is insufficient |
| K>0 and combinedScale(F.data,K)<=1/1000 | UNRESOLVED | Bound the actual K and actual source constants |
| Selected stepBound in errorConstant | UNRESOLVED | An applicable bound on the selected source value or a proved parameterized bridge |
| Explicit Profile at the selected tuple | NOT CONSTRUCTED | Construction/nonemptiness proof with all obligations |
| Core exp/expm1, gap and plateau enclosures | IMPLEMENTED, RECOMPUTED (2026-10-31) | Exact rational series/remainder experiment only |
| Numerical moment integration | NOT IMPLEMENTED | Justified integral error bounds and a reviewed integrator |

The dependency remains
`combinedScale -> errorConstant -> flattenLength -> stepBound`.
An explicit derivative bound for sigma is not automatically an upper bound on
the value selected by `Classical.choose`. Merely choosing a smaller lambda or
assigning a convenient K does not discharge this obligation.

## 3. Exact quantities to enclose

Put beta0=1/2-lambda, L=13/lambda, ell=exp(-23/20), v=exp(-17/20).
Use z=r exp(-L), whose repair-window endpoints are fixed finite exponentials.
Do not evaluate exp(L) or the physical radius X as an ordinary floating point.

1. Enclose the positive weight gap using
   `G = exp(-13+23*lambda/20) * expm1(17*lambda/10)`.
   This is the admitted identity, not a certified implementation of libm expm1.
2. Enclose the positive plateau width `w=(v-ell)/4`. The admitted inequality
   `mu01>=w` avoids numerical quadrature of this bump moment in the first target.
3. Preserve `I01=exp(L*beta0)*mu01` in a scaled/logarithmic representation.
4. Obtain justified bounds on the affine coefficients, using analytic moment
   bounds first and numerical integral enclosures where needed. For the
   main-only denominator, beta0=1/2-lambda and beta1=1/2-2*lambda imply exactly
   `exp(2*beta0)-exp(2*beta1)=exp(1-4*lambda)*(exp(2*lambda)-1)`.
   The numerical module checks the two exponent relations with exact rational
   arithmetic and uses the exponential addition identity. This is an analytic
   and implementation connection, not an eleventh admitted Lean proposition.
   Both factors receive outward enclosures; require a denominator interval
   `[d_lower,d_upper]` with `d_lower>0`. For a positive numerator
   `N=-deltaM`, a coefficient lower bound divides **lower(N) by upper(D)**,
   with a final downward rounding. Using the denominator's lower endpoint for
   that lower bound is invalid. The positive-ratio helper tests this direction;
   actual numerator/moment enclosures are still missing.
5. With p=eta*(1+eta squared), form
   `q_lower = (9/10)*lower(C_main) - upper(abs(p))*upper(abs(C_prefix))`.
   Reject if lower(C_main)<=0, the normalized determinant meets zero, or
   q_lower<=0. Do not replace a nonpositive lower enclosure by an absolute value.
6. Only under the unresolved amplitude-spec hypotheses may `c1>q_lower>0`
   be used in the exact P1 inequality. The corresponding candidate bound is
   `K1*q_lower*exp(L*beta0)*w*G`, with the same core and eta throughout.

The output must preserve unresolved hypotheses. A numerical positive q and
factor product, even if obtained, are not an explicit source-Profile certificate.
Whole-window endpoint signs and continuity would be theorem-derived, not
numerically evaluated M values. A narrow root bracket is a later experiment.

### 3.1 Analytic-first coefficient route — 12 November 2026

The following is a static derivation from the existing proof/source, proposed
for the next bounded calculation. It is not a new compiled proposition or a
successful numerical q evaluation.

Define `F_i=normalizedMainMoment(c,i)`, `A_i=rowMoment(c.exponents i)` and
`D=exp(2*beta0)-exp(2*beta1)>0`. The L2 proof contains the explicit estimate
`F_0 <= exp(-2+3*lambda)*F_1`; L3 gives
`A_0 >= exp(-3*lambda/20)*A_1 > 0`. Therefore

```text
kappa = 1 - exp(-2 + 63*lambda/20)
-deltaM = F_1/A_1 - F_0/A_0 >= kappa * F_1/A_1
C_main >= kappa * F_1 / (A_1 * D).
```

`kappa>0` under the source bound `0<lambda<1/10`. F1 supplies the further
explicit inequality

```text
F_1 >= exp(-beta1*center(c,0)) / (5000*lambda).
```

Source bindings:

- [L2 decay estimate](../formal/p2/P2_L2_NormalizedMainMomentComparison.lean):
  private `normalizedMainMoment_zero_le_decay_one`.
- [L3 template comparison](../formal/p2/P2_L3_TemplateMomentComparison.lean):
  `rowMoment_one_scaled_le_rowMoment_zero`.
- [F1 lower bound](../formal/p2/P2_F1_MainMomentPositivity.lean):
  `mainMoment_one_lower` and the definition of `normalizedMainMoment` in L2.
- [C01 coefficient identity](../formal/p2/P2_C_MainOnlyCoefficient.lean):
  `affineCoefficients_main_one_eq_neg_deltaM_div_gap`.
- Pinned upstream `NavierStokes/OutgoingPulseBounds.lean`:
  `prefixBound`, `prefixCoefficient_le_bound`, `prefixCoefficient_small`, and
  `actual_coefficients_normalized_system` supply prefix and system bounds.
  All upstream locators refer to the source commit in section 1.

The remaining obligations include a computable upper bound on A_1 unless that
factor cancels by an exact positive rescaling, a bound on the actual prefix-only
coefficient from the same normalized system, and a consistent scale conversion.
A positive kappa alone does not close q. When
turning the private L2 estimate into a reusable Lean result, add and verify a
separate bridge rather than altering the admitted module bytes.

The [MomentBound detailed design](momentbound/IMPLEMENTATION_PLAN.md#3-derivation-a-remove-the-enormous-common-scale)
develops the positive-rescaling alternative: factor
`s=exp(-beta1*center(c,0))/(A_1*D)`, bound both affine components relative to s,
and use coarse rational prefix bounds for P=m=1. This may remove row-moment
evaluation and quadrature from the first q-sign decision. Its source bridge is
new, statically derived work; the design arithmetic check is not a certificate.

The common positive exponential scales must be factored before numerical
subtraction. If `q >= s*qhat_lower`, retain the exact definition of `s>0`, its
source identity and the proof/derivation of that inequality. Certification of
`qhat_lower>0` then gives a scaled positive q bound; it does not mean the code
evaluated q as an ordinary floating-point or fixed-point number. Propagate s
into the later J bound unless it cancels by an exact identity.

The current `exp_bounds` API is intentionally restricted to rational arguments
in [-16,16], and its precision denotes absolute fractional bits. Increasing that
precision is not a remedy for an exponent of order 1/lambda. Keep the existing
five-scalar interface and records unchanged; implement only justified new bound
operations needed by this route. Use quadrature only if analytic bounds do not
close the fixed-input target. A future quadrature path must evaluate the actual
source cutoff and supply its own enclosure justification.

## 4. Arithmetic and stopping rule

The inspected Python environment has mpmath and scipy. High precision alone
does not establish validated enclosures, and no claim is made that mpmath lacks
interval functionality. The inspected environment has no flint or gmpy2 package.
No new package was installed for the bounded core calculation. Its selected
backend is exact Fraction arithmetic with the explicit geometric Taylor-tail
bound described in the [numerical method](P2_CORE_SCALAR_METHOD_2026-10-31.md).
Acceptance of a moment-quadrature backend remains UNRESOLVED.

Before the numerical run, select a backend with documented outward enclosures
for rational inputs, exp, log, sqrt and the operations used by the integrator;
review its version, trust assumptions and licensing. If no validated expm1 is
available, use a justified series/remainder enclosure, not ordinary exp(x)-1.
The certificate verifier must recompute enclosures; producer JSON and hashes
alone are not arithmetic evidence. Do not create a general interval framework.

Fixed experiment budget after backend validation: 128 bits initially, then
256 and 512 bits at most; at most 2048 integration subintervals and 120 seconds
per precision attempt. If a justified enclosure has not closed within that
budget, return UNRESOLVED rather than tuning inputs after observing results.
Changing the input, backend or budget creates a new identified experiment.

| Error source | Required treatment |
|---|---|
| Input representation | Exact rationals/expression trees; include input uncertainty if any |
| Transcendentals and rounding | Outward bounds at every operation, including expm1 or its remainder |
| Normalized moment quadrature | Proven integral enclosure over all integration points, not sampled error estimates |
| Matrix/affine solve | Consistent row/debt normalization; determinant separated from zero; outward solve propagation |
| Amplitude/reset | Analytic hypotheses recorded separately from arithmetic bounds |
| Scale and coordinates | Exact positive conversions with checked log/scaled representation |
| Truncation/model approximation | None may be silently dropped; finite support does not justify an unrelated tail truncation |

## 5. Output and review conditions

A retained result must identify the exact input, source/proof checkpoints,
backend/version, precision/budget, interval endpoints and all assumptions. It
must distinguish an evaluated factor bound from a certified coefficient bound,
and either from an explicit-instance/shared-zero certificate.

Required rejection cases are: interval denominator containing zero; a c1/q
enclosure meeting zero; an inverted support; an unbound reset/model input;
missing integral error; NaN/infinity or scale overflow; and a producer-tampered
positive margin. A high-precision reference is a comparison, not proof of inclusion.

The current producer record is labeled `CORE_SCALAR_ENCLOSURES_ONLY`; it cannot
be relabeled `CONDITIONAL_FAMILY_ENCLOSURE_ONLY` while q is not enclosed, or
`SOURCE_PROFILE_CERTIFICATE` while source admissibility is unresolved. The
verifier rejects missing unresolved assumptions, changed inputs/scales,
invented I01 upper bounds and inflated bounds. Its scaled I01 value is a
**lower-bound expression**, not an enclosure of I01 from above or an evaluated
logarithm. A separate recomputation under one operator is not independent attestation.

The next implementation task is a justified main-coefficient lower bound and
prefix-coefficient absolute upper bound, using the analytic route first.
The source-instance lane remains HELD until its actual
admissibility obligations are discharged. This is a precise outstanding condition,
not a counterexample to Z+J or the P1 exact-real propositions.
