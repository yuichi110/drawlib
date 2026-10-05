# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Relationship routing and rendering functions for UML Class diagrams."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_math import Side as MathSide
from drawlib._core.l3_math import compute_orthogonal_path
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import polygon as canvas_polygon
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.class_diagram._types import Side

if TYPE_CHECKING:
    from drawlib._diagrams.class_diagram._class_node import ClassNode
    from drawlib._diagrams.class_diagram._relationship import ClassRelationship


def render_relationship(
    rel: ClassRelationship,
    canvas_xy_map: dict[ClassNode, tuple[float, float]],
    default_edge_style: Style,
) -> None:
    """Render a relationship edge connecting two class nodes with markers and labels.

    Args:
        rel: ClassRelationship instance.
        canvas_xy_map: Mapping of ClassNode to canvas center coordinates.
        default_edge_style: Mandatory default Style for relationship edges.
    """
    path = _compute_relationship_path(rel, canvas_xy_map)

    if rel.padding != 0.0:
        path = _apply_padding(path, rel.padding)

    is_dashed = rel.relationship_type in {"realization", "dependency"}
    base_style = default_edge_style.patch(line_style="dashed") if is_dashed else default_edge_style
    line_style = base_style.patch(rel.style) if rel.style is not None else base_style

    trimmed_path = _render_relationship_markers(rel, path, line_style)
    canvas_lines(xys=trimmed_path, style=line_style)
    _render_relationship_annotations(rel, path, line_style)


def _determine_auto_sides(
    start_xy: tuple[float, float],
    end_xy: tuple[float, float],
) -> tuple[Side, Side]:
    """Determine best attachment sides when auto is specified."""
    sx, sy = start_xy
    ex, ey = end_xy
    dx = ex - sx
    dy = ey - sy

    if abs(dx) >= abs(dy):
        if dx >= 0:
            return "right", "left"
        return "left", "right"
    if dy >= 0:
        return "top", "bottom"
    return "bottom", "top"


def _get_canvas_anchor(
    node: ClassNode,
    canvas_xy: tuple[float, float],
    side: Side,
) -> tuple[float, float]:
    """Calculate absolute canvas anchor coordinate for a class border."""
    cx, cy = canvas_xy
    half_w = node.width / 2.0
    half_h = node.effective_height / 2.0

    if side == "top":
        return (cx, cy + half_h)
    if side == "bottom":
        return (cx, cy - half_h)
    if side == "left":
        return (cx - half_w, cy)
    if side == "right":
        return (cx + half_w, cy)
    return (cx, cy)


def _intersect_rect(
    center: tuple[float, float],
    target: tuple[float, float],
    width: float,
    height: float,
) -> tuple[tuple[float, float], Side]:
    """Calculate intersection of ray from center to target with rectangle boundary."""
    cx, cy = center
    tx, ty = target
    dx = tx - cx
    dy = ty - cy
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return center, "auto"

    hw = width / 2.0
    hh = height / 2.0

    sx = abs(hw / dx) if abs(dx) > 1e-6 else float("inf")
    sy = abs(hh / dy) if abs(dy) > 1e-6 else float("inf")
    s = min(sx, sy)

    ix = cx + s * dx
    iy = cy + s * dy

    if sx <= sy:
        side: Side = "right" if dx > 0 else "left"
    else:
        side = "top" if dy > 0 else "bottom"

    return (ix, iy), side


def _render_triangle_marker(
    tip: tuple[float, float],
    u: tuple[float, float],
    line_style: Style,
) -> tuple[float, float]:
    """Render hollow triangle marker at tip pointing along direction u.

    Returns:
        p_base: The base center coordinate where the connecting line should terminate.
    """
    ux, uy = u
    nx, ny = -uy, ux
    tri_len = 2.2
    tri_half_w = 1.3

    p_base = (tip[0] - tri_len * ux, tip[1] - tri_len * uy)
    v1 = (p_base[0] + tri_half_w * nx, p_base[1] + tri_half_w * ny)
    v2 = (p_base[0] - tri_half_w * nx, p_base[1] - tri_half_w * ny)

    color = line_style.line_color or (71, 85, 105, 1.0)
    lwidth = line_style.line_width or 1.5

    tri_style = Style(
        shape_fill_color=(255, 255, 255, 1.0),
        shape_line_color=color,
        shape_line_width=lwidth,
    )
    canvas_polygon(xys=[tip, v1, v2], style=tri_style)
    return p_base


