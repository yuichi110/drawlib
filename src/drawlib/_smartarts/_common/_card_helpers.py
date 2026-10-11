# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Shared card rendering helpers for KpiCards, CardList, and Roadmap."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import text as canvas_text


def resolve_card_box_style(
    style: Style,
    card_h: float,
    *,
    max_r: float = 2.2,
) -> Style:
    """Ensure card style has rounded corners unless explicitly specified.

    Args:
        style: Base card rectangle style.
        card_h: Card height in canvas units.
        max_r: Maximum default corner radius when style.shape_r is None.

    Returns:
        Style: Style with shape_r resolved.
    """
    if style.shape_r is not None:
        return style
    return style.patch(shape_r=min(max_r, card_h * 0.18))


def draw_card_title_and_description(  # noqa: PLR0913
    *,
    text_x: float,
    cy: float,
    card_h: float,
    text: str,
    description: str,
    text_style: Style,
    description_style: Style | None,
    halign: Literal["left", "center"] = "left",
) -> None:
    """Render primary card title (text) and optional description stacked vertically.

    Args:
        text_x: X coordinate for text anchor (left edge when halign='left', center when 'center').
        cy: Vertical center coordinate of the card.
        card_h: Height of the card.
        text: Primary card title text.
        description: Optional supporting description text (single-line or multi-line).
        text_style: Style for the primary title text.
        description_style: Style for the description text (required when description is non-empty).
        halign: Horizontal alignment ("left" or "center"). Defaults to "left".

    Raises:
        ValueError: If description is non-empty and description_style is None.
    """
    has_desc = bool(description.strip())
    t_style = text_style.patch(halign=halign, valign="center")

    if has_desc:
        if description_style is None:
            raise ValueError(
                "Neither default 'description_style' nor item 'description_style' was provided "
                f"for description of item '{text}'."
            )
        is_multiline = "\n" in description.strip()
        title_y = cy + card_h * (0.23 if is_multiline else 0.18)
        desc_y = cy - card_h * (0.14 if is_multiline else 0.18)
        d_style = description_style.patch(halign=halign, valign="center")
        canvas_text(xy=(text_x, title_y), text=text, style=t_style)
        canvas_text(xy=(text_x, desc_y), text=description, style=d_style)
    else:
        canvas_text(xy=(text_x, cy), text=text, style=t_style)
