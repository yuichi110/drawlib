# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for drawlib."""

from typing import Annotated, Any, Literal

from pydantic import AfterValidator, BeforeValidator, Field, InstanceOf, SkipValidation

from drawlib.v0_2.private.core.fonts import FontBase, FontFile

#
# Basic Types
#

TypeCoordinate = tuple[float, float]
TypePathPoint = (
    tuple[float, float]
    | tuple[tuple[float, float], tuple[float, float]]
    | tuple[tuple[float, float], tuple[float, float], tuple[float, float]]
)

#
# Validators
#


def _validate_literal(v: Any, supported: set[Any], name: str) -> Any:  # noqa: ANN401
    """Helper to validate literal values with a custom error message."""
    if v not in supported:
        raise ValueError(f'Arg/Attr "{name}" must be one of {sorted(list(supported))}. But "{v}" is given.')
    return v


def validate_alpha(v: float) -> float:
    """Validate alpha value."""
    if not (0.0 <= v <= 1.0):
        raise ValueError(f"Value must be between 0.0 and 1.0. But {v} is given.")
    return v


def validate_angle(v: float) -> float:
    """Validate angle value."""
    if not (0.0 <= v <= 360.0):
        raise ValueError(f"Value must be between 0.0 and 360.0. But {v} is given.")
    return v


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


def validate_color_tuple(v: tuple[Any, ...]) -> tuple[Any, ...]:
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


#
# Annotated Types
#

# Primitives with range validation
TypeAlpha = Annotated[float, AfterValidator(validate_alpha)]
TypeAngle = Annotated[float, AfterValidator(validate_angle)]
TypeAngle90 = Annotated[float, AfterValidator(validate_angle_90)]
TypeBend = Annotated[float, AfterValidator(validate_bend)]

# Primitives with simple constraints
TypePosFloat = Annotated[float, Field(ge=0.0)]
TypePosFloatEx = Annotated[float, Field(gt=0.0)]
TypePosInt = Annotated[int, Field(ge=0)]
TypePosIntEx = Annotated[int, Field(gt=0)]
TypeNumVertex = Annotated[int, Field(ge=3)]

# Complex structures
TypeCoordinates = list[TypeCoordinate]

TypeColorRGB = Annotated[
    tuple[int, int, int],
    AfterValidator(validate_color_tuple),
]
TypeColorRGBA = Annotated[
    tuple[int, int, int, float],
    AfterValidator(validate_color_tuple),
]
TypeColor = Annotated[
    TypeColorRGB | TypeColorRGBA,
    AfterValidator(validate_color_tuple),
]


TypePathPoints = list[TypePathPoint]

# Literal choices
TypeIconStyle = Annotated[
    Literal["thin", "light", "regular", "bold", "fill"],
    BeforeValidator(lambda v: _validate_literal(v, {"thin", "light", "regular", "bold", "fill"}, "IconStyle")),
]
TypeHAlign = Annotated[
    Literal["left", "center", "right"],
    BeforeValidator(lambda v: _validate_literal(v, {"left", "center", "right"}, "HAlign")),
]
TypeVAlign = Annotated[
    Literal["bottom", "center", "top"],
    BeforeValidator(lambda v: _validate_literal(v, {"bottom", "center", "top"}, "VAlign")),
]
TypeLineStyle = Annotated[
    Literal["solid", "dashed", "dotted", "dashdot"],
    BeforeValidator(lambda v: _validate_literal(v, {"solid", "dashed", "dotted", "dashdot"}, "LineStyle")),
]
TypeArrowHead = Annotated[
    Literal["", "->", "<-", "<->"],
    BeforeValidator(lambda v: _validate_literal(v, {"", "->", "<-", "<->"}, "ArrowHead")),
]
TypeImageFormat = Annotated[
    Literal["jpg", "png", "webp", "pdf"],
    BeforeValidator(lambda v: _validate_literal(v, {"jpg", "png", "webp", "pdf"}, "ImageFormat")),
]
TypeTailEdge = Annotated[
    Literal["left", "top", "right", "bottom"],
    BeforeValidator(lambda v: _validate_literal(v, {"left", "top", "right", "bottom"}, "TailEdge")),
]
TypeSize = (
    TypePosFloatEx
    | Annotated[
        Literal["small", "medium", "large"],
        BeforeValidator(lambda v: _validate_literal(v, {"small", "medium", "large"}, "Size")),
    ]
)
TypeFont = InstanceOf[FontBase] | InstanceOf[FontFile]

__all__ = [
    "TypeAlpha",
    "TypeAngle",
    "TypeAngle90",
    "TypeBend",
    "TypePosFloat",
    "TypePosFloatEx",
    "TypePosInt",
    "TypePosIntEx",
    "TypeNumVertex",
    "TypeCoordinate",
    "TypeCoordinates",
    "TypeColor",
    "TypeColorRGB",
    "TypeColorRGBA",
    "TypePathPoint",
    "TypePathPoints",
    "TypeIconStyle",
    "TypeHAlign",
    "TypeVAlign",
    "TypeLineStyle",
    "TypeArrowHead",
    "TypeImageFormat",
    "TypeTailEdge",
    "TypeSize",
    "TypeFont",
]
