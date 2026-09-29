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
from typing import Any, Self

from drawlib._core.l2_types import ColorType
from drawlib._core.styles import BaseColors, Color

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
    Gray1: Color = Color(248, 250, 252)
    Gray2: Color = Color(238, 242, 246)
    Gray3: Color = Color(220, 226, 235)
    Gray4: Color = Color(186, 196, 210)
    Gray5: Color = Color(140, 152, 170)
    Gray6: Color = Color(95, 107, 125)
    Gray7: Color = Color(50, 58, 72)
    Gray8: Color = Color(24, 28, 36)
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
    Dark: Color = Gray7
    Danger: Color = Red2
    Success: Color = Green2
    Canvas: Color = White

    def patch(
        self,
        *,
        Canvas: ColorType | None = None,
        Primary: ColorType | None = None,
        Secondary: ColorType | None = None,
        Accent: ColorType | None = None,
        Muted: ColorType | None = None,
        Light: ColorType | None = None,
        Dark: ColorType | None = None,
        Danger: ColorType | None = None,
        Success: ColorType | None = None,
        # Grays
        White: ColorType | None = None,
        Gray1: ColorType | None = None,
        Gray2: ColorType | None = None,
        Gray3: ColorType | None = None,
        Gray4: ColorType | None = None,
        Gray5: ColorType | None = None,
        Gray6: ColorType | None = None,
        Gray7: ColorType | None = None,
        Gray8: ColorType | None = None,
        Black: ColorType | None = None,
        # 4-Tone Numbered Palette
        Blue1: ColorType | None = None,
        Blue2: ColorType | None = None,
        Blue3: ColorType | None = None,
        Blue4: ColorType | None = None,
        Green1: ColorType | None = None,
        Green2: ColorType | None = None,
        Green3: ColorType | None = None,
        Green4: ColorType | None = None,
        Red1: ColorType | None = None,
        Red2: ColorType | None = None,
        Red3: ColorType | None = None,
        Red4: ColorType | None = None,
        Orange1: ColorType | None = None,
        Orange2: ColorType | None = None,
        Orange3: ColorType | None = None,
        Orange4: ColorType | None = None,
        Amber1: ColorType | None = None,
        Amber2: ColorType | None = None,
        Amber3: ColorType | None = None,
        Amber4: ColorType | None = None,
        Purple1: ColorType | None = None,
        Purple2: ColorType | None = None,
        Purple3: ColorType | None = None,
        Purple4: ColorType | None = None,
        Teal1: ColorType | None = None,
        Teal2: ColorType | None = None,
        Teal3: ColorType | None = None,
        Teal4: ColorType | None = None,
        Pink1: ColorType | None = None,
        Pink2: ColorType | None = None,
        Pink3: ColorType | None = None,
        Pink4: ColorType | None = None,
        # Standard Primaries
        Red: ColorType | None = None,
        Green: ColorType | None = None,
        Blue: ColorType | None = None,
        Yellow: ColorType | None = None,
        Orange: ColorType | None = None,
        Purple: ColorType | None = None,
        Pink: ColorType | None = None,
        Cyan: ColorType | None = None,
        Magenta: ColorType | None = None,
        Lime: ColorType | None = None,
        Teal: ColorType | None = None,
        Navy: ColorType | None = None,
        Olive: ColorType | None = None,
        Brown: ColorType | None = None,
        Gold: ColorType | None = None,
        Aqua: ColorType | None = None,
        GreenYellow: ColorType | None = None,
        Ivory: ColorType | None = None,
        Steel: ColorType | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """Create a new copy of preset colors with updated attributes.

        Args:
            Canvas: Canvas background color.
            Primary: Primary semantic color.
            Secondary: Secondary semantic color.
            Accent: Accent semantic color.
            Muted: Muted semantic color.
            Light: Light semantic color.
            Dark: Dark semantic color.
            Danger: Danger semantic color.
            Success: Success semantic color.
            White: White neutral color.
            Gray1: Neutral gray level 1.
            Gray2: Neutral gray level 2.
            Gray3: Neutral gray level 3.
            Gray4: Neutral gray level 4.
            Gray5: Neutral gray level 5.
            Gray6: Neutral gray level 6.
            Gray7: Neutral gray level 7.
            Gray8: Neutral gray level 8.
            Black: Black neutral color.
            Blue1: Blue tone level 1.
            Blue2: Blue tone level 2.
            Blue3: Blue tone level 3.
            Blue4: Blue tone level 4.
            Green1: Green tone level 1.
            Green2: Green tone level 2.
            Green3: Green tone level 3.
            Green4: Green tone level 4.
            Red1: Red tone level 1.
            Red2: Red tone level 2.
            Red3: Red tone level 3.
            Red4: Red tone level 4.
            Orange1: Orange tone level 1.
            Orange2: Orange tone level 2.
            Orange3: Orange tone level 3.
            Orange4: Orange tone level 4.
            Amber1: Amber tone level 1.
            Amber2: Amber tone level 2.
            Amber3: Amber tone level 3.
            Amber4: Amber tone level 4.
            Purple1: Purple tone level 1.
            Purple2: Purple tone level 2.
            Purple3: Purple tone level 3.
            Purple4: Purple tone level 4.
            Teal1: Teal tone level 1.
            Teal2: Teal tone level 2.
            Teal3: Teal tone level 3.
            Teal4: Teal tone level 4.
            Pink1: Pink tone level 1.
            Pink2: Pink tone level 2.
            Pink3: Pink tone level 3.
            Pink4: Pink tone level 4.
            Red: Standard red primary color.
            Green: Standard green primary color.
            Blue: Standard blue primary color.
            Yellow: Standard yellow primary color.
            Orange: Standard orange primary color.
            Purple: Standard purple primary color.
            Pink: Standard pink primary color.
            Cyan: Standard cyan primary color.
            Magenta: Standard magenta primary color.
            Lime: Standard lime primary color.
            Teal: Standard teal primary color.
            Navy: Standard navy primary color.
            Olive: Standard olive primary color.
            Brown: Standard brown primary color.
            Gold: Standard gold primary color.
            Aqua: Standard aqua primary color.
            GreenYellow: Standard green-yellow primary color.
            Ivory: Standard ivory primary color.
            Steel: Standard steel primary color.
            **kwargs: Additional color attributes to update.

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs"} and v is not None}
        return super().patch(**passed, **kwargs)


class DefaultLightColors(DefaultColors):
    """Class representing colors for default light/pastel preset styles (Tone 1 centered)."""

    Primary: Color = DefaultColors.Blue1
    Secondary: Color = DefaultColors.Teal1
    Accent: Color = DefaultColors.Amber1
    Muted: Color = DefaultColors.Gray1
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Red1
    Success: Color = DefaultColors.Green1
    Canvas: Color = DefaultColors.White


class DefaultDarkColors(DefaultColors):
    """Class representing colors for default deep tone preset styles (Tone 3 centered)."""

    Primary: Color = DefaultColors.Blue3
    Secondary: Color = DefaultColors.Teal3
    Accent: Color = DefaultColors.Amber3
    Muted: Color = DefaultColors.Gray6
    Light: Color = DefaultColors.Gray3
    Dark: Color = DefaultColors.Gray8
    Danger: Color = DefaultColors.Red3
    Success: Color = DefaultColors.Green3
    Canvas: Color = DefaultColors.White


__all__ = [
    "DefaultColors",
    "DefaultDarkColors",
    "DefaultLightColors",
]
