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

from drawlib._core.l2_types import IconStyle, LineStyle
from drawlib._core.l3_colors import Color, ColorType
from drawlib._core.l3_fonts import Font, FontBase, FontFile
from drawlib._core.l3_styles import (
    DEFAULT_FONT,
    DEFAULT_FONT_BOLD,
    DEFAULT_FONT_THIN,
    DEFAULT_TEXT_SIZE,
    Style,
)
from drawlib._preset_colors import DefaultColors as Colors

_DEFAULT_BORDER_COLOR: Color = Color(39, 39, 39)


def _resolve_target_font(
    field_name: str,
    regular: FontBase | FontFile | None,
    bold: FontBase | FontFile | None,
    thin: FontBase | FontFile | None,
) -> FontBase | FontFile | None:
    """Resolve target font for a specific style field based on naming convention.

    Args:
        field_name (str): Style attribute name.
        regular (FontBase | FontFile | None): Base font.
        bold (FontBase | FontFile | None): Bold font.
        thin (FontBase | FontFile | None): Thin font.

    Returns:
        FontBase | FontFile | None: Target font to apply.
    """
    if field_name == "Bold" or field_name.endswith("Bold"):
        return bold if bold is not None else regular
    if field_name.endswith("Thin"):
        return thin if thin is not None else regular
    return regular


def _create_style(
    fill_color: ColorType,
    line_color: ColorType,
    *,
    text_color: ColorType | None = None,
    icon_color: ColorType | None = None,
    line_width: float = 1.5,
    line_style: LineStyle = "solid",
    shape_line_width: float | None = None,
    shape_line_style: LineStyle | None = None,
    font: Font = DEFAULT_FONT,
    icon_style: IconStyle = "regular",
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
        text_size=DEFAULT_TEXT_SIZE,
        text_font=font,
        text_halign="center",
        text_valign="center",
        icon_color=i_color,
        icon_style=icon_style,
    )


