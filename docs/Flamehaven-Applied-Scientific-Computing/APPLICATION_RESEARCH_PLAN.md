# Application research plan

Planning date: 2026-10-08.
All entries below are candidates, not implemented or validated application
capabilities. Experiments are deferred until the NSRW Z and subsequent
publication checkpoints described in the [project introduction](README.md).

Research bridge added 2026-10-21: the
[Certified First-Repair Moment Witness plan](../NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md)
connects the admitted Z+J result to this application branch. It first investigates
source-Profile admissibility, an explicit J-margin and a fixed-eta interval
certificate; restricted/toy models remain separately labeled. Scaling/localization
is a later bounded research question. Completing that bridge does not demonstrate
application utility or check any of the experiment boxes below.

## 1. Select an operation, not an industry slogan

Before selecting a candidate, answer five questions:

1. What exact source result or implemented operation is being reused?
2. What computable inputs does the target workflow actually provide?
3. What decision or numerical error can the output help with?
4. What existing method is the comparison baseline?
5. What observation would show that the candidate is not worth pursuing?

A candidate without a source-to-operation link remains an unanchored hypothesis.
A generic numerical method can still be useful, but must be described as such,
not as a new application of the NSRW theorem. A computable manufactured family
can support a controlled experiment without supplying the unavailable selected
source witness.

## 2. Nine candidate primitives

These mappings are engineering hypotheses. The sources establish that related
methods or integration interfaces exist, not that NSRW has improved them.

