import P2_Z01_LocalMassIdentities

/-!
# P2 Z-02: coefficient-to-mass boundary signs

Development implementation, not compiled or admitted yet. The only external
proof dependency is Z01. C04 and the F1--C04 external chain are not imported.

`localMass` is the exact source massMoment at B + log r. The coefficient alias
below is the actual second AXIAL repair coefficient of the same Profile, not
the angular-reset coefficients stored in F.reset. Its positivity is an explicit
hypothesis of the upper-sign theorem. No small-eta existence, IVT, mass-zero
existence, uniqueness, or first-zero proposition is asserted here.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

noncomputable def localMass (F : Profile) (eta r : ℝ) : ℝ :=
  massMoment F.data.core F.amp eta (F.data.core.pulseStart + Real.log r)

noncomputable def localSecondRepairCoefficient (F : Profile) (eta : ℝ) : ℝ :=
  NavierStokes.LocalizedMomentRepair.coefficients
    F.data.core.exponents F.data.core.lower F.data.core.upper
    (debt F.data.core F.amp eta) (1 : Fin 2)

theorem prefixM_pos (c : Parameters) : 0 < prefixM c := by
  have hi : 0 ≤ ∫ y in (0 : ℝ)..c.pulseStart,
      Real.exp y * dropCoefficient c.m y :=
    intervalIntegral.integral_nonneg_of_forall c.pulseStart_pos.le
      (fun y => mul_nonneg (Real.exp_pos y).le (dropCoefficient_bounds c.m y).1)
  unfold prefixM
  linarith

private theorem first_lower_le_lower (c : Parameters) (i : Fin 2) :
    c.lower 0 ≤ c.lower i := by
  fin_cases i
  · exact le_rfl
  · exact (c.lower_lt_upper 0).le.trans (c.intervals_separated 0 1 (by decide))

private theorem first_upper_gt_one (c : Parameters) : 1 < c.upper 0 :=
  (c.one_lt_lower 0).trans (c.lower_lt_upper 0)

private theorem first_bump_zero_after (c : Parameters) (x : ℝ)
    (hx : c.upper 0 ≤ x) :
    NavierStokes.LocalizedMomentRepair.bump (c.lower 0) (c.upper 0) x = 0 := by
  by_contra hb
  have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
    (c.lower 0) (c.upper 0) (c.lower_lt_upper 0)) (subset_tsupport _ hb)
  exact (not_lt_of_ge hx) hs.2

theorem radialPulse_before_first_lower (F : Profile) (eta x : ℝ)
    (hx : x ≤ F.data.core.lower 0) :
    radialPulse F.data.core F.amp eta x =
      F.amp eta * mainPulse (F.data.core.lam * Real.log x) := by
  let c := F.data.core
  have hc : correction c F.amp eta x = 0 := by
    apply correction_zero_of_outside
    intro i hi
    have hlo := first_lower_le_lower c i
    exact (not_lt_of_ge (hx.trans hlo)) hi.1
  change F.amp eta * mainPulse (c.lam * Real.log x) + correction c F.amp eta x = _
  rw [hc, add_zero]

theorem localMass_lower_pos (F : Profile) (eta : ℝ) (heta : 0 < eta) :
    0 < localMass F eta (F.data.core.lower 0) := by
  let c := F.data.core
  have hl : 1 ≤ c.lower 0 := (c.one_lt_lower 0).le
  have hl_end : c.lower 0 ≤ Real.exp c.pulseLength :=
    (c.lower_lt_upper 0).le.trans (c.upper_lt_end 0).le
  have hamp : 0 < F.amp eta :=
    NavierStokes.CorrectedPulseAmplitude.amplitude_pos F.data F.reset.coefficients eta
  have hi : 0 ≤ ∫ x in (1 : ℝ)..c.lower 0,
      x ^ c.exponents 0 * radialPulse c F.amp eta x := by
    apply intervalIntegral.integral_nonneg hl
    intro x hx
    rw [radialPulse_before_first_lower F eta x hx.2]
    exact mul_nonneg (Real.rpow_nonneg (by linarith [hx.1]) _)
      (mul_nonneg hamp.le (NavierStokes.PulseAmplitude.mainPulse_nonneg
        (mul_nonneg c.lam_pos.le (Real.log_nonneg hx.1))))
  have hp := mul_pos (prefixM_pos c) heta
  have hk := mul_pos (momentScale_pos c 0) (shape_pos eta)
  change 0 < massMoment c F.amp eta (c.pulseStart + Real.log (c.lower 0))
  rw [localMass_partial_identity F eta (c.lower 0) hl hl_end]
  exact add_pos_of_pos_of_nonneg hp (mul_nonneg hk.le hi)

theorem secondBumpWeightedMoment_pos (c : Parameters) :
    0 < ∫ x : ℝ, x ^ c.exponents 0 *
      NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x := by
  have hentry := actual_matrix_entry c (0 : Fin 2) (1 : Fin 2)
  change (∫ x : ℝ, x ^ c.exponents 0 *
    NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x) = _ at hentry
  rw [hentry]
  exact mul_pos (rowMoment_pos c 0) (Real.exp_pos _)

