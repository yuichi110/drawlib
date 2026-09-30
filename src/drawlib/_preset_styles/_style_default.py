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

from drawlib._core.fonts import FontSourceCode
from drawlib._core.styles import BaseStyles
from drawlib._core.types import Style
from drawlib._preset_colors import (
    DefaultColors,
    DefaultColors1,
    DefaultColors2,
    DefaultColors3,
    DefaultColors4,
    DefaultColors5,
    DefaultColors6,
    DefaultDarkColors,
    DefaultLightColors,
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
    primary: Style
    primary_bordered: Style
    primary_bold: Style
    primary_light: Style
    primary_flat: Style
    primary_outline: Style
    primary_solid: Style
    primary_outline_bold: Style
    primary_solid_bold: Style
    primary_outline_light: Style
    primary_solid_light: Style
    primary_dashed: Style
    primary_dashed_bold: Style
    primary_dashed_light: Style

    # secondary
    secondary: Style
    secondary_bordered: Style
    secondary_bold: Style
    secondary_light: Style
    secondary_flat: Style
    secondary_outline: Style
    secondary_solid: Style
    secondary_outline_bold: Style
    secondary_solid_bold: Style
    secondary_outline_light: Style
    secondary_solid_light: Style
    secondary_dashed: Style
    secondary_dashed_bold: Style
    secondary_dashed_light: Style

    # accent
    accent: Style
    accent_bordered: Style
    accent_bold: Style
    accent_light: Style
    accent_flat: Style
    accent_outline: Style
    accent_solid: Style
    accent_outline_bold: Style
    accent_solid_bold: Style
    accent_outline_light: Style
    accent_solid_light: Style
    accent_dashed: Style
    accent_dashed_bold: Style
    accent_dashed_light: Style

    # muted
    muted: Style
    muted_bordered: Style
    muted_bold: Style
    muted_light: Style
    muted_flat: Style
    muted_outline: Style
    muted_solid: Style
    muted_outline_bold: Style
    muted_solid_bold: Style
    muted_outline_light: Style
    muted_solid_light: Style
    muted_dashed: Style
    muted_dashed_bold: Style
    muted_dashed_light: Style

    # light
    light: Style
    light_bordered: Style
    light_bold: Style
    light_light: Style
    light_flat: Style
    light_outline: Style
    light_solid: Style
    light_outline_bold: Style
    light_solid_bold: Style
    light_outline_light: Style
    light_solid_light: Style
    light_dashed: Style
    light_dashed_bold: Style
    light_dashed_light: Style

    # dark
    dark: Style
    dark_bordered: Style
    dark_bold: Style
    dark_light: Style
    dark_flat: Style
    dark_outline: Style
    dark_solid: Style
    dark_outline_bold: Style
    dark_solid_bold: Style
    dark_outline_light: Style
    dark_solid_light: Style
    dark_dashed: Style
    dark_dashed_bold: Style
    dark_dashed_light: Style

    # danger
    danger: Style
    danger_bordered: Style
    danger_bold: Style
    danger_light: Style
    danger_flat: Style
    danger_outline: Style
    danger_solid: Style
    danger_outline_bold: Style
    danger_solid_bold: Style
    danger_outline_light: Style
    danger_solid_light: Style
    danger_dashed: Style
    danger_dashed_bold: Style
    danger_dashed_light: Style

    # success
    success: Style
    success_bordered: Style
    success_bold: Style
    success_light: Style
    success_flat: Style
    success_outline: Style
    success_solid: Style
    success_outline_bold: Style
    success_solid_bold: Style
    success_outline_light: Style
    success_solid_light: Style
    success_dashed: Style
    success_dashed_bold: Style
    success_dashed_light: Style

    # =========================================================================
    # Numbered Semantic Roles
    # =========================================================================
    # primary1
    primary1: Style
    primary1_bordered: Style
    primary1_bold: Style
    primary1_light: Style
    primary1_flat: Style
    primary1_outline: Style
    primary1_solid: Style
    primary1_outline_bold: Style
    primary1_solid_bold: Style
    primary1_outline_light: Style
    primary1_solid_light: Style
    primary1_dashed: Style
    primary1_dashed_bold: Style
    primary1_dashed_light: Style

    # primary2
    primary2: Style
    primary2_bordered: Style
    primary2_bold: Style
    primary2_light: Style
    primary2_flat: Style
    primary2_outline: Style
    primary2_solid: Style
    primary2_outline_bold: Style
    primary2_solid_bold: Style
    primary2_outline_light: Style
    primary2_solid_light: Style
    primary2_dashed: Style
    primary2_dashed_bold: Style
    primary2_dashed_light: Style

    # primary3
    primary3: Style
    primary3_bordered: Style
    primary3_bold: Style
    primary3_light: Style
    primary3_flat: Style
    primary3_outline: Style
    primary3_solid: Style
    primary3_outline_bold: Style
    primary3_solid_bold: Style
    primary3_outline_light: Style
    primary3_solid_light: Style
    primary3_dashed: Style
    primary3_dashed_bold: Style
    primary3_dashed_light: Style

    # primary4
    primary4: Style
    primary4_bordered: Style
    primary4_bold: Style
    primary4_light: Style
    primary4_flat: Style
    primary4_outline: Style
    primary4_solid: Style
    primary4_outline_bold: Style
    primary4_solid_bold: Style
    primary4_outline_light: Style
    primary4_solid_light: Style
    primary4_dashed: Style
    primary4_dashed_bold: Style
    primary4_dashed_light: Style

    # primary5
    primary5: Style
    primary5_bordered: Style
    primary5_bold: Style
    primary5_light: Style
    primary5_flat: Style
    primary5_outline: Style
    primary5_solid: Style
    primary5_outline_bold: Style
    primary5_solid_bold: Style
    primary5_outline_light: Style
    primary5_solid_light: Style
    primary5_dashed: Style
    primary5_dashed_bold: Style
    primary5_dashed_light: Style

    # primary6
    primary6: Style
    primary6_bordered: Style
    primary6_bold: Style
    primary6_light: Style
    primary6_flat: Style
    primary6_outline: Style
    primary6_solid: Style
    primary6_outline_bold: Style
    primary6_solid_bold: Style
    primary6_outline_light: Style
    primary6_solid_light: Style
    primary6_dashed: Style
    primary6_dashed_bold: Style
    primary6_dashed_light: Style

    # secondary1
    secondary1: Style
    secondary1_bordered: Style
    secondary1_bold: Style
    secondary1_light: Style
    secondary1_flat: Style
    secondary1_outline: Style
    secondary1_solid: Style
    secondary1_outline_bold: Style
    secondary1_solid_bold: Style
    secondary1_outline_light: Style
    secondary1_solid_light: Style
    secondary1_dashed: Style
    secondary1_dashed_bold: Style
    secondary1_dashed_light: Style

    # secondary2
    secondary2: Style
    secondary2_bordered: Style
    secondary2_bold: Style
    secondary2_light: Style
    secondary2_flat: Style
    secondary2_outline: Style
    secondary2_solid: Style
    secondary2_outline_bold: Style
    secondary2_solid_bold: Style
    secondary2_outline_light: Style
    secondary2_solid_light: Style
    secondary2_dashed: Style
    secondary2_dashed_bold: Style
    secondary2_dashed_light: Style

    # secondary3
    secondary3: Style
    secondary3_bordered: Style
    secondary3_bold: Style
    secondary3_light: Style
    secondary3_flat: Style
    secondary3_outline: Style
    secondary3_solid: Style
    secondary3_outline_bold: Style
    secondary3_solid_bold: Style
    secondary3_outline_light: Style
    secondary3_solid_light: Style
    secondary3_dashed: Style
    secondary3_dashed_bold: Style
    secondary3_dashed_light: Style

    # secondary4
    secondary4: Style
    secondary4_bordered: Style
    secondary4_bold: Style
    secondary4_light: Style
    secondary4_flat: Style
    secondary4_outline: Style
    secondary4_solid: Style
    secondary4_outline_bold: Style
    secondary4_solid_bold: Style
    secondary4_outline_light: Style
    secondary4_solid_light: Style
    secondary4_dashed: Style
    secondary4_dashed_bold: Style
    secondary4_dashed_light: Style

    # secondary5
    secondary5: Style
    secondary5_bordered: Style
    secondary5_bold: Style
    secondary5_light: Style
    secondary5_flat: Style
    secondary5_outline: Style
    secondary5_solid: Style
    secondary5_outline_bold: Style
    secondary5_solid_bold: Style
    secondary5_outline_light: Style
    secondary5_solid_light: Style
    secondary5_dashed: Style
    secondary5_dashed_bold: Style
    secondary5_dashed_light: Style

    # secondary6
    secondary6: Style
    secondary6_bordered: Style
    secondary6_bold: Style
    secondary6_light: Style
    secondary6_flat: Style
    secondary6_outline: Style
    secondary6_solid: Style
    secondary6_outline_bold: Style
    secondary6_solid_bold: Style
    secondary6_outline_light: Style
    secondary6_solid_light: Style
    secondary6_dashed: Style
    secondary6_dashed_bold: Style
    secondary6_dashed_light: Style

    # accent1
    accent1: Style
    accent1_bordered: Style
    accent1_bold: Style
    accent1_light: Style
    accent1_flat: Style
    accent1_outline: Style
    accent1_solid: Style
    accent1_outline_bold: Style
    accent1_solid_bold: Style
    accent1_outline_light: Style
    accent1_solid_light: Style
    accent1_dashed: Style
    accent1_dashed_bold: Style
    accent1_dashed_light: Style

    # accent2
    accent2: Style
    accent2_bordered: Style
    accent2_bold: Style
    accent2_light: Style
    accent2_flat: Style
    accent2_outline: Style
    accent2_solid: Style
    accent2_outline_bold: Style
    accent2_solid_bold: Style
    accent2_outline_light: Style
    accent2_solid_light: Style
    accent2_dashed: Style
    accent2_dashed_bold: Style
    accent2_dashed_light: Style

    # accent3
    accent3: Style
    accent3_bordered: Style
    accent3_bold: Style
    accent3_light: Style
    accent3_flat: Style
    accent3_outline: Style
    accent3_solid: Style
    accent3_outline_bold: Style
    accent3_solid_bold: Style
    accent3_outline_light: Style
    accent3_solid_light: Style
    accent3_dashed: Style
    accent3_dashed_bold: Style
    accent3_dashed_light: Style

    # accent4
    accent4: Style
    accent4_bordered: Style
    accent4_bold: Style
    accent4_light: Style
    accent4_flat: Style
    accent4_outline: Style
    accent4_solid: Style
    accent4_outline_bold: Style
    accent4_solid_bold: Style
    accent4_outline_light: Style
    accent4_solid_light: Style
    accent4_dashed: Style
    accent4_dashed_bold: Style
    accent4_dashed_light: Style

    # accent5
    accent5: Style
    accent5_bordered: Style
    accent5_bold: Style
    accent5_light: Style
    accent5_flat: Style
    accent5_outline: Style
    accent5_solid: Style
    accent5_outline_bold: Style
    accent5_solid_bold: Style
    accent5_outline_light: Style
    accent5_solid_light: Style
    accent5_dashed: Style
    accent5_dashed_bold: Style
    accent5_dashed_light: Style

    # accent6
    accent6: Style
    accent6_bordered: Style
    accent6_bold: Style
    accent6_light: Style
    accent6_flat: Style
    accent6_outline: Style
    accent6_solid: Style
    accent6_outline_bold: Style
    accent6_solid_bold: Style
    accent6_outline_light: Style
    accent6_solid_light: Style
    accent6_dashed: Style
    accent6_dashed_bold: Style
    accent6_dashed_light: Style

    # muted1
    muted1: Style
    muted1_bordered: Style
    muted1_bold: Style
    muted1_light: Style
    muted1_flat: Style
    muted1_outline: Style
    muted1_solid: Style
    muted1_outline_bold: Style
    muted1_solid_bold: Style
    muted1_outline_light: Style
    muted1_solid_light: Style
    muted1_dashed: Style
    muted1_dashed_bold: Style
    muted1_dashed_light: Style

    # muted2
    muted2: Style
    muted2_bordered: Style
    muted2_bold: Style
    muted2_light: Style
    muted2_flat: Style
    muted2_outline: Style
    muted2_solid: Style
    muted2_outline_bold: Style
    muted2_solid_bold: Style
    muted2_outline_light: Style
    muted2_solid_light: Style
    muted2_dashed: Style
    muted2_dashed_bold: Style
    muted2_dashed_light: Style

    # muted3
    muted3: Style
    muted3_bordered: Style
    muted3_bold: Style
    muted3_light: Style
    muted3_flat: Style
    muted3_outline: Style
    muted3_solid: Style
    muted3_outline_bold: Style
    muted3_solid_bold: Style
    muted3_outline_light: Style
    muted3_solid_light: Style
    muted3_dashed: Style
    muted3_dashed_bold: Style
    muted3_dashed_light: Style

    # muted4
    muted4: Style
    muted4_bordered: Style
    muted4_bold: Style
    muted4_light: Style
    muted4_flat: Style
    muted4_outline: Style
    muted4_solid: Style
    muted4_outline_bold: Style
    muted4_solid_bold: Style
    muted4_outline_light: Style
    muted4_solid_light: Style
    muted4_dashed: Style
    muted4_dashed_bold: Style
    muted4_dashed_light: Style

    # muted5
    muted5: Style
    muted5_bordered: Style
    muted5_bold: Style
    muted5_light: Style
    muted5_flat: Style
    muted5_outline: Style
    muted5_solid: Style
    muted5_outline_bold: Style
    muted5_solid_bold: Style
    muted5_outline_light: Style
    muted5_solid_light: Style
    muted5_dashed: Style
    muted5_dashed_bold: Style
    muted5_dashed_light: Style

    # muted6
    muted6: Style
    muted6_bordered: Style
    muted6_bold: Style
    muted6_light: Style
    muted6_flat: Style
    muted6_outline: Style
    muted6_solid: Style
    muted6_outline_bold: Style
    muted6_solid_bold: Style
    muted6_outline_light: Style
    muted6_solid_light: Style
    muted6_dashed: Style
    muted6_dashed_bold: Style
    muted6_dashed_light: Style

    # danger1
    danger1: Style
    danger1_bordered: Style
    danger1_bold: Style
    danger1_light: Style
    danger1_flat: Style
    danger1_outline: Style
    danger1_solid: Style
    danger1_outline_bold: Style
    danger1_solid_bold: Style
    danger1_outline_light: Style
    danger1_solid_light: Style
    danger1_dashed: Style
    danger1_dashed_bold: Style
    danger1_dashed_light: Style

    # danger2
    danger2: Style
    danger2_bordered: Style
    danger2_bold: Style
    danger2_light: Style
    danger2_flat: Style
    danger2_outline: Style
    danger2_solid: Style
    danger2_outline_bold: Style
    danger2_solid_bold: Style
    danger2_outline_light: Style
    danger2_solid_light: Style
    danger2_dashed: Style
    danger2_dashed_bold: Style
    danger2_dashed_light: Style

    # danger3
    danger3: Style
    danger3_bordered: Style
    danger3_bold: Style
    danger3_light: Style
    danger3_flat: Style
    danger3_outline: Style
    danger3_solid: Style
    danger3_outline_bold: Style
    danger3_solid_bold: Style
    danger3_outline_light: Style
    danger3_solid_light: Style
    danger3_dashed: Style
    danger3_dashed_bold: Style
    danger3_dashed_light: Style

    # danger4
    danger4: Style
    danger4_bordered: Style
    danger4_bold: Style
    danger4_light: Style
    danger4_flat: Style
    danger4_outline: Style
    danger4_solid: Style
    danger4_outline_bold: Style
    danger4_solid_bold: Style
    danger4_outline_light: Style
    danger4_solid_light: Style
    danger4_dashed: Style
    danger4_dashed_bold: Style
    danger4_dashed_light: Style

    # danger5
    danger5: Style
    danger5_bordered: Style
    danger5_bold: Style
    danger5_light: Style
    danger5_flat: Style
    danger5_outline: Style
    danger5_solid: Style
    danger5_outline_bold: Style
    danger5_solid_bold: Style
    danger5_outline_light: Style
    danger5_solid_light: Style
    danger5_dashed: Style
    danger5_dashed_bold: Style
    danger5_dashed_light: Style

    # danger6
    danger6: Style
    danger6_bordered: Style
    danger6_bold: Style
    danger6_light: Style
    danger6_flat: Style
    danger6_outline: Style
    danger6_solid: Style
    danger6_outline_bold: Style
    danger6_solid_bold: Style
    danger6_outline_light: Style
    danger6_solid_light: Style
    danger6_dashed: Style
    danger6_dashed_bold: Style
    danger6_dashed_light: Style

    # success1
    success1: Style
    success1_bordered: Style
    success1_bold: Style
    success1_light: Style
    success1_flat: Style
    success1_outline: Style
    success1_solid: Style
    success1_outline_bold: Style
    success1_solid_bold: Style
    success1_outline_light: Style
    success1_solid_light: Style
    success1_dashed: Style
    success1_dashed_bold: Style
    success1_dashed_light: Style

    # success2
    success2: Style
    success2_bordered: Style
    success2_bold: Style
    success2_light: Style
    success2_flat: Style
    success2_outline: Style
    success2_solid: Style
    success2_outline_bold: Style
    success2_solid_bold: Style
    success2_outline_light: Style
    success2_solid_light: Style
    success2_dashed: Style
    success2_dashed_bold: Style
    success2_dashed_light: Style

    # success3
    success3: Style
    success3_bordered: Style
    success3_bold: Style
    success3_light: Style
    success3_flat: Style
    success3_outline: Style
    success3_solid: Style
    success3_outline_bold: Style
    success3_solid_bold: Style
    success3_outline_light: Style
    success3_solid_light: Style
    success3_dashed: Style
    success3_dashed_bold: Style
    success3_dashed_light: Style

    # success4
    success4: Style
    success4_bordered: Style
    success4_bold: Style
    success4_light: Style
    success4_flat: Style
    success4_outline: Style
    success4_solid: Style
    success4_outline_bold: Style
    success4_solid_bold: Style
    success4_outline_light: Style
    success4_solid_light: Style
    success4_dashed: Style
    success4_dashed_bold: Style
    success4_dashed_light: Style

    # success5
    success5: Style
    success5_bordered: Style
    success5_bold: Style
    success5_light: Style
    success5_flat: Style
    success5_outline: Style
    success5_solid: Style
    success5_outline_bold: Style
    success5_solid_bold: Style
    success5_outline_light: Style
    success5_solid_light: Style
    success5_dashed: Style
    success5_dashed_bold: Style
    success5_dashed_light: Style

    # success6
    success6: Style
    success6_bordered: Style
    success6_bold: Style
    success6_light: Style
    success6_flat: Style
    success6_outline: Style
    success6_solid: Style
    success6_outline_bold: Style
    success6_solid_bold: Style
    success6_outline_light: Style
    success6_solid_light: Style
    success6_dashed: Style
    success6_dashed_bold: Style
    success6_dashed_light: Style

    # =========================================================================
    # 6-Tone Hues
    # =========================================================================
    # blue1
    blue1: Style
    blue1_bordered: Style
    blue1_bold: Style
    blue1_light: Style
    blue1_flat: Style
    blue1_outline: Style
    blue1_solid: Style
    blue1_outline_bold: Style
    blue1_solid_bold: Style
    blue1_outline_light: Style
    blue1_solid_light: Style
    blue1_dashed: Style
    blue1_dashed_bold: Style
    blue1_dashed_light: Style

    # blue2
    blue2: Style
    blue2_bordered: Style
    blue2_bold: Style
    blue2_light: Style
    blue2_flat: Style
    blue2_outline: Style
    blue2_solid: Style
    blue2_outline_bold: Style
    blue2_solid_bold: Style
    blue2_outline_light: Style
    blue2_solid_light: Style
    blue2_dashed: Style
    blue2_dashed_bold: Style
    blue2_dashed_light: Style

    # blue3
    blue3: Style
    blue3_bordered: Style
    blue3_bold: Style
    blue3_light: Style
    blue3_flat: Style
    blue3_outline: Style
    blue3_solid: Style
    blue3_outline_bold: Style
    blue3_solid_bold: Style
    blue3_outline_light: Style
    blue3_solid_light: Style
    blue3_dashed: Style
    blue3_dashed_bold: Style
    blue3_dashed_light: Style

    # blue4
    blue4: Style
    blue4_bordered: Style
    blue4_bold: Style
    blue4_light: Style
    blue4_flat: Style
    blue4_outline: Style
    blue4_solid: Style
    blue4_outline_bold: Style
    blue4_solid_bold: Style
    blue4_outline_light: Style
    blue4_solid_light: Style
    blue4_dashed: Style
    blue4_dashed_bold: Style
    blue4_dashed_light: Style

    # blue5
    blue5: Style
    blue5_bordered: Style
    blue5_bold: Style
    blue5_light: Style
    blue5_flat: Style
    blue5_outline: Style
    blue5_solid: Style
    blue5_outline_bold: Style
    blue5_solid_bold: Style
    blue5_outline_light: Style
    blue5_solid_light: Style
    blue5_dashed: Style
    blue5_dashed_bold: Style
    blue5_dashed_light: Style

    # blue6
    blue6: Style
    blue6_bordered: Style
    blue6_bold: Style
    blue6_light: Style
    blue6_flat: Style
    blue6_outline: Style
    blue6_solid: Style
    blue6_outline_bold: Style
    blue6_solid_bold: Style
    blue6_outline_light: Style
    blue6_solid_light: Style
    blue6_dashed: Style
    blue6_dashed_bold: Style
    blue6_dashed_light: Style

    # green1
    green1: Style
    green1_bordered: Style
    green1_bold: Style
    green1_light: Style
    green1_flat: Style
    green1_outline: Style
    green1_solid: Style
    green1_outline_bold: Style
    green1_solid_bold: Style
    green1_outline_light: Style
    green1_solid_light: Style
    green1_dashed: Style
    green1_dashed_bold: Style
    green1_dashed_light: Style

    # green2
    green2: Style
    green2_bordered: Style
    green2_bold: Style
    green2_light: Style
    green2_flat: Style
    green2_outline: Style
    green2_solid: Style
    green2_outline_bold: Style
    green2_solid_bold: Style
    green2_outline_light: Style
    green2_solid_light: Style
    green2_dashed: Style
    green2_dashed_bold: Style
    green2_dashed_light: Style

    # green3
    green3: Style
    green3_bordered: Style
    green3_bold: Style
    green3_light: Style
    green3_flat: Style
    green3_outline: Style
    green3_solid: Style
    green3_outline_bold: Style
    green3_solid_bold: Style
    green3_outline_light: Style
    green3_solid_light: Style
    green3_dashed: Style
    green3_dashed_bold: Style
    green3_dashed_light: Style

    # green4
    green4: Style
    green4_bordered: Style
    green4_bold: Style
    green4_light: Style
    green4_flat: Style
    green4_outline: Style
    green4_solid: Style
    green4_outline_bold: Style
    green4_solid_bold: Style
    green4_outline_light: Style
    green4_solid_light: Style
    green4_dashed: Style
    green4_dashed_bold: Style
    green4_dashed_light: Style

    # green5
    green5: Style
    green5_bordered: Style
    green5_bold: Style
    green5_light: Style
    green5_flat: Style
    green5_outline: Style
    green5_solid: Style
    green5_outline_bold: Style
    green5_solid_bold: Style
    green5_outline_light: Style
    green5_solid_light: Style
    green5_dashed: Style
    green5_dashed_bold: Style
    green5_dashed_light: Style

    # green6
    green6: Style
    green6_bordered: Style
    green6_bold: Style
    green6_light: Style
    green6_flat: Style
    green6_outline: Style
    green6_solid: Style
    green6_outline_bold: Style
    green6_solid_bold: Style
    green6_outline_light: Style
    green6_solid_light: Style
    green6_dashed: Style
    green6_dashed_bold: Style
    green6_dashed_light: Style

    # red1
    red1: Style
    red1_bordered: Style
    red1_bold: Style
    red1_light: Style
    red1_flat: Style
    red1_outline: Style
    red1_solid: Style
    red1_outline_bold: Style
    red1_solid_bold: Style
    red1_outline_light: Style
    red1_solid_light: Style
    red1_dashed: Style
    red1_dashed_bold: Style
    red1_dashed_light: Style

    # red2
    red2: Style
    red2_bordered: Style
    red2_bold: Style
    red2_light: Style
    red2_flat: Style
    red2_outline: Style
    red2_solid: Style
    red2_outline_bold: Style
    red2_solid_bold: Style
    red2_outline_light: Style
    red2_solid_light: Style
    red2_dashed: Style
    red2_dashed_bold: Style
    red2_dashed_light: Style

    # red3
    red3: Style
    red3_bordered: Style
    red3_bold: Style
    red3_light: Style
    red3_flat: Style
    red3_outline: Style
    red3_solid: Style
    red3_outline_bold: Style
    red3_solid_bold: Style
    red3_outline_light: Style
    red3_solid_light: Style
    red3_dashed: Style
    red3_dashed_bold: Style
    red3_dashed_light: Style

    # red4
    red4: Style
    red4_bordered: Style
    red4_bold: Style
    red4_light: Style
    red4_flat: Style
    red4_outline: Style
    red4_solid: Style
    red4_outline_bold: Style
    red4_solid_bold: Style
    red4_outline_light: Style
    red4_solid_light: Style
    red4_dashed: Style
    red4_dashed_bold: Style
    red4_dashed_light: Style

    # red5
    red5: Style
    red5_bordered: Style
    red5_bold: Style
    red5_light: Style
    red5_flat: Style
    red5_outline: Style
    red5_solid: Style
    red5_outline_bold: Style
    red5_solid_bold: Style
    red5_outline_light: Style
    red5_solid_light: Style
    red5_dashed: Style
    red5_dashed_bold: Style
    red5_dashed_light: Style

    # red6
    red6: Style
    red6_bordered: Style
    red6_bold: Style
    red6_light: Style
    red6_flat: Style
    red6_outline: Style
    red6_solid: Style
    red6_outline_bold: Style
    red6_solid_bold: Style
    red6_outline_light: Style
    red6_solid_light: Style
    red6_dashed: Style
    red6_dashed_bold: Style
    red6_dashed_light: Style

    # orange1
    orange1: Style
    orange1_bordered: Style
    orange1_bold: Style
    orange1_light: Style
    orange1_flat: Style
    orange1_outline: Style
    orange1_solid: Style
    orange1_outline_bold: Style
    orange1_solid_bold: Style
    orange1_outline_light: Style
    orange1_solid_light: Style
    orange1_dashed: Style
    orange1_dashed_bold: Style
    orange1_dashed_light: Style

    # orange2
    orange2: Style
    orange2_bordered: Style
    orange2_bold: Style
    orange2_light: Style
    orange2_flat: Style
    orange2_outline: Style
    orange2_solid: Style
    orange2_outline_bold: Style
    orange2_solid_bold: Style
    orange2_outline_light: Style
    orange2_solid_light: Style
    orange2_dashed: Style
    orange2_dashed_bold: Style
    orange2_dashed_light: Style

    # orange3
    orange3: Style
    orange3_bordered: Style
    orange3_bold: Style
    orange3_light: Style
    orange3_flat: Style
    orange3_outline: Style
    orange3_solid: Style
    orange3_outline_bold: Style
    orange3_solid_bold: Style
    orange3_outline_light: Style
    orange3_solid_light: Style
    orange3_dashed: Style
    orange3_dashed_bold: Style
    orange3_dashed_light: Style

    # orange4
    orange4: Style
    orange4_bordered: Style
    orange4_bold: Style
    orange4_light: Style
    orange4_flat: Style
    orange4_outline: Style
    orange4_solid: Style
    orange4_outline_bold: Style
    orange4_solid_bold: Style
    orange4_outline_light: Style
    orange4_solid_light: Style
    orange4_dashed: Style
    orange4_dashed_bold: Style
    orange4_dashed_light: Style

    # orange5
    orange5: Style
    orange5_bordered: Style
    orange5_bold: Style
    orange5_light: Style
    orange5_flat: Style
    orange5_outline: Style
    orange5_solid: Style
    orange5_outline_bold: Style
    orange5_solid_bold: Style
    orange5_outline_light: Style
    orange5_solid_light: Style
    orange5_dashed: Style
    orange5_dashed_bold: Style
    orange5_dashed_light: Style

    # orange6
    orange6: Style
    orange6_bordered: Style
    orange6_bold: Style
    orange6_light: Style
    orange6_flat: Style
    orange6_outline: Style
    orange6_solid: Style
    orange6_outline_bold: Style
    orange6_solid_bold: Style
    orange6_outline_light: Style
    orange6_solid_light: Style
    orange6_dashed: Style
    orange6_dashed_bold: Style
    orange6_dashed_light: Style

    # amber1
    amber1: Style
    amber1_bordered: Style
    amber1_bold: Style
    amber1_light: Style
    amber1_flat: Style
    amber1_outline: Style
    amber1_solid: Style
    amber1_outline_bold: Style
    amber1_solid_bold: Style
    amber1_outline_light: Style
    amber1_solid_light: Style
    amber1_dashed: Style
    amber1_dashed_bold: Style
    amber1_dashed_light: Style

    # amber2
    amber2: Style
    amber2_bordered: Style
    amber2_bold: Style
    amber2_light: Style
    amber2_flat: Style
    amber2_outline: Style
    amber2_solid: Style
    amber2_outline_bold: Style
    amber2_solid_bold: Style
    amber2_outline_light: Style
    amber2_solid_light: Style
    amber2_dashed: Style
    amber2_dashed_bold: Style
    amber2_dashed_light: Style

    # amber3
    amber3: Style
    amber3_bordered: Style
    amber3_bold: Style
    amber3_light: Style
    amber3_flat: Style
    amber3_outline: Style
    amber3_solid: Style
    amber3_outline_bold: Style
    amber3_solid_bold: Style
    amber3_outline_light: Style
    amber3_solid_light: Style
    amber3_dashed: Style
    amber3_dashed_bold: Style
    amber3_dashed_light: Style

    # amber4
    amber4: Style
    amber4_bordered: Style
    amber4_bold: Style
    amber4_light: Style
    amber4_flat: Style
    amber4_outline: Style
    amber4_solid: Style
    amber4_outline_bold: Style
    amber4_solid_bold: Style
    amber4_outline_light: Style
    amber4_solid_light: Style
    amber4_dashed: Style
    amber4_dashed_bold: Style
    amber4_dashed_light: Style

    # amber5
    amber5: Style
    amber5_bordered: Style
    amber5_bold: Style
    amber5_light: Style
    amber5_flat: Style
    amber5_outline: Style
    amber5_solid: Style
    amber5_outline_bold: Style
    amber5_solid_bold: Style
    amber5_outline_light: Style
    amber5_solid_light: Style
    amber5_dashed: Style
    amber5_dashed_bold: Style
    amber5_dashed_light: Style

    # amber6
    amber6: Style
    amber6_bordered: Style
    amber6_bold: Style
    amber6_light: Style
    amber6_flat: Style
    amber6_outline: Style
    amber6_solid: Style
    amber6_outline_bold: Style
    amber6_solid_bold: Style
    amber6_outline_light: Style
    amber6_solid_light: Style
    amber6_dashed: Style
    amber6_dashed_bold: Style
    amber6_dashed_light: Style

    # purple1
    purple1: Style
    purple1_bordered: Style
    purple1_bold: Style
    purple1_light: Style
    purple1_flat: Style
    purple1_outline: Style
    purple1_solid: Style
    purple1_outline_bold: Style
    purple1_solid_bold: Style
    purple1_outline_light: Style
    purple1_solid_light: Style
    purple1_dashed: Style
    purple1_dashed_bold: Style
    purple1_dashed_light: Style

    # purple2
    purple2: Style
    purple2_bordered: Style
    purple2_bold: Style
    purple2_light: Style
    purple2_flat: Style
    purple2_outline: Style
    purple2_solid: Style
    purple2_outline_bold: Style
    purple2_solid_bold: Style
    purple2_outline_light: Style
    purple2_solid_light: Style
    purple2_dashed: Style
    purple2_dashed_bold: Style
    purple2_dashed_light: Style

    # purple3
    purple3: Style
    purple3_bordered: Style
    purple3_bold: Style
    purple3_light: Style
    purple3_flat: Style
    purple3_outline: Style
    purple3_solid: Style
    purple3_outline_bold: Style
    purple3_solid_bold: Style
    purple3_outline_light: Style
    purple3_solid_light: Style
    purple3_dashed: Style
    purple3_dashed_bold: Style
    purple3_dashed_light: Style

    # purple4
    purple4: Style
    purple4_bordered: Style
    purple4_bold: Style
    purple4_light: Style
    purple4_flat: Style
    purple4_outline: Style
    purple4_solid: Style
    purple4_outline_bold: Style
    purple4_solid_bold: Style
    purple4_outline_light: Style
    purple4_solid_light: Style
    purple4_dashed: Style
    purple4_dashed_bold: Style
    purple4_dashed_light: Style

    # purple5
    purple5: Style
    purple5_bordered: Style
    purple5_bold: Style
    purple5_light: Style
    purple5_flat: Style
    purple5_outline: Style
    purple5_solid: Style
    purple5_outline_bold: Style
    purple5_solid_bold: Style
    purple5_outline_light: Style
    purple5_solid_light: Style
    purple5_dashed: Style
    purple5_dashed_bold: Style
    purple5_dashed_light: Style

    # purple6
    purple6: Style
    purple6_bordered: Style
    purple6_bold: Style
    purple6_light: Style
    purple6_flat: Style
    purple6_outline: Style
    purple6_solid: Style
    purple6_outline_bold: Style
    purple6_solid_bold: Style
    purple6_outline_light: Style
    purple6_solid_light: Style
    purple6_dashed: Style
    purple6_dashed_bold: Style
    purple6_dashed_light: Style

    # teal1
    teal1: Style
    teal1_bordered: Style
    teal1_bold: Style
    teal1_light: Style
    teal1_flat: Style
    teal1_outline: Style
    teal1_solid: Style
    teal1_outline_bold: Style
    teal1_solid_bold: Style
    teal1_outline_light: Style
    teal1_solid_light: Style
    teal1_dashed: Style
    teal1_dashed_bold: Style
    teal1_dashed_light: Style

    # teal2
    teal2: Style
    teal2_bordered: Style
    teal2_bold: Style
    teal2_light: Style
    teal2_flat: Style
    teal2_outline: Style
    teal2_solid: Style
    teal2_outline_bold: Style
    teal2_solid_bold: Style
    teal2_outline_light: Style
    teal2_solid_light: Style
    teal2_dashed: Style
    teal2_dashed_bold: Style
    teal2_dashed_light: Style

    # teal3
    teal3: Style
    teal3_bordered: Style
    teal3_bold: Style
    teal3_light: Style
    teal3_flat: Style
    teal3_outline: Style
    teal3_solid: Style
    teal3_outline_bold: Style
    teal3_solid_bold: Style
    teal3_outline_light: Style
    teal3_solid_light: Style
    teal3_dashed: Style
    teal3_dashed_bold: Style
    teal3_dashed_light: Style

    # teal4
    teal4: Style
    teal4_bordered: Style
    teal4_bold: Style
    teal4_light: Style
    teal4_flat: Style
    teal4_outline: Style
    teal4_solid: Style
    teal4_outline_bold: Style
    teal4_solid_bold: Style
    teal4_outline_light: Style
    teal4_solid_light: Style
    teal4_dashed: Style
    teal4_dashed_bold: Style
    teal4_dashed_light: Style

    # teal5
    teal5: Style
    teal5_bordered: Style
    teal5_bold: Style
    teal5_light: Style
    teal5_flat: Style
    teal5_outline: Style
    teal5_solid: Style
    teal5_outline_bold: Style
    teal5_solid_bold: Style
    teal5_outline_light: Style
    teal5_solid_light: Style
    teal5_dashed: Style
    teal5_dashed_bold: Style
    teal5_dashed_light: Style

    # teal6
    teal6: Style
    teal6_bordered: Style
    teal6_bold: Style
    teal6_light: Style
    teal6_flat: Style
    teal6_outline: Style
    teal6_solid: Style
    teal6_outline_bold: Style
    teal6_solid_bold: Style
    teal6_outline_light: Style
    teal6_solid_light: Style
    teal6_dashed: Style
    teal6_dashed_bold: Style
    teal6_dashed_light: Style

    # pink1
    pink1: Style
    pink1_bordered: Style
    pink1_bold: Style
    pink1_light: Style
    pink1_flat: Style
    pink1_outline: Style
    pink1_solid: Style
    pink1_outline_bold: Style
    pink1_solid_bold: Style
    pink1_outline_light: Style
    pink1_solid_light: Style
    pink1_dashed: Style
    pink1_dashed_bold: Style
    pink1_dashed_light: Style

    # pink2
    pink2: Style
    pink2_bordered: Style
    pink2_bold: Style
    pink2_light: Style
    pink2_flat: Style
    pink2_outline: Style
    pink2_solid: Style
    pink2_outline_bold: Style
    pink2_solid_bold: Style
    pink2_outline_light: Style
    pink2_solid_light: Style
    pink2_dashed: Style
    pink2_dashed_bold: Style
    pink2_dashed_light: Style

    # pink3
    pink3: Style
    pink3_bordered: Style
    pink3_bold: Style
    pink3_light: Style
    pink3_flat: Style
    pink3_outline: Style
    pink3_solid: Style
    pink3_outline_bold: Style
    pink3_solid_bold: Style
    pink3_outline_light: Style
    pink3_solid_light: Style
    pink3_dashed: Style
    pink3_dashed_bold: Style
    pink3_dashed_light: Style

    # pink4
    pink4: Style
    pink4_bordered: Style
    pink4_bold: Style
    pink4_light: Style
    pink4_flat: Style
    pink4_outline: Style
    pink4_solid: Style
    pink4_outline_bold: Style
    pink4_solid_bold: Style
    pink4_outline_light: Style
    pink4_solid_light: Style
    pink4_dashed: Style
    pink4_dashed_bold: Style
    pink4_dashed_light: Style

    # pink5
    pink5: Style
    pink5_bordered: Style
    pink5_bold: Style
    pink5_light: Style
    pink5_flat: Style
    pink5_outline: Style
    pink5_solid: Style
    pink5_outline_bold: Style
    pink5_solid_bold: Style
    pink5_outline_light: Style
    pink5_solid_light: Style
    pink5_dashed: Style
    pink5_dashed_bold: Style
    pink5_dashed_light: Style

    # pink6
    pink6: Style
    pink6_bordered: Style
    pink6_bold: Style
    pink6_light: Style
    pink6_flat: Style
    pink6_outline: Style
    pink6_solid: Style
    pink6_outline_bold: Style
    pink6_solid_bold: Style
    pink6_outline_light: Style
    pink6_solid_light: Style
    pink6_dashed: Style
    pink6_dashed_bold: Style
    pink6_dashed_light: Style

    # =========================================================================
    # Neutrals
    # =========================================================================
    # white
    white: Style
    white_bordered: Style
    white_bold: Style
    white_light: Style
    white_flat: Style
    white_outline: Style
    white_solid: Style
    white_outline_bold: Style
    white_solid_bold: Style
    white_outline_light: Style
    white_solid_light: Style
    white_dashed: Style
    white_dashed_bold: Style
    white_dashed_light: Style

    # gray1
    gray1: Style
    gray1_bordered: Style
    gray1_bold: Style
    gray1_light: Style
    gray1_flat: Style
    gray1_outline: Style
    gray1_solid: Style
    gray1_outline_bold: Style
    gray1_solid_bold: Style
    gray1_outline_light: Style
    gray1_solid_light: Style
    gray1_dashed: Style
    gray1_dashed_bold: Style
    gray1_dashed_light: Style

    # gray2
    gray2: Style
    gray2_bordered: Style
    gray2_bold: Style
    gray2_light: Style
    gray2_flat: Style
    gray2_outline: Style
    gray2_solid: Style
    gray2_outline_bold: Style
    gray2_solid_bold: Style
    gray2_outline_light: Style
    gray2_solid_light: Style
    gray2_dashed: Style
    gray2_dashed_bold: Style
    gray2_dashed_light: Style

    # gray3
    gray3: Style
    gray3_bordered: Style
    gray3_bold: Style
    gray3_light: Style
    gray3_flat: Style
    gray3_outline: Style
    gray3_solid: Style
    gray3_outline_bold: Style
    gray3_solid_bold: Style
    gray3_outline_light: Style
    gray3_solid_light: Style
    gray3_dashed: Style
    gray3_dashed_bold: Style
    gray3_dashed_light: Style

    # gray4
    gray4: Style
    gray4_bordered: Style
    gray4_bold: Style
    gray4_light: Style
    gray4_flat: Style
    gray4_outline: Style
    gray4_solid: Style
    gray4_outline_bold: Style
    gray4_solid_bold: Style
    gray4_outline_light: Style
    gray4_solid_light: Style
    gray4_dashed: Style
    gray4_dashed_bold: Style
    gray4_dashed_light: Style

    # gray5
    gray5: Style
    gray5_bordered: Style
    gray5_bold: Style
    gray5_light: Style
    gray5_flat: Style
    gray5_outline: Style
    gray5_solid: Style
    gray5_outline_bold: Style
    gray5_solid_bold: Style
    gray5_outline_light: Style
    gray5_solid_light: Style
    gray5_dashed: Style
    gray5_dashed_bold: Style
    gray5_dashed_light: Style

    # gray6
    gray6: Style
    gray6_bordered: Style
    gray6_bold: Style
    gray6_light: Style
    gray6_flat: Style
    gray6_outline: Style
    gray6_solid: Style
    gray6_outline_bold: Style
    gray6_solid_bold: Style
    gray6_outline_light: Style
    gray6_solid_light: Style
    gray6_dashed: Style
    gray6_dashed_bold: Style
    gray6_dashed_light: Style

    # gray7
    gray7: Style
    gray7_bordered: Style
    gray7_bold: Style
    gray7_light: Style
    gray7_flat: Style
    gray7_outline: Style
    gray7_solid: Style
    gray7_outline_bold: Style
    gray7_solid_bold: Style
    gray7_outline_light: Style
    gray7_solid_light: Style
    gray7_dashed: Style
    gray7_dashed_bold: Style
    gray7_dashed_light: Style

    # gray8
    gray8: Style
    gray8_bordered: Style
    gray8_bold: Style
    gray8_light: Style
    gray8_flat: Style
    gray8_outline: Style
    gray8_solid: Style
    gray8_outline_bold: Style
    gray8_solid_bold: Style
    gray8_outline_light: Style
    gray8_solid_light: Style
    gray8_dashed: Style
    gray8_dashed_bold: Style
    gray8_dashed_light: Style

    # black
    black: Style
    black_bordered: Style
    black_bold: Style
    black_light: Style
    black_flat: Style
    black_outline: Style
    black_solid: Style
    black_outline_bold: Style
    black_solid_bold: Style
    black_outline_light: Style
    black_solid_light: Style
    black_dashed: Style
    black_dashed_bold: Style
    black_dashed_light: Style

    # =========================================================================
    # Classic Primaries
    # =========================================================================
    # red
    red: Style
    red_bordered: Style
    red_bold: Style
    red_light: Style
    red_flat: Style
    red_outline: Style
    red_solid: Style
    red_outline_bold: Style
    red_solid_bold: Style
    red_outline_light: Style
    red_solid_light: Style
    red_dashed: Style
    red_dashed_bold: Style
    red_dashed_light: Style

    # green
    green: Style
    green_bordered: Style
    green_bold: Style
    green_light: Style
    green_flat: Style
    green_outline: Style
    green_solid: Style
    green_outline_bold: Style
    green_solid_bold: Style
    green_outline_light: Style
    green_solid_light: Style
    green_dashed: Style
    green_dashed_bold: Style
    green_dashed_light: Style

    # blue
    blue: Style
    blue_bordered: Style
    blue_bold: Style
    blue_light: Style
    blue_flat: Style
    blue_outline: Style
    blue_solid: Style
    blue_outline_bold: Style
    blue_solid_bold: Style
    blue_outline_light: Style
    blue_solid_light: Style
    blue_dashed: Style
    blue_dashed_bold: Style
    blue_dashed_light: Style

    # yellow
    yellow: Style
    yellow_bordered: Style
    yellow_bold: Style
    yellow_light: Style
    yellow_flat: Style
    yellow_outline: Style
    yellow_solid: Style
    yellow_outline_bold: Style
    yellow_solid_bold: Style
    yellow_outline_light: Style
    yellow_solid_light: Style
    yellow_dashed: Style
    yellow_dashed_bold: Style
    yellow_dashed_light: Style

    # orange
    orange: Style
    orange_bordered: Style
    orange_bold: Style
    orange_light: Style
    orange_flat: Style
    orange_outline: Style
    orange_solid: Style
    orange_outline_bold: Style
    orange_solid_bold: Style
    orange_outline_light: Style
    orange_solid_light: Style
    orange_dashed: Style
    orange_dashed_bold: Style
    orange_dashed_light: Style

    # purple
    purple: Style
    purple_bordered: Style
    purple_bold: Style
    purple_light: Style
    purple_flat: Style
    purple_outline: Style
    purple_solid: Style
    purple_outline_bold: Style
    purple_solid_bold: Style
    purple_outline_light: Style
    purple_solid_light: Style
    purple_dashed: Style
    purple_dashed_bold: Style
    purple_dashed_light: Style

    # pink
    pink: Style
    pink_bordered: Style
    pink_bold: Style
    pink_light: Style
    pink_flat: Style
    pink_outline: Style
    pink_solid: Style
    pink_outline_bold: Style
    pink_solid_bold: Style
    pink_outline_light: Style
    pink_solid_light: Style
    pink_dashed: Style
    pink_dashed_bold: Style
    pink_dashed_light: Style

    # cyan
    cyan: Style
    cyan_bordered: Style
    cyan_bold: Style
    cyan_light: Style
    cyan_flat: Style
    cyan_outline: Style
    cyan_solid: Style
    cyan_outline_bold: Style
    cyan_solid_bold: Style
    cyan_outline_light: Style
    cyan_solid_light: Style
    cyan_dashed: Style
    cyan_dashed_bold: Style
    cyan_dashed_light: Style

    # magenta
    magenta: Style
    magenta_bordered: Style
    magenta_bold: Style
    magenta_light: Style
    magenta_flat: Style
    magenta_outline: Style
    magenta_solid: Style
    magenta_outline_bold: Style
    magenta_solid_bold: Style
    magenta_outline_light: Style
    magenta_solid_light: Style
    magenta_dashed: Style
    magenta_dashed_bold: Style
    magenta_dashed_light: Style

    # lime
    lime: Style
    lime_bordered: Style
    lime_bold: Style
    lime_light: Style
    lime_flat: Style
    lime_outline: Style
    lime_solid: Style
    lime_outline_bold: Style
    lime_solid_bold: Style
    lime_outline_light: Style
    lime_solid_light: Style
    lime_dashed: Style
    lime_dashed_bold: Style
    lime_dashed_light: Style

    # teal
    teal: Style
    teal_bordered: Style
    teal_bold: Style
    teal_light: Style
    teal_flat: Style
    teal_outline: Style
    teal_solid: Style
    teal_outline_bold: Style
    teal_solid_bold: Style
    teal_outline_light: Style
    teal_solid_light: Style
    teal_dashed: Style
    teal_dashed_bold: Style
    teal_dashed_light: Style

    # navy
    navy: Style
    navy_bordered: Style
    navy_bold: Style
    navy_light: Style
    navy_flat: Style
    navy_outline: Style
    navy_solid: Style
    navy_outline_bold: Style
    navy_solid_bold: Style
    navy_outline_light: Style
    navy_solid_light: Style
    navy_dashed: Style
    navy_dashed_bold: Style
    navy_dashed_light: Style

    # olive
    olive: Style
    olive_bordered: Style
    olive_bold: Style
    olive_light: Style
    olive_flat: Style
    olive_outline: Style
    olive_solid: Style
    olive_outline_bold: Style
    olive_solid_bold: Style
    olive_outline_light: Style
    olive_solid_light: Style
    olive_dashed: Style
    olive_dashed_bold: Style
    olive_dashed_light: Style

    # brown
    brown: Style
    brown_bordered: Style
    brown_bold: Style
    brown_light: Style
    brown_flat: Style
    brown_outline: Style
    brown_solid: Style
    brown_outline_bold: Style
    brown_solid_bold: Style
    brown_outline_light: Style
    brown_solid_light: Style
    brown_dashed: Style
    brown_dashed_bold: Style
    brown_dashed_light: Style

    # gold
    gold: Style
    gold_bordered: Style
    gold_bold: Style
    gold_light: Style
    gold_flat: Style
    gold_outline: Style
    gold_solid: Style
    gold_outline_bold: Style
    gold_solid_bold: Style
    gold_outline_light: Style
    gold_solid_light: Style
    gold_dashed: Style
    gold_dashed_bold: Style
    gold_dashed_light: Style

    # aqua
    aqua: Style
    aqua_bordered: Style
    aqua_bold: Style
    aqua_light: Style
    aqua_flat: Style
    aqua_outline: Style
    aqua_solid: Style
    aqua_outline_bold: Style
    aqua_solid_bold: Style
    aqua_outline_light: Style
    aqua_solid_light: Style
    aqua_dashed: Style
    aqua_dashed_bold: Style
    aqua_dashed_light: Style

    # green_yellow
    green_yellow: Style
    green_yellow_bordered: Style
    green_yellow_bold: Style
    green_yellow_light: Style
    green_yellow_flat: Style
    green_yellow_outline: Style
    green_yellow_solid: Style
    green_yellow_outline_bold: Style
    green_yellow_solid_bold: Style
    green_yellow_outline_light: Style
    green_yellow_solid_light: Style
    green_yellow_dashed: Style
    green_yellow_dashed_bold: Style
    green_yellow_dashed_light: Style

    # ivory
    ivory: Style
    ivory_bordered: Style
    ivory_bold: Style
    ivory_light: Style
    ivory_flat: Style
    ivory_outline: Style
    ivory_solid: Style
    ivory_outline_bold: Style
    ivory_solid_bold: Style
    ivory_outline_light: Style
    ivory_solid_light: Style
    ivory_dashed: Style
    ivory_dashed_bold: Style
    ivory_dashed_light: Style

    # steel
    steel: Style
    steel_bordered: Style
    steel_bold: Style
    steel_light: Style
    steel_flat: Style
    steel_outline: Style
    steel_solid: Style
    steel_outline_bold: Style
    steel_solid_bold: Style
    steel_outline_light: Style
    steel_solid_light: Style
    steel_dashed: Style
    steel_dashed_bold: Style
    steel_dashed_light: Style

    # Canvas
    canvas: Style
    canvas_flat: Style

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize preset styles instance.

        If called without arguments (or with partial overrides), missing fields are
        automatically populated from the registered default singleton instance for this class.
        """
        super().__init__(**kwargs)

    def patch(
        self,
        *,
        canvas: Style | None = None,
        canvas_flat: Style | None = None,
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


# Backward compatibility aliases
DefaultLightStyles = DefaultStyles2
DefaultDarkStyles = DefaultStyles5


def _create_default_styles(  # noqa: C901, PLR0911
    theme: Literal["default", "1", "2", "3", "4", "5", "6", "light", "dark"] = "default",
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
    elif theme in {"2", "light"}:
        col = DefaultColors2
        theme_tone = 2
    elif theme == "3":
        col = DefaultColors3
        theme_tone = 3
    elif theme in {"5", "dark"}:
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
        "blue1": col.Blue1,
        "blue2": col.Blue2,
        "blue3": col.Blue3,
        "blue4": col.Blue4,
        "blue5": col.Blue5,
        "blue6": col.Blue6,
        "green1": col.Green1,
        "green2": col.Green2,
        "green3": col.Green3,
        "green4": col.Green4,
        "green5": col.Green5,
        "green6": col.Green6,
        "red1": col.Red1,
        "red2": col.Red2,
        "red3": col.Red3,
        "red4": col.Red4,
        "red5": col.Red5,
        "red6": col.Red6,
        "orange1": col.Orange1,
        "orange2": col.Orange2,
        "orange3": col.Orange3,
        "orange4": col.Orange4,
        "orange5": col.Orange5,
        "orange6": col.Orange6,
        "amber1": col.Amber1,
        "amber2": col.Amber2,
        "amber3": col.Amber3,
        "amber4": col.Amber4,
        "amber5": col.Amber5,
        "amber6": col.Amber6,
        "purple1": col.Purple1,
        "purple2": col.Purple2,
        "purple3": col.Purple3,
        "purple4": col.Purple4,
        "purple5": col.Purple5,
        "purple6": col.Purple6,
        "teal1": col.Teal1,
        "teal2": col.Teal2,
        "teal3": col.Teal3,
        "teal4": col.Teal4,
        "teal5": col.Teal5,
        "teal6": col.Teal6,
        "pink1": col.Pink1,
        "pink2": col.Pink2,
        "pink3": col.Pink3,
        "pink4": col.Pink4,
        "pink5": col.Pink5,
        "pink6": col.Pink6,
        "primary1": col.Primary1,
        "primary2": col.Primary2,
        "primary3": col.Primary3,
        "primary4": col.Primary4,
        "primary5": col.Primary5,
        "primary6": col.Primary6,
        "secondary1": col.Secondary1,
        "secondary2": col.Secondary2,
        "secondary3": col.Secondary3,
        "secondary4": col.Secondary4,
        "secondary5": col.Secondary5,
        "secondary6": col.Secondary6,
        "accent1": col.Accent1,
        "accent2": col.Accent2,
        "accent3": col.Accent3,
        "accent4": col.Accent4,
        "accent5": col.Accent5,
        "accent6": col.Accent6,
        "muted1": col.Muted1,
        "muted2": col.Muted2,
        "muted3": col.Muted3,
        "muted4": col.Muted4,
        "muted5": col.Muted5,
        "muted6": col.Muted6,
        "danger1": col.Danger1,
        "danger2": col.Danger2,
        "danger3": col.Danger3,
        "danger4": col.Danger4,
        "danger5": col.Danger5,
        "danger6": col.Danger6,
        "success1": col.Success1,
        "success2": col.Success2,
        "success3": col.Success3,
        "success4": col.Success4,
        "success5": col.Success5,
        "success6": col.Success6,
        "white": col.White,
        "gray1": col.Gray1,
        "gray2": col.Gray2,
        "gray3": col.Gray3,
        "gray4": col.Gray4,
        "gray5": col.Gray5,
        "gray6": col.Gray6,
        "gray7": col.Gray7,
        "gray8": col.Gray8,
        "black": col.Black,
        "red": col.Red,
        "green": col.Green,
        "blue": col.Blue,
        "yellow": col.Yellow,
        "orange": col.Orange,
        "purple": col.Purple,
        "pink": col.Pink,
        "cyan": col.Cyan,
        "magenta": col.Magenta,
        "lime": col.Lime,
        "teal": col.Teal,
        "navy": col.Navy,
        "olive": col.Olive,
        "brown": col.Brown,
        "gold": col.Gold,
        "aqua": col.Aqua,
        "green_yellow": col.GreenYellow,
        "ivory": col.Ivory,
        "steel": col.Steel,
    }

    # 2. Semantic Roles Map
    semantic_map = {
        "primary": col.Primary,
        "secondary": col.Secondary,
        "accent": col.Accent,
        "muted": col.Muted,
        "light": col.Light,
        "dark": col.Dark,
        "danger": col.Danger,
        "success": col.Success,
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
            if role_name == "muted":
                text_col = col.White if theme_tone >= 5 else col.Dark
                v = _make_variants(
                    color,
                    border_color=col.Gray5,
                    default_text_color=text_col,
                    line_color=col.Gray4,
                )
            elif role_name == "light":
                v = _make_variants(
                    color,
                    border_color=col.Gray4,
                    default_text_color=col.Gray7,
                    line_color=col.Gray4,
                )
            elif role_name == "dark":
                v = _make_variants(
                    color,
                    border_color=col.Gray4,
                    default_text_color=col.White,
                    line_color=col.Gray4,
                )
            else:
                v = _make_variants(color)

            styles_dict[role_name] = v["normal"]
            styles_dict[f"{role_name}_bordered"] = v["bordered"]
            styles_dict[f"{role_name}_bold"] = v["bold"]
            styles_dict[f"{role_name}_light"] = v["light"]
            styles_dict[f"{role_name}_flat"] = v["flat"]
            styles_dict[f"{role_name}_outline"] = v["outline"]
            styles_dict[f"{role_name}_solid"] = v["solid"]
            styles_dict[f"{role_name}_outline_bold"] = v["outline_bold"]
            styles_dict[f"{role_name}_solid_bold"] = v["solid_bold"]
            styles_dict[f"{role_name}_outline_light"] = v["outline_light"]
            styles_dict[f"{role_name}_solid_light"] = v["solid_light"]
            styles_dict[f"{role_name}_dashed"] = v["dashed"]
            styles_dict[f"{role_name}_dashed_bold"] = v["dashed_bold"]
            styles_dict[f"{role_name}_dashed_light"] = v["dashed_light"]

    for cname, color in colors_map.items():
        v = _make_variants(color)
        styles_dict[cname] = v["normal"]
        styles_dict[f"{cname}_bordered"] = v["bordered"]
        styles_dict[f"{cname}_bold"] = v["bold"]
        styles_dict[f"{cname}_light"] = v["light"]
        styles_dict[f"{cname}_flat"] = v["flat"]
        styles_dict[f"{cname}_outline"] = v["outline"]
        styles_dict[f"{cname}_solid"] = v["solid"]
        styles_dict[f"{cname}_outline_bold"] = v["outline_bold"]
        styles_dict[f"{cname}_solid_bold"] = v["solid_bold"]
        styles_dict[f"{cname}_outline_light"] = v["outline_light"]
        styles_dict[f"{cname}_solid_light"] = v["solid_light"]
        styles_dict[f"{cname}_dashed"] = v["dashed"]
        styles_dict[f"{cname}_dashed_bold"] = v["dashed_bold"]
        styles_dict[f"{cname}_dashed_light"] = v["dashed_light"]

    # Canvas shape style
    canvas_col = col.Canvas
    styles_dict["canvas"] = Style(
        supports={"shape"},
        shape_fill_color=canvas_col,
        shape_line_color=canvas_col,
        shape_line_width=0.0,
    )
    styles_dict["canvas_flat"] = Style(
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
    "DefaultDarkStyles",
    "DefaultLightStyles",
    "DefaultStyles",
    "DefaultStyles1",
    "DefaultStyles2",
    "DefaultStyles3",
    "DefaultStyles4",
    "DefaultStyles5",
    "DefaultStyles6",
]
