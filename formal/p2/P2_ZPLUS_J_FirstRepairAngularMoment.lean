import P2_Z02_BoundaryMassSigns

/-!
# P2 Z+J: a conditional first-repair angular-moment mismatch

Development implementation; compilation and claim admission are separate.
For the SAME fixed source Profile and local radial coordinate, an interior
first-window mass zero and positive second axial repair coefficient force
strictly positive angular moment. No eta sign, C04 epsilon, IVT witness,
uniqueness, simple-zero, Q pole/limit, or source Profile.J coordinate bridge
is asserted here. Z04-core bytes are not modified or imported.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

noncomputable def localAngularMoment (F : Profile) (eta r : ℝ) : ℝ :=
  angularMoment F.data.core F.amp eta (F.data.core.pulseStart + Real.log r)

noncomputable def localFirstRepairCoefficient (F : Profile) (eta : ℝ) : ℝ :=
  NavierStokes.LocalizedMomentRepair.coefficients
    F.data.core.exponents F.data.core.lower F.data.core.upper
    (debt F.data.core F.amp eta) (0 : Fin 2)

/-- T_j is index 0; S_j is index 1. Both use the same future interval r..R. -/
noncomputable def repairBumpTail (c : Parameters) (i j : Fin 2) (r : ℝ) : ℝ :=
  ∫ x in r..Real.exp c.pulseLength,
    x ^ c.exponents i *
      NavierStokes.LocalizedMomentRepair.bump (c.lower j) (c.upper j) x

theorem localAngularMoment_partial_identity (F : Profile) (eta r : ℝ)
    (hr : 1 ≤ r) (_hr_end : r ≤ Real.exp F.data.core.pulseLength) :
    localAngularMoment F eta r =
      prefixJ F.data.core * eta * shape eta +
        (momentScale F.data.core 1 * shape eta ^ 2) *
          (∫ x in (1 : ℝ)..r,
            x ^ F.data.core.exponents 1 * radialPulse F.data.core F.amp eta x) := by
  let c := F.data.core
  have hr_pos : 0 < r := lt_of_lt_of_le zero_lt_one hr
  have hlog : 0 ≤ Real.log r := Real.log_nonneg hr
  have hE : Continuous (fun t => angular c.P c.dropLength c.lam (t, eta)) :=
    ((angular_contDiff c.P c.dropLength c.lam).comp
      (contDiff_id.prodMk contDiff_const)).continuous
  have hF : Continuous (fun t => Real.sqrt 2 * Real.exp (3 * t / 2) *
      angular c.P c.dropLength c.lam (t, eta) * axial c F.amp (t, eta)) :=
    ((continuous_const.mul (Real.continuous_exp.comp
      ((continuous_const.mul continuous_id).div_const 2))).mul hE).mul
      (axial_radial_contDiff c F.amp eta).continuous
  have hsplit := intervalIntegral.integral_add_adjacent_intervals (μ := volume)
    (hF.intervalIntegrable 0 c.pulseStart)
    (hF.intervalIntegrable c.pulseStart (c.pulseStart + Real.log r))
  have hI : (∫ t in c.pulseStart..c.pulseStart + Real.log r,
      Real.sqrt 2 * Real.exp (3 * t / 2) *
        angular c.P c.dropLength c.lam (t, eta) * axial c F.amp (t, eta)) =
      (momentScale c 1 * shape eta ^ 2) *
        (∫ x in (1 : ℝ)..r, x ^ c.exponents 1 * radialPulse c F.amp eta x) := by
    calc
      _ = ∫ t in c.pulseStart..c.pulseStart + Real.log r,
          (momentScale c 1 * shape eta ^ 2) *
            (Real.exp ((c.exponents 1 + 1) * (t - c.pulseStart)) *
              radialPulse c F.amp eta (Real.exp (t - c.pulseStart))) := by
        apply intervalIntegral.integral_congr
        intro t ht
        apply angular_integrand_pulse c F.amp eta
        exact (uIcc_of_le (show c.pulseStart ≤ c.pulseStart + Real.log r by
          linarith) ▸ ht).1
      _ = _ := by
        rw [intervalIntegral.integral_const_mul]
        rw [exp_weight_substitution (radialPulse_continuousOn c F.amp eta)
          (c.exponents 1) c.pulseStart (Real.log r)]
        rw [Real.exp_log hr_pos]
  change angularMoment c F.amp eta (c.pulseStart + Real.log r) = _
  calc
    _ = angularMoment c F.amp eta c.pulseStart +
        (∫ t in c.pulseStart..c.pulseStart + Real.log r,
          Real.sqrt 2 * Real.exp (3 * t / 2) *
            angular c.P c.dropLength c.lam (t, eta) * axial c F.amp (t, eta)) := by
      unfold angularMoment
      rw [← hsplit]
      ring
    _ = _ := by rw [angularMoment_at_pulseStart, hI]

