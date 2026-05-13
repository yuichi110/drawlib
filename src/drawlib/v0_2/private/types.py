# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for drawlib."""

import os
from enum import Enum
from typing import Annotated, Any, Literal, NoReturn

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    InstanceOf,
    SkipValidation,
    field_validator,
)

from drawlib.v0_2.private.util import get_script_relative_path


class StaticContainer:
    """Base class to prevent instantiation for static constant containers.

    Inherit from this class to create a namespace that only holds constants
    and static data, ensuring it cannot be initialized as an object.
    """

    def __new__(cls) -> NoReturn:
        """Raise TypeError upon any attempt to instantiate the class.

        Returns:
            NoReturn: This method never returns normally.

        Raises:
            TypeError: Always raised to prevent instantiation.
        """
        raise TypeError(
            f"'{cls.__name__}' is a static container (namespace) and cannot be instantiated. "
            f"Access its attributes directly, e.g., {cls.__name__}.AttributeName"
        )


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


class FontBase(str, Enum):
    """Base class of all font classes."""


class FontFile(BaseModel):
    """A class representing a font file"""

    model_config = ConfigDict(validate_assignment=True)

    file: str

    def __init__(self, file: str) -> None:
        """Initialize the font file."""
        super().__init__(file=file)

    @field_validator("file")
    @classmethod
    def validate_file(cls, value: str) -> str:
        """Validate the font file path.

        Validates that the provided path exists and is a valid file path. If not,
        raises an appropriate exception.

        Args:
            value (str): The path to the font file.

        Returns:
            str: The absolute path to the font file.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
        """
        path = get_script_relative_path(value)
        if not os.path.exists(path):
            raise FileNotFoundError(f'font file "{path}" does not exist.')
        return path


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
    "FontBase",
    "FontFile",
]
