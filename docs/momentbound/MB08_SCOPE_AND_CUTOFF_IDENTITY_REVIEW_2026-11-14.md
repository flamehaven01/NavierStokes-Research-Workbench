# MB-08 — proof-scope and cutoff-identity review

Reviewed: 2026-11-14 (Asia/Bangkok)
Status: `PASS[LOCAL_SOURCE_AND_HYPOTHESIS_SCOPE_REVIEW] / ADMISSION_PENDING`

## 1. Exact inspected source identities

Pinned upstream source:
`openai/NavierStokesAndEuler` commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

| Development Lean file | Exact local SHA-256 |
| --- | --- |
| `formal/p2/P2_MB08_Amplitude.lean` | `397514f2946c438acf7f491dc78748c3728ee92e500ecf83ff37d8159a5a4d34` |
| `formal/p2/P2_MB08_FixedReset.lean` | `a72bcc32a762a86f34681368335ec957b2ba9dcdc2346a6cd1c3f5ffdbeb9946` |

Existing admitted MB-05/MB-06 proof files and receipts were not edited in
this review. The development record
`docs/momentbound/MB08_FIXED_RESET_BOUNDS_2026-11-14.md`
reports four Colab development ZIPs, two failed and two successful,
including their digests and same-trust-domain private Drive reopen.
**This review did not independently reopen Drive originals or rerun Lean.**

## 2. Four exact declarations and their boundaries

1. `mb_combinedScale_gt_prefix_lower`:
   `d : TailData`, `K : Real`, `d.core.P=1`, `d.core.m=1`,
   `0<K` imply
   `30 * 2^120 * d.core.lam < combinedScale d K`.
   No numerical `Profile` claim.
2. `mb_fixed_combinedScale_gt`: same inputs, plus
   `d.core.lam=1/1000000000000`, imply
   `1/1000 < combinedScale d K`. Therefore the cited **source
   sufficient condition** `combinedScale<=1/1000` is unavailable at
   the fixed lambda for positive K; this does **not** show the actual
   amplitude inequality is false.
3. `mb_amplitude_gt_of_energyPolynomial_neg`: any source `d`,
   actual `coefficients : Real -> Coeff`, `eta`, `threshold>=0`,
   and source `constantTerm<=-1/5` (clamp inactive) with
   `energyPolynomial ... threshold eta < 0` imply
   `threshold < CorrectedPulseAmplitude.amplitude d coefficients eta`.
   This is a general criterion. It does not prove either inequality
   at `eta=2^-20` for the chosen reset.
4. `mb_fixed_reset_of_operator_bounds`: `d : TailData` with
   `d.core.lam=10^-12`, plus all **three explicit premises**
   `hinv` (inverse linear equivalence norm <=1000),
   `hquad` (quadratic CLM norm <=1), and
   `hjet` (for all `c,y`: both `|relative c y|` and
   `|deriv(relative c) y|` <= `500*||c||`)
   imply `Nonempty (ResetWitness d 81162000)`.
   **No unconditional fixed source ResetWitness has been proved.**

The two operator estimates are supported by the separate analytic
derivation in the MB-08 report (support, plateau, exponential bounds),
but are *not discharged by the compiled four theorem declarations*.
A future admitted proposition must either include those premises or
formally prove them in new Lean modules.

## 3. Choice/identity issue in the actual cutoff

The pinned upstream
`NavierStokes/AngularMomentReset.lean` defines
`template := LocalizedMomentRepair.bump (-3/10) (3/10)`
and translated `bump j` from that template.

