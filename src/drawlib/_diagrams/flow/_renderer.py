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

from typing import TYPE_CHECKING

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import parallelogram as canvas_parallelogram
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import rhombus as canvas_rhombus
from drawlib._diagrams._common import render_diagram_background, render_diagram_title
from drawlib._diagrams.flow._junction import Junction
from drawlib._diagrams.flow._node import FlowNode
from drawlib._diagrams.flow._render_edges import render_edges
from drawlib._diagrams.flow._render_lanes import render_lanes
from drawlib._diagrams.flow._types import Connectable

if TYPE_CHECKING:
    from drawlib._diagrams.flow._diagram import FlowDiagram


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
    render_diagram_background(
        center_xy=(bx + dw / 2.0, by + dh / 2.0),
        width=dw,
        height=dh,
        style=diagram.style,
    )

    # Layer 1: Swimlanes
    if diagram.lanes:
        render_lanes(diagram.lanes, diagram.lane_orientation, base_xy, dw, dh)

    # Layer 2: Flow Edges
    render_edges(diagram.edges, canvas_xy_map, base_xy, diagram.edge_style, diagram.edge_text_style)

    # Layer 3: Flow Nodes & Junctions
    _render_nodes(all_nodes, canvas_xy_map, diagram.node_style)

    # Layer 4: Title
    render_diagram_title(
        xy=(bx + dw / 2.0, by + dh + 2.0),
        title=diagram.title,
        title_style=diagram.title_style,
        default_size=16.0,
        default_color=(30, 41, 59, 1.0),
        default_halign="center",
        default_valign="bottom",
    )


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


def _render_nodes(
    nodes: list[FlowNode],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    default_node_style: Style,
) -> None:
    """Render all FlowNodes."""
    for node in nodes:
        if not node.show:
            continue
        cx, cy = canvas_xy_map[node]
        w, h = node.width, node.height

        applied_style = default_node_style.patch(node.style) if node.style is not None else default_node_style

        text_size = 12.0
        if node.text_style and node.text_style.text_size is not None:
            text_size = float(node.text_style.text_size)
        elif applied_style.text_size is not None:
            text_size = float(applied_style.text_size)

        text_color = applied_style.text_color or (30, 41, 59, 1.0)
        text_style = Style(
            text_size=text_size,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=text_color,
            text_halign="center",
            text_valign="center",
        )
        if node.text_style:
            text_style = text_style.patch(node.text_style)

        if node.shape_type == "process":
            canvas_rectangle(
                xy=(cx, cy),
                width=w,
                height=h,
                r=node.r,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                text_style=text_style,
            )
        elif node.shape_type == "decision":
            canvas_rhombus(
                xy=(cx, cy),
                width=w,
                height=h,
                angle=node.angle,
                style=applied_style,
                text=node.text,
                text_style=text_style,
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
                text_style=text_style,
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
                text_style=text_style,
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
                text_style=text_style,
            )


# Backward compatibility aliases
_render_lanes = render_lanes
_render_edges = render_edges
