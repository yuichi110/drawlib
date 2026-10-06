# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Monochrome colors module."""

from __future__ import annotations

from typing import Any, Self

from drawlib._core.l3_colors import BaseColors, Color, ColorType


class MonochromeColors(BaseColors):
    """Class representing colors for monochrome preset styles along with a transparent color."""

    White: Color = Color(255, 255, 255)
    Gray1: Color = Color(245, 245, 245)
    Gray2: Color = Color(230, 230, 230)
    Gray3: Color = Color(210, 210, 210)
    Gray4: Color = Color(175, 175, 175)
    Gray5: Color = Color(135, 135, 135)
    Gray6: Color = Color(95, 95, 95)
    Gray7: Color = Color(55, 55, 55)
    Gray8: Color = Color(25, 25, 25)
    Black: Color = Color(0, 0, 0)

    # Semantic Colors
    Primary: Color = White
    Secondary: Color = Gray2
    Accent: Color = Black
    Muted: Color = Gray1
    Light: Color = White
    Dark: Color = Gray8
    Warning: Color | None = None
    Danger: Color | None = None
    Success: Color | None = None
    Neutral: Color = Gray2
    Canvas: Color = White

    # Semantic & Tinted Neutral Colors (Fill tones mapping to Gray2)
    GrayNeutral: Color = Gray2
    PrimaryNeutral: Color = Gray2
    SecondaryNeutral: Color = Gray2
    AccentNeutral: Color = Gray2
    WarningNeutral: Color = Gray2
    DangerNeutral: Color = Gray2
    SuccessNeutral: Color = Gray2
    MutedNeutral: Color = Gray2

    BlueNeutral: Color = Gray2
    GreenNeutral: Color = Gray2
    RedNeutral: Color = Gray2
    OrangeNeutral: Color = Gray2
    AmberNeutral: Color = Gray2
    PurpleNeutral: Color = Gray2
    TealNeutral: Color = Gray2
    PinkNeutral: Color = Gray2
    CyanNeutral: Color = Gray2
    YellowNeutral: Color = Gray2
    MagentaNeutral: Color = Gray2

    def patch(
        self,
        *,
        Canvas: ColorType | None = None,
        Primary: ColorType | None = None,
        Secondary: ColorType | None = None,
        Accent: ColorType | None = None,
        Muted: ColorType | None = None,
        Light: ColorType | None = None,
        Neutral: ColorType | None = None,
        Dark: ColorType | None = None,
        Warning: ColorType | None = None,
        Danger: ColorType | None = None,
        Success: ColorType | None = None,
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
            Neutral: Neutral semantic color.
            Dark: Dark semantic color.
            Warning: Warning semantic color.
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
            **kwargs: Additional color attributes to update.

        Returns:
            Self: New preset colors instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs", "__class__"} and v is not None}
        return super().patch(**passed, **kwargs)


__all__ = [
    "MonochromeColors",
]
