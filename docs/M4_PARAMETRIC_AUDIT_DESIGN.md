# M4-P Parametric Stress / Cone / Moment Audit

Status: `OPEN[PARAMETRIC_ONLY]__PASS[V0.2.3_HOSTED_LIVE_SCOPED]`

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
| P2 | Cone inequality, threshold dependency, and margin checks | Critical | High | Sampled or reordered quantifiers promoted to a theorem |
| P3 | Exact moments, cancellation, normalization | High | Medium-high | Floating approximation hides an exact identity failure |
| P4 | Mutation and negative-control surface | Critical | High | A broken verifier reports a clean receipt |

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
supplied by a pinned dependency, cannot override a critical failure or
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
or drift the compiled target. Fourteen hashed, pre-mutated JSON manifests make
the inputs independently inspectable. A mutation is rejected only when its expected
detector appears in `mutated_failures - baseline_failures`; unrelated baseline
failures cannot kill a mutation.

## Current scoped result

The P0 contract, P1 Support, P2 Cone, P3 Moment, and P4 mutation bank are
implemented locally. The v3 verifier separates historical replay from same-run
live evidence, admits strict JSON through its declared schema before runtime
semantics, and cross-checks source and target identities. Its 14 committed
mutation manifests use full-manifest and direct-evaluator expectations; the
live-only missing-artifact case is not applicable during replay.

The optional structural-check dependency is pinned by immutable revision. A
local editable installation may report different distribution metadata; that
remains diagnostic information and cannot override required validation.

The v0.2.3 local replay pilot passes with 13 applicable cases rejected and one
live-only case marked not applicable. GitHub Actions run `34579077366` remains
historical evidence for the v0.2.2 implementation checkpoint; it does not
promote the changed v0.2.3 verifier. M4-P remains an open research direction
because a fresh exact-commit hosted run is pending and these manufactured
obligations do not establish the paper's full analytic estimates.
