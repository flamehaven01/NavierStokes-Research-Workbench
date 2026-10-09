import P2_C03_ActualCoefficientAtZero

/-!
# P2 C-04: a positive neighborhood for each fixed source Profile

C03 supplies positivity at zero and continuity of the actual second axial
repair coefficient. The positive preimage is open and contains zero, so it
contains a ball of positive radius. Restrict that ball to positive eta.

The radius may depend on F. This theorem does not supply a numerical radius,
a uniform radius over Profiles, positivity for every positive eta, or a
mass-history zero. Compilation and commit-bound receipt admission are separate.
-/

open NavierStokes.OutgoingProfile
open scoped Topology

namespace NSRW.P2

theorem actualSecondRepairCoefficient_pos_small_positive (F : Profile) :
    ∃ epsilon : ℝ, 0 < epsilon ∧
      ∀ eta : ℝ, 0 < eta → eta < epsilon →
        0 < actualSecondRepairCoefficient F eta := by
  have hopen : IsOpen {eta : ℝ | 0 < actualSecondRepairCoefficient F eta} :=
    isOpen_lt continuous_const (actualSecondRepairCoefficient_continuous F)
  have hnhds : {eta : ℝ | 0 < actualSecondRepairCoefficient F eta} ∈ 𝓝 (0 : ℝ) :=
    hopen.mem_nhds (actualSecondRepairCoefficient_zero_pos F)
  obtain ⟨epsilon, hepsilon, hball⟩ := Metric.mem_nhds_iff.mp hnhds
  refine ⟨epsilon, hepsilon, ?_⟩
  intro eta heta hlt
  apply hball
  simpa only [Metric.mem_ball, Real.dist_eq, sub_zero, abs_of_pos heta] using hlt

#print axioms NSRW.P2.actualSecondRepairCoefficient_pos_small_positive

end NSRW.P2
