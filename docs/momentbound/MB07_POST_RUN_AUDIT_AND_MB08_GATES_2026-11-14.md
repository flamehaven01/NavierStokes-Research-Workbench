# MB-07 evidence review and MB-08 fixed-reset gate

Review date: 2026-11-14 (Asia/Bangkok).
Status: `PASS[LOCAL_EVIDENCE_AND_SCOPE_REVIEW] / NEXT_GATE_DESIGNED`.
**Not** a new theorem, independent reproduction, scientific application or formal admission.

## 1. Source sufficient-condition obstruction

Pinned upstream source: `openai/NavierStokesAndEuler` commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

For source `P=m=1`, any `K>0`, and admissible
`0<lambda<1/10`, the source definitions imply

```text
prefixBoundConstant 1 1 > 30*exp(120) > 30*2^120
combinedConstant 1 1 K > prefixBoundConstant 1 1
logarithmicRate(lambda) = lambda*(1+log(1/lambda)) > lambda
combinedScale d K > 30*2^120*lambda
```

The exact source locations are
`NavierStokes/PulseAmplitude.lean`:
`prefixBoundConstant` (line 828), `errorConstant` (line 1097),
`logarithmicRate` (line 774), and
`NavierStokes/CorrectedPulseAmplitude.lean`:
`combinedConstant`/`combinedScale` (lines 136–138).

The source sufficiency condition `combinedScale d K <= 1/1000` is
therefore **impossible** at `lambda=10^-12` for every positive K.
It necessarily requires
`lambda < 1/(30000*2^120) ≈ 2.508e-41`.
This derived upper bound is **necessary, not sufficient**:
there is an additional `lambda*log(1/lambda)` factor, so the
actual threshold for this source condition may be smaller.

This is an obstruction to **one source proof's sufficient-condition
route**, *not* nonexistence of a `Profile`, falsity of its PDE
construction, or failure of the actual amplitude inequality.

Evidence currently:
`docs/momentbound/FIXED_PROFILE_THRESHOLD_FINDING_2026-11-14.md`,
SHA-256 `5150fe9e13773f86cf69fb57b3642d4c157ca81af4162f6e0c14b119e2b3997b`.
Source and exact-rational reasoning were reviewed locally; a **new
Lean proposition has not been compiled**.

## 2. MB-07 internal benchmark evidence

Results: `outputs/mb07-result-20261114.json`,
SHA-256 `cda6ce8abafd8f9db82a118de8e16f4b84b8997f452b2e90577a8c9376790ad0`
(64,200 bytes).
Manifest: `outputs/mb07-manifest-20261114.json`,
SHA-256 `ede5d96f791eb577b19874af2881d8d2b149cc890504be13ecb9e210e265ee44`.
Runner: `scripts/run-mb07-diagnostic.py`,
SHA-256 `b024505ac1ffa8d62710f616ea67b3b2e8039e3b6f0ab5dbeb313cfec0b54cda`.
Frozen contract SHA-256:
`487fcf9813727f2f640afa6162e7b36343eac6183dabe2543731edd119526c6b`.

The manifest names this runner, its existing scalar enclosure backend,
the pinned MB-06 execution commit `40e0cfe7c2defeeeee871f1923552c352f28ee5c`,
CPython 3.14.10, mpmath 1.3.0, Windows 11, 3 warmups,
20 trials, 120 seconds per input and the fixed calibration/held-out
instances.

The **held-out** set is exactly eight lambda inputs with two
threshold decisions each (16 comparisons):

| Method | Resolved | Contradictions | Unresolved |
| --- | ---: | ---: | ---: |
| Direct float64 `exp(x)-1` | 6 uncertified estimates | 1 | 10 |
| Stable float64 `expm1(x)` | 4 uncertified estimates | 0 | 12 |
| Coarse analytic rational bounds | 0 certified | 0 | 16 |
| Fraction positive-series enclosures | 12 certified | 0 | 4 |

In the *separate calibration group* there were 8 direct-float estimates
and **2** disagreements; they must not be mixed into the held-out
numerator. The held-out denominator-zero event count for direct float64
is **5 inputs**; stable expm1 had none. Fraction abstained at `2^-400`
after a too-wide 512-bit interval and at `2^-520` because all allowed
precisions yielded a zero *lower enclosure* for the denominator, **not**
because the real denominator vanishes.

The result report records the median of held-out **per-input medians**
as Fraction 268.43 µs versus analytic 22.23 µs, not a hardware-
independent operation-cost ratio or end-to-end process time. Peak
`tracemalloc` allocation is not process RSS. All interval
containment checks and seven rejection controls passed in the
record, but this review has not reexecuted the whole benchmark.

Scope: **demonstrated a local bounded-input decision benefit over the
preselected coarse analytic baseline**, at higher cost. It does not
establish benefit over a tighter analytic series bound, a mature
validated library, or an actual PDE/CFD workflow. TR-0–TR-3 remain
unearned; there is no application claim.

