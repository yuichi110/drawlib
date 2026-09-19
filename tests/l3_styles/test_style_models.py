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

import inspect
from dataclasses import asdict as ds_asdict
from typing import Any

import pytest

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles._colors import Colors
from drawlib._core.l3_styles._style_models import (
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)

ICON_FIELDS = ["icon_style", "text_color", "fill_alpha", "text_halign", "text_valign"]
IMAGE_FIELDS = ["text_halign", "text_valign", "line_width", "line_style", "line_color", "fill_color", "fill_alpha"]
LINE_FIELDS = ["line_width", "line_style", "text_color", "fill_alpha", "arrow_head_scale", "arrow_head_fill"]
SHAPE_FIELDS = ["text_halign", "text_valign", "fill_alpha", "line_width", "line_color", "line_style", "fill_color"]
SHAPE_TEXT_FIELDS = [
    "fill_alpha",
    "text_color",
    "text_size",
    "text_halign",
    "text_valign",
    "text_font",
    "text_angle",
    "text_flip",
    "text_xy_shift",
    "text_xy_abs_shift",
]
TEXT_FIELDS = [
    "fill_alpha",
    "text_color",
    "text_size",
    "text_halign",
    "text_valign",
    "text_font",
    "text_bg_fill_alpha",
    "text_bg_line_color",
    "text_bg_line_style",
    "text_bg_line_width",
    "text_bg_fill_color",
]

CLS_FIELD_MAP = {
    "TestIconStyle": ICON_FIELDS,
    "TestImageStyle": IMAGE_FIELDS,
    "TestLineStyle": LINE_FIELDS,
    "TestShapeStyle": SHAPE_FIELDS,
    "TestShapeTextStyle": SHAPE_TEXT_FIELDS,
    "TestTextStyle": TEXT_FIELDS,
}


def asdict(obj: Any) -> dict[str, Any]:
    """Helper to convert style objects or dataclasses to dict representation."""
    if hasattr(obj, "model_dump"):
        data = obj.model_dump()
        frame = inspect.currentframe()
        if frame and frame.f_back:
            self_obj = frame.f_back.f_locals.get("self")
            if self_obj:
                cls_name = type(self_obj).__name__
                fields = CLS_FIELD_MAP.get(cls_name)
                if fields:
                    return {k: data[k] for k in fields}
        return data
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
            style.icon_style = "wrong"

    def test_merge_type_mismatch(self):
        """Test that merging a style with a mismatched class raises ValueError."""
        style1 = IconStyle()
        with pytest.raises(ValueError):
            style1.merge("invalid_style")


