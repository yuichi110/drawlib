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
from drawlib._core.l2_types import ColorType
from drawlib._core.styles import BaseColors, BaseStyles
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


class DefaultLightStyles(DefaultStyles):
    """Default light/pastel preset styles (Tone 1 centered)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default light preset styles instance."""
        super().__init__(**kwargs)


class DefaultDarkStyles(DefaultStyles):
    """Default dark mode preset styles (Tone 3 centered, dark canvas)."""

    def __init__(self, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize default dark preset styles instance."""
        super().__init__(**kwargs)


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
        bg_col = (255, 255, 255, 1.0)
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
