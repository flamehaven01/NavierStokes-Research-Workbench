from __future__ import annotations

import math

import pytest

from nsrw.math_kernel.similarity import reconstruct_similarity_coordinates


def test_similarity_reconstructs_paper_coordinates() -> None:
    result = reconstruct_similarity_coordinates(0.2, 0.1, 0.4, 0.005)
    assert result.q - result.z**2 * result.q ** (2 * result.h) == pytest.approx(result.tau)
    assert result.z == pytest.approx(result.q ** (0.5 - result.h) * result.eta)
    assert result.capital_x == pytest.approx(result.radius**2 / (2 * result.q))
    assert abs(result.eta) < 1
    assert result.iterations <= 200
    assert result.as_dict()["tau"] == 0.2


def test_similarity_at_zero_z_has_q_equal_tau() -> None:
    result = reconstruct_similarity_coordinates(0.4, 0.0, 0.2, 0.005)
    assert result.q == pytest.approx(0.4, abs=1e-12)
    assert result.eta == 0.0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"tau": 0.0, "z": 0.1, "radius": 0.2, "h": 0.005},
        {"tau": math.inf, "z": 0.1, "radius": 0.2, "h": 0.005},
        {"tau": 0.2, "z": math.nan, "radius": 0.2, "h": 0.005},
        {"tau": 0.2, "z": 0.1, "radius": -0.2, "h": 0.005},
        {"tau": 0.2, "z": 0.1, "radius": 0.2, "h": 0.0},
        {"tau": 0.2, "z": 0.1, "radius": 0.2, "h": 0.01},
        {"tau": 0.2, "z": 0.1, "radius": 0.2, "h": 0.005, "tolerance": 0.0},
        {"tau": 0.2, "z": 0.1, "radius": 0.2, "h": 0.005, "max_iterations": 0},
    ],
)
def test_similarity_rejects_invalid_inputs(kwargs: dict[str, float | int]) -> None:
    with pytest.raises(ValueError):
        reconstruct_similarity_coordinates(**kwargs)  # type: ignore[arg-type]


def test_similarity_reports_nonconvergence() -> None:
    with pytest.raises(ArithmeticError, match="did not converge"):
        reconstruct_similarity_coordinates(0.2, 0.1, 0.4, 0.005, max_iterations=1)
