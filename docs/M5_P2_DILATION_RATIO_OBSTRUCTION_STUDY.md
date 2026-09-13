# M5 P2 dilation-ratio obstruction study

Status: active mathematical analysis; no new theorem, numerical witness, or
source-bound ten-law atlas is claimed.

This note studies one question created by the reviewed-static P1 scaling
metadata. It is deliberately independent of the held same-raw export/ledger
lane: P1 constrains the authority of an executable atlas, not the ability to
read and reason from the pinned source at its stated scope.

## Question and notation

For a source `Profile` `F`, dilation factor `XR`, angular coordinate `eta`,
and radial coordinate `X`, define the prospective ratio only where its
denominator is nonzero:

```text
Q(F, XR, eta, X) = J(F, XR, eta, X)
                   / (M(F, XR, eta, X) * H(F, XR, (X, eta))).
```

The question is not whether its scaling degree is formally zero. The question
is whether this ratio is defined on a source-relevant region and whether it can
contribute a useful Support, Cone, or Moment statement there.

## Source-located scaling calculation

Pinned source: `openai/NavierStokesAndEuler` commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`,
`NavierStokes/OutgoingDilation.lean`.

For `0 < XR`, the source gives:

```text
H(F, XR, (X, eta)) = sqrt(XR) * F.H(X / XR, eta)       [H_scaling, 80--85]
M(F, XR, eta, X)  = XR * F.M(eta, X / XR)              [M_scaling, 104--106]
J(F, XR, eta, X)  = XR * sqrt(XR) * F.J(eta, X / XR)   [J_scaling, 115--120]
```

Consequently, with `x = X / XR` and the additional nonzero conditions
`F.M(eta, x) != 0` and `F.H(x, eta) != 0`, elementary cancellation gives:

```text
Q(F, XR, eta, X) = F.J(eta, x) / (F.M(eta, x) * F.H(x, eta)).
```

This is a source-located algebraic derivation. It is not yet a new Lean theorem
or a statement that the ratio is globally defined, bounded, or useful.

## Current P2 status

```text
P2-A   GLOBAL OBSTRUCTION
       ESTABLISHED[SOURCE-LOCATED]

P2-B1  IDEAL PREFIX RATIO
       ESTABLISHED[SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE]

P2-B2  PRE-PULSE MASS SIGN
       ESTABLISHED[SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE]

P2-C   PULSE-INTERVAL ZERO GEOMETRY
       OPEN[PRIMARY_MATHEMATICAL_QUESTION]

P2-C1  EARLY-PULSE NO-ZERO REGION
        ESTABLISHED[SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE]

P2-C2  "ENDPOINT IS FIRST ZERO"
        REJECTED_AS_STATED[SOURCE_SUPPORT_CONTRADICTION]

P2-C3  TERMINAL ZERO PLATEAU
        ESTABLISHED[SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE]

P2-C4  ACTIVE REPAIR-WINDOW ZERO GEOMETRY
        ACTIVE[POSITIVE_SMALL_ETA_FIRST_WINDOW_ZERO_SUPPORTED;
        FULL_GEOMETRY_OPEN]

P2-C4a MAIN-PULSE COMPONENT OF SECOND REPAIR COEFFICIENT
        SUPPORTED[PINNED_DEFINITIONS_NEW_COMPARISON_ARGUMENT;
        FORMALIZATION_OPEN]

P2-C4b POSITIVE-SMALL-ETA FIRST-REPAIR ZERO
        SUPPORTED[PINNED_DEFINITIONS_AND_TAIL_ARGUMENT;
        FORMALIZATION_OPEN]

P2-D   CONE / MOMENT USEFULNESS
       OPEN

P2-E   CANONICAL-KERNEL COMPARATOR
       OPEN
```

## Formal reproduction status

The following narrow parts of this study have compiled external Lean receipts
under the pinned source and toolchain:

```text
P2-L1  mainPulse nonnegativity and mainPulse(1/25) positivity
       CONFIRMED[PINNED_SOURCE_TOOLCHAIN_EXTERNAL_MODULE]

