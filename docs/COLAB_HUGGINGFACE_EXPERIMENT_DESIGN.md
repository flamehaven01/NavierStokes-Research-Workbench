# Colab + Hugging Face Experimental Design

Date: 2026-09-09
Status: `DESIGN_BASELINE__EXTERNAL_EXPERIMENT_TRACK__M3_BOUNDARY_PRESERVED`

## 1. Purpose

This document defines the execution architecture for using Hugging Face and Google Colab inside the NavierStokes Research Workbench.

The design principle is simple:

- Hugging Face is the external experiment asset registry and source of datasets/models/Spaces.
- Google Colab is the cloud execution environment for reproducible bounded experiments.
- The local NavierStokes Research Workbench remains the custody layer that records source identity, assumptions, diagnostics, receipts, falsifiers, and non-claims.

This track is not a proof track. It is an independent numerical/control/falsification track surrounding the primary paper and Lean source.

Equation to Artifact boundary:

> A proof establishes the theorem. A numerical solver approximates the dynamics. A dataset samples the solver. A neural operator approximates the dataset. The artifact records where each transformation preserves or loses the original claim.

The global Navier–Stokes theorem claim remains `UNVERIFIED` regardless of whether an external experiment passes.

## 2. Overall architecture

```text
Primary Paper / Lean / Source equations
        |
        +-- Core workbench
        |     M1 -> M2 -> M3 -> M4 ...
        |
        +-- External experiment track
              |
              +-- Hugging Face
              |     datasets
              |     models
              |     Spaces
              |     metadata / revisions
              |
              +-- Google Colab
                    executable notebooks
                    |
                    v
                 receipts
                    |
                    v
              comparison / falsification
```

The external lane must never silently promote its results into the paper/Lean theorem lane.

## 3. Hugging Face role

Hugging Face should be treated as an external benchmark and experiment registry, not as proof authority.

Three primary asset classes are relevant:

| HF asset | Project role |
|---|---|
| Dataset | external flow trajectories, benchmark inputs, controlled comparison data |
| Model | FNO/PINO/GFNO/KNO or other surrogate baselines |
| Space | visualization, interactive inspection, reference-only exploration |

Every Hugging Face asset admitted into the workbench should carry a machine-readable metadata record containing at least:

```text
asset_id
source_url
repository_id
revision / commit
file / shard
sha256 where feasible
dataset size
domain
dimension
forced / unforced
viscosity / Reynolds number
boundary condition
time horizon
grid size
variables
license
intended experiment
claim relevance
evidence class
```

The fields `forced/unforced`, `2D/3D`, `periodic/R3`, and `velocity/vorticity` are mandatory distinctions. They must not be inferred later from filenames or model names.

## 4. Google Colab role

Colab is the executable experiment surface.

Each notebook should answer one narrow research question only. Do not combine unrelated experiments into a single large notebook because this weakens provenance and makes receipt boundaries ambiguous.

Recommended experiment identities:

```text
E1  Taylor-Green analytic control
E2  Hugging Face dataset physical audit
E3  FNO rollout physics audit
E4  forced vs unforced scope audit
E5  resolution sensitivity
E6  viscosity / Reynolds sensitivity
E7  FNO vs PINO vs other surrogate comparison
E8  independent solver comparison
```

## 5. Standard Colab notebook contract

Every project-owned notebook should follow the same structure:

```text
0. Artifact metadata
1. Research question
2. Source / dataset identity
3. Scope and non-claims
4. Environment pin
5. Data acquisition
6. Preprocessing
7. Core computation
8. Independent diagnostic
9. Negative control / mutation
10. Result
11. Receipt export
12. Boundary
```

At the top of every notebook include an explicit non-claim such as:

> This notebook is an external numerical diagnostic. It does not verify a 3D Navier–Stokes blowup theorem, establish paper–Lean semantic equivalence, or promote a sampled residual to proof authority.

## 6. First execution wave

### E1 — Taylor-Green analytic control

Purpose:

- create a cloud baseline with a known analytic solution;
- compare exact velocity/pressure/vorticity with sampled numerical operators;
- establish grid and derivative-error behavior before introducing ML.

Core measurements:

```text
velocity error
pressure error
vorticity error
divergence error
PDE residual
grid-convergence trend
```

This becomes the calibration baseline for later PINN/FNO/PINO experiments.

### E2 — Hugging Face dataset physical audit

Recommended first HF dataset: the bounded 2D periodic FNO Navier–Stokes dataset already registered in `EXTERNAL_EXPERIMENT_LANDSCAPE_HF_COLAB.md`.

Research question:

> Can a pinned external vorticity trajectory be independently reconstructed into a velocity field that preserves expected discrete incompressibility and vorticity consistency under a declared spectral scheme?

Execution chain:

```text
HF dataset
    |
trajectory selection
    |
vorticity omega(x,y,t)
    |
Poisson solve
    |
stream function psi
    |
velocity u = grad-perp psi
    |
+-- divergence
+-- vorticity reconstruction
+-- energy
+-- enstrophy
+-- spectral distribution
    |
receipt.json
```

