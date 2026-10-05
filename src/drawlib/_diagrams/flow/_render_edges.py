# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Edge routing and rendering functions for flow diagrams."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.flow._junction import Junction
from drawlib._diagrams.flow._types import Connectable, PaddingType, Side

if TYPE_CHECKING:
    from drawlib._diagrams.flow._edge import FlowEdge


def get_item_anchors(
    item: Connectable,
    canvas_xy: tuple[float, float],
) -> dict[str, tuple[float, float]]:
    """Compute anchor points for an item at its absolute canvas position."""
    cx, cy = canvas_xy
    if isinstance(item, Junction):
        return {
            "center": canvas_xy,
            "left": canvas_xy,
            "right": canvas_xy,
            "top": canvas_xy,
            "bottom": canvas_xy,
        }

    half_w = item.width / 2.0
    half_h = item.height / 2.0
    return {
        "center": (cx, cy),
        "left": (cx - half_w, cy),
        "right": (cx + half_w, cy),
        "top": (cx, cy + half_h),
        "bottom": (cx, cy - half_h),
    }


def resolve_connection_endpoints(
    start: Connectable,
    end: Connectable,
    start_canvas_xy: tuple[float, float],
    end_canvas_xy: tuple[float, float],
    start_side: Side,
    end_side: Side,
) -> tuple[tuple[float, float], tuple[float, float], Side, Side]:
    """Determine the exact start and end anchor coordinates and resolved sides."""
    start_anchors = get_item_anchors(start, start_canvas_xy)
    end_anchors = get_item_anchors(end, end_canvas_xy)

    sx, sy = start_anchors["center"]
    ex, ey = end_anchors["center"]
    dx = ex - sx
    dy = ey - sy

    # Resolve start side
    resolved_start_side: Side = start_side
    if resolved_start_side == "auto":
        if abs(dx) >= abs(dy):
            resolved_start_side = "right" if dx >= 0 else "left"
        else:
            resolved_start_side = "top" if dy >= 0 else "bottom"

    # Resolve end side
    resolved_end_side: Side = end_side
    if resolved_end_side == "auto":
        if abs(dx) >= abs(dy):
            resolved_end_side = "left" if dx >= 0 else "right"
        else:
            resolved_end_side = "bottom" if dy >= 0 else "top"

    start_pt = start_anchors.get(resolved_start_side, start_anchors["center"])
    end_pt = end_anchors.get(resolved_end_side, end_anchors["center"])

    return start_pt, end_pt, resolved_start_side, resolved_end_side


def compute_orthogonal_points(
    start_pt: tuple[float, float],
    end_pt: tuple[float, float],
    start_side: Side,
    end_side: Side,
) -> list[tuple[float, float]]:
    """Compute orthogonal bend points between start and end anchors."""
    sx, sy = start_pt
    ex, ey = end_pt

    # Straight line along single axis
    if abs(sx - ex) < 1e-4 or abs(sy - ey) < 1e-4:
        return [start_pt, end_pt]

    horizontal_sides = {"left", "right"}
    vertical_sides = {"top", "bottom"}

    # Both horizontal
    if start_side in horizontal_sides and end_side in horizontal_sides:
        mid_x = (sx + ex) / 2.0
        return [start_pt, (mid_x, sy), (mid_x, ey), end_pt]

    # Both vertical
    if start_side in vertical_sides and end_side in vertical_sides:
        mid_y = (sy + ey) / 2.0
        return [start_pt, (sx, mid_y), (ex, mid_y), end_pt]

    # Horizontal exit, Vertical entry (L-bend)
    if start_side in horizontal_sides and end_side in vertical_sides:
        return [start_pt, (ex, sy), end_pt]

    # Vertical exit, Horizontal entry (L-bend)
    if start_side in vertical_sides and end_side in horizontal_sides:
        return [start_pt, (sx, ey), end_pt]

    # Fallback to midpoint Z-bend
    mid_y = (sy + ey) / 2.0
    return [start_pt, (sx, mid_y), (ex, mid_y), end_pt]


def compute_edge_points(
    start_pt: tuple[float, float],
    end_pt: tuple[float, float],
    start_side: Side,
    end_side: Side,
    waypoints: list[tuple[float, float]],
    routing: str,
    base_xy: tuple[float, float],
) -> list[tuple[float, float]]:
    """Compute polyline points along the edge path."""
    if waypoints:
        bx, by = base_xy
        pts = [start_pt]
        for wx, wy in waypoints:
            pts.append((bx + wx, by + wy))
        pts.append(end_pt)
        return pts

    if routing == "direct":
        return [start_pt, end_pt]

    return compute_orthogonal_points(start_pt, end_pt, start_side, end_side)