P2-F1  0 < mainMoment c (1 : Fin 2)
       CONFIRMED[PINNED_SOURCE_TOOLCHAIN_EXTERNAL_MODULE]
```

The P2-F1 receipt is
[`P2_F1_LOCAL_WINDOWS_2026-09-13.md`](stage_receipts/P2_F1_LOCAL_WINDOWS_2026-09-13.md).
Its stronger compiled lower bound is an implementation aid; the study promotes
only the positivity proposition above.

`P2_L2_NormalizedMainMomentComparison.lean` currently supplies source-bound
normalization identities and a normalized `i = 1` positivity wrapper. It is
an **uncompiled scaffold**, not a formal L2 result. In particular, the strict
normalized comparison, `DeltaM < 0`, repair-coefficient signs, and the
first-repair zero remain outside this formal receipt surface.

`SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE` is deliberately narrower than a source
theorem: the result follows by combining pinned definitions and lemmas, but is
not asserted here to be a declaration already proved in the Lean source.

## Definition-domain audit

The source defines `M` as the radial primitive of `U`, `J` as the radial
primitive of `H * U`, and `H = sqrt(2X) * E`
([definitions, 61--78](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingDilation.lean#L61-L78)).

The source theorem `positive` states `0 < E(F, XR, p)` for every `p`
([139](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingDilation.lean#L139)).
Thus on the physically relevant positive radial axis, `X > 0` is a sufficient
condition for `H(F, XR, (X, eta)) > 0`. On that region, the denominator issue
for `Q` reduces to the zero set of `M`.

`J = 0` is **not** a definition-domain obstruction: it makes a defined ratio
equal to zero when `M * H != 0`. It may still matter for usefulness, signs, and
moment structure.

## P2-A: global after-pulse obstruction

The source theorem `after_pulse` states that if:

```text
0 < XR
0 < X
pulseEndRadius(F, XR) <= X
```

then `U(F, XR, (X, eta)) = 0`, `M(F, XR, eta, X) = 0`, and
`J(F, XR, eta, X) = 0`
([348--354](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingDilation.lean#L348-L354)).

Therefore `Q` is undefined in every such after-pulse point: its denominator
contains `M = 0`. This is a source-confirmed obstruction to using `Q` as a
global radial quantity. It does **not** decide whether there is a nonempty
pre-pulse region on which `M != 0` and the ratio has a useful estimate.

## P2-B1: ideal-prefix ratio

On the ideal prefix, let `0 < XR`, `0 < X <= XR`, `eta != 0`, and
`x = X / XR`. The source's `ideal_prefix` interface gives the base-profile
relations `E = P * shape(eta) * x^(1/10)` and `U = 4 * eta`
([338--346](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingDilation.lean#L338-L346)).
Together with the definitions of `M`, `J`, and `H`, integration on the positive
prefix yields:

```text
M = 4 * eta * X
H = sqrt(2) * P * shape(eta) * XR^(-1/10) * X^(3/5)
J = (5/2) * sqrt(2) * P * eta * shape(eta) * XR^(-1/10) * X^(8/5)

