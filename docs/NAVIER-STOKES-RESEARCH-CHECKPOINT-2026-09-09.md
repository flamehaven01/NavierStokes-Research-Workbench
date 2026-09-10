# Navier–Stokes Research Workbench — Checkpoint

**Project:** Equation to Artifact / Flamehaven Labs

**Workspace target:** `<local-workspace>/NavierStokes-Research-Workbench`

**Date:** 2026-09-09

**Current process marker:** M3 in progress
**Next session:** Continue tomorrow

## 1\. Project purpose

This project has three distinct layers of ambition and they must not be conflated:

1. **Reproduce and audit the checkable surface of OpenAI's 2026 Navier–Stokes finite-time blowup result.**
2. **Study materially different mathematical routes**, rather than merely re-implementing OpenAI's proof architecture.
3. **Explore whether an independent or stronger Navier–Stokes result can be developed**, including the long-term unforced problem.

The core computation is not the claim of novelty. The contribution is the custody: isolating the exact mathematical claim, reproducing it under an inspectable environment, and making its boundary visible.

A proof establishes the theorem. An executable artifact preserves the checkable surface.

## 2\. Source result being tracked

Primary paper supplied to the project:

* OpenAI, **"Finite time blowup for Navier–Stokes"** (`navier-stokes.pdf`)
* OpenAI overview: `https://openai.com/index/navier-stokes-solution/`
* Formalization repository: `https://github.com/openai/NavierStokesAndEuler`

Theorem 1.1 in the supplied paper considers the 3D incompressible Navier–Stokes equations

\[
\\partial\_t u + (u\\cdot\\nabla)u - \\nu\\Delta u + \\nabla p = f,
\\qquad \\nabla\\cdot u = 0,
]

with positive viscosity, zero initial velocity, and a smooth compactly supported force. The construction produces a smooth solution on (\[0,1)) whose kinetic energy stays uniformly bounded while the velocity becomes unbounded as (t\\uparrow 1).

The paper presents this as establishing Clay alternatives (C) in (\\mathbb{R}^3) and, via compact support / periodicization, (D) on (\\mathbb{T}^3).

### Boundary

* This is a **forced** Navier–Stokes construction.
* It is not the same statement as proving finite-time blowup for the unforced equation (f\\equiv 0).
* Clay acceptance, peer review, and broad mathematical acceptance are external processes and must not be inferred merely from the paper or formalization.
* The theorem and proof belong to the original authors.

## 3\. OpenAI proof architecture — current high-level map

The supplied paper's construction can be summarized as:

\[
\\boxed{
\\text{concentrating anisotropic vortex}
\\rightarrow
\\text{annular residual stress}
\\rightarrow
\\text{oscillatory momentum-flux realization}
\\rightarrow
\\text{iterated residual correction}
\\rightarrow
\\text{smooth compact forcing}
}
]

Important ingredients already identified:

* anisotropic similarity scales with (\\tau=1-t), approximately

  * radial scale (\\ell\_r\\asymp \\tau^{1/2}),
  * axial scale (\\ell\_z\\asymp \\tau^{1/2-h}),
  * characteristic swirl / axial velocity (\\asymp \\tau^{-1/2-h});
* an axisymmetric concentrating background flow;
* an annular stress produced by the remaining tangential momentum residual;
* two oscillatory pulse families whose averaged quadratic momentum flux spans the required stress cone;
* an auxiliary torus used to separate overlapping oscillatory supports;
* moment matching and compactly supported mean corrections;
* iterative residual improvement so that the residual becomes flat to every order near the singular point;
* localization in space and time, after which the residual is extended as a smooth compactly supported force.

This route is the **OpenAI reproduction lane**, not the novelty lane for Flamehaven.

## 4\. Formalization / artifact surface

The public repository `openai/NavierStokesAndEuler` contains Lean 4 formalizations of the Navier–Stokes and Euler results.

Current source observations already made:

* main Navier–Stokes statements include the Clay-style breakdown alternatives for (\\mathbb{R}^3) and the periodic case;
* `formalization.yaml` declares a full formalization scope and reports `sorry\_count: 0` for the listed main results;
* the repository uses Lean, Mathlib, Lake, and Comparator-based checking;
* the Comparator README gives a reproducible checking path using `lake exe comparator ...`;
* repository self-description currently labels review status as **self-assessed**.

### Required custody chain

The first Equation-to-Artifact deliverable should trace:

\[
\\text{Clay problem statement}
\\rightarrow
\\text{paper theorem}
\\rightarrow
\\text{Lean statement}
\\rightarrow
\\text{proof dependencies}
\\rightarrow
\\text{Comparator target}
\\rightarrow
\\text{reproducible build / verifier receipt}
]

Every arrow must be inspected rather than assumed.

## 5\. Independent research lanes

The project should not stop at reproducing OpenAI's construction.

### Lane A — OpenAI artifact reproduction

Goal: independently reproduce the public theorem / formalization surface and build a custody ledger.

Status: active.

### Lane B — Independent derivation of the same Clay alternative

