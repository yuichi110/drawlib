# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for UML Class diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams._common import (
    is_edge_visible,
    render_diagram_background,
    render_diagram_title,
)
from drawlib._diagrams.class_diagram._render_node import render_class_node
from drawlib._diagrams.class_diagram._render_relationship import render_relationship

if TYPE_CHECKING:
    from drawlib._diagrams.class_diagram._class_node import ClassNode
    from drawlib._diagrams.class_diagram._diagram import ClassDiagram


def draw_class_diagram(diagram: ClassDiagram, base_xy: tuple[float, float]) -> None:
    """Render the complete class diagram at the given base canvas coordinate.

    Args:
        diagram: ClassDiagram container instance.
        base_xy: Base canvas coordinate (x, y) where the diagram is placed.
    """
    canvas_xy_map = _resolve_coordinates(diagram, base_xy)
    min_x, min_y, max_x, max_y = diagram.get_bounds()
    margin = diagram.margin
    c_min_x = base_xy[0] + min_x - margin
    c_max_x = base_xy[0] + max_x + margin
    c_min_y = base_xy[1] + min_y - margin
    c_max_y = base_xy[1] + max_y + margin

    diag_w = diagram.custom_width if diagram.custom_width is not None else (c_max_x - c_min_x)
    diag_h = diagram.custom_height if diagram.custom_height is not None else (c_max_y - c_min_y)
    center_x = (c_min_x + c_max_x) / 2.0
    center_y = (c_min_y + c_max_y) / 2.0

    # 1. Render Diagram Background if specified
    render_diagram_background(
        center_xy=(center_x, center_y),
        width=diag_w,
        height=diag_h,
        style=diagram.style,
    )

    # 2. Render Diagram Title if specified
    if diagram.title:
        title_y = max(c_max_y, center_y + diag_h / 2.0) + 2.0
        render_diagram_title(
            xy=(center_x, title_y),
            title=diagram.title,
            title_style=diagram.title_style,
            default_size=16.0,
            default_color=(30, 41, 59, 1.0),
            default_halign="center",
            default_valign="bottom",
        )

    # 3. Render Relationships (Edges, UML markers, labels)
    for rel in diagram.relationships:
        if not is_edge_visible(rel):
            continue
        render_relationship(rel, canvas_xy_map, diagram.edge_style, diagram.edge_text_style)

    # 4. Render Class Nodes (Cards, Header, Compartments)
    for c in diagram.classes:
        if not c.show:
            continue
        class_canvas_xy = canvas_xy_map[c]
        render_class_node(c, class_canvas_xy, diagram.node_style, diagram.header_style)


def _resolve_coordinates(
    diagram: ClassDiagram,
    base_xy: tuple[float, float],
) -> dict[ClassNode, tuple[float, float]]:
    """Resolve canvas coordinates for all classes in diagram.

    Args:
        diagram: ClassDiagram instance.
        base_xy: Placement base coordinate on canvas.

    Returns:
        Mapping of ClassNode to canvas center coordinate (cx, cy).
    """
    bx, by = base_xy
    return {c: (bx + c._local_xy[0], by + c._local_xy[1]) for c in diagram.classes}


# Backward compatibility aliases
_render_class_node = render_class_node
_render_relationship = render_relationship
