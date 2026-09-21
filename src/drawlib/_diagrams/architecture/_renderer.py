# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for architecture diagrams."""

from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PIL.Image import Image

import drawlib._icons.font_icons.phosphor._generated as phosphor_gen
import drawlib._icons.png_icons.gcp._generated as gcp_gen
from drawlib._core.l2_models import Dimage
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._diagrams.architecture._group import NodeGroup
from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
from drawlib._diagrams.architecture._junction import Junction
from drawlib._diagrams.architecture._node import Node
from drawlib._diagrams.architecture._types import Connectable, DiagramItem, IconType, PaddingType
from drawlib.images import image as canvas_image
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram
    from drawlib._diagrams.architecture._edge import Edge


def _resolve_coordinates(
    diagram: ArchitectureDiagram,
    base_xy: tuple[float, float],
) -> tuple[dict[Connectable, tuple[float, float]], list[NodeGroup], list[Node], list[Junction]]:
    """Resolve hierarchical coordinates for all items in the diagram.

    Args:
        diagram: ArchitectureDiagram container instance.
        base_xy: (x, y) placement on the canvas.

    Returns:
        Tuple of (item_to_canvas_xy, list_of_groups, list_of_nodes, list_of_junctions).
    """
    canvas_xy_map: dict[Connectable, tuple[float, float]] = {}
    all_groups: list[NodeGroup] = []
    all_nodes: list[Node] = []
    all_junctions: list[Junction] = []

    def traverse(item: DiagramItem, parent_canvas_xy: tuple[float, float]) -> None:
        px, py = parent_canvas_xy
        ix, iy = item._local_xy
        item_canvas_xy = (px + ix, py + iy)
        canvas_xy_map[item] = item_canvas_xy

        if isinstance(item, NodeGroup):
            all_groups.append(item)
            for child, _ in item._items:
                traverse(child, item_canvas_xy)
        elif isinstance(item, Node):
            all_nodes.append(item)
        elif isinstance(item, Junction):
            all_junctions.append(item)

    for top_item, _ in diagram._items:
        traverse(top_item, base_xy)

    return canvas_xy_map, all_groups, all_nodes, all_junctions


