# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for geometry types and validation in _geometry.py."""

import pytest
from pydantic import TypeAdapter, ValidationError

from drawlib._core.l2_types_._geometry import (
    Bezier2,
    Bezier3,
    Coordinate,
    Coordinates,
    PathPoint,
    PathPoints,
)


class TestGeometryTypes:
    """Test cases for geometry type aliases using TypeAdapter."""

    def test_type_coordinate(self):
        """Test Coordinate validation."""
        adapter: TypeAdapter[Coordinate] = TypeAdapter(Coordinate)
        assert adapter.validate_python((1.5, 2.5)) == (1.5, 2.5)
        assert adapter.validate_python([10, 20]) == (10.0, 20.0)
        with pytest.raises(ValueError):
            adapter.validate_python((1, 2, 3))

    def test_type_coordinates(self):
        """Test Coordinates validation."""
        adapter: TypeAdapter[list[Coordinate]] = TypeAdapter(Coordinates)
        assert adapter.validate_python([(1, 2), (3, 4)]) == [(1.0, 2.0), (3.0, 4.0)]

    def test_type_bezier2(self):
        """Test Bezier2 validation."""
        adapter: TypeAdapter[Bezier2] = TypeAdapter(Bezier2)
        assert adapter.validate_python(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))

    def test_type_bezier3(self):
        """Test Bezier3 validation."""
        adapter: TypeAdapter[Bezier3] = TypeAdapter(Bezier3)
        assert adapter.validate_python(((1, 2), (3, 4), (5, 6))) == ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))

    def test_type_path_point(self):
        """Test PathPoint validation."""
        adapter: TypeAdapter[PathPoint] = TypeAdapter(PathPoint)
        assert adapter.validate_python((1, 2)) == (1.0, 2.0)
        assert adapter.validate_python(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))

    def test_type_path_points(self):
        """Test PathPoints validation."""
        adapter: TypeAdapter[list[PathPoint]] = TypeAdapter(PathPoints)
        points: list[PathPoint] = [(1, 2), ((1, 2), (3, 4))]
        assert adapter.validate_python(points) == [(1.0, 2.0), ((1.0, 2.0), (3.0, 4.0))]
