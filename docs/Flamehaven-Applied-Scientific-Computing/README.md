# Flamehaven Applied Scientific Computing

Planning date: 2026-10-08.
Scope: a proposed follow-on application research project, documented here before
implementation. This folder is not a new software repository, proof receipt,
claim ledger, or authorization to start experiments or publish.

## Purpose

Find out whether a mathematical structure can become a useful computation in a
specific scientific or engineering workflow, or whether a research-support
operation can make that workflow more reliable. The intended contribution is
practical: better numerical reliability, clearer failure detection, lower
computational cost, or more informative analysis. A new mathematical model is
welcome but is not a prerequisite for useful software.

NSRW remains the mathematical research project. This follow-on project asks a
different question: **what, if anything, can someone use outside the original
construction, and what evidence shows that it helps?**

요약: NSRW의 수학 연구를 먼저 마친 뒤 연구성과와 재현 자료를 공개하고,
그 다음 특정 용도의 알고리즘·진단 도구로 옮길 가능성을 시험한다.
수학적 증명, 실행 성공, 현장 효용은 서로 다른 결과다.

## Two application branches

1. **Computations motivated by mathematics:** normalization and rescaling,
   evaluation of a specified quantity, admissible-domain checks, and numerical
   instability diagnostics. Which current results can be computed from real
   inputs, and whether those computations help, remain experimental questions.
2. **Scientific research workflow tools:** detect mismatches among proof inputs,
   source versions, and execution results; classify reproduction failures; and
   run regression checks when a model changes. This is an application field in
   its own right, not merely administrative support. It may offer a nearer-term
   use case, but usefulness beyond existing tools must still be measured.

The second branch does not claim a new PDE result or acquire mathematical
authority from the first. Both follow the same post-publication schedule and
require a named task, baseline, failure cases, and evidence of benefit. They do
not authorize a second governance system or an expansion of current NSRW work.

## Relationship to NSRW

The agreed work order is:

1. Continue the existing NSRW mathematical checklist through Z. Do not add an
   application task to the current proof dependency chain.
2. After Z, prepare the bounded research account and reproducible artifacts;
   undertake the selected manuscript/Zenodo publication work under separate
   approval. The publication plan determines the appropriate objects; there is
   no mandatory quota of papers.
3. After that publication checkpoint, select one application candidate and run
   a small comparative experiment under separate approval.
4. Integrate a prototype only if the experiment demonstrates useful behavior
   beyond a named baseline. Evaluate domain utility before considering deployment.

The 2026-10-21 [post-Z+J computational bridge](../NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md)
elaborates the interval between publication and the application experiment:
reconstruct the source assumptions and quantitative moment bound, investigate an
admissible evaluable model, then produce a checked fixed-eta certificate. A
bounded scaling/localization extension is a separate research question. This
remains NSRW research, not demonstrated application utility or an instruction
to implement a general solver.

This ordering is a scheduling decision, not a theorem that publication is
necessary for engineering. A Zenodo deposit preserves a research object; it does
not substitute for peer review, independent reproduction, or application evidence.

Current mathematical state belongs to the
[NSRW checklist](../NSRW_COLAB_RESTART_TASKS_2026-10-06.md), exact proof files,
and dated receipts. This folder deliberately does not duplicate their live
statuses or hashes. The
[publication plan](../NSRW_PUBLICATION_AND_REPRODUCTION_PLAN_2026-10-08.md)
describes the intermediate public research checkpoint.

## Equation to Artifact, then Artifact to Application

Equation to Artifact makes a limited consequence inspectable: identify the
source, expose the inputs and assumptions, implement or formalize the selected
operation, and preserve observations and failure cases.

Artifact to Application asks whether a changed representation or domain adapter
has measurable value for an actual task. It requires new evidence. Source
assumptions, units, discretization, floating-point error, boundary conditions,
and the target user's decision must all be reconsidered.

The history of science is not a universal one-way sequence from theory to
product. Observation, computation, experiment, and theory often develop together.
The sequence here is a local work plan with feedback: an application experiment
can reject a candidate or reveal a new mathematical question.

Code does not make a theorem more true. It can make consequences, limitations,
and engineering costs easier to test. No reduction in research time or improvement
in solver performance has been measured for this follow-on project.

## What is worth carrying forward?

Potential outputs include a cancellation-aware diagnostic, a denominator-safety
check, a resolution-risk indicator, a numerical precondition, or a reproducible
regression test. A useful negative result is also an output: identifying that a
candidate is undefined, too noisy, redundant, or too expensive in the target task.

The P2 study supplies a particularly useful caution. A scaling-derived ratio
does not remain usable when its denominator vanishes. Exact cancellation can
also create regions in which that ratio is unavailable. These facts motivate
domain and conditioning checks; they do not already constitute a general-purpose
CFD algorithm. See the
[P2 study](../M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md) for exact scope and evidence.

The current formal construction does not supply an admitted executable numerical
evaluator for every selected witness. A manufactured fixture must therefore be
labeled as such; it cannot stand in for a reproduced selected source instance.

## Boundaries

- Lean compilation concerns a named proposition under its formal assumptions,
  not a floating-point implementation or a physical forecast.
- A scale-invariant quantity need not detect a change in absolute scale.
- A numerical alarm is not automatically a physical instability forecast.
- Two systems using PDEs does not establish a valid transfer between them.
- Existing AMR, residual monitors, rescaling methods, regression tools, and
  provenance standards are baselines, not capabilities invented by this project.
- No current claim is made about weather forecasting, semiconductor process
  improvement, clinical use, industrial deployment, or application novelty.
- Same-session execution and review are not independent external attestation.

Use the existing
[transfer protocol](../ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md) and
[operational-exposure explanation](../OPERATIONALLY_EXPOSED.md) where relevant.
This folder adds a concrete application agenda, not another stage taxonomy,
governance engine, CI system, or status authority.

## Documents

- [Application research plan](APPLICATION_RESEARCH_PLAN.md): nine candidate
  primitives, plausible fields, baselines, failure conditions, and a bounded
  post-publication checklist.
- [Source notes](SOURCE_NOTES.md): previously inspected primary sources and
  the distinction between documented technical interfaces and proposed NSRW use.

Success means a measured benefit for a stated task, not the number of adapters,
documents, proofs, or application names accumulated.
