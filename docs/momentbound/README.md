# NSRW MomentBound

**Source-derived coefficient bounds, built for checkable scientific computation.**

Design date: 12 November 2026 (Asia/Bangkok). Design version: 0.1.
Status as of 13 November. MB-00 through MB-03 delivered the tested arithmetic
prototype. MB-04 passed the pinned Lean development compile. MB-05 then
admitted fourteen coefficient propositions after clean replay and statement
review. [Dated receipt](../stage_receipts/MOMENTBOUND_COEFFICIENT_COLAB_2026-11-13.md)

## Purpose

Turn the existing moment-comparison proofs into a small callable calculation:
given the fixed source-core inputs, return a justified scaled lower bound for
the second repair coefficient, with the remaining source assumptions explicit.
Then connect that calculation to a conditional angular-moment bound and assess
one scientific-use candidate through comparison.

The first milestone is deliberately smaller than a full Profile evaluator:

```text
existing exact inequalities
  -> positive scale separation
  -> exact rational lower/upper coefficient bounds
  -> checkable fixed-input q decision
```

The design develops a route that may eliminate quadrature and row-moment
evaluation from this first decision. The new connecting inequalities are
derived in the design and implemented in the arithmetic prototype. The new
Lean modules connect both source coefficient estimates to the fixed rational
bound and the conditional actual coefficient result.

## Where to work

- [Detailed mathematical and implementation design](IMPLEMENTATION_PLAN.md)
- [Sol implementation handoff and ordered tasks](TASKS.md)
- [First implementation and verification record](IMPLEMENTATION_REVIEW_2026-11-12.md)
- [Parent P0-P4 roadmap](../NSRW_POST_Z_COMPUTATIONAL_BRIDGE_PLAN_2026-10-21.md#7-p0-p4-execution-proposal-and-ai-checklist)
- [Fixed input and error contract](../NSRW_P2_FIRST_INPUT_AND_ERROR_CONTRACT_2026-10-28.md)
- [Current NSRW position](../CURRENT_POSITION_2026-11-02.md)

| Parent stage | MomentBound role | First output |
| --- | --- | --- |
| P0 | Bind exact definitions and preserve unresolved source-instance assumptions | Input/assumption contract and working D: environment |
| P1 | Consume the ten admitted propositions unchanged | Separate new coefficient bridge; old P1 stays closed |
| P2 | Main implementation target | Exact-rational scaled coefficient bound and recomputing verifier |
| P3 | Follow-on after the first bound works | Conditional normalized-J lower bound; numerical source-J and instance work remain separate |
| P4 | Recommended branch B | One cancellation/denominator diagnostic comparison with equally informed baselines |

## First completion criterion

For the fixed tuple `P=m=1`, `lambda=10^-12`, `eta=2^-20`, compute and verify
an exact rational `B_lower>0` together with the correctly bound positive symbolic
factor `s`, such that the reviewed mathematics gives

```text
q_star = (9/10)*C_main - abs(eta*(1+eta^2))*abs(C_prefix)
q_star >= s*B_lower,    s>0.
```

The software may establish the rational decision before the connecting Lean
proof is admitted, but must label that boundary. Applying it to actual c1 also
requires the same Profile's amplitude to exceed 9/10. The plan records those
conditions rather than fabricating an evaluable source instance.

## Working agreement

MB-06 established the conditional normalized angular-moment bound and
enclosed its scalar factor at the fixed tuple.
[MB-06 dated receipt](../stage_receipts/MOMENTBOUND_NORMALIZED_J_COLAB_2026-11-13.md)
MB-07 ran the frozen ratio comparison. The Fraction method resolved twelve
of sixteen held-out threshold decisions. [Benchmark results](MB07_DIAGNOSTIC_BENCHMARK_RESULT_2026-11-14.md)

At the fixed input, the source's `combinedScale` sufficient condition
fails for every positive reset constant. Source-instance work now requires
a quantitative reset and a more direct amplitude bound.
[Threshold finding](FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md)
