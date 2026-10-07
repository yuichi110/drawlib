# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib user utility functions and constants."""

from __future__ import annotations

from typing import Literal

from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text

# Define reusable drawing helper functions, macro components,
# or project-specific constants in this file.
#
# All top-level functions, classes, and variables defined here are automatically
# accessible in drawing code via `drawlib.utils`.


def service_card(
    xy: tuple[float, float],
    title: str,
    subtitle: str = "",
    width: float = 24.0,
    height: float = 16.0,
    style: Style = Styles.PrimaryFlat,
) -> None:
    """Draw a standardized service card with a title and optional subtitle.

    Args:
        xy: Center coordinate (x, y).
        title: Main service name (e.g. 'API Gateway').
        subtitle: Secondary label or tech stack (e.g. 'FastAPI / :8000').
        width: Card width.
        height: Card height.
        style: Card shape style.
    """
    x, y = xy
    rectangle(xy, width=width, height=height, r=2.0, style=style)
    if subtitle:
        text((x, y + 2.5), title, style=Styles.WhiteBold.patch(text_size=11))
        text((x, y - 3.5), subtitle, style=Styles.White.patch(text_size=8))
    else:
        text((x, y), title, style=Styles.WhiteBold)


def connect(
    start: tuple[float, float],
    end: tuple[float, float],
    label: str = "",
    arrow_head: Literal["", "->", "<-", "<->"] = "->",
    style: Style = Styles.PrimaryBold,
) -> None:
    """Draw a styled connecting line with an optional centered protocol label.

    Args:
        start: Starting point (x, y).
        end: Ending point (x, y).
        label: Protocol or description text (e.g. 'HTTPS', 'gRPC').
        arrow_head: Arrowhead style ('->', '<->', '-').
        style: Line style.
    """
    line(start, end, arrow_head=arrow_head, style=style)
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        text((mid_x, mid_y + 3.0), label, style=Styles.Primary.patch(text_size=9))
