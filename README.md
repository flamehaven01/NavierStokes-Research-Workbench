# Navier--Stokes Research Workbench

[![CI](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An evidence-bound research environment for turning Navier--Stokes arguments,
formal statements, numerical constructions, and falsification tests into
inspectable artifacts.

This is an independent research program. It is not a wrapper around one paper,
not a repackaging of OpenAI's Lean repository, and not an assertion that the
Navier--Stokes millennium problem has been solved. The OpenAI manuscript and
Lean formalization are important source assets and adversarial benchmarks, but
they are one input lane within a broader program of mathematical reconstruction,
formal dependency analysis, independent numerical controls, and claim-scope
verification.

## Research objective

The long-range objective is deliberately ambitious: develop new, testable
directions toward the three-dimensional Navier--Stokes regularity/blowup problem.
The workbench supports that objective by asking smaller questions that can be
answered honestly and reproduced:

- Which analytic identities can be derived independently from declared equations?
- Which support, cone, moment, pressure-tail, and scaling obligations are actually
  consumed by a candidate construction?
- Where does a formal existence proof stop exposing computational content?
- Which claims are theorem-level, symbolic, sampled, manufactured, or still unknown?
- Can a verifier detect quantifier drift, missing assumptions, stale source bindings,
  and forced-to-unforced scope inflation?
- Which numerical experiments can falsify intermediate assumptions without being
  misrepresented as proof evidence?

The goal is not to generate a persuasive narrative. It is to create a chain of
artifacts from equations to executable checks, with every loss of authority made
visible.

## What makes this project independent

The current OpenAI construction and Lean proof graph provide a valuable compiled
formal surface. They do not define the full research agenda. NSRW adds independent
layers that remain useful for other Navier--Stokes constructions:

1. exact scaling and similarity-coordinate algebra;
2. differential-operator and manufactured-solution controls;
3. cylindrical leading-field and pressure-closure diagnostics;
4. source-versus-executable quantifier custody;
5. parametric Support, Cone, and Moment obligation evaluators;
6. mutation-based tests of the verifier itself;
7. external CFD, spectral, PINN, and neural-operator comparison surfaces;
8. a typed evidence graph separating papers, formal sources, computations,
   receipts, hypotheses, and non-claims.

No OpenAI source code, manuscript, or PDF is vendored here. Users obtain those
artifacts from their original sources and bind them by revision and hash. This
project is not affiliated with or endorsed by OpenAI.

## Current evidence status

| Surface | Status | Meaning |
|---|---|---|
| Python research kernel | `PASS[LOCAL_TESTS]` | Bounded software behavior passes the declared suite |
| M1 scaling/reconstruction | `PASS[LOCAL]` | Exact algebra and manufactured diagnostics |
| M2 analytic spine | `PASS[LOCAL]` | Profile interfaces and bounded obligations; no source profile instantiation |
| M3 engineering | `CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY` | Scoped compiled evidence is separated from witness extraction |
| M4-P parametric lane | `OPEN[HARDENED_PILOT_GATE_PASS]` | Manufactured evaluators pass; source signatures, compiled receipts, and 6/6 mutation deltas are bound |
| M4-S selected instance | `HELD[NONCOMPUTABLE_SOURCE_INSTANCE]` | Current source interface exposes no pinned numerical evaluator |
| Paper--Lean semantic equivalence | `OPEN_RESEARCH_OBLIGATION` | A build does not establish semantic equivalence |
| Independent selected-candidate reproduction | `UNVERIFIED` | No independent reproduction is claimed |
| Millennium-problem solution | `NOT_ESTABLISHED` | Explicit non-claim |

Status words are scoped. `PASS[LOCAL_TESTS]` is not a proof claim.
`PASS[COMPILED_TARGET]` does not mean a paper is correct, that all library
targets compile, or that two mathematical statements are equivalent.

## Architecture

```text
Primary papers / datasets / formal repositories
                      |
                      v
          pinned source and claim contracts
                      |
                      v
      equation reconstruction + proof dependency graph
                      |
          +-----------+-----------+
          |                       |
          v                       v
 exact/symbolic checks      numerical controls
          |                       |
          +-----------+-----------+
                      v
       Navier--Stokes hard evidence gate
                      |
                      v
       SPAR secondary claim-drift review
                      |
                      v
       deterministic receipt + non-claims
```

The NSRW hard gate owns admission. SPAR helps review claim/evidence consistency,
but its aggregate score cannot override a missing source hash, a failed
quantifier check, a missing compiled target, or another critical obligation.

## Navier--Stokes-specific validation pipeline

The dedicated pipeline is additional to ordinary software CI.

### Source custody

- pin the formal repository commit and primary-artifact hashes;
- distinguish the primary PDF from lossy searchable transports;
- validate theorem and paper locators without calling text presence a proof;
- preserve forced/unforced, dimension, domain, and initial-data hypotheses.

### Formal dependency evidence

- read the upstream `lean-toolchain` rather than installing an arbitrary version;
- compile only declared targets required by the current stage;
- retain target-specific `.olean` hashes and dependency outputs;
- distinguish scoped target success from a full-library build;
- keep paper--Lean semantic equivalence as a separate obligation.

### M4-P mathematical obligations

- `Support`: inclusion, region ordering, cutoff interaction;
- `Cone`: inequality direction, threshold dependencies, margin propagation;
- `Moment`: exact cancellation and normalization using rational arithmetic;
- `Falsification`: manufactured mutations that must be rejected;
- `Quantifier custody`: record source and executable quantifiers side by side.

The active v2 M4 contract also hashes each normalized Lean declaration
signature, checks ordered source fragments under the declared
`NAMED_BINDERS_AND_DATA_EXISTENTIALS` projection, and opens the structured
compiled receipt rather than trusting a handwritten `PASS`. The retained v1
schema and fixture are historical and are not accepted by the v2 runtime.

Checking one fixture and a finite grid remains
`SAMPLED_PARAMETRIC_DIAGNOSTIC`. It cannot be promoted to a source statement
of the form `forall F, exists R(F), forall X >= R(F)`.

## Repository layout

| Path | Responsibility |
|---|---|
| `contracts/` | Versioned research and M4 obligation schemas |
| `fixtures/` | Manufactured, negative-control, graph, and portable contract fixtures |
| `src/nsrw/contracts.py` | Source pins, theorem scope, hashes, and locator validation |
| `src/nsrw/falsification.py` | Research-contract mutation gate |
| `src/nsrw/graph.py` | Typed proof/evidence graph and authority propagation |
| `src/nsrw/math_kernel/` | Scaling, operators, profiles, closure, and bounded diagnostics |
| `src/nsrw/m4_audit.py` | Quantifier custody, Support/Cone/Moment checks, SPAR adapter, M4 mutations |
| `src/nsrw/external_experiments/` | Pinned external numerical experiment auditors |
| `colab/` | Project-owned notebooks; execution evidence is not prefilled |
| `docs/` | Designs, checklists, boundaries, receipts, and research map |

## Installation

Python 3.10 or newer is required.

```bash
git clone https://github.com/flamehaven01/NavierStokes-Research-Workbench.git
cd NavierStokes-Research-Workbench
python -m pip install -e ".[dev]"
```

The development extra pins SPAR to the reviewed public commit used by this
project. No local source archive is included.

## Running the workbench

Portable contract-only and manufactured checks:

```bash
python -m nsrw --no-verify-sources --output outputs/research-receipt.json
python -m nsrw.math_cli --output outputs/math-kernel-receipt.json
python -m nsrw.analytic_cli --output outputs/analytic-spine-receipt.json
python -m nsrw.m3_cli > outputs/m3-closure-receipt.json
```

Source-bound checks require external artifacts. Copy the example contract and
set its locators to your own source files; do not commit private local paths.
For M3, pass `--lean-root` or set `NSRW_LEAN_ROOT`.

```bash
python -m nsrw.m3_evidence_cli --lean-root /path/to/NavierStokesAndEuler
python -m nsrw.m4_cli fixtures/m4-parametric-pilot-v2.json \
  --lean-root /path/to/NavierStokesAndEuler \
  --output outputs/m4-parametric-pilot-receipt.json
```

The current v2 fixture returns `0` only when the pinned source signatures and
structured compiled receipt are both available and match. Exit code `1` means
a critical source, quantifier-fragment, receipt, or target binding is missing
or invalid. It does not by itself mean the mathematical theorem is false.

## CI and verification

The GitHub Actions pipeline contains three distinct jobs:

1. cross-platform Python quality: pytest, coverage, Ruff, and compilation;
2. deterministic artifact replay plus SPAR identity and mutation checks;
3. pinned upstream Lean builds for the exact Navier--Stokes targets consumed by M4.

Generated runtime outputs are ignored by Git. Reviewable bounded receipts live
under `docs/stage_receipts/`. A hosted CI PASS remains scoped to the workflow's
declared targets and cannot establish paper correctness or theorem equivalence.

Local verification:

```bash
python -m pytest
python -m ruff check src tests
python -m compileall -q src
```

## External experiments

The first planned external artifact is a pinned 2-D periodic-vorticity audit:
spectral velocity reconstruction, divergence, vorticity consistency, energy,
and enstrophy. It is a numerical/control surface, not evidence of a 3-D
finite-time singularity. See `docs/COLAB_HUGGINGFACE_EXPERIMENT_DESIGN.md`.

## Limits and non-claims

- This software does not solve the Navier--Stokes millennium problem.
- Passing numerical samples does not prove a uniform analytic estimate.
- A manufactured profile is not the paper's selected witness.
- A Lean build verifies elaboration of the compiled declarations, not the truth
  of an informal manuscript or semantic equivalence between artifacts.
- Classical or noncomputable existence may be formally valid while exposing no
  concrete numerical instance through the current interface.
- External datasets, PINNs, FNOs, and CFD solvers are comparators and
  falsification surfaces, not proof authorities.

The governing principle is `ABSTAIN > FABRICATE`: missing equations, source
witnesses, parameters, or evidence remain explicitly unknown or held.

## Documentation

- [North-star map](docs/NAVIER_STOKES_NORTH_STAR_MAP.md)
- [Realistic research design](docs/REALISTIC_RESEARCH_DESIGN.md)
- [M4-P design](docs/M4_PARAMETRIC_AUDIT_DESIGN.md)
- [M4-P verifier hardening](docs/M4P_VERIFIER_HARDENING_2026-09-11.md)
- [Mandatory stage checklist](docs/STAGE_CHECKLIST.md)
- [v0.2.0 release notes](docs/releases/v0.2.0.md)
- [Changelog](CHANGELOG.md)

## Upstream references

- [OpenAI research announcement](https://openai.com/index/navier-stokes-solution/)
- [OpenAI Lean formalization](https://github.com/openai/NavierStokesAndEuler)
- [Clay Mathematics Institute problem description](https://www.claymath.org/millennium/navier-stokes-equation/)

These links identify research inputs. They do not transfer proof authority to
this workbench or imply upstream endorsement.

## License

Original code and documentation in this repository are licensed under the
[MIT License](LICENSE). External papers, datasets, formal repositories, and
other referenced artifacts retain their own licenses and are not relicensed here.
