import P2_C_MainOnlyCoefficient
import P2_C02_ActualCoefficientDecomposition

/-!
# P2 C-03: the actual second axial repair coefficient at zero

For one fixed source Profile, the prefix term vanishes at eta = 0.
The corrected amplitude is positive and the compiled C01 main-only
coefficient is positive. Their product is the actual axial coefficient.
Its continuity follows from the exact C02 decomposition and Profile.amp_contDiff.

These statements do not supply a numerical Profile, a uniform epsilon,
a small-positive-eta sign theorem, or a mass-history zero. The angular-reset
coefficients in F.reset remain distinct from the axial coefficient below.
-/

open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds
open NavierStokes.OutgoingProfile

namespace NSRW.P2

noncomputable def actualSecondRepairCoefficient (F : Profile) (eta : ℝ) : ℝ :=
  NavierStokes.LocalizedMomentRepair.coefficients
    F.data.core.exponents F.data.core.lower F.data.core.upper
    (debt F.data.core F.amp eta) (1 : Fin 2)

theorem actualSecondRepairCoefficient_zero_eq (F : Profile) :
    actualSecondRepairCoefficient F 0 =
      F.amp 0 * affineCoefficients F.data.core 0 1 1 := by
  simpa only [actualSecondRepairCoefficient, zero_pow (by norm_num : (2 : ℕ) ≠ 0),
    zero_mul, zero_add, Profile.amp] using
    profile_secondRepairCoefficient_decomposition F 0

theorem actualSecondRepairCoefficient_zero_pos (F : Profile) :
    0 < actualSecondRepairCoefficient F 0 := by
  rw [actualSecondRepairCoefficient_zero_eq]
  exact mul_pos
    (NavierStokes.CorrectedPulseAmplitude.amplitude_pos F.data F.reset.coefficients 0)
    (affineCoefficients_main_one_pos F.data.core)

theorem actualSecondRepairCoefficient_continuous (F : Profile) :
    Continuous (actualSecondRepairCoefficient F) := by
  have heq : actualSecondRepairCoefficient F = fun eta =>
      (eta * (1 + eta ^ 2)) * affineCoefficients F.data.core 1 0 1 +
        F.amp eta * affineCoefficients F.data.core 0 1 1 := by
    funext eta
    simpa only [actualSecondRepairCoefficient, Profile.amp] using
      profile_secondRepairCoefficient_decomposition F eta
  rw [heq]
  exact ((continuous_id.mul (continuous_const.add (continuous_id.pow 2))).mul
    continuous_const).add (F.amp_contDiff.continuous.mul continuous_const)

#print axioms NSRW.P2.actualSecondRepairCoefficient_zero_eq
#print axioms NSRW.P2.actualSecondRepairCoefficient_zero_pos
#print axioms NSRW.P2.actualSecondRepairCoefficient_continuous

end NSRW.P2
