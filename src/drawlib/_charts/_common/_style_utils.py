# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Style utilities ensuring declared target support for chart elements."""

from __future__ import annotations

from typing import Literal

from drawlib._charts._common._types import ColorType
from drawlib._core.l3_colors import Color
from drawlib._core.l3_fonts import Font
from drawlib._core.l3_styles import Style

_BASE_LINE_STYLE = Style(line_color=(30, 41, 59, 1.0), line_width=1.0)
_BASE_TEXT_STYLE = Style(text_color=(30, 41, 59, 1.0), text_size=10.0, text_font=Font.SANSSERIF_REGULAR)


def clamp_ratio(ratio: float) -> float:
    """Clamp spatial rendering ratio into [0.0, 1.0]."""
    return max(0.0, min(1.0, float(ratio)))


def with_alpha(color: ColorType, alpha: float) -> tuple[int, int, int, float]:
    """Return an RGBA color tuple replacing alpha with given ratio."""
    c = color if isinstance(color, Color) else Color(color)
    return (c.r, c.g, c.b, float(alpha))


def resolve_series_color(style: Style) -> ColorType:
    """Extract primary color from a series/slice Style for legend swatches and strokes."""
    return style.line_color or style.shape_fill_color or style.shape_line_color or (30, 41, 59, 1.0)


def ensure_line_style(style: Style) -> Style:
    """Ensure style has line support by filling missing mandatory line attributes."""
    if "line" in style.supports:
        return style
    return _BASE_LINE_STYLE.patch(style)


def ensure_text_style(
    style: Style,
    *,
    halign: Literal["left", "center", "right"] | None = None,
    valign: Literal["bottom", "center", "top"] | None = None,
    size: float | None = None,
    font: Font | None = None,
) -> Style:
    """Ensure style has text support by filling missing mandatory text attributes."""
    base = _BASE_TEXT_STYLE
    if size is not None or font is not None:
        base = base.patch(text_size=size, text_font=font)
    patched = base.patch(style)
    if halign is not None or valign is not None:
        patched = patched.patch(text_halign=halign, text_valign=valign)
    return patched


def ensure_shape_style(style: Style) -> Style:
    """Ensure style has shape support by filling missing mandatory shape attributes."""
    if "shape" in style.supports:
        return style
    fill = style.shape_fill_color or style.line_color or (50, 100, 200, 1.0)
    base = Style(shape_fill_color=fill, shape_line_color=(0, 0, 0, 0.0), shape_line_width=0.0)
    return base.patch(style)