## 3. Next gate A — formalize the source obstruction

Create a *new* Lean file, not a modification of upstream or admitted
MB-05/06, with exact source types and proof of:

```text
for c : Parameters, P=m=1, and K>0:
combinedScale d K > 30 * 2^120 * c.lam
at c.lam = 1/10^12: 1/1000 < combinedScale d K
```

Prerequisites: `d : TailData`, `d.core.P=1`,
`d.core.m=1`, `K>0`, fixed lambda only in the
second theorem. Use the original `prefixBoundConstant` and
`errorConstant` definitions and a rigorous `exp(1)>2` fact;
do not insert numerical values as unproved axioms. Document the
exact dependency, Lean toolchain, source pin, hashes and axiom
output. A proof of this obstruction is not a proof that no `Profile`
exists.

No development file or compilation has been created for this gate.

## 4. Next gate B — quantitative fixed-lambda reset

Do **not** assume that solving two pressure/angular equations at one
eta constructs the upstream `ResetWitness`. The source witness
(`NavierStokes/UniformAngularReset.lean`, lines 922–933)
requires a smooth **function `eta ↦ coefficients eta`**, both
moment identities for **all eta**, uniform norm and derivative
bounds, and `small_jets`.

At `lambda=10^-12`, derive explicit source-justified upper bounds
for the norm of the inverse of `linearCLM lambda` (beta), the norm
of `quadraticCLM lambda` (K_quad), and the first-jet map (D).
The existing uniform proof uses existential beta/K_quad/D from
compactness; these are **not numerical constants**.

For a fixed-lambda effective branch, check with justified bounds:

```text
C = 3*exp(3)
radius r = 1/(4*beta*K_quad)
epsilon = r/(4*beta)
L = 2*beta*(1+D)
C*lambda^28 < epsilon
L*C*lambda^28 <= lambda/4
```

and match the original normalized debt/eta-derivative bound. Only
then attempt a source-typed `ResetWitness d (L*C)` (or a new
valid fixed-lambda witness with correctly proved bounds) and retain
its exact functional dependence on eta.

Do not infer a positive K or `combinedScale<=1/1000` from the
fixed-lambda reset's existence; the latter is already obstructed.

## 5. Next gate C — same-reset quadratic amplitude sign

From the *same source reset* `w : ResetWitness d K`, at
`eta=1/1048576`, enclose:

```text
a = PulseAmplitude.quadraticCoefficient d.core > 0
b = PulseAmplitude.linearTerm d.core eta
c = CorrectedPulseAmplitude.constantTerm d w.coefficients eta
  = PulseAmplitude.constantTerm d eta - energyShift d w.coefficients eta
Q(A) = a*A^2 + b*A + c
```

A potentially simpler **proposed** certification of the positive
root's lower bound than evaluating a square root is:

```text
c <= -1/5                   (clamp is inactive)
Q(9/10) < 0                 (certified strict sign)
a > 0                       (source theorem)
=> 9/10 < amplitude d w.coefficients eta
```

The implication must be proven in Lean from
`amplitude_pos`, `amplitude_energy_equation` and the
quadratic identities, **without** assuming that a pointwise
synthetic coefficient pair is the actual reset. The actual
`c<=-1/5` and `Q(9/10)<0` source bounds are currently open;
these are gates, not achieved results.

A pointwise numerical solution may be an informative diagnostic
only. It does not itself construct a smooth all-eta witness or a
`Profile F`.

## 6. Separate follow-up: exact local zero and numerical J

For an actual fixed source `Profile F` with
`F.amp(2^-20)>9/10`, MB-05 supplies actual `c1>0`.
The earlier admitted Z03 theorem then yields **existential**
first-window `localMass=0` (since `eta=2^-20>0`);
MB-06 provides a lower bound at that unspecified same r.

A numeric root enclosure and a numeric `Profile.J` certificate
require new evaluation/custody, coordinate normalization and the
actual prefactor. They are not supplied by this plan or MB-07.

## 7. Provenance and stop rules

- Preserve MB-05/06 proof bytes, admission receipts, ledger and
  historical execution metadata without edits.
- Fixed input `lambda=10^-12` must not be silently retuned to
  `10^-41`; a different lambda is a separate experiment.
- If explicit inverse/jet constants cannot be bounded within the
  declared development budget, record
  `HELD[FIXED_RESET_NUMERICAL_CONSTANTS_UNAVAILABLE]`,
  rather than inventing beta/K_quad/D.
- A formalized failure of the coarse sufficiency criterion does
  not falsify the original theorem.
- MB-07's internal empirical result is **not** an OE-3/4
  mathematical replay or a TR application benefit.

This document is a bounded review/next-work plan, not new
proof/execution evidence. No Git commit, push, private Drive
archive or claim promotion is authorized by this document.
