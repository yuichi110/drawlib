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
    default_styles,
    essentials_styles,
    monochrome_styles,
)
from drawlib.canvas import save
from drawlib.fonts import Font, FontJapanese, FontRoboto, FontSourceCode
from drawlib.images import image
from drawlib.shapes import circle
from drawlib.types import Style

IMAGE_FILE = "../assets/image.png"
OUTPUT_DIR_DEFAULT = "../../output_tests/preset_styles/default/"


class TestPresetStylesUnit:
    """Unit tests for preset style singletons."""

    def test_preset_styles(self) -> None:
        """Verifies official preset style singletons are valid instances."""
        assert isinstance(default_styles, DefaultStyles)
        assert isinstance(default_styles, PresetStyles)
        assert isinstance(essentials_styles, EssentialsStyles)
        assert isinstance(essentials_styles, PresetStyles)
        assert isinstance(monochrome_styles, MonochromeStyles)
        assert isinstance(monochrome_styles, PresetStyles)
        assert not hasattr(preset_styles, "ThemePreset")

    def test_preset_style_attributes(self) -> None:
        """Verifies PresetStyles provides required style attributes."""
        styles = default_styles
        assert isinstance(styles.primary, Style)
        assert isinstance(styles.light, Style)
        assert isinstance(styles.bold, Style)
        assert isinstance(styles.flat, Style)
        assert isinstance(styles.solid, Style)
        assert isinstance(styles.dashed, Style)

    def test_preset_styles_immutability(self) -> None:
        """Verifies that preset style singletons are frozen and immutable."""
        with pytest.raises(Exception):
            setattr(default_styles, "primary", default_styles.bold)

    def test_preset_styles_patch(self) -> None:
        """Verifies that preset styles can be patched without mutating the original."""
        original_primary = default_styles.primary
        new_style = default_styles.patch(primary=default_styles.bold)
        assert new_style.primary == default_styles.bold
        assert default_styles.primary == original_primary

    def test_preset_styles_patch_font_regular_only(self) -> None:
        """Verifies that patch_font with regular applies font to all styles as fallback."""
        original_font = default_styles.primary.text_font
        new_styles = default_styles.patch_font(regular=FontJapanese.SANSSERIF_REGULAR)

        # Base styles
        assert new_styles.primary.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.blue.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.blue_flat.text_font == FontJapanese.SANSSERIF_REGULAR

        # Bold and light fallback to regular when not explicitly overridden
        assert new_styles.bold.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.blue_bold.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.light.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.blue_light.text_font == FontJapanese.SANSSERIF_REGULAR

        # Original styles remain unchanged
        assert default_styles.primary.text_font == original_font
        assert default_styles.bold.text_font == Font.SANSSERIF_BOLD

    def test_preset_styles_patch_font_regular_and_variants(self) -> None:
        """Verifies that patch_font overrides bold and light styles specifically."""
        new_styles = default_styles.patch_font(
            regular=FontJapanese.SANSSERIF_REGULAR,
            bold=FontJapanese.SANSSERIF_BOLD,
            light=FontJapanese.SANSSERIF_LIGHT,
        )

        # Base styles
        assert new_styles.primary.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.blue.text_font == FontJapanese.SANSSERIF_REGULAR

        # Bold styles
        assert new_styles.bold.text_font == FontJapanese.SANSSERIF_BOLD
        assert new_styles.blue_bold.text_font == FontJapanese.SANSSERIF_BOLD

        # Light styles
        assert new_styles.light.text_font == FontJapanese.SANSSERIF_LIGHT
        assert new_styles.blue_light.text_font == FontJapanese.SANSSERIF_LIGHT

    def test_preset_styles_patch_font_bold_only(self) -> None:
        """Verifies that patching only bold modifies bold styles while preserving others."""
        new_styles = default_styles.patch_font(bold=FontRoboto.ROBOTO_BOLD)

        # Base styles remain default
        assert new_styles.primary.text_font == Font.SANSSERIF_REGULAR
        assert new_styles.blue.text_font == Font.SANSSERIF_REGULAR

        # Bold styles are updated
        assert new_styles.bold.text_font == FontRoboto.ROBOTO_BOLD
        assert new_styles.blue_bold.text_font == FontRoboto.ROBOTO_BOLD

        # Light styles remain default
        assert new_styles.light.text_font == Font.SANSSERIF_LIGHT

    def test_preset_styles_patch_font_sourcecode(self) -> None:
        """Verifies that sourcecode_font is updated properly."""
        original_code_font = default_styles.sourcecode_font
        new_styles = default_styles.patch_font(sourcecode=FontSourceCode.ROBOTO_MONO)

        assert new_styles.sourcecode_font == FontSourceCode.ROBOTO_MONO
        assert default_styles.sourcecode_font == original_code_font


def test_default_fill() -> None:
    """Integrated drawing test for default circles fill."""
    styles = default_styles
    circle((25, 25), 10, style=styles.primary, text="drawlib")
    circle((25, 50), 10, style=styles.light, text="drawlib")
    circle((25, 75), 10, style=styles.bold, text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill.png")


@pytest.mark.image_threshold(93.0)
def test_default_style_images() -> None:
    """Integrated drawing test for default image styles."""
    styles = default_styles
    image((25, 25), 20, style=styles.flat, image=IMAGE_FILE)
    image((25, 50), 20, style=styles.solid, image=IMAGE_FILE)
    image((25, 75), 20, style=styles.dashed, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_style_images.png")