This experiment intentionally uses no learned model. The external dataset itself is audited before any model is introduced.

### E3 — FNO rollout physics audit

Only after E2 is stable should a learned surrogate be inserted.

Structure:

```text
Ground truth trajectory
        |
        +-- direct physics audit
        |
        +-- FNO prediction
                 |
                 +-- predictive error
                 +-- divergence / vorticity drift
                 +-- energy / enstrophy drift
                 +-- spectral drift
```

Prediction quality and physics quality must remain separate receipt sections.

A low L2 prediction error must not be interpreted as automatic evidence of:

- small PDE residual;
- correct incompressibility;
- correct energy behavior;
- correct vorticity transport;
- long-horizon stability.

Recommended receipt structure:

```json
{
  "prediction": {},
  "physics": {}
}
```

### E4 — forced vs unforced scope audit

Use a dataset family that explicitly separates forced and unforced Navier–Stokes.

The experiment should apply identical diagnostics to both scopes while requiring metadata separation.

Fail closed if:

- forcing status is missing;
- forced and unforced samples are merged;
- model metadata hides the forcing term;
- output summaries compare them without retaining scope labels.

This experiment is especially important because the primary workbench itself preserves the forced Clay (C)/(D) boundary.

## 7. Second execution wave

After E1–E4 are stable:

### E5 — resolution sensitivity

Evaluate the same trajectory or analytic field at multiple effective resolutions.

Example:

```text
64x64
32x32
16x16
```

Measure when reconstruction, energy, enstrophy, derivative, or residual estimates drift beyond tolerance.

The artifact question is not merely “does lower resolution look worse?” but:

> Which checkable quantities disappear first as resolution is reduced?

### E6 — viscosity / Reynolds sensitivity

Use a controlled family where viscosity or Reynolds number varies.

Record whether the same diagnostic thresholds remain meaningful across regimes. Do not reuse one tolerance automatically across materially different flow scales.

### E7 — FNO / PINO / PINN / GFNO / KNO comparison

Use the same evaluation surface for all methods where possible.

Recommended comparison table:

| Method | Data fit | PDE residual | Divergence | Rollout stability | Compute |
|---|---:|---:|---:|---:|---:|
| FNO | | | | | |
| PINO | | | | | |
| PINN | | | | | |
| GFNO | | | | | |
| KNO | | | | | |
| Numerical solver | | | | | |

The goal is not to declare a winner.

The stronger question is:

> Which method loses which physical constraint first, under which pinned conditions?

### E8 — independent solver comparison

Use JAX-Fluids or another independent numerical implementation family.

Compare selected bounded quantities against the local workbench and Colab diagnostics.

Solver disagreement should trigger investigation, not automatic preference for either solver.

## 8. Hugging Face pinning discipline

Hugging Face repositories can change. Therefore each experiment should record as much of the following as feasible:

```text
repo id
revision / commit
config
split
file / shard
sample or trajectory id
source file sha256
local downloaded file sha256
download date
```

A repository name alone is insufficient long-term custody.

For large datasets, pin the bounded subset actually used rather than treating the entire repository as the executed artifact.

## 9. Colab runtime custody

Colab environments change over time. Every execution receipt should record:

```text
Python version
OS/runtime identifier
CPU/GPU/TPU type
CUDA version when relevant
PyTorch version
JAX version
NumPy
SciPy
huggingface_hub
datasets
neuraloperator or project-specific packages
random seed
```

The notebook should export at least:

```text
environment.json
experiment_receipt.json
```

Where useful, also export deterministic plots or arrays with hashes.

## 10. Common receipt schema

All external experiments should eventually use a common schema similar to:

```json
{
  "schema": "nsrw.external-experiment.v1",
  "experiment_id": "E2",
  "source": {},
  "environment": {},
  "parameters": {},
  "checks": {},
  "metrics": {},
  "falsifiers": {},
  "experiment_status": "PASS",
  "claim_status": "UNVERIFIED",
  "evidence_class": "EXTERNAL_REPRODUCIBLE_NUMERICAL_EXPERIMENT",
  "non_claims": []
}
```

For learned-model output use an evidence label such as:

`ML_SURROGATE_DIAGNOSTIC_NOT_PDE_PROOF`

The critical rule is:

```text
experiment_status != theorem claim status
```

A successful notebook may have:

```text
experiment_status = PASS
claim_status = UNVERIFIED
```

This is the same authority separation already used in M1–M3.

## 11. Recommended project-owned Colab artifacts

Create the following notebooks progressively:

```text
colab/NSRW_E1_TAYLOR_GREEN_ANALYTIC_CONTROL.ipynb
colab/NSRW_E2_HF_FNO_DATASET_AUDIT.ipynb
colab/NSRW_E3_FNO_ROLLOUT_PHYSICS_AUDIT.ipynb
colab/NSRW_E4_FORCED_UNFORCED_SCOPE_AUDIT.ipynb
colab/NSRW_E5_RESOLUTION_SENSITIVITY.ipynb
colab/NSRW_E6_REYNOLDS_VISCOSITY_SENSITIVITY.ipynb
colab/NSRW_E7_SURROGATE_COMPARISON.ipynb
colab/NSRW_E8_INDEPENDENT_SOLVER_COMPARISON.ipynb
```

