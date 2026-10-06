# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Google Sheets & Slides preset styles module."""

from __future__ import annotations

import warnings
from typing import Any, Self

from drawlib._core.l3_colors import BaseColors, Color, ColorType
from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import BaseStyles, Style
from drawlib._preset_colors import GoogleColors
from drawlib._preset_styles._utils import _make_neutral_card, _make_variants

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class GoogleStyles(BaseStyles):
    """Google preset styles with complete typing for IDE autocompletion."""

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
    Danger: Style
    DangerBordered: Style
    DangerBold: Style
    DangerThin: Style
    DangerFlat: Style
    DangerOutline: Style
    DangerSolid: Style
    DangerOutlineBold: Style
    DangerSolidBold: Style
    DangerOutlineThin: Style
    DangerSolidThin: Style
    DangerDashed: Style
    DangerDashedBold: Style
    DangerDashedThin: Style
    DangerDotted: Style
    DangerDottedBold: Style
    DangerDottedThin: Style
    Success: Style
    SuccessBordered: Style
    SuccessBold: Style
    SuccessThin: Style
    SuccessFlat: Style
    SuccessOutline: Style
    SuccessSolid: Style
    SuccessOutlineBold: Style
    SuccessSolidBold: Style
    SuccessOutlineThin: Style
    SuccessSolidThin: Style
    SuccessDashed: Style
    SuccessDashedBold: Style
    SuccessDashedThin: Style
    SuccessDotted: Style
    SuccessDottedBold: Style
    SuccessDottedThin: Style
    Warning: Style
    WarningBordered: Style
    WarningBold: Style
    WarningThin: Style
    WarningFlat: Style
    WarningOutline: Style
    WarningSolid: Style
    WarningOutlineBold: Style
    WarningSolidBold: Style
    WarningOutlineThin: Style
    WarningSolidThin: Style
    WarningDashed: Style
    WarningDashedBold: Style
    WarningDashedThin: Style
    WarningDotted: Style
    WarningDottedBold: Style
    WarningDottedThin: Style
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
    CornflowerBlue1: Style
    CornflowerBlue1Bordered: Style
    CornflowerBlue1Bold: Style
    CornflowerBlue1Thin: Style
    CornflowerBlue1Flat: Style
    CornflowerBlue1Outline: Style
    CornflowerBlue1Solid: Style
    CornflowerBlue1OutlineBold: Style
    CornflowerBlue1SolidBold: Style
    CornflowerBlue1OutlineThin: Style
    CornflowerBlue1SolidThin: Style
    CornflowerBlue1Dashed: Style
    CornflowerBlue1DashedBold: Style
    CornflowerBlue1DashedThin: Style
    CornflowerBlue1Dotted: Style
    CornflowerBlue1DottedBold: Style
    CornflowerBlue1DottedThin: Style
    CornflowerBlue2: Style
    CornflowerBlue2Bordered: Style
    CornflowerBlue2Bold: Style
    CornflowerBlue2Thin: Style
    CornflowerBlue2Flat: Style
    CornflowerBlue2Outline: Style
    CornflowerBlue2Solid: Style
    CornflowerBlue2OutlineBold: Style
    CornflowerBlue2SolidBold: Style
    CornflowerBlue2OutlineThin: Style
    CornflowerBlue2SolidThin: Style
    CornflowerBlue2Dashed: Style
    CornflowerBlue2DashedBold: Style
    CornflowerBlue2DashedThin: Style
    CornflowerBlue2Dotted: Style
    CornflowerBlue2DottedBold: Style
    CornflowerBlue2DottedThin: Style
    CornflowerBlue3: Style
    CornflowerBlue3Bordered: Style
    CornflowerBlue3Bold: Style
    CornflowerBlue3Thin: Style
    CornflowerBlue3Flat: Style
    CornflowerBlue3Outline: Style
    CornflowerBlue3Solid: Style
    CornflowerBlue3OutlineBold: Style
    CornflowerBlue3SolidBold: Style
    CornflowerBlue3OutlineThin: Style
    CornflowerBlue3SolidThin: Style
    CornflowerBlue3Dashed: Style
    CornflowerBlue3DashedBold: Style
    CornflowerBlue3DashedThin: Style
    CornflowerBlue3Dotted: Style
    CornflowerBlue3DottedBold: Style
    CornflowerBlue3DottedThin: Style
    CornflowerBlue4: Style
    CornflowerBlue4Bordered: Style
    CornflowerBlue4Bold: Style
    CornflowerBlue4Thin: Style
    CornflowerBlue4Flat: Style
    CornflowerBlue4Outline: Style
    CornflowerBlue4Solid: Style
    CornflowerBlue4OutlineBold: Style
    CornflowerBlue4SolidBold: Style
    CornflowerBlue4OutlineThin: Style
    CornflowerBlue4SolidThin: Style
    CornflowerBlue4Dashed: Style
    CornflowerBlue4DashedBold: Style
    CornflowerBlue4DashedThin: Style
    CornflowerBlue4Dotted: Style
    CornflowerBlue4DottedBold: Style
    CornflowerBlue4DottedThin: Style
    CornflowerBlue5: Style
    CornflowerBlue5Bordered: Style
    CornflowerBlue5Bold: Style
    CornflowerBlue5Thin: Style
    CornflowerBlue5Flat: Style
    CornflowerBlue5Outline: Style
    CornflowerBlue5Solid: Style
    CornflowerBlue5OutlineBold: Style
    CornflowerBlue5SolidBold: Style
    CornflowerBlue5OutlineThin: Style
    CornflowerBlue5SolidThin: Style
    CornflowerBlue5Dashed: Style
    CornflowerBlue5DashedBold: Style
    CornflowerBlue5DashedThin: Style
    CornflowerBlue5Dotted: Style
    CornflowerBlue5DottedBold: Style
    CornflowerBlue5DottedThin: Style
    CornflowerBlue6: Style
    CornflowerBlue6Bordered: Style
    CornflowerBlue6Bold: Style
    CornflowerBlue6Thin: Style
    CornflowerBlue6Flat: Style
    CornflowerBlue6Outline: Style
    CornflowerBlue6Solid: Style
    CornflowerBlue6OutlineBold: Style
    CornflowerBlue6SolidBold: Style
    CornflowerBlue6OutlineThin: Style
    CornflowerBlue6SolidThin: Style
    CornflowerBlue6Dashed: Style
    CornflowerBlue6DashedBold: Style
    CornflowerBlue6DashedThin: Style
    CornflowerBlue6Dotted: Style
    CornflowerBlue6DottedBold: Style
    CornflowerBlue6DottedThin: Style
    Blue1: Style
    Blue1Bordered: Style
    Blue1Bold: Style
    Blue1Thin: Style
    Blue1Flat: Style
    Blue1Outline: Style
    Blue1Solid: Style
    Blue1OutlineBold: Style
    Blue1SolidBold: Style
    Blue1OutlineThin: Style
    Blue1SolidThin: Style
    Blue1Dashed: Style
    Blue1DashedBold: Style
    Blue1DashedThin: Style
    Blue1Dotted: Style
    Blue1DottedBold: Style
    Blue1DottedThin: Style
    Blue2: Style
    Blue2Bordered: Style
    Blue2Bold: Style
    Blue2Thin: Style
    Blue2Flat: Style
    Blue2Outline: Style
    Blue2Solid: Style
    Blue2OutlineBold: Style
    Blue2SolidBold: Style
    Blue2OutlineThin: Style
    Blue2SolidThin: Style
    Blue2Dashed: Style
    Blue2DashedBold: Style
    Blue2DashedThin: Style
    Blue2Dotted: Style
    Blue2DottedBold: Style
    Blue2DottedThin: Style
    Blue3: Style
    Blue3Bordered: Style
    Blue3Bold: Style
    Blue3Thin: Style
    Blue3Flat: Style
    Blue3Outline: Style
    Blue3Solid: Style
    Blue3OutlineBold: Style
    Blue3SolidBold: Style
    Blue3OutlineThin: Style
    Blue3SolidThin: Style
    Blue3Dashed: Style
    Blue3DashedBold: Style
    Blue3DashedThin: Style
    Blue3Dotted: Style
    Blue3DottedBold: Style
    Blue3DottedThin: Style
    Blue4: Style
    Blue4Bordered: Style
    Blue4Bold: Style
    Blue4Thin: Style
    Blue4Flat: Style
    Blue4Outline: Style
    Blue4Solid: Style
    Blue4OutlineBold: Style
    Blue4SolidBold: Style
    Blue4OutlineThin: Style
    Blue4SolidThin: Style
    Blue4Dashed: Style
    Blue4DashedBold: Style
    Blue4DashedThin: Style
    Blue4Dotted: Style
    Blue4DottedBold: Style
    Blue4DottedThin: Style
    Blue5: Style
    Blue5Bordered: Style
    Blue5Bold: Style
    Blue5Thin: Style
    Blue5Flat: Style
    Blue5Outline: Style
    Blue5Solid: Style
    Blue5OutlineBold: Style
    Blue5SolidBold: Style
    Blue5OutlineThin: Style
    Blue5SolidThin: Style
    Blue5Dashed: Style
    Blue5DashedBold: Style
    Blue5DashedThin: Style
    Blue5Dotted: Style
    Blue5DottedBold: Style
    Blue5DottedThin: Style
    Blue6: Style
    Blue6Bordered: Style
    Blue6Bold: Style
    Blue6Thin: Style
    Blue6Flat: Style
    Blue6Outline: Style
    Blue6Solid: Style
    Blue6OutlineBold: Style
    Blue6SolidBold: Style
    Blue6OutlineThin: Style
    Blue6SolidThin: Style
    Blue6Dashed: Style
    Blue6DashedBold: Style
    Blue6DashedThin: Style
    Blue6Dotted: Style
    Blue6DottedBold: Style
    Blue6DottedThin: Style
    Red1: Style
    Red1Bordered: Style
    Red1Bold: Style
    Red1Thin: Style
    Red1Flat: Style
    Red1Outline: Style
    Red1Solid: Style
    Red1OutlineBold: Style
    Red1SolidBold: Style
    Red1OutlineThin: Style
    Red1SolidThin: Style
    Red1Dashed: Style
    Red1DashedBold: Style
    Red1DashedThin: Style
    Red1Dotted: Style
    Red1DottedBold: Style
    Red1DottedThin: Style
    Red2: Style
    Red2Bordered: Style
    Red2Bold: Style
    Red2Thin: Style
    Red2Flat: Style
    Red2Outline: Style
    Red2Solid: Style
    Red2OutlineBold: Style
    Red2SolidBold: Style
    Red2OutlineThin: Style
    Red2SolidThin: Style
    Red2Dashed: Style
    Red2DashedBold: Style
    Red2DashedThin: Style
    Red2Dotted: Style
    Red2DottedBold: Style
    Red2DottedThin: Style
    Red3: Style
    Red3Bordered: Style
    Red3Bold: Style
    Red3Thin: Style
    Red3Flat: Style
    Red3Outline: Style
    Red3Solid: Style
    Red3OutlineBold: Style
    Red3SolidBold: Style
    Red3OutlineThin: Style
    Red3SolidThin: Style
    Red3Dashed: Style
    Red3DashedBold: Style
    Red3DashedThin: Style
    Red3Dotted: Style
    Red3DottedBold: Style
    Red3DottedThin: Style
    Red4: Style
    Red4Bordered: Style
    Red4Bold: Style
    Red4Thin: Style
    Red4Flat: Style
    Red4Outline: Style
    Red4Solid: Style
    Red4OutlineBold: Style
    Red4SolidBold: Style
    Red4OutlineThin: Style
    Red4SolidThin: Style
    Red4Dashed: Style
    Red4DashedBold: Style
    Red4DashedThin: Style
    Red4Dotted: Style
    Red4DottedBold: Style
    Red4DottedThin: Style
    Red5: Style
    Red5Bordered: Style
    Red5Bold: Style
    Red5Thin: Style
    Red5Flat: Style
    Red5Outline: Style
    Red5Solid: Style
    Red5OutlineBold: Style
    Red5SolidBold: Style
    Red5OutlineThin: Style
    Red5SolidThin: Style
    Red5Dashed: Style
    Red5DashedBold: Style
    Red5DashedThin: Style
    Red5Dotted: Style
    Red5DottedBold: Style
    Red5DottedThin: Style
    Red6: Style
    Red6Bordered: Style
    Red6Bold: Style
    Red6Thin: Style
    Red6Flat: Style
    Red6Outline: Style
    Red6Solid: Style
    Red6OutlineBold: Style
    Red6SolidBold: Style
    Red6OutlineThin: Style
    Red6SolidThin: Style
    Red6Dashed: Style
    Red6DashedBold: Style
    Red6DashedThin: Style
    Red6Dotted: Style
    Red6DottedBold: Style
    Red6DottedThin: Style
    RedBerry1: Style
    RedBerry1Bordered: Style
    RedBerry1Bold: Style
    RedBerry1Thin: Style
    RedBerry1Flat: Style
    RedBerry1Outline: Style
    RedBerry1Solid: Style
    RedBerry1OutlineBold: Style
    RedBerry1SolidBold: Style
    RedBerry1OutlineThin: Style
    RedBerry1SolidThin: Style
    RedBerry1Dashed: Style
    RedBerry1DashedBold: Style
    RedBerry1DashedThin: Style
    RedBerry1Dotted: Style
    RedBerry1DottedBold: Style
    RedBerry1DottedThin: Style
    RedBerry2: Style
    RedBerry2Bordered: Style
    RedBerry2Bold: Style
    RedBerry2Thin: Style
    RedBerry2Flat: Style
    RedBerry2Outline: Style
    RedBerry2Solid: Style
    RedBerry2OutlineBold: Style
    RedBerry2SolidBold: Style
    RedBerry2OutlineThin: Style
    RedBerry2SolidThin: Style
    RedBerry2Dashed: Style
    RedBerry2DashedBold: Style
    RedBerry2DashedThin: Style
    RedBerry2Dotted: Style
    RedBerry2DottedBold: Style
    RedBerry2DottedThin: Style
    RedBerry3: Style
    RedBerry3Bordered: Style
    RedBerry3Bold: Style
    RedBerry3Thin: Style
    RedBerry3Flat: Style
    RedBerry3Outline: Style
    RedBerry3Solid: Style
    RedBerry3OutlineBold: Style
    RedBerry3SolidBold: Style
    RedBerry3OutlineThin: Style
    RedBerry3SolidThin: Style
    RedBerry3Dashed: Style
    RedBerry3DashedBold: Style
    RedBerry3DashedThin: Style
    RedBerry3Dotted: Style
    RedBerry3DottedBold: Style
    RedBerry3DottedThin: Style
    RedBerry4: Style
    RedBerry4Bordered: Style
    RedBerry4Bold: Style
    RedBerry4Thin: Style
    RedBerry4Flat: Style
    RedBerry4Outline: Style
    RedBerry4Solid: Style
    RedBerry4OutlineBold: Style
    RedBerry4SolidBold: Style
    RedBerry4OutlineThin: Style
    RedBerry4SolidThin: Style
    RedBerry4Dashed: Style
    RedBerry4DashedBold: Style
    RedBerry4DashedThin: Style
    RedBerry4Dotted: Style
    RedBerry4DottedBold: Style
    RedBerry4DottedThin: Style
    RedBerry5: Style
    RedBerry5Bordered: Style
    RedBerry5Bold: Style
    RedBerry5Thin: Style
    RedBerry5Flat: Style
    RedBerry5Outline: Style
    RedBerry5Solid: Style
    RedBerry5OutlineBold: Style
    RedBerry5SolidBold: Style
    RedBerry5OutlineThin: Style
    RedBerry5SolidThin: Style
    RedBerry5Dashed: Style
    RedBerry5DashedBold: Style
    RedBerry5DashedThin: Style
    RedBerry5Dotted: Style
    RedBerry5DottedBold: Style
    RedBerry5DottedThin: Style
    RedBerry6: Style
    RedBerry6Bordered: Style
    RedBerry6Bold: Style
    RedBerry6Thin: Style
    RedBerry6Flat: Style
    RedBerry6Outline: Style
    RedBerry6Solid: Style
    RedBerry6OutlineBold: Style
    RedBerry6SolidBold: Style
    RedBerry6OutlineThin: Style
    RedBerry6SolidThin: Style
    RedBerry6Dashed: Style
    RedBerry6DashedBold: Style
    RedBerry6DashedThin: Style
    RedBerry6Dotted: Style
    RedBerry6DottedBold: Style
    RedBerry6DottedThin: Style
    Green1: Style
    Green1Bordered: Style
    Green1Bold: Style
    Green1Thin: Style
    Green1Flat: Style
    Green1Outline: Style
    Green1Solid: Style
    Green1OutlineBold: Style
    Green1SolidBold: Style
    Green1OutlineThin: Style
    Green1SolidThin: Style
    Green1Dashed: Style
    Green1DashedBold: Style
    Green1DashedThin: Style
    Green1Dotted: Style
    Green1DottedBold: Style
    Green1DottedThin: Style
    Green2: Style
    Green2Bordered: Style
    Green2Bold: Style
    Green2Thin: Style
    Green2Flat: Style
    Green2Outline: Style
    Green2Solid: Style
    Green2OutlineBold: Style
    Green2SolidBold: Style
    Green2OutlineThin: Style
    Green2SolidThin: Style
    Green2Dashed: Style
    Green2DashedBold: Style
    Green2DashedThin: Style
    Green2Dotted: Style
    Green2DottedBold: Style
    Green2DottedThin: Style
    Green3: Style
    Green3Bordered: Style
    Green3Bold: Style
    Green3Thin: Style
    Green3Flat: Style
    Green3Outline: Style
    Green3Solid: Style
    Green3OutlineBold: Style
    Green3SolidBold: Style
    Green3OutlineThin: Style
    Green3SolidThin: Style
    Green3Dashed: Style
    Green3DashedBold: Style
    Green3DashedThin: Style
    Green3Dotted: Style
    Green3DottedBold: Style
    Green3DottedThin: Style
    Green4: Style
    Green4Bordered: Style
    Green4Bold: Style
    Green4Thin: Style
    Green4Flat: Style
    Green4Outline: Style
    Green4Solid: Style
    Green4OutlineBold: Style
    Green4SolidBold: Style
    Green4OutlineThin: Style
    Green4SolidThin: Style
    Green4Dashed: Style
    Green4DashedBold: Style
    Green4DashedThin: Style
    Green4Dotted: Style
    Green4DottedBold: Style
    Green4DottedThin: Style
    Green5: Style
    Green5Bordered: Style
    Green5Bold: Style
    Green5Thin: Style
    Green5Flat: Style
    Green5Outline: Style
    Green5Solid: Style
    Green5OutlineBold: Style
    Green5SolidBold: Style
    Green5OutlineThin: Style
    Green5SolidThin: Style
    Green5Dashed: Style
    Green5DashedBold: Style
    Green5DashedThin: Style
    Green5Dotted: Style
    Green5DottedBold: Style
    Green5DottedThin: Style
    Green6: Style
    Green6Bordered: Style
    Green6Bold: Style
    Green6Thin: Style
    Green6Flat: Style
    Green6Outline: Style
    Green6Solid: Style
    Green6OutlineBold: Style
    Green6SolidBold: Style
    Green6OutlineThin: Style
    Green6SolidThin: Style
    Green6Dashed: Style
    Green6DashedBold: Style
    Green6DashedThin: Style
    Green6Dotted: Style
    Green6DottedBold: Style
    Green6DottedThin: Style
    Yellow1: Style
    Yellow1Bordered: Style
    Yellow1Bold: Style
    Yellow1Thin: Style
    Yellow1Flat: Style
    Yellow1Outline: Style
    Yellow1Solid: Style
    Yellow1OutlineBold: Style
    Yellow1SolidBold: Style
    Yellow1OutlineThin: Style
    Yellow1SolidThin: Style
    Yellow1Dashed: Style
    Yellow1DashedBold: Style
    Yellow1DashedThin: Style
    Yellow1Dotted: Style
    Yellow1DottedBold: Style
    Yellow1DottedThin: Style
    Yellow2: Style
    Yellow2Bordered: Style
    Yellow2Bold: Style
    Yellow2Thin: Style
    Yellow2Flat: Style
    Yellow2Outline: Style
    Yellow2Solid: Style
    Yellow2OutlineBold: Style
    Yellow2SolidBold: Style
    Yellow2OutlineThin: Style
    Yellow2SolidThin: Style
    Yellow2Dashed: Style
    Yellow2DashedBold: Style
    Yellow2DashedThin: Style
    Yellow2Dotted: Style
    Yellow2DottedBold: Style
    Yellow2DottedThin: Style
    Yellow3: Style
    Yellow3Bordered: Style
    Yellow3Bold: Style
    Yellow3Thin: Style
    Yellow3Flat: Style
    Yellow3Outline: Style
    Yellow3Solid: Style
    Yellow3OutlineBold: Style
    Yellow3SolidBold: Style
    Yellow3OutlineThin: Style
    Yellow3SolidThin: Style
    Yellow3Dashed: Style
    Yellow3DashedBold: Style
    Yellow3DashedThin: Style
    Yellow3Dotted: Style
    Yellow3DottedBold: Style
    Yellow3DottedThin: Style
    Yellow4: Style
    Yellow4Bordered: Style
    Yellow4Bold: Style
    Yellow4Thin: Style
    Yellow4Flat: Style
    Yellow4Outline: Style
    Yellow4Solid: Style
    Yellow4OutlineBold: Style
    Yellow4SolidBold: Style
    Yellow4OutlineThin: Style
    Yellow4SolidThin: Style
    Yellow4Dashed: Style
    Yellow4DashedBold: Style
    Yellow4DashedThin: Style
    Yellow4Dotted: Style
    Yellow4DottedBold: Style
    Yellow4DottedThin: Style
    Yellow5: Style
    Yellow5Bordered: Style
    Yellow5Bold: Style
    Yellow5Thin: Style
    Yellow5Flat: Style
    Yellow5Outline: Style
    Yellow5Solid: Style
    Yellow5OutlineBold: Style
    Yellow5SolidBold: Style
    Yellow5OutlineThin: Style
    Yellow5SolidThin: Style
    Yellow5Dashed: Style
    Yellow5DashedBold: Style
    Yellow5DashedThin: Style
    Yellow5Dotted: Style
    Yellow5DottedBold: Style
    Yellow5DottedThin: Style
    Yellow6: Style
    Yellow6Bordered: Style
    Yellow6Bold: Style
    Yellow6Thin: Style
    Yellow6Flat: Style
    Yellow6Outline: Style
    Yellow6Solid: Style
    Yellow6OutlineBold: Style
    Yellow6SolidBold: Style
    Yellow6OutlineThin: Style
    Yellow6SolidThin: Style
    Yellow6Dashed: Style
    Yellow6DashedBold: Style
    Yellow6DashedThin: Style
    Yellow6Dotted: Style
    Yellow6DottedBold: Style
    Yellow6DottedThin: Style
    Orange1: Style
    Orange1Bordered: Style
    Orange1Bold: Style
    Orange1Thin: Style
    Orange1Flat: Style
    Orange1Outline: Style
    Orange1Solid: Style
    Orange1OutlineBold: Style
    Orange1SolidBold: Style
    Orange1OutlineThin: Style
    Orange1SolidThin: Style
    Orange1Dashed: Style
    Orange1DashedBold: Style
    Orange1DashedThin: Style
    Orange1Dotted: Style
    Orange1DottedBold: Style
    Orange1DottedThin: Style
    Orange2: Style
    Orange2Bordered: Style
    Orange2Bold: Style
    Orange2Thin: Style
    Orange2Flat: Style
    Orange2Outline: Style
    Orange2Solid: Style
    Orange2OutlineBold: Style
    Orange2SolidBold: Style
    Orange2OutlineThin: Style
    Orange2SolidThin: Style
    Orange2Dashed: Style
    Orange2DashedBold: Style
    Orange2DashedThin: Style
    Orange2Dotted: Style
    Orange2DottedBold: Style
    Orange2DottedThin: Style
    Orange3: Style
    Orange3Bordered: Style
    Orange3Bold: Style
    Orange3Thin: Style
    Orange3Flat: Style
    Orange3Outline: Style
    Orange3Solid: Style
    Orange3OutlineBold: Style
    Orange3SolidBold: Style
    Orange3OutlineThin: Style
    Orange3SolidThin: Style
    Orange3Dashed: Style
    Orange3DashedBold: Style
    Orange3DashedThin: Style
    Orange3Dotted: Style
    Orange3DottedBold: Style
    Orange3DottedThin: Style
    Orange4: Style
    Orange4Bordered: Style
    Orange4Bold: Style
    Orange4Thin: Style
    Orange4Flat: Style
    Orange4Outline: Style
    Orange4Solid: Style
    Orange4OutlineBold: Style
    Orange4SolidBold: Style
    Orange4OutlineThin: Style
    Orange4SolidThin: Style
    Orange4Dashed: Style
    Orange4DashedBold: Style
    Orange4DashedThin: Style
    Orange4Dotted: Style
    Orange4DottedBold: Style
    Orange4DottedThin: Style
    Orange5: Style
    Orange5Bordered: Style
    Orange5Bold: Style
    Orange5Thin: Style
    Orange5Flat: Style
    Orange5Outline: Style
    Orange5Solid: Style
    Orange5OutlineBold: Style
    Orange5SolidBold: Style
    Orange5OutlineThin: Style
    Orange5SolidThin: Style
    Orange5Dashed: Style
    Orange5DashedBold: Style
    Orange5DashedThin: Style
    Orange5Dotted: Style
    Orange5DottedBold: Style
    Orange5DottedThin: Style
    Orange6: Style
    Orange6Bordered: Style
    Orange6Bold: Style
    Orange6Thin: Style
    Orange6Flat: Style
    Orange6Outline: Style
    Orange6Solid: Style
    Orange6OutlineBold: Style
    Orange6SolidBold: Style
    Orange6OutlineThin: Style
    Orange6SolidThin: Style
    Orange6Dashed: Style
    Orange6DashedBold: Style
    Orange6DashedThin: Style
    Orange6Dotted: Style
    Orange6DottedBold: Style
    Orange6DottedThin: Style
    Cyan1: Style
    Cyan1Bordered: Style
    Cyan1Bold: Style
    Cyan1Thin: Style
    Cyan1Flat: Style
    Cyan1Outline: Style
    Cyan1Solid: Style
    Cyan1OutlineBold: Style
    Cyan1SolidBold: Style
    Cyan1OutlineThin: Style
    Cyan1SolidThin: Style
    Cyan1Dashed: Style
    Cyan1DashedBold: Style
    Cyan1DashedThin: Style
    Cyan1Dotted: Style
    Cyan1DottedBold: Style
    Cyan1DottedThin: Style
    Cyan2: Style
    Cyan2Bordered: Style
    Cyan2Bold: Style
    Cyan2Thin: Style
    Cyan2Flat: Style
    Cyan2Outline: Style
    Cyan2Solid: Style
    Cyan2OutlineBold: Style
    Cyan2SolidBold: Style
    Cyan2OutlineThin: Style
    Cyan2SolidThin: Style
    Cyan2Dashed: Style
    Cyan2DashedBold: Style
    Cyan2DashedThin: Style
    Cyan2Dotted: Style
    Cyan2DottedBold: Style
    Cyan2DottedThin: Style
    Cyan3: Style
    Cyan3Bordered: Style
    Cyan3Bold: Style
    Cyan3Thin: Style
    Cyan3Flat: Style
    Cyan3Outline: Style
    Cyan3Solid: Style
    Cyan3OutlineBold: Style
    Cyan3SolidBold: Style
    Cyan3OutlineThin: Style
    Cyan3SolidThin: Style
    Cyan3Dashed: Style
    Cyan3DashedBold: Style
    Cyan3DashedThin: Style
    Cyan3Dotted: Style
    Cyan3DottedBold: Style
    Cyan3DottedThin: Style
    Cyan4: Style
    Cyan4Bordered: Style
    Cyan4Bold: Style
    Cyan4Thin: Style
    Cyan4Flat: Style
    Cyan4Outline: Style
    Cyan4Solid: Style
    Cyan4OutlineBold: Style
    Cyan4SolidBold: Style
    Cyan4OutlineThin: Style
    Cyan4SolidThin: Style
    Cyan4Dashed: Style
    Cyan4DashedBold: Style
    Cyan4DashedThin: Style
    Cyan4Dotted: Style
    Cyan4DottedBold: Style
    Cyan4DottedThin: Style
    Cyan5: Style
    Cyan5Bordered: Style
    Cyan5Bold: Style
    Cyan5Thin: Style
    Cyan5Flat: Style
    Cyan5Outline: Style
    Cyan5Solid: Style
    Cyan5OutlineBold: Style
    Cyan5SolidBold: Style
    Cyan5OutlineThin: Style
    Cyan5SolidThin: Style
    Cyan5Dashed: Style
    Cyan5DashedBold: Style
    Cyan5DashedThin: Style
    Cyan5Dotted: Style
    Cyan5DottedBold: Style
    Cyan5DottedThin: Style
    Cyan6: Style
    Cyan6Bordered: Style
    Cyan6Bold: Style
    Cyan6Thin: Style
    Cyan6Flat: Style
    Cyan6Outline: Style
    Cyan6Solid: Style
    Cyan6OutlineBold: Style
    Cyan6SolidBold: Style
    Cyan6OutlineThin: Style
    Cyan6SolidThin: Style
    Cyan6Dashed: Style
    Cyan6DashedBold: Style
    Cyan6DashedThin: Style
    Cyan6Dotted: Style
    Cyan6DottedBold: Style
    Cyan6DottedThin: Style
    Purple1: Style
    Purple1Bordered: Style
    Purple1Bold: Style
    Purple1Thin: Style
    Purple1Flat: Style
    Purple1Outline: Style
    Purple1Solid: Style
    Purple1OutlineBold: Style
    Purple1SolidBold: Style
    Purple1OutlineThin: Style
    Purple1SolidThin: Style
    Purple1Dashed: Style
    Purple1DashedBold: Style
    Purple1DashedThin: Style
    Purple1Dotted: Style
    Purple1DottedBold: Style
    Purple1DottedThin: Style
    Purple2: Style
    Purple2Bordered: Style
    Purple2Bold: Style
    Purple2Thin: Style
    Purple2Flat: Style
    Purple2Outline: Style
    Purple2Solid: Style
    Purple2OutlineBold: Style
    Purple2SolidBold: Style
    Purple2OutlineThin: Style
    Purple2SolidThin: Style
    Purple2Dashed: Style
    Purple2DashedBold: Style
    Purple2DashedThin: Style
    Purple2Dotted: Style
    Purple2DottedBold: Style
    Purple2DottedThin: Style
    Purple3: Style
    Purple3Bordered: Style
    Purple3Bold: Style
    Purple3Thin: Style
    Purple3Flat: Style
    Purple3Outline: Style
    Purple3Solid: Style
    Purple3OutlineBold: Style
    Purple3SolidBold: Style
    Purple3OutlineThin: Style
    Purple3SolidThin: Style
    Purple3Dashed: Style
    Purple3DashedBold: Style
    Purple3DashedThin: Style
    Purple3Dotted: Style
    Purple3DottedBold: Style
    Purple3DottedThin: Style
    Purple4: Style
    Purple4Bordered: Style
    Purple4Bold: Style
    Purple4Thin: Style
    Purple4Flat: Style
    Purple4Outline: Style
    Purple4Solid: Style
    Purple4OutlineBold: Style
    Purple4SolidBold: Style
    Purple4OutlineThin: Style
    Purple4SolidThin: Style
    Purple4Dashed: Style
    Purple4DashedBold: Style
    Purple4DashedThin: Style
    Purple4Dotted: Style
    Purple4DottedBold: Style
    Purple4DottedThin: Style
    Purple5: Style
    Purple5Bordered: Style
    Purple5Bold: Style
    Purple5Thin: Style
    Purple5Flat: Style
    Purple5Outline: Style
    Purple5Solid: Style
    Purple5OutlineBold: Style
    Purple5SolidBold: Style
    Purple5OutlineThin: Style
    Purple5SolidThin: Style
    Purple5Dashed: Style
    Purple5DashedBold: Style
    Purple5DashedThin: Style
    Purple5Dotted: Style
    Purple5DottedBold: Style
    Purple5DottedThin: Style
    Purple6: Style
    Purple6Bordered: Style
    Purple6Bold: Style
    Purple6Thin: Style
    Purple6Flat: Style
    Purple6Outline: Style
    Purple6Solid: Style
    Purple6OutlineBold: Style
    Purple6SolidBold: Style
    Purple6OutlineThin: Style
    Purple6SolidThin: Style
    Purple6Dashed: Style
    Purple6DashedBold: Style
    Purple6DashedThin: Style
    Purple6Dotted: Style
    Purple6DottedBold: Style
    Purple6DottedThin: Style
    Magenta1: Style
    Magenta1Bordered: Style
    Magenta1Bold: Style
    Magenta1Thin: Style
    Magenta1Flat: Style
    Magenta1Outline: Style
    Magenta1Solid: Style
    Magenta1OutlineBold: Style
    Magenta1SolidBold: Style
    Magenta1OutlineThin: Style
    Magenta1SolidThin: Style
    Magenta1Dashed: Style
    Magenta1DashedBold: Style
    Magenta1DashedThin: Style
    Magenta1Dotted: Style
    Magenta1DottedBold: Style
    Magenta1DottedThin: Style
    Magenta2: Style
    Magenta2Bordered: Style
    Magenta2Bold: Style
    Magenta2Thin: Style
    Magenta2Flat: Style
    Magenta2Outline: Style
    Magenta2Solid: Style
    Magenta2OutlineBold: Style
    Magenta2SolidBold: Style
    Magenta2OutlineThin: Style
    Magenta2SolidThin: Style
    Magenta2Dashed: Style
    Magenta2DashedBold: Style
    Magenta2DashedThin: Style
    Magenta2Dotted: Style
    Magenta2DottedBold: Style
    Magenta2DottedThin: Style
    Magenta3: Style
    Magenta3Bordered: Style
    Magenta3Bold: Style
    Magenta3Thin: Style
    Magenta3Flat: Style
    Magenta3Outline: Style
    Magenta3Solid: Style
    Magenta3OutlineBold: Style
    Magenta3SolidBold: Style
    Magenta3OutlineThin: Style
    Magenta3SolidThin: Style
    Magenta3Dashed: Style
    Magenta3DashedBold: Style
    Magenta3DashedThin: Style
    Magenta3Dotted: Style
    Magenta3DottedBold: Style
    Magenta3DottedThin: Style
    Magenta4: Style
    Magenta4Bordered: Style
    Magenta4Bold: Style
    Magenta4Thin: Style
    Magenta4Flat: Style
    Magenta4Outline: Style
    Magenta4Solid: Style
    Magenta4OutlineBold: Style
    Magenta4SolidBold: Style
    Magenta4OutlineThin: Style
    Magenta4SolidThin: Style
    Magenta4Dashed: Style
    Magenta4DashedBold: Style
    Magenta4DashedThin: Style
    Magenta4Dotted: Style
    Magenta4DottedBold: Style
    Magenta4DottedThin: Style
    Magenta5: Style
    Magenta5Bordered: Style
    Magenta5Bold: Style
    Magenta5Thin: Style
    Magenta5Flat: Style
    Magenta5Outline: Style
    Magenta5Solid: Style
    Magenta5OutlineBold: Style
    Magenta5SolidBold: Style
    Magenta5OutlineThin: Style
    Magenta5SolidThin: Style
    Magenta5Dashed: Style
    Magenta5DashedBold: Style
    Magenta5DashedThin: Style
    Magenta5Dotted: Style
    Magenta5DottedBold: Style
    Magenta5DottedThin: Style
    Magenta6: Style
    Magenta6Bordered: Style
    Magenta6Bold: Style
    Magenta6Thin: Style
    Magenta6Flat: Style
    Magenta6Outline: Style
    Magenta6Solid: Style
    Magenta6OutlineBold: Style
    Magenta6SolidBold: Style
    Magenta6OutlineThin: Style
    Magenta6SolidThin: Style
    Magenta6Dashed: Style
    Magenta6DashedBold: Style
    Magenta6DashedThin: Style
    Magenta6Dotted: Style
    Magenta6DottedBold: Style
    Magenta6DottedThin: Style
    CornflowerBlue: Style
    CornflowerBlueBordered: Style
    CornflowerBlueBold: Style
    CornflowerBlueThin: Style
    CornflowerBlueFlat: Style
    CornflowerBlueOutline: Style
    CornflowerBlueSolid: Style
    CornflowerBlueOutlineBold: Style
    CornflowerBlueSolidBold: Style
    CornflowerBlueOutlineThin: Style
    CornflowerBlueSolidThin: Style
    CornflowerBlueDashed: Style
    CornflowerBlueDashedBold: Style
    CornflowerBlueDashedThin: Style
    CornflowerBlueDotted: Style
    CornflowerBlueDottedBold: Style
    CornflowerBlueDottedThin: Style
    Blue: Style
    BlueBordered: Style
    BlueBold: Style
    BlueThin: Style
    BlueFlat: Style
    BlueOutline: Style
    BlueSolid: Style
    BlueOutlineBold: Style
    BlueSolidBold: Style
    BlueOutlineThin: Style
    BlueSolidThin: Style
    BlueDashed: Style
    BlueDashedBold: Style
    BlueDashedThin: Style
    BlueDotted: Style
    BlueDottedBold: Style
    BlueDottedThin: Style
    Red: Style
    RedBordered: Style
    RedBold: Style
    RedThin: Style
    RedFlat: Style
    RedOutline: Style
    RedSolid: Style
    RedOutlineBold: Style
    RedSolidBold: Style
    RedOutlineThin: Style
    RedSolidThin: Style
    RedDashed: Style
    RedDashedBold: Style
    RedDashedThin: Style
    RedDotted: Style
    RedDottedBold: Style
    RedDottedThin: Style
    RedBerry: Style
    RedBerryBordered: Style
    RedBerryBold: Style
    RedBerryThin: Style
    RedBerryFlat: Style
    RedBerryOutline: Style
    RedBerrySolid: Style
    RedBerryOutlineBold: Style
    RedBerrySolidBold: Style
    RedBerryOutlineThin: Style
    RedBerrySolidThin: Style
    RedBerryDashed: Style
    RedBerryDashedBold: Style
    RedBerryDashedThin: Style
    RedBerryDotted: Style
    RedBerryDottedBold: Style
    RedBerryDottedThin: Style
    Green: Style
    GreenBordered: Style
    GreenBold: Style
    GreenThin: Style
    GreenFlat: Style
    GreenOutline: Style
    GreenSolid: Style
    GreenOutlineBold: Style
    GreenSolidBold: Style
    GreenOutlineThin: Style
    GreenSolidThin: Style
    GreenDashed: Style
    GreenDashedBold: Style
    GreenDashedThin: Style
    GreenDotted: Style
    GreenDottedBold: Style
    GreenDottedThin: Style
    Yellow: Style
    YellowBordered: Style
    YellowBold: Style
    YellowThin: Style
    YellowFlat: Style
    YellowOutline: Style
    YellowSolid: Style
    YellowOutlineBold: Style
    YellowSolidBold: Style
    YellowOutlineThin: Style
    YellowSolidThin: Style
    YellowDashed: Style
    YellowDashedBold: Style
    YellowDashedThin: Style
    YellowDotted: Style
    YellowDottedBold: Style
    YellowDottedThin: Style
    Orange: Style
    OrangeBordered: Style
    OrangeBold: Style
    OrangeThin: Style
    OrangeFlat: Style
    OrangeOutline: Style
    OrangeSolid: Style
    OrangeOutlineBold: Style
    OrangeSolidBold: Style
    OrangeOutlineThin: Style
    OrangeSolidThin: Style
    OrangeDashed: Style
    OrangeDashedBold: Style
    OrangeDashedThin: Style
    OrangeDotted: Style
    OrangeDottedBold: Style
    OrangeDottedThin: Style
    Cyan: Style
    CyanBordered: Style
    CyanBold: Style
    CyanThin: Style
    CyanFlat: Style
    CyanOutline: Style
    CyanSolid: Style
    CyanOutlineBold: Style
    CyanSolidBold: Style
    CyanOutlineThin: Style
    CyanSolidThin: Style
    CyanDashed: Style
    CyanDashedBold: Style
    CyanDashedThin: Style
    CyanDotted: Style
    CyanDottedBold: Style
    CyanDottedThin: Style
    Purple: Style
    PurpleBordered: Style
    PurpleBold: Style
    PurpleThin: Style
    PurpleFlat: Style
    PurpleOutline: Style
    PurpleSolid: Style
    PurpleOutlineBold: Style
    PurpleSolidBold: Style
    PurpleOutlineThin: Style
    PurpleSolidThin: Style
    PurpleDashed: Style
    PurpleDashedBold: Style
    PurpleDashedThin: Style
    PurpleDotted: Style
    PurpleDottedBold: Style
    PurpleDottedThin: Style
    Magenta: Style
    MagentaBordered: Style
    MagentaBold: Style
    MagentaThin: Style
    MagentaFlat: Style
    MagentaOutline: Style
    MagentaSolid: Style
    MagentaOutlineBold: Style
    MagentaSolidBold: Style
    MagentaOutlineThin: Style
    MagentaSolidThin: Style
    MagentaDashed: Style
    MagentaDashedBold: Style
    MagentaDashedThin: Style
    MagentaDotted: Style
    MagentaDottedBold: Style
    MagentaDottedThin: Style
    Pink: Style
    PinkBordered: Style
    PinkBold: Style
    PinkThin: Style
    PinkFlat: Style
    PinkOutline: Style
    PinkSolid: Style
    PinkOutlineBold: Style
    PinkSolidBold: Style
    PinkOutlineThin: Style
    PinkSolidThin: Style
    PinkDashed: Style
    PinkDashedBold: Style
    PinkDashedThin: Style
    PinkDotted: Style
    PinkDottedBold: Style
    PinkDottedThin: Style
    Lime: Style
    LimeBordered: Style
    LimeBold: Style
    LimeThin: Style
    LimeFlat: Style
    LimeOutline: Style
    LimeSolid: Style
    LimeOutlineBold: Style
    LimeSolidBold: Style
    LimeOutlineThin: Style
    LimeSolidThin: Style
    LimeDashed: Style
    LimeDashedBold: Style
    LimeDashedThin: Style
    LimeDotted: Style
    LimeDottedBold: Style
    LimeDottedThin: Style
    Teal: Style
    TealBordered: Style
    TealBold: Style
    TealThin: Style
    TealFlat: Style
    TealOutline: Style
    TealSolid: Style
    TealOutlineBold: Style
    TealSolidBold: Style
    TealOutlineThin: Style
    TealSolidThin: Style
    TealDashed: Style
    TealDashedBold: Style
    TealDashedThin: Style
    TealDotted: Style
    TealDottedBold: Style
    TealDottedThin: Style
    Navy: Style
    NavyBordered: Style
    NavyBold: Style
    NavyThin: Style
    NavyFlat: Style
    NavyOutline: Style
    NavySolid: Style
    NavyOutlineBold: Style
    NavySolidBold: Style
    NavyOutlineThin: Style
    NavySolidThin: Style
    NavyDashed: Style
    NavyDashedBold: Style
    NavyDashedThin: Style
    NavyDotted: Style
    NavyDottedBold: Style
    NavyDottedThin: Style
    Olive: Style
    OliveBordered: Style
    OliveBold: Style
    OliveThin: Style
    OliveFlat: Style
    OliveOutline: Style
    OliveSolid: Style
    OliveOutlineBold: Style
    OliveSolidBold: Style
    OliveOutlineThin: Style
    OliveSolidThin: Style
    OliveDashed: Style
    OliveDashedBold: Style
    OliveDashedThin: Style
    OliveDotted: Style
    OliveDottedBold: Style
    OliveDottedThin: Style
    Brown: Style
    BrownBordered: Style
    BrownBold: Style
    BrownThin: Style
    BrownFlat: Style
    BrownOutline: Style
    BrownSolid: Style
    BrownOutlineBold: Style
    BrownSolidBold: Style
    BrownOutlineThin: Style
    BrownSolidThin: Style
    BrownDashed: Style
    BrownDashedBold: Style
    BrownDashedThin: Style
    BrownDotted: Style
    BrownDottedBold: Style
    BrownDottedThin: Style
    Gold: Style
    GoldBordered: Style
    GoldBold: Style
    GoldThin: Style
    GoldFlat: Style
    GoldOutline: Style
    GoldSolid: Style
    GoldOutlineBold: Style
    GoldSolidBold: Style
    GoldOutlineThin: Style
    GoldSolidThin: Style
    GoldDashed: Style
    GoldDashedBold: Style
    GoldDashedThin: Style
    GoldDotted: Style
    GoldDottedBold: Style
    GoldDottedThin: Style
    Aqua: Style
    AquaBordered: Style
    AquaBold: Style
    AquaThin: Style
    AquaFlat: Style
    AquaOutline: Style
    AquaSolid: Style
    AquaOutlineBold: Style
    AquaSolidBold: Style
    AquaOutlineThin: Style
    AquaSolidThin: Style
    AquaDashed: Style
    AquaDashedBold: Style
    AquaDashedThin: Style
    AquaDotted: Style
    AquaDottedBold: Style
    AquaDottedThin: Style
    GreenYellow: Style
    GreenYellowBordered: Style
    GreenYellowBold: Style
    GreenYellowThin: Style
    GreenYellowFlat: Style
    GreenYellowOutline: Style
    GreenYellowSolid: Style
    GreenYellowOutlineBold: Style
    GreenYellowSolidBold: Style
    GreenYellowOutlineThin: Style
    GreenYellowSolidThin: Style
    GreenYellowDashed: Style
    GreenYellowDashedBold: Style
    GreenYellowDashedThin: Style
    GreenYellowDotted: Style
    GreenYellowDottedBold: Style
    GreenYellowDottedThin: Style
    Ivory: Style
    IvoryBordered: Style
    IvoryBold: Style
    IvoryThin: Style
    IvoryFlat: Style
    IvoryOutline: Style
    IvorySolid: Style
    IvoryOutlineBold: Style
    IvorySolidBold: Style
    IvoryOutlineThin: Style
    IvorySolidThin: Style
    IvoryDashed: Style
    IvoryDashedBold: Style
    IvoryDashedThin: Style
    IvoryDotted: Style
    IvoryDottedBold: Style
    IvoryDottedThin: Style
    Steel: Style
    SteelBordered: Style
    SteelBold: Style
    SteelThin: Style
    SteelFlat: Style
    SteelOutline: Style
    SteelSolid: Style
    SteelOutlineBold: Style
    SteelSolidBold: Style
    SteelOutlineThin: Style
    SteelSolidThin: Style
    SteelDashed: Style
    SteelDashedBold: Style
    SteelDashedThin: Style
    SteelDotted: Style
    SteelDottedBold: Style
    SteelDottedThin: Style
    GoogleBlue: Style
    GoogleBlueBordered: Style
    GoogleBlueBold: Style
    GoogleBlueThin: Style
    GoogleBlueFlat: Style
    GoogleBlueOutline: Style
    GoogleBlueSolid: Style
    GoogleBlueOutlineBold: Style
    GoogleBlueSolidBold: Style
    GoogleBlueOutlineThin: Style
    GoogleBlueSolidThin: Style
    GoogleBlueDashed: Style
    GoogleBlueDashedBold: Style
    GoogleBlueDashedThin: Style
    GoogleBlueDotted: Style
    GoogleBlueDottedBold: Style
    GoogleBlueDottedThin: Style
    GoogleRed: Style
    GoogleRedBordered: Style
    GoogleRedBold: Style
    GoogleRedThin: Style
    GoogleRedFlat: Style
    GoogleRedOutline: Style
    GoogleRedSolid: Style
    GoogleRedOutlineBold: Style
    GoogleRedSolidBold: Style
    GoogleRedOutlineThin: Style
    GoogleRedSolidThin: Style
    GoogleRedDashed: Style
    GoogleRedDashedBold: Style
    GoogleRedDashedThin: Style
    GoogleRedDotted: Style
    GoogleRedDottedBold: Style
    GoogleRedDottedThin: Style
    GoogleYellow: Style
    GoogleYellowBordered: Style
    GoogleYellowBold: Style
    GoogleYellowThin: Style
    GoogleYellowFlat: Style
    GoogleYellowOutline: Style
    GoogleYellowSolid: Style
    GoogleYellowOutlineBold: Style
    GoogleYellowSolidBold: Style
    GoogleYellowOutlineThin: Style
    GoogleYellowSolidThin: Style
    GoogleYellowDashed: Style
    GoogleYellowDashedBold: Style
    GoogleYellowDashedThin: Style
    GoogleYellowDotted: Style
    GoogleYellowDottedBold: Style
    GoogleYellowDottedThin: Style
    GoogleGreen: Style
    GoogleGreenBordered: Style
    GoogleGreenBold: Style
    GoogleGreenThin: Style
    GoogleGreenFlat: Style
    GoogleGreenOutline: Style
    GoogleGreenSolid: Style
    GoogleGreenOutlineBold: Style
    GoogleGreenSolidBold: Style
    GoogleGreenOutlineThin: Style
    GoogleGreenSolidThin: Style
    GoogleGreenDashed: Style
    GoogleGreenDashedBold: Style
    GoogleGreenDashedThin: Style
    GoogleGreenDotted: Style
    GoogleGreenDottedBold: Style
    GoogleGreenDottedThin: Style
    GoogleOrange: Style
    GoogleOrangeBordered: Style
    GoogleOrangeBold: Style
    GoogleOrangeThin: Style
    GoogleOrangeFlat: Style
    GoogleOrangeOutline: Style
    GoogleOrangeSolid: Style
    GoogleOrangeOutlineBold: Style
    GoogleOrangeSolidBold: Style
    GoogleOrangeOutlineThin: Style
    GoogleOrangeSolidThin: Style
    GoogleOrangeDashed: Style
    GoogleOrangeDashedBold: Style
    GoogleOrangeDashedThin: Style
    GoogleOrangeDotted: Style
    GoogleOrangeDottedBold: Style
    GoogleOrangeDottedThin: Style
    GooglePurple: Style
    GooglePurpleBordered: Style
    GooglePurpleBold: Style
    GooglePurpleThin: Style
    GooglePurpleFlat: Style
    GooglePurpleOutline: Style
    GooglePurpleSolid: Style
    GooglePurpleOutlineBold: Style
    GooglePurpleSolidBold: Style
    GooglePurpleOutlineThin: Style
    GooglePurpleSolidThin: Style
    GooglePurpleDashed: Style
    GooglePurpleDashedBold: Style
    GooglePurpleDashedThin: Style
    GooglePurpleDotted: Style
    GooglePurpleDottedBold: Style
    GooglePurpleDottedThin: Style
    GoogleGray: Style
    GoogleGrayBordered: Style
    GoogleGrayBold: Style
    GoogleGrayThin: Style
    GoogleGrayFlat: Style
    GoogleGrayOutline: Style
    GoogleGraySolid: Style
    GoogleGrayOutlineBold: Style
    GoogleGraySolidBold: Style
    GoogleGrayOutlineThin: Style
    GoogleGraySolidThin: Style
    GoogleGrayDashed: Style
    GoogleGrayDashedBold: Style
    GoogleGrayDashedThin: Style
    GoogleGrayDotted: Style
    GoogleGrayDottedBold: Style
    GoogleGrayDottedThin: Style
    Primary1: Style
    Primary1Bordered: Style
    Primary1Bold: Style
    Primary1Thin: Style
    Primary1Flat: Style
    Primary1Outline: Style
    Primary1Solid: Style
    Primary1OutlineBold: Style
    Primary1SolidBold: Style
    Primary1OutlineThin: Style
    Primary1SolidThin: Style
    Primary1Dashed: Style
    Primary1DashedBold: Style
    Primary1DashedThin: Style
    Primary1Dotted: Style
    Primary1DottedBold: Style
    Primary1DottedThin: Style
    Primary2: Style
    Primary2Bordered: Style
    Primary2Bold: Style
    Primary2Thin: Style
    Primary2Flat: Style
    Primary2Outline: Style
    Primary2Solid: Style
    Primary2OutlineBold: Style
    Primary2SolidBold: Style
    Primary2OutlineThin: Style
    Primary2SolidThin: Style
    Primary2Dashed: Style
    Primary2DashedBold: Style
    Primary2DashedThin: Style
    Primary2Dotted: Style
    Primary2DottedBold: Style
    Primary2DottedThin: Style
    Primary3: Style
    Primary3Bordered: Style
    Primary3Bold: Style
    Primary3Thin: Style
    Primary3Flat: Style
    Primary3Outline: Style
    Primary3Solid: Style
    Primary3OutlineBold: Style
    Primary3SolidBold: Style
    Primary3OutlineThin: Style
    Primary3SolidThin: Style
    Primary3Dashed: Style
    Primary3DashedBold: Style
    Primary3DashedThin: Style
    Primary3Dotted: Style
    Primary3DottedBold: Style
    Primary3DottedThin: Style
    Primary4: Style
    Primary4Bordered: Style
    Primary4Bold: Style
    Primary4Thin: Style
    Primary4Flat: Style
    Primary4Outline: Style
    Primary4Solid: Style
    Primary4OutlineBold: Style
    Primary4SolidBold: Style
    Primary4OutlineThin: Style
    Primary4SolidThin: Style
    Primary4Dashed: Style
    Primary4DashedBold: Style
    Primary4DashedThin: Style
    Primary4Dotted: Style
    Primary4DottedBold: Style
    Primary4DottedThin: Style
    Primary5: Style
    Primary5Bordered: Style
    Primary5Bold: Style
    Primary5Thin: Style
    Primary5Flat: Style
    Primary5Outline: Style
    Primary5Solid: Style
    Primary5OutlineBold: Style
    Primary5SolidBold: Style
    Primary5OutlineThin: Style
    Primary5SolidThin: Style
    Primary5Dashed: Style
    Primary5DashedBold: Style
    Primary5DashedThin: Style
    Primary5Dotted: Style
    Primary5DottedBold: Style
    Primary5DottedThin: Style
    Primary6: Style
    Primary6Bordered: Style
    Primary6Bold: Style
    Primary6Thin: Style
    Primary6Flat: Style
    Primary6Outline: Style
    Primary6Solid: Style
    Primary6OutlineBold: Style
    Primary6SolidBold: Style
    Primary6OutlineThin: Style
    Primary6SolidThin: Style
    Primary6Dashed: Style
    Primary6DashedBold: Style
    Primary6DashedThin: Style
    Primary6Dotted: Style
    Primary6DottedBold: Style
    Primary6DottedThin: Style
    Secondary1: Style
    Secondary1Bordered: Style
    Secondary1Bold: Style
    Secondary1Thin: Style
    Secondary1Flat: Style
    Secondary1Outline: Style
    Secondary1Solid: Style
    Secondary1OutlineBold: Style
    Secondary1SolidBold: Style
    Secondary1OutlineThin: Style
    Secondary1SolidThin: Style
    Secondary1Dashed: Style
    Secondary1DashedBold: Style
    Secondary1DashedThin: Style
    Secondary1Dotted: Style
    Secondary1DottedBold: Style
    Secondary1DottedThin: Style
    Secondary2: Style
    Secondary2Bordered: Style
    Secondary2Bold: Style
    Secondary2Thin: Style
    Secondary2Flat: Style
    Secondary2Outline: Style
    Secondary2Solid: Style
    Secondary2OutlineBold: Style
    Secondary2SolidBold: Style
    Secondary2OutlineThin: Style
    Secondary2SolidThin: Style
    Secondary2Dashed: Style
    Secondary2DashedBold: Style
    Secondary2DashedThin: Style
    Secondary2Dotted: Style
    Secondary2DottedBold: Style
    Secondary2DottedThin: Style
    Secondary3: Style
    Secondary3Bordered: Style
    Secondary3Bold: Style
    Secondary3Thin: Style
    Secondary3Flat: Style
    Secondary3Outline: Style
    Secondary3Solid: Style
    Secondary3OutlineBold: Style
    Secondary3SolidBold: Style
    Secondary3OutlineThin: Style
    Secondary3SolidThin: Style
    Secondary3Dashed: Style
    Secondary3DashedBold: Style
    Secondary3DashedThin: Style
    Secondary3Dotted: Style
    Secondary3DottedBold: Style
    Secondary3DottedThin: Style
    Secondary4: Style
    Secondary4Bordered: Style
    Secondary4Bold: Style
    Secondary4Thin: Style
    Secondary4Flat: Style
    Secondary4Outline: Style
    Secondary4Solid: Style
    Secondary4OutlineBold: Style
    Secondary4SolidBold: Style
    Secondary4OutlineThin: Style
    Secondary4SolidThin: Style
    Secondary4Dashed: Style
    Secondary4DashedBold: Style
    Secondary4DashedThin: Style
    Secondary4Dotted: Style
    Secondary4DottedBold: Style
    Secondary4DottedThin: Style
    Secondary5: Style
    Secondary5Bordered: Style
    Secondary5Bold: Style
    Secondary5Thin: Style
    Secondary5Flat: Style
    Secondary5Outline: Style
    Secondary5Solid: Style
    Secondary5OutlineBold: Style
    Secondary5SolidBold: Style
    Secondary5OutlineThin: Style
    Secondary5SolidThin: Style
    Secondary5Dashed: Style
    Secondary5DashedBold: Style
    Secondary5DashedThin: Style
    Secondary5Dotted: Style
    Secondary5DottedBold: Style
    Secondary5DottedThin: Style
    Secondary6: Style
    Secondary6Bordered: Style
    Secondary6Bold: Style
    Secondary6Thin: Style
    Secondary6Flat: Style
    Secondary6Outline: Style
    Secondary6Solid: Style
    Secondary6OutlineBold: Style
    Secondary6SolidBold: Style
    Secondary6OutlineThin: Style
    Secondary6SolidThin: Style
    Secondary6Dashed: Style
    Secondary6DashedBold: Style
    Secondary6DashedThin: Style
    Secondary6Dotted: Style
    Secondary6DottedBold: Style
    Secondary6DottedThin: Style
    Accent1: Style
    Accent1Bordered: Style
    Accent1Bold: Style
    Accent1Thin: Style
    Accent1Flat: Style
    Accent1Outline: Style
    Accent1Solid: Style
    Accent1OutlineBold: Style
    Accent1SolidBold: Style
    Accent1OutlineThin: Style
    Accent1SolidThin: Style
    Accent1Dashed: Style
    Accent1DashedBold: Style
    Accent1DashedThin: Style
    Accent1Dotted: Style
    Accent1DottedBold: Style
    Accent1DottedThin: Style
    Accent2: Style
    Accent2Bordered: Style
    Accent2Bold: Style
    Accent2Thin: Style
    Accent2Flat: Style
    Accent2Outline: Style
    Accent2Solid: Style
    Accent2OutlineBold: Style
    Accent2SolidBold: Style
    Accent2OutlineThin: Style
    Accent2SolidThin: Style
    Accent2Dashed: Style
    Accent2DashedBold: Style
    Accent2DashedThin: Style
    Accent2Dotted: Style
    Accent2DottedBold: Style
    Accent2DottedThin: Style
    Accent3: Style
    Accent3Bordered: Style
    Accent3Bold: Style
    Accent3Thin: Style
    Accent3Flat: Style
    Accent3Outline: Style
    Accent3Solid: Style
    Accent3OutlineBold: Style
    Accent3SolidBold: Style
    Accent3OutlineThin: Style
    Accent3SolidThin: Style
    Accent3Dashed: Style
    Accent3DashedBold: Style
    Accent3DashedThin: Style
    Accent3Dotted: Style
    Accent3DottedBold: Style
    Accent3DottedThin: Style
    Accent4: Style
    Accent4Bordered: Style
    Accent4Bold: Style
    Accent4Thin: Style
    Accent4Flat: Style
    Accent4Outline: Style
    Accent4Solid: Style
    Accent4OutlineBold: Style
    Accent4SolidBold: Style
    Accent4OutlineThin: Style
    Accent4SolidThin: Style
    Accent4Dashed: Style
    Accent4DashedBold: Style
    Accent4DashedThin: Style
    Accent4Dotted: Style
    Accent4DottedBold: Style
    Accent4DottedThin: Style
    Accent5: Style
    Accent5Bordered: Style
    Accent5Bold: Style
    Accent5Thin: Style
    Accent5Flat: Style
    Accent5Outline: Style
    Accent5Solid: Style
    Accent5OutlineBold: Style
    Accent5SolidBold: Style
    Accent5OutlineThin: Style
    Accent5SolidThin: Style
    Accent5Dashed: Style
    Accent5DashedBold: Style
    Accent5DashedThin: Style
    Accent5Dotted: Style
    Accent5DottedBold: Style
    Accent5DottedThin: Style
    Accent6: Style
    Accent6Bordered: Style
    Accent6Bold: Style
    Accent6Thin: Style
    Accent6Flat: Style
    Accent6Outline: Style
    Accent6Solid: Style
    Accent6OutlineBold: Style
    Accent6SolidBold: Style
    Accent6OutlineThin: Style
    Accent6SolidThin: Style
    Accent6Dashed: Style
    Accent6DashedBold: Style
    Accent6DashedThin: Style
    Accent6Dotted: Style
    Accent6DottedBold: Style
    Accent6DottedThin: Style
    Muted1: Style
    Muted1Bordered: Style
    Muted1Bold: Style
    Muted1Thin: Style
    Muted1Flat: Style
    Muted1Outline: Style
    Muted1Solid: Style
    Muted1OutlineBold: Style
    Muted1SolidBold: Style
    Muted1OutlineThin: Style
    Muted1SolidThin: Style
    Muted1Dashed: Style
    Muted1DashedBold: Style
    Muted1DashedThin: Style
    Muted1Dotted: Style
    Muted1DottedBold: Style
    Muted1DottedThin: Style
    Muted2: Style
    Muted2Bordered: Style
    Muted2Bold: Style
    Muted2Thin: Style
    Muted2Flat: Style
    Muted2Outline: Style
    Muted2Solid: Style
    Muted2OutlineBold: Style
    Muted2SolidBold: Style
    Muted2OutlineThin: Style
    Muted2SolidThin: Style
    Muted2Dashed: Style
    Muted2DashedBold: Style
    Muted2DashedThin: Style
    Muted2Dotted: Style
    Muted2DottedBold: Style
    Muted2DottedThin: Style
    Muted3: Style
    Muted3Bordered: Style
    Muted3Bold: Style
    Muted3Thin: Style
    Muted3Flat: Style
    Muted3Outline: Style
    Muted3Solid: Style
    Muted3OutlineBold: Style
    Muted3SolidBold: Style
    Muted3OutlineThin: Style
    Muted3SolidThin: Style
    Muted3Dashed: Style
    Muted3DashedBold: Style
    Muted3DashedThin: Style
    Muted3Dotted: Style
    Muted3DottedBold: Style
    Muted3DottedThin: Style
    Muted4: Style
    Muted4Bordered: Style
    Muted4Bold: Style
    Muted4Thin: Style
    Muted4Flat: Style
    Muted4Outline: Style
    Muted4Solid: Style
    Muted4OutlineBold: Style
    Muted4SolidBold: Style
    Muted4OutlineThin: Style
    Muted4SolidThin: Style
    Muted4Dashed: Style
    Muted4DashedBold: Style
    Muted4DashedThin: Style
    Muted4Dotted: Style
    Muted4DottedBold: Style
    Muted4DottedThin: Style
    Muted5: Style
    Muted5Bordered: Style
    Muted5Bold: Style
    Muted5Thin: Style
    Muted5Flat: Style
    Muted5Outline: Style
    Muted5Solid: Style
    Muted5OutlineBold: Style
    Muted5SolidBold: Style
    Muted5OutlineThin: Style
    Muted5SolidThin: Style
    Muted5Dashed: Style
    Muted5DashedBold: Style
    Muted5DashedThin: Style
    Muted5Dotted: Style
    Muted5DottedBold: Style
    Muted5DottedThin: Style
    Muted6: Style
    Muted6Bordered: Style
    Muted6Bold: Style
    Muted6Thin: Style
    Muted6Flat: Style
    Muted6Outline: Style
    Muted6Solid: Style
    Muted6OutlineBold: Style
    Muted6SolidBold: Style
    Muted6OutlineThin: Style
    Muted6SolidThin: Style
    Muted6Dashed: Style
    Muted6DashedBold: Style
    Muted6DashedThin: Style
    Muted6Dotted: Style
    Muted6DottedBold: Style
    Muted6DottedThin: Style
    Warning1: Style
    Warning1Bordered: Style
    Warning1Bold: Style
    Warning1Thin: Style
    Warning1Flat: Style
    Warning1Outline: Style
    Warning1Solid: Style
    Warning1OutlineBold: Style
    Warning1SolidBold: Style
    Warning1OutlineThin: Style
    Warning1SolidThin: Style
    Warning1Dashed: Style
    Warning1DashedBold: Style
    Warning1DashedThin: Style
    Warning1Dotted: Style
    Warning1DottedBold: Style
    Warning1DottedThin: Style
    Warning2: Style
    Warning2Bordered: Style
    Warning2Bold: Style
    Warning2Thin: Style
    Warning2Flat: Style
    Warning2Outline: Style
    Warning2Solid: Style
    Warning2OutlineBold: Style
    Warning2SolidBold: Style
    Warning2OutlineThin: Style
    Warning2SolidThin: Style
    Warning2Dashed: Style
    Warning2DashedBold: Style
    Warning2DashedThin: Style
    Warning2Dotted: Style
    Warning2DottedBold: Style
    Warning2DottedThin: Style
    Warning3: Style
    Warning3Bordered: Style
    Warning3Bold: Style
    Warning3Thin: Style
    Warning3Flat: Style
    Warning3Outline: Style
    Warning3Solid: Style
    Warning3OutlineBold: Style
    Warning3SolidBold: Style
    Warning3OutlineThin: Style
    Warning3SolidThin: Style
    Warning3Dashed: Style
    Warning3DashedBold: Style
    Warning3DashedThin: Style
    Warning3Dotted: Style
    Warning3DottedBold: Style
    Warning3DottedThin: Style
    Warning4: Style
    Warning4Bordered: Style
    Warning4Bold: Style
    Warning4Thin: Style
    Warning4Flat: Style
    Warning4Outline: Style
    Warning4Solid: Style
    Warning4OutlineBold: Style
    Warning4SolidBold: Style
    Warning4OutlineThin: Style
    Warning4SolidThin: Style
    Warning4Dashed: Style
    Warning4DashedBold: Style
    Warning4DashedThin: Style
    Warning4Dotted: Style
    Warning4DottedBold: Style
    Warning4DottedThin: Style
    Warning5: Style
    Warning5Bordered: Style
    Warning5Bold: Style
    Warning5Thin: Style
    Warning5Flat: Style
    Warning5Outline: Style
    Warning5Solid: Style
    Warning5OutlineBold: Style
    Warning5SolidBold: Style
    Warning5OutlineThin: Style
    Warning5SolidThin: Style
    Warning5Dashed: Style
    Warning5DashedBold: Style
    Warning5DashedThin: Style
    Warning5Dotted: Style
    Warning5DottedBold: Style
    Warning5DottedThin: Style
    Warning6: Style
    Warning6Bordered: Style
    Warning6Bold: Style
    Warning6Thin: Style
    Warning6Flat: Style
    Warning6Outline: Style
    Warning6Solid: Style
    Warning6OutlineBold: Style
    Warning6SolidBold: Style
    Warning6OutlineThin: Style
    Warning6SolidThin: Style
    Warning6Dashed: Style
    Warning6DashedBold: Style
    Warning6DashedThin: Style
    Warning6Dotted: Style
    Warning6DottedBold: Style
    Warning6DottedThin: Style
    Danger1: Style
    Danger1Bordered: Style
    Danger1Bold: Style
    Danger1Thin: Style
    Danger1Flat: Style
    Danger1Outline: Style
    Danger1Solid: Style
    Danger1OutlineBold: Style
    Danger1SolidBold: Style
    Danger1OutlineThin: Style
    Danger1SolidThin: Style
    Danger1Dashed: Style
    Danger1DashedBold: Style
    Danger1DashedThin: Style
    Danger1Dotted: Style
    Danger1DottedBold: Style
    Danger1DottedThin: Style
    Danger2: Style
    Danger2Bordered: Style
    Danger2Bold: Style
    Danger2Thin: Style
    Danger2Flat: Style
    Danger2Outline: Style
    Danger2Solid: Style
    Danger2OutlineBold: Style
    Danger2SolidBold: Style
    Danger2OutlineThin: Style
    Danger2SolidThin: Style
    Danger2Dashed: Style
    Danger2DashedBold: Style
    Danger2DashedThin: Style
    Danger2Dotted: Style
    Danger2DottedBold: Style
    Danger2DottedThin: Style
    Danger3: Style
    Danger3Bordered: Style
    Danger3Bold: Style
    Danger3Thin: Style
    Danger3Flat: Style
    Danger3Outline: Style
    Danger3Solid: Style
    Danger3OutlineBold: Style
    Danger3SolidBold: Style
    Danger3OutlineThin: Style
    Danger3SolidThin: Style
    Danger3Dashed: Style
    Danger3DashedBold: Style
    Danger3DashedThin: Style
    Danger3Dotted: Style
    Danger3DottedBold: Style
    Danger3DottedThin: Style
    Danger4: Style
    Danger4Bordered: Style
    Danger4Bold: Style
    Danger4Thin: Style
    Danger4Flat: Style
    Danger4Outline: Style
    Danger4Solid: Style
    Danger4OutlineBold: Style
    Danger4SolidBold: Style
    Danger4OutlineThin: Style
    Danger4SolidThin: Style
    Danger4Dashed: Style
    Danger4DashedBold: Style
    Danger4DashedThin: Style
    Danger4Dotted: Style
    Danger4DottedBold: Style
    Danger4DottedThin: Style
    Danger5: Style
    Danger5Bordered: Style
    Danger5Bold: Style
    Danger5Thin: Style
    Danger5Flat: Style
    Danger5Outline: Style
    Danger5Solid: Style
    Danger5OutlineBold: Style
    Danger5SolidBold: Style
    Danger5OutlineThin: Style
    Danger5SolidThin: Style
    Danger5Dashed: Style
    Danger5DashedBold: Style
    Danger5DashedThin: Style
    Danger5Dotted: Style
    Danger5DottedBold: Style
    Danger5DottedThin: Style
    Danger6: Style
    Danger6Bordered: Style
    Danger6Bold: Style
    Danger6Thin: Style
    Danger6Flat: Style
    Danger6Outline: Style
    Danger6Solid: Style
    Danger6OutlineBold: Style
    Danger6SolidBold: Style
    Danger6OutlineThin: Style
    Danger6SolidThin: Style
    Danger6Dashed: Style
    Danger6DashedBold: Style
    Danger6DashedThin: Style
    Danger6Dotted: Style
    Danger6DottedBold: Style
    Danger6DottedThin: Style
    Success1: Style
    Success1Bordered: Style
    Success1Bold: Style
    Success1Thin: Style
    Success1Flat: Style
    Success1Outline: Style
    Success1Solid: Style
    Success1OutlineBold: Style
    Success1SolidBold: Style
    Success1OutlineThin: Style
    Success1SolidThin: Style
    Success1Dashed: Style
    Success1DashedBold: Style
    Success1DashedThin: Style
    Success1Dotted: Style
    Success1DottedBold: Style
    Success1DottedThin: Style
    Success2: Style
    Success2Bordered: Style
    Success2Bold: Style
    Success2Thin: Style
    Success2Flat: Style
    Success2Outline: Style
    Success2Solid: Style
    Success2OutlineBold: Style
    Success2SolidBold: Style
    Success2OutlineThin: Style
    Success2SolidThin: Style
    Success2Dashed: Style
    Success2DashedBold: Style
    Success2DashedThin: Style
    Success2Dotted: Style
    Success2DottedBold: Style
    Success2DottedThin: Style
    Success3: Style
    Success3Bordered: Style
    Success3Bold: Style
    Success3Thin: Style
    Success3Flat: Style
    Success3Outline: Style
    Success3Solid: Style
    Success3OutlineBold: Style
    Success3SolidBold: Style
    Success3OutlineThin: Style
    Success3SolidThin: Style
    Success3Dashed: Style
    Success3DashedBold: Style
    Success3DashedThin: Style
    Success3Dotted: Style
    Success3DottedBold: Style
    Success3DottedThin: Style
    Success4: Style
    Success4Bordered: Style
    Success4Bold: Style
    Success4Thin: Style
    Success4Flat: Style
    Success4Outline: Style
    Success4Solid: Style
    Success4OutlineBold: Style
    Success4SolidBold: Style
    Success4OutlineThin: Style
    Success4SolidThin: Style
    Success4Dashed: Style
    Success4DashedBold: Style
    Success4DashedThin: Style
    Success4Dotted: Style
    Success4DottedBold: Style
    Success4DottedThin: Style
    Success5: Style
    Success5Bordered: Style
    Success5Bold: Style
    Success5Thin: Style
    Success5Flat: Style
    Success5Outline: Style
    Success5Solid: Style
    Success5OutlineBold: Style
    Success5SolidBold: Style
    Success5OutlineThin: Style
    Success5SolidThin: Style
    Success5Dashed: Style
    Success5DashedBold: Style
    Success5DashedThin: Style
    Success5Dotted: Style
    Success5DottedBold: Style
    Success5DottedThin: Style
    Success6: Style
    Success6Bordered: Style
    Success6Bold: Style
    Success6Thin: Style
    Success6Flat: Style
    Success6Outline: Style
    Success6Solid: Style
    Success6OutlineBold: Style
    Success6SolidBold: Style
    Success6OutlineThin: Style
    Success6SolidThin: Style
    Success6Dashed: Style
    Success6DashedBold: Style
    Success6DashedThin: Style
    Success6Dotted: Style
    Success6DottedBold: Style
    Success6DottedThin: Style
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
    YellowNeutral: Style
    YellowNeutralFlat: Style
    AmberNeutral: Style
    AmberNeutralFlat: Style
    PurpleNeutral: Style
    PurpleNeutralFlat: Style
    CyanNeutral: Style
    CyanNeutralFlat: Style
    TealNeutral: Style
    TealNeutralFlat: Style
    MagentaNeutral: Style
    MagentaNeutralFlat: Style
    PinkNeutral: Style
    PinkNeutralFlat: Style

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
        Danger: Style | None = None,
        DangerBordered: Style | None = None,
        DangerBold: Style | None = None,
        DangerThin: Style | None = None,
        DangerFlat: Style | None = None,
        DangerOutline: Style | None = None,
        DangerSolid: Style | None = None,
        DangerOutlineBold: Style | None = None,
        DangerSolidBold: Style | None = None,
        DangerOutlineThin: Style | None = None,
        DangerSolidThin: Style | None = None,
        DangerDashed: Style | None = None,
        DangerDashedBold: Style | None = None,
        DangerDashedThin: Style | None = None,
        DangerDotted: Style | None = None,
        DangerDottedBold: Style | None = None,
        DangerDottedThin: Style | None = None,
        Success: Style | None = None,
        SuccessBordered: Style | None = None,
        SuccessBold: Style | None = None,
        SuccessThin: Style | None = None,
        SuccessFlat: Style | None = None,
        SuccessOutline: Style | None = None,
        SuccessSolid: Style | None = None,
        SuccessOutlineBold: Style | None = None,
        SuccessSolidBold: Style | None = None,
        SuccessOutlineThin: Style | None = None,
        SuccessSolidThin: Style | None = None,
        SuccessDashed: Style | None = None,
        SuccessDashedBold: Style | None = None,
        SuccessDashedThin: Style | None = None,
        SuccessDotted: Style | None = None,
        SuccessDottedBold: Style | None = None,
        SuccessDottedThin: Style | None = None,
        Warning: Style | None = None,
        WarningBordered: Style | None = None,
        WarningBold: Style | None = None,
        WarningThin: Style | None = None,
        WarningFlat: Style | None = None,
        WarningOutline: Style | None = None,
        WarningSolid: Style | None = None,
        WarningOutlineBold: Style | None = None,
        WarningSolidBold: Style | None = None,
        WarningOutlineThin: Style | None = None,
        WarningSolidThin: Style | None = None,
        WarningDashed: Style | None = None,
        WarningDashedBold: Style | None = None,
        WarningDashedThin: Style | None = None,
        WarningDotted: Style | None = None,
        WarningDottedBold: Style | None = None,
        WarningDottedThin: Style | None = None,
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
        CornflowerBlue1: Style | None = None,
        CornflowerBlue1Bordered: Style | None = None,
        CornflowerBlue1Bold: Style | None = None,
        CornflowerBlue1Thin: Style | None = None,
        CornflowerBlue1Flat: Style | None = None,
        CornflowerBlue1Outline: Style | None = None,
        CornflowerBlue1Solid: Style | None = None,
        CornflowerBlue1OutlineBold: Style | None = None,
        CornflowerBlue1SolidBold: Style | None = None,
        CornflowerBlue1OutlineThin: Style | None = None,
        CornflowerBlue1SolidThin: Style | None = None,
        CornflowerBlue1Dashed: Style | None = None,
        CornflowerBlue1DashedBold: Style | None = None,
        CornflowerBlue1DashedThin: Style | None = None,
        CornflowerBlue1Dotted: Style | None = None,
        CornflowerBlue1DottedBold: Style | None = None,
        CornflowerBlue1DottedThin: Style | None = None,
        CornflowerBlue2: Style | None = None,
        CornflowerBlue2Bordered: Style | None = None,
        CornflowerBlue2Bold: Style | None = None,
        CornflowerBlue2Thin: Style | None = None,
        CornflowerBlue2Flat: Style | None = None,
        CornflowerBlue2Outline: Style | None = None,
        CornflowerBlue2Solid: Style | None = None,
        CornflowerBlue2OutlineBold: Style | None = None,
        CornflowerBlue2SolidBold: Style | None = None,
        CornflowerBlue2OutlineThin: Style | None = None,
        CornflowerBlue2SolidThin: Style | None = None,
        CornflowerBlue2Dashed: Style | None = None,
        CornflowerBlue2DashedBold: Style | None = None,
        CornflowerBlue2DashedThin: Style | None = None,
        CornflowerBlue2Dotted: Style | None = None,
        CornflowerBlue2DottedBold: Style | None = None,
        CornflowerBlue2DottedThin: Style | None = None,
        CornflowerBlue3: Style | None = None,
        CornflowerBlue3Bordered: Style | None = None,
        CornflowerBlue3Bold: Style | None = None,
        CornflowerBlue3Thin: Style | None = None,
        CornflowerBlue3Flat: Style | None = None,
        CornflowerBlue3Outline: Style | None = None,
        CornflowerBlue3Solid: Style | None = None,
        CornflowerBlue3OutlineBold: Style | None = None,
        CornflowerBlue3SolidBold: Style | None = None,
        CornflowerBlue3OutlineThin: Style | None = None,
        CornflowerBlue3SolidThin: Style | None = None,
        CornflowerBlue3Dashed: Style | None = None,
        CornflowerBlue3DashedBold: Style | None = None,
        CornflowerBlue3DashedThin: Style | None = None,
        CornflowerBlue3Dotted: Style | None = None,
        CornflowerBlue3DottedBold: Style | None = None,
        CornflowerBlue3DottedThin: Style | None = None,
        CornflowerBlue4: Style | None = None,
        CornflowerBlue4Bordered: Style | None = None,
        CornflowerBlue4Bold: Style | None = None,
        CornflowerBlue4Thin: Style | None = None,
        CornflowerBlue4Flat: Style | None = None,
        CornflowerBlue4Outline: Style | None = None,
        CornflowerBlue4Solid: Style | None = None,
        CornflowerBlue4OutlineBold: Style | None = None,
        CornflowerBlue4SolidBold: Style | None = None,
        CornflowerBlue4OutlineThin: Style | None = None,
        CornflowerBlue4SolidThin: Style | None = None,
        CornflowerBlue4Dashed: Style | None = None,
        CornflowerBlue4DashedBold: Style | None = None,
        CornflowerBlue4DashedThin: Style | None = None,
        CornflowerBlue4Dotted: Style | None = None,
        CornflowerBlue4DottedBold: Style | None = None,
        CornflowerBlue4DottedThin: Style | None = None,
        CornflowerBlue5: Style | None = None,
        CornflowerBlue5Bordered: Style | None = None,
        CornflowerBlue5Bold: Style | None = None,
        CornflowerBlue5Thin: Style | None = None,
        CornflowerBlue5Flat: Style | None = None,
        CornflowerBlue5Outline: Style | None = None,
        CornflowerBlue5Solid: Style | None = None,
        CornflowerBlue5OutlineBold: Style | None = None,
        CornflowerBlue5SolidBold: Style | None = None,
        CornflowerBlue5OutlineThin: Style | None = None,
        CornflowerBlue5SolidThin: Style | None = None,
        CornflowerBlue5Dashed: Style | None = None,
        CornflowerBlue5DashedBold: Style | None = None,
        CornflowerBlue5DashedThin: Style | None = None,
        CornflowerBlue5Dotted: Style | None = None,
        CornflowerBlue5DottedBold: Style | None = None,
        CornflowerBlue5DottedThin: Style | None = None,
        CornflowerBlue6: Style | None = None,
        CornflowerBlue6Bordered: Style | None = None,
        CornflowerBlue6Bold: Style | None = None,
        CornflowerBlue6Thin: Style | None = None,
        CornflowerBlue6Flat: Style | None = None,
        CornflowerBlue6Outline: Style | None = None,
        CornflowerBlue6Solid: Style | None = None,
        CornflowerBlue6OutlineBold: Style | None = None,
        CornflowerBlue6SolidBold: Style | None = None,
        CornflowerBlue6OutlineThin: Style | None = None,
        CornflowerBlue6SolidThin: Style | None = None,
        CornflowerBlue6Dashed: Style | None = None,
        CornflowerBlue6DashedBold: Style | None = None,
        CornflowerBlue6DashedThin: Style | None = None,
        CornflowerBlue6Dotted: Style | None = None,
        CornflowerBlue6DottedBold: Style | None = None,
        CornflowerBlue6DottedThin: Style | None = None,
        Blue1: Style | None = None,
        Blue1Bordered: Style | None = None,
        Blue1Bold: Style | None = None,
        Blue1Thin: Style | None = None,
        Blue1Flat: Style | None = None,
        Blue1Outline: Style | None = None,
        Blue1Solid: Style | None = None,
        Blue1OutlineBold: Style | None = None,
        Blue1SolidBold: Style | None = None,
        Blue1OutlineThin: Style | None = None,
        Blue1SolidThin: Style | None = None,
        Blue1Dashed: Style | None = None,
        Blue1DashedBold: Style | None = None,
        Blue1DashedThin: Style | None = None,
        Blue1Dotted: Style | None = None,
        Blue1DottedBold: Style | None = None,
        Blue1DottedThin: Style | None = None,
        Blue2: Style | None = None,
        Blue2Bordered: Style | None = None,
        Blue2Bold: Style | None = None,
        Blue2Thin: Style | None = None,
        Blue2Flat: Style | None = None,
        Blue2Outline: Style | None = None,
        Blue2Solid: Style | None = None,
        Blue2OutlineBold: Style | None = None,
        Blue2SolidBold: Style | None = None,
        Blue2OutlineThin: Style | None = None,
        Blue2SolidThin: Style | None = None,
        Blue2Dashed: Style | None = None,
        Blue2DashedBold: Style | None = None,
        Blue2DashedThin: Style | None = None,
        Blue2Dotted: Style | None = None,
        Blue2DottedBold: Style | None = None,
        Blue2DottedThin: Style | None = None,
        Blue3: Style | None = None,
        Blue3Bordered: Style | None = None,
        Blue3Bold: Style | None = None,
        Blue3Thin: Style | None = None,
        Blue3Flat: Style | None = None,
        Blue3Outline: Style | None = None,
        Blue3Solid: Style | None = None,
        Blue3OutlineBold: Style | None = None,
        Blue3SolidBold: Style | None = None,
        Blue3OutlineThin: Style | None = None,
        Blue3SolidThin: Style | None = None,
        Blue3Dashed: Style | None = None,
        Blue3DashedBold: Style | None = None,
        Blue3DashedThin: Style | None = None,
        Blue3Dotted: Style | None = None,
        Blue3DottedBold: Style | None = None,
        Blue3DottedThin: Style | None = None,
        Blue4: Style | None = None,
        Blue4Bordered: Style | None = None,
        Blue4Bold: Style | None = None,
        Blue4Thin: Style | None = None,
        Blue4Flat: Style | None = None,
        Blue4Outline: Style | None = None,
        Blue4Solid: Style | None = None,
        Blue4OutlineBold: Style | None = None,
        Blue4SolidBold: Style | None = None,
        Blue4OutlineThin: Style | None = None,
        Blue4SolidThin: Style | None = None,
        Blue4Dashed: Style | None = None,
        Blue4DashedBold: Style | None = None,
        Blue4DashedThin: Style | None = None,
        Blue4Dotted: Style | None = None,
        Blue4DottedBold: Style | None = None,
        Blue4DottedThin: Style | None = None,
        Blue5: Style | None = None,
        Blue5Bordered: Style | None = None,
        Blue5Bold: Style | None = None,
        Blue5Thin: Style | None = None,
        Blue5Flat: Style | None = None,
        Blue5Outline: Style | None = None,
        Blue5Solid: Style | None = None,
        Blue5OutlineBold: Style | None = None,
        Blue5SolidBold: Style | None = None,
        Blue5OutlineThin: Style | None = None,
        Blue5SolidThin: Style | None = None,
        Blue5Dashed: Style | None = None,
        Blue5DashedBold: Style | None = None,
        Blue5DashedThin: Style | None = None,
        Blue5Dotted: Style | None = None,
        Blue5DottedBold: Style | None = None,
        Blue5DottedThin: Style | None = None,
        Blue6: Style | None = None,
        Blue6Bordered: Style | None = None,
        Blue6Bold: Style | None = None,
        Blue6Thin: Style | None = None,
        Blue6Flat: Style | None = None,
        Blue6Outline: Style | None = None,
        Blue6Solid: Style | None = None,
        Blue6OutlineBold: Style | None = None,
        Blue6SolidBold: Style | None = None,
        Blue6OutlineThin: Style | None = None,
        Blue6SolidThin: Style | None = None,
        Blue6Dashed: Style | None = None,
        Blue6DashedBold: Style | None = None,
        Blue6DashedThin: Style | None = None,
        Blue6Dotted: Style | None = None,
        Blue6DottedBold: Style | None = None,
        Blue6DottedThin: Style | None = None,
        Red1: Style | None = None,
        Red1Bordered: Style | None = None,
        Red1Bold: Style | None = None,
        Red1Thin: Style | None = None,
        Red1Flat: Style | None = None,
        Red1Outline: Style | None = None,
        Red1Solid: Style | None = None,
        Red1OutlineBold: Style | None = None,
        Red1SolidBold: Style | None = None,
        Red1OutlineThin: Style | None = None,
        Red1SolidThin: Style | None = None,
        Red1Dashed: Style | None = None,
        Red1DashedBold: Style | None = None,
        Red1DashedThin: Style | None = None,
        Red1Dotted: Style | None = None,
        Red1DottedBold: Style | None = None,
        Red1DottedThin: Style | None = None,
        Red2: Style | None = None,
        Red2Bordered: Style | None = None,
        Red2Bold: Style | None = None,
        Red2Thin: Style | None = None,
        Red2Flat: Style | None = None,
        Red2Outline: Style | None = None,
        Red2Solid: Style | None = None,
        Red2OutlineBold: Style | None = None,
        Red2SolidBold: Style | None = None,
        Red2OutlineThin: Style | None = None,
        Red2SolidThin: Style | None = None,
        Red2Dashed: Style | None = None,
        Red2DashedBold: Style | None = None,
        Red2DashedThin: Style | None = None,
        Red2Dotted: Style | None = None,
        Red2DottedBold: Style | None = None,
        Red2DottedThin: Style | None = None,
        Red3: Style | None = None,
        Red3Bordered: Style | None = None,
        Red3Bold: Style | None = None,
        Red3Thin: Style | None = None,
        Red3Flat: Style | None = None,
        Red3Outline: Style | None = None,
        Red3Solid: Style | None = None,
        Red3OutlineBold: Style | None = None,
        Red3SolidBold: Style | None = None,
        Red3OutlineThin: Style | None = None,
        Red3SolidThin: Style | None = None,
        Red3Dashed: Style | None = None,
        Red3DashedBold: Style | None = None,
        Red3DashedThin: Style | None = None,
        Red3Dotted: Style | None = None,
        Red3DottedBold: Style | None = None,
        Red3DottedThin: Style | None = None,
        Red4: Style | None = None,
        Red4Bordered: Style | None = None,
        Red4Bold: Style | None = None,
        Red4Thin: Style | None = None,
        Red4Flat: Style | None = None,
        Red4Outline: Style | None = None,
        Red4Solid: Style | None = None,
        Red4OutlineBold: Style | None = None,
        Red4SolidBold: Style | None = None,
        Red4OutlineThin: Style | None = None,
        Red4SolidThin: Style | None = None,
        Red4Dashed: Style | None = None,
        Red4DashedBold: Style | None = None,
        Red4DashedThin: Style | None = None,
        Red4Dotted: Style | None = None,
        Red4DottedBold: Style | None = None,
        Red4DottedThin: Style | None = None,
        Red5: Style | None = None,
        Red5Bordered: Style | None = None,
        Red5Bold: Style | None = None,
        Red5Thin: Style | None = None,
        Red5Flat: Style | None = None,
        Red5Outline: Style | None = None,
        Red5Solid: Style | None = None,
        Red5OutlineBold: Style | None = None,
        Red5SolidBold: Style | None = None,
        Red5OutlineThin: Style | None = None,
        Red5SolidThin: Style | None = None,
        Red5Dashed: Style | None = None,
        Red5DashedBold: Style | None = None,
        Red5DashedThin: Style | None = None,
        Red5Dotted: Style | None = None,
        Red5DottedBold: Style | None = None,
        Red5DottedThin: Style | None = None,
        Red6: Style | None = None,
        Red6Bordered: Style | None = None,
        Red6Bold: Style | None = None,
        Red6Thin: Style | None = None,
        Red6Flat: Style | None = None,
        Red6Outline: Style | None = None,
        Red6Solid: Style | None = None,
        Red6OutlineBold: Style | None = None,
        Red6SolidBold: Style | None = None,
        Red6OutlineThin: Style | None = None,
        Red6SolidThin: Style | None = None,
        Red6Dashed: Style | None = None,
        Red6DashedBold: Style | None = None,
        Red6DashedThin: Style | None = None,
        Red6Dotted: Style | None = None,
        Red6DottedBold: Style | None = None,
        Red6DottedThin: Style | None = None,
        RedBerry1: Style | None = None,
        RedBerry1Bordered: Style | None = None,
        RedBerry1Bold: Style | None = None,
        RedBerry1Thin: Style | None = None,
        RedBerry1Flat: Style | None = None,
        RedBerry1Outline: Style | None = None,
        RedBerry1Solid: Style | None = None,
        RedBerry1OutlineBold: Style | None = None,
        RedBerry1SolidBold: Style | None = None,
        RedBerry1OutlineThin: Style | None = None,
        RedBerry1SolidThin: Style | None = None,
        RedBerry1Dashed: Style | None = None,
        RedBerry1DashedBold: Style | None = None,
        RedBerry1DashedThin: Style | None = None,
        RedBerry1Dotted: Style | None = None,
        RedBerry1DottedBold: Style | None = None,
        RedBerry1DottedThin: Style | None = None,
        RedBerry2: Style | None = None,
        RedBerry2Bordered: Style | None = None,
        RedBerry2Bold: Style | None = None,
        RedBerry2Thin: Style | None = None,
        RedBerry2Flat: Style | None = None,
        RedBerry2Outline: Style | None = None,
        RedBerry2Solid: Style | None = None,
        RedBerry2OutlineBold: Style | None = None,
        RedBerry2SolidBold: Style | None = None,
        RedBerry2OutlineThin: Style | None = None,
        RedBerry2SolidThin: Style | None = None,
        RedBerry2Dashed: Style | None = None,
        RedBerry2DashedBold: Style | None = None,
        RedBerry2DashedThin: Style | None = None,
        RedBerry2Dotted: Style | None = None,
        RedBerry2DottedBold: Style | None = None,
        RedBerry2DottedThin: Style | None = None,
        RedBerry3: Style | None = None,
        RedBerry3Bordered: Style | None = None,
        RedBerry3Bold: Style | None = None,
        RedBerry3Thin: Style | None = None,
        RedBerry3Flat: Style | None = None,
        RedBerry3Outline: Style | None = None,
        RedBerry3Solid: Style | None = None,
        RedBerry3OutlineBold: Style | None = None,
        RedBerry3SolidBold: Style | None = None,
        RedBerry3OutlineThin: Style | None = None,
        RedBerry3SolidThin: Style | None = None,
        RedBerry3Dashed: Style | None = None,
        RedBerry3DashedBold: Style | None = None,
        RedBerry3DashedThin: Style | None = None,
        RedBerry3Dotted: Style | None = None,
        RedBerry3DottedBold: Style | None = None,
        RedBerry3DottedThin: Style | None = None,
        RedBerry4: Style | None = None,
        RedBerry4Bordered: Style | None = None,
        RedBerry4Bold: Style | None = None,
        RedBerry4Thin: Style | None = None,
        RedBerry4Flat: Style | None = None,
        RedBerry4Outline: Style | None = None,
        RedBerry4Solid: Style | None = None,
        RedBerry4OutlineBold: Style | None = None,
        RedBerry4SolidBold: Style | None = None,
        RedBerry4OutlineThin: Style | None = None,
        RedBerry4SolidThin: Style | None = None,
        RedBerry4Dashed: Style | None = None,
        RedBerry4DashedBold: Style | None = None,
        RedBerry4DashedThin: Style | None = None,
        RedBerry4Dotted: Style | None = None,
        RedBerry4DottedBold: Style | None = None,
        RedBerry4DottedThin: Style | None = None,
        RedBerry5: Style | None = None,
        RedBerry5Bordered: Style | None = None,
        RedBerry5Bold: Style | None = None,
        RedBerry5Thin: Style | None = None,
        RedBerry5Flat: Style | None = None,
        RedBerry5Outline: Style | None = None,
        RedBerry5Solid: Style | None = None,
        RedBerry5OutlineBold: Style | None = None,
        RedBerry5SolidBold: Style | None = None,
        RedBerry5OutlineThin: Style | None = None,
        RedBerry5SolidThin: Style | None = None,
        RedBerry5Dashed: Style | None = None,
        RedBerry5DashedBold: Style | None = None,
        RedBerry5DashedThin: Style | None = None,
        RedBerry5Dotted: Style | None = None,
        RedBerry5DottedBold: Style | None = None,
        RedBerry5DottedThin: Style | None = None,
        RedBerry6: Style | None = None,
        RedBerry6Bordered: Style | None = None,
        RedBerry6Bold: Style | None = None,
        RedBerry6Thin: Style | None = None,
        RedBerry6Flat: Style | None = None,
        RedBerry6Outline: Style | None = None,
        RedBerry6Solid: Style | None = None,
        RedBerry6OutlineBold: Style | None = None,
        RedBerry6SolidBold: Style | None = None,
        RedBerry6OutlineThin: Style | None = None,
        RedBerry6SolidThin: Style | None = None,
        RedBerry6Dashed: Style | None = None,
        RedBerry6DashedBold: Style | None = None,
        RedBerry6DashedThin: Style | None = None,
        RedBerry6Dotted: Style | None = None,
        RedBerry6DottedBold: Style | None = None,
        RedBerry6DottedThin: Style | None = None,
        Green1: Style | None = None,
        Green1Bordered: Style | None = None,
        Green1Bold: Style | None = None,
        Green1Thin: Style | None = None,
        Green1Flat: Style | None = None,
        Green1Outline: Style | None = None,
        Green1Solid: Style | None = None,
        Green1OutlineBold: Style | None = None,
        Green1SolidBold: Style | None = None,
        Green1OutlineThin: Style | None = None,
        Green1SolidThin: Style | None = None,
        Green1Dashed: Style | None = None,
        Green1DashedBold: Style | None = None,
        Green1DashedThin: Style | None = None,
        Green1Dotted: Style | None = None,
        Green1DottedBold: Style | None = None,
        Green1DottedThin: Style | None = None,
        Green2: Style | None = None,
        Green2Bordered: Style | None = None,
        Green2Bold: Style | None = None,
        Green2Thin: Style | None = None,
        Green2Flat: Style | None = None,
        Green2Outline: Style | None = None,
        Green2Solid: Style | None = None,
        Green2OutlineBold: Style | None = None,
        Green2SolidBold: Style | None = None,
        Green2OutlineThin: Style | None = None,
        Green2SolidThin: Style | None = None,
        Green2Dashed: Style | None = None,
        Green2DashedBold: Style | None = None,
        Green2DashedThin: Style | None = None,
        Green2Dotted: Style | None = None,
        Green2DottedBold: Style | None = None,
        Green2DottedThin: Style | None = None,
        Green3: Style | None = None,
        Green3Bordered: Style | None = None,
        Green3Bold: Style | None = None,
        Green3Thin: Style | None = None,
        Green3Flat: Style | None = None,
        Green3Outline: Style | None = None,
        Green3Solid: Style | None = None,
        Green3OutlineBold: Style | None = None,
        Green3SolidBold: Style | None = None,
        Green3OutlineThin: Style | None = None,
        Green3SolidThin: Style | None = None,
        Green3Dashed: Style | None = None,
        Green3DashedBold: Style | None = None,
        Green3DashedThin: Style | None = None,
        Green3Dotted: Style | None = None,
        Green3DottedBold: Style | None = None,
        Green3DottedThin: Style | None = None,
        Green4: Style | None = None,
        Green4Bordered: Style | None = None,
        Green4Bold: Style | None = None,
        Green4Thin: Style | None = None,
        Green4Flat: Style | None = None,
        Green4Outline: Style | None = None,
        Green4Solid: Style | None = None,
        Green4OutlineBold: Style | None = None,
        Green4SolidBold: Style | None = None,
        Green4OutlineThin: Style | None = None,
        Green4SolidThin: Style | None = None,
        Green4Dashed: Style | None = None,
        Green4DashedBold: Style | None = None,
        Green4DashedThin: Style | None = None,
        Green4Dotted: Style | None = None,
        Green4DottedBold: Style | None = None,
        Green4DottedThin: Style | None = None,
        Green5: Style | None = None,
        Green5Bordered: Style | None = None,
        Green5Bold: Style | None = None,
        Green5Thin: Style | None = None,
        Green5Flat: Style | None = None,
        Green5Outline: Style | None = None,
        Green5Solid: Style | None = None,
        Green5OutlineBold: Style | None = None,
        Green5SolidBold: Style | None = None,
        Green5OutlineThin: Style | None = None,
        Green5SolidThin: Style | None = None,
        Green5Dashed: Style | None = None,
        Green5DashedBold: Style | None = None,
        Green5DashedThin: Style | None = None,
        Green5Dotted: Style | None = None,
        Green5DottedBold: Style | None = None,
        Green5DottedThin: Style | None = None,
        Green6: Style | None = None,
        Green6Bordered: Style | None = None,
        Green6Bold: Style | None = None,
        Green6Thin: Style | None = None,
        Green6Flat: Style | None = None,
        Green6Outline: Style | None = None,
        Green6Solid: Style | None = None,
        Green6OutlineBold: Style | None = None,
        Green6SolidBold: Style | None = None,
        Green6OutlineThin: Style | None = None,
        Green6SolidThin: Style | None = None,
        Green6Dashed: Style | None = None,
        Green6DashedBold: Style | None = None,
        Green6DashedThin: Style | None = None,
        Green6Dotted: Style | None = None,
        Green6DottedBold: Style | None = None,
        Green6DottedThin: Style | None = None,
        Yellow1: Style | None = None,
        Yellow1Bordered: Style | None = None,
        Yellow1Bold: Style | None = None,
        Yellow1Thin: Style | None = None,
        Yellow1Flat: Style | None = None,
        Yellow1Outline: Style | None = None,
        Yellow1Solid: Style | None = None,
        Yellow1OutlineBold: Style | None = None,
        Yellow1SolidBold: Style | None = None,
        Yellow1OutlineThin: Style | None = None,
        Yellow1SolidThin: Style | None = None,
        Yellow1Dashed: Style | None = None,
        Yellow1DashedBold: Style | None = None,
        Yellow1DashedThin: Style | None = None,
        Yellow1Dotted: Style | None = None,
        Yellow1DottedBold: Style | None = None,
        Yellow1DottedThin: Style | None = None,
        Yellow2: Style | None = None,
        Yellow2Bordered: Style | None = None,
        Yellow2Bold: Style | None = None,
        Yellow2Thin: Style | None = None,
        Yellow2Flat: Style | None = None,
        Yellow2Outline: Style | None = None,
        Yellow2Solid: Style | None = None,
        Yellow2OutlineBold: Style | None = None,
        Yellow2SolidBold: Style | None = None,
        Yellow2OutlineThin: Style | None = None,
        Yellow2SolidThin: Style | None = None,
        Yellow2Dashed: Style | None = None,
        Yellow2DashedBold: Style | None = None,
        Yellow2DashedThin: Style | None = None,
        Yellow2Dotted: Style | None = None,
        Yellow2DottedBold: Style | None = None,
        Yellow2DottedThin: Style | None = None,
        Yellow3: Style | None = None,
        Yellow3Bordered: Style | None = None,
        Yellow3Bold: Style | None = None,
        Yellow3Thin: Style | None = None,
        Yellow3Flat: Style | None = None,
        Yellow3Outline: Style | None = None,
        Yellow3Solid: Style | None = None,
        Yellow3OutlineBold: Style | None = None,
        Yellow3SolidBold: Style | None = None,
        Yellow3OutlineThin: Style | None = None,
        Yellow3SolidThin: Style | None = None,
        Yellow3Dashed: Style | None = None,
        Yellow3DashedBold: Style | None = None,
        Yellow3DashedThin: Style | None = None,
        Yellow3Dotted: Style | None = None,
        Yellow3DottedBold: Style | None = None,
        Yellow3DottedThin: Style | None = None,
        Yellow4: Style | None = None,
        Yellow4Bordered: Style | None = None,
        Yellow4Bold: Style | None = None,
        Yellow4Thin: Style | None = None,
        Yellow4Flat: Style | None = None,
        Yellow4Outline: Style | None = None,
        Yellow4Solid: Style | None = None,
        Yellow4OutlineBold: Style | None = None,
        Yellow4SolidBold: Style | None = None,
        Yellow4OutlineThin: Style | None = None,
        Yellow4SolidThin: Style | None = None,
        Yellow4Dashed: Style | None = None,
        Yellow4DashedBold: Style | None = None,
        Yellow4DashedThin: Style | None = None,
        Yellow4Dotted: Style | None = None,
        Yellow4DottedBold: Style | None = None,
        Yellow4DottedThin: Style | None = None,
        Yellow5: Style | None = None,
        Yellow5Bordered: Style | None = None,
        Yellow5Bold: Style | None = None,
        Yellow5Thin: Style | None = None,
        Yellow5Flat: Style | None = None,
        Yellow5Outline: Style | None = None,
        Yellow5Solid: Style | None = None,
        Yellow5OutlineBold: Style | None = None,
        Yellow5SolidBold: Style | None = None,
        Yellow5OutlineThin: Style | None = None,
        Yellow5SolidThin: Style | None = None,
        Yellow5Dashed: Style | None = None,
        Yellow5DashedBold: Style | None = None,
        Yellow5DashedThin: Style | None = None,
        Yellow5Dotted: Style | None = None,
        Yellow5DottedBold: Style | None = None,
        Yellow5DottedThin: Style | None = None,
        Yellow6: Style | None = None,
        Yellow6Bordered: Style | None = None,
        Yellow6Bold: Style | None = None,
        Yellow6Thin: Style | None = None,
        Yellow6Flat: Style | None = None,
        Yellow6Outline: Style | None = None,
        Yellow6Solid: Style | None = None,
        Yellow6OutlineBold: Style | None = None,
        Yellow6SolidBold: Style | None = None,
        Yellow6OutlineThin: Style | None = None,
        Yellow6SolidThin: Style | None = None,
        Yellow6Dashed: Style | None = None,
        Yellow6DashedBold: Style | None = None,
        Yellow6DashedThin: Style | None = None,
        Yellow6Dotted: Style | None = None,
        Yellow6DottedBold: Style | None = None,
        Yellow6DottedThin: Style | None = None,
        Orange1: Style | None = None,
        Orange1Bordered: Style | None = None,
        Orange1Bold: Style | None = None,
        Orange1Thin: Style | None = None,
        Orange1Flat: Style | None = None,
        Orange1Outline: Style | None = None,
        Orange1Solid: Style | None = None,
        Orange1OutlineBold: Style | None = None,
        Orange1SolidBold: Style | None = None,
        Orange1OutlineThin: Style | None = None,
        Orange1SolidThin: Style | None = None,
        Orange1Dashed: Style | None = None,
        Orange1DashedBold: Style | None = None,
        Orange1DashedThin: Style | None = None,
        Orange1Dotted: Style | None = None,
        Orange1DottedBold: Style | None = None,
        Orange1DottedThin: Style | None = None,
        Orange2: Style | None = None,
        Orange2Bordered: Style | None = None,
        Orange2Bold: Style | None = None,
        Orange2Thin: Style | None = None,
        Orange2Flat: Style | None = None,
        Orange2Outline: Style | None = None,
        Orange2Solid: Style | None = None,
        Orange2OutlineBold: Style | None = None,
        Orange2SolidBold: Style | None = None,
        Orange2OutlineThin: Style | None = None,
        Orange2SolidThin: Style | None = None,
        Orange2Dashed: Style | None = None,
        Orange2DashedBold: Style | None = None,
        Orange2DashedThin: Style | None = None,
        Orange2Dotted: Style | None = None,
        Orange2DottedBold: Style | None = None,
        Orange2DottedThin: Style | None = None,
        Orange3: Style | None = None,
        Orange3Bordered: Style | None = None,
        Orange3Bold: Style | None = None,
        Orange3Thin: Style | None = None,
        Orange3Flat: Style | None = None,
        Orange3Outline: Style | None = None,
        Orange3Solid: Style | None = None,
        Orange3OutlineBold: Style | None = None,
        Orange3SolidBold: Style | None = None,
        Orange3OutlineThin: Style | None = None,
        Orange3SolidThin: Style | None = None,
        Orange3Dashed: Style | None = None,
        Orange3DashedBold: Style | None = None,
        Orange3DashedThin: Style | None = None,
        Orange3Dotted: Style | None = None,
        Orange3DottedBold: Style | None = None,
        Orange3DottedThin: Style | None = None,
        Orange4: Style | None = None,
        Orange4Bordered: Style | None = None,
        Orange4Bold: Style | None = None,
        Orange4Thin: Style | None = None,
        Orange4Flat: Style | None = None,
        Orange4Outline: Style | None = None,
        Orange4Solid: Style | None = None,
        Orange4OutlineBold: Style | None = None,
        Orange4SolidBold: Style | None = None,
        Orange4OutlineThin: Style | None = None,
        Orange4SolidThin: Style | None = None,
        Orange4Dashed: Style | None = None,
        Orange4DashedBold: Style | None = None,
        Orange4DashedThin: Style | None = None,
        Orange4Dotted: Style | None = None,
        Orange4DottedBold: Style | None = None,
        Orange4DottedThin: Style | None = None,
        Orange5: Style | None = None,
        Orange5Bordered: Style | None = None,
        Orange5Bold: Style | None = None,
        Orange5Thin: Style | None = None,
        Orange5Flat: Style | None = None,
        Orange5Outline: Style | None = None,
        Orange5Solid: Style | None = None,
        Orange5OutlineBold: Style | None = None,
        Orange5SolidBold: Style | None = None,
        Orange5OutlineThin: Style | None = None,
        Orange5SolidThin: Style | None = None,
        Orange5Dashed: Style | None = None,
        Orange5DashedBold: Style | None = None,
        Orange5DashedThin: Style | None = None,
        Orange5Dotted: Style | None = None,
        Orange5DottedBold: Style | None = None,
        Orange5DottedThin: Style | None = None,
        Orange6: Style | None = None,
        Orange6Bordered: Style | None = None,
        Orange6Bold: Style | None = None,
        Orange6Thin: Style | None = None,
        Orange6Flat: Style | None = None,
        Orange6Outline: Style | None = None,
        Orange6Solid: Style | None = None,
        Orange6OutlineBold: Style | None = None,
        Orange6SolidBold: Style | None = None,
        Orange6OutlineThin: Style | None = None,
        Orange6SolidThin: Style | None = None,
        Orange6Dashed: Style | None = None,
        Orange6DashedBold: Style | None = None,
        Orange6DashedThin: Style | None = None,
        Orange6Dotted: Style | None = None,
        Orange6DottedBold: Style | None = None,
        Orange6DottedThin: Style | None = None,
        Cyan1: Style | None = None,
        Cyan1Bordered: Style | None = None,
        Cyan1Bold: Style | None = None,
        Cyan1Thin: Style | None = None,
        Cyan1Flat: Style | None = None,
        Cyan1Outline: Style | None = None,
        Cyan1Solid: Style | None = None,
        Cyan1OutlineBold: Style | None = None,
        Cyan1SolidBold: Style | None = None,
        Cyan1OutlineThin: Style | None = None,
        Cyan1SolidThin: Style | None = None,
        Cyan1Dashed: Style | None = None,
        Cyan1DashedBold: Style | None = None,
        Cyan1DashedThin: Style | None = None,
        Cyan1Dotted: Style | None = None,
        Cyan1DottedBold: Style | None = None,
        Cyan1DottedThin: Style | None = None,
        Cyan2: Style | None = None,
        Cyan2Bordered: Style | None = None,
        Cyan2Bold: Style | None = None,
        Cyan2Thin: Style | None = None,
        Cyan2Flat: Style | None = None,
        Cyan2Outline: Style | None = None,
        Cyan2Solid: Style | None = None,
        Cyan2OutlineBold: Style | None = None,
        Cyan2SolidBold: Style | None = None,
        Cyan2OutlineThin: Style | None = None,
        Cyan2SolidThin: Style | None = None,
        Cyan2Dashed: Style | None = None,
        Cyan2DashedBold: Style | None = None,
        Cyan2DashedThin: Style | None = None,
        Cyan2Dotted: Style | None = None,
        Cyan2DottedBold: Style | None = None,
        Cyan2DottedThin: Style | None = None,
        Cyan3: Style | None = None,
        Cyan3Bordered: Style | None = None,
        Cyan3Bold: Style | None = None,
        Cyan3Thin: Style | None = None,
        Cyan3Flat: Style | None = None,
        Cyan3Outline: Style | None = None,
        Cyan3Solid: Style | None = None,
        Cyan3OutlineBold: Style | None = None,
        Cyan3SolidBold: Style | None = None,
        Cyan3OutlineThin: Style | None = None,
        Cyan3SolidThin: Style | None = None,
        Cyan3Dashed: Style | None = None,
        Cyan3DashedBold: Style | None = None,
        Cyan3DashedThin: Style | None = None,
        Cyan3Dotted: Style | None = None,
        Cyan3DottedBold: Style | None = None,
        Cyan3DottedThin: Style | None = None,
        Cyan4: Style | None = None,
        Cyan4Bordered: Style | None = None,
        Cyan4Bold: Style | None = None,
        Cyan4Thin: Style | None = None,
        Cyan4Flat: Style | None = None,
        Cyan4Outline: Style | None = None,
        Cyan4Solid: Style | None = None,
        Cyan4OutlineBold: Style | None = None,
        Cyan4SolidBold: Style | None = None,
        Cyan4OutlineThin: Style | None = None,
        Cyan4SolidThin: Style | None = None,
        Cyan4Dashed: Style | None = None,
        Cyan4DashedBold: Style | None = None,
        Cyan4DashedThin: Style | None = None,
        Cyan4Dotted: Style | None = None,
        Cyan4DottedBold: Style | None = None,
        Cyan4DottedThin: Style | None = None,
        Cyan5: Style | None = None,
        Cyan5Bordered: Style | None = None,
        Cyan5Bold: Style | None = None,
        Cyan5Thin: Style | None = None,
        Cyan5Flat: Style | None = None,
        Cyan5Outline: Style | None = None,
        Cyan5Solid: Style | None = None,
        Cyan5OutlineBold: Style | None = None,
        Cyan5SolidBold: Style | None = None,
        Cyan5OutlineThin: Style | None = None,
        Cyan5SolidThin: Style | None = None,
        Cyan5Dashed: Style | None = None,
        Cyan5DashedBold: Style | None = None,
        Cyan5DashedThin: Style | None = None,
        Cyan5Dotted: Style | None = None,
        Cyan5DottedBold: Style | None = None,
        Cyan5DottedThin: Style | None = None,
        Cyan6: Style | None = None,
        Cyan6Bordered: Style | None = None,
        Cyan6Bold: Style | None = None,
        Cyan6Thin: Style | None = None,
        Cyan6Flat: Style | None = None,
        Cyan6Outline: Style | None = None,
        Cyan6Solid: Style | None = None,
        Cyan6OutlineBold: Style | None = None,
        Cyan6SolidBold: Style | None = None,
        Cyan6OutlineThin: Style | None = None,
        Cyan6SolidThin: Style | None = None,
        Cyan6Dashed: Style | None = None,
        Cyan6DashedBold: Style | None = None,
        Cyan6DashedThin: Style | None = None,
        Cyan6Dotted: Style | None = None,
        Cyan6DottedBold: Style | None = None,
        Cyan6DottedThin: Style | None = None,
        Purple1: Style | None = None,
        Purple1Bordered: Style | None = None,
        Purple1Bold: Style | None = None,
        Purple1Thin: Style | None = None,
        Purple1Flat: Style | None = None,
        Purple1Outline: Style | None = None,
        Purple1Solid: Style | None = None,
        Purple1OutlineBold: Style | None = None,
        Purple1SolidBold: Style | None = None,
        Purple1OutlineThin: Style | None = None,
        Purple1SolidThin: Style | None = None,
        Purple1Dashed: Style | None = None,
        Purple1DashedBold: Style | None = None,
        Purple1DashedThin: Style | None = None,
        Purple1Dotted: Style | None = None,
        Purple1DottedBold: Style | None = None,
        Purple1DottedThin: Style | None = None,
        Purple2: Style | None = None,
        Purple2Bordered: Style | None = None,
        Purple2Bold: Style | None = None,
        Purple2Thin: Style | None = None,
        Purple2Flat: Style | None = None,
        Purple2Outline: Style | None = None,
        Purple2Solid: Style | None = None,
        Purple2OutlineBold: Style | None = None,
        Purple2SolidBold: Style | None = None,
        Purple2OutlineThin: Style | None = None,
        Purple2SolidThin: Style | None = None,
        Purple2Dashed: Style | None = None,
        Purple2DashedBold: Style | None = None,
        Purple2DashedThin: Style | None = None,
        Purple2Dotted: Style | None = None,
        Purple2DottedBold: Style | None = None,
        Purple2DottedThin: Style | None = None,
        Purple3: Style | None = None,
        Purple3Bordered: Style | None = None,
        Purple3Bold: Style | None = None,
        Purple3Thin: Style | None = None,
        Purple3Flat: Style | None = None,
        Purple3Outline: Style | None = None,
        Purple3Solid: Style | None = None,
        Purple3OutlineBold: Style | None = None,
        Purple3SolidBold: Style | None = None,
        Purple3OutlineThin: Style | None = None,
        Purple3SolidThin: Style | None = None,
        Purple3Dashed: Style | None = None,
        Purple3DashedBold: Style | None = None,
        Purple3DashedThin: Style | None = None,
        Purple3Dotted: Style | None = None,
        Purple3DottedBold: Style | None = None,
        Purple3DottedThin: Style | None = None,
        Purple4: Style | None = None,
        Purple4Bordered: Style | None = None,
        Purple4Bold: Style | None = None,
        Purple4Thin: Style | None = None,
        Purple4Flat: Style | None = None,
        Purple4Outline: Style | None = None,
        Purple4Solid: Style | None = None,
        Purple4OutlineBold: Style | None = None,
        Purple4SolidBold: Style | None = None,
        Purple4OutlineThin: Style | None = None,
        Purple4SolidThin: Style | None = None,
        Purple4Dashed: Style | None = None,
        Purple4DashedBold: Style | None = None,
        Purple4DashedThin: Style | None = None,
        Purple4Dotted: Style | None = None,
        Purple4DottedBold: Style | None = None,
        Purple4DottedThin: Style | None = None,
        Purple5: Style | None = None,
        Purple5Bordered: Style | None = None,
        Purple5Bold: Style | None = None,
        Purple5Thin: Style | None = None,
        Purple5Flat: Style | None = None,
        Purple5Outline: Style | None = None,
        Purple5Solid: Style | None = None,
        Purple5OutlineBold: Style | None = None,
        Purple5SolidBold: Style | None = None,
        Purple5OutlineThin: Style | None = None,
        Purple5SolidThin: Style | None = None,
        Purple5Dashed: Style | None = None,
        Purple5DashedBold: Style | None = None,
        Purple5DashedThin: Style | None = None,
        Purple5Dotted: Style | None = None,
        Purple5DottedBold: Style | None = None,
        Purple5DottedThin: Style | None = None,
        Purple6: Style | None = None,
        Purple6Bordered: Style | None = None,
        Purple6Bold: Style | None = None,
        Purple6Thin: Style | None = None,
        Purple6Flat: Style | None = None,
        Purple6Outline: Style | None = None,
        Purple6Solid: Style | None = None,
        Purple6OutlineBold: Style | None = None,
        Purple6SolidBold: Style | None = None,
        Purple6OutlineThin: Style | None = None,
        Purple6SolidThin: Style | None = None,
        Purple6Dashed: Style | None = None,
        Purple6DashedBold: Style | None = None,
        Purple6DashedThin: Style | None = None,
        Purple6Dotted: Style | None = None,
        Purple6DottedBold: Style | None = None,
        Purple6DottedThin: Style | None = None,
        Magenta1: Style | None = None,
        Magenta1Bordered: Style | None = None,
        Magenta1Bold: Style | None = None,
        Magenta1Thin: Style | None = None,
        Magenta1Flat: Style | None = None,
        Magenta1Outline: Style | None = None,
        Magenta1Solid: Style | None = None,
        Magenta1OutlineBold: Style | None = None,
        Magenta1SolidBold: Style | None = None,
        Magenta1OutlineThin: Style | None = None,
        Magenta1SolidThin: Style | None = None,
        Magenta1Dashed: Style | None = None,
        Magenta1DashedBold: Style | None = None,
        Magenta1DashedThin: Style | None = None,
        Magenta1Dotted: Style | None = None,
        Magenta1DottedBold: Style | None = None,
        Magenta1DottedThin: Style | None = None,
        Magenta2: Style | None = None,
        Magenta2Bordered: Style | None = None,
        Magenta2Bold: Style | None = None,
        Magenta2Thin: Style | None = None,
        Magenta2Flat: Style | None = None,
        Magenta2Outline: Style | None = None,
        Magenta2Solid: Style | None = None,
        Magenta2OutlineBold: Style | None = None,
        Magenta2SolidBold: Style | None = None,
        Magenta2OutlineThin: Style | None = None,
        Magenta2SolidThin: Style | None = None,
        Magenta2Dashed: Style | None = None,
        Magenta2DashedBold: Style | None = None,
        Magenta2DashedThin: Style | None = None,
        Magenta2Dotted: Style | None = None,
        Magenta2DottedBold: Style | None = None,
        Magenta2DottedThin: Style | None = None,
        Magenta3: Style | None = None,
        Magenta3Bordered: Style | None = None,
        Magenta3Bold: Style | None = None,
        Magenta3Thin: Style | None = None,
        Magenta3Flat: Style | None = None,
        Magenta3Outline: Style | None = None,
        Magenta3Solid: Style | None = None,
        Magenta3OutlineBold: Style | None = None,
        Magenta3SolidBold: Style | None = None,
        Magenta3OutlineThin: Style | None = None,
        Magenta3SolidThin: Style | None = None,
        Magenta3Dashed: Style | None = None,
        Magenta3DashedBold: Style | None = None,
        Magenta3DashedThin: Style | None = None,
        Magenta3Dotted: Style | None = None,
        Magenta3DottedBold: Style | None = None,
        Magenta3DottedThin: Style | None = None,
        Magenta4: Style | None = None,
        Magenta4Bordered: Style | None = None,
        Magenta4Bold: Style | None = None,
        Magenta4Thin: Style | None = None,
        Magenta4Flat: Style | None = None,
        Magenta4Outline: Style | None = None,
        Magenta4Solid: Style | None = None,
        Magenta4OutlineBold: Style | None = None,
        Magenta4SolidBold: Style | None = None,
        Magenta4OutlineThin: Style | None = None,
        Magenta4SolidThin: Style | None = None,
        Magenta4Dashed: Style | None = None,
        Magenta4DashedBold: Style | None = None,
        Magenta4DashedThin: Style | None = None,
        Magenta4Dotted: Style | None = None,
        Magenta4DottedBold: Style | None = None,
        Magenta4DottedThin: Style | None = None,
        Magenta5: Style | None = None,
        Magenta5Bordered: Style | None = None,
        Magenta5Bold: Style | None = None,
        Magenta5Thin: Style | None = None,
        Magenta5Flat: Style | None = None,
        Magenta5Outline: Style | None = None,
        Magenta5Solid: Style | None = None,
        Magenta5OutlineBold: Style | None = None,
        Magenta5SolidBold: Style | None = None,
        Magenta5OutlineThin: Style | None = None,
        Magenta5SolidThin: Style | None = None,
        Magenta5Dashed: Style | None = None,
        Magenta5DashedBold: Style | None = None,
        Magenta5DashedThin: Style | None = None,
        Magenta5Dotted: Style | None = None,
        Magenta5DottedBold: Style | None = None,
        Magenta5DottedThin: Style | None = None,
        Magenta6: Style | None = None,
        Magenta6Bordered: Style | None = None,
        Magenta6Bold: Style | None = None,
        Magenta6Thin: Style | None = None,
        Magenta6Flat: Style | None = None,
        Magenta6Outline: Style | None = None,
        Magenta6Solid: Style | None = None,
        Magenta6OutlineBold: Style | None = None,
        Magenta6SolidBold: Style | None = None,
        Magenta6OutlineThin: Style | None = None,
        Magenta6SolidThin: Style | None = None,
        Magenta6Dashed: Style | None = None,
        Magenta6DashedBold: Style | None = None,
        Magenta6DashedThin: Style | None = None,
        Magenta6Dotted: Style | None = None,
        Magenta6DottedBold: Style | None = None,
        Magenta6DottedThin: Style | None = None,
        CornflowerBlue: Style | None = None,
        CornflowerBlueBordered: Style | None = None,
        CornflowerBlueBold: Style | None = None,
        CornflowerBlueThin: Style | None = None,
        CornflowerBlueFlat: Style | None = None,
        CornflowerBlueOutline: Style | None = None,
        CornflowerBlueSolid: Style | None = None,
        CornflowerBlueOutlineBold: Style | None = None,
        CornflowerBlueSolidBold: Style | None = None,
        CornflowerBlueOutlineThin: Style | None = None,
        CornflowerBlueSolidThin: Style | None = None,
        CornflowerBlueDashed: Style | None = None,
        CornflowerBlueDashedBold: Style | None = None,
        CornflowerBlueDashedThin: Style | None = None,
        CornflowerBlueDotted: Style | None = None,
        CornflowerBlueDottedBold: Style | None = None,
        CornflowerBlueDottedThin: Style | None = None,
        Blue: Style | None = None,
        BlueBordered: Style | None = None,
        BlueBold: Style | None = None,
        BlueThin: Style | None = None,
        BlueFlat: Style | None = None,
        BlueOutline: Style | None = None,
        BlueSolid: Style | None = None,
        BlueOutlineBold: Style | None = None,
        BlueSolidBold: Style | None = None,
        BlueOutlineThin: Style | None = None,
        BlueSolidThin: Style | None = None,
        BlueDashed: Style | None = None,
        BlueDashedBold: Style | None = None,
        BlueDashedThin: Style | None = None,
        BlueDotted: Style | None = None,
        BlueDottedBold: Style | None = None,
        BlueDottedThin: Style | None = None,
        Red: Style | None = None,
        RedBordered: Style | None = None,
        RedBold: Style | None = None,
        RedThin: Style | None = None,
        RedFlat: Style | None = None,
        RedOutline: Style | None = None,
        RedSolid: Style | None = None,
        RedOutlineBold: Style | None = None,
        RedSolidBold: Style | None = None,
        RedOutlineThin: Style | None = None,
        RedSolidThin: Style | None = None,
        RedDashed: Style | None = None,
        RedDashedBold: Style | None = None,
        RedDashedThin: Style | None = None,
        RedDotted: Style | None = None,
        RedDottedBold: Style | None = None,
        RedDottedThin: Style | None = None,
        RedBerry: Style | None = None,
        RedBerryBordered: Style | None = None,
        RedBerryBold: Style | None = None,
        RedBerryThin: Style | None = None,
        RedBerryFlat: Style | None = None,
        RedBerryOutline: Style | None = None,
        RedBerrySolid: Style | None = None,
        RedBerryOutlineBold: Style | None = None,
        RedBerrySolidBold: Style | None = None,
        RedBerryOutlineThin: Style | None = None,
        RedBerrySolidThin: Style | None = None,
        RedBerryDashed: Style | None = None,
        RedBerryDashedBold: Style | None = None,
        RedBerryDashedThin: Style | None = None,
        RedBerryDotted: Style | None = None,
        RedBerryDottedBold: Style | None = None,
        RedBerryDottedThin: Style | None = None,
        Green: Style | None = None,
        GreenBordered: Style | None = None,
        GreenBold: Style | None = None,
        GreenThin: Style | None = None,
        GreenFlat: Style | None = None,
        GreenOutline: Style | None = None,
        GreenSolid: Style | None = None,
        GreenOutlineBold: Style | None = None,
        GreenSolidBold: Style | None = None,
        GreenOutlineThin: Style | None = None,
        GreenSolidThin: Style | None = None,
        GreenDashed: Style | None = None,
        GreenDashedBold: Style | None = None,
        GreenDashedThin: Style | None = None,
        GreenDotted: Style | None = None,
        GreenDottedBold: Style | None = None,
        GreenDottedThin: Style | None = None,
        Yellow: Style | None = None,
        YellowBordered: Style | None = None,
        YellowBold: Style | None = None,
        YellowThin: Style | None = None,
        YellowFlat: Style | None = None,
        YellowOutline: Style | None = None,
        YellowSolid: Style | None = None,
        YellowOutlineBold: Style | None = None,
        YellowSolidBold: Style | None = None,
        YellowOutlineThin: Style | None = None,
        YellowSolidThin: Style | None = None,
        YellowDashed: Style | None = None,
        YellowDashedBold: Style | None = None,
        YellowDashedThin: Style | None = None,
        YellowDotted: Style | None = None,
        YellowDottedBold: Style | None = None,
        YellowDottedThin: Style | None = None,
        Orange: Style | None = None,
        OrangeBordered: Style | None = None,
        OrangeBold: Style | None = None,
        OrangeThin: Style | None = None,
        OrangeFlat: Style | None = None,
        OrangeOutline: Style | None = None,
        OrangeSolid: Style | None = None,
        OrangeOutlineBold: Style | None = None,
        OrangeSolidBold: Style | None = None,
        OrangeOutlineThin: Style | None = None,
        OrangeSolidThin: Style | None = None,
        OrangeDashed: Style | None = None,
        OrangeDashedBold: Style | None = None,
        OrangeDashedThin: Style | None = None,
        OrangeDotted: Style | None = None,
        OrangeDottedBold: Style | None = None,
        OrangeDottedThin: Style | None = None,
        Cyan: Style | None = None,
        CyanBordered: Style | None = None,
        CyanBold: Style | None = None,
        CyanThin: Style | None = None,
        CyanFlat: Style | None = None,
        CyanOutline: Style | None = None,
        CyanSolid: Style | None = None,
        CyanOutlineBold: Style | None = None,
        CyanSolidBold: Style | None = None,
        CyanOutlineThin: Style | None = None,
        CyanSolidThin: Style | None = None,
        CyanDashed: Style | None = None,
        CyanDashedBold: Style | None = None,
        CyanDashedThin: Style | None = None,
        CyanDotted: Style | None = None,
        CyanDottedBold: Style | None = None,
        CyanDottedThin: Style | None = None,
        Purple: Style | None = None,
        PurpleBordered: Style | None = None,
        PurpleBold: Style | None = None,
        PurpleThin: Style | None = None,
        PurpleFlat: Style | None = None,
        PurpleOutline: Style | None = None,
        PurpleSolid: Style | None = None,
        PurpleOutlineBold: Style | None = None,
        PurpleSolidBold: Style | None = None,
        PurpleOutlineThin: Style | None = None,
        PurpleSolidThin: Style | None = None,
        PurpleDashed: Style | None = None,
        PurpleDashedBold: Style | None = None,
        PurpleDashedThin: Style | None = None,
        PurpleDotted: Style | None = None,
        PurpleDottedBold: Style | None = None,
        PurpleDottedThin: Style | None = None,
        Magenta: Style | None = None,
        MagentaBordered: Style | None = None,
        MagentaBold: Style | None = None,
        MagentaThin: Style | None = None,
        MagentaFlat: Style | None = None,
        MagentaOutline: Style | None = None,
        MagentaSolid: Style | None = None,
        MagentaOutlineBold: Style | None = None,
        MagentaSolidBold: Style | None = None,
        MagentaOutlineThin: Style | None = None,
        MagentaSolidThin: Style | None = None,
        MagentaDashed: Style | None = None,
        MagentaDashedBold: Style | None = None,
        MagentaDashedThin: Style | None = None,
        MagentaDotted: Style | None = None,
        MagentaDottedBold: Style | None = None,
        MagentaDottedThin: Style | None = None,
        Pink: Style | None = None,
        PinkBordered: Style | None = None,
        PinkBold: Style | None = None,
        PinkThin: Style | None = None,
        PinkFlat: Style | None = None,
        PinkOutline: Style | None = None,
        PinkSolid: Style | None = None,
        PinkOutlineBold: Style | None = None,
        PinkSolidBold: Style | None = None,
        PinkOutlineThin: Style | None = None,
        PinkSolidThin: Style | None = None,
        PinkDashed: Style | None = None,
        PinkDashedBold: Style | None = None,
        PinkDashedThin: Style | None = None,
        PinkDotted: Style | None = None,
        PinkDottedBold: Style | None = None,
        PinkDottedThin: Style | None = None,
        Lime: Style | None = None,
        LimeBordered: Style | None = None,
        LimeBold: Style | None = None,
        LimeThin: Style | None = None,
        LimeFlat: Style | None = None,
        LimeOutline: Style | None = None,
        LimeSolid: Style | None = None,
        LimeOutlineBold: Style | None = None,
        LimeSolidBold: Style | None = None,
        LimeOutlineThin: Style | None = None,
        LimeSolidThin: Style | None = None,
        LimeDashed: Style | None = None,
        LimeDashedBold: Style | None = None,
        LimeDashedThin: Style | None = None,
        LimeDotted: Style | None = None,
        LimeDottedBold: Style | None = None,
        LimeDottedThin: Style | None = None,
        Teal: Style | None = None,
        TealBordered: Style | None = None,
        TealBold: Style | None = None,
        TealThin: Style | None = None,
        TealFlat: Style | None = None,
        TealOutline: Style | None = None,
        TealSolid: Style | None = None,
        TealOutlineBold: Style | None = None,
        TealSolidBold: Style | None = None,
        TealOutlineThin: Style | None = None,
        TealSolidThin: Style | None = None,
        TealDashed: Style | None = None,
        TealDashedBold: Style | None = None,
        TealDashedThin: Style | None = None,
        TealDotted: Style | None = None,
        TealDottedBold: Style | None = None,
        TealDottedThin: Style | None = None,
        Navy: Style | None = None,
        NavyBordered: Style | None = None,
        NavyBold: Style | None = None,
        NavyThin: Style | None = None,
        NavyFlat: Style | None = None,
        NavyOutline: Style | None = None,
        NavySolid: Style | None = None,
        NavyOutlineBold: Style | None = None,
        NavySolidBold: Style | None = None,
        NavyOutlineThin: Style | None = None,
        NavySolidThin: Style | None = None,
        NavyDashed: Style | None = None,
        NavyDashedBold: Style | None = None,
        NavyDashedThin: Style | None = None,
        NavyDotted: Style | None = None,
        NavyDottedBold: Style | None = None,
        NavyDottedThin: Style | None = None,
        Olive: Style | None = None,
        OliveBordered: Style | None = None,
        OliveBold: Style | None = None,
        OliveThin: Style | None = None,
        OliveFlat: Style | None = None,
        OliveOutline: Style | None = None,
        OliveSolid: Style | None = None,
        OliveOutlineBold: Style | None = None,
        OliveSolidBold: Style | None = None,
        OliveOutlineThin: Style | None = None,
        OliveSolidThin: Style | None = None,
        OliveDashed: Style | None = None,
        OliveDashedBold: Style | None = None,
        OliveDashedThin: Style | None = None,
        OliveDotted: Style | None = None,
        OliveDottedBold: Style | None = None,
        OliveDottedThin: Style | None = None,
        Brown: Style | None = None,
        BrownBordered: Style | None = None,
        BrownBold: Style | None = None,
        BrownThin: Style | None = None,
        BrownFlat: Style | None = None,
        BrownOutline: Style | None = None,
        BrownSolid: Style | None = None,
        BrownOutlineBold: Style | None = None,
        BrownSolidBold: Style | None = None,
        BrownOutlineThin: Style | None = None,
        BrownSolidThin: Style | None = None,
        BrownDashed: Style | None = None,
        BrownDashedBold: Style | None = None,
        BrownDashedThin: Style | None = None,
        BrownDotted: Style | None = None,
        BrownDottedBold: Style | None = None,
        BrownDottedThin: Style | None = None,
        Gold: Style | None = None,
        GoldBordered: Style | None = None,
        GoldBold: Style | None = None,
        GoldThin: Style | None = None,
        GoldFlat: Style | None = None,
        GoldOutline: Style | None = None,
        GoldSolid: Style | None = None,
        GoldOutlineBold: Style | None = None,
        GoldSolidBold: Style | None = None,
        GoldOutlineThin: Style | None = None,
        GoldSolidThin: Style | None = None,
        GoldDashed: Style | None = None,
        GoldDashedBold: Style | None = None,
        GoldDashedThin: Style | None = None,
        GoldDotted: Style | None = None,
        GoldDottedBold: Style | None = None,
        GoldDottedThin: Style | None = None,
        Aqua: Style | None = None,
        AquaBordered: Style | None = None,
        AquaBold: Style | None = None,
        AquaThin: Style | None = None,
        AquaFlat: Style | None = None,
        AquaOutline: Style | None = None,
        AquaSolid: Style | None = None,
        AquaOutlineBold: Style | None = None,
        AquaSolidBold: Style | None = None,
        AquaOutlineThin: Style | None = None,
        AquaSolidThin: Style | None = None,
        AquaDashed: Style | None = None,
        AquaDashedBold: Style | None = None,
        AquaDashedThin: Style | None = None,
        AquaDotted: Style | None = None,
        AquaDottedBold: Style | None = None,
        AquaDottedThin: Style | None = None,
        GreenYellow: Style | None = None,
        GreenYellowBordered: Style | None = None,
        GreenYellowBold: Style | None = None,
        GreenYellowThin: Style | None = None,
        GreenYellowFlat: Style | None = None,
        GreenYellowOutline: Style | None = None,
        GreenYellowSolid: Style | None = None,
        GreenYellowOutlineBold: Style | None = None,
        GreenYellowSolidBold: Style | None = None,
        GreenYellowOutlineThin: Style | None = None,
        GreenYellowSolidThin: Style | None = None,
        GreenYellowDashed: Style | None = None,
        GreenYellowDashedBold: Style | None = None,
        GreenYellowDashedThin: Style | None = None,
        GreenYellowDotted: Style | None = None,
        GreenYellowDottedBold: Style | None = None,
        GreenYellowDottedThin: Style | None = None,
        Ivory: Style | None = None,
        IvoryBordered: Style | None = None,
        IvoryBold: Style | None = None,
        IvoryThin: Style | None = None,
        IvoryFlat: Style | None = None,
        IvoryOutline: Style | None = None,
        IvorySolid: Style | None = None,
        IvoryOutlineBold: Style | None = None,
        IvorySolidBold: Style | None = None,
        IvoryOutlineThin: Style | None = None,
        IvorySolidThin: Style | None = None,
        IvoryDashed: Style | None = None,
        IvoryDashedBold: Style | None = None,
        IvoryDashedThin: Style | None = None,
        IvoryDotted: Style | None = None,
        IvoryDottedBold: Style | None = None,
        IvoryDottedThin: Style | None = None,
        Steel: Style | None = None,
        SteelBordered: Style | None = None,
        SteelBold: Style | None = None,
        SteelThin: Style | None = None,
        SteelFlat: Style | None = None,
        SteelOutline: Style | None = None,
        SteelSolid: Style | None = None,
        SteelOutlineBold: Style | None = None,
        SteelSolidBold: Style | None = None,
        SteelOutlineThin: Style | None = None,
        SteelSolidThin: Style | None = None,
        SteelDashed: Style | None = None,
        SteelDashedBold: Style | None = None,
        SteelDashedThin: Style | None = None,
        SteelDotted: Style | None = None,
        SteelDottedBold: Style | None = None,
        SteelDottedThin: Style | None = None,
        GoogleBlue: Style | None = None,
        GoogleBlueBordered: Style | None = None,
        GoogleBlueBold: Style | None = None,
        GoogleBlueThin: Style | None = None,
        GoogleBlueFlat: Style | None = None,
        GoogleBlueOutline: Style | None = None,
        GoogleBlueSolid: Style | None = None,
        GoogleBlueOutlineBold: Style | None = None,
        GoogleBlueSolidBold: Style | None = None,
        GoogleBlueOutlineThin: Style | None = None,
        GoogleBlueSolidThin: Style | None = None,
        GoogleBlueDashed: Style | None = None,
        GoogleBlueDashedBold: Style | None = None,
        GoogleBlueDashedThin: Style | None = None,
        GoogleBlueDotted: Style | None = None,
        GoogleBlueDottedBold: Style | None = None,
        GoogleBlueDottedThin: Style | None = None,
        GoogleRed: Style | None = None,
        GoogleRedBordered: Style | None = None,
        GoogleRedBold: Style | None = None,
        GoogleRedThin: Style | None = None,
        GoogleRedFlat: Style | None = None,
        GoogleRedOutline: Style | None = None,
        GoogleRedSolid: Style | None = None,
        GoogleRedOutlineBold: Style | None = None,
        GoogleRedSolidBold: Style | None = None,
        GoogleRedOutlineThin: Style | None = None,
        GoogleRedSolidThin: Style | None = None,
        GoogleRedDashed: Style | None = None,
        GoogleRedDashedBold: Style | None = None,
        GoogleRedDashedThin: Style | None = None,
        GoogleRedDotted: Style | None = None,
        GoogleRedDottedBold: Style | None = None,
        GoogleRedDottedThin: Style | None = None,
        GoogleYellow: Style | None = None,
        GoogleYellowBordered: Style | None = None,
        GoogleYellowBold: Style | None = None,
        GoogleYellowThin: Style | None = None,
        GoogleYellowFlat: Style | None = None,
        GoogleYellowOutline: Style | None = None,
        GoogleYellowSolid: Style | None = None,
        GoogleYellowOutlineBold: Style | None = None,
        GoogleYellowSolidBold: Style | None = None,
        GoogleYellowOutlineThin: Style | None = None,
        GoogleYellowSolidThin: Style | None = None,
        GoogleYellowDashed: Style | None = None,
        GoogleYellowDashedBold: Style | None = None,
        GoogleYellowDashedThin: Style | None = None,
        GoogleYellowDotted: Style | None = None,
        GoogleYellowDottedBold: Style | None = None,
        GoogleYellowDottedThin: Style | None = None,
        GoogleGreen: Style | None = None,
        GoogleGreenBordered: Style | None = None,
        GoogleGreenBold: Style | None = None,
        GoogleGreenThin: Style | None = None,
        GoogleGreenFlat: Style | None = None,
        GoogleGreenOutline: Style | None = None,
        GoogleGreenSolid: Style | None = None,
        GoogleGreenOutlineBold: Style | None = None,
        GoogleGreenSolidBold: Style | None = None,
        GoogleGreenOutlineThin: Style | None = None,
        GoogleGreenSolidThin: Style | None = None,
        GoogleGreenDashed: Style | None = None,
        GoogleGreenDashedBold: Style | None = None,
        GoogleGreenDashedThin: Style | None = None,
        GoogleGreenDotted: Style | None = None,
        GoogleGreenDottedBold: Style | None = None,
        GoogleGreenDottedThin: Style | None = None,
        GoogleOrange: Style | None = None,
        GoogleOrangeBordered: Style | None = None,
        GoogleOrangeBold: Style | None = None,
        GoogleOrangeThin: Style | None = None,
        GoogleOrangeFlat: Style | None = None,
        GoogleOrangeOutline: Style | None = None,
        GoogleOrangeSolid: Style | None = None,
        GoogleOrangeOutlineBold: Style | None = None,
        GoogleOrangeSolidBold: Style | None = None,
        GoogleOrangeOutlineThin: Style | None = None,
        GoogleOrangeSolidThin: Style | None = None,
        GoogleOrangeDashed: Style | None = None,
        GoogleOrangeDashedBold: Style | None = None,
        GoogleOrangeDashedThin: Style | None = None,
        GoogleOrangeDotted: Style | None = None,
        GoogleOrangeDottedBold: Style | None = None,
        GoogleOrangeDottedThin: Style | None = None,
        GooglePurple: Style | None = None,
        GooglePurpleBordered: Style | None = None,
        GooglePurpleBold: Style | None = None,
        GooglePurpleThin: Style | None = None,
        GooglePurpleFlat: Style | None = None,
        GooglePurpleOutline: Style | None = None,
        GooglePurpleSolid: Style | None = None,
        GooglePurpleOutlineBold: Style | None = None,
        GooglePurpleSolidBold: Style | None = None,
        GooglePurpleOutlineThin: Style | None = None,
        GooglePurpleSolidThin: Style | None = None,
        GooglePurpleDashed: Style | None = None,
        GooglePurpleDashedBold: Style | None = None,
        GooglePurpleDashedThin: Style | None = None,
        GooglePurpleDotted: Style | None = None,
        GooglePurpleDottedBold: Style | None = None,
        GooglePurpleDottedThin: Style | None = None,
        GoogleGray: Style | None = None,
        GoogleGrayBordered: Style | None = None,
        GoogleGrayBold: Style | None = None,
        GoogleGrayThin: Style | None = None,
        GoogleGrayFlat: Style | None = None,
        GoogleGrayOutline: Style | None = None,
        GoogleGraySolid: Style | None = None,
        GoogleGrayOutlineBold: Style | None = None,
        GoogleGraySolidBold: Style | None = None,
        GoogleGrayOutlineThin: Style | None = None,
        GoogleGraySolidThin: Style | None = None,
        GoogleGrayDashed: Style | None = None,
        GoogleGrayDashedBold: Style | None = None,
        GoogleGrayDashedThin: Style | None = None,
        GoogleGrayDotted: Style | None = None,
        GoogleGrayDottedBold: Style | None = None,
        GoogleGrayDottedThin: Style | None = None,
        Primary1: Style | None = None,
        Primary1Bordered: Style | None = None,
        Primary1Bold: Style | None = None,
        Primary1Thin: Style | None = None,
        Primary1Flat: Style | None = None,
        Primary1Outline: Style | None = None,
        Primary1Solid: Style | None = None,
        Primary1OutlineBold: Style | None = None,
        Primary1SolidBold: Style | None = None,
        Primary1OutlineThin: Style | None = None,
        Primary1SolidThin: Style | None = None,
        Primary1Dashed: Style | None = None,
        Primary1DashedBold: Style | None = None,
        Primary1DashedThin: Style | None = None,
        Primary1Dotted: Style | None = None,
        Primary1DottedBold: Style | None = None,
        Primary1DottedThin: Style | None = None,
        Primary2: Style | None = None,
        Primary2Bordered: Style | None = None,
        Primary2Bold: Style | None = None,
        Primary2Thin: Style | None = None,
        Primary2Flat: Style | None = None,
        Primary2Outline: Style | None = None,
        Primary2Solid: Style | None = None,
        Primary2OutlineBold: Style | None = None,
        Primary2SolidBold: Style | None = None,
        Primary2OutlineThin: Style | None = None,
        Primary2SolidThin: Style | None = None,
        Primary2Dashed: Style | None = None,
        Primary2DashedBold: Style | None = None,
        Primary2DashedThin: Style | None = None,
        Primary2Dotted: Style | None = None,
        Primary2DottedBold: Style | None = None,
        Primary2DottedThin: Style | None = None,
        Primary3: Style | None = None,
        Primary3Bordered: Style | None = None,
        Primary3Bold: Style | None = None,
        Primary3Thin: Style | None = None,
        Primary3Flat: Style | None = None,
        Primary3Outline: Style | None = None,
        Primary3Solid: Style | None = None,
        Primary3OutlineBold: Style | None = None,
        Primary3SolidBold: Style | None = None,
        Primary3OutlineThin: Style | None = None,
        Primary3SolidThin: Style | None = None,
        Primary3Dashed: Style | None = None,
        Primary3DashedBold: Style | None = None,
        Primary3DashedThin: Style | None = None,
        Primary3Dotted: Style | None = None,
        Primary3DottedBold: Style | None = None,
        Primary3DottedThin: Style | None = None,
        Primary4: Style | None = None,
        Primary4Bordered: Style | None = None,
        Primary4Bold: Style | None = None,
        Primary4Thin: Style | None = None,
        Primary4Flat: Style | None = None,
        Primary4Outline: Style | None = None,
        Primary4Solid: Style | None = None,
        Primary4OutlineBold: Style | None = None,
        Primary4SolidBold: Style | None = None,
        Primary4OutlineThin: Style | None = None,
        Primary4SolidThin: Style | None = None,
        Primary4Dashed: Style | None = None,
        Primary4DashedBold: Style | None = None,
        Primary4DashedThin: Style | None = None,
        Primary4Dotted: Style | None = None,
        Primary4DottedBold: Style | None = None,
        Primary4DottedThin: Style | None = None,
        Primary5: Style | None = None,
        Primary5Bordered: Style | None = None,
        Primary5Bold: Style | None = None,
        Primary5Thin: Style | None = None,
        Primary5Flat: Style | None = None,
        Primary5Outline: Style | None = None,
        Primary5Solid: Style | None = None,
        Primary5OutlineBold: Style | None = None,
        Primary5SolidBold: Style | None = None,
        Primary5OutlineThin: Style | None = None,
        Primary5SolidThin: Style | None = None,
        Primary5Dashed: Style | None = None,
        Primary5DashedBold: Style | None = None,
        Primary5DashedThin: Style | None = None,
        Primary5Dotted: Style | None = None,
        Primary5DottedBold: Style | None = None,
        Primary5DottedThin: Style | None = None,
        Primary6: Style | None = None,
        Primary6Bordered: Style | None = None,
        Primary6Bold: Style | None = None,
        Primary6Thin: Style | None = None,
        Primary6Flat: Style | None = None,
        Primary6Outline: Style | None = None,
        Primary6Solid: Style | None = None,
        Primary6OutlineBold: Style | None = None,
        Primary6SolidBold: Style | None = None,
        Primary6OutlineThin: Style | None = None,
        Primary6SolidThin: Style | None = None,
        Primary6Dashed: Style | None = None,
        Primary6DashedBold: Style | None = None,
        Primary6DashedThin: Style | None = None,
        Primary6Dotted: Style | None = None,
        Primary6DottedBold: Style | None = None,
        Primary6DottedThin: Style | None = None,
        Secondary1: Style | None = None,
        Secondary1Bordered: Style | None = None,
        Secondary1Bold: Style | None = None,
        Secondary1Thin: Style | None = None,
        Secondary1Flat: Style | None = None,
        Secondary1Outline: Style | None = None,
        Secondary1Solid: Style | None = None,
        Secondary1OutlineBold: Style | None = None,
        Secondary1SolidBold: Style | None = None,
        Secondary1OutlineThin: Style | None = None,
        Secondary1SolidThin: Style | None = None,
        Secondary1Dashed: Style | None = None,
        Secondary1DashedBold: Style | None = None,
        Secondary1DashedThin: Style | None = None,
        Secondary1Dotted: Style | None = None,
        Secondary1DottedBold: Style | None = None,
        Secondary1DottedThin: Style | None = None,
        Secondary2: Style | None = None,
        Secondary2Bordered: Style | None = None,
        Secondary2Bold: Style | None = None,
        Secondary2Thin: Style | None = None,
        Secondary2Flat: Style | None = None,
        Secondary2Outline: Style | None = None,
        Secondary2Solid: Style | None = None,
        Secondary2OutlineBold: Style | None = None,
        Secondary2SolidBold: Style | None = None,
        Secondary2OutlineThin: Style | None = None,
        Secondary2SolidThin: Style | None = None,
        Secondary2Dashed: Style | None = None,
        Secondary2DashedBold: Style | None = None,
        Secondary2DashedThin: Style | None = None,
        Secondary2Dotted: Style | None = None,
        Secondary2DottedBold: Style | None = None,
        Secondary2DottedThin: Style | None = None,
        Secondary3: Style | None = None,
        Secondary3Bordered: Style | None = None,
        Secondary3Bold: Style | None = None,
        Secondary3Thin: Style | None = None,
        Secondary3Flat: Style | None = None,
        Secondary3Outline: Style | None = None,
        Secondary3Solid: Style | None = None,
        Secondary3OutlineBold: Style | None = None,
        Secondary3SolidBold: Style | None = None,
        Secondary3OutlineThin: Style | None = None,
        Secondary3SolidThin: Style | None = None,
        Secondary3Dashed: Style | None = None,
        Secondary3DashedBold: Style | None = None,
        Secondary3DashedThin: Style | None = None,
        Secondary3Dotted: Style | None = None,
        Secondary3DottedBold: Style | None = None,
        Secondary3DottedThin: Style | None = None,
        Secondary4: Style | None = None,
        Secondary4Bordered: Style | None = None,
        Secondary4Bold: Style | None = None,
        Secondary4Thin: Style | None = None,
        Secondary4Flat: Style | None = None,
        Secondary4Outline: Style | None = None,
        Secondary4Solid: Style | None = None,
        Secondary4OutlineBold: Style | None = None,
        Secondary4SolidBold: Style | None = None,
        Secondary4OutlineThin: Style | None = None,
        Secondary4SolidThin: Style | None = None,
        Secondary4Dashed: Style | None = None,
        Secondary4DashedBold: Style | None = None,
        Secondary4DashedThin: Style | None = None,
        Secondary4Dotted: Style | None = None,
        Secondary4DottedBold: Style | None = None,
        Secondary4DottedThin: Style | None = None,
        Secondary5: Style | None = None,
        Secondary5Bordered: Style | None = None,
        Secondary5Bold: Style | None = None,
        Secondary5Thin: Style | None = None,
        Secondary5Flat: Style | None = None,
        Secondary5Outline: Style | None = None,
        Secondary5Solid: Style | None = None,
        Secondary5OutlineBold: Style | None = None,
        Secondary5SolidBold: Style | None = None,
        Secondary5OutlineThin: Style | None = None,
        Secondary5SolidThin: Style | None = None,
        Secondary5Dashed: Style | None = None,
        Secondary5DashedBold: Style | None = None,
        Secondary5DashedThin: Style | None = None,
        Secondary5Dotted: Style | None = None,
        Secondary5DottedBold: Style | None = None,
        Secondary5DottedThin: Style | None = None,
        Secondary6: Style | None = None,
        Secondary6Bordered: Style | None = None,
        Secondary6Bold: Style | None = None,
        Secondary6Thin: Style | None = None,
        Secondary6Flat: Style | None = None,
        Secondary6Outline: Style | None = None,
        Secondary6Solid: Style | None = None,
        Secondary6OutlineBold: Style | None = None,
        Secondary6SolidBold: Style | None = None,
        Secondary6OutlineThin: Style | None = None,
        Secondary6SolidThin: Style | None = None,
        Secondary6Dashed: Style | None = None,
        Secondary6DashedBold: Style | None = None,
        Secondary6DashedThin: Style | None = None,
        Secondary6Dotted: Style | None = None,
        Secondary6DottedBold: Style | None = None,
        Secondary6DottedThin: Style | None = None,
        Accent1: Style | None = None,
        Accent1Bordered: Style | None = None,
        Accent1Bold: Style | None = None,
        Accent1Thin: Style | None = None,
        Accent1Flat: Style | None = None,
        Accent1Outline: Style | None = None,
        Accent1Solid: Style | None = None,
        Accent1OutlineBold: Style | None = None,
        Accent1SolidBold: Style | None = None,
        Accent1OutlineThin: Style | None = None,
        Accent1SolidThin: Style | None = None,
        Accent1Dashed: Style | None = None,
        Accent1DashedBold: Style | None = None,
        Accent1DashedThin: Style | None = None,
        Accent1Dotted: Style | None = None,
        Accent1DottedBold: Style | None = None,
        Accent1DottedThin: Style | None = None,
        Accent2: Style | None = None,
        Accent2Bordered: Style | None = None,
        Accent2Bold: Style | None = None,
        Accent2Thin: Style | None = None,
        Accent2Flat: Style | None = None,
        Accent2Outline: Style | None = None,
        Accent2Solid: Style | None = None,
        Accent2OutlineBold: Style | None = None,
        Accent2SolidBold: Style | None = None,
        Accent2OutlineThin: Style | None = None,
        Accent2SolidThin: Style | None = None,
        Accent2Dashed: Style | None = None,
        Accent2DashedBold: Style | None = None,
        Accent2DashedThin: Style | None = None,
        Accent2Dotted: Style | None = None,
        Accent2DottedBold: Style | None = None,
        Accent2DottedThin: Style | None = None,
        Accent3: Style | None = None,
        Accent3Bordered: Style | None = None,
        Accent3Bold: Style | None = None,
        Accent3Thin: Style | None = None,
        Accent3Flat: Style | None = None,
        Accent3Outline: Style | None = None,
        Accent3Solid: Style | None = None,
        Accent3OutlineBold: Style | None = None,
        Accent3SolidBold: Style | None = None,
        Accent3OutlineThin: Style | None = None,
        Accent3SolidThin: Style | None = None,
        Accent3Dashed: Style | None = None,
        Accent3DashedBold: Style | None = None,
        Accent3DashedThin: Style | None = None,
        Accent3Dotted: Style | None = None,
        Accent3DottedBold: Style | None = None,
        Accent3DottedThin: Style | None = None,
        Accent4: Style | None = None,
        Accent4Bordered: Style | None = None,
        Accent4Bold: Style | None = None,
        Accent4Thin: Style | None = None,
        Accent4Flat: Style | None = None,
        Accent4Outline: Style | None = None,
        Accent4Solid: Style | None = None,
        Accent4OutlineBold: Style | None = None,
        Accent4SolidBold: Style | None = None,
        Accent4OutlineThin: Style | None = None,
        Accent4SolidThin: Style | None = None,
        Accent4Dashed: Style | None = None,
        Accent4DashedBold: Style | None = None,
        Accent4DashedThin: Style | None = None,
        Accent4Dotted: Style | None = None,
        Accent4DottedBold: Style | None = None,
        Accent4DottedThin: Style | None = None,
        Accent5: Style | None = None,
        Accent5Bordered: Style | None = None,
        Accent5Bold: Style | None = None,
        Accent5Thin: Style | None = None,
        Accent5Flat: Style | None = None,
        Accent5Outline: Style | None = None,
        Accent5Solid: Style | None = None,
        Accent5OutlineBold: Style | None = None,
        Accent5SolidBold: Style | None = None,
        Accent5OutlineThin: Style | None = None,
        Accent5SolidThin: Style | None = None,
        Accent5Dashed: Style | None = None,
        Accent5DashedBold: Style | None = None,
        Accent5DashedThin: Style | None = None,
        Accent5Dotted: Style | None = None,
        Accent5DottedBold: Style | None = None,
        Accent5DottedThin: Style | None = None,
        Accent6: Style | None = None,
        Accent6Bordered: Style | None = None,
        Accent6Bold: Style | None = None,
        Accent6Thin: Style | None = None,
        Accent6Flat: Style | None = None,
        Accent6Outline: Style | None = None,
        Accent6Solid: Style | None = None,
        Accent6OutlineBold: Style | None = None,
        Accent6SolidBold: Style | None = None,
        Accent6OutlineThin: Style | None = None,
        Accent6SolidThin: Style | None = None,
        Accent6Dashed: Style | None = None,
        Accent6DashedBold: Style | None = None,
        Accent6DashedThin: Style | None = None,
        Accent6Dotted: Style | None = None,
        Accent6DottedBold: Style | None = None,
        Accent6DottedThin: Style | None = None,
        Muted1: Style | None = None,
        Muted1Bordered: Style | None = None,
        Muted1Bold: Style | None = None,
        Muted1Thin: Style | None = None,
        Muted1Flat: Style | None = None,
        Muted1Outline: Style | None = None,
        Muted1Solid: Style | None = None,
        Muted1OutlineBold: Style | None = None,
        Muted1SolidBold: Style | None = None,
        Muted1OutlineThin: Style | None = None,
        Muted1SolidThin: Style | None = None,
        Muted1Dashed: Style | None = None,
        Muted1DashedBold: Style | None = None,
        Muted1DashedThin: Style | None = None,
        Muted1Dotted: Style | None = None,
        Muted1DottedBold: Style | None = None,
        Muted1DottedThin: Style | None = None,
        Muted2: Style | None = None,
        Muted2Bordered: Style | None = None,
        Muted2Bold: Style | None = None,
        Muted2Thin: Style | None = None,
        Muted2Flat: Style | None = None,
        Muted2Outline: Style | None = None,
        Muted2Solid: Style | None = None,
        Muted2OutlineBold: Style | None = None,
        Muted2SolidBold: Style | None = None,
        Muted2OutlineThin: Style | None = None,
        Muted2SolidThin: Style | None = None,
        Muted2Dashed: Style | None = None,
        Muted2DashedBold: Style | None = None,
        Muted2DashedThin: Style | None = None,
        Muted2Dotted: Style | None = None,
        Muted2DottedBold: Style | None = None,
        Muted2DottedThin: Style | None = None,
        Muted3: Style | None = None,
        Muted3Bordered: Style | None = None,
        Muted3Bold: Style | None = None,
        Muted3Thin: Style | None = None,
        Muted3Flat: Style | None = None,
        Muted3Outline: Style | None = None,
        Muted3Solid: Style | None = None,
        Muted3OutlineBold: Style | None = None,
        Muted3SolidBold: Style | None = None,
        Muted3OutlineThin: Style | None = None,
        Muted3SolidThin: Style | None = None,
        Muted3Dashed: Style | None = None,
        Muted3DashedBold: Style | None = None,
        Muted3DashedThin: Style | None = None,
        Muted3Dotted: Style | None = None,
        Muted3DottedBold: Style | None = None,
        Muted3DottedThin: Style | None = None,
        Muted4: Style | None = None,
        Muted4Bordered: Style | None = None,
        Muted4Bold: Style | None = None,
        Muted4Thin: Style | None = None,
        Muted4Flat: Style | None = None,
        Muted4Outline: Style | None = None,
        Muted4Solid: Style | None = None,
        Muted4OutlineBold: Style | None = None,
        Muted4SolidBold: Style | None = None,
        Muted4OutlineThin: Style | None = None,
        Muted4SolidThin: Style | None = None,
        Muted4Dashed: Style | None = None,
        Muted4DashedBold: Style | None = None,
        Muted4DashedThin: Style | None = None,
        Muted4Dotted: Style | None = None,
        Muted4DottedBold: Style | None = None,
        Muted4DottedThin: Style | None = None,
        Muted5: Style | None = None,
        Muted5Bordered: Style | None = None,
        Muted5Bold: Style | None = None,
        Muted5Thin: Style | None = None,
        Muted5Flat: Style | None = None,
        Muted5Outline: Style | None = None,
        Muted5Solid: Style | None = None,
        Muted5OutlineBold: Style | None = None,
        Muted5SolidBold: Style | None = None,
        Muted5OutlineThin: Style | None = None,
        Muted5SolidThin: Style | None = None,
        Muted5Dashed: Style | None = None,
        Muted5DashedBold: Style | None = None,
        Muted5DashedThin: Style | None = None,
        Muted5Dotted: Style | None = None,
        Muted5DottedBold: Style | None = None,
        Muted5DottedThin: Style | None = None,
        Muted6: Style | None = None,
        Muted6Bordered: Style | None = None,
        Muted6Bold: Style | None = None,
        Muted6Thin: Style | None = None,
        Muted6Flat: Style | None = None,
        Muted6Outline: Style | None = None,
        Muted6Solid: Style | None = None,
        Muted6OutlineBold: Style | None = None,
        Muted6SolidBold: Style | None = None,
        Muted6OutlineThin: Style | None = None,
        Muted6SolidThin: Style | None = None,
        Muted6Dashed: Style | None = None,
        Muted6DashedBold: Style | None = None,
        Muted6DashedThin: Style | None = None,
        Muted6Dotted: Style | None = None,
        Muted6DottedBold: Style | None = None,
        Muted6DottedThin: Style | None = None,
        Warning1: Style | None = None,
        Warning1Bordered: Style | None = None,
        Warning1Bold: Style | None = None,
        Warning1Thin: Style | None = None,
        Warning1Flat: Style | None = None,
        Warning1Outline: Style | None = None,
        Warning1Solid: Style | None = None,
        Warning1OutlineBold: Style | None = None,
        Warning1SolidBold: Style | None = None,
        Warning1OutlineThin: Style | None = None,
        Warning1SolidThin: Style | None = None,
        Warning1Dashed: Style | None = None,
        Warning1DashedBold: Style | None = None,
        Warning1DashedThin: Style | None = None,
        Warning1Dotted: Style | None = None,
        Warning1DottedBold: Style | None = None,
        Warning1DottedThin: Style | None = None,
        Warning2: Style | None = None,
        Warning2Bordered: Style | None = None,
        Warning2Bold: Style | None = None,
        Warning2Thin: Style | None = None,
        Warning2Flat: Style | None = None,
        Warning2Outline: Style | None = None,
        Warning2Solid: Style | None = None,
        Warning2OutlineBold: Style | None = None,
        Warning2SolidBold: Style | None = None,
        Warning2OutlineThin: Style | None = None,
        Warning2SolidThin: Style | None = None,
        Warning2Dashed: Style | None = None,
        Warning2DashedBold: Style | None = None,
        Warning2DashedThin: Style | None = None,
        Warning2Dotted: Style | None = None,
        Warning2DottedBold: Style | None = None,
        Warning2DottedThin: Style | None = None,
        Warning3: Style | None = None,
        Warning3Bordered: Style | None = None,
        Warning3Bold: Style | None = None,
        Warning3Thin: Style | None = None,
        Warning3Flat: Style | None = None,
        Warning3Outline: Style | None = None,
        Warning3Solid: Style | None = None,
        Warning3OutlineBold: Style | None = None,
        Warning3SolidBold: Style | None = None,
        Warning3OutlineThin: Style | None = None,
        Warning3SolidThin: Style | None = None,
        Warning3Dashed: Style | None = None,
        Warning3DashedBold: Style | None = None,
        Warning3DashedThin: Style | None = None,
        Warning3Dotted: Style | None = None,
        Warning3DottedBold: Style | None = None,
        Warning3DottedThin: Style | None = None,
        Warning4: Style | None = None,
        Warning4Bordered: Style | None = None,
        Warning4Bold: Style | None = None,
        Warning4Thin: Style | None = None,
        Warning4Flat: Style | None = None,
        Warning4Outline: Style | None = None,
        Warning4Solid: Style | None = None,
        Warning4OutlineBold: Style | None = None,
        Warning4SolidBold: Style | None = None,
        Warning4OutlineThin: Style | None = None,
        Warning4SolidThin: Style | None = None,
        Warning4Dashed: Style | None = None,
        Warning4DashedBold: Style | None = None,
        Warning4DashedThin: Style | None = None,
        Warning4Dotted: Style | None = None,
        Warning4DottedBold: Style | None = None,
        Warning4DottedThin: Style | None = None,
        Warning5: Style | None = None,
        Warning5Bordered: Style | None = None,
        Warning5Bold: Style | None = None,
        Warning5Thin: Style | None = None,
        Warning5Flat: Style | None = None,
        Warning5Outline: Style | None = None,
        Warning5Solid: Style | None = None,
        Warning5OutlineBold: Style | None = None,
        Warning5SolidBold: Style | None = None,
        Warning5OutlineThin: Style | None = None,
        Warning5SolidThin: Style | None = None,
        Warning5Dashed: Style | None = None,
        Warning5DashedBold: Style | None = None,
        Warning5DashedThin: Style | None = None,
        Warning5Dotted: Style | None = None,
        Warning5DottedBold: Style | None = None,
        Warning5DottedThin: Style | None = None,
        Warning6: Style | None = None,
        Warning6Bordered: Style | None = None,
        Warning6Bold: Style | None = None,
        Warning6Thin: Style | None = None,
        Warning6Flat: Style | None = None,
        Warning6Outline: Style | None = None,
        Warning6Solid: Style | None = None,
        Warning6OutlineBold: Style | None = None,
        Warning6SolidBold: Style | None = None,
        Warning6OutlineThin: Style | None = None,
        Warning6SolidThin: Style | None = None,
        Warning6Dashed: Style | None = None,
        Warning6DashedBold: Style | None = None,
        Warning6DashedThin: Style | None = None,
        Warning6Dotted: Style | None = None,
        Warning6DottedBold: Style | None = None,
        Warning6DottedThin: Style | None = None,
        Danger1: Style | None = None,
        Danger1Bordered: Style | None = None,
        Danger1Bold: Style | None = None,
        Danger1Thin: Style | None = None,
        Danger1Flat: Style | None = None,
        Danger1Outline: Style | None = None,
        Danger1Solid: Style | None = None,
        Danger1OutlineBold: Style | None = None,
        Danger1SolidBold: Style | None = None,
        Danger1OutlineThin: Style | None = None,
        Danger1SolidThin: Style | None = None,
        Danger1Dashed: Style | None = None,
        Danger1DashedBold: Style | None = None,
        Danger1DashedThin: Style | None = None,
        Danger1Dotted: Style | None = None,
        Danger1DottedBold: Style | None = None,
        Danger1DottedThin: Style | None = None,
        Danger2: Style | None = None,
        Danger2Bordered: Style | None = None,
        Danger2Bold: Style | None = None,
        Danger2Thin: Style | None = None,
        Danger2Flat: Style | None = None,
        Danger2Outline: Style | None = None,
        Danger2Solid: Style | None = None,
        Danger2OutlineBold: Style | None = None,
        Danger2SolidBold: Style | None = None,
        Danger2OutlineThin: Style | None = None,
        Danger2SolidThin: Style | None = None,
        Danger2Dashed: Style | None = None,
        Danger2DashedBold: Style | None = None,
        Danger2DashedThin: Style | None = None,
        Danger2Dotted: Style | None = None,
        Danger2DottedBold: Style | None = None,
        Danger2DottedThin: Style | None = None,
        Danger3: Style | None = None,
        Danger3Bordered: Style | None = None,
        Danger3Bold: Style | None = None,
        Danger3Thin: Style | None = None,
        Danger3Flat: Style | None = None,
        Danger3Outline: Style | None = None,
        Danger3Solid: Style | None = None,
        Danger3OutlineBold: Style | None = None,
        Danger3SolidBold: Style | None = None,
        Danger3OutlineThin: Style | None = None,
        Danger3SolidThin: Style | None = None,
        Danger3Dashed: Style | None = None,
        Danger3DashedBold: Style | None = None,
        Danger3DashedThin: Style | None = None,
        Danger3Dotted: Style | None = None,
        Danger3DottedBold: Style | None = None,
        Danger3DottedThin: Style | None = None,
        Danger4: Style | None = None,
        Danger4Bordered: Style | None = None,
        Danger4Bold: Style | None = None,
        Danger4Thin: Style | None = None,
        Danger4Flat: Style | None = None,
        Danger4Outline: Style | None = None,
        Danger4Solid: Style | None = None,
        Danger4OutlineBold: Style | None = None,
        Danger4SolidBold: Style | None = None,
        Danger4OutlineThin: Style | None = None,
        Danger4SolidThin: Style | None = None,
        Danger4Dashed: Style | None = None,
        Danger4DashedBold: Style | None = None,
        Danger4DashedThin: Style | None = None,
        Danger4Dotted: Style | None = None,
        Danger4DottedBold: Style | None = None,
        Danger4DottedThin: Style | None = None,
        Danger5: Style | None = None,
        Danger5Bordered: Style | None = None,
        Danger5Bold: Style | None = None,
        Danger5Thin: Style | None = None,
        Danger5Flat: Style | None = None,
        Danger5Outline: Style | None = None,
        Danger5Solid: Style | None = None,
        Danger5OutlineBold: Style | None = None,
        Danger5SolidBold: Style | None = None,
        Danger5OutlineThin: Style | None = None,
        Danger5SolidThin: Style | None = None,
        Danger5Dashed: Style | None = None,
        Danger5DashedBold: Style | None = None,
        Danger5DashedThin: Style | None = None,
        Danger5Dotted: Style | None = None,
        Danger5DottedBold: Style | None = None,
        Danger5DottedThin: Style | None = None,
        Danger6: Style | None = None,
        Danger6Bordered: Style | None = None,
        Danger6Bold: Style | None = None,
        Danger6Thin: Style | None = None,
        Danger6Flat: Style | None = None,
        Danger6Outline: Style | None = None,
        Danger6Solid: Style | None = None,
        Danger6OutlineBold: Style | None = None,
        Danger6SolidBold: Style | None = None,
        Danger6OutlineThin: Style | None = None,
        Danger6SolidThin: Style | None = None,
        Danger6Dashed: Style | None = None,
        Danger6DashedBold: Style | None = None,
        Danger6DashedThin: Style | None = None,
        Danger6Dotted: Style | None = None,
        Danger6DottedBold: Style | None = None,
        Danger6DottedThin: Style | None = None,
        Success1: Style | None = None,
        Success1Bordered: Style | None = None,
        Success1Bold: Style | None = None,
        Success1Thin: Style | None = None,
        Success1Flat: Style | None = None,
        Success1Outline: Style | None = None,
        Success1Solid: Style | None = None,
        Success1OutlineBold: Style | None = None,
        Success1SolidBold: Style | None = None,
        Success1OutlineThin: Style | None = None,
        Success1SolidThin: Style | None = None,
        Success1Dashed: Style | None = None,
        Success1DashedBold: Style | None = None,
        Success1DashedThin: Style | None = None,
        Success1Dotted: Style | None = None,
        Success1DottedBold: Style | None = None,
        Success1DottedThin: Style | None = None,
        Success2: Style | None = None,
        Success2Bordered: Style | None = None,
        Success2Bold: Style | None = None,
        Success2Thin: Style | None = None,
        Success2Flat: Style | None = None,
        Success2Outline: Style | None = None,
        Success2Solid: Style | None = None,
        Success2OutlineBold: Style | None = None,
        Success2SolidBold: Style | None = None,
        Success2OutlineThin: Style | None = None,
        Success2SolidThin: Style | None = None,
        Success2Dashed: Style | None = None,
        Success2DashedBold: Style | None = None,
        Success2DashedThin: Style | None = None,
        Success2Dotted: Style | None = None,
        Success2DottedBold: Style | None = None,
        Success2DottedThin: Style | None = None,
        Success3: Style | None = None,
        Success3Bordered: Style | None = None,
        Success3Bold: Style | None = None,
        Success3Thin: Style | None = None,
        Success3Flat: Style | None = None,
        Success3Outline: Style | None = None,
        Success3Solid: Style | None = None,
        Success3OutlineBold: Style | None = None,
        Success3SolidBold: Style | None = None,
        Success3OutlineThin: Style | None = None,
        Success3SolidThin: Style | None = None,
        Success3Dashed: Style | None = None,
        Success3DashedBold: Style | None = None,
        Success3DashedThin: Style | None = None,
        Success3Dotted: Style | None = None,
        Success3DottedBold: Style | None = None,
        Success3DottedThin: Style | None = None,
        Success4: Style | None = None,
        Success4Bordered: Style | None = None,
        Success4Bold: Style | None = None,
        Success4Thin: Style | None = None,
        Success4Flat: Style | None = None,
        Success4Outline: Style | None = None,
        Success4Solid: Style | None = None,
        Success4OutlineBold: Style | None = None,
        Success4SolidBold: Style | None = None,
        Success4OutlineThin: Style | None = None,
        Success4SolidThin: Style | None = None,
        Success4Dashed: Style | None = None,
        Success4DashedBold: Style | None = None,
        Success4DashedThin: Style | None = None,
        Success4Dotted: Style | None = None,
        Success4DottedBold: Style | None = None,
        Success4DottedThin: Style | None = None,
        Success5: Style | None = None,
        Success5Bordered: Style | None = None,
        Success5Bold: Style | None = None,
        Success5Thin: Style | None = None,
        Success5Flat: Style | None = None,
        Success5Outline: Style | None = None,
        Success5Solid: Style | None = None,
        Success5OutlineBold: Style | None = None,
        Success5SolidBold: Style | None = None,
        Success5OutlineThin: Style | None = None,
        Success5SolidThin: Style | None = None,
        Success5Dashed: Style | None = None,
        Success5DashedBold: Style | None = None,
        Success5DashedThin: Style | None = None,
        Success5Dotted: Style | None = None,
        Success5DottedBold: Style | None = None,
        Success5DottedThin: Style | None = None,
        Success6: Style | None = None,
        Success6Bordered: Style | None = None,
        Success6Bold: Style | None = None,
        Success6Thin: Style | None = None,
        Success6Flat: Style | None = None,
        Success6Outline: Style | None = None,
        Success6Solid: Style | None = None,
        Success6OutlineBold: Style | None = None,
        Success6SolidBold: Style | None = None,
        Success6OutlineThin: Style | None = None,
        Success6SolidThin: Style | None = None,
        Success6Dashed: Style | None = None,
        Success6DashedBold: Style | None = None,
        Success6DashedThin: Style | None = None,
        Success6Dotted: Style | None = None,
        Success6DottedBold: Style | None = None,
        Success6DottedThin: Style | None = None,
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
        YellowNeutral: Style | None = None,
        YellowNeutralFlat: Style | None = None,
        AmberNeutral: Style | None = None,
        AmberNeutralFlat: Style | None = None,
        PurpleNeutral: Style | None = None,
        PurpleNeutralFlat: Style | None = None,
        CyanNeutral: Style | None = None,
        CyanNeutralFlat: Style | None = None,
        TealNeutral: Style | None = None,
        TealNeutralFlat: Style | None = None,
        MagentaNeutral: Style | None = None,
        MagentaNeutralFlat: Style | None = None,
        PinkNeutral: Style | None = None,
        PinkNeutralFlat: Style | None = None,
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


