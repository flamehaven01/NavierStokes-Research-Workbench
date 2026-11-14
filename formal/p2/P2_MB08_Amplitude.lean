import NavierStokes.CorrectedPulseAmplitude
import Mathlib.Analysis.Complex.ExponentialBounds

/-! The fixed-input obstruction and a sufficient sign test for the actual amplitude. -/

open NavierStokes.OutgoingTail NavierStokes.AngularMomentReset
open NavierStokes.CorrectedPulseAmplitude
open NavierStokes

namespace NSRW.P2

theorem mb_combinedScale_gt_prefix_lower (d : TailData) (K : ℝ)
    (hP : d.core.P = 1) (hm : d.core.m = 1) (hK : 0 < K) :
    30 * (2 : ℝ) ^ (120 : ℕ) * d.core.lam < combinedScale d K := by
  have hexp : (2 : ℝ) ^ (120 : ℕ) < Real.exp 120 := by
    have hp := pow_lt_pow_left₀ Real.exp_one_gt_two (by norm_num : (0 : ℝ) ≤ 2)
      (by decide : (120 : ℕ) ≠ 0)
    rw [← Real.exp_nat_mul, mul_one] at hp
    simpa only [Nat.cast_ofNat] using hp
  have hprefix : 30 * (2 : ℝ) ^ (120 : ℕ) < PulseAmplitude.prefixBoundConstant 1 1 := by
    unfold PulseAmplitude.prefixBoundConstant
    have hweight : Real.exp 120 < Real.exp ((Real.exp 1 + 12) / 5 + 120) :=
      Real.exp_lt_exp.mpr (by linarith [Real.exp_pos (1 : ℝ)])
    have hsum : (30 : ℝ) < 16 * Real.exp (Real.exp 1) / 1 ^ (2 : ℕ) +
        5 / 12 + (Real.exp 1 + 12) / 2 + 30 := by
      have h := Real.exp_pos (Real.exp 1)
      have h' := Real.exp_pos (1 : ℝ)
      norm_num
      linarith
    have h30 : (0 : ℝ) < 30 := by norm_num
    calc
      _ < Real.exp ((Real.exp 1 + 12) / 5 + 120) * 30 :=
        by simpa only [mul_comm] using mul_lt_mul_of_pos_right (hexp.trans hweight) h30
      _ < _ := mul_lt_mul_of_pos_left hsum (Real.exp_pos _)
  have hconst : 30 * (2 : ℝ) ^ (120 : ℕ) < combinedConstant 1 1 K := by
    apply hprefix.trans
    unfold combinedConstant PulseAmplitude.errorConstant
    linarith [PulseAmplitude.correctionEnergyConstant_pos (by norm_num : (0 : ℝ) < 1) 1,
      flattenLength_pos, NavierStokes.TailEnergyBounds.tailConstant_pos]
  have hinv : 1 < 1 / d.core.lam :=
    (lt_div_iff₀ d.core.lam_pos).mpr (by linarith [d.core.lam_lt])
  have hrate : d.core.lam < PulseAmplitude.logarithmicRate d.core.lam := by
    unfold PulseAmplitude.logarithmicRate
    nlinarith [mul_pos d.core.lam_pos (Real.log_pos hinv)]
  rw [combinedScale, hP, hm]
  exact (mul_lt_mul_of_pos_right hconst d.core.lam_pos).trans
    (mul_lt_mul_of_pos_left hrate (combinedConstant_pos (by norm_num) 1 K hK))

theorem mb_fixed_combinedScale_gt (d : TailData) (K : ℝ)
    (hP : d.core.P = 1) (hm : d.core.m = 1) (hK : 0 < K)
    (hlam : d.core.lam = 1 / 1000000000000) :
    1 / 1000 < combinedScale d K := by
  have h := mb_combinedScale_gt_prefix_lower d K hP hm hK
  rw [hlam] at h
  exact (show (1 : ℝ) / 1000 < 30 * 2 ^ (120 : ℕ) * (1 / 1000000000000) by norm_num).trans h

theorem mb_amplitude_gt_of_energyPolynomial_neg
    (d : TailData) (coefficients : ℝ → Coeff) (eta threshold : ℝ)
    (ht : 0 ≤ threshold) (hc : constantTerm d coefficients eta ≤ -(1 / 5))
    (hQ : energyPolynomial d coefficients threshold eta < 0) :
    threshold < amplitude d coefficients eta := by
  let r := amplitude d coefficients eta
  let a := NavierStokes.PulseAmplitude.quadraticCoefficient d.core
  let b := NavierStokes.PulseAmplitude.linearTerm d.core eta
  let c := constantTerm d coefficients eta
  have ha : 0 < a := NavierStokes.PulseAmplitude.quadraticCoefficient_pos d.core
  have hr : 0 < r := amplitude_pos d coefficients eta
  have hroot : a * r ^ 2 + b * r + c = 0 := amplitude_energy_equation d coefficients eta hc
  change a * threshold ^ 2 + b * threshold + c < 0 at hQ
  change c ≤ -(1 / 5) at hc
  have hmul : 0 < (a * (threshold + r) + b) * r := by
    nlinarith only [hroot, hc, mul_nonneg (mul_nonneg ha.le ht) hr.le]
  have hfactor : 0 < a * (threshold + r) + b := pos_of_mul_pos_left hmul hr.le
  by_contra! hn
  have hprod := mul_nonneg (sub_nonneg.mpr hn) hfactor.le
  nlinarith

#print axioms NSRW.P2.mb_combinedScale_gt_prefix_lower
#print axioms NSRW.P2.mb_fixed_combinedScale_gt
#print axioms NSRW.P2.mb_amplitude_gt_of_energyPolynomial_neg

end NSRW.P2
