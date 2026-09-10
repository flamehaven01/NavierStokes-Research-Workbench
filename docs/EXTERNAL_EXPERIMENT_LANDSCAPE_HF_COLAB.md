# External Experiment Landscape — Hugging Face + Google Colab

Date: 2026-09-09
Status: `REFERENCE_REGISTRY__EXPERIMENT_CANDIDATES__NOT_THEOREM_EVIDENCE`

## 1. Purpose

This document extends the NavierStokes Research Workbench beyond the pinned paper/Lean track into external executable references: Hugging Face datasets/models/Spaces, public notebooks, and Google Colab-compatible experiments.

The purpose is not to treat machine-learning surrogates or CFD notebooks as proof evidence for the OpenAI finite-time breakdown result. The purpose is to obtain independent controls, numerical baselines, reproducible datasets, alternative computational representations, and falsification surfaces.

Equation to Artifact boundary:

- the theorem or scientific result remains owned by the original authors;
- external datasets/models are reference or experimental evidence only;
- a model prediction is not a PDE proof;
- a low residual on sampled points is not a global analytic estimate;
- a 2D flow benchmark does not establish a 3D finite-time singularity;
- a Colab notebook is useful because its environment and output can be pinned, not because cloud execution raises mathematical authority.

## 2. Classification used in this registry

### E1 — Direct executable control

A small or moderate experiment that can be run and compared with a known analytic/numerical quantity. Suitable for independent falsification or regression testing.

### E2 — Surrogate/model benchmark

A learned Navier–Stokes solver or operator model. Useful for sensitivity, rollout, symmetry, approximation error, or model-vs-solver comparisons. Not theorem evidence.

### E3 — Dataset/reference corpus

A reproducible simulation dataset useful for independent numerical experiments or hypothesis exploration.

### E4 — Large-scale reference

Scientifically relevant but too large or expensive for routine Colab execution. Keep as a research reference or stream only a bounded subset.

## 3. Highest-priority Hugging Face candidates

### HF-NS-001 — `abelsr1710/navier-stokes-2d-fno`

URL: https://huggingface.co/datasets/abelsr1710/navier-stokes-2d-fno

Class: `E1/E3`
Priority: `HIGH`
Colab suitability: `HIGH`

Current dataset card reports:

- 1,200 trajectories;
- 64 x 64 periodic grid;
- 20 time steps;
- vorticity-form 2D incompressible Navier–Stokes;
- viscosity `nu = 1e-3`;
- total repository size about 811 MB;
- intended FNO split commonly uses 1,000 train / 200 test trajectories.

Why it is useful here:

- small enough to stage on normal Colab storage;
- periodic 2D structure is well suited to spectral derivative and Poisson reconstruction tests;
- can be used to verify our numerical differential-operator conventions independently;
- can support divergence/vorticity/energy diagnostics and rollout-drift experiments;
- source formulation is close to standard FNO Navier–Stokes benchmarks.

Boundary:

This is a 2D periodic vorticity benchmark. It has no direct authority over the 3D forced Clay (C)/(D) finite-time breakdown construction.

Recommended experiment `COLAB-E1`:

1. download one bounded subset;
2. pin dataset revision/hash;
3. load one trajectory;
4. reconstruct velocity from vorticity using the periodic Biot–Savart/Poisson relation;
5. check discrete divergence;
6. compute vorticity consistency from the reconstructed velocity;
7. compute energy/enstrophy time series;
8. perturb viscosity/forcing or spectral cutoff and record drift;
9. emit a JSON receipt containing dataset revision, trajectory id, grid, numerical scheme, tolerances, and output hashes.

## 4. Hugging Face model baselines

### HF-NS-002 — `OneScience-Group/FNO`

URL: https://huggingface.co/OneScience-Group/FNO

Class: `E2`
Priority: `HIGH`

The model card describes an independent reproduction of the Fourier Neural Operator 2D incompressible Navier–Stokes experiment. The default task takes 10 consecutive 64 x 64 vorticity frames and predicts the next 10 frames autoregressively.

Use in this project:

- baseline surrogate against a deterministic numerical trajectory;
- measure error growth by rollout horizon;
- compare physical diagnostics, not only L1 prediction loss;
- test whether a visually plausible rollout violates divergence/vorticity/energy constraints.

