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
from drawlib._diagrams.sequence._types import ArrowType, IconType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._diagram import SequenceDiagram
    from drawlib._diagrams.sequence._message import Message
    from drawlib._diagrams.sequence._note import Note


class Participant:
    """Participant in a sequence diagram with an associated vertical lifeline."""

    def __init__(
        self,
        card_size: tuple[float, float],
        text: str = "",
        icon: IconType = None,
        icon_size: float = 8.0,
        style: Style | None = None,
        text_style: Style | None = None,
        card_style: Style | None = None,
        lifeline_style: Style | None = None,
        show: bool = True,
    ) -> None:
        """Initialize Participant.

        Args:
            card_size: (width, height) dimensions of the participant header card.
            text: Participant display name / label.
            icon: Icon identifier (GcpIcon, PhosphorIcon, CustomIcon, Dimage, PIL Image, path, or function).
            icon_size: Size of icon in coordinate units. Defaults to 8.0.
            style: Optional Style for participant icon or image.
            text_style: Optional Style for label text.
            card_style: Optional Style for participant header card background/border.
            lifeline_style: Style for vertical lifeline.
            show: Whether to render this participant and its lifeline. Defaults to True.
        """
        self.card_size: tuple[float, float] = (float(card_size[0]), float(card_size[1]))
        self.text = text
        self.icon = icon
        self.icon_size = float(icon_size)
        self.style = style
        self.text_style = text_style
        self.card_style = card_style
        self.lifeline_style = lifeline_style
        self.show = bool(show)

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
        text_style: Style | None = None,
        show: bool = True,
    ) -> Message:
        """Send a request message (solid line) from this participant to target.

        Args:
            target: Destination participant.
            label: Description text of the message.
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object for the message line.
            text_style: Optional Style object for the label text.
            show: Whether to render this message. Defaults to True.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.request(
                self, target, label=label, is_async=is_async, style=style, text_style=text_style, show=show
            )
        return _message_module.Message(
            self,
            target,
            label=label,
            is_reply=False,
            is_async=is_async,
            style=style,
            text_style=text_style,
            show=show,
        )

    def reply(
        self,
        target: Participant,
        label: str = "",
        is_async: bool = False,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> Message:
        """Send a response/return message (dashed line) from this participant to target.

        Args:
            target: Destination participant.
            label: Description text of the response.
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object for the response line.
            text_style: Optional Style object for the label text.
            show: Whether to render this message. Defaults to True.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.reply(
                self, target, label=label, is_async=is_async, style=style, text_style=text_style, show=show
            )
        return _message_module.Message(
            self,
            target,
            label=label,
            is_reply=True,
            is_async=is_async,
            style=style,
            text_style=text_style,
            show=show,
        )

    def connect(
        self,
        target: Participant,
        label: str = "",
        arrow: ArrowType = "->",
        is_async: bool = False,
        style: Style | None = None,
        text_style: Style | None = None,
        show: bool = True,
    ) -> Message:
        """Connect to target with a custom arrow (e.g. bidirectional stream '<->').

        Args:
            target: Destination participant.
            label: Description text.
            arrow: Arrowhead configuration ("->", "<->", "-"). Defaults to "->".
            is_async: True for open stick arrow; False for solid filled arrow. Defaults to False.
            style: Optional Style object.
            text_style: Optional Style object for the label text.
            show: Whether to render this message. Defaults to True.

        Returns:
            Message: Created message.
        """
        if self._diagram is not None:
            return self._diagram.connect(
                self,
                target,
                label=label,
                arrow=arrow,
                is_async=is_async,
                style=style,
                text_style=text_style,
                show=show,
            )
        return _message_module.Message(
            self,
            target,
            label=label,
            arrow=arrow,
            is_async=is_async,
            style=style,
            text_style=text_style,
            show=show,
        )

    def note(
        self,
        text: str,
        pos: Literal["left", "right"] = "right",
        style: Style | None = None,
        show: bool = True,
    ) -> Note:
        """Attach a sticky note annotation card beside this participant's lifeline.

        Args:
            text: Note content text.
            pos: Position relative to lifeline ("left" or "right"). Defaults to "right".
            style: Optional Style object for the card.
            show: Whether to render this note. Defaults to True.

        Returns:
            Note: Created note instance.
        """
        if self._diagram is not None:
            return self._diagram.note(text, on=self, pos=pos, style=style, show=show)
        return _note_module.Note(text, on=self, pos=pos, style=style, show=show)

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
        """Get width and height of the participant's header card."""
        return self.card_size

    def get_size(self) -> tuple[float, float]:
        """Get width and height of the participant's header card."""
        return self.card_size
