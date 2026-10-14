# M5 P2 Z+J source map — first-repair mass-zero / angular-moment mismatch

Date: 2026-10-11 (Asia/Bangkok)

```text
check_status: PASS[STATIC_PINNED_SOURCE_MAPPING]
claim_authority: NONE
claim_status: UNVERIFIED
formal_bridge_status: UNVERIFIED[NOT_IMPLEMENTED_OR_COMPILED]
Z04_core_dependency: PASS[LOCAL_PROOF_COMPILE:P2_Z04_CORE]
independent_attestation: false
```

This document is a static source/derivation map for the bounded Z+J question.
It is not a Lean compile record, receipt, novelty claim, or public theorem
admission.

Pinned source:

```text
repo: openai/NavierStokesAndEuler
commit: 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538
```

The successful Z04-core proof bytes remain unchanged.

## 1. Question

The P2 study began from the candidate ratio

```text
Q = J / (M H).
```

Z04-core development establishes the local existence chain toward an interior
first-repair mass zero for sufficiently small positive eta, but no J/Q result
is admitted.

The bounded Z+J question is:

> At a first-repair-window point where the source mass moment vanishes and the
> actual second repair coefficient is positive, must the source angular moment
> be strictly positive?

The preferred structural theorem is witness-independent:

```text
lower(0) < r < upper(0)
localMass(F,eta,r) = 0
0 < c1(F,eta)
--------------------------------
0 < localAngularMoment(F,eta,r)
```

No eta-sign or C04 epsilon belongs in this structural theorem. Those are
supplied only by the later existence composition.

## 2. Fixed source objects

For one pinned-source `Profile F`, write:

```text
c    := F.data.core
amp  := F.amp
B    := c.pulseStart
L    := c.pulseLength
R    := exp L

a0   := c.exponents 0 = -(1/2 + c.lam)
a1   := c.exponents 1 = -(1/2 + 2*c.lam)

l0   := c.lower 0
u0   := c.upper 0
l1   := c.lower 1
u1   := c.upper 1

b0(x):= LocalizedMomentRepair.bump l0 u0 x
b1(x):= LocalizedMomentRepair.bump l1 u1 x

c0   := LocalizedMomentRepair.coefficients
          c.exponents c.lower c.upper (debt c amp eta) 0
c1   := LocalizedMomentRepair.coefficients
          c.exponents c.lower c.upper (debt c amp eta) 1

K0(eta) := momentScale c 0 * shape eta
K1(eta) := momentScale c 1 * (shape eta)^2
```

Existing NSRW aliases:

```text
localMass F eta r
  = massMoment c amp eta (B + log r)

localSecondRepairCoefficient F eta
  = c1
```

Recommended new alias:

```text
localAngularMoment F eta r
  := angularMoment c amp eta (B + log r)
```

## 3. Pinned source facts already located

### 3.1 Exponents

Pinned `OutgoingSchedule.lean` defines

```text
a0 = -(1/2 + lam)
a1 = -(1/2 + 2*lam)
```

hence

```text
a1 = a0 - lam.
```

For positive x, the intended rpow rewrite is

```text
x^a1 = x^a0 * x^(-lam).
```

This must be proved with positive-base hypotheses in Lean.

### 3.2 Repair-window ordering

Pinned definitions give:

```text
l0 = exp(L - 63/20)
u0 = exp(L - 57/20)
l1 = exp(L - 23/20)
u1 = exp(L - 17/20)
```

Therefore

```text
1 < l0 < u0 < l1 < u1 < R.
```

The source theorem `intervals_separated` only exposes a weak separation
`u0 <= l1`; Z+J should prove the strict helper `u0 < l1` directly from the
pinned definitions.

### 3.3 Bump support and sign

Pinned `LocalizedMomentRepair.lean` provides:

```text
bump_nonneg
bump_support_subset
bump_tsupport_subset
bump_tsupport_subset_open
```

The bump support lies in the middle half of each outer repair window.

Important boundary:

```text
T0 > 0
```

means positive first-bump mass remains somewhere in the future tail. It does
not imply `b0(r) > 0` at the current point. Therefore this source map does not
claim a simple zero or uniqueness.

### 3.4 Paired terminal cancellation

Pinned `pulse_closes_prefix` gives both components:

```text
prefixM*eta + K0 * integral_1^R x^a0 radialPulse = 0

prefixJ*eta*shape(eta)
  + K1 * integral_1^R x^a1 radialPulse = 0.
```

Thus the mass and angular tails have exactly parallel cancellation structure.

### 3.5 Pulse integrand bridges

Pinned source provides:

```text
mass_integrand_pulse
angular_integrand_pulse
exp_weight_substitution
radialPulse_continuousOn
```

These are sufficient to mirror Z01 for the angular moment.

### 3.6 Pulse-start moments

Pinned source provides:

```text
massMoment_at_pulseStart
angularMoment_at_pulseStart.
```

The angular pulse-start value is

```text
prefixJ c * eta * shape eta.
```

### 3.7 Source coordinate bridges

Pinned `OutgoingProfile.lean` provides:

