# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Layout and coordinate computation engine for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams.sequence._block import Block
from drawlib._diagrams.sequence._message import Message
from drawlib._diagrams.sequence._note import Note
from drawlib._diagrams.sequence._participant import Participant
from drawlib._diagrams.sequence._types import PaddingType

if TYPE_CHECKING:
    from drawlib._diagrams.sequence._diagram import SequenceDiagram


def parse_message_padding(padding: PaddingType) -> tuple[float, float]:
    """Extract (start_pad, end_pad) from message PaddingType."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val
    return float(padding[0]), float(padding[1])


def estimate_note_size(note: Note) -> tuple[float, float]:
    """Estimate width and height of a note card."""
    lines = note.text.split("\n") if note.text else []
    max_line_len = max((len(line) for line in lines), default=0)
    card_w = max(max_line_len * 0.75 + 5.0, 14.0)
    card_h = max(len(lines) * 2.2 + 3.0, 6.0)
    return card_w, card_h


def compute_x_coordinates(
    diagram: SequenceDiagram,
    pad_left: float,
) -> dict[Participant, float]:
    """Calculate X position for each participant lifeline."""
    participant_x_map: dict[Participant, float] = {}

    first_participant = diagram.participants[0] if diagram.participants else None
    left_group_pad = max(
        (g.padding for g in diagram.groups if first_participant and first_participant in g.participants),
        default=0.0,
    )
    left_note_w = max(
        (
            estimate_note_size(ev)[0] + 3.0
            for ev in diagram.events
            if isinstance(ev, Note) and ev.on == first_participant and ev.pos == "left"
        ),
        default=0.0,
    )
    block_margin = 7.0 if diagram._blocks else 0.0
    left_extra = max(left_group_pad, left_note_w, block_margin)

    current_x = pad_left + left_extra

    for i, participant in enumerate(diagram.participants):
        if participant._fixed_x is not None:
            participant_x_map[participant] = participant._fixed_x
            current_x = max(current_x, participant._fixed_x + diagram.col_width)
            continue

        header_w, _ = participant.get_header_size()
        half_w = header_w / 2.0
        if i == 0:
            current_x += half_w
            participant_x_map[participant] = current_x
        else:
            prev_participant = diagram.participants[i - 1]
            prev_half_w = prev_participant.get_header_size()[0] / 2.0
            gap = max(diagram.col_width, prev_half_w + half_w + 4.0)
            current_x += gap
            participant_x_map[participant] = current_x

    return participant_x_map


def compute_timeline_y(  # noqa: C901
    diagram: SequenceDiagram,
) -> tuple[
    float,
    dict[object, float],
    dict[Block, tuple[float, float]],
    dict[Participant, list[tuple[float, float]]],
]:
    """Compute relative Y positions from top for events, blocks, and activations.

    Returns:
        Tuple of (total_timeline_h, event_y_map, block_bounds_y, resolved_activations).
    """
    event_y_map: dict[object, float] = {}
    block_starts: dict[Block, float] = {}
    block_ends: dict[Block, float] = {}
    step_y_record: list[float] = []

    rel_y = 0.0

    for event in diagram.events:
        if isinstance(event, Message):
            rel_y = _advance_message_step(event, rel_y, diagram.step_y, event_y_map, step_y_record)
        elif isinstance(event, Note):
            rel_y = _advance_note_step(event, rel_y, event_y_map, step_y_record)
        elif isinstance(event, tuple):
            rel_y = _handle_tuple_event(event, rel_y, block_starts, block_ends)

    block_bounds_y: dict[Block, tuple[float, float]] = {}
    for block in diagram._blocks:
        start_y = block_starts.get(block, 0.0)
        end_y = block_ends.get(block, rel_y)
        block_bounds_y[block] = (start_y, end_y)

    resolved_activations = _resolve_activations(diagram, step_y_record, rel_y)
    return rel_y, event_y_map, block_bounds_y, resolved_activations


def _advance_message_step(
    message: Message,
    rel_y: float,
    step_y: float,
    event_y_map: dict[object, float],
    step_y_record: list[float],
) -> float:
    """Advance timeline for a message."""
    if message.is_self_call:
        advance = step_y * 1.8
    else:
        lines = message.label.count("\n") + 1 if message.label else 1
        advance = step_y + (lines - 1) * 2.5

    event_y_map[message] = rel_y + advance * 0.4
    step_y_record.append(event_y_map[message])
    return rel_y + advance


def _advance_note_step(
    note: Note,
    rel_y: float,
    event_y_map: dict[object, float],
    step_y_record: list[float],
) -> float:
    """Advance timeline for a note card."""
    lines = note.text.count("\n") + 1 if note.text else 1
    note_h = max(lines * 2.2 + 3.0, 6.0)
    event_y_map[note] = rel_y + note_h * 0.5
    step_y_record.append(event_y_map[note])
    return rel_y + note_h + 2.0


def _handle_tuple_event(
    event: tuple[object, ...],
    rel_y: float,
    block_starts: dict[Block, float],
    block_ends: dict[Block, float],
) -> float:
    """Handle spacer and block boundary timeline events."""
    if not event:
        return rel_y
    tag = event[0]
    if tag == "space" and len(event) > 1 and isinstance(event[1], (int, float)):
        return rel_y + float(event[1])
    if tag == "block_start" and len(event) > 1:
        blk = event[1]
        if isinstance(blk, Block):
            block_starts[blk] = rel_y
        return rel_y + 5.5
    if tag == "block_end" and len(event) > 1:
        blk = event[1]
        if isinstance(blk, Block):
            block_ends[blk] = rel_y
        return rel_y + 3.0
    return rel_y


def _resolve_activations(
    diagram: SequenceDiagram,
    step_y_record: list[float],
    total_rel_y: float,
) -> dict[Participant, list[tuple[float, float]]]:
    """Map activation step indices to relative Y coordinates."""
    resolved: dict[Participant, list[tuple[float, float]]] = {}
    for participant in diagram.participants:
        acts: list[tuple[float, float]] = []
        for start_idx, end_idx in participant._activations:
            sy = step_y_record[start_idx] if 0 <= start_idx < len(step_y_record) else 0.0
            if end_idx is not None and 0 <= end_idx < len(step_y_record):
                ey = step_y_record[end_idx]
            else:
                ey = total_rel_y
            acts.append((sy, ey))
        resolved[participant] = acts
    return resolved


def compute_diagram_size(diagram: SequenceDiagram) -> tuple[float, float]:
    """Compute diagram overall dimensions."""
    pad_top = pad_right = pad_bottom = pad_left = float(diagram.margin)
    participant_x_map = compute_x_coordinates(diagram, pad_left)

    max_x = max(participant_x_map.values(), default=50.0)
    last_participant = diagram.participants[-1] if diagram.participants else None
    last_half_w = last_participant.get_header_size()[0] / 2.0 if last_participant else 10.0
    right_group_pad = max(
        (g.padding for g in diagram.groups if last_participant and last_participant in g.participants),
        default=0.0,
    )
    right_note_w = max(
        (
            estimate_note_size(ev)[0] + 3.0
            for ev in diagram.events
            if isinstance(ev, Note) and ev.on == last_participant and ev.pos == "right"
        ),
        default=0.0,
    )
    block_margin = 7.0 if diagram._blocks else 0.0
    right_extra = max(right_group_pad, right_note_w, block_margin)
    total_w = max_x + last_half_w + right_extra + pad_right

    max_header_h = max((p.get_header_size()[1] for p in diagram.participants), default=12.0)
    group_top_extra = max((g.padding + (5.0 if g.title else 0.0) for g in diagram.groups), default=0.0)
    group_bottom_extra = max((g.padding for g in diagram.groups), default=0.0)
    title_extra = 6.0 if diagram.title else 0.0
    timeline_h, _, _, _ = compute_timeline_y(diagram)
    total_h = (
        pad_top + title_extra + group_top_extra + max_header_h + group_bottom_extra + timeline_h + 8.0 + pad_bottom
    )

    dw = diagram.width if diagram.width is not None else total_w
    dh = diagram.height if diagram.height is not None else total_h
    return dw, dh