def _make_variants(
    color: ColorType,
    *,
    border_color: ColorType | None = None,
    default_text_color: ColorType | None = None,
    line_color: ColorType | None = None,
) -> dict[str, Style]:
    """Generate 10 orthogonal variant styles for a specific color.

    Variants:
        normal (bordered regular), bold, light, flat,
        outline, outline_bold, outline_light,
        dashed, dashed_bold, dashed_light
        (plus 'bordered' and 'solid' aliases).

    Args:
        color: Base color to generate variants for.
        border_color: Optional border color override (defaults to Charcoal).
        default_text_color: Optional default text color override.
        line_color: Optional line color override.

    Returns:
        dict[str, Style]: Dictionary mapping variant names to Style instances.
    """
    line_col = border_color if border_color is not None else _DEFAULT_BORDER_COLOR
    txt_col = default_text_color if default_text_color is not None else color
    actual_line_col = line_color if line_color is not None else color

    bordered_regular = Style(
        supports={"shape", "line", "text", "icon"},
        shape_fill_color=color,
        shape_line_color=line_col,
        shape_line_width=1.5,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=1.5,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
        text_color=txt_col,
        text_size=DEFAULT_TEXT_SIZE,
        text_font=DEFAULT_FONT,
        text_halign="center",
        text_valign="center",
        icon_color=txt_col,
        icon_style="regular",
    )
    bordered_bold = Style(
        supports={"shape", "line", "text", "icon"},
        shape_fill_color=color,
        shape_line_color=line_col,
        shape_line_width=2.5,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=2.5,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
        text_color=txt_col,
        text_size=DEFAULT_TEXT_SIZE,
        text_font=DEFAULT_FONT_BOLD,
        text_halign="center",
        text_valign="center",
        icon_color=txt_col,
        icon_style="bold",
    )
    bordered_thin = Style(
        supports={"shape", "line", "text", "icon"},
        shape_fill_color=color,
        shape_line_color=line_col,
        shape_line_width=0.75,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=0.75,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
        text_color=txt_col,
        text_size=DEFAULT_TEXT_SIZE,
        text_font=DEFAULT_FONT_THIN,
        text_halign="center",
        text_valign="center",
        icon_color=txt_col,
        icon_style="thin",
    )
    flat = Style(
        supports={"shape", "icon"},
        shape_fill_color=color,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
        icon_color=color,
        icon_style="regular",
    )
    outline_regular = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=1.5,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=1.5,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    outline_bold = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=2.5,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=2.5,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    outline_thin = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=0.75,
        shape_line_style="solid",
        line_color=actual_line_col,
        line_width=0.75,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dashed_regular = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=1.5,
        shape_line_style="dashed",
        line_color=actual_line_col,
        line_width=1.5,
        line_style="dashed",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dashed_bold = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=2.5,
        shape_line_style="dashed",
        line_color=actual_line_col,
        line_width=2.5,
        line_style="dashed",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dashed_thin = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=0.75,
        shape_line_style="dashed",
        line_color=actual_line_col,
        line_width=0.75,
        line_style="dashed",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dotted_regular = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=1.5,
        shape_line_style="dotted",
        line_color=actual_line_col,
        line_width=1.5,
        line_style="dotted",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dotted_bold = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=2.5,
        shape_line_style="dotted",
        line_color=actual_line_col,
        line_width=2.5,
        line_style="dotted",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )
    dotted_thin = Style(
        supports={"shape", "line"},
        shape_fill_color=Colors.Transparent,
        shape_line_color=actual_line_col,
        shape_line_width=0.75,
        shape_line_style="dotted",
        line_color=actual_line_col,
        line_width=0.75,
        line_style="dotted",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
    )

    return {
        "normal": bordered_regular,
        "bordered": bordered_regular,
        "bold": bordered_bold,
        "thin": bordered_thin,
        "flat": flat,
        "outline": outline_regular,
        "solid": outline_regular,
        "outline_bold": outline_bold,
        "solid_bold": outline_bold,
        "outline_thin": outline_thin,
        "solid_thin": outline_thin,
        "dashed": dashed_regular,
        "dashed_bold": dashed_bold,
        "dashed_thin": dashed_thin,
        "dotted": dotted_regular,
        "dotted_bold": dotted_bold,
        "dotted_thin": dotted_thin,
    }


def _make_neutral_card(
    fill_color: ColorType,
    *,
    border_color: ColorType | None = None,
    text_color: ColorType | None = None,
) -> tuple[Style, Style]:
    """Generate (bordered, flat) neutral card styles for tinted container cards.

    Args:
        fill_color: Fill color (typically tone 1 or tone 2).
        border_color: Border line color (typically tone 3 or tone 4).
        text_color: High contrast text and icon color (typically tone 6 or tone 7).

    Returns:
        tuple[Style, Style]: (neutral_bordered, neutral_flat) Style instances.
    """
    b_col = border_color if border_color is not None else _DEFAULT_BORDER_COLOR
    t_col = text_color if text_color is not None else b_col

    bordered = Style(
        supports={"shape", "line", "text", "icon"},
        shape_fill_color=fill_color,
        shape_line_color=b_col,
        shape_line_width=1.5,
        shape_line_style="solid",
        line_color=b_col,
        line_width=1.5,
        line_style="solid",
        line_arrow_head_scale=20.0,
        line_arrow_head_fill=False,
        text_color=t_col,
        text_size=DEFAULT_TEXT_SIZE,
        text_font=DEFAULT_FONT,
        text_halign="center",
        text_valign="center",
        icon_color=t_col,
        icon_style="regular",
    )
    flat = Style(
        supports={"shape", "text", "icon"},
        shape_fill_color=fill_color,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
        shape_line_style="solid",
        text_color=t_col,
        text_size=DEFAULT_TEXT_SIZE,
        text_font=DEFAULT_FONT,
        text_halign="center",
        text_valign="center",
        icon_color=t_col,
        icon_style="regular",
    )
    return bordered, flat


__all__ = [
    "_create_style",
    "_make_neutral_card",
    "_make_variants",
    "_resolve_target_font",
]
