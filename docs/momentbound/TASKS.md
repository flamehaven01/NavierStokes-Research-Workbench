# MomentBound — Sol implementation handoff

Date: 2026-11-12. Read [the design](IMPLEMENTATION_PLAN.md) before coding.
The user intends a subsequent Sol high implementation session. This file is
the handoff; it neither switches models nor launches a background task.

## Current boundary

- Existing Z+J and ten P1 propositions remain admitted in their original scopes.
- MB-00 through MB-03 completed on 12 November; see the
  [implementation record](IMPLEMENTATION_REVIEW_2026-11-12.md).
- Fixed-input producer and recomputing verifier passed 87 focused tests;
  the full suite passed 760 tests, with 3 skipped and 22 subtests.
- MB-04's source coefficient bounds, fixed rational value and conditional
  actual coefficient positivity passed the pinned development compile on
  13 November. All three development archives were reopened and checked
  from private Drive.
  [MB-04 development record](MB04_DEVELOPMENT_2026-11-13.md)
- MB-05 static correspondence review passed. The replay runner pins the two
  development proof files and their dependencies. The 45 focused replay tests
  passed. [Correspondence review](MB05_CORRESPONDENCE_REVIEW_2026-11-13.md)
- MB-05 clean replay and scoped receipt review completed on 13 November.
  Fourteen Lean propositions were admitted at OE-2.
  [Dated receipt](../stage_receipts/MOMENTBOUND_COEFFICIENT_COLAB_2026-11-13.md)
- MB-06 factor-only prototype completed on 13 November: a bounded rational
  R(lambda) and B_coarse*R interval were produced and recomputed, with 20 targeted
  tests and Ruff PASS. The same-Profile Lean bridge passed the pinned
  development compile. The clean replay and private Drive archive review
  admitted four exact-real propositions at OE-2.
  [MB-06 dated receipt](../stage_receipts/MOMENTBOUND_NORMALIZED_J_COLAB_2026-11-13.md)
- Fixed-tuple Profile existence and amplitude remain open. The source's
  sufficient condition on `combinedScale` fails at `lambda = 10^-12` for
  every positive reset constant. [Threshold finding](FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md)
- P0 deterministic evidence hardening implemented locally on 14 November:
  SPAR math editorial verdict is separated from mathematical evidence and
  missing proof is UNVERIFIED (155 full-suite tests PASS); FHVAL required
  baseline/scorer missing measurements are UNRESOLVED rather than zero or
  0.0% disagreement (42 executable tests PASS; full suite ENV_BLOCKED because
  scipy is absent from this Python environment).
- MB-06's R(lambda) has one additional algorithmic interval cross-check:
  mpmath.iv direct exp differences contain the recorded exact Fraction bounds.
  This is same-operator numerical checking, not OE-3 or J certification.
  The original 13 November JSON is not rewritten.
- MB-08 source inverse and quadratic bounds and the fixed reset conditional
  bridge are development-compiled. The successful inverse-run ZIP has only
  Colab-VM preservation recorded: **durable Drive or D: copy is unverified**.
  Original selected-cutoff jet and same-reset polynomial signs remain OPEN/HELD.
- The executed exact B_coarse record is not a complete source certificate.
- Preserve uncommitted docs and ignored essay drafts. Do not stage the whole tree.

## Ordered work packages

| Task | Parent | Work | Completion evidence |
| --- | --- | --- | --- |
| MB-00 | P0 | Inspect HEAD/status; restore a dedicated D: project environment and verify exact dependencies | Interpreter and dependency identities; working targeted tests |
| MB-01 | P0/P2-02A | Independently rederive section 3's prefix sign, scale s and B; check source definitions and section 4 constants | Reviewed equation-to-source table; no unresolved algebra hidden in code |
| MB-02 | P2-02B/C | Implement the fixed-input exact rational producer and closed record format | Correct deterministic arithmetic record; no claim promotion |
| MB-03 | P2-03 | Implement a recomputing verifier and rejection tests | Valid round trip; mutated input/bound/scope/scale rejected |
| MB-04 | P2 plus new proof bridge | Develop and compile the coefficient modules | Development PASS on 13 November. Admission pending |
| MB-05 | P2 closure | Review Python/source/Lean correspondence and replay the fixed proof inputs | Completed. Ten replay stages passed and the scoped receipt admits fourteen propositions |
| MB-06 | P3 | Validate normalized-J cancellation and bound R(lambda) for the fixed tuple | Completed. Factor enclosure passed and the scoped receipt admits four Lean propositions |
| MB-07 | P4-B | Compare ratio/denominator diagnostic against equally informed float64, stable expm1 and analytic-rational baselines | Internal benchmark executed. Fraction resolved 12/16 held-out thresholds. Scientific workflow utility remains open. [Benchmark results](MB07_DIAGNOSTIC_BENCHMARK_RESULT_2026-11-14.md) |
| MB-08 | P0, active | Bound the fixed-lambda reset and verify the source amplitude through its energy polynomial | Seven declarations have passed development compile across the MB-08 runs. The source inverse and quadratic bounds discharge both operator premises at the fixed lambda. The reset still requires supplied `TailData` and the original cutoff jet bound. Actual polynomial signs remain open. [Source cutoff decision and development evidence](MB08_SOURCE_CUTOFF_BOUND_DECISION_2026-11-14.md) |

