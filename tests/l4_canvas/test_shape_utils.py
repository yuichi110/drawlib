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

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas._shapes import ShapeUtil


class TestShapeUtil:
    """Unit tests for the ShapeUtil static helper class."""

    def test_format_styles(self) -> None:
        """Verifies format_styles validates shape style and embedded textstyle."""
        shape_s = Style(shape_fill_color=(255, 0, 0), shape_line_color=(0, 0, 0), shape_line_width=1.0)
        text_s = Style(text_color=(0, 0, 0), text_size=12, text_font=Font.SANSSERIF_REGULAR)

        # 1. With textstyle
        s, t = ShapeUtil.format_styles(shape_s, text_s)
        assert s == shape_s
        assert t == text_s

        # 2. Without textstyle (returns None for textstyle)
        s, t = ShapeUtil.format_styles(shape_s, None)
        assert s == shape_s
        assert t is None

        # 3. Unsupported shape style raises ValueError
        with pytest.raises(ValueError, match="Style cannot be used for shape"):
            ShapeUtil.format_styles(Style(shape_fill_color=(255, 0, 0)))

        with pytest.raises(ValueError, match="Style cannot be used for shape"):
            ShapeUtil.validate_shape_style(Style(shape_fill_color=(255, 0, 0)))

        # 4. Invalid types raise TypeError
        with pytest.raises(TypeError):
            ShapeUtil.format_styles("primary")  # type: ignore

    def test_resolve_embedded_text_style(self) -> None:
        """Verifies resolve_embedded_text_style contrast resolution and overrides."""
        # 1. Light shape fill -> dark text
        light_style = Style(
            supports={"shape"},
            shape_fill_color=(240, 240, 240),
            shape_line_color=(0, 0, 0),
            shape_line_width=1.0,
        )
        resolved_light = ShapeUtil.resolve_embedded_text_style(light_style)
        assert resolved_light.supports == frozenset({"text"})
        assert resolved_light.text_color == (40, 40, 40, 1.0)

        # 2. Dark shape fill -> white text
        dark_style = Style(
            supports={"shape"},
            shape_fill_color=(20, 20, 50),
            shape_line_color=(0, 0, 0),
            shape_line_width=1.0,
        )
        resolved_dark = ShapeUtil.resolve_embedded_text_style(dark_style)
        assert resolved_dark.supports == frozenset({"text"})
        assert resolved_dark.text_color == (255, 255, 255, 1.0)

        # 3. Transparent shape -> border color
        trans_style = Style(
            supports={"shape"},
            shape_fill_color=(0, 0, 0, 0.0),
            shape_line_color=(255, 0, 0),
            shape_line_width=1.0,
        )
        resolved_trans = ShapeUtil.resolve_embedded_text_style(trans_style)
        assert resolved_trans.text_color == (255, 0, 0)

        # 4. Explicit textstyle override
        explicit_text = Style(text_color=(0, 255, 0), text_size=20, text_font=Font.SANSSERIF_BOLD)
        resolved_explicit = ShapeUtil.resolve_embedded_text_style(dark_style, textstyle=explicit_text)
        assert resolved_explicit.text_color == (0, 255, 0)
        assert resolved_explicit.text_size == 20

    def test_apply_alignment(self) -> None:
        """Verifies alignment shifting logic for all horizontal and vertical alignment settings."""
        # 1. Angle is None, is_default_center = False (defaults to left/bottom)
        style = Style(text_halign=None, text_valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=False)
        assert updated_style.text_halign == "left"
        assert updated_style.text_valign == "bottom"
        assert xy == (10.0, 20.0)

        # 2. Angle is None, is_default_center = True (defaults to center/center)
        style = Style(text_halign=None, text_valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=True)
        assert updated_style.text_halign == "center"
        assert updated_style.text_valign == "center"
        assert xy == (10.0, 20.0)

        # 3. With angle (always defaults to center/center)
        style = Style(text_halign=None, text_valign=None)
        xy, updated_style = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, 45.0, style, is_default_center=False)
        assert updated_style.text_halign == "center"
        assert updated_style.text_valign == "center"
        # Center-alignment adjustments
        assert xy == (8.0, 17.0)

        # 4. Explicit non-center alignments when is_default_center = False
        style = Style(text_halign="right", text_valign="top")
        xy, _ = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=False)
        assert xy == (6.0, 14.0)

        # 5. Explicit non-center alignments when is_default_center = True
        style = Style(text_halign="left", text_valign="bottom")
        xy, _ = ShapeUtil.apply_alignment((10.0, 20.0), 4.0, 6.0, None, style, is_default_center=True)
        assert xy == (12.0, 23.0)

    def test_get_shape_text(self) -> None:
        """Verifies get_shape_text constructs a matplotlib Text object with rotation and shift offsets."""
        base_style = Style(text_size=12, text_color=(0, 0, 0), text_font=Font.SANSSERIF_REGULAR)

        # 1. Base style
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 30.0, "hello", style=base_style)
        assert isinstance(t_obj, Text)
        assert t_obj.get_text() == "hello"
        assert t_obj.get_rotation() == 30.0

        # 2. With style, custom rotation, flip, and relative xy_shift
        style = base_style.patch(text_angle=45.0, text_flip=True, text_xy_shift=(5.0, 10.0))
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 0.0, "hello", style=style)
        assert t_obj.get_rotation() == 225.0  # (45.0 + 180) % 360
        # shift at angle 0: x + 5, y + 10
        assert t_obj.get_position() == (55.0, 60.0)

        # 3. Test absolute shift
        abs_style = base_style.patch(text_xy_abs_shift=(3.0, -3.0))
        t_obj = ShapeUtil.get_shape_text((50.0, 50.0), 0.0, "hello", style=abs_style)
        assert t_obj.get_position() == (53.0, 47.0)

    def test_get_shape_options(self) -> None:
        """Verifies get_shape_options maps Style fields to matplotlib patch dictionary format."""
        style = Style(
            shape_line_width=2.5,
            shape_line_style="dashed",
            shape_line_color=(255, 0, 0),
            shape_fill_color=(0, 255, 0, 0.5),
            shape_fill_alpha=0.8,
        )
        options = ShapeUtil.get_shape_options(style)
        assert options["linewidth"] == 2.5
        assert options["linestyle"] == "dashed"
        assert options["edgecolor"] == (1.0, 0.0, 0.0, 1.0)
        assert options["facecolor"] == (0.0, 1.0, 0.0, 0.5)
        assert options["alpha"] == 0.8
