# M4-P Parametric Stress / Cone / Moment Audit

Status: `OPEN[V3_LOCAL_REPLAY_PASS__HOSTED_LIVE_PENDING]`

## Research boundary

M4-P tests symbolic and manufactured parametric obligations. It does not
reconstruct the source-selected witness, prove the paper equivalent to Lean,
or establish a Navier--Stokes millennium result. M4-S retains the selected
source-instance question as `HELD[NONCOMPUTABLE_SOURCE_INSTANCE]`.

## Importance and difficulty

| Phase | Purpose | Importance | Difficulty | Main failure mode |
|---|---|---:|---:|---|
| P0 | Obligation, quantifier, source, and receipt contract | Critical | High | Later checks acquire ambiguous meaning |
| P1 | Support ordering, inclusion, cutoff interaction | High | Medium | Boundary convention or region drift |
| P2 | Cone inequality, threshold dependency, margin custody | Critical | High | Sampled or reordered quantifiers promoted to a theorem |
| P3 | Exact moments, cancellation, normalization | High | Medium-high | Floating approximation hides an exact identity failure |
| P4 | Mutation and falsification surface | Critical | High | A broken verifier reports a clean receipt |

P0 and P2 carry the greatest semantic risk. P4 carries the greatest assurance
risk because it must demonstrate that invalid claims are rejected rather than
merely exercise a success path.

## Pipeline

```text
Lean source / target-specific compiled receipt
                    |
                    v
           M4 obligation manifest
       source quantifiers + artifact quantifiers
                    |
                    v
        Support / Cone / Moment evaluators
                    |
                    v
           required NSRW validation
                    |
                    v
       secondary structural consistency check
```

The required NSRW checks determine admission. The optional structural check,
implemented with the pinned SPAR package, cannot override a critical failure or
skipped source binding.

## Phase definitions

### P0 -- contract

The v3 manifest binds the formal-source commit and toolchain, target-specific
structured build receipt, source paths and file hashes, normalized declaration
signature hashes, ordered quantifier fragments, assumptions, evidence class,
claim scope, constructibility classification, evidence mode, build request, and
migration record when applicable. The quantifier projection is explicitly
limited to named binders and data existentials; it is a bounded source/check
comparison, not a general Lean parser or semantic-equivalence proof.

### P1 -- support

The initial evaluator checks finite ordered intervals, inclusion under the
declared cutoff, and boundary ordering. Its scoped result is
`PASS[MANUFACTURED_SUPPORT_FIXTURE]`, not a source-selected profile result.

### P2 -- cone

The evaluator admits only `LE` and `GE`, checks minimum margin, and rejects
cycles, malformed nodes, and dangling dependencies. Its scoped result is
`PASS[PARAMETRIC_CONE_EVALUATOR]`; it is not a numerical evaluation of
`CleanOutgoingCone`.

### P3 -- moment

Moment and normalization identities use exact rational arithmetic. No
floating tolerance may turn a failed exact cancellation into PASS. The pilot
result is `PASS[EXACT_FIXTURE_ARITHMETIC]`, not reproduction of a source moment.

### P4 -- negative controls

The required mutations change quantifier order, remove an assumption, promote
finite evidence, claim a noncomputable source instance, malform a source hash,
or drift the compiled target. A mutation is killed only when its expected
detector appears in `mutated_failures - baseline_failures`; unrelated baseline
failures cannot kill a mutation.

## Current scoped result

The P0 contract, P1 Support, P2 Cone, P3 Moment, and P4 mutation bank are
implemented locally. The v3 verifier separates historical replay from same-run
live evidence, opens deterministic JSON records, and cross-checks source and
target identities. Its 14-case staged mutation corpus uses full-manifest and
direct-evaluator expectations; the live-only missing-artifact case is not
applicable during replay.

The optional structural-check dependency is pinned by immutable revision. A
local editable installation may report different distribution metadata; that
remains diagnostic information and cannot override required validation.

The local replay pilot passes. Hosted same-run Lean validation remains required
for release. M4-P remains an open research direction because these manufactured
obligations do not establish the paper's full analytic estimates.
