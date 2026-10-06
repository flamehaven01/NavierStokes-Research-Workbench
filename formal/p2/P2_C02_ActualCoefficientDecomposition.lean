import NavierStokes.OutgoingProfile

/-!
# P2 C-02: actual repair coefficient decomposition

The generic identity below restates the pinned source's `debt_eq_affine` and
`affineCoefficients_decomposition`. The second identity specializes it to the
second axial repair coefficient of one fixed Profile, using that Profile's
core and corrected amplitude. These axial repair coefficients are not the
angular-reset coefficients stored in `F.reset`.

This module establishes only equalities. It does not prove positivity at zero,
a small-positive-eta sign, a mass-history zero, or uniformity over Profiles.
It does not require a numerical instance of the existential source Profile.
-/

open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds
open NavierStokes.OutgoingProfile

namespace NSRW.P2

theorem actualRepairCoefficient_decomposition
    (c : Parameters) (amp : ℝ → ℝ) (eta : ℝ) (j : Fin 2) :
    NavierStokes.LocalizedMomentRepair.coefficients c.exponents c.lower c.upper
        (debt c amp eta) j =
      parameterPolynomial eta * affineCoefficients c 1 0 j +
        amp eta * affineCoefficients c 0 1 j := by
  rw [debt_eq_affine]
  exact affineCoefficients_decomposition c _ _ j

theorem profile_secondRepairCoefficient_decomposition (F : Profile) (eta : ℝ) :
    NavierStokes.LocalizedMomentRepair.coefficients
        F.data.core.exponents F.data.core.lower F.data.core.upper
        (debt F.data.core F.amp eta) (1 : Fin 2) =
      (eta * (1 + eta ^ 2)) * affineCoefficients F.data.core 1 0 1 +
        NavierStokes.CorrectedPulseAmplitude.amplitude
          F.data F.reset.coefficients eta * affineCoefficients F.data.core 0 1 1 := by
  simpa only [parameterPolynomial, Profile.amp] using
    actualRepairCoefficient_decomposition F.data.core F.amp eta (1 : Fin 2)

#print axioms NSRW.P2.actualRepairCoefficient_decomposition
#print axioms NSRW.P2.profile_secondRepairCoefficient_decomposition

end NSRW.P2
