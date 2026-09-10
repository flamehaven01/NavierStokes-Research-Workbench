"""Independent numerical witness for the source's eventual power tail.

The source tail has the form ``A * (X / K)^(-p)`` after the terminal taper,
where ``p = 1/2 + h``.  This module integrates the pressure kernel in the log
coordinate and compares it with the closed-form integral.  It is a parametric
witness: callers must still provide the source-instance ``A`` and ``K``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, isfinite
from typing import Any


@dataclass(frozen=True)
class TailWitness:
    exponent: float
    amplitude: float
    radius: float
    cutoff: float
    log_window: float
    numerical_integral: float
    expected_integral: float
    numerical_pressure_tail: float
    expected_pressure_tail: float
    remainder_bound: float
    absolute_error: float
    tolerance: float
    check_status: str
    evidence_class: str = "PARAMETRIC_SOURCE_TAIL_NUMERICAL_WITNESS"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _simpson(function: Any, upper: float, panels: int) -> float:
    if panels <= 0 or panels % 2:
        raise ValueError("panels must be a positive even integer")
    step = upper / panels
    total = function(0.0) + function(upper)
    total += 4.0 * sum(function(i * step) for i in range(1, panels, 2))
    total += 2.0 * sum(function(i * step) for i in range(2, panels, 2))
    return total * step / 3.0


def source_power_tail_witness(
    *,
    h: float,
    amplitude: float,
    radius: float,
    cutoff: float,
    tolerance: float = 1e-10,
    panels: int = 4096,
    log_window: float = 24.0,
) -> TailWitness:
    """Numerically verify ``∫_cutoff^∞ E(X)^2/X dX`` for the pure tail."""

    values = (h, amplitude, radius, cutoff, tolerance, log_window)
    if any(not isfinite(value) for value in values) or h <= 0 or amplitude <= 0:
        raise ValueError("tail parameters must be finite and positive")
    if radius <= 0 or cutoff < radius * exp(14.0 / 5.0):
        raise ValueError("cutoff must be at or beyond the terminal taper")
    if tolerance <= 0 or panels <= 0 or panels % 2 or log_window <= 0:
        raise ValueError("invalid witness tolerance, panels, or log window")
    exponent = 0.5 + h
    prefactor = amplitude * amplitude * (cutoff / radius) ** (-2.0 * exponent)
    # X = cutoff * exp(s), dX/X = ds.  This is an independent finite
    # quadrature surface; the omitted positive tail is bounded explicitly.
    numerical = _simpson(lambda s: prefactor * exp(-2.0 * exponent * s), log_window, panels)
    remainder = prefactor * exp(-2.0 * exponent * log_window) / (2.0 * exponent)
    expected = prefactor / (2.0 * exponent)
    error = abs((numerical + remainder) - expected)
    numerical_total = numerical + remainder
    return TailWitness(
        exponent,
        amplitude,
        radius,
        cutoff,
        log_window,
        numerical_total,
        expected,
        -0.5 * numerical_total,
        -0.5 * expected,
        remainder,
        error,
        tolerance,
        "PASS" if error <= tolerance else "FAIL",
    )
