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

import math
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PIL.Image import Image

import drawlib._icons.font_icons.phosphor._generated as phosphor_gen
import drawlib._icons.png_icons.gcp._generated as gcp_gen
from drawlib._core.l2_models import Dimage
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Colors, Style
from drawlib._diagrams.architecture._icons import CustomIcon, GcpIcon, PhosphorIcon
from drawlib._diagrams.sequence._block import Block
from drawlib._diagrams.sequence._group import ParticipantGroup
from drawlib._diagrams.sequence._message import Message
from drawlib._diagrams.sequence._note import Note
from drawlib._diagrams.sequence._participant import Participant
from drawlib._diagrams.sequence._types import DiagramPadding, IconType, PaddingType
from drawlib.images import image as canvas_image
from drawlib.lines import line as canvas_line
from drawlib.lines import lines as canvas_lines
from drawlib.shapes import rectangle as canvas_rectangle
from drawlib.text import text as canvas_text

if TYPE_CHECKING:
    from drawlib._diagrams.sequence._diagram import Diagram


def _parse_diagram_padding(padding: DiagramPadding) -> tuple[float, float, float, float]:
    """Parse padding into (top, right, bottom, left)."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val, val, val
    return float(padding[0]), float(padding[1]), float(padding[2]), float(padding[3])


def _parse_message_padding(padding: PaddingType) -> tuple[float, float]:
    """Extract (start_pad, end_pad) from message PaddingType."""
    if isinstance(padding, (int, float)):
        val = float(padding)
        return val, val
    return float(padding[0]), float(padding[1])


def _draw_enum_icon(
    icon: GcpIcon | PhosphorIcon,
    canvas_xy: tuple[float, float],
    icon_size: float,
    applied_style: Style,
) -> None:
    """Draw a phosphor or GCP icon enum."""
    cx, cy = canvas_xy
    if isinstance(icon, PhosphorIcon):
        p_name = icon.name.lower()
        if hasattr(phosphor_gen, p_name):
            getattr(phosphor_gen, p_name)(xy=(cx, cy), width=icon_size, style=applied_style)
        else:
            canvas_rectangle(xy=(cx, cy), width=icon_size, height=icon_size, style=applied_style)
    else:
        g_name = icon.name.lower()
        if hasattr(gcp_gen, g_name):
            getattr(gcp_gen, g_name)(xy=(cx, cy), width=icon_size, style=applied_style)
        else:
            canvas_rectangle(xy=(cx, cy), width=icon_size, height=icon_size, style=applied_style)


def _draw_image_icon(
    icon: CustomIcon | Dimage | Image | str | Path,
    canvas_xy: tuple[float, float],
    icon_size: float,
    applied_style: Style,
) -> None:
    """Draw an image-based icon or file."""
    cx, cy = canvas_xy
    img: str | Dimage
    if isinstance(icon, CustomIcon):
        img = icon.dimage
    elif isinstance(icon, Image):
        img = Dimage(icon)
    elif isinstance(icon, Dimage):
        img = icon
    else:
        img = str(icon)

    canvas_image(xy=(cx, cy), image=img, width=icon_size, style=applied_style)


def _draw_icon(
    icon: IconType,
    canvas_xy: tuple[float, float],
    icon_size: float,
    icon_style: Style | None = None,
) -> None:
    """Draw icon representation at coordinate with given size."""
    if icon is None:
        return

    applied_style = icon_style if icon_style is not None else Style(line_width=0)
    if isinstance(icon, (GcpIcon, PhosphorIcon)):
        _draw_enum_icon(icon, canvas_xy, icon_size, applied_style)
    elif isinstance(icon, (CustomIcon, Dimage, Image, str, Path)):
        _draw_image_icon(icon, canvas_xy, icon_size, applied_style)
    elif callable(icon):
        icon(xy=canvas_xy, width=icon_size, style=applied_style)


def _estimate_note_size(note: Note) -> tuple[float, float]:
    """Estimate width and height of a note card."""
    lines = note.text.split("\n") if note.text else []
    max_line_len = max((len(line) for line in lines), default=0)
    card_w = max(max_line_len * 0.75 + 5.0, 14.0)
    card_h = max(len(lines) * 2.2 + 3.0, 6.0)
    return card_w, card_h


def _compute_x_coordinates(
    diagram: Diagram,
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
            _estimate_note_size(ev)[0] + 3.0
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


def _compute_timeline_y(  # noqa: C901
    diagram: Diagram,
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
    tag = event[0]
    if tag == "space" and len(event) > 1 and isinstance(event[1], (int, float)):
        return rel_y + float(event[1])
    if tag == "block_start":
        blk = event[1]
        if isinstance(blk, Block):
            block_starts[blk] = rel_y
        return rel_y + 3.0
    if tag == "block_end":
        blk = event[1]
        if isinstance(blk, Block):
            block_ends[blk] = rel_y
        return rel_y + 2.0
    return rel_y


def _resolve_activations(
    diagram: Diagram,
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


def _compute_diagram_size(diagram: Diagram) -> tuple[float, float]:
    """Compute diagram overall dimensions."""
    pad_top, pad_right, pad_bottom, pad_left = _parse_diagram_padding(diagram.padding)
    participant_x_map = _compute_x_coordinates(diagram, pad_left)

    max_x = max(participant_x_map.values(), default=50.0)
    last_participant = diagram.participants[-1] if diagram.participants else None
    last_half_w = last_participant.get_header_size()[0] / 2.0 if last_participant else 10.0
    right_group_pad = max(
        (g.padding for g in diagram.groups if last_participant and last_participant in g.participants),
        default=0.0,
    )
    right_note_w = max(
        (
            _estimate_note_size(ev)[0] + 3.0
            for ev in diagram.events
            if isinstance(ev, Note) and ev.on == last_participant and ev.pos == "right"
        ),
        default=0.0,
    )
    block_margin = 7.0 if diagram._blocks else 0.0
    right_extra = max(right_group_pad, right_note_w, block_margin)
    total_w = max_x + last_half_w + right_extra + pad_right

    max_header_h = max((p.get_header_size()[1] for p in diagram.participants), default=12.0)
    timeline_h, _, _, _ = _compute_timeline_y(diagram)
    total_h = pad_top + max_header_h + timeline_h + 8.0 + pad_bottom

    dw = diagram.width if diagram.width is not None else max(total_w, 100.0)
    dh = diagram.height if diagram.height is not None else max(total_h, 80.0)
    return dw, dh


def _render_lifelines(
    participants: list[Participant],
    participant_x_map: dict[Participant, float],
    y_header_bottom: float,
    y_lifeline_bottom: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw vertical dashed lifelines for all participants."""
    bx, by = base_xy
    default_lifeline_style = Style(
        line_color=(185, 185, 190, 1.0),
        line_width=1.0,
        line_style="dashed",
    )
    for participant in participants:
        nx = bx + participant_x_map[participant]
        applied = (
            default_lifeline_style.merge(participant.lifeline_style)
            if participant.lifeline_style
            else default_lifeline_style
        )
        canvas_line(
            xy1=(nx, by + y_header_bottom),
            xy2=(nx, by + y_lifeline_bottom),
            style=applied,
        )


