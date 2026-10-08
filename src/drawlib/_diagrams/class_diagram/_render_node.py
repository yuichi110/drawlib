# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Class card rendering functions for UML Class diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._preset_colors import DefaultColors as Colors

if TYPE_CHECKING:
    from drawlib._diagrams.class_diagram._class_node import ClassNode


def render_class_node(
    node: ClassNode,
    canvas_xy: tuple[float, float],
    default_node_style: Style,
    default_header_style: Style | None = None,
) -> None:
    """Render a single class card on the canvas.

    Args:
        node: ClassNode instance to draw.
        canvas_xy: Center coordinate (cx, cy) on the canvas.
        default_node_style: Mandatory default Style for class card nodes.
        default_header_style: Optional default Style for class headers.
    """
    cx, cy = canvas_xy
    w = node.width
    h = node.effective_height
    half_w = w / 2.0
    half_h = h / 2.0
    top_y = cy + half_h

    # 1. Main Background and Outer Box
    box_style = default_node_style.patch(node.style) if node.style is not None else default_node_style
    border_color = box_style.shape_line_color or (71, 85, 105, 1.0)
    canvas_rectangle(xy=(cx, cy), width=w, height=h, r=1.0, style=box_style)

    # 2. Header Box & Title Text
    hh = node.header_height
    header_cy = top_y - hh / 2.0
    if node.header_style is not None:
        header_base = default_header_style if default_header_style is not None else default_node_style
        header_box_style = header_base.patch(node.header_style)
    elif default_header_style is not None:
        header_box_style = default_header_style
    else:
        header_box_style = Style(
            shape_fill_color=border_color,
            shape_line_color=border_color,
            shape_line_width=1.5,
            text_color=(255, 255, 255, 1.0),
        )
    canvas_rectangle(xy=(cx, header_cy), width=w, height=hh, r=1.0, style=header_box_style)

    header_text_color = header_box_style.text_color or (255, 255, 255, 1.0)
    header_font = Font.SANSSERIF_BOLD

    effective_stereotype = node.stereotype
    if not effective_stereotype and node.is_abstract:
        effective_stereotype = "abstract"

    if effective_stereotype:
        canvas_text(
            xy=(cx, header_cy + 1.4),
            text=f"«{effective_stereotype}»",
            style=Style(
                text_size=7.5,
                text_font=Font.SANSSERIF_REGULAR,
                text_color=(203, 213, 225, 1.0),
                halign="center",
                valign="center",
            ),
        )
        canvas_text(
            xy=(cx, header_cy - 1.2),
            text=node.name,
            style=Style(
                text_size=10.5,
                text_font=header_font,
                text_color=header_text_color,
                halign="center",
                valign="center",
            ),
        )
    else:
        canvas_text(
            xy=(cx, header_cy),
            text=node.name,
            style=Style(
                text_size=11.0,
                text_font=header_font,
                text_color=header_text_color,
                halign="center",
                valign="center",
            ),
        )

    # Header Divider Line
    divider_y = top_y - hh
    canvas_line(
        xy1=(cx - half_w, divider_y),
        xy2=(cx + half_w, divider_y),
        style=Style(
            line_color=border_color,
            line_width=1.5,
        ),
    )

    # 3. Attributes Section
    curr_y = divider_y
    left_x = cx - half_w + 1.8
    body_text_color = box_style.text_color or (30, 41, 59, 1.0)
    if node.attributes:
        curr_y -= 0.8
        for attr in node.attributes:
            row_y = curr_y - node.row_height / 2.0
            canvas_text(
                xy=(left_x, row_y),
                text=attr.display_text,
                style=Style(
                    text_size=8.5,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=body_text_color,
                    halign="left",
                    valign="center",
                ),
            )
            curr_y -= node.row_height
        curr_y -= 0.7

    # Divider between attributes and methods
    if node.attributes and node.methods:
        canvas_line(
            xy1=(cx - half_w, curr_y),
            xy2=(cx + half_w, curr_y),
            style=Style(
                line_color=(226, 232, 240, 1.0),
                line_width=1.0,
            ),
        )

    # 4. Methods Section
    if node.methods:
        curr_y -= 0.8
        for meth in node.methods:
            row_y = curr_y - node.row_height / 2.0
            canvas_text(
                xy=(left_x, row_y),
                text=meth.display_text,
                style=Style(
                    text_size=8.5,
                    text_font=Font.SANSSERIF_REGULAR,
                    text_color=body_text_color,
                    halign="left",
                    valign="center",
                ),
            )
            curr_y -= node.row_height

    # 5. Redraw Outer Border on Top
    canvas_rectangle(
        xy=(cx, cy),
        width=w,
        height=h,
        r=1.0,
        style=Style(
            shape_fill_color=Colors.Transparent,
            shape_fill_alpha=0.0,
            shape_line_color=border_color,
            shape_line_width=1.5,
        ),
    )
