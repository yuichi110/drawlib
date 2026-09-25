# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for flow diagrams."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Colors, Style
from drawlib._diagrams.flow._junction import Junction
from drawlib._diagrams.flow._lane import Lane
from drawlib._diagrams.flow._node import FlowNode
from drawlib._diagrams.flow._nodes import Data, Decision, End, Process, Start
from drawlib._diagrams.flow._types import Connectable, PaddingType, Side
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.shapes import parallelogram as canvas_parallelogram
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.shapes import rhombus as canvas_rhombus
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._diagrams.flow._diagram import FlowDiagram
    from drawlib._diagrams.flow._edge import FlowEdge

# Default colors
_DEFAULT_BORDER_COLOR = (71, 85, 105, 1.0)  # Slate-600
_DEFAULT_FILL_COLOR = (248, 250, 252, 1.0)  # Slate-50
_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_EDGE_COLOR = (71, 85, 105, 1.0)  # Slate-600

_DEFAULT_LANE_BG = (248, 250, 252, 0.5)
_DEFAULT_LANE_ALT_BG = (241, 245, 249, 0.5)
_DEFAULT_LANE_BORDER = (203, 213, 225, 1.0)  # Slate-300
_DEFAULT_LANE_HEADER_BG = (226, 232, 240, 1.0)  # Slate-200