Q(F, XR, eta, X) = 5/8.
```

This is an exact source-located algebraic consequence, including the elementary
integral of the ideal field; it is not a claim that the source contains a
theorem named `Q_eq_five_eighths`. Positivity of `shape` is source-proved
([OutgoingSchedule 147](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L147)),
and the already noted positivity of `H` applies for `X > 0`.

At `eta = 0`, the same ideal-prefix formulas give `M = J = 0`; `Q` is
undefined because `M = 0`. Thus `eta != 0` is a genuine domain condition, not
an omitted boundary case.

## P2-B2: pre-pulse mass sign

This statement uses the base log coordinate `y`, and separates two intervals
because their source justifications differ.

For `y <= 0`, the source gives the ideal axial field `U(exp(y), eta) = 4 * eta`
([OutgoingSchedule 803--806](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L803-L806)).
Integrating the mass primitive from the axis therefore gives:

```text
M(eta, exp(y)) = 4 * eta * exp(y).
```

Hence `sign(M) = sign(eta)` for `y <= 0`, and `M != 0` when `eta != 0`.

For `0 <= y <= pulseStart`, `M_at_exp` identifies the mass with
`massMoment`, while `axial_before_pulse` supplies the integrand:

```text
M(eta, exp(y))
  = eta * [4 + integral(0, y, exp(t) * dropCoefficient(m, t) dt)].
```

([OutgoingProfile 436--449](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingProfile.lean#L436-L449),
[OutgoingSchedule 507--509](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L507-L509)).
The pinned bound `dropCoefficient >= 0`
([OutgoingSchedule 243--248](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L243-L248))
makes the bracket at least `4` on this oriented interval. Therefore `eta != 0` implies `M != 0` and
`sign(M) = sign(eta)` throughout this second interval.

Consequently, the entire pre-pulse region is a defined region for `Q` when
`eta != 0` (after applying the existing dilation relation to the physical
coordinate). This is a source-located algebraic consequence, not a new source
theorem. It does not make any claim about the pulse interval itself.

## P2-C: pulse-interval zero geometry

At pulse start, the source identifies the mass moment as
`M = prefixM * eta`; at the pulse endpoint it proves exact terminal
cancellation `M = 0`
([OutgoingSchedule 749--761](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L749-L761),
[846--878](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L846-L878)).

For local pulse radius `r = exp(y - pulseStart)`, write

```text
M_pulse(eta, r) = M(eta, exp(pulseStart + log(r))).
```

The local notation is used below whenever `r`, `lower(i)`, `upper(i)`, or
`R = exp(pulseLength)` appears. It prevents a local repair radius from being
silently identified with the base profile's global radial coordinate.

### C1: source-located early-pulse exclusion

There is a limited, source-located exclusion zone before the first repair
window. Write `s = y - pulseStart` and restrict to the specification range
`eta^2 <= 1`. The specification supplies `amp(eta) > 9/10`
([OutgoingProfile 564--566](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingProfile.lean#L564-L566)).

The main pulse is supported before `11 / lam`; each correction interval begins
strictly after that endpoint
([OutgoingSchedule 282--285](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L282-L285),
[368--375](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L368-L375)).
The correction has support only in its two declared open intervals
([422--423](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L422-L423),
[447--455](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L447-L455)).

Thus, up to the lower endpoint of the first repair interval, `radialPulse` is
the positive-amplitude multiple of `eta * mainPulse`, followed by a zero gap.
From the nonnegative cutoff factors in the definition of `mainPulse`, its
contribution has the sign of `eta`. Combined with the nonzero, same-signed
pre-pulse value, this gives:

```text
eta^2 <= 1 and eta != 0
and pulseStart <= y <= firstRepairStart
    => sign(M(eta, exp(y))) = sign(eta)
       and M(eta, exp(y)) != 0.
```

This is again a source-located algebraic consequence, not a theorem name from
the source. It is deliberately restricted to the specified angular range and
does not extend across either repair interval.

### C2: endpoint-first-zero condition rejected

The previously proposed condition

```text
eta * integral(r, R, x^a * radialPulse(eta, x) dx) < 0
for every 1 <= r < R
```

is **rejected as stated**. It would assert that the endpoint is the first zero
of `M`, but the source support geometry rules this out.

### C3: terminal zero plateau

Let `u1 = upper(1)` and `R = exp(pulseLength)`. The source gives
`u1 < R`. For `u1 < r < R`, both summands in `radialPulse` vanish:

```text
mainPulse(lam * log(r)) = 0
correction(eta, r) = 0
radialPulse(eta, r) = 0.
```

The first follows because the main pulse ends before every repair interval;
the second follows because the repair is supported in the two separated open
intervals, both below `u1`
([OutgoingSchedule 363--375](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L363-L375),
[347--352](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L347-L352),
[447--455](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L447-L455),
[543--544](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L543-L544)).

The full-pulse cancellation gives `M(R) = 0`. Hence the radial primitive is
already zero on this terminal inactive interval:

```text
u1 < r < R
  => integral(r, R, x^a * radialPulse(eta, x) dx) = 0
  => M_pulse(eta, r) = 0.
