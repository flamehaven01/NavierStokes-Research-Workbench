# A First-Repair Mass Zero Without Angular-Moment Cancellation

**Yun Kwansub**

Research manuscript, version 0.4 — 14 October 2026.

## Abstract

We study two weighted histories in a specified outgoing-profile construction. For each fixed source Profile, we prove that every sufficiently small positive angular parameter admits a point strictly inside the first repair window where the mass history vanishes and the angular-weighted history is strictly positive at the same point. The positive parameter threshold may depend on the Profile. The decisive argument compares future moments of two separated repair bumps. At a mass zero, positivity of the second repair coefficient forces the first coefficient to be negative; the decreasing relative weight between the two histories then makes the angular tail negative and the accumulated angular history positive. We give the coefficient, boundary-sign, continuity and coordinate arguments needed to turn this conditional statement into an existence theorem. The corresponding source-bound propositions are formalized in Lean 4 and have a recorded fixed-checkpoint compilation. The result identifies a denominator obstruction for a prospective normalized ratio without requiring that ratio to be introduced into the source construction.

**Keywords:** weighted moments; localized repair; separated supports; formalized analysis; Lean 4.

## 1. Introduction

Moment repair can enforce several terminal cancellation conditions while leaving their partial histories markedly different. The location and sign of those partial histories matter when a derived quantity divides by one of them. A terminal identity alone does not determine whether cancellation occurs earlier, or whether a second history cancels at the same point.

This paper analyzes that question for the outgoing-profile construction defined in the pinned `NavierStokesAndEuler` source [1]. The two quantities are the source mass history M and its H-weighted history J. Our initial investigation considered the ratio J/(M H). The principal result is more naturally stated directly in terms of M and J: each fixed source Profile has a positive parameter neighborhood in which every positive parameter admits an interior first-repair point with M=0 and J>0.

The construction prescribes outgoing fields through localized pulse and repair terms. Its two terminal history constraints make partial cancellation a natural question: enforcing both histories at the end of the schedule need not synchronize them inside a repair window. Our analysis concerns that precise feature of the source construction. The names of the histories are used according to their defining integrals, without assigning an additional flux or vorticity interpretation.

The argument has two parts. First, moment comparisons determine the sign of the main-only second repair coefficient. The exact coefficient decomposition and continuity transfer this sign to the actual coefficient near zero. Boundary signs and the intermediate value theorem then produce an interior mass zero. Second, a relative-weight comparison proves J>0 at every first-window mass zero whose second coefficient is positive, not merely at a particular zero selected by the existence argument.

The mathematical contribution of this paper is the explicit source-linked derivation of this non-simultaneous cancellation and its formalization. The weighted comparison itself uses elementary real analysis. We do not claim priority over an exhaustive mathematical literature; the references establish the construction and formalization context, not a completed novelty survey. The proof and its precise quantifiers are the objects offered for assessment.

Section 2 specifies the construction and notation. Section 3 states the results. Sections 4 and 5 prove the conditional comparison and the existence theorem. Section 6 explains the formal correspondence and recorded computation. Section 7 discusses the interpretation of the result.

## 2. Construction and notation

### 2.1. Fixed source Profile

Fix a `Profile F` of the source `NavierStokes.OutgoingProfile` namespace at revision

