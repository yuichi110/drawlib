# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base data structures for modular slide stage components."""

from __future__ import annotations

import contextvars
from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    """A rectangular bounding box on the slide stage (typically 1920x1080).

    Attributes:
        x: The horizontal coordinate of the top-left corner in stage pixels.
        y: The vertical coordinate of the top-left corner in stage pixels.
        width: The width of the bounding box in stage pixels.
        height: The height of the bounding box in stage pixels.
    """

    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class SlideContext:
    """Runtime context providing slide index and deck metadata.

    Attributes:
        index: 1-based index of the current slide.
        total: Total number of slides in the presentation deck.
    """

    index: int = 1
    total: int = 1

    @property
    def text(self) -> str:
        """Formatted slide counter string, e.g. '4 / 9'."""
        return f"{self.index} / {self.total}"

    def format(self, template: str = "{index} / {total}") -> str:
        """Render a custom formatted slide counter string.

        Args:
            template: Format string with {index} and {total} placeholders.

        Returns:
            str: Formatted slide counter text.
        """
        return template.format(index=self.index, total=self.total)


_slide_context_var: contextvars.ContextVar[SlideContext] = contextvars.ContextVar(
    "slide_context", default=SlideContext(index=1, total=1)
)


def set_slide_context(index: int, total: int) -> contextvars.Token[SlideContext]:
    """Set the active slide context.

    Args:
        index: 1-based slide index.
        total: Total slides count.

    Returns:
        contextvars.Token: Token to reset context.
    """
    return _slide_context_var.set(SlideContext(index=index, total=total))


def reset_slide_context(token: contextvars.Token[SlideContext]) -> None:
    """Reset the slide context using token.

    Args:
        token: Context token returned by set_slide_context.
    """
    _slide_context_var.reset(token)


class _CurrentSlideProxy:
    """Dynamic proxy accessing the active SlideContext."""

    @property
    def index(self) -> int:
        """Current slide index (1-based)."""
        return _slide_context_var.get().index

    @property
    def total(self) -> int:
        """Total number of slides in the presentation."""
        return _slide_context_var.get().total

    @property
    def text(self) -> str:
        """Formatted slide counter string, e.g. '4 / 9'."""
        return _slide_context_var.get().text

    def format(self, template: str = "{index} / {total}") -> str:
        """Render a custom formatted slide counter string.

        Args:
            template: Format string with {index} and {total} placeholders.

        Returns:
            str: Formatted slide counter string.
        """
        return template.format(index=self.index, total=self.total)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        ctx = _slide_context_var.get()
        return f"SlideContext(index={ctx.index}, total={ctx.total})"


current_slide = _CurrentSlideProxy()
