# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Default preset styles module."""

from __future__ import annotations

import warnings
from typing import Any, Literal, Self

from drawlib._core.l3_fonts import FontSourceCode
from drawlib._core.l3_styles import BaseStyles, Style
from drawlib._preset_colors import (
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
)
from drawlib._preset_styles._utils import _make_variants

warnings.filterwarnings(
    "ignore",
    message=r'Field name ".*" in ".*" shadows an attribute in parent ".*"',
    category=UserWarning,
)


class DefaultStyles(BaseStyles):
    """Default preset styles with complete typing for IDE autocompletion."""

    # =========================================================================
    # Semantic Roles
    # =========================================================================
    # primary
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

    # secondary
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

    # accent
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

    # muted
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

    # light
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

    # dark
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

    # danger
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

    # success
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

    # =========================================================================
    # 6-Tone Hues
    # =========================================================================
    # blue1
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

    # blue2
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

    # blue3
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

    # blue4
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

    # blue5
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

    # blue6
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

    # green1
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

    # green2
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

    # green3
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

    # green4
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

    # green5
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

    # green6
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

    # red1
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

    # red2
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

    # red3
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

    # red4
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

    # red5
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

    # red6
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

    # orange1
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

    # orange2
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

    # orange3
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

    # orange4
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

    # orange5
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

    # orange6
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

    # amber1
    Amber1: Style
    Amber1Bordered: Style
    Amber1Bold: Style
    Amber1Light: Style
    Amber1Flat: Style
    Amber1Outline: Style
    Amber1Solid: Style
    Amber1OutlineBold: Style
    Amber1SolidBold: Style
    Amber1OutlineLight: Style
    Amber1SolidLight: Style
    Amber1Dashed: Style
    Amber1DashedBold: Style
    Amber1DashedLight: Style

    # amber2
    Amber2: Style
    Amber2Bordered: Style
    Amber2Bold: Style
    Amber2Light: Style
    Amber2Flat: Style
    Amber2Outline: Style
    Amber2Solid: Style
    Amber2OutlineBold: Style
    Amber2SolidBold: Style
    Amber2OutlineLight: Style
    Amber2SolidLight: Style
    Amber2Dashed: Style
    Amber2DashedBold: Style
    Amber2DashedLight: Style

    # amber3
    Amber3: Style
    Amber3Bordered: Style
    Amber3Bold: Style
    Amber3Light: Style
    Amber3Flat: Style
    Amber3Outline: Style
    Amber3Solid: Style
    Amber3OutlineBold: Style
    Amber3SolidBold: Style
    Amber3OutlineLight: Style
    Amber3SolidLight: Style
    Amber3Dashed: Style
    Amber3DashedBold: Style
    Amber3DashedLight: Style

    # amber4
    Amber4: Style
    Amber4Bordered: Style
    Amber4Bold: Style
    Amber4Light: Style
    Amber4Flat: Style
    Amber4Outline: Style
    Amber4Solid: Style
    Amber4OutlineBold: Style
    Amber4SolidBold: Style
    Amber4OutlineLight: Style
    Amber4SolidLight: Style
    Amber4Dashed: Style
    Amber4DashedBold: Style
    Amber4DashedLight: Style

    # amber5
    Amber5: Style
    Amber5Bordered: Style
    Amber5Bold: Style
    Amber5Light: Style
    Amber5Flat: Style
    Amber5Outline: Style
    Amber5Solid: Style
    Amber5OutlineBold: Style
    Amber5SolidBold: Style
    Amber5OutlineLight: Style
    Amber5SolidLight: Style
    Amber5Dashed: Style
    Amber5DashedBold: Style
    Amber5DashedLight: Style

    # amber6
    Amber6: Style
    Amber6Bordered: Style
    Amber6Bold: Style
    Amber6Light: Style
    Amber6Flat: Style
    Amber6Outline: Style
    Amber6Solid: Style
    Amber6OutlineBold: Style
    Amber6SolidBold: Style
    Amber6OutlineLight: Style
    Amber6SolidLight: Style
    Amber6Dashed: Style
    Amber6DashedBold: Style
    Amber6DashedLight: Style

    # purple1
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

    # purple2
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

    # purple3
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

    # purple4
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

    # purple5
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

    # purple6
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

    # teal1
    Teal1: Style
    Teal1Bordered: Style
    Teal1Bold: Style
    Teal1Light: Style
    Teal1Flat: Style
    Teal1Outline: Style
    Teal1Solid: Style
    Teal1OutlineBold: Style
    Teal1SolidBold: Style
    Teal1OutlineLight: Style
    Teal1SolidLight: Style
    Teal1Dashed: Style
    Teal1DashedBold: Style
    Teal1DashedLight: Style

    # teal2
    Teal2: Style
    Teal2Bordered: Style
    Teal2Bold: Style
    Teal2Light: Style
    Teal2Flat: Style
    Teal2Outline: Style
    Teal2Solid: Style
    Teal2OutlineBold: Style
    Teal2SolidBold: Style
    Teal2OutlineLight: Style
    Teal2SolidLight: Style
    Teal2Dashed: Style
    Teal2DashedBold: Style
    Teal2DashedLight: Style

    # teal3
    Teal3: Style
    Teal3Bordered: Style
    Teal3Bold: Style
    Teal3Light: Style
    Teal3Flat: Style
    Teal3Outline: Style
    Teal3Solid: Style
    Teal3OutlineBold: Style
    Teal3SolidBold: Style
    Teal3OutlineLight: Style
    Teal3SolidLight: Style
    Teal3Dashed: Style
    Teal3DashedBold: Style
    Teal3DashedLight: Style

    # teal4
    Teal4: Style
    Teal4Bordered: Style
    Teal4Bold: Style
    Teal4Light: Style
    Teal4Flat: Style
    Teal4Outline: Style
    Teal4Solid: Style
    Teal4OutlineBold: Style
    Teal4SolidBold: Style
    Teal4OutlineLight: Style
    Teal4SolidLight: Style
    Teal4Dashed: Style
    Teal4DashedBold: Style
    Teal4DashedLight: Style

    # teal5
    Teal5: Style
    Teal5Bordered: Style
    Teal5Bold: Style
    Teal5Light: Style
    Teal5Flat: Style
    Teal5Outline: Style
    Teal5Solid: Style
    Teal5OutlineBold: Style
    Teal5SolidBold: Style
    Teal5OutlineLight: Style
    Teal5SolidLight: Style
    Teal5Dashed: Style
    Teal5DashedBold: Style
    Teal5DashedLight: Style

    # teal6
    Teal6: Style
    Teal6Bordered: Style
    Teal6Bold: Style
    Teal6Light: Style
    Teal6Flat: Style
    Teal6Outline: Style
    Teal6Solid: Style
    Teal6OutlineBold: Style
    Teal6SolidBold: Style
    Teal6OutlineLight: Style
    Teal6SolidLight: Style
    Teal6Dashed: Style
    Teal6DashedBold: Style
    Teal6DashedLight: Style

    # pink1
    Pink1: Style
    Pink1Bordered: Style
    Pink1Bold: Style
    Pink1Light: Style
    Pink1Flat: Style
    Pink1Outline: Style
    Pink1Solid: Style
    Pink1OutlineBold: Style
    Pink1SolidBold: Style
    Pink1OutlineLight: Style
    Pink1SolidLight: Style
    Pink1Dashed: Style
    Pink1DashedBold: Style
    Pink1DashedLight: Style

    # pink2
    Pink2: Style
    Pink2Bordered: Style
    Pink2Bold: Style
    Pink2Light: Style
    Pink2Flat: Style
    Pink2Outline: Style
    Pink2Solid: Style
    Pink2OutlineBold: Style
    Pink2SolidBold: Style
    Pink2OutlineLight: Style
    Pink2SolidLight: Style
    Pink2Dashed: Style
    Pink2DashedBold: Style
    Pink2DashedLight: Style

    # pink3
    Pink3: Style
    Pink3Bordered: Style
    Pink3Bold: Style
    Pink3Light: Style
    Pink3Flat: Style
    Pink3Outline: Style
    Pink3Solid: Style
    Pink3OutlineBold: Style
    Pink3SolidBold: Style
    Pink3OutlineLight: Style
    Pink3SolidLight: Style
    Pink3Dashed: Style
    Pink3DashedBold: Style
    Pink3DashedLight: Style

    # pink4
    Pink4: Style
    Pink4Bordered: Style
    Pink4Bold: Style
    Pink4Light: Style
    Pink4Flat: Style
    Pink4Outline: Style
    Pink4Solid: Style
    Pink4OutlineBold: Style
    Pink4SolidBold: Style
    Pink4OutlineLight: Style
    Pink4SolidLight: Style
    Pink4Dashed: Style
    Pink4DashedBold: Style
    Pink4DashedLight: Style

    # pink5
    Pink5: Style
    Pink5Bordered: Style
    Pink5Bold: Style
    Pink5Light: Style
    Pink5Flat: Style
    Pink5Outline: Style
    Pink5Solid: Style
    Pink5OutlineBold: Style
    Pink5SolidBold: Style
    Pink5OutlineLight: Style
    Pink5SolidLight: Style
    Pink5Dashed: Style
    Pink5DashedBold: Style
    Pink5DashedLight: Style

    # pink6
    Pink6: Style
    Pink6Bordered: Style
    Pink6Bold: Style
    Pink6Light: Style
    Pink6Flat: Style
    Pink6Outline: Style
    Pink6Solid: Style
    Pink6OutlineBold: Style
    Pink6SolidBold: Style
    Pink6OutlineLight: Style
    Pink6SolidLight: Style
    Pink6Dashed: Style
    Pink6DashedBold: Style
    Pink6DashedLight: Style

    # =========================================================================
    # Neutrals
    # =========================================================================
    # white
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

    # gray1
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

    # gray2
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

    # gray3
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

    # gray4
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

    # gray5
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

    # gray6
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

    # gray7
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

    # gray8
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

    # black
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

    # =========================================================================
    # Classic Primaries
    # =========================================================================
    # red
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

    # green
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

    # blue
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

    # yellow
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

    # orange
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

    # purple
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

    # pink
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

    # cyan
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

    # magenta
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

    # lime
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

    # teal
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

    # navy
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

    # olive
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

    # brown
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

    # gold
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

    # aqua
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

    # green_yellow
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

    # ivory
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

    # steel
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

    # Canvas
    Canvas: Style
    CanvasFlat: Style

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
        Primary: Style | None = None,
        PrimaryBordered: Style | None = None,
        PrimaryBold: Style | None = None,
        PrimaryLight: Style | None = None,
        PrimaryFlat: Style | None = None,
        PrimaryOutline: Style | None = None,
        PrimarySolid: Style | None = None,
        PrimaryOutlineBold: Style | None = None,
        PrimarySolidBold: Style | None = None,
        PrimaryOutlineLight: Style | None = None,
        PrimarySolidLight: Style | None = None,
        PrimaryDashed: Style | None = None,
        PrimaryDashedBold: Style | None = None,
        PrimaryDashedLight: Style | None = None,
        Secondary: Style | None = None,
        SecondaryBordered: Style | None = None,
        SecondaryBold: Style | None = None,
        SecondaryLight: Style | None = None,
        SecondaryFlat: Style | None = None,
        SecondaryOutline: Style | None = None,
        SecondarySolid: Style | None = None,
        SecondaryOutlineBold: Style | None = None,
        SecondarySolidBold: Style | None = None,
        SecondaryOutlineLight: Style | None = None,
        SecondarySolidLight: Style | None = None,
        SecondaryDashed: Style | None = None,
        SecondaryDashedBold: Style | None = None,
        SecondaryDashedLight: Style | None = None,
        Accent: Style | None = None,
        AccentBordered: Style | None = None,
        AccentBold: Style | None = None,
        AccentLight: Style | None = None,
        AccentFlat: Style | None = None,
        AccentOutline: Style | None = None,
        AccentSolid: Style | None = None,
        AccentOutlineBold: Style | None = None,
        AccentSolidBold: Style | None = None,
        AccentOutlineLight: Style | None = None,
        AccentSolidLight: Style | None = None,
        AccentDashed: Style | None = None,
        AccentDashedBold: Style | None = None,
        AccentDashedLight: Style | None = None,
        Muted: Style | None = None,
        MutedBordered: Style | None = None,
        MutedBold: Style | None = None,
        MutedLight: Style | None = None,
        MutedFlat: Style | None = None,
        MutedOutline: Style | None = None,
        MutedSolid: Style | None = None,
        MutedOutlineBold: Style | None = None,
        MutedSolidBold: Style | None = None,
        MutedOutlineLight: Style | None = None,
        MutedSolidLight: Style | None = None,
        MutedDashed: Style | None = None,
        MutedDashedBold: Style | None = None,
        MutedDashedLight: Style | None = None,
        Light: Style | None = None,
        LightBordered: Style | None = None,
        LightBold: Style | None = None,
        LightLight: Style | None = None,
        LightFlat: Style | None = None,
        LightOutline: Style | None = None,
        LightSolid: Style | None = None,
        LightOutlineBold: Style | None = None,
        LightSolidBold: Style | None = None,
        LightOutlineLight: Style | None = None,
        LightSolidLight: Style | None = None,
        LightDashed: Style | None = None,
        LightDashedBold: Style | None = None,
        LightDashedLight: Style | None = None,
        Dark: Style | None = None,
        DarkBordered: Style | None = None,
        DarkBold: Style | None = None,
        DarkLight: Style | None = None,
        DarkFlat: Style | None = None,
        DarkOutline: Style | None = None,
        DarkSolid: Style | None = None,
        DarkOutlineBold: Style | None = None,
        DarkSolidBold: Style | None = None,
        DarkOutlineLight: Style | None = None,
        DarkSolidLight: Style | None = None,
        DarkDashed: Style | None = None,
        DarkDashedBold: Style | None = None,
        DarkDashedLight: Style | None = None,
        Danger: Style | None = None,
        DangerBordered: Style | None = None,
        DangerBold: Style | None = None,
        DangerLight: Style | None = None,
        DangerFlat: Style | None = None,
        DangerOutline: Style | None = None,
        DangerSolid: Style | None = None,
        DangerOutlineBold: Style | None = None,
        DangerSolidBold: Style | None = None,
        DangerOutlineLight: Style | None = None,
        DangerSolidLight: Style | None = None,
        DangerDashed: Style | None = None,
        DangerDashedBold: Style | None = None,
        DangerDashedLight: Style | None = None,
        Success: Style | None = None,
        SuccessBordered: Style | None = None,
        SuccessBold: Style | None = None,
        SuccessLight: Style | None = None,
        SuccessFlat: Style | None = None,
        SuccessOutline: Style | None = None,
        SuccessSolid: Style | None = None,
        SuccessOutlineBold: Style | None = None,
        SuccessSolidBold: Style | None = None,
        SuccessOutlineLight: Style | None = None,
        SuccessSolidLight: Style | None = None,
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
        Amber1: Style | None = None,
        Amber1Bordered: Style | None = None,
        Amber1Bold: Style | None = None,
        Amber1Light: Style | None = None,
        Amber1Flat: Style | None = None,
        Amber1Outline: Style | None = None,
        Amber1Solid: Style | None = None,
        Amber1OutlineBold: Style | None = None,
        Amber1SolidBold: Style | None = None,
        Amber1OutlineLight: Style | None = None,
        Amber1SolidLight: Style | None = None,
        Amber1Dashed: Style | None = None,
        Amber1DashedBold: Style | None = None,
        Amber1DashedLight: Style | None = None,
        Amber2: Style | None = None,
        Amber2Bordered: Style | None = None,
        Amber2Bold: Style | None = None,
        Amber2Light: Style | None = None,
        Amber2Flat: Style | None = None,
        Amber2Outline: Style | None = None,
        Amber2Solid: Style | None = None,
        Amber2OutlineBold: Style | None = None,
        Amber2SolidBold: Style | None = None,
        Amber2OutlineLight: Style | None = None,
        Amber2SolidLight: Style | None = None,
        Amber2Dashed: Style | None = None,
        Amber2DashedBold: Style | None = None,
        Amber2DashedLight: Style | None = None,
        Amber3: Style | None = None,
        Amber3Bordered: Style | None = None,
        Amber3Bold: Style | None = None,
        Amber3Light: Style | None = None,
        Amber3Flat: Style | None = None,
        Amber3Outline: Style | None = None,
        Amber3Solid: Style | None = None,
        Amber3OutlineBold: Style | None = None,
        Amber3SolidBold: Style | None = None,
        Amber3OutlineLight: Style | None = None,
        Amber3SolidLight: Style | None = None,
        Amber3Dashed: Style | None = None,
        Amber3DashedBold: Style | None = None,
        Amber3DashedLight: Style | None = None,
        Amber4: Style | None = None,
        Amber4Bordered: Style | None = None,
        Amber4Bold: Style | None = None,
        Amber4Light: Style | None = None,
        Amber4Flat: Style | None = None,
        Amber4Outline: Style | None = None,
        Amber4Solid: Style | None = None,
        Amber4OutlineBold: Style | None = None,
        Amber4SolidBold: Style | None = None,
        Amber4OutlineLight: Style | None = None,
        Amber4SolidLight: Style | None = None,
        Amber4Dashed: Style | None = None,
        Amber4DashedBold: Style | None = None,
        Amber4DashedLight: Style | None = None,
        Amber5: Style | None = None,
        Amber5Bordered: Style | None = None,
        Amber5Bold: Style | None = None,
        Amber5Light: Style | None = None,
        Amber5Flat: Style | None = None,
        Amber5Outline: Style | None = None,
        Amber5Solid: Style | None = None,
        Amber5OutlineBold: Style | None = None,
        Amber5SolidBold: Style | None = None,
        Amber5OutlineLight: Style | None = None,
        Amber5SolidLight: Style | None = None,
        Amber5Dashed: Style | None = None,
        Amber5DashedBold: Style | None = None,
        Amber5DashedLight: Style | None = None,
        Amber6: Style | None = None,
        Amber6Bordered: Style | None = None,
        Amber6Bold: Style | None = None,
        Amber6Light: Style | None = None,
        Amber6Flat: Style | None = None,
        Amber6Outline: Style | None = None,
        Amber6Solid: Style | None = None,
        Amber6OutlineBold: Style | None = None,
        Amber6SolidBold: Style | None = None,
        Amber6OutlineLight: Style | None = None,
        Amber6SolidLight: Style | None = None,
        Amber6Dashed: Style | None = None,
        Amber6DashedBold: Style | None = None,
        Amber6DashedLight: Style | None = None,
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
        Teal1: Style | None = None,
        Teal1Bordered: Style | None = None,
        Teal1Bold: Style | None = None,
        Teal1Light: Style | None = None,
        Teal1Flat: Style | None = None,
        Teal1Outline: Style | None = None,
        Teal1Solid: Style | None = None,
        Teal1OutlineBold: Style | None = None,
        Teal1SolidBold: Style | None = None,
        Teal1OutlineLight: Style | None = None,
        Teal1SolidLight: Style | None = None,
        Teal1Dashed: Style | None = None,
        Teal1DashedBold: Style | None = None,
        Teal1DashedLight: Style | None = None,
        Teal2: Style | None = None,
        Teal2Bordered: Style | None = None,
        Teal2Bold: Style | None = None,
        Teal2Light: Style | None = None,
        Teal2Flat: Style | None = None,
        Teal2Outline: Style | None = None,
        Teal2Solid: Style | None = None,
        Teal2OutlineBold: Style | None = None,
        Teal2SolidBold: Style | None = None,
        Teal2OutlineLight: Style | None = None,
        Teal2SolidLight: Style | None = None,
        Teal2Dashed: Style | None = None,
        Teal2DashedBold: Style | None = None,
        Teal2DashedLight: Style | None = None,
        Teal3: Style | None = None,
        Teal3Bordered: Style | None = None,
        Teal3Bold: Style | None = None,
        Teal3Light: Style | None = None,
        Teal3Flat: Style | None = None,
        Teal3Outline: Style | None = None,
        Teal3Solid: Style | None = None,
        Teal3OutlineBold: Style | None = None,
        Teal3SolidBold: Style | None = None,
        Teal3OutlineLight: Style | None = None,
        Teal3SolidLight: Style | None = None,
        Teal3Dashed: Style | None = None,
        Teal3DashedBold: Style | None = None,
        Teal3DashedLight: Style | None = None,
        Teal4: Style | None = None,
        Teal4Bordered: Style | None = None,
        Teal4Bold: Style | None = None,
        Teal4Light: Style | None = None,
        Teal4Flat: Style | None = None,
        Teal4Outline: Style | None = None,
        Teal4Solid: Style | None = None,
        Teal4OutlineBold: Style | None = None,
        Teal4SolidBold: Style | None = None,
        Teal4OutlineLight: Style | None = None,
        Teal4SolidLight: Style | None = None,
        Teal4Dashed: Style | None = None,
        Teal4DashedBold: Style | None = None,
        Teal4DashedLight: Style | None = None,
        Teal5: Style | None = None,
        Teal5Bordered: Style | None = None,
        Teal5Bold: Style | None = None,
        Teal5Light: Style | None = None,
        Teal5Flat: Style | None = None,
        Teal5Outline: Style | None = None,
        Teal5Solid: Style | None = None,
        Teal5OutlineBold: Style | None = None,
        Teal5SolidBold: Style | None = None,
        Teal5OutlineLight: Style | None = None,
        Teal5SolidLight: Style | None = None,
        Teal5Dashed: Style | None = None,
        Teal5DashedBold: Style | None = None,
        Teal5DashedLight: Style | None = None,
        Teal6: Style | None = None,
        Teal6Bordered: Style | None = None,
        Teal6Bold: Style | None = None,
        Teal6Light: Style | None = None,
        Teal6Flat: Style | None = None,
        Teal6Outline: Style | None = None,
        Teal6Solid: Style | None = None,
        Teal6OutlineBold: Style | None = None,
        Teal6SolidBold: Style | None = None,
        Teal6OutlineLight: Style | None = None,
        Teal6SolidLight: Style | None = None,
        Teal6Dashed: Style | None = None,
        Teal6DashedBold: Style | None = None,
        Teal6DashedLight: Style | None = None,
        Pink1: Style | None = None,
        Pink1Bordered: Style | None = None,
        Pink1Bold: Style | None = None,
        Pink1Light: Style | None = None,
        Pink1Flat: Style | None = None,
        Pink1Outline: Style | None = None,
        Pink1Solid: Style | None = None,
        Pink1OutlineBold: Style | None = None,
        Pink1SolidBold: Style | None = None,
        Pink1OutlineLight: Style | None = None,
        Pink1SolidLight: Style | None = None,
        Pink1Dashed: Style | None = None,
        Pink1DashedBold: Style | None = None,
        Pink1DashedLight: Style | None = None,
        Pink2: Style | None = None,
        Pink2Bordered: Style | None = None,
        Pink2Bold: Style | None = None,
        Pink2Light: Style | None = None,
        Pink2Flat: Style | None = None,
        Pink2Outline: Style | None = None,
        Pink2Solid: Style | None = None,
        Pink2OutlineBold: Style | None = None,
        Pink2SolidBold: Style | None = None,
        Pink2OutlineLight: Style | None = None,
        Pink2SolidLight: Style | None = None,
        Pink2Dashed: Style | None = None,
        Pink2DashedBold: Style | None = None,
        Pink2DashedLight: Style | None = None,
        Pink3: Style | None = None,
        Pink3Bordered: Style | None = None,
        Pink3Bold: Style | None = None,
        Pink3Light: Style | None = None,
        Pink3Flat: Style | None = None,
        Pink3Outline: Style | None = None,
        Pink3Solid: Style | None = None,
        Pink3OutlineBold: Style | None = None,
        Pink3SolidBold: Style | None = None,
        Pink3OutlineLight: Style | None = None,
        Pink3SolidLight: Style | None = None,
        Pink3Dashed: Style | None = None,
        Pink3DashedBold: Style | None = None,
        Pink3DashedLight: Style | None = None,
        Pink4: Style | None = None,
        Pink4Bordered: Style | None = None,
        Pink4Bold: Style | None = None,
        Pink4Light: Style | None = None,
        Pink4Flat: Style | None = None,
        Pink4Outline: Style | None = None,
        Pink4Solid: Style | None = None,
        Pink4OutlineBold: Style | None = None,
        Pink4SolidBold: Style | None = None,
        Pink4OutlineLight: Style | None = None,
        Pink4SolidLight: Style | None = None,
        Pink4Dashed: Style | None = None,
        Pink4DashedBold: Style | None = None,
        Pink4DashedLight: Style | None = None,
        Pink5: Style | None = None,
        Pink5Bordered: Style | None = None,
        Pink5Bold: Style | None = None,
        Pink5Light: Style | None = None,
        Pink5Flat: Style | None = None,
        Pink5Outline: Style | None = None,
        Pink5Solid: Style | None = None,
        Pink5OutlineBold: Style | None = None,
        Pink5SolidBold: Style | None = None,
        Pink5OutlineLight: Style | None = None,
        Pink5SolidLight: Style | None = None,
        Pink5Dashed: Style | None = None,
        Pink5DashedBold: Style | None = None,
        Pink5DashedLight: Style | None = None,
        Pink6: Style | None = None,
        Pink6Bordered: Style | None = None,
        Pink6Bold: Style | None = None,
        Pink6Light: Style | None = None,
        Pink6Flat: Style | None = None,
        Pink6Outline: Style | None = None,
        Pink6Solid: Style | None = None,
        Pink6OutlineBold: Style | None = None,
        Pink6SolidBold: Style | None = None,
        Pink6OutlineLight: Style | None = None,
        Pink6SolidLight: Style | None = None,
        Pink6Dashed: Style | None = None,
        Pink6DashedBold: Style | None = None,
        Pink6DashedLight: Style | None = None,
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


