import P2_C04_SmallPositiveEta
import P2_Z03_ConditionalInteriorZero

/-!
# P2 Z04-core: source-facing first-repair interior mass zero

The coefficient branch supplies a Profile-dependent positive neighborhood.
The geometry branch supplies a conditional interior local mass zero.
Their composition is transported to the same source Profile.M object.

Development target only: no J/Q, uniform or numerical epsilon, uniqueness,
first-zero claim, authority replay, or claim admission is supplied here.
-/

open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

theorem localSecondRepairCoefficient_eq_actual (F : Profile) (eta : ℝ) :
    localSecondRepairCoefficient F eta = actualSecondRepairCoefficient F eta := by
  rfl

theorem exists_firstRepair_zero_small_positive (F : Profile) :
    ∃ epsilon : ℝ, 0 < epsilon ∧
      ∀ eta : ℝ, 0 < eta → eta < epsilon →
        ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
          localMass F eta r = 0 := by
  obtain ⟨epsilon, hepsilon, hcoeff⟩ := actualSecondRepairCoefficient_pos_small_positive F
  refine ⟨epsilon, hepsilon, ?_⟩
  intro eta heta hsmall
  apply exists_firstRepair_zero_of_secondCoeff_pos F eta heta
  rw [localSecondRepairCoefficient_eq_actual]
  exact hcoeff eta heta hsmall

theorem localMass_eq_profileM (F : Profile) (eta r : ℝ) (hr : 1 ≤ r) :
    localMass F eta r = F.M eta (Real.exp F.data.core.pulseStart * r) := by
  have hrpos : 0 < r := lt_of_lt_of_le zero_lt_one hr
  have hy : 0 ≤ F.data.core.pulseStart + Real.log r :=
    add_nonneg F.data.core.pulseStart_pos.le (Real.log_nonneg hr)
  have hmass := F.M_at_exp eta hy
  rw [Real.exp_add, Real.exp_log hrpos] at hmass
  exact hmass.symm

theorem profileM_firstRepair_zero_small_positive (F : Profile) :
    ∃ epsilon : ℝ, 0 < epsilon ∧
      ∀ eta : ℝ, 0 < eta → eta < epsilon →
        ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
          F.M eta (Real.exp F.data.core.pulseStart * r) = 0 := by
  obtain ⟨epsilon, hepsilon, hzero⟩ := exists_firstRepair_zero_small_positive F
  refine ⟨epsilon, hepsilon, ?_⟩
  intro eta heta hsmall
  obtain ⟨r, hlower, hupper, hmass⟩ := hzero eta heta hsmall
  have hr : 1 ≤ r := (lt_trans (F.data.core.one_lt_lower 0) hlower).le
  refine ⟨r, hlower, hupper, ?_⟩
  rw [← localMass_eq_profileM F eta r hr]
  exact hmass

#print axioms NSRW.P2.localSecondRepairCoefficient_eq_actual
#print axioms NSRW.P2.exists_firstRepair_zero_small_positive
#print axioms NSRW.P2.localMass_eq_profileM
#print axioms NSRW.P2.profileM_firstRepair_zero_small_positive

end NSRW.P2
