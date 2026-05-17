# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

# pyright: reportUnknownMemberType=false
import pytest
from matplotlib.text import Text

from drawlib.v0_2.private.l3_styles import ShapeStyle, ShapeTextStyle
from drawlib.v0_2.private.l4_theme import dtheme
from drawlib.v0_2.private.l5_canvas_utils._shape import ShapeUtil


class TestShapeUtil:
    """Unit tests for the ShapeUtil static helper class."""

    def test_format_styles(self) -> None:
        """Verifies format_styles retrieves and merges both shape and text styles, and handles callbacks."""
        dtheme.apply_official_theme("default")

        def get_shape_style(name: str = "") -> ShapeStyle:
            if name == "custom_shape":
                return ShapeStyle(lwidth=15.0)
            return ShapeStyle(lwidth=5.0)

        def get_text_style(name: str = "") -> ShapeTextStyle:
            if name == "custom_text":
                return ShapeTextStyle(size=40)
            return ShapeTextStyle(size=20)

        # 1. Test None styles
        style, textstyle = ShapeUtil.format_styles(None, None, get_shape_style, get_text_style)
        assert style.lwidth == 5.0
        assert textstyle.size == 20

        # 2. Test string lookup
        style, textstyle = ShapeUtil.format_styles("custom_shape", "custom_text", get_shape_style, get_text_style)
        assert style.lwidth == 15.0
        assert textstyle.size == 40

        # 3. Test direct style objects (copied and merged)
        custom_s = ShapeStyle(lwidth=25.0)
        custom_t = ShapeTextStyle(size=50)
        style, textstyle = ShapeUtil.format_styles(custom_s, custom_t, get_shape_style, get_text_style)
        assert style.lwidth == 25.0
        assert textstyle.size == 50
        assert style is not custom_s
        assert textstyle is not custom_t

        # 4. Invalid types raise ValueError
        with pytest.raises(ValueError):
            ShapeUtil.format_styles(123, None, get_shape_style, get_text_style)  # type: ignore

        with pytest.raises(ValueError):
            ShapeUtil.format_styles(None, 123, get_shape_style, get_text_style)  # type: ignore

    def test_apply_alignment(self) -> None:
        """Verifies alignment shifting logic for all horizontal and vertical alignment settings."""
        # 1. Angle is None, is_default_center = False (defaults to left/bottom)
        style = ShapeStyle(halign=None, valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=False)
        assert updated_style.halign == "left"
        assert updated_style.valign == "bottom"
        assert xy == (10.0, 20.0)

        # 2. Angle is None, is_default_center = True (defaults to center/center)
        style = ShapeStyle(halign=None, valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=True)
        assert updated_style.halign == "center"
        assert updated_style.valign == "center"
        assert xy == (10.0, 20.0)

        # 3. With angle (always defaults to center/center)
        style = ShapeStyle(halign=None, valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, 45.0, style, is_default_center=False)
        assert updated_style.halign == "center"
        assert updated_style.valign == "center"
        # Center-alignment adjustments
        assert xy == (8.0, 17.0)

        # 4. Explicit non-center alignments when is_default_center = False
        style = ShapeStyle(halign="right", valign="top")
        xy, _ = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=False)
        assert xy == (6.0, 14.0)

        # 5. Explicit non-center alignments when is_default_center = True
        style = ShapeStyle(halign="left", valign="bottom")
        xy, _ = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=True)
        assert xy == (12.0, 23.0)

    def test_get_shape_text(self) -> None:
        """Verifies get_shape_text constructs a matplotlib Text object with rotation and shift offsets."""
        dtheme.apply_official_theme("default")

        # 1. Without style
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 30.0, "hello")
        assert isinstance(t_obj, Text)
        assert t_obj.get_text() == "hello"
        assert t_obj.get_rotation() == 30.0

        # 2. With style, custom rotation, flip, and relative xy_shift
        style = ShapeTextStyle(size=12, angle=45.0, flip=True, xy_shift=(5.0, 10.0))
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 0.0, "hello", style=style)
        assert t_obj.get_rotation() == 225.0  # (45.0 + 180) % 360
        # shift at angle 0: x + 5, y + 10
        assert t_obj.get_position() == (55.0, 60.0)

        # 3. Test absolute shift
        abs_style = ShapeTextStyle(xy_abs_shift=(3.0, -3.0))
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 0.0, "hello", style=abs_style)
        assert t_obj.get_position() == (53.0, 47.0)

    def test_get_shape_options(self) -> None:
        """Verifies get_shape_options maps ShapeStyle fields to matplotlib patch dictionary format."""
        # 1. Test None style
        assert ShapeUtil.get_shape_options(None, default_no_line=True) == {"linewidth": 0}
        assert ShapeUtil.get_shape_options(None, default_no_line=False) == {}

        # 2. Test mapped options
        style = ShapeStyle(lwidth=2.5, lstyle="dashed", lcolor=(255, 0, 0), fcolor=(0, 255, 0, 0.5), alpha=0.8)
        options = ShapeUtil.get_shape_options(style)
        assert options["linewidth"] == 2.5
        assert options["linestyle"] == "dashed"
        assert options["edgecolor"] == (1.0, 0.0, 0.0, 1.0)
        assert options["facecolor"] == (0.0, 1.0, 0.0, 0.5)
        assert options["alpha"] == 0.8
