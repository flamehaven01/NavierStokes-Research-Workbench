import P2_ZPLUS_J_QuantitativeMargin

/-!
# Fixed-coordinate normalization and a conservative plateau lower bound

This module leaves the previous quantitative proof unchanged. All identities
are exact real identities. `exp t - 1` is not an implementation or an error
bound for floating-point `expm1`. No numerical Profile, coefficient lower bound
q, amplitude hypothesis, or source admissibility certificate is asserted.
-/

noncomputable section

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

def secondNormalizedLower : ℝ := Real.exp (-(23 / 20 : ℝ))
def secondNormalizedUpper : ℝ := Real.exp (-(17 / 20 : ℝ))

/-- Whole-line notation; the next theorem identifies the stated interval integral. -/
def normalizedSecondBumpMoment (c : Parameters) : ℝ :=
  ∫ z : ℝ, z ^ c.exponents 0 * NavierStokes.LocalizedMomentRepair.bump
    secondNormalizedLower secondNormalizedUpper z

private theorem normalized_bounds :
    0 < secondNormalizedLower ∧ secondNormalizedLower < secondNormalizedUpper ∧
      secondNormalizedUpper < 1 := by
  refine ⟨Real.exp_pos _, ?_, ?_⟩
  · apply Real.exp_lt_exp.mpr
    norm_num [secondNormalizedLower, secondNormalizedUpper]
  · rw [secondNormalizedUpper, ← Real.exp_zero]
    exact Real.exp_lt_exp.mpr (by norm_num)

theorem firstRepair_weightGap_exp_eq (c : Parameters) :
    c.upper 0 ^ (-c.lam) - c.lower 1 ^ (-c.lam) =
      Real.exp (-13 + 23 * c.lam / 20) * (Real.exp (17 * c.lam / 10) - 1) := by
  have hu : c.upper 0 ^ (-c.lam) = Real.exp (-13 + 57 * c.lam / 20) := by
    change Real.exp (c.pulseLength - 57 / 20) ^ (-c.lam) = _
    rw [Real.rpow_def_of_pos (Real.exp_pos _), Real.log_exp]
    congr 1
    dsimp [Parameters.pulseLength]
    field_simp [c.lam_pos.ne']
    ring
  have hl : c.lower 1 ^ (-c.lam) = Real.exp (-13 + 23 * c.lam / 20) := by
    change Real.exp (c.pulseLength - 23 / 20) ^ (-c.lam) = _
    rw [Real.rpow_def_of_pos (Real.exp_pos _), Real.log_exp]
    congr 1
    dsimp [Parameters.pulseLength]
    field_simp [c.lam_pos.ne']
    ring
  have he : Real.exp (-13 + 57 * c.lam / 20) =
      Real.exp (-13 + 23 * c.lam / 20) * Real.exp (17 * c.lam / 10) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [hu, hl, he]
  ring

theorem normalizedSecondBumpMoment_eq_interval (c : Parameters) :
    normalizedSecondBumpMoment c =
      ∫ z in secondNormalizedLower..secondNormalizedUpper,
        z ^ c.exponents 0 * NavierStokes.LocalizedMomentRepair.bump
          secondNormalizedLower secondNormalizedUpper z := by
  unfold normalizedSecondBumpMoment
  symm
  apply intervalIntegral.integral_eq_integral_of_support_subset
  intro z hz
  have hb : NavierStokes.LocalizedMomentRepair.bump
      secondNormalizedLower secondNormalizedUpper z ≠ 0 := by
    intro h
    exact hz (by simp [h])
  have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
    _ _ normalized_bounds.2.1) (subset_tsupport _ hb)
  exact ⟨hs.1, hs.2.le⟩

theorem secondBumpWeightedMoment_eq_normalized (c : Parameters) :
    (∫ x : ℝ, x ^ c.exponents 0 * NavierStokes.LocalizedMomentRepair.bump
      (c.lower 1) (c.upper 1) x) =
      Real.exp (c.pulseLength * (1 / 2 - c.lam)) * normalizedSecondBumpMoment c := by
  have hl : c.lower 1 = Real.exp c.pulseLength * secondNormalizedLower := by
    change Real.exp (c.pulseLength - 23 / 20) = _
    rw [secondNormalizedLower, ← Real.exp_add]
    congr 1
  have hu : c.upper 1 = Real.exp c.pulseLength * secondNormalizedUpper := by
    change Real.exp (c.pulseLength - 17 / 20) = _
    rw [secondNormalizedUpper, ← Real.exp_add]
    congr 1
  rw [hl, hu, power_bump_integral_scale (c.exponents 0) (Real.exp_pos _)
    normalized_bounds.1 normalized_bounds.2.1]
  rw [Real.rpow_def_of_pos (Real.exp_pos _), Real.log_exp, ← Real.exp_add]
  have he : c.pulseLength + c.pulseLength * c.exponents 0 =
      c.pulseLength * (1 / 2 - c.lam) := by
    norm_num [Parameters.exponents]
    ring
  rw [he]
  rfl

theorem normalizedSecondBumpMoment_eq_rowMoment (c : Parameters) :
    normalizedSecondBumpMoment c =
      Real.exp (-(1 / 2 - c.lam)) * rowMoment (c.exponents 0) := by
  have hl : secondNormalizedLower = Real.exp (-1) * templateLower := by
    rw [templateLower, ← Real.exp_add, secondNormalizedLower]
    congr 1
    norm_num
  have hu : secondNormalizedUpper = Real.exp (-1) * templateUpper := by
    rw [templateUpper, ← Real.exp_add, secondNormalizedUpper]
    congr 1
    norm_num
  rw [normalizedSecondBumpMoment, hl, hu,
    power_bump_integral_scale (c.exponents 0) (Real.exp_pos _)
      templateLower_pos templateLower_lt_upper]
  rw [Real.rpow_def_of_pos (Real.exp_pos _), Real.log_exp, ← Real.exp_add]
  have he : (-1 : ℝ) + -1 * c.exponents 0 = -(1 / 2 - c.lam) := by
    norm_num [Parameters.exponents]
    ring
  rw [he]
  rfl

private theorem powerBump_intervalIntegrable (a l u : ℝ)
    (hl : 0 < l) (hlu : l ≤ u) :
    IntervalIntegrable (fun z : ℝ => z ^ a *
      NavierStokes.LocalizedMomentRepair.bump l u z) volume l u := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hlu]
  exact (continuousOn_id.rpow_const (fun z hz =>
    Or.inl (ne_of_gt (hl.trans_le hz.1)))).mul
      (NavierStokes.LocalizedMomentRepair.bump_contDiff l u).continuous.continuousOn

