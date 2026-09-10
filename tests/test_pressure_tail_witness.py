from __future__ import annotations

import math

import pytest

from nsrw.math_kernel.pressure_tail_witness import source_power_tail_witness


def test_source_power_tail_witness_matches_closed_form() -> None:
    result = source_power_tail_witness(
        h=1.0 / 200.0,
        amplitude=1.25,
        radius=2.0,
        cutoff=2.0 * math.exp(14.0 / 5.0),
    )
    assert result.check_status == "PASS"
    assert result.numerical_integral == pytest.approx(result.expected_integral, abs=1e-10)
    assert result.numerical_pressure_tail == pytest.approx(result.expected_pressure_tail, abs=1e-10)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"h": 0.0, "amplitude": 1.0, "radius": 1.0, "cutoff": 20.0},
        {"h": 0.1, "amplitude": 0.0, "radius": 1.0, "cutoff": 20.0},
        {"h": 0.1, "amplitude": 1.0, "radius": 0.0, "cutoff": 20.0},
        {"h": 0.1, "amplitude": 1.0, "radius": 2.0, "cutoff": 10.0},
        {"h": 0.1, "amplitude": 1.0, "radius": 1.0, "cutoff": 20.0, "panels": 3},
    ],
)
def test_source_power_tail_witness_fails_closed(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        source_power_tail_witness(**kwargs)
