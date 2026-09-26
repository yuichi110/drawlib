# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Style type definitions for drawlib."""

import re
from typing import Annotated, Any, Literal

from pydantic import AfterValidator, BeforeValidator, Field

from drawlib._core.l2_types_._primitive import TypePosFloat
from drawlib._core.l2_types_._utils import validate_literal

_HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def validate_alpha(v: float) -> float:
    """Validate alpha value."""
    if not (0.0 <= v <= 1.0):
        raise ValueError(f"Value must be between 0.0 and 1.0. But {v} is given.")
    return v


def validate_angle(v: float) -> float:
    """Validate angle value."""
    if not (0.0 <= v <= 360.0):
        raise ValueError(f"Angle must be between 0.0 and 360.0. But {v} is given.")
    return float(v)


def validate_angle_90(v: float) -> float:
    """Validate angle value max 90."""
    if not (0.0 <= v <= 90.0):
        raise ValueError(f"Value must be between 0.0 and 90.0. But {v} is given.")
    return v


def validate_bend(v: float) -> float:
    """Validate bend value."""
    if not (-2.0 < v < 2.0):
        raise ValueError(f"Value must be between -2.0 and 2.0 (exclusive). But {v} is given.")
    return v


def validate_color_tuple(v: tuple[Any, ...]) -> tuple[Any, ...]:  # noqa: ANN401
    """Validate color tuple."""
    if len(v) not in {3, 4}:
        raise ValueError(f"Color tuple must be length 3 (RGB) or 4 (RGBA). But {v} is given.")

    for i in range(3):
        if not isinstance(v[i], int) or not (0 <= v[i] <= 255):
            raise ValueError(f"RGB values must be integers between 0 and 255. But {v[i]} is given.")

    if len(v) == 4:
        if not isinstance(v[3], (int, float)) or not (0.0 <= v[3] <= 1.0):
            raise ValueError(f"Alpha value must be float between 0.0 and 1.0. But {v[3]} is given.")

    return v


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


def normalize_angle90(v: Any) -> float:  # noqa: ANN401
    """Validate angle in degrees in range [0.0, 90.0]."""
    try:
        val = float(v)
        if not (0.0 <= val <= 90.0):
            raise ValueError(f"Value must be between 0.0 and 90.0. But {v} is given.")
        return val
    except (TypeError, ValueError) as e:
        raise ValueError(f"Angle must be a number between 0.0 and 90.0. But '{v}' is given.") from e


def normalize_color(v: Any) -> tuple[int, int, int, float]:  # noqa: ANN401
    """Normalize RGB/RGBA tuple, list, or Hex string to RGBA (r, g, b, a).

    If RGB is provided, alpha defaults to 1.0.
    """
    if isinstance(v, str):
        hex_val = v.strip()
        if not _HEX_COLOR_PATTERN.match(hex_val):
            raise ValueError(f"String color must be a valid hex code (e.g. '#3498db'). But '{v}' is given.")
        hex_code = hex_val.lstrip("#")
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        a = 1.0 if len(hex_code) == 6 else int(hex_code[6:8], 16) / 255.0
        return (r, g, b, a)

    if isinstance(v, (tuple, list)):
        length = len(v)
        if length not in {3, 4}:
            raise ValueError(f"Color tuple must be length 3 (RGB) or 4 (RGBA). But {v} is given.")
        try:
            r = int(v[0])
            g = int(v[1])
            b = int(v[2])
        except (TypeError, ValueError) as e:
            raise ValueError(f"RGB values must be integers between 0 and 255. But {v} is given.") from e

        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be integers between 0 and 255. But {(r, g, b)} is given.")

        if length == 3:
            return (r, g, b, 1.0)
        else:
            try:
                a = float(v[3])
            except (TypeError, ValueError) as e:
                raise ValueError(f"Alpha value must be float between 0.0 and 1.0. But {v[3]} is given.") from e
            if not (0.0 <= a <= 1.0):
                raise ValueError(f"Alpha value must be float between 0.0 and 1.0. But {a} is given.")
            return (r, g, b, a)

    raise ValueError(f"Color must be RGB (r, g, b) or RGBA (r, g, b, a) tuple/list, or hex string. But {v} is given.")


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
Color = Annotated[ColorRGB | ColorRGBA | str, BeforeValidator(normalize_color)]

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
    TypePosFloat
    | Annotated[
        Literal["small", "medium", "large"],
        BeforeValidator(normalize_literal_str),
    ]
)

# Backward Compatibility Aliases
TypeAlpha = Alpha
TypeAngle = Angle
TypeAngle90 = Angle90
TypeBend = Bend
TypeColor = Color
TypeColorRGB = Annotated[tuple[int, int, int], AfterValidator(validate_color_tuple)]
TypeColorRGBA = Annotated[tuple[int, int, int, float], AfterValidator(validate_color_tuple)]
TypeIconStyle = IconStyle
TypeHAlign = HAlign
TypeVAlign = VAlign
TypeLineStyle = LineStyle
TypeArrowHead = ArrowHead
TypeTailEdge = TailEdge
TypeSize = Size
