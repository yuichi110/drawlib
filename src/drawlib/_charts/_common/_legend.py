# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Automatic legend layout and renderer for charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._charts._common._types import ColorType, LegendPosition
from drawlib._core.colors import Colors
from drawlib._core.fonts import Font
from drawlib._core.shapes import rectangle as canvas_rectangle
from drawlib._core.text import text as canvas_text
from drawlib._core.types import Style

if TYPE_CHECKING:
    pass

_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)


def resolve_legend_position(position: LegendPosition, series_count: int) -> LegendPosition:
    """Determine whether and where the legend should be rendered.

    Args:
        position: Configured LegendPosition preference.
        series_count: Number of series in chart.

    Returns:
        Resolved LegendPosition ("top", "bottom", "right", or "none").
    """
    if position == "none":
        return "none"
    if position == "auto":
        return "top" if series_count >= 2 else "none"
    return position


def get_legend_size(
    position: LegendPosition,
    series_names: list[str],  # noqa: ARG001
    series_count: int,
) -> tuple[float, float]:
    """Calculate the margin dimensions (width, height) reserved for the legend.

    Args:
        position: LegendPosition preference.
        series_names: List of series names.
        series_count: Number of series.

    Returns:
        Tuple of (width_margin, height_margin) to subtract from plot area.
    """
    resolved = resolve_legend_position(position, series_count)
    if resolved == "none":
        return (0.0, 0.0)
    if resolved in {"top", "bottom"}:
        # Reserve height at top or bottom for horizontal legend
        return (0.0, 4.0)
    if resolved == "right":
        # Reserve width on the right
        return (14.0, 0.0)
    return (0.0, 0.0)


def render_legend(
    names: list[str],
    colors: list[ColorType],
    position: LegendPosition,
    plot_bounds: tuple[float, float, float, float],
    chart_bounds: tuple[float, float, float, float],
    textstyle: Style | None = None,
) -> None:
    """Render the legend items onto the canvas.

    Args:
        names: List of series names.
        colors: List of series colors.
        position: Legend position.
        plot_bounds: (plot_min_x, plot_min_y, plot_max_x, plot_max_y).
        chart_bounds: (chart_min_x, chart_min_y, chart_max_x, chart_max_y).
        textstyle: Optional custom text style for labels.
    """
    resolved = resolve_legend_position(position, len(names))
    if resolved == "none" or not names:
        return

    p_min_x, p_min_y, p_max_x, p_max_y = plot_bounds
    _, _, c_max_x, _ = chart_bounds

    swatch_w = 2.4
    swatch_h = 1.2
    swatch_r = 0.3
    item_gap = 4.0
    text_offset = 1.8

    label_style = Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="left",
        text_valign="center",
    )
    if textstyle is not None:
        label_style = label_style.patch(textstyle)

    if resolved == "top":
        legend_y = p_max_y + 2.0
        # Estimate total width to center the legend items
        # Roughly 1.5 units per character + swatch
        item_widths = [swatch_w + text_offset + (len(name) * 1.5) for name in names]
        total_w = sum(item_widths) + item_gap * (len(names) - 1)
        plot_center_x = (p_min_x + p_max_x) / 2.0
        cur_x = plot_center_x - total_w / 2.0

        for name, color, item_w in zip(names, colors, item_widths, strict=False):
            # Swatch
            swatch_cx = cur_x + swatch_w / 2.0
            canvas_rectangle(
                xy=(swatch_cx, legend_y),
                width=swatch_w,
                height=swatch_h,
                r=swatch_r,
                style=Style(
                    shape_fill_color=color,
                    shape_line_color=Colors.Transparent,
                    shape_line_width=0,
                ),
            )
            # Label
            text_x = cur_x + swatch_w + 0.8
            canvas_text(xy=(text_x, legend_y), text=name, style=label_style)
            cur_x += item_w + item_gap

    elif resolved == "bottom":
        legend_y = p_min_y - 4.5
        item_widths = [swatch_w + text_offset + (len(name) * 1.5) for name in names]
        total_w = sum(item_widths) + item_gap * (len(names) - 1)
        plot_center_x = (p_min_x + p_max_x) / 2.0
        cur_x = plot_center_x - total_w / 2.0

        for name, color, item_w in zip(names, colors, item_widths, strict=False):
            swatch_cx = cur_x + swatch_w / 2.0
            canvas_rectangle(
                xy=(swatch_cx, legend_y),
                width=swatch_w,
                height=swatch_h,
                r=swatch_r,
                style=Style(
                    shape_fill_color=color,
                    shape_line_color=Colors.Transparent,
                    shape_line_width=0,
                ),
            )
            text_x = cur_x + swatch_w + 0.8
            canvas_text(xy=(text_x, legend_y), text=name, style=label_style)
            cur_x += item_w + item_gap

    elif resolved == "right":
        cur_x = p_max_x + 3.0
        # Stack vertically from top
        start_y = p_max_y - 2.0
        step_y = 3.5

        for i, (name, color) in enumerate(zip(names, colors, strict=False)):
            item_y = start_y - (i * step_y)
            swatch_cx = cur_x + swatch_w / 2.0
            canvas_rectangle(
                xy=(swatch_cx, item_y),
                width=swatch_w,
                height=swatch_h,
                r=swatch_r,
                style=Style(
                    shape_fill_color=color,
                    shape_line_color=Colors.Transparent,
                    shape_line_width=0,
                ),
            )
            text_x = cur_x + swatch_w + 0.8
            canvas_text(xy=(text_x, item_y), text=name, style=label_style)
