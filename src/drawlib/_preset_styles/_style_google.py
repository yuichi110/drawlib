# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Google Sheets preset styles module."""

from __future__ import annotations

from typing import Any

from drawlib._core.fonts import FontSourceCode
from drawlib._core.types import Style
from drawlib._preset_colors import google_colors
from drawlib._preset_styles._base import BaseStyles
from drawlib._preset_styles._utils import _DEFAULT_BORDER_COLOR, _make_variants

_DARK_GRAY_4: tuple[int, int, int, float] = (67, 67, 67, 1.0)
_WHITE: tuple[int, int, int, float] = (255, 255, 255, 1.0)

_GREYS: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "dark_gray_4": (67, 67, 67),
    "dark_gray_3": (102, 102, 102),
    "dark_gray_2": (153, 153, 153),
    "dark_gray_1": (183, 183, 183),
    "gray": (204, 204, 204),
    "light_gray_1": (217, 217, 217),
    "light_gray_2": (239, 239, 239),
    "light_gray_3": (243, 243, 243),
    "white": (255, 255, 255),
}

_HUES: dict[str, dict[str, tuple[int, int, int]]] = {
    "red_berry": {
        "light_3": (230, 184, 175),
        "light_2": (221, 126, 107),
        "light_1": (204, 65, 37),
        "base": (152, 0, 0),
        "dark_1": (166, 28, 0),
        "dark_2": (133, 32, 12),
        "dark_3": (91, 15, 0),
    },
    "red": {
        "light_3": (244, 204, 204),
        "light_2": (234, 153, 153),
        "light_1": (224, 102, 102),
        "base": (255, 0, 0),
        "dark_1": (204, 0, 0),
        "dark_2": (153, 0, 0),
        "dark_3": (102, 0, 0),
    },
    "orange": {
        "light_3": (252, 229, 205),
        "light_2": (249, 203, 156),
        "light_1": (246, 178, 107),
        "base": (255, 153, 0),
        "dark_1": (230, 145, 56),
        "dark_2": (180, 95, 6),
        "dark_3": (120, 63, 4),
    },
    "yellow": {
        "light_3": (255, 242, 204),
        "light_2": (255, 229, 153),
        "light_1": (255, 217, 102),
        "base": (255, 255, 0),
        "dark_1": (241, 194, 50),
        "dark_2": (191, 144, 0),
        "dark_3": (127, 96, 0),
    },
    "green": {
        "light_3": (217, 234, 211),
        "light_2": (182, 215, 168),
        "light_1": (147, 196, 125),
        "base": (0, 255, 0),
        "dark_1": (106, 168, 79),
        "dark_2": (56, 118, 29),
        "dark_3": (39, 78, 19),
    },
    "cyan": {
        "light_3": (208, 224, 227),
        "light_2": (162, 196, 201),
        "light_1": (118, 165, 175),
        "base": (0, 255, 255),
        "dark_1": (69, 129, 142),
        "dark_2": (19, 79, 92),
        "dark_3": (12, 52, 61),
    },
    "cornflower_blue": {
        "light_3": (201, 218, 248),
        "light_2": (164, 194, 244),
        "light_1": (109, 158, 235),
        "base": (74, 134, 232),
        "dark_1": (60, 120, 216),
        "dark_2": (17, 85, 204),
        "dark_3": (28, 69, 135),
    },
    "blue": {
        "light_3": (207, 226, 243),
        "light_2": (159, 197, 232),
        "light_1": (111, 168, 220),
        "base": (0, 0, 255),
        "dark_1": (61, 133, 198),
        "dark_2": (11, 83, 148),
        "dark_3": (7, 55, 99),
    },
    "purple": {
        "light_3": (217, 210, 233),
        "light_2": (180, 167, 214),
        "light_1": (142, 124, 195),
        "base": (153, 0, 255),
        "dark_1": (103, 78, 167),
        "dark_2": (53, 28, 117),
        "dark_3": (32, 18, 77),
    },
    "magenta": {
        "light_3": (234, 209, 220),
        "light_2": (213, 166, 189),
        "light_1": (194, 123, 160),
        "base": (255, 0, 255),
        "dark_1": (166, 77, 121),
        "dark_2": (116, 27, 71),
        "dark_3": (76, 17, 48),
    },
}


