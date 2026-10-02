# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""SequenceDiagram container class implementation for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

import drawlib._diagrams.sequence._block as _block_module
import drawlib._diagrams.sequence._message as _message_module
import drawlib._diagrams.sequence._note as _note_module
import drawlib._diagrams.sequence._renderer as _renderer_module
from drawlib._diagrams.sequence._types import ArrowType, DiagramPadding, NotePosition

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._block import Block
    from drawlib._diagrams.sequence._group import ParticipantGroup
    from drawlib._diagrams.sequence._message import Message
    from drawlib._diagrams.sequence._note import Note
    from drawlib._diagrams.sequence._participant import Participant


class SequenceDiagram:
    """Top-level container and timeline manager for sequence diagrams."""

    def __init__(
        self,
        title: str = "",
        autonumber: bool = False,
        width: float | None = None,
        height: float | None = None,
        col_width: float = 20.0,
        step_y: float = 7.0,
        padding: DiagramPadding = 5.0,
        style: Style | None = None,
        title_style: Style | None = None,
    ) -> None:
        """Initialize SequenceDiagram.

        Args:
            title: Diagram title.
            autonumber: Whether to automatically number message arrows (1, 2, 3...).
            width: Optional fixed width of the diagram canvas area.
            height: Optional fixed height of the diagram canvas area.
            col_width: Default horizontal spacing between participant lifelines. Defaults to 20.0.
            step_y: Default vertical advance per timeline message step. Defaults to 7.0.
            padding: Margin clearance (float or (top, right, bottom, left) tuple). Defaults to 5.0.
            style: Style for diagram background.
            title_style: Style for title text.
        """
        self.title = title
        self.autonumber = autonumber
        self.width = float(width) if width is not None else None
        self.height = float(height) if height is not None else None
        self.col_width = float(col_width)
        self.step_y = float(step_y)
        self.padding = padding
        self.style = style
        self.title_style = title_style

        self._participants: list[Participant] = []
        self._groups: list[ParticipantGroup] = []
        self._events: list[object] = []
        self._blocks: list[Block] = []
        self._active_blocks: list[Block] = []
        self._message_counter = 0

    @property
    def participants(self) -> list[Participant]:
        """Get the ordered list of participants in this diagram."""
        return list(self._participants)

    @property
    def groups(self) -> list[ParticipantGroup]:
        """Get the participant grouping boxes in this diagram."""
        return list(self._groups)

    @property
    def events(self) -> list[object]:
        """Get the timeline event sequence in declaration order."""
        return list(self._events)

    def add(self, participant: Participant, x: float | None = None) -> Participant:
        """Add a participant to the diagram.

        Args:
            participant: Participant instance.
            x: Optional explicitly fixed X coordinate for this participant.

        Returns:
            Participant: The added participant for assignment or chaining.
        """
        if participant not in self._participants:
            self._participants.append(participant)
        participant._diagram = self
        if x is not None:
            participant._fixed_x = float(x)
        return participant

    def add_group(self, group: ParticipantGroup) -> ParticipantGroup:
        """Add a participant header boundary box.

        Args:
            group: ParticipantGroup instance.

        Returns:
            ParticipantGroup: The added group.
        """
        if group not in self._groups:
            self._groups.append(group)
        group._diagram = self
        for p in group.participants:
            if p not in self._participants:
                self.add(p)
        return group

    def request(
        self,
        source: Participant,
        target: Participant,
        label: str = "",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Record a synchronous or asynchronous request message (solid line).

        Args:
            source: Calling participant.
            target: Destination participant.
            label: Text label describing the message.
            is_async: True for open stick arrow; False for solid triangular arrow. Defaults to False.
            style: Optional line Style.

        Returns:
            Message: Created message.
        """
        message = _message_module.Message(
            source=source,
            target=target,
            label=label,
            is_reply=False,
            is_async=is_async,
            arrow="->",
            style=style,
        )
        self._record_message(message)
        return message

    def reply(
        self,
        source: Participant,
        target: Participant,
        label: str = "",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Record a response/return message (dashed line).

        Args:
            source: Responding participant.
            target: Destination participant.
            label: Text label describing the reply.
            is_async: True for open stick arrow; False for solid triangular arrow. Defaults to False.
            style: Optional line Style.

        Returns:
            Message: Created message.
        """
        message = _message_module.Message(
            source=source,
            target=target,
            label=label,
            is_reply=True,
            is_async=is_async,
            arrow="->",
            style=style,
        )
        self._record_message(message)
        return message

    def connect(
        self,
        source: Participant,
        target: Participant,
        label: str = "",
        arrow: ArrowType = "->",
        is_async: bool = False,
        style: Style | None = None,
    ) -> Message:
        """Record a custom connection message (e.g. bidirectional stream '<->').

        Args:
            source: Source participant.
            target: Target participant.
            label: Text label.
            arrow: Arrowhead configuration ("->", "<->", "-"). Defaults to "->".
            is_async: True for open stick arrow; False for solid triangular arrow. Defaults to False.
            style: Optional line Style.

        Returns:
            Message: Created message.
        """
        message = _message_module.Message(
            source=source,
            target=target,
            label=label,
            is_reply=False,
            is_async=is_async,
            arrow=arrow,
            style=style,
        )
        self._record_message(message)
        return message

    def note(
        self,
        text: str,
        on: Participant | None = None,
        over: list[Participant] | None = None,
        pos: NotePosition = "right",
        style: Style | None = None,
    ) -> Note:
        """Record a sticky note annotation at the current timeline step.

        Args:
            text: Note content text.
            on: Single participant to attach note to.
            over: List of participants to span note across.
            pos: Position relative to lifeline ("left", "right", "over"). Defaults to "right".
            style: Optional Style for note card.

        Returns:
            Note: Created note instance.
        """
        note_item = _note_module.Note(text=text, on=on, over=over, pos=pos, style=style)
        note_item._diagram = self
        self._events.append(note_item)
        for block in self._active_blocks:
            if on is not None:
                block.involved_participants.add(on)
            if over is not None:
                block.involved_participants.update(over)
        return note_item

    def loop(self, label: str = "") -> Block:
        """Create a loop block context manager for repeated steps.

        Args:
            label: Condition or description text.

        Returns:
            Block: Context manager.
        """
        return _block_module.Block("loop", label=label, diagram=self)

    def alt(self, label: str = "") -> Block:
        """Create an alt block context manager for alternative conditional branches.

        Args:
            label: Condition text.

        Returns:
            Block: Context manager.
        """
        return _block_module.Block("alt", label=label, diagram=self)

    def else_(self, label: str = "") -> Block:
        """Create an else branch block context manager.

        Args:
            label: Condition or description text.

        Returns:
            Block: Context manager.
        """
        return _block_module.Block("else", label=label, diagram=self)

    def opt(self, label: str = "") -> Block:
        """Create an optional execution block context manager.

        Args:
            label: Condition text.

        Returns:
            Block: Context manager.
        """
        return _block_module.Block("opt", label=label, diagram=self)

    def par(self, label: str = "") -> Block:
        """Create a parallel execution block context manager.

        Args:
            label: Description text.

        Returns:
            Block: Context manager.
        """
        return _block_module.Block("par", label=label, diagram=self)

    def space(self, dy: float = 5.0) -> None:
        """Advance timeline vertically by an extra distance for spacing.

        Args:
            dy: Vertical distance to advance. Defaults to 5.0.
        """
        self._events.append(("space", float(dy)))

    def _record_message(self, message: Message) -> None:
        """Internal helper to record a message and register participants."""
        if message.source not in self._participants:
            self.add(message.source)
        if message.target not in self._participants:
            self.add(message.target)

        message._diagram = self
        if self.autonumber:
            self._message_counter += 1
            message.number = self._message_counter

        self._events.append(message)
        for block in self._active_blocks:
            block.involved_participants.add(message.source)
            block.involved_participants.add(message.target)

    def _on_block_enter(self, block: Block) -> None:
        """Handle block context manager entrance."""
        block.start_event_idx = len(self._events)
        self._active_blocks.append(block)
        if block not in self._blocks:
            self._blocks.append(block)
        self._events.append(("block_start", block))

    def _on_block_exit(self, block: Block) -> None:
        """Handle block context manager exit."""
        block.end_event_idx = len(self._events)
        if block in self._active_blocks:
            self._active_blocks.remove(block)
        self._events.append(("block_end", block))

    def get_size(self) -> tuple[float, float]:
        """Estimate the total diagram width and height in coordinate units."""
        return _renderer_module._compute_diagram_size(self)

    def draw(self, xy: tuple[float, float] = (0.0, 0.0)) -> None:
        """Render the complete sequence diagram onto the active canvas.

        Args:
            xy: Bottom-left placement coordinate on the canvas. Defaults to (0.0, 0.0).
        """
        _renderer_module.draw_sequence_diagram(self, xy=xy)
