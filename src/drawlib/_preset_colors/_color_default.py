# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default colors module."""

from __future__ import annotations

import warnings

from drawlib._core.l2_types import Color
from drawlib._core.l3_styles import BaseColors

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class DefaultColors(BaseColors):
    """Class representing colors for default preset styles along with standard colors."""

    # --- 4-Tone Numbered Palette (8 Hues x 4 Levels) ---
    # Blue
    Blue1: Color = Color(210, 225, 255)
    Blue2: Color = Color(111, 111, 239)
    Blue3: Color = Color(40, 75, 200)
    Blue4: Color = Color(18, 32, 95)

    # Green
    Green1: Color = Color(210, 245, 215)
    Green2: Color = Color(79, 191, 79)
    Green3: Color = Color(20, 130, 60)
    Green4: Color = Color(10, 60, 28)

    # Red
    Red1: Color = Color(255, 218, 220)
    Red2: Color = Color(239, 95, 95)
    Red3: Color = Color(200, 35, 45)
    Red4: Color = Color(100, 15, 22)

    # Orange
    Orange1: Color = Color(255, 228, 205)
    Orange2: Color = Color(245, 145, 65)
    Orange3: Color = Color(215, 95, 20)
    Orange4: Color = Color(110, 42, 8)

    # Amber
    Amber1: Color = Color(255, 242, 195)
    Amber2: Color = Color(235, 185, 55)
    Amber3: Color = Color(195, 135, 15)
    Amber4: Color = Color(105, 68, 5)

    # Purple
    Purple1: Color = Color(238, 220, 255)
    Purple2: Color = Color(165, 115, 235)
    Purple3: Color = Color(115, 50, 185)
    Purple4: Color = Color(58, 20, 98)

    # Teal
    Teal1: Color = Color(205, 245, 245)
    Teal2: Color = Color(60, 180, 180)
    Teal3: Color = Color(15, 125, 130)
    Teal4: Color = Color(8, 62, 65)

    # Pink
    Pink1: Color = Color(255, 220, 238)
    Pink2: Color = Color(240, 110, 175)
    Pink3: Color = Color(195, 35, 115)
    Pink4: Color = Color(100, 14, 58)

    # --- Neutrals (Grayscale ordered Light to Dark) ---
    White: Color = Color(255, 255, 255)
    Gray1: Color = Color(246, 248, 251)
    Gray2: Color = Color(215, 222, 232)
    Gray3: Color = Color(145, 158, 175)
    Gray4: Color = Color(90, 100, 115)
    Gray5: Color = Color(38, 42, 50)
    Gray6: Color = Color(24, 28, 36)
    Black: Color = Color(0, 0, 0)

    # --- Standard / Classic Primaries (Unnumbered) ---
    Red: Color = Color(255, 23, 23)
    Green: Color = Color(15, 127, 15)
    Blue: Color = Color(31, 31, 255)
    Yellow: Color = Color(255, 230, 0)
    Orange: Color = Color(255, 120, 0)
    Purple: Color = Color(130, 20, 160)
    Pink: Color = Color(255, 50, 150)
    Cyan: Color = Color(0, 210, 230)
    Magenta: Color = Color(230, 0, 200)
    Lime: Color = Color(100, 215, 0)
    Teal: Color = Color(15, 127, 127)
    Navy: Color = Color(15, 25, 110)
    Olive: Color = Color(127, 127, 31)
    Brown: Color = Color(145, 45, 25)
    Gold: Color = Color(218, 165, 32)
    Aqua: Color = Color(47, 239, 239)
    GreenYellow: Color = Color(127, 207, 31)
    Ivory: Color = Color(239, 239, 207)
    Steel: Color = Color(96, 96, 143)

    # --- Semantic Colors (Default Preset: Tone 2 centered) ---
    Primary: Color = Blue2
    Secondary: Color = Teal2
    Accent: Color = Amber2
    Muted: Color = Gray2
    Light: Color = White
    Dark: Color = Gray5
    Danger: Color = Red
    Success: Color = Green
    Canvas: Color = White


class DefaultLightColors(DefaultColors):
    """Class representing colors for default light/pastel preset styles (Tone 1 centered)."""

    Primary: Color = DefaultColors.Blue1
    Secondary: Color = DefaultColors.Teal1
    Accent: Color = DefaultColors.Amber1
    Muted: Color = DefaultColors.Gray1
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray5
    Danger: Color = DefaultColors.Red
    Success: Color = DefaultColors.Green
    Canvas: Color = DefaultColors.White


class DefaultDarkColors(DefaultColors):
    """Class representing colors for default dark mode preset styles (Tone 3 centered)."""

    Primary: Color = DefaultColors.Blue3
    Secondary: Color = DefaultColors.Teal3
    Accent: Color = DefaultColors.Amber3
    Muted: Color = DefaultColors.Gray5
    Light: Color = DefaultColors.Gray2
    Dark: Color = DefaultColors.Gray6
    Danger: Color = DefaultColors.Red
    Success: Color = DefaultColors.Green
    Canvas: Color = DefaultColors.Gray6


default_colors: DefaultColors = DefaultColors()
default_light_colors: DefaultLightColors = DefaultLightColors()
default_dark_colors: DefaultDarkColors = DefaultDarkColors()

__all__ = [
    "DefaultColors",
    "DefaultDarkColors",
    "DefaultLightColors",
    "default_colors",
    "default_dark_colors",
    "default_light_colors",
]