## Immediate execution order (post P0 patch)

- [x] SPAR math evidence separation, byte-bound record checker and self-report
  relabeling, local full-suite regression PASS (not a Lean replay).
- [x] FHVAL baseline fail-closed patch and deterministic regression tests;
  scipy-dependent full suite remains ENV_BLOCKED in current environment.
- [x] MB-06 one alternative arithmetic algorithm cross-check on the *factor only*.
- [x] MB-08 exact inverse diagnostic. Nine synthetic cases matched their
  expected outcomes and the source-envelope arithmetic passed.
  [Design and local results](MB08_INVERSE_DIAGNOSTIC_2026-11-14.md).
- [x] Extend the internal verification runner across exact arithmetic,
  interval containment, a manufactured Navier–Stokes field and existing
  P1 Lean evidence. [Research verification](../NSRW_RESEARCH_VERIFICATION.md).
- [x] Generic research verification input custody P0: snapshot bytes before
  evaluation, read-only checker inputs, mutation/invalid-type failure and
  permission read error classification. Existing four check JSONs rerun
  byte-identically; post-fix full JUnit: 849 recorded, 0 failures/errors,
  3 skipped (subtests separately reported).
- [x] Emit versioned execution manifests for all four checks. The installed
  command binds the selected implementation files, runtime, inputs and
  report digest. [Execution manifests](../NSRW_RESEARCH_VERIFICATION.md#execution-manifests)
- [ ] Persist and reopen the exact MB-08 successful Colab ZIP at a durable
  local or Drive destination. The old Colab runtime is disconnected
  and the original archive was not located locally on 14 November.
- [ ] Check SPAR/FHVAL CLI/result consumers for format compatibility before
  installation, Inspector rebind or release. No live MCP deployment is claimed.
- [ ] Continue source cutoff choice/jet obstruction and actual same-reset
  energy polynomial signs; fixed source Profile and J remain unconstructed.

The proof checkpoint `80325a2d999c7da6af49398aaf1fae83df024b95` contains
`P2_CoefficientScaledBounds.lean` and `P2_CoefficientSourceBounds.lean`. The
execution checkpoint `fb5ad6001f1637417efda6ef34f3b75c8266c059` adds
`scripts/run-momentbound-replay.py` and `tests/test_momentbound_replay.py`.
The dated receipt records the printed statement review and archive checks.

## First code-session procedure

1. Read repo AGENTS/README/MICA as directed. Observe actual status and pins.
2. Verify a dedicated D: Python environment; the old shared venv references a
   removed interpreter. Do not rely on activation success alone.
3. Re-read the exact normalized 2x2 system and reproduce the prefix subtraction
   on paper/in the work record. Check the sign before copying formulas.
4. Verify `H0_upper=328`, `H1_upper=3099396717/2` and the distinction between
   B_coarse and q_star. Verify that positive s remains in the final relation.
5. Implement only the two proposed Python modules and focused tests. Reuse
   existing arithmetic; leave old core JSON and formal modules unchanged.
6. Produce one actual result in an ignored run directory. Run the verifier on
   that file, then on deliberately altered records.
7. Run targeted tests/Ruff; then the full suite once when the changes settle.
   Do not reuse the earlier 673-test result as evidence for new code.
8. Record exact inputs, files, command, outputs, unresolved formal/source
   obligations and next action. Do not commit/push or publish by default.

## Required implementation checks

- [x] Producer and verifier never return q=B_coarse or numeric s without evaluation.
- [x] Exact rational format, closed keys, size limits, duplicate-key rejection.
- [x] Verifier recomputes constants, p and B without calling producer.
- [x] Fixed source/tuple binding and mandatory unresolved assumptions preserved.
- [x] Supporting exp(1) precision is separate from exact B arithmetic.
- [x] Arithmetic PASS cannot become `CONFIRMED` or a Profile/J certificate.
- [x] Known exact normalized systems catch reversed coefficient signs.
- [x] Old 128/256/512 core records and tests remain unchanged.
- [x] New formal work imports the actual dependencies and never private generated names.
- [x] No fabricated compile, benchmark, independent-review or utility result.

## First handoff output

Report implementation status, exact result location, producer/verifier outcomes,
tests, scope, and the remaining new-Lean/source-instance obligations. If blocked,
identify the failed equation, dependency or check. A small verified arithmetic
prototype is the intended first output; do not create empty later-stage modules.
