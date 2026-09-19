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
from pydantic import TypeAdapter

from drawlib._core.l2_types_._geometry import (
    TypeBezier2,
    TypeBezier3,
    TypeCoordinate,
    TypeCoordinates,
    TypePathPoint,
    TypePathPoints,
    validate_bezier2,
    validate_bezier3,
    validate_coordinate,
    validate_path_point,
)


class TestCoordinateValidation:
    """Test cases for coordinate validation functions."""

    def test_validate_coordinate_valid(self):
        """Test validate_coordinate with valid inputs."""
        assert validate_coordinate((1.5, 2.5)) == (1.5, 2.5)
        assert validate_coordinate([3, 4]) == (3.0, 4.0)

    def test_validate_coordinate_invalid(self):
        """Test validate_coordinate with invalid inputs."""
        with pytest.raises(ValueError, match="Coordinate must be a tuple of 2 floats"):
            validate_coordinate("not a coordinate")
        with pytest.raises(ValueError, match="Coordinate must be a tuple of 2 floats"):
            validate_coordinate((1.0,))
        with pytest.raises(ValueError, match="Coordinate must be a tuple of 2 floats"):
            validate_coordinate((1.0, 2.0, 3.0))


class TestBezierValidation:
    """Test cases for bezier validation functions."""

    def test_validate_bezier2_valid(self):
        """Test validate_bezier2 with valid inputs."""
        assert validate_bezier2(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))

    def test_validate_bezier2_invalid(self):
        """Test validate_bezier2 with invalid inputs."""
        with pytest.raises(ValueError, match="Bezier2 must be a tuple of 2 coordinates"):
            validate_bezier2("invalid")
        with pytest.raises(ValueError, match="Bezier2 must be a tuple of 2 coordinates"):
            validate_bezier2(((1, 2),))

    def test_validate_bezier3_valid(self):
        """Test validate_bezier3 with valid inputs."""
        assert validate_bezier3(((1, 2), (3, 4), (5, 6))) == ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))

    def test_validate_bezier3_invalid(self):
        """Test validate_bezier3 with invalid inputs."""
        with pytest.raises(ValueError, match="Bezier3 must be a tuple of 3 coordinates"):
            validate_bezier3("invalid")
        with pytest.raises(ValueError, match="Bezier3 must be a tuple of 3 coordinates"):
            validate_bezier3(((1, 2), (3, 4)))


class TestPathPointValidation:
    """Test cases for path point validation function."""

    def test_validate_path_point_valid(self):
        """Test validate_path_point with valid coordinate, bezier2 and bezier3."""
        # Coordinate dispatch
        assert validate_path_point((1, 2)) == (1.0, 2.0)
        # Bezier2 dispatch
        assert validate_path_point(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))
        # Bezier3 dispatch
        assert validate_path_point(((1, 2), (3, 4), (5, 6))) == ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))

    def test_validate_path_point_invalid(self):
        """Test validate_path_point with invalid inputs."""
        with pytest.raises(ValueError, match="PathPoint must be a tuple"):
            validate_path_point("invalid")
        with pytest.raises(ValueError, match="PathPoint must be length 2"):
            validate_path_point((1, 2, 3, 4))


class TestGeometryTypes:
    """Test cases for geometry type aliases using TypeAdapter."""

    def test_type_coordinate(self):
        """Test TypeCoordinate validation."""
        adapter: TypeAdapter[TypeCoordinate] = TypeAdapter(TypeCoordinate)
        assert adapter.validate_python((1.5, 2.5)) == (1.5, 2.5)
        with pytest.raises(ValueError):
            adapter.validate_python((1, 2, 3))

    def test_type_coordinates(self):
        """Test TypeCoordinates validation."""
        adapter: TypeAdapter[list[TypeCoordinate]] = TypeAdapter(TypeCoordinates)
        assert adapter.validate_python([(1, 2), (3, 4)]) == [(1.0, 2.0), (3.0, 4.0)]

    def test_type_bezier2(self):
        """Test TypeBezier2 validation."""
        adapter: TypeAdapter[TypeBezier2] = TypeAdapter(TypeBezier2)
        assert adapter.validate_python(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))

    def test_type_bezier3(self):
        """Test TypeBezier3 validation."""
        adapter: TypeAdapter[TypeBezier3] = TypeAdapter(TypeBezier3)
        assert adapter.validate_python(((1, 2), (3, 4), (5, 6))) == ((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))

    def test_type_path_point(self):
        """Test TypePathPoint validation."""
        adapter: TypeAdapter[TypePathPoint] = TypeAdapter(TypePathPoint)
        assert adapter.validate_python((1, 2)) == (1.0, 2.0)
        assert adapter.validate_python(((1, 2), (3, 4))) == ((1.0, 2.0), (3.0, 4.0))

    def test_type_path_points(self):
        """Test TypePathPoints validation."""
        adapter: TypeAdapter[list[TypePathPoint]] = TypeAdapter(TypePathPoints)
        points: list[TypePathPoint] = [(1, 2), ((1, 2), (3, 4))]
        assert adapter.validate_python(points) == [(1.0, 2.0), ((1.0, 2.0), (3.0, 4.0))]
