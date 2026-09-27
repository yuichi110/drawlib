# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Style type definitions for drawlib."""

from typing import Annotated, Any, Literal

from pydantic import BeforeValidator, Field

from drawlib._core.l2_models import Color
from drawlib._core.l2_types_._primitive import PosFloat


def normalize_angle(v: Any) -> float:  # noqa: ANN401
    """Normalize angle in degrees.

    Values in [0.0, 360.0] are preserved.
    Values outside this range are cyclically mapped via modulo arithmetic.

    Examples:
        450.0 -> 90.0
        -90.0 -> 270.0
        -270.0 -> 90.0
        360.0 -> 360.0
        0.0 -> 0.0
    """
    try:
        val = float(v)
        if 0.0 <= val <= 360.0:
            return val
        mod = val % 360.0
        return 0.0 if mod == 0.0 else mod
    except (TypeError, ValueError) as e:
        raise ValueError(f"Angle must be a number. But '{v}' is given.") from e


def normalize_color(v: Any) -> Color:  # noqa: ANN401
    """Normalize RGB/RGBA tuple, list, Hex string, dict, or Color to Color instance."""
    if isinstance(v, Color):
        return v
    if isinstance(v, str):
        return Color.from_hex(v)
    if isinstance(v, (tuple, list)):
        return Color(v)
    if isinstance(v, dict):
        return Color(**v)
    raise ValueError(f"Color must be Color, RGB/RGBA tuple/list, dict, or hex string. But {v} is given.")


def normalize_literal_str(v: Any) -> Any:  # noqa: ANN401
    """Normalize string by stripping whitespace and converting to lowercase."""
    if isinstance(v, str):
        return v.strip().lower()
    return v


# Modern Type Definitions
Alpha = Annotated[float, Field(ge=0.0, le=1.0)]
Angle = Annotated[float, BeforeValidator(normalize_angle)]
Angle90 = Annotated[float, Field(ge=0.0, le=90.0)]
Bend = Annotated[float, Field(gt=-2.0, lt=2.0)]

RGBChannel = Annotated[int, Field(ge=0, le=255)]
ColorRGB = tuple[RGBChannel, RGBChannel, RGBChannel]
ColorRGBA = tuple[RGBChannel, RGBChannel, RGBChannel, Alpha]
ColorType = Annotated[Color | ColorRGB | ColorRGBA | str, BeforeValidator(normalize_color)]

HAlign = Annotated[
    Literal["left", "center", "right"],
    BeforeValidator(normalize_literal_str),
]
VAlign = Annotated[
    Literal["bottom", "center", "top"],
    BeforeValidator(normalize_literal_str),
]
LineStyle = Annotated[
    Literal["solid", "dashed", "dotted", "dashdot"],
    BeforeValidator(normalize_literal_str),
]
ArrowHead = Annotated[
    Literal["", "->", "<-", "<->"],
    BeforeValidator(normalize_literal_str),
]
TailEdge = Annotated[
    Literal["left", "top", "right", "bottom"],
    BeforeValidator(normalize_literal_str),
]
IconStyle = Annotated[
    Literal["thin", "light", "regular", "bold", "fill"],
    BeforeValidator(normalize_literal_str),
]
Size = (
    PosFloat
    | Annotated[
        Literal["small", "medium", "large"],
        BeforeValidator(normalize_literal_str),
    ]
)
