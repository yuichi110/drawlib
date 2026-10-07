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

from drawlib._core.l2_types._primitive import PosFloat, _normalize_str


def _normalize_angle(v: Any) -> float:  # noqa: ANN401
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


# Modern Type Definitions
Angle = Annotated[float, BeforeValidator(_normalize_angle)]
Angle90 = Annotated[float, Field(ge=0.0, le=90.0)]
Bend = Annotated[float, Field(gt=-2.0, lt=2.0)]

HAlign = Annotated[
    Literal["left", "center", "right"],
    BeforeValidator(_normalize_str),
]
VAlign = Annotated[
    Literal["bottom", "center", "top"],
    BeforeValidator(_normalize_str),
]
LineStyle = Annotated[
    Literal["solid", "dashed", "dotted", "dashdot"],
    BeforeValidator(_normalize_str),
]
ArrowHead = Annotated[
    Literal["", "->", "<-", "<->"],
    BeforeValidator(_normalize_str),
]
TailEdge = Annotated[
    Literal["left", "top", "right", "bottom"],
    BeforeValidator(_normalize_str),
]
FaceMood = Annotated[
    Literal["smile", "neutral", "sad", "angry", "surprised"],
    BeforeValidator(_normalize_str),
]
IconStyle = Annotated[
    Literal["thin", "light", "regular", "bold", "fill"],
    BeforeValidator(_normalize_str),
]
Size = (
    PosFloat
    | Annotated[
        Literal["small", "medium", "large"],
        BeforeValidator(_normalize_str),
    ]
)

__all__ = [
    "Angle",
    "Angle90",
    "ArrowHead",
    "Bend",
    "FaceMood",
    "HAlign",
    "IconStyle",
    "LineStyle",
    "Size",
    "TailEdge",
    "VAlign",
]
