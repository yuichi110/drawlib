# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Renderer engine for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams._common import render_diagram_background, render_diagram_title
from drawlib._diagrams.sequence._layout import (
    compute_diagram_size,
    compute_timeline_y,
    compute_x_coordinates,
)
from drawlib._diagrams.sequence._message import Message
from drawlib._diagrams.sequence._note import Note
from drawlib._diagrams.sequence._render_elements import (
    render_activation_bars,
    render_blocks,
    render_groups,
    render_headers,
    render_lifelines,
    render_note,
    render_single_message,
)

if TYPE_CHECKING:
    from drawlib._diagrams.sequence._diagram import SequenceDiagram


def draw_sequence_diagram(diagram: SequenceDiagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Execute complete 2-pass drawing pipeline for a sequence diagram.

    Args:
        diagram: SequenceDiagram container instance.
        xy: Base canvas anchor coordinate (x, y). Defaults to (0.0, 0.0).
    """
    bx, by = float(xy[0]), float(xy[1])
    pad_top = pad_bottom = pad_left = float(diagram.margin)

    dw, dh = compute_diagram_size(diagram)
    participant_x_map = compute_x_coordinates(diagram, pad_left)
    timeline_h, event_y_map, block_bounds_y, resolved_acts = compute_timeline_y(diagram)

    max_header_h = max((p.get_header_size()[1] for p in diagram.participants), default=12.0)
    group_top_extra = max((g.padding + (5.0 if g.title else 0.0) for g in diagram.groups), default=0.0)
    group_bottom_extra = max((g.padding for g in diagram.groups), default=0.0)
    title_extra = 6.0 if diagram.title else 0.0
    header_cy = dh - pad_top - title_extra - group_top_extra - max_header_h / 2.0
    y_header_bottom = header_cy - max_header_h / 2.0
    y_origin_top = y_header_bottom - group_bottom_extra - 2.0
    y_lifeline_bottom = max(pad_bottom + 2.0, y_origin_top - timeline_h - 4.0)

    # Layer 0: Diagram Background
    render_diagram_background(
        center_xy=(bx + dw / 2.0, by + dh / 2.0),
        width=dw,
        height=dh,
        style=diagram.style,
    )

    # Layer 1: Participant Groups
    render_groups(diagram.groups, participant_x_map, header_cy, (bx, by))

    # Layer 2: Blocks (loops, condition frames)
    render_blocks(diagram._blocks, block_bounds_y, participant_x_map, y_origin_top, (bx, by), diagram.participants)

    # Layer 3: Lifelines
    render_lifelines(diagram.participants, participant_x_map, y_header_bottom, y_lifeline_bottom, (bx, by))

    # Layer 4: Activation Bars
    render_activation_bars(diagram.participants, participant_x_map, resolved_acts, y_origin_top, (bx, by))

    # Layer 5: Messages and Notes
    default_msg_style = diagram.edge_style
    for event in diagram.events:
        if isinstance(event, Message):
            rel_y = event_y_map[event]
            abs_y = by + (y_origin_top - rel_y)
            render_single_message(
                event,
                abs_y,
                participant_x_map,
                (bx, by),
                default_msg_style,
                diagram.edge_text_style,
            )
        elif isinstance(event, Note):
            rel_y = event_y_map[event]
            abs_y = by + (y_origin_top - rel_y)
            render_note(event, abs_y, participant_x_map, (bx, by))

    # Layer 6: Participant Headers
    render_headers(diagram.participants, participant_x_map, header_cy, (bx, by), diagram.node_style)

    # Layer 7: Diagram Title
    if diagram.title:
        render_diagram_title(
            xy=(bx + pad_left, by + dh - pad_top - title_extra + 1.0),
            title=diagram.title,
            title_style=diagram.title_style,
            default_size=15.0,
            default_color=diagram.edge_text_style.text_color or (35, 35, 45, 1.0),
            default_halign="left",
            default_valign="bottom",
        )


# Internal re-export for diagram sizing query
_compute_diagram_size = compute_diagram_size
