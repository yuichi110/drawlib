# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib import preset_styles
from drawlib._preset_styles import (
    DefaultStyles,
    EssentialsStyles,
    MonochromeStyles,
    PresetStyles,
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
    get_styles,
)
from drawlib.canvas import save
from drawlib.images import image
from drawlib.shapes import circle
from drawlib.types import Style

IMAGE_FILE = "../assets/image.png"
OUTPUT_DIR_DEFAULT = "../../output_tests/preset_styles/default/"


class TestPresetStylesUnit:
    """Unit tests for preset styles and get_styles."""

    def test_preset_styles(self) -> None:
        """Verifies get_styles returns valid PresetStyles objects."""
        default = get_styles("default")
        essentials = get_styles("essentials")
        monochrome = get_styles("monochrome")

        assert isinstance(default, DefaultStyles)
        assert isinstance(default, PresetStyles)
        assert isinstance(essentials, EssentialsStyles)
        assert isinstance(essentials, PresetStyles)
        assert isinstance(monochrome, MonochromeStyles)
        assert isinstance(monochrome, PresetStyles)
        assert get_default_styles() == default
        assert get_essentials_styles() == essentials
        assert get_monochrome_styles() == monochrome
        assert not hasattr(preset_styles, "ThemePreset")

    def test_preset_style_attributes(self) -> None:
        """Verifies PresetStyles provides required style attributes."""
        styles = get_default_styles()
        assert isinstance(styles.primary, Style)
        assert isinstance(styles.light, Style)
        assert isinstance(styles.bold, Style)
        assert isinstance(styles.flat, Style)
        assert isinstance(styles.solid, Style)
        assert isinstance(styles.dashed, Style)

    def test_invalid_style_name(self) -> None:
        """Verifies get_styles raises ValueError for invalid style name."""
        with pytest.raises(ValueError, match="is not supported"):
            get_styles("invalid_style")


def test_default_fill() -> None:
    """Integrated drawing test for default circles fill."""
    styles = get_default_styles()
    circle((25, 25), 10, style=styles.primary, text="drawlib")
    circle((25, 50), 10, style=styles.light, text="drawlib")
    circle((25, 75), 10, style=styles.bold, text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill.png")


def test_default_style_images() -> None:
    """Integrated drawing test for default image styles."""
    styles = get_default_styles()
    image((25, 25), 20, style=styles.flat, image=IMAGE_FILE)
    image((25, 50), 20, style=styles.solid, image=IMAGE_FILE)
    image((25, 75), 20, style=styles.dashed, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_style_images.png")
