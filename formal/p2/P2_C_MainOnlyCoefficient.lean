import P2_D_DeltaMComposition

/-!
# P2 C-01: main-only second repair coefficient

The source's actual normalized matrix equations give the exact identity
`affineCoefficients c 0 1 1 = -deltaM c / (exp (2 * beta c 0) - exp (2 * beta c 1))`.
The source separation estimate makes the denominator positive, so the compiled
D result implies positivity of this main-only coefficient.

This module does not identify it with the actual coefficient at any eta and
does not establish a small-eta coefficient sign or a mass-history zero.
-/

open NavierStokes.OutgoingSchedule
open NavierStokes.OutgoingPulseBounds

namespace NSRW.P2

theorem mainOnly_separation_gap_pos (c : Parameters) :
    0 < Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1) := by
  have hg := separation_exponential_gap c
  linarith [c.lam_pos]

theorem affineCoefficients_main_one_eq_neg_deltaM_div_gap (c : Parameters) :
    affineCoefficients c 0 1 1 =
      -deltaM c / (Real.exp (2 * beta c 0) - Real.exp (2 * beta c 1)) := by
  have hs := actual_coefficients_normalized_system c (affineDebt c 0 1)
  have h0 := congrFun hs 0
  have h1 := congrFun hs 1
  simp only [Matrix.mulVec, dotProduct, Fin.sum_univ_two, normalizedMatrix_entry] at h0 h1
  norm_num at h0 h1
  change rowMoment (c.exponents 0) * affineCoefficients c 0 1 0 +
      (rowMoment (c.exponents 0) * Real.exp (2 * beta c 0)) *
        affineCoefficients c 0 1 1 = normalizedDebt c (affineDebt c 0 1) 0 at h0
  change rowMoment (c.exponents 1) * affineCoefficients c 0 1 0 +
      (rowMoment (c.exponents 1) * Real.exp (2 * beta c 1)) *
        affineCoefficients c 0 1 1 = normalizedDebt c (affineDebt c 0 1) 1 at h1
  have hr0 : affineCoefficients c 0 1 0 +
      Real.exp (2 * beta c 0) * affineCoefficients c 0 1 1 =
        normalizedDebt c (affineDebt c 0 1) 0 / rowMoment (c.exponents 0) :=
    (eq_div_iff (rowMoment_pos c 0).ne').mpr (by nlinarith [h0])
  have hr1 : affineCoefficients c 0 1 0 +
      Real.exp (2 * beta c 1) * affineCoefficients c 0 1 1 =
        normalizedDebt c (affineDebt c 0 1) 1 / rowMoment (c.exponents 1) :=
    (eq_div_iff (rowMoment_pos c 1).ne').mpr (by nlinarith [h1])
  have hdiff := normalizedAffineMainDifference_eq_neg_deltaM c
  apply (eq_div_iff (mainOnly_separation_gap_pos c).ne').mpr
  nlinarith [hr0, hr1, hdiff]

theorem affineCoefficients_main_one_pos (c : Parameters) :
    0 < affineCoefficients c 0 1 1 := by
  rw [affineCoefficients_main_one_eq_neg_deltaM_div_gap]
  exact div_pos (neg_pos.mpr (deltaM_neg c)) (mainOnly_separation_gap_pos c)

#print axioms NSRW.P2.mainOnly_separation_gap_pos
#print axioms NSRW.P2.affineCoefficients_main_one_eq_neg_deltaM_div_gap
#print axioms NSRW.P2.affineCoefficients_main_one_pos

end NSRW.P2
