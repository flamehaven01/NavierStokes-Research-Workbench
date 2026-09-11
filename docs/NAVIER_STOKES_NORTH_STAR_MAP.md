# Navier--Stokes research direction map

Status: adopted research principle; not an executable gate.

This document was previously called the internal `#map-north-star`. The plain
title is used publicly; the research objective is unchanged.

## Long-range objective

The workbench exists to discover, isolate, and eventually prove a mathematical
mechanism that closes a genuine gap in the three-dimensional incompressible
Navier–Stokes problem. The long-horizon goal is a rigorous contribution toward
the Clay problem. The immediate product is not a larger collection of receipts
or a claim of proof; it is a sharper, reproducible understanding of which
analytic obligations are true, false, or still missing.

## Map

```text
Primary source / formal source
            ↓
Exact mathematical obligation
            ↓
Independent reconstruction or counterexample
            ↓
Quantitative estimate with explicit hypotheses
            ↓
Formal-semantic bridge
            ↓
Candidate theorem contribution
```

The OpenAI construction is the reproduction lane and a valuable source of
scales, profile identities, stress geometry, and Lean proof structure. It is not
the novelty lane. A new lane must differ in its central mechanism, not merely
rename the same annular stress–pulse architecture.

## Architecture test for every artifact

Before adding code, a ledger, a receipt, or a new research lane, ask:

1. Does it expose a mathematical quantity or dependency that was previously
   opaque?
2. Does it support an independent derivation or kill a concrete alternative?
3. Does it preserve the exact source hypotheses and their boundary cases?
4. Does it produce the next falsifier or proof obligation needed for the
   Navier–Stokes argument?

If all answers are no, the artifact is process growth rather than research
progress and should be removed or deferred. Tests, CI, code-quality heuristic
checks, and receipts
are guardrails: they protect the research engine but are not its destination.

## Current map position

- M1: exact scaling and similarity-coordinate algebra — local support.
- M2: source-shaped leading-field interface and local diagnostics — local
  support; source profiles not instantiated.
- M3: dependent profile closure and paper–Lean crosswalk —
  **closed with a noncomputable source boundary**. The source-domain contract,
  axis pressure limit, endpoint policy, declaration matching, and scoped Lean
  compilation are verified. A concrete selected `TailData` evaluator remains
  unavailable through the current source interface.
- M3R: closure recovery — **completed for the scoped compiled dependency
  target**. Its remaining source-instance question is carried by M4-S rather
  than silently reopening M3 engineering.
- M4-P: Support, Cone, Moment, and verifier falsification — **active**. The v2
  pilot gate binds normalized Lean signatures and ordered quantifier fragments,
  cross-verifies structured build receipts, and uses baseline-delta mutation
  verdicts. Its evaluators remain manufactured controls, not source theorem
  reproductions.
- M4-S: selected source instance — **held** because the current formal source
  exposes no pinned numerical evaluator for the existential witness.
- External E2: pinned 2-D vorticity reconstruction — **contract implemented;
  execution held until source revision/file/sample/hash admission**. This is
  an independent numerical observation surface, not theorem evidence.
- Later: full Theorem 4.6 conjunction audit, Lean build/dependency receipt,
  independent stable-profile or multiscale lanes, and only then any candidate
  theorem claim.

## Strategic decision

The near-term objective is not “finish reproducing 167 pages.” It is to reduce
the highest-risk semantic debt surface:

1. map each quantitative conjunct of Theorem 4.6 to an inspectable proof
   dependency;
2. replace manufactured M4-P controls one family at a time with source-derived
   Support, Cone, and Moment obligations without widening their claim scope;
3. independently test one materially different mechanism (stable/dynamically
   rescaled profile or multiscale cascade) against the same PDE obligations;
4. promote nothing beyond `UNVERIFIED` until the pinned Lean build and an
   obligation-by-obligation semantic comparison exist.

The external experiment lane is interleaved only where it adds a measurable
quantity or falsifier: E1 analytic control, E2 dataset-to-field reconstruction,
E3 learned-rollout drift, and E4 forced/unforced scope custody. It cannot close
the M4-S hold or substitute for the missing pressure-tail witness and
paper–Lean semantic bridge.

This keeps the ambitious goal visible while ensuring each stage is cumulative,
mathematically useful, and able to fail.
