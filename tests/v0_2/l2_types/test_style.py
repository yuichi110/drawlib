# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for style validations and types in _style.py."""

import pytest
from pydantic import TypeAdapter, ValidationError

from drawlib.v0_2.private.l2_types_._style import (
    TypeAlpha,
    TypeAngle,
    TypeAngle90,
    TypeArrowHead,
    TypeBend,
    TypeColor,
    TypeColorRGB,
    TypeColorRGBA,
    TypeHAlign,
    TypeIconStyle,
    TypeLineStyle,
    TypeSize,
    TypeTailEdge,
    TypeVAlign,
    validate_alpha,
    validate_angle,
    validate_angle_90,
    validate_bend,
    validate_color_tuple,
)


class TestAlphaValidation:
    """Test cases for validate_alpha."""

    def test_validate_alpha(self):
        """Test validate_alpha with valid and invalid bounds."""
        assert validate_alpha(0.0) == 0.0
        assert validate_alpha(0.5) == 0.5
        assert validate_alpha(1.0) == 1.0

        with pytest.raises(ValueError, match="Value must be between 0.0 and 1.0"):
            validate_alpha(-0.1)
        with pytest.raises(ValueError, match="Value must be between 0.0 and 1.0"):
            validate_alpha(1.01)


class TestAngleValidation:
    """Test cases for validate_angle and validate_angle_90."""

    def test_validate_angle(self):
        """Test validate_angle with valid and invalid bounds."""
        assert validate_angle(0.0) == 0.0
        assert validate_angle(180.0) == 180.0
        assert validate_angle(360.0) == 360.0

        with pytest.raises(ValueError, match="Angle must be between 0.0 and 360.0"):
            validate_angle(-0.1)
        with pytest.raises(ValueError, match="Angle must be between 0.0 and 360.0"):
            validate_angle(360.01)

    def test_validate_angle_90(self):
        """Test validate_angle_90 with valid and invalid bounds."""
        assert validate_angle_90(0.0) == 0.0
        assert validate_angle_90(45.0) == 45.0
        assert validate_angle_90(90.0) == 90.0

        with pytest.raises(ValueError, match="Value must be between 0.0 and 90.0"):
            validate_angle_90(-0.1)
        with pytest.raises(ValueError, match="Value must be between 0.0 and 90.0"):
            validate_angle_90(90.01)


class TestBendValidation:
    """Test cases for validate_bend."""

    def test_validate_bend(self):
        """Test validate_bend with valid and invalid bounds."""
        assert validate_bend(0.0) == 0.0
        assert validate_bend(1.9) == 1.9
        assert validate_bend(-1.9) == -1.9

        with pytest.raises(ValueError, match="Value must be between -2.0 and 2.0"):
            validate_bend(-2.0)
        with pytest.raises(ValueError, match="Value must be between -2.0 and 2.0"):
            validate_bend(2.0)


class TestColorTupleValidation:
    """Test cases for validate_color_tuple."""

    def test_validate_color_tuple_valid(self):
        """Test validate_color_tuple with valid RGB and RGBA tuples."""
        assert validate_color_tuple((255, 0, 128)) == (255, 0, 128)
        assert validate_color_tuple((0, 255, 0, 0.5)) == (0, 255, 0, 0.5)

    def test_validate_color_tuple_invalid_len(self):
        """Test validate_color_tuple with invalid length."""
        with pytest.raises(ValueError, match="Color tuple must be length 3"):
            validate_color_tuple((255, 0))
        with pytest.raises(ValueError, match="Color tuple must be length 3"):
            validate_color_tuple((255, 0, 128, 0.5, 9))

    def test_validate_color_tuple_invalid_rgb(self):
        """Test validate_color_tuple with invalid RGB values."""
        with pytest.raises(ValueError, match="RGB values must be integers between 0 and 255"):
            validate_color_tuple((-1, 0, 128))
        with pytest.raises(ValueError, match="RGB values must be integers between 0 and 255"):
            validate_color_tuple((256, 0, 128))
        with pytest.raises(ValueError, match="RGB values must be integers between 0 and 255"):
            validate_color_tuple((255.5, 0, 128))

    def test_validate_color_tuple_invalid_alpha(self):
        """Test validate_color_tuple with invalid RGBA alpha values."""
        with pytest.raises(ValueError, match="Alpha value must be float between 0.0 and 1.0"):
            validate_color_tuple((255, 0, 128, -0.1))
        with pytest.raises(ValueError, match="Alpha value must be float between 0.0 and 1.0"):
            validate_color_tuple((255, 0, 128, 1.01))
        with pytest.raises(ValueError, match="Alpha value must be float between 0.0 and 1.0"):
            validate_color_tuple((255, 0, 128, "opaque"))


