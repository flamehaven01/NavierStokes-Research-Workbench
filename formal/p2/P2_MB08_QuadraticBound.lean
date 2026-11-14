import NavierStokes.UniformAngularReset

/-! A bound on the original pressure quadratic map using the two bump supports. -/

open Set MeasureTheory
open NavierStokes.AngularMomentReset

namespace NSRW.P2

private theorem mb_quadraticMoment_le (lam : ℝ) (j : Fin 2) (C : ℝ)
    (hweight : ∀ y ∈ Icc (2 * (j.val : ℝ) - 4 / 25) (2 * (j.val : ℝ) + 4 / 25),
      Real.exp (pressureSlope lam * y) ≤ C) :
    quadraticMoment lam j ≤ C * (8 / 25) := by
  let a := 2 * (j.val : ℝ) - 4 / 25
  let b := 2 * (j.val : ℝ) + 4 / 25
  have hab : a ≤ b := by dsimp [a, b]; linarith
  have hloc : (∫ y in a..b, Real.exp (pressureSlope lam * y) * (bump j y) ^ 2) =
      quadraticMoment lam j := by
    unfold quadraticMoment
    apply intervalIntegral.integral_eq_integral_of_support_subset
    intro y hy
    have hn : bump j y ≠ 0 := by
      intro hz
      exact hy (by simp [hz])
    have hs := bump_support j hn
    change a < y ∧ y ≤ b
    constructor
    · dsimp [a]
      linarith [hs.1]
    · dsimp [b]
      linarith [hs.2]
  rw [← hloc]
  calc
    _ ≤ ∫ _ in a..b, C := by
      apply intervalIntegral.integral_mono_on hab
        (weighted_bump_sq_integrable (pressureSlope lam) j).intervalIntegrable
        (continuous_const.intervalIntegrable _ _)
      intro y hy
      exact (mul_le_mul_of_nonneg_left
        (by nlinarith [bump_nonneg j y, bump_le_one j y,
          mul_nonneg (bump_nonneg j y) (sub_nonneg.mpr (bump_le_one j y))] :
          (bump j y) ^ 2 ≤ 1) (Real.exp_pos _).le).trans
        (by simpa using hweight y hy)
    _ = _ := by
      rw [intervalIntegral.integral_const, smul_eq_mul]
      dsimp [a, b]
      ring

theorem mb_source_quadraticCLM_norm_le_one (lam : ℝ) (hl : 0 ≤ lam)
    (hu : lam ≤ 1 / 10) : ‖quadraticCLM lam‖ ≤ 1 := by
  have hp : -(6 / 5 : ℝ) ≤ pressureSlope lam ∧ pressureSlope lam ≤ 0 := by
    unfold pressureSlope
    constructor <;> linarith
  have h0 : quadraticMoment lam 0 ≤ 2 * (8 / 25) := by
    apply mb_quadraticMoment_le lam 0 2
    intro y hy
    simp only [Fin.val_zero, Nat.cast_zero, mul_zero, zero_sub, zero_add] at hy
    change -(4 / 25 : ℝ) ≤ y ∧ y ≤ 4 / 25 at hy
    have hex : pressureSlope lam * y ≤ 24 / 125 := by
      nlinarith only [mul_nonneg (sub_nonneg.mpr hp.2) (sub_nonneg.mpr hy.1),
        hp.1]
    have harg : (24 / 125 : ℝ) < Real.log 2 := by
      linarith [Real.one_sub_inv_le_log_of_pos (by norm_num : (0 : ℝ) < 2)]
    have h := Real.exp_le_exp.mpr (hex.trans harg.le)
    rwa [Real.exp_log (by norm_num : (0 : ℝ) < 2)] at h
  have h1 : quadraticMoment lam 1 ≤ 1 * (8 / 25) := by
    apply mb_quadraticMoment_le lam 1 1
    intro y hy
    have hy0 : 0 ≤ y := by
      norm_num at hy
      linarith [hy.1]
    simpa using Real.exp_le_exp.mpr (mul_nonpos_of_nonpos_of_nonneg hp.2 hy0)
  have hnonneg (j : Fin 2) : 0 ≤ quadraticMoment lam j := by
    exact integral_nonneg (fun _ => mul_nonneg (Real.exp_pos _).le (sq_nonneg _))
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro c
  rw [one_mul]
  apply ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg c)
  intro d
  apply (pi_norm_le_iff_of_nonneg (mul_nonneg (norm_nonneg c) (norm_nonneg d))).mpr
  intro i
  rw [quadraticCLM_apply]
  fin_cases i
  · simpa using mul_nonneg (norm_nonneg c) (norm_nonneg d)
  · change ‖quadraticMoment lam 0 * c 0 * d 0 + quadraticMoment lam 1 * c 1 * d 1‖ ≤ _
    have hb (j : Fin 2) : ‖quadraticMoment lam j * c j * d j‖ ≤
        quadraticMoment lam j * (‖c‖ * ‖d‖) := by
      rw [norm_mul, norm_mul, Real.norm_of_nonneg (hnonneg j), mul_assoc]
      exact mul_le_mul_of_nonneg_left
        (mul_le_mul (norm_le_pi_norm c j) (norm_le_pi_norm d j)
          (norm_nonneg _) (norm_nonneg _)) (hnonneg j)
    calc
      _ ≤ ‖quadraticMoment lam 0 * c 0 * d 0‖ + ‖quadraticMoment lam 1 * c 1 * d 1‖ :=
        norm_add_le _ _
      _ ≤ _ := (add_le_add (hb 0) (hb 1)).trans (by
        rw [← add_mul]
        simpa only [one_mul] using mul_le_mul_of_nonneg_right
          (show quadraticMoment lam 0 + quadraticMoment lam 1 ≤ 1 by linarith)
          (mul_nonneg (norm_nonneg c) (norm_nonneg d)))

#print axioms NSRW.P2.mb_source_quadraticCLM_norm_le_one

end NSRW.P2
