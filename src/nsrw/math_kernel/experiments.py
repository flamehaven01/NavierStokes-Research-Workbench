"""Deterministic mathematical-kernel self-checks and bounded receipts."""

from __future__ import annotations

from nsrw.math_kernel.manufactured import decaying_shear, forced_linear_shear
from nsrw.math_kernel.operators import sample_residual
from nsrw.math_kernel.scaling import (
    periodic_scaling_certificate,
    viscosity_scaling_certificate,
)
from nsrw.math_kernel.similarity import reconstruct_similarity_coordinates


def run_math_self_check(tolerance: float = 2e-6) -> dict[str, object]:
    """Run exact exponent checks plus local numerical manufactured-solution checks."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    samples = []
    shear = decaying_shear(0.7)
    samples.append(sample_residual(*shear, 0.7, (0.2, 0.7, -0.1), 0.4).as_dict())
    forced = forced_linear_shear()
    samples.append(sample_residual(*forced, 1.3, (-0.3, 0.8, 0.2), 0.6).as_dict())
    max_residual = max(float(sample["residual_infinity_norm"]) for sample in samples)
    max_divergence = max(abs(float(sample["divergence"])) for sample in samples)

    scaling = [viscosity_scaling_certificate(), periodic_scaling_certificate()]
    scaling_pass = all(certificate.momentum_terms_match for certificate in scaling)
    similarity = reconstruct_similarity_coordinates(0.2, 0.1, 0.4, 0.005)
    similarity_pass = abs(similarity.equation_residual) <= 1e-12 and abs(similarity.eta) < 1
    numerical_pass = max(max_residual, max_divergence) <= tolerance
    passed = scaling_pass and similarity_pass and numerical_pass
    return {
        "schema_id": "flamehaven.navier-stokes-math-kernel-receipt.v1",
        "check_status": "PASS" if passed else "FAIL",
        "claim_status": "UNVERIFIED",
        "authority": {
            "exact_scaling": "EXACT_EXPONENT_ALGEBRA",
            "manufactured_solutions": "NUMERICAL_DIAGNOSTIC",
            "similarity_coordinates": "NUMERICAL_RECONSTRUCTION",
            "global_navier_stokes_claim": "NOT_ESTABLISHED",
        },
        "checks": {
            "scaling_exponents": "PASS" if scaling_pass else "FAIL",
            "manufactured_residuals": "PASS" if numerical_pass else "FAIL",
            "similarity_reconstruction": "PASS" if similarity_pass else "FAIL",
        },
        "tolerance": tolerance,
        "max_residual_infinity_norm": max_residual,
        "max_divergence_absolute": max_divergence,
        "scaling_certificates": [certificate.as_dict() for certificate in scaling],
        "samples": samples,
        "similarity_sample": similarity.as_dict(),
    }
