# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest
from pydantic import ValidationError

from drawlib import preset_styles
from drawlib._core.l3_styles import DEFAULT_FONT, DEFAULT_TEXT_SIZE
from drawlib._preset_styles import (
    BaseStyles,
    DefaultStyles,
    GoogleStyles,
    MonochromeStyles,
)
from drawlib.canvas import save
from drawlib.fonts import Font, FontJapanese, FontRoboto, FontSourceCode
from drawlib.images import image
from drawlib.shapes import circle
from drawlib.types import Style

_ds_inst = DefaultStyles.get_default_instance()
assert isinstance(_ds_inst, DefaultStyles)
default_styles = _ds_inst

_gs_inst = GoogleStyles.get_default_instance()
assert isinstance(_gs_inst, GoogleStyles)
google_styles = _gs_inst

_ms_inst = MonochromeStyles.get_default_instance()
assert isinstance(_ms_inst, MonochromeStyles)
monochrome_styles = _ms_inst

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
        assert isinstance(styles.Primary, Style)
        assert isinstance(styles.PrimaryThin, Style)
        assert isinstance(styles.PrimaryBold, Style)
        assert isinstance(styles.PrimaryFlat, Style)
        assert isinstance(styles.PrimarySolid, Style)
        assert isinstance(styles.PrimaryDashed, Style)

    def test_semantic_roles_10_variants(self) -> None:
        """Verifies 4 core semantic roles provide all 10 orthogonal variants with proper supports."""
        roles = ["Primary", "Secondary", "Accent", "Muted"]
        presets = [default_styles, monochrome_styles]
        for st in presets:
            for role in roles:
                bordered = getattr(st, role)
                assert getattr(st, f"{role}Bordered") == bordered
                assert bordered.supports == frozenset({"shape", "line", "text", "icon"})

                bold = getattr(st, f"{role}Bold")
                assert bold.supports == frozenset({"shape", "line", "text", "icon"})

                thin = getattr(st, f"{role}Thin")
                assert thin.supports == frozenset({"shape", "line", "text", "icon"})

                flat = getattr(st, f"{role}Flat")
                assert flat.supports == frozenset({"shape", "icon"})

                outline = getattr(st, f"{role}Outline")
                assert outline.supports == frozenset({"shape", "line"})

                outline_bold = getattr(st, f"{role}OutlineBold")
                assert outline_bold.supports == frozenset({"shape", "line"})

                outline_thin = getattr(st, f"{role}OutlineThin")
                assert outline_thin.supports == frozenset({"shape", "line"})

                dashed = getattr(st, f"{role}Dashed")
                assert dashed.supports == frozenset({"shape", "line"})

                dashed_bold = getattr(st, f"{role}DashedBold")
                assert dashed_bold.supports == frozenset({"shape", "line"})

                dashed_thin = getattr(st, f"{role}DashedThin")
                assert dashed_thin.supports == frozenset({"shape", "line"})

    def test_palette_colors_10_variants(self) -> None:
        """Verifies palette colors provide 10 variants with accurate supports declaration."""
        colors = ["Red", "Blue", "Green", "White", "Black"]
        for c in colors:
            normal = getattr(default_styles, c)
            assert getattr(default_styles, f"{c}Bordered") == normal
            assert normal.supports == frozenset({"shape", "line", "text", "icon"})

            flat = getattr(default_styles, f"{c}Flat")
            assert flat.supports == frozenset({"shape", "icon"})

            outline = getattr(default_styles, f"{c}Outline")
            assert outline.supports == frozenset({"shape", "line"})
            assert getattr(default_styles, f"{c}Solid") == outline

            dashed = getattr(default_styles, f"{c}Dashed")
            assert dashed.supports == frozenset({"shape", "line"})

    def test_semantic_danger_success(self) -> None:
        """Verifies danger and success semantic roles on DefaultStyles and GoogleStyles."""
        for st in [default_styles, google_styles]:
            for role in ["Danger", "Success"]:
                bordered = getattr(st, role)
                assert isinstance(bordered, Style)
                assert getattr(st, f"{role}Bordered") == bordered
                assert bordered.supports == frozenset({"shape", "line", "text", "icon"})

                bold = getattr(st, f"{role}Bold")
                assert isinstance(bold, Style)
                assert bold.supports == frozenset({"shape", "line", "text", "icon"})

                thin = getattr(st, f"{role}Thin")
                assert isinstance(thin, Style)
                assert thin.supports == frozenset({"shape", "line", "text", "icon"})

                flat = getattr(st, f"{role}Flat")
                assert isinstance(flat, Style)
                assert flat.supports == frozenset({"shape", "icon"})

                outline = getattr(st, f"{role}Outline")
                assert isinstance(outline, Style)
                assert outline.supports == frozenset({"shape", "line"})
                assert getattr(st, f"{role}Solid") == outline

                outline_bold = getattr(st, f"{role}OutlineBold")
                assert isinstance(outline_bold, Style)
                assert outline_bold.supports == frozenset({"shape", "line"})

                outline_thin = getattr(st, f"{role}OutlineThin")
                assert isinstance(outline_thin, Style)
                assert outline_thin.supports == frozenset({"shape", "line"})

                dashed = getattr(st, f"{role}Dashed")
                assert isinstance(dashed, Style)
                assert dashed.supports == frozenset({"shape", "line"})

                dashed_bold = getattr(st, f"{role}DashedBold")
                assert isinstance(dashed_bold, Style)
                assert dashed_bold.supports == frozenset({"shape", "line"})

                dashed_thin = getattr(st, f"{role}DashedThin")
                assert isinstance(dashed_thin, Style)
                assert dashed_thin.supports == frozenset({"shape", "line"})

    def test_neutral_styles(self) -> None:
        """Verifies Neutral and tinted neutral card styles across presets."""
        presets = [default_styles, google_styles, monochrome_styles]
        for st in presets:
            # Base Neutral and aliases
            assert isinstance(st.Neutral, Style)
            assert isinstance(st.NeutralFlat, Style)
            assert isinstance(st.NeutralBordered, Style)
            assert st.NeutralBordered == st.Neutral
            assert isinstance(st.GrayNeutral, Style)
            assert isinstance(st.GrayNeutralFlat, Style)
            assert st.Neutral.supports == frozenset({"shape", "line", "text", "icon"})
            assert st.NeutralFlat.supports == frozenset({"shape", "text", "icon"})

            # Semantic neutral cards
            assert isinstance(st.PrimaryNeutral, Style)
            assert isinstance(st.PrimaryNeutralFlat, Style)
            assert isinstance(st.SecondaryNeutral, Style)
            assert isinstance(st.SecondaryNeutralFlat, Style)
            assert isinstance(st.AccentNeutral, Style)
            assert isinstance(st.AccentNeutralFlat, Style)
            assert isinstance(st.WarningNeutral, Style)
            assert isinstance(st.WarningNeutralFlat, Style)

            # Named color neutral cards
            assert isinstance(st.BlueNeutral, Style)
            assert isinstance(st.BlueNeutralFlat, Style)
            assert isinstance(st.GreenNeutral, Style)
            assert isinstance(st.GreenNeutralFlat, Style)
            assert isinstance(st.RedNeutral, Style)
            assert isinstance(st.RedNeutralFlat, Style)
            assert isinstance(st.AmberNeutral, Style)
            assert isinstance(st.AmberNeutralFlat, Style)
            assert isinstance(st.PurpleNeutral, Style)
            assert isinstance(st.PurpleNeutralFlat, Style)
            assert isinstance(st.TealNeutral, Style)
            assert isinstance(st.TealNeutralFlat, Style)

        # Verify default_styles specific tone mapping
        assert default_styles.Neutral.shape_fill_color == default_styles.colors.Neutral
        assert default_styles.BlueNeutral.shape_fill_color == default_styles.colors.Blue1
        assert default_styles.BlueNeutral.shape_line_color == default_styles.colors.Blue3
        assert default_styles.BlueNeutral.text_color == default_styles.colors.Blue6
        assert default_styles.BlueNeutralFlat.shape_fill_color == default_styles.colors.Blue1
        assert default_styles.BlueNeutralFlat.text_color == default_styles.colors.Blue6

    def test_monochrome_danger_success_unsupported(self) -> None:
        """Verifies MonochromeStyles raises AttributeError for unsupported danger and success."""
        for role in ["Danger", "Success"]:
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, role)
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, f"{role}Flat")
            with pytest.raises(AttributeError):
                _ = getattr(monochrome_styles, f"{role}Outline")
            with pytest.raises(KeyError):
                _ = monochrome_styles[role]

        assert "Danger" not in monochrome_styles.styles()
        assert "Success" not in monochrome_styles.styles()

    def test_preset_styles_immutability(self) -> None:
        """Verifies that preset style singletons are frozen and immutable."""
        with pytest.raises(Exception):
            setattr(default_styles, "Primary", default_styles.PrimaryBold)

    def test_preset_styles_patch(self) -> None:
        """Verifies that preset styles can be patched without mutating the original."""
        original_primary = default_styles.Primary
        new_style = default_styles.patch(Primary=default_styles.PrimaryBold)
        assert new_style.Primary == default_styles.PrimaryBold
        assert default_styles.Primary == original_primary

    def test_preset_styles_patch_font_regular_only(self) -> None:
        """Verifies that patch_font with regular applies font to all styles as fallback."""
        original_font = default_styles.Primary.text_font
        new_styles = default_styles.patch_font(regular=FontJapanese.SANSSERIF_REGULAR)

        # Base styles
        assert new_styles.Primary.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.Blue.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.BlueFlat.text_font == FontJapanese.SANSSERIF_REGULAR

        # Bold and thin fallback to regular when not explicitly overridden
        assert new_styles.PrimaryBold.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.BlueBold.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.PrimaryThin.text_font == FontJapanese.SANSSERIF_REGULAR

        # Original styles remain unchanged
        assert default_styles.Primary.text_font == original_font
        assert default_styles.PrimaryBold.text_font == Font.SANSSERIF_BOLD

    def test_preset_styles_patch_font_regular_and_variants(self) -> None:
        """Verifies that patch_font overrides bold and thin styles specifically."""
        new_styles = default_styles.patch_font(
            regular=FontJapanese.SANSSERIF_REGULAR,
            bold=FontJapanese.SANSSERIF_BOLD,
            thin=FontJapanese.SANSSERIF_LIGHT,
        )

        # Base styles
        assert new_styles.Primary.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.Blue.text_font == FontJapanese.SANSSERIF_REGULAR

        # Bold styles
        assert new_styles.PrimaryBold.text_font == FontJapanese.SANSSERIF_BOLD
        assert new_styles.BlueBold.text_font == FontJapanese.SANSSERIF_BOLD

        # Thin styles
        assert new_styles.PrimaryThin.text_font == FontJapanese.SANSSERIF_LIGHT
        assert new_styles.LightThin.text_font == FontJapanese.SANSSERIF_LIGHT

    def test_preset_styles_patch_font_bold_only(self) -> None:
        """Verifies that patching only bold modifies bold styles while preserving others."""
        new_styles = default_styles.patch_font(bold=FontRoboto.ROBOTO_BOLD)

        # Base styles remain default
        assert new_styles.Primary.text_font == Font.SANSSERIF_REGULAR
        assert new_styles.Blue.text_font == Font.SANSSERIF_REGULAR

        # Bold styles are updated
        assert new_styles.PrimaryBold.text_font == FontRoboto.ROBOTO_BOLD
        assert new_styles.BlueBold.text_font == FontRoboto.ROBOTO_BOLD

        # Thin styles remain default
        assert new_styles.PrimaryThin.text_font == Font.SANSSERIF_LIGHT
        assert new_styles.LightThin.text_font == Font.SANSSERIF_LIGHT

    def test_preset_styles_patch_font_sourcecode(self) -> None:
        """Verifies that sourcecode_font is updated properly."""
        original_code_font = default_styles.sourcecode_font
        new_styles = default_styles.patch_font(sourcecode=FontSourceCode.ROBOTO_MONO)

        assert new_styles.sourcecode_font == FontSourceCode.ROBOTO_MONO
        assert default_styles.sourcecode_font == original_code_font

    def test_preset_styles_patch_font_size_only(self) -> None:
        """Verifies that patch_font with size updates font size across all styles while keeping fonts."""
        original_primary_size = default_styles.Primary.text_size
        original_primary_font = default_styles.Primary.text_font
        new_styles = default_styles.patch_font(size=14)

        # Base and variant styles update their text_size
        assert new_styles.Primary.text_size == 14.0
        assert new_styles.PrimaryBold.text_size == 14.0
        assert new_styles.PrimaryThin.text_size == 14.0
        assert new_styles.PrimaryFlat.text_size == 14.0
        assert new_styles.Blue.text_size == 14.0

        # Existing fonts remain preserved
        assert new_styles.Primary.text_font == original_primary_font
        assert new_styles.PrimaryBold.text_font == Font.SANSSERIF_BOLD

        # Original styles instance is not modified
        assert default_styles.Primary.text_size == original_primary_size

    def test_preset_styles_patch_font_size_and_fonts(self) -> None:
        """Verifies that patch_font simultaneously updates both font families and size."""
        new_styles = default_styles.patch_font(
            regular=FontJapanese.SANSSERIF_REGULAR,
            bold=FontJapanese.SANSSERIF_BOLD,
            size=18,
        )

        assert new_styles.Primary.text_font == FontJapanese.SANSSERIF_REGULAR
        assert new_styles.Primary.text_size == 18.0
        assert new_styles.PrimaryBold.text_font == FontJapanese.SANSSERIF_BOLD
        assert new_styles.PrimaryBold.text_size == 18.0

    def test_preset_styles_patch_font_invalid_size(self) -> None:
        """Verifies that negative size raises ValidationError."""
        with pytest.raises(ValidationError):
            default_styles.patch_font(size=-5)

    def test_preset_styles_default_constants(self) -> None:
        """Verifies module and class-level default font and size constants."""
        assert DEFAULT_TEXT_SIZE == 16.0
        assert DEFAULT_FONT == Font.SANSSERIF_REGULAR
        assert BaseStyles.DEFAULT_TEXT_SIZE == 16.0
        assert BaseStyles.DEFAULT_FONT == Font.SANSSERIF_REGULAR
        assert default_styles.Primary.text_size == DEFAULT_TEXT_SIZE
        assert default_styles.Primary.text_font == DEFAULT_FONT


@pytest.mark.image_threshold(93.0)
def test_default_fill() -> None:
    """Integrated drawing test for default circles fill."""
    styles = default_styles
    circle((25, 25), 10, style=styles.Primary, text="drawlib")
    circle((25, 50), 10, style=styles.Light, text="drawlib")
    circle((25, 75), 10, style=styles.PrimaryBold, text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill.png")


@pytest.mark.image_threshold(93.0)
def test_default_style_images() -> None:
    """Integrated drawing test for default image styles."""
    styles = default_styles
    image((25, 25), 20, style=styles.PrimaryFlat, image=IMAGE_FILE)
    image((25, 50), 20, style=styles.PrimarySolid, image=IMAGE_FILE)
    image((25, 75), 20, style=styles.PrimaryDashed, image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_style_images.png")
