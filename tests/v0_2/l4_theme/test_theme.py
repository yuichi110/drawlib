# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib.apis import (
    circle,
    config,
    dtheme,
    dutil_script,
    icon_phosphor,
    image,
    line,
    save,
    text,
)
from drawlib.v0_2.private.l2_models import FontFile
from drawlib.v0_2.private.l3_fonts import FontSansSerif, FontSourceCode
from drawlib.v0_2.private.l3_styles import (
    Colors,
    Colors140,
    IconStyle,
    ImageStyle,
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
    TextStyle,
)
from drawlib.v0_2.private.l4_theme._theme import AllStyleModifier, Theme
from drawlib.v0_2.private.l4_theme._theme_models import ThemeStyles

IMAGE_FILE = "../../assets/image.png"
OUTPUT_DIR_DEFAULT = "../../../output_tests/v0_2/l4_theme/default/"
OUTPUT_DIR_CUSTOM = "../../../output_tests/v0_2/l4_theme/custom/"
OUTPUT_DIR_FONT = "../../../output_tests/v0_2/l4_theme/font/"
OUTPUT_DIR_LINE = "../../../output_tests/v0_2/l4_theme/line/"
OUTPUT_DIR_ALLSTYLES = "../../../output_tests/v0_2/l4_theme/allstyles/"

FONT_MPLUS1P_LIGHT = "../../assets/mplus1p/light.ttf"
FONT_MPLUS1P_REGULAR = "../../assets/mplus1p/regular.ttf"
FONT_MPLUS1P_BOLD = "../../assets/mplus1p/bold.ttf"


class TestThemeUnit:
    """Unit tests for the Theme core class and the global dtheme singleton."""

    def test_singleton_and_initial_state(self) -> None:
        """Verifies that the global dtheme is an instance of Theme and starts with default theme."""
        assert isinstance(dtheme, Theme)
        # Check that basic style names are populated
        assert len(dtheme._style_names) > 0
        assert "" in dtheme._style_names

    def test_apply_official_theme_validation(self) -> None:
        """Verifies that applying non-existent theme name raises ValueError."""
        with pytest.raises(ValueError):
            dtheme.apply_official_theme("non_existent_theme")  # type: ignore

    def test_change_default_helpers(self) -> None:
        """Verifies changing default style attributes modifies the fallback/default styles in cache."""
        dtheme.apply_official_theme("default")

        # Test line arrow fill change
        dtheme.change_default_linearrow_fill(True)
        assert dtheme.linestyles.get("").ahfill is True

        # Test font size change
        dtheme.change_default_font_size(28.0)
        assert dtheme.textstyles.get("").size == 28.0
        assert dtheme.shapetextstyles.get("").size == 28.0

        # Test fonts change
        dtheme.change_default_fonts(
            light_font=FontSansSerif.RALEWAYS_LIGHT,
            regular_font=FontSansSerif.RALEWAYS_REGULAR,
            bold_font=FontSansSerif.RALEWAYS_BOLD,
        )
        assert dtheme.textstyles.get("light").font == FontSansSerif.RALEWAYS_LIGHT
        assert dtheme.textstyles.get("").font == FontSansSerif.RALEWAYS_REGULAR
        assert dtheme.textstyles.get("bold").font == FontSansSerif.RALEWAYS_BOLD

        # Restore
        dtheme.apply_official_theme("default")


class TestAllStyleModifierUnit:
    """Unit tests for the AllStyleModifier class."""

    def test_all_style_modifier_operations(self) -> None:
        """Verifies AllStyleModifier list, copy, delete, rename and boundary exceptions."""
        dtheme.apply_official_theme("default")
        modifier = dtheme.allstyles
        assert isinstance(modifier, AllStyleModifier)

        # List
        names = modifier.list()
        assert "blue" in names

        # Copy non-existent raises ValueError
        with pytest.raises(ValueError):
            modifier.copy("non_existent", "target")

        # Copy valid
        modifier.copy("blue", "blue_copy")
        assert "blue_copy" in dtheme.shapestyles.list()

        # Delete default raises ValueError
        with pytest.raises(ValueError):
            modifier.delete("")

        # Delete valid
        modifier.delete("blue_copy")
        assert "blue_copy" not in dtheme.shapestyles.list()

        # Rename default raises ValueError
        with pytest.raises(ValueError):
            modifier.rename("", "new_default")

        # Rename non-existent raises ValueError
        with pytest.raises(ValueError):
            modifier.rename("non_existent", "new_name")

        # Rename valid
        modifier.copy("blue", "temp_style")
        modifier.rename("temp_style", "renamed_style")
        assert "renamed_style" in dtheme.shapestyles.list()
        assert "temp_style" not in dtheme.shapestyles.list()

        # Clean up
        modifier.delete("renamed_style")


