# MomentBound MB-07 — preregistration draft for one numerical diagnostic

Date: 2026-11-13 (Asia/Bangkok)
Status: `BENCHMARK_CONTRACT_DRAFT / NOT_EXECUTED / NO_UTILITY_CLAIM`.
This is an **internal cancellation/denominator diagnostic**, not an
application transfer or TR-3 admission. There is no independent domain
reviewer, OE-4 transfer waiver, CFD workload, solver or deployment claim.

## Exact object and decision

Upstream anchor: MB-06 receipt
`docs/stage_receipts/MOMENTBOUND_NORMALIZED_J_COLAB_2026-11-13.md`
with source commit `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`,
execution `40e0cfe7c2defeeeee871f1923552c352f28ee5c`.

Primitive to compare, for exact rational `0<lambda<1/10`:

```text
R(lambda) = expm1(17*lambda/10) / expm1(2*lambda)
```

The source theorem establishes `R>0`; the previously run Fraction
implementation gives an *outward* rational interval for the **factor**
alone. It does not evaluate `F`, `J`, `q`, `r` or source amplitudes.

The benchmark task is to return either (a) an asserted numerical estimate
with explicitly stated limitations or (b) a justified rational enclosure
`[lower,upper]` and a decision `BELOW/ABOVE/UNRESOLVED` relative to
each predetermined rational threshold:

```text
T_low(lambda)  = 17/20 - 13*lambda/100
T_high(lambda) = 17/20 - lambda/8
```

For interval methods:
`BELOW` only when `upper < threshold`;
`ABOVE` only when `lower > threshold`;
otherwise `UNRESOLVED`. Floating-point methods provide estimates,
**not certified** decisions; compare their estimated sign to a separate
high-precision reference and record indeterminacy from rounding.

## Information parity / baselines (freeze before a reported run)

All methods receive exactly the same rational `lambda`, the same
formula, same two thresholds, and no privileged precomputed numerical
factors or exact answers. Do not tune case-specific formulas after
observing results.

| Method | Same input / implementation | Output class |
| --- | --- | --- |
| A — ordinary float64 | Convert rational lambda to binary64, use `math.exp(a)-1` and `math.exp(b)-1`; report zero denominators and conversion loss | Uncertified estimate or error |
| B — stable float64 | Same binary64 conversion but `math.expm1(a)/math.expm1(b)` | Uncertified estimate or error |
| C — analytic exact-rational | Published conservative bracket `(17/20)*(1-2*lambda) <= R <= (17/20)/(1-17*lambda/10)` | Certified coarse bracket, threshold decision or abstain |
| D — tested Fraction enclosure | `p2_core_scalars.expm1_bounds`, numerator/denominator outward interval quotient, 128 then 256 then 512 fractional bits | Certified bounded bracket, threshold decision or abstain |
| Reference (not a contestant) | Independently evaluated high-precision `mpmath` with precision and input conversion recorded; cross-check its numeric value against C/D brackets | Empirical reference, **not** proof authority |

A, B and D may have different precision/output guarantees; reporting a
smaller error or a certified interval is not by itself an equal-cost utility
result. Explicitly record the information/assurance difference. The
high-precision reference must construct lambda without binary64 rounding.
The exact bounds in C also count as a serious baseline, not a straw man.

## Frozen cases; no post-result selection

All inputs are exact rationals. The **calibration set** (for checking
harness behavior only, no threshold tuning) is:

```text
1/16, 1/1048576, 1/1000000000000, 1/(2^40)
```

The **held-out set** for reported metrics is:

```text
1/128, 1/1024, 1/(2^52), 1/(2^60),
1/(2^120), 1/(2^160), 1/(2^400), 1/(2^520)
```

Invalid/rejection controls: `lambda=0`, negative `-1/10^12`,
`lambda=1/10` (source strict upper bound), wrong types, noncanonical
rationals and input changed after record creation. Rejection controls
are counted separately from numeric-reference cases.

The **primary source-bound numerical tuple** remains
`P=m=1, lambda=10^-12, eta=2^-20`; only there do we separately
record `B_coarse*R`. The other lambdas test factor conditioning
**only**: do not assign them a source Profile, a coefficient value or
the fixed B record from lambda=10^-12.

Very small lambda may be below 128-bit dyadic resolution. If the
lower denominator bound becomes zero, D must abstain, not silently
divide; bounded 256/512 escalation may or may not close that case.

## Metrics, budgets and stopping

For every case, report:

- accepted and unresolved threshold decisions; contradictions with the
  separately computed reference; interval containment and width;
- the direct-vs-`expm1` difference, zero/catastrophic-denominator events,
  incorrect acceptance, safe abstention, and source-range input rejection;
- method runtime (median and p95) and measured peak allocated memory,
  with runtime/hardware/environment, warm-up and observation counts;
- interval factor precision/bits and number of escalation attempts.
  Distinguish memory allocation tracking from OS process RSS.

Freeze the execution procedure before use: 3 warm-ups and 20
timed trials per method/case on the same host with identical environment,
no parallel loads, no online library installation. D may attempt only
128, 256 and 512 fractional bits, in that order; **120 seconds maximum
per case**, fail closed on timeout. Report every skipped or unresolved case;
do not silently resample it.

Minimum validity: zero invalid-input acceptances, zero knowingly false
interval claims, and no use of a numerical reference as a Lean proof.
A possible empirical improvement is an additional correctly separated
near-threshold decision with a reproducible error budget at stated cost.
If B and C handle the cases as well at lower cost, or D's additional
certification does not matter for a stated consumer, report
`NO_INCREMENTAL_VALUE` instead of declaring a product success.

This **is a plan, not a preregistered completed benchmark**. Establish the
baseline versions/environment, reviewer and frozen run manifest before
testing. Record all attempts and negative results. Do not interpret
`math.exp` cancellation as falsifying the mathematical theorem.

## Execution contract and next gate

Suggested future bounded interface:

```text
ratio_diagnostic(lambda_exact, precision_bits)
  -> {status, enclosure?, thresholds?, source_identity, error_reason?}
```

Required statuses include `PASS[FACTOR_ONLY]`,
`UNRESOLVED[PRECISION]`, `REJECT[OUT_OF_DOMAIN]`,
`REJECT[MALFORMED]`. No `Profile`/J numeric fields.

Existing candidate: `src/nsrw/math_kernel/p2_normalized_j_factors.py`,
verifier `p2_normalized_j_verify.py`, tests
`tests/test_p2_normalized_j_factors.py`.
Their 20 targeted tests do not constitute this comparative workload.

This protocol should first yield a dated, source-bound diagnostic *run*
with A/B/C/D measurements and negative cases. It creates no immediate
TR-0/1/2/3, application capability, independent attestation, or proof
claim. Practical transfer requires the separate rules in
`docs/ARTIFACT_TO_APPLICATION_TRANSFER_GATES.md`.
