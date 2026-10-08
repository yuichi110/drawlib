# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared internal rendering, padding, and visibility utilities for diagrams."""

from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, TypeVar

from PIL.Image import Image

import drawlib._icons.font_icons.phosphor._generated as phosphor_gen
import drawlib._icons.png_icons.gcp._generated as gcp_gen
from drawlib._core.l3_colors import ColorType
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_images import Dimage
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import image as canvas_image
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
from drawlib._diagrams.architecture._types import IconType
from drawlib._preset_colors import DefaultColors as Colors

EdgeT = TypeVar("EdgeT")


def parse_padding(padding: float | tuple[float, float]) -> tuple[float, float]:
    """Extract (start_pad, end_pad) from a scalar or 2-tuple padding specification."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val
    return float(padding[0]), float(padding[1])


def apply_segment_padding(
    p0: tuple[float, float],
    p1: tuple[float, float],
    start_pad: float,
    end_pad: float,
) -> list[tuple[float, float]]:
    """Trim a 2-point segment by start and end padding distances."""
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


def apply_edge_padding(
    pts: list[tuple[float, float]],
    padding: float | tuple[float, float],
) -> list[tuple[float, float]]:
    """Shorten the start and end of an edge polyline path by padding distance."""
    if len(pts) < 2:
        return pts

    start_pad, end_pad = parse_padding(padding)
    if start_pad <= 0.0 and end_pad <= 0.0:
        return pts

    if len(pts) == 2:
        return apply_segment_padding(pts[0], pts[1], start_pad, end_pad)

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


def render_diagram_background(
    center_xy: tuple[float, float],
    width: float,
    height: float,
    style: Style | None,
) -> None:
    """Render optional diagram background card centered at center_xy."""
    if style is None:
        return
    bg_style = Style(
        shape_fill_color=Colors.White,
        shape_line_color=Colors.Transparent,
        shape_line_width=0.0,
    ).patch(style)
    canvas_rectangle(xy=center_xy, width=width, height=height, style=bg_style)


def render_diagram_title(
    xy: tuple[float, float],
    title: str,
    title_style: Style | None,
    *,
    default_size: float = 16.0,
    default_color: ColorType = (30, 41, 59, 1.0),
    default_halign: Literal["left", "center", "right"] = "center",
    default_valign: Literal["top", "center", "bottom"] = "bottom",
) -> None:
    """Render optional diagram title text with consistent base styling."""
    if not title:
        return
    base_title_style = Style(
        text_size=default_size,
        text_font=Font.SANSSERIF_BOLD,
        text_color=default_color,
        halign=default_halign,
        valign=default_valign,
    )
    applied_style = base_title_style.patch(title_style) if title_style is not None else base_title_style
    canvas_text(xy=xy, text=title, style=applied_style)


def draw_enum_icon(
    icon: GcpIcon | PhosphorIcon,
    canvas_xy: tuple[float, float],
    icon_size: float,
    applied_style: Style,
    *,
    fallback_box: bool = False,
) -> None:
    """Draw a GCP or Phosphor enum icon from generated function modules."""
    module = gcp_gen if isinstance(icon, GcpIcon) else phosphor_gen
    func = getattr(module, icon.value, None) or getattr(module, icon.name.lower(), None)
    if func is not None:
        func(xy=canvas_xy, width=icon_size, style=applied_style)
    elif fallback_box:
        fallback_style = Style(
            shape_fill_color=Colors.Transparent,
            shape_line_color=(150, 150, 150, 1.0),
            shape_line_width=1.0,
        )
        canvas_rectangle(xy=canvas_xy, width=icon_size, height=icon_size, style=fallback_style)


def draw_image_icon(
    icon: CustomIcon | Dimage | Image | str | Path,
    canvas_xy: tuple[float, float],
    icon_size: float,
    applied_style: Style,
) -> None:
    """Draw a raster image icon (CustomIcon, Dimage, PIL Image, or path)."""
    img: str | Dimage
    if isinstance(icon, CustomIcon):
        img = icon.dimage
    elif isinstance(icon, Image):
        img = Dimage(icon)
    elif isinstance(icon, Dimage):
        img = icon
    else:
        img = str(icon)
    canvas_image(xy=canvas_xy, image=img, width=icon_size, style=applied_style)


def draw_diagram_icon(
    icon: IconType,
    canvas_xy: tuple[float, float],
    icon_size: float,
    icon_style: Style | None = None,
    *,
    fallback_box: bool = False,
) -> None:
    """Draw an icon (enum, image, or callable) at canvas_xy with size icon_size."""
    if icon is None:
        return

    base_icon_color = (
        (icon_style.icon_color or icon_style.shape_line_color or (50, 50, 50, 1.0))
        if icon_style is not None
        else (50, 50, 50, 1.0)
    )
    default_style = Style(icon_color=base_icon_color, image_border_width=0)
    applied_style = default_style.patch(icon_style) if icon_style is not None else default_style
    applied_style = applied_style.patch(image_border_width=0)

    if isinstance(icon, (GcpIcon, PhosphorIcon)):
        draw_enum_icon(icon, canvas_xy, icon_size, applied_style, fallback_box=fallback_box)
    elif isinstance(icon, (CustomIcon, Dimage, Image, str, Path)):
        draw_image_icon(icon, canvas_xy, icon_size, applied_style)
    elif callable(icon):
        icon(xy=canvas_xy, width=icon_size, style=applied_style)


def render_icon_text_card(
    canvas_xy: tuple[float, float],
    card_size: tuple[float, float],
    *,
    text: str = "",
    icon: IconType = None,
    icon_size: float = 8.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    default_node_style: Style,
    default_node_text_style: Style,
    default_node_card_style: Style | None = None,
    fallback_box: bool = False,
) -> None:
    """Render a unified card (optional), icon/image (optional), and text (optional) at canvas_xy."""
    cx, cy = canvas_xy
    card_w, card_h = card_size

    resolved_card_style: Style | None = None
    if default_node_card_style is not None and card_style is not None:
        resolved_card_style = default_node_card_style.patch(card_style)
    elif card_style is not None:
        resolved_card_style = card_style
    elif default_node_card_style is not None:
        resolved_card_style = default_node_card_style

    if resolved_card_style is not None:
        canvas_rectangle(xy=(cx, cy), width=card_w, height=card_h, style=resolved_card_style)

    if icon is not None and text:
        is_multiline = "\n" in text
        eff_h = max(card_h, icon_size + 4.0)
        top_margin = max(1.0, (eff_h - icon_size) * (0.12 if is_multiline else 0.18))
        icon_top = cy + eff_h / 2.0 - top_margin
        iy = icon_top - icon_size / 2.0
        icon_bottom = iy - icon_size / 2.0
        card_bottom = cy - eff_h / 2.0
        ty = (icon_bottom + card_bottom) / 2.0 + (0.65 if is_multiline else 0.25)
    else:
        iy = cy
        ty = cy

    if icon is not None:
        applied_icon_style = default_node_style.patch(style) if style is not None else default_node_style
        draw_diagram_icon(icon, (cx, iy), icon_size, applied_icon_style, fallback_box=fallback_box)

    if text:
        base_text_style = Style(
            text_size=12.0,
            text_font=Font.SANSSERIF_REGULAR,
            text_color=(35, 35, 40, 1.0),
            halign="center",
            valign="center",
        )
        applied_text_style = base_text_style.patch(default_node_text_style)
        if text_style is not None:
            applied_text_style = applied_text_style.patch(text_style)
        canvas_text(xy=(cx, ty), text=text, style=applied_text_style)


def is_edge_visible(edge: object) -> bool:
    """Return True if the edge and both of its endpoints are visible in the current frame."""
    if not getattr(edge, "show", True):
        return False
    start = getattr(edge, "start", None)
    end = getattr(edge, "end", None)
    if start is not None and not getattr(start, "show", True):
        return False
    return not (end is not None and not getattr(end, "show", True))


def _is_endpoint_active(
    item: object,
    active_junctions: set[object],
    junction_cls: type,
) -> bool:
    """Return True if a connection endpoint is active in the current frame."""
    if isinstance(item, junction_cls):
        return item in active_junctions
    return bool(getattr(item, "show", True))


def _prune_inactive_junctions(
    edges: Sequence[object],
    active_junctions: set[object],
    junction_cls: type,
) -> None:
    """Iteratively deactivate pass-through junctions lacking active incoming or outgoing edges."""
    changed = True
    while changed:
        changed = False
        for j in list(active_junctions):
            in_edges = [e for e in edges if getattr(e, "end", None) is j]
            out_edges = [e for e in edges if getattr(e, "start", None) is j]
            if not (in_edges and out_edges):
                continue
            has_vis_in = any(
                getattr(e, "show", True)
                and _is_endpoint_active(getattr(e, "start", None), active_junctions, junction_cls)
                for e in in_edges
            )
            has_vis_out = any(
                getattr(e, "show", True)
                and _is_endpoint_active(getattr(e, "end", None), active_junctions, junction_cls)
                for e in out_edges
            )
            if not (has_vis_in and has_vis_out):
                active_junctions.remove(j)
                changed = True


def resolve_visible_edges_with_junctions(
    edges: Sequence[EdgeT],
    junction_cls: type,
) -> list[EdgeT]:
    """Filter edges to those visible, auto-hiding dangling pass-through Junction edges.

    A Junction that has both incoming and outgoing edges registered in the diagram
    is only active in a frame if at least one incoming edge AND at least one outgoing
    edge are visible. This prevents dangling half-lines when animating `fork()` / `Junction`
    branches via `node.show = False` or `edge.show = False`.
    """
    junctions = {
        endpoint
        for edge in edges
        for endpoint in (getattr(edge, "start", None), getattr(edge, "end", None))
        if isinstance(endpoint, junction_cls)
    }
    if not junctions:
        return [e for e in edges if is_edge_visible(e)]

    active_junctions = {j for j in junctions if getattr(j, "show", True)}
    _prune_inactive_junctions(edges, active_junctions, junction_cls)

    return [
        e
        for e in edges
        if getattr(e, "show", True)
        and _is_endpoint_active(getattr(e, "start", None), active_junctions, junction_cls)
        and _is_endpoint_active(getattr(e, "end", None), active_junctions, junction_cls)
    ]