```

This passage uses the source bridge from `massMoment` to the profile mass at
positive log radii
([OutgoingProfile 436--449](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingProfile.lean#L436-L449)).

This is an `ESTABLISHED[SOURCE-LOCATED_ALGEBRAIC_CONSEQUENCE]`, not a direct
source theorem with this statement. It strengthens P2-A: `Q` is already
undefined on a nonempty terminal interval before the after-pulse theorem's
endpoint regime begins. The interval above is safe rather than sharp; the
actual bump supports end strictly inside their declared repair intervals.

### C4: repair-coefficient and partial-tail problem

The remaining question is not whether the endpoint is the first zero. It is:

```text
Does M_pulse retain sign(eta) throughout the active repair support,
until it enters the inevitable terminal zero plateau?

Or does it cross zero earlier inside a repair window?
```

The repair has the exact two-bump form

```text
correction(eta, x) = c0(eta) * b0(x) + c1(eta) * b1(x),
```

where each `bj` is nonnegative and its support lies in its corresponding,
separated repair interval
([LocalizedMomentRepair 25--35](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/LocalizedMomentRepair.lean#L25-L35),
[111--115](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/LocalizedMomentRepair.lean#L111-L115)).
Thus the second repair window reduces first to the sign of `c1`: where its
remaining weighted bump tail is positive, sign preservation requires
`eta * c1 < 0`. The first repair window additionally requires a comparison of
the partial `c0` tail with the future `c1` tail.

The source's normalized system makes this sign question explicit. Set
`Ai = rowMoment(exponents(i))`, `rho_i = exp(2 * beta(i))`,
`Di = normalizedDebt(i)`, and `zi = Di / Ai`. For the actual coefficients,
the source gives:

```text
A0 * (c0 + rho_0 * c1) = D0
A1 * (c0 + rho_1 * c1) = D1
rho_0 > rho_1.

c1 = (z0 - z1) / (rho_0 - rho_1)
c0 = (rho_0 * z1 - rho_1 * z0) / (rho_0 - rho_1).
```

([OutgoingPulseBounds 577--608](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L577-L608),
[727--750](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L727-L750)).

Therefore absolute coefficient bounds alone are insufficient. The remaining
questions are the full `eta`-dependent ordering of `z0 - z1` and
`rho_0 * z1 - rho_1 * z0`, followed in the first window by a partial-tail
domination estimate. The source's named correction-jet bounds remain absolute
bounds only; they do not themselves state these signs.

#### C4a: small-eta main-pulse falsifier

The second coefficient has a particularly sharp adversarial test. Let

```text
q(eta) = eta * (1 + eta^2)
alpha_i = exp(-beta(i) * center(0)) / Ai > 0

DeltaP = alpha_0 * prefixCoefficient(0) - alpha_1 * prefixCoefficient(1)
DeltaM = alpha_0 * mainMoment(0) - alpha_1 * mainMoment(1).
```

The source definitions of `debt`, `normalizedDebt`, and `affineCoefficients`
then give the algebraic identity:

```text
z0 - z1 = -q(eta) * DeltaP - amp(eta) * DeltaM.
```

Equivalently, for the main-pulse-only affine input,

```text
affineCoefficients(c, 0, 1, 1) = -DeltaM / (rho_0 - rho_1).
```

([OutgoingSchedule 407--423](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L407-L423),
[OutgoingPulseBounds 727--750](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L727-L750),
[875--880](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L875-L880)).

Within the specification range, `amp` is continuous and remains positive at
`eta = 0`, while `q(eta)` vanishes there. If `DeltaM != 0`, then `c1` has a
fixed nonzero sign in a two-sided neighbourhood of zero. Consequently the
necessary second-window condition `eta * c1 < 0` cannot hold for both small
positive and small negative `eta`.

This makes the following a necessary-condition falsifier for any uniform
two-sided sign-preservation claim:

```text
DeltaM = 0

