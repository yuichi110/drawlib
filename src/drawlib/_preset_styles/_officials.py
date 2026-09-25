# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Module for generating official preset styles."""

from __future__ import annotations

from typing import Literal, overload

from drawlib._core.l2_types import TypeColor, TypeIconStyle, TypeLineStyle
from drawlib._core.l3_fonts import Font, FontSourceCode
from drawlib._core.l3_styles import (
    Colors,
    ColorsDefault,
    ColorsEssentials,
    ColorsMonochrome,
    Style,
)
from drawlib._preset_styles._models import (
    BasePresetStyles,
    DefaultStyles,
    EssentialsStyles,
    MonochromeStyles,
)


def _create_style(
    fill_color: TypeColor,
    line_color: TypeColor,
    *,
    text_color: TypeColor | None = None,
    icon_color: TypeColor | None = None,
    line_width: float = 1.5,
    line_style: TypeLineStyle = "solid",
    shape_line_width: float | None = None,
    shape_line_style: TypeLineStyle | None = None,
    font: Font = Font.SANSSERIF_REGULAR,
    icon_style: TypeIconStyle = "regular",
) -> Style:
    t_color = text_color if text_color is not None else line_color
    i_color = icon_color if icon_color is not None else t_color
    s_line_w = shape_line_width if shape_line_width is not None else line_width
    s_line_s = shape_line_style if shape_line_style is not None else line_style

    return Style(
        shape_fill_color=fill_color,
        shape_line_color=line_color,
        shape_line_width=s_line_w,
        shape_line_style=s_line_s,
        line_color=line_color,
        line_width=line_width,
        line_style=line_style,
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
        text_color=t_color,
        text_size=16,
        text_font=font,
        text_halign="center",
        text_valign="center",
        icon_color=i_color,
        icon_style=icon_style,
    )


def _make_variants(
    color: TypeColor,
    *,
    border_color: TypeColor | None = None,
    default_text_color: TypeColor | None = None,
) -> dict[str, Style]:
    line_col = border_color if border_color is not None else color
    txt_col = default_text_color if default_text_color is not None else line_col

    return {
        "normal": _create_style(color, line_col, text_color=txt_col, line_width=1.5, font=Font.SANSSERIF_REGULAR),
        "flat": _create_style(
            color, color, text_color=txt_col, line_width=1.5, shape_line_width=0.0, icon_style="fill"
        ),
        "solid": _create_style(Colors.Transparent, color, text_color=color, line_width=1.5),
        "bold": _create_style(
            color, line_col, text_color=txt_col, line_width=2.25, font=Font.SANSSERIF_BOLD, icon_style="bold"
        ),
        "light": _create_style(
            color, line_col, text_color=txt_col, line_width=0.75, font=Font.SANSSERIF_LIGHT, icon_style="thin"
        ),
        "dashed": _create_style(
            Colors.Transparent,
            color,
            text_color=color,
            line_width=1.5,
            line_style="dashed",
            shape_line_style="dashed",
        ),
    }


