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

from typing import TYPE_CHECKING

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams._common import (
    draw_diagram_icon,
    render_diagram_background,
    render_diagram_title,
    render_icon_text_card,
)
from drawlib._diagrams._common import (
    draw_enum_icon as _common_draw_enum_icon,
)
from drawlib._diagrams._common import (
    draw_image_icon as _common_draw_image_icon,
)
from drawlib._diagrams.architecture._group import NodeGroup
from drawlib._diagrams.architecture._junction import Junction
from drawlib._diagrams.architecture._node import Node
from drawlib._diagrams.architecture._render_edges import (
    apply_edge_padding,
    draw_edges,
    draw_single_edge,
    get_item_anchors,
    resolve_connection_endpoints,
)
from drawlib._diagrams.architecture._types import Connectable, DiagramItem, IconType

if TYPE_CHECKING:
    from drawlib._diagrams.architecture._diagram import ArchitectureDiagram


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


def _draw_icon(
    icon: IconType,
    canvas_xy: tuple[float, float],
    icon_size: float,
    icon_style: Style | None,
) -> None:
    """Draw an icon at canvas_xy with size icon_size."""
    draw_diagram_icon(icon, canvas_xy, icon_size, icon_style, fallback_box=False)


def _render_groups(
    groups: list[NodeGroup],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
) -> None:
    """Draw Layer 0: Groups (background boxes and titles)."""
    default_group_style = Style(
        shape_line_style="dashed",
        shape_line_width=1.0,
        shape_line_color=(160, 160, 165, 1.0),
        shape_fill_color=(245, 246, 250, 0.6),
    )

    for group in groups:
        if not group.show:
            continue
        gx, gy = canvas_xy_map[group]
        min_x, min_y, max_x, max_y = group.get_bounds()
        w = max_x - min_x
        h = max_y - min_y
        box_cx = gx + (min_x + max_x) / 2.0
        box_cy = gy + (min_y + max_y) / 2.0

        applied_style = default_group_style.patch(group.style)
        canvas_rectangle(xy=(box_cx, box_cy), width=w, height=h, style=applied_style)

        if group.title:
            title_style = Style(
                text_size=12,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(80, 80, 85, 1.0),
                halign="left",
                valign="top",
            )
            if group.text_style:
                title_style = title_style.patch(group.text_style)

            tx = gx + min_x + 2.5
            ty = gy + max_y - 2.0
            canvas_text(xy=(tx, ty), text=group.title, style=title_style)


def _render_nodes(
    nodes: list[Node],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    default_node_style: Style,
    default_node_text_style: Style,
    default_node_card_style: Style | None = None,
) -> None:
    """Draw Layer 2: Nodes (cards, icons, labels)."""
    for node in nodes:
        if not node.show:
            continue
        nx, ny = canvas_xy_map[node]
        render_icon_text_card(
            canvas_xy=(nx, ny),
            width=node.width,
            height=node.height,
            text=node.text,
            icon=node.icon,
            icon_size=node.icon_size,
            style=node.style,
            text_style=node.text_style,
            card_style=node.card_style,
            default_node_style=default_node_style,
            default_node_text_style=default_node_text_style,
            default_node_card_style=default_node_card_style,
            fallback_box=False,
        )


def draw_diagram(diagram: ArchitectureDiagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Execute complete 2-pass drawing pipeline for an architecture diagram.

    Args:
        diagram: ArchitectureDiagram container instance.
        xy: Placement anchor coordinate (x, y). Defaults to (0.0, 0.0).
    """
    base_xy = (float(xy[0]), float(xy[1]))
    canvas_xy_map, all_groups, all_nodes, _ = _resolve_coordinates(diagram, base_xy)

    if diagram.style is not None:
        dw, dh = diagram.get_size()
        render_diagram_background(
            center_xy=(base_xy[0] + dw / 2.0, base_xy[1] + dh / 2.0),
            width=dw,
            height=dh,
            style=diagram.style,
        )

    _render_groups(all_groups, canvas_xy_map)
    draw_edges(diagram._edges, canvas_xy_map, base_xy, diagram.edge_style, diagram.edge_text_style)
    _render_nodes(
        all_nodes,
        canvas_xy_map,
        diagram.node_style,
        diagram.node_text_style,
        diagram.node_card_style,
    )

    if diagram.title:
        _, dh = diagram.get_size()
        render_diagram_title(
            xy=(base_xy[0] + 1.0, base_xy[1] + dh + 2.0),
            title=diagram.title,
            title_style=diagram.title_style,
            default_size=15.0,
            default_color=(40, 40, 45, 1.0),
            default_halign="left",
            default_valign="bottom",
        )


# Re-exports for test compatibility
_draw_enum_icon = _common_draw_enum_icon
_draw_image_icon = _common_draw_image_icon
_apply_edge_padding = apply_edge_padding
_draw_edges = draw_edges
_draw_single_edge = draw_single_edge
_get_item_anchors = get_item_anchors
_resolve_connection_endpoints = resolve_connection_endpoints
