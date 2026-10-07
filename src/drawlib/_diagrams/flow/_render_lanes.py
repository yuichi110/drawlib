# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Swimlane rendering functions for flow diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text

if TYPE_CHECKING:
    from drawlib._diagrams.flow._lane import Lane

DEFAULT_LANE_BG = (248, 250, 252, 0.5)
DEFAULT_LANE_ALT_BG = (241, 245, 249, 0.5)
DEFAULT_LANE_BORDER = (203, 213, 225, 1.0)  # Slate-300
DEFAULT_LANE_HEADER_BG = (226, 232, 240, 1.0)  # Slate-200


def render_lanes(
    lanes: list[Lane],
    orientation: str,
    base_xy: tuple[float, float],
    dw: float,
    dh: float,
) -> None:
    """Render swimlane backgrounds, boundaries, and headers.

    Args:
        lanes: List of Lane instances.
        orientation: 'vertical' or 'horizontal'.
        base_xy: Base placement coordinate (x, y) on canvas.
        dw: Diagram total width.
        dh: Diagram total height.
    """
    bx, by = base_xy

    if orientation == "vertical":
        cur_x = bx
        for i, lane in enumerate(lanes):
            lane_w = lane.size
            if not lane.show:
                cur_x += lane_w
                continue
            lane_h = dh
            bg_color = DEFAULT_LANE_ALT_BG if i % 2 == 1 else DEFAULT_LANE_BG
            default_lane_style = Style(
                shape_fill_color=bg_color,
                shape_line_color=DEFAULT_LANE_BORDER,
                shape_line_width=1.0,
            )
            lane_style = default_lane_style.patch(lane.style)

            # Lane body (centered at cur_x + lane_w / 2, by + lane_h / 2)
            canvas_rectangle(
                xy=(cur_x + lane_w / 2.0, by + lane_h / 2.0),
                width=lane_w,
                height=lane_h,
                style=lane_style,
            )

            # Lane header
            header_h = min(lane.header_size, lane_h)
            header_y = by + lane_h - header_h
            default_header_style = Style(
                shape_fill_color=DEFAULT_LANE_HEADER_BG,
                shape_line_color=DEFAULT_LANE_BORDER,
                shape_line_width=1.0,
            )
            header_style = default_header_style.patch(lane.header_style)
            canvas_rectangle(
                xy=(cur_x + lane_w / 2.0, header_y + header_h / 2.0),
                width=lane_w,
                height=header_h,
                style=header_style,
            )

            # Header text
            text_size = 12.0
            if lane.text_style and lane.text_style.text_size is not None:
                text_size = float(lane.text_style.text_size)
            default_header_text_style = Style(
                text_size=text_size,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(30, 41, 59, 1.0),
                text_halign="center",
                text_valign="center",
            )
            header_text_style = (
                default_header_text_style.patch(lane.text_style) if lane.text_style else default_header_text_style
            )
            canvas_text(
                xy=(cur_x + lane_w / 2.0, header_y + header_h / 2.0),
                text=lane.title,
                style=header_text_style,
            )

            cur_x += lane_w
    else:
        # Horizontal lanes (top-to-bottom)
        cur_y = by + dh
        for i, lane in enumerate(lanes):
            lane_h = lane.size
            if not lane.show:
                cur_y -= lane_h
                continue
            lane_w = dw
            lane_y = cur_y - lane_h
            bg_color = DEFAULT_LANE_ALT_BG if i % 2 == 1 else DEFAULT_LANE_BG
            default_lane_style = Style(
                shape_fill_color=bg_color,
                shape_line_color=DEFAULT_LANE_BORDER,
                shape_line_width=1.0,
            )
            lane_style = default_lane_style.patch(lane.style)

            # Lane body (centered at bx + lane_w / 2, lane_y + lane_h / 2)
            canvas_rectangle(
                xy=(bx + lane_w / 2.0, lane_y + lane_h / 2.0),
                width=lane_w,
                height=lane_h,
                style=lane_style,
            )

            # Lane header (left column, centered at bx + header_w / 2, lane_y + lane_h / 2)
            header_w = min(lane.header_size, lane_w)
            default_header_style = Style(
                shape_fill_color=DEFAULT_LANE_HEADER_BG,
                shape_line_color=DEFAULT_LANE_BORDER,
                shape_line_width=1.0,
            )
            header_style = default_header_style.patch(lane.header_style)
            canvas_rectangle(
                xy=(bx + header_w / 2.0, lane_y + lane_h / 2.0),
                width=header_w,
                height=lane_h,
                style=header_style,
            )

            # Header text
            text_size = 12.0
            if lane.text_style and lane.text_style.text_size is not None:
                text_size = float(lane.text_style.text_size)
            default_header_text_style = Style(
                text_size=text_size,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(30, 41, 59, 1.0),
                text_halign="center",
                text_valign="center",
            )
            header_text_style = (
                default_header_text_style.patch(lane.text_style) if lane.text_style else default_header_text_style
            )
            canvas_text(
                xy=(bx + header_w / 2.0, lane_y + lane_h / 2.0),
                text=lane.title,
                style=header_text_style,
            )

            cur_y -= lane_h