The correct artifact question is not “does FNO solve Navier–Stokes?” but “under what pinned inputs and horizon does the surrogate preserve or lose selected physical invariants?”

### HF-NS-003 — `OneScience-Group/GFNO`

URL: https://huggingface.co/OneScience-Group/GFNO

Class: `E2`
Priority: `MEDIUM-HIGH`

GFNO adds C4/D4 geometric equivariance to FNO-like spectral learning and predicts 2D Navier–Stokes time series.

Potential experiment:

- rotate/reflect the same initial vorticity field;
- run FNO and GFNO;
- compare equivariance error separately from physical residual error.

This is useful because it creates a clean falsifier: a model may have low prediction loss but fail a known symmetry relation.

### HF-NS-004 — `OneScience-Group/KNO`

URL: https://huggingface.co/OneScience-Group/KNO

Class: `E2`
Priority: `MEDIUM`

The model package provides Koopman Neural Operator weights for a standard Navier–Stokes dataset and inference/evaluation code.

Potential use:

- compare FNO vs KNO error accumulation;
- inspect whether different learned operator families fail on the same trajectories;
- use disagreement as a candidate-selection signal, not as mathematical evidence.

### HF-NS-005 — `polymathic-ai/walrus_ft_pdearena_ins`

Parent/reference: https://huggingface.co/polymathic-ai/walrus

Class: `E2/E4`
Priority: `MEDIUM`

The Walrus model card lists a fine-tuned checkpoint for PDEArena conditioned incompressible Navier–Stokes. This is potentially useful later as a cross-domain foundation-model baseline.

Do not place this in the first experiment wave. Its value comes after we have deterministic solver and FNO/PINN baselines.

## 5. Hugging Face dataset families

### HF-NS-006 — PDEInvBench

URL: https://huggingface.co/datasets/DabbyOWL/PDE_Inverse_Problem_Benchmarking

Class: `E3`
Priority: `HIGH`

The dataset includes multiple Navier–Stokes regimes:

- `navier-stokes-forced-2d`;
- `navier-stokes-forced-2d-2048`;
- `navier-stokes-unforced-2d`;
- train/validation/test plus out-of-distribution and extreme-OOD splits.

The forced turbulent dataset uses a Kolmogorov-type forcing in vorticity form. The unforced dataset spans viscosity/Reynolds-number variation.

Why this is especially valuable:

- forced vs unforced is an explicit axis, matching one of the key authority boundaries of our workbench;
- OOD splits are ideal for testing whether learned models preserve physical constraints when generalization degrades;
- inverse-problem framing allows viscosity-identification experiments.

Recommended experiment `COLAB-E2`:

Take a very small forced and unforced matched subset. Verify that our experiment metadata never merges those scopes. Train no model initially. First compute identical diagnostics across both datasets and confirm the receipt records forcing status explicitly.

### HF-NS-007 — `pdearena/NavierStokes-2D`

URL: https://huggingface.co/datasets/pdearena/NavierStokes-2D

Class: `E3/E4`
Priority: `MEDIUM-HIGH`

Current repository size is about 43 GB. This is too large for routine full Colab download, but a bounded sample or streaming strategy may be appropriate.

Use later for architecture-independent validation and conditioned incompressible Navier–Stokes experiments.

### HF-NS-008 — PreGen Navier–Stokes 2D

URL: https://huggingface.co/datasets/sage-lab/PreGen-NavierStokes-2D

Class: `E4`
Priority: `REFERENCE-HIGH / EXECUTION-LOW`

The current dataset card describes:

- about 501 GB hosted data;
- 6,400 trajectories per difficulty file;
- 20 time steps;
- 128 x 128 grid;
- OpenFOAM `icoFoam` simulations;
- difficulty axes based on geometry and Reynolds number.

This dataset is highly relevant for studying difficulty transfer and failure under increasing flow complexity, but it is not appropriate for a first Colab experiment.

Use later for a targeted “easy -> medium -> hard” falsification study with selected shards only.

### HF-NS-009 — The Well `shear_flow`

URL: https://huggingface.co/datasets/polymathic-ai/shear_flow
Repository: https://github.com/PolymathicAI/the_well
Visualization Space: https://huggingface.co/spaces/polymathic-ai/TheWell

Class: `E4`
Priority: `REFERENCE-HIGH`

