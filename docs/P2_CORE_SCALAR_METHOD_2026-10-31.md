# Exact rational core-scalar enclosures

Date: 2026-10-31. Scope: one fixed P2 scalar experiment, not a Profile evaluator.
The [input contract](NSRW_P2_FIRST_INPUT_AND_ERROR_CONTRACT_2026-10-28.md)
retains lambda=10^-12, eta=2^-20 and all unresolved source assumptions.

## Method and error bound

For rational 0<=y<=1/2, let a_k=y^k/k! and S_N=sum(k=0..N) a_k.
All terms are nonnegative and the ratio after a_(N+1) is at most y/(N+2).
Consequently

\[
S_N\le e^y\le S_N+\frac{y^{N+1}}{(N+1)!}\frac1{1-y/(N+2)}.
\]

This geometric-tail bound contains no unevaluated exp(y) on its right side.
The positive expm1 calculation uses the sum starting at k=1; it does not subtract
one from two nearly equal rounded values. Range reduction reduces |x|<=16 to
y<=1/2, followed by exact interval squaring. Negative arguments use reciprocals
of positive intervals. Every dyadic floor/ceiling is computed using integers.
Products use lower*lower and upper*upper only after nonnegativity is checked.

Precision values 128/256/512 denote **fractional bits**. Rational numerators and
denominators are not limited to 128-bit machine integers. Exponent range reduction
uses 64 guard fractional bits. The final interval endpoints lie on the declared
dyadic grid. The implementation is the small module
[`p2_core_scalars.py`](../src/nsrw/math_kernel/p2_core_scalars.py), not a general
interval arithmetic library or a Lean-verified numerical kernel.

## What is evaluated

- ell=exp(-23/20), v=exp(-17/20) and w=(v-ell)/4;
- G=exp(-13+23*lambda/20)*expm1(17*lambda/10);
- D=exp(1-4*lambda)*expm1(2*lambda), the positive main-only separation denominator;
- the exact exponent L*beta0=6499999999987 and the lower-bound expression
  `exp(L*beta0)*lower(w)` for I01.

The last item is not an upper enclosure for I01, a computed logarithm or an
evaluated huge exponential. It uses the admitted plateau inequality. No
coefficient, q, J, mass zero or source Profile is evaluated by this module.

The D identity follows from exact rational exponent relations and
exp(a)-exp(b)=exp(b)*(exp(a-b)-1). It is not part of the ten admitted P1
propositions. Once valid positive numerator and denominator intervals are
available, lower(N/D) uses lower(N)/upper(D). The current helper checks that
arithmetic direction but does not construct the missing source numerator bound.

## Recompute and reject

From a checkout with Python >=3.10, in a POSIX shell:

```sh
PYTHONPATH=src python -m nsrw.math_kernel.p2_core_scalars produce --precision 128 --output core.json
PYTHONPATH=src python -m nsrw.math_kernel.p2_core_scalars verify --input core.json
```

In PowerShell set `$env:PYTHONPATH='src'` before the same `python -m` commands.
No Lean installation or external numeric package is required for this scalar
calculation. The fixed output retains every unresolved assumption and has the
scope `CORE_SCALAR_ENCLOSURES_ONLY`. Verification recomputes all fields rather
than checking a digest. It shares the producer's algorithm and trust domain.

Tests compare selected exp/expm1 bounds with a tighter, direct positive series
using a separately bounded remainder, and exercise inverse/zero-crossing
intervals, changed inputs, missing assumptions, scope promotion, duplicate JSON
keys and a lower bound increased by one declared dyadic quantum. An arbitrary
exact rational has no unique floating-point ULP; this test uses 2^-128 explicitly.
The original mathematical result is not enlarged by these software tests.

## Remaining research

Validated moment quadrature, determinant/affine coefficient enclosures, positive
q, actual reset/K/combinedScale admissibility, source nonemptiness and a compiled
named quantitative Profile.J wrapper remain separate. Numerical backend progress
for these core factors does not discharge the selected-constant dependency in
the source amplitude hypotheses. No independent reproduction is asserted.
