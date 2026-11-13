import P2_CoefficientSourceBounds
import P2_ZPLUS_J_MarginNormalization

/-! MomentBound's normalized angular-moment bound at a first-window mass zero. -/

noncomputable section

open MeasureTheory
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingPulseBounds
open NavierStokes.OutgoingProfile

namespace NSRW.P2

def mbRepairRatio (lam : ℝ) : ℝ :=
  (Real.exp (17 * lam / 10) - 1) / (Real.exp (2 * lam) - 1)

private theorem exp_two_lam_sub_one_pos (c : Parameters) :
    0 < Real.exp (2 * c.lam) - 1 := by
  rw [sub_pos, ← Real.exp_zero]
  exact Real.exp_lt_exp.mpr (by linarith [c.lam_pos])

theorem mbRepairRatio_pos (c : Parameters) : 0 < mbRepairRatio c.lam := by
  apply div_pos _ (exp_two_lam_sub_one_pos c)
  rw [sub_pos, ← Real.exp_zero]
  exact Real.exp_lt_exp.mpr (by linarith [c.lam_pos])

private theorem main_gap_factorization (c : Parameters) :
    Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1) =
      Real.exp (1 - 4 * c.lam) * (Real.exp (2 * c.lam) - 1) := by
  have h0 : 2 * beta c 0 = (1 - 4 * c.lam) + 2 * c.lam := by
    norm_num [beta, Parameters.exponents]
    ring
  have h1 : 2 * beta c 1 = 1 - 4 * c.lam := by
    norm_num [beta, Parameters.exponents]
    ring
  rw [h0, h1, Real.exp_add]
  ring

def mbSecondBumpMass (c : Parameters) : ℝ :=
  ∫ x : ℝ, x ^ c.exponents 0 *
    NavierStokes.LocalizedMomentRepair.bump (c.lower 1) (c.upper 1) x

def mbFirstRepairWeightGap (c : Parameters) : ℝ :=
  c.upper 0 ^ (-c.lam) - c.lower 1 ^ (-c.lam)

