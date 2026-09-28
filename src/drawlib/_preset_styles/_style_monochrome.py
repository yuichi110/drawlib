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

    # Semantic Roles
    primary: Style
    secondary: Style
    accent: Style
    muted: Style
    light: Style
    dark: Style
    canvas: Style
    canvas_flat: Style

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
    gray1 = monochrome_colors.Gray1
    gray2 = monochrome_colors.Gray2
    gray3 = monochrome_colors.Gray3
    gray4 = monochrome_colors.Gray4
    gray5 = monochrome_colors.Gray5
    gray6 = monochrome_colors.Gray6
    white = monochrome_colors.White

    p_v = _make_variants(
        white,
        border_color=black,
        default_text_color=black,
        line_color=black,
    )
    p_v["flat"] = Style(
        supports={"shape", "icon"},
        shape_fill_color=black,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
        icon_color=black,
        icon_style="regular",
    )

    s_v = _make_variants(
        gray2,
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
        gray1,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )

    l_v = _make_variants(
        white,
        border_color=gray5,
        default_text_color=gray5,
        line_color=gray5,
    )
    d_v = _make_variants(
        gray6,
        border_color=black,
        default_text_color=white,
        line_color=black,
    )

    role_variants = {
        "primary": p_v,
        "secondary": s_v,
        "accent": a_v,
        "muted": m_v,
        "light": l_v,
        "dark": d_v,
    }

    styles_dict: dict[str, Any] = {
        "width": 140,
        "height": 70,
        "dpi": 100,
        "colors": monochrome_colors,
        "background_color": (255, 255, 255, 1.0),
        "sourcecode_font": FontSourceCode.SOURCECODEPRO,
        "canvas": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
        "canvas_flat": Style(supports={"shape"}, shape_fill_color=white, shape_line_color=white, shape_line_width=0.0),
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
        "white": _make_variants(white, border_color=black, default_text_color=black),
        "gray1": _make_variants(gray1, border_color=gray5, default_text_color=gray5),
        "gray2": _make_variants(gray2, border_color=gray5, default_text_color=gray5),
        "gray3": _make_variants(gray3, border_color=gray6, default_text_color=black),
        "gray4": _make_variants(gray4, border_color=black, default_text_color=white),
        "gray5": _make_variants(gray5, border_color=black, default_text_color=white),
        "gray6": _make_variants(gray6, border_color=black, default_text_color=white),
        "black": _make_variants(black, border_color=black, default_text_color=white),
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
