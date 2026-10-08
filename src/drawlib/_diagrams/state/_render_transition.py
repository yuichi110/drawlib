# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""State transition rendering and routing functions for StateDiagram."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import LineArcHelper
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import line_curved as canvas_line_curved
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import lines_bezier as canvas_lines_bezier
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.state._state_node import (
    ChoiceState,
    FinalState,
    InitialState,
    State,
    StateNodeBase,
)
from drawlib._diagrams.state._types import Side

if TYPE_CHECKING:
    from drawlib._diagrams.state._transition import StateTransition


def render_transition(
    trans: StateTransition,
    canvas_xy_map: dict[StateNodeBase, tuple[float, float]],
    default_edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render a transition edge.

    Args:
        trans: StateTransition instance.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
        default_edge_style: Base Style for transition edges.
        default_edge_text_style: Base Style for transition labels.
    """
    edge_style = default_edge_style.patch(trans.style) if trans.style is not None else default_edge_style
    if trans.is_self_transition:
        _render_self_transition(trans, canvas_xy_map, edge_style, default_edge_text_style)
    else:
        _render_normal_transition(trans, canvas_xy_map, edge_style, default_edge_text_style)


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
    edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render a self-transition loop curving along a side or corner using an ellipse arc.

    Args:
        trans: StateTransition instance where start is end or is_loop is True.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
        edge_style: Style for the transition edge.
        default_edge_text_style: Base Style for transition labels.
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

    loop_xy, center_angle, label_pos, halign, valign = _compute_loop_geometry(
        node=node,
        center=center,
        side=side,
        w_l=w_l,
        h_l=h_l,
        ratio=ratio,
    )

    gap_deg = (1.0 - ratio) * 360.0
    base_angle = center_angle - 180.0
    a_start = base_angle + gap_deg / 2.0
    a_end = base_angle + 360.0 - gap_deg / 2.0

    pts = LineArcHelper.get_ellipse_path_points(loop_xy, w_l, h_l, a_start, a_end)
    canvas_lines_bezier(pts[0], path_points=pts[1:], arrow_head="->", style=edge_style)  # type: ignore

    label = trans.effective_label
    if label:
        applied_text_style = trans.text_style or default_edge_text_style
        label_style = (
            Style(
                text_size=8.5,
                text_font=Font.SANSSERIF_REGULAR,
            )
            .patch(applied_text_style)
            .patch(
                halign=(
                    trans.text_style.halign
                    if trans.text_style and trans.text_style.halign is not None
                    else halign
                ),
                valign=(
                    trans.text_style.valign
                    if trans.text_style and trans.text_style.valign is not None
                    else valign
                ),
            )
        )
        canvas_text(xy=label_pos, text=label, style=label_style)


def _render_normal_transition(
    trans: StateTransition,
    canvas_xy_map: dict[StateNodeBase, tuple[float, float]],
    edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render a transition between two distinct states.

    Args:
        trans: StateTransition instance.
        canvas_xy_map: Mapping of state nodes to canvas coordinates.
        edge_style: Style for the transition edge.
        default_edge_text_style: Base Style for transition labels.
    """
    start_c = canvas_xy_map[trans.start]
    end_c = canvas_xy_map[trans.end]

    pad_start = trans.padding if isinstance(trans.padding, (int, float)) else trans.padding[0]
    pad_end = trans.padding if isinstance(trans.padding, (int, float)) else trans.padding[1]

    xy1 = _get_node_border_point(trans.start, start_c, end_c, trans.start_side, pad_start)
    xy2 = _get_node_border_point(trans.end, end_c, start_c, trans.end_side, pad_end)

    if trans.routing == "orthogonal":
        _render_orthogonal_transition(xy1, xy2, trans, edge_style, default_edge_text_style)
    else:
        _render_curved_or_direct_transition(xy1, xy2, trans, edge_style, default_edge_text_style)


def _render_orthogonal_transition(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    trans: StateTransition,
    edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render orthogonal (stepped) transition line.

    Args:
        xy1: Start point on boundary.
        xy2: End point on boundary.
        trans: StateTransition instance.
        edge_style: Edge style.
        default_edge_text_style: Base Style for transition labels.
    """
    mid_x = (xy1[0] + xy2[0]) / 2.0
    p1 = (mid_x, xy1[1])
    p2 = (mid_x, xy2[1])

    canvas_lines(xys=[xy1, p1, p2, xy2], arrow_head="->", style=edge_style)

    label = trans.effective_label
    if label:
        applied_text_style = trans.text_style or default_edge_text_style
        label_style = (
            Style(
                text_size=8.5,
                text_font=Font.SANSSERIF_REGULAR,
            )
            .patch(applied_text_style)
            .patch(
                halign=(
                    trans.text_style.halign
                    if trans.text_style and trans.text_style.halign is not None
                    else "center"
                ),
                valign=(
                    trans.text_style.valign
                    if trans.text_style and trans.text_style.valign is not None
                    else "bottom"
                ),
            )
        )
        mid_y = (xy1[1] + xy2[1]) / 2.0
        canvas_text(xy=(mid_x, mid_y + 1.2), text=label, style=label_style)


def _render_curved_or_direct_transition(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    trans: StateTransition,
    edge_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Render curved or straight direct transition line.

    Args:
        xy1: Start point on boundary.
        xy2: End point on boundary.
        trans: StateTransition instance.
        edge_style: Edge style.
        default_edge_text_style: Base Style for transition labels.
    """
    bend = trans.bend
    if bend != 0.0:
        canvas_line_curved(xy1=xy1, xy2=xy2, bend=bend, arrow_head="->", style=edge_style)
    else:
        canvas_line(xy1=xy1, xy2=xy2, arrow_head="->", style=edge_style)

    label = trans.effective_label
    if not label:
        return

    applied_text_style = trans.text_style or default_edge_text_style
    label_style = Style(
        text_size=8.5,
        text_font=Font.SANSSERIF_REGULAR,
        halign="center",
        valign="center",
    ).patch(applied_text_style)

    # Compute label offset along normal vector
    dx = xy2[0] - xy1[0]
    dy = xy2[1] - xy1[1]
    dist = math.hypot(dx, dy)
    if dist < 1e-6:
        canvas_text(xy=xy1, text=label, style=label_style)
        return

    mid_x = (xy1[0] + xy2[0]) / 2.0
    mid_y = (xy1[1] + xy2[1]) / 2.0

    if abs(bend) < 1e-6:
        # Straight line: offset perpendicular pointing generally upward or to the right
        px = -dy / dist
        py = dx / dist
        if py < 0 or (abs(py) < 1e-6 and px < 0):
            px, py = -px, -py
        label_x = mid_x + px * 2.2
        label_y = mid_y + py * 2.2
    else:
        # Curved line: out_vector in direction of Arc3 bow
        sign = 1.0 if bend > 0 else -1.0
        out_x = (dy / dist) * sign
        out_y = (-dx / dist) * sign
        apex_offset = dist * abs(bend) * 0.5
        label_offset = apex_offset + 2.2
        label_x = mid_x + out_x * label_offset
        label_y = mid_y + out_y * label_offset

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
