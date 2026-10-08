# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Element rendering functions for sequence diagrams."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import line as canvas_line
from drawlib._core.l4_canvas import lines as canvas_lines
from drawlib._core.l4_canvas import rectangle as canvas_rectangle
from drawlib._core.l4_canvas import text as canvas_text
from drawlib._diagrams._common import (
    draw_diagram_icon,
    draw_image_icon,
)
from drawlib._diagrams._common import (
    draw_enum_icon as _common_draw_enum_icon,
)
from drawlib._diagrams.architecture._icons import GcpIcon, PhosphorIcon
from drawlib._diagrams.sequence._block import Block
from drawlib._diagrams.sequence._group import ParticipantGroup
from drawlib._diagrams.sequence._layout import estimate_note_size, parse_message_padding
from drawlib._diagrams.sequence._message import Message
from drawlib._diagrams.sequence._note import Note
from drawlib._diagrams.sequence._participant import Participant
from drawlib._diagrams.sequence._types import IconType, PaddingType


def draw_enum_icon(
    icon: GcpIcon | PhosphorIcon,
    canvas_xy: tuple[float, float],
    icon_size: float,
    applied_style: Style,
) -> None:
    """Draw a phosphor or GCP icon enum."""
    _common_draw_enum_icon(icon, canvas_xy, icon_size, applied_style, fallback_box=True)


def draw_icon(
    icon: IconType,
    canvas_xy: tuple[float, float],
    icon_size: float,
    icon_style: Style | None = None,
) -> None:
    """Draw icon representation at coordinate with given size."""
    draw_diagram_icon(icon, canvas_xy, icon_size, icon_style, fallback_box=True)


