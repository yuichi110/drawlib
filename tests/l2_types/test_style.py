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

from drawlib._core.l2_types_._style import (
    Alpha,
    Angle,
    Angle90,
    ArrowHead,
    Bend,
    ColorRGB,
    ColorRGBA,
    ColorType,
    HAlign,
    IconStyle,
    LineStyle,
    Size,
    TailEdge,
    VAlign,
)


class TestStyleTypes:
    """Test cases for style type validation using TypeAdapter."""

    def test_type_alpha(self):
        """Test Alpha validation."""
        adapter: TypeAdapter[Alpha] = TypeAdapter(Alpha)
        assert adapter.validate_python(0.5) == 0.5
        with pytest.raises(ValidationError):
            adapter.validate_python(-0.1)

    def test_type_angle(self):
        """Test Angle validation and normalization."""
        adapter: TypeAdapter[Angle] = TypeAdapter(Angle)
        assert adapter.validate_python(180.0) == 180.0
        assert adapter.validate_python(450.0) == 90.0
        assert adapter.validate_python(-270.0) == 90.0
        assert adapter.validate_python(360.0) == 360.0
        assert adapter.validate_python(0.0) == 0.0
        assert adapter.validate_python(720.0) == 0.0
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")

    def test_type_angle_90(self):
        """Test Angle90 validation and normalization."""
        adapter: TypeAdapter[Angle90] = TypeAdapter(Angle90)
        assert adapter.validate_python(45.0) == 45.0
        assert adapter.validate_python(0.0) == 0.0
        assert adapter.validate_python(90.0) == 90.0
        with pytest.raises(ValidationError):
            adapter.validate_python(135.0)
        with pytest.raises(ValidationError):
            adapter.validate_python(-45.0)
        with pytest.raises(ValidationError):
            adapter.validate_python("invalid")

    def test_type_bend(self):
        """Test Bend validation."""
        adapter: TypeAdapter[Bend] = TypeAdapter(Bend)
        assert adapter.validate_python(1.0) == 1.0
        with pytest.raises(ValidationError):
            adapter.validate_python(2.0)

    def test_type_color_rgb(self):
        """Test ColorRGB validation."""
        adapter: TypeAdapter[ColorRGB] = TypeAdapter(ColorRGB)
        assert adapter.validate_python((255, 0, 128)) == (255, 0, 128)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128, 0.5))

    def test_type_color_rgba(self):
        """Test ColorRGBA validation."""
        adapter: TypeAdapter[ColorRGBA] = TypeAdapter(ColorRGBA)
        assert adapter.validate_python((255, 0, 128, 0.5)) == (255, 0, 128, 0.5)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0, 128))

    def test_type_color(self):
        """Test ColorType validation and normalization."""
        adapter: TypeAdapter[ColorType] = TypeAdapter(ColorType)
        # RGB is normalized to RGBA with alpha=1.0
        assert adapter.validate_python((255, 0, 128)) == (255, 0, 128, 1.0)
        assert adapter.validate_python([255, 0, 128]) == (255, 0, 128, 1.0)
        # RGBA is preserved
        assert adapter.validate_python((255, 0, 128, 0.5)) == (255, 0, 128, 0.5)
        # Hex string is converted to RGBA
        assert adapter.validate_python("#ff0000") == (255, 0, 0, 1.0)
        with pytest.raises(ValidationError):
            adapter.validate_python((255, 0))
        with pytest.raises(ValidationError):
            adapter.validate_python("not-a-color")


class TestStyleLiterals:
    """Test cases for literal style types validation using TypeAdapter."""

    def test_type_icon_style(self):
        """Test IconStyle validation."""
        adapter: TypeAdapter[IconStyle] = TypeAdapter(IconStyle)
        assert adapter.validate_python("regular") == "regular"
        assert adapter.validate_python("bold") == "bold"
        with pytest.raises(ValidationError):
            adapter.validate_python("italic")

    def test_type_halign(self):
        """Test HAlign validation."""
        adapter: TypeAdapter[HAlign] = TypeAdapter(HAlign)
        assert adapter.validate_python("center") == "center"
        with pytest.raises(ValidationError):
            adapter.validate_python("justify")

    def test_type_valign(self):
        """Test VAlign validation."""
        adapter: TypeAdapter[VAlign] = TypeAdapter(VAlign)
        assert adapter.validate_python("top") == "top"
        with pytest.raises(ValidationError):
            adapter.validate_python("middle")

    def test_type_line_style(self):
        """Test LineStyle validation."""
        adapter: TypeAdapter[LineStyle] = TypeAdapter(LineStyle)
        assert adapter.validate_python("solid") == "solid"
        assert adapter.validate_python("dashed") == "dashed"
        with pytest.raises(ValidationError):
            adapter.validate_python("wavy")

    def test_type_arrow_head(self):
        """Test ArrowHead validation."""
        adapter: TypeAdapter[ArrowHead] = TypeAdapter(ArrowHead)
        assert adapter.validate_python("->") == "->"
        assert adapter.validate_python("") == ""
        with pytest.raises(ValidationError):
            adapter.validate_python("==>")

    def test_type_tail_edge(self):
        """Test TailEdge validation."""
        adapter: TypeAdapter[TailEdge] = TypeAdapter(TailEdge)
        assert adapter.validate_python("bottom") == "bottom"
        with pytest.raises(ValidationError):
            adapter.validate_python("center")

    def test_type_size(self):
        """Test Size validation."""
        adapter: TypeAdapter[Size] = TypeAdapter(Size)
        assert adapter.validate_python("medium") == "medium"
        assert adapter.validate_python(12.5) == 12.5
        with pytest.raises(ValidationError):
            adapter.validate_python("huge")
        with pytest.raises(ValidationError):
            adapter.validate_python(-1.5)
