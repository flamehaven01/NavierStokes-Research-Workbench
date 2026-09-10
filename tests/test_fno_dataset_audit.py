from __future__ import annotations

import numpy as np
import pytest

from nsrw.external_experiments.fno_dataset_audit import (
    ExternalSource,
    audit_vorticity_trajectory,
    reconstruct_velocity,
)


def source(**overrides: object) -> ExternalSource:
    values: dict[str, object] = {
        "asset_id": "abelsr1710/navier-stokes-2d-fno",
        "source_url": "https://huggingface.co/datasets/abelsr1710/navier-stokes-2d-fno",
        "repository_id": "abelsr1710/navier-stokes-2d-fno",
        "revision": "deadbeef",
        "file": "train/sample-000.npz",
        "forcing_scope": "unforced",
        "domain_lengths": (2.0 * np.pi, 2.0 * np.pi),
        "source_file_sha256": "a" * 64,
    }
    values.update(overrides)
    return ExternalSource(**values)


def periodic_mode() -> np.ndarray:
    grid = np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False)
    x, y = np.meshgrid(grid, grid)
    return np.stack([np.sin(x) + np.cos(2.0 * y), 0.5 * np.sin(x - y)])[:, None, :, :].reshape(2, 8, 8)


def test_reconstruction_and_audit_pass_for_zero_mean_periodic_modes() -> None:
    receipt = audit_vorticity_trajectory(periodic_mode(), source=source(), sample_id="t0-t1")
    assert receipt["experiment_status"] == "PASS"
    assert receipt["claim_status"] == "UNVERIFIED"
    assert all(receipt["checks"].values())


def test_mean_mode_is_reported_as_a_failing_physical_check() -> None:
    omega = np.ones((1, 8, 8))
    receipt = audit_vorticity_trajectory(omega, source=source(), sample_id="mean-mode")
    assert receipt["experiment_status"] == "FAIL"
    assert receipt["checks"]["zero_mean_vorticity"] is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"revision": ""},
        {"forcing_scope": "unknown"},
        {"dimension": "3D"},
        {"domain_lengths": None},
        {"domain_lengths": (0.0, 1.0)},
        {"source_file_sha256": "not-a-hash"},
    ],
)
def test_source_contract_fails_closed(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        source(**kwargs)


@pytest.mark.parametrize(
    "value",
    [np.zeros((8, 8)), np.zeros((1, 1, 8)), np.full((1, 8, 8), np.nan)],
)
def test_trajectory_shape_and_finiteness_are_strict(value: np.ndarray) -> None:
    with pytest.raises(ValueError):
        reconstruct_velocity(value)


def test_reconstruction_rejects_bad_domain_and_audit_arguments() -> None:
    with pytest.raises(ValueError):
        reconstruct_velocity(np.zeros((1, 8, 8)), (0.0, 1.0))
    with pytest.raises(ValueError):
        audit_vorticity_trajectory(periodic_mode(), source=source(), sample_id="", tolerance=1.0)
    with pytest.raises(ValueError):
        audit_vorticity_trajectory(periodic_mode(), source=source(), sample_id="x", tolerance=0.0)