theorem mb_scale_mul_secondBump_mul_weightGap (c : Parameters) :
    mbCommonScale c * mbSecondBumpMass c * mbFirstRepairWeightGap c =
      (rowMoment (c.exponents 0) / rowMoment (c.exponents 1)) *
        Real.exp (3 * c.lam / 20) * mbRepairRatio c.lam := by
  have hexp :
      Real.exp (-(beta c 1 * center c 0)) *
        Real.exp (c.pulseLength * (1 / 2 - c.lam)) *
        Real.exp (-(1 / 2 - c.lam)) * Real.exp (-13 + 23 * c.lam / 20) =
      Real.exp (3 * c.lam / 20) * Real.exp (1 - 4 * c.lam) := by
    simp only [← Real.exp_add]
    congr 1
    norm_num [beta, Parameters.exponents, center, Parameters.pulseLength]
    field_simp [c.lam_pos.ne']
    ring
  unfold mbCommonScale mbSecondBumpMass mbFirstRepairWeightGap mbRepairRatio
  rw [secondBumpWeightedMoment_eq_normalized, normalizedSecondBumpMoment_eq_rowMoment,
    firstRepair_weightGap_exp_eq, main_gap_factorization]
  calc
    _ = (Real.exp (-(beta c 1 * center c 0)) *
          Real.exp (c.pulseLength * (1 / 2 - c.lam)) *
          Real.exp (-(1 / 2 - c.lam)) * Real.exp (-13 + 23 * c.lam / 20)) *
        rowMoment (c.exponents 0) * (Real.exp (17 * c.lam / 10) - 1) /
        (rowMoment (c.exponents 1) *
          (Real.exp (1 - 4 * c.lam) * (Real.exp (2 * c.lam) - 1))) := by ring
    _ = _ := by
      rw [hexp]
      field_simp [(rowMoment_pos c 1).ne', (exp_two_lam_sub_one_pos c).ne',
        (Real.exp_pos (1 - 4 * c.lam)).ne']

theorem mb_repairRatio_le_scale_mul_secondBump_mul_weightGap (c : Parameters) :
    mbRepairRatio c.lam ≤ mbCommonScale c * mbSecondBumpMass c * mbFirstRepairWeightGap c := by
  rw [mb_scale_mul_secondBump_mul_weightGap]
  have h := mul_le_mul_of_nonneg_left (rowMoment_one_scaled_le_rowMoment_zero c)
    (Real.exp_pos (3 * c.lam / 20)).le
  have he : Real.exp (3 * c.lam / 20) * Real.exp (-(3 / 20 : ℝ) * c.lam) = 1 := by
    rw [← Real.exp_add, show 3 * c.lam / 20 + -(3 / 20 : ℝ) * c.lam = 0 by ring,
      Real.exp_zero]
  rw [← mul_assoc, he, one_mul] at h
  have hfactor : 1 ≤ (rowMoment (c.exponents 0) / rowMoment (c.exponents 1)) *
      Real.exp (3 * c.lam / 20) := by
    rw [div_mul_eq_mul_div]
    apply (le_div_iff₀ (rowMoment_pos c 1)).mpr
    simpa only [one_mul, mul_comm] using h
  simpa only [one_mul] using mul_le_mul_of_nonneg_right hfactor (mbRepairRatio_pos c).le

theorem mb_normalizedAngularMoment_gt_coarse_mul_ratio (F : Profile) (eta r : ℝ)
    (hP : F.data.core.P = 1) (hm : F.data.core.m = 1)
    (hAmp : (9 / 10 : ℝ) < F.amp eta) (hB : 0 < mbCoarseBound F.data.core eta)
    (hr : F.data.core.lower 0 < r) (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0) :
    0 < mbCoarseBound F.data.core eta * mbRepairRatio F.data.core.lam ∧
      mbCoarseBound F.data.core eta * mbRepairRatio F.data.core.lam <
        localAngularMoment F eta r / (momentScale F.data.core 1 * shape eta ^ 2) := by
  let c := F.data.core
  let k := momentScale c 1 * shape eta ^ 2
  have hk : 0 < k := mul_pos (momentScale_pos c 1) (sq_pos_of_pos (shape_pos eta))
  have hi : 0 < mbSecondBumpMass c := secondBumpWeightedMoment_pos c
  have hd : 0 < mbFirstRepairWeightGap c := firstRepair_weightGap_pos c
  have hcoeff : mbCommonScale c * mbCoarseBound c eta <
      localSecondRepairCoefficient F eta :=
    (mb_qStar_ge_source_coarse c eta hP hm).trans_lt
      (mb_actualSecondRepairCoefficient_gt_qStar F eta hAmp)
  have hc1 := (mul_pos (mbCommonScale_pos c) hB).trans hcoeff
  have hj := angularMoment_ge_firstRepair_margin F eta r hr hr_upper hM hc1
  have hjnorm : localSecondRepairCoefficient F eta * mbSecondBumpMass c *
      mbFirstRepairWeightGap c ≤ localAngularMoment F eta r / k := by
    apply (le_div_iff₀ hk).mpr
    calc
      _ = k * localSecondRepairCoefficient F eta * mbSecondBumpMass c *
          mbFirstRepairWeightGap c := by ring
      _ ≤ _ := hj
  refine ⟨mul_pos hB (mbRepairRatio_pos c), ?_⟩
  calc
    mbCoarseBound c eta * mbRepairRatio c.lam ≤
        mbCoarseBound c eta * (mbCommonScale c * mbSecondBumpMass c * mbFirstRepairWeightGap c) :=
      mul_le_mul_of_nonneg_left (mb_repairRatio_le_scale_mul_secondBump_mul_weightGap c) hB.le
    _ = mbCommonScale c * mbCoarseBound c eta * mbSecondBumpMass c * mbFirstRepairWeightGap c := by ring
    _ < localSecondRepairCoefficient F eta * mbSecondBumpMass c * mbFirstRepairWeightGap c :=
      mul_lt_mul_of_pos_right (mul_lt_mul_of_pos_right hcoeff hi) hd
    _ ≤ localAngularMoment F eta r / k := hjnorm

#check NSRW.P2.mbRepairRatio_pos
#check NSRW.P2.mb_scale_mul_secondBump_mul_weightGap
#check NSRW.P2.mb_repairRatio_le_scale_mul_secondBump_mul_weightGap
#check NSRW.P2.mb_normalizedAngularMoment_gt_coarse_mul_ratio

#print axioms NSRW.P2.mbRepairRatio_pos
#print axioms NSRW.P2.mb_scale_mul_secondBump_mul_weightGap
#print axioms NSRW.P2.mb_repairRatio_le_scale_mul_secondBump_mul_weightGap
#print axioms NSRW.P2.mb_normalizedAngularMoment_gt_coarse_mul_ratio

end NSRW.P2
