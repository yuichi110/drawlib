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

from drawlib._core.fonts import Font, FontSourceCode
from drawlib._core.types import Style
from drawlib._preset_colors import Colors, DefaultStyleColors
from drawlib._preset_styles._base import BasePresetStyles
from drawlib._preset_styles._utils import _create_style, _make_variants


class DefaultStyles(BasePresetStyles):
    """Default preset styles with complete typing for IDE autocompletion."""

    # Semantic roles
    primary: Style
    light: Style
    bold: Style
    flat: Style
    solid: Style
    dashed: Style

    # Blue
    blue: Style
    blue_flat: Style
    blue_solid: Style
    blue_bold: Style
    blue_light: Style
    blue_dashed: Style

    # Red
    red: Style
    red_flat: Style
    red_solid: Style
    red_bold: Style
    red_light: Style
    red_dashed: Style

    # Green
    green: Style
    green_flat: Style
    green_solid: Style
    green_bold: Style
    green_light: Style
    green_dashed: Style

    # Black
    black: Style
    black_flat: Style
    black_solid: Style
    black_bold: Style
    black_light: Style
    black_dashed: Style

    # White
    white: Style
    white_flat: Style
    white_solid: Style
    white_bold: Style
    white_light: Style
    white_dashed: Style


def _create_default_styles() -> DefaultStyles:
    """Generate default preset styles.

    Returns:
        DefaultStyles: Default preset styles.
    """
    blue = DefaultStyleColors.Blue
    black = DefaultStyleColors.Black
    red = DefaultStyleColors.Red
    green = DefaultStyleColors.Green
    white = DefaultStyleColors.White

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
        bold=_create_style(blue, black, text_color=black, line_width=2.25, font=Font.SANSSERIF_BOLD, icon_style="bold"),
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


default_styles: DefaultStyles = _create_default_styles()

__all__ = [
    "DefaultStyles",
    "default_styles",
]
