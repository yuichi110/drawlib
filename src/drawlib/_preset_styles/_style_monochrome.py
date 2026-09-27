# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Monochrome preset styles module."""

from __future__ import annotations

from drawlib._core.fonts import Font, FontSourceCode
from drawlib._core.types import Style
from drawlib._preset_colors import Colors, monochrome_colors
from drawlib._preset_styles._base import BaseStyles
from drawlib._preset_styles._utils import _create_style, _make_variants


class MonochromeStyles(BaseStyles):
    """Monochrome preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Colors: black, charcoal, graphite, gray, silver, snow, white
    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style
    black_light: Style
    black_dashed: Style

    charcoal: Style
    charcoal_flat: Style
    charcoal_solid: Style
    charcoal_bold: Style
    charcoal_light: Style
    charcoal_dashed: Style

    graphite: Style
    graphite_flat: Style
    graphite_solid: Style
    graphite_bold: Style
    graphite_light: Style
    graphite_dashed: Style

    gray: Style
    gray_flat: Style
    gray_solid: Style
    gray_bold: Style
    gray_light: Style
    gray_dashed: Style

    silver: Style
    silver_flat: Style
    silver_solid: Style
    silver_bold: Style
    silver_light: Style
    silver_dashed: Style

    snow: Style
    snow_flat: Style
    snow_solid: Style
    snow_bold: Style
    snow_light: Style
    snow_dashed: Style

    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style
    white_light: Style
    white_dashed: Style


def _create_monochrome_styles() -> MonochromeStyles:
    """Generate monochrome preset styles.

    Returns:
        MonochromeStyles: Monochrome preset styles.
    """
    black = monochrome_colors.Black
    charcoal = monochrome_colors.Charcoal
    graphite = monochrome_colors.Graphite
    gray = monochrome_colors.Gray
    silver = monochrome_colors.Silver
    snow = monochrome_colors.Snow
    white = monochrome_colors.White

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


monochrome_styles: MonochromeStyles = _create_monochrome_styles()

__all__ = [
    "MonochromeStyles",
    "monochrome_styles",
]
