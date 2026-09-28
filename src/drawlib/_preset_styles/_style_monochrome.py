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

from typing import Any

from drawlib._core.fonts import FontSourceCode
from drawlib._core.types import Style
from drawlib._preset_colors import Colors, monochrome_colors
from drawlib._preset_styles._base import BaseStyles
from drawlib._preset_styles._utils import _make_variants


class StylesMonochrome(BaseStyles):
    """Monochrome preset styles with complete typing for IDE autocompletion."""

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

    def __getattribute__(self, name: str) -> Any:  # noqa: ANN401
        """Intercept attribute access to raise AttributeError for unsupported semantic roles.

        Args:
            name (str): Attribute name being accessed.

        Returns:
            Any: Attribute value if defined.

        Raises:
            AttributeError: If accessing an unsupported danger or success style.
        """
        val = super().__getattribute__(name)
        if (name.startswith("danger") or name.startswith("success")) and val is None:
            raise AttributeError(f"{self.__class__.__name__} has no {name} style.")
        return val


# Backwards compatibility alias
MonochromeStyles = StylesMonochrome


def _create_monochrome_styles() -> StylesMonochrome:
    """Generate monochrome preset styles.

    Returns:
        StylesMonochrome: Monochrome preset styles instance.
    """
    black = monochrome_colors.Black
    charcoal = monochrome_colors.Charcoal
    graphite = monochrome_colors.Graphite
    gray = monochrome_colors.Gray
    silver = monochrome_colors.Silver
    snow = monochrome_colors.Snow
    white = monochrome_colors.White

    p_v = _make_variants(
        white,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )
    p_v["flat"] = Style(
        supports={"shape"},
        shape_fill_color=black,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
    )

    s_v = _make_variants(
        gray,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )

    a_v = _make_variants(
        black,
        border_color=black,
        default_text_color=white,
        line_color=black,
    )

    m_v = _make_variants(
        snow,
        border_color=charcoal,
        default_text_color=charcoal,
        line_color=charcoal,
    )

    role_variants = {
        "primary": p_v,
        "secondary": s_v,
        "accent": a_v,
        "muted": m_v,
    }

    styles_dict: dict[str, Any] = {
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
    }

    for role_name, v in role_variants.items():
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

    color_variants = {
        "black": _make_variants(black),
        "charcoal": _make_variants(charcoal),
        "graphite": _make_variants(graphite),
        "gray": _make_variants(gray),
        "silver": _make_variants(silver),
        "snow": _make_variants(snow, border_color=charcoal, default_text_color=charcoal),
        "white": _make_variants(white, border_color=black, default_text_color=black),
    }

    for cname, v in color_variants.items():
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

    return StylesMonochrome(**styles_dict)


monochrome_styles: StylesMonochrome = _create_monochrome_styles()

__all__ = [
    "MonochromeStyles",
    "StylesMonochrome",
    "monochrome_styles",
]
