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

from drawlib._core.fonts import FontSourceCode
from drawlib._core.l2_types import ColorType
from drawlib._core.styles import BaseColors, BaseStyles, Color
from drawlib._core.types import Style
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

    # Secondary
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

    # Accent
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

    # Muted
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

    # Light
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

    # Dark
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

    # Danger
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

    # Success
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

    # White
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

    # Gray1
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

    # Gray2
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

    # Gray3
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

    # Gray4
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

    # Gray5
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

    # Gray6
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

    # Gray7
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

    # Gray8
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

    # Black
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

    # --- CornflowerBlue Tones ---

    # CornflowerBlue1
    cornflower_blue1: Style
    cornflower_blue1_bordered: Style
    cornflower_blue1_bold: Style
    cornflower_blue1_light: Style
    cornflower_blue1_flat: Style
    cornflower_blue1_outline: Style
    cornflower_blue1_solid: Style
    cornflower_blue1_outline_bold: Style
    cornflower_blue1_solid_bold: Style
    cornflower_blue1_outline_light: Style
    cornflower_blue1_solid_light: Style
    cornflower_blue1_dashed: Style
    cornflower_blue1_dashed_bold: Style
    cornflower_blue1_dashed_light: Style

    # CornflowerBlue2
    cornflower_blue2: Style
    cornflower_blue2_bordered: Style
    cornflower_blue2_bold: Style
    cornflower_blue2_light: Style
    cornflower_blue2_flat: Style
    cornflower_blue2_outline: Style
    cornflower_blue2_solid: Style
    cornflower_blue2_outline_bold: Style
    cornflower_blue2_solid_bold: Style
    cornflower_blue2_outline_light: Style
    cornflower_blue2_solid_light: Style
    cornflower_blue2_dashed: Style
    cornflower_blue2_dashed_bold: Style
    cornflower_blue2_dashed_light: Style

    # CornflowerBlue3
    cornflower_blue3: Style
    cornflower_blue3_bordered: Style
    cornflower_blue3_bold: Style
    cornflower_blue3_light: Style
    cornflower_blue3_flat: Style
    cornflower_blue3_outline: Style
    cornflower_blue3_solid: Style
    cornflower_blue3_outline_bold: Style
    cornflower_blue3_solid_bold: Style
    cornflower_blue3_outline_light: Style
    cornflower_blue3_solid_light: Style
    cornflower_blue3_dashed: Style
    cornflower_blue3_dashed_bold: Style
    cornflower_blue3_dashed_light: Style

    # CornflowerBlue4
    cornflower_blue4: Style
    cornflower_blue4_bordered: Style
    cornflower_blue4_bold: Style
    cornflower_blue4_light: Style
    cornflower_blue4_flat: Style
    cornflower_blue4_outline: Style
    cornflower_blue4_solid: Style
    cornflower_blue4_outline_bold: Style
    cornflower_blue4_solid_bold: Style
    cornflower_blue4_outline_light: Style
    cornflower_blue4_solid_light: Style
    cornflower_blue4_dashed: Style
    cornflower_blue4_dashed_bold: Style
    cornflower_blue4_dashed_light: Style

    # CornflowerBlue5
    cornflower_blue5: Style
    cornflower_blue5_bordered: Style
    cornflower_blue5_bold: Style
    cornflower_blue5_light: Style
    cornflower_blue5_flat: Style
    cornflower_blue5_outline: Style
    cornflower_blue5_solid: Style
    cornflower_blue5_outline_bold: Style
    cornflower_blue5_solid_bold: Style
    cornflower_blue5_outline_light: Style
    cornflower_blue5_solid_light: Style
    cornflower_blue5_dashed: Style
    cornflower_blue5_dashed_bold: Style
    cornflower_blue5_dashed_light: Style

    # CornflowerBlue6
    cornflower_blue6: Style
    cornflower_blue6_bordered: Style
    cornflower_blue6_bold: Style
    cornflower_blue6_light: Style
    cornflower_blue6_flat: Style
    cornflower_blue6_outline: Style
    cornflower_blue6_solid: Style
    cornflower_blue6_outline_bold: Style
    cornflower_blue6_solid_bold: Style
    cornflower_blue6_outline_light: Style
    cornflower_blue6_solid_light: Style
    cornflower_blue6_dashed: Style
    cornflower_blue6_dashed_bold: Style
    cornflower_blue6_dashed_light: Style

    # --- Blue Tones ---

    # Blue1
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

    # Blue2
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

    # Blue3
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

    # Blue4
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

    # Blue5
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

    # Blue6
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

    # --- Red Tones ---

    # Red1
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

    # Red2
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

    # Red3
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

    # Red4
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

    # Red5
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

    # Red6
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

    # --- RedBerry Tones ---

    # RedBerry1
    red_berry1: Style
    red_berry1_bordered: Style
    red_berry1_bold: Style
    red_berry1_light: Style
    red_berry1_flat: Style
    red_berry1_outline: Style
    red_berry1_solid: Style
    red_berry1_outline_bold: Style
    red_berry1_solid_bold: Style
    red_berry1_outline_light: Style
    red_berry1_solid_light: Style
    red_berry1_dashed: Style
    red_berry1_dashed_bold: Style
    red_berry1_dashed_light: Style

    # RedBerry2
    red_berry2: Style
    red_berry2_bordered: Style
    red_berry2_bold: Style
    red_berry2_light: Style
    red_berry2_flat: Style
    red_berry2_outline: Style
    red_berry2_solid: Style
    red_berry2_outline_bold: Style
    red_berry2_solid_bold: Style
    red_berry2_outline_light: Style
    red_berry2_solid_light: Style
    red_berry2_dashed: Style
    red_berry2_dashed_bold: Style
    red_berry2_dashed_light: Style

    # RedBerry3
    red_berry3: Style
    red_berry3_bordered: Style
    red_berry3_bold: Style
    red_berry3_light: Style
    red_berry3_flat: Style
    red_berry3_outline: Style
    red_berry3_solid: Style
    red_berry3_outline_bold: Style
    red_berry3_solid_bold: Style
    red_berry3_outline_light: Style
    red_berry3_solid_light: Style
    red_berry3_dashed: Style
    red_berry3_dashed_bold: Style
    red_berry3_dashed_light: Style

    # RedBerry4
    red_berry4: Style
    red_berry4_bordered: Style
    red_berry4_bold: Style
    red_berry4_light: Style
    red_berry4_flat: Style
    red_berry4_outline: Style
    red_berry4_solid: Style
    red_berry4_outline_bold: Style
    red_berry4_solid_bold: Style
    red_berry4_outline_light: Style
    red_berry4_solid_light: Style
    red_berry4_dashed: Style
    red_berry4_dashed_bold: Style
    red_berry4_dashed_light: Style

    # RedBerry5
    red_berry5: Style
    red_berry5_bordered: Style
    red_berry5_bold: Style
    red_berry5_light: Style
    red_berry5_flat: Style
    red_berry5_outline: Style
    red_berry5_solid: Style
    red_berry5_outline_bold: Style
    red_berry5_solid_bold: Style
    red_berry5_outline_light: Style
    red_berry5_solid_light: Style
    red_berry5_dashed: Style
    red_berry5_dashed_bold: Style
    red_berry5_dashed_light: Style

    # RedBerry6
    red_berry6: Style
    red_berry6_bordered: Style
    red_berry6_bold: Style
    red_berry6_light: Style
    red_berry6_flat: Style
    red_berry6_outline: Style
    red_berry6_solid: Style
    red_berry6_outline_bold: Style
    red_berry6_solid_bold: Style
    red_berry6_outline_light: Style
    red_berry6_solid_light: Style
    red_berry6_dashed: Style
    red_berry6_dashed_bold: Style
    red_berry6_dashed_light: Style

    # --- Green Tones ---

    # Green1
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

    # Green2
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

    # Green3
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

    # Green4
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

    # Green5
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

    # Green6
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

    # --- Yellow Tones ---

    # Yellow1
    yellow1: Style
    yellow1_bordered: Style
    yellow1_bold: Style
    yellow1_light: Style
    yellow1_flat: Style
    yellow1_outline: Style
    yellow1_solid: Style
    yellow1_outline_bold: Style
    yellow1_solid_bold: Style
    yellow1_outline_light: Style
    yellow1_solid_light: Style
    yellow1_dashed: Style
    yellow1_dashed_bold: Style
    yellow1_dashed_light: Style

    # Yellow2
    yellow2: Style
    yellow2_bordered: Style
    yellow2_bold: Style
    yellow2_light: Style
    yellow2_flat: Style
    yellow2_outline: Style
    yellow2_solid: Style
    yellow2_outline_bold: Style
    yellow2_solid_bold: Style
    yellow2_outline_light: Style
    yellow2_solid_light: Style
    yellow2_dashed: Style
    yellow2_dashed_bold: Style
    yellow2_dashed_light: Style

    # Yellow3
    yellow3: Style
    yellow3_bordered: Style
    yellow3_bold: Style
    yellow3_light: Style
    yellow3_flat: Style
    yellow3_outline: Style
    yellow3_solid: Style
    yellow3_outline_bold: Style
    yellow3_solid_bold: Style
    yellow3_outline_light: Style
    yellow3_solid_light: Style
    yellow3_dashed: Style
    yellow3_dashed_bold: Style
    yellow3_dashed_light: Style

    # Yellow4
    yellow4: Style
    yellow4_bordered: Style
    yellow4_bold: Style
    yellow4_light: Style
    yellow4_flat: Style
    yellow4_outline: Style
    yellow4_solid: Style
    yellow4_outline_bold: Style
    yellow4_solid_bold: Style
    yellow4_outline_light: Style
    yellow4_solid_light: Style
    yellow4_dashed: Style
    yellow4_dashed_bold: Style
    yellow4_dashed_light: Style

    # Yellow5
    yellow5: Style
    yellow5_bordered: Style
    yellow5_bold: Style
    yellow5_light: Style
    yellow5_flat: Style
    yellow5_outline: Style
    yellow5_solid: Style
    yellow5_outline_bold: Style
    yellow5_solid_bold: Style
    yellow5_outline_light: Style
    yellow5_solid_light: Style
    yellow5_dashed: Style
    yellow5_dashed_bold: Style
    yellow5_dashed_light: Style

    # Yellow6
    yellow6: Style
    yellow6_bordered: Style
    yellow6_bold: Style
    yellow6_light: Style
    yellow6_flat: Style
    yellow6_outline: Style
    yellow6_solid: Style
    yellow6_outline_bold: Style
    yellow6_solid_bold: Style
    yellow6_outline_light: Style
    yellow6_solid_light: Style
    yellow6_dashed: Style
    yellow6_dashed_bold: Style
    yellow6_dashed_light: Style

    # --- Orange Tones ---

    # Orange1
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

    # Orange2
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

    # Orange3
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

    # Orange4
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

    # Orange5
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

    # Orange6
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

    # --- Cyan Tones ---

    # Cyan1
    cyan1: Style
    cyan1_bordered: Style
    cyan1_bold: Style
    cyan1_light: Style
    cyan1_flat: Style
    cyan1_outline: Style
    cyan1_solid: Style
    cyan1_outline_bold: Style
    cyan1_solid_bold: Style
    cyan1_outline_light: Style
    cyan1_solid_light: Style
    cyan1_dashed: Style
    cyan1_dashed_bold: Style
    cyan1_dashed_light: Style

    # Cyan2
    cyan2: Style
    cyan2_bordered: Style
    cyan2_bold: Style
    cyan2_light: Style
    cyan2_flat: Style
    cyan2_outline: Style
    cyan2_solid: Style
    cyan2_outline_bold: Style
    cyan2_solid_bold: Style
    cyan2_outline_light: Style
    cyan2_solid_light: Style
    cyan2_dashed: Style
    cyan2_dashed_bold: Style
    cyan2_dashed_light: Style

    # Cyan3
    cyan3: Style
    cyan3_bordered: Style
    cyan3_bold: Style
    cyan3_light: Style
    cyan3_flat: Style
    cyan3_outline: Style
    cyan3_solid: Style
    cyan3_outline_bold: Style
    cyan3_solid_bold: Style
    cyan3_outline_light: Style
    cyan3_solid_light: Style
    cyan3_dashed: Style
    cyan3_dashed_bold: Style
    cyan3_dashed_light: Style

    # Cyan4
    cyan4: Style
    cyan4_bordered: Style
    cyan4_bold: Style
    cyan4_light: Style
    cyan4_flat: Style
    cyan4_outline: Style
    cyan4_solid: Style
    cyan4_outline_bold: Style
    cyan4_solid_bold: Style
    cyan4_outline_light: Style
    cyan4_solid_light: Style
    cyan4_dashed: Style
    cyan4_dashed_bold: Style
    cyan4_dashed_light: Style

    # Cyan5
    cyan5: Style
    cyan5_bordered: Style
    cyan5_bold: Style
    cyan5_light: Style
    cyan5_flat: Style
    cyan5_outline: Style
    cyan5_solid: Style
    cyan5_outline_bold: Style
    cyan5_solid_bold: Style
    cyan5_outline_light: Style
    cyan5_solid_light: Style
    cyan5_dashed: Style
    cyan5_dashed_bold: Style
    cyan5_dashed_light: Style

    # Cyan6
    cyan6: Style
    cyan6_bordered: Style
    cyan6_bold: Style
    cyan6_light: Style
    cyan6_flat: Style
    cyan6_outline: Style
    cyan6_solid: Style
    cyan6_outline_bold: Style
    cyan6_solid_bold: Style
    cyan6_outline_light: Style
    cyan6_solid_light: Style
    cyan6_dashed: Style
    cyan6_dashed_bold: Style
    cyan6_dashed_light: Style

    # --- Purple Tones ---

    # Purple1
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

    # Purple2
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

    # Purple3
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

    # Purple4
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

    # Purple5
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

    # Purple6
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

    # --- Magenta Tones ---

    # Magenta1
    magenta1: Style
    magenta1_bordered: Style
    magenta1_bold: Style
    magenta1_light: Style
    magenta1_flat: Style
    magenta1_outline: Style
    magenta1_solid: Style
    magenta1_outline_bold: Style
    magenta1_solid_bold: Style
    magenta1_outline_light: Style
    magenta1_solid_light: Style
    magenta1_dashed: Style
    magenta1_dashed_bold: Style
    magenta1_dashed_light: Style

    # Magenta2
    magenta2: Style
    magenta2_bordered: Style
    magenta2_bold: Style
    magenta2_light: Style
    magenta2_flat: Style
    magenta2_outline: Style
    magenta2_solid: Style
    magenta2_outline_bold: Style
    magenta2_solid_bold: Style
    magenta2_outline_light: Style
    magenta2_solid_light: Style
    magenta2_dashed: Style
    magenta2_dashed_bold: Style
    magenta2_dashed_light: Style

    # Magenta3
    magenta3: Style
    magenta3_bordered: Style
    magenta3_bold: Style
    magenta3_light: Style
    magenta3_flat: Style
    magenta3_outline: Style
    magenta3_solid: Style
    magenta3_outline_bold: Style
    magenta3_solid_bold: Style
    magenta3_outline_light: Style
    magenta3_solid_light: Style
    magenta3_dashed: Style
    magenta3_dashed_bold: Style
    magenta3_dashed_light: Style

    # Magenta4
    magenta4: Style
    magenta4_bordered: Style
    magenta4_bold: Style
    magenta4_light: Style
    magenta4_flat: Style
    magenta4_outline: Style
    magenta4_solid: Style
    magenta4_outline_bold: Style
    magenta4_solid_bold: Style
    magenta4_outline_light: Style
    magenta4_solid_light: Style
    magenta4_dashed: Style
    magenta4_dashed_bold: Style
    magenta4_dashed_light: Style

    # Magenta5
    magenta5: Style
    magenta5_bordered: Style
    magenta5_bold: Style
    magenta5_light: Style
    magenta5_flat: Style
    magenta5_outline: Style
    magenta5_solid: Style
    magenta5_outline_bold: Style
    magenta5_solid_bold: Style
    magenta5_outline_light: Style
    magenta5_solid_light: Style
    magenta5_dashed: Style
    magenta5_dashed_bold: Style
    magenta5_dashed_light: Style

    # Magenta6
    magenta6: Style
    magenta6_bordered: Style
    magenta6_bold: Style
    magenta6_light: Style
    magenta6_flat: Style
    magenta6_outline: Style
    magenta6_solid: Style
    magenta6_outline_bold: Style
    magenta6_solid_bold: Style
    magenta6_outline_light: Style
    magenta6_solid_light: Style
    magenta6_dashed: Style
    magenta6_dashed_bold: Style
    magenta6_dashed_light: Style

    # --- Primaries (Unnumbered) ---

    # CornflowerBlue
    cornflower_blue: Style
    cornflower_blue_bordered: Style
    cornflower_blue_bold: Style
    cornflower_blue_light: Style
    cornflower_blue_flat: Style
    cornflower_blue_outline: Style
    cornflower_blue_solid: Style
    cornflower_blue_outline_bold: Style
    cornflower_blue_solid_bold: Style
    cornflower_blue_outline_light: Style
    cornflower_blue_solid_light: Style
    cornflower_blue_dashed: Style
    cornflower_blue_dashed_bold: Style
    cornflower_blue_dashed_light: Style

    # Blue
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

    # Red
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

    # RedBerry
    red_berry: Style
    red_berry_bordered: Style
    red_berry_bold: Style
    red_berry_light: Style
    red_berry_flat: Style
    red_berry_outline: Style
    red_berry_solid: Style
    red_berry_outline_bold: Style
    red_berry_solid_bold: Style
    red_berry_outline_light: Style
    red_berry_solid_light: Style
    red_berry_dashed: Style
    red_berry_dashed_bold: Style
    red_berry_dashed_light: Style

    # Green
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

    # Yellow
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

    # Orange
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

    # Cyan
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

    # Purple
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

    # Magenta
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

    # Pink
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

    # Lime
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

    # Teal
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

    # Navy
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

    # Olive
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

    # Brown
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

    # Gold
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

    # Aqua
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

    # GreenYellow
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

    # Ivory
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

    # Steel
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

    # --- Google Brand Colors ---

    # GoogleBlue
    google_blue: Style
    google_blue_bordered: Style
    google_blue_bold: Style
    google_blue_light: Style
    google_blue_flat: Style
    google_blue_outline: Style
    google_blue_solid: Style
    google_blue_outline_bold: Style
    google_blue_solid_bold: Style
    google_blue_outline_light: Style
    google_blue_solid_light: Style
    google_blue_dashed: Style
    google_blue_dashed_bold: Style
    google_blue_dashed_light: Style

    # GoogleRed
    google_red: Style
    google_red_bordered: Style
    google_red_bold: Style
    google_red_light: Style
    google_red_flat: Style
    google_red_outline: Style
    google_red_solid: Style
    google_red_outline_bold: Style
    google_red_solid_bold: Style
    google_red_outline_light: Style
    google_red_solid_light: Style
    google_red_dashed: Style
    google_red_dashed_bold: Style
    google_red_dashed_light: Style

    # GoogleYellow
    google_yellow: Style
    google_yellow_bordered: Style
    google_yellow_bold: Style
    google_yellow_light: Style
    google_yellow_flat: Style
    google_yellow_outline: Style
    google_yellow_solid: Style
    google_yellow_outline_bold: Style
    google_yellow_solid_bold: Style
    google_yellow_outline_light: Style
    google_yellow_solid_light: Style
    google_yellow_dashed: Style
    google_yellow_dashed_bold: Style
    google_yellow_dashed_light: Style

    # GoogleGreen
    google_green: Style
    google_green_bordered: Style
    google_green_bold: Style
    google_green_light: Style
    google_green_flat: Style
    google_green_outline: Style
    google_green_solid: Style
    google_green_outline_bold: Style
    google_green_solid_bold: Style
    google_green_outline_light: Style
    google_green_solid_light: Style
    google_green_dashed: Style
    google_green_dashed_bold: Style
    google_green_dashed_light: Style

    # GoogleOrange
    google_orange: Style
    google_orange_bordered: Style
    google_orange_bold: Style
    google_orange_light: Style
    google_orange_flat: Style
    google_orange_outline: Style
    google_orange_solid: Style
    google_orange_outline_bold: Style
    google_orange_solid_bold: Style
    google_orange_outline_light: Style
    google_orange_solid_light: Style
    google_orange_dashed: Style
    google_orange_dashed_bold: Style
    google_orange_dashed_light: Style

    # GooglePurple
    google_purple: Style
    google_purple_bordered: Style
    google_purple_bold: Style
    google_purple_light: Style
    google_purple_flat: Style
    google_purple_outline: Style
    google_purple_solid: Style
    google_purple_outline_bold: Style
    google_purple_solid_bold: Style
    google_purple_outline_light: Style
    google_purple_solid_light: Style
    google_purple_dashed: Style
    google_purple_dashed_bold: Style
    google_purple_dashed_light: Style

    # GoogleGray
    google_gray: Style
    google_gray_bordered: Style
    google_gray_bold: Style
    google_gray_light: Style
    google_gray_flat: Style
    google_gray_outline: Style
    google_gray_solid: Style
    google_gray_outline_bold: Style
    google_gray_solid_bold: Style
    google_gray_outline_light: Style
    google_gray_solid_light: Style
    google_gray_dashed: Style
    google_gray_dashed_bold: Style
    google_gray_dashed_light: Style

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
        "primary": col.Primary,
        "secondary": col.Secondary,
        "accent": col.Accent,
        "muted": col.Muted,
        "light": col.Light,
        "dark": col.Dark,
        "danger": col.Danger,
        "success": col.Success,
    }
    for role_name, color in semantic_map.items():
        v = _make_variants(color, border_color=border_color)
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

    # 2. Neutrals
    neutrals_map = {
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
    }

    # 3. Tones (10 hues x 6 tones)
    tones_map: dict[str, Color] = {}
    tones_map["cornflower_blue1"] = getattr(col, "CornflowerBlue1")
    tones_map["cornflower_blue2"] = getattr(col, "CornflowerBlue2")
    tones_map["cornflower_blue3"] = getattr(col, "CornflowerBlue3")
    tones_map["cornflower_blue4"] = getattr(col, "CornflowerBlue4")
    tones_map["cornflower_blue5"] = getattr(col, "CornflowerBlue5")
    tones_map["cornflower_blue6"] = getattr(col, "CornflowerBlue6")
    tones_map["blue1"] = getattr(col, "Blue1")
    tones_map["blue2"] = getattr(col, "Blue2")
    tones_map["blue3"] = getattr(col, "Blue3")
    tones_map["blue4"] = getattr(col, "Blue4")
    tones_map["blue5"] = getattr(col, "Blue5")
    tones_map["blue6"] = getattr(col, "Blue6")
    tones_map["red1"] = getattr(col, "Red1")
    tones_map["red2"] = getattr(col, "Red2")
    tones_map["red3"] = getattr(col, "Red3")
    tones_map["red4"] = getattr(col, "Red4")
    tones_map["red5"] = getattr(col, "Red5")
    tones_map["red6"] = getattr(col, "Red6")
    tones_map["red_berry1"] = getattr(col, "RedBerry1")
    tones_map["red_berry2"] = getattr(col, "RedBerry2")
    tones_map["red_berry3"] = getattr(col, "RedBerry3")
    tones_map["red_berry4"] = getattr(col, "RedBerry4")
    tones_map["red_berry5"] = getattr(col, "RedBerry5")
    tones_map["red_berry6"] = getattr(col, "RedBerry6")
    tones_map["green1"] = getattr(col, "Green1")
    tones_map["green2"] = getattr(col, "Green2")
    tones_map["green3"] = getattr(col, "Green3")
    tones_map["green4"] = getattr(col, "Green4")
    tones_map["green5"] = getattr(col, "Green5")
    tones_map["green6"] = getattr(col, "Green6")
    tones_map["yellow1"] = getattr(col, "Yellow1")
    tones_map["yellow2"] = getattr(col, "Yellow2")
    tones_map["yellow3"] = getattr(col, "Yellow3")
    tones_map["yellow4"] = getattr(col, "Yellow4")
    tones_map["yellow5"] = getattr(col, "Yellow5")
    tones_map["yellow6"] = getattr(col, "Yellow6")
    tones_map["orange1"] = getattr(col, "Orange1")
    tones_map["orange2"] = getattr(col, "Orange2")
    tones_map["orange3"] = getattr(col, "Orange3")
    tones_map["orange4"] = getattr(col, "Orange4")
    tones_map["orange5"] = getattr(col, "Orange5")
    tones_map["orange6"] = getattr(col, "Orange6")
    tones_map["cyan1"] = getattr(col, "Cyan1")
    tones_map["cyan2"] = getattr(col, "Cyan2")
    tones_map["cyan3"] = getattr(col, "Cyan3")
    tones_map["cyan4"] = getattr(col, "Cyan4")
    tones_map["cyan5"] = getattr(col, "Cyan5")
    tones_map["cyan6"] = getattr(col, "Cyan6")
    tones_map["purple1"] = getattr(col, "Purple1")
    tones_map["purple2"] = getattr(col, "Purple2")
    tones_map["purple3"] = getattr(col, "Purple3")
    tones_map["purple4"] = getattr(col, "Purple4")
    tones_map["purple5"] = getattr(col, "Purple5")
    tones_map["purple6"] = getattr(col, "Purple6")
    tones_map["magenta1"] = getattr(col, "Magenta1")
    tones_map["magenta2"] = getattr(col, "Magenta2")
    tones_map["magenta3"] = getattr(col, "Magenta3")
    tones_map["magenta4"] = getattr(col, "Magenta4")
    tones_map["magenta5"] = getattr(col, "Magenta5")
    tones_map["magenta6"] = getattr(col, "Magenta6")

    # 4. Primaries
    primaries_map: dict[str, Color] = {}
    primaries_map["cornflower_blue"] = getattr(col, "CornflowerBlue")
    primaries_map["blue"] = getattr(col, "Blue")
    primaries_map["red"] = getattr(col, "Red")
    primaries_map["red_berry"] = getattr(col, "RedBerry")
    primaries_map["green"] = getattr(col, "Green")
    primaries_map["yellow"] = getattr(col, "Yellow")
    primaries_map["orange"] = getattr(col, "Orange")
    primaries_map["cyan"] = getattr(col, "Cyan")
    primaries_map["purple"] = getattr(col, "Purple")
    primaries_map["magenta"] = getattr(col, "Magenta")
    primaries_map["pink"] = getattr(col, "Pink")
    primaries_map["lime"] = getattr(col, "Lime")
    primaries_map["teal"] = getattr(col, "Teal")
    primaries_map["navy"] = getattr(col, "Navy")
    primaries_map["olive"] = getattr(col, "Olive")
    primaries_map["brown"] = getattr(col, "Brown")
    primaries_map["gold"] = getattr(col, "Gold")
    primaries_map["aqua"] = getattr(col, "Aqua")
    primaries_map["green_yellow"] = getattr(col, "GreenYellow")
    primaries_map["ivory"] = getattr(col, "Ivory")
    primaries_map["steel"] = getattr(col, "Steel")

    # 5. Brand
    brand_map: dict[str, Color] = {}
    brand_map["google_blue"] = getattr(col, "GoogleBlue")
    brand_map["google_red"] = getattr(col, "GoogleRed")
    brand_map["google_yellow"] = getattr(col, "GoogleYellow")
    brand_map["google_green"] = getattr(col, "GoogleGreen")
    brand_map["google_orange"] = getattr(col, "GoogleOrange")
    brand_map["google_purple"] = getattr(col, "GooglePurple")
    brand_map["google_gray"] = getattr(col, "GoogleGray")

    # 6. Semantic Tones (6 roles x 6 tones)
    semantic_tones_map: dict[str, Color] = {}
    for r in ["primary", "secondary", "accent", "muted", "danger", "success"]:
        for i in range(1, 7):
            semantic_tones_map[f"{r}{i}"] = getattr(col, f"{r.capitalize()}{i}")

    all_colors: dict[str, Color] = {**neutrals_map, **tones_map, **primaries_map, **brand_map, **semantic_tones_map}
    for cname, color in all_colors.items():
        v = _make_variants(color, border_color=border_color)
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

    return GoogleStyles(**styles_dict)


_google_styles: GoogleStyles = _create_google_styles()
GoogleStyles.register_default_instance(_google_styles)

__all__ = [
    "GoogleStyles",
]
