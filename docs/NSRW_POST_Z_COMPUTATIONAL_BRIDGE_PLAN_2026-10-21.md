# Post-Z+J research bridge: Certified First-Repair Moment Witness

Design date: 2026-10-21 (Asia/Bangkok).
Execution-design revision: P0-P4 priorities, 2026-10-21.
Current status, 2026-10-22: P1's ten exact-real margin/normalization propositions
are admitted by the [scoped receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md),
OE-2, after clean replay and direct archive review. P0 numerical admissibility
remains partial; P2-P4 computations/experiments have not been performed.
Approved route refinement: try a conditional source-family J lower bound using
amplitude bounds before constructing a full Profile evaluator; explicit-instance
and narrow numerical-bracket milestones remain separate.
Historical implementation observation, 2026-10-21: the separate P1 margin module
existed with static statement/input checks only. The development compiles,
commit-bound replay and 2026-10-22 admission described in section 7 supersede
that initial UNVERIFIED status for precisely the ten admitted propositions.
Decision: adopt this bounded research direction; implementation and experiments
are not started merely by this document. Claims outside the named P1 receipt
remain unverified. Existing Z-core/Z+J receipts retain their exact scopes.

## 1. Purpose and place in the program

**목표:** Z+J의 존재·부호 결과를, 명시적인 입력에서 재검사할 수 있는
moment witness certificate로 연결한다. 그 다음에만 현실 과제에서의 효용을
비교한다. 외부 자료는 수학과 구현의 재료이며, 프로젝트 우열의 기준이 아니다.

```text
admitted Z-core / Z+J and publication lineage
    -> mathematical reconstruction and quantitative bound
    -> admissible evaluable model + checked moment certificate
    -> bounded scaling/localization research
    -> selected-result reproduction and semantic review
    -> one task-specific comparative application experiment
```

This bridge belongs to NSRW research, before the application experiments in
the [application plan](Flamehaven-Applied-Scientific-Computing/APPLICATION_RESEARCH_PLAN.md).
It does not add an R/OE/TR axis, a new claim ledger, or a general verification
framework. The [roadmap](EQUATION_TO_ARTIFACT_VISION_ROADMAP.md) and
[transfer protocol](ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md) still govern
the meaning of application evidence. Deposit/publication is not peer review.

NSRW's candidate -> rejection -> refined M/J proposition -> Lean proof is an
observed research trajectory, not evidence of a general autonomous discovery
engine. External projects also conduct research; treating selected outputs as
inputs here does not reduce their contributions to mere raw material.

### First research question

Can one explicitly described admissible model, at one fixed positive eta,
produce a certified first-repair bracket containing an M-zero and a strictly
positive lower bound for J at that same zero?

The first, smaller milestone is now a quantitative bound for every source
Profile satisfying explicit parameter/amplitude conditions. It may be derived
without evaluating that Profile's reset function. This is a conditional-family
result, not a claim to have constructed a numerical Profile or located a root.

Success may be a source-bound certificate, a separately proved restricted-model
certificate, a counterexample to a proposed extension, or a precise missing
computability condition. A previously unreported result is a target, not an
assumption; literature novelty needs its own comparison.

## 2. Fixed mathematical starting point

The [Z+J receipt](stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md) admits both
conditional angular positivity and the same-witness small-positive-eta result.
Use the exact declarations in
[conditional Z+J](../formal/p2/P2_ZPLUS_J_FirstRepairAngularMoment.lean) and
[source composition](../formal/p2/P2_ZPLUS_J_SourceComposition.lean).
Their original execution checkpoint, receipts and bytes are not edited here.

For one fixed F and eta, put c = F.data.core, B = c.pulseStart,
R = exp(c.pulseLength), l_i = c.lower i, u_i = c.upper i,
a_i = c.exponents i, and b_i equal to the source repair bumps.
For l_0 < r < u_0, define

\[
T_i(r)=\int_r^R x^{a_0}b_i(x)\,dx,\qquad
S_i(r)=\int_r^R x^{a_1}b_i(x)\,dx.
\]

Here c_i are the actual **axial** repair coefficients, not the angular-reset
coefficients in F.reset. Write K_0 = momentScale(c,0) shape(eta) and
K_1 = momentScale(c,1) shape(eta)^2. The source-bound tail identities give

\[
M_{local}=-K_0(c_0T_0+c_1T_1),\qquad
J_{local}=-K_1(c_0S_0+c_1S_1).
\]

At an exact mass zero with c_1 > 0, the current argument gives T_0 > 0,
c_0 < 0 and the positive-gap comparison

\[
J_{local}(\eta,r)\ \ge
K_1 c_1 T_1(r)\bigl(u_0^{-\lambda}-l_1^{-\lambda}\bigr)>0.
\]

This displayed exact-real strengthening was subsequently compiled and admitted
on 2026-10-22 as `angularMoment_ge_firstRepair_margin`, together with
`secondBump_massTail_eq_full` identifying T_1(r) with its whole-line moment.
It is independent of the qualifying zero's location under the theorem's own
support, mass-zero and positive-c1 hypotheses. It is not a numerical J certificate.

The coordinate bridge is X = exp(B) r with 1 <= r. Local and source M/J use
the same F, eta and r; two unrelated witnesses are never combined.

## 3. Source-instance feasibility: inspect before implementing

