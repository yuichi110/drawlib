# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit tests for the IconUtil class and formatting helper methods."""

import pytest

from drawlib._core.l2_models import StaticContainer
from drawlib._core.l3_styles import IconStyle
from drawlib._icons._utils import IconUtil


class TestIconUtils:
    """Tests for the IconUtil class and style formatting helper methods."""

    def test_static_container_subclass(self) -> None:
        """Verify that IconUtil inherits from StaticContainer."""
        assert issubclass(IconUtil, StaticContainer)

    def test_static_container_instantiation_raises_type_error(self) -> None:
        """Verify that instantiating IconUtil directly raises a TypeError."""
        with pytest.raises(TypeError):
            IconUtil()

    def test_format_style_none(self) -> None:
        """Verify format_style returns the merged default style when input style is None."""
        formatted = IconUtil.format_style(None)
        assert isinstance(formatted, IconStyle)

    def test_format_style_string(self) -> None:
        """Verify format_style formats from a named string registered in the active theme."""
        # Using "blue" as a standard registered theme style key
        formatted = IconUtil.format_style("blue")
        assert isinstance(formatted, IconStyle)

    def test_format_style_object(self) -> None:
        """Verify format_style retains properties and merges custom IconStyle instances."""
        custom_style = IconStyle(text_color=(255, 0, 0), text_halign="center")
        formatted = IconUtil.format_style(custom_style)
        assert formatted.text_color == (255, 0, 0)
        assert formatted.text_halign == "center"

    def test_format_style_invalid_type_raises_value_error(self) -> None:
        """Verify that passing an invalid style type raises a ValueError."""
        with pytest.raises(ValueError):
            IconUtil.format_style(12345)  # type: ignore

    def test_format_style_invalid_default_style_type_raises_value_error(self) -> None:
        """Verify that passing an invalid default style name type raises a ValueError."""
        with pytest.raises(ValueError):
            IconUtil.format_style(None, default_icon_style=123)  # type: ignore
