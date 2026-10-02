# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Block context manager for conditional and loop frames in sequence diagrams."""

from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING

from drawlib._diagrams.sequence._types import BlockType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._diagram import SequenceDiagram
    from drawlib._diagrams.sequence._participant import Participant


class Block:
    """Context manager framing boundary for sequence diagrams (loop, alt, opt, par)."""

    def __init__(
        self,
        block_type: BlockType,
        label: str = "",
        diagram: SequenceDiagram | None = None,
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Initialize Block.

        Args:
            block_type: Type of block ("loop", "alt", "else", "opt", "par", etc.).
            label: Text description shown in the frame header.
            diagram: Parent SequenceDiagram instance.
            style: Optional Style object for the boundary box.
            textstyle: Optional Style object for the label text.
        """
        self.block_type = block_type
        self.label = label
        self.diagram = diagram
        self.style = style
        self.textstyle = textstyle
        self.start_event_idx: int = -1
        self.end_event_idx: int = -1
        self.involved_participants: set[Participant] = set()

    def __enter__(self) -> Block:
        """Enter block context manager, marking the start of framed actions."""
        if self.diagram is not None:
            self.diagram._on_block_enter(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit block context manager, marking the end of framed actions."""
        if self.diagram is not None:
            self.diagram._on_block_exit(self)