Pinned OpenAI source: `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
Exact local material paths and paper versions are in the
local material index `NSRW_RESEARCH_MATERIALS_AI_INDEX_2026-10-15.md` and its
manifest. Those machine-local acquisition catalogs and downloaded originals are
Git-ignored, not required public replay inputs; the source identities below
identify the research materials without redistributing them.

The source's OutgoingProfile.Profile contains TailData, coefficientBound and
a ResetWitness. TailData includes the schedule Parameters and h with
0 < h and 2h < lambda. Parameters include P, m, lambda and wait with their
inequalities. These scalar checks are necessary, not sufficient.

UniformAngularReset.ResetWitness additionally requires a smooth coefficient
function, the angular-debt integral equality, the pressure integral equality,
uniform coefficient/eta-derivative bounds, and relative-profile small-jet bounds.
CorrectedPulseAmplitude.amplitude uses the **same** reset coefficients and
normalized reset energy. Do not substitute a main-only energy root or confuse
angular reset coefficients with the axial c_1 in Z+J.

The first feasibility audit must trace these fields through source formulas,
integrals, implicit/existential branches and any Classical.choose dependencies.
The keyword `noncomputable` alone is not evidence that no evaluator can exist.
Conversely, numerical samples do not prove global smoothness, an exact integral
identity, or a uniform-in-eta bound. Such fields need analytic proof and, where
appropriate, validated implicit solving or integral enclosures.

Keep three model labels distinct:

| Model class | Required connection | Permitted conclusion |
| --- | --- | --- |
| Source Profile instance | Exact construction or a proved extension to the full pinned Profile contract, with evaluator error bounds | A certificate for that source-bound F and declared eta |
| Restricted local repair model | Explicit functions and a separately justified local theorem; full Profile extension unresolved | A certificate for the restricted model, not a selected source witness |
| Manufactured/toy family | Fully specified test functions and hypotheses of its own | Algorithm/reference test only; no source-Profile admission |

An explicit Profile need not equal an upstream existentially selected witness:
the existing theorem quantifies over every Profile. Record which assertion is
actually proved. If only a restricted local model is feasible, report
`HELD[NO_ADMISSIBLE_SOURCE_EVALUATOR]` for the source lane and keep the restricted
lane separately named. This is not a claim of mathematical impossibility.

The awkronos analytic-axis evaluator is a reference for numerical construction
techniques, not a complete replacement for these fields. Its own documentation
identifies matching, corrections and localization as additional stages.

### Preliminary source dependency inventory

These are inspected definitions and remaining obligations, not a certificate of
computability. Source file names below are within the pinned NavierStokes tree.
Keep paper/Lean correspondence separate from equality between two formulas.

| Object | Exact source entry | Representation / first unresolved obligation |
| --- | --- | --- |
| Core data | OutgoingSchedule.Parameters | P, m, lambda, wait with elementary inequalities; retain input intervals/rationals |
| Windows and exponents | Parameters.lower, upper, exponents | Explicit exp/rational formulas; raw radial values can overflow |
| Bump and moment matrix | LocalizedMomentRepair.bump, matrix, coefficients | Explicit cutoff + integrals + matrix inverse; need integral enclosures and determinant separated from zero |
| Local tail geometry | NSRW repairBumpTail, weighted_future_integral_eq_two_tails | Finite support and two coefficient terms; no root search required to state the identities |
| Full second-bump moment | secondBumpWeightedMoment_pos; secondBump_massTail_eq_full | Positivity and the named tail/full-moment equality are compiled; the latter is admitted by the scoped P1 receipt |
| TailData itself | OutgoingTail.TailData | core and h with inequalities; no selected constant is a field |
| Selected tail constant | OutgoingTail.stepBound -> flattenLength -> flattenEnd/releaseStart | Classical.choose of a sigma derivative bound; trace whether the requested quantity still depends on it after source identities simplify the expression |
| Angular reset | UniformAngularReset.ResetWitness, exists_scheduled_reset | Smooth coefficient function and global equalities/bounds, with an existential branch; values sampled at one eta do not construct this witness |
| Corrected amplitude | CorrectedPulseAmplitude.amplitude, energyShift | Quadratic-root formula plus actual reset-energy integral; prove branch and radicand bounds, not just evaluate sqrt |
| Actual axial c_1 | OutgoingSchedule.debt -> LocalizedMomentRepair.coefficients | Prefix moments, main moments and the same corrected amplitude; angular reset coefficients are a different object |
| Histories | OutgoingProfile.Profile.M/J and source coordinate bridges | Real integrals; need rigorous enclosures of the represented functions, not only float operands |

For each unresolved entry, the P0 output must state: used by the local target
or only by full-Profile admission; analytic reduction if any; validated numerical
operation if any; and the first missing bound. Replacing stepBound by a convenient
number is not equality with the selected source constant. Such replacement needs
a parameterized proof/bridge or an explicitly different model.

### Approved first route: conditional source-family lower bound

Static readback on 2026-10-21 matched the source declarations below. No new Lean
compile, numerical evaluation or source-instance admission has occurred.

| Factor | Exact path | Computational separation |
| --- | --- | --- |
| K_1 | momentScale(c,1) * shape(eta)^2 | Core and eta only; no reset or stepBound |
| I_01 | actual_matrix_entry c 0 1 | Fixed radialTemplate moment and explicit positive exponential scale |
| Delta | Parameters.upper 0, lower 1 and lambda | Core only; use a validated stable exponential difference |
| C_prefix | affineCoefficients c 1 0 1 | Core prefix moments and repair matrix |
| C_main | affineCoefficients c 0 1 1 | Core main moments and repair matrix; positivity is the existing C01 proposition |
| Actual c_1 | C02 profile_secondRepairCoefficient_decomposition | Depends on A=F.amp eta; use the source bound only under all its hypotheses |
| Amplitude-bound precondition | combinedScale d K -> errorConstant P m | Contains selected tail constants; not automatically a computable core-only check |

With a_0=-(1/2+lambda), L=13/lambda, the existing source
OutgoingPulseBounds.actual_matrix_entry gives

\[
I_{01}=\operatorname{rowMoment}(a_0)
       e^{(1/2-\lambda)(L-1)}.
\]

rowMoment is the actual radialTemplate integral in the pinned source, not a new
numerical approximation. Prefer this existing template identity over reproving
a generic normalization solely to obtain I_01. A numerical enclosure of its
integral and positive scale representation is still required.

For a source Profile F, set d=F.data, c=d.core and K=F.coefficientBound.
To apply CorrectedPulseAmplitude.amplitude_spec to F.reset, require **all**:

- F.reset is the same ResetWitness d K as the Profile's actual amplitude uses;
- K > 0;
- c.lam <= 1/120 (with c.lam > 0 already supplied by Parameters);
- c.wait = 60 * log(1/c.lam), as an exact expression identity, not a float equality;
- combinedScale d K <= 1/1000;
- eta^2 <= 1.

The source then supplies 9/10 < A < 6/5. With p=eta(1+eta^2), C02 and
C_main > 0 imply the proposed coefficient lower bound

\[
q(c,\eta)=\tfrac9{10}C_{main}-|p|\,|C_{prefix}|,
\qquad c_1(F,\eta)>q(c,\eta).
\]

If a rigorous enclosure establishes q_lower > 0, the P1 quantitative theorem
would give J_local >= K_1 c_1 I_01 Delta > K_1 q I_01 Delta > 0 at every
admissible mass zero. This does not need an evaluated reset coefficient function.
To enclose q conservatively, use a positive lower enclosure for C_main and
upper enclosures for |p| and |C_prefix|, plus outward arithmetic. Use the same
core and eta throughout; a numerical witness for one factor cannot stand in
for an unrelated Profile.

**P0 dependency finding:** this shortcut does not remove every selected constant.
The definitions explicitly give

```text
combinedScale d K
  = (errorConstant P m + 36*K + 1) * lambda*(1+log(1/lambda))