def parse_padding(padding: PaddingType) -> tuple[float, float]:
    """Extract (start_pad, end_pad) from PaddingType."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val
    return float(padding[0]), float(padding[1])


def apply_segment_padding(
    p0: tuple[float, float],
    p1: tuple[float, float],
    start_pad: float,
    end_pad: float,
) -> list[tuple[float, float]]:
    """Trim a 2-point segment by start and end padding."""
    dist = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if dist < 1e-6:
        return [p0, p1]

    if start_pad + end_pad >= dist:
        scale = (dist * 0.9) / (start_pad + end_pad)
        sp = start_pad * scale
        ep = end_pad * scale
    else:
        sp = start_pad
        ep = end_pad

    dx = (p1[0] - p0[0]) / dist
    dy = (p1[1] - p0[1]) / dist
    new_p0 = (p0[0] + dx * sp, p0[1] + dy * sp)
    new_p1 = (p1[0] - dx * ep, p1[1] - dy * ep)
    return [new_p0, new_p1]


def apply_edge_padding(
    pts: list[tuple[float, float]],
    padding: PaddingType,
) -> list[tuple[float, float]]:
    """Shorten the start and end of an edge path by padding distance."""
    if len(pts) < 2:
        return pts

    start_pad, end_pad = parse_padding(padding)
    if start_pad <= 0.0 and end_pad <= 0.0:
        return pts

    if len(pts) == 2:
        return apply_segment_padding(pts[0], pts[1], start_pad, end_pad)

    result = list(pts)
    if start_pad > 0.0:
        p0, p1 = result[0], result[1]
        dist_start = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        if dist_start > 1e-6:
            sp = min(start_pad, dist_start * 0.9)
            dx = (p1[0] - p0[0]) / dist_start
            dy = (p1[1] - p0[1]) / dist_start
            result[0] = (p0[0] + dx * sp, p0[1] + dy * sp)

    if end_pad > 0.0:
        p_prev, p_last = result[-2], result[-1]
        dist_end = math.hypot(p_last[0] - p_prev[0], p_last[1] - p_prev[1])
        if dist_end > 1e-6:
            ep = min(end_pad, dist_end * 0.9)
            dx = (p_prev[0] - p_last[0]) / dist_end
            dy = (p_prev[1] - p_last[1]) / dist_end
            result[-1] = (p_last[0] + dx * ep, p_last[1] + dy * ep)

    return result


def render_edges(
    edges: list[FlowEdge],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
    default_edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render all FlowEdge connections."""
    for edge in edges:
        if edge.start not in canvas_xy_map or edge.end not in canvas_xy_map:
            continue

        start_canvas_xy = canvas_xy_map[edge.start]
        end_canvas_xy = canvas_xy_map[edge.end]

        start_pt, end_pt, s_side, e_side = resolve_connection_endpoints(
            edge.start,
            edge.end,
            start_canvas_xy,
            end_canvas_xy,
            edge.start_side,
            edge.end_side,
        )

        applied_style = default_edge_style.patch(edge.style) if edge.style is not None else default_edge_style
        pts = compute_edge_points(
            start_pt,
            end_pt,
            s_side,
            e_side,
            edge.waypoints,
            edge.routing,
            base_xy,
        )
        pts = apply_edge_padding(pts, edge.padding)

        arrow_head: Literal["", "->", "<-", "<->"] = ""
        if edge.arrow == "->":
            arrow_head = "->"
        elif edge.arrow == "<-":
            arrow_head = "<-"
        elif edge.arrow == "<->":
            arrow_head = "<->"

        if len(pts) == 2:
            canvas_line(xy1=pts[0], xy2=pts[1], arrow_head=arrow_head, style=applied_style)
        else:
            canvas_lines(xys=pts, arrow_head=arrow_head, style=applied_style)

        if edge.label:
            mid_idx = len(pts) // 2
            lx = (pts[mid_idx - 1][0] + pts[mid_idx][0]) / 2.0
            ly = (pts[mid_idx - 1][1] + pts[mid_idx][1]) / 2.0

            base_label_style = Style(
                text_size=11,
                text_font=Font.SANSSERIF_REGULAR,
                text_bg_fill_color=(255, 255, 255, 0.9),
                text_bg_line_color=None,
                text_bg_line_width=0,
                text_halign="center",
                text_valign="center",
            )
            applied_text_style = edge.text_style or default_edge_text_style
            label_style = base_label_style.patch(applied_text_style)

            canvas_text(xy=(lx, ly), text=edge.label, style=label_style)
