# Navier--Stokes Mathematical Kernel Design

## Decision

The workbench now treats the mathematical problem as the primary research surface. Lean is an
optional formal-evidence backend, while the existing contract and proof graph remain the L0
research-integrity layer. This stage does not attempt to reproduce the paper's 167-page
construction.

## Source-bound formulas

Only formulas inspected in the primary PDF are implemented:

- the forced residual
  `u_t + (u·grad)u - nu Delta u + grad p - f`;
- equation (3.2), including `q - z^2 q^(2h) = tau`,
  `eta = z/q^(1/2-h)`, and `X = r^2/(2q)` with `0 < h < 1/100`;
- viscosity rescaling (10.22):
  `u_nu(x,t)=sqrt(nu)u(x/sqrt(nu),t)`,
  `p_nu(x,t)=nu p(x/sqrt(nu),t)`, and
  `f_nu(x,t)=sqrt(nu)f(x/sqrt(nu),t)`;
- energy and viscous-dissipation exponent `5/2` in (10.23);
- the page-125 parabolic scaling with velocity, pressure, force, space, and time powers
  `1, 2, 3, 1, 2`.

The Markdown transport is useful for line lookup but does not authorize formula recovery. A
missing or damaged equation must remain unknown until it is checked in the PDF.

## Architecture and authority

| Layer | Artifact | What it establishes | What it cannot establish |
|---|---|---|---|
| L0 | contract, graph, falsifiers | identity, scope, locators, evidence flow | mathematical truth |
| L1 | `ScalingLaw` | exact rational exponent consequences of declared scaling powers | analytic estimates or existence |
| L1 | similarity reconstruction | numerical solution of the explicit coordinate equation | properties outside sampled inputs |
| L2 | finite-difference operators | local residual, divergence, curl, and Laplacian diagnostics | global PDE equality |
| L2 | manufactured solutions | positive controls and mutation sensitivity | the paper's blowup construction |
| L3 | Lean source | formal declarations when built and audited | paper equivalence by name alone |

The math receipt therefore keeps `claim_status=UNVERIFIED` even if every bounded check passes.

## Exact exponent engine

For a scaling parameter `s`, declare

```text
u_s(x,t) = s^a u(s^b x, s^c t)
p_s(x,t) = s^d p(s^b x, s^c t)
f_s(x,t) = s^e f(s^b x, s^c t).
```

The kernel derives the momentum exponents rather than storing their expected common value:

```text
time derivative     a + c
convection           2a + b
viscous Laplacian    k + a + 2b
pressure gradient    d + b
force                e
```

Here `k` is the exponent of the viscosity coefficient. It also derives divergence, vorticity,
energy-squared, time-integrated BKM, and time-integrated dissipation exponents. All arithmetic
uses `fractions.Fraction`. A wrong force exponent is a required killed mutation.

## Numerical kernel

The spatial and time operators use centered finite differences with explicit positive steps.
The receipt records samples from two controls:

- unforced decaying shear `u=(exp(-nu t) sin y,0,0)`;
- forced linear shear `u=(t y,0,0)`, `f=(y,0,0)`.

The wrong-force version of the second fixture must produce a nonzero residual. A compressible
linear field must produce nonzero divergence. These are falsification controls, not evidence of
the source paper's construction.

## Green gate

A local math-kernel stage is GREEN only when:

1. exact momentum exponents agree for both source-bound scaling laws;
2. the force-exponent mutation breaks covariance;
3. manufactured-solution residuals and divergence remain within the recorded tolerance;
4. wrong forcing and compressible fields are detected;
5. similarity coordinates reconstruct the defining equation;
6. focused tests, full pytest coverage gate, Ruff, compile checks, deterministic receipt replay,
   and a nonzero-coverage slop scan pass.

None of these checks promotes the Clay claim. Progress toward that goal requires implementing
and falsifying specific analytic lemmas from the construction, with their hypotheses and norms
represented explicitly rather than inferred from prose or theorem names.