def _get_item_anchors(
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


def _resolve_connection_endpoints(
    start: Connectable,
    end: Connectable,
    start_canvas_xy: tuple[float, float],
    end_canvas_xy: tuple[float, float],
) -> tuple[tuple[float, float], tuple[float, float], str]:
    """Determine the optimal anchor pair and primary axis orientation."""
    start_anchors = _get_item_anchors(start, start_canvas_xy)
    end_anchors = _get_item_anchors(end, end_canvas_xy)

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


def _draw_enum_icon(
    icon: GcpIcon | PhosphorIcon,
    canvas_xy: tuple[float, float],
    icon_size: float,
    style: Style,
) -> None:
    """Draw a GCP or Phosphor icon from generated function modules."""
    if isinstance(icon, GcpIcon):
        func = getattr(gcp_gen, icon.value, None)
    else:
        func = getattr(phosphor_gen, icon.value, None)
    if func:
        func(xy=canvas_xy, width=icon_size, style=style)


def _draw_image_icon(
    icon: CustomIcon | Dimage | Image | str | Path,
    canvas_xy: tuple[float, float],
    icon_size: float,
    style: Style,
) -> None:
    """Draw a raster image icon (CustomIcon, Dimage, PIL Image, or path)."""
    if isinstance(icon, CustomIcon):
        img = icon.dimage
    elif isinstance(icon, Image):
        img = Dimage(icon)
    elif isinstance(icon, Dimage):
        img = icon
    else:
        img = str(icon)
    canvas_image(xy=canvas_xy, width=icon_size, image=img, style=style)


def _draw_icon(
    icon: IconType,
    canvas_xy: tuple[float, float],
    icon_size: float,
    icon_style: Style | None,
) -> None:
    """Draw an icon at canvas_xy with size icon_size."""
    if icon is None:
        return

    applied_style = icon_style if icon_style is not None else Style(line_width=0)

    if isinstance(icon, (GcpIcon, PhosphorIcon)):
        _draw_enum_icon(icon, canvas_xy, icon_size, applied_style)
    elif isinstance(icon, (CustomIcon, Dimage, Image, str, Path)):
        _draw_image_icon(icon, canvas_xy, icon_size, applied_style)
    elif callable(icon):
        icon(xy=canvas_xy, width=icon_size, style=applied_style)


def _compute_edge_points(
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
    """Shorten the start and end of an edge path by padding distance.

    Args:
        pts: List of (x, y) coordinates along the edge polyline.
        padding: Padding value (single float or (start_pad, end_pad) tuple).

    Returns:
        New list of (x, y) coordinates with padding applied to endpoints.
    """
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


def _draw_single_edge(
    edge: Edge,
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
    default_edge_style: Style,
) -> None:
    """Draw a single edge and its label."""
    if edge.start not in canvas_xy_map or edge.end not in canvas_xy_map:
        return

    start_canvas_xy = canvas_xy_map[edge.start]
    end_canvas_xy = canvas_xy_map[edge.end]

    start_pt, end_pt, orientation = _resolve_connection_endpoints(edge.start, edge.end, start_canvas_xy, end_canvas_xy)
    applied_style = default_edge_style.merge(edge.style) if edge.style else default_edge_style
    pts = _compute_edge_points(start_pt, end_pt, orientation, edge.waypoints, edge.routing, base_xy)
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

    if not edge.label:
        return

    mid_idx = len(pts) // 2
    lx = (pts[mid_idx - 1][0] + pts[mid_idx][0]) / 2.0
    ly = (pts[mid_idx - 1][1] + pts[mid_idx][1]) / 2.0

    label_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=(50, 50, 50, 1.0),
        text_bg_fill_color=(255, 255, 255, 0.9),
        text_bg_line_color=None,
        text_bg_line_width=0,
        text_halign="center",
        text_valign="center",
    )
    if edge.textstyle:
        label_style = label_style.merge(edge.textstyle)

    canvas_text(xy=(lx, ly), text=edge.label, style=label_style)


def _draw_edges(
    edges: list[Edge],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    base_xy: tuple[float, float],
) -> None:
    """Draw all connections in Layer 1."""
    default_edge_style = Style(
        line_color=(70, 70, 70, 1.0),
        line_width=1.5,
        line_style="solid",
    )
    for edge in edges:
        _draw_single_edge(edge, canvas_xy_map, base_xy, default_edge_style)


def _render_groups(
    groups: list[NodeGroup],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
) -> None:
    """Draw Layer 0: Groups (background boxes and titles)."""
    default_group_style = Style(
        line_style="dashed",
        line_width=1.0,
        line_color=(160, 160, 165, 1.0),
        fill_color=(245, 246, 250, 0.6),
    )

    for group in groups:
        gx, gy = canvas_xy_map[group]
        min_x, min_y, max_x, max_y = group.get_bounds()
        w = max_x - min_x
        h = max_y - min_y
        box_cx = gx + (min_x + max_x) / 2.0
        box_cy = gy + (min_y + max_y) / 2.0

        applied_style = default_group_style.merge(group.style) if group.style else default_group_style
        canvas_rectangle(xy=(box_cx, box_cy), width=w, height=h, style=applied_style)

        if group.title:
            title_style = Style(
                text_size=12,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(80, 80, 85, 1.0),
                text_halign="left",
                text_valign="top",
            )
            if group.textstyle:
                title_style = title_style.merge(group.textstyle)

            tx = gx + min_x + 2.5
            ty = gy + max_y - 2.0
            canvas_text(xy=(tx, ty), text=group.title, style=title_style)


def _render_node_label(node: Node, nx: float, ny: float) -> None:
    """Render label text for a node."""
    if not node.text:
        return

    pos = node.text_position
    margin = node.text_margin
    half_size = node.icon_size / 2.0

    halign: Literal["left", "center", "right"]
    valign: Literal["top", "center", "bottom"]

    if pos == "top":
        tx = nx
        ty = ny + half_size + margin
        halign = "center"
        valign = "bottom"
    elif pos == "left":
        tx = nx - half_size - margin
        ty = ny
        halign = "right"
        valign = "center"
    elif pos == "right":
        tx = nx + half_size + margin
        ty = ny
        halign = "left"
        valign = "center"
    else:
        # "bottom"
        tx = nx
        ty = ny - half_size - margin
        halign = "center"
        valign = "top"

    font_size = node.text_size if node.text_size is not None else 13
    text_style = Style(
        text_size=font_size,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=(30, 30, 30, 1.0),
        text_halign=halign,
        text_valign=valign,
        text_angle=node.text_angle,
    )
    if node.textstyle:
        text_style = text_style.merge(node.textstyle)

    canvas_text(xy=(tx, ty), text=node.text, style=text_style)


def _render_nodes(
    nodes: list[Node],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
) -> None:
    """Draw Layer 2: Nodes (cards, icons, labels)."""
    for node in nodes:
        nx, ny = canvas_xy_map[node]
        if node.style:
            min_x, min_y, max_x, max_y = node.get_bounds()
            nw = max_x - min_x
            nh = max_y - min_y
            cx = nx + (min_x + max_x) / 2.0
            cy = ny + (min_y + max_y) / 2.0
            canvas_rectangle(xy=(cx, cy), width=nw, height=nh, style=node.style)

        _draw_icon(node.icon, (nx, ny), node.icon_size, node.icon_style)
        _render_node_label(node, nx, ny)


def draw_diagram(diagram: ArchitectureDiagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Execute complete 2-pass drawing pipeline for an architecture diagram."""
    base_xy = (float(xy[0]), float(xy[1]))
    canvas_xy_map, all_groups, all_nodes, _ = _resolve_coordinates(diagram, base_xy)

    if diagram.style:
        dw, dh = diagram.get_size()
        canvas_rectangle(
            xy=(base_xy[0] + dw / 2.0, base_xy[1] + dh / 2.0),
            width=dw,
            height=dh,
            style=diagram.style,
        )

    _render_groups(all_groups, canvas_xy_map)
    _draw_edges(diagram._edges, canvas_xy_map, base_xy)
    _render_nodes(all_nodes, canvas_xy_map)

    if diagram.title:
        _, dh = diagram.get_size()
        title_style = Style(
            text_size=15,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(40, 40, 45, 1.0),
            text_halign="left",
            text_valign="bottom",
        )
        canvas_text(xy=(base_xy[0] + 1.0, base_xy[1] + dh + 2.0), text=diagram.title, style=title_style)
