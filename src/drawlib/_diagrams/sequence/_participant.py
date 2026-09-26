# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Participant class implementation for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import drawlib._diagrams.sequence._message as _message_module
import drawlib._diagrams.sequence._note as _note_module
from drawlib._diagrams.sequence._types import ArrowType, IconType, TextPosition

if TYPE_CHECKING:
    from drawlib._core.types import Style
    from drawlib._diagrams.sequence._diagram import SequenceDiagram
    from drawlib._diagrams.sequence._message import Message
    from drawlib._diagrams.sequence._note import Note


class Participant:
    """Participant in a sequence diagram with an associated vertical lifeline."""

    def __init__(
        self,
        text: str = "",
        icon: IconType = None,
        icon_size: float = 8.0,
        text_position: TextPosition = "bottom",
        text_margin: float = 2.0,
        text_size: float | None = None,
        text_angle: float = 0.0,
        style: Style | None = None,
        icon_style: Style | None = None,
        textstyle: Style | None = None,
        lifeline_style: Style | None = None,
    ) -> None:
        """Initialize Participant.

        Args:
            text: Participant display name / label.
            icon: Icon identifier (GcpIcon, PhosphorIcon, CustomIcon, or image path).
            icon_size: Size of icon in coordinate units. Defaults to 8.0.
            text_position: Placement of label relative to icon ("bottom", "top", "left", "right").
            text_margin: Clearance between icon boundary and label text. Defaults to 2.0.
            text_size: Font size in pt. If None, uses default 12.
            text_angle: Rotation angle of label text in degrees. Defaults to 0.0.
            style: Style for participant header card.
            icon_style: Style for participant icon.
            textstyle: Style for label text.
            lifeline_style: Style for vertical lifeline.
        """
        self.text = text
        self.icon = icon
        self.icon_size = float(icon_size)
        self.text_position: TextPosition = text_position
        self.text_margin = float(text_margin)
        self.text_size = float(text_size) if text_size is not None else None
        self.text_angle = float(text_angle)
        self.style = style
        self.icon_style = icon_style
        self.textstyle = textstyle
        self.lifeline_style = lifeline_style

        self._fixed_x: float | None = None
        self._diagram: SequenceDiagram | None = None
        self._activations: list[tuple[int, int | None]] = []

    def set_x(self, x: float) -> Participant:
        """Explicitly pin this participant's horizontal lifeline position.

        Args:
            x: Diagram-local X coordinate.

        Returns:
            Participant: self for method chaining.
        """
        self._fixed_x = float(x)
        return self

    def request(
        self,
        target: Participant,
        label: str = "",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Send a request message (solid line) from this participant to target.

        Args:
            target: Destination participant.
            label: Description text of the message.
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object for the message line.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.request(self, target, label=label, is_async=is_async, style=style)
        return _message_module.Message(self, target, label=label, is_reply=False, is_async=is_async, style=style)

    def reply(
        self,
        target: Participant,
        label: str = "",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Send a response/return message (dashed line) from this participant to target.

        Args:
            target: Destination participant.
            label: Description text of the response.
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object for the response line.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.reply(self, target, label=label, is_async=is_async, style=style)
        return _message_module.Message(self, target, label=label, is_reply=True, is_async=is_async, style=style)

    def connect(
        self,
        target: Participant,
        label: str = "",
        arrow: ArrowType = "->",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Connect to target with a custom arrow (e.g. bidirectional stream '<->').

        Args:
            target: Destination participant.
            label: Description text.
            arrow: Arrowhead configuration ("->", "<->", "-"). Defaults to "->".
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.connect(self, target, label=label, arrow=arrow, is_async=is_async, style=style)
        return _message_module.Message(self, target, label=label, arrow=arrow, is_async=is_async, style=style)

    def note(
        self,
        text: str,
        pos: Literal["left", "right"] = "right",
        style: Style | None = None,
    ) -> Note:
        """Attach a sticky note annotation card beside this participant's lifeline.

        Args:
            text: Note content text.
            pos: Position relative to lifeline ("left" or "right"). Defaults to "right".
            style: Optional Style object for the card.

        Returns:
            Note: Created note instance.
        """
        if self._diagram is not None:
            return self._diagram.note(text, on=self, pos=pos, style=style)
        return _note_module.Note(text, on=self, pos=pos, style=style)

    def activate(self) -> None:
        """Start an active execution span on this participant's lifeline."""
        current_step = len(self._diagram._events) if self._diagram is not None else 0
        self._activations.append((current_step, None))

    def deactivate(self) -> None:
        """End the current active execution span on this participant's lifeline."""
        current_step = len(self._diagram._events) if self._diagram is not None else 0
        for i in reversed(range(len(self._activations))):
            start, end = self._activations[i]
            if end is None:
                self._activations[i] = (start, current_step)
                break

    def get_header_size(self) -> tuple[float, float]:
        """Estimate width and height of the participant's header card."""
        font_size = self.text_size if self.text_size is not None else 12.0
        # Text dimension approximations
        lines = self.text.split("\n") if self.text else []
        max_line_len = max((len(line) for line in lines), default=0)
        text_w = max_line_len * (font_size * 0.065)
        text_h = len(lines) * (font_size * 0.18) if lines else 0.0

        if self.icon is None:
            w = max(text_w + 6.0, 16.0)
            h = max(text_h + 4.0, 8.0)
            return w, h

        # If icon exists
        if self.text_position in {"bottom", "top"}:
            w = max(self.icon_size + 4.0, text_w + 4.0)
            h = self.icon_size + self.text_margin + text_h + 2.0
        else:
            w = self.icon_size + self.text_margin + text_w + 4.0
            h = max(self.icon_size + 2.0, text_h + 2.0)
        return max(w, 16.0), max(h, 8.0)
