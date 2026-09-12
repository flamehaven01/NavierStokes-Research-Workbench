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

P2-D   CONE / MOMENT USEFULNESS
       OPEN

P2-E   CANONICAL-KERNEL COMPARATOR
       OPEN
```

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

The primary open question is the geometry of the zero set between these two
facts:

```text
- Is the endpoint the first zero of M?
- Can M cross zero earlier and return?
- Is sign(M) preserved on [pulseStart, endpoint)?
- Is |M| bounded away from zero on a useful subinterval?
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

The inspected source gives exact endpoint cancellation, but it has not yet
supplied a partial-pulse integral monotonicity or sign lemma sufficient to
settle this interior zero-set question. Endpoint cancellation alone cannot
exclude an earlier zero followed by a return. P2-C is therefore the first new
analysis question in this lane, rather than a closure claim.

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
