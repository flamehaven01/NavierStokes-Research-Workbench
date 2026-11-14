# MomentBound MB-06 — normalized-J factor and source-bridge review

Date: 2026-11-13 (Asia/Bangkok). Review and bounded implementation in the
same operator's D: workspace. **Partial development**, not claim admission.

```yaml
arithmetic_result: PASS[MB06_POSITIVE_RATIO_ENCLOSURE]
verifier_result: PASS[RECOMPUTED_MB06_FACTOR_ONLY]
targeted_tests: 20_PASS
ruff: PASS
formal_normalized_J_bridge: NOT_IMPLEMENTED_OR_COMPILED
claim_authority: NONE
claim_status: UNVERIFIED
independent_attestation: false
independent_reproduction: false
source_profile_at_fixed_tuple: NOT_CONSTRUCTED
amplitude_hypothesis: NOT_ESTABLISHED
new_git_checkpoint: NOT_CREATED
private_drive_archive: NOT_CREATED
```

## 1. Reused admitted mathematical surfaces

- Upstream source: `openai/NavierStokesAndEuler` at
  `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.
- P1 exact-real quantitative and normalized-bump theorems: receipt
  `docs/stage_receipts/P1_QUANTITATIVE_MARGIN_COLAB_2026-10-22.md`;
  execution commit `7f29ebf0e2b894bf598144628230ae09df436c3d`.
- MB-05 fourteen source-coefficient propositions: receipt
  `docs/stage_receipts/MOMENTBOUND_COEFFICIENT_COLAB_2026-11-13.md`;
  proof checkpoint `80325a2d999c7da6af49398aaf1fae83df024b95`;
  execution checkpoint `fb5ad6001f1637417efda6ef34f3b75c8266c059`.
  Both sets are admitted at OE-2, not independently reproduced.

Use one source `Profile F`, core `c=F.data.core`, parameters `eta,r`
and, only when stated, an exact interior zero
`c.lower 0 < r < c.upper 0` with `localMass F eta r=0`.

Definitions:

```text
lambda = c.lam > 0             L = 13/lambda
beta0 = 1/2-lambda            beta1 = 1/2-2*lambda
b = center(c,0) = L-3
A_i = rowMoment(c.exponents i) > 0
D = exp(1-4*lambda)*(exp(2*lambda)-1) > 0
s = exp(-beta1*b)/(A1*D) > 0
I01 = A0*exp(beta0*(L-1)) > 0
Delta = exp(-13+23*lambda/20)*(exp(17*lambda/10)-1) > 0
R(lambda) = (exp(17*lambda/10)-1)/(exp(2*lambda)-1) > 0
K1 = momentScale(c,1)*shape(eta)^2 > 0
```

The *proposed, not yet separately Lean-compiled* cancellation is exactly

```text
s*I01*Delta =
  (A0/A1)*exp(3*lambda/20)*R(lambda)
>= R(lambda).
```

The exponent identity behind this cancellation is

```text
-beta1*(L-3) + beta0*(L-1)
  + (-13+23*lambda/20) - (1-4*lambda)
= 3*lambda/20.
```

The last inequality follows from the **admitted L3 theorem**
`exp(-3*lambda/20)*A1 <= A0` with `A1>0`.
It eliminates the huge `exp(L)`, `I01`, and individually unknown
`A0/A1`, `s` from the *candidate normalized lower bound* without
evaluating them numerically. It uses the **full exact I01 identity**, not
the weaker cutoff-plateau lower bound. Both numerator and denominator
of R are positive because lambda>0.

The existing admitted P1 J theorem establishes
`localJ >= K1*c1*I01*Delta` at every specified first-window exact
mass zero with actual `c1>0`. MB-05 gives
`c1 > s*B_coarse` for `P=m=1`, `F.amp eta>9/10`.
If additionally `B_coarse>0`, positivity of all factors yields the
new **conditional mathematical target**

```text
localAngularMoment F eta r / K1 > B_coarse(c,eta) * R(c.lam) > 0.
```

This target is **not** an already admitted Lean theorem, numerical
Profile.J, source J computation, or numerical root. A future source
`Profile.J` interpretation also requires the matching coordinate
bridge `localAngularMoment_eq_profileJ` and `r>=1`.

## 2. Exact rational analytic enclosure for R

Set `x=17*lambda/10`, `y=2*lambda`. For the source range
`0<lambda<1/10`, both are positive and `0<x<y<1`.
Using `z <= exp(z)-1 <= z*exp(z)` for `z>=0` and
`1-z <= exp(-z)`, plus positivity of `1-x`, gives

```text
(17/20)*(1-2*lambda)
 <= R(lambda)
 <= (17/20)/(1-17*lambda/10).
