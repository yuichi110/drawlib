# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the immutable Style model in l3_styles."""

from typing import Any

import pytest
from pydantic import ValidationError

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles._colors import Colors
from drawlib._core.l3_styles._style_models import Style


class TestStyleModelBase:
    """Test cases for core Style model behaviors: immutability, extra fields, patch."""

    def test_default_values(self):
        """Test default values of Style attributes are all None."""
        style = Style()
        for field in style.model_fields:
            assert getattr(style, field) is None

    def test_extra_fields_forbidden(self):
        """Test that instantiating Style with unknown fields raises ValueError."""
        with pytest.raises(ValueError):
            bad_kwargs: dict[str, Any] = {"unknown_prop": "forbidden"}
            Style(**bad_kwargs)

    def test_immutable_frozen(self):
        """Test that direct attribute assignment raises ValueError (frozen model)."""
        style = Style(shape_fill_color=Colors.Red)
        with pytest.raises(ValueError):
            setattr(style, "shape_fill_color", Colors.Blue)

    def test_patch_creates_new_instance(self):
        """Test that patch() returns a new instance and does not mutate the original."""
        original = Style(shape_fill_color=Colors.Red, shape_line_width=1.0)
        patched = original.patch(shape_fill_color=Colors.Blue, line_width=2.5)

        assert original.shape_fill_color == Colors.Red
        assert original.shape_line_width == 1.0
        assert original.line_width is None

        assert patched.shape_fill_color == Colors.Blue
        assert patched.shape_line_width == 1.0
        assert patched.line_width == 2.5

    def test_patch_forbidden_attribute(self):
        """Test that patching with invalid attribute raises ValidationError or TypeError."""
        style = Style()
        bad_patch: dict[str, Any] = {"non_existent_prop": 123}
        with pytest.raises((ValidationError, TypeError)):
            style.patch(**bad_patch)


class TestShapeProperties:
    """Test cases for shape_* properties."""

    def test_valid_shape_properties(self):
        """Test valid shape property values."""
        s = Style(
            shape_fill_color=Colors.Blue,
            shape_fill_alpha=0.8,
            shape_line_color=Colors.Black,
            shape_line_width=2.0,
            shape_line_style="dashed",
        )
        assert s.shape_fill_color == Colors.Blue
        assert s.shape_fill_alpha == 0.8
        assert s.shape_line_color == Colors.Black
        assert s.shape_line_width == 2.0
        assert s.shape_line_style == "dashed"

    def test_invalid_shape_properties(self):
        """Test invalid shape property values raise ValueError."""
        with pytest.raises(ValueError):
            Style(**{"shape_line_style": "invalid_style"})
        with pytest.raises(ValueError):
            Style(shape_line_width=-1.0)
        with pytest.raises(ValueError):
            Style(shape_fill_alpha=1.5)


class TestLineProperties:
    """Test cases for line_* properties."""

    def test_valid_line_properties(self):
        """Test valid line property values."""
        s = Style(
            line_color=Colors.Green,
            line_width=3.0,
            line_style="dotted",
            line_alpha=0.9,
            line_arrow_head_fill=True,
            line_arrow_head_scale=15.0,
        )
        assert s.line_color == Colors.Green
        assert s.line_width == 3.0
        assert s.line_style == "dotted"
        assert s.line_alpha == 0.9
        assert s.line_arrow_head_fill is True
        assert s.line_arrow_head_scale == 15.0

    def test_invalid_line_properties(self):
        """Test invalid line property values raise ValueError."""
        with pytest.raises(ValueError):
            Style(**{"line_style": "zigzag"})
        with pytest.raises(ValueError):
            Style(line_width=-0.5)


class TestTextProperties:
    """Test cases for text_* properties."""

    def test_valid_text_properties(self):
        """Test valid text property values."""
        s = Style(
            text_color=Colors.Black,
            text_size=18.0,
            text_font=Font.SANSSERIF_BOLD,
            text_halign="center",
            text_valign="bottom",
            text_angle=45.0,
            text_flip=True,
            text_xy_shift=(2.0, 3.0),
            text_bg_fill_color=Colors.Gray,
            text_bg_fill_alpha=0.5,
            text_bg_line_color=Colors.Black,
            text_bg_line_width=1.0,
            text_bg_line_style="solid",
        )
        assert s.text_color == Colors.Black
        assert s.text_size == 18.0
        assert s.text_font == Font.SANSSERIF_BOLD
        assert s.text_halign == "center"
        assert s.text_valign == "bottom"
        assert s.text_angle == 45.0
        assert s.text_flip is True
        assert s.text_xy_shift == (2.0, 3.0)
        assert s.text_bg_fill_color == Colors.Gray

    def test_invalid_text_properties(self):
        """Test invalid text property values raise ValueError."""
        with pytest.raises(ValueError):
            Style(**{"text_halign": "middle"})
        with pytest.raises(ValueError):
            Style(**{"text_valign": "middle"})
        with pytest.raises(ValueError):
            Style(text_size=-5.0)


class TestIconProperties:
    """Test cases for icon_* properties."""

    def test_valid_icon_properties(self):
        """Test valid icon property values."""
        s = Style(
            icon_color=Colors.Purple,
            icon_style="bold",
        )
        assert s.icon_color == Colors.Purple
        assert s.icon_style == "bold"

    def test_invalid_icon_properties(self):
        """Test invalid icon property values raise ValueError."""
        with pytest.raises(ValueError):
            Style(**{"icon_style": "huge"})


class TestImageProperties:
    """Test cases for image_* properties."""

    def test_valid_image_properties(self):
        """Test valid image property values."""
        s = Style(
            image_tint_color=Colors.Gray,
            image_alpha=0.7,
            image_border_color=Colors.Black,
            image_border_width=2.0,
            image_border_style="solid",
        )
        assert s.image_tint_color == Colors.Gray
        assert s.image_alpha == 0.7
        assert s.image_border_color == Colors.Black
        assert s.image_border_width == 2.0
        assert s.image_border_style == "solid"

    def test_invalid_image_properties(self):
        """Test invalid image property values raise ValueError."""
        with pytest.raises(ValueError):
            Style(image_border_width=-1.0)
        with pytest.raises(ValueError):
            Style(image_alpha=2.0)