Do not create all notebooks at once. Build and stabilize them sequentially.

## 12. Hugging Face publication direction

If the experiment lane becomes stable, a Flamehaven Hugging Face repository or organization can be used as a public experiment registry.

A suitable structure would emphasize artifacts rather than model marketing:

```text
README
experiment manifests
dataset cards / source cards
notebook links
small bounded reproducible samples
receipt JSON files
plots
hash manifests
```

Large upstream datasets should generally not be duplicated. Prefer provenance manifests and exact bounded sample identities.

## 13. Execution order

Recommended implementation order:

### Phase HF-C0 — registry

- normalize external asset metadata;
- pin revisions where possible;
- classify each source as dataset/model/Space/reference;
- record dimensionality, domain, forcing, variables, and intended use.

### Phase COLAB-C1 — analytic control

- Taylor–Green exact solution;
- no ML;
- establish common receipt format and cloud environment capture.

### Phase COLAB-C2 — dataset audit

- one pinned HF trajectory;
- spectral reconstruction;
- divergence/vorticity/energy/enstrophy diagnostics;
- deterministic receipt.

### Phase COLAB-C3 — resolution study

- controlled downsampling;
- identify which checkable physical quantities fail first.

### Phase COLAB-C4 — FNO inference

- prediction error and physical error reported separately.

### Phase COLAB-C5 — long rollout

- short vs long horizon drift;
- identify first failing physical tolerance.

### Phase COLAB-C6 — PINO/PINN/surrogate comparison

- same input surface and diagnostics where possible.

### Phase COLAB-C7 — forced/unforced sensitivity

- explicit scope mutation and metadata fail-closed gate.

### Phase COLAB-C8 — independent solver

- JAX-Fluids or equivalent implementation family;
- compare bounded quantities and investigate disagreement.

## 14. Stop conditions

Hold an experiment rather than promote it when:

- the dataset or checkpoint revision cannot be identified sufficiently;
- forced/unforced status is ambiguous;
- 2D and 3D results are being mixed;
- periodic and whole-space domains are being mixed;
- velocity and vorticity representations are being conflated;
- the notebook reports only training loss without independent diagnostics;
- environment/seed information is absent for a stochastic experiment;
- a surrogate output is described as a PDE proof;
- finite samples are described as uniform analytic estimates;
- a large dataset cannot be bounded to a reproducible subset;
- external notebook code silently changes assumptions or equations;
- the experiment result is being used to promote the OpenAI theorem claim.

## 15. Core research direction

The most useful research question for the Colab + Hugging Face lane is not:

> Can AI solve Navier–Stokes again?

The stronger and more inspectable question is:

> How does the same Navier–Stokes surface change as it passes through an analytic representation, numerical solver, dataset, learned surrogate, and executable artifact — and where does each representation begin to drift?

This creates a transformation chain:

```text
Equation
  |
Numerical solver
  |
Dataset
  |
Neural surrogate
  |
Artifact
```

At each boundary the workbench should ask:

- what was preserved?
- what approximation was introduced?
- what assumptions changed?
- which quantity can still be checked?
- which quantity became unavailable?
- what mutation or falsifier exposes the loss?

This turns Colab + Hugging Face into a Navier–Stokes claim-custody laboratory rather than a collection of demonstrations.

## 16. Relationship to current M3 work

This external lane does not replace or bypass the current M3 review.

Current M3 blockers remain authoritative for the core workbench, especially the source-domain `h` boundary and canonical-pressure axis behavior recorded in `SESSION_HANDOFF_2026-09-09_M3.md`.

Recommended sequencing:

1. preserve the current M3 hold;
2. repair and freshly verify M3 blockers;
3. in parallel or immediately afterward, implement COLAB-C1 and COLAB-C2;
4. keep all external results in `UNVERIFIED` theorem status;
5. use disagreements from the external lane as new falsification questions for later M4+ research.

The external lane is therefore complementary: it broadens the inspectable numerical surface without weakening the paper/Lean claim boundary.

## 17. Current execution gate — 2026-09-09

The first real HF/Colab execution remains intentionally held.

Current status: `E2_HELD[PINNING_INCOMPLETE]`.

Before `NSRW_E2_HF_FNO_DATASET_AUDIT.ipynb` may execute, the E2 admission contract must contain:

- pinned Hugging Face repository revision or commit;
- exact file or shard identity;
- exact sample/trajectory id;
- source/download SHA-256 where feasible.

Until those fields exist, no dataset download or numerical result is treated as an admitted experiment artifact. This hold is separate from the M3 core gate. M3 is currently `HELD_LEAN_TOOLCHAIN_AND_SOURCE_INSTANCE`; E2 can proceed once its own source custody is complete, but it cannot bypass or promote M3/M4 theorem status.
