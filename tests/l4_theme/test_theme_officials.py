# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib._theme import (
    ThemePreset,
    get_default_styles,
    get_essentials_styles,
    get_monochrome_styles,
)
from drawlib.canvas import save
from drawlib.icons import icon_phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.text import text

IMAGE_FILE = "../assets/image.png"
OUTPUT_DIR_ESSENTIALS = "../../output_tests/l4_theme/essentials/"
OUTPUT_DIR_MONOCHROME = "../../output_tests/l4_theme/monochrome/"


def test_official_theme_generators() -> None:
    """Verifies that all three official theme generation functions return valid ThemePreset instances."""
    default_theme = get_default_styles()
    assert isinstance(default_theme, ThemePreset)

    essentials_theme = get_essentials_styles()
    assert isinstance(essentials_theme, ThemePreset)

    monochrome_theme = get_monochrome_styles()
    assert isinstance(monochrome_theme, ThemePreset)


def test_essentials_fill() -> None:
    """Integrated drawing test for essentials circle filling styles."""
    theme = get_essentials_styles()
    circle((25, 25), 10, text="drawlib")
    circle((25, 50), 10, style=theme.primary, text="drawlib")
    circle((25, 75), 10, style=theme.light, text="drawlib")
    circle((75, 25), 10, style=theme.bold, text="drawlib")
    save(f"{OUTPUT_DIR_ESSENTIALS}test_fill.png")


def test_monochrome_icon_text_lightbold() -> None:
    """Integrated drawing test for monochrome icons and text."""
    theme = get_monochrome_styles()
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    y3 = 80

    icon_phosphor.airplane((x1, y1), width=20, style=theme.light)
    icon_phosphor.airplane((x2, y1), width=20, style=theme.primary)
    icon_phosphor.airplane((x3, y1), width=20, style=theme.bold)

    text((x1, y2), "Hello Drawlib1", style=theme.light)
    text((x2, y2), "Hello Drawlib1", style=theme.primary)
    text((x3, y2), "Hello Drawlib1", style=theme.bold)

    icon_phosphor.airplane((x1, y3), width=20, style=theme.flat)
    icon_phosphor.airplane((x2, y3), width=20, style=theme.solid)
    icon_phosphor.airplane((x3, y3), width=20, style=theme.dashed)

    save(f"{OUTPUT_DIR_MONOCHROME}test_icon_text_lightbold.png")


def test_monochrome_shape_lightbold() -> None:
    """Integrated drawing test for monochrome circles with text."""
    theme = get_monochrome_styles()
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50
    radius = 10

    circle((x1, y1), radius, style=theme.light, text="drawlib")
    circle((x2, y1), radius, style=theme.primary, text="drawlib")
    circle((x3, y1), radius, style=theme.bold, text="drawlib")

    circle((x1, y2), radius, style=theme.solid, text="drawlib")
    circle((x2, y2), radius, style=theme.flat, text="drawlib")
    circle((x3, y2), radius, style=theme.dashed, text="drawlib")

    save(f"{OUTPUT_DIR_MONOCHROME}test_shape_lightbold.png")


def test_monochrome_line_lightbold() -> None:
    """Integrated drawing test for monochrome line styles."""
    theme = get_monochrome_styles()
    x1 = 20
    x2 = 50
    x3 = 80
    y1 = 20
    y2 = 50

    line((x1 - 5, y1), (x1 + 5, y1), style=theme.light)
    line((x2 - 5, y1), (x2 + 5, y1), style=theme.primary)
    line((x3 - 5, y1), (x3 + 5, y1), style=theme.bold)

    line((x1 - 5, y2), (x1 + 5, y2), style=theme.solid)
    line((x2 - 5, y2), (x2 + 5, y2), style=theme.flat)
    line((x3 - 5, y2), (x3 + 5, y2), style=theme.dashed)

    save(f"{OUTPUT_DIR_MONOCHROME}test_line_lightbold.png")
