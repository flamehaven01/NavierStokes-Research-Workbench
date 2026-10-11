import NavierStokes.OutgoingProfile

/-!
# P2 Z-01D: partial mass and tail identities

The two named propositions concern the exact source `massMoment`, evaluated at
`pulseStart + log r`, for the amplitude of one fixed source Profile. The positive
`momentScale * shape` is an integral prefactor, not a conversion factor between
`massMoment` and `Profile.M`.

No boundary sign, bump-integral positivity, IVT, or mass-zero existence is
proved here. Development compilation is separate from receipt admission.
-/

open Set MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingProfile

namespace NSRW.P2

theorem localMass_partial_identity (F : Profile) (eta r : ℝ)
    (hr : 1 ≤ r) (_hr_end : r ≤ Real.exp F.data.core.pulseLength) :
    massMoment F.data.core F.amp eta (F.data.core.pulseStart + Real.log r) =
      prefixM F.data.core * eta +
        (momentScale F.data.core 0 * shape eta) *
          (∫ x in (1 : ℝ)..r,
            x ^ F.data.core.exponents 0 * radialPulse F.data.core F.amp eta x) := by
  let c := F.data.core
  have hr_pos : 0 < r := lt_of_lt_of_le zero_lt_one hr
  have hlog : 0 ≤ Real.log r := Real.log_nonneg hr
  have hF : Continuous (fun t => Real.exp t * axial c F.amp (t, eta)) :=
    Real.continuous_exp.mul (axial_radial_contDiff c F.amp eta).continuous
  have hsplit := intervalIntegral.integral_add_adjacent_intervals (μ := volume)
    (hF.intervalIntegrable 0 c.pulseStart)
    (hF.intervalIntegrable c.pulseStart (c.pulseStart + Real.log r))
  have hI : (∫ t in c.pulseStart..c.pulseStart + Real.log r,
      Real.exp t * axial c F.amp (t, eta)) =
      (momentScale c 0 * shape eta) *
        (∫ x in (1 : ℝ)..r, x ^ c.exponents 0 * radialPulse c F.amp eta x) := by
    calc
      _ = ∫ t in c.pulseStart..c.pulseStart + Real.log r,
          (momentScale c 0 * shape eta) *
            (Real.exp ((c.exponents 0 + 1) * (t - c.pulseStart)) *
              radialPulse c F.amp eta (Real.exp (t - c.pulseStart))) := by
        apply intervalIntegral.integral_congr
        intro t ht
        apply mass_integrand_pulse c F.amp eta
        exact (uIcc_of_le (show c.pulseStart ≤ c.pulseStart + Real.log r by
          linarith) ▸ ht).1
      _ = _ := by
        rw [intervalIntegral.integral_const_mul]
        rw [exp_weight_substitution (radialPulse_continuousOn c F.amp eta)
          (c.exponents 0) c.pulseStart (Real.log r)]
        rw [Real.exp_log hr_pos]
  change massMoment c F.amp eta (c.pulseStart + Real.log r) = _
  calc
    _ = massMoment c F.amp eta c.pulseStart +
        (∫ t in c.pulseStart..c.pulseStart + Real.log r,
          Real.exp t * axial c F.amp (t, eta)) := by
      unfold massMoment
      rw [← hsplit]
      ring
    _ = _ := by rw [massMoment_at_pulseStart, hI]

theorem localMass_tail_identity (F : Profile) (eta r : ℝ)
    (hr : 1 ≤ r) (hr_end : r ≤ Real.exp F.data.core.pulseLength) :
    massMoment F.data.core F.amp eta (F.data.core.pulseStart + Real.log r) =
      -(momentScale F.data.core 0 * shape eta) *
        (∫ x in r..Real.exp F.data.core.pulseLength,
          x ^ F.data.core.exponents 0 * radialPulse F.data.core F.amp eta x) := by
  let c := F.data.core
  let g : ℝ → ℝ := fun x => x ^ c.exponents 0 * radialPulse c F.amp eta x
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
  have hcancel := (pulse_closes_prefix c F.amp eta).1
  rw [localMass_partial_identity F eta r hr hr_end]
  change prefixM c * eta + (momentScale c 0 * shape eta) * (∫ x in 1..r, g x) =
    -(momentScale c 0 * shape eta) * (∫ x in r..Real.exp c.pulseLength, g x)
  change prefixM c * eta + (momentScale c 0 * shape eta) *
    (∫ x in (1 : ℝ)..Real.exp c.pulseLength, g x) = 0 at hcancel
  rw [← hsplit] at hcancel
  nlinarith [hcancel]

#print axioms NSRW.P2.localMass_partial_identity
#print axioms NSRW.P2.localMass_tail_identity

end NSRW.P2