def _get_text_color(rgb: tuple[int, int, int, float]) -> tuple[int, int, int, float]:
    r, g, b, _ = rgb
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    if lum < 140:
        return _WHITE
    return _DARK_GRAY_4


def _collect_colors() -> dict[str, tuple[int, int, int, float]]:
    colors: dict[str, tuple[int, int, int, float]] = {}
    for name, rgb in _GREYS.items():
        colors[name] = (rgb[0], rgb[1], rgb[2], 1.0)

    for hue, shades in _HUES.items():
        for shade, rgb in shades.items():
            if shade == "base":
                cname = hue
            elif shade.startswith("light_"):
                num = shade.split("_")[1]
                cname = f"light_{hue}_{num}"
            else:
                num = shade.split("_")[1]
                cname = f"dark_{hue}_{num}"
            colors[cname] = (rgb[0], rgb[1], rgb[2], 1.0)

    # Aliases
    for name in list(_GREYS.keys()):
        if "gray" in name:
            colors[name.replace("gray", "grey")] = colors[name]
    colors["light_gray"] = colors["light_gray_1"]
    colors["light_grey"] = colors["light_gray_1"]
    colors["dark_gray"] = colors["dark_gray_1"]
    colors["dark_grey"] = colors["dark_gray_1"]

    for hue in _HUES:
        colors[f"light_{hue}"] = colors[f"light_{hue}_1"]
        colors[f"dark_{hue}"] = colors[f"dark_{hue}_1"]

    return colors