equivalently:
affineCoefficients(c, 0, 1, 1) = 0.
```

The normalizers cannot be discarded. However, the pinned definitions supply a
comparison that is stronger than the available absolute bounds. Put

```text
Fi = exp(-beta(i) * center(0)) * mainMoment(i).
```

The `mainMoment_log_short` representation and `beta_0 - beta_1 = lam` give

```text
F0 = integral(0, 11 / lam,
              exp(beta_1 * (y - center(0)))
              * exp(lam * (y - center(0)))
              * mainPulse(lam * y)).
```

On this integration interval, `y - center(0) <= -2 / lam + 3`, so, from
`lam < 1/10`,

```text
F0 / F1 <= exp(-2 + 3 * lam) < exp(-(3 / 20) * lam).
```

Here `F1 > 0`: the cutoff definition makes `mainPulse` nonnegative on its
positive support and nonzero on a subinterval. This is an elementary
positivity consequence of the pinned definition, not a separately located
source theorem. The needed ingredients are the cutoff bounds
([OutgoingSchedule 52--55](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L52-L55)),
the definitions of `pulseRamp` and `mainPulse`
([260--262](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L260-L262)),
and the compact-support representation of `mainMoment`
([OutgoingPulseBounds 786--841](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L786-L841)).

Independently, `exponents(0) - exponents(1) = lam`. Since `rowMoment` is the
positive integral of the nonnegative template supported in
`(exp(-3/20), exp(3/20))`, its two normalizers obey

```text
A0 / A1 >= exp(-(3 / 20) * lam).
```

This uses the template support and nonnegativity facts
([OutgoingPulseBounds 409--430](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L409-L430))
with the definition of `rowMoment`; it is not inferred from the much coarser
uniform `rowMoment_bounds` theorem.

Combining the strict first comparison with the weak second comparison yields

```text
F0 / A0 < F1 / A1
DeltaM = F0 / A0 - F1 / A1 < 0
affineCoefficients(c, 0, 1, 1) > 0.
```

This is a new analytic comparison assembled from pinned definitions and
elementary integral monotonicity. It is **not** a source theorem and has not
yet been encoded or compiled as a Lean lemma; accordingly its claim status is
`SUPPORTED`, not `ESTABLISHED`.

The amplitude component of `c1` is consequently positive. Since `amp(0) > 0`
and `q(0) = 0`, continuity gives `c1(eta) > 0` for all sufficiently small
`|eta|`. For sufficiently small positive `eta`, the necessary second-window
sign-preservation condition `eta * c1 < 0` therefore fails.

This also locates an interior zero more precisely than the initial
obstruction. Let `a0 = exponents(0)`, choose sufficiently small positive
`eta`, and write

```text
K(eta) = momentScale(0) * shape(eta) > 0.
```

At `r = upper(0)`, and throughout the gap after the first repair support,
the main pulse and the first bump vanish. The future pulse contribution is
therefore only the second bump. Exact endpoint cancellation and the mass
integrand identity give the tail representation

```text
M_pulse(eta, r) = -K(eta) * c1(eta)
                  * integral(lower(1), upper(1), x^a0 * b1(x) dx) < 0.
