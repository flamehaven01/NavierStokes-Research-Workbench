import P2_CoefficientScaledBounds
import Mathlib.Analysis.Complex.ExponentialBounds

/-! Source estimates for MomentBound's scaled coefficient calculation. -/

open NavierStokes.OutgoingSchedule NavierStokes.OutgoingPulseBounds
open NavierStokes.OutgoingProfile

namespace NSRW.P2

private theorem mbExpLtPower {x : ℝ} {n : ℕ} (hx : x < (n : ℝ))
    (he : Real.exp 1 ≤ 3) : Real.exp x < (3 : ℝ) ^ n := by
  have hpow : Real.exp (n : ℝ) = Real.exp 1 ^ n := by
    rw [← Real.exp_nat_mul, mul_one]
  calc
    Real.exp x < Real.exp (n : ℝ) := Real.exp_lt_exp.mpr hx
    _ = Real.exp 1 ^ n := hpow
    _ ≤ 3 ^ n := pow_le_pow_left₀ (Real.exp_pos _).le he _

private theorem mb_main_ratio (c : Parameters) :
    normalizedMainMoment c 0 / rowMoment (c.exponents 0) ≤
      (1 / 2 : ℝ) * (normalizedMainMoment c 1 / rowMoment (c.exponents 1)) := by
  have hrow0 := rowMoment_pos c 0
  have hrow1 := rowMoment_pos c 1
  have hmain := normalizedMainMoment_one_pos c
  have hdecay : Real.exp (-2 + 3 * c.lam) ≤
      (1 / 2 : ℝ) * Real.exp (-(3 / 20 : ℝ) * c.lam) := by
    have he : Real.exp (-1 : ℝ) ≤ 1 / 2 := by
      rw [Real.exp_neg]
      simpa only [one_div] using one_div_le_one_div_of_le
        (by norm_num : (0 : ℝ) < 2) Real.exp_one_gt_two.le
    have h : Real.exp (-2 + 63 * c.lam / 20) ≤ 1 / 2 :=
      (Real.exp_le_exp.mpr (by linarith [c.lam_lt])).trans he
    calc
      Real.exp (-2 + 3 * c.lam) =
          Real.exp (-2 + 63 * c.lam / 20) * Real.exp (-(3 / 20 : ℝ) * c.lam) := by
        rw [← Real.exp_add]
        congr 1
        ring
      _ ≤ _ := mul_le_mul_of_nonneg_right h (Real.exp_pos _).le
  have hL2 := (mb_normalizedMainMoment_zero_le_decay_one c).trans
    (mul_le_mul_of_nonneg_right hdecay hmain.le)
  have hL3 := mul_le_mul_of_nonneg_left (rowMoment_one_scaled_le_rowMoment_zero c)
    (mul_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) hmain.le)
  have hcross : normalizedMainMoment c 0 * rowMoment (c.exponents 1) ≤
      ((1 / 2 : ℝ) * normalizedMainMoment c 1) * rowMoment (c.exponents 0) := by
    have h := mul_le_mul_of_nonneg_right hL2 hrow1.le
    linarith only [h, hL3]
  rw [← mul_div_assoc]
  exact (div_le_div_iff₀ hrow0 hrow1).mpr hcross

private theorem mb_scale_mul_gap (c : Parameters) :
    mbCommonScale c * (Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1)) =
      Real.exp (-(beta c 1 * center c 0)) / rowMoment (c.exponents 1) := by
  let gap := Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1)
  have hgap : gap ≠ 0 := (mainOnly_separation_gap_pos c).ne'
  have hrow : rowMoment (c.exponents 1) ≠ 0 := (rowMoment_pos c 1).ne'
  change Real.exp (-(beta c 1 * center c 0)) /
    (rowMoment (c.exponents 1) * gap) * gap =
    Real.exp (-(beta c 1 * center c 0)) / rowMoment (c.exponents 1)
  field_simp [hgap, hrow]

