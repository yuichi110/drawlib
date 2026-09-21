# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Message class implementation for sequence diagrams."""

from __future__ import annotations

from typing import TYPE_CHECKING

from drawlib._diagrams.sequence._types import ArrowType, PaddingType

if TYPE_CHECKING:
    from drawlib._core.l3_styles import Style
    from drawlib._diagrams.sequence._diagram import Diagram
    from drawlib._diagrams.sequence._participant import Participant


class Message:
    """Interaction message between participants in a sequence diagram."""

    def __init__(
        self,
        source: Participant,
        target: Participant,
        label: str = "",
        is_reply: bool = False,
        is_async: bool = False,
        arrow: ArrowType = "->",
        style: Style | None = None,
        textstyle: Style | None = None,
        padding: PaddingType = 0.0,
    ) -> None:
        """Initialize Message.

        Args:
            source: Originating participant.
            target: Destination participant.
            label: Text description of the message.
            is_reply: Whether this message is a response (renders dashed line). Defaults to False.
            is_async: Whether this message is asynchronous (renders open stick arrow). Defaults to False.
            arrow: Arrowhead directionality ("->", "<->", "-"). Defaults to "->".
            style: Optional line Style (color, width, dash).
            textstyle: Optional text Style for label.
            padding: Gap clearance between lifeline and line endpoints. Defaults to 0.0.
        """
        self.source = source
        self.target = target
        self.label = label
        self.is_reply = is_reply
        self.is_async = is_async
        self.arrow = arrow
        self.style = style
        self.textstyle = textstyle
        self.padding = padding
        self.number: int | None = None
        self._diagram: Diagram | None = None

    @property
    def is_self_call(self) -> bool:
        """Whether this message is a recursive / self-invocation loop."""
        return self.source is self.target

    def set_label(self, text: str) -> Message:
        """Set message label text.

        Args:
            text: Description text.

        Returns:
            Message: self for method chaining.
        """
        self.label = text
        return self

    def set_reply(self, is_reply: bool = True) -> Message:
        """Set whether this message is a response (dashed line).

        Args:
            is_reply: True for dashed response line.

        Returns:
            Message: self for method chaining.
        """
        self.is_reply = is_reply
        return self

    def set_async(self, is_async: bool = True) -> Message:
        """Set whether this message is asynchronous (open stick arrow).

        Args:
            is_async: True for open stick arrow.

        Returns:
            Message: self for method chaining.
        """
        self.is_async = is_async
        return self

    def set_arrow(self, arrow: ArrowType) -> Message:
        """Set arrowhead style.

        Args:
            arrow: Directionality ("->", "<->", "-").

        Returns:
            Message: self for method chaining.
        """
        self.arrow = arrow
        return self

    def set_style(self, style: Style) -> Message:
        """Set message line style.

        Args:
            style: Style object for the line.

        Returns:
            Message: self for method chaining.
        """
        self.style = style
        return self

    def set_textstyle(self, textstyle: Style) -> Message:
        """Set message label text style.

        Args:
            textstyle: Style object for label text.

        Returns:
            Message: self for method chaining.
        """
        self.textstyle = textstyle
        return self

    def set_padding(self, padding: PaddingType) -> Message:
        """Set clearance padding between lifelines and line endpoints.

        Args:
            padding: Clearance distance (float or (start, end) tuple).

        Returns:
            Message: self for method chaining.
        """
        self.padding = padding
        return self