class TestStyleTypes:
    """Test cases for style type validation using TypeAdapter."""

    def test_type_alpha(self):
        """Test TypeAlpha validation."""
        adapter: TypeAdapter[TypeAlpha] = TypeAdapter(TypeAlpha)
        assert adapter.validate_python(0.5) == 0.5
        with pytest.raises(ValidationError):
            adapter.validate_python(-0.1)

    def test_type_angle(self):
        """Test TypeAngle validation."""
        adapter: TypeAdapter[TypeAngle] = TypeAdapter(TypeAngle)
        assert adapter.validate_python(180.0) == 180.0
        with pytest.raises(ValidationError):
            adapter.validate_python(360.1)

    def test_type_angle_90(self):
        """Test TypeAngle90 validation."""
        adapter: TypeAdapter[TypeAngle90] = TypeAdapter(TypeAngle90)
        assert adapter.validate_python(45.0) == 45.0
        with pytest.raises(ValidationError):
            adapter.validate_python(90.1)

    def test_type_bend(self):
        """Test TypeBend validation."""
        adapter: TypeAdapter[TypeBend] = TypeAdapter(TypeBend)
        assert adapter.validate_python(1.0) == 1.0
        with pytest.raises(ValidationError):
            adapter.validate_python(2.0)

    def test_type_color_rgb(self):
        """Test TypeColorRGB validation."""
        adapter: TypeAdapter[TypeColorRGB] = TypeAdapter(TypeColorRGB)
        assert adapter.validate_python((255, 0, 128)) == (255, 0, 128)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128, 0.5))

    def test_type_color_rgba(self):
        """Test TypeColorRGBA validation."""
        adapter: TypeAdapter[TypeColorRGBA] = TypeAdapter(TypeColorRGBA)
        assert adapter.validate_python((255, 0, 128, 0.5)) == (255, 0, 128, 0.5)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128))

    def test_type_color(self):
        """Test TypeColor validation."""
        adapter: TypeAdapter[TypeColor] = TypeAdapter(TypeColor)
        assert adapter.validate_python((255, 0, 128)) == (255, 0, 128)
        assert adapter.validate_python((255, 0, 128, 0.5)) == (255, 0, 128, 0.5)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0))


class TestStyleLiterals:
    """Test cases for literal style types validation using TypeAdapter."""

    def test_type_icon_style(self):
        """Test TypeIconStyle validation."""
        adapter: TypeAdapter[TypeIconStyle] = TypeAdapter(TypeIconStyle)
        assert adapter.validate_python("regular") == "regular"
        assert adapter.validate_python("bold") == "bold"
        with pytest.raises(ValidationError):
            adapter.validate_python("italic")

    def test_type_halign(self):
        """Test TypeHAlign validation."""
        adapter: TypeAdapter[TypeHAlign] = TypeAdapter(TypeHAlign)
        assert adapter.validate_python("center") == "center"
        with pytest.raises(ValidationError):
            adapter.validate_python("justify")

    def test_type_valign(self):
        """Test TypeVAlign validation."""
        adapter: TypeAdapter[TypeVAlign] = TypeAdapter(TypeVAlign)
        assert adapter.validate_python("top") == "top"
        with pytest.raises(ValidationError):
            adapter.validate_python("middle")

    def test_type_line_style(self):
        """Test TypeLineStyle validation."""
        adapter: TypeAdapter[TypeLineStyle] = TypeAdapter(TypeLineStyle)
        assert adapter.validate_python("solid") == "solid"
        assert adapter.validate_python("dashed") == "dashed"
        with pytest.raises(ValidationError):
            adapter.validate_python("wavy")

    def test_type_arrow_head(self):
        """Test TypeArrowHead validation."""
        adapter: TypeAdapter[TypeArrowHead] = TypeAdapter(TypeArrowHead)
        assert adapter.validate_python("->") == "->"
        assert adapter.validate_python("") == ""
        with pytest.raises(ValidationError):
            adapter.validate_python("==>")

    def test_type_tail_edge(self):
        """Test TypeTailEdge validation."""
        adapter: TypeAdapter[TypeTailEdge] = TypeAdapter(TypeTailEdge)
        assert adapter.validate_python("bottom") == "bottom"
        with pytest.raises(ValidationError):
            adapter.validate_python("center")

    def test_type_size(self):
        """Test TypeSize validation."""
        adapter: TypeAdapter[TypeSize] = TypeAdapter(TypeSize)
        assert adapter.validate_python("medium") == "medium"
        assert adapter.validate_python(12.5) == 12.5
        with pytest.raises(ValidationError):
            adapter.validate_python("huge")
        with pytest.raises(ValidationError):
            adapter.validate_python(-1.5)