```text
M_at_exp
J_at_exp
```

for nonnegative global log-coordinate y.

For this research lane use `1 <= r`, so

```text
0 <= B + log r
exp(B + log r) = exp(B) * r.
```

No extra scale factor appears between `angularMoment` and `Profile.J`.

## 4. Angular partial and tail identities

The Z01 mass proof has a direct angular analogue.

Target partial identity:

```text
localAngularMoment(F,eta,r)
 =
 prefixJ(c)*eta*shape(eta)
 + K1(eta)
   * integral_1^r x^a1 radialPulse(c,amp,eta,x)
```

for

```text
1 <= r <= R.
```

Target tail identity:

```text
localAngularMoment(F,eta,r)
 =
 -K1(eta)
   * integral_r^R x^a1 radialPulse(c,amp,eta,x).
```

Expected source ingredients:

```text
angularMoment_at_pulseStart
angular_integrand_pulse
exp_weight_substitution
(pulse_closes_prefix ...).2
```

This is a formal bridge obligation. It has not yet been implemented or
compiled.

## 5. First-window future radial pulse

Assume:

```text
l0 < r < u0
r <= x <= R.
```

Since the pinned main-pulse end lies strictly before `l0`, the main pulse is
zero throughout this future interval.

The correction has exactly the two repair bumps, so the intended reduction is:

```text
radialPulse(c,amp,eta,x)
 =
 c0*b0(x) + c1*b1(x).
```

Unlike Z02's `upperTail_radialPulse_eq`, the first bump cannot be killed
because r lies inside the first outer repair window.

Recommended helper:

```text
radialPulse_after_first_lower_eq_repair_pair
```

with a hypothesis sufficient to place x after the main pulse.

## 6. Tail quantities

For fixed r in the first repair window define:

```text
T0(r) := integral_r^R x^a0 * b0(x)
T1(r) := integral_r^R x^a0 * b1(x)

S0(r) := integral_r^R x^a1 * b0(x)
S1(r) := integral_r^R x^a1 * b1(x).
```

Because

```text
r < u0 < l1
```

and the second bump is supported inside `(l1,u1)`, the entire second bump lies
in the future of r.

Thus

```text
T1(r)
 =
 integral_R x^a0*b1(x)
```

and existing Z02 theorem `secondBumpWeightedMoment_pos` gives

```text
T1(r) > 0.
```

A corresponding whole-line angular second-bump moment may be useful for
integrability or comparison, but strict positivity of S1 is not required by
the main argument.

## 7. Mass zero forces c0 < 0 and T0 > 0

The mass tail identity and the two-bump decomposition give:

```text
localMass(F,eta,r)
 =
 -K0(eta) * (c0*T0 + c1*T1).
```

Pinned/source facts give:

```text
K0(eta) > 0
T0 >= 0
T1 > 0.
```

Assume:

```text
localMass(F,eta,r) = 0
c1 > 0.
```

Then:

```text
c0*T0 + c1*T1 = 0
c0*T0 = -c1*T1 < 0.
```

Since `T0 >= 0`, this forces:

```text
T0 > 0
c0 < 0.
```

No independent estimate on the first repair coefficient is needed.

This is a central simplification of the Z+J route.

## 8. Weighted-tail comparison

Because

```text
a1 = a0 - lam,
```

for x > 0:

```text
x^a1 = x^a0 * x^(-lam).
```

Since `lam > 0`, the function `x -> x^(-lam)` is strictly decreasing on
positive x.

### 8.1 First bump

For x where `b0(x) != 0`, support gives

```text
x < u0.
```

Therefore

```text
u0^(-lam) <= x^(-lam).
```

Outside the bump support both weighted bump integrands are zero.

Hence the intended interval-integral comparison is:

```text
u0^(-lam) * T0 <= S0.
```

### 8.2 Second bump

For x where `b1(x) != 0`, support gives

```text
l1 < x.
```

Therefore

```text
x^(-lam) <= l1^(-lam).
```

Hence:

```text
S1 <= l1^(-lam) * T1.
```

### 8.3 Strict separation of the constants

From

```text
u0 < l1
lam > 0
```

one obtains:

```text
l1^(-lam) < u0^(-lam).
```

A robust Lean path is available through positive-base rpow identities and
monotonicity; if direct negative-exponent lemmas are awkward, rewrite negative
powers as inverses of positive powers or use the log/exp definition.

The proof should not rely on an unverified theorem name.

## 9. Angular tail sign

Using `c0 < 0`, `c1 > 0`, the two weighted comparisons, and

```text
c0*T0 = -c1*T1,
```

derive:

```text
c0*S0 + c1*S1
 <= c0*u0^(-lam)*T0 + c1*l1^(-lam)*T1
  = c1*T1*(l1^(-lam) - u0^(-lam))
  < 0.
```

The sign reversal in the first term is essential because `c0 < 0`.

The angular tail identity gives:

```text
localAngularMoment(F,eta,r)
 =
 -K1(eta) * (c0*S0 + c1*S1).
```

Pinned facts give:

```text
K1(eta) > 0
```

