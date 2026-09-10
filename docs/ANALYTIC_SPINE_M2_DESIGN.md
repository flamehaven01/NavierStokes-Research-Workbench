# Analytic Spine M2 Design

## Objective

M2 turns the source paper's concentrating leading-field interface into executable,
falsification-oriented obligations. It does not reproduce the profiles constructed later in the
paper and does not certify their existence.

## Directly inspected source scope

The implemented formulas were visually checked in the primary PDF:

- page 7: `A=1/2+h`, `D=1/2-h`, `0<h<1/100`, equation (3.2),
  `u_theta=q^-A E`, `u_z=q^-A U`, `r u_r=V0`, `p=q^-2A Pi`, and cylindrical
  incompressibility;
- page 8: radial pressure balance, axis regularity requirements, core bounds, radial and axial
  length scales, velocity growth rates, Reynolds powers, and the `q^(2h)` axial-diffusion
  suppression factor;
- page 9: the inner/annulus/exterior stress-support geometry and its strict radial ordering.

The Markdown file remains a locator transport. No missing display equation was reconstructed
from model memory.

## Exact algebra layer

`AffineHExponent` represents every power as `constant + coefficient*h` with exact rational
coefficients. `ConcentrationParameters` accepts only `Fraction` and enforces
`0 < h < 1/100`. The ledger includes:

| Quantity | Derived power of `q` |
|---|---:|
| radial length | `1/2` |
| axial length | `1/2-h` |
| aspect ratio | `-h` |
| azimuthal and axial velocity | `-1/2-h` |
| radial velocity | `-1/2` |
| radial/tangential velocity ratio | `h` |
| pressure | `-1-2h` |
| azimuthal Reynolds number | `-h` |
| transport and radial diffusion rates | `-1` |
| axial/radial diffusion ratio | `2h` |

Background correction order `n` is generated as `2nh`, rather than stored as a list.

## Profile interface

`LeadingProfiles` accepts four functions of `(X, eta)`: `E`, `U`, `V0`, and `Pi`. The field
evaluator applies the source formulas and converts cylindrical velocity to Cartesian velocity.
It fails if a nonzero radial flux is requested on the axis.

M2 includes `toy-pure-swirl-v1` solely as a positive control:

```text
E(X,eta) = sqrt(2X) exp(-X)
U(X,eta) = 0
V0(X,eta) = 0
Pi(X,eta) = -(1/2) exp(-2X)
```

This fixture has exact cylindrical incompressibility and radial pressure balance, but it is not
the paper's constructed profile and does not satisfy or claim the full blowup construction.

## Obligations and falsifiers

The receipt checks:

1. exact parameter domain and exponent ledger;
2. a wrong axial-diffusion exponent mutation;
3. core membership and inner/annulus/exterior classification;
4. sampled cylindrical incompressibility;
5. sampled radial pressure balance;
6. fixed-`X`, `eta=0` velocity growth at two `tau` values;
7. finite sampled `O(q^N)` bookkeeping with derivative metadata;
8. an intentionally overclaimed residual power that must fail.

Wrong pressure and non-divergence-free axial-profile mutations are covered by tests. Every
local or asymptotic sample retains numerical-diagnostic authority.

## Stop boundary and M3 entry condition

M2 may be called GREEN only for the local interface and obligation harness. The global claim
remains `UNVERIFIED`, and the receipt must say `source_paper_profiles=NOT_INSTANTIATED`.

M3 should begin only after selecting one exact source profile/lemma package whose complete
hypotheses can be recovered from the PDF. A useful candidate is the near-axis analytic profile
package leading to Theorem 4.6. M3 must represent axis regularity, the radial integral defining
pressure, the induced `V0`, and at least one support or moment condition. If any defining formula
is missing from the transport, implementation pauses until the PDF is visually checked.
