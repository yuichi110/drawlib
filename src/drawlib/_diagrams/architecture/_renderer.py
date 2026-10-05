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

from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PIL.Image import Image

import drawlib._icons.font_icons.phosphor._generated as phosphor_gen
import drawlib._icons.png_icons.gcp._generated as gcp_gen
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_images import Dimage
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import image as canvas_image
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams.architecture._group import NodeGroup
from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
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
from drawlib._preset_colors import DefaultColors as Colors

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

    default_style = Style(icon_color=(50, 50, 50, 1.0), image_border_width=0)
    applied_style = default_style.patch(icon_style)

    if isinstance(icon, (GcpIcon, PhosphorIcon)):
        _draw_enum_icon(icon, canvas_xy, icon_size, applied_style)
    elif isinstance(icon, (CustomIcon, Dimage, Image, str, Path)):
        _draw_image_icon(icon, canvas_xy, icon_size, applied_style)
    elif callable(icon):
        icon(xy=canvas_xy, width=icon_size, style=applied_style)


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
                text_halign="left",
                text_valign="top",
            )
            if group.text_style:
                title_style = title_style.patch(group.text_style)

            tx = gx + min_x + 2.5
            ty = gy + max_y - 2.0
            canvas_text(xy=(tx, ty), text=group.title, style=title_style)


def _render_node_label(node: Node, nx: float, ny: float, default_node_text_style: Style) -> None:
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

    font_size = float(node.text_style.text_size) if node.text_style and node.text_style.text_size is not None else 13.0
    base_style = Style(
        text_size=font_size,
        text_font=Font.SANSSERIF_REGULAR,
        text_halign=halign,
        text_valign=valign,
        text_angle=node.text_angle,
    )
    applied_style = base_style.patch(default_node_text_style)
    if node.text_style:
        applied_style = applied_style.patch(node.text_style)

    canvas_text(xy=(tx, ty), text=node.text, style=applied_style)


def _render_nodes(
    nodes: list[Node],
    canvas_xy_map: dict[Connectable, tuple[float, float]],
    default_node_style: Style,
    default_node_text_style: Style,
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
            applied_card = default_node_style.patch(node.style)
            canvas_rectangle(xy=(cx, cy), width=nw, height=nh, style=applied_card)

        default_icon_style = Style(
            icon_color=default_node_style.icon_color or default_node_style.shape_line_color or (50, 50, 50, 1.0),
            image_border_width=0,
        )
        applied_icon_style = (
            default_icon_style.patch(node.icon_style) if node.icon_style is not None else default_icon_style
        )
        _draw_icon(node.icon, (nx, ny), node.icon_size, applied_icon_style)
        _render_node_label(node, nx, ny, default_node_text_style)


def draw_diagram(diagram: ArchitectureDiagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Execute complete 2-pass drawing pipeline for an architecture diagram.

    Args:
        diagram: ArchitectureDiagram container instance.
        xy: Placement anchor coordinate (x, y). Defaults to (0.0, 0.0).
    """
    base_xy = (float(xy[0]), float(xy[1]))
    canvas_xy_map, all_groups, all_nodes, _ = _resolve_coordinates(diagram, base_xy)

    if diagram.style:
        dw, dh = diagram.get_size()
        bg_style = Style(
            shape_fill_color=Colors.White,
            shape_line_color=Colors.Transparent,
            shape_line_width=0.0,
        ).patch(diagram.style)
        canvas_rectangle(
            xy=(base_xy[0] + dw / 2.0, base_xy[1] + dh / 2.0),
            width=dw,
            height=dh,
            style=bg_style,
        )

    _render_groups(all_groups, canvas_xy_map)
    draw_edges(diagram._edges, canvas_xy_map, base_xy, diagram.edge_style, diagram.edge_text_style)
    _render_nodes(all_nodes, canvas_xy_map, diagram.node_style, diagram.node_text_style)

    if diagram.title:
        _, dh = diagram.get_size()
        base_title_style = Style(
            text_size=15,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(40, 40, 45, 1.0),
            text_halign="left",
            text_valign="bottom",
        )
        if diagram.title_style:
            title_style = base_title_style.patch(diagram.title_style)
        else:
            title_style = base_title_style
        canvas_text(xy=(base_xy[0] + 1.0, base_xy[1] + dh + 2.0), text=diagram.title, style=title_style)


# Re-exports for test compatibility
_apply_edge_padding = apply_edge_padding
_draw_edges = draw_edges
_draw_single_edge = draw_single_edge
_get_item_anchors = get_item_anchors
_resolve_connection_endpoints = resolve_connection_endpoints
