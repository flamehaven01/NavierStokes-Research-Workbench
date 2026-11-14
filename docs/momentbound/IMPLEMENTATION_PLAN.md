# MomentBound v0.1 — detailed implementation design

Date: 2026-11-12, Asia/Bangkok. Design baseline NSRW HEAD:
`90f7091251d98063e91c458cd72e8a0f5d9eaf20` plus the existing uncommitted planning
documents. Upstream source:
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

This is a design with source-checked algebra, not an execution receipt. The
coefficient and normalized-J bridges below are new proof obligations. Existing
Z+J/P1 admissions remain unchanged. A small exact-rational design sanity check
was performed; it is identified in section 4 and is not a source certificate.

## 1. Objective, outputs and non-goals

First build a fixed-input coefficient-bound calculation that can be rerun and
rejected when its input, algebraic constants or scope are altered. Its useful
operation is a positive-bound decision, with a later route to normalized moment
postprocessing. Do not begin by implementing all source integrals.

Three separately observable outputs:

1. **Arithmetic result:** an exact rational positive scaled bound, with a
   verifier recomputing the mathematical arithmetic rather than calling produce.
2. **Mathematical bridge:** new Lean declarations relating that bound to the
   actual source affine coefficients; development compile and later admission
   have their own identities.
3. **Conditional application:** under the same Profile's amplitude conditions,
   actual c1 and then a root-applicable normalized-J bound. An explicit source
   instance and empirical scientific utility require further work.

Do not implement a generic interval framework, full ResetWitness evaluator,
root finder, CFD solver, UI, new publication pipeline or P03 framework in v0.1.
No novelty or performance advantage is inferred from a short implementation.

## 2. Source definitions and mathematical interfaces

All real quantities in this section belong to the same source core `c`.
Use `f_i` for normalized main moments, so `F` remains reserved for Profile.

| Symbol | Exact source object |
| --- | --- |
| lambda | `c.lam`, with `0<lambda<1/10` |
| L | `c.pulseLength = 13/lambda` |
| b | `center c 0 = L-3` |
| beta0, beta1 | `1/2-lambda`, `1/2-2*lambda` |
| A_i | `rowMoment (c.exponents i)`, strictly positive |
| f_i | `normalizedMainMoment c i = exp(-beta_i*b)*mainMoment c i` |
| E_i | `exp(-beta_i*b)`, strictly positive |
| U_i | `prefixCoefficient c i`, nonnegative |
| H_i | `prefixBound c.P c.m i`, an explicit bound, NOT source Profile.H |
| C_main | `affineCoefficients c 0 1 1` |
| C_prefix | `affineCoefficients c 1 0 1` |
| D | `exp(2*beta0)-exp(2*beta1)>0` |
| p | `eta*(1+eta^2)` |
| q_star | `(9/10)*C_main - abs(p)*abs(C_prefix)`; exact-real auxiliary quantity |

`H_i` here is only temporary mathematical notation for prefix bounds. Use
`prefix_bound_upper_0/1` in code and JSON to prevent confusion with Profile.H.
Do not identify the axial coefficients above with `F.reset.coefficients`.

Essential source bindings:

| Input fact | Location/declaration | Status used here |
| --- | --- | --- |
| main moment lower bound | [F1](../../formal/p2/P2_F1_MainMomentPositivity.lean), `mainMoment_one_lower` | Existing proof |
| strong explicit decay | [L2](../../formal/p2/P2_L2_NormalizedMainMomentComparison.lean), private `normalizedMainMoment_zero_le_decay_one` | Existing proof-local fact; export via a new proof, not a private-name dependency |
| row comparison | [L3](../../formal/p2/P2_L3_TemplateMomentComparison.lean), `rowMoment_one_scaled_le_rowMoment_zero` | Existing proof |
| main coefficient formula | [C01](../../formal/p2/P2_C_MainOnlyCoefficient.lean), `affineCoefficients_main_one_eq_neg_deltaM_div_gap` | Existing proof |
| actual coefficient decomposition | [C02](../../formal/p2/P2_C02_ActualCoefficientDecomposition.lean) | Existing proof |
| prefix bounds/system | pinned `OutgoingPulseBounds.lean`: `prefixCoefficient_nonneg`, `prefixCoefficient_le_bound`, `actual_coefficients_normalized_system`, `prefixBound`, `scaleFloor` | Upstream theorem/definition |
| actual second-bump moment | pinned `OutgoingPulseBounds.lean`: `actual_matrix_entry` | Upstream theorem |
| J margin and weight gap | [QuantitativeMargin](../../formal/p2/P2_ZPLUS_J_QuantitativeMargin.lean), [MarginNormalization](../../formal/p2/P2_ZPLUS_J_MarginNormalization.lean) | Existing scoped P1 admission |
| amplitude conditions | pinned `CorrectedPulseAmplitude.lean`: `amplitude_spec` | Upstream theorem; numerical-instance conditions unresolved |

