import P2_C03_ActualCoefficientAtZero

/-!
# MomentBound MB-04 — source-coefficient bridge (development source)

Exact-real, source-typed statements. No numerical source Profile or evaluation
of the positive scale is constructed here. In particular, a Python record with
B_coarse > 0 is not by itself a bound on the actual coefficient.

This first development surface exposes the strong L2 estimate without referring
to private declarations, derives the prefix-only row-elimination sign from the
actual normalized repair system, and proves the final conditional reduction.
The required source-derived main and prefix scale inequalities remain *explicit
premises* of the conditional theorem; they must be discharged separately before
claiming a complete MB-04 source-to-B bridge.

No earlier admitted modules are changed. This file has not been Lean-compiled,
and it has no claim authority or admission receipt.
-/

noncomputable section

open Set MeasureTheory
open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds
open NavierStokes.OutgoingProfile

namespace NSRW.P2

/-! ## Strong explicit L2 comparison — reconstructed, not a private import -/

private theorem mb_beta_zero_eq_one_add_lam (c : Parameters) :
    beta c 0 = beta c 1 + c.lam := by
  norm_num [beta, Parameters.exponents]
  ring

private theorem mb_lam_center_gap_le (c : Parameters) {y : ℝ}
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

private theorem mb_integrand_continuous (c : Parameters) (i : Fin 2) :
    Continuous (fun y : ℝ =>
      Real.exp (beta c i * (y - center c 0)) * mainPulse (c.lam * y)) := by
  exact (Real.continuous_exp.comp
    (continuous_const.mul (continuous_id.sub continuous_const))).mul
      (mainPulse_contDiff.continuous.comp (continuous_const.mul continuous_id))

private theorem mb_integrand_zero_le_scaled_one (c : Parameters) {y : ℝ}
    (hy : y ∈ Icc (0 : ℝ) (11 / c.lam)) :
    Real.exp (beta c 0 * (y - center c 0)) * mainPulse (c.lam * y) ≤
      Real.exp (-2 + 3 * c.lam) *
        (Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y)) := by
  have hgap := mb_lam_center_gap_le c hy.2
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
      rw [mb_beta_zero_eq_one_add_lam c]
      rw [show (beta c 1 + c.lam) * (y - center c 0) =
        c.lam * (y - center c 0) + beta c 1 * (y - center c 0) by ring,
        Real.exp_add]
      ring
    _ ≤ Real.exp (-2 + 3 * c.lam) *
          (Real.exp (beta c 1 * (y - center c 0)) * mainPulse (c.lam * y)) :=
      mul_le_mul_of_nonneg_right hexp hone_nonneg

