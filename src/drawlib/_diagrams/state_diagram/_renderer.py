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

import math
from typing import TYPE_CHECKING, Literal

from drawlib._core.colors import Colors
from drawlib._core.fonts import Font
from drawlib._core.lines import LineArcHelper
from drawlib._core.lines import line as canvas_line
from drawlib._core.lines import line_curved as canvas_line_curved
from drawlib._core.lines import lines as canvas_lines
from drawlib._core.lines import lines_bezier as canvas_lines_bezier
from drawlib._core.lines import lines_curved as canvas_lines_curved
from drawlib._core.shapes import circle as canvas_circle
from drawlib._core.shapes import ellipse as canvas_ellipse
from drawlib._core.shapes import rectangle as canvas_rectangle
from drawlib._core.shapes import rhombus as canvas_rhombus
from drawlib._core.text import text as canvas_text
from drawlib._core.types import Style
from drawlib._diagrams.state_diagram._state_node import (
    ChoiceState,
    FinalState,
    ForkJoinState,
    InitialState,
    State,
    StateNodeBase,
)
from drawlib._diagrams.state_diagram._types import Side

if TYPE_CHECKING:
    from drawlib._diagrams.state_diagram._diagram import StateDiagram
    from drawlib._diagrams.state_diagram._transition import StateTransition

# Default color palette (Slate)
_DEFAULT_BORDER_COLOR = (71, 85, 105, 1.0)  # Slate-600
_DEFAULT_FILL_COLOR = (248, 250, 252, 1.0)  # Slate-50
_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_MUTED_TEXT_COLOR = (100, 116, 139, 1.0)  # Slate-500
_DEFAULT_SOLID_COLOR = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_EDGE_COLOR = (71, 85, 105, 1.0)  # Slate-600


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
        title_style = Style(
            text_size=16,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_SOLID_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(center_x, title_y), text=diagram.title, style=title_style)

    # 3. Transitions
    for trans in diagram.transitions:
        _render_transition(trans, canvas_xy_map)

    # 4. State Nodes
    for node in diagram.states:
        node_canvas_xy = canvas_xy_map[node]
        _render_node(node, node_canvas_xy)


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


def _render_node(node: StateNodeBase, center_xy: tuple[float, float]) -> None:
    """Dispatch rendering for a state node or pseudo-state.

    Args:
        node: StateNodeBase instance to render.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    if isinstance(node, State):
        _render_state_node(node, center_xy)
    elif isinstance(node, InitialState):
        _render_initial_state(node, center_xy)
    elif isinstance(node, FinalState):
        _render_final_state(node, center_xy)
    elif isinstance(node, ChoiceState):
        _render_choice_state(node, center_xy)
    elif isinstance(node, ForkJoinState):
        _render_fork_join_state(node, center_xy)


def _render_state_node(node: State, center_xy: tuple[float, float]) -> None:
    """Render a State instance based on its shape type.

    Args:
        node: State instance.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    if node.shape == "box":
        _render_box_state(node, center_xy)
    elif node.shape == "oval":
        _render_oval_state(node, center_xy)
    elif node.shape == "circle":
        _render_circle_state(node, center_xy)
    elif node.shape == "double_circle":
        _render_double_circle_state(node, center_xy)
    elif node.shape == "text_only":
        _render_text_only_state(node, center_xy)


