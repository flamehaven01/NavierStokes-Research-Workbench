# `#map-north-star` — Navier–Stokes research direction

Status: adopted research principle; not an executable gate.

## North star

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
progress and should be removed or deferred. Tests, CI, slop checks, and receipts
are guardrails: they protect the research engine but are not its destination.

## Current map position

- M1: exact scaling and similarity-coordinate algebra — local support.
- M2: source-shaped leading-field interface and local diagnostics — local
  support; source profiles not instantiated.
- M3: dependent profile closure and paper–Lean crosswalk — **review held**.
  The (V_0) relation was found in Lean, so that suspected gap is falsified.
  The source-domain contract (0<h<1/100), explicit (X=0) pressure limit,
  one-sided endpoint policy, declaration-aware matching, and M3 CI replay are
  now locally verified. The supplied pressure tail still lacks an independent
  source-profile witness, and Lean build/semantic equivalence remain open.
- M3R: closure recovery — **active**. M3R-1 recovers the pinned Lean/Lake
  compiled dependency graph; M3R-2 evaluates the concrete `TailData` instance
  against the independent pressure-tail witness. Full paper–Lean semantic
  equivalence remains an open research obligation, not an invisible gate.
- M4: stress support, cone margin, and moment identities — held until the
  remaining Lean/semantic and tail-witness bridges are resolved.
- External E2: pinned 2-D vorticity reconstruction — **contract implemented;
  execution held until source revision/file/sample/hash admission**. This is
  an independent numerical observation surface, not theorem evidence.
- Later: full Theorem 4.6 conjunction audit, Lean build/dependency receipt,
  independent stable-profile or multiscale lanes, and only then any candidate
  theorem claim.

## Strategic decision

The near-term objective is not “finish reproducing 167 pages.” It is to reduce
the highest-risk semantic debt surface:

1. repair and freshly verify M3's source-domain and axis-limit contracts;
2. map each quantitative conjunct of Theorem 4.6 to an inspectable proof
   dependency;
3. independently test one materially different mechanism (stable/dynamically
   rescaled profile or multiscale cascade) against the same PDE obligations;
4. promote nothing beyond `UNVERIFIED` until a pinned Lean build and an
   obligation-by-obligation semantic comparison exist.

The external experiment lane is interleaved only where it adds a measurable
quantity or falsifier: E1 analytic control, E2 dataset-to-field reconstruction,
E3 learned-rollout drift, and E4 forced/unforced scope custody. It cannot close
the M3 hold or substitute for the missing pressure-tail witness and Lean
semantic/build bridges.

This keeps the ambitious goal visible while ensuring each stage is cumulative,
mathematically useful, and able to fail.