theorem mb_normalizedMainMoment_zero_le_decay_one (c : Parameters) :
    normalizedMainMoment c 0 ≤
      Real.exp (-2 + 3 * c.lam) * normalizedMainMoment c 1 := by
  rw [normalizedMainMoment_log_short c 0, normalizedMainMoment_log_short c 1,
    ← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_mono_on (μ := volume)
    (div_nonneg (by norm_num) c.lam_pos.le)
  · exact (mb_integrand_continuous c 0).intervalIntegrable _ _
  · exact (continuous_const.mul (mb_integrand_continuous c 1)).intervalIntegrable _ _
  · intro y hy
    exact mb_integrand_zero_le_scaled_one c hy

/-! ## Prefix-only coefficient from the source-normalized 2x2 system -/

theorem mb_prefix_one_eq_row_difference (c : Parameters) :
    affineCoefficients c 1 0 1 =
      ((Real.exp (-(beta c 1 * center c 0)) * prefixCoefficient c 1) /
          rowMoment (c.exponents 1) -
        (Real.exp (-(beta c 0 * center c 0)) * prefixCoefficient c 0) /
          rowMoment (c.exponents 0)) /
        (Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1)) := by
  have hs := actual_coefficients_normalized_system c (affineDebt c 1 0)
  have h0 := congrFun hs 0
  have h1 := congrFun hs 1
  simp only [Matrix.mulVec, dotProduct, Fin.sum_univ_two, normalizedMatrix_entry] at h0 h1
  norm_num at h0 h1
  change rowMoment (c.exponents 0) * affineCoefficients c 1 0 0 +
      (rowMoment (c.exponents 0) * Real.exp (2 * beta c 0)) *
        affineCoefficients c 1 0 1 = normalizedDebt c (affineDebt c 1 0) 0 at h0
  change rowMoment (c.exponents 1) * affineCoefficients c 1 0 0 +
      (rowMoment (c.exponents 1) * Real.exp (2 * beta c 1)) *
        affineCoefficients c 1 0 1 = normalizedDebt c (affineDebt c 1 0) 1 at h1
  have hd0 : normalizedDebt c (affineDebt c 1 0) 0 =
      -(Real.exp (-(beta c 0 * center c 0)) * prefixCoefficient c 0) := by
    unfold normalizedDebt affineDebt
    ring
  have hd1 : normalizedDebt c (affineDebt c 1 0) 1 =
      -(Real.exp (-(beta c 1 * center c 0)) * prefixCoefficient c 1) := by
    unfold normalizedDebt affineDebt
    ring
  have hrow0 : affineCoefficients c 1 0 0 +
      Real.exp (2 * beta c 0) * affineCoefficients c 1 0 1 =
      -(Real.exp (-(beta c 0 * center c 0)) * prefixCoefficient c 0) /
        rowMoment (c.exponents 0) :=
    (eq_div_iff (rowMoment_pos c 0).ne').mpr (by rw [hd0] at h0; nlinarith [h0])
  have hrow1 : affineCoefficients c 1 0 0 +
      Real.exp (2 * beta c 1) * affineCoefficients c 1 0 1 =
      -(Real.exp (-(beta c 1 * center c 0)) * prefixCoefficient c 1) /
        rowMoment (c.exponents 1) :=
    (eq_div_iff (rowMoment_pos c 1).ne').mpr (by rw [hd1] at h1; nlinarith [h1])
  apply (eq_div_iff (mainOnly_separation_gap_pos c).ne').mpr
  simp only [neg_div] at hrow0 hrow1
  linear_combination hrow0 - hrow1

/-! ## Positive symbolic scale and exact coefficient identity -/

noncomputable def mbCommonScale (c : Parameters) : ℝ :=
  Real.exp (-(beta c 1 * center c 0)) /
    (rowMoment (c.exponents 1) *
      (Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1)))

theorem mbCommonScale_pos (c : Parameters) : 0 < mbCommonScale c := by
  unfold mbCommonScale
  exact div_pos (Real.exp_pos _)
    (mul_pos (rowMoment_pos c 1) (mainOnly_separation_gap_pos c))

noncomputable def mbQStar (c : Parameters) (eta : ℝ) : ℝ :=
  (9 / 10 : ℝ) * affineCoefficients c 0 1 1 -
    |parameterPolynomial eta| * |affineCoefficients c 1 0 1|

/-- Source-affine C01/C02 coefficient identity at the same Profile and eta. -/
theorem mb_actualSecondRepairCoefficient_eq (F : Profile) (eta : ℝ) :
    actualSecondRepairCoefficient F eta =
      parameterPolynomial eta * affineCoefficients F.data.core 1 0 1 +
        F.amp eta * affineCoefficients F.data.core 0 1 1 := by
  simpa only [actualSecondRepairCoefficient, parameterPolynomial, Profile.amp] using
    profile_secondRepairCoefficient_decomposition F eta

/-- This is conditional on the actual Profile amplitude, not on a sampled number. -/
theorem mb_actualSecondRepairCoefficient_gt_qStar (F : Profile) (eta : ℝ)
    (hAmp : (9 / 10 : ℝ) < F.amp eta) :
    mbQStar F.data.core eta < actualSecondRepairCoefficient F eta := by
  let c := F.data.core
  have hmain : (9 / 10 : ℝ) * affineCoefficients c 0 1 1 <
      F.amp eta * affineCoefficients c 0 1 1 :=
    mul_lt_mul_of_pos_right hAmp (affineCoefficients_main_one_pos c)
  have hpref : -(|parameterPolynomial eta| * |affineCoefficients c 1 0 1|) ≤
      parameterPolynomial eta * affineCoefficients c 1 0 1 := by
    simpa only [abs_mul] using
      (neg_abs_le (parameterPolynomial eta * affineCoefficients c 1 0 1))
  have heq := mb_actualSecondRepairCoefficient_eq F eta
  unfold mbQStar
  rw [heq]
  dsimp [c] at hmain hpref ⊢
  linarith

/-! ## Explicit bridge obligations: these must still be proved for source c -/

noncomputable def mbCoarseBound (c : Parameters) (eta : ℝ) : ℝ :=
  (9 / 10 : ℝ) * (1 / (10000 * c.lam)) -
    |parameterPolynomial eta| * (328 + 3099396717 / 2)

/-- Correct scaled inequality; the two source coefficient bounds are explicit
premises, not silently inferred from the positive rational B record. -/
theorem mb_qStar_ge_scaled_coarse (c : Parameters) (eta : ℝ)
    (hmain : mbCommonScale c * (1 / (10000 * c.lam)) ≤
      affineCoefficients c 0 1 1)
    (hprefix : |affineCoefficients c 1 0 1| ≤
      mbCommonScale c * (328 + 3099396717 / 2)) :
    mbCommonScale c * mbCoarseBound c eta ≤ mbQStar c eta := by
  have hm := mul_le_mul_of_nonneg_left hmain (by norm_num : (0 : ℝ) ≤ 9 / 10)
  have hp := mul_le_mul_of_nonneg_left hprefix (abs_nonneg (parameterPolynomial eta))
  unfold mbCoarseBound mbQStar
  calc
    mbCommonScale c * ((9 / 10 : ℝ) * (1 / (10000 * c.lam)) -
          |parameterPolynomial eta| * (328 + 3099396717 / 2)) =
        (9 / 10 : ℝ) * (mbCommonScale c * (1 / (10000 * c.lam))) -
          |parameterPolynomial eta| *
            (mbCommonScale c * (328 + 3099396717 / 2)) := by ring
    _ ≤ (9 / 10 : ℝ) * affineCoefficients c 0 1 1 -
          |parameterPolynomial eta| * |affineCoefficients c 1 0 1| :=
      sub_le_sub hm hp

/-- Conditional actual-c1 consequence, keeping source c, F and eta bound together.
No source admissibility or numerical evaluation is inferred from this theorem. -/
theorem mb_actualSecondRepairCoefficient_gt_scaled_coarse (F : Profile) (eta : ℝ)
    (hAmp : (9 / 10 : ℝ) < F.amp eta)
    (hmain : mbCommonScale F.data.core * (1 / (10000 * F.data.core.lam)) ≤
      affineCoefficients F.data.core 0 1 1)
    (hprefix : |affineCoefficients F.data.core 1 0 1| ≤
      mbCommonScale F.data.core * (328 + 3099396717 / 2)) :
    mbCommonScale F.data.core * mbCoarseBound F.data.core eta <
      actualSecondRepairCoefficient F eta := by
  exact (mb_qStar_ge_scaled_coarse F.data.core eta hmain hprefix).trans_lt
    (mb_actualSecondRepairCoefficient_gt_qStar F eta hAmp)

/-- Positivity also requires the coarse bound to be positive at the chosen
parameters. A Python Fraction result cannot discharge this Lean assumption. -/
theorem mb_actualSecondRepairCoefficient_pos_of_scaled_coarse (F : Profile) (eta : ℝ)
    (hAmp : (9 / 10 : ℝ) < F.amp eta)
    (hmain : mbCommonScale F.data.core * (1 / (10000 * F.data.core.lam)) ≤
      affineCoefficients F.data.core 0 1 1)
    (hprefix : |affineCoefficients F.data.core 1 0 1| ≤
      mbCommonScale F.data.core * (328 + 3099396717 / 2))
    (hB : 0 < mbCoarseBound F.data.core eta) :
    0 < actualSecondRepairCoefficient F eta := by
  exact (mul_pos (mbCommonScale_pos F.data.core) hB).trans
    (mb_actualSecondRepairCoefficient_gt_scaled_coarse F eta hAmp hmain hprefix)

#check NSRW.P2.mb_normalizedMainMoment_zero_le_decay_one
#check NSRW.P2.mb_prefix_one_eq_row_difference
#check NSRW.P2.mbCommonScale_pos
#check NSRW.P2.mb_actualSecondRepairCoefficient_eq
#check NSRW.P2.mb_actualSecondRepairCoefficient_gt_qStar
#check NSRW.P2.mb_qStar_ge_scaled_coarse
#check NSRW.P2.mb_actualSecondRepairCoefficient_gt_scaled_coarse
#check NSRW.P2.mb_actualSecondRepairCoefficient_pos_of_scaled_coarse

#print axioms NSRW.P2.mb_normalizedMainMoment_zero_le_decay_one
#print axioms NSRW.P2.mb_prefix_one_eq_row_difference
#print axioms NSRW.P2.mbCommonScale_pos
#print axioms NSRW.P2.mb_actualSecondRepairCoefficient_eq
#print axioms NSRW.P2.mb_actualSecondRepairCoefficient_gt_qStar
#print axioms NSRW.P2.mb_qStar_ge_scaled_coarse
#print axioms NSRW.P2.mb_actualSecondRepairCoefficient_gt_scaled_coarse
#print axioms NSRW.P2.mb_actualSecondRepairCoefficient_pos_of_scaled_coarse

end NSRW.P2
