# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Edge routing and rendering functions for architecture diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams._common import (
    apply_edge_padding,
    apply_segment_padding,
    parse_padding,
    resolve_visible_edges_with_junctions,
)
from drawlib._diagrams.architecture._junction import Junction
from drawlib._diagrams.architecture._node import Node
from drawlib._diagrams.architecture._types import Connectable

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._edge import Edge


def get_item_anchors(
    item: Connectable,
    canvas_xy: tuple[float, float],
) -> dict[str, tuple[float, float]]:
    """Compute anchor points for an item at its absolute canvas position."""
    cx, cy = canvas_xy
    if isinstance(item, Junction):
        return {"center": canvas_xy, "left": canvas_xy, "right": canvas_xy, "top": canvas_xy, "bottom": canvas_xy}

    if isinstance(item, Node):
        lx, ly = item.left
        rx, ry = item.right
        tx, ty = item.top
        bx, by = item.bottom
        ox, oy = item._local_xy
        return {
            "center": canvas_xy,
            "left": (cx + (lx - ox), cy + (ly - oy)),
            "right": (cx + (rx - ox), cy + (ry - oy)),
            "top": (cx + (tx - ox), cy + (ty - oy)),
            "bottom": (cx + (bx - ox), cy + (by - oy)),
        }

    # NodeGroup
    min_x, min_y, max_x, max_y = item.get_bounds()
    w = max_x - min_x
    h = max_y - min_y
    return {
        "center": (cx + min_x + w / 2.0, cy + min_y + h / 2.0),
        "left": (cx + min_x, cy + min_y + h / 2.0),
        "right": (cx + max_x, cy + min_y + h / 2.0),
        "top": (cx + min_x + w / 2.0, cy + max_y),
        "bottom": (cx + min_x + w / 2.0, cy + min_y),
    }


def resolve_connection_endpoints(
    start: Connectable,
    end: Connectable,
    start_canvas_xy: tuple[float, float],
    end_canvas_xy: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float], str]:
    """Determine the optimal anchor pair and primary axis orientation."""
    start_anchors = get_item_anchors(start, start_canvas_xy)
    end_anchors = get_item_anchors(end, end_canvas_xy)

    sx, sy = start_anchors["center"]
    ex, ey = end_anchors["center"]

    dx = ex - sx
    dy = ey - sy

    if abs(dx) >= abs(dy):
        # Major horizontal direction
        orientation = "horizontal"
        start_pt = start_anchors["right"] if dx > 0 else start_anchors["left"]
        end_pt = end_anchors["left"] if dx > 0 else end_anchors["right"]
    else:
        # Major vertical direction
        orientation = "vertical"
        start_pt = start_anchors["top"] if dy > 0 else start_anchors["bottom"]
        end_pt = end_anchors["bottom"] if dy > 0 else end_anchors["top"]

    return start_pt, end_pt, orientation


def compute_edge_points(
    start_pt: tuple[float, float],
    end_pt: tuple[float, float],
    orientation: str,
    waypoints: list[tuple[float, float]],
    routing: str,
    base_xy: tuple[float, float],
) -> list[tuple[float, float]]:
    """Compute the list of polyline points for an edge."""
    if waypoints:
        bx, by = base_xy
        pts = [start_pt]
        for wx, wy in waypoints:
            pts.append((bx + wx, by + wy))
        pts.append(end_pt)
        return pts

    if routing == "orthogonal":
        sx, sy = start_pt
        ex, ey = end_pt
        if abs(sx - ex) < 1e-4 or abs(sy - ey) < 1e-4:
            return [start_pt, end_pt]
        if orientation == "horizontal":
            mid_x = (sx + ex) / 2.0
            return [start_pt, (mid_x, sy), (mid_x, ey), end_pt]
        mid_y = (sy + ey) / 2.0
        return [start_pt, (sx, mid_y), (ex, mid_y), end_pt]

    return [start_pt, end_pt]


def draw_single_edge(
    edge: Edge,
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
    default_edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Draw a single edge and its label."""
    if not edge.show or not edge.start.show or not edge.end.show:
        return
    if edge.start not in canvas_xy_map or edge.end not in canvas_xy_map:
        return

    start_canvas_xy = canvas_xy_map[edge.start]
    end_canvas_xy = canvas_xy_map[edge.end]

    start_pt, end_pt, orientation = resolve_connection_endpoints(edge.start, edge.end, start_canvas_xy, end_canvas_xy)
    applied_style = default_edge_style.patch(edge.style)
    pts = compute_edge_points(start_pt, end_pt, orientation, edge.waypoints, edge.routing, base_xy)
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

    if not edge.label:
        return

    mid_idx = len(pts) // 2
    lx = (pts[mid_idx - 1][0] + pts[mid_idx][0]) / 2.0
    ly = (pts[mid_idx - 1][1] + pts[mid_idx][1]) / 2.0

    base_label_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_REGULAR,
        text_bg_fill_color=(255, 255, 255, 0.9),
        text_bg_line_color=None,
        text_bg_line_width=0,
        halign="center",
        valign="center",
    )
    applied_text_style = edge.text_style or default_edge_text_style
    label_style = base_label_style.patch(applied_text_style)

    canvas_text(xy=(lx, ly), text=edge.label, style=label_style)


def draw_edges(
    edges: list[Edge],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
    default_edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Draw all connections in Layer 1."""
    visible_edges = resolve_visible_edges_with_junctions(edges, Junction)
    for edge in visible_edges:
        draw_single_edge(edge, canvas_xy_map, base_xy, default_edge_style, default_edge_text_style)


__all__ = [
    "apply_edge_padding",
    "apply_segment_padding",
    "compute_edge_points",
    "draw_edges",
    "draw_single_edge",
    "get_item_anchors",
    "parse_padding",
    "resolve_connection_endpoints",
]
