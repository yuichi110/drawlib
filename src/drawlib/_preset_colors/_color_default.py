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

from drawlib._core.l3_colors import BaseColors, Color, ColorType

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class DefaultColors(BaseColors):
    """Class representing colors for default preset styles along with standard colors."""

    # --- 6-Tone Numbered Palette (8 Hues x 6 Levels) ---
    # Blue
    Blue1: Color = Color(232, 242, 255)
    Blue2: Color = Color(176, 196, 250)
    Blue3: Color = Color(120, 145, 242)
    Blue4: Color = Color(72, 98, 218)
    Blue5: Color = Color(38, 62, 160)
    Blue6: Color = Color(18, 32, 95)

    # Green
    Green1: Color = Color(232, 250, 235)
    Green2: Color = Color(162, 223, 172)
    Green3: Color = Color(92, 196, 110)
    Green4: Color = Color(58, 150, 75)
    Green5: Color = Color(30, 102, 48)
    Green6: Color = Color(10, 60, 28)

    # Red
    Red1: Color = Color(255, 235, 238)
    Red2: Color = Color(245, 168, 174)
    Red3: Color = Color(235, 102, 110)
    Red4: Color = Color(190, 58, 68)
    Red5: Color = Color(142, 32, 42)
    Red6: Color = Color(100, 15, 22)

    # Orange
    Orange1: Color = Color(255, 238, 218)
    Orange2: Color = Color(250, 198, 145)
    Orange3: Color = Color(240, 148, 55)
    Orange4: Color = Color(215, 100, 20)
    Orange5: Color = Color(165, 68, 12)
    Orange6: Color = Color(110, 42, 8)

    # Amber
    Amber1: Color = Color(255, 246, 222)
    Amber2: Color = Color(248, 216, 140)
    Amber3: Color = Color(242, 180, 58)
    Amber4: Color = Color(215, 134, 20)
    Amber5: Color = Color(162, 92, 12)
    Amber6: Color = Color(106, 56, 6)

    # Purple
    Purple1: Color = Color(245, 232, 255)
    Purple2: Color = Color(205, 168, 248)
    Purple3: Color = Color(165, 110, 235)
    Purple4: Color = Color(128, 55, 195)
    Purple5: Color = Color(92, 32, 145)
    Purple6: Color = Color(58, 20, 98)

    # Teal
    Teal1: Color = Color(230, 250, 250)
    Teal2: Color = Color(158, 222, 222)
    Teal3: Color = Color(85, 195, 195)
    Teal4: Color = Color(42, 152, 154)
    Teal5: Color = Color(22, 104, 108)
    Teal6: Color = Color(8, 62, 65)

    # Pink
    Pink1: Color = Color(255, 230, 242)
    Pink2: Color = Color(248, 175, 210)
    Pink3: Color = Color(235, 110, 170)
    Pink4: Color = Color(195, 45, 125)
    Pink5: Color = Color(145, 25, 90)
    Pink6: Color = Color(100, 14, 58)

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

    # --- Semantic Numbered Palette (6 Roles x 6 Levels) ---
    Primary1: Color = Blue1
    Primary2: Color = Blue2
    Primary3: Color = Blue3
    Primary4: Color = Blue4
    Primary5: Color = Blue5
    Primary6: Color = Blue6
    Secondary1: Color = Teal1
    Secondary2: Color = Teal2
    Secondary3: Color = Teal3
    Secondary4: Color = Teal4
    Secondary5: Color = Teal5
    Secondary6: Color = Teal6
    Accent1: Color = Amber1
    Accent2: Color = Amber2
    Accent3: Color = Amber3
    Accent4: Color = Amber4
    Accent5: Color = Amber5
    Accent6: Color = Amber6
    Muted1: Color = Gray1
    Muted2: Color = Gray2
    Muted3: Color = Gray3
    Muted4: Color = Gray4
    Muted5: Color = Gray5
    Muted6: Color = Gray6
    Danger1: Color = Red1
    Danger2: Color = Red2
    Danger3: Color = Red3
    Danger4: Color = Red4
    Danger5: Color = Red5
    Danger6: Color = Red6
    Success1: Color = Green1
    Success2: Color = Green2
    Success3: Color = Green3
    Success4: Color = Green4
    Success5: Color = Green5
    Success6: Color = Green6

    # --- Semantic Colors (Tone 4 Centered as Default) ---
    Primary: Color = Primary4
    Secondary: Color = Secondary4
    Accent: Color = Accent4
    Muted: Color = Muted4
    Light: Color = White
    Dark: Color = Gray7
    Danger: Color = Danger4
    Success: Color = Success4
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
        # Semantic Tones
        Primary1: ColorType | None = None,
        Primary2: ColorType | None = None,
        Primary3: ColorType | None = None,
        Primary4: ColorType | None = None,
        Primary5: ColorType | None = None,
        Primary6: ColorType | None = None,
        Secondary1: ColorType | None = None,
        Secondary2: ColorType | None = None,
        Secondary3: ColorType | None = None,
        Secondary4: ColorType | None = None,
        Secondary5: ColorType | None = None,
        Secondary6: ColorType | None = None,
        Accent1: ColorType | None = None,
        Accent2: ColorType | None = None,
        Accent3: ColorType | None = None,
        Accent4: ColorType | None = None,
        Accent5: ColorType | None = None,
        Accent6: ColorType | None = None,
        Muted1: ColorType | None = None,
        Muted2: ColorType | None = None,
        Muted3: ColorType | None = None,
        Muted4: ColorType | None = None,
        Muted5: ColorType | None = None,
        Muted6: ColorType | None = None,
        Danger1: ColorType | None = None,
        Danger2: ColorType | None = None,
        Danger3: ColorType | None = None,
        Danger4: ColorType | None = None,
        Danger5: ColorType | None = None,
        Danger6: ColorType | None = None,
        Success1: ColorType | None = None,
        Success2: ColorType | None = None,
        Success3: ColorType | None = None,
        Success4: ColorType | None = None,
        Success5: ColorType | None = None,
        Success6: ColorType | None = None,
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
        # 6-Tone Numbered Palette
        Blue1: ColorType | None = None,
        Blue2: ColorType | None = None,
        Blue3: ColorType | None = None,
        Blue4: ColorType | None = None,
        Blue5: ColorType | None = None,
        Blue6: ColorType | None = None,
        Green1: ColorType | None = None,
        Green2: ColorType | None = None,
        Green3: ColorType | None = None,
        Green4: ColorType | None = None,
        Green5: ColorType | None = None,
        Green6: ColorType | None = None,
        Red1: ColorType | None = None,
        Red2: ColorType | None = None,
        Red3: ColorType | None = None,
        Red4: ColorType | None = None,
        Red5: ColorType | None = None,
        Red6: ColorType | None = None,
        Orange1: ColorType | None = None,
        Orange2: ColorType | None = None,
        Orange3: ColorType | None = None,
        Orange4: ColorType | None = None,
        Orange5: ColorType | None = None,
        Orange6: ColorType | None = None,
        Amber1: ColorType | None = None,
        Amber2: ColorType | None = None,
        Amber3: ColorType | None = None,
        Amber4: ColorType | None = None,
        Amber5: ColorType | None = None,
        Amber6: ColorType | None = None,
        Purple1: ColorType | None = None,
        Purple2: ColorType | None = None,
        Purple3: ColorType | None = None,
        Purple4: ColorType | None = None,
        Purple5: ColorType | None = None,
        Purple6: ColorType | None = None,
        Teal1: ColorType | None = None,
        Teal2: ColorType | None = None,
        Teal3: ColorType | None = None,
        Teal4: ColorType | None = None,
        Teal5: ColorType | None = None,
        Teal6: ColorType | None = None,
        Pink1: ColorType | None = None,
        Pink2: ColorType | None = None,
        Pink3: ColorType | None = None,
        Pink4: ColorType | None = None,
        Pink5: ColorType | None = None,
        Pink6: ColorType | None = None,
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
            Primary1: Primary semantic color tone level 1.
            Primary2: Primary semantic color tone level 2.
            Primary3: Primary semantic color tone level 3.
            Primary4: Primary semantic color tone level 4.
            Primary5: Primary semantic color tone level 5.
            Primary6: Primary semantic color tone level 6.
            Secondary1: Secondary semantic color tone level 1.
            Secondary2: Secondary semantic color tone level 2.
            Secondary3: Secondary semantic color tone level 3.
            Secondary4: Secondary semantic color tone level 4.
            Secondary5: Secondary semantic color tone level 5.
            Secondary6: Secondary semantic color tone level 6.
            Accent1: Accent semantic color tone level 1.
            Accent2: Accent semantic color tone level 2.
            Accent3: Accent semantic color tone level 3.
            Accent4: Accent semantic color tone level 4.
            Accent5: Accent semantic color tone level 5.
            Accent6: Accent semantic color tone level 6.
            Muted1: Muted semantic color tone level 1.
            Muted2: Muted semantic color tone level 2.
            Muted3: Muted semantic color tone level 3.
            Muted4: Muted semantic color tone level 4.
            Muted5: Muted semantic color tone level 5.
            Muted6: Muted semantic color tone level 6.
            Danger1: Danger semantic color tone level 1.
            Danger2: Danger semantic color tone level 2.
            Danger3: Danger semantic color tone level 3.
            Danger4: Danger semantic color tone level 4.
            Danger5: Danger semantic color tone level 5.
            Danger6: Danger semantic color tone level 6.
            Success1: Success semantic color tone level 1.
            Success2: Success semantic color tone level 2.
            Success3: Success semantic color tone level 3.
            Success4: Success semantic color tone level 4.
            Success5: Success semantic color tone level 5.
            Success6: Success semantic color tone level 6.
            White: Neutral White color.
            Gray1: Neutral Gray1 color.
            Gray2: Neutral Gray2 color.
            Gray3: Neutral Gray3 color.
            Gray4: Neutral Gray4 color.
            Gray5: Neutral Gray5 color.
            Gray6: Neutral Gray6 color.
            Gray7: Neutral Gray7 color.
            Gray8: Neutral Gray8 color.
            Black: Neutral Black color.
            Blue1: Blue color tone level 1.
            Blue2: Blue color tone level 2.
            Blue3: Blue color tone level 3.
            Blue4: Blue color tone level 4.
            Blue5: Blue color tone level 5.
            Blue6: Blue color tone level 6.
            Green1: Green color tone level 1.
            Green2: Green color tone level 2.
            Green3: Green color tone level 3.
            Green4: Green color tone level 4.
            Green5: Green color tone level 5.
            Green6: Green color tone level 6.
            Red1: Red color tone level 1.
            Red2: Red color tone level 2.
            Red3: Red color tone level 3.
            Red4: Red color tone level 4.
            Red5: Red color tone level 5.
            Red6: Red color tone level 6.
            Orange1: Orange color tone level 1.
            Orange2: Orange color tone level 2.
            Orange3: Orange color tone level 3.
            Orange4: Orange color tone level 4.
            Orange5: Orange color tone level 5.
            Orange6: Orange color tone level 6.
            Amber1: Amber color tone level 1.
            Amber2: Amber color tone level 2.
            Amber3: Amber color tone level 3.
            Amber4: Amber color tone level 4.
            Amber5: Amber color tone level 5.
            Amber6: Amber color tone level 6.
            Purple1: Purple color tone level 1.
            Purple2: Purple color tone level 2.
            Purple3: Purple color tone level 3.
            Purple4: Purple color tone level 4.
            Purple5: Purple color tone level 5.
            Purple6: Purple color tone level 6.
            Teal1: Teal color tone level 1.
            Teal2: Teal color tone level 2.
            Teal3: Teal color tone level 3.
            Teal4: Teal color tone level 4.
            Teal5: Teal color tone level 5.
            Teal6: Teal color tone level 6.
            Pink1: Pink color tone level 1.
            Pink2: Pink color tone level 2.
            Pink3: Pink color tone level 3.
            Pink4: Pink color tone level 4.
            Pink5: Pink color tone level 5.
            Pink6: Pink color tone level 6.
            Red: Classic primary Red color.
            Green: Classic primary Green color.
            Blue: Classic primary Blue color.
            Yellow: Classic primary Yellow color.
            Orange: Classic primary Orange color.
            Purple: Classic primary Purple color.
            Pink: Classic primary Pink color.
            Cyan: Classic primary Cyan color.
            Magenta: Classic primary Magenta color.
            Lime: Classic primary Lime color.
            Teal: Classic primary Teal color.
            Navy: Classic primary Navy color.
            Olive: Classic primary Olive color.
            Brown: Classic primary Brown color.
            Gold: Classic primary Gold color.
            Aqua: Classic primary Aqua color.
            GreenYellow: Classic primary GreenYellow color.
            Ivory: Classic primary Ivory color.
            Steel: Classic primary Steel color.
            **kwargs: Additional color attributes to update.

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs"} and v is not None}
        return super().patch(**passed, **kwargs)


