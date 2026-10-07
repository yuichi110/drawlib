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

from typing import TYPE_CHECKING, Literal, Sequence

from drawlib._charts._common._style_utils import ensure_text_style
from drawlib._charts._common._types import ColorType, Orientation
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import canvas
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    pass


def _unpack_legend_item(
    item: tuple[str, ColorType, Style | None] | tuple[str, ColorType, Style | None, bool],
) -> tuple[str, ColorType, Style | None, bool]:
    """Unpack 3-tuple or 4-tuple legend item into (name, color, custom_text_style, show)."""
    match item:
        case (name, color, custom_text_style, show):
            return (name, color, custom_text_style, show)
        case (name, color, custom_text_style):
            return (name, color, custom_text_style, True)
    return (item[0], item[1], item[2], True)


def draw_legend(
    items: Sequence[tuple[str, ColorType, Style | None] | tuple[str, ColorType, Style | None, bool]],
    xy: tuple[float, float],
    text_style: Style,
    orientation: Orientation | Literal["vertical", "horizontal"] = "vertical",
    swatch_size: tuple[float, float] = (2.4, 1.2),
    item_gap: float = 4.0,
    *,
    scale: float = 1.0,
) -> None:
    """Render legend items onto the canvas at coordinate xy.

    Args:
        items: List of (name, color, optional_item_text_style[, show]) tuples.
        xy: Starting placement coordinate (x, y). For vertical orientation, this is top-left.
            For horizontal orientation, this is middle-left.
        text_style: Base text style for legend labels.
        orientation: "vertical" or "horizontal". Defaults to "vertical".
        swatch_size: (width, height) of the color swatch rectangle. Defaults to (2.4, 1.2).
        item_gap: Spacing between consecutive legend items. Defaults to 4.0.
        scale: Proportional scaling factor around xy. Defaults to 1.0.
    """
    if not items:
        return

    swatch_w, swatch_h = float(swatch_size[0]), float(swatch_size[1])
    swatch_r = 0.3
    text_offset = 0.8
    start_x, start_y = float(xy[0]), float(xy[1])

    with canvas.transform(origin=(start_x, start_y), scale=scale):
        if orientation == "vertical":
            base_size = float(text_style.text_size) if text_style.text_size is not None else 10.0
            step_y = max(swatch_h + 1.5, base_size * 0.35, 3.5)
            for i, raw_item in enumerate(items):
                name, color, custom_text_style, show = _unpack_legend_item(raw_item)
                if not show:
                    continue
                item_y = start_y - (i * step_y)
                swatch_cx = start_x + swatch_w / 2.0
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
                raw_style = text_style.patch(custom_text_style) if custom_text_style is not None else text_style
                item_style = ensure_text_style(raw_style, halign="left", valign="center")
                canvas_text(
                    xy=(start_x + swatch_w + text_offset, item_y),
                    text=name,
                    style=item_style,
                )
        else:
            cur_x = start_x
            for raw_item in items:
                name, color, custom_text_style, show = _unpack_legend_item(raw_item)
                raw_style = text_style.patch(custom_text_style) if custom_text_style is not None else text_style
                item_style = ensure_text_style(raw_style, halign="left", valign="center")
                t_size: float = float(item_style.text_size) if item_style.text_size is not None else 10.0
                approx_w = float(len(name)) * t_size * 0.12
                if show:
                    swatch_cx = cur_x + swatch_w / 2.0
                    canvas_rectangle(
                        xy=(swatch_cx, start_y),
                        width=swatch_w,
                        height=swatch_h,
                        r=swatch_r,
                        style=Style(
                            shape_fill_color=color,
                            shape_line_color=Colors.Transparent,
                            shape_line_width=0,
                        ),
                    )
                    text_x = cur_x + swatch_w + text_offset
                    canvas_text(
                        xy=(text_x, start_y),
                        text=name,
                        style=item_style,
                    )
                cur_x += swatch_w + text_offset + approx_w + item_gap
