# M4-P Parametric Stress / Cone / Moment Audit

Status: `IN_PROGRESS__TARGET_BUILDS_AND_SPAR_IDENTITY_HELD`

## North-star boundary

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
             NSRW critical hard gate
                    |
                    v
          SPAR secondary claim diagnostic
```

The NSRW hard gate owns admission. SPAR's aggregate score and journal verdict
are diagnostics and cannot override a critical failure or skipped source
binding.

## Phase definitions

### P0 -- contract

The versioned manifest binds the formal-source commit, target-specific build
records, source paths and hashes, ordered quantifier prefixes, assumptions,
evidence class, claim scope, and constructibility classification.

### P1 -- support

The initial evaluator checks finite ordered intervals, inclusion under the
declared cutoff, and boundary ordering. The pilot is a manufactured fixture,
not the source-selected profile.

### P2 -- cone

The evaluator checks declared inequality direction, minimum margin, and an
acyclic threshold-dependency graph. Exact agreement of source and artifact
quantifier prefixes is required for symbolic claims.

### P3 -- moment

Moment and normalization identities use exact rational arithmetic. No
floating tolerance may turn a failed exact cancellation into PASS.

### P4 -- falsification

The required mutations change quantifier order, remove an assumption, promote
finite evidence, claim a noncomputable source instance, malform a source hash,
or drift the compiled target. Every mutation must be killed.

## Current scoped result

The P0 contract, P1 evaluator, P2/P3 evaluator code, and P4 mutation bank are
implemented. Focused tests pass. The live pilot remains HELD because
`+NavierStokes.OutgoingCone` and `+NavierStokes.NominalConeAssembly` do not yet
have scoped compiled receipts in the manifest. The installed SPAR identity is
also held: imported source reports `0.6.0`, while editable distribution
metadata reports `0.1.4`.

This is an active M4-P implementation state, not an M4-P completion claim.
