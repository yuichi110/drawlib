# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Essentials preset styles module."""

from __future__ import annotations

from drawlib._core.fonts import Font, FontSourceCode
from drawlib._core.types import Style, TypeColor
from drawlib._preset_colors import Colors, EssentialsStyleColors
from drawlib._preset_styles._base import BasePresetStyles
from drawlib._preset_styles._utils import _create_style, _make_variants


class EssentialsStyles(BasePresetStyles):
    """Essentials preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Popular essentials colors
    red: Style
    red_flat: Style
    red_solid: Style
    red_bold: Style
    red_dashed: Style

    light_red: Style
    light_red_flat: Style
    light_red_solid: Style
    light_red_bold: Style

    green: Style
    green_flat: Style
    green_solid: Style
    green_bold: Style
    green_dashed: Style

    light_green: Style
    light_green_flat: Style
    light_green_solid: Style
    light_green_bold: Style

    blue: Style
    blue_flat: Style
    blue_solid: Style
    blue_bold: Style
    blue_dashed: Style

    light_blue: Style
    light_blue_flat: Style
    light_blue_solid: Style
    light_blue_bold: Style

    yellow: Style
    yellow_flat: Style
    yellow_solid: Style
    yellow_bold: Style

    purple: Style
    purple_flat: Style
    purple_solid: Style
    purple_bold: Style
    purple_dashed: Style

    orange: Style
    orange_flat: Style
    orange_solid: Style
    orange_bold: Style
    orange_dashed: Style

    navy: Style
    navy_flat: Style
    navy_solid: Style
    navy_bold: Style
    navy_dashed: Style

    pink: Style
    pink_flat: Style
    pink_solid: Style
    pink_bold: Style

    charcoal: Style
    charcoal_flat: Style
    charcoal_solid: Style
    charcoal_bold: Style
    charcoal_dashed: Style

    graphite: Style
    graphite_flat: Style
    graphite_solid: Style
    graphite_bold: Style

    gray: Style
    gray_flat: Style
    gray_solid: Style
    gray_bold: Style
    gray_dashed: Style

    silver: Style
    silver_flat: Style
    silver_solid: Style
    silver_bold: Style
    silver_dashed: Style

    snow: Style
    snow_flat: Style
    snow_solid: Style
    snow_bold: Style

    teal: Style
    teal_flat: Style
    teal_solid: Style
    teal_bold: Style
    teal_dashed: Style

    olive: Style
    olive_flat: Style
    olive_solid: Style
    olive_bold: Style

    brown: Style
    brown_flat: Style
    brown_solid: Style
    brown_bold: Style

    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style

    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style

    aqua: Style
    aqua_flat: Style
    aqua_solid: Style
    aqua_bold: Style

    green_yellow: Style
    green_yellow_flat: Style
    green_yellow_solid: Style
    green_yellow_bold: Style

    ivory: Style
    ivory_flat: Style
    ivory_solid: Style
    ivory_bold: Style

    steel: Style
    steel_flat: Style
    steel_solid: Style
    steel_bold: Style


def _create_essentials_styles() -> EssentialsStyles:
    """Generate essentials preset styles.

    Returns:
        EssentialsStyles: Essentials preset styles.
    """
    charcoal = EssentialsStyleColors.Charcoal
    lightblue = EssentialsStyleColors.LightBlue

    def v(col: TypeColor) -> dict[str, Style]:
        return _make_variants(col)

    r_v = v(EssentialsStyleColors.Red)
    lr_v = v(EssentialsStyleColors.LightRed)
    g_v = v(EssentialsStyleColors.Green)
    lg_v = v(EssentialsStyleColors.LightGreen)
    b_v = v(EssentialsStyleColors.Blue)
    lb_v = v(EssentialsStyleColors.LightBlue)
    y_v = v(EssentialsStyleColors.Yellow)
    p_v = v(EssentialsStyleColors.Purple)
    o_v = v(EssentialsStyleColors.Orange)
    n_v = v(EssentialsStyleColors.Navy)
    pi_v = v(EssentialsStyleColors.Pink)
    c_v = v(EssentialsStyleColors.Charcoal)
    gr_v = v(EssentialsStyleColors.Graphite)
    gy_v = v(EssentialsStyleColors.Gray)
    si_v = v(EssentialsStyleColors.Silver)
    sn_v = v(EssentialsStyleColors.Snow)
    te_v = v(EssentialsStyleColors.Teal)
    ol_v = v(EssentialsStyleColors.Olive)
    br_v = v(EssentialsStyleColors.Brown)
    k_v = v(EssentialsStyleColors.Black)
    w_v = _make_variants(EssentialsStyleColors.White, border_color=charcoal, default_text_color=charcoal)
    aq_v = v(EssentialsStyleColors.Aqua)
    gy_yel_v = v(EssentialsStyleColors.GreenYellow)
    iv_v = v(EssentialsStyleColors.Ivory)
    st_v = v(EssentialsStyleColors.Steel)

    return EssentialsStyles(
        primary=_create_style(lightblue, charcoal, text_color=charcoal, line_width=1.5, font=Font.SANSSERIF_REGULAR),
        light=_create_style(
            lightblue, charcoal, text_color=charcoal, line_width=0.75, font=Font.SANSSERIF_LIGHT, icon_style="thin"
        ),
        bold=_create_style(
            lightblue, charcoal, text_color=charcoal, line_width=2.25, font=Font.SANSSERIF_BOLD, icon_style="bold"
        ),
        flat=_create_style(
            lightblue, lightblue, text_color=charcoal, line_width=1.5, shape_line_width=0.0, icon_style="fill"
        ),
        solid=_create_style(Colors.Transparent, lightblue, text_color=lightblue, line_width=1.5),
        dashed=_create_style(
            Colors.Transparent,
            lightblue,
            text_color=lightblue,
            line_width=1.5,
            line_style="dashed",
            shape_line_style="dashed",
        ),
        red=r_v["normal"],
        red_flat=r_v["flat"],
        red_solid=r_v["solid"],
        red_bold=r_v["bold"],
        red_dashed=r_v["dashed"],
        light_red=lr_v["normal"],
        light_red_flat=lr_v["flat"],
        light_red_solid=lr_v["solid"],
        light_red_bold=lr_v["bold"],
        green=g_v["normal"],
        green_flat=g_v["flat"],
        green_solid=g_v["solid"],
        green_bold=g_v["bold"],
        green_dashed=g_v["dashed"],
        light_green=lg_v["normal"],
        light_green_flat=lg_v["flat"],
        light_green_solid=lg_v["solid"],
        light_green_bold=lg_v["bold"],
        blue=b_v["normal"],
        blue_flat=b_v["flat"],
        blue_solid=b_v["solid"],
        blue_bold=b_v["bold"],
        blue_dashed=b_v["dashed"],
        light_blue=lb_v["normal"],
        light_blue_flat=lb_v["flat"],
        light_blue_solid=lb_v["solid"],
        light_blue_bold=lb_v["bold"],
        yellow=y_v["normal"],
        yellow_flat=y_v["flat"],
        yellow_solid=y_v["solid"],
        yellow_bold=y_v["bold"],
        purple=p_v["normal"],
        purple_flat=p_v["flat"],
        purple_solid=p_v["solid"],
        purple_bold=p_v["bold"],
        purple_dashed=p_v["dashed"],
        orange=o_v["normal"],
        orange_flat=o_v["flat"],
        orange_solid=o_v["solid"],
        orange_bold=o_v["bold"],
        orange_dashed=o_v["dashed"],
        navy=n_v["normal"],
        navy_flat=n_v["flat"],
        navy_solid=n_v["solid"],
        navy_bold=n_v["bold"],
        navy_dashed=n_v["dashed"],
        pink=pi_v["normal"],
        pink_flat=pi_v["flat"],
        pink_solid=pi_v["solid"],
        pink_bold=pi_v["bold"],
        charcoal=c_v["normal"],
        charcoal_flat=c_v["flat"],
        charcoal_solid=c_v["solid"],
        charcoal_bold=c_v["bold"],
        charcoal_dashed=c_v["dashed"],
        graphite=gr_v["normal"],
        graphite_flat=gr_v["flat"],
        graphite_solid=gr_v["solid"],
        graphite_bold=gr_v["bold"],
        gray=gy_v["normal"],
        gray_flat=gy_v["flat"],
        gray_solid=gy_v["solid"],
        gray_bold=gy_v["bold"],
        gray_dashed=gy_v["dashed"],
        silver=si_v["normal"],
        silver_flat=si_v["flat"],
        silver_solid=si_v["solid"],
        silver_bold=si_v["bold"],
        silver_dashed=si_v["dashed"],
        snow=sn_v["normal"],
        snow_flat=sn_v["flat"],
        snow_solid=sn_v["solid"],
        snow_bold=sn_v["bold"],
        teal=te_v["normal"],
        teal_flat=te_v["flat"],
        teal_solid=te_v["solid"],
        teal_bold=te_v["bold"],
        teal_dashed=te_v["dashed"],
        olive=ol_v["normal"],
        olive_flat=ol_v["flat"],
        olive_solid=ol_v["solid"],
        olive_bold=ol_v["bold"],
        brown=br_v["normal"],
        brown_flat=br_v["flat"],
        brown_solid=br_v["solid"],
        brown_bold=br_v["bold"],
        black=k_v["normal"],
        black_flat=k_v["flat"],
        black_solid=k_v["solid"],
        black_bold=k_v["bold"],
        white=w_v["normal"],
        white_flat=w_v["flat"],
        white_solid=w_v["solid"],
        white_bold=w_v["bold"],
        aqua=aq_v["normal"],
        aqua_flat=aq_v["flat"],
        aqua_solid=aq_v["solid"],
        aqua_bold=aq_v["bold"],
        green_yellow=gy_yel_v["normal"],
        green_yellow_flat=gy_yel_v["flat"],
        green_yellow_solid=gy_yel_v["solid"],
        green_yellow_bold=gy_yel_v["bold"],
        ivory=iv_v["normal"],
        ivory_flat=iv_v["flat"],
        ivory_solid=iv_v["solid"],
        ivory_bold=iv_v["bold"],
        steel=st_v["normal"],
        steel_flat=st_v["flat"],
        steel_solid=st_v["solid"],
        steel_bold=st_v["bold"],
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


essentials_styles: EssentialsStyles = _create_essentials_styles()

__all__ = [
    "EssentialsStyles",
    "essentials_styles",
]
