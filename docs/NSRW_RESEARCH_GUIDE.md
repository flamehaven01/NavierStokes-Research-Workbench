# Start with the research

NSRW turns mathematical questions into source-linked results, checked proofs and
executable scientific computations. The present study starts with OpenAI's
outgoing-profile construction and investigates how two differently weighted
histories cancel.

## The central finding

For every fixed source Profile F, there is a positive threshold depending on F.
For every positive parameter below that threshold, a point strictly inside the
first repair window has **M = 0 and J > 0 at the same point**.

M is the source mass history; J is its H-weighted angular history. Separated
repair supports and unequal relative weights explain why their cancellations
do not coincide. This gives a concrete obstruction to using the candidate
ratio Q = J/(M H) at that point.

The quantitative extension gives a positive lower bound for local J at every
qualifying first-window mass zero. Normalization and a cutoff plateau replace
an exact bump integral with a conservative computable lower bound.

## Choose a route

- **Understand the mathematics:** read [P01](../research-papers/versions/P01-v0.5/P01_MassZero_AngularMismatch.pdf), then inspect the named Lean statements.
- **Run a concrete computation:** use the [core-scalar method](P2_CORE_SCALAR_METHOD_2026-10-31.md) and [second-backend check](NSRW_CORE_SCALAR_CROSSCHECK.md).
- **Replay the proofs:** follow [REPRODUCE](../research-papers/REPRODUCE.md). It distinguishes proof execution checkpoints from later document revisions.
- **Follow the next research step:** see the [math-to-code bridge](NSRW_MATH_TO_CODE_BRIDGE.md).
- **Read the research process:** [P02](../research-papers/versions/P02-v0.6/P02_SourceBound_ReproducibleResearch.pdf) explains the implementation and observed failure cases.

## Important source documents

The following documents contain detail beyond the papers. They retain dated
research history; use their headings and dates when reading an older task state.

- [P2 mathematical investigation](M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md): candidate ratio, rejected endpoint-first-zero assumption, repair geometry and weighted-tail argument.
- [Quantitative receipt](stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md): ten named quantitative and normalization propositions.
- [Z-core receipt](stage_receipts/P2_Z_CORE_COLAB_2026-10-12.md) and [Z+J receipt](stage_receipts/P2_ZPLUS_J_COLAB_2026-10-12.md): the source-facing existence and same-witness results.
- [Equation to Artifact roadmap](EQUATION_TO_ARTIFACT_VISION_ROADMAP.md): the broader route to reusable operations and scientific use.

## Practical direction

Two useful outputs are being pursued: mathematical computation primitives
(normalization, certified bounds and cancellation diagnostics) and research
workflow primitives (source/result consistency and regression checks).

The next numerical milestone is a certified moment witness: an admissible
evaluable model, strict mass signs around an interval, and a positive J lower
bound applying to the same exact zero. A reusable diagnostic can then be
evaluated against a baseline in a selected scientific workflow.
