# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for drawlib."""

from drawlib.v0_2.private.types.base import (
    StaticContainer,
)
from drawlib.v0_2.private.types.font import (
    FontBase,
    FontFile,
    TypeFont,
)
from drawlib.v0_2.private.types.geometry import (
    TypeBezier2,
    TypeBezier3,
    TypeCoordinate,
    TypeCoordinates,
    TypePathPoint,
    TypePathPoints,
)
from drawlib.v0_2.private.types.image import (
    TypeImageFormat,
    TypeImageQuality,
    TypeImageResample,
    TypeImageZoom,
)
from drawlib.v0_2.private.types.primitive import (
    TypeAlpha,
    TypeAngle,
    TypeAngle90,
    TypeBend,
    TypeBool,
    TypeFloat,
    TypeInt,
    TypeNumVertex,
    TypePosFloat,
    TypePosFloatEx,
    TypePosInt,
    TypePosIntEx,
    TypeStr,
)
from drawlib.v0_2.private.types.style import (
    TypeArrowHead,
    TypeColor,
    TypeColorRGB,
    TypeColorRGBA,
    TypeHAlign,
    TypeIconStyle,
    TypeLineStyle,
    TypeSize,
    TypeTailEdge,
    TypeVAlign,
)

__all__ = [
    "StaticContainer",
    "TypeAlpha",
    "TypeAngle",
    "TypeAngle90",
    "TypeBend",
    "TypePosFloat",
    "TypePosFloatEx",
    "TypePosInt",
    "TypePosIntEx",
    "TypeNumVertex",
    "TypeFloat",
    "TypeInt",
    "TypeStr",
    "TypeBool",
    "TypeCoordinate",
    "TypeCoordinates",
    "TypeBezier2",
    "TypeBezier3",
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
    "TypeImageZoom",
    "TypeImageQuality",
    "TypeImageResample",
    "TypeTailEdge",
    "TypeSize",
    "TypeFont",
    "FontBase",
    "FontFile",
]