for all real eta, because `momentScale_pos` and `shape_pos` are global.

Therefore:

```text
0 < localAngularMoment(F,eta,r).
```

No eta-sign hypothesis is required for this structural theorem.

## 10. Source-facing J bridge

Recommended helper:

```text
localAngularMoment_eq_profileJ
  (hr : 1 <= r)
:
localAngularMoment F eta r
 =
F.J eta (exp(B)*r).
```

Use pinned `J_at_exp` and the same coordinate algebra as Z04-core's
`localMass_eq_profileM`.

For a first-window r, `1 <= r` follows from `one_lt_lower 0`.

## 11. Preferred structural theorem surface

Recommended target:

```lean
theorem localAngularMoment_pos_of_firstRepair_mass_zero
    (F : Profile) (eta r : ℝ)
    (hr_lower : F.data.core.lower 0 < r)
    (hr_upper : r < F.data.core.upper 0)
    (hM : localMass F eta r = 0)
    (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < localAngularMoment F eta r
```

Source-facing companion:

```lean
theorem profileJ_pos_of_firstRepair_profileM_zero
    ...
    (hM : F.M eta (exp B * r) = 0)
    (hc1 : 0 < localSecondRepairCoefficient F eta) :
    0 < F.J eta (exp B * r)
```

The exact source-facing statement may instead consume the local mass equality
to avoid unnecessary reverse-coordinate rewriting. Choose the smaller stable
surface after implementation.

## 12. Final existence composition

Do not modify successful Z04-core bytes merely to carry c1 through its public
existence theorem.

The final Z+ composition can separately consume C04 and Z03/Z04 bridges:

```text
C04:
  exists epsilon > 0,
  0 < eta < epsilon -> actual c1 > 0

alias bridge:
  local c1 = actual c1

Z03:
  eta > 0 and local c1 > 0
  -> exists first-window r with localMass = 0

Z+J structural theorem:
  first-window localMass = 0 and local c1 > 0
  -> localAngularMoment > 0

M/J coordinate bridges:
  -> Profile.M = 0 and Profile.J > 0 at the same source point.
```

Target combined proposition:

```text
forall F,
exists epsilon_F > 0,
forall eta,
  0 < eta < epsilon_F ->
  exists r,
    l0 < r < u0
    and F.M eta (exp(B)*r) = 0
    and 0 < F.J eta (exp(B)*r).
```

This is separate from the Z04-core existence theorem even if a later clean
full-DAG replay executes both in one run.

## 13. Q consequence and boundary

If the combined proposition closes, then at the same source point:

```text
M = 0
J > 0.
```

Thus numerator cancellation does not accompany mass cancellation.

For the intended ratio candidate

```text
Q = J / (M H),
```

an admissibility predicate requiring

```text
M * H != 0
```

fails automatically because M = 0.

Do not infer yet:

- simple pole;
- blow-up rate;
- unique or first zero;
- two-sided Q limit;
- non-removable extension without a proved admissible-domain approach result;
- literature novelty;
- a general Navier-Stokes consequence.

Lean real division is total, so "Q undefined" must refer to the intended
mathematical admissibility condition, not raw evaluation of Lean's division.

## 14. Implementation obligations

Recommended order:

```text
Z+J-01
  localAngularMoment definition
  angular partial identity
  angular tail identity

Z+J-02
  local first coefficient alias
  radialPulse future pair decomposition
  second-bump tail = whole-line mass moment

Z+J-03
  mass-zero coefficient identity
  T0 >= 0, T1 > 0
  T0 > 0, c0 < 0

Z+J-04
  a1 = a0 - lam
  strict u0 < l1
  positive-base rpow factorization
  decreasing-weight helpers

Z+J-05
  S0/T0 and S1/T1 integral comparisons

Z+J-06
  structural localAngularMoment > 0 theorem

Z+J-07
  Profile.J coordinate bridge

Z+J-08
  small-positive-eta M=0 and J>0 existence composition
```

No implementation or compile has been performed by this source-map review.

## 15. Falsifiers / stop conditions

Stop or narrow Z+J if any of the following occurs:

- the angular tail identity cannot be obtained from the pinned source without
  adding assumptions absent from the construction;
- the first/second bump tail cannot be separated with the source support facts;
- the weighted rpow comparison fails on the actual positive support;
- the sign algebra requires an unproved sign of c0 rather than deriving it from
  the mass-zero identity;
- the source Profile.J bridge changes the object or coordinate being studied.

A Lean API/tactic failure is not a mathematical falsification.

## 16. Static verdict

```text
Z+J source route:
  SUPPORTED[STATIC_PINNED_SOURCE_MAPPING]

Key reason:
  paired terminal cancellation
  + separated repair supports
  + a1 = a0 - lam
  + c1 > 0
  + mass zero
  force a strictly negative angular weighted tail
  and hence positive local angular moment.

Formal theorem:
  UNVERIFIED[NOT_IMPLEMENTED_OR_COMPILED]

Next action:
  implement Z+J-01 through Z+J-06 in a separate proof module,
  without modifying successful Z04-core proof bytes.
```