theorem mb_main_one_ge_coarse (c : Parameters) :
    mbCommonScale c * (1 / (10000 * c.lam)) ≤ affineCoefficients c 0 1 1 := by
  have hrow := rowMoment_pos c 1
  have hgap := mainOnly_separation_gap_pos c
  have hratio := mb_main_ratio c
  have hf := mul_le_mul_of_nonneg_left (mainMoment_one_lower c)
    (Real.exp_pos (-(beta c 1 * center c 0))).le
  change Real.exp (-(beta c 1 * center c 0)) * (1 / (5000 * c.lam)) ≤
    normalizedMainMoment c 1 at hf
  have hscaled := mul_le_mul_of_nonneg_left ((div_le_div_iff_of_pos_right hrow).mpr hf)
    (show (0 : ℝ) ≤ 1 / 2 by norm_num)
  rw [affineCoefficients_main_one_eq_neg_deltaM_div_gap]
  apply (le_div_iff₀ hgap).mpr
  calc
    _ = (1 / 2 : ℝ) * (Real.exp (-(beta c 1 * center c 0)) *
          (1 / (5000 * c.lam)) / rowMoment (c.exponents 1)) := by
      rw [mul_right_comm, mb_scale_mul_gap]
      have h : (1 : ℝ) / (10000 * c.lam) = (1 / 2) * (1 / (5000 * c.lam)) := by
        field_simp [c.lam_pos.ne'] <;> ring
      rw [h]
      ring
    _ ≤ (1 / 2 : ℝ) * (normalizedMainMoment c 1 / rowMoment (c.exponents 1)) := hscaled
    _ ≤ -deltaM c := by unfold deltaM; linarith only [hratio]

private theorem mb_prefix_ratio (c : Parameters) :
    Real.exp (-(beta c 0 * center c 0)) / rowMoment (c.exponents 0) ≤
      Real.exp (-(beta c 1 * center c 0)) / rowMoment (c.exponents 1) := by
  have hrow0 := rowMoment_pos c 0
  have hrow1 := rowMoment_pos c 1
  have hbeta : beta c 0 = beta c 1 + c.lam := by
    norm_num [beta, Parameters.exponents]
    ring
  have hcenter : c.lam * center c 0 = 13 - 3 * c.lam := by
    dsimp [center, Parameters.pulseLength]
    field_simp [c.lam_pos.ne']
  have hexp : Real.exp (-(beta c 0 * center c 0)) ≤
      Real.exp (-(beta c 1 * center c 0)) * Real.exp (-(3 / 20 : ℝ) * c.lam) := by
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    rw [hbeta, add_mul]
    linarith only [hcenter, c.lam_lt]
  apply (div_le_div_iff₀ hrow0 hrow1).mpr
  calc
    _ ≤ (Real.exp (-(beta c 1 * center c 0)) * Real.exp (-(3 / 20 : ℝ) * c.lam)) *
        rowMoment (c.exponents 1) := mul_le_mul_of_nonneg_right hexp hrow1.le
    _ = Real.exp (-(beta c 1 * center c 0)) *
        (Real.exp (-(3 / 20 : ℝ) * c.lam) * rowMoment (c.exponents 1)) := by ring
    _ ≤ _ := mul_le_mul_of_nonneg_left (rowMoment_one_scaled_le_rowMoment_zero c)
      (Real.exp_pos _).le

private theorem mb_prefix_bounds :
    prefixBound 1 1 0 ≤ 328 ∧ prefixBound 1 1 1 ≤ 3099396717 / 2 := by
  have he : Real.exp 1 ≤ 3 := Real.exp_one_lt_three.le
  have hx0 := (mbExpLtPower (n := 3) (x := Real.exp 1)
    (by simpa using Real.exp_one_lt_three) he).le
  have hx1 := (mbExpLtPower (n := 9) (x := 3 * Real.exp 1)
    (by norm_num; linarith only [Real.exp_one_lt_three]) he).le
  have hs := (mbExpLtPower (n := 8) (x := (Real.exp 1 + 12) / 2)
    (by norm_num; linarith only [he]) he).le
  change Real.exp (Real.exp 1) ≤ (3 : ℝ) ^ 3 at hx0
  change Real.exp (3 * Real.exp 1) ≤ (3 : ℝ) ^ 9 at hx1
  have hm0 := mul_le_mul he hx0 (Real.exp_pos _).le (by norm_num : (0 : ℝ) ≤ 3)
  have hm1 := mul_le_mul he hx1 (Real.exp_pos _).le (by norm_num : (0 : ℝ) ≤ 3)
  constructor
  · norm_num [prefixBound, prefixNumeratorBound, scaleFloor] at hm0 ⊢
    linarith only [hm0]
  · have hroot : Real.sqrt 2 ≠ 0 := (Real.sqrt_pos.2 (by norm_num)).ne'
    have heq : prefixBound 1 1 1 =
        (5 / 2 + 4 * Real.exp 1 * Real.exp (3 * Real.exp 1)) *
          Real.exp ((Real.exp 1 + 12) / 2) := by
      norm_num [prefixBound, prefixNumeratorBound, scaleFloor]
      rw [show (-12 + -Real.exp 1) / 2 = -((Real.exp 1 + 12) / 2) by ring,
        Real.exp_neg]
      field_simp [hroot, Real.exp_ne_zero] <;> ring
    rw [heq]
    calc
      _ ≤ (5 / 2 + 12 * (3 : ℝ) ^ 9) * (3 : ℝ) ^ 8 :=
        mul_le_mul (by linarith only [hm1]) hs (Real.exp_pos _).le (by norm_num)
      _ = _ := by norm_num

theorem mb_prefix_one_abs_le_coarse (c : Parameters) (hP : c.P = 1) (hm : c.m = 1) :
    |affineCoefficients c 1 0 1| ≤ mbCommonScale c * (328 + 3099396717 / 2) := by
  have hgap := mainOnly_separation_gap_pos c
  have hrow0 := rowMoment_pos c 0
  have hrow1 := rowMoment_pos c 1
  let w0 := Real.exp (-(beta c 0 * center c 0)) / rowMoment (c.exponents 0)
  let w1 := Real.exp (-(beta c 1 * center c 0)) / rowMoment (c.exponents 1)
  have hw0 : 0 ≤ w0 := div_nonneg (Real.exp_pos _).le hrow0.le
  have hw1 : 0 ≤ w1 := div_nonneg (Real.exp_pos _).le hrow1.le
  have hw : w0 ≤ w1 := mb_prefix_ratio c
  have hu0 := prefixCoefficient_le_bound c 0
  have hu1 := prefixCoefficient_le_bound c 1
  rw [hP, hm] at hu0 hu1
  have h0 := mul_le_mul (hu0.trans mb_prefix_bounds.1) hw
    hw0 (by norm_num : (0 : ℝ) ≤ 328)
  have h1 := mul_le_mul_of_nonneg_left (hu1.trans mb_prefix_bounds.2) hw1
  have htriangle : |w1 * prefixCoefficient c 1 - w0 * prefixCoefficient c 0| ≤
      w1 * |prefixCoefficient c 1| + w0 * |prefixCoefficient c 0| := by
    simpa only [sub_eq_add_neg, abs_neg, abs_mul, abs_of_nonneg hw1, abs_of_nonneg hw0] using
      (abs_add_le (w1 * prefixCoefficient c 1) (-(w0 * prefixCoefficient c 0)))
  rw [mb_prefix_one_eq_row_difference, abs_div, abs_of_pos hgap]
  apply (div_le_iff₀ hgap).mpr
  have h0eq : Real.exp (-(beta c 0 * center c 0)) * prefixCoefficient c 0 /
      rowMoment (c.exponents 0) = w0 * prefixCoefficient c 0 := by dsimp [w0]; ring
  have h1eq : Real.exp (-(beta c 1 * center c 0)) * prefixCoefficient c 1 /
      rowMoment (c.exponents 1) = w1 * prefixCoefficient c 1 := by dsimp [w1]; ring
  rw [h0eq, h1eq]
  calc
    _ ≤ w1 * (328 + 3099396717 / 2) := by linarith only [htriangle, h0, h1]
    _ = _ := by
      rw [mul_right_comm, mb_scale_mul_gap]

theorem mb_qStar_ge_source_coarse (c : Parameters) (eta : ℝ) (hP : c.P = 1) (hm : c.m = 1) :
    mbCommonScale c * mbCoarseBound c eta ≤ mbQStar c eta :=
  mb_qStar_ge_scaled_coarse c eta (mb_main_one_ge_coarse c) (mb_prefix_one_abs_le_coarse c hP hm)

theorem mb_fixed_coarse_eq (c : Parameters) (hlam : c.lam = 1 / 1000000000000) :
    mbCoarseBound c (1 / 1048576) = 207522463005781740692370179 / 2305843009213693952 := by
  unfold mbCoarseBound parameterPolynomial
  rw [hlam]
  norm_num

theorem mb_fixed_coarse_pos (c : Parameters) (hlam : c.lam = 1 / 1000000000000) :
    0 < mbCoarseBound c (1 / 1048576) := by
  rw [mb_fixed_coarse_eq c hlam]
  norm_num

theorem mb_actualSecondRepairCoefficient_fixed_pos (F : Profile)
    (hP : F.data.core.P = 1) (hm : F.data.core.m = 1)
    (hlam : F.data.core.lam = 1 / 1000000000000)
    (hAmp : (9 / 10 : ℝ) < F.amp (1 / 1048576)) :
    0 < actualSecondRepairCoefficient F (1 / 1048576) := by
  exact mb_actualSecondRepairCoefficient_pos_of_scaled_coarse F _ hAmp
    (mb_main_one_ge_coarse F.data.core) (mb_prefix_one_abs_le_coarse F.data.core hP hm)
    (mb_fixed_coarse_pos F.data.core hlam)

#check NSRW.P2.mb_main_one_ge_coarse
#check NSRW.P2.mb_prefix_one_abs_le_coarse
#check NSRW.P2.mb_qStar_ge_source_coarse
#check NSRW.P2.mb_fixed_coarse_eq
#check NSRW.P2.mb_fixed_coarse_pos
#check NSRW.P2.mb_actualSecondRepairCoefficient_fixed_pos

#print axioms NSRW.P2.mb_main_one_ge_coarse
#print axioms NSRW.P2.mb_prefix_one_abs_le_coarse
#print axioms NSRW.P2.mb_qStar_ge_source_coarse
#print axioms NSRW.P2.mb_fixed_coarse_eq
#print axioms NSRW.P2.mb_fixed_coarse_pos
#print axioms NSRW.P2.mb_actualSecondRepairCoefficient_fixed_pos

end NSRW.P2