def draw_diagram(diagram: FlowDiagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Render the complete flow diagram onto the canvas at base coordinate xy.

    Args:
        diagram: FlowDiagram container instance.
        xy: Base canvas coordinate (x, y) where the diagram is placed.
    """
    base_xy = (float(xy[0]), float(xy[1]))
    canvas_xy_map, all_nodes, all_junctions = _resolve_coordinates(diagram, base_xy)
    dw, dh = diagram.get_size()
    bx, by = base_xy

    # Layer 0: Canvas Background
    if diagram.style is not None:
        bg_style = Style(
            shape_fill_color=Colors.White,
            shape_line_color=Colors.Transparent,
            shape_line_width=0.0,
        ).patch(diagram.style)
        canvas_rectangle(
            xy=(bx + dw / 2.0, by + dh / 2.0),
            width=dw,
            height=dh,
            style=bg_style,
        )

    # Layer 1: Swimlanes
    if diagram.lanes:
        _render_lanes(diagram.lanes, diagram.lane_orientation, base_xy, dw, dh)

    # Layer 2: Flow Edges
    _render_edges(diagram.edges, canvas_xy_map, base_xy)

    # Layer 3: Flow Nodes & Junctions
    _render_nodes(all_nodes, canvas_xy_map)

    # Layer 4: Title
    if diagram.title:
        title_style = Style(
            text_size=16,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(bx + dw / 2.0, by + dh + 2.0), text=diagram.title, style=title_style)


def _resolve_coordinates(
    diagram: FlowDiagram,
    base_xy: tuple[float, float],
) -> tuple[dict[Connectable, tuple[float, float]], list[FlowNode], list[Junction]]:
    """Resolve canvas coordinates for all items in the diagram.

    Args:
        diagram: FlowDiagram instance.
        base_xy: Placement base coordinate on canvas.

    Returns:
        Tuple of (item_to_canvas_xy, list_of_nodes, list_of_junctions).
    """
    canvas_xy_map: dict[Connectable, tuple[float, float]] = {}
    all_nodes: list[FlowNode] = []
    all_junctions: list[Junction] = []
    bx, by = base_xy

    for item, (ix, iy) in diagram._items:
        canvas_xy = (bx + ix, by + iy)
        canvas_xy_map[item] = canvas_xy
        if isinstance(item, FlowNode):
            all_nodes.append(item)
        elif isinstance(item, Junction):
            all_junctions.append(item)

    return canvas_xy_map, all_nodes, all_junctions


def _render_lanes(
    lanes: list[Lane],
    orientation: str,
    base_xy: tuple[float, float],
    dw: float,
    dh: float,
) -> None:
    """Render swimlane backgrounds, boundaries, and headers."""
    bx, by = base_xy

    if orientation == "vertical":
        cur_x = bx
        for i, lane in enumerate(lanes):
            lane_w = lane.size
            lane_h = dh
            bg_color = _DEFAULT_LANE_ALT_BG if i % 2 == 1 else _DEFAULT_LANE_BG
            default_lane_style = Style(
                shape_fill_color=bg_color,
                shape_line_color=_DEFAULT_LANE_BORDER,
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
                shape_fill_color=_DEFAULT_LANE_HEADER_BG,
                shape_line_color=_DEFAULT_LANE_BORDER,
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
            text_size = lane.textsize or 12.0
            default_header_textstyle = Style(
                text_size=text_size,
                text_font=Font.SANSSERIF_BOLD,
                text_color=_DEFAULT_TEXT_COLOR,
                text_halign="center",
                text_valign="center",
            )
            header_textstyle = default_header_textstyle.patch(lane.textstyle)
            canvas_text(
                xy=(cur_x + lane_w / 2.0, header_y + header_h / 2.0),
                text=lane.title,
                style=header_textstyle,
            )

            cur_x += lane_w
    else:
        # Horizontal lanes (top-to-bottom)
        cur_y = by + dh
        for i, lane in enumerate(lanes):
            lane_h = lane.size
            lane_w = dw
            lane_y = cur_y - lane_h
            bg_color = _DEFAULT_LANE_ALT_BG if i % 2 == 1 else _DEFAULT_LANE_BG
            default_lane_style = Style(
                shape_fill_color=bg_color,
                shape_line_color=_DEFAULT_LANE_BORDER,
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
                shape_fill_color=_DEFAULT_LANE_HEADER_BG,
                shape_line_color=_DEFAULT_LANE_BORDER,
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
            text_size = lane.textsize or 12.0
            default_header_textstyle = Style(
                text_size=text_size,
                text_font=Font.SANSSERIF_BOLD,
                text_color=_DEFAULT_TEXT_COLOR,
                text_halign="center",
                text_valign="center",
            )
            header_textstyle = default_header_textstyle.patch(lane.textstyle)
            canvas_text(
                xy=(bx + header_w / 2.0, lane_y + lane_h / 2.0),
                text=lane.title,
                style=header_textstyle,
            )

            cur_y -= lane_h


def _get_item_anchors(
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


def _resolve_connection_endpoints(
    start: Connectable,
    end: Connectable,
    start_canvas_xy: tuple[float, float],
    end_canvas_xy: tuple[float, float],
    start_side: Side,
    end_side: Side,
) -> tuple[tuple[float, float], tuple[float, float], Side, Side]:
    """Determine the exact start and end anchor coordinates and resolved sides."""
    start_anchors = _get_item_anchors(start, start_canvas_xy)
    end_anchors = _get_item_anchors(end, end_canvas_xy)

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


def _compute_orthogonal_points(
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


def _compute_edge_points(
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

    return _compute_orthogonal_points(start_pt, end_pt, start_side, end_side)


def _parse_padding(padding: PaddingType) -> tuple[float, float]:
    """Extract (start_pad, end_pad) from PaddingType."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val
    return float(padding[0]), float(padding[1])


def _apply_segment_padding(
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


def _apply_edge_padding(
    pts: list[tuple[float, float]],
    padding: PaddingType,
) -> list[tuple[float, float]]:
    """Shorten the start and end of an edge path by padding distance."""
    if len(pts) < 2:
        return pts

    start_pad, end_pad = _parse_padding(padding)
    if start_pad <= 0.0 and end_pad <= 0.0:
        return pts

    if len(pts) == 2:
        return _apply_segment_padding(pts[0], pts[1], start_pad, end_pad)

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


def _render_edges(
    edges: list[FlowEdge],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
) -> None:
    """Render all FlowEdge connections."""
    default_edge_style = Style(
        line_color=_DEFAULT_EDGE_COLOR,
        line_width=1.5,
    )

    for edge in edges:
        if edge.start not in canvas_xy_map or edge.end not in canvas_xy_map:
            continue

        start_canvas_xy = canvas_xy_map[edge.start]
        end_canvas_xy = canvas_xy_map[edge.end]

        start_pt, end_pt, s_side, e_side = _resolve_connection_endpoints(
            edge.start,
            edge.end,
            start_canvas_xy,
            end_canvas_xy,
            edge.start_side,
            edge.end_side,
        )

        applied_style = default_edge_style.patch(edge.style)
        pts = _compute_edge_points(
            start_pt,
            end_pt,
            s_side,
            e_side,
            edge.waypoints,
            edge.routing,
            base_xy,
        )
        pts = _apply_edge_padding(pts, edge.padding)

        arrowhead: Literal["", "->", "<-", "<->"] = ""
        if edge.arrow == "->":
            arrowhead = "->"
        elif edge.arrow == "<-":
            arrowhead = "<-"
        elif edge.arrow == "<->":
            arrowhead = "<->"

        if len(pts) == 2:
            canvas_line(xy1=pts[0], xy2=pts[1], arrowhead=arrowhead, style=applied_style)
        else:
            canvas_lines(xys=pts, arrowhead=arrowhead, style=applied_style)

        if edge.label:
            mid_idx = len(pts) // 2
            lx = (pts[mid_idx - 1][0] + pts[mid_idx][0]) / 2.0
            ly = (pts[mid_idx - 1][1] + pts[mid_idx][1]) / 2.0

            label_style = Style(
                text_size=11,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=_DEFAULT_TEXT_COLOR,
                text_bg_fill_color=(255, 255, 255, 0.9),
                text_bg_line_color=None,
                text_bg_line_width=0,
                text_halign="center",
                text_valign="center",
            )
            if edge.textstyle:
                label_style = label_style.patch(edge.textstyle)

            canvas_text(xy=(lx, ly), text=edge.label, style=label_style)


def _render_nodes(
    nodes: list[FlowNode],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
) -> None:
    """Render all FlowNodes."""
    default_node_style = Style(
        shape_fill_color=_DEFAULT_FILL_COLOR,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )

    for node in nodes:
        cx, cy = canvas_xy_map[node]
        w, h = node.width, node.height

        applied_style = default_node_style.patch(node.style)

        text_size = node.textsize or 12.0
        text_style = Style(
            text_size=text_size,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="center",
        )
        if node.textstyle:
            text_style = text_style.patch(node.textstyle)

        if node.shape_type == "process":
            canvas_rectangle(
                xy=(cx, cy),
                width=w,
                height=h,
                r=node.r,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                textsize=text_size,
                textstyle=text_style,
            )
        elif node.shape_type == "decision":
            canvas_rhombus(
                xy=(cx, cy),
                width=w,
                height=h,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                textsize=text_size,
                textstyle=text_style,
            )
        elif node.shape_type in {"start", "end"}:
            # Stadium/pill shape
            radius = node.r if node.r > 0 else h / 2.0
            canvas_rectangle(
                xy=(cx, cy),
                width=w,
                height=h,
                r=radius,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                textsize=text_size,
                textstyle=text_style,
            )
        elif node.shape_type == "data":
            canvas_parallelogram(
                xy=(cx, cy),
                width=w,
                height=h,
                corner_angle=75.0,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                textsize=text_size,
                textstyle=text_style,
            )
        else:
            canvas_rectangle(
                xy=(cx, cy),
                width=w,
                height=h,
                r=node.r,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                textsize=text_size,
                textstyle=text_style,
            )
