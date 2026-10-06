# Artifact to Application — transfer gates

Document status: `PROPOSED`
Scope: translational research protocol; no current application capability claim.

## 1. Central rule

> Transferability is a new empirical claim and therefore requires new evidence.

A theorem can motivate a computational primitive. It cannot certify usefulness
in weather, semiconductor physics, CFD, plasma, biology, or another target
domain.

Default admission into this protocol requires a stable source lineage and an
artifact that has reached OE-4. An exception must be explicitly recorded as a
waiver and cannot be presented as validated transfer.

## 2. Required translation object

Before selecting an application domain, define the exact object being
transferred.

A valid object should be expressible as a bounded interface:

~~~text
detector(state, parameters) -> score
invariant(state, parameters) -> pass/fail
residual(state, parameters) -> residual norm
rescaler(state, parameters) -> transformed state
trigger(state, parameters) -> action recommendation
~~~

The transfer record must identify:

- upstream `claim_id`;
- mathematical lineage;
- artifact/content identity;
- hypotheses;
- units or nondimensionalization;
- precision;
- expected behavior;
- invalid input region;
- known failure modes;
- source-to-code tests;
- named comparison baseline.

If the lineage or baseline cannot be written, the object is not ready.

## 3. TR-0 — primitive extraction

Question:

> What reusable computation remains after source-specific narrative is removed?

Required output:

- one bounded callable primitive;
- exact upstream claim lineage;
- transformation record;
- non-claims;
- falsifiers.

Gate:

~~~text
PASS[PRIMITIVE_DEFINED]
HELD[NO_REUSABLE_PRIMITIVE]
HELD[UNANCHORED_HYPOTHESIS]
~~~

A candidate without an upstream claim is labeled
`unanchored_hypothesis`; it is not silently promoted into the transfer
pipeline.

## 4. TR-1 — relevance screen

Question:

> Is there a target-domain quantity, failure mode, or decision that this
> primitive can actually observe or improve?

Required evidence:

- target equation/model;
- variable and units correspondence;
- explicit transformation boundary;
- named existing baseline diagnostic;
- independent domain reviewer;
- bounded go/no-go question.

Gate:

~~~text
PASS[PLAUSIBLE_CORRESPONDENCE]
TRANSFER_FAILED[NO_DOMAIN_MAPPING]
HELD[DOMAIN_REVIEW_MISSING]
~~~

Shared use of PDEs is not a domain mapping.

## 5. TR-2 — controlled transfer

Question:

> Does the primitive behave coherently outside the source construction on a
> controlled benchmark?

Two low-cost falsifiers are mandatory where applicable.

### 5.1 Regular-regime dynamic-range test

A singularity- or concentration-inspired signal must also be tested on a
regular benchmark. For fluid candidates, a benchmark such as Taylor--Green
vortex may be used when scientifically appropriate.

Measure whether the signal has usable dynamic range and acceptable false-alarm
behavior before attempting an extreme application.

### 5.2 Precision/resolution signal-to-noise test

Sweep precision, spatial resolution, and timestep where applicable.

An identity that is exact symbolically may become numerically useless through
cancellation or discretization error.

Required measurements can include:

- signal/noise ratio;
- grid sensitivity;
- timestep sensitivity;
- floating-point sensitivity;
- numerical noise;
- computational overhead.

Gate:

~~~text
PASS[CONTROLLED_TRANSFER]
TRANSFER_FAILED[NO_DYNAMIC_RANGE]
TRANSFER_FAILED[NUMERICALLY_UNSTABLE]
TRANSFER_FAILED[PRECISION_LOSS]
~~~

## 6. TR-3 — preregistered comparative benchmark

Question:

> Does the primitive add measurable information beyond an existing diagnostic?

The experiment must be preregistered before the reported run.

Freeze:

- baseline name and version;
- event/ground-truth definition;
- metrics;
- equal or explicitly normalized compute budget;
- pass/fail thresholds;
- stopping rule;
- held-out cases;
- permitted tuning.

Possible metrics include detection lead time, false-positive/false-negative
rate, calibration error, solver residual, reconstruction error, wall-clock
overhead, and memory overhead.

Gate:

~~~text
PASS[ADDS_MEASURABLE_SIGNAL]
TRANSFER_FAILED[NO_INCREMENTAL_VALUE]
TRANSFER_FAILED[TOO_EXPENSIVE]
~~~

Thresholds chosen after seeing the reported result cannot support this gate.