`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

A source Profile contains tail data, a coefficient bound and a reset witness. Its corrected amplitude is the source function `F.amp`; the coefficients contained in its angular-reset witness are not the axial repair coefficients studied below. All these objects belong to the same fixed Profile.

Write c for `F.data.core`. Its parameter structure includes P>0, m>0, 0<λ<1/10 and wait>25. We retain the full source Profile type, including its tail and reset data, rather than substituting an arbitrary amplitude satisfying only selected properties. Let

\[
B=c.\mathrm{pulseStart},\qquad L=\frac{13}{\lambda},\qquad R=e^L,
\qquad a_0=-\left(\frac12+\lambda\right),\qquad
a_1=-\left(\frac12+2\lambda\right)=a_0-\lambda. \tag{2.1}
\]

The pulse-local radius is r; its source radial coordinate is X=e^B r. The source's logarithmic coordinate is y=B+log r.

The two repair intervals have endpoints

\[
\begin{aligned}
l_0&=e^{L-63/20},&u_0&=e^{L-57/20},\\
l_1&=e^{L-23/20},&u_1&=e^{L-17/20}.
\end{aligned} \tag{2.2}
\]

The parameter bounds imply

\[
1<e^{11/\lambda}<l_0<u_0<l_1<u_1<R. \tag{2.3}
\]

Indeed, L-63/20-11/λ=2/λ-63/20>0, and the remaining comparisons follow by comparing exponential arguments. In particular the first and second repair supports are strictly separated.

### 2.2. Source histories and pulse-local histories

The source defines the radial fields U_F, E_F and

\[
H_F(X,\eta)=\sqrt{2X}\,E_F(X,\eta).
\]

Its histories are

\[
M_F(\eta,X)=\int_{(0,X]}U_F(u,\eta)\,du,\qquad
J_F(\eta,X)=\int_{(0,X]}H_F(u,\eta)U_F(u,\eta)\,du. \tag{2.4}
\]

These are the definitions of `Profile.M` and `Profile.J`, respectively [1]. J is an H-weighted history; no identification with vorticity or enstrophy is needed here.

For r≥1 define the local histories

\[
\mathcal M_F(\eta,r)=\mathrm{massMoment}(c,F.\mathrm{amp},\eta,B+\log r),\qquad
\mathcal J_F(\eta,r)=\mathrm{angularMoment}(c,F.\mathrm{amp},\eta,B+\log r).
\]

The source identities `M_at_exp` and `J_at_exp` apply because B+log r≥0, and give the exact equalities

\[
\mathcal M_F(\eta,r)=M_F(\eta,e^B r),\qquad
\mathcal J_F(\eta,r)=J_F(\eta,e^B r). \tag{2.5}
\]

There is no additional scale factor in (2.5). The integral prefactors introduced next belong to the histories themselves.

### 2.3. Repair coefficients and tails

Let A_F(η)=F.amp(η). It is smooth and strictly positive by the source corrected-amplitude results. Put s(η)=(1+η²)⁻¹. Let

\[
b_j(x)=\mathrm{LocalizedMomentRepair.bump}(l_j,u_j,x),\qquad j=0,1.
\]

Each b_j is nonnegative with topological support contained in (l_j,u_j). More precisely, the source bump is supported inside the middle half
\([(3l_j+u_j)/4,(l_j+3u_j)/4]\) of its declared window. Positivity throughout the larger window is not an assumption. Define c_j(η) to be component j of the source axial repair coefficient vector

\[
\mathrm{LocalizedMomentRepair.coefficients}
\bigl(c.\mathrm{exponents},c.\mathrm{lower},c.\mathrm{upper},
\mathrm{debt}(c,A_F,\eta)\bigr).
\]

The pulse is

\[
p_F(\eta,x)=A_F(\eta)\,\mathrm{mainPulse}(\lambda\log x)
               +c_0(\eta)b_0(x)+c_1(\eta)b_1(x). \tag{2.6}
\]

For x≥l₀ the main pulse is zero. Thus every future interval starting inside the first repair window sees only the two correction bumps.

Let κ_i=`momentScale c i` and define the strictly positive prefactors

\[
K_0(\eta)=\kappa_0 s(\eta),\qquad K_1(\eta)=\kappa_1 s(\eta)^2.
\]

The source prefix constants P_M=`prefixM c` and P_J=`prefixJ c` give, for 1≤r≤R,

\[
\begin{aligned}
\mathcal M_F(\eta,r)&=P_M\eta+K_0(\eta)\int_1^r x^{a_0}p_F(\eta,x)\,dx,\\
\mathcal J_F(\eta,r)&=P_J\eta s(\eta)+K_1(\eta)\int_1^r x^{a_1}p_F(\eta,x)\,dx.
\end{aligned} \tag{2.7}
\]

Terminal cancellation, supplied by `pulse_closes_prefix`, changes these to

\[
\mathcal M_F(\eta,r)=-K_0(\eta)\int_r^R x^{a_0}p_F(\eta,x)\,dx,\qquad
\mathcal J_F(\eta,r)=-K_1(\eta)\int_r^R x^{a_1}p_F(\eta,x)\,dx. \tag{2.8}
\]

For r∈(l₀,u₀), abbreviate

\[
T_j(r)=\int_r^R x^{a_0}b_j(x)\,dx,\qquad
S_j(r)=\int_r^R x^{a_1}b_j(x)\,dx. \tag{2.9}
\]

Then (2.8) becomes

\[
\mathcal M_F=-K_0(c_0T_0+c_1T_1),\qquad
\mathcal J_F=-K_1(c_0S_0+c_1S_1). \tag{2.10}
\]

All terms in each equation refer to the same F, η and r.

## 3. Main results

**Theorem 3.1 (conditional angular mismatch).** Fix a source Profile F. For any real η and any r satisfying l₀<r<u₀,

\[
\mathcal M_F(\eta,r)=0\quad\text{and}\quad c_1(\eta)>0
\quad\Longrightarrow\quad\mathcal J_F(\eta,r)>0.
\]

No sign assumption on η is required in this theorem.

**Theorem 3.2 (same-point existence).** For every fixed source Profile F there exists ε_F>0 such that, for every 0<η<ε_F, there exists r∈(l₀,u₀) with

\[
M_F(\eta,e^B r)=0\quad\text{and}\quad J_F(\eta,e^B r)>0. \tag{3.1}
\]

The positive threshold ε_F may depend on F, and the witness radius r may depend on η. Both clauses in (3.1) use that one witness.

## 4. Proof of the conditional comparison

**Lemma 4.1 (tail signs and coefficient sign).** At a point satisfying the hypotheses of Theorem 3.1, T₁>0, T₀>0 and c₀<0.

*Proof.* Since r<u₀<l₁ and u₁<R, the future interval contains the whole second support. Therefore T₁ equals its whole-line weighted bump moment. The source matrix-entry identity expresses this moment as a positive template row moment times a positive exponential. Hence T₁>0. Also T₀≥0 because its integrand is nonnegative on positive x. The mass-zero identity in (2.10), with K₀>0, gives

\[
c_0T_0=-c_1T_1<0. \tag{4.1}
\]

If T₀=0, (4.1) is impossible. Thus T₀>0, and (4.1) forces c₀<0. ∎

**Lemma 4.2 (comparison of relative weights).** For every r∈(l₀,u₀),

\[
u_0^{-\lambda}T_0\le S_0,\qquad
S_1\le l_1^{-\lambda}T_1,\qquad
l_1^{-\lambda}<u_0^{-\lambda}. \tag{4.2}
\]

*Proof.* The identity a₁=a₀−λ gives x^{a₁}=x^{a₀}x^{−λ} for x>0. The function x↦x^{−λ} strictly decreases since λ>0. Wherever b₀ is nonzero, x<u₀ and thus x^{−λ}≥u₀^{−λ}. Wherever b₁ is nonzero, x>l₁ and x^{−λ}≤l₁^{−λ}. Multiplying these inequalities by the respective nonnegative integrands x^{a₀}b_j(x) and integrating gives the first two comparisons. The final strict comparison follows from u₀<l₁. ∎

*Proof of Theorem 3.1.* By Lemma 4.1, c₀<0 and c₁>0. Consequently the first inequality in (4.2) reverses when multiplied by c₀. Using both tail bounds and then (4.1),

\[
\begin{aligned}
c_0S_0+c_1S_1
&\le c_0u_0^{-\lambda}T_0+c_1l_1^{-\lambda}T_1\\
&=c_1T_1\bigl(l_1^{-\lambda}-u_0^{-\lambda}\bigr)<0.
\end{aligned} \tag{4.3}
\]

Equation (2.10) and K₁>0 now give \(\mathcal J_F(\eta,r)>0\). ∎

The argument explains why moment cancellation is not transported from one weight to the other: a negative first-support contribution receives a larger relative weight than the positive second-support contribution. Positivity of T₀ is a consequence of mass balance, not an additional assumption. It does not imply b₀(r)>0 at the zero itself.

## 5. Coefficient positivity and interior existence

### 5.1. Sign of the actual coefficient near zero

Write β_i=a_i+1 and q=L−3. The source main moments and their normalized values are

\[
\mu_i=\int_1^R x^{a_i}\mathrm{mainPulse}(\lambda\log x)\,dx,
\qquad \mathcal F_i=e^{-\beta_i q}\mu_i.
\]

Let A_i=`rowMoment(c.exponents i)` be the positive source template moments and k=e^{−3λ/20}.

The notation corresponds to `OutgoingPulseBounds.beta c i`, `OutgoingPulseBounds.center c 0`, `OutgoingSchedule.mainMoment c i`, `NSRW.P2.normalizedMainMoment c i` and `OutgoingPulseBounds.rowMoment (c.exponents i)`, respectively. Exact locators are the pinned definitions of [beta](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L178), [center](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L462) and [rowMoment](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L493), together with the [NSRW normalized-moment definition at the execution revision](https://github.com/flamehaven01/NavierStokes-Research-Workbench/blob/3a50b5f50b034319a469b9de68f556be70fff02c/formal/p2/P2_L2_NormalizedMainMomentComparison.lean). Thus q is the first repair center in logarithmic coordinates; it is not the endpoint l₀ or u₀. The formalized main-pulse and template comparisons give

\[
\mathcal F_1>0,\qquad \mathcal F_0<k\mathcal F_1,
\qquad kA_1\le A_0. \tag{5.1}
\]

For completeness, the strict main comparison first bounds the extra exponential on the short logarithmic interval 0≤y≤11/λ by e^{−2+3λ}. The condition λ<1/10 implies −2+3λ<−3λ/20. Multiplication by the positive normalized first moment provides strictness. The template comparison uses the nonnegative template support in x>e^{−3/20} and the factor x^λ. These are separately formalized comparisons [2].

Multiplying (5.1) by the appropriate positive factors yields

\[
\mathcal F_0A_1<k\mathcal F_1A_1\le\mathcal F_1A_0.
\]

Thus

\[
\Delta=\frac{\mathcal F_0}{A_0}-\frac{\mathcal F_1}{A_1}<0. \tag{5.2}
\]

The normalized source repair equations identify the main-only second coefficient m₁ as

\[
m_1=\frac{-\Delta}{e^{2\beta_0}-e^{2\beta_1}}>0. \tag{5.3}
\]

The denominator is positive because β₀−β₁=λ>0. Explicitly, let
\(p_1=\mathrm{affineCoefficients}(c,1,0,1)\) and
\(m_1=\mathrm{affineCoefficients}(c,0,1,1)\).
Both are constants determined by the fixed core c, independent of η. The actual coefficient of the fixed Profile satisfies the exact decomposition

\[
c_1(\eta)=\eta(1+\eta^2)p_1+A_F(\eta)m_1. \tag{5.4}
\]

In particular c₁(0)=A_F(0)m₁>0. The corrected amplitude is smooth, so (5.4) is continuous in η. The preimage of the positive half-line is an open neighborhood of zero. It therefore contains (−ε_F,ε_F) for some ε_F>0. Restricting to 0<η<ε_F supplies the required sign c₁(η)>0.

### 5.2. Boundary signs and continuity

**Lemma 5.1 (first-window boundary signs).** If η>0 and c₁(η)>0, then

\[
\mathcal M_F(\eta,l_0)>0,\qquad
\mathcal M_F(\eta,u_0)<0. \tag{5.5}
\]

*Proof.* The source prefix constant satisfies

\[
P_M=4+\int_0^B e^y\,\mathrm{dropCoefficient}(c.m,y)\,dy>0,
\]

because the integrand is nonnegative. Both repair bumps vanish before and at l₀, so the partial pulse integral in (2.7) at l₀ is nonnegative: A_F>0, the main pulse is nonnegative for nonnegative argument, and x^{a₀}>0 on x≥1. The term P_Mη is strictly positive.

At u₀, the main pulse and first bump vanish on the future interval. The mass-tail identity reduces to

\[
\mathcal M_F(\eta,u_0)=-K_0(\eta)c_1(\eta)
\int_{u_0}^R x^{a_0}b_1(x)\,dx<0,
\]

since the second-bump moment is strictly positive. ∎

**Lemma 5.2 (continuity on the repair interval).** For fixed F and η, the map r↦\(\mathcal M_F(\eta,r)\) is continuous on [l₀,u₀].

*Proof.* The source logarithmic mass primitive is

\[
4\eta+\int_0^y e^t\,\mathrm{axial}(c,A_F)(t,\eta)\,dt.
\]

Its integrand is continuous, so it is continuous in y. The map r↦B+log r is continuous on [l₀,u₀], where r>0. Composition proves the assertion. ∎

*Proof of Theorem 3.2.* Choose ε_F from (5.4) and continuity. For every 0<η<ε_F, Lemmas 5.1 and 5.2 and the intermediate value theorem give a zero in [l₀,u₀]. The strict signs in (5.5) exclude both endpoints, so the zero belongs to (l₀,u₀). Theorem 3.1 gives positive local angular history at that very zero. Equation (2.5) transfers both statements to the same source radial coordinate e^B r. ∎

## 6. Formalization and computational record

The proofs use Lean 4 [3] with the source and dependencies fixed by the recorded environment. The theorem-to-declaration correspondence is given in Appendix A. The final declaration binds one F and one η, obtains a single radius from the conditional intermediate-value theorem, and passes that radius to the angular-positivity theorem. It does not combine separately chosen existential witnesses.

The recorded compilation at NSRW revision `3a50b5f50b034319a469b9de68f556be70fff02c` used Lean 4.34.0-rc2 and the source revision of Section 2. The 12 October 2026 record comprises a source-target build and fourteen fresh external modules. All fifteen stages exited zero with empty stderr. Nineteen reported axiom surfaces for the final local, source-facing and composition declarations contain `propext`, `Classical.choice` and `Quot.sound`, with no `sorryAx` [4,5]. A retained nonfatal stdout linter warning is documented in those records.

The formal compilation establishes the stated Lean propositions relative to the imported definitions and proof environment. The prose proof above explains their mathematical mechanism. The execution reused the pinned upstream cache; it was not a fresh rebuild of the entire upstream library. Execution and archive review were carried out within one operator trust domain. These facts describe the computational record, not an external peer-review process.

## 7. Interpretation and further questions

The result distinguishes terminal cancellation from intermediate behavior. M and J can both satisfy prescribed endpoint cancellation while having different signs or zeros inside a repair interval. The proof identifies the responsible structure: opposite-signed repair coefficients, separated supports and a strictly decreasing relative weight.

For a prospective real ratio Q=J/(M H), the point in Theorem 3.2 fails the condition M H≠0 regardless of H at that point. This is a domain obstruction. It does not supply a quotient limit, divergence rate or singularity classification. In particular, total real division in Lean should not be confused with a partial-domain ratio used in analysis.

The present theorem is existential. It does not compute ε_F or r. Stronger zero geometry calls for a derivative argument and localization inside the actual positive region of the first bump, rather than positivity throughout its larger declared window. In particular, the positive integral T₀ alone does not establish positive bump density at the witness. These observations identify a concrete route toward investigating monotonicity, uniqueness and crossing behavior; those statements are not added to the present formal result. The full zero set outside the positive parameter neighborhood is another open question.

## 8. Conclusion

In the fixed outgoing-profile construction, an interior mass cancellation is accompanied by strictly positive angular-weighted history whenever the second repair coefficient is positive. Moment comparison, coefficient continuity and boundary signs ensure that such a point exists for every sufficiently small positive parameter of each fixed source Profile. The proof exposes a concrete mechanism for non-simultaneous cancellation and connects that mechanism to exact source-facing formal propositions.

## Code availability and authorship

The formal input files and replay runner are identified by NSRW revision `3a50b5f50b034319a469b9de68f556be70fff02c` [2]. The two post-execution records [4,5] are separate documents; their text is not asserted to exist at the execution revision. The accompanying reproduction guide identifies the selected inputs and receipt snapshots supplied with the local distribution candidate. Original raw execution evidence is privately retained. No published download or artifact DOI is claimed here.

Yun Kwansub is the named human author. AI assistance was used in analysis, formal-code development and manuscript preparation. The source construction and imported formal mathematics are attributed to their source repositories and authors.

Copyright © 2026 Yun Kwansub. The authored manuscript text and its LaTeX representation are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). NSRW code and Lean proof files retain their MIT license; third-party material retains its own applicable terms. See [license scope](LICENSE-PAPERS.md).

## References

[1] OpenAI and repository contributors. *NavierStokesAndEuler*. Source revision `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, especially `OutgoingSchedule.lean`, `LocalizedMomentRepair.lean`, `OutgoingPulseBounds.lean` and `OutgoingProfile.lean`. [Fixed source](https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538).