def render_lifelines(
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
        if not participant.show:
            continue
        nx = bx + participant_x_map[participant]
        applied = default_lifeline_style.patch(participant.lifeline_style)
        canvas_line(
            xy1=(nx, by + y_header_bottom),
            xy2=(nx, by + y_lifeline_bottom),
            style=applied,
        )


def render_activation_bars(
    participants: list[Participant],
    participant_x_map: dict[Participant, float],
    resolved_acts: dict[Participant, list[tuple[float, float]]],
    y_origin_top: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw slender execution activation rectangles along lifelines."""
    bx, by = base_xy
    act_style = Style(
        shape_fill_color=(235, 238, 245, 0.9),
        shape_line_color=(120, 125, 135, 1.0),
        shape_line_width=1.0,
    )
    bar_width = 2.4

    for participant in participants:
        if not participant.show:
            continue
        nx = bx + participant_x_map[participant]
        for start_rel, end_rel in resolved_acts.get(participant, []):
            y_start = by + (y_origin_top - start_rel)
            y_end = by + (y_origin_top - end_rel)
            h = abs(y_start - y_end)
            if h < 0.5:
                continue
            cy = (y_start + y_end) / 2.0
            canvas_rectangle(xy=(nx, cy), width=bar_width, height=h, style=act_style)


def render_participant_header(
    participant: Participant,
    canvas_xy: tuple[float, float],
    header_w: float,
    header_h: float,
    default_node_style: Style,
) -> None:
    """Render a participant's top card, icon, and label."""
    cx, cy = canvas_xy
    card_style = default_node_style.patch(participant.style) if participant.style is not None else default_node_style
    canvas_rectangle(xy=(cx, cy), width=header_w, height=header_h, style=card_style)

    if participant.icon is not None:
        draw_icon(participant.icon, (cx, cy), participant.icon_size, participant.icon_style)

    if not participant.text:
        return

    font_size = (
        float(participant.text_style.text_size)
        if participant.text_style and participant.text_style.text_size is not None
        else 12.0
    )
    text_color = card_style.text_color or (35, 35, 40, 1.0)
    text_style = Style(
        text_size=font_size,
        text_font=Font.SANSSERIF_BOLD if participant.icon is None else Font.SANSSERIF_REGULAR,
        text_color=text_color,
        text_halign="center",
        text_valign="center",
        angle=participant.text_angle,
    )
    if participant.text_style:
        text_style = text_style.patch(participant.text_style)

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


def render_headers(
    participants: list[Participant],
    participant_x_map: dict[Participant, float],
    header_cy: float,
    base_xy: tuple[float, float],
    default_node_style: Style,
) -> None:
    """Draw all participant headers."""
    bx, by = base_xy
    for participant in participants:
        if not participant.show:
            continue
        nx = bx + participant_x_map[participant]
        hw, hh = participant.get_header_size()
        render_participant_header(participant, (nx, by + header_cy), hw, hh, default_node_style)


def render_groups(
    groups: list[ParticipantGroup],
    participant_x_map: dict[Participant, float],
    header_cy: float,
    base_xy: tuple[float, float],
) -> None:
    """Draw participant grouping boxes around header cards."""
    bx, by = base_xy
    default_group_style = Style(
        shape_fill_color=(240, 243, 250, 0.4),
        shape_line_color=(170, 175, 185, 1.0),
        shape_line_width=1.0,
        shape_line_style="dashed",
    )
    for group in groups:
        if not group.show or not group.participants:
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
        applied = default_group_style.patch(group.style)
        canvas_rectangle(xy=(box_cx, box_cy), width=max_x - min_x, height=max_h, style=applied)

        if group.title:
            title_style = Style(
                text_size=11,
                text_font=Font.SANSSERIF_BOLD,
                text_color=(90, 95, 105, 1.0),
                text_halign="left",
                text_valign="bottom",
            )
            if group.text_style:
                title_style = title_style.patch(group.text_style)
            canvas_text(xy=(min_x + 2.0, box_cy + max_h / 2.0 + 1.0), text=group.title, style=title_style)


def render_single_message(  # noqa: C901
    message: Message,
    y: float,
    participant_x_map: dict[Participant, float],
    base_xy: tuple[float, float],
    default_msg_style: Style,
    default_edge_text_style: Style,
) -> None:
    """Draw a single horizontal message or self-call loop."""
    if not message.show or not message.source.show or not message.target.show:
        return
    bx, _ = base_xy
    sx = bx + participant_x_map[message.source]
    tx = bx + participant_x_map[message.target]

    applied_style = default_msg_style.patch(message.style)
    if message.is_reply:
        applied_style = applied_style.patch(line_style="dashed")

    arrow_head: Literal["", "->", "<-", "<->"]
    if message.arrow == "<->":
        arrow_head = "<->"
    elif message.arrow == "->":
        arrow_head = "->" if not message.is_async else "->"
    else:
        arrow_head = ""

    if message.is_self_call:
        draw_self_call(sx, y, arrow_head, applied_style)
        lx = sx + 8.0
        ly = y - 2.0
    else:
        lx, ly = draw_horizontal_message(sx, tx, y, message.padding, arrow_head, applied_style)

    if message.label:
        display_text = f"{message.number}. {message.label}" if message.number is not None else message.label
        render_message_label(lx, ly, display_text, message.text_style, default_edge_text_style)


def draw_horizontal_message(
    sx: float,
    tx: float,
    y: float,
    padding: PaddingType,
    arrow_head: Literal["", "->", "<-", "<->"],
    style: Style,
) -> tuple[float, float]:
    """Draw straight horizontal message line and return label coordinate."""
    sp, ep = parse_message_padding(padding)
    dx = tx - sx
    dist = abs(dx)
    if dist > 1e-4:
        sign = 1.0 if dx > 0 else -1.0
        p0 = sx + sign * min(sp, dist * 0.4)
        p1 = tx - sign * min(ep, dist * 0.4)
    else:
        p0, p1 = sx, tx

    canvas_line(xy1=(p0, y), xy2=(p1, y), arrow_head=arrow_head, style=style)
    return (p0 + p1) / 2.0, y + 2.5


def draw_self_call(
    sx: float,
    y: float,
    arrow_head: Literal["", "->", "<-", "<->"],
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
    canvas_lines(xys=pts, arrow_head=arrow_head, style=style)


def render_message_label(
    lx: float,
    ly: float,
    text: str,
    custom_text_style: Style | None,
    default_edge_text_style: Style,
) -> None:
    """Draw message label resting cleanly above the message arrow."""
    base_label_style = Style(
        text_size=10,
        text_font=Font.SANSSERIF_REGULAR,
        text_halign="center",
        text_valign="bottom",
    )
    applied_text_style = custom_text_style or default_edge_text_style
    label_style = base_label_style.patch(applied_text_style)
    canvas_text(xy=(lx, ly), text=text, style=label_style)


def render_note(
    note: Note,
    y: float,
    participant_x_map: dict[Participant, float],
    base_xy: tuple[float, float],
) -> None:
    """Draw a sticky note annotation card."""
    if not note.show:
        return
    if note.on is not None and not note.on.show:
        return
    if note.over is not None and any(not p.show for p in note.over):
        return
    bx, _ = base_xy
    default_note_style = Style(
        shape_fill_color=(255, 252, 235, 0.95),
        shape_line_color=(220, 210, 160, 1.0),
        shape_line_width=1.0,
    )
    applied_style = default_note_style.patch(note.style)

    card_w, card_h = estimate_note_size(note)

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
    if note.text_style:
        text_style = text_style.patch(note.text_style)
    canvas_text(xy=(cx, y), text=note.text, style=text_style)


def render_blocks(
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
        shape_fill_color=(245, 247, 252, 0.25),
        shape_line_color=(165, 175, 195, 1.0),
        shape_line_width=1.0,
        shape_line_style="dashed",
    )

    for block in blocks:
        if not block.show:
            continue
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

        applied = default_block_style.patch(block.style)
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
            style=Style(
                shape_fill_color=(235, 240, 250, 0.95),
                shape_line_color=(165, 175, 195, 1.0),
                shape_line_width=1.0,
            ),
        )
        block_text_style = Style(
            text_size=9,
            text_font=Font.SANSSERIF_BOLD,
            text_color=(60, 70, 90, 1.0),
            text_halign="center",
            text_valign="center",
        )
        if block.text_style:
            block_text_style = block_text_style.patch(block.text_style)
        canvas_text(
            xy=(tab_cx, tab_cy),
            text=tag,
            style=block_text_style,
        )


__all__ = [
    "draw_enum_icon",
    "draw_horizontal_message",
    "draw_icon",
    "draw_image_icon",
    "draw_self_call",
    "render_activation_bars",
    "render_blocks",
    "render_groups",
    "render_headers",
    "render_lifelines",
    "render_message_label",
    "render_note",
    "render_participant_header",
    "render_single_message",
]
