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

from typing import Any

from drawlib._core.fonts import FontSourceCode
from drawlib._core.types import Style
from drawlib._preset_colors import default_colors
from drawlib._preset_styles._base import BaseStyles
from drawlib._preset_styles._utils import _make_variants


class StylesDefault(BaseStyles):
    """Default preset styles with complete typing for IDE autocompletion."""

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

    # Light Red
    light_red: Style
    light_red_bordered: Style
    light_red_bold: Style
    light_red_light: Style
    light_red_flat: Style
    light_red_outline: Style
    light_red_solid: Style
    light_red_outline_bold: Style
    light_red_solid_bold: Style
    light_red_outline_light: Style
    light_red_solid_light: Style
    light_red_dashed: Style
    light_red_dashed_bold: Style
    light_red_dashed_light: Style

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

    # Light Green
    light_green: Style
    light_green_bordered: Style
    light_green_bold: Style
    light_green_light: Style
    light_green_flat: Style
    light_green_outline: Style
    light_green_solid: Style
    light_green_outline_bold: Style
    light_green_solid_bold: Style
    light_green_outline_light: Style
    light_green_solid_light: Style
    light_green_dashed: Style
    light_green_dashed_bold: Style
    light_green_dashed_light: Style

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

    # Light Blue
    light_blue: Style
    light_blue_bordered: Style
    light_blue_bold: Style
    light_blue_light: Style
    light_blue_flat: Style
    light_blue_outline: Style
    light_blue_solid: Style
    light_blue_outline_bold: Style
    light_blue_solid_bold: Style
    light_blue_outline_light: Style
    light_blue_solid_light: Style
    light_blue_dashed: Style
    light_blue_dashed_bold: Style
    light_blue_dashed_light: Style

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

    # Charcoal
    charcoal: Style
    charcoal_bordered: Style
    charcoal_bold: Style
    charcoal_light: Style
    charcoal_flat: Style
    charcoal_outline: Style
    charcoal_solid: Style
    charcoal_outline_bold: Style
    charcoal_solid_bold: Style
    charcoal_outline_light: Style
    charcoal_solid_light: Style
    charcoal_dashed: Style
    charcoal_dashed_bold: Style
    charcoal_dashed_light: Style

    # Graphite
    graphite: Style
    graphite_bordered: Style
    graphite_bold: Style
    graphite_light: Style
    graphite_flat: Style
    graphite_outline: Style
    graphite_solid: Style
    graphite_outline_bold: Style
    graphite_solid_bold: Style
    graphite_outline_light: Style
    graphite_solid_light: Style
    graphite_dashed: Style
    graphite_dashed_bold: Style
    graphite_dashed_light: Style

    # Gray
    gray: Style
    gray_bordered: Style
    gray_bold: Style
    gray_light: Style
    gray_flat: Style
    gray_outline: Style
    gray_solid: Style
    gray_outline_bold: Style
    gray_solid_bold: Style
    gray_outline_light: Style
    gray_solid_light: Style
    gray_dashed: Style
    gray_dashed_bold: Style
    gray_dashed_light: Style

    # Silver
    silver: Style
    silver_bordered: Style
    silver_bold: Style
    silver_light: Style
    silver_flat: Style
    silver_outline: Style
    silver_solid: Style
    silver_outline_bold: Style
    silver_solid_bold: Style
    silver_outline_light: Style
    silver_solid_light: Style
    silver_dashed: Style
    silver_dashed_bold: Style
    silver_dashed_light: Style

    # Snow
    snow: Style
    snow_bordered: Style
    snow_bold: Style
    snow_light: Style
    snow_flat: Style
    snow_outline: Style
    snow_solid: Style
    snow_outline_bold: Style
    snow_solid_bold: Style
    snow_outline_light: Style
    snow_solid_light: Style
    snow_dashed: Style
    snow_dashed_bold: Style
    snow_dashed_light: Style

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


# Backwards compatibility alias
DefaultStyles = StylesDefault


def _create_default_styles() -> StylesDefault:
    """Generate default preset styles.

    Returns:
        StylesDefault: Default preset styles instance.
    """
    colors_map = {
        "red": default_colors.Red,
        "light_red": default_colors.LightRed,
        "green": default_colors.Green,
        "light_green": default_colors.LightGreen,
        "blue": default_colors.Blue,
        "light_blue": default_colors.LightBlue,
        "yellow": default_colors.Yellow,
        "purple": default_colors.Purple,
        "orange": default_colors.Orange,
        "navy": default_colors.Navy,
        "pink": default_colors.Pink,
        "charcoal": default_colors.Charcoal,
        "graphite": default_colors.Graphite,
        "gray": default_colors.Gray,
        "silver": default_colors.Silver,
        "snow": default_colors.Snow,
        "teal": default_colors.Teal,
        "olive": default_colors.Olive,
        "brown": default_colors.Brown,
        "black": default_colors.Black,
        "white": default_colors.White,
        "aqua": default_colors.Aqua,
        "green_yellow": default_colors.GreenYellow,
        "ivory": default_colors.Ivory,
        "steel": default_colors.Steel,
    }

    semantic_map = {
        "primary": default_colors.Primary,
        "secondary": default_colors.Secondary,
        "accent": default_colors.Accent,
        "muted": default_colors.Muted,
    }

    styles_dict: dict[str, Any] = {
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
    }

    for role_name, color in semantic_map.items():
        v = _make_variants(color)
        styles_dict[role_name] = v["normal"]
        styles_dict[f"{role_name}_bordered"] = v["bordered"]
        styles_dict[f"{role_name}_bold"] = v["bold"]
        styles_dict[f"{role_name}_light"] = v["light"]
        styles_dict[f"{role_name}_flat"] = v["flat"]
        styles_dict[f"{role_name}_outline"] = v["outline"]
        styles_dict[f"{role_name}_outline_bold"] = v["outline_bold"]
        styles_dict[f"{role_name}_outline_light"] = v["outline_light"]
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

    return StylesDefault(**styles_dict)


default_styles: StylesDefault = _create_default_styles()

__all__ = [
    "DefaultStyles",
    "StylesDefault",
    "default_styles",
]