```

The weighted second-bump integral is strictly positive: `b1` is nonnegative,
equals one at its center, and the radial weight is positive. On the other
hand C1 gives `M_pulse(eta, lower(0)) > 0`. Continuity of the mass primitive now
forces

```text
exists r_* in (lower(0), upper(0)), M_pulse(eta, r_*) = 0.
```

Thus, for sufficiently small positive `eta`, the zero is not merely somewhere
in the union of repair supports: it lies in the **first repair window**. This
is a source-definition tail argument, not a source theorem or compiled Lean
result. It is consequently `SUPPORTED`, with formalization still required.
The relevant source identities are `mass_integrand_pulse`
([OutgoingSchedule 695--713](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L695-L713)),
endpoint cancellation
([846--878](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingSchedule.lean#L846-L878)),
and the strict interior support/nonnegativity of the repair bumps
([LocalizedMomentRepair 25--68](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/LocalizedMomentRepair.lean#L25-L68)).

The promotion obligation is narrow and has four components:

```text
L1  main-pulse positivity: F1 > 0
L2  normalized main-pulse comparison: F0 / F1 < exp(-(3/20) * lam)
L3  template moment-ratio comparison: exp(-(3/20) * lam) <= A0 / A1
L4  second-tail and first-window zero:
    c1 > 0 -> M_pulse(eta, upper(0)) < 0
           -> exists r in (lower(0), upper(0)), M_pulse(eta, r) = 0.
```

Their composition proves `DeltaM < 0` and then the positive-small-`eta`
first-window zero. No numerical `TailData` witness or new verifier framework
is needed for this proof obligation.

The source provides exact full moments and uniform absolute correction-jet
bounds under a small-`lam` hypothesis
([OutgoingPulseBounds 1134--1146](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingPulseBounds.lean#L1134-L1146)).
The source does not provide a named theorem for the comparison above, nor does
it settle the full `eta`-dependent coefficient signs or partial-tail
domination. Those are the current analytic boundary.

The primary open question is the geometry of the zero set between these two
facts:

```text
- For negative or non-small `eta`, does M retain sign(eta) until it reaches
  the terminal zero plateau?
- For negative or non-small `eta`, can the mass retain its sign through both
  repair supports, and what is the complete zero set?
- What ordering of `DeltaP` and the full `eta`-dependent `z0 - z1` determines
  the signs of `c0` and `c1` away from the small-eta obstruction?
- What partial-tail domination is needed in the first repair window?
- What bound, if any, follows for Q - 5/8?
```

The relevant source path is:

```text
axial_pulse
  -> radialPulse
  -> mainPulse + correction
  -> mass_integrand_pulse
  -> pulse_closes_prefix
  -> massMoment_endpoint
```

The inspected source gives exact endpoint cancellation and the stronger
terminal-zero plateau derived above, but it has not supplied a one-sided
coefficient ordering or partial-tail domination lemma sufficient to settle
the active repair windows. P2-C is therefore the first new analysis question
in this lane, rather than a closure claim.

## P2-D: Cone and Moment usefulness

Only after P2-C identifies a source-relevant region on which `Q` is defined
and controlled can this project assess whether `Q` or `Q - 5/8` helps a
Support, Cone, or Moment estimate. Manufactured fixtures and finite numerical
samples cannot settle that implication.

## P2-E: comparator — scaled canonical kernel

The source also gives, for `0 < XR`,

```text
canonicalKernel(F, XR, eta, X)
  = XR^(-1) * F.canonicalKernel(eta, X / XR).
```

Hence `XR * canonicalKernel(F, XR, eta, X)` is a corresponding-coordinate
dilation quantity without division by the history variables `M` or `H`.
This is not an axis-regularity result: `canonicalKernel` is itself defined as
`E^2 / X`, and the source's scaling proof explicitly treats `X = 0` separately
([canonicalKernel_scaling, 97--102](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/OutgoingDilation.lean#L97-L102)).

Valid P2 outcomes are a documented obstruction, a precisely restricted
surviving region, or an explicitly open condition. Neither a software PASS nor
a finite numerical sample is a substitute for that mathematical decision.
