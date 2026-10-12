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
FaceVariant = Annotated[
    Literal[
        "smile",
        "neutral",
        "sad",
        "angry",
        "surprised",
        "dizzy",
        "dead",
        "skull",
        "devil",
    ],
    BeforeValidator(_normalize_str),
]
FaceMood = FaceVariant
MathSymbol = Annotated[
    Literal[
        "+",
        "-",
        "−",
        "*",
        "x",
        "×",
        "/",
        "÷",
        "=",
        "!=",
        "≠",
        "plus",
        "minus",
        "multiply",
        "divide",
        "equal",
        "not_equal",
    ],
    BeforeValidator(_normalize_str),
]
CloudVariant = Annotated[
    Literal["standard", "flat", "flat_bottom", "fluffy", "dense", "simple", "minimal"],
    BeforeValidator(_normalize_str),
]
BraceSymbol = Annotated[
    Literal[
        "{",
        "}",
        "{}",
        "curly",
        "[",
        "]",
        "[]",
        "square",
        "(",
        ")",
        "()",
        "round",
    ],
    BeforeValidator(_normalize_str),
]
BraceDirection = Annotated[
    Literal["left", "right", "top", "bottom"],
    BeforeValidator(_normalize_str),
]
DocumentVariant = Annotated[
    Literal[
        "wave",
        "standard",
        "folded",
        "page",
        "note",
        "double_wave",
        "snippet",
        "folded_wave",
        "report",
    ],
    BeforeValidator(_normalize_str),
]
ForbiddenVariant = Annotated[
    Literal["slash", "standard", "backslash", "cross", "no_entry", "minus"],
    BeforeValidator(_normalize_str),
]
CheckmarkVariant = Annotated[
    Literal["standard", "check", "circle", "solid_circle"],
    BeforeValidator(_normalize_str),
]
ShieldVariant = Annotated[
    Literal["classic", "standard", "flat", "heater", "round"],
    BeforeValidator(_normalize_str),
]
LightningVariant = Annotated[
    Literal["standard", "flat", "double", "flat_double", "angled", "slanted"],
    BeforeValidator(_normalize_str),
]
ExplosionVariant = Annotated[
    Literal["standard", "irregular", "heavy", "wild", "curved", "comic"],
    BeforeValidator(_normalize_str),
]
RibbonVariant = Annotated[
    Literal["down", "standard", "up", "flat", "banner"],
    BeforeValidator(_normalize_str),
]
TagVariant = Annotated[
    Literal["angled", "standard", "chamfered", "beveled", "rounded"],
    BeforeValidator(_normalize_str),
]
FunnelVariant = Annotated[
    Literal["standard", "flat", "3d", "cylinder", "curved"],
    BeforeValidator(_normalize_str),
]
PlaqueVariant = Annotated[
    Literal["concave", "standard", "chamfered", "octagon", "notched"],
    BeforeValidator(_normalize_str),
]
PinVariant = Annotated[
    Literal["pointer", "standard", "teardrop", "drop", "pin", "badge"],
    BeforeValidator(_normalize_str),
]
HeartVariant = Annotated[
    Literal["standard", "classic", "broken"],
    BeforeValidator(_normalize_str),
]
SunVariant = Annotated[
    Literal["rays", "standard", "ring", "beams"],
    BeforeValidator(_normalize_str),
]
MoonVariant = Annotated[
    Literal["crescent", "standard", "thin", "waxing", "half"],
    BeforeValidator(_normalize_str),
]
ClockVariant = Annotated[
    Literal["standard", "ticks", "dial", "stopwatch", "timer", "alarm", "digital"],
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
ShapeRadius = PosFloat | Annotated[tuple[PosFloat, ...], Field(min_length=1)]

__all__ = [
    "Angle",
    "Angle90",
    "ArrowHead",
    "Bend",
    "BraceDirection",
    "BraceSymbol",
    "CheckmarkVariant",
    "ClockVariant",
    "CloudVariant",
    "DocumentVariant",
    "ExplosionVariant",
    "FaceMood",
    "FaceVariant",
    "ForbiddenVariant",
    "FunnelVariant",
    "HAlign",
    "HeartVariant",
    "IconStyle",
    "LightningVariant",
    "LineStyle",
    "MathSymbol",
    "MoonVariant",
    "PinVariant",
    "PlaqueVariant",
    "RibbonVariant",
    "ShapeRadius",
    "ShieldVariant",
    "Size",
    "SunVariant",
    "TagVariant",
    "TailEdge",
    "VAlign",
]

