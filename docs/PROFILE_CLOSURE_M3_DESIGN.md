# M3 — Profile closure and missing-link audit

M3 consumes the M1 scaling ledger and M2 `LeadingProfiles` interface. Its
purpose is to make the paper's dependent profile relations executable while
preserving the boundary between a diagnostic and a theorem.

## Source obligations

The primary PDF (`navier-stokes.pdf`) gives the relevant relations on printed
pages 25–26 and 33:

* (4.6) defines the radial average `A_X(f)`, including the axis extension;
* (4.7) derives `V0` from `U` and `A_X(U)`, and requires
  `Pi_X = E^2/(2X)`;
* (4.25) fixes pressure by integrating to radial infinity.

The implementation therefore derives `radial_flux` from `axial` and derives
`pressure` from `azimuthal` plus an explicit finite-cutoff tail contract. An
infinite tail is never silently replaced by a finite truncation. The `h`
parameter is held as an exact `Fraction` and is validated by the same
`0 < h < 1/100` contract used by M1/M2.

## Organic stage contract

M1 supplies the exponent/scaling identities. M2 supplies the cylindrical
field evaluator and local sampled obligations. M3 consumes those objects and
produces a closed profile bundle, pressure-balance samples, and a
paper–Lean crosswalk. M4 can consume the closed bundle for stress support,
cone, and moment obligations. A failed M3 relation blocks M4; a passing sample
does not promote the global claim beyond `UNVERIFIED`.

## Lean relationship

Static inspection at pinned revision
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` finds the expected declarations:
`ProfileHistories.average`, `SlowDivergence.radialFlux`,
`ProfileHistories.radialPartial_pressure`, `NominalProfile.pressure_canonical`,
and `ActualCandidateAssembly.selected_candidate`. The local Lean toolchain is
not available, so this is source-location evidence, not a build or semantic
equivalence result.

The first suspected gap—absence of the `V0` relation—is therefore falsified.
The meaningful remaining audit is whether the final selected candidate really
discharges all six quantitative parts of Theorem 4.6 and whether those parts
match the original global problem quantifiers.

The numerical closure itself is now hardened at the two previously identified
boundaries: `X=0` requires an explicit integrand limit, and `eta=±1` uses a
one-sided derivative stencil. These are executable policies, not claims that
the source theorem's endpoint estimates have been proved.

## Non-claims

The manufactured exponential swirl and constant axial profile are diagnostic
fixtures. M3 proves no existence, smoothness, contraction, cone margin, global
solution failure, or millennium-problem result.
