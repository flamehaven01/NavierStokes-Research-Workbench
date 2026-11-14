# Navier--Stokes research direction map

Document status: `ADOPTED`
Scope: stable mathematical and scientific-computation direction; not a dated status report and not an
execution gate.

The filename preserves the project's historical internal "north-star" naming.
Public summaries should call this the research direction map.

## 1. Long-range objective

The workbench investigates Navier--Stokes mathematics to obtain justified
mathematical results and turn reusable structures into useful scientific
computation.

Two connected outcomes guide the work:

- **Mathematical research:** discover, isolate and prove mechanisms that clarify
  genuine analytic questions, with a rigorous theorem-level contribution as a
  long-horizon objective.
- **Scientific use:** produce an evaluable algorithm, bound or diagnostic with
  explicit inputs and error assumptions, then demonstrate its value in a named
  scientific or engineering workflow.

A theorem is a substantial milestone. Useful, measured scientific computation
is the practical destination. A general Navier--Stokes solution is not a
prerequisite for a bounded scientific application.

Receipts, CI, papers and websites preserve or communicate the results. The next
research priority is the mathematical or computational output they support.

The nearest useful output may be a conservative bound rather than a full
function evaluator. Reuse explicit inequalities when they suffice for the
specified decision, and compute additional quantities only as needed. Keep
core-dependent computation separate from the existence and evaluability of a
complete source instance. Each application must name the decision it improves
and compare against methods given the same mathematical information.

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
            |
            v
evaluable bound / algorithm / diagnostic
            |
            v
comparison in a selected scientific workflow
~~~

## 4. Architecture test

Before adding code, a ledger, a receipt, or a new research direction, ask:

1. Does it expose a mathematical quantity or dependency that was previously
   opaque?
2. Does it support an independent derivation or kill a concrete alternative?
3. Does it preserve source hypotheses and boundary cases?
4. Does it produce the next falsifier or proof obligation?
5. Does it turn an established structure into a bounded computation, or measure
   whether an existing computation is useful against a relevant baseline?

If all answers are no, the artifact is process growth rather than research
progress and should be removed or deferred.

## 5. Nontriviality and semantic-review gate

State the derived propositions and their mechanism directly. Their mathematical
content is not diminished by an incomplete literature-priority assessment.
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

This map connects the mathematical objective to scientific use. A theorem-derived
application must identify the reusable structure and preserve its hypotheses:

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

- [Current-position reassessment with its 12 November addendum](CURRENT_POSITION_2026-11-02.md), followed by the
  active tasks in the restart checklist;
- `CURRENT_POSITION_2026-10-05.md` as a historical snapshot;
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
