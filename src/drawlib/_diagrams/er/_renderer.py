# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for ER (Entity-Relationship) diagrams."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Colors, Style
from drawlib._diagrams.er._types import Cardinality, RoutingType, Side
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.shapes import circle as canvas_circle
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._diagrams.er._diagram import ERDiagram
    from drawlib._diagrams.er._entity import Entity
    from drawlib._diagrams.er._relationship import Relationship

# Default palette
_DEFAULT_BORDER_COLOR = (71, 85, 105, 1.0)  # Slate-600
_DEFAULT_HEADER_BG = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_HEADER_TEXT_COLOR = (255, 255, 255, 1.0)  # White
_DEFAULT_BODY_BG = (255, 255, 255, 1.0)  # White
_DEFAULT_SEPARATOR_COLOR = (226, 232, 240, 1.0)  # Slate-200
_DEFAULT_TEXT_COLOR = (30, 41, 59, 1.0)  # Slate-800
_DEFAULT_MUTED_TEXT_COLOR = (100, 116, 139, 1.0)  # Slate-500
_DEFAULT_PK_COLOR = (217, 119, 6, 1.0)  # Amber-600
_DEFAULT_FK_COLOR = (37, 99, 235, 1.0)  # Blue-600
_DEFAULT_RELATION_LINE_COLOR = (71, 85, 105, 1.0)  # Slate-600


def draw_er_diagram(diagram: ERDiagram, base_xy: tuple[float, float]) -> None:
    """Render the complete ER diagram at the given base canvas coordinate.

    Args:
        diagram: ERDiagram container instance.
        base_xy: Base canvas coordinate (x, y) where the diagram is placed.
    """
    canvas_xy_map = _resolve_coordinates(diagram, base_xy)

    # 1. Render Diagram Background if specified
    if diagram.style is not None:
        dw, dh = diagram.get_size()
        bx, by = base_xy
        bg_style = Style(
            shape_fill_color=Colors.White,
            shape_line_color=Colors.Transparent,
            shape_line_width=0.0,
        ).patch(diagram.style)
        canvas_rectangle(xy=(bx + dw / 2.0, by + dh / 2.0), width=dw, height=dh, style=bg_style)

    # 2. Render Diagram Title if specified
    if diagram.title:
        dw, dh = diagram.get_size()
        bx, by = base_xy
        title_style = Style(
            text_size=18,
            text_font=Font.SANSSERIF_BOLD,
            text_color=_DEFAULT_HEADER_BG,
            text_halign="center",
            text_valign="bottom",
        )
        canvas_text(xy=(bx + dw / 2.0, by + dh + 2.0), text=diagram.title, style=title_style)

    # 3. Render Relationships (Edges & Crow's Foot markers)
    for rel in diagram.relationships:
        _render_relationship(rel, canvas_xy_map)

    # 4. Render Entities (Cards, Headers, Columns)
    for entity, _ in diagram._entities:
        ent_canvas_xy = canvas_xy_map[entity]
        _render_entity(entity, ent_canvas_xy)


def _resolve_coordinates(
    diagram: ERDiagram,
    base_xy: tuple[float, float],
) -> dict[Entity, tuple[float, float]]:
    """Resolve canvas coordinates for all entities.

    Args:
        diagram: ERDiagram instance.
        base_xy: Placement base coordinate on canvas.

    Returns:
        Mapping of Entity to canvas center coordinate (cx, cy).
    """
    bx, by = base_xy
    return {entity: (bx + ex, by + ey) for entity, (ex, ey) in diagram._entities}