theorem upperTail_radialPulse_eq (F : Profile) (eta x : ℝ)
    (hx : F.data.core.upper 0 ≤ x)
    (_hx_end : x ≤ Real.exp F.data.core.pulseLength) :
    radialPulse F.data.core F.amp eta x =
      localSecondRepairCoefficient F eta *
        NavierStokes.LocalizedMomentRepair.bump
          (F.data.core.lower 1) (F.data.core.upper 1) x := by
  let c := F.data.core
  have hexp : Real.exp (11 / c.lam) ≤ x :=
    (c.main_end_lt_lower 0).le.trans ((c.lower_lt_upper 0).le.trans hx)
  have hlog : 11 / c.lam ≤ Real.log x := by
    have h := Real.log_le_log (Real.exp_pos (11 / c.lam)) hexp
    simpa only [Real.log_exp] using h
  have harg : 11 ≤ c.lam * Real.log x := by
    have h := mul_le_mul_of_nonneg_left hlog c.lam_pos.le
    have hid : c.lam * (11 / c.lam) = 11 := by field_simp [c.lam_pos.ne']
    rwa [hid] at h
  have hm := mainPulse_zero_right harg
  have hb := first_bump_zero_after c x hx
  change F.amp eta * mainPulse (c.lam * Real.log x) + correction c F.amp eta x = _
  rw [hm, mul_zero, zero_add]
  simp only [correction, NavierStokes.LocalizedMomentRepair.repair, Fin.sum_univ_two]
  rw [hb, mul_zero, zero_add]
  rfl

theorem secondBumpWeightedMoment_tail_eq (c : Parameters) :
    (∫ x in c.upper 0..Real.exp c.pulseLength,
      x ^ c.exponents 0 *
        NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x) =
    ∫ x : ℝ, x ^ c.exponents 0 *
      NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x := by
  rw [intervalIntegral.integral_eq_integral_of_support_subset]
  intro x hx
  have hb : NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x ≠ 0 := by
    intro hzero
    exact hx (by simp [hzero])
  have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
    (c.lower 1) (c.upper 1) (c.lower_lt_upper 1)) (subset_tsupport _ hb)
  exact ⟨(c.intervals_separated 0 1 (by decide)).trans_lt hs.1,
    hs.2.le.trans (c.upper_lt_end 1).le⟩

theorem localMass_upper_eq_second_tail (F : Profile) (eta : ℝ) :
    localMass F eta (F.data.core.upper 0) =
      -(momentScale F.data.core 0 * shape eta) *
        (localSecondRepairCoefficient F eta *
          (∫ x : ℝ, x ^ F.data.core.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump
              (F.data.core.lower 1) (F.data.core.upper 1) x)) := by
  let c := F.data.core
  change massMoment c F.amp eta (c.pulseStart + Real.log (c.upper 0)) = _
  rw [localMass_tail_identity F eta (c.upper 0)
    (first_upper_gt_one c).le (c.upper_lt_end 0).le]
  have hi : (∫ x in c.upper 0..Real.exp c.pulseLength,
      x ^ c.exponents 0 * radialPulse c F.amp eta x) =
      localSecondRepairCoefficient F eta *
        (∫ x in c.upper 0..Real.exp c.pulseLength,
          x ^ c.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x) := by
    rw [← intervalIntegral.integral_const_mul]
    apply intervalIntegral.integral_congr
    intro x hx
    have hx' := uIcc_of_le (c.upper_lt_end 0).le ▸ hx
    dsimp only
    rw [upperTail_radialPulse_eq F eta x hx'.1 hx'.2]
    ring
  rw [hi, secondBumpWeightedMoment_tail_eq c]

theorem localMass_upper_neg_of_secondCoeff_pos (F : Profile) (eta : ℝ)
    (hc1 : 0 < localSecondRepairCoefficient F eta) :
    localMass F eta (F.data.core.upper 0) < 0 := by
  rw [localMass_upper_eq_second_tail]
  exact mul_neg_of_neg_of_pos
    (neg_neg_of_pos (mul_pos (momentScale_pos F.data.core 0) (shape_pos eta)))
    (mul_pos hc1 (secondBumpWeightedMoment_pos F.data.core))

#print axioms NSRW.P2.prefixM_pos
#print axioms NSRW.P2.radialPulse_before_first_lower
#print axioms NSRW.P2.localMass_lower_pos
#print axioms NSRW.P2.secondBumpWeightedMoment_pos
#print axioms NSRW.P2.upperTail_radialPulse_eq
#print axioms NSRW.P2.secondBumpWeightedMoment_tail_eq
#print axioms NSRW.P2.localMass_upper_eq_second_tail
#print axioms NSRW.P2.localMass_upper_neg_of_secondCoeff_pos

end NSRW.P2
