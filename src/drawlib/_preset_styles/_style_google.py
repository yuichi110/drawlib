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
from drawlib._preset_styles._utils import _make_variants

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class GoogleStyles(BaseStyles):
    """Google preset styles with complete typing for IDE autocompletion."""

    # Primary
    Primary: Style
    PrimaryBordered: Style
    PrimaryBold: Style
    PrimaryLight: Style
    PrimaryFlat: Style
    PrimaryOutline: Style
    PrimarySolid: Style
    PrimaryOutlineBold: Style
    PrimarySolidBold: Style
    PrimaryOutlineLight: Style
    PrimarySolidLight: Style
    PrimaryDashed: Style
    PrimaryDashedBold: Style
    PrimaryDashedLight: Style

    # Secondary
    Secondary: Style
    SecondaryBordered: Style
    SecondaryBold: Style
    SecondaryLight: Style
    SecondaryFlat: Style
    SecondaryOutline: Style
    SecondarySolid: Style
    SecondaryOutlineBold: Style
    SecondarySolidBold: Style
    SecondaryOutlineLight: Style
    SecondarySolidLight: Style
    SecondaryDashed: Style
    SecondaryDashedBold: Style
    SecondaryDashedLight: Style

    # Accent
    Accent: Style
    AccentBordered: Style
    AccentBold: Style
    AccentLight: Style
    AccentFlat: Style
    AccentOutline: Style
    AccentSolid: Style
    AccentOutlineBold: Style
    AccentSolidBold: Style
    AccentOutlineLight: Style
    AccentSolidLight: Style
    AccentDashed: Style
    AccentDashedBold: Style
    AccentDashedLight: Style

    # Muted
    Muted: Style
    MutedBordered: Style
    MutedBold: Style
    MutedLight: Style
    MutedFlat: Style
    MutedOutline: Style
    MutedSolid: Style
    MutedOutlineBold: Style
    MutedSolidBold: Style
    MutedOutlineLight: Style
    MutedSolidLight: Style
    MutedDashed: Style
    MutedDashedBold: Style
    MutedDashedLight: Style

    # Light
    Light: Style
    LightBordered: Style
    LightBold: Style
    LightLight: Style
    LightFlat: Style
    LightOutline: Style
    LightSolid: Style
    LightOutlineBold: Style
    LightSolidBold: Style
    LightOutlineLight: Style
    LightSolidLight: Style
    LightDashed: Style
    LightDashedBold: Style
    LightDashedLight: Style

    # Dark
    Dark: Style
    DarkBordered: Style
    DarkBold: Style
    DarkLight: Style
    DarkFlat: Style
    DarkOutline: Style
    DarkSolid: Style
    DarkOutlineBold: Style
    DarkSolidBold: Style
    DarkOutlineLight: Style
    DarkSolidLight: Style
    DarkDashed: Style
    DarkDashedBold: Style
    DarkDashedLight: Style

    # Danger
    Danger: Style
    DangerBordered: Style
    DangerBold: Style
    DangerLight: Style
    DangerFlat: Style
    DangerOutline: Style
    DangerSolid: Style
    DangerOutlineBold: Style
    DangerSolidBold: Style
    DangerOutlineLight: Style
    DangerSolidLight: Style
    DangerDashed: Style
    DangerDashedBold: Style
    DangerDashedLight: Style

    # Success
    Success: Style
    SuccessBordered: Style
    SuccessBold: Style
    SuccessLight: Style
    SuccessFlat: Style
    SuccessOutline: Style
    SuccessSolid: Style
    SuccessOutlineBold: Style
    SuccessSolidBold: Style
    SuccessOutlineLight: Style
    SuccessSolidLight: Style
    SuccessDashed: Style
    SuccessDashedBold: Style
    SuccessDashedLight: Style

    # =========================================================================
    # Numbered Semantic Roles
    # =========================================================================

    # primary1
    Primary1: Style
    Primary1Bordered: Style
    Primary1Bold: Style
    Primary1Light: Style
    Primary1Flat: Style
    Primary1Outline: Style
    Primary1Solid: Style
    Primary1OutlineBold: Style
    Primary1SolidBold: Style
    Primary1OutlineLight: Style
    Primary1SolidLight: Style
    Primary1Dashed: Style
    Primary1DashedBold: Style
    Primary1DashedLight: Style

    # primary2
    Primary2: Style
    Primary2Bordered: Style
    Primary2Bold: Style
    Primary2Light: Style
    Primary2Flat: Style
    Primary2Outline: Style
    Primary2Solid: Style
    Primary2OutlineBold: Style
    Primary2SolidBold: Style
    Primary2OutlineLight: Style
    Primary2SolidLight: Style
    Primary2Dashed: Style
    Primary2DashedBold: Style
    Primary2DashedLight: Style

    # primary3
    Primary3: Style
    Primary3Bordered: Style
    Primary3Bold: Style
    Primary3Light: Style
    Primary3Flat: Style
    Primary3Outline: Style
    Primary3Solid: Style
    Primary3OutlineBold: Style
    Primary3SolidBold: Style
    Primary3OutlineLight: Style
    Primary3SolidLight: Style
    Primary3Dashed: Style
    Primary3DashedBold: Style
    Primary3DashedLight: Style

    # primary4
    Primary4: Style
    Primary4Bordered: Style
    Primary4Bold: Style
    Primary4Light: Style
    Primary4Flat: Style
    Primary4Outline: Style
    Primary4Solid: Style
    Primary4OutlineBold: Style
    Primary4SolidBold: Style
    Primary4OutlineLight: Style
    Primary4SolidLight: Style
    Primary4Dashed: Style
    Primary4DashedBold: Style
    Primary4DashedLight: Style

    # primary5
    Primary5: Style
    Primary5Bordered: Style
    Primary5Bold: Style
    Primary5Light: Style
    Primary5Flat: Style
    Primary5Outline: Style
    Primary5Solid: Style
    Primary5OutlineBold: Style
    Primary5SolidBold: Style
    Primary5OutlineLight: Style
    Primary5SolidLight: Style
    Primary5Dashed: Style
    Primary5DashedBold: Style
    Primary5DashedLight: Style

    # primary6
    Primary6: Style
    Primary6Bordered: Style
    Primary6Bold: Style
    Primary6Light: Style
    Primary6Flat: Style
    Primary6Outline: Style
    Primary6Solid: Style
    Primary6OutlineBold: Style
    Primary6SolidBold: Style
    Primary6OutlineLight: Style
    Primary6SolidLight: Style
    Primary6Dashed: Style
    Primary6DashedBold: Style
    Primary6DashedLight: Style

    # secondary1
    Secondary1: Style
    Secondary1Bordered: Style
    Secondary1Bold: Style
    Secondary1Light: Style
    Secondary1Flat: Style
    Secondary1Outline: Style
    Secondary1Solid: Style
    Secondary1OutlineBold: Style
    Secondary1SolidBold: Style
    Secondary1OutlineLight: Style
    Secondary1SolidLight: Style
    Secondary1Dashed: Style
    Secondary1DashedBold: Style
    Secondary1DashedLight: Style

    # secondary2
    Secondary2: Style
    Secondary2Bordered: Style
    Secondary2Bold: Style
    Secondary2Light: Style
    Secondary2Flat: Style
    Secondary2Outline: Style
    Secondary2Solid: Style
    Secondary2OutlineBold: Style
    Secondary2SolidBold: Style
    Secondary2OutlineLight: Style
    Secondary2SolidLight: Style
    Secondary2Dashed: Style
    Secondary2DashedBold: Style
    Secondary2DashedLight: Style

    # secondary3
    Secondary3: Style
    Secondary3Bordered: Style
    Secondary3Bold: Style
    Secondary3Light: Style
    Secondary3Flat: Style
    Secondary3Outline: Style
    Secondary3Solid: Style
    Secondary3OutlineBold: Style
    Secondary3SolidBold: Style
    Secondary3OutlineLight: Style
    Secondary3SolidLight: Style
    Secondary3Dashed: Style
    Secondary3DashedBold: Style
    Secondary3DashedLight: Style

    # secondary4
    Secondary4: Style
    Secondary4Bordered: Style
    Secondary4Bold: Style
    Secondary4Light: Style
    Secondary4Flat: Style
    Secondary4Outline: Style
    Secondary4Solid: Style
    Secondary4OutlineBold: Style
    Secondary4SolidBold: Style
    Secondary4OutlineLight: Style
    Secondary4SolidLight: Style
    Secondary4Dashed: Style
    Secondary4DashedBold: Style
    Secondary4DashedLight: Style

    # secondary5
    Secondary5: Style
    Secondary5Bordered: Style
    Secondary5Bold: Style
    Secondary5Light: Style
    Secondary5Flat: Style
    Secondary5Outline: Style
    Secondary5Solid: Style
    Secondary5OutlineBold: Style
    Secondary5SolidBold: Style
    Secondary5OutlineLight: Style
    Secondary5SolidLight: Style
    Secondary5Dashed: Style
    Secondary5DashedBold: Style
    Secondary5DashedLight: Style

    # secondary6
    Secondary6: Style
    Secondary6Bordered: Style
    Secondary6Bold: Style
    Secondary6Light: Style
    Secondary6Flat: Style
    Secondary6Outline: Style
    Secondary6Solid: Style
    Secondary6OutlineBold: Style
    Secondary6SolidBold: Style
    Secondary6OutlineLight: Style
    Secondary6SolidLight: Style
    Secondary6Dashed: Style
    Secondary6DashedBold: Style
    Secondary6DashedLight: Style

    # accent1
    Accent1: Style
    Accent1Bordered: Style
    Accent1Bold: Style
    Accent1Light: Style
    Accent1Flat: Style
    Accent1Outline: Style
    Accent1Solid: Style
    Accent1OutlineBold: Style
    Accent1SolidBold: Style
    Accent1OutlineLight: Style
    Accent1SolidLight: Style
    Accent1Dashed: Style
    Accent1DashedBold: Style
    Accent1DashedLight: Style

    # accent2
    Accent2: Style
    Accent2Bordered: Style
    Accent2Bold: Style
    Accent2Light: Style
    Accent2Flat: Style
    Accent2Outline: Style
    Accent2Solid: Style
    Accent2OutlineBold: Style
    Accent2SolidBold: Style
    Accent2OutlineLight: Style
    Accent2SolidLight: Style
    Accent2Dashed: Style
    Accent2DashedBold: Style
    Accent2DashedLight: Style

    # accent3
    Accent3: Style
    Accent3Bordered: Style
    Accent3Bold: Style
    Accent3Light: Style
    Accent3Flat: Style
    Accent3Outline: Style
    Accent3Solid: Style
    Accent3OutlineBold: Style
    Accent3SolidBold: Style
    Accent3OutlineLight: Style
    Accent3SolidLight: Style
    Accent3Dashed: Style
    Accent3DashedBold: Style
    Accent3DashedLight: Style

    # accent4
    Accent4: Style
    Accent4Bordered: Style
    Accent4Bold: Style
    Accent4Light: Style
    Accent4Flat: Style
    Accent4Outline: Style
    Accent4Solid: Style
    Accent4OutlineBold: Style
    Accent4SolidBold: Style
    Accent4OutlineLight: Style
    Accent4SolidLight: Style
    Accent4Dashed: Style
    Accent4DashedBold: Style
    Accent4DashedLight: Style

    # accent5
    Accent5: Style
    Accent5Bordered: Style
    Accent5Bold: Style
    Accent5Light: Style
    Accent5Flat: Style
    Accent5Outline: Style
    Accent5Solid: Style
    Accent5OutlineBold: Style
    Accent5SolidBold: Style
    Accent5OutlineLight: Style
    Accent5SolidLight: Style
    Accent5Dashed: Style
    Accent5DashedBold: Style
    Accent5DashedLight: Style

    # accent6
    Accent6: Style
    Accent6Bordered: Style
    Accent6Bold: Style
    Accent6Light: Style
    Accent6Flat: Style
    Accent6Outline: Style
    Accent6Solid: Style
    Accent6OutlineBold: Style
    Accent6SolidBold: Style
    Accent6OutlineLight: Style
    Accent6SolidLight: Style
    Accent6Dashed: Style
    Accent6DashedBold: Style
    Accent6DashedLight: Style

    # muted1
    Muted1: Style
    Muted1Bordered: Style
    Muted1Bold: Style
    Muted1Light: Style
    Muted1Flat: Style
    Muted1Outline: Style
    Muted1Solid: Style
    Muted1OutlineBold: Style
    Muted1SolidBold: Style
    Muted1OutlineLight: Style
    Muted1SolidLight: Style
    Muted1Dashed: Style
    Muted1DashedBold: Style
    Muted1DashedLight: Style

    # muted2
    Muted2: Style
    Muted2Bordered: Style
    Muted2Bold: Style
    Muted2Light: Style
    Muted2Flat: Style
    Muted2Outline: Style
    Muted2Solid: Style
    Muted2OutlineBold: Style
    Muted2SolidBold: Style
    Muted2OutlineLight: Style
    Muted2SolidLight: Style
    Muted2Dashed: Style
    Muted2DashedBold: Style
    Muted2DashedLight: Style

    # muted3
    Muted3: Style
    Muted3Bordered: Style
    Muted3Bold: Style
    Muted3Light: Style
    Muted3Flat: Style
    Muted3Outline: Style
    Muted3Solid: Style
    Muted3OutlineBold: Style
    Muted3SolidBold: Style
    Muted3OutlineLight: Style
    Muted3SolidLight: Style
    Muted3Dashed: Style
    Muted3DashedBold: Style
    Muted3DashedLight: Style

    # muted4
    Muted4: Style
    Muted4Bordered: Style
    Muted4Bold: Style
    Muted4Light: Style
    Muted4Flat: Style
    Muted4Outline: Style
    Muted4Solid: Style
    Muted4OutlineBold: Style
    Muted4SolidBold: Style
    Muted4OutlineLight: Style
    Muted4SolidLight: Style
    Muted4Dashed: Style
    Muted4DashedBold: Style
    Muted4DashedLight: Style

    # muted5
    Muted5: Style
    Muted5Bordered: Style
    Muted5Bold: Style
    Muted5Light: Style
    Muted5Flat: Style
    Muted5Outline: Style
    Muted5Solid: Style
    Muted5OutlineBold: Style
    Muted5SolidBold: Style
    Muted5OutlineLight: Style
    Muted5SolidLight: Style
    Muted5Dashed: Style
    Muted5DashedBold: Style
    Muted5DashedLight: Style

    # muted6
    Muted6: Style
    Muted6Bordered: Style
    Muted6Bold: Style
    Muted6Light: Style
    Muted6Flat: Style
    Muted6Outline: Style
    Muted6Solid: Style
    Muted6OutlineBold: Style
    Muted6SolidBold: Style
    Muted6OutlineLight: Style
    Muted6SolidLight: Style
    Muted6Dashed: Style
    Muted6DashedBold: Style
    Muted6DashedLight: Style

    # danger1
    Danger1: Style
    Danger1Bordered: Style
    Danger1Bold: Style
    Danger1Light: Style
    Danger1Flat: Style
    Danger1Outline: Style
    Danger1Solid: Style
    Danger1OutlineBold: Style
    Danger1SolidBold: Style
    Danger1OutlineLight: Style
    Danger1SolidLight: Style
    Danger1Dashed: Style
    Danger1DashedBold: Style
    Danger1DashedLight: Style

    # danger2
    Danger2: Style
    Danger2Bordered: Style
    Danger2Bold: Style
    Danger2Light: Style
    Danger2Flat: Style
    Danger2Outline: Style
    Danger2Solid: Style
    Danger2OutlineBold: Style
    Danger2SolidBold: Style
    Danger2OutlineLight: Style
    Danger2SolidLight: Style
    Danger2Dashed: Style
    Danger2DashedBold: Style
    Danger2DashedLight: Style

    # danger3
    Danger3: Style
    Danger3Bordered: Style
    Danger3Bold: Style
    Danger3Light: Style
    Danger3Flat: Style
    Danger3Outline: Style
    Danger3Solid: Style
    Danger3OutlineBold: Style
    Danger3SolidBold: Style
    Danger3OutlineLight: Style
    Danger3SolidLight: Style
    Danger3Dashed: Style
    Danger3DashedBold: Style
    Danger3DashedLight: Style

    # danger4
    Danger4: Style
    Danger4Bordered: Style
    Danger4Bold: Style
    Danger4Light: Style
    Danger4Flat: Style
    Danger4Outline: Style
    Danger4Solid: Style
    Danger4OutlineBold: Style
    Danger4SolidBold: Style
    Danger4OutlineLight: Style
    Danger4SolidLight: Style
    Danger4Dashed: Style
    Danger4DashedBold: Style
    Danger4DashedLight: Style

    # danger5
    Danger5: Style
    Danger5Bordered: Style
    Danger5Bold: Style
    Danger5Light: Style
    Danger5Flat: Style
    Danger5Outline: Style
    Danger5Solid: Style
    Danger5OutlineBold: Style
    Danger5SolidBold: Style
    Danger5OutlineLight: Style
    Danger5SolidLight: Style
    Danger5Dashed: Style
    Danger5DashedBold: Style
    Danger5DashedLight: Style

    # danger6
    Danger6: Style
    Danger6Bordered: Style
    Danger6Bold: Style
    Danger6Light: Style
    Danger6Flat: Style
    Danger6Outline: Style
    Danger6Solid: Style
    Danger6OutlineBold: Style
    Danger6SolidBold: Style
    Danger6OutlineLight: Style
    Danger6SolidLight: Style
    Danger6Dashed: Style
    Danger6DashedBold: Style
    Danger6DashedLight: Style

    # success1
    Success1: Style
    Success1Bordered: Style
    Success1Bold: Style
    Success1Light: Style
    Success1Flat: Style
    Success1Outline: Style
    Success1Solid: Style
    Success1OutlineBold: Style
    Success1SolidBold: Style
    Success1OutlineLight: Style
    Success1SolidLight: Style
    Success1Dashed: Style
    Success1DashedBold: Style
    Success1DashedLight: Style

    # success2
    Success2: Style
    Success2Bordered: Style
    Success2Bold: Style
    Success2Light: Style
    Success2Flat: Style
    Success2Outline: Style
    Success2Solid: Style
    Success2OutlineBold: Style
    Success2SolidBold: Style
    Success2OutlineLight: Style
    Success2SolidLight: Style
    Success2Dashed: Style
    Success2DashedBold: Style
    Success2DashedLight: Style

    # success3
    Success3: Style
    Success3Bordered: Style
    Success3Bold: Style
    Success3Light: Style
    Success3Flat: Style
    Success3Outline: Style
    Success3Solid: Style
    Success3OutlineBold: Style
    Success3SolidBold: Style
    Success3OutlineLight: Style
    Success3SolidLight: Style
    Success3Dashed: Style
    Success3DashedBold: Style
    Success3DashedLight: Style

    # success4
    Success4: Style
    Success4Bordered: Style
    Success4Bold: Style
    Success4Light: Style
    Success4Flat: Style
    Success4Outline: Style
    Success4Solid: Style
    Success4OutlineBold: Style
    Success4SolidBold: Style
    Success4OutlineLight: Style
    Success4SolidLight: Style
    Success4Dashed: Style
    Success4DashedBold: Style
    Success4DashedLight: Style

    # success5
    Success5: Style
    Success5Bordered: Style
    Success5Bold: Style
    Success5Light: Style
    Success5Flat: Style
    Success5Outline: Style
    Success5Solid: Style
    Success5OutlineBold: Style
    Success5SolidBold: Style
    Success5OutlineLight: Style
    Success5SolidLight: Style
    Success5Dashed: Style
    Success5DashedBold: Style
    Success5DashedLight: Style

    # success6
    Success6: Style
    Success6Bordered: Style
    Success6Bold: Style
    Success6Light: Style
    Success6Flat: Style
    Success6Outline: Style
    Success6Solid: Style
    Success6OutlineBold: Style
    Success6SolidBold: Style
    Success6OutlineLight: Style
    Success6SolidLight: Style
    Success6Dashed: Style
    Success6DashedBold: Style
    Success6DashedLight: Style

    # White
    White: Style
    WhiteBordered: Style
    WhiteBold: Style
    WhiteLight: Style
    WhiteFlat: Style
    WhiteOutline: Style
    WhiteSolid: Style
    WhiteOutlineBold: Style
    WhiteSolidBold: Style
    WhiteOutlineLight: Style
    WhiteSolidLight: Style
    WhiteDashed: Style
    WhiteDashedBold: Style
    WhiteDashedLight: Style

    # Gray1
    Gray1: Style
    Gray1Bordered: Style
    Gray1Bold: Style
    Gray1Light: Style
    Gray1Flat: Style
    Gray1Outline: Style
    Gray1Solid: Style
    Gray1OutlineBold: Style
    Gray1SolidBold: Style
    Gray1OutlineLight: Style
    Gray1SolidLight: Style
    Gray1Dashed: Style
    Gray1DashedBold: Style
    Gray1DashedLight: Style

    # Gray2
    Gray2: Style
    Gray2Bordered: Style
    Gray2Bold: Style
    Gray2Light: Style
    Gray2Flat: Style
    Gray2Outline: Style
    Gray2Solid: Style
    Gray2OutlineBold: Style
    Gray2SolidBold: Style
    Gray2OutlineLight: Style
    Gray2SolidLight: Style
    Gray2Dashed: Style
    Gray2DashedBold: Style
    Gray2DashedLight: Style

    # Gray3
    Gray3: Style
    Gray3Bordered: Style
    Gray3Bold: Style
    Gray3Light: Style
    Gray3Flat: Style
    Gray3Outline: Style
    Gray3Solid: Style
    Gray3OutlineBold: Style
    Gray3SolidBold: Style
    Gray3OutlineLight: Style
    Gray3SolidLight: Style
    Gray3Dashed: Style
    Gray3DashedBold: Style
    Gray3DashedLight: Style

    # Gray4
    Gray4: Style
    Gray4Bordered: Style
    Gray4Bold: Style
    Gray4Light: Style
    Gray4Flat: Style
    Gray4Outline: Style
    Gray4Solid: Style
    Gray4OutlineBold: Style
    Gray4SolidBold: Style
    Gray4OutlineLight: Style
    Gray4SolidLight: Style
    Gray4Dashed: Style
    Gray4DashedBold: Style
    Gray4DashedLight: Style

    # Gray5
    Gray5: Style
    Gray5Bordered: Style
    Gray5Bold: Style
    Gray5Light: Style
    Gray5Flat: Style
    Gray5Outline: Style
    Gray5Solid: Style
    Gray5OutlineBold: Style
    Gray5SolidBold: Style
    Gray5OutlineLight: Style
    Gray5SolidLight: Style
    Gray5Dashed: Style
    Gray5DashedBold: Style
    Gray5DashedLight: Style

    # Gray6
    Gray6: Style
    Gray6Bordered: Style
    Gray6Bold: Style
    Gray6Light: Style
    Gray6Flat: Style
    Gray6Outline: Style
    Gray6Solid: Style
    Gray6OutlineBold: Style
    Gray6SolidBold: Style
    Gray6OutlineLight: Style
    Gray6SolidLight: Style
    Gray6Dashed: Style
    Gray6DashedBold: Style
    Gray6DashedLight: Style

    # Gray7
    Gray7: Style
    Gray7Bordered: Style
    Gray7Bold: Style
    Gray7Light: Style
    Gray7Flat: Style
    Gray7Outline: Style
    Gray7Solid: Style
    Gray7OutlineBold: Style
    Gray7SolidBold: Style
    Gray7OutlineLight: Style
    Gray7SolidLight: Style
    Gray7Dashed: Style
    Gray7DashedBold: Style
    Gray7DashedLight: Style

    # Gray8
    Gray8: Style
    Gray8Bordered: Style
    Gray8Bold: Style
    Gray8Light: Style
    Gray8Flat: Style
    Gray8Outline: Style
    Gray8Solid: Style
    Gray8OutlineBold: Style
    Gray8SolidBold: Style
    Gray8OutlineLight: Style
    Gray8SolidLight: Style
    Gray8Dashed: Style
    Gray8DashedBold: Style
    Gray8DashedLight: Style

    # Black
    Black: Style
    BlackBordered: Style
    BlackBold: Style
    BlackLight: Style
    BlackFlat: Style
    BlackOutline: Style
    BlackSolid: Style
    BlackOutlineBold: Style
    BlackSolidBold: Style
    BlackOutlineLight: Style
    BlackSolidLight: Style
    BlackDashed: Style
    BlackDashedBold: Style
    BlackDashedLight: Style

    # --- CornflowerBlue Tones ---

    # CornflowerBlue1
    CornflowerBlue1: Style
    CornflowerBlue1Bordered: Style
    CornflowerBlue1Bold: Style
    CornflowerBlue1Light: Style
    CornflowerBlue1Flat: Style
    CornflowerBlue1Outline: Style
    CornflowerBlue1Solid: Style
    CornflowerBlue1OutlineBold: Style
    CornflowerBlue1SolidBold: Style
    CornflowerBlue1OutlineLight: Style
    CornflowerBlue1SolidLight: Style
    CornflowerBlue1Dashed: Style
    CornflowerBlue1DashedBold: Style
    CornflowerBlue1DashedLight: Style

    # CornflowerBlue2
    CornflowerBlue2: Style
    CornflowerBlue2Bordered: Style
    CornflowerBlue2Bold: Style
    CornflowerBlue2Light: Style
    CornflowerBlue2Flat: Style
    CornflowerBlue2Outline: Style
    CornflowerBlue2Solid: Style
    CornflowerBlue2OutlineBold: Style
    CornflowerBlue2SolidBold: Style
    CornflowerBlue2OutlineLight: Style
    CornflowerBlue2SolidLight: Style
    CornflowerBlue2Dashed: Style
    CornflowerBlue2DashedBold: Style
    CornflowerBlue2DashedLight: Style

    # CornflowerBlue3
    CornflowerBlue3: Style
    CornflowerBlue3Bordered: Style
    CornflowerBlue3Bold: Style
    CornflowerBlue3Light: Style
    CornflowerBlue3Flat: Style
    CornflowerBlue3Outline: Style
    CornflowerBlue3Solid: Style
    CornflowerBlue3OutlineBold: Style
    CornflowerBlue3SolidBold: Style
    CornflowerBlue3OutlineLight: Style
    CornflowerBlue3SolidLight: Style
    CornflowerBlue3Dashed: Style
    CornflowerBlue3DashedBold: Style
    CornflowerBlue3DashedLight: Style

    # CornflowerBlue4
    CornflowerBlue4: Style
    CornflowerBlue4Bordered: Style
    CornflowerBlue4Bold: Style
    CornflowerBlue4Light: Style
    CornflowerBlue4Flat: Style
    CornflowerBlue4Outline: Style
    CornflowerBlue4Solid: Style
    CornflowerBlue4OutlineBold: Style
    CornflowerBlue4SolidBold: Style
    CornflowerBlue4OutlineLight: Style
    CornflowerBlue4SolidLight: Style
    CornflowerBlue4Dashed: Style
    CornflowerBlue4DashedBold: Style
    CornflowerBlue4DashedLight: Style

    # CornflowerBlue5
    CornflowerBlue5: Style
    CornflowerBlue5Bordered: Style
    CornflowerBlue5Bold: Style
    CornflowerBlue5Light: Style
    CornflowerBlue5Flat: Style
    CornflowerBlue5Outline: Style
    CornflowerBlue5Solid: Style
    CornflowerBlue5OutlineBold: Style
    CornflowerBlue5SolidBold: Style
    CornflowerBlue5OutlineLight: Style
    CornflowerBlue5SolidLight: Style
    CornflowerBlue5Dashed: Style
    CornflowerBlue5DashedBold: Style
    CornflowerBlue5DashedLight: Style

    # CornflowerBlue6
    CornflowerBlue6: Style
    CornflowerBlue6Bordered: Style
    CornflowerBlue6Bold: Style
    CornflowerBlue6Light: Style
    CornflowerBlue6Flat: Style
    CornflowerBlue6Outline: Style
    CornflowerBlue6Solid: Style
    CornflowerBlue6OutlineBold: Style
    CornflowerBlue6SolidBold: Style
    CornflowerBlue6OutlineLight: Style
    CornflowerBlue6SolidLight: Style
    CornflowerBlue6Dashed: Style
    CornflowerBlue6DashedBold: Style
    CornflowerBlue6DashedLight: Style

    # --- Blue Tones ---

    # Blue1
    Blue1: Style
    Blue1Bordered: Style
    Blue1Bold: Style
    Blue1Light: Style
    Blue1Flat: Style
    Blue1Outline: Style
    Blue1Solid: Style
    Blue1OutlineBold: Style
    Blue1SolidBold: Style
    Blue1OutlineLight: Style
    Blue1SolidLight: Style
    Blue1Dashed: Style
    Blue1DashedBold: Style
    Blue1DashedLight: Style

    # Blue2
    Blue2: Style
    Blue2Bordered: Style
    Blue2Bold: Style
    Blue2Light: Style
    Blue2Flat: Style
    Blue2Outline: Style
    Blue2Solid: Style
    Blue2OutlineBold: Style
    Blue2SolidBold: Style
    Blue2OutlineLight: Style
    Blue2SolidLight: Style
    Blue2Dashed: Style
    Blue2DashedBold: Style
    Blue2DashedLight: Style

    # Blue3
    Blue3: Style
    Blue3Bordered: Style
    Blue3Bold: Style
    Blue3Light: Style
    Blue3Flat: Style
    Blue3Outline: Style
    Blue3Solid: Style
    Blue3OutlineBold: Style
    Blue3SolidBold: Style
    Blue3OutlineLight: Style
    Blue3SolidLight: Style
    Blue3Dashed: Style
    Blue3DashedBold: Style
    Blue3DashedLight: Style

    # Blue4
    Blue4: Style
    Blue4Bordered: Style
    Blue4Bold: Style
    Blue4Light: Style
    Blue4Flat: Style
    Blue4Outline: Style
    Blue4Solid: Style
    Blue4OutlineBold: Style
    Blue4SolidBold: Style
    Blue4OutlineLight: Style
    Blue4SolidLight: Style
    Blue4Dashed: Style
    Blue4DashedBold: Style
    Blue4DashedLight: Style

    # Blue5
    Blue5: Style
    Blue5Bordered: Style
    Blue5Bold: Style
    Blue5Light: Style
    Blue5Flat: Style
    Blue5Outline: Style
    Blue5Solid: Style
    Blue5OutlineBold: Style
    Blue5SolidBold: Style
    Blue5OutlineLight: Style
    Blue5SolidLight: Style
    Blue5Dashed: Style
    Blue5DashedBold: Style
    Blue5DashedLight: Style

    # Blue6
    Blue6: Style
    Blue6Bordered: Style
    Blue6Bold: Style
    Blue6Light: Style
    Blue6Flat: Style
    Blue6Outline: Style
    Blue6Solid: Style
    Blue6OutlineBold: Style
    Blue6SolidBold: Style
    Blue6OutlineLight: Style
    Blue6SolidLight: Style
    Blue6Dashed: Style
    Blue6DashedBold: Style
    Blue6DashedLight: Style

    # --- Red Tones ---

    # Red1
    Red1: Style
    Red1Bordered: Style
    Red1Bold: Style
    Red1Light: Style
    Red1Flat: Style
    Red1Outline: Style
    Red1Solid: Style
    Red1OutlineBold: Style
    Red1SolidBold: Style
    Red1OutlineLight: Style
    Red1SolidLight: Style
    Red1Dashed: Style
    Red1DashedBold: Style
    Red1DashedLight: Style

    # Red2
    Red2: Style
    Red2Bordered: Style
    Red2Bold: Style
    Red2Light: Style
    Red2Flat: Style
    Red2Outline: Style
    Red2Solid: Style
    Red2OutlineBold: Style
    Red2SolidBold: Style
    Red2OutlineLight: Style
    Red2SolidLight: Style
    Red2Dashed: Style
    Red2DashedBold: Style
    Red2DashedLight: Style

    # Red3
    Red3: Style
    Red3Bordered: Style
    Red3Bold: Style
    Red3Light: Style
    Red3Flat: Style
    Red3Outline: Style
    Red3Solid: Style
    Red3OutlineBold: Style
    Red3SolidBold: Style
    Red3OutlineLight: Style
    Red3SolidLight: Style
    Red3Dashed: Style
    Red3DashedBold: Style
    Red3DashedLight: Style

    # Red4
    Red4: Style
    Red4Bordered: Style
    Red4Bold: Style
    Red4Light: Style
    Red4Flat: Style
    Red4Outline: Style
    Red4Solid: Style
    Red4OutlineBold: Style
    Red4SolidBold: Style
    Red4OutlineLight: Style
    Red4SolidLight: Style
    Red4Dashed: Style
    Red4DashedBold: Style
    Red4DashedLight: Style

    # Red5
    Red5: Style
    Red5Bordered: Style
    Red5Bold: Style
    Red5Light: Style
    Red5Flat: Style
    Red5Outline: Style
    Red5Solid: Style
    Red5OutlineBold: Style
    Red5SolidBold: Style
    Red5OutlineLight: Style
    Red5SolidLight: Style
    Red5Dashed: Style
    Red5DashedBold: Style
    Red5DashedLight: Style

    # Red6
    Red6: Style
    Red6Bordered: Style
    Red6Bold: Style
    Red6Light: Style
    Red6Flat: Style
    Red6Outline: Style
    Red6Solid: Style
    Red6OutlineBold: Style
    Red6SolidBold: Style
    Red6OutlineLight: Style
    Red6SolidLight: Style
    Red6Dashed: Style
    Red6DashedBold: Style
    Red6DashedLight: Style

    # --- RedBerry Tones ---

    # RedBerry1
    RedBerry1: Style
    RedBerry1Bordered: Style
    RedBerry1Bold: Style
    RedBerry1Light: Style
    RedBerry1Flat: Style
    RedBerry1Outline: Style
    RedBerry1Solid: Style
    RedBerry1OutlineBold: Style
    RedBerry1SolidBold: Style
    RedBerry1OutlineLight: Style
    RedBerry1SolidLight: Style
    RedBerry1Dashed: Style
    RedBerry1DashedBold: Style
    RedBerry1DashedLight: Style

    # RedBerry2
    RedBerry2: Style
    RedBerry2Bordered: Style
    RedBerry2Bold: Style
    RedBerry2Light: Style
    RedBerry2Flat: Style
    RedBerry2Outline: Style
    RedBerry2Solid: Style
    RedBerry2OutlineBold: Style
    RedBerry2SolidBold: Style
    RedBerry2OutlineLight: Style
    RedBerry2SolidLight: Style
    RedBerry2Dashed: Style
    RedBerry2DashedBold: Style
    RedBerry2DashedLight: Style

    # RedBerry3
    RedBerry3: Style
    RedBerry3Bordered: Style
    RedBerry3Bold: Style
    RedBerry3Light: Style
    RedBerry3Flat: Style
    RedBerry3Outline: Style
    RedBerry3Solid: Style
    RedBerry3OutlineBold: Style
    RedBerry3SolidBold: Style
    RedBerry3OutlineLight: Style
    RedBerry3SolidLight: Style
    RedBerry3Dashed: Style
    RedBerry3DashedBold: Style
    RedBerry3DashedLight: Style

    # RedBerry4
    RedBerry4: Style
    RedBerry4Bordered: Style
    RedBerry4Bold: Style
    RedBerry4Light: Style
    RedBerry4Flat: Style
    RedBerry4Outline: Style
    RedBerry4Solid: Style
    RedBerry4OutlineBold: Style
    RedBerry4SolidBold: Style
    RedBerry4OutlineLight: Style
    RedBerry4SolidLight: Style
    RedBerry4Dashed: Style
    RedBerry4DashedBold: Style
    RedBerry4DashedLight: Style

    # RedBerry5
    RedBerry5: Style
    RedBerry5Bordered: Style
    RedBerry5Bold: Style
    RedBerry5Light: Style
    RedBerry5Flat: Style
    RedBerry5Outline: Style
    RedBerry5Solid: Style
    RedBerry5OutlineBold: Style
    RedBerry5SolidBold: Style
    RedBerry5OutlineLight: Style
    RedBerry5SolidLight: Style
    RedBerry5Dashed: Style
    RedBerry5DashedBold: Style
    RedBerry5DashedLight: Style

    # RedBerry6
    RedBerry6: Style
    RedBerry6Bordered: Style
    RedBerry6Bold: Style
    RedBerry6Light: Style
    RedBerry6Flat: Style
    RedBerry6Outline: Style
    RedBerry6Solid: Style
    RedBerry6OutlineBold: Style
    RedBerry6SolidBold: Style
    RedBerry6OutlineLight: Style
    RedBerry6SolidLight: Style
    RedBerry6Dashed: Style
    RedBerry6DashedBold: Style
    RedBerry6DashedLight: Style

    # --- Green Tones ---

    # Green1
    Green1: Style
    Green1Bordered: Style
    Green1Bold: Style
    Green1Light: Style
    Green1Flat: Style
    Green1Outline: Style
    Green1Solid: Style
    Green1OutlineBold: Style
    Green1SolidBold: Style
    Green1OutlineLight: Style
    Green1SolidLight: Style
    Green1Dashed: Style
    Green1DashedBold: Style
    Green1DashedLight: Style

    # Green2
    Green2: Style
    Green2Bordered: Style
    Green2Bold: Style
    Green2Light: Style
    Green2Flat: Style
    Green2Outline: Style
    Green2Solid: Style
    Green2OutlineBold: Style
    Green2SolidBold: Style
    Green2OutlineLight: Style
    Green2SolidLight: Style
    Green2Dashed: Style
    Green2DashedBold: Style
    Green2DashedLight: Style

    # Green3
    Green3: Style
    Green3Bordered: Style
    Green3Bold: Style
    Green3Light: Style
    Green3Flat: Style
    Green3Outline: Style
    Green3Solid: Style
    Green3OutlineBold: Style
    Green3SolidBold: Style
    Green3OutlineLight: Style
    Green3SolidLight: Style
    Green3Dashed: Style
    Green3DashedBold: Style
    Green3DashedLight: Style

    # Green4
    Green4: Style
    Green4Bordered: Style
    Green4Bold: Style
    Green4Light: Style
    Green4Flat: Style
    Green4Outline: Style
    Green4Solid: Style
    Green4OutlineBold: Style
    Green4SolidBold: Style
    Green4OutlineLight: Style
    Green4SolidLight: Style
    Green4Dashed: Style
    Green4DashedBold: Style
    Green4DashedLight: Style

    # Green5
    Green5: Style
    Green5Bordered: Style
    Green5Bold: Style
    Green5Light: Style
    Green5Flat: Style
    Green5Outline: Style
    Green5Solid: Style
    Green5OutlineBold: Style
    Green5SolidBold: Style
    Green5OutlineLight: Style
    Green5SolidLight: Style
    Green5Dashed: Style
    Green5DashedBold: Style
    Green5DashedLight: Style

    # Green6
    Green6: Style
    Green6Bordered: Style
    Green6Bold: Style
    Green6Light: Style
    Green6Flat: Style
    Green6Outline: Style
    Green6Solid: Style
    Green6OutlineBold: Style
    Green6SolidBold: Style
    Green6OutlineLight: Style
    Green6SolidLight: Style
    Green6Dashed: Style
    Green6DashedBold: Style
    Green6DashedLight: Style

    # --- Yellow Tones ---

    # Yellow1
    Yellow1: Style
    Yellow1Bordered: Style
    Yellow1Bold: Style
    Yellow1Light: Style
    Yellow1Flat: Style
    Yellow1Outline: Style
    Yellow1Solid: Style
    Yellow1OutlineBold: Style
    Yellow1SolidBold: Style
    Yellow1OutlineLight: Style
    Yellow1SolidLight: Style
    Yellow1Dashed: Style
    Yellow1DashedBold: Style
    Yellow1DashedLight: Style

    # Yellow2
    Yellow2: Style
    Yellow2Bordered: Style
    Yellow2Bold: Style
    Yellow2Light: Style
    Yellow2Flat: Style
    Yellow2Outline: Style
    Yellow2Solid: Style
    Yellow2OutlineBold: Style
    Yellow2SolidBold: Style
    Yellow2OutlineLight: Style
    Yellow2SolidLight: Style
    Yellow2Dashed: Style
    Yellow2DashedBold: Style
    Yellow2DashedLight: Style

    # Yellow3
    Yellow3: Style
    Yellow3Bordered: Style
    Yellow3Bold: Style
    Yellow3Light: Style
    Yellow3Flat: Style
    Yellow3Outline: Style
    Yellow3Solid: Style
    Yellow3OutlineBold: Style
    Yellow3SolidBold: Style
    Yellow3OutlineLight: Style
    Yellow3SolidLight: Style
    Yellow3Dashed: Style
    Yellow3DashedBold: Style
    Yellow3DashedLight: Style

    # Yellow4
    Yellow4: Style
    Yellow4Bordered: Style
    Yellow4Bold: Style
    Yellow4Light: Style
    Yellow4Flat: Style
    Yellow4Outline: Style
    Yellow4Solid: Style
    Yellow4OutlineBold: Style
    Yellow4SolidBold: Style
    Yellow4OutlineLight: Style
    Yellow4SolidLight: Style
    Yellow4Dashed: Style
    Yellow4DashedBold: Style
    Yellow4DashedLight: Style

    # Yellow5
    Yellow5: Style
    Yellow5Bordered: Style
    Yellow5Bold: Style
    Yellow5Light: Style
    Yellow5Flat: Style
    Yellow5Outline: Style
    Yellow5Solid: Style
    Yellow5OutlineBold: Style
    Yellow5SolidBold: Style
    Yellow5OutlineLight: Style
    Yellow5SolidLight: Style
    Yellow5Dashed: Style
    Yellow5DashedBold: Style
    Yellow5DashedLight: Style

    # Yellow6
    Yellow6: Style
    Yellow6Bordered: Style
    Yellow6Bold: Style
    Yellow6Light: Style
    Yellow6Flat: Style
    Yellow6Outline: Style
    Yellow6Solid: Style
    Yellow6OutlineBold: Style
    Yellow6SolidBold: Style
    Yellow6OutlineLight: Style
    Yellow6SolidLight: Style
    Yellow6Dashed: Style
    Yellow6DashedBold: Style
    Yellow6DashedLight: Style

    # --- Orange Tones ---

    # Orange1
    Orange1: Style
    Orange1Bordered: Style
    Orange1Bold: Style
    Orange1Light: Style
    Orange1Flat: Style
    Orange1Outline: Style
    Orange1Solid: Style
    Orange1OutlineBold: Style
    Orange1SolidBold: Style
    Orange1OutlineLight: Style
    Orange1SolidLight: Style
    Orange1Dashed: Style
    Orange1DashedBold: Style
    Orange1DashedLight: Style

    # Orange2
    Orange2: Style
    Orange2Bordered: Style
    Orange2Bold: Style
    Orange2Light: Style
    Orange2Flat: Style
    Orange2Outline: Style
    Orange2Solid: Style
    Orange2OutlineBold: Style
    Orange2SolidBold: Style
    Orange2OutlineLight: Style
    Orange2SolidLight: Style
    Orange2Dashed: Style
    Orange2DashedBold: Style
    Orange2DashedLight: Style

    # Orange3
    Orange3: Style
    Orange3Bordered: Style
    Orange3Bold: Style
    Orange3Light: Style
    Orange3Flat: Style
    Orange3Outline: Style
    Orange3Solid: Style
    Orange3OutlineBold: Style
    Orange3SolidBold: Style
    Orange3OutlineLight: Style
    Orange3SolidLight: Style
    Orange3Dashed: Style
    Orange3DashedBold: Style
    Orange3DashedLight: Style

    # Orange4
    Orange4: Style
    Orange4Bordered: Style
    Orange4Bold: Style
    Orange4Light: Style
    Orange4Flat: Style
    Orange4Outline: Style
    Orange4Solid: Style
    Orange4OutlineBold: Style
    Orange4SolidBold: Style
    Orange4OutlineLight: Style
    Orange4SolidLight: Style
    Orange4Dashed: Style
    Orange4DashedBold: Style
    Orange4DashedLight: Style

    # Orange5
    Orange5: Style
    Orange5Bordered: Style
    Orange5Bold: Style
    Orange5Light: Style
    Orange5Flat: Style
    Orange5Outline: Style
    Orange5Solid: Style
    Orange5OutlineBold: Style
    Orange5SolidBold: Style
    Orange5OutlineLight: Style
    Orange5SolidLight: Style
    Orange5Dashed: Style
    Orange5DashedBold: Style
    Orange5DashedLight: Style

    # Orange6
    Orange6: Style
    Orange6Bordered: Style
    Orange6Bold: Style
    Orange6Light: Style
    Orange6Flat: Style
    Orange6Outline: Style
    Orange6Solid: Style
    Orange6OutlineBold: Style
    Orange6SolidBold: Style
    Orange6OutlineLight: Style
    Orange6SolidLight: Style
    Orange6Dashed: Style
    Orange6DashedBold: Style
    Orange6DashedLight: Style

    # --- Cyan Tones ---

    # Cyan1
    Cyan1: Style
    Cyan1Bordered: Style
    Cyan1Bold: Style
    Cyan1Light: Style
    Cyan1Flat: Style
    Cyan1Outline: Style
    Cyan1Solid: Style
    Cyan1OutlineBold: Style
    Cyan1SolidBold: Style
    Cyan1OutlineLight: Style
    Cyan1SolidLight: Style
    Cyan1Dashed: Style
    Cyan1DashedBold: Style
    Cyan1DashedLight: Style

    # Cyan2
    Cyan2: Style
    Cyan2Bordered: Style
    Cyan2Bold: Style
    Cyan2Light: Style
    Cyan2Flat: Style
    Cyan2Outline: Style
    Cyan2Solid: Style
    Cyan2OutlineBold: Style
    Cyan2SolidBold: Style
    Cyan2OutlineLight: Style
    Cyan2SolidLight: Style
    Cyan2Dashed: Style
    Cyan2DashedBold: Style
    Cyan2DashedLight: Style

    # Cyan3
    Cyan3: Style
    Cyan3Bordered: Style
    Cyan3Bold: Style
    Cyan3Light: Style
    Cyan3Flat: Style
    Cyan3Outline: Style
    Cyan3Solid: Style
    Cyan3OutlineBold: Style
    Cyan3SolidBold: Style
    Cyan3OutlineLight: Style
    Cyan3SolidLight: Style
    Cyan3Dashed: Style
    Cyan3DashedBold: Style
    Cyan3DashedLight: Style

    # Cyan4
    Cyan4: Style
    Cyan4Bordered: Style
    Cyan4Bold: Style
    Cyan4Light: Style
    Cyan4Flat: Style
    Cyan4Outline: Style
    Cyan4Solid: Style
    Cyan4OutlineBold: Style
    Cyan4SolidBold: Style
    Cyan4OutlineLight: Style
    Cyan4SolidLight: Style
    Cyan4Dashed: Style
    Cyan4DashedBold: Style
    Cyan4DashedLight: Style

    # Cyan5
    Cyan5: Style
    Cyan5Bordered: Style
    Cyan5Bold: Style
    Cyan5Light: Style
    Cyan5Flat: Style
    Cyan5Outline: Style
    Cyan5Solid: Style
    Cyan5OutlineBold: Style
    Cyan5SolidBold: Style
    Cyan5OutlineLight: Style
    Cyan5SolidLight: Style
    Cyan5Dashed: Style
    Cyan5DashedBold: Style
    Cyan5DashedLight: Style

    # Cyan6
    Cyan6: Style
    Cyan6Bordered: Style
    Cyan6Bold: Style
    Cyan6Light: Style
    Cyan6Flat: Style
    Cyan6Outline: Style
    Cyan6Solid: Style
    Cyan6OutlineBold: Style
    Cyan6SolidBold: Style
    Cyan6OutlineLight: Style
    Cyan6SolidLight: Style
    Cyan6Dashed: Style
    Cyan6DashedBold: Style
    Cyan6DashedLight: Style

    # --- Purple Tones ---

    # Purple1
    Purple1: Style
    Purple1Bordered: Style
    Purple1Bold: Style
    Purple1Light: Style
    Purple1Flat: Style
    Purple1Outline: Style
    Purple1Solid: Style
    Purple1OutlineBold: Style
    Purple1SolidBold: Style
    Purple1OutlineLight: Style
    Purple1SolidLight: Style
    Purple1Dashed: Style
    Purple1DashedBold: Style
    Purple1DashedLight: Style

    # Purple2
    Purple2: Style
    Purple2Bordered: Style
    Purple2Bold: Style
    Purple2Light: Style
    Purple2Flat: Style
    Purple2Outline: Style
    Purple2Solid: Style
    Purple2OutlineBold: Style
    Purple2SolidBold: Style
    Purple2OutlineLight: Style
    Purple2SolidLight: Style
    Purple2Dashed: Style
    Purple2DashedBold: Style
    Purple2DashedLight: Style

    # Purple3
    Purple3: Style
    Purple3Bordered: Style
    Purple3Bold: Style
    Purple3Light: Style
    Purple3Flat: Style
    Purple3Outline: Style
    Purple3Solid: Style
    Purple3OutlineBold: Style
    Purple3SolidBold: Style
    Purple3OutlineLight: Style
    Purple3SolidLight: Style
    Purple3Dashed: Style
    Purple3DashedBold: Style
    Purple3DashedLight: Style

    # Purple4
    Purple4: Style
    Purple4Bordered: Style
    Purple4Bold: Style
    Purple4Light: Style
    Purple4Flat: Style
    Purple4Outline: Style
    Purple4Solid: Style
    Purple4OutlineBold: Style
    Purple4SolidBold: Style
    Purple4OutlineLight: Style
    Purple4SolidLight: Style
    Purple4Dashed: Style
    Purple4DashedBold: Style
    Purple4DashedLight: Style

    # Purple5
    Purple5: Style
    Purple5Bordered: Style
    Purple5Bold: Style
    Purple5Light: Style
    Purple5Flat: Style
    Purple5Outline: Style
    Purple5Solid: Style
    Purple5OutlineBold: Style
    Purple5SolidBold: Style
    Purple5OutlineLight: Style
    Purple5SolidLight: Style
    Purple5Dashed: Style
    Purple5DashedBold: Style
    Purple5DashedLight: Style

    # Purple6
    Purple6: Style
    Purple6Bordered: Style
    Purple6Bold: Style
    Purple6Light: Style
    Purple6Flat: Style
    Purple6Outline: Style
    Purple6Solid: Style
    Purple6OutlineBold: Style
    Purple6SolidBold: Style
    Purple6OutlineLight: Style
    Purple6SolidLight: Style
    Purple6Dashed: Style
    Purple6DashedBold: Style
    Purple6DashedLight: Style

    # --- Magenta Tones ---

    # Magenta1
    Magenta1: Style
    Magenta1Bordered: Style
    Magenta1Bold: Style
    Magenta1Light: Style
    Magenta1Flat: Style
    Magenta1Outline: Style
    Magenta1Solid: Style
    Magenta1OutlineBold: Style
    Magenta1SolidBold: Style
    Magenta1OutlineLight: Style
    Magenta1SolidLight: Style
    Magenta1Dashed: Style
    Magenta1DashedBold: Style
    Magenta1DashedLight: Style

    # Magenta2
    Magenta2: Style
    Magenta2Bordered: Style
    Magenta2Bold: Style
    Magenta2Light: Style
    Magenta2Flat: Style
    Magenta2Outline: Style
    Magenta2Solid: Style
    Magenta2OutlineBold: Style
    Magenta2SolidBold: Style
    Magenta2OutlineLight: Style
    Magenta2SolidLight: Style
    Magenta2Dashed: Style
    Magenta2DashedBold: Style
    Magenta2DashedLight: Style

    # Magenta3
    Magenta3: Style
    Magenta3Bordered: Style
    Magenta3Bold: Style
    Magenta3Light: Style
    Magenta3Flat: Style
    Magenta3Outline: Style
    Magenta3Solid: Style
    Magenta3OutlineBold: Style
    Magenta3SolidBold: Style
    Magenta3OutlineLight: Style
    Magenta3SolidLight: Style
    Magenta3Dashed: Style
    Magenta3DashedBold: Style
    Magenta3DashedLight: Style

    # Magenta4
    Magenta4: Style
    Magenta4Bordered: Style
    Magenta4Bold: Style
    Magenta4Light: Style
    Magenta4Flat: Style
    Magenta4Outline: Style
    Magenta4Solid: Style
    Magenta4OutlineBold: Style
    Magenta4SolidBold: Style
    Magenta4OutlineLight: Style
    Magenta4SolidLight: Style
    Magenta4Dashed: Style
    Magenta4DashedBold: Style
    Magenta4DashedLight: Style

    # Magenta5
    Magenta5: Style
    Magenta5Bordered: Style
    Magenta5Bold: Style
    Magenta5Light: Style
    Magenta5Flat: Style
    Magenta5Outline: Style
    Magenta5Solid: Style
    Magenta5OutlineBold: Style
    Magenta5SolidBold: Style
    Magenta5OutlineLight: Style
    Magenta5SolidLight: Style
    Magenta5Dashed: Style
    Magenta5DashedBold: Style
    Magenta5DashedLight: Style

    # Magenta6
    Magenta6: Style
    Magenta6Bordered: Style
    Magenta6Bold: Style
    Magenta6Light: Style
    Magenta6Flat: Style
    Magenta6Outline: Style
    Magenta6Solid: Style
    Magenta6OutlineBold: Style
    Magenta6SolidBold: Style
    Magenta6OutlineLight: Style
    Magenta6SolidLight: Style
    Magenta6Dashed: Style
    Magenta6DashedBold: Style
    Magenta6DashedLight: Style

    # --- Primaries (Unnumbered) ---

    # CornflowerBlue
    CornflowerBlue: Style
    CornflowerBlueBordered: Style
    CornflowerBlueBold: Style
    CornflowerBlueLight: Style
    CornflowerBlueFlat: Style
    CornflowerBlueOutline: Style
    CornflowerBlueSolid: Style
    CornflowerBlueOutlineBold: Style
    CornflowerBlueSolidBold: Style
    CornflowerBlueOutlineLight: Style
    CornflowerBlueSolidLight: Style
    CornflowerBlueDashed: Style
    CornflowerBlueDashedBold: Style
    CornflowerBlueDashedLight: Style

    # Blue
    Blue: Style
    BlueBordered: Style
    BlueBold: Style
    BlueLight: Style
    BlueFlat: Style
    BlueOutline: Style
    BlueSolid: Style
    BlueOutlineBold: Style
    BlueSolidBold: Style
    BlueOutlineLight: Style
    BlueSolidLight: Style
    BlueDashed: Style
    BlueDashedBold: Style
    BlueDashedLight: Style

    # Red
    Red: Style
    RedBordered: Style
    RedBold: Style
    RedLight: Style
    RedFlat: Style
    RedOutline: Style
    RedSolid: Style
    RedOutlineBold: Style
    RedSolidBold: Style
    RedOutlineLight: Style
    RedSolidLight: Style
    RedDashed: Style
    RedDashedBold: Style
    RedDashedLight: Style

    # RedBerry
    RedBerry: Style
    RedBerryBordered: Style
    RedBerryBold: Style
    RedBerryLight: Style
    RedBerryFlat: Style
    RedBerryOutline: Style
    RedBerrySolid: Style
    RedBerryOutlineBold: Style
    RedBerrySolidBold: Style
    RedBerryOutlineLight: Style
    RedBerrySolidLight: Style
    RedBerryDashed: Style
    RedBerryDashedBold: Style
    RedBerryDashedLight: Style

    # Green
    Green: Style
    GreenBordered: Style
    GreenBold: Style
    GreenLight: Style
    GreenFlat: Style
    GreenOutline: Style
    GreenSolid: Style
    GreenOutlineBold: Style
    GreenSolidBold: Style
    GreenOutlineLight: Style
    GreenSolidLight: Style
    GreenDashed: Style
    GreenDashedBold: Style
    GreenDashedLight: Style

    # Yellow
    Yellow: Style
    YellowBordered: Style
    YellowBold: Style
    YellowLight: Style
    YellowFlat: Style
    YellowOutline: Style
    YellowSolid: Style
    YellowOutlineBold: Style
    YellowSolidBold: Style
    YellowOutlineLight: Style
    YellowSolidLight: Style
    YellowDashed: Style
    YellowDashedBold: Style
    YellowDashedLight: Style

    # Orange
    Orange: Style
    OrangeBordered: Style
    OrangeBold: Style
    OrangeLight: Style
    OrangeFlat: Style
    OrangeOutline: Style
    OrangeSolid: Style
    OrangeOutlineBold: Style
    OrangeSolidBold: Style
    OrangeOutlineLight: Style
    OrangeSolidLight: Style
    OrangeDashed: Style
    OrangeDashedBold: Style
    OrangeDashedLight: Style

    # Cyan
    Cyan: Style
    CyanBordered: Style
    CyanBold: Style
    CyanLight: Style
    CyanFlat: Style
    CyanOutline: Style
    CyanSolid: Style
    CyanOutlineBold: Style
    CyanSolidBold: Style
    CyanOutlineLight: Style
    CyanSolidLight: Style
    CyanDashed: Style
    CyanDashedBold: Style
    CyanDashedLight: Style

    # Purple
    Purple: Style
    PurpleBordered: Style
    PurpleBold: Style
    PurpleLight: Style
    PurpleFlat: Style
    PurpleOutline: Style
    PurpleSolid: Style
    PurpleOutlineBold: Style
    PurpleSolidBold: Style
    PurpleOutlineLight: Style
    PurpleSolidLight: Style
    PurpleDashed: Style
    PurpleDashedBold: Style
    PurpleDashedLight: Style

    # Magenta
    Magenta: Style
    MagentaBordered: Style
    MagentaBold: Style
    MagentaLight: Style
    MagentaFlat: Style
    MagentaOutline: Style
    MagentaSolid: Style
    MagentaOutlineBold: Style
    MagentaSolidBold: Style
    MagentaOutlineLight: Style
    MagentaSolidLight: Style
    MagentaDashed: Style
    MagentaDashedBold: Style
    MagentaDashedLight: Style

    # Pink
    Pink: Style
    PinkBordered: Style
    PinkBold: Style
    PinkLight: Style
    PinkFlat: Style
    PinkOutline: Style
    PinkSolid: Style
    PinkOutlineBold: Style
    PinkSolidBold: Style
    PinkOutlineLight: Style
    PinkSolidLight: Style
    PinkDashed: Style
    PinkDashedBold: Style
    PinkDashedLight: Style

    # Lime
    Lime: Style
    LimeBordered: Style
    LimeBold: Style
    LimeLight: Style
    LimeFlat: Style
    LimeOutline: Style
    LimeSolid: Style
    LimeOutlineBold: Style
    LimeSolidBold: Style
    LimeOutlineLight: Style
    LimeSolidLight: Style
    LimeDashed: Style
    LimeDashedBold: Style
    LimeDashedLight: Style

    # Teal
    Teal: Style
    TealBordered: Style
    TealBold: Style
    TealLight: Style
    TealFlat: Style
    TealOutline: Style
    TealSolid: Style
    TealOutlineBold: Style
    TealSolidBold: Style
    TealOutlineLight: Style
    TealSolidLight: Style
    TealDashed: Style
    TealDashedBold: Style
    TealDashedLight: Style

    # Navy
    Navy: Style
    NavyBordered: Style
    NavyBold: Style
    NavyLight: Style
    NavyFlat: Style
    NavyOutline: Style
    NavySolid: Style
    NavyOutlineBold: Style
    NavySolidBold: Style
    NavyOutlineLight: Style
    NavySolidLight: Style
    NavyDashed: Style
    NavyDashedBold: Style
    NavyDashedLight: Style

    # Olive
    Olive: Style
    OliveBordered: Style
    OliveBold: Style
    OliveLight: Style
    OliveFlat: Style
    OliveOutline: Style
    OliveSolid: Style
    OliveOutlineBold: Style
    OliveSolidBold: Style
    OliveOutlineLight: Style
    OliveSolidLight: Style
    OliveDashed: Style
    OliveDashedBold: Style
    OliveDashedLight: Style

    # Brown
    Brown: Style
    BrownBordered: Style
    BrownBold: Style
    BrownLight: Style
    BrownFlat: Style
    BrownOutline: Style
    BrownSolid: Style
    BrownOutlineBold: Style
    BrownSolidBold: Style
    BrownOutlineLight: Style
    BrownSolidLight: Style
    BrownDashed: Style
    BrownDashedBold: Style
    BrownDashedLight: Style

    # Gold
    Gold: Style
    GoldBordered: Style
    GoldBold: Style
    GoldLight: Style
    GoldFlat: Style
    GoldOutline: Style
    GoldSolid: Style
    GoldOutlineBold: Style
    GoldSolidBold: Style
    GoldOutlineLight: Style
    GoldSolidLight: Style
    GoldDashed: Style
    GoldDashedBold: Style
    GoldDashedLight: Style

    # Aqua
    Aqua: Style
    AquaBordered: Style
    AquaBold: Style
    AquaLight: Style
    AquaFlat: Style
    AquaOutline: Style
    AquaSolid: Style
    AquaOutlineBold: Style
    AquaSolidBold: Style
    AquaOutlineLight: Style
    AquaSolidLight: Style
    AquaDashed: Style
    AquaDashedBold: Style
    AquaDashedLight: Style

    # GreenYellow
    GreenYellow: Style
    GreenYellowBordered: Style
    GreenYellowBold: Style
    GreenYellowLight: Style
    GreenYellowFlat: Style
    GreenYellowOutline: Style
    GreenYellowSolid: Style
    GreenYellowOutlineBold: Style
    GreenYellowSolidBold: Style
    GreenYellowOutlineLight: Style
    GreenYellowSolidLight: Style
    GreenYellowDashed: Style
    GreenYellowDashedBold: Style
    GreenYellowDashedLight: Style

    # Ivory
    Ivory: Style
    IvoryBordered: Style
    IvoryBold: Style
    IvoryLight: Style
    IvoryFlat: Style
    IvoryOutline: Style
    IvorySolid: Style
    IvoryOutlineBold: Style
    IvorySolidBold: Style
    IvoryOutlineLight: Style
    IvorySolidLight: Style
    IvoryDashed: Style
    IvoryDashedBold: Style
    IvoryDashedLight: Style

    # Steel
    Steel: Style
    SteelBordered: Style
    SteelBold: Style
    SteelLight: Style
    SteelFlat: Style
    SteelOutline: Style
    SteelSolid: Style
    SteelOutlineBold: Style
    SteelSolidBold: Style
    SteelOutlineLight: Style
    SteelSolidLight: Style
    SteelDashed: Style
    SteelDashedBold: Style
    SteelDashedLight: Style

    # --- Google Brand Colors ---

    # GoogleBlue
    GoogleBlue: Style
    GoogleBlueBordered: Style
    GoogleBlueBold: Style
    GoogleBlueLight: Style
    GoogleBlueFlat: Style
    GoogleBlueOutline: Style
    GoogleBlueSolid: Style
    GoogleBlueOutlineBold: Style
    GoogleBlueSolidBold: Style
    GoogleBlueOutlineLight: Style
    GoogleBlueSolidLight: Style
    GoogleBlueDashed: Style
    GoogleBlueDashedBold: Style
    GoogleBlueDashedLight: Style

    # GoogleRed
    GoogleRed: Style
    GoogleRedBordered: Style
    GoogleRedBold: Style
    GoogleRedLight: Style
    GoogleRedFlat: Style
    GoogleRedOutline: Style
    GoogleRedSolid: Style
    GoogleRedOutlineBold: Style
    GoogleRedSolidBold: Style
    GoogleRedOutlineLight: Style
    GoogleRedSolidLight: Style
    GoogleRedDashed: Style
    GoogleRedDashedBold: Style
    GoogleRedDashedLight: Style

    # GoogleYellow
    GoogleYellow: Style
    GoogleYellowBordered: Style
    GoogleYellowBold: Style
    GoogleYellowLight: Style
    GoogleYellowFlat: Style
    GoogleYellowOutline: Style
    GoogleYellowSolid: Style
    GoogleYellowOutlineBold: Style
    GoogleYellowSolidBold: Style
    GoogleYellowOutlineLight: Style
    GoogleYellowSolidLight: Style
    GoogleYellowDashed: Style
    GoogleYellowDashedBold: Style
    GoogleYellowDashedLight: Style

    # GoogleGreen
    GoogleGreen: Style
    GoogleGreenBordered: Style
    GoogleGreenBold: Style
    GoogleGreenLight: Style
    GoogleGreenFlat: Style
    GoogleGreenOutline: Style
    GoogleGreenSolid: Style
    GoogleGreenOutlineBold: Style
    GoogleGreenSolidBold: Style
    GoogleGreenOutlineLight: Style
    GoogleGreenSolidLight: Style
    GoogleGreenDashed: Style
    GoogleGreenDashedBold: Style
    GoogleGreenDashedLight: Style

    # GoogleOrange
    GoogleOrange: Style
    GoogleOrangeBordered: Style
    GoogleOrangeBold: Style
    GoogleOrangeLight: Style
    GoogleOrangeFlat: Style
    GoogleOrangeOutline: Style
    GoogleOrangeSolid: Style
    GoogleOrangeOutlineBold: Style
    GoogleOrangeSolidBold: Style
    GoogleOrangeOutlineLight: Style
    GoogleOrangeSolidLight: Style
    GoogleOrangeDashed: Style
    GoogleOrangeDashedBold: Style
    GoogleOrangeDashedLight: Style

    # GooglePurple
    GooglePurple: Style
    GooglePurpleBordered: Style
    GooglePurpleBold: Style
    GooglePurpleLight: Style
    GooglePurpleFlat: Style
    GooglePurpleOutline: Style
    GooglePurpleSolid: Style
    GooglePurpleOutlineBold: Style
    GooglePurpleSolidBold: Style
    GooglePurpleOutlineLight: Style
    GooglePurpleSolidLight: Style
    GooglePurpleDashed: Style
    GooglePurpleDashedBold: Style
    GooglePurpleDashedLight: Style

    # GoogleGray
    GoogleGray: Style
    GoogleGrayBordered: Style
    GoogleGrayBold: Style
    GoogleGrayLight: Style
    GoogleGrayFlat: Style
    GoogleGrayOutline: Style
    GoogleGraySolid: Style
    GoogleGrayOutlineBold: Style
    GoogleGraySolidBold: Style
    GoogleGrayOutlineLight: Style
    GoogleGraySolidLight: Style
    GoogleGrayDashed: Style
    GoogleGrayDashedBold: Style
    GoogleGrayDashedLight: Style

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        super().__init__(**kwargs)

    def patch(
        self,
        *,
        Canvas: Style | None = None,
        CanvasFlat: Style | None = None,
        BackgroundColor: ColorType | None = None,
        Width: int | None = None,
        Height: int | None = None,
        Dpi: int | None = None,
        SourcecodeFont: FontSourceCode | None = None,
        Colors: BaseColors | None = None,
        Primary: Style | None = None,
        PrimaryBordered: Style | None = None,
        PrimaryBold: Style | None = None,
        PrimaryLight: Style | None = None,
        PrimaryFlat: Style | None = None,
        PrimaryOutline: Style | None = None,
        PrimaryOutlineBold: Style | None = None,
        PrimaryOutlineLight: Style | None = None,
        PrimaryDashed: Style | None = None,
        PrimaryDashedBold: Style | None = None,
        PrimaryDashedLight: Style | None = None,
        Secondary: Style | None = None,
        SecondaryBordered: Style | None = None,
        SecondaryBold: Style | None = None,
        SecondaryLight: Style | None = None,
        SecondaryFlat: Style | None = None,
        SecondaryOutline: Style | None = None,
        SecondaryOutlineBold: Style | None = None,
        SecondaryOutlineLight: Style | None = None,
        SecondaryDashed: Style | None = None,
        SecondaryDashedBold: Style | None = None,
        SecondaryDashedLight: Style | None = None,
        Accent: Style | None = None,
        AccentBordered: Style | None = None,
        AccentBold: Style | None = None,
        AccentLight: Style | None = None,
        AccentFlat: Style | None = None,
        AccentOutline: Style | None = None,
        AccentOutlineBold: Style | None = None,
        AccentOutlineLight: Style | None = None,
        AccentDashed: Style | None = None,
        AccentDashedBold: Style | None = None,
        AccentDashedLight: Style | None = None,
        Muted: Style | None = None,
        MutedBordered: Style | None = None,
        MutedBold: Style | None = None,
        MutedLight: Style | None = None,
        MutedFlat: Style | None = None,
        MutedOutline: Style | None = None,
        MutedOutlineBold: Style | None = None,
        MutedOutlineLight: Style | None = None,
        MutedDashed: Style | None = None,
        MutedDashedBold: Style | None = None,
        MutedDashedLight: Style | None = None,
        Light: Style | None = None,
        LightBordered: Style | None = None,
        LightBold: Style | None = None,
        LightLight: Style | None = None,
        LightFlat: Style | None = None,
        LightOutline: Style | None = None,
        LightOutlineBold: Style | None = None,
        LightOutlineLight: Style | None = None,
        LightDashed: Style | None = None,
        LightDashedBold: Style | None = None,
        LightDashedLight: Style | None = None,
        Dark: Style | None = None,
        DarkBordered: Style | None = None,
        DarkBold: Style | None = None,
        DarkLight: Style | None = None,
        DarkFlat: Style | None = None,
        DarkOutline: Style | None = None,
        DarkOutlineBold: Style | None = None,
        DarkOutlineLight: Style | None = None,
        DarkDashed: Style | None = None,
        DarkDashedBold: Style | None = None,
        DarkDashedLight: Style | None = None,
        Danger: Style | None = None,
        DangerBordered: Style | None = None,
        DangerBold: Style | None = None,
        DangerLight: Style | None = None,
        DangerFlat: Style | None = None,
        DangerOutline: Style | None = None,
        DangerOutlineBold: Style | None = None,
        DangerOutlineLight: Style | None = None,
        DangerDashed: Style | None = None,
        DangerDashedBold: Style | None = None,
        DangerDashedLight: Style | None = None,
        Success: Style | None = None,
        SuccessBordered: Style | None = None,
        SuccessBold: Style | None = None,
        SuccessLight: Style | None = None,
        SuccessFlat: Style | None = None,
        SuccessOutline: Style | None = None,
        SuccessOutlineBold: Style | None = None,
        SuccessOutlineLight: Style | None = None,
        SuccessDashed: Style | None = None,
        SuccessDashedBold: Style | None = None,
        SuccessDashedLight: Style | None = None,
        Primary1: Style | None = None,
        Primary1Bordered: Style | None = None,
        Primary1Bold: Style | None = None,
        Primary1Light: Style | None = None,
        Primary1Flat: Style | None = None,
        Primary1Outline: Style | None = None,
        Primary1Solid: Style | None = None,
        Primary1OutlineBold: Style | None = None,
        Primary1SolidBold: Style | None = None,
        Primary1OutlineLight: Style | None = None,
        Primary1SolidLight: Style | None = None,
        Primary1Dashed: Style | None = None,
        Primary1DashedBold: Style | None = None,
        Primary1DashedLight: Style | None = None,
        Primary2: Style | None = None,
        Primary2Bordered: Style | None = None,
        Primary2Bold: Style | None = None,
        Primary2Light: Style | None = None,
        Primary2Flat: Style | None = None,
        Primary2Outline: Style | None = None,
        Primary2Solid: Style | None = None,
        Primary2OutlineBold: Style | None = None,
        Primary2SolidBold: Style | None = None,
        Primary2OutlineLight: Style | None = None,
        Primary2SolidLight: Style | None = None,
        Primary2Dashed: Style | None = None,
        Primary2DashedBold: Style | None = None,
        Primary2DashedLight: Style | None = None,
        Primary3: Style | None = None,
        Primary3Bordered: Style | None = None,
        Primary3Bold: Style | None = None,
        Primary3Light: Style | None = None,
        Primary3Flat: Style | None = None,
        Primary3Outline: Style | None = None,
        Primary3Solid: Style | None = None,
        Primary3OutlineBold: Style | None = None,
        Primary3SolidBold: Style | None = None,
        Primary3OutlineLight: Style | None = None,
        Primary3SolidLight: Style | None = None,
        Primary3Dashed: Style | None = None,
        Primary3DashedBold: Style | None = None,
        Primary3DashedLight: Style | None = None,
        Primary4: Style | None = None,
        Primary4Bordered: Style | None = None,
        Primary4Bold: Style | None = None,
        Primary4Light: Style | None = None,
        Primary4Flat: Style | None = None,
        Primary4Outline: Style | None = None,
        Primary4Solid: Style | None = None,
        Primary4OutlineBold: Style | None = None,
        Primary4SolidBold: Style | None = None,
        Primary4OutlineLight: Style | None = None,
        Primary4SolidLight: Style | None = None,
        Primary4Dashed: Style | None = None,
        Primary4DashedBold: Style | None = None,
        Primary4DashedLight: Style | None = None,
        Primary5: Style | None = None,
        Primary5Bordered: Style | None = None,
        Primary5Bold: Style | None = None,
        Primary5Light: Style | None = None,
        Primary5Flat: Style | None = None,
        Primary5Outline: Style | None = None,
        Primary5Solid: Style | None = None,
        Primary5OutlineBold: Style | None = None,
        Primary5SolidBold: Style | None = None,
        Primary5OutlineLight: Style | None = None,
        Primary5SolidLight: Style | None = None,
        Primary5Dashed: Style | None = None,
        Primary5DashedBold: Style | None = None,
        Primary5DashedLight: Style | None = None,
        Primary6: Style | None = None,
        Primary6Bordered: Style | None = None,
        Primary6Bold: Style | None = None,
        Primary6Light: Style | None = None,
        Primary6Flat: Style | None = None,
        Primary6Outline: Style | None = None,
        Primary6Solid: Style | None = None,
        Primary6OutlineBold: Style | None = None,
        Primary6SolidBold: Style | None = None,
        Primary6OutlineLight: Style | None = None,
        Primary6SolidLight: Style | None = None,
        Primary6Dashed: Style | None = None,
        Primary6DashedBold: Style | None = None,
        Primary6DashedLight: Style | None = None,
        Secondary1: Style | None = None,
        Secondary1Bordered: Style | None = None,
        Secondary1Bold: Style | None = None,
        Secondary1Light: Style | None = None,
        Secondary1Flat: Style | None = None,
        Secondary1Outline: Style | None = None,
        Secondary1Solid: Style | None = None,
        Secondary1OutlineBold: Style | None = None,
        Secondary1SolidBold: Style | None = None,
        Secondary1OutlineLight: Style | None = None,
        Secondary1SolidLight: Style | None = None,
        Secondary1Dashed: Style | None = None,
        Secondary1DashedBold: Style | None = None,
        Secondary1DashedLight: Style | None = None,
        Secondary2: Style | None = None,
        Secondary2Bordered: Style | None = None,
        Secondary2Bold: Style | None = None,
        Secondary2Light: Style | None = None,
        Secondary2Flat: Style | None = None,
        Secondary2Outline: Style | None = None,
        Secondary2Solid: Style | None = None,
        Secondary2OutlineBold: Style | None = None,
        Secondary2SolidBold: Style | None = None,
        Secondary2OutlineLight: Style | None = None,
        Secondary2SolidLight: Style | None = None,
        Secondary2Dashed: Style | None = None,
        Secondary2DashedBold: Style | None = None,
        Secondary2DashedLight: Style | None = None,
        Secondary3: Style | None = None,
        Secondary3Bordered: Style | None = None,
        Secondary3Bold: Style | None = None,
        Secondary3Light: Style | None = None,
        Secondary3Flat: Style | None = None,
        Secondary3Outline: Style | None = None,
        Secondary3Solid: Style | None = None,
        Secondary3OutlineBold: Style | None = None,
        Secondary3SolidBold: Style | None = None,
        Secondary3OutlineLight: Style | None = None,
        Secondary3SolidLight: Style | None = None,
        Secondary3Dashed: Style | None = None,
        Secondary3DashedBold: Style | None = None,
        Secondary3DashedLight: Style | None = None,
        Secondary4: Style | None = None,
        Secondary4Bordered: Style | None = None,
        Secondary4Bold: Style | None = None,
        Secondary4Light: Style | None = None,
        Secondary4Flat: Style | None = None,
        Secondary4Outline: Style | None = None,
        Secondary4Solid: Style | None = None,
        Secondary4OutlineBold: Style | None = None,
        Secondary4SolidBold: Style | None = None,
        Secondary4OutlineLight: Style | None = None,
        Secondary4SolidLight: Style | None = None,
        Secondary4Dashed: Style | None = None,
        Secondary4DashedBold: Style | None = None,
        Secondary4DashedLight: Style | None = None,
        Secondary5: Style | None = None,
        Secondary5Bordered: Style | None = None,
        Secondary5Bold: Style | None = None,
        Secondary5Light: Style | None = None,
        Secondary5Flat: Style | None = None,
        Secondary5Outline: Style | None = None,
        Secondary5Solid: Style | None = None,
        Secondary5OutlineBold: Style | None = None,
        Secondary5SolidBold: Style | None = None,
        Secondary5OutlineLight: Style | None = None,
        Secondary5SolidLight: Style | None = None,
        Secondary5Dashed: Style | None = None,
        Secondary5DashedBold: Style | None = None,
        Secondary5DashedLight: Style | None = None,
        Secondary6: Style | None = None,
        Secondary6Bordered: Style | None = None,
        Secondary6Bold: Style | None = None,
        Secondary6Light: Style | None = None,
        Secondary6Flat: Style | None = None,
        Secondary6Outline: Style | None = None,
        Secondary6Solid: Style | None = None,
        Secondary6OutlineBold: Style | None = None,
        Secondary6SolidBold: Style | None = None,
        Secondary6OutlineLight: Style | None = None,
        Secondary6SolidLight: Style | None = None,
        Secondary6Dashed: Style | None = None,
        Secondary6DashedBold: Style | None = None,
        Secondary6DashedLight: Style | None = None,
        Accent1: Style | None = None,
        Accent1Bordered: Style | None = None,
        Accent1Bold: Style | None = None,
        Accent1Light: Style | None = None,
        Accent1Flat: Style | None = None,
        Accent1Outline: Style | None = None,
        Accent1Solid: Style | None = None,
        Accent1OutlineBold: Style | None = None,
        Accent1SolidBold: Style | None = None,
        Accent1OutlineLight: Style | None = None,
        Accent1SolidLight: Style | None = None,
        Accent1Dashed: Style | None = None,
        Accent1DashedBold: Style | None = None,
        Accent1DashedLight: Style | None = None,
        Accent2: Style | None = None,
        Accent2Bordered: Style | None = None,
        Accent2Bold: Style | None = None,
        Accent2Light: Style | None = None,
        Accent2Flat: Style | None = None,
        Accent2Outline: Style | None = None,
        Accent2Solid: Style | None = None,
        Accent2OutlineBold: Style | None = None,
        Accent2SolidBold: Style | None = None,
        Accent2OutlineLight: Style | None = None,
        Accent2SolidLight: Style | None = None,
        Accent2Dashed: Style | None = None,
        Accent2DashedBold: Style | None = None,
        Accent2DashedLight: Style | None = None,
        Accent3: Style | None = None,
        Accent3Bordered: Style | None = None,
        Accent3Bold: Style | None = None,
        Accent3Light: Style | None = None,
        Accent3Flat: Style | None = None,
        Accent3Outline: Style | None = None,
        Accent3Solid: Style | None = None,
        Accent3OutlineBold: Style | None = None,
        Accent3SolidBold: Style | None = None,
        Accent3OutlineLight: Style | None = None,
        Accent3SolidLight: Style | None = None,
        Accent3Dashed: Style | None = None,
        Accent3DashedBold: Style | None = None,
        Accent3DashedLight: Style | None = None,
        Accent4: Style | None = None,
        Accent4Bordered: Style | None = None,
        Accent4Bold: Style | None = None,
        Accent4Light: Style | None = None,
        Accent4Flat: Style | None = None,
        Accent4Outline: Style | None = None,
        Accent4Solid: Style | None = None,
        Accent4OutlineBold: Style | None = None,
        Accent4SolidBold: Style | None = None,
        Accent4OutlineLight: Style | None = None,
        Accent4SolidLight: Style | None = None,
        Accent4Dashed: Style | None = None,
        Accent4DashedBold: Style | None = None,
        Accent4DashedLight: Style | None = None,
        Accent5: Style | None = None,
        Accent5Bordered: Style | None = None,
        Accent5Bold: Style | None = None,
        Accent5Light: Style | None = None,
        Accent5Flat: Style | None = None,
        Accent5Outline: Style | None = None,
        Accent5Solid: Style | None = None,
        Accent5OutlineBold: Style | None = None,
        Accent5SolidBold: Style | None = None,
        Accent5OutlineLight: Style | None = None,
        Accent5SolidLight: Style | None = None,
        Accent5Dashed: Style | None = None,
        Accent5DashedBold: Style | None = None,
        Accent5DashedLight: Style | None = None,
        Accent6: Style | None = None,
        Accent6Bordered: Style | None = None,
        Accent6Bold: Style | None = None,
        Accent6Light: Style | None = None,
        Accent6Flat: Style | None = None,
        Accent6Outline: Style | None = None,
        Accent6Solid: Style | None = None,
        Accent6OutlineBold: Style | None = None,
        Accent6SolidBold: Style | None = None,
        Accent6OutlineLight: Style | None = None,
        Accent6SolidLight: Style | None = None,
        Accent6Dashed: Style | None = None,
        Accent6DashedBold: Style | None = None,
        Accent6DashedLight: Style | None = None,
        Muted1: Style | None = None,
        Muted1Bordered: Style | None = None,
        Muted1Bold: Style | None = None,
        Muted1Light: Style | None = None,
        Muted1Flat: Style | None = None,
        Muted1Outline: Style | None = None,
        Muted1Solid: Style | None = None,
        Muted1OutlineBold: Style | None = None,
        Muted1SolidBold: Style | None = None,
        Muted1OutlineLight: Style | None = None,
        Muted1SolidLight: Style | None = None,
        Muted1Dashed: Style | None = None,
        Muted1DashedBold: Style | None = None,
        Muted1DashedLight: Style | None = None,
        Muted2: Style | None = None,
        Muted2Bordered: Style | None = None,
        Muted2Bold: Style | None = None,
        Muted2Light: Style | None = None,
        Muted2Flat: Style | None = None,
        Muted2Outline: Style | None = None,
        Muted2Solid: Style | None = None,
        Muted2OutlineBold: Style | None = None,
        Muted2SolidBold: Style | None = None,
        Muted2OutlineLight: Style | None = None,
        Muted2SolidLight: Style | None = None,
        Muted2Dashed: Style | None = None,
        Muted2DashedBold: Style | None = None,
        Muted2DashedLight: Style | None = None,
        Muted3: Style | None = None,
        Muted3Bordered: Style | None = None,
        Muted3Bold: Style | None = None,
        Muted3Light: Style | None = None,
        Muted3Flat: Style | None = None,
        Muted3Outline: Style | None = None,
        Muted3Solid: Style | None = None,
        Muted3OutlineBold: Style | None = None,
        Muted3SolidBold: Style | None = None,
        Muted3OutlineLight: Style | None = None,
        Muted3SolidLight: Style | None = None,
        Muted3Dashed: Style | None = None,
        Muted3DashedBold: Style | None = None,
        Muted3DashedLight: Style | None = None,
        Muted4: Style | None = None,
        Muted4Bordered: Style | None = None,
        Muted4Bold: Style | None = None,
        Muted4Light: Style | None = None,
        Muted4Flat: Style | None = None,
        Muted4Outline: Style | None = None,
        Muted4Solid: Style | None = None,
        Muted4OutlineBold: Style | None = None,
        Muted4SolidBold: Style | None = None,
        Muted4OutlineLight: Style | None = None,
        Muted4SolidLight: Style | None = None,
        Muted4Dashed: Style | None = None,
        Muted4DashedBold: Style | None = None,
        Muted4DashedLight: Style | None = None,
        Muted5: Style | None = None,
        Muted5Bordered: Style | None = None,
        Muted5Bold: Style | None = None,
        Muted5Light: Style | None = None,
        Muted5Flat: Style | None = None,
        Muted5Outline: Style | None = None,
        Muted5Solid: Style | None = None,
        Muted5OutlineBold: Style | None = None,
        Muted5SolidBold: Style | None = None,
        Muted5OutlineLight: Style | None = None,
        Muted5SolidLight: Style | None = None,
        Muted5Dashed: Style | None = None,
        Muted5DashedBold: Style | None = None,
        Muted5DashedLight: Style | None = None,
        Muted6: Style | None = None,
        Muted6Bordered: Style | None = None,
        Muted6Bold: Style | None = None,
        Muted6Light: Style | None = None,
        Muted6Flat: Style | None = None,
        Muted6Outline: Style | None = None,
        Muted6Solid: Style | None = None,
        Muted6OutlineBold: Style | None = None,
        Muted6SolidBold: Style | None = None,
        Muted6OutlineLight: Style | None = None,
        Muted6SolidLight: Style | None = None,
        Muted6Dashed: Style | None = None,
        Muted6DashedBold: Style | None = None,
        Muted6DashedLight: Style | None = None,
        Danger1: Style | None = None,
        Danger1Bordered: Style | None = None,
        Danger1Bold: Style | None = None,
        Danger1Light: Style | None = None,
        Danger1Flat: Style | None = None,
        Danger1Outline: Style | None = None,
        Danger1Solid: Style | None = None,
        Danger1OutlineBold: Style | None = None,
        Danger1SolidBold: Style | None = None,
        Danger1OutlineLight: Style | None = None,
        Danger1SolidLight: Style | None = None,
        Danger1Dashed: Style | None = None,
        Danger1DashedBold: Style | None = None,
        Danger1DashedLight: Style | None = None,
        Danger2: Style | None = None,
        Danger2Bordered: Style | None = None,
        Danger2Bold: Style | None = None,
        Danger2Light: Style | None = None,
        Danger2Flat: Style | None = None,
        Danger2Outline: Style | None = None,
        Danger2Solid: Style | None = None,
        Danger2OutlineBold: Style | None = None,
        Danger2SolidBold: Style | None = None,
        Danger2OutlineLight: Style | None = None,
        Danger2SolidLight: Style | None = None,
        Danger2Dashed: Style | None = None,
        Danger2DashedBold: Style | None = None,
        Danger2DashedLight: Style | None = None,
        Danger3: Style | None = None,
        Danger3Bordered: Style | None = None,
        Danger3Bold: Style | None = None,
        Danger3Light: Style | None = None,
        Danger3Flat: Style | None = None,
        Danger3Outline: Style | None = None,
        Danger3Solid: Style | None = None,
        Danger3OutlineBold: Style | None = None,
        Danger3SolidBold: Style | None = None,
        Danger3OutlineLight: Style | None = None,
        Danger3SolidLight: Style | None = None,
        Danger3Dashed: Style | None = None,
        Danger3DashedBold: Style | None = None,
        Danger3DashedLight: Style | None = None,
        Danger4: Style | None = None,
        Danger4Bordered: Style | None = None,
        Danger4Bold: Style | None = None,
        Danger4Light: Style | None = None,
        Danger4Flat: Style | None = None,
        Danger4Outline: Style | None = None,
        Danger4Solid: Style | None = None,
        Danger4OutlineBold: Style | None = None,
        Danger4SolidBold: Style | None = None,
        Danger4OutlineLight: Style | None = None,
        Danger4SolidLight: Style | None = None,
        Danger4Dashed: Style | None = None,
        Danger4DashedBold: Style | None = None,
        Danger4DashedLight: Style | None = None,
        Danger5: Style | None = None,
        Danger5Bordered: Style | None = None,
        Danger5Bold: Style | None = None,
        Danger5Light: Style | None = None,
        Danger5Flat: Style | None = None,
        Danger5Outline: Style | None = None,
        Danger5Solid: Style | None = None,
        Danger5OutlineBold: Style | None = None,
        Danger5SolidBold: Style | None = None,
        Danger5OutlineLight: Style | None = None,
        Danger5SolidLight: Style | None = None,
        Danger5Dashed: Style | None = None,
        Danger5DashedBold: Style | None = None,
        Danger5DashedLight: Style | None = None,
        Danger6: Style | None = None,
        Danger6Bordered: Style | None = None,
        Danger6Bold: Style | None = None,
        Danger6Light: Style | None = None,
        Danger6Flat: Style | None = None,
        Danger6Outline: Style | None = None,
        Danger6Solid: Style | None = None,
        Danger6OutlineBold: Style | None = None,
        Danger6SolidBold: Style | None = None,
        Danger6OutlineLight: Style | None = None,
        Danger6SolidLight: Style | None = None,
        Danger6Dashed: Style | None = None,
        Danger6DashedBold: Style | None = None,
        Danger6DashedLight: Style | None = None,
        Success1: Style | None = None,
        Success1Bordered: Style | None = None,
        Success1Bold: Style | None = None,
        Success1Light: Style | None = None,
        Success1Flat: Style | None = None,
        Success1Outline: Style | None = None,
        Success1Solid: Style | None = None,
        Success1OutlineBold: Style | None = None,
        Success1SolidBold: Style | None = None,
        Success1OutlineLight: Style | None = None,
        Success1SolidLight: Style | None = None,
        Success1Dashed: Style | None = None,
        Success1DashedBold: Style | None = None,
        Success1DashedLight: Style | None = None,
        Success2: Style | None = None,
        Success2Bordered: Style | None = None,
        Success2Bold: Style | None = None,
        Success2Light: Style | None = None,
        Success2Flat: Style | None = None,
        Success2Outline: Style | None = None,
        Success2Solid: Style | None = None,
        Success2OutlineBold: Style | None = None,
        Success2SolidBold: Style | None = None,
        Success2OutlineLight: Style | None = None,
        Success2SolidLight: Style | None = None,
        Success2Dashed: Style | None = None,
        Success2DashedBold: Style | None = None,
        Success2DashedLight: Style | None = None,
        Success3: Style | None = None,
        Success3Bordered: Style | None = None,
        Success3Bold: Style | None = None,
        Success3Light: Style | None = None,
        Success3Flat: Style | None = None,
        Success3Outline: Style | None = None,
        Success3Solid: Style | None = None,
        Success3OutlineBold: Style | None = None,
        Success3SolidBold: Style | None = None,
        Success3OutlineLight: Style | None = None,
        Success3SolidLight: Style | None = None,
        Success3Dashed: Style | None = None,
        Success3DashedBold: Style | None = None,
        Success3DashedLight: Style | None = None,
        Success4: Style | None = None,
        Success4Bordered: Style | None = None,
        Success4Bold: Style | None = None,
        Success4Light: Style | None = None,
        Success4Flat: Style | None = None,
        Success4Outline: Style | None = None,
        Success4Solid: Style | None = None,
        Success4OutlineBold: Style | None = None,
        Success4SolidBold: Style | None = None,
        Success4OutlineLight: Style | None = None,
        Success4SolidLight: Style | None = None,
        Success4Dashed: Style | None = None,
        Success4DashedBold: Style | None = None,
        Success4DashedLight: Style | None = None,
        Success5: Style | None = None,
        Success5Bordered: Style | None = None,
        Success5Bold: Style | None = None,
        Success5Light: Style | None = None,
        Success5Flat: Style | None = None,
        Success5Outline: Style | None = None,
        Success5Solid: Style | None = None,
        Success5OutlineBold: Style | None = None,
        Success5SolidBold: Style | None = None,
        Success5OutlineLight: Style | None = None,
        Success5SolidLight: Style | None = None,
        Success5Dashed: Style | None = None,
        Success5DashedBold: Style | None = None,
        Success5DashedLight: Style | None = None,
        Success6: Style | None = None,
        Success6Bordered: Style | None = None,
        Success6Bold: Style | None = None,
        Success6Light: Style | None = None,
        Success6Flat: Style | None = None,
        Success6Outline: Style | None = None,
        Success6Solid: Style | None = None,
        Success6OutlineBold: Style | None = None,
        Success6SolidBold: Style | None = None,
        Success6OutlineLight: Style | None = None,
        Success6SolidLight: Style | None = None,
        Success6Dashed: Style | None = None,
        Success6DashedBold: Style | None = None,
        Success6DashedLight: Style | None = None,
        PrimarySolid: Style | None = None,
        PrimarySolidBold: Style | None = None,
        PrimarySolidLight: Style | None = None,
        SecondarySolid: Style | None = None,
        SecondarySolidBold: Style | None = None,
        SecondarySolidLight: Style | None = None,
        AccentSolid: Style | None = None,
        AccentSolidBold: Style | None = None,
        AccentSolidLight: Style | None = None,
        MutedSolid: Style | None = None,
        MutedSolidBold: Style | None = None,
        MutedSolidLight: Style | None = None,
        LightSolid: Style | None = None,
        LightSolidBold: Style | None = None,
        LightSolidLight: Style | None = None,
        DarkSolid: Style | None = None,
        DarkSolidBold: Style | None = None,
        DarkSolidLight: Style | None = None,
        DangerSolid: Style | None = None,
        DangerSolidBold: Style | None = None,
        DangerSolidLight: Style | None = None,
        SuccessSolid: Style | None = None,
        SuccessSolidBold: Style | None = None,
        SuccessSolidLight: Style | None = None,
        White: Style | None = None,
        WhiteBordered: Style | None = None,
        WhiteBold: Style | None = None,
        WhiteLight: Style | None = None,
        WhiteFlat: Style | None = None,
        WhiteOutline: Style | None = None,
        WhiteSolid: Style | None = None,
        WhiteOutlineBold: Style | None = None,
        WhiteSolidBold: Style | None = None,
        WhiteOutlineLight: Style | None = None,
        WhiteSolidLight: Style | None = None,
        WhiteDashed: Style | None = None,
        WhiteDashedBold: Style | None = None,
        WhiteDashedLight: Style | None = None,
        Gray1: Style | None = None,
        Gray1Bordered: Style | None = None,
        Gray1Bold: Style | None = None,
        Gray1Light: Style | None = None,
        Gray1Flat: Style | None = None,
        Gray1Outline: Style | None = None,
        Gray1Solid: Style | None = None,
        Gray1OutlineBold: Style | None = None,
        Gray1SolidBold: Style | None = None,
        Gray1OutlineLight: Style | None = None,
        Gray1SolidLight: Style | None = None,
        Gray1Dashed: Style | None = None,
        Gray1DashedBold: Style | None = None,
        Gray1DashedLight: Style | None = None,
        Gray2: Style | None = None,
        Gray2Bordered: Style | None = None,
        Gray2Bold: Style | None = None,
        Gray2Light: Style | None = None,
        Gray2Flat: Style | None = None,
        Gray2Outline: Style | None = None,
        Gray2Solid: Style | None = None,
        Gray2OutlineBold: Style | None = None,
        Gray2SolidBold: Style | None = None,
        Gray2OutlineLight: Style | None = None,
        Gray2SolidLight: Style | None = None,
        Gray2Dashed: Style | None = None,
        Gray2DashedBold: Style | None = None,
        Gray2DashedLight: Style | None = None,
        Gray3: Style | None = None,
        Gray3Bordered: Style | None = None,
        Gray3Bold: Style | None = None,
        Gray3Light: Style | None = None,
        Gray3Flat: Style | None = None,
        Gray3Outline: Style | None = None,
        Gray3Solid: Style | None = None,
        Gray3OutlineBold: Style | None = None,
        Gray3SolidBold: Style | None = None,
        Gray3OutlineLight: Style | None = None,
        Gray3SolidLight: Style | None = None,
        Gray3Dashed: Style | None = None,
        Gray3DashedBold: Style | None = None,
        Gray3DashedLight: Style | None = None,
        Gray4: Style | None = None,
        Gray4Bordered: Style | None = None,
        Gray4Bold: Style | None = None,
        Gray4Light: Style | None = None,
        Gray4Flat: Style | None = None,
        Gray4Outline: Style | None = None,
        Gray4Solid: Style | None = None,
        Gray4OutlineBold: Style | None = None,
        Gray4SolidBold: Style | None = None,
        Gray4OutlineLight: Style | None = None,
        Gray4SolidLight: Style | None = None,
        Gray4Dashed: Style | None = None,
        Gray4DashedBold: Style | None = None,
        Gray4DashedLight: Style | None = None,
        Gray5: Style | None = None,
        Gray5Bordered: Style | None = None,
        Gray5Bold: Style | None = None,
        Gray5Light: Style | None = None,
        Gray5Flat: Style | None = None,
        Gray5Outline: Style | None = None,
        Gray5Solid: Style | None = None,
        Gray5OutlineBold: Style | None = None,
        Gray5SolidBold: Style | None = None,
        Gray5OutlineLight: Style | None = None,
        Gray5SolidLight: Style | None = None,
        Gray5Dashed: Style | None = None,
        Gray5DashedBold: Style | None = None,
        Gray5DashedLight: Style | None = None,
        Gray6: Style | None = None,
        Gray6Bordered: Style | None = None,
        Gray6Bold: Style | None = None,
        Gray6Light: Style | None = None,
        Gray6Flat: Style | None = None,
        Gray6Outline: Style | None = None,
        Gray6Solid: Style | None = None,
        Gray6OutlineBold: Style | None = None,
        Gray6SolidBold: Style | None = None,
        Gray6OutlineLight: Style | None = None,
        Gray6SolidLight: Style | None = None,
        Gray6Dashed: Style | None = None,
        Gray6DashedBold: Style | None = None,
        Gray6DashedLight: Style | None = None,
        Gray7: Style | None = None,
        Gray7Bordered: Style | None = None,
        Gray7Bold: Style | None = None,
        Gray7Light: Style | None = None,
        Gray7Flat: Style | None = None,
        Gray7Outline: Style | None = None,
        Gray7Solid: Style | None = None,
        Gray7OutlineBold: Style | None = None,
        Gray7SolidBold: Style | None = None,
        Gray7OutlineLight: Style | None = None,
        Gray7SolidLight: Style | None = None,
        Gray7Dashed: Style | None = None,
        Gray7DashedBold: Style | None = None,
        Gray7DashedLight: Style | None = None,
        Gray8: Style | None = None,
        Gray8Bordered: Style | None = None,
        Gray8Bold: Style | None = None,
        Gray8Light: Style | None = None,
        Gray8Flat: Style | None = None,
        Gray8Outline: Style | None = None,
        Gray8Solid: Style | None = None,
        Gray8OutlineBold: Style | None = None,
        Gray8SolidBold: Style | None = None,
        Gray8OutlineLight: Style | None = None,
        Gray8SolidLight: Style | None = None,
        Gray8Dashed: Style | None = None,
        Gray8DashedBold: Style | None = None,
        Gray8DashedLight: Style | None = None,
        Black: Style | None = None,
        BlackBordered: Style | None = None,
        BlackBold: Style | None = None,
        BlackLight: Style | None = None,
        BlackFlat: Style | None = None,
        BlackOutline: Style | None = None,
        BlackSolid: Style | None = None,
        BlackOutlineBold: Style | None = None,
        BlackSolidBold: Style | None = None,
        BlackOutlineLight: Style | None = None,
        BlackSolidLight: Style | None = None,
        BlackDashed: Style | None = None,
        BlackDashedBold: Style | None = None,
        BlackDashedLight: Style | None = None,
        CornflowerBlue1: Style | None = None,
        CornflowerBlue1Bordered: Style | None = None,
        CornflowerBlue1Bold: Style | None = None,
        CornflowerBlue1Light: Style | None = None,
        CornflowerBlue1Flat: Style | None = None,
        CornflowerBlue1Outline: Style | None = None,
        CornflowerBlue1Solid: Style | None = None,
        CornflowerBlue1OutlineBold: Style | None = None,
        CornflowerBlue1SolidBold: Style | None = None,
        CornflowerBlue1OutlineLight: Style | None = None,
        CornflowerBlue1SolidLight: Style | None = None,
        CornflowerBlue1Dashed: Style | None = None,
        CornflowerBlue1DashedBold: Style | None = None,
        CornflowerBlue1DashedLight: Style | None = None,
        CornflowerBlue2: Style | None = None,
        CornflowerBlue2Bordered: Style | None = None,
        CornflowerBlue2Bold: Style | None = None,
        CornflowerBlue2Light: Style | None = None,
        CornflowerBlue2Flat: Style | None = None,
        CornflowerBlue2Outline: Style | None = None,
        CornflowerBlue2Solid: Style | None = None,
        CornflowerBlue2OutlineBold: Style | None = None,
        CornflowerBlue2SolidBold: Style | None = None,
        CornflowerBlue2OutlineLight: Style | None = None,
        CornflowerBlue2SolidLight: Style | None = None,
        CornflowerBlue2Dashed: Style | None = None,
        CornflowerBlue2DashedBold: Style | None = None,
        CornflowerBlue2DashedLight: Style | None = None,
        CornflowerBlue3: Style | None = None,
        CornflowerBlue3Bordered: Style | None = None,
        CornflowerBlue3Bold: Style | None = None,
        CornflowerBlue3Light: Style | None = None,
        CornflowerBlue3Flat: Style | None = None,
        CornflowerBlue3Outline: Style | None = None,
        CornflowerBlue3Solid: Style | None = None,
        CornflowerBlue3OutlineBold: Style | None = None,
        CornflowerBlue3SolidBold: Style | None = None,
        CornflowerBlue3OutlineLight: Style | None = None,
        CornflowerBlue3SolidLight: Style | None = None,
        CornflowerBlue3Dashed: Style | None = None,
        CornflowerBlue3DashedBold: Style | None = None,
        CornflowerBlue3DashedLight: Style | None = None,
        CornflowerBlue4: Style | None = None,
        CornflowerBlue4Bordered: Style | None = None,
        CornflowerBlue4Bold: Style | None = None,
        CornflowerBlue4Light: Style | None = None,
        CornflowerBlue4Flat: Style | None = None,
        CornflowerBlue4Outline: Style | None = None,
        CornflowerBlue4Solid: Style | None = None,
        CornflowerBlue4OutlineBold: Style | None = None,
        CornflowerBlue4SolidBold: Style | None = None,
        CornflowerBlue4OutlineLight: Style | None = None,
        CornflowerBlue4SolidLight: Style | None = None,
        CornflowerBlue4Dashed: Style | None = None,
        CornflowerBlue4DashedBold: Style | None = None,
        CornflowerBlue4DashedLight: Style | None = None,
        CornflowerBlue5: Style | None = None,
        CornflowerBlue5Bordered: Style | None = None,
        CornflowerBlue5Bold: Style | None = None,
        CornflowerBlue5Light: Style | None = None,
        CornflowerBlue5Flat: Style | None = None,
        CornflowerBlue5Outline: Style | None = None,
        CornflowerBlue5Solid: Style | None = None,
        CornflowerBlue5OutlineBold: Style | None = None,
        CornflowerBlue5SolidBold: Style | None = None,
        CornflowerBlue5OutlineLight: Style | None = None,
        CornflowerBlue5SolidLight: Style | None = None,
        CornflowerBlue5Dashed: Style | None = None,
        CornflowerBlue5DashedBold: Style | None = None,
        CornflowerBlue5DashedLight: Style | None = None,
        CornflowerBlue6: Style | None = None,
        CornflowerBlue6Bordered: Style | None = None,
        CornflowerBlue6Bold: Style | None = None,
        CornflowerBlue6Light: Style | None = None,
        CornflowerBlue6Flat: Style | None = None,
        CornflowerBlue6Outline: Style | None = None,
        CornflowerBlue6Solid: Style | None = None,
        CornflowerBlue6OutlineBold: Style | None = None,
        CornflowerBlue6SolidBold: Style | None = None,
        CornflowerBlue6OutlineLight: Style | None = None,
        CornflowerBlue6SolidLight: Style | None = None,
        CornflowerBlue6Dashed: Style | None = None,
        CornflowerBlue6DashedBold: Style | None = None,
        CornflowerBlue6DashedLight: Style | None = None,
        Blue1: Style | None = None,
        Blue1Bordered: Style | None = None,
        Blue1Bold: Style | None = None,
        Blue1Light: Style | None = None,
        Blue1Flat: Style | None = None,
        Blue1Outline: Style | None = None,
        Blue1Solid: Style | None = None,
        Blue1OutlineBold: Style | None = None,
        Blue1SolidBold: Style | None = None,
        Blue1OutlineLight: Style | None = None,
        Blue1SolidLight: Style | None = None,
        Blue1Dashed: Style | None = None,
        Blue1DashedBold: Style | None = None,
        Blue1DashedLight: Style | None = None,
        Blue2: Style | None = None,
        Blue2Bordered: Style | None = None,
        Blue2Bold: Style | None = None,
        Blue2Light: Style | None = None,
        Blue2Flat: Style | None = None,
        Blue2Outline: Style | None = None,
        Blue2Solid: Style | None = None,
        Blue2OutlineBold: Style | None = None,
        Blue2SolidBold: Style | None = None,
        Blue2OutlineLight: Style | None = None,
        Blue2SolidLight: Style | None = None,
        Blue2Dashed: Style | None = None,
        Blue2DashedBold: Style | None = None,
        Blue2DashedLight: Style | None = None,
        Blue3: Style | None = None,
        Blue3Bordered: Style | None = None,
        Blue3Bold: Style | None = None,
        Blue3Light: Style | None = None,
        Blue3Flat: Style | None = None,
        Blue3Outline: Style | None = None,
        Blue3Solid: Style | None = None,
        Blue3OutlineBold: Style | None = None,
        Blue3SolidBold: Style | None = None,
        Blue3OutlineLight: Style | None = None,
        Blue3SolidLight: Style | None = None,
        Blue3Dashed: Style | None = None,
        Blue3DashedBold: Style | None = None,
        Blue3DashedLight: Style | None = None,
        Blue4: Style | None = None,
        Blue4Bordered: Style | None = None,
        Blue4Bold: Style | None = None,
        Blue4Light: Style | None = None,
        Blue4Flat: Style | None = None,
        Blue4Outline: Style | None = None,
        Blue4Solid: Style | None = None,
        Blue4OutlineBold: Style | None = None,
        Blue4SolidBold: Style | None = None,
        Blue4OutlineLight: Style | None = None,
        Blue4SolidLight: Style | None = None,
        Blue4Dashed: Style | None = None,
        Blue4DashedBold: Style | None = None,
        Blue4DashedLight: Style | None = None,
        Blue5: Style | None = None,
        Blue5Bordered: Style | None = None,
        Blue5Bold: Style | None = None,
        Blue5Light: Style | None = None,
        Blue5Flat: Style | None = None,
        Blue5Outline: Style | None = None,
        Blue5Solid: Style | None = None,
        Blue5OutlineBold: Style | None = None,
        Blue5SolidBold: Style | None = None,
        Blue5OutlineLight: Style | None = None,
        Blue5SolidLight: Style | None = None,
        Blue5Dashed: Style | None = None,
        Blue5DashedBold: Style | None = None,
        Blue5DashedLight: Style | None = None,
        Blue6: Style | None = None,
        Blue6Bordered: Style | None = None,
        Blue6Bold: Style | None = None,
        Blue6Light: Style | None = None,
        Blue6Flat: Style | None = None,
        Blue6Outline: Style | None = None,
        Blue6Solid: Style | None = None,
        Blue6OutlineBold: Style | None = None,
        Blue6SolidBold: Style | None = None,
        Blue6OutlineLight: Style | None = None,
        Blue6SolidLight: Style | None = None,
        Blue6Dashed: Style | None = None,
        Blue6DashedBold: Style | None = None,
        Blue6DashedLight: Style | None = None,
        Red1: Style | None = None,
        Red1Bordered: Style | None = None,
        Red1Bold: Style | None = None,
        Red1Light: Style | None = None,
        Red1Flat: Style | None = None,
        Red1Outline: Style | None = None,
        Red1Solid: Style | None = None,
        Red1OutlineBold: Style | None = None,
        Red1SolidBold: Style | None = None,
        Red1OutlineLight: Style | None = None,
        Red1SolidLight: Style | None = None,
        Red1Dashed: Style | None = None,
        Red1DashedBold: Style | None = None,
        Red1DashedLight: Style | None = None,
        Red2: Style | None = None,
        Red2Bordered: Style | None = None,
        Red2Bold: Style | None = None,
        Red2Light: Style | None = None,
        Red2Flat: Style | None = None,
        Red2Outline: Style | None = None,
        Red2Solid: Style | None = None,
        Red2OutlineBold: Style | None = None,
        Red2SolidBold: Style | None = None,
        Red2OutlineLight: Style | None = None,
        Red2SolidLight: Style | None = None,
        Red2Dashed: Style | None = None,
        Red2DashedBold: Style | None = None,
        Red2DashedLight: Style | None = None,
        Red3: Style | None = None,
        Red3Bordered: Style | None = None,
        Red3Bold: Style | None = None,
        Red3Light: Style | None = None,
        Red3Flat: Style | None = None,
        Red3Outline: Style | None = None,
        Red3Solid: Style | None = None,
        Red3OutlineBold: Style | None = None,
        Red3SolidBold: Style | None = None,
        Red3OutlineLight: Style | None = None,
        Red3SolidLight: Style | None = None,
        Red3Dashed: Style | None = None,
        Red3DashedBold: Style | None = None,
        Red3DashedLight: Style | None = None,
        Red4: Style | None = None,
        Red4Bordered: Style | None = None,
        Red4Bold: Style | None = None,
        Red4Light: Style | None = None,
        Red4Flat: Style | None = None,
        Red4Outline: Style | None = None,
        Red4Solid: Style | None = None,
        Red4OutlineBold: Style | None = None,
        Red4SolidBold: Style | None = None,
        Red4OutlineLight: Style | None = None,
        Red4SolidLight: Style | None = None,
        Red4Dashed: Style | None = None,
        Red4DashedBold: Style | None = None,
        Red4DashedLight: Style | None = None,
        Red5: Style | None = None,
        Red5Bordered: Style | None = None,
        Red5Bold: Style | None = None,
        Red5Light: Style | None = None,
        Red5Flat: Style | None = None,
        Red5Outline: Style | None = None,
        Red5Solid: Style | None = None,
        Red5OutlineBold: Style | None = None,
        Red5SolidBold: Style | None = None,
        Red5OutlineLight: Style | None = None,
        Red5SolidLight: Style | None = None,
        Red5Dashed: Style | None = None,
        Red5DashedBold: Style | None = None,
        Red5DashedLight: Style | None = None,
        Red6: Style | None = None,
        Red6Bordered: Style | None = None,
        Red6Bold: Style | None = None,
        Red6Light: Style | None = None,
        Red6Flat: Style | None = None,
        Red6Outline: Style | None = None,
        Red6Solid: Style | None = None,
        Red6OutlineBold: Style | None = None,
        Red6SolidBold: Style | None = None,
        Red6OutlineLight: Style | None = None,
        Red6SolidLight: Style | None = None,
        Red6Dashed: Style | None = None,
        Red6DashedBold: Style | None = None,
        Red6DashedLight: Style | None = None,
        RedBerry1: Style | None = None,
        RedBerry1Bordered: Style | None = None,
        RedBerry1Bold: Style | None = None,
        RedBerry1Light: Style | None = None,
        RedBerry1Flat: Style | None = None,
        RedBerry1Outline: Style | None = None,
        RedBerry1Solid: Style | None = None,
        RedBerry1OutlineBold: Style | None = None,
        RedBerry1SolidBold: Style | None = None,
        RedBerry1OutlineLight: Style | None = None,
        RedBerry1SolidLight: Style | None = None,
        RedBerry1Dashed: Style | None = None,
        RedBerry1DashedBold: Style | None = None,
        RedBerry1DashedLight: Style | None = None,
        RedBerry2: Style | None = None,
        RedBerry2Bordered: Style | None = None,
        RedBerry2Bold: Style | None = None,
        RedBerry2Light: Style | None = None,
        RedBerry2Flat: Style | None = None,
        RedBerry2Outline: Style | None = None,
        RedBerry2Solid: Style | None = None,
        RedBerry2OutlineBold: Style | None = None,
        RedBerry2SolidBold: Style | None = None,
        RedBerry2OutlineLight: Style | None = None,
        RedBerry2SolidLight: Style | None = None,
        RedBerry2Dashed: Style | None = None,
        RedBerry2DashedBold: Style | None = None,
        RedBerry2DashedLight: Style | None = None,
        RedBerry3: Style | None = None,
        RedBerry3Bordered: Style | None = None,
        RedBerry3Bold: Style | None = None,
        RedBerry3Light: Style | None = None,
        RedBerry3Flat: Style | None = None,
        RedBerry3Outline: Style | None = None,
        RedBerry3Solid: Style | None = None,
        RedBerry3OutlineBold: Style | None = None,
        RedBerry3SolidBold: Style | None = None,
        RedBerry3OutlineLight: Style | None = None,
        RedBerry3SolidLight: Style | None = None,
        RedBerry3Dashed: Style | None = None,
        RedBerry3DashedBold: Style | None = None,
        RedBerry3DashedLight: Style | None = None,
        RedBerry4: Style | None = None,
        RedBerry4Bordered: Style | None = None,
        RedBerry4Bold: Style | None = None,
        RedBerry4Light: Style | None = None,
        RedBerry4Flat: Style | None = None,
        RedBerry4Outline: Style | None = None,
        RedBerry4Solid: Style | None = None,
        RedBerry4OutlineBold: Style | None = None,
        RedBerry4SolidBold: Style | None = None,
        RedBerry4OutlineLight: Style | None = None,
        RedBerry4SolidLight: Style | None = None,
        RedBerry4Dashed: Style | None = None,
        RedBerry4DashedBold: Style | None = None,
        RedBerry4DashedLight: Style | None = None,
        RedBerry5: Style | None = None,
        RedBerry5Bordered: Style | None = None,
        RedBerry5Bold: Style | None = None,
        RedBerry5Light: Style | None = None,
        RedBerry5Flat: Style | None = None,
        RedBerry5Outline: Style | None = None,
        RedBerry5Solid: Style | None = None,
        RedBerry5OutlineBold: Style | None = None,
        RedBerry5SolidBold: Style | None = None,
        RedBerry5OutlineLight: Style | None = None,
        RedBerry5SolidLight: Style | None = None,
        RedBerry5Dashed: Style | None = None,
        RedBerry5DashedBold: Style | None = None,
        RedBerry5DashedLight: Style | None = None,
        RedBerry6: Style | None = None,
        RedBerry6Bordered: Style | None = None,
        RedBerry6Bold: Style | None = None,
        RedBerry6Light: Style | None = None,
        RedBerry6Flat: Style | None = None,
        RedBerry6Outline: Style | None = None,
        RedBerry6Solid: Style | None = None,
        RedBerry6OutlineBold: Style | None = None,
        RedBerry6SolidBold: Style | None = None,
        RedBerry6OutlineLight: Style | None = None,
        RedBerry6SolidLight: Style | None = None,
        RedBerry6Dashed: Style | None = None,
        RedBerry6DashedBold: Style | None = None,
        RedBerry6DashedLight: Style | None = None,
        Green1: Style | None = None,
        Green1Bordered: Style | None = None,
        Green1Bold: Style | None = None,
        Green1Light: Style | None = None,
        Green1Flat: Style | None = None,
        Green1Outline: Style | None = None,
        Green1Solid: Style | None = None,
        Green1OutlineBold: Style | None = None,
        Green1SolidBold: Style | None = None,
        Green1OutlineLight: Style | None = None,
        Green1SolidLight: Style | None = None,
        Green1Dashed: Style | None = None,
        Green1DashedBold: Style | None = None,
        Green1DashedLight: Style | None = None,
        Green2: Style | None = None,
        Green2Bordered: Style | None = None,
        Green2Bold: Style | None = None,
        Green2Light: Style | None = None,
        Green2Flat: Style | None = None,
        Green2Outline: Style | None = None,
        Green2Solid: Style | None = None,
        Green2OutlineBold: Style | None = None,
        Green2SolidBold: Style | None = None,
        Green2OutlineLight: Style | None = None,
        Green2SolidLight: Style | None = None,
        Green2Dashed: Style | None = None,
        Green2DashedBold: Style | None = None,
        Green2DashedLight: Style | None = None,
        Green3: Style | None = None,
        Green3Bordered: Style | None = None,
        Green3Bold: Style | None = None,
        Green3Light: Style | None = None,
        Green3Flat: Style | None = None,
        Green3Outline: Style | None = None,
        Green3Solid: Style | None = None,
        Green3OutlineBold: Style | None = None,
        Green3SolidBold: Style | None = None,
        Green3OutlineLight: Style | None = None,
        Green3SolidLight: Style | None = None,
        Green3Dashed: Style | None = None,
        Green3DashedBold: Style | None = None,
        Green3DashedLight: Style | None = None,
        Green4: Style | None = None,
        Green4Bordered: Style | None = None,
        Green4Bold: Style | None = None,
        Green4Light: Style | None = None,
        Green4Flat: Style | None = None,
        Green4Outline: Style | None = None,
        Green4Solid: Style | None = None,
        Green4OutlineBold: Style | None = None,
        Green4SolidBold: Style | None = None,
        Green4OutlineLight: Style | None = None,
        Green4SolidLight: Style | None = None,
        Green4Dashed: Style | None = None,
        Green4DashedBold: Style | None = None,
        Green4DashedLight: Style | None = None,
        Green5: Style | None = None,
        Green5Bordered: Style | None = None,
        Green5Bold: Style | None = None,
        Green5Light: Style | None = None,
        Green5Flat: Style | None = None,
        Green5Outline: Style | None = None,
        Green5Solid: Style | None = None,
        Green5OutlineBold: Style | None = None,
        Green5SolidBold: Style | None = None,
        Green5OutlineLight: Style | None = None,
        Green5SolidLight: Style | None = None,
        Green5Dashed: Style | None = None,
        Green5DashedBold: Style | None = None,
        Green5DashedLight: Style | None = None,
        Green6: Style | None = None,
        Green6Bordered: Style | None = None,
        Green6Bold: Style | None = None,
        Green6Light: Style | None = None,
        Green6Flat: Style | None = None,
        Green6Outline: Style | None = None,
        Green6Solid: Style | None = None,
        Green6OutlineBold: Style | None = None,
        Green6SolidBold: Style | None = None,
        Green6OutlineLight: Style | None = None,
        Green6SolidLight: Style | None = None,
        Green6Dashed: Style | None = None,
        Green6DashedBold: Style | None = None,
        Green6DashedLight: Style | None = None,
        Yellow1: Style | None = None,
        Yellow1Bordered: Style | None = None,
        Yellow1Bold: Style | None = None,
        Yellow1Light: Style | None = None,
        Yellow1Flat: Style | None = None,
        Yellow1Outline: Style | None = None,
        Yellow1Solid: Style | None = None,
        Yellow1OutlineBold: Style | None = None,
        Yellow1SolidBold: Style | None = None,
        Yellow1OutlineLight: Style | None = None,
        Yellow1SolidLight: Style | None = None,
        Yellow1Dashed: Style | None = None,
        Yellow1DashedBold: Style | None = None,
        Yellow1DashedLight: Style | None = None,
        Yellow2: Style | None = None,
        Yellow2Bordered: Style | None = None,
        Yellow2Bold: Style | None = None,
        Yellow2Light: Style | None = None,
        Yellow2Flat: Style | None = None,
        Yellow2Outline: Style | None = None,
        Yellow2Solid: Style | None = None,
        Yellow2OutlineBold: Style | None = None,
        Yellow2SolidBold: Style | None = None,
        Yellow2OutlineLight: Style | None = None,
        Yellow2SolidLight: Style | None = None,
        Yellow2Dashed: Style | None = None,
        Yellow2DashedBold: Style | None = None,
        Yellow2DashedLight: Style | None = None,
        Yellow3: Style | None = None,
        Yellow3Bordered: Style | None = None,
        Yellow3Bold: Style | None = None,
        Yellow3Light: Style | None = None,
        Yellow3Flat: Style | None = None,
        Yellow3Outline: Style | None = None,
        Yellow3Solid: Style | None = None,
        Yellow3OutlineBold: Style | None = None,
        Yellow3SolidBold: Style | None = None,
        Yellow3OutlineLight: Style | None = None,
        Yellow3SolidLight: Style | None = None,
        Yellow3Dashed: Style | None = None,
        Yellow3DashedBold: Style | None = None,
        Yellow3DashedLight: Style | None = None,
        Yellow4: Style | None = None,
        Yellow4Bordered: Style | None = None,
        Yellow4Bold: Style | None = None,
        Yellow4Light: Style | None = None,
        Yellow4Flat: Style | None = None,
        Yellow4Outline: Style | None = None,
        Yellow4Solid: Style | None = None,
        Yellow4OutlineBold: Style | None = None,
        Yellow4SolidBold: Style | None = None,
        Yellow4OutlineLight: Style | None = None,
        Yellow4SolidLight: Style | None = None,
        Yellow4Dashed: Style | None = None,
        Yellow4DashedBold: Style | None = None,
        Yellow4DashedLight: Style | None = None,
        Yellow5: Style | None = None,
        Yellow5Bordered: Style | None = None,
        Yellow5Bold: Style | None = None,
        Yellow5Light: Style | None = None,
        Yellow5Flat: Style | None = None,
        Yellow5Outline: Style | None = None,
        Yellow5Solid: Style | None = None,
        Yellow5OutlineBold: Style | None = None,
        Yellow5SolidBold: Style | None = None,
        Yellow5OutlineLight: Style | None = None,
        Yellow5SolidLight: Style | None = None,
        Yellow5Dashed: Style | None = None,
        Yellow5DashedBold: Style | None = None,
        Yellow5DashedLight: Style | None = None,
        Yellow6: Style | None = None,
        Yellow6Bordered: Style | None = None,
        Yellow6Bold: Style | None = None,
        Yellow6Light: Style | None = None,
        Yellow6Flat: Style | None = None,
        Yellow6Outline: Style | None = None,
        Yellow6Solid: Style | None = None,
        Yellow6OutlineBold: Style | None = None,
        Yellow6SolidBold: Style | None = None,
        Yellow6OutlineLight: Style | None = None,
        Yellow6SolidLight: Style | None = None,
        Yellow6Dashed: Style | None = None,
        Yellow6DashedBold: Style | None = None,
        Yellow6DashedLight: Style | None = None,
        Orange1: Style | None = None,
        Orange1Bordered: Style | None = None,
        Orange1Bold: Style | None = None,
        Orange1Light: Style | None = None,
        Orange1Flat: Style | None = None,
        Orange1Outline: Style | None = None,
        Orange1Solid: Style | None = None,
        Orange1OutlineBold: Style | None = None,
        Orange1SolidBold: Style | None = None,
        Orange1OutlineLight: Style | None = None,
        Orange1SolidLight: Style | None = None,
        Orange1Dashed: Style | None = None,
        Orange1DashedBold: Style | None = None,
        Orange1DashedLight: Style | None = None,
        Orange2: Style | None = None,
        Orange2Bordered: Style | None = None,
        Orange2Bold: Style | None = None,
        Orange2Light: Style | None = None,
        Orange2Flat: Style | None = None,
        Orange2Outline: Style | None = None,
        Orange2Solid: Style | None = None,
        Orange2OutlineBold: Style | None = None,
        Orange2SolidBold: Style | None = None,
        Orange2OutlineLight: Style | None = None,
        Orange2SolidLight: Style | None = None,
        Orange2Dashed: Style | None = None,
        Orange2DashedBold: Style | None = None,
        Orange2DashedLight: Style | None = None,
        Orange3: Style | None = None,
        Orange3Bordered: Style | None = None,
        Orange3Bold: Style | None = None,
        Orange3Light: Style | None = None,
        Orange3Flat: Style | None = None,
        Orange3Outline: Style | None = None,
        Orange3Solid: Style | None = None,
        Orange3OutlineBold: Style | None = None,
        Orange3SolidBold: Style | None = None,
        Orange3OutlineLight: Style | None = None,
        Orange3SolidLight: Style | None = None,
        Orange3Dashed: Style | None = None,
        Orange3DashedBold: Style | None = None,
        Orange3DashedLight: Style | None = None,
        Orange4: Style | None = None,
        Orange4Bordered: Style | None = None,
        Orange4Bold: Style | None = None,
        Orange4Light: Style | None = None,
        Orange4Flat: Style | None = None,
        Orange4Outline: Style | None = None,
        Orange4Solid: Style | None = None,
        Orange4OutlineBold: Style | None = None,
        Orange4SolidBold: Style | None = None,
        Orange4OutlineLight: Style | None = None,
        Orange4SolidLight: Style | None = None,
        Orange4Dashed: Style | None = None,
        Orange4DashedBold: Style | None = None,
        Orange4DashedLight: Style | None = None,
        Orange5: Style | None = None,
        Orange5Bordered: Style | None = None,
        Orange5Bold: Style | None = None,
        Orange5Light: Style | None = None,
        Orange5Flat: Style | None = None,
        Orange5Outline: Style | None = None,
        Orange5Solid: Style | None = None,
        Orange5OutlineBold: Style | None = None,
        Orange5SolidBold: Style | None = None,
        Orange5OutlineLight: Style | None = None,
        Orange5SolidLight: Style | None = None,
        Orange5Dashed: Style | None = None,
        Orange5DashedBold: Style | None = None,
        Orange5DashedLight: Style | None = None,
        Orange6: Style | None = None,
        Orange6Bordered: Style | None = None,
        Orange6Bold: Style | None = None,
        Orange6Light: Style | None = None,
        Orange6Flat: Style | None = None,
        Orange6Outline: Style | None = None,
        Orange6Solid: Style | None = None,
        Orange6OutlineBold: Style | None = None,
        Orange6SolidBold: Style | None = None,
        Orange6OutlineLight: Style | None = None,
        Orange6SolidLight: Style | None = None,
        Orange6Dashed: Style | None = None,
        Orange6DashedBold: Style | None = None,
        Orange6DashedLight: Style | None = None,
        Cyan1: Style | None = None,
        Cyan1Bordered: Style | None = None,
        Cyan1Bold: Style | None = None,
        Cyan1Light: Style | None = None,
        Cyan1Flat: Style | None = None,
        Cyan1Outline: Style | None = None,
        Cyan1Solid: Style | None = None,
        Cyan1OutlineBold: Style | None = None,
        Cyan1SolidBold: Style | None = None,
        Cyan1OutlineLight: Style | None = None,
        Cyan1SolidLight: Style | None = None,
        Cyan1Dashed: Style | None = None,
        Cyan1DashedBold: Style | None = None,
        Cyan1DashedLight: Style | None = None,
        Cyan2: Style | None = None,
        Cyan2Bordered: Style | None = None,
        Cyan2Bold: Style | None = None,
        Cyan2Light: Style | None = None,
        Cyan2Flat: Style | None = None,
        Cyan2Outline: Style | None = None,
        Cyan2Solid: Style | None = None,
        Cyan2OutlineBold: Style | None = None,
        Cyan2SolidBold: Style | None = None,
        Cyan2OutlineLight: Style | None = None,
        Cyan2SolidLight: Style | None = None,
        Cyan2Dashed: Style | None = None,
        Cyan2DashedBold: Style | None = None,
        Cyan2DashedLight: Style | None = None,
        Cyan3: Style | None = None,
        Cyan3Bordered: Style | None = None,
        Cyan3Bold: Style | None = None,
        Cyan3Light: Style | None = None,
        Cyan3Flat: Style | None = None,
        Cyan3Outline: Style | None = None,
        Cyan3Solid: Style | None = None,
        Cyan3OutlineBold: Style | None = None,
        Cyan3SolidBold: Style | None = None,
        Cyan3OutlineLight: Style | None = None,
        Cyan3SolidLight: Style | None = None,
        Cyan3Dashed: Style | None = None,
        Cyan3DashedBold: Style | None = None,
        Cyan3DashedLight: Style | None = None,
        Cyan4: Style | None = None,
        Cyan4Bordered: Style | None = None,
        Cyan4Bold: Style | None = None,
        Cyan4Light: Style | None = None,
        Cyan4Flat: Style | None = None,
        Cyan4Outline: Style | None = None,
        Cyan4Solid: Style | None = None,
        Cyan4OutlineBold: Style | None = None,
        Cyan4SolidBold: Style | None = None,
        Cyan4OutlineLight: Style | None = None,
        Cyan4SolidLight: Style | None = None,
        Cyan4Dashed: Style | None = None,
        Cyan4DashedBold: Style | None = None,
        Cyan4DashedLight: Style | None = None,
        Cyan5: Style | None = None,
        Cyan5Bordered: Style | None = None,
        Cyan5Bold: Style | None = None,
        Cyan5Light: Style | None = None,
        Cyan5Flat: Style | None = None,
        Cyan5Outline: Style | None = None,
        Cyan5Solid: Style | None = None,
        Cyan5OutlineBold: Style | None = None,
        Cyan5SolidBold: Style | None = None,
        Cyan5OutlineLight: Style | None = None,
        Cyan5SolidLight: Style | None = None,
        Cyan5Dashed: Style | None = None,
        Cyan5DashedBold: Style | None = None,
        Cyan5DashedLight: Style | None = None,
        Cyan6: Style | None = None,
        Cyan6Bordered: Style | None = None,
        Cyan6Bold: Style | None = None,
        Cyan6Light: Style | None = None,
        Cyan6Flat: Style | None = None,
        Cyan6Outline: Style | None = None,
        Cyan6Solid: Style | None = None,
        Cyan6OutlineBold: Style | None = None,
        Cyan6SolidBold: Style | None = None,
        Cyan6OutlineLight: Style | None = None,
        Cyan6SolidLight: Style | None = None,
        Cyan6Dashed: Style | None = None,
        Cyan6DashedBold: Style | None = None,
        Cyan6DashedLight: Style | None = None,
        Purple1: Style | None = None,
        Purple1Bordered: Style | None = None,
        Purple1Bold: Style | None = None,
        Purple1Light: Style | None = None,
        Purple1Flat: Style | None = None,
        Purple1Outline: Style | None = None,
        Purple1Solid: Style | None = None,
        Purple1OutlineBold: Style | None = None,
        Purple1SolidBold: Style | None = None,
        Purple1OutlineLight: Style | None = None,
        Purple1SolidLight: Style | None = None,
        Purple1Dashed: Style | None = None,
        Purple1DashedBold: Style | None = None,
        Purple1DashedLight: Style | None = None,
        Purple2: Style | None = None,
        Purple2Bordered: Style | None = None,
        Purple2Bold: Style | None = None,
        Purple2Light: Style | None = None,
        Purple2Flat: Style | None = None,
        Purple2Outline: Style | None = None,
        Purple2Solid: Style | None = None,
        Purple2OutlineBold: Style | None = None,
        Purple2SolidBold: Style | None = None,
        Purple2OutlineLight: Style | None = None,
        Purple2SolidLight: Style | None = None,
        Purple2Dashed: Style | None = None,
        Purple2DashedBold: Style | None = None,
        Purple2DashedLight: Style | None = None,
        Purple3: Style | None = None,
        Purple3Bordered: Style | None = None,
        Purple3Bold: Style | None = None,
        Purple3Light: Style | None = None,
        Purple3Flat: Style | None = None,
        Purple3Outline: Style | None = None,
        Purple3Solid: Style | None = None,
        Purple3OutlineBold: Style | None = None,
        Purple3SolidBold: Style | None = None,
        Purple3OutlineLight: Style | None = None,
        Purple3SolidLight: Style | None = None,
        Purple3Dashed: Style | None = None,
        Purple3DashedBold: Style | None = None,
        Purple3DashedLight: Style | None = None,
        Purple4: Style | None = None,
        Purple4Bordered: Style | None = None,
        Purple4Bold: Style | None = None,
        Purple4Light: Style | None = None,
        Purple4Flat: Style | None = None,
        Purple4Outline: Style | None = None,
        Purple4Solid: Style | None = None,
        Purple4OutlineBold: Style | None = None,
        Purple4SolidBold: Style | None = None,
        Purple4OutlineLight: Style | None = None,
        Purple4SolidLight: Style | None = None,
        Purple4Dashed: Style | None = None,
        Purple4DashedBold: Style | None = None,
        Purple4DashedLight: Style | None = None,
        Purple5: Style | None = None,
        Purple5Bordered: Style | None = None,
        Purple5Bold: Style | None = None,
        Purple5Light: Style | None = None,
        Purple5Flat: Style | None = None,
        Purple5Outline: Style | None = None,
        Purple5Solid: Style | None = None,
        Purple5OutlineBold: Style | None = None,
        Purple5SolidBold: Style | None = None,
        Purple5OutlineLight: Style | None = None,
        Purple5SolidLight: Style | None = None,
        Purple5Dashed: Style | None = None,
        Purple5DashedBold: Style | None = None,
        Purple5DashedLight: Style | None = None,
        Purple6: Style | None = None,
        Purple6Bordered: Style | None = None,
        Purple6Bold: Style | None = None,
        Purple6Light: Style | None = None,
        Purple6Flat: Style | None = None,
        Purple6Outline: Style | None = None,
        Purple6Solid: Style | None = None,
        Purple6OutlineBold: Style | None = None,
        Purple6SolidBold: Style | None = None,
        Purple6OutlineLight: Style | None = None,
        Purple6SolidLight: Style | None = None,
        Purple6Dashed: Style | None = None,
        Purple6DashedBold: Style | None = None,
        Purple6DashedLight: Style | None = None,
        Magenta1: Style | None = None,
        Magenta1Bordered: Style | None = None,
        Magenta1Bold: Style | None = None,
        Magenta1Light: Style | None = None,
        Magenta1Flat: Style | None = None,
        Magenta1Outline: Style | None = None,
        Magenta1Solid: Style | None = None,
        Magenta1OutlineBold: Style | None = None,
        Magenta1SolidBold: Style | None = None,
        Magenta1OutlineLight: Style | None = None,
        Magenta1SolidLight: Style | None = None,
        Magenta1Dashed: Style | None = None,
        Magenta1DashedBold: Style | None = None,
        Magenta1DashedLight: Style | None = None,
        Magenta2: Style | None = None,
        Magenta2Bordered: Style | None = None,
        Magenta2Bold: Style | None = None,
        Magenta2Light: Style | None = None,
        Magenta2Flat: Style | None = None,
        Magenta2Outline: Style | None = None,
        Magenta2Solid: Style | None = None,
        Magenta2OutlineBold: Style | None = None,
        Magenta2SolidBold: Style | None = None,
        Magenta2OutlineLight: Style | None = None,
        Magenta2SolidLight: Style | None = None,
        Magenta2Dashed: Style | None = None,
        Magenta2DashedBold: Style | None = None,
        Magenta2DashedLight: Style | None = None,
        Magenta3: Style | None = None,
        Magenta3Bordered: Style | None = None,
        Magenta3Bold: Style | None = None,
        Magenta3Light: Style | None = None,
        Magenta3Flat: Style | None = None,
        Magenta3Outline: Style | None = None,
        Magenta3Solid: Style | None = None,
        Magenta3OutlineBold: Style | None = None,
        Magenta3SolidBold: Style | None = None,
        Magenta3OutlineLight: Style | None = None,
        Magenta3SolidLight: Style | None = None,
        Magenta3Dashed: Style | None = None,
        Magenta3DashedBold: Style | None = None,
        Magenta3DashedLight: Style | None = None,
        Magenta4: Style | None = None,
        Magenta4Bordered: Style | None = None,
        Magenta4Bold: Style | None = None,
        Magenta4Light: Style | None = None,
        Magenta4Flat: Style | None = None,
        Magenta4Outline: Style | None = None,
        Magenta4Solid: Style | None = None,
        Magenta4OutlineBold: Style | None = None,
        Magenta4SolidBold: Style | None = None,
        Magenta4OutlineLight: Style | None = None,
        Magenta4SolidLight: Style | None = None,
        Magenta4Dashed: Style | None = None,
        Magenta4DashedBold: Style | None = None,
        Magenta4DashedLight: Style | None = None,
        Magenta5: Style | None = None,
        Magenta5Bordered: Style | None = None,
        Magenta5Bold: Style | None = None,
        Magenta5Light: Style | None = None,
        Magenta5Flat: Style | None = None,
        Magenta5Outline: Style | None = None,
        Magenta5Solid: Style | None = None,
        Magenta5OutlineBold: Style | None = None,
        Magenta5SolidBold: Style | None = None,
        Magenta5OutlineLight: Style | None = None,
        Magenta5SolidLight: Style | None = None,
        Magenta5Dashed: Style | None = None,
        Magenta5DashedBold: Style | None = None,
        Magenta5DashedLight: Style | None = None,
        Magenta6: Style | None = None,
        Magenta6Bordered: Style | None = None,
        Magenta6Bold: Style | None = None,
        Magenta6Light: Style | None = None,
        Magenta6Flat: Style | None = None,
        Magenta6Outline: Style | None = None,
        Magenta6Solid: Style | None = None,
        Magenta6OutlineBold: Style | None = None,
        Magenta6SolidBold: Style | None = None,
        Magenta6OutlineLight: Style | None = None,
        Magenta6SolidLight: Style | None = None,
        Magenta6Dashed: Style | None = None,
        Magenta6DashedBold: Style | None = None,
        Magenta6DashedLight: Style | None = None,
        CornflowerBlue: Style | None = None,
        CornflowerBlueBordered: Style | None = None,
        CornflowerBlueBold: Style | None = None,
        CornflowerBlueLight: Style | None = None,
        CornflowerBlueFlat: Style | None = None,
        CornflowerBlueOutline: Style | None = None,
        CornflowerBlueSolid: Style | None = None,
        CornflowerBlueOutlineBold: Style | None = None,
        CornflowerBlueSolidBold: Style | None = None,
        CornflowerBlueOutlineLight: Style | None = None,
        CornflowerBlueSolidLight: Style | None = None,
        CornflowerBlueDashed: Style | None = None,
        CornflowerBlueDashedBold: Style | None = None,
        CornflowerBlueDashedLight: Style | None = None,
        Blue: Style | None = None,
        BlueBordered: Style | None = None,
        BlueBold: Style | None = None,
        BlueLight: Style | None = None,
        BlueFlat: Style | None = None,
        BlueOutline: Style | None = None,
        BlueSolid: Style | None = None,
        BlueOutlineBold: Style | None = None,
        BlueSolidBold: Style | None = None,
        BlueOutlineLight: Style | None = None,
        BlueSolidLight: Style | None = None,
        BlueDashed: Style | None = None,
        BlueDashedBold: Style | None = None,
        BlueDashedLight: Style | None = None,
        Red: Style | None = None,
        RedBordered: Style | None = None,
        RedBold: Style | None = None,
        RedLight: Style | None = None,
        RedFlat: Style | None = None,
        RedOutline: Style | None = None,
        RedSolid: Style | None = None,
        RedOutlineBold: Style | None = None,
        RedSolidBold: Style | None = None,
        RedOutlineLight: Style | None = None,
        RedSolidLight: Style | None = None,
        RedDashed: Style | None = None,
        RedDashedBold: Style | None = None,
        RedDashedLight: Style | None = None,
        RedBerry: Style | None = None,
        RedBerryBordered: Style | None = None,
        RedBerryBold: Style | None = None,
        RedBerryLight: Style | None = None,
        RedBerryFlat: Style | None = None,
        RedBerryOutline: Style | None = None,
        RedBerrySolid: Style | None = None,
        RedBerryOutlineBold: Style | None = None,
        RedBerrySolidBold: Style | None = None,
        RedBerryOutlineLight: Style | None = None,
        RedBerrySolidLight: Style | None = None,
        RedBerryDashed: Style | None = None,
        RedBerryDashedBold: Style | None = None,
        RedBerryDashedLight: Style | None = None,
        Green: Style | None = None,
        GreenBordered: Style | None = None,
        GreenBold: Style | None = None,
        GreenLight: Style | None = None,
        GreenFlat: Style | None = None,
        GreenOutline: Style | None = None,
        GreenSolid: Style | None = None,
        GreenOutlineBold: Style | None = None,
        GreenSolidBold: Style | None = None,
        GreenOutlineLight: Style | None = None,
        GreenSolidLight: Style | None = None,
        GreenDashed: Style | None = None,
        GreenDashedBold: Style | None = None,
        GreenDashedLight: Style | None = None,
        Yellow: Style | None = None,
        YellowBordered: Style | None = None,
        YellowBold: Style | None = None,
        YellowLight: Style | None = None,
        YellowFlat: Style | None = None,
        YellowOutline: Style | None = None,
        YellowSolid: Style | None = None,
        YellowOutlineBold: Style | None = None,
        YellowSolidBold: Style | None = None,
        YellowOutlineLight: Style | None = None,
        YellowSolidLight: Style | None = None,
        YellowDashed: Style | None = None,
        YellowDashedBold: Style | None = None,
        YellowDashedLight: Style | None = None,
        Orange: Style | None = None,
        OrangeBordered: Style | None = None,
        OrangeBold: Style | None = None,
        OrangeLight: Style | None = None,
        OrangeFlat: Style | None = None,
        OrangeOutline: Style | None = None,
        OrangeSolid: Style | None = None,
        OrangeOutlineBold: Style | None = None,
        OrangeSolidBold: Style | None = None,
        OrangeOutlineLight: Style | None = None,
        OrangeSolidLight: Style | None = None,
        OrangeDashed: Style | None = None,
        OrangeDashedBold: Style | None = None,
        OrangeDashedLight: Style | None = None,
        Cyan: Style | None = None,
        CyanBordered: Style | None = None,
        CyanBold: Style | None = None,
        CyanLight: Style | None = None,
        CyanFlat: Style | None = None,
        CyanOutline: Style | None = None,
        CyanSolid: Style | None = None,
        CyanOutlineBold: Style | None = None,
        CyanSolidBold: Style | None = None,
        CyanOutlineLight: Style | None = None,
        CyanSolidLight: Style | None = None,
        CyanDashed: Style | None = None,
        CyanDashedBold: Style | None = None,
        CyanDashedLight: Style | None = None,
        Purple: Style | None = None,
        PurpleBordered: Style | None = None,
        PurpleBold: Style | None = None,
        PurpleLight: Style | None = None,
        PurpleFlat: Style | None = None,
        PurpleOutline: Style | None = None,
        PurpleSolid: Style | None = None,
        PurpleOutlineBold: Style | None = None,
        PurpleSolidBold: Style | None = None,
        PurpleOutlineLight: Style | None = None,
        PurpleSolidLight: Style | None = None,
        PurpleDashed: Style | None = None,
        PurpleDashedBold: Style | None = None,
        PurpleDashedLight: Style | None = None,
        Magenta: Style | None = None,
        MagentaBordered: Style | None = None,
        MagentaBold: Style | None = None,
        MagentaLight: Style | None = None,
        MagentaFlat: Style | None = None,
        MagentaOutline: Style | None = None,
        MagentaSolid: Style | None = None,
        MagentaOutlineBold: Style | None = None,
        MagentaSolidBold: Style | None = None,
        MagentaOutlineLight: Style | None = None,
        MagentaSolidLight: Style | None = None,
        MagentaDashed: Style | None = None,
        MagentaDashedBold: Style | None = None,
        MagentaDashedLight: Style | None = None,
        Pink: Style | None = None,
        PinkBordered: Style | None = None,
        PinkBold: Style | None = None,
        PinkLight: Style | None = None,
        PinkFlat: Style | None = None,
        PinkOutline: Style | None = None,
        PinkSolid: Style | None = None,
        PinkOutlineBold: Style | None = None,
        PinkSolidBold: Style | None = None,
        PinkOutlineLight: Style | None = None,
        PinkSolidLight: Style | None = None,
        PinkDashed: Style | None = None,
        PinkDashedBold: Style | None = None,
        PinkDashedLight: Style | None = None,
        Lime: Style | None = None,
        LimeBordered: Style | None = None,
        LimeBold: Style | None = None,
        LimeLight: Style | None = None,
        LimeFlat: Style | None = None,
        LimeOutline: Style | None = None,
        LimeSolid: Style | None = None,
        LimeOutlineBold: Style | None = None,
        LimeSolidBold: Style | None = None,
        LimeOutlineLight: Style | None = None,
        LimeSolidLight: Style | None = None,
        LimeDashed: Style | None = None,
        LimeDashedBold: Style | None = None,
        LimeDashedLight: Style | None = None,
        Teal: Style | None = None,
        TealBordered: Style | None = None,
        TealBold: Style | None = None,
        TealLight: Style | None = None,
        TealFlat: Style | None = None,
        TealOutline: Style | None = None,
        TealSolid: Style | None = None,
        TealOutlineBold: Style | None = None,
        TealSolidBold: Style | None = None,
        TealOutlineLight: Style | None = None,
        TealSolidLight: Style | None = None,
        TealDashed: Style | None = None,
        TealDashedBold: Style | None = None,
        TealDashedLight: Style | None = None,
        Navy: Style | None = None,
        NavyBordered: Style | None = None,
        NavyBold: Style | None = None,
        NavyLight: Style | None = None,
        NavyFlat: Style | None = None,
        NavyOutline: Style | None = None,
        NavySolid: Style | None = None,
        NavyOutlineBold: Style | None = None,
        NavySolidBold: Style | None = None,
        NavyOutlineLight: Style | None = None,
        NavySolidLight: Style | None = None,
        NavyDashed: Style | None = None,
        NavyDashedBold: Style | None = None,
        NavyDashedLight: Style | None = None,
        Olive: Style | None = None,
        OliveBordered: Style | None = None,
        OliveBold: Style | None = None,
        OliveLight: Style | None = None,
        OliveFlat: Style | None = None,
        OliveOutline: Style | None = None,
        OliveSolid: Style | None = None,
        OliveOutlineBold: Style | None = None,
        OliveSolidBold: Style | None = None,
        OliveOutlineLight: Style | None = None,
        OliveSolidLight: Style | None = None,
        OliveDashed: Style | None = None,
        OliveDashedBold: Style | None = None,
        OliveDashedLight: Style | None = None,
        Brown: Style | None = None,
        BrownBordered: Style | None = None,
        BrownBold: Style | None = None,
        BrownLight: Style | None = None,
        BrownFlat: Style | None = None,
        BrownOutline: Style | None = None,
        BrownSolid: Style | None = None,
        BrownOutlineBold: Style | None = None,
        BrownSolidBold: Style | None = None,
        BrownOutlineLight: Style | None = None,
        BrownSolidLight: Style | None = None,
        BrownDashed: Style | None = None,
        BrownDashedBold: Style | None = None,
        BrownDashedLight: Style | None = None,
        Gold: Style | None = None,
        GoldBordered: Style | None = None,
        GoldBold: Style | None = None,
        GoldLight: Style | None = None,
        GoldFlat: Style | None = None,
        GoldOutline: Style | None = None,
        GoldSolid: Style | None = None,
        GoldOutlineBold: Style | None = None,
        GoldSolidBold: Style | None = None,
        GoldOutlineLight: Style | None = None,
        GoldSolidLight: Style | None = None,
        GoldDashed: Style | None = None,
        GoldDashedBold: Style | None = None,
        GoldDashedLight: Style | None = None,
        Aqua: Style | None = None,
        AquaBordered: Style | None = None,
        AquaBold: Style | None = None,
        AquaLight: Style | None = None,
        AquaFlat: Style | None = None,
        AquaOutline: Style | None = None,
        AquaSolid: Style | None = None,
        AquaOutlineBold: Style | None = None,
        AquaSolidBold: Style | None = None,
        AquaOutlineLight: Style | None = None,
        AquaSolidLight: Style | None = None,
        AquaDashed: Style | None = None,
        AquaDashedBold: Style | None = None,
        AquaDashedLight: Style | None = None,
        GreenYellow: Style | None = None,
        GreenYellowBordered: Style | None = None,
        GreenYellowBold: Style | None = None,
        GreenYellowLight: Style | None = None,
        GreenYellowFlat: Style | None = None,
        GreenYellowOutline: Style | None = None,
        GreenYellowSolid: Style | None = None,
        GreenYellowOutlineBold: Style | None = None,
        GreenYellowSolidBold: Style | None = None,
        GreenYellowOutlineLight: Style | None = None,
        GreenYellowSolidLight: Style | None = None,
        GreenYellowDashed: Style | None = None,
        GreenYellowDashedBold: Style | None = None,
        GreenYellowDashedLight: Style | None = None,
        Ivory: Style | None = None,
        IvoryBordered: Style | None = None,
        IvoryBold: Style | None = None,
        IvoryLight: Style | None = None,
        IvoryFlat: Style | None = None,
        IvoryOutline: Style | None = None,
        IvorySolid: Style | None = None,
        IvoryOutlineBold: Style | None = None,
        IvorySolidBold: Style | None = None,
        IvoryOutlineLight: Style | None = None,
        IvorySolidLight: Style | None = None,
        IvoryDashed: Style | None = None,
        IvoryDashedBold: Style | None = None,
        IvoryDashedLight: Style | None = None,
        Steel: Style | None = None,
        SteelBordered: Style | None = None,
        SteelBold: Style | None = None,
        SteelLight: Style | None = None,
        SteelFlat: Style | None = None,
        SteelOutline: Style | None = None,
        SteelSolid: Style | None = None,
        SteelOutlineBold: Style | None = None,
        SteelSolidBold: Style | None = None,
        SteelOutlineLight: Style | None = None,
        SteelSolidLight: Style | None = None,
        SteelDashed: Style | None = None,
        SteelDashedBold: Style | None = None,
        SteelDashedLight: Style | None = None,
        GoogleBlue: Style | None = None,
        GoogleBlueBordered: Style | None = None,
        GoogleBlueBold: Style | None = None,
        GoogleBlueLight: Style | None = None,
        GoogleBlueFlat: Style | None = None,
        GoogleBlueOutline: Style | None = None,
        GoogleBlueSolid: Style | None = None,
        GoogleBlueOutlineBold: Style | None = None,
        GoogleBlueSolidBold: Style | None = None,
        GoogleBlueOutlineLight: Style | None = None,
        GoogleBlueSolidLight: Style | None = None,
        GoogleBlueDashed: Style | None = None,
        GoogleBlueDashedBold: Style | None = None,
        GoogleBlueDashedLight: Style | None = None,
        GoogleRed: Style | None = None,
        GoogleRedBordered: Style | None = None,
        GoogleRedBold: Style | None = None,
        GoogleRedLight: Style | None = None,
        GoogleRedFlat: Style | None = None,
        GoogleRedOutline: Style | None = None,
        GoogleRedSolid: Style | None = None,
        GoogleRedOutlineBold: Style | None = None,
        GoogleRedSolidBold: Style | None = None,
        GoogleRedOutlineLight: Style | None = None,
        GoogleRedSolidLight: Style | None = None,
        GoogleRedDashed: Style | None = None,
        GoogleRedDashedBold: Style | None = None,
        GoogleRedDashedLight: Style | None = None,
        GoogleYellow: Style | None = None,
        GoogleYellowBordered: Style | None = None,
        GoogleYellowBold: Style | None = None,
        GoogleYellowLight: Style | None = None,
        GoogleYellowFlat: Style | None = None,
        GoogleYellowOutline: Style | None = None,
        GoogleYellowSolid: Style | None = None,
        GoogleYellowOutlineBold: Style | None = None,
        GoogleYellowSolidBold: Style | None = None,
        GoogleYellowOutlineLight: Style | None = None,
        GoogleYellowSolidLight: Style | None = None,
        GoogleYellowDashed: Style | None = None,
        GoogleYellowDashedBold: Style | None = None,
        GoogleYellowDashedLight: Style | None = None,
        GoogleGreen: Style | None = None,
        GoogleGreenBordered: Style | None = None,
        GoogleGreenBold: Style | None = None,
        GoogleGreenLight: Style | None = None,
        GoogleGreenFlat: Style | None = None,
        GoogleGreenOutline: Style | None = None,
        GoogleGreenSolid: Style | None = None,
        GoogleGreenOutlineBold: Style | None = None,
        GoogleGreenSolidBold: Style | None = None,
        GoogleGreenOutlineLight: Style | None = None,
        GoogleGreenSolidLight: Style | None = None,
        GoogleGreenDashed: Style | None = None,
        GoogleGreenDashedBold: Style | None = None,
        GoogleGreenDashedLight: Style | None = None,
        GoogleOrange: Style | None = None,
        GoogleOrangeBordered: Style | None = None,
        GoogleOrangeBold: Style | None = None,
        GoogleOrangeLight: Style | None = None,
        GoogleOrangeFlat: Style | None = None,
        GoogleOrangeOutline: Style | None = None,
        GoogleOrangeSolid: Style | None = None,
        GoogleOrangeOutlineBold: Style | None = None,
        GoogleOrangeSolidBold: Style | None = None,
        GoogleOrangeOutlineLight: Style | None = None,
        GoogleOrangeSolidLight: Style | None = None,
        GoogleOrangeDashed: Style | None = None,
        GoogleOrangeDashedBold: Style | None = None,
        GoogleOrangeDashedLight: Style | None = None,
        GooglePurple: Style | None = None,
        GooglePurpleBordered: Style | None = None,
        GooglePurpleBold: Style | None = None,
        GooglePurpleLight: Style | None = None,
        GooglePurpleFlat: Style | None = None,
        GooglePurpleOutline: Style | None = None,
        GooglePurpleSolid: Style | None = None,
        GooglePurpleOutlineBold: Style | None = None,
        GooglePurpleSolidBold: Style | None = None,
        GooglePurpleOutlineLight: Style | None = None,
        GooglePurpleSolidLight: Style | None = None,
        GooglePurpleDashed: Style | None = None,
        GooglePurpleDashedBold: Style | None = None,
        GooglePurpleDashedLight: Style | None = None,
        GoogleGray: Style | None = None,
        GoogleGrayBordered: Style | None = None,
        GoogleGrayBold: Style | None = None,
        GoogleGrayLight: Style | None = None,
        GoogleGrayFlat: Style | None = None,
        GoogleGrayOutline: Style | None = None,
        GoogleGraySolid: Style | None = None,
        GoogleGrayOutlineBold: Style | None = None,
        GoogleGraySolidBold: Style | None = None,
        GoogleGrayOutlineLight: Style | None = None,
        GoogleGraySolidLight: Style | None = None,
        GoogleGrayDashed: Style | None = None,
        GoogleGrayDashedBold: Style | None = None,
        GoogleGrayDashedLight: Style | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Self:
        """Create a new copy of preset styles with updated attributes.

        Args:
            **kwargs: Additional style attributes to update.

        Returns:
            Self: New preset styles instance with updated attributes.
        """
        passed = {k: v for k, v in locals().items() if k not in {"self", "kwargs"} and v is not None}
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
        "Muted": col.Muted,
        "Light": col.Light,
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
        elif role_name == "Dark":
            v = _make_variants(
                color,
                border_color=col.Gray6,
                default_text_color=col.White,
                line_color=col.Gray6,
            )
        else:
            v = _make_variants(color, border_color=border_color)
        styles_dict[role_name] = v["normal"]
        styles_dict[f"{role_name}Bordered"] = v["bordered"]
        styles_dict[f"{role_name}Bold"] = v["bold"]
        styles_dict[f"{role_name}Light"] = v["light"]
        styles_dict[f"{role_name}Flat"] = v["flat"]
        styles_dict[f"{role_name}Outline"] = v["outline"]
        styles_dict[f"{role_name}Solid"] = v["solid"]
        styles_dict[f"{role_name}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{role_name}SolidBold"] = v["solid_bold"]
        styles_dict[f"{role_name}OutlineLight"] = v["outline_light"]
        styles_dict[f"{role_name}SolidLight"] = v["solid_light"]
        styles_dict[f"{role_name}Dashed"] = v["dashed"]
        styles_dict[f"{role_name}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{role_name}DashedLight"] = v["dashed_light"]

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

    # 6. Semantic Tones (6 roles x 6 tones)
    semantic_tones_map: dict[str, Color] = {}
    for r in ["primary", "secondary", "accent", "muted", "danger", "success"]:
        for i in range(1, 7):
            semantic_tones_map[f"{r.capitalize()}{i}"] = getattr(col, f"{r.capitalize()}{i}")

    all_colors: dict[str, Color] = {**neutrals_map, **tones_map, **primaries_map, **brand_map, **semantic_tones_map}
    for cname, color in all_colors.items():
        v = _make_variants(color, border_color=border_color)
        styles_dict[cname] = v["normal"]
        styles_dict[f"{cname}Bordered"] = v["bordered"]
        styles_dict[f"{cname}Bold"] = v["bold"]
        styles_dict[f"{cname}Light"] = v["light"]
        styles_dict[f"{cname}Flat"] = v["flat"]
        styles_dict[f"{cname}Outline"] = v["outline"]
        styles_dict[f"{cname}Solid"] = v["solid"]
        styles_dict[f"{cname}OutlineBold"] = v["outline_bold"]
        styles_dict[f"{cname}SolidBold"] = v["solid_bold"]
        styles_dict[f"{cname}OutlineLight"] = v["outline_light"]
        styles_dict[f"{cname}SolidLight"] = v["solid_light"]
        styles_dict[f"{cname}Dashed"] = v["dashed"]
        styles_dict[f"{cname}DashedBold"] = v["dashed_bold"]
        styles_dict[f"{cname}DashedLight"] = v["dashed_light"]

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

    return GoogleStyles(**styles_dict)


_google_styles: GoogleStyles = _create_google_styles()
GoogleStyles.register_default_instance(_google_styles)

__all__ = [
    "GoogleStyles",
]