def _render_entity(entity: Entity, canvas_xy: tuple[float, float]) -> None:
    """Render a single entity box on the canvas.

    Args:
        entity: Entity instance to draw.
        canvas_xy: Center coordinate (cx, cy) on the canvas.
    """
    cx, cy = canvas_xy
    w = entity.width
    h = entity.effective_height
    half_w = w / 2.0
    half_h = h / 2.0

    # 1. Main Background and Outer Box
    box_style = Style(
        shape_fill_color=_DEFAULT_BODY_BG,
        shape_line_color=_DEFAULT_BORDER_COLOR,
        shape_line_width=1.5,
    )
    if entity.style is not None:
        box_style = box_style.patch(entity.style)
    canvas_rectangle(xy=(cx, cy), width=w, height=h, style=box_style)

    # 2. Header Box & Title Text
    hh = entity.header_height
    header_cy = cy + half_h - hh / 2.0
    header_box_style = Style(
        shape_fill_color=_DEFAULT_HEADER_BG,
        shape_line_color=_DEFAULT_HEADER_BG,
        shape_line_width=1.0,
    )
    if entity.header_style is not None:
        header_box_style = header_box_style.patch(entity.header_style)
    canvas_rectangle(xy=(cx, header_cy), width=w, height=hh, style=header_box_style)

    header_text_color = header_box_style.text_color or _DEFAULT_HEADER_TEXT_COLOR
    header_text_style = Style(
        text_size=13,
        text_font=Font.SANSSERIF_BOLD,
        text_color=header_text_color,
        text_halign="center",
        text_valign="center",
    )
    canvas_text(xy=(cx, header_cy), text=entity.name, style=header_text_style)

    # Header Divider Line
    divider_y = cy + half_h - hh
    canvas_line(
        xy1=(cx - half_w, divider_y),
        xy2=(cx + half_w, divider_y),
        style=Style(line_color=_DEFAULT_BORDER_COLOR, line_width=1.5),
    )

    # 3. Columns Rendering
    rh = entity.row_height
    start_y = divider_y
    separator_style = Style(
        line_color=_DEFAULT_SEPARATOR_COLOR,
        line_width=0.8,
    )

    for idx, col in enumerate(entity.columns):
        row_cy = start_y - (idx + 0.5) * rh
        row_bottom_y = start_y - (idx + 1.0) * rh

        # Row separator line
        canvas_line(
            xy1=(cx - half_w, row_bottom_y),
            xy2=(cx + half_w, row_bottom_y),
            style=separator_style,
        )

        # Key badge (PK / FK)
        badge_text = ""
        badge_color = _DEFAULT_TEXT_COLOR
        if col.pk and col.fk:
            badge_text = "PK,FK"
            badge_color = _DEFAULT_PK_COLOR
        elif col.pk:
            badge_text = "PK"
            badge_color = _DEFAULT_PK_COLOR
        elif col.fk:
            badge_text = "FK"
            badge_color = _DEFAULT_FK_COLOR

        if badge_text:
            badge_x = cx - half_w + 1.2
            canvas_text(
                xy=(badge_x, row_cy),
                text=badge_text,
                style=Style(
                    text_size=9,
                    text_font=Font.SANSSERIF_BOLD,
                    text_color=badge_color,
                    text_halign="left",
                    text_valign="center",
                ),
            )

        # Column Name
        name_x = cx - half_w + w * 0.20
        col_font = Font.SANSSERIF_BOLD if col.pk else Font.SANSSERIF_REGULAR
        canvas_text(
            xy=(name_x, row_cy),
            text=col.name,
            style=Style(
                text_size=9.5,
                text_font=col_font,
                text_color=_DEFAULT_TEXT_COLOR,
                text_halign="left",
                text_valign="center",
            ),
        )

        # Column Data Type
        if col.type:
            type_x = cx + half_w - 1.2
            canvas_text(
                xy=(type_x, row_cy),
                text=col.type,
                style=Style(
                    text_size=8.5,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=_DEFAULT_MUTED_TEXT_COLOR,
                    text_halign="right",
                    text_valign="center",
                ),
            )

    # 4. Redraw Outer Border on Top
    canvas_rectangle(
        xy=(cx, cy),
        width=w,
        height=h,
        style=Style(
            shape_fill_color=Colors.Transparent,
            shape_fill_alpha=0.0,
            shape_line_color=_DEFAULT_BORDER_COLOR,
            shape_line_width=1.5,
        ),
    )


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


