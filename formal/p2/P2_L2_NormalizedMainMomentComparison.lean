import P2_F1_MainMomentPositivity

/-!
# P2 L2: normalized main-moment comparison

This module binds the normalized main moments to the same short log-coordinate
integral used by the pinned source.  It uses the compiled F1 positivity to
upgrade a weak integral comparison to the strict L2 bound
`normalizedMainMoment c 0 < exp (-(3 / 20) * c.lam) *
normalizedMainMoment c 1`.

It does not prove `DeltaM < 0`, the template-moment comparison required for
that conclusion, or any repair-window zero statement.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

noncomputable def normalizedMainMoment (c : Parameters) (i : Fin 2) : ℝ :=
  Real.exp (-(beta c i * center c 0)) * mainMoment c i

theorem normalizedMainMoment_log_short (c : Parameters) (i : Fin 2) :
    normalizedMainMoment c i =
      ∫ y in (0 : ℝ)..11 / c.lam,
        Real.exp (beta c i * (y - center c 0)) * mainPulse (c.lam * y) := by
  unfold normalizedMainMoment
  rw [mainMoment_log_short, ← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_congr
  intro y _
  dsimp
  rw [show beta c i * (y - center c 0) =
    -(beta c i * center c 0) + beta c i * y by ring, Real.exp_add]
  ring

theorem normalizedMainMoment_one_pos (c : Parameters) :
    0 < normalizedMainMoment c (1 : Fin 2) := by
  unfold normalizedMainMoment
  exact mul_pos (Real.exp_pos _) (mainMoment_one_pos c)

private theorem beta_zero_eq_beta_one_add_lam (c : Parameters) :
    beta c 0 = beta c 1 + c.lam := by
  norm_num [beta, Parameters.exponents]
  ring

private theorem lam_center_gap_le (c : Parameters) {y : ℝ}
    (hy : y ≤ 11 / c.lam) :
    c.lam * (y - center c 0) ≤ -2 + 3 * c.lam := by
  have hmul := mul_le_mul_of_nonneg_left hy c.lam_pos.le
  have hbound : c.lam * y ≤ 11 := by
    calc
      c.lam * y ≤ c.lam * (11 / c.lam) := hmul
      _ = 11 := by field_simp [c.lam_pos.ne']
  dsimp [NavierStokes.OutgoingPulseBounds.center, Parameters.pulseLength]
  field_simp [c.lam_pos.ne']
  linarith [hbound]

private theorem normalized_integrand_continuous (c : Parameters) (i : Fin 2) :
    Continuous (fun y : ℝ =>
      Real.exp (beta c i * (y - center c 0)) * mainPulse (c.lam * y)) := by
  exact (Real.continuous_exp.comp
    (continuous_const.mul (continuous_id.sub continuous_const))).mul
      (mainPulse_contDiff.continuous.comp (continuous_const.mul continuous_id))

private theorem normalized_integrand_zero_le_scaled_one (c : Parameters) {y : ℝ}
    (hy : y ∈ Icc (0 : ℝ) (11 / c.lam)) :
    Real.exp (beta c 0 * (y - center c 0)) * mainPulse (c.lam * y) ≤
      Real.exp (-2 + 3 * c.lam) *
        (Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y)) := by
  have hgap := lam_center_gap_le c hy.2
  have hexp : Real.exp (c.lam * (y - center c 0)) ≤
      Real.exp (-2 + 3 * c.lam) := Real.exp_le_exp.mpr hgap
  have hpulse : 0 ≤ mainPulse (c.lam * y) :=
    NavierStokes.PulseAmplitude.mainPulse_nonneg
      (mul_nonneg c.lam_pos.le hy.1)
  have hone_nonneg : 0 ≤
      Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y) :=
    mul_nonneg (Real.exp_pos _).le hpulse
  calc
    Real.exp (beta c 0 * (y - center c 0)) * mainPulse (c.lam * y) =
        Real.exp (c.lam * (y - center c 0)) *
          (Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y)) := by
      rw [beta_zero_eq_beta_one_add_lam c]
      rw [show (beta c 1 + c.lam) * (y - center c 0) =
        c.lam * (y - center c 0) + beta c 1 * (y - center c 0) by ring,
        Real.exp_add]
      ring
    _ ≤ Real.exp (-2 + 3 * c.lam) *
          (Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y)) :=
      mul_le_mul_of_nonneg_right hexp hone_nonneg

private theorem normalizedMainMoment_zero_le_decay_one (c : Parameters) :
    normalizedMainMoment c 0 ≤
      Real.exp (-2 + 3 * c.lam) * normalizedMainMoment c 1 := by
  rw [normalizedMainMoment_log_short c 0, normalizedMainMoment_log_short c 1,
    ← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_mono_on (μ := volume)
    (div_nonneg (by norm_num) c.lam_pos.le)
  · exact (normalized_integrand_continuous c 0).intervalIntegrable _ _
  · exact (continuous_const.mul (normalized_integrand_continuous c 1)).intervalIntegrable _ _
  · intro y hy
    exact normalized_integrand_zero_le_scaled_one c hy

private theorem decay_constant_lt_target (c : Parameters) :
    Real.exp (-2 + 3 * c.lam) < Real.exp (-(3 / 20 : ℝ) * c.lam) := by
  apply Real.exp_lt_exp.mpr
  nlinarith [c.lam_lt]

theorem normalizedMainMoment_zero_lt_target_one (c : Parameters) :
    normalizedMainMoment c 0 <
      Real.exp (-(3 / 20 : ℝ) * c.lam) * normalizedMainMoment c 1 := by
  have hweak := normalizedMainMoment_zero_le_decay_one c
  have hstrict := mul_lt_mul_of_pos_right (decay_constant_lt_target c)
    (normalizedMainMoment_one_pos c)
  exact hweak.trans_lt hstrict

#print axioms NSRW.P2.normalizedMainMoment_log_short
#print axioms NSRW.P2.normalizedMainMoment_one_pos
#print axioms NSRW.P2.normalizedMainMoment_zero_lt_target_one

end NSRW.P2