The Well is a 15 TB multi-physics simulation collection. Its `shear_flow` dataset alone is currently about 471 GB on Hugging Face. The package supports direct HF streaming with `hf://datasets/polymathic-ai/`.

Why retain it:

- realistic turbulent/shear-flow reference;
- unified loader and benchmark models;
- Hugging Face Space allows visual inspection before data acquisition;
- useful later for transfer/generalization questions.

Do not download the full dataset into Colab. Only bounded streaming or selected samples are acceptable for our artifact track.

## 6. Google Colab and notebook references

### COLAB-REF-001 — Taylor–Green vortex PINN

Repository: https://github.com/mattialoszach/navier-stokes-pinn
Notebook: `taylor-green-vortex-pinn.ipynb`
Direct Colab form:
https://colab.research.google.com/github/mattialoszach/navier-stokes-pinn/blob/main/taylor-green-vortex-pinn.ipynb

Class: `E1`
Priority: `VERY HIGH`

The notebook applies a PINN to the 2D incompressible Taylor–Green vortex, which has an analytic solution.

This is an excellent first cloud control because our local workbench already uses Taylor–Green as a falsified negative control for a different purpose. We can keep those roles separate:

- local Taylor–Green negative control: demonstrates that a convenient ansatz must not be inflated into a blowup claim;
- Colab Taylor–Green PINN: measures how a learned approximation approaches a known analytic flow and where PDE residual/field error diverge.

Recommended artifact outputs:

- pinned notebook source hash;
- package versions and accelerator type;
- random seed;
- training-point count;
- analytic field error;
- continuity residual;
- momentum residual;
- rerun variability across at least 3 seeds.

### COLAB-REF-002 — JAX-Fluids notebooks

Repository/reference: https://github.com/tumaer/JAXFLUIDS

The JAX-Fluids project documents Google Colab-compatible notebooks including:

- Taylor-Green Vortex;
- Cylinder Flow;
- Laminar Channel Flow;
- automatic differentiation;
- neural networks in JAX-Fluids.

Class: `E1/E3`
Priority: `HIGH`

JAX-Fluids is a differentiable finite-volume CFD framework with CPU/GPU/TPU support. It is useful as an independent numerical implementation family.

Important boundary:

JAX-Fluids is primarily a CFD solver and includes compressible/two-phase capabilities. A successful Taylor–Green or cylinder simulation is numerical reference evidence, not evidence for the exact incompressible 3D source theorem.

Recommended use:

- execute Taylor–Green using an independent solver stack;
- record grid/order/time-step sensitivity;
- compare numerical derivatives/residual trends against our own finite-difference kernel;
- use solver disagreement as a diagnostic trigger.

### COLAB-REF-003 — NeuralOperator bootcamp

Repository: https://github.com/neuraloperator/bootcamp

The Caltech AI4Science bootcamp covers FNO/NeuralOp and learning Navier–Stokes, plus PINN/PINO material and a Navier–Stokes mini-project.

Class: `E2/METHOD_REFERENCE`
Priority: `MEDIUM-HIGH`

Useful for building a clean instructional Colab and for checking expected NeuralOperator workflows before we create a project-specific notebook.

### COLAB-REF-004 — PINO Navier–Stokes reference implementation

Repository: https://github.com/neuraloperator/physics_informed

Class: `E2/METHOD_REFERENCE`
Priority: `HIGH`

The repository includes long-rollout 2D Navier–Stokes data and Re=500 experiments, including FNO vs PINO configurations and physics-informed fine-tuning.

This is valuable for a later question:

Does adding PDE residual information reduce long-horizon physical drift relative to a purely data-driven FNO under the same dataset and evaluation surface?

## 7. NVIDIA PhysicsNeMo reference

Repository: https://github.com/NVIDIA/physicsnemo
Lid-driven cavity PINN example:
`examples/cfd/ldc_pinns/train.py`

Class: `METHOD_REFERENCE/E1`
Priority: `MEDIUM-HIGH`

PhysicsNeMo provides an explicit symbolic steady 2D incompressible Navier–Stokes PINN example with continuity and momentum residuals.

This is useful for checking our PDE residual definitions against a second implementation and for designing a later lid-driven-cavity benchmark.

Do not let framework agreement substitute for analytic validation.

