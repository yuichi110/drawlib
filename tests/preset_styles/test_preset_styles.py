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
    BaseStyles,
    DefaultStyles,
    MonochromeStyles,
    default_styles,
    google_styles,
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
        assert isinstance(default_styles, BaseStyles)
        assert isinstance(monochrome_styles, MonochromeStyles)
        assert isinstance(monochrome_styles, BaseStyles)
        assert not hasattr(preset_styles, "ThemePreset")
        assert not hasattr(preset_styles, "PresetStyles")

    def test_preset_style_attributes(self) -> None:
        """Verifies BaseStyles provides required style attributes."""
        styles = default_styles
        assert isinstance(styles.primary, Style)
        assert isinstance(styles.light, Style)
        assert isinstance(styles.bold, Style)
        assert isinstance(styles.flat, Style)
        assert isinstance(styles.solid, Style)
        assert isinstance(styles.dashed, Style)

    def test_semantic_roles_10_variants(self) -> None:
        """Verifies 4 core semantic roles provide all 10 orthogonal variants with proper supports."""
        roles = ["primary", "secondary", "accent", "muted"]
        presets = [default_styles, monochrome_styles]
        for st in presets:
            for role in roles:
                bordered = getattr(st, role)
                assert getattr(st, f"{role}_bordered") == bordered
                assert bordered.supports == frozenset({"shape", "line", "text", "icon"})

                bold = getattr(st, f"{role}_bold")
                assert bold.supports == frozenset({"shape", "line", "text", "icon"})

                light = getattr(st, f"{role}_light")
                assert light.supports == frozenset({"shape", "line", "text", "icon"})

                flat = getattr(st, f"{role}_flat")
                assert flat.supports == frozenset({"shape"})

                outline = getattr(st, f"{role}_outline")
                assert outline.supports == frozenset({"shape", "line"})

                outline_bold = getattr(st, f"{role}_outline_bold")
                assert outline_bold.supports == frozenset({"shape", "line"})

                outline_light = getattr(st, f"{role}_outline_light")
                assert outline_light.supports == frozenset({"shape", "line"})

                dashed = getattr(st, f"{role}_dashed")
                assert dashed.supports == frozenset({"shape", "line"})

                dashed_bold = getattr(st, f"{role}_dashed_bold")
                assert dashed_bold.supports == frozenset({"shape", "line"})

                dashed_light = getattr(st, f"{role}_dashed_light")
                assert dashed_light.supports == frozenset({"shape", "line"})

    def test_palette_colors_10_variants(self) -> None:
        """Verifies palette colors provide 10 variants with accurate supports declaration."""
        colors = ["red", "blue", "green", "white", "black"]
        for c in colors:
            normal = getattr(default_styles, c)
            assert getattr(default_styles, f"{c}_bordered") == normal
            assert normal.supports == frozenset({"shape", "line", "text", "icon"})

            flat = getattr(default_styles, f"{c}_flat")
            assert flat.supports == frozenset({"shape"})

            outline = getattr(default_styles, f"{c}_outline")
            assert outline.supports == frozenset({"shape", "line"})
            assert getattr(default_styles, f"{c}_solid") == outline

            dashed = getattr(default_styles, f"{c}_dashed")
            assert dashed.supports == frozenset({"shape", "line"})

    def test_semantic_danger_success(self) -> None:
        """Verifies danger and success semantic roles on DefaultStyles and GoogleStyles."""
        for st in [default_styles, google_styles]:
            for role in ["danger", "success"]:
                bordered = getattr(st, role)
                assert isinstance(bordered, Style)
                assert getattr(st, f"{role}_bordered") == bordered
                assert bordered.supports == frozenset({"shape", "line", "text", "icon"})

                bold = getattr(st, f"{role}_bold")
                assert isinstance(bold, Style)
                assert bold.supports == frozenset({"shape", "line", "text", "icon"})

                light = getattr(st, f"{role}_light")
                assert isinstance(light, Style)
                assert light.supports == frozenset({"shape", "line", "text", "icon"})

                flat = getattr(st, f"{role}_flat")
                assert isinstance(flat, Style)
                assert flat.supports == frozenset({"shape"})

                outline = getattr(st, f"{role}_outline")
                assert isinstance(outline, Style)
                assert outline.supports == frozenset({"shape", "line"})
                assert getattr(st, f"{role}_solid") == outline

                outline_bold = getattr(st, f"{role}_outline_bold")
                assert isinstance(outline_bold, Style)
                assert outline_bold.supports == frozenset({"shape", "line"})

                outline_light = getattr(st, f"{role}_outline_light")
                assert isinstance(outline_light, Style)
                assert outline_light.supports == frozenset({"shape", "line"})

                dashed = getattr(st, f"{role}_dashed")
                assert isinstance(dashed, Style)
                assert dashed.supports == frozenset({"shape", "line"})

                dashed_bold = getattr(st, f"{role}_dashed_bold")
                assert isinstance(dashed_bold, Style)
                assert dashed_bold.supports == frozenset({"shape", "line"})

                dashed_light = getattr(st, f"{role}_dashed_light")
                assert isinstance(dashed_light, Style)
                assert dashed_light.supports == frozenset({"shape", "line"})

    def test_monochrome_danger_success_unsupported(self) -> None:
        """Verifies MonochromeStyles raises AttributeError for unsupported danger and success."""
        for role in ["danger", "success"]:
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, role)
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, f"{role}_flat")
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, f"{role}_outline")
            with pytest.raises(KeyError):
                _ = monochrome_styles[role]

        assert "danger" not in monochrome_styles.styles()
        assert "success" not in monochrome_styles.styles()

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
        assert new_styles.light.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.primary_light.text_font == FontJapanese.SANSSERIF_LIGHT
        assert new_styles.light_light.text_font == FontJapanese.SANSSERIF_LIGHT

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
        assert new_styles.light.text_font == Font.SANSSERIF_REGULAR
        assert new_styles.primary_light.text_font == Font.SANSSERIF_LIGHT
        assert new_styles.light_light.text_font == Font.SANSSERIF_LIGHT

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
