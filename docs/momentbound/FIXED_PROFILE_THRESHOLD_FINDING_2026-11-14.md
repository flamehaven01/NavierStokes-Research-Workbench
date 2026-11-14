# The source amplitude sufficient condition fails at the fixed tuple

14 November 2026. Analytic derivation from the clean local upstream checkout
at `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

The existing `amplitude_spec` route requires `combinedScale d K ≤ 1/1000`.
For `P=m=1`, every positive `K` and every source `0 < lambda < 1/10`,
the actual constants in the pinned definitions imply

```text
prefixBoundConstant 1 1 > 30 * exp(120) > 30 * 2^120
combinedConstant 1 1 K > prefixBoundConstant 1 1
logarithmicRate(lambda) = lambda * (1 + log(1/lambda)) > lambda
combinedScale d K > 30 * 2^120 * lambda
```

The first line uses the positive addition to 120 in the exponent, the
positive terms added to 30 in the other factor, and `exp(1) > 2`. The
second uses the positivity of the other terms in `errorConstant` and
`K > 0`. The third follows from `lambda < 1`. These inequalities use
the source's chosen constants only through their positivity.
[Prefix bound and error constant](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/PulseAmplitude.lean#L828)
· [Combined scale](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/CorrectedPulseAmplitude.lean#L136)

Consequently the source sufficient condition requires
`lambda < 1/(30000*2^120)`, approximately `2.508e-41`. At the fixed
`lambda = 10^-12`, the strict lower bound on `combinedScale` already
exceeds `1/1000`. This obstruction concerns the particular sufficient
condition used by the upstream proof. Fixed-tuple Profile existence and
the actual amplitude inequality remain open.
[Amplitude hypothesis and construction](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/CorrectedPulseAmplitude.lean#L406)

The reset route has a separate quantitative dependency. The upstream
uniform branch builds `epsilon = 1/(16*beta^2*K_quad)` and
`L = 2*beta*(1+D)` from compactness bounds on the inverse operator and the
quadratic term, and a first-jet bound `D`. The scheduled reset then uses
`C = 3*exp(3)`, threshold `min(1/15, epsilon/C, 1/(4*L*C))` and
witness constant `K = L*C`. A fixed-tuple reset can instead target the
operator and jet bounds at the fixed lambda, using the actual
`C*lambda^28` bound for debt and its eta derivative.
[Uniform reset branch](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/UniformAngularReset.lean#L364)
· [Scheduled reset](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/UniformAngularReset.lean#L937)

For amplitude, a more direct source route is to bound the three actual
quadratic coefficients, including the energy shift for that reset, at
`eta = 2^-20`. The positive root formula can then be checked against
`9/10` using those bounds. The exact rational comparison at the selected
lambda was evaluated locally. The analytic implication has yet to be
compiled as a Lean declaration.
[Source root formula](https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/CorrectedPulseAmplitude.lean#L74)