class StylesGoogle(BaseStyles):
    """Google Sheets preset styles with complete typing for IDE autocompletion."""

    # Greys / Neutrals
    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style
    black_light: Style
    black_dashed: Style
    dark_gray_4: Style
    dark_gray_4_flat: Style
    dark_gray_4_solid: Style
    dark_gray_4_bold: Style
    dark_gray_4_light: Style
    dark_gray_4_dashed: Style
    dark_gray_3: Style
    dark_gray_3_flat: Style
    dark_gray_3_solid: Style
    dark_gray_3_bold: Style
    dark_gray_3_light: Style
    dark_gray_3_dashed: Style
    dark_gray_2: Style
    dark_gray_2_flat: Style
    dark_gray_2_solid: Style
    dark_gray_2_bold: Style
    dark_gray_2_light: Style
    dark_gray_2_dashed: Style
    dark_gray_1: Style
    dark_gray_1_flat: Style
    dark_gray_1_solid: Style
    dark_gray_1_bold: Style
    dark_gray_1_light: Style
    dark_gray_1_dashed: Style
    gray: Style
    gray_flat: Style
    gray_solid: Style
    gray_bold: Style
    gray_light: Style
    gray_dashed: Style
    light_gray_1: Style
    light_gray_1_flat: Style
    light_gray_1_solid: Style
    light_gray_1_bold: Style
    light_gray_1_light: Style
    light_gray_1_dashed: Style
    light_gray_2: Style
    light_gray_2_flat: Style
    light_gray_2_solid: Style
    light_gray_2_bold: Style
    light_gray_2_light: Style
    light_gray_2_dashed: Style
    light_gray_3: Style
    light_gray_3_flat: Style
    light_gray_3_solid: Style
    light_gray_3_bold: Style
    light_gray_3_light: Style
    light_gray_3_dashed: Style
    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style
    white_light: Style
    white_dashed: Style
    dark_grey_4: Style
    dark_grey_4_flat: Style
    dark_grey_4_solid: Style
    dark_grey_4_bold: Style
    dark_grey_4_light: Style
    dark_grey_4_dashed: Style
    dark_grey_3: Style
    dark_grey_3_flat: Style
    dark_grey_3_solid: Style
    dark_grey_3_bold: Style
    dark_grey_3_light: Style
    dark_grey_3_dashed: Style
    dark_grey_2: Style
    dark_grey_2_flat: Style
    dark_grey_2_solid: Style
    dark_grey_2_bold: Style
    dark_grey_2_light: Style
    dark_grey_2_dashed: Style
    dark_grey_1: Style
    dark_grey_1_flat: Style
    dark_grey_1_solid: Style
    dark_grey_1_bold: Style
    dark_grey_1_light: Style
    dark_grey_1_dashed: Style
    grey: Style
    grey_flat: Style
    grey_solid: Style
    grey_bold: Style
    grey_light: Style
    grey_dashed: Style
    light_grey_1: Style
    light_grey_1_flat: Style
    light_grey_1_solid: Style
    light_grey_1_bold: Style
    light_grey_1_light: Style
    light_grey_1_dashed: Style
    light_grey_2: Style
    light_grey_2_flat: Style
    light_grey_2_solid: Style
    light_grey_2_bold: Style
    light_grey_2_light: Style
    light_grey_2_dashed: Style
    light_grey_3: Style
    light_grey_3_flat: Style
    light_grey_3_solid: Style
    light_grey_3_bold: Style
    light_grey_3_light: Style
    light_grey_3_dashed: Style
    light_gray: Style
    light_gray_flat: Style
    light_gray_solid: Style
    light_gray_bold: Style
    light_gray_light: Style
    light_gray_dashed: Style
    light_grey: Style
    light_grey_flat: Style
    light_grey_solid: Style
    light_grey_bold: Style
    light_grey_light: Style
    light_grey_dashed: Style
    dark_gray: Style
    dark_gray_flat: Style
    dark_gray_solid: Style
    dark_gray_bold: Style
    dark_gray_light: Style
    dark_gray_dashed: Style
    dark_grey: Style
    dark_grey_flat: Style
    dark_grey_solid: Style
    dark_grey_bold: Style
    dark_grey_light: Style
    dark_grey_dashed: Style

    # Red Berry
    red_berry: Style
    red_berry_flat: Style
    red_berry_solid: Style
    red_berry_bold: Style
    red_berry_light: Style
    red_berry_dashed: Style
    light_red_berry_1: Style
    light_red_berry_1_flat: Style
    light_red_berry_1_solid: Style
    light_red_berry_1_bold: Style
    light_red_berry_1_light: Style
    light_red_berry_1_dashed: Style
    light_red_berry_2: Style
    light_red_berry_2_flat: Style
    light_red_berry_2_solid: Style
    light_red_berry_2_bold: Style
    light_red_berry_2_light: Style
    light_red_berry_2_dashed: Style
    light_red_berry_3: Style
    light_red_berry_3_flat: Style
    light_red_berry_3_solid: Style
    light_red_berry_3_bold: Style
    light_red_berry_3_light: Style
    light_red_berry_3_dashed: Style
    dark_red_berry_1: Style
    dark_red_berry_1_flat: Style
    dark_red_berry_1_solid: Style
    dark_red_berry_1_bold: Style
    dark_red_berry_1_light: Style
    dark_red_berry_1_dashed: Style
    dark_red_berry_2: Style
    dark_red_berry_2_flat: Style
    dark_red_berry_2_solid: Style
    dark_red_berry_2_bold: Style
    dark_red_berry_2_light: Style
    dark_red_berry_2_dashed: Style
    dark_red_berry_3: Style
    dark_red_berry_3_flat: Style
    dark_red_berry_3_solid: Style
    dark_red_berry_3_bold: Style
    dark_red_berry_3_light: Style
    dark_red_berry_3_dashed: Style
    light_red_berry: Style
    light_red_berry_flat: Style
    light_red_berry_solid: Style
    light_red_berry_bold: Style
    light_red_berry_light: Style
    light_red_berry_dashed: Style
    dark_red_berry: Style
    dark_red_berry_flat: Style
    dark_red_berry_solid: Style
    dark_red_berry_bold: Style
    dark_red_berry_light: Style
    dark_red_berry_dashed: Style

    # Red
    red: Style
    red_flat: Style
    red_solid: Style
    red_bold: Style
    red_light: Style
    red_dashed: Style
    light_red_1: Style
    light_red_1_flat: Style
    light_red_1_solid: Style
    light_red_1_bold: Style
    light_red_1_light: Style
    light_red_1_dashed: Style
    light_red_2: Style
    light_red_2_flat: Style
    light_red_2_solid: Style
    light_red_2_bold: Style
    light_red_2_light: Style
    light_red_2_dashed: Style
    light_red_3: Style
    light_red_3_flat: Style
    light_red_3_solid: Style
    light_red_3_bold: Style
    light_red_3_light: Style
    light_red_3_dashed: Style
    dark_red_1: Style
    dark_red_1_flat: Style
    dark_red_1_solid: Style
    dark_red_1_bold: Style
    dark_red_1_light: Style
    dark_red_1_dashed: Style
    dark_red_2: Style
    dark_red_2_flat: Style
    dark_red_2_solid: Style
    dark_red_2_bold: Style
    dark_red_2_light: Style
    dark_red_2_dashed: Style
    dark_red_3: Style
    dark_red_3_flat: Style
    dark_red_3_solid: Style
    dark_red_3_bold: Style
    dark_red_3_light: Style
    dark_red_3_dashed: Style
    light_red: Style
    light_red_flat: Style
    light_red_solid: Style
    light_red_bold: Style
    light_red_light: Style
    light_red_dashed: Style
    dark_red: Style
    dark_red_flat: Style
    dark_red_solid: Style
    dark_red_bold: Style
    dark_red_light: Style
    dark_red_dashed: Style

    # Orange
    orange: Style
    orange_flat: Style
    orange_solid: Style
    orange_bold: Style
    orange_light: Style
    orange_dashed: Style
    light_orange_1: Style
    light_orange_1_flat: Style
    light_orange_1_solid: Style
    light_orange_1_bold: Style
    light_orange_1_light: Style
    light_orange_1_dashed: Style
    light_orange_2: Style
    light_orange_2_flat: Style
    light_orange_2_solid: Style
    light_orange_2_bold: Style
    light_orange_2_light: Style
    light_orange_2_dashed: Style
    light_orange_3: Style
    light_orange_3_flat: Style
    light_orange_3_solid: Style
    light_orange_3_bold: Style
    light_orange_3_light: Style
    light_orange_3_dashed: Style
    dark_orange_1: Style
    dark_orange_1_flat: Style
    dark_orange_1_solid: Style
    dark_orange_1_bold: Style
    dark_orange_1_light: Style
    dark_orange_1_dashed: Style
    dark_orange_2: Style
    dark_orange_2_flat: Style
    dark_orange_2_solid: Style
    dark_orange_2_bold: Style
    dark_orange_2_light: Style
    dark_orange_2_dashed: Style
    dark_orange_3: Style
    dark_orange_3_flat: Style
    dark_orange_3_solid: Style
    dark_orange_3_bold: Style
    dark_orange_3_light: Style
    dark_orange_3_dashed: Style
    light_orange: Style
    light_orange_flat: Style
    light_orange_solid: Style
    light_orange_bold: Style
    light_orange_light: Style
    light_orange_dashed: Style
    dark_orange: Style
    dark_orange_flat: Style
    dark_orange_solid: Style
    dark_orange_bold: Style
    dark_orange_light: Style
    dark_orange_dashed: Style

    # Yellow
    yellow: Style
    yellow_flat: Style
    yellow_solid: Style
    yellow_bold: Style
    yellow_light: Style
    yellow_dashed: Style
    light_yellow_1: Style
    light_yellow_1_flat: Style
    light_yellow_1_solid: Style
    light_yellow_1_bold: Style
    light_yellow_1_light: Style
    light_yellow_1_dashed: Style
    light_yellow_2: Style
    light_yellow_2_flat: Style
    light_yellow_2_solid: Style
    light_yellow_2_bold: Style
    light_yellow_2_light: Style
    light_yellow_2_dashed: Style
    light_yellow_3: Style
    light_yellow_3_flat: Style
    light_yellow_3_solid: Style
    light_yellow_3_bold: Style
    light_yellow_3_light: Style
    light_yellow_3_dashed: Style
    dark_yellow_1: Style
    dark_yellow_1_flat: Style
    dark_yellow_1_solid: Style
    dark_yellow_1_bold: Style
    dark_yellow_1_light: Style
    dark_yellow_1_dashed: Style
    dark_yellow_2: Style
    dark_yellow_2_flat: Style
    dark_yellow_2_solid: Style
    dark_yellow_2_bold: Style
    dark_yellow_2_light: Style
    dark_yellow_2_dashed: Style
    dark_yellow_3: Style
    dark_yellow_3_flat: Style
    dark_yellow_3_solid: Style
    dark_yellow_3_bold: Style
    dark_yellow_3_light: Style
    dark_yellow_3_dashed: Style
    light_yellow: Style
    light_yellow_flat: Style
    light_yellow_solid: Style
    light_yellow_bold: Style
    light_yellow_light: Style
    light_yellow_dashed: Style
    dark_yellow: Style
    dark_yellow_flat: Style
    dark_yellow_solid: Style
    dark_yellow_bold: Style
    dark_yellow_light: Style
    dark_yellow_dashed: Style

    # Green
    green: Style
    green_flat: Style
    green_solid: Style
    green_bold: Style
    green_light: Style
    green_dashed: Style
    light_green_1: Style
    light_green_1_flat: Style
    light_green_1_solid: Style
    light_green_1_bold: Style
    light_green_1_light: Style
    light_green_1_dashed: Style
    light_green_2: Style
    light_green_2_flat: Style
    light_green_2_solid: Style
    light_green_2_bold: Style
    light_green_2_light: Style
    light_green_2_dashed: Style
    light_green_3: Style
    light_green_3_flat: Style
    light_green_3_solid: Style
    light_green_3_bold: Style
    light_green_3_light: Style
    light_green_3_dashed: Style
    dark_green_1: Style
    dark_green_1_flat: Style
    dark_green_1_solid: Style
    dark_green_1_bold: Style
    dark_green_1_light: Style
    dark_green_1_dashed: Style
    dark_green_2: Style
    dark_green_2_flat: Style
    dark_green_2_solid: Style
    dark_green_2_bold: Style
    dark_green_2_light: Style
    dark_green_2_dashed: Style
    dark_green_3: Style
    dark_green_3_flat: Style
    dark_green_3_solid: Style
    dark_green_3_bold: Style
    dark_green_3_light: Style
    dark_green_3_dashed: Style
    light_green: Style
    light_green_flat: Style
    light_green_solid: Style
    light_green_bold: Style
    light_green_light: Style
    light_green_dashed: Style
    dark_green: Style
    dark_green_flat: Style
    dark_green_solid: Style
    dark_green_bold: Style
    dark_green_light: Style
    dark_green_dashed: Style

    # Cyan
    cyan: Style
    cyan_flat: Style
    cyan_solid: Style
    cyan_bold: Style
    cyan_light: Style
    cyan_dashed: Style
    light_cyan_1: Style
    light_cyan_1_flat: Style
    light_cyan_1_solid: Style
    light_cyan_1_bold: Style
    light_cyan_1_light: Style
    light_cyan_1_dashed: Style
    light_cyan_2: Style
    light_cyan_2_flat: Style
    light_cyan_2_solid: Style
    light_cyan_2_bold: Style
    light_cyan_2_light: Style
    light_cyan_2_dashed: Style
    light_cyan_3: Style
    light_cyan_3_flat: Style
    light_cyan_3_solid: Style
    light_cyan_3_bold: Style
    light_cyan_3_light: Style
    light_cyan_3_dashed: Style
    dark_cyan_1: Style
    dark_cyan_1_flat: Style
    dark_cyan_1_solid: Style
    dark_cyan_1_bold: Style
    dark_cyan_1_light: Style
    dark_cyan_1_dashed: Style
    dark_cyan_2: Style
    dark_cyan_2_flat: Style
    dark_cyan_2_solid: Style
    dark_cyan_2_bold: Style
    dark_cyan_2_light: Style
    dark_cyan_2_dashed: Style
    dark_cyan_3: Style
    dark_cyan_3_flat: Style
    dark_cyan_3_solid: Style
    dark_cyan_3_bold: Style
    dark_cyan_3_light: Style
    dark_cyan_3_dashed: Style
    light_cyan: Style
    light_cyan_flat: Style
    light_cyan_solid: Style
    light_cyan_bold: Style
    light_cyan_light: Style
    light_cyan_dashed: Style
    dark_cyan: Style
    dark_cyan_flat: Style
    dark_cyan_solid: Style
    dark_cyan_bold: Style
    dark_cyan_light: Style
    dark_cyan_dashed: Style

    # Cornflower Blue
    cornflower_blue: Style
    cornflower_blue_flat: Style
    cornflower_blue_solid: Style
    cornflower_blue_bold: Style
    cornflower_blue_light: Style
    cornflower_blue_dashed: Style
    light_cornflower_blue_1: Style
    light_cornflower_blue_1_flat: Style
    light_cornflower_blue_1_solid: Style
    light_cornflower_blue_1_bold: Style
    light_cornflower_blue_1_light: Style
    light_cornflower_blue_1_dashed: Style
    light_cornflower_blue_2: Style
    light_cornflower_blue_2_flat: Style
    light_cornflower_blue_2_solid: Style
    light_cornflower_blue_2_bold: Style
    light_cornflower_blue_2_light: Style
    light_cornflower_blue_2_dashed: Style
    light_cornflower_blue_3: Style
    light_cornflower_blue_3_flat: Style
    light_cornflower_blue_3_solid: Style
    light_cornflower_blue_3_bold: Style
    light_cornflower_blue_3_light: Style
    light_cornflower_blue_3_dashed: Style
    dark_cornflower_blue_1: Style
    dark_cornflower_blue_1_flat: Style
    dark_cornflower_blue_1_solid: Style
    dark_cornflower_blue_1_bold: Style
    dark_cornflower_blue_1_light: Style
    dark_cornflower_blue_1_dashed: Style
    dark_cornflower_blue_2: Style
    dark_cornflower_blue_2_flat: Style
    dark_cornflower_blue_2_solid: Style
    dark_cornflower_blue_2_bold: Style
    dark_cornflower_blue_2_light: Style
    dark_cornflower_blue_2_dashed: Style
    dark_cornflower_blue_3: Style
    dark_cornflower_blue_3_flat: Style
    dark_cornflower_blue_3_solid: Style
    dark_cornflower_blue_3_bold: Style
    dark_cornflower_blue_3_light: Style
    dark_cornflower_blue_3_dashed: Style
    light_cornflower_blue: Style
    light_cornflower_blue_flat: Style
    light_cornflower_blue_solid: Style
    light_cornflower_blue_bold: Style
    light_cornflower_blue_light: Style
    light_cornflower_blue_dashed: Style
    dark_cornflower_blue: Style
    dark_cornflower_blue_flat: Style
    dark_cornflower_blue_solid: Style
    dark_cornflower_blue_bold: Style
    dark_cornflower_blue_light: Style
    dark_cornflower_blue_dashed: Style

    # Blue
    blue: Style
    blue_flat: Style
    blue_solid: Style
    blue_bold: Style
    blue_light: Style
    blue_dashed: Style
    light_blue_1: Style
    light_blue_1_flat: Style
    light_blue_1_solid: Style
    light_blue_1_bold: Style
    light_blue_1_light: Style
    light_blue_1_dashed: Style
    light_blue_2: Style
    light_blue_2_flat: Style
    light_blue_2_solid: Style
    light_blue_2_bold: Style
    light_blue_2_light: Style
    light_blue_2_dashed: Style
    light_blue_3: Style
    light_blue_3_flat: Style
    light_blue_3_solid: Style
    light_blue_3_bold: Style
    light_blue_3_light: Style
    light_blue_3_dashed: Style
    dark_blue_1: Style
    dark_blue_1_flat: Style
    dark_blue_1_solid: Style
    dark_blue_1_bold: Style
    dark_blue_1_light: Style
    dark_blue_1_dashed: Style
    dark_blue_2: Style
    dark_blue_2_flat: Style
    dark_blue_2_solid: Style
    dark_blue_2_bold: Style
    dark_blue_2_light: Style
    dark_blue_2_dashed: Style
    dark_blue_3: Style
    dark_blue_3_flat: Style
    dark_blue_3_solid: Style
    dark_blue_3_bold: Style
    dark_blue_3_light: Style
    dark_blue_3_dashed: Style
    light_blue: Style
    light_blue_flat: Style
    light_blue_solid: Style
    light_blue_bold: Style
    light_blue_light: Style
    light_blue_dashed: Style
    dark_blue: Style
    dark_blue_flat: Style
    dark_blue_solid: Style
    dark_blue_bold: Style
    dark_blue_light: Style
    dark_blue_dashed: Style

    # Purple
    purple: Style
    purple_flat: Style
    purple_solid: Style
    purple_bold: Style
    purple_light: Style
    purple_dashed: Style
    light_purple_1: Style
    light_purple_1_flat: Style
    light_purple_1_solid: Style
    light_purple_1_bold: Style
    light_purple_1_light: Style
    light_purple_1_dashed: Style
    light_purple_2: Style
    light_purple_2_flat: Style
    light_purple_2_solid: Style
    light_purple_2_bold: Style
    light_purple_2_light: Style
    light_purple_2_dashed: Style
    light_purple_3: Style
    light_purple_3_flat: Style
    light_purple_3_solid: Style
    light_purple_3_bold: Style
    light_purple_3_light: Style
    light_purple_3_dashed: Style
    dark_purple_1: Style
    dark_purple_1_flat: Style
    dark_purple_1_solid: Style
    dark_purple_1_bold: Style
    dark_purple_1_light: Style
    dark_purple_1_dashed: Style
    dark_purple_2: Style
    dark_purple_2_flat: Style
    dark_purple_2_solid: Style
    dark_purple_2_bold: Style
    dark_purple_2_light: Style
    dark_purple_2_dashed: Style
    dark_purple_3: Style
    dark_purple_3_flat: Style
    dark_purple_3_solid: Style
    dark_purple_3_bold: Style
    dark_purple_3_light: Style
    dark_purple_3_dashed: Style
    light_purple: Style
    light_purple_flat: Style
    light_purple_solid: Style
    light_purple_bold: Style
    light_purple_light: Style
    light_purple_dashed: Style
    dark_purple: Style
    dark_purple_flat: Style
    dark_purple_solid: Style
    dark_purple_bold: Style
    dark_purple_light: Style
    dark_purple_dashed: Style

    # Magenta
    magenta: Style
    magenta_flat: Style
    magenta_solid: Style
    magenta_bold: Style
    magenta_light: Style
    magenta_dashed: Style
    light_magenta_1: Style
    light_magenta_1_flat: Style
    light_magenta_1_solid: Style
    light_magenta_1_bold: Style
    light_magenta_1_light: Style
    light_magenta_1_dashed: Style
    light_magenta_2: Style
    light_magenta_2_flat: Style
    light_magenta_2_solid: Style
    light_magenta_2_bold: Style
    light_magenta_2_light: Style
    light_magenta_2_dashed: Style
    light_magenta_3: Style
    light_magenta_3_flat: Style
    light_magenta_3_solid: Style
    light_magenta_3_bold: Style
    light_magenta_3_light: Style
    light_magenta_3_dashed: Style
    dark_magenta_1: Style
    dark_magenta_1_flat: Style
    dark_magenta_1_solid: Style
    dark_magenta_1_bold: Style
    dark_magenta_1_light: Style
    dark_magenta_1_dashed: Style
    dark_magenta_2: Style
    dark_magenta_2_flat: Style
    dark_magenta_2_solid: Style
    dark_magenta_2_bold: Style
    dark_magenta_2_light: Style
    dark_magenta_2_dashed: Style
    dark_magenta_3: Style
    dark_magenta_3_flat: Style
    dark_magenta_3_solid: Style
    dark_magenta_3_bold: Style
    dark_magenta_3_light: Style
    dark_magenta_3_dashed: Style
    light_magenta: Style
    light_magenta_flat: Style
    light_magenta_solid: Style
    light_magenta_bold: Style
    light_magenta_light: Style
    light_magenta_dashed: Style
    dark_magenta: Style
    dark_magenta_flat: Style
    dark_magenta_solid: Style
    dark_magenta_bold: Style
    dark_magenta_light: Style
    dark_magenta_dashed: Style

    # Danger
    danger: Style
    danger_bordered: Style
    danger_bold: Style
    danger_light: Style
    danger_flat: Style
    danger_outline: Style
    danger_outline_bold: Style
    danger_outline_light: Style
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
    success_outline_bold: Style
    success_outline_light: Style
    success_dashed: Style
    success_dashed_bold: Style
    success_dashed_light: Style


