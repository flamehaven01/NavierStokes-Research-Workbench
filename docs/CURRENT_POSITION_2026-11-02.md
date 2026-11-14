# NSRW: current position and next research work

Reviewed: 2 November 2026, Asia/Bangkok. Repository inspected at
`a7e7c14ac48b775c1e020805ab342f36a8a199cc`.

Rechecked: **12 November 2026**, at
`90f7091251d98063e91c458cd72e8a0f5d9eaf20`. The original snapshot date and
mathematical evidence below are retained. Section 9 records the new code check
and route refinement; the bridge plan's section 7 owns the detailed P0-P4 tasks.

## 1. Position relative to the research direction

**NSRW has established source-bound mathematical results, formalized their
qualitative and quantitative statements, and implemented checked numerical
building blocks. The active frontier is coefficient enclosure, before a
numerical moment certificate and measured scientific use.**

The destination is justified mathematics that can become useful scientific
computation. A theorem is an important result; a publication or website makes
it accessible. The next research advance must supply another mathematical or
computational capability, rather than another presentation layer.

## 2. What has been achieved

| Work | Current result | Primary evidence |
| --- | --- | --- |
| Source-derived investigation | Rejected the study's endpoint-first-zero candidate and redirected the question toward repair-window geometry | [P2 study](M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md); this particular terminal-plateau analysis is not a separately admitted Lean theorem |
| Qualitative mathematical chain | Each fixed Profile admits, for every sufficiently small positive parameter, a first-window point with source M = 0 and J > 0 at that same point | [Z-core receipt](stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md), [Z+J receipt](stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md); execution `3a50b5f50b034319a469b9de68f556be70fff02c` |
| Quantitative extension | A positive local J margin independent of the selected qualifying zero; normalized moment identities and a plateau lower bound | [P1 receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md): ten named propositions; execution `7f29ebf0e2b894bf598144628230ae09df436c3d` |
| Numerical core | Exact-rational enclosures for ell, v, plateau width w, gap G and denominator D at 128/256/512 fractional bits | [Method](P2_CORE_SCALAR_METHOD_2026-10-31.md), [retained records](../examples/p2-core-scalars/) |
| Second arithmetic path | Fifteen full interval containments using mpmath interval arithmetic and direct exponential differences | [Checker](../scripts/check-core-scalars-mpmath.py), [retained cross-check](../examples/p2-core-scalars/mpmath-crosscheck.json), [EQA 0061](https://flamehaven01.github.io/Flamehaven-Verification-Ledger/eqa.html#toe-test-0061) |
| Public research artifacts | Software v0.5.0; P01 v0.5 mathematics and P02 v0.6 research software; research library, reproduction guides and linked EQA record | [Software release](https://github.com/flamehaven01/NavierStokes-Research-Workbench/releases/tag/v0.5.0), [P01](https://doi.org/10.5281/zenodo.23835054), [P02](https://doi.org/10.5281/zenodo.23835112), [website](https://flamehaven01.github.io/NavierStokes-Research-Workbench/) |

The theorem receipts remain scoped to their named statements and same operator
trust domain. The second numerical backend is a different arithmetic path, not
a separately operated reproduction. These distinctions identify what was done;
they do not diminish the mathematical derivation or the computed bounds.

## 3. The present bottleneck

The scalar prototype does not yet evaluate normalized main/prefix moment
integrals or the affine coefficients. Its positive-ratio helper does not
construct the missing numerator enclosure. In particular, a positive D interval
does not by itself give a numerical positive lower bound for C_main.

The next intended bound, for the already selected core and eta, is

```text
p = eta * (1 + eta^2)
q_lower = (9/10) * lower(C_main)
          - upper(abs(p)) * upper(abs(C_prefix))
```

Here C_main and C_prefix are the source affine coefficients, not fitted or
rounded replacements. The [fixed input/error contract](NSRW_P2_FIRST_INPUT_AND_ERROR_CONTRACT_2026-10-28.md)
retains lambda = 10^-12 and eta = 2^-20.

Two distinct uncertainties remain:

1. **Computational:** bound the actual affine coefficients using explicit
   analytic inequalities and, where needed, normalized integral enclosures;
   propagate every error to q.
2. **Source admissibility:** connect the amplitude estimate to the same Profile,
   ResetWitness and K; retain the actual combinedScale/selected-constant
   hypotheses. This is not resolved by a successful core computation.

Computing the core-dependent q bound can proceed with those source hypotheses
explicitly conditional. Applying it to actual c1 requires their justification.
An explicit source instance and a numerical mass bracket are further outputs.

## 4. Existing P0–P4 priorities, reassessed

These identifiers retain the computational bridge's existing meaning; they are
not paper numbers or a new maturity system.

| Priority | Current position | Next exit condition |
| --- | --- | --- |
| P0 — source/model contract | PARTIAL. Conditional-family route and first input fixed; source-instance hypotheses remain open | State exactly what the coefficient computation depends on and what is still conditional; decide the instance route separately |
| P1 — quantitative mathematics | COMPLETE for the ten admitted propositions | Preserve the proof inputs and receipts; no repeat implementation or replay is needed for this reassessment |
| P2 — bounded evaluator | PARTIAL. Core scalars and two arithmetic paths implemented; coefficient bounds are next | Justified lower C_main, upper abs(C_prefix) and q bounds at the fixed input, or a specific unresolved outcome |
| P3 — moment certificate | NOT STARTED | First a conditional-family margin with explicit hypotheses; an explicit-instance same-zero certificate additionally needs admissibility, continuity and strict bracket signs |
| P4 — bounded extension or scientific use | PLANNED; practical branch B recommended, preservation branch A deferred | One selected extension result or diagnostic with a baseline, fixed workload and measured utility |

Publications and the website are now supporting assets, not the next research
blocker. P03 remains deferred. External localization/gluing mechanisms are
subsequent research materials, not prerequisites for the current coefficient task.

## 5. Next work: finish the coefficient calculation before a full evaluator

### P2-02A — fix the actual integrands and normalizations

- [ ] Map `rowMoment`, `normalizedMainMoment`, `prefixCoefficient` and
  `affineCoefficients` to the exact integrals needed for the selected core.
- [ ] Bind the actual Mathlib cutoff used by the source bump. If pointwise
  evaluation or quadrature is needed, implement that function; do not replace
  it with another smooth function with similar support.
- [ ] Factor large positive scales analytically. Keep fixed normalized charts
  and the same source exponent/row/debt conventions throughout.
- [ ] Distinguish actual integrands from constants used in bounds. For example,
  `OutgoingPulseBounds.mainBound` is selected by `Classical.choose`; do not
  assign it a numerical value. Enclosing the actual main-pulse integral or
  proving a separate explicit bound can avoid depending on that selected
  bound, without asserting a value for it.

**Deliverable:** one coefficient-computation specification with exact source
locators, integrands, scaling identities and required assumptions. Extend the
existing input/error contract; no empty evaluator modules or generic framework.

### P2-02B — justify integral enclosure

- [ ] First check whether computable conservative analytic bounds close the
  coefficient target. Use justified quadrature only where those bounds do not
  suffice; include the plateau/transition boundaries of the actual cutoff.
- [ ] Supply an inclusion/error justification over the integration intervals.
  A pointwise exp checker, high precision, or an adaptive quadrature error
  estimate alone does not establish that justification.
- [ ] Retain the contract's 128 → 256 → 512 schedule, at most 2048 integration
  subintervals and 120 seconds per precision attempt. A changed budget or input
  is a new identified experiment, not a silent retry policy.

### P2-02C / P2-03 — compute the moments, coefficients and q

- [ ] Implement only the coefficient bounds required by the analytic-first
  route, adding normalized moment enclosures where needed.
- [ ] Require a determinant/denominator interval separated from zero; preserve
  exact solution semantics rather than substituting approximate coefficients.
- [ ] For a positive ratio N/D use lower(N)/upper(D), rounded downward. Obtain
  upper abs(C_prefix) from a proved absolute bound or its full signed interval.
  A scaled q bound must retain its exact positive conversion factor.
- [ ] Retain one result with actual bounds, precision, input identity and error
  contributions. Either q_lower > 0 succeeds or the remaining uncertainty is
  identified precisely.

If q's enclosure straddles zero, the sign is unresolved at that budget. If the
conservative q bound is nonpositive, that does not prove the actual coefficient
negative or refute C04. Keep the fixed input; consider a different eta only in a
separately specified follow-up.

### P0-03 in parallel — discharge only the source assumptions actually needed

- [ ] Track K, the matching reset and combinedScale for the chosen family.
- [ ] Resolve the selected `stepBound` dependency, or prove an applicable
  parameterized/source-identity bridge. A convenient derivative bound is not
  automatically a bound on a `Classical.choose` value.
- [ ] If these remain unresolved, retain a conditional-family computation;
  do not describe it as an explicit source Profile.

This investigation must not prevent the independent core-dependent coefficient
calculation from producing its own well-defined result.

## 6. What follows a positive q result

1. Combine q, the normalized plateau factor and the positive weight gap into a
   rigorously bounded **conditional local-J margin**, preserving scale factors.
2. Check the amplitude-to-coefficient inference against C02 and the source
   amplitude hypotheses. Any new Lean corollary receives its own verification.
3. Complete the quantitative local-to-Profile.J bridge before making a named
   source-J numerical claim. The older source-J positivity theorem is not that
   new quantitative wrapper.
4. For an explicit-instance witness, additionally construct an admissible
   evaluable model and establish strict opposite mass signs on a bracket,
   continuity, and a J bound applicable to the same exact zero.

A conditional-family margin can be useful before a narrow root bracket exists.
A restricted explicit model is a separate option requiring the theorem to be
shown applicable to that model; it is not an implicit source substitution.

## 7. Practical destination and first selected use

The closest current transfer candidate is **cancellation/denominator diagnostics
for scientific moment postprocessing**. It asks whether software can distinguish
usable ratios, certified cancellation and unresolved near-cancellation on real
inputs, while exposing error bounds.

After the coefficient milestone, select one controlled workload of explicit
weighted sums or integrals. Compare against stable summation, existing interval
evaluation and ordinary conditioning checks at a comparable cost. Measure
reference error, usable-bound width, invalid-ratio acceptance, unnecessary
rejections and runtime. A controlled benchmark precedes claims of practical
benefit in a named scientific workflow.

This explicit-model experiment need not wait for a full source Profile, but its
mathematics and model class must be identified separately. It must demonstrate
value beyond standard methods. See the existing
[application plan](Flamehaven-Applied-Scientific-Computing/APPLICATION_RESEARCH_PLAN.md).

General CFD, turbulence/forecasting claims, mesh control, uniqueness/simple
zeros, ratio poles, broad new-repository ingestion and a new governance/schema
project are not the next task. The research-workflow diagnostic branch remains
available after a concrete use case is selected; do not start both branches now.

## 8. Immediate handoff

**Next action: P2-02A/B — exact coefficient identities, analytic lower/upper
bounds and positive scale factoring. Justify quadrature only if needed. Then
implement P2-02C/P2-03 and decide a conservative q bound's sign at the fixed input.**

The original 2 November reassessment read the pinned source, implementation, retained
records and scoped receipts. That review did not add a proof, numerical execution,
receipt admission or application-performance claim. Historical records and
their hashes remain unchanged. Current operational checkboxes belong in the
[restart checklist](NSRW_COLAB_RESTART_TASKS_2026-10-06.md).

## 9. Reassessment — 12 November 2026

The research frontier remains P2 coefficient bounds. The latest code check
completed 673 tests with 3 external-export tests skipped and 90.53% coverage;
Ruff and diff checks passed. Fresh 128/256/512-bit core records matched the
retained JSON, and the second arithmetic path passed all fifteen interval
containments. This was a same-operator Python/numerical rerun, not a new Lean
replay or an independent reproduction. Local check records are retained under
the ignored `outputs/` directory and are not published evidence attachments.

Two initial test failures came from an unavailable pinned internal diagnostic
dependency; they passed after its exact source revision was built into an
isolated D: check directory. The old shared venv launcher still references a
removed interpreter. Restore a working project environment before sustained
implementation; no production/proof change was needed for this check.

The [analytic-first coefficient route](NSRW_P2_FIRST_INPUT_AND_ERROR_CONTRACT_2026-10-28.md#31-analytic-first-coefficient-route--12-november-2026)
extracts a candidate lower bound from the existing stronger L2 estimate, L3,
F1 and C01. This clarifies the existing instruction to try conservative
analytic bounds before quadrature. It is a static derivation, not a newly
compiled/admitted theorem or a completed coefficient computation.

Refinements to sections 4-8:

1. P0's fixed core inputs support P2 now; unresolved full-Profile conditions
   remain parallel obligations. P1's ten admitted statements remain closed.
2. P2 first needs a lower C_main bound and an upper abs(C_prefix) bound adequate
   for q. Accurate two-sided evaluation of every integral is optional. A scaled
   bound must preserve the exact positive factor and conversion back to q/J.
3. P3 first assembles a conditional local-J bound, distinguishing evaluated
   factors from symbolic positive factors. A quantitative source-J wrapper and
   explicit-instance numerical bracket are further outputs, not requirements
   for starting the core calculation.
4. P4 retains its original alternatives: A, bounded mathematical preservation;
   B, practical comparison. B is recommended after the coefficient milestone,
   with equally informed standard baselines. A is deferred, not deleted.

See the [canonical P0-P4 work breakdown](NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md#7-p0-p4-execution-proposal-and-ai-checklist).
The next concrete output is the coefficient-bound specification and its error
justification, followed by one fixed-input q decision. No new paper, general
verification framework or full CFD implementation is required for that output.