Upstream files are under the pinned [source tree](https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes).
Read local pinned bytes for implementation. Record actual file hashes before
new proof/runner work; do not assume a planning HEAD pins untracked changes.

## 3. Derivation A: remove the enormous common scale

### 3.1 Main coefficient

Existing L2/L3 facts give

```text
f_0 <= exp(-2+3*lambda)*f_1
A_0 >= exp(-3*lambda/20)*A_1 > 0
kappa = 1-exp(-2+63*lambda/20) > 0
f_1/A_1 - f_0/A_0 >= kappa*f_1/A_1.
```

C01 and F1 therefore imply

```text
C_main >= kappa*f_1/(A_1*D)
f_1 >= E_1/(5000*lambda)
s := E_1/(A_1*D) > 0
C_main >= s*kappa/(5000*lambda).
```

This uses the stronger L2 helper, not merely the weaker final strict-positivity
statement. Reproduce that helper in a new module without changing old bytes.

### 3.2 Prefix coefficient — the sign must be checked explicitly

For the prefix-only debt, the two row-normalized equations are

```text
x0 + exp(2*beta0)*x1 = -E_0*U_0/A_0
x0 + exp(2*beta1)*x1 = -E_1*U_1/A_1.
```

Subtract the second equation from the first:

```text
C_prefix = (E_1*U_1/A_1 - E_0*U_0/A_0)/D
         = s*(U_1 - rho_actual*U_0)
rho_actual = exp(-lambda*b)*(A_1/A_0) > 0.
```

L3 and `b=13/lambda-3` give

```text
rho_actual <= rho := exp(-13+63*lambda/20).
abs(C_prefix) <= s*(H_1 + rho*H_0).
```

The last inequality uses `0<=U_i<=H_i` and the triangle inequality. It does
not assert a sign for C_prefix and does not require measuring U_i precisely.

### 3.3 The first decision

```text
B := (9/10)*kappa/(5000*lambda) - abs(p)*(H_1+rho*H_0)
q_star >= s*B.
```

For any rigorously justified `B_lower<=B`, `B_lower>0` proves
`q_star>=s*B_lower>0`. The scale s is symbolic; the code need not compute A_1,
D or the tiny E_1 to decide this sign. D and A_1 positivity remain mathematical
obligations, not disposable terms. This route provides scaled one-sided bounds,
not numerical two-sided intervals for the actual coefficients.

## 4. Derivation B: a deliberately coarse rational baseline

For the fixed `P=m=1`, write `e=exp(1)`. Directly simplifying the upstream
prefixBound and scaleFloor definitions yields

```text
H_0 = 4 + 4*e*exp(e)
H_1 = (5/2 + 4*e*exp(3*e))*exp((e+12)/2).
```

The sqrt(2) factor cancels in H_1. Check this against the actual source, not
an independently chosen physical normalization.

The elementary `2<e<3` bounds, exponential monotonicity and exp(n)=e^n imply

```text
H_0 < 4 + 12*3^3 = 328 =: H0_upper
H_1 < (5/2 + 12*3^9)*3^8 = 3099396717/2 =: H1_upper.
```

For the second bound use `3*e<9` and `(e+12)/2<15/2<8`.
Because `0<lambda<1/10`,

```text
-2+63*lambda/20 < -1, so kappa > 1-1/e > 1/2
-13+63*lambda/20 < 0, so 0<rho<1.
```

A sufficient fully rational decision is consequently

```text
B_coarse = 9/(100000*lambda) - abs(p)*(328+3099396717/2)
B_coarse <= B.
```

This baseline is the first implementation target. It requires no numerical
quadrature, logarithm, square root or huge exponential. A supporting enclosure
for exp(1) may be obtained using the existing exact-rational routine to check
`2<lower(exp(1))<=upper(exp(1))<3`. That numerical check is not a Lean proof of
the full source-to-bound derivation.

### Fixed-input design arithmetic, not a completed certificate

At the already selected lambda and eta, exact Fraction arithmetic gives

```text
p = 1099511627777/1152921504606846976
B_coarse = 207522463005781740692370179/2305843009213693952
floor(B_coarse) = 89998522.
```