def _create_google_styles() -> GoogleStyles:
    col = GoogleColors
    styles_dict: dict[str, Any] = {
        "background_color": col.Canvas,
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
        "colors": col,
    }

    border_color = col.Gray8

    # 1. Semantic roles
    semantic_map = {
        "Primary": col.Primary,
        "Secondary": col.Secondary,
        "Accent": col.Accent,
        "Warning": col.Warning,
        "Muted": col.Muted,
        "Light": col.Light,
        "Neutral": col.Neutral,
        "Dark": col.Dark,
        "Danger": col.Danger,
        "Success": col.Success,
    }
    for role_name, color in semantic_map.items():
        if role_name == "Muted":
            v = _make_variants(
                color,
                border_color=col.Gray6,
                default_text_color=col.Gray6,
                line_color=col.Gray5,
            )
        elif role_name == "Light":
            v = _make_variants(
                color,
                border_color=col.Gray4,
                default_text_color=col.Gray8,
                line_color=col.Gray4,
            )
        elif role_name == "Neutral":
            v = _make_variants(
                color,
                border_color=col.Gray4,
                default_text_color=col.Gray8,
                line_color=col.Gray4,
            )
        elif role_name == "Dark":
            v = _make_variants(
                color,
                border_color=col.Gray6,
                default_text_color=col.Dark,
                line_color=col.Dark,
            )
        elif role_name == "Warning":
            v = _make_variants(
                color,
                border_color=border_color,
                default_text_color=col.Gray8,
            )
        else:
            v = _make_variants(color, border_color=border_color)
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

    # 2. Neutrals
    neutrals_map = {
        "White": col.White,
        "Gray1": col.Gray1,
        "Gray2": col.Gray2,
        "Gray3": col.Gray3,
        "Gray4": col.Gray4,
        "Gray5": col.Gray5,
        "Gray6": col.Gray6,
        "Gray7": col.Gray7,
        "Gray8": col.Gray8,
        "Black": col.Black,
    }

    # 3. Tones (10 hues x 6 tones)
    tones_map: dict[str, Color] = {}
    tones_map["CornflowerBlue1"] = getattr(col, "CornflowerBlue1")
    tones_map["CornflowerBlue2"] = getattr(col, "CornflowerBlue2")
    tones_map["CornflowerBlue3"] = getattr(col, "CornflowerBlue3")
    tones_map["CornflowerBlue4"] = getattr(col, "CornflowerBlue4")
    tones_map["CornflowerBlue5"] = getattr(col, "CornflowerBlue5")
    tones_map["CornflowerBlue6"] = getattr(col, "CornflowerBlue6")
    tones_map["Blue1"] = getattr(col, "Blue1")
    tones_map["Blue2"] = getattr(col, "Blue2")
    tones_map["Blue3"] = getattr(col, "Blue3")
    tones_map["Blue4"] = getattr(col, "Blue4")
    tones_map["Blue5"] = getattr(col, "Blue5")
    tones_map["Blue6"] = getattr(col, "Blue6")
    tones_map["Red1"] = getattr(col, "Red1")
    tones_map["Red2"] = getattr(col, "Red2")
    tones_map["Red3"] = getattr(col, "Red3")
    tones_map["Red4"] = getattr(col, "Red4")
    tones_map["Red5"] = getattr(col, "Red5")
    tones_map["Red6"] = getattr(col, "Red6")
    tones_map["RedBerry1"] = getattr(col, "RedBerry1")
    tones_map["RedBerry2"] = getattr(col, "RedBerry2")
    tones_map["RedBerry3"] = getattr(col, "RedBerry3")
    tones_map["RedBerry4"] = getattr(col, "RedBerry4")
    tones_map["RedBerry5"] = getattr(col, "RedBerry5")
    tones_map["RedBerry6"] = getattr(col, "RedBerry6")
    tones_map["Green1"] = getattr(col, "Green1")
    tones_map["Green2"] = getattr(col, "Green2")
    tones_map["Green3"] = getattr(col, "Green3")
    tones_map["Green4"] = getattr(col, "Green4")
    tones_map["Green5"] = getattr(col, "Green5")
    tones_map["Green6"] = getattr(col, "Green6")
    tones_map["Yellow1"] = getattr(col, "Yellow1")
    tones_map["Yellow2"] = getattr(col, "Yellow2")
    tones_map["Yellow3"] = getattr(col, "Yellow3")
    tones_map["Yellow4"] = getattr(col, "Yellow4")
    tones_map["Yellow5"] = getattr(col, "Yellow5")
    tones_map["Yellow6"] = getattr(col, "Yellow6")
    tones_map["Orange1"] = getattr(col, "Orange1")
    tones_map["Orange2"] = getattr(col, "Orange2")
    tones_map["Orange3"] = getattr(col, "Orange3")
    tones_map["Orange4"] = getattr(col, "Orange4")
    tones_map["Orange5"] = getattr(col, "Orange5")
    tones_map["Orange6"] = getattr(col, "Orange6")
    tones_map["Cyan1"] = getattr(col, "Cyan1")
    tones_map["Cyan2"] = getattr(col, "Cyan2")
    tones_map["Cyan3"] = getattr(col, "Cyan3")
    tones_map["Cyan4"] = getattr(col, "Cyan4")
    tones_map["Cyan5"] = getattr(col, "Cyan5")
    tones_map["Cyan6"] = getattr(col, "Cyan6")
    tones_map["Purple1"] = getattr(col, "Purple1")
    tones_map["Purple2"] = getattr(col, "Purple2")
    tones_map["Purple3"] = getattr(col, "Purple3")
    tones_map["Purple4"] = getattr(col, "Purple4")
    tones_map["Purple5"] = getattr(col, "Purple5")
    tones_map["Purple6"] = getattr(col, "Purple6")
    tones_map["Magenta1"] = getattr(col, "Magenta1")
    tones_map["Magenta2"] = getattr(col, "Magenta2")
    tones_map["Magenta3"] = getattr(col, "Magenta3")
    tones_map["Magenta4"] = getattr(col, "Magenta4")
    tones_map["Magenta5"] = getattr(col, "Magenta5")
    tones_map["Magenta6"] = getattr(col, "Magenta6")

    # 4. Primaries
    primaries_map: dict[str, Color] = {}
    primaries_map["CornflowerBlue"] = getattr(col, "CornflowerBlue")
    primaries_map["Blue"] = getattr(col, "Blue")
    primaries_map["Red"] = getattr(col, "Red")
    primaries_map["RedBerry"] = getattr(col, "RedBerry")
    primaries_map["Green"] = getattr(col, "Green")
    primaries_map["Yellow"] = getattr(col, "Yellow")
    primaries_map["Orange"] = getattr(col, "Orange")
    primaries_map["Cyan"] = getattr(col, "Cyan")
    primaries_map["Purple"] = getattr(col, "Purple")
    primaries_map["Magenta"] = getattr(col, "Magenta")
    primaries_map["Pink"] = getattr(col, "Pink")
    primaries_map["Lime"] = getattr(col, "Lime")
    primaries_map["Teal"] = getattr(col, "Teal")
    primaries_map["Navy"] = getattr(col, "Navy")
    primaries_map["Olive"] = getattr(col, "Olive")
    primaries_map["Brown"] = getattr(col, "Brown")
    primaries_map["Gold"] = getattr(col, "Gold")
    primaries_map["Aqua"] = getattr(col, "Aqua")
    primaries_map["GreenYellow"] = getattr(col, "GreenYellow")
    primaries_map["Ivory"] = getattr(col, "Ivory")
    primaries_map["Steel"] = getattr(col, "Steel")

    # 5. Brand
    brand_map: dict[str, Color] = {}
    brand_map["GoogleBlue"] = getattr(col, "GoogleBlue")
    brand_map["GoogleRed"] = getattr(col, "GoogleRed")
    brand_map["GoogleYellow"] = getattr(col, "GoogleYellow")
    brand_map["GoogleGreen"] = getattr(col, "GoogleGreen")
    brand_map["GoogleOrange"] = getattr(col, "GoogleOrange")
    brand_map["GooglePurple"] = getattr(col, "GooglePurple")
    brand_map["GoogleGray"] = getattr(col, "GoogleGray")

    # 6. Semantic Tones (7 roles x 6 tones)
    semantic_tones_map: dict[str, Color] = {}
    for r in ["primary", "secondary", "accent", "muted", "warning", "danger", "success"]:
        for i in range(1, 7):
            semantic_tones_map[f"{r.capitalize()}{i}"] = getattr(col, f"{r.capitalize()}{i}")

    all_colors: dict[str, Color] = {**neutrals_map, **tones_map, **primaries_map, **brand_map, **semantic_tones_map}
    for cname, color in all_colors.items():
        v = _make_variants(color, border_color=border_color)
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

    # Canvas shape style
    canvas_col = col.Canvas
    styles_dict["Canvas"] = Style(
        supports={"shape"},
        shape_fill_color=canvas_col,
        shape_line_color=canvas_col,
        shape_line_width=0.0,
    )
    styles_dict["CanvasFlat"] = Style(
        supports={"shape"},
        shape_fill_color=canvas_col,
        shape_line_color=canvas_col,
        shape_line_width=0.0,
    )

    # Neutral Card Styles (Bordered & Flat)
    # Base / Gray Neutral
    styles_dict["GrayNeutral"], styles_dict["GrayNeutralFlat"] = _make_neutral_card(
        col.Gray2, border_color=col.Gray4, text_color=col.Gray8
    )
    styles_dict["Neutral"] = styles_dict["GrayNeutral"]
    styles_dict["NeutralBordered"] = styles_dict["GrayNeutral"]
    styles_dict["NeutralFlat"] = styles_dict["GrayNeutralFlat"]

    # Semantic Neutral Cards
    styles_dict["PrimaryNeutral"], styles_dict["PrimaryNeutralFlat"] = _make_neutral_card(
        col.Primary1, border_color=col.Primary3, text_color=col.Primary6
    )
    styles_dict["SecondaryNeutral"], styles_dict["SecondaryNeutralFlat"] = _make_neutral_card(
        col.Secondary1, border_color=col.Secondary3, text_color=col.Secondary6
    )
    styles_dict["AccentNeutral"], styles_dict["AccentNeutralFlat"] = _make_neutral_card(
        col.Accent1, border_color=col.Accent3, text_color=col.Accent6
    )
    styles_dict["WarningNeutral"], styles_dict["WarningNeutralFlat"] = _make_neutral_card(
        col.Warning1, border_color=col.Warning3, text_color=col.Warning6
    )
    styles_dict["DangerNeutral"], styles_dict["DangerNeutralFlat"] = _make_neutral_card(
        col.Danger1, border_color=col.Danger3, text_color=col.Danger6
    )
    styles_dict["SuccessNeutral"], styles_dict["SuccessNeutralFlat"] = _make_neutral_card(
        col.Success1, border_color=col.Success3, text_color=col.Success6
    )
    styles_dict["MutedNeutral"], styles_dict["MutedNeutralFlat"] = _make_neutral_card(
        col.Gray2, border_color=col.Gray4, text_color=col.Gray8
    )

    # Named Color Neutral Cards
    styles_dict["BlueNeutral"], styles_dict["BlueNeutralFlat"] = _make_neutral_card(
        col.Blue1, border_color=col.Blue3, text_color=col.Blue6
    )
    styles_dict["GreenNeutral"], styles_dict["GreenNeutralFlat"] = _make_neutral_card(
        col.Green1, border_color=col.Green3, text_color=col.Green6
    )
    styles_dict["RedNeutral"], styles_dict["RedNeutralFlat"] = _make_neutral_card(
        col.Red1, border_color=col.Red3, text_color=col.Red6
    )
    styles_dict["OrangeNeutral"], styles_dict["OrangeNeutralFlat"] = _make_neutral_card(
        col.Orange1, border_color=col.Orange3, text_color=col.Orange6
    )
    styles_dict["YellowNeutral"], styles_dict["YellowNeutralFlat"] = _make_neutral_card(
        col.Yellow1, border_color=col.Yellow3, text_color=col.Yellow6
    )
    styles_dict["AmberNeutral"], styles_dict["AmberNeutralFlat"] = _make_neutral_card(
        col.Yellow1, border_color=col.Yellow3, text_color=col.Yellow6
    )
    styles_dict["PurpleNeutral"], styles_dict["PurpleNeutralFlat"] = _make_neutral_card(
        col.Purple1, border_color=col.Purple3, text_color=col.Purple6
    )
    styles_dict["CyanNeutral"], styles_dict["CyanNeutralFlat"] = _make_neutral_card(
        col.Cyan1, border_color=col.Cyan3, text_color=col.Cyan6
    )
    styles_dict["TealNeutral"], styles_dict["TealNeutralFlat"] = _make_neutral_card(
        col.Cyan1, border_color=col.Cyan3, text_color=col.Cyan6
    )
    styles_dict["MagentaNeutral"], styles_dict["MagentaNeutralFlat"] = _make_neutral_card(
        col.Magenta1, border_color=col.Magenta3, text_color=col.Magenta6
    )
    styles_dict["PinkNeutral"], styles_dict["PinkNeutralFlat"] = _make_neutral_card(
        col.Magenta1, border_color=col.Magenta3, text_color=col.Magenta6
    )

    return GoogleStyles(**styles_dict)


_google_styles: GoogleStyles = _create_google_styles()
GoogleStyles.register_default_instance(_google_styles)

__all__ = [
    "GoogleStyles",
]
