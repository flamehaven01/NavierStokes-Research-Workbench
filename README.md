# Navier--Stokes Research Workbench

[![CI](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

NSRW is an open research-lab workbench for studying selected, checkable links
between Navier--Stokes papers, Lean formalizations, and bounded computational
experiments. It records what source was used, what was actually checked, and
which conclusions remain unavailable.

The project supports serious mathematical research without claiming to be a
theorem prover, production CFD solver, or solution to the Navier--Stokes
millennium problem. The OpenAI manuscript and Lean repository are important
pinned research inputs and audit benchmarks; they are not proof authority for
this project and are not vendored.

The current contribution is narrow and inspectable: preserve source identity,
state executable scope, test bounded mathematical controls, and withhold
stronger conclusions when evidence is missing. New mathematical, numerical,
CFD, and SciML investigations are research-program directions, not current
proof claims.

## Research objective

The long-range objective is deliberately ambitious: explore new, testable
directions toward the three-dimensional Navier--Stokes regularity/blowup problem.
The present workbench does not claim to answer that problem. It asks smaller
questions that can be answered honestly and reproduced:

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

## Implemented now

The pinned OpenAI construction and Lean proof graph provide a valuable compiled
formal surface. NSRW adds bounded controls implemented in this repository that can
also be reused for later Navier--Stokes candidates:

1. exact scaling and similarity-coordinate algebra;
2. differential-operator and manufactured-solution controls;
3. cylindrical leading-field and pressure-closure diagnostics;
4. side-by-side comparison of source quantifiers and executable checks;
5. parametric Support, Cone, and Moment obligation evaluators;
6. mutation-based tests of the verifier itself;
7. a typed evidence graph separating papers, formal sources, computations,
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
| M4-P fixed pilot | `PASS[SCOPED]` | Manufactured control surface passes its declared bounded checks |
| M4-P v3 replay pilot | `PASS[LOCAL_REPLAY_V0.2.3_RC]` | Schema-first admission, committed golden mutations, and 13 applicable replay cases pass locally; the live-only case is not applicable |
| M4-P v3 live release candidate | `HELD[V0.2.3_HOSTED_LIVE_PENDING]` | The earlier v0.2.2 checkpoint passed run 34579077366, but the changed v0.2.3 verifier requires a fresh exact-commit run |
| M4-S selected instance | `HELD[NONCOMPUTABLE_SOURCE_INSTANCE]` | Current source interface exposes no pinned numerical evaluator |
| Paper--Lean semantic equivalence | `OPEN_RESEARCH_OBLIGATION` | A build does not establish semantic equivalence |
| Independent selected-candidate reproduction | `UNVERIFIED` | No independent reproduction is claimed |
| Millennium-problem solution | `NOT_ESTABLISHED` | Explicit non-claim |

Status words are scoped. `PASS[LOCAL_TESTS]` is not a proof claim.
`PASS[COMPILED_TARGET]` does not mean a paper is correct, that all library
targets compile, or that two mathematical statements are equivalent.

## Public vocabulary and research posture

The project prefers plain descriptions over authority-heavy labels:

| Project term | Meaning here | Explicit non-meaning |
|---|---|---|
| evidence traceability | keeping source, scope, input, and result boundaries inspectable | truth of the underlying theorem |
| source/check comparison | recording source and executable quantifiers side by side | formal quantifier equivalence |
| required validation | a check that must succeed before an artifact is accepted | a mathematical proof |
| manufactured control | a deliberately constructed test input | the selected Navier--Stokes witness |
| structural consistency check | an optional secondary review supplied by a pinned dependency | semantic AI review or proof authority |
| research direction | a planned investigation or comparator track | a completed independent solution |

This wording is intentional. The lab's role is governance, reproducibility, and
guardrails around mathematical research. It does not use verification language
to imply a stronger result than the recorded artifact supports.

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
       required Navier--Stokes validation
                      |
                      v
       secondary structural consistency check
                      |
                      v
       deterministic receipt + non-claims
```

The required NSRW checks determine whether an artifact is accepted. A secondary
structural consistency check, supplied by an optional pinned dependency, can
flag suspicious wording or structure. Its score cannot override a missing
source hash, failed scope check, missing compiled target, or other required
condition. It is not an AI semantic engine and does not establish theorem truth.

## Navier--Stokes-specific validation pipeline

The dedicated pipeline is additional to ordinary software CI.

### Source traceability

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
- `Negative controls`: manufactured mutations that must be rejected;
- `Source/check comparison`: record source quantifiers and executable checks side by side;
  this is an audit record, not a proof of quantifier equivalence.

The active v3 M4 contract hashes each normalized Lean declaration signature,
checks ordered source fragments under the declared
`NAMED_BINDERS_AND_DATA_EXISTENTIALS` projection, and reads structured compiled
evidence rather than trusting a handwritten `PASS`. Version 3 also separates
historical replay from same-run live evidence and uses 14 committed, hashed
negative-control manifests with stage-specific expected detectors. The v1 and
v2 fixtures remain historical compatibility inputs and cannot be promoted to
v3 authority.

Checking one fixture and a finite grid remains
`SAMPLED_PARAMETRIC_DIAGNOSTIC`. It cannot be promoted to a source statement
of the form `forall F, exists R(F), forall X >= R(F)`.

## Repository layout

| Path | Responsibility |
|---|---|
| `contracts/` | Versioned research and M4 obligation schemas |
| `fixtures/` | Manufactured, negative-control, graph, and portable contract fixtures |
| `src/nsrw/contracts.py` | Source pins, theorem scope, hashes, and locator validation |
| `src/nsrw/falsification.py` | Research-contract negative controls |
| `src/nsrw/graph.py` | Typed proof/evidence graph and authority propagation |
| `src/nsrw/math_kernel/` | Scaling, operators, profiles, closure, and bounded diagnostics |
| `src/nsrw/m4_audit.py` | Source/check scope comparison, Support/Cone/Moment checks, secondary diagnostic adapter, and M4 mutations |
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

The development extra pins the optional SPAR structural-check dependency to the
reviewed public commit used by this project. No local source archive is included.

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
python -m nsrw.m4_cli fixtures/m4-parametric-pilot-v3.json \
  --evidence-root . \
  --output outputs/m4-parametric-pilot-receipt.json
```

The v3 example above is a historical receipt replay and does not claim current
Lean artifact freshness. Hosted CI separately performs the same-run clean build,
generates a live receipt through `nsrw.lean_receipt`, and verifies the live
manifest against the pinned source. The v2 fixture remains available only for
historical compatibility. Exit code `1` means a critical declared gate failed;
it does not by itself mean the mathematical theorem is false.

## CI and verification

The GitHub Actions pipeline contains three distinct jobs:

1. cross-platform Python quality: pytest, coverage, Ruff, and compilation;
2. deterministic artifact replay, structural-check dependency identity, and mutation checks;
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

## Future research directions

The first planned external artifact is a pinned 2-D periodic-vorticity comparator:
spectral velocity reconstruction, divergence, vorticity consistency, energy,
and enstrophy. It is a numerical/control surface, not evidence of a 3-D
finite-time singularity and not part of the current proof authority. See
`docs/COLAB_HUGGINGFACE_EXPERIMENT_DESIGN.md`.

## Limits and non-claims

- This software does not solve the Navier--Stokes millennium problem.
- Passing numerical samples does not prove a uniform analytic estimate.
- A manufactured profile is not the paper's selected witness.
- A Lean build verifies elaboration of the compiled declarations, not the truth
  of an informal manuscript or semantic equivalence between artifacts.
- Classical or noncomputable existence may be formally valid while exposing no
  concrete numerical instance through the current interface.
- External datasets, PINNs, FNOs, and CFD solvers are comparators and
  numerical or negative-control surfaces, not proof authorities.

The governing principle is simple: do not invent missing evidence. Missing
equations, source witnesses, parameters, or evidence remain explicitly unknown
or held.

## Documentation

- [Documentation status index](docs/README.md)
- [Research direction map](docs/NAVIER_STOKES_NORTH_STAR_MAP.md)
- [Public research language guide](docs/PUBLIC_RESEARCH_LANGUAGE.md)
- [Realistic research design](docs/REALISTIC_RESEARCH_DESIGN.md)
- [M4-P design](docs/M4_PARAMETRIC_AUDIT_DESIGN.md)
- [M4-P verifier hardening](docs/M4P_VERIFIER_HARDENING_2026-09-11.md)
- [M4-P v0.2.1 evidence-integrity patch plan](docs/M4P_V0.2.1_EVIDENCE_INTEGRITY_PATCH_PLAN.md)
- [v0.2.2 audit-alignment implementation addendum](docs/V0.2.1_SUBPATCH_AUDIT_ALIGNMENT_AND_SOURCE_INTERFACE.md)
- [v0.2.3 post-implementation audit closure](docs/V0.2.2_AUDIT_PATCH_TO_V0.2.3_CLOSURE.md)
- [M3 historical execution-assertion tombstone](docs/stage_receipts/M3_HISTORICAL_INVALIDATION.md)
- [M4-P v0.2.3 local closure receipt](docs/stage_receipts/M4P_V0.2.3_LOCAL_CLOSURE.md)
- [M4-P v0.2.2 local implementation receipt](docs/stage_receipts/M4P_V0.2.2_LOCAL_IMPLEMENTATION.md)
- [M4-P v0.2.2 hosted live receipt](docs/stage_receipts/M4P_V0.2.2_HOSTED_LIVE.md)
- [Mandatory stage checklist](docs/STAGE_CHECKLIST.md)
- [v0.2.3 release candidate notes](docs/releases/v0.2.3.md)
- [v0.2.2 release notes](docs/releases/v0.2.2.md)
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
