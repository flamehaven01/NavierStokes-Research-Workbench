import NavierStokes.PulseAmplitude

/-!
# P2 L1: main-pulse positivity surface

External module: compile from the pinned NavierStokesAndEuler source root.
This module is intentionally narrow. It records two source-bound facts needed
before any separate weighted-integral positivity proof can be attempted.
-/

namespace NSRW.P2

theorem mainPulse_nonnegative {z : ℝ} (hz : 0 ≤ z) :
    0 ≤ NavierStokes.OutgoingSchedule.mainPulse z :=
  NavierStokes.PulseAmplitude.mainPulse_nonneg hz

theorem mainPulse_positive_at_one_twenty_fifth :
    0 < NavierStokes.OutgoingSchedule.mainPulse (1 / 25 : ℝ) := by
  have h := NavierStokes.PulseAmplitude.mainPulse_lower
    (z := (1 / 25 : ℝ)) (by norm_num) (by norm_num)
  norm_num at h ⊢
  linarith

#print axioms NSRW.P2.mainPulse_nonnegative
#print axioms NSRW.P2.mainPulse_positive_at_one_twenty_fifth

end NSRW.P2