Goal: reconstruct a route to the forced breakdown statement from the broader literature without relying on OpenAI's proof architecture as the only template.

The result is only meaningfully independent if its central mechanism is materially different.

### Lane C — Stable-profile / dynamically rescaled route

Candidate research program:

\[
\\text{candidate singular profile}
\\rightarrow
\\text{certified PDE residual}
\\rightarrow
\\text{linear stability / spectral information}
\\rightarrow
\\text{nonlinear stability}
\\rightarrow
\\text{singularity conclusion}
]

The search should include anisotropic, two-scale, nearly self-similar, or dynamically rescaled profiles rather than assuming a naive one-scale Leray profile.

This is currently the preferred independent discovery lane.

### Lane D — Multiscale cascade / amplification route

Study whether a genuine Navier–Stokes internal cascade can be closed using repeated vorticity / shear amplification across scales without reproducing OpenAI's annular stress–pulse mechanism.

Toy or averaged equations must be kept clearly separate from the actual Navier–Stokes nonlinearity.

### Lane E — Unforced 3D Navier–Stokes

Long-term target:

\[
f\\equiv0
]

with either a rigorous finite-time singularity construction or a global-regularity result.

This is substantially stronger than reproducing the current forced construction and must not be implied by success on Lane A.

## 6\. Research discipline

For every claim or implementation, keep five layers separate:

1. **Original theorem / scientific result** — belongs to the source authors.
2. **Source claim** — quoted or paraphrased accurately from the primary source.
3. **Checkable surface** — the narrow statement or computation that can be reproduced.
4. **Executable artifact** — code, Lean proof, tests, verifier commands, manifests, expected outputs, receipts.
5. **Boundary** — what the artifact does not prove or verify.

Preferred language:

* reproduced
* isolated
* pinned
* made executable
* checked under a specified environment
* boundary documented

Avoid:

* "we proved the Navier–Stokes problem"
* "we verified the whole theorem" unless the evidence literally supports that scope
* claims that an executable reproduction replaces expert mathematical review

## 7\. Audit protocol for the workbench

The next detailed review must proceed strictly in this order:

### Phase 1 — README

Read the entire README first.

Check:

* exact project claim;
* source attribution;
* distinction between OpenAI reproduction and independent research;
* Clay / Millennium wording;
* whether forced vs unforced is stated correctly;
* reproducibility commands;
* environment / dependency pins;
* claims of proof, verification, or novelty;
* current milestone description and M3 semantics.

Do not use code to reinterpret an unclear README claim. Record the mismatch first.

### Phase 2 — docs

Read all relevant documentation next.

Check:

* roadmap and milestone definitions;
* source map and bibliography;
* theorem / equation identifiers;
* research-lane separation;
* mathematical assumptions;
* artifact boundary statements;
* evidence / receipt / manifest policy;
* any M1/M2/M3 acceptance criteria;
* stale or contradictory documents.

Build a documentation inconsistency list before code review.

### Phase 3 — code

Only after README and docs are understood, inspect the implementation.

Review:

* module boundaries;
* equations actually implemented;
* normalization and scaling conventions;
* residual definitions;
* divergence-free constraints;
* precision / tolerance choices;
* deterministic behavior;
* symbolic vs numerical steps;
* tests and falsifiers;
* source-to-code traceability;
* dependency pins;
* executable verifier path;
* whether outputs match documented claims;
* whether code silently assumes stronger facts than docs establish.

All code findings must be classified as one of:

* `CONFIRMED`
* `PARTIAL`
* `UNVERIFIED`
* `CONTRADICTED`
* `OUT\_OF\_SCOPE`

## 8\. M3 checkpoint

User-reported state at this checkpoint:

* **M3 is currently in progress.**
* Review is not complete.
* The next session should continue from the existing M3 state rather than restart the project conceptually.
* Before new implementation, inspect the work already completed and reconcile it against README and docs.
* Required review order remains **README → docs → code**.

No inference is made here about what M3 specifically means until the repository's own milestone documentation is read.

## 9\. Tomorrow's restart protocol

At the start of the next session:

1. Open the exact workspace.
2. Capture Git status before changing anything.
3. Read README in full.
4. Read milestone / roadmap / research / architecture docs relevant to M3.
5. Build an evidence table of current claims and acceptance criteria.
6. Only then inspect code and tests.
7. Run verification only after the code path and expected outcome are understood.
8. Separate pre-existing issues from issues introduced during the current session.
9. Do not mutate files during audit unless an explicit fix is requested.
10. Preserve all runtime receipts for any subsequent mutation or verification step.

## 10\. Current boundary

This checkpoint records the current research framing and intended audit method only.

It does **not** assert that:

* the local workbench has been fully reviewed;
* M3 has passed;
* the OpenAI proof has been independently reproduced locally;
* the Lean repository has been rebuilt locally;
* Comparator has been independently rerun locally;
* the forced result establishes an unforced Navier–Stokes singularity;
* Flamehaven has solved the Millennium problem.

The next step is evidence-first inspection of the local repository in README → docs → code order.
