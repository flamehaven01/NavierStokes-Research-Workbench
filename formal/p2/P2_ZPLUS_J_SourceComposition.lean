import P2_Z04_FirstRepairInteriorZero
import P2_ZPLUS_J_FirstRepairAngularMoment

/-!
# P2 Z+J: source-facing mass/angular mismatch at one common point

The same C04 positive radius supplies the coefficient hypothesis for both
conditional geometry branches. The witness, Profile, eta and physical radius
are shared; separate existential witnesses are not combined.

Development only. No uniform/numerical epsilon, uniqueness, simple zero,
Q pole/limit, literature novelty or claim admission is asserted.
-/

open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

theorem localAngularMoment_eq_profileJ (F : Profile) (eta r : ℝ) (hr : 1 ≤ r) :
    localAngularMoment F eta r = F.J eta (Real.exp F.data.core.pulseStart * r) := by
  have hrpos : 0 < r := lt_of_lt_of_le zero_lt_one hr
  have hy : 0 ≤ F.data.core.pulseStart + Real.log r :=
    add_nonneg F.data.core.pulseStart_pos.le (Real.log_nonneg hr)
  have hangular := F.J_at_exp eta hy
  rw [Real.exp_add, Real.exp_log hrpos] at hangular
  exact hangular.symm

theorem profileJ_pos_of_firstRepair_mass_zero (F : Profile) (eta r : ℝ)
    (hr_lower : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : F.M eta (Real.exp F.data.core.pulseStart * r) = 0)
    (hc1 : 0 < actualSecondRepairCoefficient F eta) :
    0 < F.J eta (Real.exp F.data.core.pulseStart * r) := by
  have hr : 1 ≤ r := (lt_trans (F.data.core.one_lt_lower 0) hr_lower).le
  have hlocalM : localMass F eta r = 0 := by
    rw [localMass_eq_profileM F eta r hr]
    exact hM
  have hlocalC : 0 < localSecondRepairCoefficient F eta := by
    rw [localSecondRepairCoefficient_eq_actual]
    exact hc1
  rw [← localAngularMoment_eq_profileJ F eta r hr]
  exact angularMoment_pos_of_firstRepair_mass_zero F eta r hr_lower hr_upper hlocalM hlocalC

theorem profileMJ_firstRepair_zero_small_positive (F : Profile) :
    ∃ epsilon : ℝ, 0 < epsilon ∧
      ∀ eta : ℝ, 0 < eta → eta < epsilon →
        ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
          F.M eta (Real.exp F.data.core.pulseStart * r) = 0 ∧
          0 < F.J eta (Real.exp F.data.core.pulseStart * r) := by
  obtain ⟨epsilon, hepsilon, hcoeff⟩ := actualSecondRepairCoefficient_pos_small_positive F
  refine ⟨epsilon, hepsilon, ?_⟩
  intro eta heta hsmall
  have hc1 : 0 < actualSecondRepairCoefficient F eta := hcoeff eta heta hsmall
  have hlocalC : 0 < localSecondRepairCoefficient F eta := by
    rw [localSecondRepairCoefficient_eq_actual]
    exact hc1
  obtain ⟨r, hlower, hupper, hmass⟩ :=
    exists_firstRepair_zero_of_secondCoeff_pos F eta heta hlocalC
  have hr : 1 ≤ r := (lt_trans (F.data.core.one_lt_lower 0) hlower).le
  have hprofileM : F.M eta (Real.exp F.data.core.pulseStart * r) = 0 := by
    rw [← localMass_eq_profileM F eta r hr]
    exact hmass
  exact ⟨r, hlower, hupper, hprofileM,
    profileJ_pos_of_firstRepair_mass_zero F eta r hlower hupper hprofileM hc1⟩

#print axioms NSRW.P2.localAngularMoment_eq_profileJ
#print axioms NSRW.P2.profileJ_pos_of_firstRepair_mass_zero
#print axioms NSRW.P2.profileMJ_firstRepair_zero_small_positive

end NSRW.P2
