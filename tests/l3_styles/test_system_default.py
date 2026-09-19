# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the system default styles module in l3_styles."""

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
from drawlib._core.l3_styles._system_default import (
    SYSTEM_DEFAULT_ICON_STYLE,
    SYSTEM_DEFAULT_IMAGE_STYLE,
    SYSTEM_DEFAULT_LINE_STYLE,
    SYSTEM_DEFAULT_SHAPE_STYLE,
    SYSTEM_DEFAULT_SHAPE_TEXT_STYLE,
    SYSTEM_DEFAULT_TEXT_STYLE,
)


class TestSystemDefaults:
    """Test cases for system default style instances."""

    def test_system_default_styles(self):
        """Test that default style constants are instances of the correct class."""
        assert isinstance(SYSTEM_DEFAULT_ICON_STYLE, IconStyle)
        assert isinstance(SYSTEM_DEFAULT_IMAGE_STYLE, ImageStyle)
        assert isinstance(SYSTEM_DEFAULT_LINE_STYLE, LineStyle)
        assert isinstance(SYSTEM_DEFAULT_SHAPE_STYLE, ShapeStyle)
        assert isinstance(SYSTEM_DEFAULT_SHAPE_TEXT_STYLE, ShapeTextStyle)
        assert isinstance(SYSTEM_DEFAULT_TEXT_STYLE, TextStyle)

    def test_system_default_styles_values(self):
        """Test specific default attribute values of system defaults."""
        # IconStyle default values
        assert SYSTEM_DEFAULT_ICON_STYLE.icon_style == "thin"
        assert SYSTEM_DEFAULT_ICON_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_ICON_STYLE.text_halign == "center"

        # ImageStyle default values
        assert SYSTEM_DEFAULT_IMAGE_STYLE.text_halign == "center"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.text_valign == "center"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.line_style == "solid"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.line_width == 0

        # LineStyle default values
        assert SYSTEM_DEFAULT_LINE_STYLE.line_width == 1.0
        assert SYSTEM_DEFAULT_LINE_STYLE.line_color == Colors.Black
        assert SYSTEM_DEFAULT_LINE_STYLE.line_style == "solid"

        # ShapeStyle default values
        assert SYSTEM_DEFAULT_SHAPE_STYLE.text_halign == "center"
        assert SYSTEM_DEFAULT_SHAPE_STYLE.line_width == 1.0
        assert SYSTEM_DEFAULT_SHAPE_STYLE.fill_color == Colors.White

        # ShapeTextStyle default values
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_size == 16
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_font == Font.SANSSERIF_REGULAR

        # TextStyle default values
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_size == 16
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_font == Font.SANSSERIF_REGULAR
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_bg_line_color == Colors.Black