theorem localAngularMoment_tail_identity (F : Profile) (eta r : ℝ)
    (hr : 1 ≤ r) (hr_end : r ≤ Real.exp F.data.core.pulseLength) :
    localAngularMoment F eta r =
      -(momentScale F.data.core 1 * shape eta ^ 2) *
        (∫ x in r..Real.exp F.data.core.pulseLength,
          x ^ F.data.core.exponents 1 * radialPulse F.data.core F.amp eta x) := by
  let c := F.data.core
  let g : ℝ → ℝ := fun x => x ^ c.exponents 1 * radialPulse c F.amp eta x
  have hg : ContinuousOn g (Icc 1 (Real.exp c.pulseLength)) := by
    apply (continuousOn_id.rpow_const (fun x hx =>
      Or.inl (ne_of_gt (lt_of_lt_of_le zero_lt_one hx.1)))).mul
    exact (radialPulse_continuousOn c F.amp eta).mono
      (fun x hx => lt_of_lt_of_le zero_lt_one hx.1)
  have hg_left : IntervalIntegrable g volume 1 r := by
    apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le hr]
    exact hg.mono (fun x hx => ⟨hx.1, hx.2.trans hr_end⟩)
  have hg_right : IntervalIntegrable g volume r (Real.exp c.pulseLength) := by
    apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le hr_end]
    exact hg.mono (fun x hx => ⟨hr.trans hx.1, hx.2⟩)
  have hsplit := intervalIntegral.integral_add_adjacent_intervals hg_left hg_right
  have hcancel := (pulse_closes_prefix c F.amp eta).2
  rw [localAngularMoment_partial_identity F eta r hr hr_end]
  change prefixJ c * eta * shape eta + (momentScale c 1 * shape eta ^ 2) *
    (∫ x in 1..r, g x) =
      -(momentScale c 1 * shape eta ^ 2) * (∫ x in r..Real.exp c.pulseLength, g x)
  change prefixJ c * eta * shape eta + (momentScale c 1 * shape eta ^ 2) *
    (∫ x in (1 : ℝ)..Real.exp c.pulseLength, g x) = 0 at hcancel
  rw [← hsplit] at hcancel
  nlinarith [hcancel]

theorem first_upper_lt_second_lower (c : Parameters) : c.upper 0 < c.lower 1 := by
  apply Real.exp_lt_exp.mpr
  norm_num [Parameters.upper, Parameters.lower]

theorem secondExponent_eq_first_sub_lam (c : Parameters) :
    c.exponents 1 = c.exponents 0 + (-c.lam) := by
  norm_num [Parameters.exponents] <;> ring

theorem future_radialPulse_eq_two_bumps (F : Profile) (eta r x : ℝ)
    (hr : F.data.core.lower 0 < r) (hx : r ≤ x) :
    radialPulse F.data.core F.amp eta x =
      localFirstRepairCoefficient F eta *
        NavierStokes.LocalizedMomentRepair.bump
          (F.data.core.lower 0) (F.data.core.upper 0) x +
      localSecondRepairCoefficient F eta *
        NavierStokes.LocalizedMomentRepair.bump
          (F.data.core.lower 1) (F.data.core.upper 1) x := by
  let c := F.data.core
  have hexp : Real.exp (11 / c.lam) ≤ x :=
    (c.main_end_lt_lower 0).le.trans (hr.le.trans hx)
  have hlog : 11 / c.lam ≤ Real.log x := by
    have h := Real.log_le_log (Real.exp_pos (11 / c.lam)) hexp
    simpa only [Real.log_exp] using h
  have harg : 11 ≤ c.lam * Real.log x := by
    have h := mul_le_mul_of_nonneg_left hlog c.lam_pos.le
    have hid : c.lam * (11 / c.lam) = 11 := by field_simp [c.lam_pos.ne']
    rwa [hid] at h
  change F.amp eta * mainPulse (c.lam * Real.log x) + correction c F.amp eta x = _
  rw [mainPulse_zero_right harg, mul_zero, zero_add]
  simp only [correction, NavierStokes.LocalizedMomentRepair.repair, Fin.sum_univ_two]
  rfl

private theorem weighted_bump_intervalIntegrable (c : Parameters) (i j : Fin 2)
    (r : ℝ) (hr : 0 < r) (hr_end : r ≤ Real.exp c.pulseLength) :
    IntervalIntegrable (fun x => x ^ c.exponents i *
      NavierStokes.LocalizedMomentRepair.bump (c.lower j) (c.upper j) x)
      volume r (Real.exp c.pulseLength) := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hr_end]
  exact (continuousOn_id.rpow_const (fun x hx =>
    Or.inl (ne_of_gt (hr.trans_le hx.1)))).mul
      (NavierStokes.LocalizedMomentRepair.bump_contDiff _ _).continuous.continuousOn