private theorem powerBump_plateau_lower (a l u : ℝ)
    (ha : a ≤ 0) (hl : 0 < l) (hlu : l < u) (hu : u ≤ 1) :
    (u - l) / 4 ≤ ∫ z in l..u,
      z ^ a * NavierStokes.LocalizedMomentRepair.bump l u z := by
  let A := (l + u) / 2 - (u - l) / 8
  let B := (l + u) / 2 + (u - l) / 8
  let f : ℝ → ℝ := fun z => z ^ a * NavierStokes.LocalizedMomentRepair.bump l u z
  have hlA : l ≤ A := by dsimp [A]; linarith
  have hAB : A ≤ B := by dsimp [A, B]; linarith
  have hBu : B ≤ u := by dsimp [B]; linarith
  have hA : 0 < A := hl.trans_le hlA
  have hf : IntervalIntegrable f volume l u := powerBump_intervalIntegrable a l u hl hlu.le
  have hfAB : IntervalIntegrable f volume A B := by
    apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le hAB]
    exact (continuousOn_id.rpow_const (fun z hz =>
      Or.inl (ne_of_gt (hA.trans_le hz.1)))).mul
        (NavierStokes.LocalizedMomentRepair.bump_contDiff l u).continuous.continuousOn
  have hsub : (∫ _z in A..B, (1 : ℝ)) ≤ ∫ z in A..B, f z := by
    apply intervalIntegral.integral_mono_on hAB (continuous_const.intervalIntegrable _ _) hfAB
    intro z hz
    have hzpos : 0 < z := hA.trans_le hz.1
    have hzone : z ≤ 1 := hz.2.trans (hBu.trans hu)
    have hp : 1 ≤ z ^ a := by
      rw [Real.rpow_def_of_pos hzpos]
      rw [← Real.exp_zero]
      apply Real.exp_le_exp.mpr
      exact mul_nonneg_of_nonpos_of_nonpos (Real.log_nonpos hzpos.le hzone) ha
    have hb : NavierStokes.LocalizedMomentRepair.bump l u z = 1 := by
      unfold NavierStokes.LocalizedMomentRepair.bump
      apply NavierStokes.SmoothCutoffs.cutoff_one_of_abs_le
      apply abs_le.mpr
      have hd : 0 < (u - l) / 4 := by linarith
      constructor
      · apply (le_div_iff₀ hd).mpr
        dsimp [A, B] at hz
        linarith [hz.1]
      · apply (div_le_iff₀ hd).mpr
        dsimp [A, B] at hz
        linarith [hz.2]
    simpa only [f, hb, mul_one] using hp
  have hvalue : (∫ _z in A..B, (1 : ℝ)) = (u - l) / 4 := by
    simp only [intervalIntegral.integral_const, smul_eq_mul, mul_one]
    dsimp [A, B]
    ring
  rw [hvalue] at hsub
  have hn : 0 ≤ᵐ[volume.restrict (Ioc l u)] f := by
    apply (ae_restrict_iff' measurableSet_Ioc).mpr
    exact ae_of_all volume (fun z hz => mul_nonneg
      (Real.rpow_nonneg (hl.trans hz.1).le a)
      (NavierStokes.LocalizedMomentRepair.bump_nonneg l u z))
  exact hsub.trans (intervalIntegral.integral_mono_interval hlA hAB hBu hn hf)

theorem normalizedSecondBumpMoment_ge_plateau (c : Parameters) :
    (secondNormalizedUpper - secondNormalizedLower) / 4 ≤ normalizedSecondBumpMoment c := by
  rw [normalizedSecondBumpMoment_eq_interval]
  apply powerBump_plateau_lower _ _ _ _ normalized_bounds.1
    normalized_bounds.2.1 normalized_bounds.2.2.le
  norm_num [Parameters.exponents]
  linarith [c.lam_pos]

theorem angularMoment_ge_plateau_margin (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    (momentScale F.data.core 1 * shape eta ^ 2) * localSecondRepairCoefficient F eta *
      (Real.exp (F.data.core.pulseLength * (1 / 2 - F.data.core.lam)) *
        ((secondNormalizedUpper - secondNormalizedLower) / 4)) *
      (F.data.core.upper 0 ^ (-F.data.core.lam) -
        F.data.core.lower 1 ^ (-F.data.core.lam)) ≤ localAngularMoment F eta r := by
  have h := angularMoment_ge_firstRepair_margin F eta r hr hr_upper hM hc1
  rw [secondBumpWeightedMoment_eq_normalized] at h
  have hp : 0 ≤ (momentScale F.data.core 1 * shape eta ^ 2) *
      localSecondRepairCoefficient F eta :=
    (mul_pos (mul_pos (momentScale_pos _ 1) (sq_pos_of_pos (shape_pos eta))) hc1).le
  exact (mul_le_mul_of_nonneg_right
    (mul_le_mul_of_nonneg_left
      (mul_le_mul_of_nonneg_left (normalizedSecondBumpMoment_ge_plateau F.data.core)
        (Real.exp_pos _).le) hp)
    (firstRepair_weightGap_pos F.data.core).le).trans h

#check NSRW.P2.firstRepair_weightGap_exp_eq
#check NSRW.P2.normalizedSecondBumpMoment_eq_interval
#check NSRW.P2.secondBumpWeightedMoment_eq_normalized
#check NSRW.P2.normalizedSecondBumpMoment_eq_rowMoment
#check NSRW.P2.normalizedSecondBumpMoment_ge_plateau
#check NSRW.P2.angularMoment_ge_plateau_margin

#print axioms NSRW.P2.firstRepair_weightGap_exp_eq
#print axioms NSRW.P2.normalizedSecondBumpMoment_eq_interval
#print axioms NSRW.P2.secondBumpWeightedMoment_eq_normalized
#print axioms NSRW.P2.normalizedSecondBumpMoment_eq_rowMoment
#print axioms NSRW.P2.normalizedSecondBumpMoment_ge_plateau
#print axioms NSRW.P2.angularMoment_ge_plateau_margin

end NSRW.P2
