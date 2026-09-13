import NavierStokes.PulseAmplitude

/-!
# P2 F1: weighted main-moment positivity

This external module proves positivity of `mainMoment c 1` through a concrete
subinterval lower bound. It does not prove the later normalized comparison or
the first-repair interior-zero consequence.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

private def f1Integrand (c : Parameters) (y : ℝ) : ℝ :=
  Real.exp (beta c 1 * y) * mainPulse (c.lam * y)

private theorem f1Integrand_continuous (c : Parameters) :
    Continuous (f1Integrand c) := by
  exact (Real.continuous_exp.comp (continuous_const.mul continuous_id)).mul
    (mainPulse_contDiff.continuous.comp (continuous_const.mul continuous_id))

private theorem f1_interval_order (c : Parameters) :
    (0 : ℝ) ≤ 1 / (25 * c.lam) ∧
      1 / (25 * c.lam) ≤ 1 / (20 * c.lam) ∧
      1 / (20 * c.lam) ≤ 11 / c.lam := by
  constructor
  · positivity
  constructor
  · exact one_div_le_one_div_of_le (mul_pos (by norm_num) c.lam_pos)
      (by nlinarith [c.lam_pos])
  · field_simp [c.lam_pos.ne']
    nlinarith [c.lam_pos]

private theorem f1_integrand_nonnegative_on_short_interval (c : Parameters)
    {y : ℝ} (hy : y ∈ Ioc (0 : ℝ) (11 / c.lam)) :
    0 ≤ f1Integrand c y := by
  unfold f1Integrand
  exact mul_nonneg (Real.exp_pos _).le
    (NavierStokes.PulseAmplitude.mainPulse_nonneg
      (mul_nonneg c.lam_pos.le hy.1.le))

private theorem f1_integrand_lower_on_witness_interval (c : Parameters)
    {y : ℝ} (hy : y ∈ Icc (1 / (25 * c.lam)) (1 / (20 * c.lam))) :
    (1 / 50 : ℝ) ≤ f1Integrand c y := by
  have harg_lower : (1 / 50 : ℝ) ≤ c.lam * y := by
    calc
      (1 / 50 : ℝ) ≤ 1 / 25 := by norm_num
      _ = c.lam * (1 / (25 * c.lam)) := by
        field_simp [c.lam_pos.ne']
        ring
      _ ≤ c.lam * y := mul_le_mul_of_nonneg_left hy.1 c.lam_pos.le
  have harg_upper : c.lam * y ≤ 10 := by
    calc
      c.lam * y ≤ c.lam * (1 / (20 * c.lam)) :=
        mul_le_mul_of_nonneg_left hy.2 c.lam_pos.le
      _ = 1 / 20 := by
        field_simp [c.lam_pos.ne']
        ring
      _ ≤ 10 := by norm_num
  have hpulse := NavierStokes.PulseAmplitude.mainPulse_lower harg_lower harg_upper
  have hy_nonneg : 0 ≤ y := (f1_interval_order c).1.trans hy.1
  have hexp : (1 : ℝ) ≤ Real.exp (beta c 1 * y) :=
    Real.one_le_exp_iff.mpr
      (mul_nonneg (beta_bounds c 1).1.le hy_nonneg)
  unfold f1Integrand
  calc
    (1 / 50 : ℝ) = 1 * (1 / 50 : ℝ) := by ring
    _ ≤ Real.exp (beta c 1 * y) * (1 / 50 : ℝ) :=
      mul_le_mul_of_nonneg_right hexp (by norm_num)
    _ ≤ Real.exp (beta c 1 * y) * mainPulse (c.lam * y) :=
      mul_le_mul_of_nonneg_left hpulse (Real.exp_pos _).le

theorem mainMoment_one_lower (c : Parameters) :
    1 / (5000 * c.lam) ≤ mainMoment c (1 : Fin 2) := by
  let f : ℝ → ℝ := f1Integrand c
  have hf : Continuous f := by
    exact f1Integrand_continuous c
  have horder := f1_interval_order c
  have hnonneg : 0 ≤ᵐ[volume.restrict (Ioc (0 : ℝ) (11 / c.lam))] f := by
    refine (ae_restrict_iff' measurableSet_Ioc).mpr ?_
    exact ae_of_all volume (fun y hy => f1_integrand_nonnegative_on_short_interval c hy)
  have hsub :
      (∫ y in (1 / (25 * c.lam) : ℝ)..1 / (20 * c.lam), (1 / 50 : ℝ)) ≤
        ∫ y in (1 / (25 * c.lam) : ℝ)..1 / (20 * c.lam), f y := by
    apply intervalIntegral.integral_mono_on (μ := volume) horder.2.1
    · exact continuous_const.intervalIntegrable _ _
    · exact hf.intervalIntegrable _ _
    · intro y hy
      exact f1_integrand_lower_on_witness_interval c hy
  have hsub_value :
      (∫ _y in (1 / (25 * c.lam) : ℝ)..1 / (20 * c.lam), (1 / 50 : ℝ)) =
        1 / (5000 * c.lam) := by
    simp only [intervalIntegral.integral_const, sub_zero, smul_eq_mul]
    field_simp [c.lam_pos.ne']
    ring
  rw [hsub_value] at hsub
  have hmonotone :
      (∫ y in (1 / (25 * c.lam) : ℝ)..1 / (20 * c.lam), f y) ≤
        ∫ y in (0 : ℝ)..11 / c.lam, f y := by
    exact intervalIntegral.integral_mono_interval (μ := volume)
      horder.1 horder.2.1 horder.2.2 hnonneg (hf.intervalIntegrable _ _)
  rw [mainMoment_log_short]
  change 1 / (5000 * c.lam) ≤ ∫ y in (0 : ℝ)..11 / c.lam, f y
  exact hsub.trans hmonotone

theorem mainMoment_one_pos (c : Parameters) :
    0 < mainMoment c (1 : Fin 2) := by
  exact (div_pos (by norm_num) (mul_pos (by norm_num) c.lam_pos)).trans_le
    (mainMoment_one_lower c)

#print axioms NSRW.P2.mainMoment_one_lower
#print axioms NSRW.P2.mainMoment_one_pos

end NSRW.P2