Pinned Mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`:

- `Mathlib/Analysis/Calculus/BumpFunction/Basic.lean` defines
  `someContDiffBumpBase E := Nonempty.some (HasContDiffBump.out)`,
  and `ContDiffBump.toFun` uses that choice;
- `Mathlib/Analysis/Calculus/BumpFunction/InnerProduct.lean`
  defines a *specific available witness*
  `ContDiffBumpBase.ofInnerProductSpace` through
  `Real.smoothTransition` and registers its existence;
- `Mathlib/Analysis/SpecialFunctions/SmoothTransition.lean`
  defines the explicit transition through `expNegInvGlue`.

The explicit witness's derivative bound `D=500`, if formally
established, **does not automatically transfer** to the unspecified
`Nonempty.some` selected function. The current interface provides
smoothness, plateau, support and `[0,1]` control, but no *quantified
numerical derivative bound* for that arbitrary choice. Those properties
alone do not imply a universal bound of 500 or 10^318: a smooth
transition can have much steeper slopes.

This is a **source-identity/evidence gap**, not a float precision or
algebraic issue.

## 4. Exact numerical slack; what it does and does not establish

The source-derived coefficient bound from the development theorem
is `||coefficients eta|| <= 162000*lambda^28` after eliminating the
looser chosen witness constant. To ensure the `small_jets` derivative
constraint from a bound `D*||coefficients eta||`, require:

```text
D*162000*lambda^28 <= lambda/4
D <= lambda^(-27)/648000
```

At `lambda=10^-12`, this permits
`D <= 10^324/648000 ≈ 1.5432098765e318`;
thus `D=10^318` is arithmetically sufficient **if and only if**
a valid source-cutoff derivative bound of that size can be proved.
Merely knowing a finite D exists is insufficient to certify a
particular fixed lambda. Also check the relative value bound and
all other `ResetWitness` fields, not just this one inequality.

### Distinct valid research routes

**Route A, original source identity preserved**: prove a numerical
derivative bound for the *actual chosen* cutoff, or find a source-level
lemma that identifies that choice with a concrete bump. Do not use
a bound for a different explicitly constructed witness without a
formal identity/transport theorem. If neither is available, record
`HELD[SOURCE_CUTOFF_NUMERIC_JET_UNAVAILABLE]`.

**Route B, explicit derivative-controlled cutoff**: instantiate an
explicit `smoothTransition`-based bump and prove the repaired
operator, moment/pressure, reset, and downstream hypotheses for
this **new variant**. This changes the construction lineage even if
some formulas look alike. It must be labeled as an NSRW-derived
variant and cannot silently inherit the original source's
fixed-Profile claim.

**Route C, lambda-dependent existential**: compact support and
smoothness may justify existence of some finite derivative bound,
allowing a sufficiently small lambda chosen *after* that bound.
This does not settle the fixed `10^-12` tuple.

## 5. Same-reset amplitude obligation

For the genuine source reset
`w : ResetWitness d K`, define at `eta=2^-20`:

```text
a = PulseAmplitude.quadraticCoefficient d.core > 0
b = PulseAmplitude.linearTerm d.core eta
c = CorrectedPulseAmplitude.constantTerm d w.coefficients eta
Q(t) = a*t^2 + b*t + c
```

Prove separately, for the **same** `d,w,eta`:

```text
c <= -1/5
Q(9/10) < 0
```

Only then does the compiled general sign theorem establish
`9/10 < amplitude d w.coefficients eta`.
No value for the actual source amplitude or `Profile.J` has been
certified. Solving a synthetic pointwise two-coefficient system at
one eta does not produce the required smooth all-eta witness.

## 6. Execution / admission actions still separate

- Development report: success/failed runs and hashes **recorded**,
  not independently re-opened or replayed in this review.
- Before claim admission: exact-byte proof checkpoint, separate
  runner/checkpoint, pinned clean replay, printed four exact
  signatures and axioms, ZIP/Drive evidence review, dated receipt.
- Admit the **actual conditional signatures only**. No proof of
  `hinv`, `hquad`, `hjet`, fixed Profile existence, amplitude
  signs, numerical root or `J` may be inferred from the
  conditional `mb_fixed_reset_of_operator_bounds`.
- Preserve existing admitted MB-05/06 claims at OE-2. Do not
  promote MB-08 or claim OE-3 based on same-trust-domain runs.

This document is a source/claim scope audit and research direction,
not a new proof, compilation, certification or application result.