def get_default_styles() -> DefaultStyles:
    """Generate default preset styles.

    Returns:
        DefaultStyles: Default preset styles.
    """
    blue = ColorsDefault.Blue
    black = ColorsDefault.Black
    red = ColorsDefault.Red
    green = ColorsDefault.Green
    white = ColorsDefault.White

    # Color variants
    b_v = _make_variants(blue)
    r_v = _make_variants(red)
    g_v = _make_variants(green)
    k_v = _make_variants(black)
    w_v = _make_variants(white, border_color=black, default_text_color=black)

    return DefaultStyles(
        # Semantic roles
        primary=_create_style(blue, black, text_color=black, line_width=1.5, font=Font.SANSSERIF_REGULAR),
        light=_create_style(
            blue, black, text_color=black, line_width=0.75, font=Font.SANSSERIF_LIGHT, icon_style="thin"
        ),
        bold=_create_style(
            blue, black, text_color=black, line_width=2.25, font=Font.SANSSERIF_BOLD, icon_style="bold"
        ),
        flat=_create_style(blue, blue, text_color=black, line_width=1.5, shape_line_width=0.0, icon_style="fill"),
        solid=_create_style(Colors.Transparent, blue, text_color=blue, line_width=1.5),
        dashed=_create_style(
            Colors.Transparent,
            blue,
            text_color=blue,
            line_width=1.5,
            line_style="dashed",
            shape_line_style="dashed",
        ),
        # Blue
        blue=b_v["normal"],
        blue_flat=b_v["flat"],
        blue_solid=b_v["solid"],
        blue_bold=b_v["bold"],
        blue_light=b_v["light"],
        blue_dashed=b_v["dashed"],
        # Red
        red=r_v["normal"],
        red_flat=r_v["flat"],
        red_solid=r_v["solid"],
        red_bold=r_v["bold"],
        red_light=r_v["light"],
        red_dashed=r_v["dashed"],
        # Green
        green=g_v["normal"],
        green_flat=g_v["flat"],
        green_solid=g_v["solid"],
        green_bold=g_v["bold"],
        green_light=g_v["light"],
        green_dashed=g_v["dashed"],
        # Black
        black=k_v["normal"],
        black_flat=k_v["flat"],
        black_solid=k_v["solid"],
        black_bold=k_v["bold"],
        black_light=k_v["light"],
        black_dashed=k_v["dashed"],
        # White
        white=w_v["normal"],
        white_flat=w_v["flat"],
        white_solid=w_v["solid"],
        white_bold=w_v["bold"],
        white_light=w_v["light"],
        white_dashed=w_v["dashed"],
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


def get_monochrome_styles() -> MonochromeStyles:
    """Generate monochrome preset styles.

    Returns:
        MonochromeStyles: Monochrome preset styles.
    """
    black = ColorsMonochrome.Black
    charcoal = ColorsMonochrome.Charcoal
    graphite = ColorsMonochrome.Graphite
    gray = ColorsMonochrome.Gray
    silver = ColorsMonochrome.Silver
    snow = ColorsMonochrome.Snow
    white = ColorsMonochrome.White

    k_v = _make_variants(black)
    c_v = _make_variants(charcoal)
    g_v = _make_variants(graphite)
    y_v = _make_variants(gray)
    s_v = _make_variants(silver)
    n_v = _make_variants(snow, border_color=charcoal, default_text_color=charcoal)
    w_v = _make_variants(white, border_color=black, default_text_color=black)

    return MonochromeStyles(
        primary=_create_style(white, black, text_color=black, line_width=1.5, font=Font.SANSSERIF_REGULAR),
        light=_create_style(
            white, black, text_color=black, line_width=0.75, font=Font.SANSSERIF_LIGHT, icon_style="thin"
        ),
        bold=_create_style(
            white, black, text_color=black, line_width=2.25, font=Font.SANSSERIF_BOLD, icon_style="bold"
        ),
        flat=_create_style(black, black, text_color=white, line_width=1.5, shape_line_width=0.0, icon_style="fill"),
        solid=_create_style(Colors.Transparent, black, text_color=black, line_width=1.5),
        dashed=_create_style(
            Colors.Transparent,
            black,
            text_color=black,
            line_width=1.5,
            line_style="dashed",
            shape_line_style="dashed",
        ),
        black=k_v["normal"],
        black_flat=k_v["flat"],
        black_solid=k_v["solid"],
        black_bold=k_v["bold"],
        black_light=k_v["light"],
        black_dashed=k_v["dashed"],
        charcoal=c_v["normal"],
        charcoal_flat=c_v["flat"],
        charcoal_solid=c_v["solid"],
        charcoal_bold=c_v["bold"],
        charcoal_light=c_v["light"],
        charcoal_dashed=c_v["dashed"],
        graphite=g_v["normal"],
        graphite_flat=g_v["flat"],
        graphite_solid=g_v["solid"],
        graphite_bold=g_v["bold"],
        graphite_light=g_v["light"],
        graphite_dashed=g_v["dashed"],
        gray=y_v["normal"],
        gray_flat=y_v["flat"],
        gray_solid=y_v["solid"],
        gray_bold=y_v["bold"],
        gray_light=y_v["light"],
        gray_dashed=y_v["dashed"],
        silver=s_v["normal"],
        silver_flat=s_v["flat"],
        silver_solid=s_v["solid"],
        silver_bold=s_v["bold"],
        silver_light=s_v["light"],
        silver_dashed=s_v["dashed"],
        snow=n_v["normal"],
        snow_flat=n_v["flat"],
        snow_solid=n_v["solid"],
        snow_bold=n_v["bold"],
        snow_light=n_v["light"],
        snow_dashed=n_v["dashed"],
        white=w_v["normal"],
        white_flat=w_v["flat"],
        white_solid=w_v["solid"],
        white_bold=w_v["bold"],
        white_light=w_v["light"],
        white_dashed=w_v["dashed"],
        background_color=(255, 255, 255, 1.0),
        sourcecode_font=FontSourceCode.SOURCECODEPRO,
    )


def get_essentials_styles() -> EssentialsStyles:
    """Generate essentials preset styles.

    Returns:
        EssentialsStyles: Essentials preset styles.
    """
    charcoal = ColorsEssentials.Charcoal
    lightblue = ColorsEssentials.LightBlue

    def v(col: TypeColor) -> dict[str, Style]:
        return _make_variants(col)

    r_v = v(ColorsEssentials.Red)
    lr_v = v(ColorsEssentials.LightRed)
    g_v = v(ColorsEssentials.Green)
    lg_v = v(ColorsEssentials.LightGreen)
    b_v = v(ColorsEssentials.Blue)
    lb_v = v(ColorsEssentials.LightBlue)
    y_v = v(ColorsEssentials.Yellow)
    p_v = v(ColorsEssentials.Purple)
    o_v = v(ColorsEssentials.Orange)
    n_v = v(ColorsEssentials.Navy)
    pi_v = v(ColorsEssentials.Pink)
    c_v = v(ColorsEssentials.Charcoal)
    gr_v = v(ColorsEssentials.Graphite)
    gy_v = v(ColorsEssentials.Gray)
    si_v = v(ColorsEssentials.Silver)
    sn_v = v(ColorsEssentials.Snow)
    te_v = v(ColorsEssentials.Teal)
    ol_v = v(ColorsEssentials.Olive)
    br_v = v(ColorsEssentials.Brown)
    k_v = v(ColorsEssentials.Black)
    w_v = _make_variants(ColorsEssentials.White, border_color=charcoal, default_text_color=charcoal)
    aq_v = v(ColorsEssentials.Aqua)
    gy_yel_v = v(ColorsEssentials.GreenYellow)
    iv_v = v(ColorsEssentials.Ivory)
    st_v = v(ColorsEssentials.Steel)

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


@overload
def get_styles(name: Literal["default"] = "default") -> DefaultStyles: ...


@overload
def get_styles(name: Literal["essentials"]) -> EssentialsStyles: ...


@overload
def get_styles(name: Literal["monochrome"]) -> MonochromeStyles: ...


@overload
def get_styles(name: str) -> BasePresetStyles: ...


def get_styles(
    name: Literal["default", "essentials", "monochrome"] | str = "default",
) -> BasePresetStyles:
    """Get preset styles by name.

    Args:
        name: Preset styles name ("default", "essentials", "monochrome").

    Returns:
        BasePresetStyles: Preset styles object.
    """
    if name == "default":
        return get_default_styles()
    if name == "essentials":
        return get_essentials_styles()
    if name == "monochrome":
        return get_monochrome_styles()
    raise ValueError(f'Preset style "{name}" is not supported.')
