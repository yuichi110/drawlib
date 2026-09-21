# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Note annotation class implementation for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams.sequence._types import NotePosition

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._diagram import Diagram
    from drawlib._diagrams.sequence._participant import Participant


class Note:
    """Sticky note annotation card attached to lifelines in a sequence diagram."""

    def __init__(
        self,
        text: str,
        on: Participant | None = None,
        over: list[Participant] | None = None,
        pos: NotePosition = "right",
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None:
        """Initialize Note.

        Args:
            text: Note content text.
            on: Single participant to attach note to.
            over: List of participants to span note across.
            pos: Position relative to lifeline ("left", "right", "over"). Defaults to "right".
            style: Style for the note background card.
            textstyle: Style for the note text.
        """
        self.text = text
        self.on = on
        self.over = list(over) if over is not None else None
        self.pos = pos
        self.style = style
        self.textstyle = textstyle
        self._diagram: Diagram | None = None

    def set_text(self, text: str) -> Note:
        """Set note content text.

        Args:
            text: New text content.

        Returns:
            Note: self for method chaining.
        """
        self.text = text
        return self

    def set_style(self, style: Style) -> Note:
        """Set card background style.

        Args:
            style: Style object.

        Returns:
            Note: self for method chaining.
        """
        self.style = style
        return self

    def set_textstyle(self, textstyle: Style) -> Note:
        """Set text style.

        Args:
            textstyle: Style object for text.

        Returns:
            Note: self for method chaining.
        """
        self.textstyle = textstyle
        return self
