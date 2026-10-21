import P2_ZPLUS_J_FirstRepairAngularMoment

/-!
# P2 Z+J: a quantitative lower bound at every admissible mass zero

For the same fixed source Profile, eta and first-window radius, exact mass
cancellation and a positive second AXIAL repair coefficient give a positive
angular-history lower bound independent of the chosen zero's location.

The full second-bump moment is I01, and the weight gap is
upper(0)^(-lam) - lower(1)^(-lam). Neither eta > 0 nor an amplitude bound,
C04 epsilon, numerical Profile, uniqueness or pole assertion is used here.

This is a development implementation. Compilation, commit-bound execution and
claim admission are separate events. The imported historical proofs are not
modified; no additional axiom or admitted proof is introduced.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

/-- The entire second bump lies to the right of any first-window radius. -/
theorem secondBump_massTail_eq_full (c : Parameters) (r : ℝ) (hr : r < c.upper 0) :
    repairBumpTail c 0 1 r =
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

/-- Strict support separation and the decreasing positive-base weight give a gap. -/
theorem firstRepair_weightGap_pos (c : Parameters) :
    0 < c.upper 0 ^ (-c.lam) - c.lower 1 ^ (-c.lam) := by
  apply sub_pos.mpr
  exact Real.rpow_lt_rpow_of_neg ((c.lower_pos 0).trans (c.lower_lt_upper 0))
    (first_upper_lt_second_lower c) (neg_neg_of_pos c.lam_pos)

/-- A root-location-independent lower bound; the mass zero and c1 are actual
source objects for the same F and eta. The full second-bump integral is I01. -/
theorem angularMoment_ge_firstRepair_margin (F : Profile) (eta r : ℝ)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    (momentScale F.data.core 1 * shape eta ^ 2) *
        localSecondRepairCoefficient F eta *
        (∫ x : ℝ, x ^ F.data.core.exponents 0 *
          NavierStokes.LocalizedMomentRepair.bump
            (F.data.core.lower 1) (F.data.core.upper 1) x) *
        (F.data.core.upper 0 ^ (-F.data.core.lam) -
          F.data.core.lower 1 ^ (-F.data.core.lam)) ≤
      localAngularMoment F eta r := by
  let c := F.data.core
  have hr_one := (c.one_lt_lower 0).trans hr
  have hr_end := (hr_upper.trans (c.upper_lt_end 0)).le
  have hc0 := (firstBumpTail_pos_and_firstCoeff_neg F eta r hr hr_upper hM hc1).2
  have hbalance := firstRepair_mass_zero_tail_balance F eta r hr hr_upper hM
  have hS0 := firstBump_angularTail_lower c r hr hr_upper
  have hS1 := secondBump_angularTail_upper c r hr hr_upper
  have hsum : localFirstRepairCoefficient F eta * repairBumpTail c 1 0 r +
      localSecondRepairCoefficient F eta * repairBumpTail c 1 1 r ≤
        (localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) *
          (c.lower 1 ^ (-c.lam) - c.upper 0 ^ (-c.lam)) := by
    calc
      _ ≤ localFirstRepairCoefficient F eta *
            (c.upper 0 ^ (-c.lam) * repairBumpTail c 0 0 r) +
          localSecondRepairCoefficient F eta *
            (c.lower 1 ^ (-c.lam) * repairBumpTail c 0 1 r) :=
        add_le_add (mul_le_mul_of_nonpos_left hS0 hc0.le)
          (mul_le_mul_of_nonneg_left hS1 hc1.le)
      _ = _ := by
        have heq : localFirstRepairCoefficient F eta * repairBumpTail c 0 0 r =
            -(localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) := by
          linarith [hbalance]
        calc
          _ = c.upper 0 ^ (-c.lam) *
                (localFirstRepairCoefficient F eta * repairBumpTail c 0 0 r) +
              c.lower 1 ^ (-c.lam) *
                (localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) := by ring
          _ = _ := by rw [heq]; ring
  have hK : 0 < momentScale c 1 * shape eta ^ 2 :=
    mul_pos (momentScale_pos c 1) (sq_pos_of_pos (shape_pos eta))
  have hscaled := mul_le_mul_of_nonpos_left hsum (neg_nonpos.mpr hK.le)
  rw [localAngularMoment_tail_identity F eta r hr_one.le hr_end,
    weighted_future_integral_eq_two_tails F eta r hr hr_upper 1]
  calc
    _ = -(momentScale c 1 * shape eta ^ 2) *
          ((localSecondRepairCoefficient F eta * repairBumpTail c 0 1 r) *
            (c.lower 1 ^ (-c.lam) - c.upper 0 ^ (-c.lam))) := by
      rw [secondBump_massTail_eq_full c r hr_upper]
      ring
    _ ≤ _ := hscaled

/-- The margin is positive once the actual second axial coefficient is positive;
this factor-positivity statement does not require choosing a mass zero. -/
theorem firstRepair_margin_pos (F : Profile) (eta : ℝ)
    (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < (momentScale F.data.core 1 * shape eta ^ 2) *
      localSecondRepairCoefficient F eta *
      (∫ x : ℝ, x ^ F.data.core.exponents 0 *
        NavierStokes.LocalizedMomentRepair.bump
          (F.data.core.lower 1) (F.data.core.upper 1) x) *
      (F.data.core.upper 0 ^ (-F.data.core.lam) -
        F.data.core.lower 1 ^ (-F.data.core.lam)) := by
  have hK : 0 < momentScale F.data.core 1 * shape eta ^ 2 :=
    mul_pos (momentScale_pos F.data.core 1) (sq_pos_of_pos (shape_pos eta))
  exact mul_pos (mul_pos (mul_pos hK hc1) (secondBumpWeightedMoment_pos F.data.core))
    (firstRepair_weightGap_pos F.data.core)

#check NSRW.P2.secondBump_massTail_eq_full
#check NSRW.P2.firstRepair_weightGap_pos
#check NSRW.P2.angularMoment_ge_firstRepair_margin
#check NSRW.P2.firstRepair_margin_pos

#print axioms NSRW.P2.secondBump_massTail_eq_full
#print axioms NSRW.P2.firstRepair_weightGap_pos
#print axioms NSRW.P2.angularMoment_ge_firstRepair_margin
#print axioms NSRW.P2.firstRepair_margin_pos

end NSRW.P2