def _render_box_state(node: State, center_xy: tuple[float, float]) -> None:
    """Render a rounded box state node with optional actions.

    Args:
        node: State instance with shape='box'.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    w = node.effective_width
    h = node.effective_height

    base_style = Style(
        shape_fill_color=_DEFAULT_FILL_COLOR,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    style = base_style.patch(node.style)
    canvas_rectangle(xy=(cx, cy), width=w, height=h, r=node.r, style=style)

    if not node.actions:
        # Single central name label
        text_style = Style(
            text_size=11,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="center",
        )
        if node.style is not None:
            text_style = text_style.patch(node.style)
        canvas_text(xy=(cx, cy), text=node.name, style=text_style)
        return

    # Complex state with header and action compartments
    header_h = 4.5
    top_y = cy + h / 2.0
    header_cy = top_y - header_h / 2.0
    div_y = top_y - header_h

    # State name in header compartment
    name_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None:
        name_style = name_style.patch(node.style)
    canvas_text(xy=(cx, header_cy), text=node.name, style=name_style)

    # Divider line
    div_style = Style(
        line_color=style.shape_line_color if style.shape_line_color is not None else _DEFAULT_BORDER_COLOR,
        line_width=1.0,
    )
    canvas_line(xy1=(cx - w / 2.0, div_y), xy2=(cx + w / 2.0, div_y), style=div_style)

    # Internal actions list
    row_h = 2.8
    act_x = cx - w / 2.0 + 2.0
    action_style = Style(
        text_size=9,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_MUTED_TEXT_COLOR,
        text_halign="left",
        text_valign="center",
    )
    for i, action in enumerate(node.actions):
        act_y = div_y - 1.8 - i * row_h
        canvas_text(xy=(act_x, act_y), text=action.display_text, style=action_style)


def _render_oval_state(node: State, center_xy: tuple[float, float]) -> None:
    """Render an oval (capsule/ellipse) state node.

    Args:
        node: State instance with shape='oval'.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    w = node.effective_width
    h = node.effective_height

    base_style = Style(
        shape_fill_color=_DEFAULT_FILL_COLOR,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    style = base_style.patch(node.style)
    canvas_ellipse(xy=(cx, cy), width=w, height=h, style=style)

    text_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_circle_state(node: State, center_xy: tuple[float, float]) -> None:
    """Render a circle state node (transparent background by default).

    Args:
        node: State instance with shape='circle'.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    radius = node.effective_width / 2.0

    # Default background is transparent unless overridden by user style
    base_style = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    style = base_style.patch(node.style)
    canvas_circle(xy=(cx, cy), radius=radius, style=style)

    text_style = Style(
        text_size=10.5,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_double_circle_state(node: State, center_xy: tuple[float, float]) -> None:
    """Render a double circle state node (FSM accepting state).

    Args:
        node: State instance with shape='double_circle'.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    r_outer = node.effective_width / 2.0
    r_inner = max(r_outer - 1.2, 0.5)

    # Outer circle: transparent background by default unless overridden
    outer_base = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    outer_style = outer_base.patch(node.style)
    canvas_circle(xy=(cx, cy), radius=r_outer, style=outer_style)

    # Inner ring: transparent fill, border matches outer line color
    inner_line_color = (
        outer_style.shape_line_color if outer_style.shape_line_color is not None else _DEFAULT_BORDER_COLOR
    )
    inner_line_width = outer_style.shape_line_width if outer_style.shape_line_width is not None else 1.5
    inner_style = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=inner_line_color,
        shape_line_width=inner_line_width,
    )
    canvas_circle(xy=(cx, cy), radius=r_inner, style=inner_style)

    text_style = Style(
        text_size=10.0,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_text_only_state(node: State, center_xy: tuple[float, float]) -> None:
    """Render a text-only state node without border.

    Args:
        node: State instance with shape='text_only'.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    text_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_BOLD,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )
    if node.style is not None:
        text_style = text_style.patch(node.style)
    canvas_text(xy=(cx, cy), text=node.name, style=text_style)


def _render_initial_state(node: InitialState, center_xy: tuple[float, float]) -> None:
    """Render an InitialState pseudo-state (filled solid circle).

    Args:
        node: InitialState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    base_style = Style(
        shape_fill_color=_DEFAULT_SOLID_COLOR,
        shape_line_color=_DEFAULT_SOLID_COLOR,
        shape_line_width=1.0,
    )
    style = base_style.patch(node.style)
    canvas_circle(xy=(cx, cy), radius=node.radius, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_MUTED_TEXT_COLOR,
            text_halign="center",
            text_valign="top",
        )
        canvas_text(xy=(cx, cy - node.radius - 1.0), text=node.name, style=label_style)


def _render_final_state(node: FinalState, center_xy: tuple[float, float]) -> None:
    """Render a FinalState pseudo-state (bullseye circle).

    Args:
        node: FinalState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    r_outer = node.radius
    r_inner = r_outer * 0.65

    outer_base = Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=_DEFAULT_SOLID_COLOR,
        shape_line_width=1.5,
    )
    outer_style = outer_base.patch(node.style)
    canvas_circle(xy=(cx, cy), radius=r_outer, style=outer_style)

    inner_style = Style(
        shape_fill_color=_DEFAULT_SOLID_COLOR,
        shape_line_color=_DEFAULT_SOLID_COLOR,
        shape_line_width=1.0,
    )
    canvas_circle(xy=(cx, cy), radius=r_inner, style=inner_style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_MUTED_TEXT_COLOR,
            text_halign="center",
            text_valign="top",
        )
        canvas_text(xy=(cx, cy - r_outer - 1.0), text=node.name, style=label_style)


def _render_choice_state(node: ChoiceState, center_xy: tuple[float, float]) -> None:
    """Render a ChoiceState pseudo-state (diamond).

    Args:
        node: ChoiceState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    base_style = Style(
        shape_fill_color=_DEFAULT_FILL_COLOR,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    style = base_style.patch(node.style)
    canvas_rhombus(xy=(cx, cy), width=node.size, height=node.size, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_MUTED_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(cx, cy + node.size / 2.0 + 1.0), text=node.name, style=label_style)


def _render_fork_join_state(node: ForkJoinState, center_xy: tuple[float, float]) -> None:
    """Render a ForkJoinState pseudo-state (solid sync bar).

    Args:
        node: ForkJoinState instance.
        center_xy: Center coordinate (cx, cy) on canvas.
    """
    cx, cy = center_xy
    base_style = Style(
        shape_fill_color=_DEFAULT_SOLID_COLOR,
        shape_line_color=_DEFAULT_SOLID_COLOR,
        shape_line_width=1.0,
    )
    style = base_style.patch(node.style)
    canvas_rectangle(xy=(cx, cy), width=node.width, height=node.height, r=0.4, style=style)

    if node.name:
        label_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_MUTED_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(cx, cy + node.height / 2.0 + 1.0), text=node.name, style=label_style)


def _render_transition(
    trans: StateTransition,
    canvas_xy_map: dict[StateNodeBase, tuple[float, float]],
) -> None:
    """Render a transition edge.

    Args:
        trans: StateTransition instance.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
    """
    if trans.is_self_transition:
        _render_self_transition(trans, canvas_xy_map)
    else:
        _render_normal_transition(trans, canvas_xy_map)


_LOOP_SIDE_CONFIG: dict[
    str, tuple[float, float, float, Literal["left", "center", "right"], Literal["top", "center", "bottom"]]
] = {
    "top": (90.0, 0.0, 1.0, "center", "bottom"),
    "bottom": (270.0, 0.0, -1.0, "center", "top"),
    "right": (0.0, 1.0, 0.0, "left", "center"),
    "left": (180.0, -1.0, 0.0, "right", "center"),
    "top_right": (45.0, 1.0, 1.0, "left", "bottom"),
    "top_left": (135.0, -1.0, 1.0, "right", "bottom"),
    "bottom_right": (-45.0, 1.0, -1.0, "left", "top"),
    "bottom_left": (-135.0, -1.0, -1.0, "right", "top"),
}

_CORNER_MAP: dict[tuple[Side, Side], str] = {
    ("top", "right"): "top_right",
    ("right", "top"): "top_right",
    ("top", "left"): "top_left",
    ("left", "top"): "top_left",
    ("bottom", "right"): "bottom_right",
    ("right", "bottom"): "bottom_right",
    ("bottom", "left"): "bottom_left",
    ("left", "bottom"): "bottom_left",
}


def _resolve_self_loop_orientation(start_side: Side, end_side: Side) -> str:
    """Resolve self-transition loop orientation (corner name or side name)."""
    if (start_side, end_side) in _CORNER_MAP:
        return _CORNER_MAP[(start_side, end_side)]
    if start_side in {"top", "bottom", "left", "right", "top_right", "top_left", "bottom_right", "bottom_left"}:
        return start_side
    if end_side in {"top", "bottom", "left", "right", "top_right", "top_left", "bottom_right", "bottom_left"}:
        return end_side
    return "top_right"


def _compute_loop_geometry(
    node: StateNodeBase,
    center: tuple[float, float],
    side: str,
    w_l: float,
    h_l: float,
    ratio: float,
) -> tuple[
    tuple[float, float],
    float,
    tuple[float, float],
    Literal["left", "center", "right"],
    Literal["top", "center", "bottom"],
]:
    """Calculate loop center coordinate, center angle, and label position/alignment."""
    cx, cy = center
    hw = node.effective_width / 2.0
    hh = node.effective_height / 2.0

    gap_deg = (1.0 - ratio) * 360.0
    half_gap_rad = math.radians(gap_deg / 2.0)
    cos_gap = math.cos(half_gap_rad)

    cfg = _LOOP_SIDE_CONFIG.get(side, _LOOP_SIDE_CONFIG["top"])
    center_angle, dx_sign, dy_sign, halign, valign = cfg

    is_corner = side in {"top_right", "top_left", "bottom_right", "bottom_left"}
    if is_corner:
        is_curved = getattr(node, "shape", "box") in {"circle", "double_circle", "oval"}
        scale = 0.70710678 if is_curved else 1.0
        dist_x = (w_l / 2.0) * cos_gap * 0.70710678
        dist_y = (h_l / 2.0) * cos_gap * 0.70710678
        loop_cx = cx + dx_sign * (hw * scale + dist_x)
        loop_cy = cy + dy_sign * (hh * scale + dist_y)
        label_x = loop_cx + dx_sign * (w_l / 2.0 + 2.0) * 0.70710678
        label_y = loop_cy + dy_sign * (h_l / 2.0 + 2.0) * 0.70710678
    else:
        loop_cx = cx + dx_sign * (hw + (w_l / 2.0) * cos_gap)
        loop_cy = cy + dy_sign * (hh + (h_l / 2.0) * cos_gap)
        label_x = loop_cx + dx_sign * (w_l / 2.0 + 2.0)
        label_y = loop_cy + dy_sign * (h_l / 2.0 + 2.0)

    return (loop_cx, loop_cy), center_angle, (label_x, label_y), halign, valign


def _render_self_transition(
    trans: StateTransition,
    canvas_xy_map: dict[StateNodeBase, tuple[float, float]],
) -> None:
    """Render a self-transition loop curving along a side or corner using an ellipse arc.

    Args:
        trans: StateTransition instance where start is end or is_loop is True.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
    """
    node = trans.start
    center = canvas_xy_map[node]
    hw = node.effective_width / 2.0
    hh = node.effective_height / 2.0

    if trans.loop_width is not None and trans.loop_height is not None:
        w_l = trans.loop_width
        h_l = trans.loop_height
    elif trans.loop_width is not None:
        w_l = trans.loop_width
        h_l = trans.loop_width
    elif trans.loop_height is not None:
        w_l = trans.loop_height
        h_l = trans.loop_height
    else:
        base = max(8.0, min(hw, hh) * 0.9)
        w_l = base
        h_l = base

    ratio = trans.loop_ratio if 0.5 <= trans.loop_ratio <= 0.98 else 0.88
    side = trans.loop_side if trans.is_loop else _resolve_self_loop_orientation(trans.start_side, trans.end_side)

    loop_xy, center_angle, label_pos, text_halign, text_valign = _compute_loop_geometry(
        node=node,
        center=center,
        side=side,
        w_l=w_l,
        h_l=h_l,
        ratio=ratio,
    )

    base_style = Style(line_color=_DEFAULT_EDGE_COLOR, line_width=1.5)
    edge_style = base_style.patch(trans.style)

    gap_deg = (1.0 - ratio) * 360.0
    base_angle = center_angle - 180.0
    a_start = base_angle + gap_deg / 2.0
    a_end = base_angle + 360.0 - gap_deg / 2.0

    pts = LineArcHelper.get_ellipse_path_points(loop_xy, w_l, h_l, a_start, a_end)
    canvas_lines_bezier(pts[0], path_points=pts[1:], arrowhead="->", style=edge_style)  # type: ignore

    label = trans.effective_label
    if label:
        label_style = Style(
            text_size=8.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign=text_halign,
            text_valign=text_valign,
        )
        canvas_text(xy=label_pos, text=label, style=label_style)


def _render_normal_transition(
    trans: StateTransition,
    canvas_xy_map: dict[StateNodeBase, tuple[float, float]],
) -> None:
    """Render a transition between two distinct states.

    Args:
        trans: StateTransition instance.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
    """
    start_c = canvas_xy_map[trans.start]
    end_c = canvas_xy_map[trans.end]

    pad_start = trans.padding if isinstance(trans.padding, (int, float)) else trans.padding[0]
    pad_end = trans.padding if isinstance(trans.padding, (int, float)) else trans.padding[1]

    xy1 = _get_node_border_point(trans.start, start_c, end_c, trans.start_side, pad_start)
    xy2 = _get_node_border_point(trans.end, end_c, start_c, trans.end_side, pad_end)

    base_style = Style(line_color=_DEFAULT_EDGE_COLOR, line_width=1.5)
    edge_style = base_style.patch(trans.style)

    if trans.routing == "orthogonal":
        _render_orthogonal_transition(xy1, xy2, trans, edge_style)
    else:
        _render_curved_or_direct_transition(xy1, xy2, trans, edge_style)


def _render_orthogonal_transition(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    trans: StateTransition,
    edge_style: Style,
) -> None:
    """Render orthogonal (stepped) transition line.

    Args:
        xy1: Start point on boundary.
        xy2: End point on boundary.
        trans: StateTransition instance.
        edge_style: Edge style.
    """
    mid_x = (xy1[0] + xy2[0]) / 2.0
    p1 = (mid_x, xy1[1])
    p2 = (mid_x, xy2[1])

    canvas_lines(xys=[xy1, p1, p2, xy2], arrowhead="->", style=edge_style)

    label = trans.effective_label
    if label:
        label_style = Style(
            text_size=8.5,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=_DEFAULT_TEXT_COLOR,
            text_halign="center",
            text_valign="bottom",
        )
        mid_y = (xy1[1] + xy2[1]) / 2.0
        canvas_text(xy=(mid_x, mid_y + 1.2), text=label, style=label_style)


def _render_curved_or_direct_transition(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    trans: StateTransition,
    edge_style: Style,
) -> None:
    """Render curved or straight direct transition line.

    Args:
        xy1: Start point on boundary.
        xy2: End point on boundary.
        trans: StateTransition instance.
        edge_style: Edge style.
    """
    bend = trans.bend
    if bend != 0.0:
        canvas_line_curved(xy1=xy1, xy2=xy2, bend=bend, arrowhead="->", style=edge_style)
    else:
        canvas_line(xy1=xy1, xy2=xy2, arrowhead="->", style=edge_style)

    label = trans.effective_label
    if not label:
        return

    label_style = Style(
        text_size=8.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_halign="center",
        text_valign="center",
    )

    # Compute label offset along normal vector
    dx = xy2[0] - xy1[0]
    dy = xy2[1] - xy1[1]
    dist = math.hypot(dx, dy)
    if dist < 1e-6:
        canvas_text(xy=xy1, text=label, style=label_style)
        return

    mid_x = (xy1[0] + xy2[0]) / 2.0
    mid_y = (xy1[1] + xy2[1]) / 2.0
    norm_x = -dy / dist
    norm_y = dx / dist

    sign = 1.0 if bend >= 0 else -1.0
    disp = dist * bend * 0.25 + sign * 2.2
    label_x = mid_x + norm_x * disp
    label_y = mid_y + norm_y * disp

    canvas_text(xy=(label_x, label_y), text=label, style=label_style)


def _get_node_border_point(
    node: StateNodeBase,
    center: tuple[float, float],
    target_xy: tuple[float, float],
    side: Side,
    padding: float = 0.0,
) -> tuple[float, float]:
    """Calculate the precise intersection coordinate on the node boundary.

    Args:
        node: StateNodeBase instance.
        center: Node center coordinate (cx, cy).
        target_xy: Target coordinate (x, y) towards which edge points.
        side: Attachment side ('left', 'right', 'top', 'bottom', 'auto').
        padding: Boundary clearance offset.

    Returns:
        Intersection coordinate (x, y) on the node border.
    """
    cx, cy = center
    hw = node.effective_width / 2.0 + padding
    hh = node.effective_height / 2.0 + padding

    explicit_point = _get_explicit_side_point(center, hw, hh, side)
    if explicit_point is not None:
        return explicit_point

    return _get_auto_border_point(node, center, target_xy, hw, hh)


def _get_explicit_side_point(
    center: tuple[float, float],
    hw: float,
    hh: float,
    side: Side,
) -> tuple[float, float] | None:
    """Calculate boundary coordinate for explicitly requested side.

    Args:
        center: Node center coordinate (cx, cy).
        hw: Half width of node.
        hh: Half height of node.
        side: Side name.

    Returns:
        Coordinate tuple if side is explicit, else None.
    """
    cx, cy = center
    if side == "top":
        return (cx, cy + hh)
    if side == "bottom":
        return (cx, cy - hh)
    if side == "left":
        return (cx - hw, cy)
    if side == "right":
        return (cx + hw, cy)
    return None


def _get_auto_border_point(
    node: StateNodeBase,
    center: tuple[float, float],
    target_xy: tuple[float, float],
    hw: float,
    hh: float,
) -> tuple[float, float]:
    """Calculate automatic raycast intersection coordinate on node boundary.

    Args:
        node: StateNodeBase instance.
        center: Node center coordinate (cx, cy).
        target_xy: Target coordinate (x, y).
        hw: Half width of node.
        hh: Half height of node.

    Returns:
        Intersection coordinate on node boundary.
    """
    cx, cy = center
    dx = target_xy[0] - cx
    dy = target_xy[1] - cy

    if isinstance(node, (InitialState, FinalState)) or (
        isinstance(node, State) and node.shape in {"circle", "double_circle"}
    ):
        return _intersect_circle(cx, cy, hw, dx, dy)

    if isinstance(node, State) and node.shape == "oval":
        return _intersect_ellipse(cx, cy, hw, hh, dx, dy)

    if isinstance(node, ChoiceState):
        return _intersect_diamond(cx, cy, hw, hh, dx, dy)

    return _intersect_box(cx, cy, hw, hh, dx, dy)


def _intersect_circle(
    cx: float,
    cy: float,
    radius: float,
    dx: float,
    dy: float,
) -> tuple[float, float]:
    """Calculate raycast intersection on circle perimeter."""
    dist = math.hypot(dx, dy)
    if dist < 1e-6:
        return (cx, cy)
    return (cx + (dx / dist) * radius, cy + (dy / dist) * radius)


def _intersect_ellipse(
    cx: float,
    cy: float,
    a: float,
    b: float,
    dx: float,
    dy: float,
) -> tuple[float, float]:
    """Calculate raycast intersection on ellipse boundary."""
    denom = math.hypot(dx / a, dy / b)
    if denom < 1e-6:
        return (cx, cy)
    t = 1.0 / denom
    return (cx + dx * t, cy + dy * t)


def _intersect_diamond(
    cx: float,
    cy: float,
    a: float,
    b: float,
    dx: float,
    dy: float,
) -> tuple[float, float]:
    """Calculate raycast intersection on rhombus boundary."""
    denom = abs(dx) / a + abs(dy) / b
    if denom < 1e-6:
        return (cx, cy)
    t = 1.0 / denom
    return (cx + dx * t, cy + dy * t)


def _intersect_box(
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    dx: float,
    dy: float,
) -> tuple[float, float]:
    """Calculate raycast intersection on rectangle boundary."""
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return (cx, cy)
    scale_x = hw / abs(dx) if abs(dx) > 1e-6 else float("inf")
    scale_y = hh / abs(dy) if abs(dy) > 1e-6 else float("inf")
    scale = min(scale_x, scale_y)
    return (cx + dx * scale, cy + dy * scale)
