"""Mathematical diagnostics for three-dimensional incompressible Navier--Stokes."""

from nsrw.math_kernel.operators import (
    ResidualSample,
    curl,
    divergence,
    navier_stokes_residual,
    sample_residual,
)
from nsrw.math_kernel.profile_closure import (
    ClosedLeadingProfiles,
    ClosureSample,
    QuadratureSpec,
    audit_lean_crosswalk,
    canonical_pressure,
    derived_radial_flux,
    radial_average,
)
from nsrw.math_kernel.scaling import (
    periodic_scaling_certificate,
    viscosity_scaling_certificate,
)

__all__ = [
    "ResidualSample",
    "curl",
    "divergence",
    "navier_stokes_residual",
    "periodic_scaling_certificate",
    "sample_residual",
    "viscosity_scaling_certificate",
    "ClosedLeadingProfiles",
    "ClosureSample",
    "QuadratureSpec",
    "audit_lean_crosswalk",
    "canonical_pressure",
    "derived_radial_flux",
    "radial_average",
]
