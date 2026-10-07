# Navier–Stokes Research Workbench

<!-- MICA:INVOKE manifest="mica.yaml" -->

[![Software CI](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/workflows/ci.yml)
[![Checkpoint tag](https://img.shields.io/github/v/tag/flamehaven01/NavierStokes-Research-Workbench?label=checkpoint)](https://github.com/flamehaven01/NavierStokes-Research-Workbench/tags)
[![Python requirement](https://img.shields.io/badge/Python-%E2%89%A53.10-blue)](pyproject.toml)
[![Pinned Lean](https://img.shields.io/badge/pinned_Lean-4.34.0--rc2-blue)](formal/p2/README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Badges describe software CI, Git tags, environment requirements, and licensing.
They do not certify a mathematical result. A checkpoint tag is not necessarily
a published GitHub Release; P2 proof evidence lives in individual dated receipts.

NSRW is an open research-lab workbench investigating bounded mathematical
consequences of a pinned Navier–Stokes construction. The current P2 study asks
where a scale-invariant ratio fails, rather than treating scaling as sufficient
evidence that the ratio is useful. Source analysis has rejected one of our own
candidate assumptions; separate Lean modules have compiled narrow comparison
and repair-coefficient results. Reproduction tools support this research.

**Start here:** [Research roadmap](docs/EQUATION_TO_ARTIFACT_VISION_ROADMAP.md)
· [Current P2 work](#current-p2-research)
· [Install](#installation)
· [Reproduce P2](#reproduce-the-current-p2-artifacts)
· [Run software checks](#running-the-workbench)
· [Documentation index](docs/README.md)

## Current P2 research

**Evidence snapshot: 2026-10-07.** The findings and table below describe that
snapshot, not the live Colab VM. Consult the
[dated checklist](docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md) and individual
receipts for subsequent execution history.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Cdut_XJhMX6tDQX6mberM7I37sr844sM)

Opens the shared execution notebook, not a verified result. Historical outputs
are not evidence of a current successful run. Use the
[restart checklist](docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md) and pinned
inputs for execution; individual dated receipts record admitted proof evidence.

The study follows `Q = J / (M H)` into the repair geometry of the pinned
construction. Its [mathematical note](docs/M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md)
distinguishes source-derived arguments from propositions with compiled receipts.

### Research findings so far

- **A candidate assumption was rejected.** In the study's stated source domain,
  the endpoint cannot be the first mass-history zero: support geometry and exact
  endpoint cancellation imply
  `M_pulse = 0` on a nonempty terminal interval before that endpoint. This
  terminal zero plateau also makes `Q` undefined there. It is a source-derived
  algebraic consequence, not a separately compiled plateau theorem.
- **Two comparison branches have been compiled.** Strict L2 bounds the
  normalized main moments; L3 bounds the template moments. Their separately
  compiled source-linked composition proves `deltaM c < 0`.
- **The main-only second repair coefficient is compiled positive.** C01 binds
  that result to the source repair system. This component is not actual
  `c1(0)` or `c1(eta)`.
- **The actual-coefficient bridge is advancing, not closed.** C02's two
  decomposition equalities passed development compilation on 2026-10-07;
  commit-bound admission remains pending. Actual coefficient signs and the
  first-repair interior-zero formal proof remain open. The small-positive-eta
  zero argument is supported analytically, not yet formally admitted.

We falsified one of **our own candidate assumptions**, not the upstream theorem.
These findings do not establish a new Navier–Stokes solution, manuscript–Lean
equivalence, or independently novel mathematics. **Independent external
reproduction of the current P2 receipts has not yet been performed.**

### Notation in brief

For the ratio, fix a source `Profile`, a positive dilation factor `XR`, and
angular coordinate `eta`; `X` is the radial coordinate. Suppressing those fixed
arguments, the main quantities are:

| Quantity | Meaning in this study |
|---|---|
| `H(X, eta)` | The source's rescaled angular field `sqrt(2*X) * E(X, eta)`, not a history integral |
| `M(eta, X)` | Source mass history: the integral of the axial field `U(u, eta)` over `0 < u <= X` |
| `J(eta, X)` | Source `H`-weighted history: the integral of `H(u, eta) * U(u, eta)` over the same interval |
| `Q = J/(M H)` | Our candidate ratio, studied only where `M*H != 0`; degree-zero scaling alone does not give this domain condition |
| `deltaM c` | **NSRW-defined shorthand**, not an upstream declaration: `F0/A0 - F1/A1`, with `Fi = normalizedMainMoment c i` and `Ai = rowMoment (c.exponents i)` |
| `c1(eta)` | Study notation for the second **axial** repair coefficient for one fixed Profile and its corrected amplitude; not the angular-reset coefficients stored in `F.reset` |

Here `normalizedMainMoment c i = exp(-(beta c i * center c 0)) * mainMoment c i`.
The index `i` ranges over `0, 1`, and `lambda = c.lam`. The stage name **F1**
below denotes the positivity proof for `mainMoment c 1`; the notation `F1` in
the formula for `deltaM` denotes its normalized value. Exact definitions and
hypotheses are in the [P2 study](docs/M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md)
and [D module](formal/p2/P2_D_DeltaMComposition.lean).

### Current mathematical chain

Proof labels (`L1`, `F1`, `L2`, `L3`, `D`, `C01`, `C02`) name mathematical
modules. Checklist labels `C-02A/B/C` instead distinguish implementation,
development compilation, and commit-bound replay/admission of the **same C02
module**; they are not three additional mathematical results.

```text
L1 → F1 → strict L2 ─┐
                    ├→ D: deltaM < 0 → C01: main-only coefficient > 0
             L3 ────┘

OutgoingProfile → C02: actual decomposition (development compile only)
                    ↓ commit-bound replay still pending
                 C03 / C04: actual sign and continuity → Z: first-window zero
```

The two branches have distinct compiled dependencies. C02 imports only the
upstream `OutgoingProfile`, not the external F1/L2/L3/D/C01 chain; C03 is where
its decomposition must be combined with main-only positivity.

| Step | Recorded result | Evidence / next gate |
|---|---|---|
| L1 | `mainPulse z >= 0` for `z >= 0`, and `mainPulse(1/25) > 0`, confirmed | [Compiled receipt](docs/stage_receipts/P2_L1_COLAB_2026-09-12.md); not integral positivity by itself |
| F1 | `0 < mainMoment c (1 : Fin 2)` confirmed | [Compiled receipt](docs/stage_receipts/P2_F1_LOCAL_WINDOWS_2026-09-13.md) |
| strict L2 | Normalized main-moment comparison confirmed | [Compiled receipt](docs/stage_receipts/P2_L2_COLAB_2026-10-06.md) |
| L3 | Template-moment comparison confirmed | [Compiled receipt](docs/stage_receipts/P2_L3_COLAB_2026-10-06.md) |
| D | `NSRW.P2.deltaM c < 0` confirmed for the NSRW-defined difference above | [Compiled composition receipt](docs/stage_receipts/P2_D_COLAB_2026-10-06.md) |
| C01 | Main-only repair coefficient positivity confirmed | [Compiled receipt](docs/stage_receipts/P2_C01_COLAB_2026-10-06.md); not actual `c1(eta)` |
| C02 | Two decomposition equalities passed development compile; claim admission unverified | [Development handoff](colab/C02_DEVELOPMENT_2026-10-07.md); C-02C clean commit-bound replay pending |
| C03–C04 / Z | Actual coefficient sign and first-repair zero formal closure open | Separate downstream amplitude, continuity, and partial-tail obligations |

**At this snapshot, the next mathematical admission gate is C-02C**, not another
C02 development compile. The original successful development evidence is
preserved locally, but has `claim_authority: NONE`. A replay wrapper is now
implemented at [the runner checkpoint](scripts/run-p2-c02-replay.py); its existence
does not close that gate. The
[restart checklist](docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md) separates
implementation, development compilation, and receipt admission.

P1 source-atlas closure remains parallel and non-blocking. Numerical source
witness extraction and external dataset experiments remain held; they do not
replace or widen the current parametric formal claims.

## Research objective

The long-range objective is deliberately ambitious: explore new, testable
directions toward the three-dimensional Navier--Stokes regularity/blowup problem.
The present workbench does not claim to answer that problem. P2 pursues smaller
mathematical questions:

- Where is `Q` defined, and where does repair-induced cancellation obstruct its
  use as a bounded quantity?
- How do the main-pulse and template comparisons determine the main-only repair
  coefficient, and what changes when the actual amplitude is included?
- For one fixed Profile, can positivity at `eta = 0` and continuity give a
  construction-dependent positive neighborhood for the actual coefficient?
- Which partial-tail estimates would then force a mass-history zero inside the
  first repair window? What remains possible outside that neighborhood?

The current route tests a candidate, rejects unsupported assumptions, and turns
narrow analytic consequences into inspectable formal propositions. Longer-term
work may explore other quantities and constructions; this particular ratio is
not assumed to survive. Reproduction and evidence checks support that inquiry,
rather than becoming its mathematical objective.

## Reproduce the current P2 artifacts

Start with the [Lean reproduction guide](formal/p2/README.md) and the stage's
dated receipt in the table above. Each receipt identifies the proof/runner
commit, source revision, toolchain, execution commands, and admitted proposition.
Use a fresh clean checkout of that recorded NSRW commit, rather than assuming
the latest `main` reproduces historical bytes.

The source environment is `openai/NavierStokesAndEuler` at
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, with Lean `4.34.0-rc2` and the
committed dependency manifest. Stage-specific runners under `scripts/` compile
the required source target and fresh external modules in one recorded run.
They do not install dependencies or admit claims automatically. See the
[Colab execution guide](docs/P2_COLAB_AUTHORITY_RUN.md) for the executor rationale
and [Colab storage instructions](colab/README.md) for preservation.

L2-A's normalized representation/positivity bridge is distinct from **strict
L2's comparison theorem**. C02's development handoff is not a commit-bound
receipt. No current P2 claim is established by running manufactured controls.

### Public evidence access and external review

Proofs, runners, dated receipts, commands and digests are public. The original
execution ZIPs, raw logs and generated `.olean` files are currently retained in
a non-public local evidence store, **not published download assets**. A published
hash alone does not let a third party inspect those bytes or authenticate the
reported run. The public inputs support a new replay, not direct inspection of
our retained execution bundle. See the [storage policy](colab/README.md).

A reviewed public evidence bundle could improve inspection of recorded runs,
but none is promised here. Publishing one requires checking privacy, licensing,
completeness and its exact relation to the receipt. It would still not be an
independent reproduction or semantic proof audit by itself.

External review is welcome, starting with two bounded targets:

1. **Terminal zero plateau:** check the support intervals and exact endpoint
   cancellation in the [P2 study](docs/M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md).
   Look for an omitted hypothesis, coordinate mismatch or invalid inference.
   This argument has no separate compiled Lean theorem yet.
2. **D composition:** inspect the [D proof](formal/p2/P2_D_DeltaMComposition.lean)
   and [receipt](docs/stage_receipts/P2_D_COLAB_2026-10-06.md). Check the NSRW
   definition, strict-L2/L3 inputs and positivity needed for division. To test
   reproduction, use the receipt's exact commit and pinned source/toolchain,
   retaining your own commands, logs and exit codes.

Please identify the precise statement, source location and hypothesis at issue.
For a replay, include input identities and distinguish an invocation/cache
failure from a mathematical counterexample. Reading a receipt is not replaying
it; neither should be described as independent review of the entire construction.

## Supporting workbench infrastructure

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

## Historical validation and tooling surfaces

Software checkpoint: `v0.3.2` ([release notes](docs/releases/v0.3.2.md)).
The version/tag records software and documentation; it is not a new P2 proof receipt.

<details>
<summary>Earlier infrastructure checks and held lanes — separate from current P2 findings</summary>

| Surface | Status | Meaning |
|---|---|---|
| Python research kernel | `PASS[LOCAL_TESTS]` | Bounded software behavior passes the declared suite |
| M1 scaling/reconstruction | `PASS[LOCAL]` | Exact algebra and manufactured diagnostics |
| M2 analytic spine | `PASS[LOCAL]` | Profile interfaces and bounded obligations; no source profile instantiation |
| M3 engineering | `CLOSED_WITH_NONCOMPUTABLE_SOURCE_BOUNDARY` | Scoped compiled evidence is separated from witness extraction |
| M4-P fixed pilot | `PASS[SCOPED]` | Manufactured control surface passes its declared bounded checks |
| M4-P v3 replay pilot | `PASS[LOCAL_REPLAY_V0.2.3]` | Schema-first admission, committed golden mutations, and 13 applicable replay cases pass locally; the live-only case is not applicable |
| M4-P v3 hosted live | `PASS[HOSTED_LIVE_V0.2.3]` | Tagged commit `1120b77` passed the full hosted pipeline in [run 34666375341](https://github.com/flamehaven01/NavierStokes-Research-Workbench/actions/runs/34666375341) |
| M4-S selected instance | `HELD[NONCOMPUTABLE_SOURCE_INSTANCE]` | Current source interface exposes no pinned numerical evaluator |
| M5 Lean-native source interface | `PASS[LOCAL_SOURCE_DERIVED_VERTICAL_SLICE]` | Pinned `H_scaling` export and 78-node type projection are hash-bound locally. `NOT_EXECUTED[RUNTIME_MISMATCH]` concerns only its historical separately operated pytest attempt, not the current P2 Lean receipt chain. |
| M5 P1 scaling-atlas analysis | `PASS[LOCAL_REVIEWED_METADATA]` | Ten reviewed static scaling-law entries and exact `Fraction` algebra produce bounded degree-zero candidates, not Lean-derived exponents or theorem claims |
| M5 P1 source-bound atlas | `HELD[LEDGER_NOT_INDEPENDENTLY_PINNED]` | No complete 4-law/10-law same-raw export or independently pinned ten-law digest ledger exists; production admission fails closed |
| Paper--Lean semantic equivalence | `OPEN_RESEARCH_OBLIGATION` | A build does not establish semantic equivalence |
| Historical M4-S selected numerical witness reproduction | `UNVERIFIED` | Separate from P2 compiled propositions; no independent reproduction or concrete numerical evaluator is claimed |
| Millennium-problem solution | `NOT_ESTABLISHED` | Explicit non-claim |

</details>

Status words are scoped. `PASS[LOCAL_TESTS]` is not a proof claim.
`PASS[COMPILED_TARGET]` does not mean a paper is correct, that all library
targets compile, or that two mathematical statements are equivalent.

The CI badge reports the latest software pipeline, not the status of a P2
Colab proof replay. Local test success does not imply that every hosted OS/Python
job passed. The hosted Lean job checks the M4 targets; P2 claims instead retain
their separately recorded external-module receipts.

Evidence vocabulary, operational-exposure definitions and proposed application
transfer are documented in the [documentation index](docs/README.md) and
[public language guide](docs/PUBLIC_RESEARCH_LANGUAGE.md). They describe how
results are reported, not additional mathematical results or demonstrated
application capability.

## Supporting validation design

The historical validation infrastructure records source pins, declared
hypotheses, compiled dependencies, bounded numerical checks, and mutations of
the verifier itself. It does not turn text matching or finite samples into
theorem evidence. An optional structural consistency diagnostic cannot override
a failed required check or establish mathematical truth.

The [M4-P design](docs/M4_PARAMETRIC_AUDIT_DESIGN.md) and
[verifier-hardening notes](docs/M4P_VERIFIER_HARDENING_2026-09-11.md) describe
these controls in detail. They support, rather than replace, the current P2
mathematical investigation. Historical replay and same-run live evidence remain
distinct; checking a manufactured fixture is not proving the source's universal
statement.

## Repository layout

| Path | Responsibility |
|---|---|
| `contracts/` | Versioned research and M4 obligation schemas |
| `fixtures/` | Manufactured, negative-control, graph, and portable contract fixtures |
| `src/nsrw/contracts.py` | Source pins, theorem scope, hashes, and locator validation |
| `src/nsrw/falsification.py` | Research-contract negative controls |
| `src/nsrw/graph.py` | Typed proof/evidence graph and authority propagation |
| `src/nsrw/math_kernel/` | Scaling, operators, profiles, closure, and bounded diagnostics |
| `src/nsrw/m5/` | Streaming type-only Lean export normalization, bounded `H_scaling` reconstruction, and fail-closed scaling-atlas admission |
| `src/nsrw/m4_audit.py` | Source/check scope comparison, Support/Cone/Moment checks, secondary diagnostic adapter, and M4 mutations |
| `src/nsrw/external_experiments/` | Pinned external numerical experiment auditors |
| `colab/` | Project-owned notebooks; execution evidence is not prefilled |
| `formal/p2/` | Source-bound external Lean modules and their reproduction guide |
| `scripts/run-p2-*-replay.py` | Stage-specific commit-bound replay runners |
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

The GitHub Actions pipeline contains three job families:

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

## Current mathematical frontier

After C-02C's commit-bound decomposition replay, C03 must combine that equality
with C01 and the **same fixed Profile's** corrected amplitude to establish
actual `c1(0)` positivity and continuity. C04 then asks for a construction-dependent
`epsilon > 0` with positivity for `0 < eta < epsilon`. Z must separately connect
that sign to partial weighted tails and a first-repair-window mass zero.
None of these downstream propositions is admitted by C01 or C02 development
success. See the [active checklist](docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md).

## Deferred numerical comparators

The bounded E2 auditor for a 2-D periodic-vorticity comparator is implemented:
spectral velocity reconstruction, divergence, vorticity consistency, energy,
and enstrophy. A pinned, admitted execution against the external dataset remains
a future research experiment. Even when run, it is a numerical control surface,
not evidence of a 3-D finite-time singularity and not part of the current proof
authority. It is not the current active research task. See the
[external experiment design](docs/COLAB_HUGGINGFACE_EXPERIMENT_DESIGN.md).

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
- [Program roadmap: source → artifact → controlled transfer](docs/EQUATION_TO_ARTIFACT_VISION_ROADMAP.md)
- [Active P2 restart checklist](docs/NSRW_COLAB_RESTART_TASKS_2026-10-06.md)
- [P2 mathematical study](docs/M5_P2_DILATION_RATIO_OBSTRUCTION_STUDY.md)
- [Lean reproduction capsule](formal/p2/README.md)
- [Research direction map](docs/NAVIER_STOKES_NORTH_STAR_MAP.md)
- [Changelog](CHANGELOG.md)

For AI maintainers: [AGENTS.md](AGENTS.md) identifies the
[MICA manifest](mica.yaml), which selects short maintenance memory and a
playbook. Read those files directly; no external repository or Python loader
is required. They provide orientation, not permission or proof authority.
Current research state belongs to the dated checklist and receipts, not memory.

<details>
<summary>Earlier stage designs, receipts, and checkpoint notes</summary>

- [M5 Lean export and `H_scaling` vertical-slice contract](docs/M5_LEAN4EXPORT_H_SCALING_VERTICAL_SLICE.md)
- [M5 `H_scaling` local receipt](docs/stage_receipts/M5_H_SCALING_LOCAL.md)
- [M5 P1 `OutgoingDilation` scaling-atlas contract](docs/M5_OUTGOING_DILATION_SCALING_ATLAS_P1.md)
- [Public research language guide](docs/PUBLIC_RESEARCH_LANGUAGE.md)
- [Realistic research design](docs/REALISTIC_RESEARCH_DESIGN.md)
- [M4-P design](docs/M4_PARAMETRIC_AUDIT_DESIGN.md)
- [M4-P verifier hardening](docs/M4P_VERIFIER_HARDENING_2026-09-11.md)
- [M4-P v0.2.1 evidence-integrity patch plan](docs/M4P_V0.2.1_EVIDENCE_INTEGRITY_PATCH_PLAN.md)
- [v0.2.2 audit-alignment implementation addendum](docs/V0.2.1_SUBPATCH_AUDIT_ALIGNMENT_AND_SOURCE_INTERFACE.md)
- [v0.2.3 post-implementation audit closure](docs/V0.2.2_AUDIT_PATCH_TO_V0.2.3_CLOSURE.md)
- [M3 historical execution-assertion tombstone](docs/stage_receipts/M3_HISTORICAL_INVALIDATION.md)
- [M4-P v0.2.3 local closure receipt](docs/stage_receipts/M4P_V0.2.3_LOCAL_CLOSURE.md)
- [M4-P v0.2.3 release-candidate hosted receipt](docs/stage_receipts/M4P_V0.2.3_HOSTED_LIVE.md)
- [M4-P v0.2.3 final release hosted receipt](docs/stage_receipts/M4P_V0.2.3_FINAL_RELEASE_HOSTED.md)
- [M4-P v0.2.2 local implementation receipt](docs/stage_receipts/M4P_V0.2.2_LOCAL_IMPLEMENTATION.md)
- [M4-P v0.2.2 hosted live receipt](docs/stage_receipts/M4P_V0.2.2_HOSTED_LIVE.md)
- [Mandatory stage checklist](docs/STAGE_CHECKLIST.md)
- [v0.2.3 release notes](docs/releases/v0.2.3.md)
- [v0.3.0 release notes](docs/releases/v0.3.0.md)
- [v0.3.2 checkpoint notes](docs/releases/v0.3.2.md)
- [v0.2.2 release notes](docs/releases/v0.2.2.md)
- [v0.2.0 release notes](docs/releases/v0.2.0.md)

</details>

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
