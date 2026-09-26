# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper utilities for preset styles."""

from __future__ import annotations

from drawlib._core.fonts import Font, FontBase, FontFile
from drawlib._core.types import Style, TypeColor, TypeIconStyle, TypeLineStyle
from drawlib._preset_colors import Colors


def _resolve_target_font(
    field_name: str,
    regular: FontBase | FontFile | None,
    bold: FontBase | FontFile | None,
    light: FontBase | FontFile | None,
) -> FontBase | FontFile | None:
    """Resolve target font for a specific style field based on naming convention.

    Args:
        field_name (str): Style attribute name.
        regular (FontBase | FontFile | None): Base font.
        bold (FontBase | FontFile | None): Bold font.
        light (FontBase | FontFile | None): Light font.

    Returns:
        FontBase | FontFile | None: Target font to apply.
    """
    if field_name == "bold" or field_name.endswith("_bold"):
        return bold if bold is not None else regular
    if field_name == "light" or field_name.endswith("_light"):
        return light if light is not None else regular
    return regular


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
    """Helper function to create a Style instance with preset defaults.

    Args:
        fill_color: Shape fill color.
        line_color: Main line and outline color.
        text_color: Text color (defaults to line_color).
        icon_color: Icon color (defaults to text_color).
        line_width: Main line width.
        line_style: Main line style pattern.
        shape_line_width: Shape border width (defaults to line_width).
        shape_line_style: Shape border style pattern (defaults to line_style).
        font: Font family and weight.
        icon_style: Icon weight/fill style variant.

    Returns:
        Style: Constructed Style instance.
    """
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
    """Generate variant styles (normal, flat, solid, bold, light, dashed) for a specific color.

    Args:
        color: Base color to generate variants for.
        border_color: Optional border color override.
        default_text_color: Optional default text color override.

    Returns:
        dict[str, Style]: Dictionary mapping variant names to Style instances.
    """
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


__all__ = [
    "_create_style",
    "_make_variants",
    "_resolve_target_font",
]