class TestIconStyle:
    """Test cases for IconStyle validation, copy, and merge."""

    def test_icon_style_validation(self):
        """Test validation and default values of IconStyle fields."""
        assert asdict(IconStyle()) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(icon_style="thin")) == {
            "icon_style": "thin",
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(text_color=Colors.Red)) == {
            "icon_style": None,
            "text_color": Colors.Red,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(text_color=(100, 100, 100))) == {
            "icon_style": None,
            "text_color": (100, 100, 100),
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(text_color=(100, 100, 100, 0.5))) == {
            "icon_style": None,
            "text_color": (100, 100, 100, 0.5),
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(fill_alpha=0.5)) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": 0.5,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(IconStyle(text_halign="left")) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": "left",
            "text_valign": None,
        }
        assert asdict(IconStyle(text_valign="bottom")) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": "bottom",
        }

        with pytest.raises(ValueError):
            IconStyle(icon_style="wrong")
        with pytest.raises(ValueError):
            IconStyle(text_color=0.1)
        with pytest.raises(ValueError):
            IconStyle(text_color=(100, 100, 1000))
        with pytest.raises(ValueError):
            IconStyle(text_color=(100, 100, 100, 10))
        with pytest.raises(ValueError):
            IconStyle(text_halign="wrong")
        with pytest.raises(ValueError):
            IconStyle(text_valign="wrong")

    def test_icon_style_copy(self):
        """Test copy() behavior on IconStyle."""
        style1 = IconStyle(icon_style="thin", text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_icon_style_merge(self):
        """Test merge() behavior on IconStyle."""
        style1 = IconStyle(icon_style="thin", text_color=Colors.Red)
        style2 = IconStyle(text_halign="left")
        style3 = style1.merge(style2)

        assert style1 == IconStyle(icon_style="thin", text_color=Colors.Red)
        assert style2 == IconStyle(text_halign="left")
        assert style3 == IconStyle(icon_style="thin", text_color=Colors.Red, text_halign="left")


class TestImageStyle:
    """Test cases for ImageStyle validation, copy, and merge."""

    def test_image_style_validation(self):
        """Test validation and default values of ImageStyle fields."""
        assert asdict(ImageStyle()) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(text_halign="left")) == {
            "text_halign": "left",
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(text_valign="bottom")) == {
            "text_halign": None,
            "text_valign": "bottom",
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(line_width=2)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": 2,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(line_style="dashed")) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": "dashed",
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(line_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": Colors.Red,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(fill_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": Colors.Red,
            "fill_alpha": None,
        }
        assert asdict(ImageStyle(fill_alpha=0.3)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": 0.3,
        }
        with pytest.raises(ValueError):
            ImageStyle(text_halign="wrong")
        with pytest.raises(ValueError):
            ImageStyle(text_valign="wrong")
        with pytest.raises(ValueError):
            ImageStyle(line_style="wrong")

    def test_image_style_copy(self):
        """Test copy() behavior on ImageStyle."""
        style1 = ImageStyle(text_halign="left", line_style="dashed", line_width=1)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_image_style_merge(self):
        """Test merge() behavior on ImageStyle."""
        style1 = ImageStyle(text_halign="left", line_style="dashed", line_width=1)
        style2 = ImageStyle(text_valign="bottom")
        style3 = style1.merge(style2)
        assert style3 == ImageStyle(text_halign="left", text_valign="bottom", line_style="dashed", line_width=1)


class TestLineStyle:
    """Test cases for LineStyle validation, copy, and merge."""

    def test_line_style_validation(self):
        """Test validation and default values of LineStyle fields."""
        assert asdict(LineStyle()) == {
            "line_width": None,
            "line_style": None,
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(LineStyle(line_width=2)) == {
            "line_width": 2,
            "line_style": None,
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(LineStyle(line_style="dashed")) == {
            "line_width": None,
            "line_style": "dashed",
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(LineStyle(text_color=Colors.Red)) == {
            "line_width": None,
            "line_style": None,
            "text_color": Colors.Red,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(LineStyle(fill_alpha=0.5)) == {
            "line_width": None,
            "line_style": None,
            "text_color": None,
            "fill_alpha": 0.5,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }

        with pytest.raises(ValueError):
            LineStyle(line_width="wrong")
        with pytest.raises(ValueError):
            LineStyle(line_style="wrong")
        with pytest.raises(ValueError):
            LineStyle(text_color="wrong")
        with pytest.raises(ValueError):
            LineStyle(fill_alpha="wrong")

    def test_line_style_copy(self):
        """Test copy() behavior on LineStyle."""
        style1 = LineStyle(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_line_style_merge(self):
        """Test merge() behavior on LineStyle."""
        style1 = LineStyle(text_color=Colors.Red, line_width=2)
        style2 = LineStyle(line_style="dashed")
        style3 = style1.merge(style2)
        assert style3 == LineStyle(text_color=Colors.Red, line_width=2, line_style="dashed")


class TestShapeStyle:
    """Test cases for ShapeStyle validation, copy, and merge."""

    def test_shape_style_validation(self):
        """Test validation and default values of ShapeStyle fields."""
        assert asdict(ShapeStyle()) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(ShapeStyle(text_halign="left")) == {
            "text_halign": "left",
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(ShapeStyle(text_valign="bottom")) == {
            "text_halign": None,
            "text_valign": "bottom",
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }

        assert asdict(ShapeStyle(fill_alpha=0.5)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": 0.5,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(ShapeStyle(line_width=2)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": 2,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(ShapeStyle(line_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": Colors.Red,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(ShapeStyle(line_style="dashed")) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": "dashed",
            "fill_color": None,
        }
        assert asdict(ShapeStyle(fill_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": Colors.Red,
        }

        with pytest.raises(ValueError):
            ShapeStyle(text_halign="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(text_valign="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(fill_alpha="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(line_width="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(line_color="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(line_style="wrong")
        with pytest.raises(ValueError):
            ShapeStyle(fill_color="wrong")

    def test_shape_style_copy(self):
        """Test copy() behavior on ShapeStyle."""
        style1 = ShapeStyle(line_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_style_merge(self):
        """Test merge() behavior on ShapeStyle."""
        style1 = ShapeStyle(line_color=Colors.Red, line_width=2)
        style2 = ShapeStyle(fill_color=Colors.Blue)
        style3 = style1.merge(style2)
        assert style3 == ShapeStyle(line_color=Colors.Red, line_width=2, fill_color=Colors.Blue)


class TestShapeTextStyle:
    """Test cases for ShapeTextStyle validation, copy, and merge."""

    def test_shape_text_style_validation(self):
        """Test validation and default values of ShapeTextStyle fields."""
        assert asdict(ShapeTextStyle()) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(fill_alpha=0.5)) == {
            "fill_alpha": 0.5,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_color=Colors.Red)) == {
            "fill_alpha": None,
            "text_color": Colors.Red,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_size=20)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": 20,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_halign="left")) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": "left",
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_valign="bottom")) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": "bottom",
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_font=Font.SANSSERIF_BOLD)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": Font.SANSSERIF_BOLD,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_angle=90)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": 90,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_flip=True)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": True,
            "text_xy_shift": None,
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_xy_shift=(10, 10))) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": (10, 10),
            "text_xy_abs_shift": None,
        }
        assert asdict(ShapeTextStyle(text_xy_abs_shift=(10, 10))) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_angle": None,
            "text_flip": None,
            "text_xy_shift": None,
            "text_xy_abs_shift": (10, 10),
        }

        with pytest.raises(ValueError):
            ShapeTextStyle(fill_alpha="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_color="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_size="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_halign="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_valign="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_font="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_angle="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_flip="wrong")
        with pytest.raises(ValueError):
            ShapeTextStyle(text_xy_shift="wrong")

    def test_shape_text_style_copy(self):
        """Test copy() behavior on ShapeTextStyle."""
        style1 = ShapeTextStyle(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_text_style_merge(self):
        """Test merge() behavior on ShapeTextStyle."""
        style1 = ShapeTextStyle(text_color=Colors.Red, text_size=20)
        style2 = ShapeTextStyle(text_font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == ShapeTextStyle(text_color=Colors.Red, text_size=20, text_font=Font.SANSSERIF_BOLD)


class TestTextStyle:
    """Test cases for TextStyle validation, copy, and merge."""

    def test_text_style_validation(self):
        """Test validation and default values of TextStyle fields."""
        assert asdict(TextStyle()) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(fill_alpha=0.5)) == {
            "fill_alpha": 0.5,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_color=Colors.Red)) == {
            "fill_alpha": None,
            "text_color": Colors.Red,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_size=20)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": 20,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_halign="left")) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": "left",
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_valign="bottom")) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": "bottom",
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_font=Font.SANSSERIF_BOLD)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": Font.SANSSERIF_BOLD,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }

        assert asdict(TextStyle(text_bg_fill_alpha=0.5)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": 0.5,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_bg_line_color=Colors.Red)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": Colors.Red,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_bg_line_style="dashed")) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": "dashed",
            "text_bg_line_width": None,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_bg_line_width=2)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": 2,
            "text_bg_fill_color": None,
        }
        assert asdict(TextStyle(text_bg_fill_color=Colors.Red)) == {
            "fill_alpha": None,
            "text_color": None,
            "text_size": None,
            "text_halign": None,
            "text_valign": None,
            "text_font": None,
            "text_bg_fill_alpha": None,
            "text_bg_line_color": None,
            "text_bg_line_style": None,
            "text_bg_line_width": None,
            "text_bg_fill_color": Colors.Red,
        }

        with pytest.raises(ValueError):
            TextStyle(fill_alpha="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_color="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_size="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_halign="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_valign="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_font="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_bg_fill_alpha="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_bg_line_color="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_bg_line_style="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_bg_line_width="wrong")
        with pytest.raises(ValueError):
            TextStyle(text_bg_fill_color="wrong")

    def test_text_style_copy(self):
        """Test copy() behavior on TextStyle."""
        style1 = TextStyle(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_text_style_merge(self):
        """Test merge() behavior on TextStyle."""
        style1 = TextStyle(text_color=Colors.Red, text_size=20)
        style2 = TextStyle(text_font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == TextStyle(text_color=Colors.Red, text_size=20, text_font=Font.SANSSERIF_BOLD)
