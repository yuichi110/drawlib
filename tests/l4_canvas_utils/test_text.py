# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import os

import pytest
from matplotlib.font_manager import FontProperties

from drawlib._core.l2_models import FontFile
from drawlib._core.l3_fonts import FontSansSerif
from drawlib._core.l3_styles import Colors, ShapeTextStyle, TextStyle
from drawlib._core.l4_canvas_utils._text import TextUtil
from drawlib._theme import get_style


class TestTextUtil:
    """Unit tests for the TextUtil static helper class."""

    def test_format_style(self) -> None:
        """Verifies format_style merges and formats TextStyle and copies attributes."""
        # 1. Test None style
        formatted_none = TextUtil.format_style(None)
        assert isinstance(formatted_none, TextStyle)
        assert formatted_none.text_size == get_style().text_size

        # 2. Test string style lookup
        formatted_str = TextUtil.format_style("primary")
        assert formatted_str.text_color == get_style("primary").text_color

        # 3. Test TextStyle object (deep copied and merged)
        custom_style = TextStyle(text_size=32.0, text_color=(255, 0, 0))
        formatted_obj = TextUtil.format_style(custom_style)
        assert formatted_obj.text_size == 32.0
        assert formatted_obj.text_color == (255, 0, 0)
        assert formatted_obj is not custom_style

        # 4. Invalid types raise ValueError
        with pytest.raises(ValueError):
            TextUtil.format_style(123)  # type: ignore

    def test_get_text_options(self) -> None:
        """Verifies mapping from TextStyle to matplotlib's options dictionary."""
        # 1. Test None style
        assert TextUtil.get_text_options(None) == {}

        # 2. Test mapped values
        style = TextStyle(text_color=(0, 255, 0), text_halign="center", text_valign="top")
        options = TextUtil.get_text_options(style)
        assert options["color"] == (0.0, 1.0, 0.0, 1.0)
        assert options["horizontalalignment"] == "center"
        assert options["verticalalignment"] == "top"

    def test_get_font_properties(self) -> None:
        """Verifies get_font_properties constructs a FontProperties object for custom and default fonts."""
        # 1. Test TextStyle with custom FontFile (referencing an existing file)
        font_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "../../src/drawlib/_assets/fonts/roboto/regular.ttf")
        )
        font_file = FontFile(font_path)
        style_file = TextStyle(text_font=font_file, text_size=18.0)
        props = TextUtil.get_font_properties(style_file)
        assert isinstance(props, FontProperties)
        assert props.get_size() == 18.0
        assert props.get_file() == font_path

        # 2. Test ShapeTextStyle with FontSansSerif
        style_sans = ShapeTextStyle(text_font=FontSansSerif.LATO_REGULAR, text_size=15.0)
        props_sans = TextUtil.get_font_properties(style_sans)
        assert isinstance(props_sans, FontProperties)
        assert props_sans.get_size() == 15.0
        font_file_path = props_sans.get_file()
        assert font_file_path is not None
        if isinstance(font_file_path, bytes):
            font_file_path = font_file_path.decode("utf-8")
        assert "lato" in font_file_path.lower() or "ttf" in font_file_path.lower()

        # 3. Invalid types raise ValueError
        with pytest.raises(ValueError):
            TextUtil.get_font_properties(123)  # type: ignore

        with pytest.raises(ValueError):
            # Font type not supported
            invalid_font_style = TextStyle(text_font=123, text_size=12.0)  # type: ignore
            TextUtil.get_font_properties(invalid_font_style)

    def test_get_bbox_dict(self) -> None:
        """Verifies get_bbox_dict converts TextStyle background properties to bbox options."""
        # 1. Test None style
        assert TextUtil.get_bbox_dict(None) is None

        # 2. Test style with all None background options
        assert TextUtil.get_bbox_dict(TextStyle()) is None

        # 3. Test background options mapping
        style = TextStyle(
            text_bg_fill_color=(255, 0, 0),
            text_bg_line_color=(0, 255, 0),
            text_bg_line_style="dashed",
            text_bg_line_width=2.0,
            text_bg_fill_alpha=0.5,
        )
        bbox = TextUtil.get_bbox_dict(style)
        assert bbox is not None
        assert bbox["boxstyle"] == "square"
        assert bbox["facecolor"] == (1.0, 0.0, 0.0, 1.0)
        assert bbox["edgecolor"] == (0.0, 1.0, 0.0, 1.0)
        assert bbox["linestyle"] == "dashed"
        assert bbox["linewidth"] == 2.0
        assert bbox["alpha"] == 0.5

        # 4. Transparent fallback
        transparent_style = TextStyle(text_bg_fill_color=None, text_bg_line_color=None, text_bg_line_style="solid")
        bbox_trans = TextUtil.get_bbox_dict(transparent_style)
        assert bbox_trans is not None
        assert bbox_trans["facecolor"] == Colors.Transparent
        assert bbox_trans["edgecolor"] == Colors.Transparent