class DefaultStyles1(DefaultStyles):
    """Default preset styles for Tone 1 (Ultra light pastel)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 1 instance."""
        super().__init__(**kwargs)


class DefaultStyles2(DefaultStyles):
    """Default preset styles for Tone 2 (Light / card background)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 2 instance."""
        super().__init__(**kwargs)


class DefaultStyles3(DefaultStyles):
    """Default preset styles for Tone 3 (Medium soft)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 3 instance."""
        super().__init__(**kwargs)


class DefaultStyles4(DefaultStyles):
    """Default preset styles for Tone 4 (Standard base / high contrast)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 4 instance."""
        super().__init__(**kwargs)


class DefaultStyles5(DefaultStyles):
    """Default preset styles for Tone 5 (Deep tone)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 5 instance."""
        super().__init__(**kwargs)


class DefaultStyles6(DefaultStyles):
    """Default preset styles for Tone 6 (Darkest shade)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default preset styles 6 instance."""
        super().__init__(**kwargs)


def _create_default_styles(  # noqa: C901, PLR0911
    theme: Literal["default", "1", "2", "3", "4", "5", "6"] = "default",
) -> DefaultStyles:
    """Generate default preset styles for the given theme variant.

    Args:
        theme: Theme variant to generate. Defaults to "default".

    Returns:
        DefaultStyles: Default preset styles instance.
    """
    if theme in {"default", "4"}:
        col = DefaultColors4
        theme_tone = 4
    elif theme == "1":
        col = DefaultColors1
        theme_tone = 1
    elif theme == "2":
        col = DefaultColors2
        theme_tone = 2
    elif theme == "3":
        col = DefaultColors3
        theme_tone = 3
    elif theme == "5":
        col = DefaultColors5
        theme_tone = 5
    elif theme == "6":
        col = DefaultColors6
        theme_tone = 6
    else:
        col = DefaultColors
        theme_tone = 4

    bg_col = (255, 255, 255, 1.0)

    # 1. Colors Map for all registered color names
    colors_map: dict[str, Any] = {
        "Blue1": col.Blue1,
        "Blue2": col.Blue2,
        "Blue3": col.Blue3,
        "Blue4": col.Blue4,
        "Blue5": col.Blue5,
        "Blue6": col.Blue6,
        "Green1": col.Green1,
        "Green2": col.Green2,
        "Green3": col.Green3,
        "Green4": col.Green4,
        "Green5": col.Green5,
        "Green6": col.Green6,
        "Red1": col.Red1,
        "Red2": col.Red2,
        "Red3": col.Red3,
        "Red4": col.Red4,
        "Red5": col.Red5,
        "Red6": col.Red6,
        "Orange1": col.Orange1,
        "Orange2": col.Orange2,
        "Orange3": col.Orange3,
        "Orange4": col.Orange4,
        "Orange5": col.Orange5,
        "Orange6": col.Orange6,
        "Amber1": col.Amber1,
        "Amber2": col.Amber2,
        "Amber3": col.Amber3,
        "Amber4": col.Amber4,
        "Amber5": col.Amber5,
        "Amber6": col.Amber6,
        "Purple1": col.Purple1,
        "Purple2": col.Purple2,
        "Purple3": col.Purple3,
        "Purple4": col.Purple4,
        "Purple5": col.Purple5,
        "Purple6": col.Purple6,
        "Teal1": col.Teal1,
        "Teal2": col.Teal2,
        "Teal3": col.Teal3,
        "Teal4": col.Teal4,
        "Teal5": col.Teal5,
        "Teal6": col.Teal6,
        "Pink1": col.Pink1,
        "Pink2": col.Pink2,
        "Pink3": col.Pink3,
        "Pink4": col.Pink4,
        "Pink5": col.Pink5,
        "Pink6": col.Pink6,
        "Primary1": col.Primary1,
        "Primary2": col.Primary2,
        "Primary3": col.Primary3,
        "Primary4": col.Primary4,
        "Primary5": col.Primary5,
        "Primary6": col.Primary6,
        "Secondary1": col.Secondary1,
        "Secondary2": col.Secondary2,
        "Secondary3": col.Secondary3,
        "Secondary4": col.Secondary4,
        "Secondary5": col.Secondary5,
        "Secondary6": col.Secondary6,
        "Accent1": col.Accent1,
        "Accent2": col.Accent2,
        "Accent3": col.Accent3,
        "Accent4": col.Accent4,
        "Accent5": col.Accent5,
        "Accent6": col.Accent6,
        "Muted1": col.Muted1,
        "Muted2": col.Muted2,
        "Muted3": col.Muted3,
        "Muted4": col.Muted4,
        "Muted5": col.Muted5,
        "Muted6": col.Muted6,
        "Danger1": col.Danger1,
        "Danger2": col.Danger2,
        "Danger3": col.Danger3,
        "Danger4": col.Danger4,
        "Danger5": col.Danger5,
        "Danger6": col.Danger6,
        "Success1": col.Success1,
        "Success2": col.Success2,
        "Success3": col.Success3,
        "Success4": col.Success4,
        "Success5": col.Success5,
        "Success6": col.Success6,
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
        "Red": col.Red,
        "Green": col.Green,
        "Blue": col.Blue,
        "Yellow": col.Yellow,
        "Orange": col.Orange,
        "Purple": col.Purple,
        "Pink": col.Pink,
        "Cyan": col.Cyan,
        "Magenta": col.Magenta,
        "Lime": col.Lime,
        "Teal": col.Teal,
        "Navy": col.Navy,
        "Olive": col.Olive,
        "Brown": col.Brown,
        "Gold": col.Gold,
        "Aqua": col.Aqua,
        "GreenYellow": col.GreenYellow,
        "Ivory": col.Ivory,
        "Steel": col.Steel,
    }

    # 2. Semantic Roles Map
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

    styles_dict: dict[str, Any] = {
        "width": 140,
        "height": 70,
        "dpi": 100,
        "colors": col,
        "background_color": bg_col,
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
    }

    for role_name, color in semantic_map.items():
        if color is not None:
            if role_name == "Muted":
                text_col = col.White if theme_tone >= 5 else col.Dark
                v = _make_variants(
                    color,
                    border_color=col.Gray5,
                    default_text_color=text_col,
                    line_color=col.Gray4,
                )
            elif role_name == "Light":
                v = _make_variants(
                    color,
                    border_color=col.Gray4,
                    default_text_color=col.Gray7,
                    line_color=col.Gray4,
                )
            elif role_name == "Dark":
                v = _make_variants(
                    color,
                    border_color=col.Gray4,
                    default_text_color=col.White,
                    line_color=col.Gray4,
                )
            else:
                v = _make_variants(color)

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

    for cname, color in colors_map.items():
        v = _make_variants(color)
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

    if theme == "1":
        return DefaultStyles1(**styles_dict)
    elif theme in {"2", "light"}:
        return DefaultStyles2(**styles_dict)
    elif theme == "3":
        return DefaultStyles3(**styles_dict)
    elif theme == "4":
        return DefaultStyles4(**styles_dict)
    elif theme in {"5", "dark"}:
        return DefaultStyles5(**styles_dict)
    elif theme == "6":
        return DefaultStyles6(**styles_dict)
    return DefaultStyles(**styles_dict)


_default_styles: DefaultStyles = _create_default_styles("default")
_default_styles1: DefaultStyles1 = _create_default_styles("1")  # type: ignore
_default_styles2: DefaultStyles2 = _create_default_styles("2")  # type: ignore
_default_styles3: DefaultStyles3 = _create_default_styles("3")  # type: ignore
_default_styles4: DefaultStyles4 = _create_default_styles("4")  # type: ignore
_default_styles5: DefaultStyles5 = _create_default_styles("5")  # type: ignore
_default_styles6: DefaultStyles6 = _create_default_styles("6")  # type: ignore

DefaultStyles.register_default_instance(_default_styles)
DefaultStyles1.register_default_instance(_default_styles1)
DefaultStyles2.register_default_instance(_default_styles2)
DefaultStyles3.register_default_instance(_default_styles3)
DefaultStyles4.register_default_instance(_default_styles4)
DefaultStyles5.register_default_instance(_default_styles5)
DefaultStyles6.register_default_instance(_default_styles6)

__all__ = [
    "DefaultStyles",
    "DefaultStyles1",
    "DefaultStyles2",
    "DefaultStyles3",
    "DefaultStyles4",
    "DefaultStyles5",
    "DefaultStyles6",
]