These arithmetic identities were sanity-checked while preparing the design.
The result is **not q**, **not J**, and **not a performance measurement**. The
new source bridge is uncompiled, no MomentBound verifier exists yet, and no
admissible numerical Profile has been constructed. Do not report this planning
calculation as P2 completion. Local scratch record:
`outputs/momentbound-design-20261112.json` (ignored, not a release attachment).

## 5. Input contract and scope

Accept exactly the existing first tuple for v0.1:

| Field | Value |
| --- | --- |
| P, m | 1, 1 |
| lambda | 1/1000000000000 |
| eta | 1/1048576 |
| h | lambda/4, contextual source field |
| wait | exact expression `60*log(1000000000000)` |
| K/reset | unassigned/unconstructed; do not fill in a convenient value |

The coefficient algebra uses the core parameter assumptions. Actual c1 uses
the same Profile and `F.amp(eta)>9/10`. A source wrapper may derive that from
`ResetWitness d K`, `K>0`, `lambda<=1/120`, the exact wait identity,
`combinedScale d K<=1/1000`, and `eta^2<=1`. Copy the full signature, including
the matching data/reset, when implementing; tests on finite samples cannot
discharge those hypotheses.

Under that amplitude assumption, C02 and C_main>0 give

```text
actual_c1 = p*C_prefix + amp*C_main
actual_c1 > q_star >= s*B_coarse > 0.
```

The existing source existence theorem has an existential small-lambda threshold;
it does not certify that the selected tuple admits the required instance.
Keep core arithmetic and conditional source consequences distinct.

## 6. Minimal production architecture

Proposed files; create real implementations only during the code turn:

| File | Responsibility |
| --- | --- |
| `src/nsrw/math_kernel/p2_coefficient_bounds.py` | Fixed-input exact-rational B_coarse computation, record construction and CLI |
| `src/nsrw/math_kernel/p2_coefficient_verify.py` | Parse and independently recompute the rational decision; never call produce to get a verdict |
| `tests/test_p2_coefficient_bounds.py` | Source-algebra fixtures, boundary/mutation tests and CLI checks |
| `formal/p2/P2_CoefficientScaledBounds.lean` | New source-to-scaled-coefficient bridge, preserving old proofs |
| `examples/p2-coefficient-bounds/` | Reviewed small public examples only after actual execution/review |

Reuse Python Fraction and the existing public `exp_bounds` for the optional
exp(1) supporting check. Do not widen its [-16,16] domain, refactor existing
scalar internals, or change the old record format. No new dependency is needed
for the rational decision. The verifier may share Fraction and reviewed parsing
utilities; disclose that trusted code and the common operator. It is a separate
checking path, not independent external reproduction.

Suggested callable interfaces:

```python
compute_coarse_scaled_bound() -> Fraction
produce_coefficient_bound_record(*, supporting_bits: int = 128) -> dict
verify_coefficient_bound_record(payload: object) -> dict
```

v0.1 does not expose arbitrary lambda/eta/P/m parameters. A generalized
interface is a separately designed experiment. Private arithmetic helpers may
accept rational fixtures for tests without creating an unrestricted public API.

### Proposed commands — not implemented yet

```text
python -m nsrw.math_kernel.p2_coefficient_bounds produce --output result.json
python -m nsrw.math_kernel.p2_coefficient_verify --input result.json
```

| Command | Exit code | Meaning |
| --- | --- | --- |
| produce | 0 | Valid positive arithmetic record written |
| produce | 2 | Invalid input/CLI usage |
| produce | 3 | Valid calculation did not establish positivity within its budget |
| produce | 1 | Operational/runtime failure |
| verify | 0 | Arithmetic record accepted |
| verify | 1 | Record rejected: malformed, inconsistent, altered or out of scope |
| verify | 2 | Invalid CLI usage |
| verify | 3 | Operational failure prevented verification |

Return a structured reason for nonzero outcomes. Neither command may emit a
formal claim admission or full Profile/J certificate. A nonpositive conservative
bound is not a counterexample. File-read failures are operational errors;
successfully read but malformed JSON is a rejected record.

## 7. Record contract

Use one compact, closed JSON format: `nsrw-p2-scaled-coefficient-bound-v1`.
The implementation must reject unknown/missing fields and duplicate JSON keys.
Rationals use canonical Fraction strings, never float JSON numbers.

Required logical fields:

