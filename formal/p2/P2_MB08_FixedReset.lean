import NavierStokes.UniformAngularReset
import Mathlib.Analysis.Complex.ExponentialBounds

/-! Assemble the fixed-lambda scheduled reset from explicit operator bounds. -/

open Set Filter
open scoped ContDiff Topology
open NavierStokes.OutgoingTail NavierStokes.AngularMomentReset
open NavierStokes.UniformAngularReset

namespace NSRW.P2

theorem mb_fixed_reset_of_operator_bounds (d : TailData)
    (hlam : d.core.lam = 1 / 1000000000000)
    (hinv : ∀ x, ‖(linearEquivNonneg d.core.lam d.core.lam_pos.le).symm x‖ ≤ 1000 * ‖x‖)
    (hquad : ‖quadraticCLM d.core.lam‖ ≤ 1)
    (hjet : ∀ (c : Coeff) (y : ℝ),
      |relative c y| ≤ 500 * ‖c‖ ∧ |deriv (relative c) y| ≤ 500 * ‖c‖) :
    Nonempty (ResetWitness d 81162000) := by
  have hsmall : d.core.lam ≤ 1 / 15 := by rw [hlam]; norm_num
  have hC : 3 * Real.exp 3 ≤ (81 : ℝ) := by
    have hp : Real.exp 3 = Real.exp 1 ^ (3 : ℕ) := by rw [← Real.exp_nat_mul]; norm_num
    rw [hp]
    linarith [pow_le_pow_left₀ (Real.exp_pos 1).le Real.exp_one_lt_three.le (3 : ℕ)]
  have hbound (eta : ℝ) : |normalizedDebt d eta| ≤ 81 * d.core.lam ^ (28 : ℕ) ∧
      |deriv (normalizedDebt d) eta| ≤ 81 * d.core.lam ^ (28 : ℕ) := by
    have hb := actual_debt_first_jet_bound d hsmall eta
    have hm := mul_le_mul_of_nonneg_right hC (pow_nonneg d.core.lam_pos.le 28)
    exact ⟨hb.1.trans hm, hb.2.trans hm⟩
  obtain ⟨g, hg, hsolve, hlip⟩ := exists_smooth_solver_on_ball
    (linearEquivNonneg d.core.lam d.core.lam_pos.le) (quadraticCLM d.core.lam)
    1000 1 (1 / 4000) (by norm_num) (by norm_num) (by norm_num) hinv hquad (by norm_num)
  let f : ℝ → Coeff := fun delta => g (debt delta)
  have hball {delta : ℝ} (hd : |delta| < (1 / 4000) / (4 * 1000)) :
      debt delta ∈ Metric.ball 0 ((1 / 4000) / (4 * 1000)) := by
    simpa only [Metric.mem_ball, dist_zero_right] using (debt_norm_le delta).trans_lt hd
  have hdebt (eta : ℝ) : |normalizedDebt d eta| < (1 / 4000) / (4 * 1000) :=
    (hbound eta).1.trans_lt (by rw [hlam]; norm_num)
  have hf : ContDiffOn ℝ ∞ f (Ioo (-((1 / 4000) / (4 * 1000))) ((1 / 4000) / (4 * 1000))) :=
    hg.comp debt_contDiff.contDiffOn (fun _ hx => hball (abs_lt.mpr hx))
  have hn (eta : ℝ) : ‖f (normalizedDebt d eta)‖ ≤ 162000 * d.core.lam ^ (28 : ℕ) := by
    have h := (hsolve _ (hball (hdebt eta))).2
    calc
      _ ≤ 2 * 1000 * ‖debt (normalizedDebt d eta)‖ := h
      _ ≤ _ := by nlinarith only [debt_norm_le (normalizedDebt d eta), (hbound eta).1]
  have heq (eta : ℝ) :
      linearCLM d.core.lam (f (normalizedDebt d eta)) +
        quadraticCLM d.core.lam (f (normalizedDebt d eta)) (f (normalizedDebt d eta)) =
        debt (normalizedDebt d eta) := (hsolve _ (hball (hdebt eta))).1
  refine ⟨{
    coefficients := fun eta => f (normalizedDebt d eta)
    smooth := contDiffOn_univ.mp (hf.comp (normalizedDebt_contDiff d).contDiffOn
      (fun eta _ => abs_lt.mp (hdebt eta)))
    angular := ?_
    pressure := ?_
    coefficient_bound := fun eta => (hn eta).trans
      (by nlinarith [pow_nonneg d.core.lam_pos.le (28 : ℕ)])
    eta_derivative_bound := ?_
    small_jets := ?_ }⟩
  · intro eta
    have h := heq eta
    rw [actual_moment_map] at h
    exact congrFun h 0
  · intro eta
    have h := heq eta
    rw [actual_moment_map] at h
    exact congrFun h 1
  · intro eta
    let delta := normalizedDebt d eta
    have hd := isOpen_Ioo.mem_nhds (abs_lt.mp (hdebt eta))
    have hfd : HasDerivAt f (deriv f delta) delta :=
      ((hf.contDiffAt hd).differentiableAt (by simp)).hasDerivAt
    have hD : ‖deriv f delta‖ ≤ 2 * 1000 := by
      apply norm_deriv_le_of_lip' (by norm_num)
      filter_upwards [hd] with x hx
      have he : debt x - debt delta = debt (x - delta) := by
        ext i
        fin_cases i <;> simp [debt]
      have h := hlip _ (hball (abs_lt.mpr hx)) _ (hball (hdebt eta))
      rw [he] at h
      simpa only [Real.norm_eq_abs] using h.trans
        (mul_le_mul_of_nonneg_left (debt_norm_le (x - delta)) (by norm_num : (0 : ℝ) ≤ 2 * 1000))
    have hdD := ((normalizedDebt_contDiff d).differentiable (by simp) eta).hasDerivAt
    have hchain := hfd.scomp eta hdD
    change HasDerivAt (fun x => f (normalizedDebt d x)) _ eta at hchain
    rw [hchain.deriv, norm_smul, Real.norm_eq_abs]
    calc
      _ ≤ (81 * d.core.lam ^ (28 : ℕ)) * (2 * 1000) :=
        mul_le_mul (hbound eta).2 hD (norm_nonneg _) (by positivity)
      _ ≤ _ := by nlinarith [pow_nonneg d.core.lam_pos.le (28 : ℕ)]
  · intro eta y
    have hj := hjet (f (normalizedDebt d eta)) y
    have h := mul_le_mul_of_nonneg_left (hn eta) (by norm_num : (0 : ℝ) ≤ 500)
    exact ⟨hj.1.trans (h.trans (by rw [hlam]; norm_num)),
      hj.2.trans (h.trans (by rw [hlam]; norm_num))⟩

#print axioms NSRW.P2.mb_fixed_reset_of_operator_bounds

end NSRW.P2
