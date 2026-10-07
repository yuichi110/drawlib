# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for UML and FSM State diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.state._render_node import render_node
from drawlib._diagrams.state._render_transition import render_transition
from drawlib._diagrams.state._state_node import StateNodeBase
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from drawlib._diagrams.state._diagram import StateDiagram


def draw_state_diagram(diagram: StateDiagram, base_xy: tuple[float, float]) -> None:
    """Render the complete state diagram at the given base canvas coordinate.

    Args:
        diagram: StateDiagram container instance.
        base_xy: Base canvas coordinate (x, y) where the diagram is anchored.
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

    # 1. Background
    if diagram.style is not None:
        bg_style = Style(
            shape_fill_color=Colors.White,
            shape_line_color=Colors.Transparent,
            shape_line_width=0.0,
        ).patch(diagram.style)
        canvas_rectangle(xy=(center_x, center_y), width=diag_w, height=diag_h, style=bg_style)

    # 2. Title
    if diagram.title:
        title_y = max(c_max_y, center_y + diag_h / 2.0) + 2.0
        base_title_style = Style(
            text_size=16,
            text_font=Font.SANSSERIF_BOLD,
            text_color=diagram.edge_text_style.text_color or (30, 41, 59, 1.0),
            text_halign="center",
            text_valign="bottom",
        )
        applied_title_style = (
            base_title_style.patch(diagram.title_style)
            if diagram.title_style is not None
            else base_title_style
        )
        canvas_text(xy=(center_x, title_y), text=diagram.title, style=applied_title_style)

    # 3. Transitions
    for trans in diagram.transitions:
        if not trans.show:
            continue
        if (trans.start is not None and not trans.start.show) or (trans.end is not None and not trans.end.show):
            continue
        render_transition(trans, canvas_xy_map, diagram.edge_style, diagram.edge_text_style)

    # 4. State Nodes
    for node in diagram.states:
        if not node.show:
            continue
        node_canvas_xy = canvas_xy_map[node]
        render_node(node, node_canvas_xy, diagram.node_style)


def _resolve_coordinates(
    diagram: StateDiagram,
    base_xy: tuple[float, float],
) -> dict[StateNodeBase, tuple[float, float]]:
    """Map all state nodes to canvas coordinates.

    Args:
        diagram: StateDiagram instance.
        base_xy: Placement base coordinate on canvas.

    Returns:
        Mapping of StateNodeBase to absolute canvas center coordinate (cx, cy).
    """
    xy_map: dict[StateNodeBase, tuple[float, float]] = {}
    for node in diagram.states:
        xy_map[node] = (base_xy[0] + node._local_xy[0], base_xy[1] + node._local_xy[1])
    return xy_map


# Re-exports for internal compatibility
_render_node = render_node
_render_transition = render_transition
