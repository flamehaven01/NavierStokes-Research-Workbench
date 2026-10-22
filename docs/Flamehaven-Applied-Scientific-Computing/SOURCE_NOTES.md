# Source notes and limits of the application proposals

Prepared: 2026-10-08.
Basis: primary sources inspected during the preceding application discussion,
the supplied historical discussion, and relevant NSRW documents. This is a
planning bibliography, not a comprehensive literature/novelty review or an
application validation report.

Official documentation establishes an existing method or interface. Connecting
that interface to an NSRW-derived computation is a separate proposed experiment.
No listed tool has been installed or benchmarked as part of writing this folder.
Future experiments must pin their actual software versions and inputs.

## S1. AMReX

[AmrCore documentation](https://amrex-codes.github.io/amrex/docs_html/AmrCore.html)
describes application-defined error tagging through `ErrorEst` and regridding.
This supports the feasibility of supplying a diagnostic to an existing adaptive
mesh workflow; it does not derive a directional estimator from NSRW scaling.
Coarse/fine interpolation and time-subcycling constraints also matter: a mesh
change must not be assumed to preserve the original divergence properties.

The [AMReX application list](https://amrex-codes.github.io/amrex/applications.html)
provides concrete ecosystem examples in incompressible flow, wind-farm modeling,
combustion, regional atmosphere/ocean modeling, and plasma-related simulation.
These examples justify investigating integration contexts, not asserting that
one NSRW primitive transfers across those governing models.

## S2. MOOSE flow and heat transfer

The inspected
[NavierStokesFV documentation](https://mooseframework.inl.gov/syntax/Modules/NavierStokesFV/index.html)
describes flow and fluid heat-transfer capabilities. Its syntax entry is marked
deprecated and points to newer Physics-based configuration. It is a capability
reference, not a recommended implementation template for a future adapter.

Cooling-channel analysis is a proposed target task, not a tested NSRW use case.
Any prototype must select a supported API/version and independently establish
the model and benchmark correspondence.

## S3. PETSc

[SNES nonlinear-solver documentation](https://petsc.org/release/manual/snes/)
describes existing nonlinear residual/convergence controls and related diagnostic
facilities. These are comparison baselines, not evidence that a source moment
identity supplies a better residual monitor.

[TSAdapt documentation](https://petsc.org/release/manualpages/TS/TSAdapt/) and the
[time-integration manual](https://petsc.org/main/manual/ts/) describe established
adaptive timestep machinery and error-control context. A candidate recommendation
would need to be compared with these controls, not simply attached to them.
An algebraic residual for a discretized operator does not by itself establish
accuracy against the continuous physical model.

## S4. Dynamic rescaling

The primary research manuscript
[Potential Singularity of the Axisymmetric Euler Equations with C^α Initial Vorticity for a Large Range of α](https://arxiv.org/abs/2212.11912)
provides a concrete research context for dynamic rescaling and numerical
investigation of concentration. It concerns an Euler setting, not validation of
the NSRW construction or a general industrial predictor. Its numerical evidence
must not be relabeled as a proof of singularity or as transferable NSRW performance.

## S5. Gappa

[Gappa](https://gappa.gitlabpages.inria.fr/) and its
[tool documentation](https://gappa.gitlabpages.inria.fr/gappa/tools.html)
illustrate formal checking of numerical computations with explicit bounds and
rounded operations. This supports the need for a real-to-numerical implementation
bridge. It does not establish a current Lean/Gappa integration in NSRW, and the
documented proof-tool ecosystem must not be described as such.

## S6. MOOSE TestHarness

[MOOSE TestHarness](https://mooseframework.inl.gov/python/TestHarness.html)
documents existing scientific-code regression facilities. It is an appropriate
baseline context for testing a proposed regression contribution. Internally
designed mutations alone do not demonstrate sensitivity to real solver defects.

## S7. W3C PROV

[W3C PROV overview](https://www.w3.org/TR/prov-overview/)
describes provenance in terms of entities, activities, and agents, with a
standard interchange family. A proposed scientific-run provenance feature should
be compared with such existing representations. Provenance does not by itself
certify correctness, authenticity, or successful independent reproduction.

## NSRW references and historical discussion

The [P2 study](../M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md) is the starting point
for the ratio/cancellation questions. For live mathematical status, follow the
[dated checklist](../NSRW_COLAB_RESTART_TASKS_2026-10-06.md) to exact proofs and
execution receipts. The [publication plan](../NSRW_PUBLICATION_AND_REPRODUCTION_PLAN_2026-10-08.md)
defines the deferred public research work, and the
[transfer protocol](../ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md) defines the
existing application-evidence requirements.

The user-supplied historical discussion is a design reference, not primary
mathematical evidence. Its durable points are retained: expose computable
operations, distinguish proof from application utility, preserve negative results,
and keep research ahead of infrastructure growth. Historical progress percentages,
superseded compile states, speculative acceleration claims, and publication
aspirations are not copied as current facts. Metaphors about making equations
"exist" through execution are not used as scientific justification.

The remaining evidence gaps are explicit: a selected transferable primitive,
source-to-domain mapping, admitted numerical evaluator where needed, justified
rounding/discretization bounds, a preregistered comparison, independent review,
and demonstrated benefit for a specific task. None is supplied merely by this
bibliography or by creating the project folder.
