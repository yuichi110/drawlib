# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data models and color-stop interpolation utilities for heatmap charts."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import drawlib._charts._common._legend as _legend_module
from drawlib._charts._common._style_utils import (
    clamp_ratio,
    ensure_line_style,
    ensure_shape_style,
    ensure_text_style,
)
from drawlib._charts._common._types import DrawDirection, FormatterType, Orientation
from drawlib._core import l4_canvas as canvas
from drawlib._core.l3_colors import Color, ColorType
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from collections.abc import Sequence


class Row:
    """Represents a horizontal row of matrix values in a HeatmapChart.

    Attributes:
        name: Row category label displayed along the Y-axis.
        values: List of numerical values (or None for empty cells) across columns.
        show: Whether this row is rendered on the canvas.
        draw_ratio: Spatial rendering ratio from 0.0 to 1.0.
        draw_direction: Direction of partial rendering ("left_to_right" or "bottom_to_top").
    """

    def __init__(
        self,
        name: str,
        values: Sequence[float | None],
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None:
        """Initialize a HeatmapChart Row.

        Args:
            name: Row label shown on the Y-axis.
            values: Sequence of numeric values or None for missing cells.
            show: Whether to render this row. Defaults to True.
            draw_ratio: Spatial rendering ratio in [0.0, 1.0]. Defaults to 1.0.
            draw_direction: Partial rendering direction ("left_to_right" or "bottom_to_top").
        """
        self.name: str = name
        self.values: list[float | None] = [float(v) if v is not None else None for v in values]
        self.show: bool = bool(show)
        self.draw_ratio: float = clamp_ratio(draw_ratio)
        self.draw_direction: DrawDirection = draw_direction


class Cell:
    """Represents a cell-level override in a HeatmapChart.

    Attributes:
        x: Zero-based column index.
        y: Zero-based row index.
        value: Numeric cell value (or None for empty cell).
        label: Custom text label overriding formatted numeric value.
        style: Optional custom Style overriding color-scale fill and border for this cell.
        show: Whether this cell is rendered.
    """

    def __init__(
        self,
        x: int,
        y: int,
        value: float | None,
        *,
        label: str = "",
        style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize a HeatmapChart Cell override.

        Args:
            x: Zero-based column index.
            y: Zero-based row index.
            value: Numeric value for the cell, or None.
            label: Custom text annotation inside the cell. Defaults to "".
            style: Optional explicit Style for the cell rectangle.
            show: Whether to render this cell. Defaults to True.
        """
        self.x: int = int(x)
        self.y: int = int(y)
        self.value: float | None = float(value) if value is not None else None
        self.label: str = label
        self.style: Style | None = style
        self.show: bool = bool(show)


class Spot:
    """Represents a spatial thermal hotspot in a HeatmapOverlay.

    Attributes:
        xy: Center coordinate (x, y) of the hotspot.
        value: Numerical intensity/temperature value of the hotspot.
        radius: Influence radius of the hotspot in canvas units.
        label: Optional text annotation displayed at the hotspot center.
        label_style: Optional custom Style for the hotspot annotation text.
        style: Optional Style overriding the hotspot's contour/peak color.
        show: Whether this hotspot is rendered.
        draw_ratio: Spatial rendering ratio in [0.0, 1.0] scaling hotspot intensity/radius.
    """

    def __init__(
        self,
        xy: tuple[float, float],
        value: float = 1.0,
        radius: float = 15.0,
        *,
        label: str = "",
        label_style: Style | None = None,
        style: Style | None = None,
        show: bool = True,
        draw_ratio: float = 1.0,
    ) -> None:
        """Initialize a spatial hotspot.

        Args:
            xy: Center coordinate (x, y) on the canvas or relative to overlay base_xy.
            value: Numerical intensity value. Defaults to 1.0.
            radius: Influence radius in canvas units. Defaults to 15.0.
            label: Optional text label displayed at the hotspot. Defaults to "".
            label_style: Optional Style for the hotspot label text.
            style: Optional Style overriding the hotspot color.
            show: Whether to render this hotspot. Defaults to True.
            draw_ratio: Partial rendering ratio in [0.0, 1.0]. Defaults to 1.0.
        """
        self.xy: tuple[float, float] = (float(xy[0]), float(xy[1]))
        self.value: float = float(value)
        self.radius: float = max(0.1, float(radius))
        self.label: str = label
        self.label_style: Style | None = label_style
        self.style: Style | None = style
        self.show: bool = bool(show)
        self.draw_ratio: float = clamp_ratio(draw_ratio)


def resolve_style_stops(
    styles: Sequence[Style] | None,
    min_style: Style | None,
    max_style: Style | None,
) -> list[Style]:
    """Validate and resolve color scale Style stops from styles list or min_style/max_style.

    Args:
        styles: Optional sequence of 2 or more Style objects.
        min_style: Optional minimum value Style object.
        max_style: Optional maximum value Style object.

    Returns:
        List of at least 2 Style objects representing color scale stops.

    Raises:
        ValueError: If fewer than 2 Style stops are provided.
    """
    if styles is not None:
        stop_list = list(styles)
        if len(stop_list) < 2:
            raise ValueError(f"'styles' must contain at least 2 Style objects, got {len(stop_list)}.")
        return stop_list

    if min_style is not None and max_style is not None:
        return [min_style, max_style]

    msg = "Heatmap color scale requires either 'styles' (>= 2 Style objects) or both 'min_style' and 'max_style'."
    raise ValueError(msg)


def _is_visible_color(c: ColorType | None) -> bool:
    """Return True if color is not None and has positive alpha."""
    if c is None:
        return False
    col = c if isinstance(c, Color) else Color(c)
    return col.alpha > 0.0


def extract_heatmap_color(style: Style) -> Color:
    """Extract primary fill or stroke Color from a Style object for heatmap interpolation.

    Args:
        style: Style instance defining a color stop.

    Returns:
        Extracted Color instance.
    """
    raw_color: ColorType = (30, 41, 59, 1.0)
    if _is_visible_color(style.shape_fill_color) and style.shape_fill_color is not None:
        raw_color = style.shape_fill_color
    elif _is_visible_color(style.line_color) and style.line_color is not None:
        raw_color = style.line_color
    elif _is_visible_color(style.shape_line_color) and style.shape_line_color is not None:
        raw_color = style.shape_line_color
    elif _is_visible_color(style.text_color) and style.text_color is not None:
        raw_color = style.text_color
    elif style.shape_fill_color is not None:
        raw_color = style.shape_fill_color

    col = raw_color if isinstance(raw_color, Color) else Color(raw_color)
    if style.alpha is not None:
        return Color(col.r, col.g, col.b, alpha=round(float(style.alpha), 5))
    return col


def interpolate_color_stops(stops: Sequence[Color], ratio: float) -> Color:
    """Interpolate a Color along a multi-stop color gradient at normalized ratio in [0.0, 1.0].

    Args:
        stops: Sequence of 2 or more Color instances from min (0.0) to max (1.0).
        ratio: Normalized position in [0.0, 1.0].

    Returns:
        Interpolated Color instance.
    """
    t = clamp_ratio(ratio)
    n = len(stops)
    if n == 0:
        return Color(30, 41, 59, alpha=1.0)
    if n == 1 or t <= 0.0:
        return stops[0]
    if t >= 1.0:
        return stops[-1]

    scaled = t * (n - 1)
    idx = min(int(math.floor(scaled)), n - 2)
    frac = scaled - idx
    c1 = stops[idx]
    c2 = stops[idx + 1]

    r = round(c1.r + (c2.r - c1.r) * frac)
    g = round(c1.g + (c2.g - c1.g) * frac)
    b = round(c1.b + (c2.b - c1.b) * frac)
    a = round(c1.alpha + (c2.alpha - c1.alpha) * frac, 5)
    return Color(r, g, b, alpha=a)


def format_heatmap_value(value: float, fmt: FormatterType) -> str:
    """Format a numeric heatmap value into a display string.

    Args:
        value: Float value to format.
        fmt: Optional format string or callable.

    Returns:
        Formatted string.
    """
    if isinstance(fmt, str):
        try:
            return fmt.format(value)
        except Exception:
            return f"{value:g}"
    if callable(fmt):
        return str(fmt(value))
    if abs(value - round(value)) < 1e-6:
        return f"{int(round(value))}"
    return f"{value:.2g}" if abs(value) < 1.0 else f"{value:.1f}"


def _resolve_colorbar_stroke_style(border_style: Style | None, text_style: Style) -> Style:
    """Resolve effective stroke Style for colorbar border and ticks from border_style or text_style."""
    if border_style is not None:
        stroke_col = border_style.line_color or border_style.shape_line_color or (100, 116, 139, 1.0)
        stroke_w = border_style.line_width or border_style.shape_line_width or 0.8
        l_style = border_style.line_style or border_style.shape_line_style or "solid"
    else:
        stroke_col = text_style.text_color or text_style.line_color or (100, 116, 139, 1.0)
        stroke_w = 0.8
        l_style = "solid"
    return Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=stroke_col,
        shape_line_width=stroke_w,
        shape_line_style=l_style,
        line_color=stroke_col,
        line_width=stroke_w,
        line_style=l_style,
    )


def _draw_horizontal_colorbar(
    stops: Sequence[Color],
    eff_min: float,
    eff_max: float,
    bx: float,
    by: float,
    bar_len: float,
    bar_thick: float,
    n_ticks: int,
    text_style: Style,
    value_format: FormatterType,
    label: str,
    border_style: Style | None,
) -> None:
    """Render horizontal gradient colorbar segments, border, ticks, and label."""
    n_segments = 64
    seg_w = bar_len / n_segments
    for i in range(n_segments):
        col = interpolate_color_stops(stops, (i + 0.5) / n_segments)
        opaque_col = Color(col.r, col.g, col.b, alpha=1.0)
        canvas_rectangle(
            xy=(bx + (i + 0.5) * seg_w, by + bar_thick / 2.0),
            width=seg_w,
            height=bar_thick,
            style=Style(shape_fill_color=opaque_col, shape_line_color=opaque_col, shape_line_width=0.3),
        )

    eff_border = _resolve_colorbar_stroke_style(border_style, text_style)
    canvas_rectangle(
        xy=(bx + bar_len / 2.0, by + bar_thick / 2.0),
        width=bar_len,
        height=bar_thick,
        style=eff_border,
    )

    tick_t_style = ensure_text_style(text_style, halign="center", valign="top")
    tick_line_style = ensure_line_style(eff_border)
    for k in range(n_ticks):
        ratio = k / (n_ticks - 1)
        val = eff_min + (eff_max - eff_min) * ratio
        tx = bx + ratio * bar_len
        canvas_line(xy1=(tx, by), xy2=(tx, by - 0.6), style=tick_line_style)
        canvas_text(xy=(tx, by - 1.0), text=format_heatmap_value(val, value_format), style=tick_t_style)

    if label:
        lbl_style = ensure_text_style(text_style, halign="center", valign="bottom")
        canvas_text(xy=(bx + bar_len / 2.0, by + bar_thick + 0.8), text=label, style=lbl_style)


def _draw_vertical_colorbar(
    stops: Sequence[Color],
    eff_min: float,
    eff_max: float,
    bx: float,
    by: float,
    bar_len: float,
    bar_thick: float,
    n_ticks: int,
    text_style: Style,
    value_format: FormatterType,
    label: str,
    border_style: Style | None,
) -> None:
    """Render vertical gradient colorbar segments, border, ticks, and label."""
    n_segments = 64
    seg_h = bar_len / n_segments
    for i in range(n_segments):
        col = interpolate_color_stops(stops, (i + 0.5) / n_segments)
        opaque_col = Color(col.r, col.g, col.b, alpha=1.0)
        canvas_rectangle(
            xy=(bx + bar_thick / 2.0, by + (i + 0.5) * seg_h),
            width=bar_thick,
            height=seg_h,
            style=Style(shape_fill_color=opaque_col, shape_line_color=opaque_col, shape_line_width=0.3),
        )

    eff_border = _resolve_colorbar_stroke_style(border_style, text_style)
    canvas_rectangle(
        xy=(bx + bar_thick / 2.0, by + bar_len / 2.0),
        width=bar_thick,
        height=bar_len,
        style=eff_border,
    )

    tick_t_style = ensure_text_style(text_style, halign="left", valign="center")
    tick_line_style = ensure_line_style(eff_border)
    for k in range(n_ticks):
        ratio = k / (n_ticks - 1)
        val = eff_min + (eff_max - eff_min) * ratio
        ty = by + ratio * bar_len
        canvas_line(xy1=(bx + bar_thick, ty), xy2=(bx + bar_thick + 0.6, ty), style=tick_line_style)
        canvas_text(xy=(bx + bar_thick + 1.0, ty), text=format_heatmap_value(val, value_format), style=tick_t_style)

    if label:
        lbl_style = ensure_text_style(text_style, halign="left", valign="bottom")
        canvas_text(xy=(bx, by + bar_len + 1.0), text=label, style=lbl_style)


def draw_colorbar_common(
    stops: Sequence[Color],
    eff_min: float,
    eff_max: float,
    xy: tuple[float, float],
    text_style: Style,
    *,
    length: float = 30.0,
    thickness: float = 2.2,
    orientation: Orientation = "horizontal",
    num_ticks: int = 5,
    value_format: FormatterType = None,
    label: str = "",
    border_style: Style | None = None,
    scale: float = 1.0,
) -> None:
    """Render a continuous gradient colorbar legend with tick labels.

    Args:
        stops: Color stops from eff_min to eff_max.
        eff_min: Minimum scale value.
        eff_max: Maximum scale value.
        xy: Bottom-left anchor coordinate (x, y) of the colorbar bar.
        text_style: Style for tick labels and colorbar title.
        length: Length of the colorbar along its primary axis. Defaults to 30.0.
        thickness: Thickness of the colorbar perpendicular to its axis. Defaults to 2.2.
        orientation: "horizontal" or "vertical". Defaults to "horizontal".
        num_ticks: Number of tick labels along the bar (>= 2). Defaults to 5.
        value_format: Formatter for tick values.
        label: Optional descriptive title label for the colorbar. Defaults to "".
        border_style: Optional Style for the colorbar outline stroke and tick marks.
        scale: Proportional scale factor around xy. Defaults to 1.0.
    """
    bx, by = float(xy[0]), float(xy[1])
    bar_len = max(4.0, float(length))
    bar_thick = max(0.8, float(thickness))
    n_ticks = max(2, int(num_ticks))

    with canvas.transform(origin=(bx, by), scale=scale):
        if orientation == "horizontal":
            _draw_horizontal_colorbar(
                stops,
                eff_min,
                eff_max,
                bx,
                by,
                bar_len,
                bar_thick,
                n_ticks,
                text_style,
                value_format,
                label,
                border_style,
            )
        else:
            _draw_vertical_colorbar(
                stops,
                eff_min,
                eff_max,
                bx,
                by,
                bar_len,
                bar_thick,
                n_ticks,
                text_style,
                value_format,
                label,
                border_style,
            )


def draw_stops_legend_common(
    stops: Sequence[Color],
    eff_min: float,
    eff_max: float,
    xy: tuple[float, float],
    text_style: Style,
    orientation: Orientation = "vertical",
    swatch_width: float = 2.4,
    swatch_height: float = 1.2,
    item_gap: float = 4.0,
    *,
    num_steps: int = 5,
    value_format: FormatterType = None,
    labels: Sequence[str] | None = None,
    scale: float = 1.0,
) -> None:
    """Render discrete stepped color swatches using standard chart legend layout.

    Args:
        stops: Color stops from eff_min to eff_max.
        eff_min: Minimum scale value.
        eff_max: Maximum scale value.
        xy: Starting placement coordinate (x, y).
        text_style: Base Style for legend text labels.
        orientation: "vertical" or "horizontal". Defaults to "vertical".
        swatch_width: Width of color swatches. Defaults to 2.4.
        swatch_height: Height of color swatches. Defaults to 1.2.
        item_gap: Spacing between consecutive legend items. Defaults to 4.0.
        num_steps: Number of discrete swatch steps when labels is None. Defaults to 5.
        value_format: Optional value formatter for step labels.
        labels: Optional explicit list of step label strings.
        scale: Proportional scaling factor around xy. Defaults to 1.0.
    """
    steps = len(labels) if labels is not None and len(labels) >= 2 else max(2, int(num_steps))
    items: list[tuple[str, ColorType, Style | None, bool]] = []
    for i in range(steps):
        ratio = i / (steps - 1)
        col = interpolate_color_stops(stops, ratio)
        if labels is not None and i < len(labels):
            lbl = labels[i]
        else:
            val = eff_min + (eff_max - eff_min) * ratio
            lbl = format_heatmap_value(val, value_format)
        items.append((lbl, col, None, True))

    _legend_module.draw_legend(
        items=items,
        xy=xy,
        text_style=text_style,
        orientation=orientation,
        swatch_width=swatch_width,
        swatch_height=swatch_height,
        item_gap=item_gap,
        scale=scale,
    )
