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
from typing import Any

from drawlib._core.fonts import FontSourceCode
from drawlib._core.styles import BaseStyles
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
    tones_map = {}
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
    primaries_map = {}
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
    brand_map = {}
    brand_map["google_blue"] = getattr(col, "GoogleBlue")
    brand_map["google_red"] = getattr(col, "GoogleRed")
    brand_map["google_yellow"] = getattr(col, "GoogleYellow")
    brand_map["google_green"] = getattr(col, "GoogleGreen")
    brand_map["google_orange"] = getattr(col, "GoogleOrange")

    all_colors = {**neutrals_map, **tones_map, **primaries_map, **brand_map}
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