def _render_activation_bars(
    participants: list[Participant],
    participant_x_map: dict[Participant, float],
    resolved_acts: dict[Participant, list[tuple[float, float]]],
    y_origin_top: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw slender execution activation rectangles along lifelines."""
    bx, by = base_xy
    act_style = Style(
        fill_color=(235, 238, 245, 0.9),
        line_color=(120, 125, 135, 1.0),
        line_width=1.0,
    )
    bar_width = 2.4

    for participant in participants:
        nx = bx + participant_x_map[participant]
        for start_rel, end_rel in resolved_acts.get(participant, []):
            y_start = by + (y_origin_top - start_rel)
            y_end = by + (y_origin_top - end_rel)
            h = abs(y_start - y_end)
            if h < 0.5:
                continue
            cy = (y_start + y_end) / 2.0
            canvas_rectangle(xy=(nx, cy), width=bar_width, height=h, style=act_style)


def _render_participant_header(
    participant: Participant,
    canvas_xy: tuple[float, float],
    header_w: float,
    header_h: float,
) -> None:
    """Render a participant's top card, icon, and label."""
    cx, cy = canvas_xy
    default_card_style = Style(
        fill_color=(255, 255, 255, 1.0),
        line_color=(150, 155, 165, 1.0),
        line_width=1.2,
    )
    card_style = default_card_style.merge(participant.style) if participant.style else default_card_style
    canvas_rectangle(xy=(cx, cy), width=header_w, height=header_h, style=card_style)

    if participant.icon is not None:
        _draw_icon(participant.icon, (cx, cy), participant.icon_size, participant.icon_style)

    if not participant.text:
        return

    font_size = participant.text_size if participant.text_size is not None else 12.0
    text_style = Style(
        text_size=font_size,
        text_font=Font.SANSSERIF_BOLD if participant.icon is None else Font.SANSSERIF_REGULAR,
        text_color=(35, 35, 40, 1.0),
        text_halign="center",
        text_valign="center",
        text_angle=participant.text_angle,
    )
    if participant.textstyle:
        text_style = text_style.merge(participant.textstyle)

    if participant.icon is None:
        canvas_text(xy=(cx, cy), text=participant.text, style=text_style)
    else:
        half_icon = participant.icon_size / 2.0
        ty = (
            cy - half_icon - participant.text_margin
            if participant.text_position == "bottom"
            else cy + half_icon + participant.text_margin
        )
        canvas_text(xy=(cx, ty), text=participant.text, style=text_style)


def _render_headers(
    participants: list[Participant],
    participant_x_map: dict[Participant, float],
    header_cy: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw all participant headers."""
    bx, by = base_xy
    for participant in participants:
        nx = bx + participant_x_map[participant]
        hw, hh = participant.get_header_size()
        _render_participant_header(participant, (nx, by + header_cy), hw, hh)


def _render_groups(
    groups: list[ParticipantGroup],
    participant_x_map: dict[Participant, float],
    header_cy: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw participant grouping boxes around header cards."""
    bx, by = base_xy
    default_group_style = Style(
        fill_color=(240, 243, 250, 0.4),
        line_color=(170, 175, 185, 1.0),
        line_width=1.0,
        line_style="dashed",
    )
    for group in groups:
        if not group.participants:
            continue
        xs = [bx + participant_x_map[p] for p in group.participants if p in participant_x_map]
        if not xs:
            continue
        half_ws = [p.get_header_size()[0] / 2.0 for p in group.participants if p in participant_x_map]
        half_hs = [p.get_header_size()[1] / 2.0 for p in group.participants if p in participant_x_map]

        min_x = min(x - hw for x, hw in zip(xs, half_ws, strict=False)) - group.padding
        max_x = max(x + hw for x, hw in zip(xs, half_ws, strict=False)) + group.padding
        max_h = max(half_hs) * 2.0 + group.padding * 2.0

        box_cx = (min_x + max_x) / 2.0
        box_cy = by + header_cy
        applied = default_group_style.merge(group.style) if group.style else default_group_style
        canvas_rectangle(xy=(box_cx, box_cy), width=max_x - min_x, height=max_h, style=applied)

        if group.title:
            title_style = Style(
                text_size=11,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(90, 95, 105, 1.0),
                text_halign="left",
                text_valign="bottom",
            )
            if group.textstyle:
                title_style = title_style.merge(group.textstyle)
            canvas_text(xy=(min_x + 2.0, box_cy + max_h / 2.0 + 1.0), text=group.title, style=title_style)


def _render_single_message(  # noqa: C901
    message: Message,
    y: float,
    participant_x_map: dict[Participant, float],
    base_xy: tuple[float, float],
    default_msg_style: Style,
) -> None:
    """Draw a single horizontal message or self-call loop."""
    bx, by = base_xy
    sx = bx + participant_x_map[message.source]
    tx = bx + participant_x_map[message.target]

    applied_style = default_msg_style.merge(message.style) if message.style else default_msg_style
    if message.is_reply:
        applied_style = applied_style.merge(Style(line_style="dashed"))

    arrowhead: Literal["", "->", "<-", "<->"]
    if message.arrow == "<->":
        arrowhead = "<->"
    elif message.arrow == "->":
        arrowhead = "->" if not message.is_async else "->"
    else:
        arrowhead = ""

    if message.is_self_call:
        _draw_self_call(sx, y, arrowhead, applied_style)
        lx = sx + 8.0
        ly = y - 2.0
    else:
        lx, ly = _draw_horizontal_message(sx, tx, y, message.padding, arrowhead, applied_style)

    if message.label:
        display_text = f"{message.number}. {message.label}" if message.number is not None else message.label
        _render_message_label(lx, ly, display_text, message.textstyle)


def _draw_horizontal_message(
    sx: float,
    tx: float,
    y: float,
    padding: PaddingType,
    arrowhead: Literal["", "->", "<-", "<->"],
    style: Style,
) -> tuple[float, float]:
    """Draw straight horizontal message line and return label coordinate."""
    sp, ep = _parse_message_padding(padding)
    dx = tx - sx
    dist = abs(dx)
    if dist > 1e-4:
        sign = 1.0 if dx > 0 else -1.0
        p0 = sx + sign * min(sp, dist * 0.4)
        p1 = tx - sign * min(ep, dist * 0.4)
    else:
        p0, p1 = sx, tx

    canvas_line(xy1=(p0, y), xy2=(p1, y), arrowhead=arrowhead, style=style)
    return (p0 + p1) / 2.0, y + 1.8


def _draw_self_call(
    sx: float,
    y: float,
    arrowhead: Literal["", "->", "<-", "<->"],
    style: Style,
) -> None:
    """Draw 3-segment self-invocation loop."""
    loop_w = 6.0
    loop_h = 5.0
    pts = [
        (sx, y),
        (sx + loop_w, y),
        (sx + loop_w, y - loop_h),
        (sx, y - loop_h),
    ]
    canvas_lines(xys=pts, arrowhead=arrowhead, style=style)


def _render_message_label(lx: float, ly: float, text: str, custom_textstyle: Style | None) -> None:
    """Draw message label with clear semi-transparent background backplate."""
    label_style = Style(
        text_size=11,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=(40, 40, 45, 1.0),
        text_bg_fill_color=(255, 255, 255, 0.95),
        text_bg_line_color=None,
        text_bg_line_width=0,
        text_halign="center",
        text_valign="center",
    )
    if custom_textstyle:
        label_style = label_style.merge(custom_textstyle)
    canvas_text(xy=(lx, ly), text=text, style=label_style)


def _render_note(
    note: Note,
    y: float,
    participant_x_map: dict[Participant, float],
    base_xy: tuple[float, float],
) -> None:
    """Draw a sticky note annotation card."""
    bx, by = base_xy
    default_note_style = Style(
        fill_color=(255, 252, 235, 0.95),
        line_color=(220, 210, 160, 1.0),
        line_width=1.0,
    )
    applied_style = default_note_style.merge(note.style) if note.style else default_note_style

    card_w, card_h = _estimate_note_size(note)

    if note.over and len(note.over) >= 2:
        xs = [bx + participant_x_map[p] for p in note.over if p in participant_x_map]
        card_w = max(max(xs) - min(xs) + 8.0, card_w)
        cx = (min(xs) + max(xs)) / 2.0
    elif note.on:
        nx = bx + participant_x_map[note.on]
        cx = nx + card_w / 2.0 + 3.0 if note.pos == "right" else nx - card_w / 2.0 - 3.0
    else:
        cx = bx + 30.0

    canvas_rectangle(xy=(cx, y), width=card_w, height=card_h, style=applied_style)

    text_style = Style(
        text_size=10,
        text_font=Font.SANSSERIF_REGULAR,
        text_color=(60, 55, 45, 1.0),
        text_halign="center",
        text_valign="center",
    )
    if note.textstyle:
        text_style = text_style.merge(note.textstyle)
    canvas_text(xy=(cx, y), text=note.text, style=text_style)


def _render_blocks(
    blocks: list[Block],
    block_bounds_y: dict[Block, tuple[float, float]],
    participant_x_map: dict[Participant, float],
    y_origin_top: float,
    base_xy: tuple[float, float],
    participants: list[Participant],
) -> None:
    """Draw framing boundary rectangles and header tabs for condition/loop blocks."""
    bx, by = base_xy
    default_block_style = Style(
        fill_color=(245, 247, 252, 0.25),
        line_color=(165, 175, 195, 1.0),
        line_width=1.0,
        line_style="dashed",
    )

    for block in blocks:
        start_rel, end_rel = block_bounds_y.get(block, (0.0, 10.0))
        y_top = by + (y_origin_top - start_rel)
        y_bot = by + (y_origin_top - end_rel)
        bh = max(abs(y_top - y_bot), 6.0)
        cy = (y_top + y_bot) / 2.0

        involved = block.involved_participants if block.involved_participants else set(participants)
        xs = [bx + participant_x_map[p] for p in involved if p in participant_x_map]
        if not xs:
            xs = [bx + x for x in participant_x_map.values()]

        min_x = min(xs) - 7.0
        max_x = max(xs) + 7.0
        bw = max_x - min_x
        cx = (min_x + max_x) / 2.0

        applied = default_block_style.merge(block.style) if block.style else default_block_style
        canvas_rectangle(xy=(cx, cy), width=bw, height=bh, style=applied)

        # Draw header tab box
        tag = f"[{block.block_type.upper()}] {block.label}" if block.label else f"[{block.block_type.upper()}]"
        tab_w = max(len(tag) * 0.7 + 3.0, 8.0)
        tab_h = 3.0
        tab_cx = min_x + tab_w / 2.0
        tab_cy = y_top - tab_h / 2.0
        canvas_rectangle(
            xy=(tab_cx, tab_cy),
            width=tab_w,
            height=tab_h,
            style=Style(fill_color=(235, 240, 250, 0.95), line_color=(165, 175, 195, 1.0), line_width=1.0),
        )
        canvas_text(
            xy=(tab_cx, tab_cy),
            text=tag,
            style=Style(
                text_size=9,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(60, 70, 90, 1.0),
                text_halign="center",
                text_valign="center",
            ),
        )


def draw_sequence_diagram(diagram: Diagram, xy: tuple[float, float] = (0.0, 0.0)) -> None:
    """Execute complete 2-pass drawing pipeline for a sequence diagram."""
    bx, by = float(xy[0]), float(xy[1])
    pad_top, pad_right, pad_bottom, pad_left = _parse_diagram_padding(diagram.padding)

    dw, dh = _compute_diagram_size(diagram)
    participant_x_map = _compute_x_coordinates(diagram, pad_left)
    timeline_h, event_y_map, block_bounds_y, resolved_acts = _compute_timeline_y(diagram)

    max_header_h = max((p.get_header_size()[1] for p in diagram.participants), default=12.0)
    header_cy = dh - pad_top - max_header_h / 2.0
    y_header_bottom = header_cy - max_header_h / 2.0
    y_origin_top = y_header_bottom
    y_lifeline_bottom = pad_bottom + 2.0

    # Layer 0: Diagram Background
    if diagram.style:
        canvas_rectangle(xy=(bx + dw / 2.0, by + dh / 2.0), width=dw, height=dh, style=diagram.style)

    # Layer 1: Participant Groups
    _render_groups(diagram.groups, participant_x_map, header_cy, (bx, by))

    # Layer 2: Blocks (loops, condition frames)
    _render_blocks(diagram._blocks, block_bounds_y, participant_x_map, y_origin_top, (bx, by), diagram.participants)

    # Layer 3: Lifelines
    _render_lifelines(diagram.participants, participant_x_map, y_header_bottom, y_lifeline_bottom, (bx, by))

    # Layer 4: Activation Bars
    _render_activation_bars(diagram.participants, participant_x_map, resolved_acts, y_origin_top, (bx, by))

    # Layer 5: Messages and Notes
    default_msg_style = Style(line_color=(60, 60, 65, 1.0), line_width=1.5)
    for event in diagram.events:
        if isinstance(event, Message):
            rel_y = event_y_map[event]
            abs_y = by + (y_origin_top - rel_y)
            _render_single_message(event, abs_y, participant_x_map, (bx, by), default_msg_style)
        elif isinstance(event, Note):
            rel_y = event_y_map[event]
            abs_y = by + (y_origin_top - rel_y)
            _render_note(event, abs_y, participant_x_map, (bx, by))

    # Layer 6: Participant Headers
    _render_headers(diagram.participants, participant_x_map, header_cy, (bx, by))

    # Layer 7: Diagram Title
    if diagram.title:
        title_style = Style(
            text_size=15,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(35, 35, 45, 1.0),
            text_halign="left",
            text_valign="bottom",
        )
        if diagram.title_style:
            title_style = title_style.merge(diagram.title_style)
        canvas_text(xy=(bx + pad_left, by + dh - pad_top + 2.0), text=diagram.title, style=title_style)
