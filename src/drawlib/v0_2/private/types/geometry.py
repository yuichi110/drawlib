# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Geometry type definitions for drawlib."""

from typing import Annotated, Any

from pydantic import AfterValidator


def validate_coordinate(v: Any) -> tuple[float, float]:  # noqa: ANN401
    """Validate coordinate."""
    if not isinstance(v, (tuple, list)) or len(v) != 2:
        raise ValueError(f"Coordinate must be a tuple of 2 floats. But {v} is given.")
    return (float(v[0]), float(v[1]))


def validate_bezier2(v: Any) -> tuple[tuple[float, float], tuple[float, float]]:  # noqa: ANN401
    """Validate Bezier2 (Quadratic Bezier)."""
    if not isinstance(v, (tuple, list)) or len(v) != 2:
        raise ValueError(f"Bezier2 must be a tuple of 2 coordinates. But {v} is given.")
    return (validate_coordinate(v[0]), validate_coordinate(v[1]))


def validate_bezier3(v: Any) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:  # noqa: ANN401
    """Validate Bezier3 (Cubic Bezier)."""
    if not isinstance(v, (tuple, list)) or len(v) != 3:
        raise ValueError(f"Bezier3 must be a tuple of 3 coordinates. But {v} is given.")
    return (validate_coordinate(v[0]), validate_coordinate(v[1]), validate_coordinate(v[2]))


def validate_path_point(v: Any) -> Any:  # noqa: ANN401
    """Validate path point (dispatch to Coord/Bezier2/Bezier3)."""
    if not isinstance(v, (tuple, list)):
        raise ValueError(f"PathPoint must be a tuple. But {v} is given.")

    length = len(v)
    if length == 2:
        if isinstance(v[0], (int, float)):
            return validate_coordinate(v)
        else:
            return validate_bezier2(v)
    elif length == 3:
        return validate_bezier3(v)
    else:
        raise ValueError(f"PathPoint must be length 2 (Coord/Bezier2) or 3 (Bezier3). But {v} is given.")


TypeCoordinate = Annotated[tuple[float, float], AfterValidator(validate_coordinate)]
TypeCoordinates = Annotated[list[TypeCoordinate], AfterValidator(lambda v: v)]

TypeBezier2 = Annotated[tuple[TypeCoordinate, TypeCoordinate], AfterValidator(validate_bezier2)]
TypeBezier3 = Annotated[tuple[TypeCoordinate, TypeCoordinate, TypeCoordinate], AfterValidator(validate_bezier3)]
TypePathPoint = Annotated[TypeCoordinate | TypeBezier2 | TypeBezier3, AfterValidator(validate_path_point)]
TypePathPoints = Annotated[list[TypePathPoint], AfterValidator(lambda v: v)]