def _render_diamond_marker(
    root: tuple[float, float],
    u: tuple[float, float],
    is_composition: bool,
    line_style: Style,
) -> tuple[float, float]:
    """Render diamond marker at root pointing along direction u into line.

    Returns:
        p_tip: The far tip coordinate where the connecting line should originate.
    """
    ux, uy = u
    nx, ny = -uy, ux
    diamond_len = 2.4
    diamond_half_w = 1.1

    mid = (root[0] + (diamond_len / 2.0) * ux, root[1] + (diamond_len / 2.0) * uy)
    p_tip = (root[0] + diamond_len * ux, root[1] + diamond_len * uy)
    v1 = (mid[0] + diamond_half_w * nx, mid[1] + diamond_half_w * ny)
    v2 = (mid[0] - diamond_half_w * nx, mid[1] - diamond_half_w * ny)

    color = line_style.line_color or (71, 85, 105, 1.0)
    lwidth = line_style.line_width or 1.5
    fill_color = color if is_composition else (255, 255, 255, 1.0)

    d_style = Style(
        shape_fill_color=fill_color,
        shape_line_color=color,
        shape_line_width=lwidth,
    )
    canvas_polygon(xys=[root, v1, p_tip, v2], style=d_style)
    return p_tip


def _render_open_arrow_marker(
    tip: tuple[float, float],
    u: tuple[float, float],
    line_style: Style,
) -> None:
    """Render open arrowhead marker at tip pointing along direction u."""
    ux, uy = u
    nx, ny = -uy, ux
    arrow_len = 1.8
    arrow_half_w = 1.2

    w1 = (tip[0] - arrow_len * ux + arrow_half_w * nx, tip[1] - arrow_len * uy + arrow_half_w * ny)
    w2 = (tip[0] - arrow_len * ux - arrow_half_w * nx, tip[1] - arrow_len * uy - arrow_half_w * ny)

    color = line_style.line_color or (71, 85, 105, 1.0)
    lwidth = line_style.line_width or 1.5

    arrow_style = Style(
        line_color=color,
        line_width=lwidth,
    )
    canvas_lines(xys=[w1, tip, w2], style=arrow_style)


def _compute_relationship_path(
    rel: ClassRelationship,
    canvas_xy_map: dict[ClassNode, tuple[float, float]],
) -> list[tuple[float, float]]:
    """Calculate raw routing path between start and end classes."""
    start_node = rel.start
    end_node = rel.end
    scx, scy = canvas_xy_map[start_node]
    ecx, ecy = canvas_xy_map[end_node]

    if rel.routing == "direct":
        if rel.start_side == "auto":
            start_anchor, _ = _intersect_rect((scx, scy), (ecx, ecy), start_node.width, start_node.effective_height)
        else:
            start_anchor = _get_canvas_anchor(start_node, (scx, scy), rel.start_side)

        if rel.end_side == "auto":
            end_anchor, _ = _intersect_rect((ecx, ecy), (scx, scy), end_node.width, end_node.effective_height)
        else:
            end_anchor = _get_canvas_anchor(end_node, (ecx, ecy), rel.end_side)

        return [start_anchor, end_anchor]

    start_side = rel.start_side
    end_side = rel.end_side
    if start_side == "auto" or end_side == "auto":
        auto_s, auto_e = _determine_auto_sides((scx, scy), (ecx, ecy))
        if start_side == "auto":
            start_side = auto_s
        if end_side == "auto":
            end_side = auto_e

    start_anchor = _get_canvas_anchor(start_node, (scx, scy), start_side)
    end_anchor = _get_canvas_anchor(end_node, (ecx, ecy), end_side)
    return compute_orthogonal_path(
        start_anchor,
        end_anchor,
        cast(MathSide, start_side),
        cast(MathSide, end_side),
        rel.routing,
    )


def _apply_padding(
    path: list[tuple[float, float]],
    padding: float | tuple[float, float],
) -> list[tuple[float, float]]:
    """Offset start and end anchors by the padding distance."""
    if len(path) < 2:
        return path

    result = list(path)
    pad_s = padding[0] if isinstance(padding, tuple) else float(padding)
    pad_e = padding[1] if isinstance(padding, tuple) else float(padding)

    if pad_s > 0:
        dx = result[1][0] - result[0][0]
        dy = result[1][1] - result[0][1]
        dist = math.hypot(dx, dy)
        if dist > pad_s:
            result[0] = (result[0][0] + (pad_s / dist) * dx, result[0][1] + (pad_s / dist) * dy)

    if pad_e > 0:
        dx = result[-2][0] - result[-1][0]
        dy = result[-2][1] - result[-1][1]
        dist = math.hypot(dx, dy)
        if dist > pad_e:
            result[-1] = (result[-1][0] + (pad_e / dist) * dx, result[-1][1] + (pad_e / dist) * dy)

    return result


