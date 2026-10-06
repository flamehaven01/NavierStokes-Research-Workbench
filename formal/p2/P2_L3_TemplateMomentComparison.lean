import NavierStokes.OutgoingPulseBounds

/-!
# P2 L3: template-moment comparison

This module proves the cross-multiplied template-moment comparison needed after
strict L2:

`exp (-(3 / 20) * c.lam) * rowMoment (c.exponents 1)
  <= rowMoment (c.exponents 0)`.

The proof uses only the pinned source definitions and support facts for
`rowMoment` and `radialTemplate`.  It does not prove `DeltaM < 0`, any
repair-coefficient sign, or a repair-window zero statement.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

private theorem exponent_zero_eq_exponent_one_add_lam (c : Parameters) :
    c.exponents 0 = c.exponents 1 + c.lam := by
  norm_num [Parameters.exponents]
  ring

private theorem decay_le_rpow_on_template (c : Parameters) {x : ℝ}
    (hx : radialTemplate x ≠ 0) :
    Real.exp (-(3 / 20 : ℝ) * c.lam) ≤ x ^ c.lam := by
  have hs := radialTemplate_support x hx
  have hxpos : 0 < x := templateLower_pos.trans hs.1
  have hlog : -(3 / 20 : ℝ) < Real.log x := by
    simpa only [templateLower, Real.log_exp] using
      Real.log_lt_log templateLower_pos hs.1
  have hscaled : -(3 / 20 : ℝ) * c.lam ≤ Real.log x * c.lam :=
    mul_le_mul_of_nonneg_right hlog.le c.lam_pos.le
  rw [Real.rpow_def_of_pos hxpos]
  exact Real.exp_le_exp.mpr hscaled

private theorem scaled_row_one_integrand_le_row_zero (c : Parameters) (x : ℝ) :
    Real.exp (-(3 / 20 : ℝ) * c.lam) *
        (x ^ c.exponents 1 * radialTemplate x) ≤
      x ^ c.exponents 0 * radialTemplate x := by
  by_cases hx : radialTemplate x = 0
  · simp [hx]
  · have hs := radialTemplate_support x hx
    have hxpos : 0 < x := templateLower_pos.trans hs.1
    have hdecay := decay_le_rpow_on_template c hx
    have hnonneg : 0 ≤ x ^ c.exponents 1 * radialTemplate x :=
      mul_nonneg (Real.rpow_nonneg hxpos.le _) (radialTemplate_nonneg x)
    calc
      Real.exp (-(3 / 20 : ℝ) * c.lam) *
          (x ^ c.exponents 1 * radialTemplate x) ≤
          x ^ c.lam * (x ^ c.exponents 1 * radialTemplate x) :=
        mul_le_mul_of_nonneg_right hdecay hnonneg
      _ = x ^ (c.exponents 1 + c.lam) * radialTemplate x := by
        rw [Real.rpow_add hxpos]
        ring
      _ = x ^ c.exponents 0 * radialTemplate x := by
        rw [exponent_zero_eq_exponent_one_add_lam c]

theorem rowMoment_one_scaled_le_rowMoment_zero (c : Parameters) :
    Real.exp (-(3 / 20 : ℝ) * c.lam) * rowMoment (c.exponents 1) ≤
      rowMoment (c.exponents 0) := by
  rw [rowMoment, rowMoment, ← integral_const_mul]
  apply integral_mono
  · exact (rowMoment_integrable (c.exponents 1)).const_mul _
  · exact rowMoment_integrable (c.exponents 0)
  · intro x
    exact scaled_row_one_integrand_le_row_zero c x

#print axioms NSRW.P2.rowMoment_one_scaled_le_rowMoment_zero

end NSRW.P2
