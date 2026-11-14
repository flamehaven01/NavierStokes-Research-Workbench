# MB-08 source inverse-operator bound — Lean formalization contract

Date: 2026-11-14 (Asia/Bangkok). Status:
`FORMALIZATION_SPEC_READY / LEAN_NOT_COMPILED / CLAIM_UNVERIFIED`.

## 1. Provenance

Original: `openai/NavierStokesAndEuler` at
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

The target is the **same** source
`NavierStokes.UniformAngularReset.linearEquivNonneg`, not the P2
moment-repair normalization matrix and not a new cutoff.

- `NavierStokes/AngularMomentReset.lean`: `template`, `moment`,
  `angularSlope`, `pressureSlope`, `linearMatrix` and determinant.
- `NavierStokes/LocalizedMomentRepair.lean`: actual middle-half bump.
- `NavierStokes/SmoothCutoffs.lean`: actual plateau, value and support.
- `NavierStokes/UniformAngularReset.lean`:
  `linearEquivNonneg` and `linearCLM`.

Existing new source theorem:
`NSRW.P2.mb_source_quadraticCLM_norm_le_one`
in `formal/p2/P2_MB08_QuadraticBound.lean`,
local SHA-256 `eaf811f995154e45c83906321a7869252721d90dffea160051d2b6c99dd0da8e`.
The development run is recorded as exit 0, with standard
`propext/Classical.choice/Quot.sound`, no `sorryAx`.
Its ZIP was reopened on its Colab VM, **not** retained or
verified in Drive or the D: workspace. Claim admission remains
`UNVERIFIED`. This review does not independently rerun the archive.

## 2. Exact mathematical objective

For each `lam : Real` with `0 <= lam <= 1/10`, prove

```lean
theorem mb_source_linear_inverse_norm_le_1000
    (lam : ℝ) (hl : 0 ≤ lam) (hu : lam ≤ 1 / 10) :
    ∀ x : NavierStokes.AngularMomentReset.Coeff,
      ‖(NavierStokes.UniformAngularReset.linearEquivNonneg lam hl).symm x‖
        ≤ 1000 * ‖x‖
```

and specialize by rewriting `d.core.lam=1/10^12` to discharge
`hinv` in the **existing compiled conditional**
`mb_fixed_reset_of_operator_bounds`. The `hquad` premise can already
be discharged using `mb_source_quadraticCLM_norm_le_one`.
The `hjet` premise is STILL OPEN.

## 3. Source scalar estimates, independent of cutoff derivative

Let `s=1-lam`, `p=-1-2*lam`,
`A=moment s`, `B=moment p`,
`E=exp(2*s)`, `F=exp(2*p)`.

The source template has

```text
0 <= template(y) <= 1
support(template) subset [-3/20,3/20]
template(y)=1 on [-3/40,3/40]
```

At `0<=lam<=1/10`, both slopes lie in `[-6/5,1]`.
For `y` in template support, `|s*y|,|p*y|<=9/50`.
The exponential bounds
`1-z<=exp(-z)` and `exp(z)<=1/(1-z)` for `0<=z<1`
give `1/2<=exp(s*y),exp(p*y)<=2`.
The same lower bound holds on the plateau.

Consequently both source moments satisfy the conservative **exact
real** bounds

```text
3/40 <= A <= 3/5
3/40 <= B <= 3/5
```

The first lower bound uses the plateau length `3/20`;
the upper bound uses support length `3/10`.
No norm of `template'` is used. This step must be formalized
from the **actual integral**, rather than taken as a new axiom or
assumed scalar data.

Additional exponential inequalities:

```text
0 < F <= 1
1 <= E <= 9
E-F > 9/5       (because E >= 1+2*s >= 14/5, F<1)
```

The actual source matrix and its adjugate are

```text
linearMatrix lam = [[A, E*A], [2*B, 2*F*B]]
adjugate        = [[2*F*B, -E*A], [-2*B, A]]
abs(det)        = 2*A*B*(E-F)
```

Thus

```text
abs(det) > 2*(3/40)^2*(9/5) = 81/4000 > 9/800
adjugate row 0 sum <= 2*(3/5)*1 + 9*(3/5) = 33/5
adjugate row 1 sum <= 2*(3/5)+(3/5) = 9/5
inverse norm <= (33/5)/(9/800) = 1760/3 < 1000
```

The tighter determinant bound alone would give
`(33/5)/(81/4000) = 8800/27 < 1000`.
These rational comparisons were independently recalculated using
exact `Fraction` arithmetic. They are *not* Lean compile output.

The source `Coeff := Fin 2 -> Real` uses the max/sup norm, so a
coordinate-wise adjugate calculation must justify the final
`‖.symm x‖` bound. Do not substitute the matrix's other norms
without a proved norm comparison.

## 4. Proof sequence with explicit gates

1. **Plateau:** formalize `template(y)=1` for
   `-3/40<=y<=3/40` from the existing
   `SmoothCutoffs.cutoff_one_of_abs_le` and
   `LocalizedMomentRepair.bump` formula.
2. **Moment bounds:** integrate over the real source support
   and plateau; prove the exact `[3/40,3/5]` bounds uniformly
   for `s` in `[-6/5,1]`. Check interval integral orientation,
   nonnegative integrands and equality of whole-line integrals.
3. **Exponent gap:** prove the `E,F` bounds with named Mathlib
   `Real.exp` inequalities, without using decimal floats.
4. **Matrix:** use the existing `linearMatrix_det` and
   `linearEquivNonneg` definitions to prove a coordinate formula
   or adjugate bound and the `Fin 2` sup norm inequality.
5. **Source closure:** prove the proposed theorem with no hypotheses
   beyond `hl`/`hu`. In a new downstream wrapper, combine with
   the *already compiled* quadratic bound, leaving the exact
   original-cutoff `hjet` as the only reset premise.
6. Compile the entire new module and `#print axioms` in the
   pinned Lean 4.34.0-rc2, dependency and source environment.
   Collect actual stdout/stderr, signatures and file SHA-256.
   Until then do not mark any new declaration `PASS`.

## 5. Negative and custody boundaries

The source cutoff is selected by Mathlib
`Nonempty.some`, not identified with the explicit
`smoothTransition` witness. The available support/plateau/value
laws can justify the inverse and quadratic bounds, but **cannot**
imply a numeric first-derivative bound for the selected function.
Keep `HELD[SOURCE_CUTOFF_NUMERIC_JET_UNAVAILABLE]`.

The source `ResetWitness` still requires a *global smooth function*
of `eta`, both moment identities for all eta, norm and derivative
bounds and `small_jets`. An inverse estimate alone does not
construct a fixed source `Profile`.

Also unresolved at `eta=2^-20` for the **same reset**:
`constantTerm<=-1/5` and `energyPolynomial(9/10)<0`.
The MB-08 sign theorem is conditional on those statements.

This file is a formalization contract, **not** a Lean proof, new
compile, independent reproduction, receipt or claim promotion.
No existing MB-05/06 proof, receipt, ledger or ZIP should be rewritten.
