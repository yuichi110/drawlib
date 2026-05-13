# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Primitive type definitions for drawlib."""

from typing import Annotated

from pydantic import AfterValidator, Field


def validate_alpha(v: float) -> float:
    """Validate alpha value."""
    if not (0.0 <= v <= 1.0):
        raise ValueError(f"Value must be between 0.0 and 1.0. But {v} is given.")
    return v


def validate_angle(v: float) -> float:
    """Validate angle value."""
    if not (0.0 <= v <= 360.0):
        raise ValueError(f"Value must be between 0.0 and 360.0. But {v} is given.")
    return v


def validate_angle_90(v: float) -> float:
    """Validate angle value max 90."""
    if not (0.0 <= v <= 90.0):
        raise ValueError(f"Value must be between 0.0 and 90.0. But {v} is given.")
    return v


def validate_bend(v: float) -> float:
    """Validate bend value."""
    if not (-2.0 < v < 2.0):
        raise ValueError(f"Value must be between -2.0 and 2.0 (exclusive). But {v} is given.")
    return v


TypeAlpha = Annotated[float, AfterValidator(validate_alpha)]
TypeAngle = Annotated[float, AfterValidator(validate_angle)]
TypeAngle90 = Annotated[float, AfterValidator(validate_angle_90)]
TypeBend = Annotated[float, AfterValidator(validate_bend)]

TypePosFloat = Annotated[float, Field(ge=0.0)]
TypePosFloatEx = Annotated[float, Field(gt=0.0)]
TypePosInt = Annotated[int, Field(ge=0)]
TypePosIntEx = Annotated[int, Field(gt=0)]
TypeNumVertex = Annotated[int, Field(ge=3)]