| Field | Required content |
| --- | --- |
| format / scope | Version above / `SCALED_COEFFICIENT_BOUND_ONLY` |
| inputs | Exact fixed P,m,lambda,eta and contextual h/wait; K remains null |
| method | `coarse-rational-source-bounds-v1` |
| p | Exact eta*(1+eta^2), recomputed |
| constants | kappa lower 1/2, rho upper 1, prefix uppers 328 and 3099396717/2 |
| scaled_bounds | C_main/s lower 1/(10000*lambda); abs(C_prefix)/s upper H0_upper+H1_upper; B_coarse exact |
| positive_scale | Fixed symbolic definition E_1/(A_1*D), exact E_1 exponent, bound core identity, positivity references; explicitly not numerically evaluated |
| supporting_arithmetic | exp(1) enclosure and its fractional-bit precision if used; B arithmetic itself is exact and has no rounding precision |
| source_binding | Upstream revision; used proof/file identities captured from actual inputs |
| mathematical_bridge | Initially `STATIC_DERIVATION_NOT_ADMITTED`; no fabricated theorem receipt |
| assumptions | Full actual-c1/source-instance conditions still unresolved |
| check_status | Arithmetic result only, independently recomputed by verifier |

Do not put a numeric q field containing B_coarse. Do not label one-sided scaled
bounds as actual coefficient intervals. The verifier must compare the symbolic
scale's definition and exact exponent, not claim to evaluate its unknown row
moment. The expected source binding is code/release-controlled; an input record
cannot choose its own trusted source pin.

Bound file size to 64 KiB and each rational string to 1024 characters before
parsing. Reject zero/negative denominators, noncanonical strings if canonical
format is required, NaN/Infinity, floats, booleans in integer fields, inverted
supporting intervals, changed inputs, altered constants, missing assumptions
and an attempted scope promotion. Treat a serialized check_status as data, not
the verifier's decision.

An eventual admitted bridge gets a separately identified record revision and
evidence binding. Never rewrite the earlier arithmetic-only record as if its
execution had included that proof. Keep runtime timing/environment metadata in
a sidecar so the mathematical record can remain deterministic.

## 8. New Lean work: precise boundary

Proposed new module imports the existing F1/L2/L3/C01/C02 dependencies needed
for its statements. It is not the old minimal Z-only P1 dependency chain.

Implement in this order:

1. Public version of the explicit L2 decay estimate, proving it afresh from
   the same pinned integrand/support facts; no reference to mangled private names.
2. Exact prefix-only second-coefficient identity from the two normalized rows.
3. Positivity of s and the upper bound on rho_actual.
4. Main lower bound and absolute prefix upper bound with the same core/scale.
5. `q_star >= s*B` and the P=m=1 coarse rational reduction.
6. A conditional actual-c1 result under `F.amp eta>9/10`, using C02.
7. Optional separate wrapper consuming the full amplitude_spec conditions.

Theorem names and definitions must be frozen after checking collisions and the
pinned Mathlib API; do not prefill compiler outcomes in the plan. Every theorem
must retain its real hypotheses and distinguish general Parameters from the
fixed numerical core. Any rational positivity theorem for the chosen tuple must
be explicitly specialized.

Development compile is followed by statement/#print axioms review. Existing
standard axiom surfaces are compared, with no sorry/admit/new axiom. Later
proof-only and execution checkpoints, clean replay and dated admission require
their actual execution scope; do not change old modules or receipts to reuse an
old success. Arithmetic implementation can proceed before formal admission, but
its record keeps the static-bridge status until the new evidence exists.

## 9. Test matrix and review oracle

| Test family | Meaningful expected outcome |
| --- | --- |
| Exact constants | Independently derive H1_upper from (5/2+12*3^9)*3^8; do not only compare producer output to itself |
| Fixed rational decision | Recompute p and B with exact integer/Fraction expressions and the section 4 fixture |
| Sign/algebra direction | Synthetic normalized 2x2 systems with known exact solutions catch reversed debt signs and swapped beta rows |
| Bounds | Synthetic nonnegative U_i and positive A_i satisfying the declared ratio bound exercise the actual inequality and its failure outside assumptions |
| Scale conversion | Changing center index, dropping A_1/D, or calling B q must be rejected |
| Parser | Duplicate/missing/extra keys, oversized input, invalid rational, bool/float fields, NaN and changed tuple rejected |
| Mutation | Increased B, understated prefix upper, inflated kappa, rho changed below its justified bound, missing assumptions and self-promoted scope rejected |
| Verifier separation | Patching producer to raise must not affect verify; no import/call to producer for expected result |
| CLI | Successful round trip, tampered file nonzero exit, deterministic mathematical bytes, distinct error/unresolved handling |
| Regression | Existing core scalar records/tests unchanged; full suite and coverage gate pass after new code |