[2] NSRW repository. *NavierStokes Research Workbench*: formal inputs and replay runner at revision `3a50b5f50b034319a469b9de68f556be70fff02c`. [Fixed repository](https://github.com/flamehaven01/NavierStokes-Research-Workbench/tree/3a50b5f50b034319a469b9de68f556be70fff02c).

[3] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language. In *Automated Deduction—CADE 28*, LNCS 12699, 2021. [doi:10.1007/978-3-030-79876-5_37](https://doi.org/10.1007/978-3-030-79876-5_37).

[4] NSRW. *P2 Z-core Colab execution receipt*, 12 October 2026. [Local document](../docs/stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md).

[5] NSRW. *P2 Z+J Colab execution receipt*, 12 October 2026. [Local document](../docs/stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md).

## Appendix A. Formal correspondence

Module filenames and local navigation are given below. All listed proof modules are also available under `formal/p2/` at the fixed execution revision [2].

| Mathematical statement | Lean declaration in `NSRW.P2` | Module |
|---|---|---|
| Local mass partial/tail identities | `localMass_partial_identity`, `localMass_tail_identity` | [P2_Z01_LocalMassIdentities.lean](../formal/p2/P2_Z01_LocalMassIdentities.lean) |
| Local angular partial/tail identities | `localAngularMoment_partial_identity`, `localAngularMoment_tail_identity` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| Strict support separation | `first_upper_lt_second_lower` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| Future mass balance | `firstRepair_mass_zero_tail_balance` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| T₀>0 and c₀<0 | `firstBumpTail_pos_and_firstCoeff_neg` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| Relative-weight inequalities | `firstBump_angularTail_lower`, `secondBump_angularTail_upper` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| Theorem 3.1 | `angularMoment_pos_of_firstRepair_mass_zero` | [P2_ZPLUS_J_FirstRepairAngularMoment.lean](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) |
| Coefficient positivity near zero | `actualSecondRepairCoefficient_pos_small_positive` | [P2_C04_SmallPositiveEta.lean](../formal/p2/P2_C04_SmallPositiveEta.lean) |
| Strict boundary signs | `localMass_lower_pos`, `localMass_upper_neg_of_secondCoeff_pos` | [P2_Z02_BoundaryMassSigns.lean](../formal/p2/P2_Z02_BoundaryMassSigns.lean) |
| Conditional interior mass zero | `exists_firstRepair_zero_of_secondCoeff_pos` | [P2_Z03_ConditionalInteriorZero.lean](../formal/p2/P2_Z03_ConditionalInteriorZero.lean) |
| Source mass coordinate bridge | `localMass_eq_profileM` | [P2_Z04_FirstRepairInteriorZero.lean](../formal/p2/P2_Z04_FirstRepairInteriorZero.lean) |
| Source angular coordinate bridge | `localAngularMoment_eq_profileJ` | [P2_ZPLUS_J_SourceComposition.lean](../formal/p2/P2_ZPLUS_J_SourceComposition.lean) |
| Theorem 3.2 | `profileMJ_firstRepair_zero_small_positive` | [P2_ZPLUS_J_SourceComposition.lean](../formal/p2/P2_ZPLUS_J_SourceComposition.lean) |

## Appendix B. Reproduction identity

| Item | Recorded identity |
|---|---|
| NSRW execution revision | `3a50b5f50b034319a469b9de68f556be70fff02c` |
| Upstream revision | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` |
| Dependency manifest Git blob | `f07a8454cb6200d90bcc4371bc9965e9f8f46c7d` |
| Lean | `4.34.0-rc2` |
| Replay runner | `scripts/run-p2-z-replay.py` |
| Reference execution | `nsrw-z-phase-replay-20261012T065216884451Z` |

The runner requires the pinned source environment and exact NSRW checkout. It does not install dependencies. A new execution will have its own logs, timings and generated artifact hashes. Detailed invocation and distributed-evidence information is in the [reproduction guide](REPRODUCE.md) and the two records [4,5].