# Backwards compatibility alias
GoogleStyles = StylesGoogle


def _create_google_styles() -> StylesGoogle:
    """Generate Google Sheets preset styles.

    Returns:
        StylesGoogle: Google Sheets preset styles instance.
    """
    colors = _collect_colors()
    styles: dict[str, Any] = {
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
    }

    semantic_map = {
        "primary": google_colors.Primary,
        "secondary": google_colors.Secondary,
        "accent": google_colors.Accent,
        "muted": google_colors.Muted,
        "danger": google_colors.Danger,
        "success": google_colors.Success,
    }

    for role_name, color in semantic_map.items():
        if color is not None:
            v = _make_variants(color)
            styles[role_name] = v["normal"]
            styles[f"{role_name}_bordered"] = v["bordered"]
            styles[f"{role_name}_bold"] = v["bold"]
            styles[f"{role_name}_light"] = v["light"]
            styles[f"{role_name}_flat"] = v["flat"]
            styles[f"{role_name}_outline"] = v["outline"]
            styles[f"{role_name}_outline_bold"] = v["outline_bold"]
            styles[f"{role_name}_outline_light"] = v["outline_light"]
            styles[f"{role_name}_dashed"] = v["dashed"]
            styles[f"{role_name}_dashed_bold"] = v["dashed_bold"]
            styles[f"{role_name}_dashed_light"] = v["dashed_light"]

    for cname, col in colors.items():
        txt_col = _get_text_color(col)
        border_col = _DARK_GRAY_4 if cname == "white" else _DEFAULT_BORDER_COLOR
        v = _make_variants(col, border_color=border_col, default_text_color=txt_col)
        styles[cname] = v["normal"]
        styles[f"{cname}_bordered"] = v["bordered"]
        styles[f"{cname}_bold"] = v["bold"]
        styles[f"{cname}_light"] = v["light"]
        styles[f"{cname}_flat"] = v["flat"]
        styles[f"{cname}_outline"] = v["outline"]
        styles[f"{cname}_solid"] = v["solid"]
        styles[f"{cname}_outline_bold"] = v["outline_bold"]
        styles[f"{cname}_solid_bold"] = v["solid_bold"]
        styles[f"{cname}_outline_light"] = v["outline_light"]
        styles[f"{cname}_solid_light"] = v["solid_light"]
        styles[f"{cname}_dashed"] = v["dashed"]
        styles[f"{cname}_dashed_bold"] = v["dashed_bold"]
        styles[f"{cname}_dashed_light"] = v["dashed_light"]

    return StylesGoogle(**styles)


google_styles: StylesGoogle = _create_google_styles()

__all__ = [
    "GoogleStyles",
    "StylesGoogle",
    "google_styles",
]