class DefaultColors1(DefaultColors):
    """Class representing colors for Default preset Tone 1 (Ultra light pastel)."""

    Primary: Color = DefaultColors.Primary1
    Secondary: Color = DefaultColors.Secondary1
    Accent: Color = DefaultColors.Accent1
    Muted: Color = DefaultColors.Muted1
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Danger1
    Success: Color = DefaultColors.Success1
    Canvas: Color = DefaultColors.White


class DefaultColors2(DefaultColors):
    """Class representing colors for Default preset Tone 2 (Light / card background)."""

    Primary: Color = DefaultColors.Primary2
    Secondary: Color = DefaultColors.Secondary2
    Accent: Color = DefaultColors.Accent2
    Muted: Color = DefaultColors.Muted2
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Danger2
    Success: Color = DefaultColors.Success2
    Canvas: Color = DefaultColors.White


class DefaultColors3(DefaultColors):
    """Class representing colors for Default preset Tone 3 (Medium soft)."""

    Primary: Color = DefaultColors.Primary3
    Secondary: Color = DefaultColors.Secondary3
    Accent: Color = DefaultColors.Accent3
    Muted: Color = DefaultColors.Muted3
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Danger3
    Success: Color = DefaultColors.Success3
    Canvas: Color = DefaultColors.White