errorConstant P m
  = 1 + prefixBoundConstant P m + correctionEnergyConstant P m
      + 2*OutgoingTail.flattenLength + 4*TailEnergyBounds.tailConstant
TailEnergyBounds.tailConstant
  = OutgoingTail.flattenLength + 30 + releaseConstant
OutgoingTail.flattenLength = 10*(stepBound+1)*log 2 + 1
OutgoingTail.stepBound = Classical.choose exists_sigma_derivative_bound
```

Thus K_1/I_01/Delta and the core affine coefficients can avoid stepBound,
while numerical discharge of this amplitude-spec hypothesis still needs a
justified bound on the source's selected constants and K. An explicit derivative
bound on sigma alone does **not** upper-bound the opaque selected stepBound.
Do not replace it by a convenient constant or invent a numerical reset K.
Possible future routes are an exact applicable source theorem, a proved estimate
for the actual constants, or a separately parameterized construction with its
own bridge. None has been established by this inspection.

The chosen first route is therefore a **conditional source-family bound**:
record hypotheses proved/evaluated separately from those still assumed. It is
a result scope within source mathematics, not a fourth manufactured model class.
It does not establish nonemptiness for a particular numerical parameter tuple.
To claim an explicit source-instance certificate, supply a matching Profile or
a nonemptiness/construction proof under those actual parameter values as well
as all relevant computation/error evidence. Full Profile reconstruction remains
held; failure of that reconstruction does not invalidate the conditional bound.

## 4. Minimum certificate experiment

The first certificate uses **one fixed eta**, not an interval of eta values and
not a numerical value for C04's existential epsilon. Directly enclosing actual
c_1(eta) above zero can supply the conditional theorem's coefficient hypothesis.
This does not require computing epsilon. The model must still satisfy the
relevant source/local hypotheses; the theorem for every sufficiently small eta
and a certificate for one evaluated eta are different results.

There are two sequential certificate targets, not interchangeable successes:

1. **Conditional-family margin:** certify core factors/q under the source
   hypotheses above, and use existing boundary-sign/continuity theorems on
   [l_0,u_0]. For eta > 0 and c_1 > 0, they imply a zero strictly inside the
   window; a root-independent J bound applies there. Carry every unresolved
   source assumption and any nonemptiness gap in the output.
2. **Explicit-instance/narrow-bracket certificate:** construct or justify an
   admissible instance and evaluate a,b strictly inside the window, with the
   numerical endpoint enclosures and error budgets below. This is the original
   computational witness target, not completed by target 1.

Target 1's boundary signs can be theorem-derived; do not report them as observed
numerical M evaluations. Its conditional bound does not require eta > 0, but
the proposed whole-window existence composition does. The amplitude-bound route
also needs eta^2 <= 1. These restrictions do not alter the older Z+J theorem.

### Certificate obligations

1. Identify model/version, exact input values or input intervals, source/proof
   references, coordinate chart, arithmetic backend/version and precision.
2. Establish l_0 < a < b < u_0, continuity on [a,b], and rigorous endpoint
   enclosures with lower(M(a)) > 0 and upper(M(b)) < 0.
3. Establish lower(c_1) > 0 and the required support/weight hypotheses.
4. Supply either lower(J([a,b])) > 0, or a certified positive margin applying
   to **every exact M-zero in [a,b]**, via the justified quantitative theorem.
5. Apply IVT to the exact function represented by the enclosures. Conclude
   existence of at least one shared M-zero/J-positive point in (a,b).
6. Recheck the model binding and mathematical/arithmetic evidence through a
   small verification path; reject missing fields, inconsistent bounds and drift.

Neither M(midpoint) approximately zero nor an interval M([a,b]) containing zero
proves existence. Opposite strict endpoint signs plus continuity do. No
uniqueness, first-zero, exact numeric root or pole follows from this certificate.
If exp(B) r is too large for the chosen arithmetic, retain a log/scaled chart
and its proved conversion; do not silently overflow or change the quantity.

### Proposed implementation surface, not existing modules

```text
profile_evaluator.py    -> bounded M/J/coefficient evaluations for one model
interval_certificate.py -> bracket + margin + explicit arithmetic obligations
verify_certificate.py   -> binding checks and rechecked interval/theorem evidence
```

Choose the final location after the source audit; reuse existing NSRW numerical
code where suitable. These names are not an already implemented "Math Kernel".
Use an established reviewed interval backend if available; do not build a new
general interval library or proof checker merely to fill this plan.

The verifier must not simply trust producer JSON or compare stored hashes. It
must recompute/validate the enclosures under the declared arithmetic assumptions
or check suitable mathematical certificates. State its trusted components.
A separate function/process under the same operator is not independent attestation.

Output must distinguish a valid certificate, violated input hypotheses, unresolved
admissibility, insufficient enclosure, unavailable arithmetic, and invocation
failure. A held calculation is not a counterexample to Z+J.

## 5. Error model, falsifiers and comparison

Account separately for input representation, coefficient/implicit-solve error,
quadrature and tail truncation, transcendental/rpow enclosure, finite arithmetic,
coordinate conversion, and any model approximation. Compose these through
interval propagation or a justified analytic bound, not an arbitrary tolerance.
An arithmetic envelope on sampled operands does not enclose unsampled integrals,
FFT errors or the continuum field. High precision is not certification by itself.

The inspected awkronos interval code is useful reference material, but its
declared operand/order/backend assumptions require review before reuse. Review
file-level licensing first; no wholesale dependency import is planned.

Minimum adversarial cases for the future experiment:

| Case | Expected behavior |
| --- | --- |
| Analytic manufactured family with known signs | Enclosures contain reference values; report its model class |
| Both endpoint signs equal, despite 0 in a broad interval enclosure | No existence certificate |
| c_1 interval meets zero, supports overlap/reverse, or a weight base is nonpositive | Refuse the affected theorem path |
| Near cancellation and insufficient precision | Refine within the fixed budget or report unresolved |
| NaN/infinity, coordinate overflow, missing quadrature/tail error | No certificate |
| Changed reset/model/eta or fabricated positive J margin | Reverification rejects binding/evidence mismatch |
| Well-conditioned ordinary case | No spurious invalidity report |

Compare ordinary quadrature, stable/compensated summation where relevant, and
the selected interval/reference method on the **same** cases and precision/cost
budgets. Extra correct digits alone are not the target: measure valid/invalid
output discrimination, enclosure width, false certificates, justified abstention,
runtime and memory. Compensated summation is only one baseline, not a replacement
for a quadrature error analysis. Keep separate development and held-out cases.

Before execution fix model instances, eta choices, precision schedule, tolerance,
reference justification, stopping rule and cost budget. Initial source feasibility
is limited to two focused implementation sessions after the mapping session;
if no complete source-admissibility route is found, stop that attempt and request
a restricted-model decision rather than extending the search indefinitely.
Backend-specific numeric limits are fixed after availability is inspected,
before reported results are viewed. No backend installation is authorized here.

### Stable coordinates and explicit scale separation

Raw r is a poor default arithmetic coordinate. Put L=13/lambda, z=r exp(-L)
and t=log(r)-L. Then the declared first-window z endpoints are exp(-63/20)
and exp(-57/20); the second-window endpoints are exp(-23/20) and exp(-17/20).
These are the **declared** windows, not a claim that the bump is positive
throughout them: its actual support lies in the middle half in radial x.

The exact gap identity, admitted as `firstRepair_weightGap_exp_eq`, is

\[
\Delta=u_0^{-\lambda}-l_1^{-\lambda}
=e^{-13+23\lambda/20}\bigl(e^{17\lambda/10}-1\bigr).
\]

An equivalent candidate is
Delta = exp(-13+57*lambda/20) * (1-exp(-17*lambda/10)), evaluated numerically
with a validated negative-expm1 enclosure when available. Both formulas refer
to the same exact gap; neither ordinary floating-point expression is certified
merely by being algebraically equivalent.

The exact-real identity does not validate its numerical implementation. A validated
expm1 operation, or a justified series/remainder enclosure, can avoid subtracting
two nearly equal exponentials. An ordinary libm expm1 result is not automatically
a rigorous interval. Keep lambda bounded strictly away from zero in each input
enclosure, without inventing a global lower lambda assumption for the theorem.

With ell=exp(-23/20), v=exp(-17/20), a_0=-(1/2+lambda), the second bump also has
the normalization admitted by the P1 receipt

\[
I_{01}=e^{L(a_0+1)}\mu_{01},\qquad
\mu_{01}=\int_{\ell}^{v} z^{a_0}
 \operatorname{cutoff}\!\left(\frac{z-(\ell+v)/2}{(v-\ell)/4}\right)dz.
\]

This requires support localization and change of variables, not a change from
the source bump to a different log-space bump. Scale matrix rows and debts
consistently before solving for coefficients. Certify the normalized determinant;
do not infer numerical conditioning from the exact invertibility theorem.

Keep positive scale factors outside computed integrals. If physical X or the
J lower bound cannot be represented as a finite ordinary float, retain a checked
mantissa/exponent or logarithmic bound together with the exact positive conversion.
Sign preservation is then a real mathematical assertion about the original J,
not permission to return zero, infinity or an unexplained normalized number.

## 6. Scaling first; full localization is a separate research question

Start with an abstract one-dimensional check, not the full PDE insertion.
For b, A, C > 0 and fixed eta, define U_tilde(X)=A U(X/b),
H_tilde(X)=C H(X/b), with integrability on the relevant intervals. Then target

\[
\widetilde M(bX)=Ab\,M(X),\qquad
\widetilde J(bX)=ACb\,J(X).
\]

These are proposed change-of-variable lemmas for the defined histories.
They preserve zero/sign and ordered supports, but do not prove that the
transformed pair is a source Profile or a Navier-Stokes solution. A genuine
PDE rescaling additionally needs the time/eta transformation, cylindrical and
local/global radial maps, field-amplitude factors and domain boundary choices.

For blowup_density, inspect only ParabolicScaling.parabolic_residual and the
LocalizedInsertion correction/background-removal identities at
`af963994418ae32ff16e00a942bf532410928b09` first. Pin the paper separately at
arXiv `2609.10262v4`. They do not themselves state transformation rules for
NSRW's Profile.M/Profile.J. Insertion operates on spacetime velocity/pressure;
our histories are derived profile objects. Matching these carriers is an open
obligation, not an automatic adapter.

For a cutoff chi, even the scalar identity

\[
\int_0^X \chi(s)U(s)\,ds
=M(X)+\int_0^X(\chi(s)-1)U(s)\,ds
\]

shows why support ordering alone does not preserve a cumulative mass zero.
A vector-potential cutoff introduces derivative terms as well. The candidate
must either prove exact preservation, bound all new terms, or exhibit failure.

A robust alternative is to retain strict endpoint margins m_a,m_b and a J
margin j_0 valid on the necessary set of exact roots. Prove perturbations are
smaller than those margins, preserve continuity and the required domain, and
recover existence/J positivity. A J bound only at the old witness is insufficient
to control a moved root. Near-touching supports and localized cross terms are
falsifiers. A verified non-preservation example is a useful research output.

The s < 1/2 iff classification is not an M/J preservation theorem. Any use of
it must retain its exact paper version, domain, relative force space, time norm
and zero-initial-data restriction for the iff; do not promote it to all forces,
fixed-force dynamics, or unforced global regularity.

## 7. P0-P4 execution proposal and AI checklist

P0-P4 are local work priorities, not manuscript versions, the historical P2
proof stages, or a new maturity axis. This section supersedes the earlier
BR-only work ordering without changing the mathematical scope. All execution
boxes remain unchecked. Selected-result review accompanies every priority.

| Priority | One principal output | Existing work mapping | Exit decision |
| --- | --- | --- | --- |
| P0 | Source computability map + conditional-family contract first | BR-01 | All amplitude hypotheses tracked, including hidden selected constants; instance route separately decided |
| P1 | Named root-independent quantitative J-margin theorem | BR-01 + proof portion of BR-04 | Development compile of the stated theorem, not automatic claim admission |
| P2 | Core-factor/q enclosure first; full evaluator only if justified | Evaluator portion of BR-02 | Complete error contract and explicit unresolved source assumptions |
| P3 | Conditional-family certificate, then explicit-instance bracket | Certificate portion of BR-02 + BR-04 | Exact certificate scope and valid margin/sign evidence; no family-to-instance promotion |
| P4 | One bounded preservation or practical-use experiment | BR-03 / BR-05 + separate review | Scoped theorem/counterexample or measured utility; no automatic deployment |

Critical path: P0 -> P1 -> P2 -> P3. A restricted-model result also needs a
theorem applicable to that model; the Profile-typed P1 theorem alone does not
cover arbitrary explicit functions. The full gluing branch is not a prerequisite
for a meaningful P3 result. P4 contains separately selected follow-ons, not an
instruction to implement both at once.

### P0 — Resolve the first real computability obstacle

**Input:** pinned source, current Z+J modules/receipt, the source inventory in
section 3, and the fixed-version Lei-Ren exposition. No external scripts run.

Completed static subchecks, 2026-10-21 (not completion of P0):

- [x] Match actual_matrix_entry, C02 decomposition and amplitude_spec to the
      proposed I_01 and coefficient-bound formulas, including eta^2 <= 1.
- [x] Trace combinedScale -> errorConstant -> flattenLength -> selected
      stepBound and retain this hypothesis as unresolved for numerical admission.

- [ ] P0-01: complete each source inventory row with formula/dependency, needed
      hypothesis, proposed analytic reduction and exact unresolved bound. Separate
      local M/J use from full-Profile construction requirements.
- [ ] P0-02: compare first-repair/moment definitions with Lei-Ren locators;
      record a conversion or a difference, not assumed equivalence of expositions.
- [ ] P0-03: trace stepBound and reset-energy dependence to the actual requested
      value. Decide if a source identity removes it. Do not replace a chosen
      constant/function without proving the relevant bridge.
- [ ] P0-04: fix the P1 statement, I_01 integral, c_1 alias, prefactors and
      coordinate convention; verify dimensions/normalization against the source.
- [ ] P0-05: finalize the selected conditional source-family contract and its
      assumptions/nonemptiness boundary. Keep explicit Source / Restricted / Toy
      instance decisions separate. For a restricted model list exactly which
      theorem assumptions it can establish. Do not mix outcomes.
- [ ] P0-06: inspect available approved arithmetic dependencies read-only; fix
      one development input, one held-out input, eta, precision schedule, error
      target, time/memory limits and reference method before reported computation.

**Output:** one completed table and a model contract in this plan's task trail,
not a new ledger. Initial source feasibility stops at the two-session limit
in section 5; a specific obstruction is an acceptable finding, not source success.
Keep source admission held until all its obligations are justified.

### P1 — Extract the quantitative theorem without rewriting Z+J

**Development file:**
[P2_ZPLUS_J_QuantitativeMargin.lean](../formal/p2/P2_ZPLUS_J_QuantitativeMargin.lean).
The four declarations below are implemented as uncompiled development source,
not compiled claims. No amplitude-bound corollary or numerical evaluator is added.

1. `secondBump_massTail_eq_full`: expose the arbitrary-r equality currently
   proved locally inside secondBump_massTail_pos. Use the existing support
   localization pattern; do not edit the historical theorem to export its local fact.
2. `firstRepair_weightGap_pos`: name Delta > 0 using strict u_0 < l_1,
   lambda > 0 and positive bases.
3. `angularMoment_ge_firstRepair_margin`: for the **same F, eta, r**, assume
   l_0 < r < u_0, localMass F eta r = 0 and c_1(F,eta) > 0; conclude
   K_1 c_1 I_01 Delta <= localAngularMoment F eta r.
4. `firstRepair_margin_pos`: under the relevant coefficient and source
   positivity assumptions, prove 0 < K_1 c_1 I_01 Delta.

No eta > 0, C04 epsilon, uniqueness, root search or full source-composition
theorem is needed for this conditional margin. Stop the current proof's weighted
sum comparison before its final strict-negativity step, then multiply by the
negative tail prefactor with the correct reversed inequality. Every member of
the margin must remain tied to the same model/input.

The later proposed source-facing wrapper
`firstRepair_angularMoment_quantitative_lower` states the same inequality for
Profile.J at exp(B)*r, with Profile.M=0 and the matching actual c_1>0.
A separate amplitude-bound coefficient corollary may consume C02 and C01 plus
all amplitude_spec assumptions. Those imports bring their real transitive proof
dependencies; do not mislabel that enriched corollary as the minimal conditional
Z-only chain below. Its additional hypotheses are not added to the original theorem.

For a restricted-model route, a small algebraic lemma can isolate the needed
core: K_1 > 0, c_1 > 0, T_1 > 0, T_0 >= 0, c_0 T_0+c_1 T_1=0,
alpha > beta, S_0 >= alpha T_0 and S_1 <= beta T_1 imply
K_1 c_1 T_1(alpha-beta) <= -K_1(c_0 S_0+c_1 S_1).
The balance forces T_0 > 0 and c_0 < 0. Instantiating this lemma still requires
proof that the chosen exact functions satisfy the tail identities and weighted
inequalities. It does not make an arbitrary sampled function a Profile.

The minimal fresh compile route, after separate execution scope is established:

```text
pinned source +NavierStokes.OutgoingProfile
    -> fresh Z01 -> fresh Z02 -> fresh conditional Z+J -> fresh margin module
