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
from drawlib._core.l3_styles import Style
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

    def test_format_style_none_raises_type_error(self) -> None:
        """Verify format_style raises TypeError when input style is None."""
        with pytest.raises(TypeError):
            IconUtil.format_style(None)  # type: ignore

    def test_format_style_string_raises_type_error(self) -> None:
        """Verify format_style raises TypeError when input style is a string."""
        with pytest.raises(TypeError):
            IconUtil.format_style("blue")  # type: ignore

    def test_format_style_object(self) -> None:
        """Verify format_style retains properties and applies default_icon_style."""
        custom_style = Style(icon_color=(255, 0, 0))
        formatted = IconUtil.format_style(custom_style, default_icon_style="light")
        assert formatted.icon_color == (255, 0, 0, 1.0)
        assert formatted.icon_style == "light"

    def test_format_style_missing_icon_color_raises_value_error(self) -> None:
        """Verify that style missing icon_color raises ValueError."""
        with pytest.raises(ValueError, match="Icon drawing requires attribute 'icon_color'"):
            IconUtil.format_style(Style())

    def test_format_style_invalid_type_raises_type_error(self) -> None:
        """Verify that passing an invalid style type raises a TypeError."""
        with pytest.raises(TypeError):
            IconUtil.format_style(12345)  # type: ignore