# ==========================================
# Integrated Drawing and Visual Tests
# ==========================================


def test_default_fill() -> None:
    """Integrated drawing test for default circles fill."""
    dtheme.apply_official_theme("default")
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style="blue", text="drawlib")
    circle((25, 75), 10, style="green", text="drawlib")
    circle((75, 25), 10, style="red", text="drawlib")
    circle((75, 50), 10, style="black", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white", text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_fill.png")


def test_default_style_images() -> None:
    """Integrated drawing test for default image styles."""
    dtheme.apply_official_theme("default")
    image((25, 25), 20, style="blue", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="blue_solid", image=IMAGE_FILE)
    image((50, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_style_images.png")


def test_default_fill_images() -> None:
    """Integrated drawing test for default image fill colors."""
    dtheme.apply_official_theme("default")
    image((25, 25), 20, image=IMAGE_FILE)
    image((25, 50), 20, style="blue", image=IMAGE_FILE)
    image((25, 75), 20, style="green", image=IMAGE_FILE)
    image((75, 25), 20, style="red", image=IMAGE_FILE)
    image((75, 50), 20, style="black", image=IMAGE_FILE)
    image((75, 75), 20, style="white", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_fill_images.png")


def test_default_flat_images() -> None:
    """Integrated drawing test for default flat styled images."""
    dtheme.apply_official_theme("default")
    config(grid_only=True, background_color=Colors.Gray)
    image((25, 25), 20, style="flat", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_flat", image=IMAGE_FILE)
    image((25, 75), 20, style="green_flat", image=IMAGE_FILE)
    image((75, 25), 20, style="red_flat", image=IMAGE_FILE)
    image((75, 50), 20, style="black_flat", image=IMAGE_FILE)
    image((75, 75), 20, style="white_flat", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_flat_images.png")


def test_default_solid_images() -> None:
    """Integrated drawing test for default solid styled images."""
    dtheme.apply_official_theme("default")
    image((25, 25), 20, style="solid", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_solid", image=IMAGE_FILE)
    image((25, 75), 20, style="green_solid", image=IMAGE_FILE)
    image((75, 25), 20, style="red_solid", image=IMAGE_FILE)
    image((75, 50), 20, style="black_solid", image=IMAGE_FILE)
    image((75, 75), 20, style="white_solid", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_solid_images.png")


def test_default_dashed_images() -> None:
    """Integrated drawing test for default dashed styled images."""
    dtheme.apply_official_theme("default")
    image((25, 25), 20, style="dashed", image=IMAGE_FILE)
    image((25, 50), 20, style="blue_dashed", image=IMAGE_FILE)
    image((25, 75), 20, style="green_dashed", image=IMAGE_FILE)
    image((75, 25), 20, style="red_dashed", image=IMAGE_FILE)
    image((75, 50), 20, style="black_dashed", image=IMAGE_FILE)
    image((75, 75), 20, style="white_dashed", image=IMAGE_FILE)
    save(f"{OUTPUT_DIR_DEFAULT}test_dashed_images.png")


def test_default_flat() -> None:
    """Integrated drawing test for default flat circles."""
    dtheme.apply_official_theme("default")
    circle((25, 25), 10, style="flat", text="drawlib")
    circle((25, 50), 10, style="blue_flat", text="drawlib")
    circle((25, 75), 10, style="green_flat", text="drawlib")
    circle((75, 25), 10, style="red_flat", text="drawlib")
    circle((75, 50), 10, style="black_flat", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_flat", text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_flat.png")


def test_default_solid() -> None:
    """Integrated drawing test for default solid circles."""
    dtheme.apply_official_theme("default")
    circle((25, 25), 10, style="solid", text="drawlib")
    circle((25, 50), 10, style="blue_solid", text="drawlib")
    circle((25, 75), 10, style="green_solid", text="drawlib")
    circle((75, 25), 10, style="red_solid", text="drawlib")
    circle((75, 50), 10, style="black_solid", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_solid", text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_solid.png")


def test_default_dashed() -> None:
    """Integrated drawing test for default dashed circles."""
    dtheme.apply_official_theme("default")
    circle((25, 25), 10, style="dashed", text="drawlib")
    circle((25, 50), 10, style="blue_dashed", text="drawlib")
    circle((25, 75), 10, style="green_dashed", text="drawlib")
    circle((75, 25), 10, style="red_dashed", text="drawlib")
    circle((75, 50), 10, style="black_dashed", text="drawlib", textstyle="white")
    circle((75, 75), 10, style="white_dashed", text="drawlib")
    save(f"{OUTPUT_DIR_DEFAULT}test_dashed.png")


def test_theme_custom() -> None:
    """Integrated drawing test for custom themes and apply_custom_theme()."""
    default_style = ThemeStyles(
        iconstyle=IconStyle(style="fill", color=Colors140.Gold),
        imagestyle=ImageStyle(lcolor=Colors140.Gold, lwidth=0),
        linestyle=LineStyle(width=3, color=Colors140.Gold),
        shapestyle=ShapeStyle(lwidth=0, lcolor=Colors140.Black, fcolor=Colors140.Gold),
        shapetextstyle=ShapeTextStyle(color=Colors140.DarkRed, font=FontSansSerif.RALEWAYS_BOLD),
        textstyle=TextStyle(color=Colors140.DarkRed, font=FontSansSerif.RALEWAYS_BOLD),
    )

    gold = ThemeStyles(
        iconstyle=IconStyle(style="fill", color=Colors140.Gold),
        imagestyle=ImageStyle(lcolor=Colors140.Gold, lwidth=0),
        linestyle=LineStyle(width=3, color=Colors140.Gold),
        shapestyle=ShapeStyle(lwidth=0, lcolor=Colors140.Black, fcolor=Colors140.Gold),
        shapetextstyle=ShapeTextStyle(color=Colors140.Gold, font=FontSansSerif.RALEWAYS_BOLD),
        textstyle=TextStyle(color=Colors140.Gold, font=FontSansSerif.RALEWAYS_BOLD),
    )

    silver = ThemeStyles(
        iconstyle=IconStyle(style="fill", color=Colors140.Silver),
        imagestyle=ImageStyle(lcolor=Colors140.Silver, lwidth=0),
        linestyle=LineStyle(width=3, color=Colors140.Silver),
        shapestyle=ShapeStyle(lwidth=0, lcolor=Colors140.Black, fcolor=Colors140.Silver),
        shapetextstyle=ShapeTextStyle(color=Colors140.Silver, font=FontSansSerif.RALEWAYS_BOLD),
        textstyle=TextStyle(color=Colors140.Silver, font=FontSansSerif.RALEWAYS_BOLD),
    )

    dtheme.apply_custom_theme(
        default_style=default_style,
        named_styles=[
            ("gold", gold),
            ("silver", silver),
        ],
        theme_colors=[
            ("gold", Colors140.Gold),
            ("silver", Colors140.Silver),
        ],
        backgroundcolor=Colors140.AliceBlue,
        sourcecodefont=FontSourceCode.ROBOTO_MONO,
    )

    config(width=100, height=50)
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 10
    y2 = 25
    y3 = 40

    line((x1 - 10, y1), (x1 + 10, y1))
    circle((x1, y2), radius=10)
    text((x1, y3), "Hello Drawlib!")

    for x, name in [(x2, "gold"), (x3, "silver")]:
        line((x - 10, y1), (x + 10, y1), style=name)
        circle((x, y2), radius=10, style=name)
        text((x, y3), "Hello Drawlib!", style=name)

    save(f"{OUTPUT_DIR_CUSTOM}test_custom.png")


def test_theme_change_default_fonts() -> None:
    """Integrated drawing test for font customization and size variations."""
    dtheme.apply_official_theme("default")
    dtheme.change_default_fonts(
        light_font=FontSansSerif.RALEWAYS_LIGHT,
        regular_font=FontSansSerif.RALEWAYS_REGULAR,
        bold_font=FontSansSerif.RALEWAYS_BOLD,
    )

    text((25, 25), "Hello Drawlib", style="light")
    text((25, 50), "Hello Drawlib")
    text((25, 75), "Hello Drawlib", style="bold")
    text((75, 25), "Hello Drawlib", style="red_light")
    text((75, 50), "Hello Drawlib", style="red")
    text((75, 75), "Hello Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR_FONT}test_change_default_fonts.png")


def test_theme_change_default_fonts_file() -> None:
    """Integrated drawing test for font customization using FontFile."""
    dtheme.apply_official_theme("default")
    dtheme.change_default_fonts(
        light_font=FontFile(FONT_MPLUS1P_LIGHT),
        regular_font=FontFile(FONT_MPLUS1P_REGULAR),
        bold_font=FontFile(FONT_MPLUS1P_BOLD),
    )

    text((25, 25), "こんにちは Drawlib", style="light")
    text((25, 50), "こんにちは Drawlib")
    text((25, 75), "こんにちは Drawlib", style="bold")
    text((75, 25), "こんにちは Drawlib", style="red_light")
    text((75, 50), "こんにちは Drawlib", style="red")
    text((75, 75), "こんにちは Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR_FONT}test_change_default_fonts_file.png")


def test_theme_change_default_font_size() -> None:
    """Integrated drawing test for global font size configuration changes."""
    dtheme.apply_official_theme("default")
    dtheme.change_default_font_size(28)

    text((25, 25), "Hello Drawlib", style="light")
    text((25, 50), "Hello Drawlib")
    text((25, 75), "Hello Drawlib", style="bold")
    text((75, 25), "Hello Drawlib", style="red_light")
    text((75, 50), "Hello Drawlib", style="red")
    text((75, 75), "Hello Drawlib", style="red_bold")
    save(f"{OUTPUT_DIR_FONT}test_change_default_font_size.png")


def test_theme_change_default_linearrow_fill() -> None:
    """Integrated drawing test for changing arrow fill configurations."""
    dtheme.apply_official_theme("default")
    dtheme.change_default_linearrow_fill(True)

    line((20, 30), (80, 30), arrowhead="->")
    line((20, 50), (80, 50), arrowhead="<-", style="red")
    line((20, 80), (80, 80), arrowhead="<->", style="blue_dashed_bold")
    save(f"{OUTPUT_DIR_LINE}test_change_default_linearrow_fill.png")


def test_allstyles_copy() -> None:
    """Integrated drawing test for copying theme styles using allstyles."""
    dtheme.apply_official_theme("default")
    dtheme.allstyles.copy("blue", "blue_copy")
    circle((50, 50), 10, style="blue_copy")
    save(f"{OUTPUT_DIR_ALLSTYLES}test_copy.png")
    dtheme.allstyles.delete("blue_copy")


def test_allstyles_merge() -> None:
    """Integrated drawing test for merging new theme styles using allstyles."""
    dtheme.apply_official_theme("default")
    theme_styles = ThemeStyles(
        iconstyle=IconStyle(style="fill", color=Colors.Red),
        imagestyle=ImageStyle(lwidth=2, lcolor=Colors.Red),
        linestyle=LineStyle(style="dashed", width=5),
        shapestyle=ShapeStyle(lwidth=5, lcolor=Colors.Red),
        shapetextstyle=ShapeTextStyle(color=Colors.White, size=24),
        textstyle=TextStyle(size=24, font=FontSansSerif.RALEWAYS_REGULAR),
    )
    dtheme.allstyles.merge(theme_styles)

    icon_phosphor.google_logo((25, 25), width=30)
    image(xy=(25, 75), width=30, image=IMAGE_FILE)
    line((10, 50), (90, 50))
    line((50, 10), (50, 90), arrowhead="->")
    circle((75, 25), radius=20)
    circle((75, 75), radius=20, text="Hello")
    text((50, 50), "Hello Drawlib", angle=45)
    save(f"{OUTPUT_DIR_ALLSTYLES}test_merge.png")
