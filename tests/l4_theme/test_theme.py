# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._theme import (
    ThemePreset,
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
    get_style,
    get_styles,
)
from drawlib.canvas import save
from drawlib.images import image
from drawlib.shapes import circle
from drawlib.types import Style

IMAGE_FILE = "../assets/image.png"
OUTPUT_DIR_DEFAULT = "../../output_tests/l4_theme/default/"


class TestThemeUnit:
    """Unit tests for theme presets and get_styles."""

    def test_theme_presets(self) -> None:
        """Verifies get_styles returns valid ThemePreset objects."""
        default = get_styles("default")
        essentials = get_styles("essentials")
        monochrome = get_styles("monochrome")

        assert isinstance(default, ThemePreset)
        assert isinstance(essentials, ThemePreset)
        assert isinstance(monochrome, ThemePreset)
        assert get_default_styles() == default
        assert get_essentials_styles() == essentials
        assert get_monochrome_styles() == monochrome

    def test_get_style_resolution(self) -> None:
        """Verifies get_style resolves None, Style instance, and string preset names."""
        st = get_style(None)
        assert isinstance(st, Style)

        custom_st = Style(fill_color=(255, 0, 0, 1.0))
        assert get_style(custom_st) == custom_st

        assert isinstance(get_style("primary"), Style)
        assert isinstance(get_style("light"), Style)
        assert isinstance(get_style("bold"), Style)
        assert isinstance(get_style("flat"), Style)
        assert isinstance(get_style("solid"), Style)
        assert isinstance(get_style("dashed"), Style)

    def test_invalid_theme_name(self) -> None:
        """Verifies get_styles raises ValueError for invalid theme name."""
        with pytest.raises(ValueError, match="is not supported"):
            get_styles("invalid_theme")  # type: ignore


def test_default_fill() -> None:
    """Integrated drawing test for default circles fill."""
    theme = get_default_styles()
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style=theme.light, text="drawlib")
    circle((25, 75), 10, style=theme.bold, text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill.png")


def test_default_style_images() -> None:
    """Integrated drawing test for default image styles."""
    theme = get_default_styles()
    image((25, 25), 20, style=theme.flat, image=IMAGE_FILE)
    image((25, 50), 20, style=theme.solid, image=IMAGE_FILE)
    image((25, 75), 20, style=theme.dashed, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_style_images.png")