theorem weighted_future_integral_eq_two_tails (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (i : Fin 2) :
    (∫ x in r..Real.exp F.data.core.pulseLength,
      x ^ F.data.core.exponents i * radialPulse F.data.core F.amp eta x) =
      localFirstRepairCoefficient F eta * repairBumpTail F.data.core i 0 r +
      localSecondRepairCoefficient F eta * repairBumpTail F.data.core i 1 r := by
  let c := F.data.core
  have hr_pos := (c.lower_pos 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have h0 := (weighted_bump_intervalIntegrable c i 0 r hr_pos hr_end).const_mul
    (localFirstRepairCoefficient F eta)
  have h1 := (weighted_bump_intervalIntegrable c i 1 r hr_pos hr_end).const_mul
    (localSecondRepairCoefficient F eta)
  calc
    _ = ∫ x in r..Real.exp c.pulseLength,
        localFirstRepairCoefficient F eta *
            (x ^ c.exponents i * NavierStokes.LocalizedMomentRepair.bump
              (c.lower 0) (c.upper 0) x) +
          localSecondRepairCoefficient F eta *
            (x ^ c.exponents i * NavierStokes.LocalizedMomentRepair.bump
              (c.lower 1) (c.upper 1) x) := by
      apply intervalIntegral.integral_congr
      intro x hx
      have hx' := uIcc_of_le hr_end ▸ hx
      dsimp only
      rw [future_radialPulse_eq_two_bumps F eta r x hr hx'.1]
      ring
    _ = _ := by
      rw [intervalIntegral.integral_add h0 h1,
        intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul]
      rfl

theorem secondBump_massTail_pos (c : Parameters) (r : ℝ) (hr : r < c.upper 0) :
    0 < repairBumpTail c 0 1 r := by
  have heq : repairBumpTail c 0 1 r =
      ∫ x : ℝ, x ^ c.exponents 0 *
        NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x := by
    unfold repairBumpTail
    rw [intervalIntegral.integral_eq_integral_of_support_subset]
    intro x hx
    have hb : NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x ≠ 0 := by
      intro hz
      exact hx (by simp [hz])
    have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
      (c.lower 1) (c.upper 1) (c.lower_lt_upper 1)) (subset_tsupport _ hb)
    exact ⟨(hr.trans (first_upper_lt_second_lower c)).trans hs.1,
      hs.2.le.trans (c.upper_lt_end 1).le⟩
  rw [heq]
  exact secondBumpWeightedMoment_pos c

theorem firstRepair_mass_zero_tail_balance (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) :
    localFirstRepairCoefficient F eta * repairBumpTail F.data.core 0 0 r +
      localSecondRepairCoefficient F eta * repairBumpTail F.data.core 0 1 r = 0 := by
  have hr_one := (F.data.core.one_lt_lower 0).trans hr
  have hr_end := (hr_upper.trans (F.data.core.upper_lt_end 0)).le
  change massMoment F.data.core F.amp eta (F.data.core.pulseStart + Real.log r) = 0 at hM
  rw [localMass_tail_identity F eta r hr_one.le hr_end,
    weighted_future_integral_eq_two_tails F eta r hr hr_upper 0] at hM
  have hk := mul_pos (momentScale_pos F.data.core 0) (shape_pos eta)
  exact (mul_eq_zero.mp hM).resolve_left (neg_ne_zero.mpr hk.ne')

theorem firstBumpTail_pos_and_firstCoeff_neg (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < repairBumpTail F.data.core 0 0 r ∧ localFirstRepairCoefficient F eta < 0 := by
  let c := F.data.core
  have hr_pos := (c.lower_pos 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have hT0 : 0 ≤ repairBumpTail c 0 0 r := by
    apply intervalIntegral.integral_nonneg hr_end
    intro x hx
    exact mul_nonneg (Real.rpow_nonneg (hr_pos.trans_le hx.1).le _)
      (NavierStokes.LocalizedMomentRepair.bump_nonneg _ _ _)
  have hT1 := secondBump_massTail_pos c r hr_upper
  have hbalance := firstRepair_mass_zero_tail_balance F eta r hr hr_upper hM
  have hprod : localFirstRepairCoefficient F eta * repairBumpTail c 0 0 r < 0 := by
    linarith [mul_pos hc1 hT1]
  have hT0_pos : 0 < repairBumpTail c 0 0 r := by
    by_contra h
    have hz : repairBumpTail c 0 0 r = 0 := le_antisymm (le_of_not_gt h) hT0
    rw [hz, mul_zero] at hprod
    exact (lt_irrefl 0) hprod
  have hc0 : localFirstRepairCoefficient F eta < 0 := by
    by_contra h
    have hn := mul_nonneg (le_of_not_gt h) hT0
    linarith
  exact ⟨hT0_pos, hc0⟩

theorem firstBump_angularTail_lower (c : Parameters) (r : ℝ)
    (hr : c.lower 0 < r) (hr_upper : r < c.upper 0) :
    c.upper 0 ^ (-c.lam) * repairBumpTail c 0 0 r ≤ repairBumpTail c 1 0 r := by
  have hr_pos := (c.lower_pos 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have h0 := (weighted_bump_intervalIntegrable c 0 0 r hr_pos hr_end).const_mul
    (c.upper 0 ^ (-c.lam))
  have h1 := weighted_bump_intervalIntegrable c 1 0 r hr_pos hr_end
  unfold repairBumpTail
  rw [← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_mono_on hr_end h0 h1
  intro x hx
  have hx_pos := hr_pos.trans_le hx.1
  by_cases hb : NavierStokes.LocalizedMomentRepair.bump (c.lower 0) (c.upper 0) x = 0
  · simp [hb]
  · have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
      (c.lower 0) (c.upper 0) (c.lower_lt_upper 0)) (subset_tsupport _ hb)
    have hw := Real.rpow_le_rpow_of_nonpos hx_pos hs.2.le (neg_nonpos.mpr c.lam_pos.le)
    have hbase : 0 ≤ x ^ c.exponents 0 *
        NavierStokes.LocalizedMomentRepair.bump (c.lower 0) (c.upper 0) x :=
      mul_nonneg (Real.rpow_nonneg hx_pos.le (c.exponents 0))
        (NavierStokes.LocalizedMomentRepair.bump_nonneg (c.lower 0) (c.upper 0) x)
    have hm :
        (x ^ c.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump (c.lower 0) (c.upper 0) x) *
            (c.upper 0 ^ (-c.lam)) ≤
          (x ^ c.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump (c.lower 0) (c.upper 0) x) *
            (x ^ (-c.lam)) :=
      mul_le_mul_of_nonneg_left hw hbase
    rw [secondExponent_eq_first_sub_lam, Real.rpow_add hx_pos]
    simpa [mul_assoc, mul_left_comm, mul_comm] using hm

theorem secondBump_angularTail_upper (c : Parameters) (r : ℝ)
    (hr : c.lower 0 < r) (hr_upper : r < c.upper 0) :
    repairBumpTail c 1 1 r ≤ c.lower 1 ^ (-c.lam) * repairBumpTail c 0 1 r := by
  have hr_pos := (c.lower_pos 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have h1 := weighted_bump_intervalIntegrable c 1 1 r hr_pos hr_end
  have h0 := (weighted_bump_intervalIntegrable c 0 1 r hr_pos hr_end).const_mul
    (c.lower 1 ^ (-c.lam))
  unfold repairBumpTail
  rw [← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_mono_on hr_end h1 h0
  intro x hx
  have hx_pos := hr_pos.trans_le hx.1
  by_cases hb : NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x = 0
  · simp [hb]
  · have hs := (NavierStokes.LocalizedMomentRepair.bump_tsupport_subset_open
      (c.lower 1) (c.upper 1) (c.lower_lt_upper 1)) (subset_tsupport _ hb)
    have hw := Real.rpow_le_rpow_of_nonpos (c.lower_pos 1) hs.1.le
      (neg_nonpos.mpr c.lam_pos.le)
    have hbase : 0 ≤ x ^ c.exponents 0 *
        NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x :=
      mul_nonneg (Real.rpow_nonneg hx_pos.le (c.exponents 0))
        (NavierStokes.LocalizedMomentRepair.bump_nonneg (c.lower 1) (c.upper 1) x)
    have hm :
        (x ^ c.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x) *
            (x ^ (-c.lam)) ≤
          (x ^ c.exponents 0 *
            NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x) *
            (c.lower 1 ^ (-c.lam)) :=
      mul_le_mul_of_nonneg_left hw hbase
    rw [secondExponent_eq_first_sub_lam, Real.rpow_add hx_pos]
    simpa [mul_assoc, mul_left_comm, mul_comm] using hm

theorem angularMoment_pos_of_firstRepair_mass_zero (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < localAngularMoment F eta r := by
  let c := F.data.core
  have hr_one := (c.one_lt_lower 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have hc0 := (firstBumpTail_pos_and_firstCoeff_neg F eta r hr hr_upper hM hc1).2
  have hT1 := secondBump_massTail_pos c r hr_upper
  have hbalance := firstRepair_mass_zero_tail_balance F eta r hr hr_upper hM
  have hS0 := firstBump_angularTail_lower c r hr hr_upper
  have hS1 := secondBump_angularTail_upper c r hr hr_upper
  have hweights : c.lower 1 ^ (-c.lam) < c.upper 0 ^ (-c.lam) :=
    Real.rpow_lt_rpow_of_neg ((c.lower_pos 0).trans (c.lower_lt_upper 0))
      (first_upper_lt_second_lower c) (neg_neg_of_pos c.lam_pos)
  have hsum : localFirstRepairCoefficient F eta * repairBumpTail c 1 0 r +
      localSecondRepairCoefficient F eta * repairBumpTail c 1 1 r < 0 := by
    calc
      _ ≤ localFirstRepairCoefficient F eta *
            (c.upper 0 ^ (-c.lam) * repairBumpTail c 0 0 r) +
          localSecondRepairCoefficient F eta *
            (c.lower 1 ^ (-c.lam) * repairBumpTail c 0 1 r) :=
        add_le_add (mul_le_mul_of_nonpos_left hS0 hc0.le)
          (mul_le_mul_of_nonneg_left hS1 hc1.le)
      _ = (localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) *
          (c.lower 1 ^ (-c.lam) - c.upper 0 ^ (-c.lam)) := by
        have heq : localFirstRepairCoefficient F eta * repairBumpTail c 0 0 r =
            -(localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) := by
          linarith [hbalance]
        calc
          _ = c.upper 0 ^ (-c.lam) *
                (localFirstRepairCoefficient F eta * repairBumpTail c 0 0 r) +
              c.lower 1 ^ (-c.lam) *
                (localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) := by ring
          _ = _ := by rw [heq]; ring
      _ < 0 := mul_neg_of_pos_of_neg (mul_pos hc1 hT1) (sub_neg.mpr hweights)
  rw [localAngularMoment_tail_identity F eta r hr_one.le hr_end,
    weighted_future_integral_eq_two_tails F eta r hr hr_upper 1]
  exact mul_pos_of_neg_of_neg
    (neg_neg_of_pos (mul_pos (momentScale_pos c 1) (sq_pos_of_pos (shape_pos eta)))) hsum

#print axioms NSRW.P2.localAngularMoment_partial_identity
#print axioms NSRW.P2.localAngularMoment_tail_identity
#print axioms NSRW.P2.first_upper_lt_second_lower
#print axioms NSRW.P2.secondExponent_eq_first_sub_lam
#print axioms NSRW.P2.future_radialPulse_eq_two_bumps
#print axioms NSRW.P2.weighted_future_integral_eq_two_tails
#print axioms NSRW.P2.secondBump_massTail_pos
#print axioms NSRW.P2.firstRepair_mass_zero_tail_balance
#print axioms NSRW.P2.firstBumpTail_pos_and_firstCoeff_neg
#print axioms NSRW.P2.firstBump_angularTail_lower
#print axioms NSRW.P2.secondBump_angularTail_upper
#print axioms NSRW.P2.angularMoment_pos_of_firstRepair_mass_zero

end NSRW.P2
