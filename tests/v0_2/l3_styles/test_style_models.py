# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# type: ignore

"""Unit tests for the style models in l3_styles."""

from dataclasses import asdict as ds_asdict
from typing import Any

import pytest

from drawlib.v0_2.private.l3_fonts import Font
from drawlib.v0_2.private.l3_styles._colors import Colors
from drawlib.v0_2.private.l3_styles._style_models import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)


def asdict(obj: Any) -> dict[str, Any]:
    """Helper to convert style objects or dataclasses to dict representation."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return ds_asdict(obj)


class TestStyleModelBase:
    """Test cases for _StyleModel base features (extra fields, assignments, types)."""

    def test_extra_fields_forbidden(self):
        """Test that instantiating a style model with extra fields raises ValueError."""
        with pytest.raises(ValueError):
            IconStyle(extra_field_name="forbidden")

    def test_validate_assignment(self):
        """Test that validation is performed on attribute assignment."""
        style = IconStyle()
        with pytest.raises(ValueError):
            style.style = "wrong"  # type: ignore

    def test_merge_type_mismatch(self):
        """Test that merging a style with a mismatched class raises ValueError."""
        style1 = IconStyle()
        style2 = TextStyle()
        with pytest.raises(ValueError, match='Arg "style" requires IconStyle'):
            style1.merge(style2)  # type: ignore


class TestIconStyle:
    """Test cases for IconStyle validation, copy, and merge."""

    def test_icon_style_validation(self):
        """Test validation and default values of IconStyle fields."""
        assert asdict(IconStyle()) == {
            "style": None,
            "color": None,
            "alpha": None,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(style="thin")) == {
            "style": "thin",
            "color": None,
            "alpha": None,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(color=Colors.Red)) == {
            "style": None,
            "color": Colors.Red,
            "alpha": None,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(color=(100, 100, 100))) == {
            "style": None,
            "color": (100, 100, 100),
            "alpha": None,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(color=(100, 100, 100, 0.5))) == {
            "style": None,
            "color": (100, 100, 100, 0.5),
            "alpha": None,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(alpha=0.5)) == {
            "style": None,
            "color": None,
            "alpha": 0.5,
            "halign": None,
            "valign": None,
        }
        assert asdict(IconStyle(halign="left")) == {
            "style": None,
            "color": None,
            "alpha": None,
            "halign": "left",
            "valign": None,
        }
        assert asdict(IconStyle(valign="bottom")) == {
            "style": None,
            "color": None,
            "alpha": None,
            "halign": None,
            "valign": "bottom",
        }

        with pytest.raises(ValueError):
            IconStyle(style="wrong")
        with pytest.raises(ValueError):
            IconStyle(color=0.1)
        with pytest.raises(ValueError):
            IconStyle(color=(100, 100, 1000))
        with pytest.raises(ValueError):
            IconStyle(color=(100, 100, 100, 10))
        with pytest.raises(ValueError):
            IconStyle(halign="wrong")
        with pytest.raises(ValueError):
            IconStyle(valign="wrong")

    def test_icon_style_copy(self):
        """Test copy() behavior on IconStyle."""
        style1 = IconStyle(style="thin", color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_icon_style_merge(self):
        """Test merge() behavior on IconStyle."""
        style1 = IconStyle(style="thin", color=Colors.Red)
        style2 = IconStyle(halign="left")
        style3 = style1.merge(style2)

        assert style1 == IconStyle(style="thin", color=Colors.Red)
        assert style2 == IconStyle(halign="left")
        assert style3 == IconStyle(style="thin", color=Colors.Red, halign="left")


class TestImageStyle:
    """Test cases for ImageStyle validation, copy, and merge."""

    def test_image_style_validation(self):
        """Test validation and default values of ImageStyle fields."""
        assert asdict(ImageStyle()) == {
            "halign": None,
            "valign": None,
            "lwidth": None,
            "lstyle": None,
            "lcolor": None,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(halign="left")) == {
            "halign": "left",
            "valign": None,
            "lwidth": None,
            "lstyle": None,
            "lcolor": None,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(valign="bottom")) == {
            "halign": None,
            "valign": "bottom",
            "lwidth": None,
            "lstyle": None,
            "lcolor": None,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(lwidth=2)) == {
            "halign": None,
            "valign": None,
            "lwidth": 2,
            "lstyle": None,
            "lcolor": None,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(lstyle="dashed")) == {
            "halign": None,
            "valign": None,
            "lwidth": None,
            "lstyle": "dashed",
            "lcolor": None,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(lcolor=Colors.Red)) == {
            "halign": None,
            "valign": None,
            "lwidth": None,
            "lstyle": None,
            "lcolor": Colors.Red,
            "fcolor": None,
            "alpha": None,
        }
        assert asdict(ImageStyle(fcolor=Colors.Red)) == {
            "halign": None,
            "valign": None,
            "lwidth": None,
            "lstyle": None,
            "lcolor": None,
            "fcolor": Colors.Red,
            "alpha": None,
        }
        assert asdict(ImageStyle(alpha=0.3)) == {
            "halign": None,
            "valign": None,
            "lwidth": None,
            "lstyle": None,
            "lcolor": None,
            "fcolor": None,
            "alpha": 0.3,
        }
        with pytest.raises(ValueError):
            ImageStyle(halign="wrong")
        with pytest.raises(ValueError):
            ImageStyle(valign="wrong")
        with pytest.raises(ValueError):
            ImageStyle(lstyle="wrong")

    def test_image_style_copy(self):
        """Test copy() behavior on ImageStyle."""
        style1 = ImageStyle(halign="left", lstyle="dashed", lwidth=1)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_image_style_merge(self):
        """Test merge() behavior on ImageStyle."""
        style1 = ImageStyle(halign="left", lstyle="dashed", lwidth=1)
        style2 = ImageStyle(valign="bottom")
        style3 = style1.merge(style2)
        assert style3 == ImageStyle(halign="left", valign="bottom", lstyle="dashed", lwidth=1)


class TestLineStyle:
    """Test cases for LineStyle validation, copy, and merge."""

    def test_line_style_validation(self):
        """Test validation and default values of LineStyle fields."""
        assert asdict(LineStyle()) == {
            "width": None,
            "style": None,
            "color": None,
            "alpha": None,
            "ahscale": None,
            "ahfill": None,
        }
        assert asdict(LineStyle(width=2)) == {
            "width": 2,
            "style": None,
            "color": None,
            "alpha": None,
            "ahscale": None,
            "ahfill": None,
        }
        assert asdict(LineStyle(style="dashed")) == {
            "width": None,
            "style": "dashed",
            "color": None,
            "alpha": None,
            "ahscale": None,
            "ahfill": None,
        }
        assert asdict(LineStyle(color=Colors.Red)) == {
            "width": None,
            "style": None,
            "color": Colors.Red,
            "alpha": None,
            "ahscale": None,
            "ahfill": None,
        }
        assert asdict(LineStyle(alpha=0.5)) == {
            "width": None,
            "style": None,
            "color": None,
            "alpha": 0.5,
            "ahscale": None,
            "ahfill": None,
        }

        with pytest.raises(ValueError):
            LineStyle(width="wrong")
        with pytest.raises(ValueError):
            LineStyle(style="wrong")
        with pytest.raises(ValueError):
            LineStyle(color="wrong")
        with pytest.raises(ValueError):
            LineStyle(alpha="wrong")

    def test_line_style_copy(self):
        """Test copy() behavior on LineStyle."""
        style1 = LineStyle(color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_line_style_merge(self):
        """Test merge() behavior on LineStyle."""
        style1 = LineStyle(color=Colors.Red, width=2)
        style2 = LineStyle(style="dashed")
        style3 = style1.merge(style2)
        assert style3 == LineStyle(color=Colors.Red, width=2, style="dashed")


class TestShapeStyle:
    """Test cases for ShapeStyle validation, copy, and merge."""

    def test_shape_style_validation(self):
        """Test validation and default values of ShapeStyle fields."""
        assert asdict(ShapeStyle()) == {
            "halign": None,
            "valign": None,
            "alpha": None,
            "lwidth": None,
            "lcolor": None,
            "lstyle": None,
            "fcolor": None,
        }
        assert asdict(ShapeStyle(halign="left")) == {
            "halign": "left",
            "valign": None,
            "alpha": None,
            "lwidth": None,
            "lcolor": None,
            "lstyle": None,
            "fcolor": None,
        }
        assert asdict(ShapeStyle(valign="bottom")) == {
            "halign": None,
            "valign": "bottom",
            "alpha": None,
            "lwidth": None,
            "lcolor": None,
            "lstyle": None,
            "fcolor": None,
        }

        assert asdict(ShapeStyle(alpha=0.5)) == {
            "halign": None,
            "valign": None,
            "alpha": 0.5,
            "lwidth": None,
            "lcolor": None,
            "lstyle": None,
            "fcolor": None,
        }
        assert asdict(ShapeStyle(lwidth=2)) == {
            "halign": None,
            "valign": None,
            "alpha": None,
            "lwidth": 2,
            "lcolor": None,
            "lstyle": None,
            "fcolor": None,
        }
        assert asdict(ShapeStyle(lcolor=Colors.Red)) == {
            "halign": None,
            "valign": None,
            "alpha": None,
            "lwidth": None,
            "lcolor": Colors.Red,
            "lstyle": None,
            "fcolor": None,
        }
        assert asdict(ShapeStyle(lstyle="dashed")) == {
            "halign": None,
            "valign": None,
            "alpha": None,
            "lwidth": None,
            "lcolor": None,
            "lstyle": "dashed",
            "fcolor": None,
        }
        assert asdict(ShapeStyle(fcolor=Colors.Red)) == {
            "halign": None,
            "valign": None,
            "alpha": None,
            "lwidth": None,
            "lcolor": None,
            "lstyle": None,
            "fcolor": Colors.Red,
        }

        with pytest.raises(ValueError):
            ShapeStyle(halign="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(valign="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(alpha="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(lwidth="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(lcolor="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(lstyle="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(fcolor="wrong")

    def test_shape_style_copy(self):
        """Test copy() behavior on ShapeStyle."""
        style1 = ShapeStyle(lcolor=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_style_merge(self):
        """Test merge() behavior on ShapeStyle."""
        style1 = ShapeStyle(lcolor=Colors.Red, lwidth=2)
        style2 = ShapeStyle(fcolor=Colors.Blue)
        style3 = style1.merge(style2)
        assert style3 == ShapeStyle(lcolor=Colors.Red, lwidth=2, fcolor=Colors.Blue)


class TestShapeTextStyle:
    """Test cases for ShapeTextStyle validation, copy, and merge."""

    def test_shape_text_style_validation(self):
        """Test validation and default values of ShapeTextStyle fields."""
        assert asdict(ShapeTextStyle()) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(alpha=0.5)) == {
            "alpha": 0.5,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(color=Colors.Red)) == {
            "alpha": None,
            "color": Colors.Red,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(size=20)) == {
            "alpha": None,
            "color": None,
            "size": 20,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(halign="left")) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": "left",
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(valign="bottom")) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": "bottom",
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(font=Font.SANSSERIF_BOLD)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": Font.SANSSERIF_BOLD,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(angle=90)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": 90,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(flip=True)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": True,
            "xy_shift": None,
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(xy_shift=(10, 10))) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": (10, 10),
            "xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(xy_abs_shift=(10, 10))) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "angle": None,
            "flip": None,
            "xy_shift": None,
            "xy_abs_shift": (10, 10),
        }

        with pytest.raises(ValueError):
            ShapeTextStyle(alpha="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(color="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(size="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(halign="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(valign="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(font="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(angle="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(flip="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(xy_shift="wrong")

    def test_shape_text_style_copy(self):
        """Test copy() behavior on ShapeTextStyle."""
        style1 = ShapeTextStyle(color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_text_style_merge(self):
        """Test merge() behavior on ShapeTextStyle."""
        style1 = ShapeTextStyle(color=Colors.Red, size=20)
        style2 = ShapeTextStyle(font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == ShapeTextStyle(color=Colors.Red, size=20, font=Font.SANSSERIF_BOLD)


class TestTextStyle:
    """Test cases for TextStyle validation, copy, and merge."""

    def test_text_style_validation(self):
        """Test validation and default values of TextStyle fields."""
        assert asdict(TextStyle()) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(alpha=0.5)) == {
            "alpha": 0.5,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(color=Colors.Red)) == {
            "alpha": None,
            "color": Colors.Red,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(size=20)) == {
            "alpha": None,
            "color": None,
            "size": 20,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(halign="left")) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": "left",
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(valign="bottom")) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": "bottom",
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(font=Font.SANSSERIF_BOLD)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": Font.SANSSERIF_BOLD,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }

        assert asdict(TextStyle(bgalpha=0.5)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": 0.5,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(bglcolor=Colors.Red)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": Colors.Red,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(bglstyle="dashed")) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": "dashed",
            "bglwidth": None,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(bglwidth=2)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": 2,
            "bgfcolor": None,
        }
        assert asdict(TextStyle(bgfcolor=Colors.Red)) == {
            "alpha": None,
            "color": None,
            "size": None,
            "halign": None,
            "valign": None,
            "font": None,
            "bgalpha": None,
            "bglcolor": None,
            "bglstyle": None,
            "bglwidth": None,
            "bgfcolor": Colors.Red,
        }

        with pytest.raises(ValueError):
            TextStyle(alpha="wrong")
        with pytest.raises(ValueError):
            TextStyle(color="wrong")
        with pytest.raises(ValueError):
            TextStyle(size="wrong")
        with pytest.raises(ValueError):
            TextStyle(halign="wrong")
        with pytest.raises(ValueError):
            TextStyle(valign="wrong")
        with pytest.raises(ValueError):
            TextStyle(font="wrong")
        with pytest.raises(ValueError):
            TextStyle(bgalpha="wrong")
        with pytest.raises(ValueError):
            TextStyle(bglcolor="wrong")
        with pytest.raises(ValueError):
            TextStyle(bglstyle="wrong")
        with pytest.raises(ValueError):
            TextStyle(bglwidth="wrong")
        with pytest.raises(ValueError):
            TextStyle(bgfcolor="wrong")

    def test_text_style_copy(self):
        """Test copy() behavior on TextStyle."""
        style1 = TextStyle(color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_text_style_merge(self):
        """Test merge() behavior on TextStyle."""
        style1 = TextStyle(color=Colors.Red, size=20)
        style2 = TextStyle(font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == TextStyle(color=Colors.Red, size=20, font=Font.SANSSERIF_BOLD)
