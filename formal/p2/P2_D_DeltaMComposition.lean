import P2_L2_NormalizedMainMomentComparison
import P2_L3_TemplateMomentComparison

/-!
# P2 D: source-linked DeltaM composition

This module introduces the NSRW shorthand

`deltaM c =
  normalizedMainMoment c 0 / rowMoment (c.exponents 0) -
  normalizedMainMoment c 1 / rowMoment (c.exponents 1)`

and proves it is negative by composing the separately compiled strict-L2 and
L3 comparisons with the pinned source positivity of the row moments.

The bridge to the source repair system is kept explicit:
`normalizedDebt c (affineDebt c 0 1) i = -normalizedMainMoment c i`.

This module does not prove a repair-coefficient sign or a first-repair zero.
-/

open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

noncomputable def deltaM (c : Parameters) : ℝ :=
  normalizedMainMoment c 0 / rowMoment (c.exponents 0) -
    normalizedMainMoment c 1 / rowMoment (c.exponents 1)

theorem normalizedDebt_affineDebt_zero_one_eq_neg_normalizedMainMoment
    (c : Parameters) (i : Fin 2) :
    normalizedDebt c (affineDebt c 0 1) i = -normalizedMainMoment c i := by
  unfold normalizedDebt affineDebt normalizedMainMoment
  ring

theorem normalizedAffineMainDifference_eq_neg_deltaM (c : Parameters) :
    normalizedDebt c (affineDebt c 0 1) 0 / rowMoment (c.exponents 0) -
        normalizedDebt c (affineDebt c 0 1) 1 / rowMoment (c.exponents 1) =
      -deltaM c := by
  rw [normalizedDebt_affineDebt_zero_one_eq_neg_normalizedMainMoment c 0,
    normalizedDebt_affineDebt_zero_one_eq_neg_normalizedMainMoment c 1]
  unfold deltaM
  ring

theorem deltaM_neg (c : Parameters) : deltaM c < 0 := by
  have hL2 := normalizedMainMoment_zero_lt_target_one c
  have hL3 := rowMoment_one_scaled_le_rowMoment_zero c
  have hA0 : 0 < rowMoment (c.exponents 0) := rowMoment_pos c 0
  have hA1 : 0 < rowMoment (c.exponents 1) := rowMoment_pos c 1
  have hF1 : 0 < normalizedMainMoment c 1 := normalizedMainMoment_one_pos c
  have hcross :
      normalizedMainMoment c 0 * rowMoment (c.exponents 1) <
        normalizedMainMoment c 1 * rowMoment (c.exponents 0) := by
    calc
      normalizedMainMoment c 0 * rowMoment (c.exponents 1) <
          (Real.exp (-(3 / 20 : ℝ) * c.lam) * normalizedMainMoment c 1) *
            rowMoment (c.exponents 1) :=
        mul_lt_mul_of_pos_right hL2 hA1
      _ = normalizedMainMoment c 1 *
          (Real.exp (-(3 / 20 : ℝ) * c.lam) * rowMoment (c.exponents 1)) := by
        ring
      _ ≤ normalizedMainMoment c 1 * rowMoment (c.exponents 0) :=
        mul_le_mul_of_nonneg_left hL3 hF1.le
  have hratio :
      normalizedMainMoment c 0 / rowMoment (c.exponents 0) <
        normalizedMainMoment c 1 / rowMoment (c.exponents 1) := by
    exact (div_lt_div_iff₀ hA0 hA1).2 hcross
  unfold deltaM
  linarith

#print axioms NSRW.P2.normalizedDebt_affineDebt_zero_one_eq_neg_normalizedMainMoment
#print axioms NSRW.P2.normalizedAffineMainDifference_eq_neg_deltaM
#print axioms NSRW.P2.deltaM_neg

end NSRW.P2