def _render_relationship_markers(
    rel: ClassRelationship,
    path: list[tuple[float, float]],
    line_style: Style,
) -> list[tuple[float, float]]:
    """Render UML relationship markers (triangles, diamonds, arrows) and return trimmed line path."""
    if len(path) < 2:
        return list(path)

    trimmed = list(path)

    # Start marker: Diamond for composition / aggregation
    if rel.relationship_type in {"composition", "aggregation"}:
        p0, p1 = trimmed[0], trimmed[1]
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dist = math.hypot(dx, dy)
        if dist > 1e-4:
            u0 = (dx / dist, dy / dist)
            is_comp = rel.relationship_type == "composition"
            new_p0 = _render_diamond_marker(p0, u0, is_comp, line_style)
            if dist >= 2.4:
                trimmed[0] = new_p0

    # End marker: Triangle for inheritance/realization, open arrow for dependency/directed
    p_last, p_prev = trimmed[-1], trimmed[-2]
    dx = p_last[0] - p_prev[0]
    dy = p_last[1] - p_prev[1]
    dist = math.hypot(dx, dy)
    if dist > 1e-4:
        u_end = (dx / dist, dy / dist)
        if rel.relationship_type in {"inheritance", "realization"}:
            new_p_last = _render_triangle_marker(p_last, u_end, line_style)
            if dist >= 2.2:
                trimmed[-1] = new_p_last
        elif rel.relationship_type == "dependency" or rel.directed:
            _render_open_arrow_marker(p_last, u_end, line_style)

    return trimmed


def _render_start_annotations(
    rel: ClassRelationship,
    p0: tuple[float, float],
    p1: tuple[float, float],
    line_style: Style,
) -> None:
    """Render start multiplicity and role label near start anchor."""
    if not (rel.start_multiplicity or rel.start_role):
        return

    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    dist = math.hypot(dx, dy)
    if dist <= 1e-4:
        return

    u = (dx / dist, dy / dist)
    n = (-u[1], u[0])
    offset_dist = 4.0 if rel.relationship_type in {"composition", "aggregation"} else 2.8
    anchor = (p0[0] + offset_dist * u[0], p0[1] + offset_dist * u[1])

    text_color = line_style.text_color or (30, 41, 59, 1.0)
    muted_color = (100, 116, 139, 1.0)

    if rel.start_multiplicity:
        canvas_text(
            xy=(anchor[0] + 1.4 * n[0], anchor[1] + 1.4 * n[1]),
            text=rel.start_multiplicity,
            style=Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=text_color,
                text_halign="center",
                text_valign="center",
            ),
        )
    if rel.start_role:
        canvas_text(
            xy=(anchor[0] - 1.4 * n[0], anchor[1] - 1.4 * n[1]),
            text=rel.start_role,
            style=Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=muted_color,
                text_halign="center",
                text_valign="center",
            ),
        )


def _render_end_annotations(
    rel: ClassRelationship,
    p_last: tuple[float, float],
    p_prev: tuple[float, float],
    line_style: Style,
) -> None:
    """Render end multiplicity and role label near end anchor."""
    if not (rel.end_multiplicity or rel.end_role):
        return

    dx = p_prev[0] - p_last[0]
    dy = p_prev[1] - p_last[1]
    dist = math.hypot(dx, dy)
    if dist <= 1e-4:
        return

    u = (dx / dist, dy / dist)
    n = (-u[1], u[0])
    offset_dist = 4.0 if rel.relationship_type in {"inheritance", "realization"} or rel.directed else 2.8
    anchor = (p_last[0] + offset_dist * u[0], p_last[1] + offset_dist * u[1])

    text_color = line_style.text_color or (30, 41, 59, 1.0)
    muted_color = (100, 116, 139, 1.0)

    if rel.end_multiplicity:
        canvas_text(
            xy=(anchor[0] - 1.4 * n[0], anchor[1] - 1.4 * n[1]),
            text=rel.end_multiplicity,
            style=Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=text_color,
                text_halign="center",
                text_valign="center",
            ),
        )
    if rel.end_role:
        canvas_text(
            xy=(anchor[0] + 1.4 * n[0], anchor[1] + 1.4 * n[1]),
            text=rel.end_role,
            style=Style(
                text_size=8.0,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=muted_color,
                text_halign="center",
                text_valign="center",
            ),
        )


def _render_relationship_annotations(
    rel: ClassRelationship,
    path: list[tuple[float, float]],
    line_style: Style,
) -> None:
    """Render multiplicities, roles, and center label for a relationship."""
    if len(path) < 2:
        return

    _render_start_annotations(rel, path[0], path[1], line_style)
    _render_end_annotations(rel, path[-1], path[-2], line_style)

    # Center label
    if rel.label:
        mid_idx = (len(path) - 1) // 2
        p1 = path[mid_idx]
        p2 = path[mid_idx + 1]
        mx = (p1[0] + p2[0]) / 2.0
        my = (p1[1] + p2[1]) / 2.0
        label_text_color = line_style.text_color or (30, 41, 59, 1.0)
        canvas_text(
            xy=(mx, my),
            text=rel.label,
            style=Style(
                text_size=8.5,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=label_text_color,
                text_bg_fill_color=(255, 255, 255, 0.9),
                text_bg_fill_alpha=0.9,
                text_bg_line_color=(226, 232, 240, 1.0),
                text_bg_line_width=0.5,
                text_halign="center",
                text_valign="center",
            ),
        )