| Mathematical structure | Bounded operation to investigate | Plausible task / field | Required comparison and principal failure condition |
| --- | --- | --- | --- |
| Anisotropic scaling | Directional resolution-risk score; initially a recommendation, not automatic mesh control | Incompressible shear layers, wakes, flow/heat-transfer simulation | Compare gradient/error-based mesh indicators through an existing AMR interface. Derive the local metric first; a source scaling law alone does not define a mesh estimator. Reject if error reduction at comparable cost does not improve. [AMReX](SOURCE_NOTES.md#s1-amrex) |
| Scale-invariant ratio | Dimensionless shape comparison with an explicit denominator-validity mask | Comparing resolved flow structures across scales | Compare conventional normalized observables. Invariance can hide absolute-scale change; a vanishing or uncertain denominator invalidates the ratio. The P2 candidate `Q = J/(M H)` is not admitted as a global detector. |
| Residual / moment cancellation | Weighted-sum or quadrature diagnostic that reports cancellation, uncertainty, and unavailable outputs | Flux/moment postprocessing; solver consistency checks | Compare ordinary residual monitoring and stable summation/quadrature against a reference. Exact cancellation is not an error estimator by itself. Reject if the proposed output adds no information beyond standard conditioning checks. [PETSc](SOURCE_NOTES.md#s3-petsc) |
| Concentration rate | Local under-resolution warning | Vortex/shear-layer diagnostics in research CFD | Compare resolved-reference errors and existing gradient/vorticity indicators. Predefine the numerical event and false alarms; do not label it a physical blow-up or catastrophe predictor. |
| Dynamic rescaling | Coordinate transformation for examining a localized evolving structure | Research simulations of rapidly concentrating structures | Compare fixed/adaptive-grid observations at comparable cost. Check inverse mapping, interpolation, boundary conditions, and conservation. A research microscope is not a validated industrial forecast. [Primary research](SOURCE_NOTES.md#s4-dynamic-rescaling) |
| Exact inequality | Computable input guard or error-margin check | Scientific kernels with denominator, normalization, or parameter constraints | Compare an ordinary guard or interval check. Establish the real-to-floating-point link and hypothesis checks. Reject if the bound cannot be evaluated or rounding consumes the margin. [Gappa](SOURCE_NOTES.md#s5-gappa) |
| Lean theorem | Formally justified numerical precondition, after a separate implementation bridge | A narrowly specified scientific computation | Trace the exact theorem to the callable operation and runtime inputs. Compilation alone does not verify discretization or provide a computable witness. Gappa illustrates numerical-verification methods, not an existing Lean integration. |
| Mutation / falsifier | Scientific-code regression cases tied to known failure modes | Solver/library maintenance and model changes | Compare an established harness and real defect cases, not only internally manufactured mutants. Reject if coverage or diagnostic value is unchanged. [MOOSE TestHarness](SOURCE_NOTES.md#s6-moose-testharness) |
| Dependency traceability | Run-to-source/dependency/result provenance record | Reproducible scientific workflows | Compare PROV-compatible records and existing workflow tools. Version binding is not authenticity, physical validity, or proof of reproduction. [W3C PROV](SOURCE_NOTES.md#s7-w3c-prov) |

The first five rows require additional source/domain analysis; their interfaces
are not derived automatically from current proofs. The last four may be easier
to implement, but ease of implementation is not evidence of novelty or usefulness.

There are two application branches, not a single maturity ladder. Mathematical
computations include normalization/rescaling, quantity evaluation, domain checks,
and numerical diagnostics. Research-workflow applications include input/result
consistency checks, reproduction-failure classification, and model regression
checks. A Lean-backed numerical precondition belongs to the first branch;
checking which proof bytes a run consumed belongs to the second.

## 3. Recommended first candidate: cancellation and denominator diagnostics

This is a recommendation within the mathematical-computation branch for later
selection, not an active experiment. It does not exclude selecting a bounded
research-workflow use case instead after the publication checkpoint.
It is the closest practical question to the P2 obstruction study: can software
make a mathematically unavailable or numerically unreliable output visible
instead of returning a convincing but misleading number?

Start with explicit weighted terms or an explicitly computable profile family.
Do not require an unavailable selected `Profile`/`TailData` numerical instance.
The source analysis motivates the failure cases; any new numerical procedure
requires its own justification.

Proposed input/output:

```text
input:
  explicit weighted terms or quadrature samples
  declared precision, units, and error assumptions
  declared denominator margin when a ratio is requested

output:
  computed moment and an uncertainty estimate with stated coverage
  cancellation/conditioning observation
  ratio value only when its denominator is demonstrably admissible
  unavailable/uncertain reason otherwise
```

Separate three cases: mathematically zero, numerically indistinguishable from
zero at the available precision, and nonzero with a justified usable margin.
A heuristic tolerance alone must not be described as a rigorous error bound.

Candidate failure cases:

- a nonzero prefix followed by exact terminal cancellation;
- nearly cancelling terms with a small nonzero reference remainder;
- a denominator that changes sign or falls below the justified margin;
- benign, well-conditioned data on which extra checks should not raise alarms.

Baselines include ordinary evaluation, pairwise/compensated summation where
applicable, existing conditioning estimates, and appropriate quadrature error
controls. A high-precision or analytic reference needs its own error assessment;
more digits alone are not a certified ground truth.

Measure numerical error, invalid-output detection, false alarms, runtime, and
memory at matching workloads. Use cases not used for tuning. If existing methods
already provide the same output and reliability, document that outcome instead
of packaging the method as an NSRW innovation.

This initial offline experiment is not a solver controller. It does not change
mesh, timestep, physical model, or production decisions automatically.

## 4. Specific fields: where the connection is nearer or further away

| Field / task | Why it is worth examining | What is still missing |
| --- | --- | --- |
| Scientific research workflow tools | Proof/source/run mismatches, reproduction failures, and model changes are concrete problems for researchers and scientific-software maintainers | Real cases with known causes, compatibility with existing workflows, and measured benefit over Git/build diagnostics, test harnesses, and provenance records; not an independent mathematical verifier |
| Scientific numerical postprocessing | Moments, fluxes, normalization, and cancellation are direct computational operations | A useful primitive, error analysis, and evidence of improvement beyond stable numerical baselines |
| Cooling-channel / fluid heat-transfer simulation | Flow and thermal quantities provide a relatively concrete target workflow; existing solvers support such models | Actual governing equations, boundary conditions, variable mapping, accepted benchmarks, and independent domain review. This is not a semiconductor-process breakthrough claim. [MOOSE capability context](SOURCE_NOTES.md#s2-moose-flow-and-heat-transfer) |
| Wind-farm wakes / flow resolution | Existing AMR applications provide possible integration contexts | A justified local diagnostic and comparison against established resolution/error measures. No energy-yield improvement is inferred. [AMReX applications](SOURCE_NOTES.md#s1-amrex) |
| Combustion, plasma, or process multiphysics | Related computational ecosystems exist | Compressibility, reactions, species, electromagnetic effects, and coupling change the mathematical object; each needs separate mapping and evidence |
| Atmosphere / ocean modeling | Adaptive numerical methods are used in these fields | Forcing, stratification, rotation, closure, data assimilation, and scale differences make transfer substantially less direct; no forecast improvement is currently supported |

Clinical or safety-critical applications are not initial targets. No medical,
hazard-warning, or other consequential human decision should rely on an
unvalidated research diagnostic.

### Research-workflow branch: a bounded first use case

Proposed task: help a researcher determine why a reproduction did not match its
declared inputs or expected result. This is a possible user-facing tool, not a
new claim-admission gate.

Inputs would be a declared proof/source identity, the observed identities and
commands, and preserved execution results. Outputs would identify a mismatch,
classify an observed failure boundary, or report insufficient evidence. Relevant
classes include input/version drift, environment or dependency absence,
invocation failure, compile/test failure, and output drift. An unsuccessful
compile is not automatically a mathematical counterexample; unchanged hashes
are not proof of semantic equivalence.

For model regression, define the changed model, intended preserved behavior,
and allowed differences before comparing outputs. A changed result can be an
intentional correction, not a defect. Do not infer model validity from a passing
regression suite.

Compare against ordinary Git diffs, existing build/test error reporting, and
provenance records. Use real past failures with independently reviewed labels
as well as synthetic controls, and hold out cases not used for tuning. Measure
classification accuracy, false diagnoses, correct abstention when evidence is
missing, setup burden, and researcher triage time. Any time-saving claim needs
an actual comparative user-task measurement, not a faster script alone.

This branch may be closer to a usable tool because its inputs are already
recordable. That is a feasibility hypothesis, not a demonstrated advantage or
a reason to displace the mathematical/computational research bridge. The earlier
C03/C04/Z scheduling language is superseded by the linked post-Z+J plan; it does
not reopen those historical proofs. Start with one task, not a generic
research platform. The existing provenance and regression baselines are linked
in the [source notes](SOURCE_NOTES.md#s6-moose-testharness).

## 5. Post-publication execution checklist

These boxes are intentionally unchecked. They do not reopen the NSRW proof
checklist or record current proof progress. The existing
[transfer protocol](../ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md) remains the
reference for lineage, independent domain review, comparative evidence, and
stopping rules; this list does not waive it.

- [ ] Verify Z closure and its exact admitted scope using source, proof, and receipts.
- [ ] Complete the separately approved publication checkpoint; record actual
  manuscript/artifact identifiers without treating a deposit as peer review.
- [ ] Obtain approval to start one bounded application experiment.
- [ ] Select one candidate and branch, identify its source lineage, and name the intended user/task.
- [ ] Record the target equations or research workflow, units where applicable,
  hypotheses, invalid inputs, and
  representation changes; obtain the independent domain review required by the
  transfer protocol, or keep the affected stage held.
- [ ] Define a callable operation using available inputs. Label manufactured
  inputs and keep them separate from selected-source reproduction claims.
- [ ] Fix baseline names/versions, reference accuracy, datasets, held-out cases,
  permitted tuning, and precision/resolution sweeps before the reported run.
- [ ] Fix quantitative success criteria, maximum time/compute/reviewer budget,
  overhead allowance, and stopping date before inspecting reported results.
- [ ] Execute the controlled comparison and preserve failures as well as successes.
- [ ] Decide whether incremental value exists. Stop if mapping fails, the signal
  is redundant/unstable, inputs are unavailable, or cost exceeds the declared budget.
- [ ] Only on demonstrated benefit, seek approval for a domain prototype and
  independent reproduction. Do not equate a prototype with deployment readiness.

Thresholds are not invented at this planning stage: the selected task determines
appropriate values. They must nevertheless be explicit before the experiment,
not chosen retrospectively to fit its output.

## 6. Useful outcomes and stopping

A positive outcome is a reproducible improvement on a named task within a stated
budget. A negative outcome is an informative limitation: no usable signal,
insufficient precision, broken assumptions, unavailable evaluator, redundancy,
or excessive cost. Both should remain inspectable.

If the first candidate fails, do not build a generic framework to keep it alive.
Choose whether to stop, make a narrowly justified mathematical revision, or
consider one different candidate under new approval. Practical benefit, not a
preselected narrative about scientific breakthroughs, determines the next step.