## 7. TR-4 — prototype integration

Question:

> Can the primitive operate inside a real solver or scientific workflow?

Requirements:

- versioned integration;
- stable interface;
- recorded runtime environment;
- reproducible benchmark;
- failure logging;
- no hidden manual tuning;
- explicit domain adapter identity.

Gate: `PASS[PROTOTYPE]`.

This is not production validation.

## 8. TR-5 — domain validation

Question:

> Does the prototype survive the actual constraints of the target field?

Requirements include, as applicable:

- independent domain-expert review;
- accepted benchmark datasets;
- realistic boundary conditions;
- uncertainty analysis;
- comparison with accepted models;
- sensitivity and ablation studies;
- independent reproduction.

Gate: `SUPPORTED[DOMAIN_VALIDATION]` only for the measured use case.

## 9. TR-6 — operational feasibility

Question:

> Can the capability be used reliably outside the research environment?

Evaluate runtime/cost, reliability, monitoring, update policy, security, safety,
regulatory obligations where relevant, and human workflow fit.

Gate: `READY_FOR_DEPLOYMENT_REVIEW`.

This is an engineering state, not a mathematical status.

## 10. Budget and stopping rules

Every TR stage must declare:

- maximum calendar time;
- maximum compute budget;
- required reviewer time;
- go/no-go date;
- stop condition.

A stage that misses its stop condition becomes `HELD` or
`TRANSFER_FAILED`; it does not extend indefinitely by default.

## 11. Candidate NSRW hypotheses

These are hypotheses, not current capabilities.

### A. Scale-change detector

Candidate form: `scale_signal(flow_state) -> scalar`.

Possible use: detect loss of resolution or a regime change.

Current resource status: `unanchored_hypothesis` until a specific claim_id is
selected and TR-0 lineage is written.

### B. Simulation-integrity monitor

Candidate form:

~~~text
integrity(flow_state) -> {
  divergence_error,
  residual_error,
  invariant_error
}
~~~

Possible use: distinguish numerical convergence from physical-consistency
drift.

Current resource status: `unanchored_hypothesis` unless bound to an admitted
residual/invariant claim.

### C. Dynamic-rescaling microscope

Candidate form:
`rescale(flow_state, detected_scale) -> normalized_local_state`.

Possible use: keep a rapidly concentrating local structure numerically
observable.

Current resource status: `unanchored_hypothesis` until lineage is fixed.

### D. Evidence/provenance primitive

Candidate source: existing evidence graph and identity-binding artifacts.

Possible use: scientific-model provenance and reproducibility checks.

This infrastructure branch may be closer to TR-0 than the PDE candidates, but
must be compared with named provenance baselines rather than assuming novelty.
A TR-1 plan may include W3C PROV-compatible provenance systems when they match
the target use case.

### E. Mutation/regression primitive

Candidate source: existing mutation/falsifier machinery.

Possible use: scientific-model regression and fail-closed validation.

This branch likewise requires named baseline regression/verification harnesses
before TR-3.

## 12. Domain-specific caution

Weather and cyclone models include physics and coupling beyond the narrow
forced incompressible Navier--Stokes construction. Semiconductor process
simulation may involve flow, heat, species transport, plasma, chemistry, and
multiphysics coupling.

No domain is a current NSRW capability merely because it is listed here.

## 13. Negative-result policy

Legitimate outcomes include:

~~~text
TRANSFER_FAILED[NO_DOMAIN_MAPPING]
TRANSFER_FAILED[NO_DYNAMIC_RANGE]
TRANSFER_FAILED[NUMERICALLY_UNSTABLE]
TRANSFER_FAILED[PRECISION_LOSS]
TRANSFER_FAILED[NO_INCREMENTAL_VALUE]
TRANSFER_FAILED[TOO_EXPENSIVE]
TRANSFER_FAILED[ASSUMPTIONS_BREAK]
HELD[DOMAIN_REVIEW_MISSING]
HELD[INSUFFICIENT_DOMAIN_EVIDENCE]
~~~

Negative results are retained in `NEGATIVE_RESULT_REGISTER.md`.

## 14. Application custody chain

Every positive application claim preserves:

~~~text
source claim_id
  -> mathematical result claim_id
  -> executable artifact version
  -> primitive version
  -> domain adapter version
  -> benchmark identity
  -> environment
  -> observed metrics
  -> boundary / non-claims
~~~

The application claim belongs only to the measured benchmark and domain scope.
