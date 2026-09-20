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
    Style,
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
        assert isinstance(SYSTEM_DEFAULT_ICON_STYLE, Style)
        assert isinstance(SYSTEM_DEFAULT_IMAGE_STYLE, Style)
        assert isinstance(SYSTEM_DEFAULT_LINE_STYLE, Style)
        assert isinstance(SYSTEM_DEFAULT_SHAPE_STYLE, Style)
        assert isinstance(SYSTEM_DEFAULT_SHAPE_TEXT_STYLE, Style)
        assert isinstance(SYSTEM_DEFAULT_TEXT_STYLE, Style)

    def test_system_default_styles_values(self):
        """Test specific default attribute values of system defaults."""
        # Style default values
        assert SYSTEM_DEFAULT_ICON_STYLE.icon_style == "thin"
        assert SYSTEM_DEFAULT_ICON_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_ICON_STYLE.text_halign == "center"

        # Style default values
        assert SYSTEM_DEFAULT_IMAGE_STYLE.text_halign == "center"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.text_valign == "center"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.line_style == "solid"
        assert SYSTEM_DEFAULT_IMAGE_STYLE.line_width == 0

        # Style default values
        assert SYSTEM_DEFAULT_LINE_STYLE.line_width == 1.0
        assert SYSTEM_DEFAULT_LINE_STYLE.line_color == Colors.Black
        assert SYSTEM_DEFAULT_LINE_STYLE.line_style == "solid"

        # Style default values
        assert SYSTEM_DEFAULT_SHAPE_STYLE.text_halign == "center"
        assert SYSTEM_DEFAULT_SHAPE_STYLE.line_width == 1.0
        assert SYSTEM_DEFAULT_SHAPE_STYLE.fill_color == Colors.White

        # Style default values
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_size == 16
        assert SYSTEM_DEFAULT_SHAPE_TEXT_STYLE.text_font == Font.SANSSERIF_REGULAR

        # Style default values
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_color == Colors.Black
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_size == 16
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_font == Font.SANSSERIF_REGULAR
        assert SYSTEM_DEFAULT_TEXT_STYLE.text_bg_line_color == Colors.Black
