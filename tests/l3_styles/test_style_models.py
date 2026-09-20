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
    Style,
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
            Style(extra_field_name="forbidden")

    def test_validate_assignment(self):
        """Test that validation is performed on attribute assignment."""
        style = Style()
        with pytest.raises(ValueError):
            style.icon_style = "wrong"

    def test_merge_type_mismatch(self):
        """Test that merging a style with a mismatched class raises ValueError."""
        style1 = Style()
        with pytest.raises(ValueError):
            style1.merge("invalid_style")


class TestIconStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_icon_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(icon_style="thin")) == {
            "icon_style": "thin",
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(text_color=Colors.Red)) == {
            "icon_style": None,
            "text_color": Colors.Red,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(text_color=(100, 100, 100))) == {
            "icon_style": None,
            "text_color": (100, 100, 100),
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(text_color=(100, 100, 100, 0.5))) == {
            "icon_style": None,
            "text_color": (100, 100, 100, 0.5),
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(fill_alpha=0.5)) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": 0.5,
            "text_halign": None,
            "text_valign": None,
        }
        assert asdict(Style(text_halign="left")) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": "left",
            "text_valign": None,
        }
        assert asdict(Style(text_valign="bottom")) == {
            "icon_style": None,
            "text_color": None,
            "fill_alpha": None,
            "text_halign": None,
            "text_valign": "bottom",
        }

        with pytest.raises(ValueError):
            Style(icon_style="wrong")
        with pytest.raises(ValueError):
            Style(text_color=0.1)
        with pytest.raises(ValueError):
            Style(text_color=(100, 100, 1000))
        with pytest.raises(ValueError):
            Style(text_color=(100, 100, 100, 10))
        with pytest.raises(ValueError):
            Style(text_halign="wrong")
        with pytest.raises(ValueError):
            Style(text_valign="wrong")

    def test_icon_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(icon_style="thin", text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_icon_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(icon_style="thin", text_color=Colors.Red)
        style2 = Style(text_halign="left")
        style3 = style1.merge(style2)

        assert style1 == Style(icon_style="thin", text_color=Colors.Red)
        assert style2 == Style(text_halign="left")
        assert style3 == Style(icon_style="thin", text_color=Colors.Red, text_halign="left")


class TestImageStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_image_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(text_halign="left")) == {
            "text_halign": "left",
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(text_valign="bottom")) == {
            "text_halign": None,
            "text_valign": "bottom",
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(line_width=2)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": 2,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(line_style="dashed")) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": "dashed",
            "line_color": None,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(line_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": Colors.Red,
            "fill_color": None,
            "fill_alpha": None,
        }
        assert asdict(Style(fill_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": Colors.Red,
            "fill_alpha": None,
        }
        assert asdict(Style(fill_alpha=0.3)) == {
            "text_halign": None,
            "text_valign": None,
            "line_width": None,
            "line_style": None,
            "line_color": None,
            "fill_color": None,
            "fill_alpha": 0.3,
        }
        with pytest.raises(ValueError):
            Style(text_halign="wrong")
        with pytest.raises(ValueError):
            Style(text_valign="wrong")
        with pytest.raises(ValueError):
            Style(line_style="wrong")

    def test_image_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(text_halign="left", line_style="dashed", line_width=1)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_image_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(text_halign="left", line_style="dashed", line_width=1)
        style2 = Style(text_valign="bottom")
        style3 = style1.merge(style2)
        assert style3 == Style(text_halign="left", text_valign="bottom", line_style="dashed", line_width=1)


class TestLineStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_line_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
            "line_width": None,
            "line_style": None,
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(Style(line_width=2)) == {
            "line_width": 2,
            "line_style": None,
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(Style(line_style="dashed")) == {
            "line_width": None,
            "line_style": "dashed",
            "text_color": None,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(Style(text_color=Colors.Red)) == {
            "line_width": None,
            "line_style": None,
            "text_color": Colors.Red,
            "fill_alpha": None,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }
        assert asdict(Style(fill_alpha=0.5)) == {
            "line_width": None,
            "line_style": None,
            "text_color": None,
            "fill_alpha": 0.5,
            "arrow_head_scale": None,
            "arrow_head_fill": None,
        }

        with pytest.raises(ValueError):
            Style(line_width="wrong")
        with pytest.raises(ValueError):
            Style(line_style="wrong")
        with pytest.raises(ValueError):
            Style(text_color="wrong")
        with pytest.raises(ValueError):
            Style(fill_alpha="wrong")

    def test_line_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_line_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(text_color=Colors.Red, line_width=2)
        style2 = Style(line_style="dashed")
        style3 = style1.merge(style2)
        assert style3 == Style(text_color=Colors.Red, line_width=2, line_style="dashed")


class TestShapeStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_shape_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(Style(text_halign="left")) == {
            "text_halign": "left",
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(Style(text_valign="bottom")) == {
            "text_halign": None,
            "text_valign": "bottom",
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }

        assert asdict(Style(fill_alpha=0.5)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": 0.5,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(Style(line_width=2)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": 2,
            "line_color": None,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(Style(line_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": Colors.Red,
            "line_style": None,
            "fill_color": None,
        }
        assert asdict(Style(line_style="dashed")) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": "dashed",
            "fill_color": None,
        }
        assert asdict(Style(fill_color=Colors.Red)) == {
            "text_halign": None,
            "text_valign": None,
            "fill_alpha": None,
            "line_width": None,
            "line_color": None,
            "line_style": None,
            "fill_color": Colors.Red,
        }

        with pytest.raises(ValueError):
            Style(text_halign="wrong")
        with pytest.raises(ValueError):
            Style(text_valign="wrong")
        with pytest.raises(ValueError):
            Style(fill_alpha="wrong")
        with pytest.raises(ValueError):
            Style(line_width="wrong")
        with pytest.raises(ValueError):
            Style(line_color="wrong")
        with pytest.raises(ValueError):
            Style(line_style="wrong")
        with pytest.raises(ValueError):
            Style(fill_color="wrong")

    def test_shape_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(line_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(line_color=Colors.Red, line_width=2)
        style2 = Style(fill_color=Colors.Blue)
        style3 = style1.merge(style2)
        assert style3 == Style(line_color=Colors.Red, line_width=2, fill_color=Colors.Blue)


class TestShapeTextStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_shape_text_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
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
        assert asdict(Style(fill_alpha=0.5)) == {
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
        assert asdict(Style(text_color=Colors.Red)) == {
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
        assert asdict(Style(text_size=20)) == {
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
        assert asdict(Style(text_halign="left")) == {
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
        assert asdict(Style(text_valign="bottom")) == {
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
        assert asdict(Style(text_font=Font.SANSSERIF_BOLD)) == {
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
        assert asdict(Style(text_angle=90)) == {
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
        assert asdict(Style(text_flip=True)) == {
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
        assert asdict(Style(text_xy_shift=(10, 10))) == {
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
        assert asdict(Style(text_xy_abs_shift=(10, 10))) == {
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
            Style(fill_alpha="wrong")
        with pytest.raises(ValueError):
            Style(text_color="wrong")
        with pytest.raises(ValueError):
            Style(text_size="wrong")
        with pytest.raises(ValueError):
            Style(text_halign="wrong")
        with pytest.raises(ValueError):
            Style(text_valign="wrong")
        with pytest.raises(ValueError):
            Style(text_font="wrong")
        with pytest.raises(ValueError):
            Style(text_angle="wrong")
        with pytest.raises(ValueError):
            Style(text_flip="wrong")
        with pytest.raises(ValueError):
            Style(text_xy_shift="wrong")

    def test_shape_text_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_shape_text_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(text_color=Colors.Red, text_size=20)
        style2 = Style(text_font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == Style(text_color=Colors.Red, text_size=20, text_font=Font.SANSSERIF_BOLD)


class TestTextStyle:
    """Test cases for Style validation, copy, and merge."""

    def test_text_style_validation(self):
        """Test validation and default values of Style fields."""
        assert asdict(Style()) == {
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
        assert asdict(Style(fill_alpha=0.5)) == {
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
        assert asdict(Style(text_color=Colors.Red)) == {
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
        assert asdict(Style(text_size=20)) == {
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
        assert asdict(Style(text_halign="left")) == {
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
        assert asdict(Style(text_valign="bottom")) == {
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
        assert asdict(Style(text_font=Font.SANSSERIF_BOLD)) == {
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

        assert asdict(Style(text_bg_fill_alpha=0.5)) == {
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
        assert asdict(Style(text_bg_line_color=Colors.Red)) == {
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
        assert asdict(Style(text_bg_line_style="dashed")) == {
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
        assert asdict(Style(text_bg_line_width=2)) == {
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
        assert asdict(Style(text_bg_fill_color=Colors.Red)) == {
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
            Style(fill_alpha="wrong")
        with pytest.raises(ValueError):
            Style(text_color="wrong")
        with pytest.raises(ValueError):
            Style(text_size="wrong")
        with pytest.raises(ValueError):
            Style(text_halign="wrong")
        with pytest.raises(ValueError):
            Style(text_valign="wrong")
        with pytest.raises(ValueError):
            Style(text_font="wrong")
        with pytest.raises(ValueError):
            Style(text_bg_fill_alpha="wrong")
        with pytest.raises(ValueError):
            Style(text_bg_line_color="wrong")
        with pytest.raises(ValueError):
            Style(text_bg_line_style="wrong")
        with pytest.raises(ValueError):
            Style(text_bg_line_width="wrong")
        with pytest.raises(ValueError):
            Style(text_bg_fill_color="wrong")

    def test_text_style_copy(self):
        """Test copy() behavior on Style."""
        style1 = Style(text_color=Colors.Red)
        style2 = style1.copy()

        assert id(style1) != id(style2)
        assert style1 == style2

    def test_text_style_merge(self):
        """Test merge() behavior on Style."""
        style1 = Style(text_color=Colors.Red, text_size=20)
        style2 = Style(text_font=Font.SANSSERIF_BOLD)
        style3 = style1.merge(style2)
        assert style3 == Style(text_color=Colors.Red, text_size=20, text_font=Font.SANSSERIF_BOLD)
