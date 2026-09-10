"""E2: bounded physical audit for a periodic 2-D vorticity trajectory.

The module deliberately accepts an already materialized array.  Downloading a
Hugging Face repository is an acquisition concern and must happen in the
project-owned Colab notebook after its revision, file, and sample are pinned.
The numerical surface here is independent of any learned model.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Any


@dataclass(frozen=True)
class ExternalSource:
    """Minimum provenance needed before an external array is admitted."""

    asset_id: str
    source_url: str
    repository_id: str
    revision: str
    file: str
    forcing_scope: str
    dimension: str = "2D"
    representation: str = "vorticity"
    domain: str = "periodic"
    domain_lengths: tuple[float, float] | None = None
    source_file_sha256: str | None = None

    def __post_init__(self) -> None:
        required = (self.asset_id, self.source_url, self.repository_id, self.revision, self.file)
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("source identity, URL, revision, and file are required")
        if self.source_file_sha256 is None or re.fullmatch(r"[0-9a-fA-F]{64}", self.source_file_sha256) is None:
            raise ValueError("source_file_sha256 must be a 64-character SHA-256 digest")
        if self.forcing_scope not in {"forced", "unforced"}:
            raise ValueError("forcing_scope must be explicitly forced or unforced")
        if self.dimension != "2D" or self.representation != "vorticity" or self.domain != "periodic":
            raise ValueError("E2 only admits 2D periodic vorticity inputs")
        if self.domain_lengths is None or len(self.domain_lengths) != 2 or any(
            not isfinite(length) or length <= 0 for length in self.domain_lengths
        ):
            raise ValueError("domain lengths must be two finite positive values")


def _numpy() -> Any:
    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - exercised in dependency-light Colab setup
        raise RuntimeError("E2 requires numpy; install the notebook's pinned dependencies") from exc
    return np


def _as_trajectory(omega: Any) -> Any:
    np = _numpy()
    values = np.asarray(omega, dtype=float)
    if values.ndim != 3:
        raise ValueError("vorticity trajectory must have shape (time, height, width)")
    if values.shape[1] <= 1 or values.shape[2] <= 1 or not np.isfinite(values).all():
        raise ValueError("trajectory must be finite and have non-trivial grid axes")
    return values


def reconstruct_velocity(omega: Any, domain_lengths: tuple[float, float] = (2.0 * 3.141592653589793,) * 2) -> tuple[Any, Any]:
    """Solve ``-Delta psi = omega`` and return ``u=psi_y, v=-psi_x``.

    The zero Fourier mode is set to zero because a periodic velocity field has
    zero-mean vorticity.  The caller must audit that discarded mode separately.
    """

    np = _numpy()
    values = _as_trajectory(omega)
    if len(domain_lengths) != 2 or any(length <= 0 for length in domain_lengths):
        raise ValueError("domain lengths must be positive")
    _, height, width = values.shape
    ky = 2.0 * np.pi * np.fft.fftfreq(height, d=domain_lengths[0] / height)
    kx = 2.0 * np.pi * np.fft.fftfreq(width, d=domain_lengths[1] / width)
    kx_grid, ky_grid = np.meshgrid(kx, ky)
    denominator = kx_grid * kx_grid + ky_grid * ky_grid
    omega_hat = np.fft.fft2(values, axes=(-2, -1))
    stream_hat = np.zeros_like(omega_hat, dtype=complex)
    nonzero = denominator > 0
    stream_hat[:, nonzero] = omega_hat[:, nonzero] / denominator[nonzero]
    u = np.fft.ifft2(1j * ky_grid * stream_hat, axes=(-2, -1)).real
    v = np.fft.ifft2(-1j * kx_grid * stream_hat, axes=(-2, -1)).real
    return u, v


def audit_vorticity_trajectory(
    omega: Any,
    *,
    source: ExternalSource,
    sample_id: str,
    tolerance: float = 1e-10,
) -> dict[str, object]:
    """Produce a scoped E2 receipt for one pinned trajectory."""

    np = _numpy()
    if not isinstance(sample_id, str) or not sample_id.strip():
        raise ValueError("sample_id is required")
    if not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    values = _as_trajectory(omega)
    u, v = reconstruct_velocity(values, source.domain_lengths)
    height, width = values.shape[1:]
    ky = 2.0 * np.pi * np.fft.fftfreq(height, d=source.domain_lengths[0] / height)
    kx = 2.0 * np.pi * np.fft.fftfreq(width, d=source.domain_lengths[1] / width)
    kx_grid, ky_grid = np.meshgrid(kx, ky)
    u_hat = np.fft.fft2(u, axes=(-2, -1))
    v_hat = np.fft.fft2(v, axes=(-2, -1))
    divergence = np.fft.ifft2(1j * kx_grid * u_hat + 1j * ky_grid * v_hat, axes=(-2, -1)).real
    reconstructed = np.fft.ifft2(
        1j * kx_grid * v_hat - 1j * ky_grid * u_hat, axes=(-2, -1)
    ).real
    mean_vorticity = np.mean(values, axis=(-2, -1))
    divergence_error = float(np.max(np.abs(divergence)))
    vorticity_error = float(np.max(np.abs(reconstructed - values)))
    mean_error = float(np.max(np.abs(mean_vorticity)))
    checks = {
        "finite_input": bool(np.isfinite(values).all()),
        "zero_mean_vorticity": mean_error <= tolerance,
        "spectral_divergence": divergence_error <= tolerance,
        "vorticity_reconstruction": vorticity_error <= tolerance,
    }
    metrics = {
        "trajectory_shape": list(values.shape),
        "max_abs_divergence": divergence_error,
        "max_abs_vorticity_error": vorticity_error,
        "max_abs_mean_vorticity": mean_error,
        "energy_by_step": (0.5 * np.mean(u * u + v * v, axis=(-2, -1))).tolist(),
        "enstrophy_by_step": (0.5 * np.mean(values * values, axis=(-2, -1))).tolist(),
    }
    return {
        "schema": "nsrw.external-experiment.v1",
        "experiment_id": "E2_HF_FNO_DATASET_AUDIT",
        "sample_id": sample_id,
        "source": asdict(source),
        "parameters": {"tolerance": tolerance, "scheme": "periodic_fft_poisson"},
        "checks": checks,
        "metrics": metrics,
        "experiment_status": "PASS" if all(checks.values()) else "FAIL",
        "claim_status": "UNVERIFIED",
        "evidence_class": "EXTERNAL_REPRODUCIBLE_NUMERICAL_EXPERIMENT",
        "non_claims": [
            "This is a 2D sampled numerical diagnostic, not a 3D Navier-Stokes proof.",
            "No learned model, long-rollout, or uniform analytic estimate is established.",
            "The source file hash is recorded when supplied but is not inferred by this module.",
        ],
    }
