# Navier--Stokes research direction map

Document status: `ADOPTED`
Scope: stable mathematical research policy; not a dated status report and not an
execution gate.

The filename preserves the project's historical internal "north-star" naming.
Public summaries should call this the research direction map.

## 1. Long-range objective

The workbench exists to discover, isolate, and eventually prove a mathematical
mechanism that closes a genuine gap in the three-dimensional incompressible
Navier--Stokes problem.

The long-horizon objective is a rigorous theorem-level contribution. The
immediate product is a sharper, reproducible understanding of which analytic
obligations are true, false, held, or still missing.

Receipts and CI are guardrails. They are not the mathematical destination.

## 2. Research directions

Verification boundaries constrain claims; they do not constrain mathematical
investigation. Exploratory freedom does not remove mathematical obligations.

| Direction | Core question | Legitimate output |
| --- | --- | --- |
| Source reproduction | What does the pinned source actually state? | source-bound executable surface or explicit unresolved loss |
| Mathematical analysis | Which quantities and inequalities are genuine bottlenecks? | derivation, obstruction, open lemma, counterexample |
| Candidate exploration | Can a materially different mechanism meet the PDE obligations? | candidate, failed candidate, or new proof obligation |

The source construction is a research input and source of definitions,
scalings, geometry, and formal structure. It is not the novelty claim.

## 3. Stable mathematical map

~~~text
primary source / formal source
            |
            v
exact mathematical obligation
            |
            v
independent reconstruction or counterexample
            |
            v
quantitative estimate with explicit hypotheses
            |
            v
formal-semantic bridge
            |
            v
candidate theorem contribution
~~~

## 4. Architecture test

Before adding code, a ledger, a receipt, or a new research direction, ask:

1. Does it expose a mathematical quantity or dependency that was previously
   opaque?
2. Does it support an independent derivation or kill a concrete alternative?
3. Does it preserve source hypotheses and boundary cases?
4. Does it produce the next falsifier or proof obligation?

If all answers are no, the artifact is process growth rather than research
progress and should be removed or deferred.

## 5. Nontriviality and semantic-review gate

A proposition should not be described as an independent nontrivial mathematical
result merely because it was not copied verbatim from the source.

Before that label is used, record:

- exact source lineage;
- proof/derivation;
- why the statement is not a direct restatement;
- paper/formal semantic comparison;
- expert review appropriate to the analytic content.

Where feasible, the reviewer should be operationally separate from the artifact
author. A blind review may be used: show the proposed proposition and source
surface to a reviewer and ask whether it follows immediately from the source or
requires a genuinely new derivation.

Until this review is complete, use a bounded status such as
`SUPPORTED[NONTRIVIALITY_UNREVIEWED]`.

## 6. Relation to the wider Equation to Artifact program

This map governs the mathematical objective. The broader program continues only
when an admitted artifact exposes a reusable computational structure:

~~~text
mathematical result
    -> executable custody
    -> operational exposure
    -> computational primitive
    -> transfer experiment
    -> prototype
    -> domain validation
~~~

The later stages do not widen the mathematical claim.

See:

- `OPERATIONALLY_EXPOSED.md`;
- `EQUATION_TO_ARTIFACT_VISION_ROADMAP.md`;
- `ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md`;
- `E2A_RESOURCE_STAGE_CROSSWALK.md`;
- `E2A_RESOURCE_CLAIM_LEDGER.yaml`.

## 7. Status indirection

This policy document intentionally contains no "current map position" section.

Dated state belongs in:

- `CURRENT_POSITION_2026-10-05.md`;
- execution receipts;
- `E2A_RESOURCE_CLAIM_LEDGER.yaml`;
- `NEGATIVE_RESULT_REGISTER.md`.

This prevents a stable research-policy document from becoming stale when an
execution state changes.

## 8. Strategic rule

The near-term objective is not to reproduce a manuscript page count.

The objective is to reduce the highest-risk mathematical and semantic
uncertainty, preserve explicit source boundaries, and allow each candidate to
fail visibly.

No candidate theorem claim is promoted merely because software checks pass.