def _render_relationship(
    rel: Relationship,
    canvas_xy_map: dict[Entity, tuple[float, float]],
) -> None:
    """Render a relationship edge with Crow's Foot markers and label.

    Args:
        rel: Relationship instance.
        canvas_xy_map: Mapping of Entity to canvas center coordinates.
    """
    start_ent = rel.start
    end_ent = rel.end
    scx, scy = canvas_xy_map[start_ent]
    ecx, ecy = canvas_xy_map[end_ent]

    # Resolve sides
    start_side = rel.start_side
    end_side = rel.end_side
    if start_side == "auto" or end_side == "auto":
        auto_s, auto_e = _determine_auto_sides((scx, scy), (ecx, ecy))
        if start_side == "auto":
            start_side = auto_s
        if end_side == "auto":
            end_side = auto_e

    # Compute anchor coordinates
    start_anchor = _get_canvas_anchor(start_ent, (scx, scy), start_side, rel.start_column)
    end_anchor = _get_canvas_anchor(end_ent, (ecx, ecy), end_side, rel.end_column)

    # Compute routing path
    path = _compute_orthogonal_path(
        start_anchor,
        end_anchor,
        start_side,
        end_side,
        rel.routing,
    )

    # Edge Style
    line_style = Style(
        line_color=_DEFAULT_RELATION_LINE_COLOR,
        line_width=1.5,
    )
    if rel.style is not None:
        line_style = line_style.patch(rel.style)

    # Draw main line path
    canvas_lines(xys=path, style=line_style)

    # Parse Cardinality: "start_spec:end_spec"
    parts = rel.cardinality.split(":")
    start_spec = parts[0]
    end_spec = parts[1]

    # Render Start Crow's Foot Marker
    if len(path) >= 2:
        p0 = path[0]
        p1 = path[1]
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dist = math.hypot(dx, dy)
        if dist > 1e-4:
            u = (dx / dist, dy / dist)
            _render_crows_foot_marker(p0, u, start_spec, line_style)

    # Render End Crow's Foot Marker
    if len(path) >= 2:
        p_last = path[-1]
        p_prev = path[-2]
        dx = p_prev[0] - p_last[0]
        dy = p_prev[1] - p_last[1]
        dist = math.hypot(dx, dy)
        if dist > 1e-4:
            u = (dx / dist, dy / dist)
            _render_crows_foot_marker(p_last, u, end_spec, line_style)

    # Render Label if provided
    if rel.label:
        _render_relationship_label(path, rel.label)


def _get_canvas_anchor(
    entity: Entity,
    canvas_xy: tuple[float, float],
    side: Side,
    column_name: str | None,
) -> tuple[float, float]:
    """Calculate absolute canvas anchor coordinate for an entity border."""
    cx, cy = canvas_xy
    w = entity.width
    h = entity.effective_height
    half_w = w / 2.0
    half_h = h / 2.0

    if side == "top":
        return (cx, cy + half_h)
    if side == "bottom":
        return (cx, cy - half_h)

    target_y = cy
    if column_name is not None and side in {"left", "right", "auto"}:
        for idx, col in enumerate(entity.columns):
            if col.name == column_name:
                top_y = cy + half_h
                row_top_y = top_y - entity.header_height - idx * entity.row_height
                target_y = row_top_y - entity.row_height / 2.0
                break

    if side == "left":
        return (cx - half_w, target_y)
    if side == "right":
        return (cx + half_w, target_y)

    return (cx, target_y)


def _compute_orthogonal_path(
    start_pt: tuple[float, float],
    end_pt: tuple[float, float],
    start_side: Side,
    end_side: Side,
    routing: RoutingType,
) -> list[tuple[float, float]]:
    """Compute 2D polyline waypoints connecting start and end anchors."""
    if routing == "direct" or abs(start_pt[0] - end_pt[0]) < 1e-4 or abs(start_pt[1] - end_pt[1]) < 1e-4:
        return [start_pt, end_pt]

    sx, sy = start_pt
    ex, ey = end_pt

    # Horizontal exit to Horizontal entry (e.g. right -> left)
    if start_side in {"left", "right"} and end_side in {"left", "right"}:
        if (start_side == "right" and ex > sx) or (start_side == "left" and ex < sx):
            mid_x = (sx + ex) / 2.0
            path = [start_pt, (mid_x, sy), (mid_x, ey), end_pt]
        else:
            offset_s = 3.0 if start_side == "right" else -3.0
            offset_e = 3.0 if end_side == "right" else -3.0
            mid_y = (sy + ey) / 2.0
            path = [
                start_pt,
                (sx + offset_s, sy),
                (sx + offset_s, mid_y),
                (ex + offset_e, mid_y),
                (ex + offset_e, ey),
                end_pt,
            ]
    # Vertical exit to Vertical entry (e.g. bottom -> top)
    elif start_side in {"top", "bottom"} and end_side in {"top", "bottom"}:
        if (start_side == "top" and ey > sy) or (start_side == "bottom" and ey < sy):
            mid_y = (sy + ey) / 2.0
            path = [start_pt, (sx, mid_y), (ex, mid_y), end_pt]
        else:
            offset_s = 3.0 if start_side == "top" else -3.0
            offset_e = 3.0 if end_side == "top" else -3.0
            mid_x = (sx + ex) / 2.0
            path = [
                start_pt,
                (sx, sy + offset_s),
                (mid_x, sy + offset_s),
                (mid_x, ey + offset_e),
                (ex, ey + offset_e),
                end_pt,
            ]
    # Horizontal exit to Vertical entry
    elif start_side in {"left", "right"} and end_side in {"top", "bottom"}:
        path = [start_pt, (ex, sy), end_pt]
    # Vertical exit to Horizontal entry
    elif start_side in {"top", "bottom"} and end_side in {"left", "right"}:
        path = [start_pt, (sx, ey), end_pt]
    else:
        path = [start_pt, (ex, sy), end_pt]

    return path


