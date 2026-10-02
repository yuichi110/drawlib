# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""bubblespeech() implementation module."""

from __future__ import annotations

from pydantic import validate_call

from drawlib._core.l2_types import Coordinate, PosFloat, Ratio, TailEdge
from drawlib._core.l3_colors import ColorUtil
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style
from drawlib._core.l4_canvas import polygon
from drawlib._core.l4_canvas import text as canvas_text


@validate_call
def bubblespeech(
    xy: Coordinate,
    width: PosFloat,
    height: PosFloat,
    tail_edge: TailEdge,
    tail_start_ratio: Ratio,
    tail_vertex_xy: Coordinate,
    tail_end_ratio: Ratio,
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None:
    """Draw a speech bubble on the canvas.

    Args:
        xy: The (x, y) coordinates of the bottom-left corner of the bubble body.
        width: The width of the bubble body.
        height: The height of the bubble body.
        tail_edge: The edge ("left", "top", "right", "bottom") where the tail originates.
        tail_start_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail begins.
        tail_vertex_xy: The (x, y) target coordinates pointing to the vertex of the tail.
        tail_end_ratio: Ratio (between 0.0 and 1.0) along the edge where the tail ends.
        style: The Style of the speech bubble shape (required).
        text: Optional text to display inside the bubble. Defaults to an empty string.
        text_style: Optional Style of the text. If None and text is provided,
            a high-contrast text style is automatically derived from the bubble style.

    Raises:
        ValueError: If tail_start_ratio is greater than or equal to tail_end_ratio.
    """
    if tail_start_ratio >= tail_end_ratio:
        raise ValueError("tail_start_ratio must be smaller than tail_end_ratio.")

    x, y = xy
    xys: list[Coordinate] = [(x, y)]  # left bottom

    if tail_edge == "left":
        xys.append((x, y + height * tail_start_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x, y + height * tail_end_ratio))
    xys.append((x, y + height))  # left top

    if tail_edge == "top":
        xys.append((x + width * tail_start_ratio, y + height))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_end_ratio, y + height))
    xys.append((x + width, y + height))  # right top

    if tail_edge == "right":
        xys.append((x + width, y + height * tail_end_ratio))
        xys.append(tail_vertex_xy)
        xys.append((x + width, y + height * tail_start_ratio))
    xys.append((x + width, y))  # right bottom

    if tail_edge == "bottom":
        xys.append((x + width * tail_end_ratio, y))
        xys.append(tail_vertex_xy)
        xys.append((x + width * tail_start_ratio, y))

    # Draw speech bubble polygon via l4_canvas primitive
    polygon(xys=xys, style=style)

    # Draw centered text within bubble body if provided
    if text:
        center_x = x + width / 2.0
        center_y = y + height / 2.0

        if text_style is not None:
            effective_text_style = text_style
            if effective_text_style.text_halign is None or effective_text_style.text_valign is None:
                effective_text_style = effective_text_style.patch(
                    text_halign=effective_text_style.text_halign or "center",
                    text_valign=effective_text_style.text_valign or "center",
                )
        else:
            contrast_color = ColorUtil.get_contrast_text_color(
                style.shape_fill_color,
                style.shape_fill_alpha,
                transparent_color=style.shape_line_color,
            )
            effective_text_style = Style(
                text_color=contrast_color,
                text_font=style.text_font or Font.SANSSERIF_REGULAR,
                text_size=style.text_size or 16.0,
                text_halign="center",
                text_valign="center",
            )

        canvas_text(xy=(center_x, center_y), text=text, style=effective_text_style)
