import P2_F1_MainMomentPositivity

/-!
# P2 L2: normalized main-moment comparison

This module begins the L2 chain.  It binds the normalized main moments to the
same short log-coordinate integral used by the pinned source, and carries the
already compiled F1 positivity into the normalized `i = 1` quantity.

It does not prove the strict `i = 0` versus `i = 1` comparison, `DeltaM < 0`,
or any repair-window zero statement.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

noncomputable def normalizedMainMoment (c : Parameters) (i : Fin 2) : ℝ :=
  Real.exp (-(beta c i * center c 0)) * mainMoment c i

theorem normalizedMainMoment_log_short (c : Parameters) (i : Fin 2) :
    normalizedMainMoment c i =
      ∫ y in (0 : ℝ)..11 / c.lam,
        Real.exp (beta c i * (y - center c 0)) * mainPulse (c.lam * y) := by
  unfold normalizedMainMoment
  rw [mainMoment_log_short, ← intervalIntegral.integral_const_mul]
  apply intervalIntegral.integral_congr
  intro y _
  rw [show beta c i * (y - center c 0) =
    -(beta c i * center c 0) + beta c i * y by ring, Real.exp_add]
  ring

theorem normalizedMainMoment_one_pos (c : Parameters) :
    0 < normalizedMainMoment c (1 : Fin 2) := by
  unfold normalizedMainMoment
  exact mul_pos (Real.exp_pos _) (mainMoment_one_pos c)

#print axioms NSRW.P2.normalizedMainMoment_log_short
#print axioms NSRW.P2.normalizedMainMoment_one_pos

end NSRW.P2
