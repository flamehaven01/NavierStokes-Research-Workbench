import P2_MB08_FixedReset
import P2_MB08_QuadraticBound

/-! Bound the inverse of the source's two-row reset matrix and specialize the reset. -/

open Set MeasureTheory
open NavierStokes AngularMomentReset OutgoingTail UniformAngularReset

namespace NSRW.P2

private theorem mb_template_source_moment_bounds (s : ℝ) (hs₀ : -(6 / 5) ≤ s) (hs₁ : s ≤ 1) :
    3 / 40 ≤ moment s ∧ moment s ≤ 3 / 5 := by
  let f : ℝ → ℝ := fun y => Real.exp (s * y) * template y
  have hf : Integrable f :=
    ((Real.continuous_exp.comp (continuous_const.mul continuous_id)).mul
      template_contDiff.continuous).integrable_of_hasCompactSupport
      template_hasCompactSupport.mul_left
  have hnonneg (y : ℝ) : 0 ≤ f y :=
    mul_nonneg (Real.exp_pos _).le (LocalizedMomentRepair.bump_nonneg _ _ _)
  have hlocal : (∫ y in -(3 / 20 : ℝ)..(3 / 20 : ℝ), f y) = moment s := by
    apply intervalIntegral.integral_eq_integral_of_support_subset
    intro y hy
    have hn : template y ≠ 0 := fun hz => hy (by simp [f, hz])
    have hy' : (y - ((-(3 : ℝ) / 10) + 3 / 10) / 2) / ((3 / 10 - (-(3 : ℝ) / 10)) / 4)
        ∈ Ioo (-1 : ℝ) 1 := by
      rw [← SmoothCutoffs.cutoff_support]
      exact hn
    change -(3 / 20 : ℝ) < y ∧ y ≤ 3 / 20
    have hlo := (lt_div_iff₀ (by norm_num :
      (0 : ℝ) < (3 / 10 - (-(3 : ℝ) / 10)) / 4)).mp hy'.1
    exact ⟨by linarith, (template_support hn).2⟩
  have hs : |s| ≤ 6 / 5 := abs_le.mpr ⟨hs₀, by linarith⟩
  have hweight (y : ℝ) (hy : y ∈ Icc (-(3 / 20 : ℝ)) (3 / 20)) :
      1 / 2 ≤ Real.exp (s * y) ∧ Real.exp (s * y) ≤ 2 := by
    have hp : |s * y| ≤ 9 / 50 := by
      rw [abs_mul]
      exact (mul_le_mul hs (abs_le.mpr hy) (abs_nonneg _) (by norm_num)).trans (by norm_num)
    have hz := abs_le.mp hp
    constructor
    · linarith [Real.add_one_le_exp (s * y), hz.1]
    · have hlog : (9 / 50 : ℝ) ≤ Real.log 2 := by
        linarith [Real.one_sub_inv_le_log_of_pos (by norm_num : (0 : ℝ) < 2)]
      have h := Real.exp_le_exp.mpr (hz.2.trans hlog)
      rwa [Real.exp_log (by norm_num : (0 : ℝ) < 2)] at h
  rw [← hlocal]
  constructor
  · have hplateau : (∫ _ in -(3 / 40 : ℝ)..(3 / 40 : ℝ), (1 / 2 : ℝ)) ≤
        ∫ y in -(3 / 40 : ℝ)..(3 / 40 : ℝ), f y := by
      apply intervalIntegral.integral_mono_on (by norm_num) (continuous_const.intervalIntegrable _ _)
        hf.intervalIntegrable
      intro y hy
      have hb : template y = 1 := by
        unfold template LocalizedMomentRepair.bump
        apply SmoothCutoffs.cutoff_one_of_abs_le
        apply abs_le.mpr
        have hd : (0 : ℝ) < ((3 / 10) - (-3 / 10)) / 4 := by norm_num
        exact ⟨(le_div_iff₀ hd).mpr (by linarith [hy.1]),
          (div_le_iff₀ hd).mpr (by linarith [hy.2])⟩
      simpa only [f, hb, mul_one] using
        (hweight y ⟨by linarith [hy.1], by linarith [hy.2]⟩).1
    have hsub : (∫ y in -(3 / 40 : ℝ)..(3 / 40 : ℝ), f y) ≤
        ∫ y in -(3 / 20 : ℝ)..(3 / 20 : ℝ), f y :=
      intervalIntegral.integral_mono_interval (by norm_num) (by norm_num) (by norm_num)
        ((ae_restrict_iff' measurableSet_Ioc).mpr (ae_of_all volume (fun y _ => hnonneg y)))
        hf.intervalIntegrable
    norm_num [intervalIntegral.integral_const, smul_eq_mul] at hplateau
    exact hplateau.trans hsub
  · have hupper : (∫ y in -(3 / 20 : ℝ)..(3 / 20 : ℝ), f y) ≤
        ∫ _ in -(3 / 20 : ℝ)..(3 / 20 : ℝ), (2 : ℝ) := by
      apply intervalIntegral.integral_mono_on (by norm_num) hf.intervalIntegrable
        (continuous_const.intervalIntegrable _ _)
      intro y hy
      exact (mul_le_mul_of_nonneg_left (LocalizedMomentRepair.bump_le_one _ _ _)
        (Real.exp_pos _).le).trans (by simpa only [mul_one] using (hweight y hy).2)
    norm_num [intervalIntegral.integral_const, smul_eq_mul] at hupper
    exact hupper

theorem mb_source_linear_inverse_norm_le_1000
    (lam : ℝ) (hl : 0 ≤ lam) (hu : lam ≤ 1 / 10) (x : Coeff) :
    ‖(linearEquivNonneg lam hl).symm x‖ ≤ 1000 * ‖x‖ := by
  let A := moment (angularSlope lam)
  let B := moment (pressureSlope lam)
  let E := Real.exp (2 * angularSlope lam)
  let F := Real.exp (2 * pressureSlope lam)
  let y := (linearEquivNonneg lam hl).symm x
  have hA : 3 / 40 ≤ A :=
    (mb_template_source_moment_bounds _ (by unfold angularSlope; linarith)
      (by unfold angularSlope; linarith)).1
  have hB : 3 / 40 ≤ B :=
    (mb_template_source_moment_bounds _ (by unfold pressureSlope; linarith)
      (by unfold pressureSlope; linarith)).1
  have hF : F ≤ 1 := by
    change Real.exp _ ≤ 1
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr (by unfold pressureSlope; linarith)
  have hE : E ≤ 9 := by
    have h : E ≤ Real.exp 2 :=
      Real.exp_le_exp.mpr (by unfold angularSlope; linarith)
    have hpow : Real.exp 2 = Real.exp 1 ^ (2 : ℕ) := by rw [← Real.exp_nat_mul]; norm_num
    rw [hpow] at h
    exact h.trans (by nlinarith [Real.exp_one_lt_three, Real.exp_pos 1])
  have hgap : 1 ≤ E - F := by
    have he := Real.add_one_le_exp (2 * angularSlope lam)
    change 2 * angularSlope lam + 1 ≤ E at he
    unfold angularSlope at he
    linarith
  have hrows : (linearMatrix lam).mulVec y = x :=
    (linearEquivNonneg lam hl).apply_symm_apply x
  have hrow₀ : A * y 0 + E * A * y 1 = x 0 := by
    simpa [linearMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two, A, E] using congrFun hrows 0
  have hrow₁ : 2 * B * y 0 + 2 * (F * B) * y 1 = x 1 := by
    simpa [linearMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two, B, F] using congrFun hrows 1
  let u := x 0 / A
  let v := x 1 / (2 * B)
  have hurow : y 0 + E * y 1 = u := by
    apply (eq_div_iff (show A ≠ 0 by linarith)).mpr
    linear_combination hrow₀
  have hvrow : y 0 + F * y 1 = v := by
    apply (eq_div_iff (show 2 * B ≠ 0 by linarith)).mpr
    linear_combination hrow₁
  have hub : |u| ≤ 14 * ‖x‖ := by
    change |x 0 / A| ≤ _
    rw [abs_div, abs_of_pos (show 0 < A by linarith)]
    apply (div_le_iff₀ (show 0 < A by linarith)).mpr
    calc
      |x 0| ≤ ‖x‖ := norm_le_pi_norm x 0
      _ = 1 * ‖x‖ := (one_mul _).symm
      _ ≤ (14 * A) * ‖x‖ := mul_le_mul_of_nonneg_right (by linarith) (norm_nonneg _)
      _ = _ := by ring
  have hvb : |v| ≤ 7 * ‖x‖ := by
    change |x 1 / (2 * B)| ≤ _
    rw [abs_div, abs_of_pos (show 0 < 2 * B by linarith)]
    apply (div_le_iff₀ (show 0 < 2 * B by linarith)).mpr
    calc
      |x 1| ≤ ‖x‖ := norm_le_pi_norm x 1
      _ = 1 * ‖x‖ := (one_mul _).symm
      _ ≤ (7 * (2 * B)) * ‖x‖ := mul_le_mul_of_nonneg_right (by linarith) (norm_nonneg _)
      _ = _ := by ring
  have hy₀ : (E - F) * y 0 = E * v - F * u := by
    linear_combination E * hvrow - F * hurow
  have hy₁ : (E - F) * y 1 = u - v := by
    linear_combination hurow - hvrow
  have hscale (i : Fin 2) : |y i| ≤ |(E - F) * y i| := by
    rw [abs_mul, abs_of_nonneg (show 0 ≤ E - F by linarith)]
    simpa only [one_mul] using mul_le_mul_of_nonneg_right hgap (abs_nonneg (y i))
  change ‖y‖ ≤ _
  apply (pi_norm_le_iff_of_nonneg (mul_nonneg (by norm_num) (norm_nonneg x))).mpr
  intro i
  rw [Real.norm_eq_abs]
  fin_cases i
  · have he : |E * v| ≤ 9 * (7 * ‖x‖) := by
      rw [abs_mul, abs_of_nonneg (Real.exp_pos _).le]
      exact mul_le_mul hE hvb (abs_nonneg _) (by norm_num)
    have hf : |F * u| ≤ 1 * (14 * ‖x‖) := by
      rw [abs_mul, abs_of_nonneg (Real.exp_pos _).le]
      exact mul_le_mul hF hub (abs_nonneg _) (by norm_num)
    calc
      _ ≤ |(E - F) * y 0| := hscale 0
      _ ≤ |E * v| + |F * u| := by rw [hy₀]; simpa using abs_sub_le (E * v) 0 (F * u)
      _ ≤ _ := by linarith [norm_nonneg x]
  · calc
      _ ≤ |(E - F) * y 1| := hscale 1
      _ ≤ |u| + |v| := by rw [hy₁]; simpa using abs_sub_le u 0 v
      _ ≤ _ := by linarith [norm_nonneg x]

theorem mb_fixed_reset_of_source_jet_bound (d : TailData)
    (hlam : d.core.lam = 1 / 1000000000000)
    (hjet : ∀ (c : Coeff) (y : ℝ),
      |relative c y| ≤ 500 * ‖c‖ ∧ |deriv (relative c) y| ≤ 500 * ‖c‖) :
    Nonempty (ResetWitness d 81162000) := by
  have hsmall : d.core.lam ≤ 1 / 10 := by rw [hlam]; norm_num
  exact mb_fixed_reset_of_operator_bounds d hlam
    (mb_source_linear_inverse_norm_le_1000 _ d.core.lam_pos.le hsmall)
    (mb_source_quadraticCLM_norm_le_one _ d.core.lam_pos.le hsmall) hjet

#print axioms NSRW.P2.mb_source_linear_inverse_norm_le_1000
#print axioms NSRW.P2.mb_fixed_reset_of_source_jet_bound

end NSRW.P2