Synthetic tests exercise arithmetic and interface semantics; they are not
numerical source Profiles. The mathematical bridge requires actual proof/source
review. The separate mpmath backend is optional for tighter transcendental bounds,
not necessary to repeat an exact integer calculation or manufacture independence.

## 10. Follow-on P3: a normalized-J route worth checking

Do not make this follow-on a dependency of the first coefficient output.
There is a further static cancellation that may eliminate large exponentials
and row-moment evaluation from a normalized angular bound.

Let `K1=momentScale(c,1)*shape(eta)^2>0`, the actual P1 prefactor, and
`I01=A_0*exp(beta0*(L-1))`. The source matrix identity and admitted gap formula
give

```text
s*I01*Delta
 = (A_0/A_1)*exp(3*lambda/20)
     * expm1(17*lambda/10)/expm1(2*lambda)
 >= expm1(17*lambda/10)/expm1(2*lambda) =: R(lambda)>0.
```

The last comparison is L3. The exponent check is

```text
-beta1*(L-3) + beta0*(L-1)
 + (-13+23*lambda/20) - (1-4*lambda) = 3*lambda/20.
```

Thus, if the new coefficient bridge, same-Profile amplitude assumptions and
an admissible first-window exact M-zero are all supplied, P1 would imply

```text
localJ/K1 > B_coarse * R(lambda) > 0.
```

This is a **proposed normalized bound**, not an evaluated actual J. Use the
existing expm1 enclosures for a later R lower bound only after checking this
identity and the alias/coordinate bindings. A new Lean wrapper is required for
a formal claim. A numerical source-J claim still needs the correct coordinate
conversion and all applicable factors/assumptions.

If a qualifying Profile exists and the derived actual c1 is positive at this
eta, the existing conditional Z03 theorem can supply an interior mass zero.
That is conditional existence, not numerical root localization and not proof
that the selected numerical tuple constructs a Profile. Do not assume the
existential C04 epsilon contains the selected eta.

## 11. Budgets, fallback and stopping

Keep the fixed experiment: lambda=10^-12, eta=2^-20. Do not tune eta after a
failed calculation. Existing supporting precision schedule is at most
128 -> 256 -> 512 fractional bits, with 120 seconds per attempt. Exact rational
B needs no precision escalation; repeated identical exact arithmetic is not a
precision experiment. If exp(1)'s first enclosure establishes 2<e<3, stop there.

At most 2048 integration subintervals applies only if a justified fallback
quadrature method becomes necessary. No quadrature is budgeted or required by
the coarse baseline. No automatic dependency download, benchmark expansion or
unlimited refinement is part of a numerical run.

Fallback order:

1. If the source-to-bound algebra is wrong, correct the design and preserve
   the failed derivation; do not patch numbers to obtain a positive result.
2. If the rational baseline is too weak for a later input, use the tighter
   kappa/rho/explicit prefix expressions under the same reviewed semantics.
3. Only if analytic bounds remain insufficient, design the needed validated
   integral calculation under the existing budget.
4. A nonpositive conservative bound is an unresolved positivity decision,
   not a negative actual coefficient or a refutation of the source theorem.

## 12. Practical-use transition and completion gates

MomentBound v0.1 is complete as an **arithmetic prototype** when the specified
record, rational verifier, rejection tests and reproducible invocation work.
It is complete as a **formally connected coefficient result** only after the
new bridge's actual proof/replay/review scope is satisfied. Both statuses must
remain visible; a passing Python suite does not fill the formal gap.

After that milestone, choose one P4-B weighted-moment/denominator task with
observable inputs and a declared decision. Compare ordinary/stable evaluation,
an appropriate validated method and an analytic-bound-aware baseline given
the same information. Measure error/bound width, invalid ratio acceptance,
unnecessary rejection, runtime and memory on held-out cases.

A fixed positive B result does not demonstrate workload benefit. If an equally
informed standard method performs the same operation as well, report that
finding and choose the next useful problem. No uniqueness, first-zero ordering,
pole, full Profile evaluator or deployed scientific tool is part of v0.1.

## 13. Handoff discipline

Use [TASKS.md](TASKS.md) for execution order. Preserve the existing dirty
worktree. Restore a project-specific D: environment, rather than repointing
the shared venv used by other projects. Use the pinned Colab Lean environment
for separately authorized compile work; do not install Lean on Windows or run
lake update as a side effect of Python setup.

Keep raw logs under ignored outputs/colab evidence. Keep proof/runner changes
separate from planning docs when a later checkpoint is authorized. No historical
receipt, upstream source, claim ledger or public paper is rewritten to record
the proposed result. No implementation, new Lean compile, commit, push or
publication was performed during preparation of this design.