```

Do not pull F1/L2/L3/D/C01/C02/C03/C04 into this conditional proof. A later
source-facing corollary or small-eta composition may add only the imports it
actually consumes. Keep old proof/receipt bytes unchanged. Development success
is not commit-bound admission; checkpoint/replay and claim review remain separate.

- [x] P1-01: implement only these four helpers/bounds; static statement review
      preserves the same F/eta/r, exact mass zero and actual axial c_1 hypothesis.
- [x] P1-02: fresh compile, exact axiom inspection and unchanged dependency inputs;
      record failure logs as well as success. Do not weaken assumptions to pass.
- [x] P1-03: review the positive product and root independence; implement and
      development-compile exact stable-gap/normalized-integral/plateau links
      separately, preserving the original quantitative proof. Numerical
      enclosures and q remain P2 work, not part of this completion.

**Exit:** a development-compiled quantitative theorem and exact dependency list,
or an identified proof obstacle. Literature novelty remains a separate question.

Implementation/execution observation (updated 2026-10-22, Asia/Bangkok):

```text
proof raw SHA-256 (local executor bytes):
  7a504d7c9cde6d76f2d0e826572fbbebeae905166802adc3e7b0d9b844e534b6
check_status: PASS[STATIC:FOUR_DECLARATIONS_SINGLE_IMPORT_NO_PLACEHOLDERS]
existing Z01/Z02/conditional-Z+J/source-composition hashes: unchanged, 4/4
pinned source HEAD / manifest Git blob: matched; source tracked tree clean
Lean compile: PASS[LOCAL_PROOF_COMPILE:P2_ZPLUS_J_QUANTITATIVE_MARGIN]
observed #check / #print axioms: four statements; exact standard three axioms each
source -> fresh Z01 -> fresh Z02 -> fresh conditional Z+J -> fresh margin: exit 0
five compile-stage stderr streams: empty; sorryAx: absent
source/dependency identity and source-target olean: unchanged pre/post
archive preservation: PASS[DRIVE_ARCHIVE_CROSSCHECK:P1_QUANTITATIVE_MARGIN]
Colab-only pinned restoration completed; Windows installation: NONE
claim_authority: NONE
claim_status: UNVERIFIED
```

See the [development and preservation record](../colab/P1_QUANTITATIVE_MARGIN_DEVELOPMENT_2026-10-22.md)
for the exact run, six input hashes, four fresh artifacts, source pins, archive
SHA and private Drive destination. The original empty VM was restored following
explicit approval. Browser transport failures were overcome without changing
proof bytes. No Lean retry or proof repair was needed for this run.

The positive product and chosen-root independence were checked against actual
compiler statements. P1-03 subsequently completed as a separate module,
[MarginNormalization](../formal/p2/P2_ZPLUS_J_MarginNormalization.lean), raw SHA-256
`058ad35fca4228ea29773cef7c118dce7414745451f7f20361ca159d9a68ab8b`.
It compiles the exact Delta identity, whole-line/interval normalized moment
equality, its scaling and rowMoment identities, the conservative cutoff plateau
bound `(v-ell)/4 <= mu01`, and the resulting conditional J lower bound.
The successful separate fresh chain has six zero-exit/empty-stderr stages,
five fresh artifacts and six standard-three-axiom outputs without sorryAx or
warnings. A prior failed attempt and the successful retry were both preserved
and reviewed in private Drive; see the
[P1-03 execution record](../colab/P1_MARGIN_NORMALIZATION_DEVELOPMENT_2026-10-22.md).
The original quantitative proof and its earlier execution ZIP were not changed.
The exponential identities are exact-real statements, not an interval expm1
implementation. P0 numerical admissibility and P2/P3 are not closed.
Following explicit approval, proof-only commit
`fba27381bcfda3af6f03e2fbae82f6db016ca534` and execution commit
`7f29ebf0e2b894bf598144628230ae09df436c3d` were separately pushed. One new
clean checkout replay at the latter SHA passed all six stages, ten named
statement/axiom checks, seven exact committed inputs and five fresh artifacts.
The private Drive archive was reopened and internally rechecked using separate
code in the same trust domain. See the
[commit-bound execution record](../colab/P1_MARGIN_COMMIT_BOUND_REPLAY_2026-10-22.md).

- [x] P1-04: exact proof / minimal execution checkpoints, push, one clean replay,
      private archive preservation and scoped execution-evidence review.
- [x] P1-05: dated receipt review/admission of the ten named propositions only,
      accepted 2026-10-22 in the same operator/trust domain, OE-2. See the
      [scoped receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md).
      The original private ZIP was fetched through the Drive API and rechecked
      on D: against its original SHA, exact input Git bytes, log/artifact hashes
      and ten statement/axiom outputs. A new Colab review attempt with no observed
      result is not credited. The dependency linter warning is retained/disclosed.
      Replay metadata remains claim_authority NONE / claim_status UNVERIFIED;
      separate receipt/atomic ledger entries admit only the ten named scopes.

Next is the unresolved P0 admissibility/model/input decision and the smallest
rigorous P2 computation contract, not another replay or a full Profile evaluator.
Development, replay execution, archive review and claim admission remain
distinct. P1 formal admission is complete; no independent attestation, numerical
q certificate or numerical admissibility is asserted. P2 execution is not started.

### P2 — Build a small evaluator, not a solver platform

**Proposed surface:** `profile_evaluator.py` plus focused tests, at a location
chosen after inspecting existing NSRW numerical code. Do not create stub files
to represent progress. Source and restricted evaluators expose different model IDs.

First implement only template integrals, K_1, Delta, C_main/C_prefix and q for
the conditional-family route if justified arithmetic is available. Do not make
a full reset/Profile evaluator a prerequisite for symbolic margin extraction.
If combinedScale or witness existence cannot be discharged, return a conditional
result with those assumptions open, not a source-instance certificate. The
full-evaluator tasks below remain later work unless a concrete route is established.

- [ ] P2-01: implement the z/t chart, exact positive scale factors and their
      conversion obligations. Use the source radial bump, not a different bump
      defined by convenience in log coordinates.
- [ ] P2-02: enclose normalized bump moments and main/prefix moments needed by
      the chosen model. Include truncation/quadrature error, not just rounding.
- [ ] P2-03: solve the row-normalized 2x2 repair system with an interval
      determinant away from zero and a residual/error enclosure. Use actual debt
      and corrected amplitude for source mode; explicit alternative inputs must
      carry the restricted-model label and theorem.
- [ ] P2-04: return M/J enclosures, c_1, K_1, I_01 and Delta in a common chart,
      with separated error contributions and finite checked scale representation.
- [ ] P2-05: test known-reference manufactured cases, input intervals touching
      forbidden boundaries, matrix near-singularity, cancellation and overflow.

**Exit:** callable bounded evaluations for one chosen input family. Finite scalar
output and higher precision alone are insufficient. The method is held if its
backend cannot justify transcendental, integration or implicit-solve enclosures.
The full global ResetWitness is not inferred from numerical tests.
Enclose the coefficients of the exact defined repair system. Silently treating
rounded approximate coefficients as its exact solution loses the cancellation
identity; either bound the exact solution or rederive the changed-model identities.

### P3 — Certify a common-point witness and recheck it

**Proposed surface:** `interval_certificate.py`, `verify_certificate.py` and
focused adversarial tests. Reuse the P1 mathematical bound, continuity and IVT.

The first record must distinguish conditional-family margin from explicit-instance
and numerical localization. For the first kind, [l_0,u_0] with theorem-derived
strict signs is allowed. Narrow-bracket search, observed endpoint evaluations
and explicit-instance success below must not be marked complete on that basis.

- [ ] P3-01: search only inside the declared first window, in the chosen chart.
      Refine endpoint evaluations/brackets within the fixed budget; uniqueness
      is not needed for bisection of a continuous sign-changing bracket.
- [ ] P3-02: require strict endpoint M signs, c_1 lower bound > 0 and a rigorous
      root-applicable J lower bound > 0. A zero-containing M range is insufficient.
- [ ] P3-03: emit the minimum record: model/input identities and class, chart,
      bracket, continuity justification, endpoint enclosures, coefficient/moment/
      gap bounds, error budgets, precision/backend identity, theorem references,
      checked scale conversion and explicit failure reason when not certified.
- [ ] P3-04: make the verifier recompute/check the bound evidence and input
      binding without calling the certificate producer to obtain its verdict.
      Share only reviewed arithmetic primitives; disclose shared trusted code
      and operator. Hash matching alone is not mathematical verification.
- [ ] P3-05: obtain one development and one held-out valid certificate for the
      chosen model class; reject fabricated margin, changed eta/reset, same-sign
      endpoints, missing continuity/error evidence and a singular matrix interval.

**Proposed initial execution limits:** at most three predeclared precision
levels, 40 bracket bisections per level and 4096 quadrature subdivisions per
integral. Before running, freeze actual backend-supported precision values and
wall-time/memory limits in P0's contract. Reaching a limit produces a held result,
not weaker acceptance or automatic unlimited refinement. These are proposed
resource limits, not measured feasibility or a convergence guarantee.

**Exit:** at least the two declared valid examples and all required rejection
controls pass, with zero false certificates on that declared test set. This
does not establish a population-wide false-positive rate. An exact/analytic or
rigorously enclosed reference is needed; arbitrary high-precision digits do not
suffice. Private run preservation follows section 8. Independent reproduction
must actually be performed before reporting it, even with a separate verifier.

### P4 — Select a bounded extension or practical-use experiment

**P4-A: mathematical preservation.** Prove the positive-dilation formulas in
section 6. Only then select one actual blowup_density insertion/cutoff operation
and map its carriers, support changes and derivative/cross terms. Produce a
preservation/perturbation theorem, counterexample or exact unresolved prerequisite.
Keep the source's forced/domain/topology restrictions. Failure to preserve M/J
does not invalidate P1/P3. Do not require the entire density theorem as an import.

**P4-B: practical comparison.** Select one weighted-moment/flux postprocessing
or denominator-admissibility task with observable inputs. Compare ordinary
quadrature, stable summation and a justified validated baseline under equal
precision/cost budgets. Use held-out regular, near-cancellation and invalid-domain
cases. Predeclare useful output/error criteria, false-certification checks,
runtime/memory overhead allowance and a stopping rule. A source certificate is
not evidence of benefit for a different physical model.

- [ ] P4-01: select A or B explicitly; do not launch both by default. Full PDE
      gluing need not precede an independently justified bounded diagnostic trial.
- [ ] P4-02: review the selected mathematical mapping, licenses and assumptions;
      apply existing transfer requirements for B, including domain review or held
      status. No new maturity taxonomy or automatic production control is added.
- [ ] P4-03: perform the bounded experiment and retain negative results. Stop
      if mapping fails, the signal duplicates existing methods, or cost exceeds
      the predeclared budget. A negative result is a research output, not utility.
- [ ] P4-04: seek separate human semantic review/reproduction for the actual
      surviving result. Tenet is optional after compatibility/cost inspection;
      it does not substitute for either review. Lack of a reviewer limits the
      claim/transfer admission, not the ability to conduct local development.

**Exit:** a scoped extension result or demonstrated benefit on one named task.
First user-facing output is an offline checkable diagnostic, not a general CFD,
weather, singularity-prediction or autonomous mesh-control product. Further domain
integration/deployment requires its own evidence and authority.

## 8. Working boundaries and immediate next task

Future local Python uses the configured D: venv; approved Lean experiments use
the pinned Colab environment. Follow [Colab storage practice](../colab/README.md):
execute in /content, preserve success/failure archives primarily to private Drive,
reopen/hash the saved copy, keep small records under colab/, and use D: only for
needed checks/backups. No C: or Temp staging; no automatic raw-evidence Git commit.

Existing source snapshots remain ignored references. Review licenses before
copying code and preserve attribution. No installs, third-party script execution,
new Colab run, commit/push/release or publication occurs through adopting this plan.

**Next task is the remaining P0 contract, not three empty Python modules:**
finish the source correspondence and amplitude-hypothesis discharge analysis
for the selected conditional-family bound. The newly traced combinedScale
dependency prevents declaring a numerical source instance ready. P1's exact
conditional margin/normalization is already admitted without a full evaluator;
numerical q, explicit-instance and narrow-bracket claims remain separate.
Record its result in the existing task trail. Create code only after that choice.
Do not add more downloaded repositories, more proof-checking infrastructure or a
new paper quota to demonstrate progress. The deliverable is a mathematically
meaningful computation, or an equally precise result explaining why it fails.
