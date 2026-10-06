# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Monochrome preset styles module."""

from __future__ import annotations

from typing import Any, Self

from drawlib._core.l3_colors import BaseColors, ColorType
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import BaseStyles, Style
from drawlib._preset_colors import MonochromeColors
from drawlib._preset_styles._utils import _make_neutral_card, _make_variants


class MonochromeStyles(BaseStyles):
    """Monochrome preset styles with complete typing for IDE autocompletion."""

    Primary: Style
    PrimaryBordered: Style
    PrimaryBold: Style
    PrimaryThin: Style
    PrimaryFlat: Style
    PrimaryOutline: Style
    PrimarySolid: Style
    PrimaryOutlineBold: Style
    PrimarySolidBold: Style
    PrimaryOutlineThin: Style
    PrimarySolidThin: Style
    PrimaryDashed: Style
    PrimaryDashedBold: Style
    PrimaryDashedThin: Style
    PrimaryDotted: Style
    PrimaryDottedBold: Style
    PrimaryDottedThin: Style
    Secondary: Style
    SecondaryBordered: Style
    SecondaryBold: Style
    SecondaryThin: Style
    SecondaryFlat: Style
    SecondaryOutline: Style
    SecondarySolid: Style
    SecondaryOutlineBold: Style
    SecondarySolidBold: Style
    SecondaryOutlineThin: Style
    SecondarySolidThin: Style
    SecondaryDashed: Style
    SecondaryDashedBold: Style
    SecondaryDashedThin: Style
    SecondaryDotted: Style
    SecondaryDottedBold: Style
    SecondaryDottedThin: Style
    Accent: Style
    AccentBordered: Style
    AccentBold: Style
    AccentThin: Style
    AccentFlat: Style
    AccentOutline: Style
    AccentSolid: Style
    AccentOutlineBold: Style
    AccentSolidBold: Style
    AccentOutlineThin: Style
    AccentSolidThin: Style
    AccentDashed: Style
    AccentDashedBold: Style
    AccentDashedThin: Style
    AccentDotted: Style
    AccentDottedBold: Style
    AccentDottedThin: Style
    Muted: Style
    MutedBordered: Style
    MutedBold: Style
    MutedThin: Style
    MutedFlat: Style
    MutedOutline: Style
    MutedSolid: Style
    MutedOutlineBold: Style
    MutedSolidBold: Style
    MutedOutlineThin: Style
    MutedSolidThin: Style
    MutedDashed: Style
    MutedDashedBold: Style
    MutedDashedThin: Style
    MutedDotted: Style
    MutedDottedBold: Style
    MutedDottedThin: Style
    Light: Style
    LightBordered: Style
    LightBold: Style
    LightThin: Style
    LightFlat: Style
    LightOutline: Style
    LightSolid: Style
    LightOutlineBold: Style
    LightSolidBold: Style
    LightOutlineThin: Style
    LightSolidThin: Style
    LightDashed: Style
    LightDashedBold: Style
    LightDashedThin: Style
    LightDotted: Style
    LightDottedBold: Style
    LightDottedThin: Style
    Neutral: Style
    NeutralBordered: Style
    NeutralBold: Style
    NeutralThin: Style
    NeutralFlat: Style
    NeutralOutline: Style
    NeutralSolid: Style
    NeutralOutlineBold: Style
    NeutralSolidBold: Style
    NeutralOutlineThin: Style
    NeutralSolidThin: Style
    NeutralDashed: Style
    NeutralDashedBold: Style
    NeutralDashedThin: Style
    NeutralDotted: Style
    NeutralDottedBold: Style
    NeutralDottedThin: Style
    Dark: Style
    DarkBordered: Style
    DarkBold: Style
    DarkThin: Style
    DarkFlat: Style
    DarkOutline: Style
    DarkSolid: Style
    DarkOutlineBold: Style
    DarkSolidBold: Style
    DarkOutlineThin: Style
    DarkSolidThin: Style
    DarkDashed: Style
    DarkDashedBold: Style
    DarkDashedThin: Style
    DarkDotted: Style
    DarkDottedBold: Style
    DarkDottedThin: Style
    White: Style
    WhiteBordered: Style
    WhiteBold: Style
    WhiteThin: Style
    WhiteFlat: Style
    WhiteOutline: Style
    WhiteSolid: Style
    WhiteOutlineBold: Style
    WhiteSolidBold: Style
    WhiteOutlineThin: Style
    WhiteSolidThin: Style
    WhiteDashed: Style
    WhiteDashedBold: Style
    WhiteDashedThin: Style
    WhiteDotted: Style
    WhiteDottedBold: Style
    WhiteDottedThin: Style
    Gray1: Style
    Gray1Bordered: Style
    Gray1Bold: Style
    Gray1Thin: Style
    Gray1Flat: Style
    Gray1Outline: Style
    Gray1Solid: Style
    Gray1OutlineBold: Style
    Gray1SolidBold: Style
    Gray1OutlineThin: Style
    Gray1SolidThin: Style
    Gray1Dashed: Style
    Gray1DashedBold: Style
    Gray1DashedThin: Style
    Gray1Dotted: Style
    Gray1DottedBold: Style
    Gray1DottedThin: Style
    Gray2: Style
    Gray2Bordered: Style
    Gray2Bold: Style
    Gray2Thin: Style
    Gray2Flat: Style
    Gray2Outline: Style
    Gray2Solid: Style
    Gray2OutlineBold: Style
    Gray2SolidBold: Style
    Gray2OutlineThin: Style
    Gray2SolidThin: Style
    Gray2Dashed: Style
    Gray2DashedBold: Style
    Gray2DashedThin: Style
    Gray2Dotted: Style
    Gray2DottedBold: Style
    Gray2DottedThin: Style
    Gray3: Style
    Gray3Bordered: Style
    Gray3Bold: Style
    Gray3Thin: Style
    Gray3Flat: Style
    Gray3Outline: Style
    Gray3Solid: Style
    Gray3OutlineBold: Style
    Gray3SolidBold: Style
    Gray3OutlineThin: Style
    Gray3SolidThin: Style
    Gray3Dashed: Style
    Gray3DashedBold: Style
    Gray3DashedThin: Style
    Gray3Dotted: Style
    Gray3DottedBold: Style
    Gray3DottedThin: Style
    Gray4: Style
    Gray4Bordered: Style
    Gray4Bold: Style
    Gray4Thin: Style
    Gray4Flat: Style
    Gray4Outline: Style
    Gray4Solid: Style
    Gray4OutlineBold: Style
    Gray4SolidBold: Style
    Gray4OutlineThin: Style
    Gray4SolidThin: Style
    Gray4Dashed: Style
    Gray4DashedBold: Style
    Gray4DashedThin: Style
    Gray4Dotted: Style
    Gray4DottedBold: Style
    Gray4DottedThin: Style
    Gray5: Style
    Gray5Bordered: Style
    Gray5Bold: Style
    Gray5Thin: Style
    Gray5Flat: Style
    Gray5Outline: Style
    Gray5Solid: Style
    Gray5OutlineBold: Style
    Gray5SolidBold: Style
    Gray5OutlineThin: Style
    Gray5SolidThin: Style
    Gray5Dashed: Style
    Gray5DashedBold: Style
    Gray5DashedThin: Style
    Gray5Dotted: Style
    Gray5DottedBold: Style
    Gray5DottedThin: Style
    Gray6: Style
    Gray6Bordered: Style
    Gray6Bold: Style
    Gray6Thin: Style
    Gray6Flat: Style
    Gray6Outline: Style
    Gray6Solid: Style
    Gray6OutlineBold: Style
    Gray6SolidBold: Style
    Gray6OutlineThin: Style
    Gray6SolidThin: Style
    Gray6Dashed: Style
    Gray6DashedBold: Style
    Gray6DashedThin: Style
    Gray6Dotted: Style
    Gray6DottedBold: Style
    Gray6DottedThin: Style
    Gray7: Style
    Gray7Bordered: Style
    Gray7Bold: Style
    Gray7Thin: Style
    Gray7Flat: Style
    Gray7Outline: Style
    Gray7Solid: Style
    Gray7OutlineBold: Style
    Gray7SolidBold: Style
    Gray7OutlineThin: Style
    Gray7SolidThin: Style
    Gray7Dashed: Style
    Gray7DashedBold: Style
    Gray7DashedThin: Style
    Gray7Dotted: Style
    Gray7DottedBold: Style
    Gray7DottedThin: Style
    Gray8: Style
    Gray8Bordered: Style
    Gray8Bold: Style
    Gray8Thin: Style
    Gray8Flat: Style
    Gray8Outline: Style
    Gray8Solid: Style
    Gray8OutlineBold: Style
    Gray8SolidBold: Style
    Gray8OutlineThin: Style
    Gray8SolidThin: Style
    Gray8Dashed: Style
    Gray8DashedBold: Style
    Gray8DashedThin: Style
    Gray8Dotted: Style
    Gray8DottedBold: Style
    Gray8DottedThin: Style
    Black: Style
    BlackBordered: Style
    BlackBold: Style
    BlackThin: Style
    BlackFlat: Style
    BlackOutline: Style
    BlackSolid: Style
    BlackOutlineBold: Style
    BlackSolidBold: Style
    BlackOutlineThin: Style
    BlackSolidThin: Style
    BlackDashed: Style
    BlackDashedBold: Style
    BlackDashedThin: Style
    BlackDotted: Style
    BlackDottedBold: Style
    BlackDottedThin: Style
    Canvas: Style
    CanvasFlat: Style
    GrayNeutral: Style
    GrayNeutralFlat: Style
    PrimaryNeutral: Style
    PrimaryNeutralFlat: Style
    SecondaryNeutral: Style
    SecondaryNeutralFlat: Style
    AccentNeutral: Style
    AccentNeutralFlat: Style
    WarningNeutral: Style
    WarningNeutralFlat: Style
    DangerNeutral: Style
    DangerNeutralFlat: Style
    SuccessNeutral: Style
    SuccessNeutralFlat: Style
    MutedNeutral: Style
    MutedNeutralFlat: Style
    BlueNeutral: Style
    BlueNeutralFlat: Style
    GreenNeutral: Style
    GreenNeutralFlat: Style
    RedNeutral: Style
    RedNeutralFlat: Style
    OrangeNeutral: Style
    OrangeNeutralFlat: Style
    AmberNeutral: Style
    AmberNeutralFlat: Style
    PurpleNeutral: Style
    PurpleNeutralFlat: Style
    TealNeutral: Style
    TealNeutralFlat: Style
    PinkNeutral: Style
    PinkNeutralFlat: Style
    CyanNeutral: Style
    CyanNeutralFlat: Style
    YellowNeutral: Style
    YellowNeutralFlat: Style
    MagentaNeutral: Style
    MagentaNeutralFlat: Style

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        super().__init__(**kwargs)

    def patch(
        self,
        *,
        BackgroundColor: ColorType | None = None,
        Width: int | None = None,
        Height: int | None = None,
        Dpi: int | None = None,
        SourcecodeFont: FontSourceCode | None = None,
        Colors: BaseColors | None = None,
        Canvas: Style | None = None,
        CanvasFlat: Style | None = None,
        Primary: Style | None = None,
        PrimaryBordered: Style | None = None,
        PrimaryBold: Style | None = None,
        PrimaryThin: Style | None = None,
        PrimaryFlat: Style | None = None,
        PrimaryOutline: Style | None = None,
        PrimarySolid: Style | None = None,
        PrimaryOutlineBold: Style | None = None,
        PrimarySolidBold: Style | None = None,
        PrimaryOutlineThin: Style | None = None,
        PrimarySolidThin: Style | None = None,
        PrimaryDashed: Style | None = None,
        PrimaryDashedBold: Style | None = None,
        PrimaryDashedThin: Style | None = None,
        PrimaryDotted: Style | None = None,
        PrimaryDottedBold: Style | None = None,
        PrimaryDottedThin: Style | None = None,
        Secondary: Style | None = None,
        SecondaryBordered: Style | None = None,
        SecondaryBold: Style | None = None,
        SecondaryThin: Style | None = None,
        SecondaryFlat: Style | None = None,
        SecondaryOutline: Style | None = None,
        SecondarySolid: Style | None = None,
        SecondaryOutlineBold: Style | None = None,
        SecondarySolidBold: Style | None = None,
        SecondaryOutlineThin: Style | None = None,
        SecondarySolidThin: Style | None = None,
        SecondaryDashed: Style | None = None,
        SecondaryDashedBold: Style | None = None,
        SecondaryDashedThin: Style | None = None,
        SecondaryDotted: Style | None = None,
        SecondaryDottedBold: Style | None = None,
        SecondaryDottedThin: Style | None = None,
        Accent: Style | None = None,
        AccentBordered: Style | None = None,
        AccentBold: Style | None = None,
        AccentThin: Style | None = None,
        AccentFlat: Style | None = None,
        AccentOutline: Style | None = None,
        AccentSolid: Style | None = None,
        AccentOutlineBold: Style | None = None,
        AccentSolidBold: Style | None = None,
        AccentOutlineThin: Style | None = None,
        AccentSolidThin: Style | None = None,
        AccentDashed: Style | None = None,
        AccentDashedBold: Style | None = None,
        AccentDashedThin: Style | None = None,
        AccentDotted: Style | None = None,
        AccentDottedBold: Style | None = None,
        AccentDottedThin: Style | None = None,
        Muted: Style | None = None,
        MutedBordered: Style | None = None,
        MutedBold: Style | None = None,
        MutedThin: Style | None = None,
        MutedFlat: Style | None = None,
        MutedOutline: Style | None = None,
        MutedSolid: Style | None = None,
        MutedOutlineBold: Style | None = None,
        MutedSolidBold: Style | None = None,
        MutedOutlineThin: Style | None = None,
        MutedSolidThin: Style | None = None,
        MutedDashed: Style | None = None,
        MutedDashedBold: Style | None = None,
        MutedDashedThin: Style | None = None,
        MutedDotted: Style | None = None,
        MutedDottedBold: Style | None = None,
        MutedDottedThin: Style | None = None,
        Light: Style | None = None,
        LightBordered: Style | None = None,
        LightBold: Style | None = None,
        LightThin: Style | None = None,
        LightFlat: Style | None = None,
        LightOutline: Style | None = None,
        LightSolid: Style | None = None,
        LightOutlineBold: Style | None = None,
        LightSolidBold: Style | None = None,
        LightOutlineThin: Style | None = None,
        LightSolidThin: Style | None = None,
        LightDashed: Style | None = None,
        LightDashedBold: Style | None = None,
        LightDashedThin: Style | None = None,
        LightDotted: Style | None = None,
        LightDottedBold: Style | None = None,
        LightDottedThin: Style | None = None,
        Neutral: Style | None = None,
        NeutralBordered: Style | None = None,
        NeutralBold: Style | None = None,
        NeutralThin: Style | None = None,
        NeutralFlat: Style | None = None,
        NeutralOutline: Style | None = None,
        NeutralSolid: Style | None = None,
        NeutralOutlineBold: Style | None = None,
        NeutralSolidBold: Style | None = None,
        NeutralOutlineThin: Style | None = None,
        NeutralSolidThin: Style | None = None,
        NeutralDashed: Style | None = None,
        NeutralDashedBold: Style | None = None,
        NeutralDashedThin: Style | None = None,
        NeutralDotted: Style | None = None,
        NeutralDottedBold: Style | None = None,
        NeutralDottedThin: Style | None = None,
        Dark: Style | None = None,
        DarkBordered: Style | None = None,
        DarkBold: Style | None = None,
        DarkThin: Style | None = None,
        DarkFlat: Style | None = None,
        DarkOutline: Style | None = None,
        DarkSolid: Style | None = None,
        DarkOutlineBold: Style | None = None,
        DarkSolidBold: Style | None = None,
        DarkOutlineThin: Style | None = None,
        DarkSolidThin: Style | None = None,
        DarkDashed: Style | None = None,
        DarkDashedBold: Style | None = None,
        DarkDashedThin: Style | None = None,
        DarkDotted: Style | None = None,
        DarkDottedBold: Style | None = None,
        DarkDottedThin: Style | None = None,
        White: Style | None = None,
        WhiteBordered: Style | None = None,
        WhiteBold: Style | None = None,
        WhiteThin: Style | None = None,
        WhiteFlat: Style | None = None,
        WhiteOutline: Style | None = None,
        WhiteSolid: Style | None = None,
        WhiteOutlineBold: Style | None = None,
        WhiteSolidBold: Style | None = None,
        WhiteOutlineThin: Style | None = None,
        WhiteSolidThin: Style | None = None,
        WhiteDashed: Style | None = None,
        WhiteDashedBold: Style | None = None,
        WhiteDashedThin: Style | None = None,
        WhiteDotted: Style | None = None,
        WhiteDottedBold: Style | None = None,
        WhiteDottedThin: Style | None = None,
        Gray1: Style | None = None,
        Gray1Bordered: Style | None = None,
        Gray1Bold: Style | None = None,
        Gray1Thin: Style | None = None,
        Gray1Flat: Style | None = None,
        Gray1Outline: Style | None = None,
        Gray1Solid: Style | None = None,
        Gray1OutlineBold: Style | None = None,
        Gray1SolidBold: Style | None = None,
        Gray1OutlineThin: Style | None = None,
        Gray1SolidThin: Style | None = None,
        Gray1Dashed: Style | None = None,
        Gray1DashedBold: Style | None = None,
        Gray1DashedThin: Style | None = None,
        Gray1Dotted: Style | None = None,
        Gray1DottedBold: Style | None = None,
        Gray1DottedThin: Style | None = None,
        Gray2: Style | None = None,
        Gray2Bordered: Style | None = None,
        Gray2Bold: Style | None = None,
        Gray2Thin: Style | None = None,
        Gray2Flat: Style | None = None,
        Gray2Outline: Style | None = None,
        Gray2Solid: Style | None = None,
        Gray2OutlineBold: Style | None = None,
        Gray2SolidBold: Style | None = None,
        Gray2OutlineThin: Style | None = None,
        Gray2SolidThin: Style | None = None,
        Gray2Dashed: Style | None = None,
        Gray2DashedBold: Style | None = None,
        Gray2DashedThin: Style | None = None,
        Gray2Dotted: Style | None = None,
        Gray2DottedBold: Style | None = None,
        Gray2DottedThin: Style | None = None,
        Gray3: Style | None = None,
        Gray3Bordered: Style | None = None,
        Gray3Bold: Style | None = None,
        Gray3Thin: Style | None = None,
        Gray3Flat: Style | None = None,
        Gray3Outline: Style | None = None,
        Gray3Solid: Style | None = None,
        Gray3OutlineBold: Style | None = None,
        Gray3SolidBold: Style | None = None,
        Gray3OutlineThin: Style | None = None,
        Gray3SolidThin: Style | None = None,
        Gray3Dashed: Style | None = None,
        Gray3DashedBold: Style | None = None,
        Gray3DashedThin: Style | None = None,
        Gray3Dotted: Style | None = None,
        Gray3DottedBold: Style | None = None,
        Gray3DottedThin: Style | None = None,
        Gray4: Style | None = None,
        Gray4Bordered: Style | None = None,
        Gray4Bold: Style | None = None,
        Gray4Thin: Style | None = None,
        Gray4Flat: Style | None = None,
        Gray4Outline: Style | None = None,
        Gray4Solid: Style | None = None,
        Gray4OutlineBold: Style | None = None,
        Gray4SolidBold: Style | None = None,
        Gray4OutlineThin: Style | None = None,
        Gray4SolidThin: Style | None = None,
        Gray4Dashed: Style | None = None,
        Gray4DashedBold: Style | None = None,
        Gray4DashedThin: Style | None = None,
        Gray4Dotted: Style | None = None,
        Gray4DottedBold: Style | None = None,
        Gray4DottedThin: Style | None = None,
        Gray5: Style | None = None,
        Gray5Bordered: Style | None = None,
        Gray5Bold: Style | None = None,
        Gray5Thin: Style | None = None,
        Gray5Flat: Style | None = None,
        Gray5Outline: Style | None = None,
        Gray5Solid: Style | None = None,
        Gray5OutlineBold: Style | None = None,
        Gray5SolidBold: Style | None = None,
        Gray5OutlineThin: Style | None = None,
        Gray5SolidThin: Style | None = None,
        Gray5Dashed: Style | None = None,
        Gray5DashedBold: Style | None = None,
        Gray5DashedThin: Style | None = None,
        Gray5Dotted: Style | None = None,
        Gray5DottedBold: Style | None = None,
        Gray5DottedThin: Style | None = None,
        Gray6: Style | None = None,
        Gray6Bordered: Style | None = None,
        Gray6Bold: Style | None = None,
        Gray6Thin: Style | None = None,
        Gray6Flat: Style | None = None,
        Gray6Outline: Style | None = None,
        Gray6Solid: Style | None = None,
        Gray6OutlineBold: Style | None = None,
        Gray6SolidBold: Style | None = None,
        Gray6OutlineThin: Style | None = None,
        Gray6SolidThin: Style | None = None,
        Gray6Dashed: Style | None = None,
        Gray6DashedBold: Style | None = None,
        Gray6DashedThin: Style | None = None,
        Gray6Dotted: Style | None = None,
        Gray6DottedBold: Style | None = None,
        Gray6DottedThin: Style | None = None,
        Gray7: Style | None = None,
        Gray7Bordered: Style | None = None,
        Gray7Bold: Style | None = None,
        Gray7Thin: Style | None = None,
        Gray7Flat: Style | None = None,
        Gray7Outline: Style | None = None,
        Gray7Solid: Style | None = None,
        Gray7OutlineBold: Style | None = None,
        Gray7SolidBold: Style | None = None,
        Gray7OutlineThin: Style | None = None,
        Gray7SolidThin: Style | None = None,
        Gray7Dashed: Style | None = None,
        Gray7DashedBold: Style | None = None,
        Gray7DashedThin: Style | None = None,
        Gray7Dotted: Style | None = None,
        Gray7DottedBold: Style | None = None,
        Gray7DottedThin: Style | None = None,
        Gray8: Style | None = None,
        Gray8Bordered: Style | None = None,
        Gray8Bold: Style | None = None,
        Gray8Thin: Style | None = None,
        Gray8Flat: Style | None = None,
        Gray8Outline: Style | None = None,
        Gray8Solid: Style | None = None,
        Gray8OutlineBold: Style | None = None,
        Gray8SolidBold: Style | None = None,
        Gray8OutlineThin: Style | None = None,
        Gray8SolidThin: Style | None = None,
        Gray8Dashed: Style | None = None,
        Gray8DashedBold: Style | None = None,
        Gray8DashedThin: Style | None = None,
        Gray8Dotted: Style | None = None,
        Gray8DottedBold: Style | None = None,
        Gray8DottedThin: Style | None = None,
        Black: Style | None = None,
        BlackBordered: Style | None = None,
        BlackBold: Style | None = None,
        BlackThin: Style | None = None,
        BlackFlat: Style | None = None,
        BlackOutline: Style | None = None,
        BlackSolid: Style | None = None,
        BlackOutlineBold: Style | None = None,
        BlackSolidBold: Style | None = None,
        BlackOutlineThin: Style | None = None,
        BlackSolidThin: Style | None = None,
        BlackDashed: Style | None = None,
        BlackDashedBold: Style | None = None,
        BlackDashedThin: Style | None = None,
        BlackDotted: Style | None = None,
        BlackDottedBold: Style | None = None,
        BlackDottedThin: Style | None = None,
        GrayNeutral: Style | None = None,
        GrayNeutralFlat: Style | None = None,
        PrimaryNeutral: Style | None = None,
        PrimaryNeutralFlat: Style | None = None,
        SecondaryNeutral: Style | None = None,
        SecondaryNeutralFlat: Style | None = None,
        AccentNeutral: Style | None = None,
        AccentNeutralFlat: Style | None = None,
        WarningNeutral: Style | None = None,
        WarningNeutralFlat: Style | None = None,
        DangerNeutral: Style | None = None,
        DangerNeutralFlat: Style | None = None,
        SuccessNeutral: Style | None = None,
        SuccessNeutralFlat: Style | None = None,
        MutedNeutral: Style | None = None,
        MutedNeutralFlat: Style | None = None,
        BlueNeutral: Style | None = None,
        BlueNeutralFlat: Style | None = None,
        GreenNeutral: Style | None = None,
        GreenNeutralFlat: Style | None = None,
        RedNeutral: Style | None = None,
        RedNeutralFlat: Style | None = None,
        OrangeNeutral: Style | None = None,
        OrangeNeutralFlat: Style | None = None,
        AmberNeutral: Style | None = None,
        AmberNeutralFlat: Style | None = None,
        PurpleNeutral: Style | None = None,
        PurpleNeutralFlat: Style | None = None,
        TealNeutral: Style | None = None,
        TealNeutralFlat: Style | None = None,
        PinkNeutral: Style | None = None,
        PinkNeutralFlat: Style | None = None,
        CyanNeutral: Style | None = None,
        CyanNeutralFlat: Style | None = None,
        YellowNeutral: Style | None = None,
        YellowNeutralFlat: Style | None = None,
        MagentaNeutral: Style | None = None,
        MagentaNeutralFlat: Style | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """Create a new copy of preset styles with updated attributes.

        Args:
            **kwargs: Additional style attributes to update.

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs", "__class__"} and v is not None}
        return super().patch(**passed, **kwargs)

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Intercept attribute access to raise AttributeError for unsupported semantic roles.

        Args:
            name (str): Attribute name being accessed.

        Returns:
            Any: Attribute value if defined.

        Raises:
            AttributeError: If accessing an unsupported danger or success style.
        """
        val = super().__getattribute__(name)
        if (name.startswith("Danger") or name.startswith("Success")) and val is None:
            raise AttributeError(f"{self.__class__.__name__} has no {name} style.")
        return val


def _create_monochrome_styles() -> MonochromeStyles:
    """Generate monochrome preset styles.

    Returns:
        MonochromeStyles: Monochrome preset styles instance.
    """
    black = MonochromeColors.Black
    gray1 = MonochromeColors.Gray1
    gray2 = MonochromeColors.Gray2
    gray3 = MonochromeColors.Gray3
    gray4 = MonochromeColors.Gray4
    gray5 = MonochromeColors.Gray5
    gray6 = MonochromeColors.Gray6
    gray7 = MonochromeColors.Gray7
    gray8 = MonochromeColors.Gray8
    white = MonochromeColors.White

    p_v = _make_variants(
        white,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )
    p_v["flat"] = Style(
        supports={"shape", "icon"},
        shape_fill_color=black,
        shape_line_color=MonochromeColors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
        icon_color=black,
        icon_style="regular",
    )

    s_v = _make_variants(
        gray2,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )

    a_v = _make_variants(
        black,
        border_color=black,
        default_text_color=white,
        line_color=black,
    )

    m_v = _make_variants(
        gray1,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )

    l_v = _make_variants(
        white,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )
    d_v = _make_variants(
        gray8,
        border_color=black,
        default_text_color=gray8,
        line_color=black,
    )
    n_v = _make_variants(
        gray2,
        border_color=gray5,
        default_text_color=gray8,
        line_color=gray5,
    )

    role_variants = {
        "Primary": p_v,
        "Secondary": s_v,
        "Accent": a_v,
        "Muted": m_v,
        "Light": l_v,
        "Neutral": n_v,
        "Dark": d_v,
    }

    styles_dict: dict[str, Any] = {
        "width": 140,
        "height": 70,
        "dpi": 100,
        "colors": MonochromeColors,
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
        "Canvas": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
        "CanvasFlat": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
    }

    for role_name, v in role_variants.items():
        styles_dict[role_name] = v["normal"]
        styles_dict[f"{role_name}Bordered"] = v["bordered"]
        styles_dict[f"{role_name}Bold"] = v["bold"]
        styles_dict[f"{role_name}Thin"] = v["thin"]
        styles_dict[f"{role_name}Flat"] = v["flat"]
        styles_dict[f"{role_name}Outline"] = v["outline"]
        styles_dict[f"{role_name}Solid"] = v["solid"]
        styles_dict[f"{role_name}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{role_name}SolidBold"] = v["solid_bold"]
        styles_dict[f"{role_name}OutlineThin"] = v["outline_thin"]
        styles_dict[f"{role_name}SolidThin"] = v["solid_thin"]
        styles_dict[f"{role_name}Dashed"] = v["dashed"]
        styles_dict[f"{role_name}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{role_name}DashedThin"] = v["dashed_thin"]
        styles_dict[f"{role_name}Dotted"] = v["dotted"]
        styles_dict[f"{role_name}DottedBold"] = v["dotted_bold"]
        styles_dict[f"{role_name}DottedThin"] = v["dotted_thin"]

    color_variants = {
        "White": _make_variants(white, border_color=black),
        "Gray1": _make_variants(gray1, border_color=gray5),
        "Gray2": _make_variants(gray2, border_color=gray5),
        "Gray3": _make_variants(gray3, border_color=gray6),
        "Gray4": _make_variants(gray4, border_color=black),
        "Gray5": _make_variants(gray5, border_color=black),
        "Gray6": _make_variants(gray6, border_color=black),
        "Gray7": _make_variants(gray7, border_color=black),
        "Gray8": _make_variants(gray8, border_color=black),
        "Black": _make_variants(black, border_color=black),
    }

    for cname, v in color_variants.items():
        styles_dict[cname] = v["normal"]
        styles_dict[f"{cname}Bordered"] = v["bordered"]
        styles_dict[f"{cname}Bold"] = v["bold"]
        styles_dict[f"{cname}Thin"] = v["thin"]
        styles_dict[f"{cname}Flat"] = v["flat"]
        styles_dict[f"{cname}Outline"] = v["outline"]
        styles_dict[f"{cname}Solid"] = v["solid"]
        styles_dict[f"{cname}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{cname}SolidBold"] = v["solid_bold"]
        styles_dict[f"{cname}OutlineThin"] = v["outline_thin"]
        styles_dict[f"{cname}SolidThin"] = v["solid_thin"]
        styles_dict[f"{cname}Dashed"] = v["dashed"]
        styles_dict[f"{cname}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{cname}DashedThin"] = v["dashed_thin"]
        styles_dict[f"{cname}Dotted"] = v["dotted"]
        styles_dict[f"{cname}DottedBold"] = v["dotted_bold"]
        styles_dict[f"{cname}DottedThin"] = v["dotted_thin"]

    # Neutral Card Styles (Bordered & Flat)
    neutral_card, neutral_flat = _make_neutral_card(gray2, border_color=gray5, text_color=gray8)
    styles_dict["GrayNeutral"] = neutral_card
    styles_dict["GrayNeutralFlat"] = neutral_flat
    styles_dict["Neutral"] = neutral_card
    styles_dict["NeutralBordered"] = neutral_card
    styles_dict["NeutralFlat"] = neutral_flat

    neutral_keys = [
        "PrimaryNeutral",
        "PrimaryNeutralFlat",
        "SecondaryNeutral",
        "SecondaryNeutralFlat",
        "AccentNeutral",
        "AccentNeutralFlat",
        "WarningNeutral",
        "WarningNeutralFlat",
        "DangerNeutral",
        "DangerNeutralFlat",
        "SuccessNeutral",
        "SuccessNeutralFlat",
        "MutedNeutral",
        "MutedNeutralFlat",
        "BlueNeutral",
        "BlueNeutralFlat",
        "GreenNeutral",
        "GreenNeutralFlat",
        "RedNeutral",
        "RedNeutralFlat",
        "OrangeNeutral",
        "OrangeNeutralFlat",
        "AmberNeutral",
        "AmberNeutralFlat",
        "PurpleNeutral",
        "PurpleNeutralFlat",
        "TealNeutral",
        "TealNeutralFlat",
        "PinkNeutral",
        "PinkNeutralFlat",
        "CyanNeutral",
        "CyanNeutralFlat",
        "YellowNeutral",
        "YellowNeutralFlat",
        "MagentaNeutral",
        "MagentaNeutralFlat",
    ]
    for k in neutral_keys:
        styles_dict[k] = neutral_flat if k.endswith("Flat") else neutral_card

    return MonochromeStyles(**styles_dict)


_monochrome_styles: MonochromeStyles = _create_monochrome_styles()
MonochromeStyles.register_default_instance(_monochrome_styles)

__all__ = [
    "MonochromeStyles",
]
