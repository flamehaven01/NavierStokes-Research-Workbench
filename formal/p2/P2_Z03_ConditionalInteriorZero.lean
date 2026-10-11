import P2_Z02_BoundaryMassSigns

/-!
# P2 Z-03: conditional first-repair interior mass zero

Continuity uses the original source mass primitive for a fixed Profile and eta.
The IVT consumes Z02's boundary signs with explicit eta and actual second axial
coefficient positivity hypotheses. Endpoint exclusion gives an open interval.

C04 is not imported. No existential epsilon, Profile.M coordinate conversion,
uniqueness, first-zero claim, J behavior, or claim admission is supplied here.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

theorem massMoment_continuous (F : Profile) (eta : ℝ) :
    Continuous (fun y => massMoment F.data.core F.amp eta y) := by
  have hg : Continuous (fun t => Real.exp t * axial F.data.core F.amp (t, eta)) :=
    Real.continuous_exp.mul (axial_radial_contDiff F.data.core F.amp eta).continuous
  have hp : Continuous (fun y => ∫ t in (0 : ℝ)..y,
      Real.exp t * axial F.data.core F.amp (t, eta)) :=
    intervalIntegral.continuous_primitive (fun a b => hg.intervalIntegrable a b) 0
  exact continuous_const.add hp

theorem localMass_continuousOn_firstRepair (F : Profile) (eta : ℝ) :
    ContinuousOn (localMass F eta)
      (Icc (F.data.core.lower 0) (F.data.core.upper 0)) := by
  have hlog : ContinuousOn Real.log
      (Icc (F.data.core.lower 0) (F.data.core.upper 0)) :=
    continuousOn_id.log (fun r hr => ne_of_gt
      (lt_trans zero_lt_one (lt_of_lt_of_le (F.data.core.one_lt_lower 0) hr.1)))
  exact (massMoment_continuous F eta).comp_continuousOn
    (continuousOn_const.add hlog)

theorem exists_firstRepair_zero_of_secondCoeff_pos (F : Profile) (eta : ℝ)
    (heta : 0 < eta) (hc1 : 0 < localSecondRepairCoefficient F eta) :
    ∃ r : ℝ, F.data.core.lower 0 < r ∧ r < F.data.core.upper 0 ∧
      localMass F eta r = 0 := by
  have hl := localMass_lower_pos F eta heta
  have hu := localMass_upper_neg_of_secondCoeff_pos F eta hc1
  obtain ⟨r, hr, hzero⟩ := intermediate_value_Icc'
    (F.data.core.lower_lt_upper 0).le (localMass_continuousOn_firstRepair F eta)
    (show (0 : ℝ) ∈ Icc (localMass F eta (F.data.core.upper 0))
      (localMass F eta (F.data.core.lower 0)) from ⟨hu.le, hl.le⟩)
  have hne_lower : r ≠ F.data.core.lower 0 := by
    intro heq
    have hz := hzero
    rw [heq] at hz
    exact (ne_of_gt hl) hz
  have hne_upper : r ≠ F.data.core.upper 0 := by
    intro heq
    have hz := hzero
    rw [heq] at hz
    exact (ne_of_lt hu) hz
  exact ⟨r, lt_of_le_of_ne hr.1 (Ne.symm hne_lower),
    lt_of_le_of_ne hr.2 hne_upper, hzero⟩

#print axioms NSRW.P2.massMoment_continuous
#print axioms NSRW.P2.localMass_continuousOn_firstRepair
#print axioms NSRW.P2.exists_firstRepair_zero_of_secondCoeff_pos

end NSRW.P2
