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
from typing import Any, Literal

from drawlib._core.fonts import FontSourceCode
from drawlib._core.styles import BaseStyles
from drawlib._core.types import Style
from drawlib._preset_colors import (
    DefaultColors,
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

    # Amber1
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

    # Amber2
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

    # Amber3
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

    # Amber4
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

    # Teal1
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

    # Teal2
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

    # Teal3
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

    # Teal4
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

    # Pink1
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

    # Pink2
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

    # Pink3
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

    # Pink4
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

    # Green Yellow
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

    # Canvas
    canvas: Style
    canvas_flat: Style


class DefaultLightStyles(DefaultStyles):
    """Default light/pastel preset styles (Tone 1 centered)."""


class DefaultDarkStyles(DefaultStyles):
    """Default dark mode preset styles (Tone 3 centered, dark canvas)."""


def _create_default_styles(  # noqa: C901
    theme: Literal["default", "light", "dark"] = "default",
) -> DefaultStyles:
    """Generate default preset styles for the given theme variant.

    Args:
        theme (Literal["default", "light", "dark"]): Theme variant to generate. Defaults to "default".

    Returns:
        StylesDefault: Default preset styles instance.
    """
    if theme == "light":
        col = DefaultLightColors
        bg_col = (255, 255, 255, 1.0)
    elif theme == "dark":
        col = DefaultDarkColors
        bg_col = (24, 28, 36, 1.0)
    else:
        col = DefaultColors
        bg_col = (255, 255, 255, 1.0)

    # 1. Colors Map for all registered color names
    colors_map = {
        # 4 Tones
        "blue1": col.Blue1, "blue2": col.Blue2, "blue3": col.Blue3, "blue4": col.Blue4,
        "green1": col.Green1, "green2": col.Green2, "green3": col.Green3, "green4": col.Green4,
        "red1": col.Red1, "red2": col.Red2, "red3": col.Red3, "red4": col.Red4,
        "orange1": col.Orange1, "orange2": col.Orange2, "orange3": col.Orange3, "orange4": col.Orange4,
        "amber1": col.Amber1, "amber2": col.Amber2, "amber3": col.Amber3, "amber4": col.Amber4,
        "purple1": col.Purple1, "purple2": col.Purple2, "purple3": col.Purple3, "purple4": col.Purple4,
        "teal1": col.Teal1, "teal2": col.Teal2, "teal3": col.Teal3, "teal4": col.Teal4,
        "pink1": col.Pink1, "pink2": col.Pink2, "pink3": col.Pink3, "pink4": col.Pink4,
        # Neutrals
        "white": col.White, "gray1": col.Gray1, "gray2": col.Gray2, "gray3": col.Gray3,
        "gray4": col.Gray4, "gray5": col.Gray5, "gray6": col.Gray6, "gray7": col.Gray7,
        "gray8": col.Gray8, "black": col.Black,
        # Standard Primaries
        "red": col.Red, "green": col.Green, "blue": col.Blue, "yellow": col.Yellow,
        "orange": col.Orange, "purple": col.Purple, "pink": col.Pink, "cyan": col.Cyan,
        "magenta": col.Magenta, "lime": col.Lime, "teal": col.Teal, "navy": col.Navy,
        "brown": col.Brown, "olive": col.Olive, "gold": col.Gold, "aqua": col.Aqua, "green_yellow": col.GreenYellow,
        "ivory": col.Ivory, "steel": col.Steel,
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
                v = _make_variants(
                    color,
                    border_color=col.Gray5,
                    default_text_color=col.Gray4,
                    line_color=col.Gray4,
                )
            elif role_name == "light":
                v = _make_variants(
                    color,
                    border_color=col.Gray4,
                    default_text_color=col.Gray5,
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

    if theme == "light":
        return DefaultLightStyles(**styles_dict)
    elif theme == "dark":
        return DefaultDarkStyles(**styles_dict)
    return DefaultStyles(**styles_dict)


_default_styles: DefaultStyles = _create_default_styles("default")
_default_light_styles: DefaultLightStyles = _create_default_styles("light")  # type: ignore
_default_dark_styles: DefaultDarkStyles = _create_default_styles("dark")    # type: ignore

DefaultStyles.register_default_instance(_default_styles)
DefaultLightStyles.register_default_instance(_default_light_styles)
DefaultDarkStyles.register_default_instance(_default_dark_styles)

__all__ = [
    "DefaultDarkStyles",
    "DefaultLightStyles",
    "DefaultStyles",
]