def _render_crows_foot_marker(
    pt: tuple[float, float],
    u: tuple[float, float],
    spec: str,
    line_style: Style,
) -> None:
    """Render IE Crow's foot marker at pt pointing along direction u into the line."""
    ux, uy = u
    # Perpendicular vector n
    nx, ny = -uy, ux

    tick_len = 1.0
    fork_width = 0.9
    circle_radius = 0.45

    color = line_style.line_color or _DEFAULT_RELATION_LINE_COLOR
    lwidth = line_style.line_width or 1.5

    marker_style = Style(line_color=color, line_width=lwidth)
    circle_style = Style(
        shape_fill_color=_DEFAULT_BODY_BG,
        shape_line_color=color,
        shape_line_width=lwidth,
    )

    def draw_tick(distance: float) -> None:
        p_center = (pt[0] + distance * ux, pt[1] + distance * uy)
        p1 = (p_center[0] - tick_len * nx, p_center[1] - tick_len * ny)
        p2 = (p_center[0] + tick_len * nx, p_center[1] + tick_len * ny)
        canvas_line(xy1=p1, xy2=p2, style=marker_style)

    def draw_circle(distance: float) -> None:
        p_center = (pt[0] + distance * ux, pt[1] + distance * uy)
        canvas_circle(xy=p_center, radius=circle_radius, style=circle_style)

    def draw_fork(root_dist: float) -> None:
        root = (pt[0] + root_dist * ux, pt[1] + root_dist * uy)
        # 3 branches of crow's foot
        # Top branch
        t_tip = (pt[0] + fork_width * nx, pt[1] + fork_width * ny)
        # Bottom branch
        b_tip = (pt[0] - fork_width * nx, pt[1] - fork_width * ny)
        canvas_line(xy1=root, xy2=t_tip, style=marker_style)
        canvas_line(xy1=root, xy2=pt, style=marker_style)
        canvas_line(xy1=root, xy2=b_tip, style=marker_style)

    if spec == "1":
        # Exactly 1: two parallel vertical bars
        draw_tick(0.6)
        draw_tick(1.4)
    elif spec == "0..1":
        # Zero or 1: circle and bar
        draw_tick(0.6)
        draw_circle(1.5)
    elif spec == "*":
        # Zero or more: crow's foot and circle
        draw_circle(2.1)
        draw_fork(1.4)
    elif spec == "1..*":
        # One or more: crow's foot and bar
        draw_tick(2.1)
        draw_fork(1.4)


def _render_relationship_label(
    path: list[tuple[float, float]],
    label_text: str,
) -> None:
    """Draw text label near the midpoint of the relationship line path."""
    if not path:
        return

    # Find middle segment
    mid_idx = (len(path) - 1) // 2
    p1 = path[mid_idx]
    p2 = path[mid_idx + 1]
    mx = (p1[0] + p2[0]) / 2.0
    my = (p1[1] + p2[1]) / 2.0

    label_style = Style(
        text_size=9.5,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=_DEFAULT_TEXT_COLOR,
        text_bg_fill_color=_DEFAULT_BODY_BG,
        text_bg_fill_alpha=0.9,
        text_bg_line_color=_DEFAULT_SEPARATOR_COLOR,
        text_bg_line_width=0.5,
        text_halign="center",
        text_valign="center",
    )
    canvas_text(xy=(mx, my), text=label_text, style=label_style)