class DefaultColors4(DefaultColors):
    """Class representing colors for Default preset Tone 4 (Standard base / high contrast)."""

    Primary: Color = DefaultColors.Primary4
    Secondary: Color = DefaultColors.Secondary4
    Accent: Color = DefaultColors.Accent4
    Muted: Color = DefaultColors.Muted4
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Danger4
    Success: Color = DefaultColors.Success4
    Canvas: Color = DefaultColors.White


class DefaultColors5(DefaultColors):
    """Class representing colors for Default preset Tone 5 (Deep tone)."""

    Primary: Color = DefaultColors.Primary5
    Secondary: Color = DefaultColors.Secondary5
    Accent: Color = DefaultColors.Accent5
    Muted: Color = DefaultColors.Muted5
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray7
    Danger: Color = DefaultColors.Danger5
    Success: Color = DefaultColors.Success5
    Canvas: Color = DefaultColors.White


class DefaultColors6(DefaultColors):
    """Class representing colors for Default preset Tone 6 (Darkest shade)."""

    Primary: Color = DefaultColors.Primary6
    Secondary: Color = DefaultColors.Secondary6
    Accent: Color = DefaultColors.Accent6
    Muted: Color = DefaultColors.Muted6
    Light: Color = DefaultColors.White
    Dark: Color = DefaultColors.Gray8
    Danger: Color = DefaultColors.Danger6
    Success: Color = DefaultColors.Success6
    Canvas: Color = DefaultColors.White


__all__ = [
    "DefaultColors",
    "DefaultColors1",
    "DefaultColors2",
    "DefaultColors3",
    "DefaultColors4",
    "DefaultColors5",
    "DefaultColors6",
]
