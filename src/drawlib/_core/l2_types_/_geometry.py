# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Geometry type definitions for drawlib."""

from typing import Any

from pydantic import TypeAdapter

# Modern type definitions
Coordinate = tuple[float, float]
Coordinates = list[Coordinate]

Bezier2 = tuple[Coordinate, Coordinate]
Bezier3 = tuple[Coordinate, Coordinate, Coordinate]
PathPoint = Coordinate | Bezier2 | Bezier3
PathPoints = list[PathPoint]

# Backward compatibility aliases
TypeCoordinate = Coordinate
TypeCoordinates = Coordinates
TypeBezier2 = Bezier2
TypeBezier3 = Bezier3
TypePathPoint = PathPoint
TypePathPoints = PathPoints

# Adapters and helpers for programmatic validation and normalization
_coordinate_adapter: TypeAdapter[Coordinate] = TypeAdapter(Coordinate)
_bezier2_adapter: TypeAdapter[Bezier2] = TypeAdapter(Bezier2)
_bezier3_adapter: TypeAdapter[Bezier3] = TypeAdapter(Bezier3)
_path_point_adapter: TypeAdapter[PathPoint] = TypeAdapter(PathPoint)


def normalize_coordinate(v: Any) -> tuple[float, float]:  # noqa: ANN401
    """Normalize input coordinate to a 2-tuple of floats using Pydantic."""
    return _coordinate_adapter.validate_python(v)


validate_coordinate = normalize_coordinate


def validate_bezier2(v: Any) -> tuple[tuple[float, float], tuple[float, float]]:  # noqa: ANN401
    """Validate Bezier2 (Quadratic Bezier) using Pydantic."""
    return _bezier2_adapter.validate_python(v)


def validate_bezier3(v: Any) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:  # noqa: ANN401
    """Validate Bezier3 (Cubic Bezier) using Pydantic."""
    return _bezier3_adapter.validate_python(v)


def validate_path_point(v: Any) -> Any:  # noqa: ANN401
    """Validate path point using Pydantic."""
    return _path_point_adapter.validate_python(v)