## 8. Proposed project-specific Google Colab artifacts

Instead of merely linking external notebooks, create our own narrow Colab notebooks whose outputs feed the workbench.

### `colab/NSRW_E1_TAYLOR_GREEN_PINN_AUDIT.ipynb`

Purpose:

- reproduce analytic Taylor–Green fields;
- optionally train a small PINN;
- calculate field error and PDE residual separately;
- show that low training loss does not automatically imply uniformly low physical error;
- export `taylor-green-pinn-audit-receipt.json`.

### `colab/NSRW_E2_HF_FNO_DATASET_AUDIT.ipynb`

Purpose:

- download a pinned subset of `abelsr1710/navier-stokes-2d-fno`;
- verify tensor shape and dataset identity;
- reconstruct velocity from vorticity spectrally;
- compute divergence, vorticity reconstruction error, energy, and enstrophy;
- export a deterministic receipt.

### `colab/NSRW_E3_FNO_ROLLOUT_PHYSICS_AUDIT.ipynb`

Purpose:

- load a pinned FNO checkpoint;
- predict future vorticity frames;
- compare predictive error and physical-diagnostic error by rollout horizon;
- record the first horizon where a selected physical tolerance fails.

### `colab/NSRW_E4_FORCED_UNFORCED_SCOPE_AUDIT.ipynb`

Purpose:

- sample PDEInvBench forced and unforced datasets;
- use the same diagnostics on both;
- prove only that the experiment pipeline distinguishes scopes and metadata correctly;
- fail closed if the forcing metadata is absent or merged.

## 9. Experimental ladder

Recommended order after M3 blockers are repaired:

1. `COLAB-E0`: analytic Taylor–Green only, no ML — validate cloud environment and receipt format.
2. `COLAB-E1`: Taylor–Green PINN — separate field error from residual error.
3. `COLAB-E2`: Hugging Face 2D FNO dataset audit — no learned model yet.
4. `COLAB-E3`: FNO rollout audit — learned model vs physical diagnostics.
5. `COLAB-E4`: forced/unforced PDEInvBench scope audit.
6. `COLAB-E5`: FNO vs PINO vs GFNO/KNO comparison.
7. `COLAB-E6`: JAX-Fluids independent-solver comparison.
8. only later: The Well / PreGen / PDEArena large-scale experiments.

## 10. Receipt fields required for every external experiment

Every Colab/Hugging Face experiment should emit at least:

- experiment id;
- date/time;
- source URL/repository id;
- dataset/model revision or commit when available;
- source file/checkpoint hash where feasible;
- runtime (`python`, CUDA, GPU/TPU/CPU);
- package versions;
- random seed;
- equation form and domain;
- forced/unforced label;
- viscosity/Reynolds parameters;
- spatial/temporal resolution;
- numerical differentiation scheme;
- sample ids;
- tolerance values;
- measured outputs;
- check status;
- evidence class;
- explicit non-claims.

A recommended evidence label is:

`EXTERNAL_REPRODUCIBLE_NUMERICAL_EXPERIMENT`

For learned-model output:

`ML_SURROGATE_DIAGNOSTIC_NOT_PDE_PROOF`

## 11. Stop conditions

Hold an external experiment rather than promote it when:

- the dataset revision cannot be pinned;
- forced/unforced status is ambiguous;
- the equation/domain differs materially but is not documented;
- the notebook only reports training loss without independent physical diagnostics;
- random seeds/environment are absent and the result is unstable;
- a surrogate prediction is being treated as a solution proof;
- a 2D result is being extrapolated to the 3D theorem;
- a finite sample is being described as a uniform estimate;
- a large dataset cannot be bounded to a reproducible subset.

## 12. Current recommendation

The highest-value next external experiment is not a giant training run.

It is a small project-owned Google Colab that combines:

1. the 811 MB Hugging Face FNO Navier–Stokes dataset;
2. deterministic spectral reconstruction/diagnostics;
3. one pinned trajectory/subset;
4. a machine-readable receipt;
5. explicit forced/2D/periodic/non-proof boundaries.

This gives the Equation to Artifact project an independent, cloud-runnable numerical lane without confusing neural-operator performance with the OpenAI theorem claim.

After that baseline is stable, add Taylor–Green PINN and FNO/PINO rollout comparisons.
