"""Manufactured fields with analytically known residual behavior."""

from __future__ import annotations

from functools import partial
from math import exp, sin
from typing import TypeVar, cast

from nsrw.math_kernel.types import ForceField, ScalarField, Vector3, VelocityField

FieldValue = TypeVar("FieldValue", float, Vector3)


def _constant_field(
    value: FieldValue, _point: tuple[float, float, float], _time: float
) -> FieldValue:
    return value


zero_pressure = cast(ScalarField, partial(_constant_field, 0.0))
zero_force = cast(ForceField, partial(_constant_field, (0.0, 0.0, 0.0)))


def decaying_shear(viscosity: float) -> tuple[VelocityField, ScalarField, ForceField]:
    """Return ``u=(exp(-nu*t) sin(y),0,0)``, an unforced exact shear solution."""
    if viscosity <= 0:
        raise ValueError("viscosity must be positive")

    def velocity(point: tuple[float, float, float], time: float) -> tuple[float, float, float]:
        return exp(-viscosity * time) * sin(point[1]), 0.0, 0.0

    return velocity, zero_pressure, zero_force


def forced_linear_shear() -> tuple[VelocityField, ScalarField, ForceField]:
    """Return ``u=(t*y,0,0)`` with the matching force ``f=(y,0,0)``."""

    def velocity(point: tuple[float, float, float], time: float) -> tuple[float, float, float]:
        return time * point[1], 0.0, 0.0

    def force(point: tuple[float, float, float], _time: float) -> tuple[float, float, float]:
        return point[1], 0.0, 0.0

    return velocity, zero_pressure, force