```

These are **exact real analytic bounds**, evaluated at the fixed rational
lambda without floating-point cancellation.

For `lambda=1/1000000000000`:

```text
analytic lower = 8499999999983/10000000000000
analytic upper = 8500000000000/9999999999983
```

The upper bound is an upper bound **for R only**, not for normalized J.

## 3. Bounded ratio computation — observed execution

Fixed tuple: `P=m=1`, `lambda=10^-12`, `eta=2^-20`,
`B_coarse=207522463005781740692370179/2305843009213693952`.

Inputs to the existing reviewed positive-series `expm1_bounds`:

```text
numerator argument   = 17*lambda/10
denominator argument = 2*lambda
precision            = 128 fractional bits
```

Using `Fraction` and proved remainder-bound formulas implemented in the
existing core-scalar backend, the producer returns positive dyadic bounds
`[nL,nU]` and `[dL,dU]` and uses the **correct quotient direction**:

```text
R_lower = nL/dU
R_upper = nU/dL
B_times_R_lower = B_coarse*R_lower
B_times_R_upper = B_coarse*R_upper.
```

Actual generated and verified values:

```text
R_lower = 192826674588695698635979289/226854911280852497220197182
R_upper = 578480023766087095907937868/680564733842557491660591545

R in approximately
[0.8499999999998724999999999691,
 0.8499999999998724999999999719]

B_coarse*R in approximately
[76498743.7783283630275347200445,
 76498743.7783283630275347202893]
```

Both intervals are for **the fully specified factor expression**, not
observed/estimated source `qStar`, `c1`, `localJ` or `Profile.J`.
The analytic bracket independently checks that the exact-rational
series interval lies in a justified wider positive interval. Both
numerical implementations share the `expm1_bounds` backend; this does
not constitute an independent arithmetic engine or external attestation.

## 4. Code, tests and byte identities

- Producer: `src/nsrw/math_kernel/p2_normalized_j_factors.py`
  SHA-256 `d4e0a4ae37045eb5cfd8c9e5fd44efa12b2a8432bd7057afd7523761356e5ae6`.
- Recomputing verifier: `src/nsrw/math_kernel/p2_normalized_j_verify.py`
  SHA-256 `8b22d62ae996652dee46f40dac36738faa4634e01a24453300e55d5fa204942a`.
  It does not import or call the producer, but shares the reviewed
  `exp_bounds` family and previously tested bounded JSON parser.
- Targeted tests: `tests/test_p2_normalized_j_factors.py`
  SHA-256 `934ca9a69a0359998021d657dd597577f7601dc49fef4565e0df5ac8e06bb87a`.
- Original record:
  `outputs/mb06-ratio-20261113.json`, SHA-256
  `c4d28daf7b44ef4ab0d7d90c74c1b942b181ddc9901e50a3a8a4beaf78a674e8`,
  2,054 bytes, ignored local evidence only.

The normal MCP `python-pytest` profile was **environment-blocked**
(`FH_FAIL_EXECUTABLE_UNAVAILABLE: python`; no test started).
The known D: venv was then invoked through the allowlisted
`pwsh-file` profile. Observed:

```text
python -m ruff check [three changed files]
  All checks passed!
python -m pytest tests/test_p2_normalized_j_factors.py -v --no-cov
  20 passed in 0.44s
python -m nsrw.math_kernel.p2_normalized_j_factors --output outputs/mb06-ratio-20261113.json --precision 128
  PASS[FACTOR_ENCLOSURE_ONLY]
python -m nsrw.math_kernel.p2_normalized_j_verify --input outputs/mb06-ratio-20261113.json
  PASS[RECOMPUTED_MB06_FACTOR_ONLY], claim_status: UNVERIFIED
```

Tests include input/scope/commit mutation, lower-bound inflation,
zero-denominator, malformed precision and verifier operation with the
producer monkeypatched to raise. No full project regression suite
was rerun, and no actual Lean compile occurred for MB-06.

## 5. Remaining proof and source admissibility gates

A separate `P2_MB06_NormalizedJ.lean` module is the **next target**, not
an existing admission. It should establish:

1. Exact `D = exp(1-4*lambda)*(exp(2*lambda)-1)` with its positive denominator.
2. The exact product cancellation `s*I01*Delta =
   (A0/A1)*exp(3*lambda/20)*R(lambda)`.
3. L3 lower comparison `s*I01*Delta >= R(lambda)>0`.
4. Composition with P1 and MB-05 at the *same F, eta, r*:
   `localJ/K1 > Bcoarse * R` under `P=m=1`, `Bcoarse>0`,
   `F.amp eta>9/10`, first-window membership and exact `localMass=0`.
5. Optional fixed-tuple wrapper consuming admitted `mb_fixed_coarse_pos`;
   do **not** assert an instantiated `Profile F` without its constructor.

Keep source `ResetWitness`, `K>0`, the combinedScale/stepBound path,
and amplitude-spec hypotheses explicit. The fixed tuple's nonempty
source Profile family has **not** been established. Replaying existing
MB-05 receipts does not prove MB-06.

A successful development compile would still require a distinct
checkpoint, clean replay, preservation and dated receipt before claim
admission. Do not mutate MB-05 evidence, historical JSON or any admitted
proof module. No Git commit/push or Drive preservation has been performed
for this MB-06 work.
