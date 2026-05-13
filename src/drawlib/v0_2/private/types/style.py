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

from pydantic import AfterValidator, BeforeValidator

from drawlib.v0_2.private.types.base import validate_literal
from drawlib.v0_2.private.types.primitive import TypePosFloatEx


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

TypeIconStyle = Annotated[
    Literal["thin", "light", "regular", "bold", "fill"],
    BeforeValidator(lambda v: validate_literal(v, {"thin", "light", "regular", "bold", "fill"}, "IconStyle")),
]
TypeHAlign = Annotated[
    Literal["left", "center", "right"],
    BeforeValidator(lambda v: validate_literal(v, {"left", "center", "right"}, "HAlign")),
]
TypeVAlign = Annotated[
    Literal["bottom", "center", "top"],
    BeforeValidator(lambda v: validate_literal(v, {"bottom", "center", "top"}, "VAlign")),
]
TypeLineStyle = Annotated[
    Literal["solid", "dashed", "dotted", "dashdot"],
    BeforeValidator(lambda v: validate_literal(v, {"solid", "dashed", "dotted", "dashdot"}, "LineStyle")),
]
TypeArrowHead = Annotated[
    Literal["", "->", "<-", "<->"],
    BeforeValidator(lambda v: validate_literal(v, {"", "->", "<-", "<->"}, "ArrowHead")),
]
TypeTailEdge = Annotated[
    Literal["left", "top", "right", "bottom"],
    BeforeValidator(lambda v: validate_literal(v, {"left", "top", "right", "bottom"}, "TailEdge")),
]
TypeSize = (
    TypePosFloatEx
    | Annotated[
        Literal["small", "medium", "large"],
        BeforeValidator(lambda v: validate_literal(v, {"small", "medium", "large"}, "Size")),
    ]
)
