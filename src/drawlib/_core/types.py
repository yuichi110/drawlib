# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular PURPOSE and noninfringement.

"""Core types facade module."""

from drawlib._core.l2_models import FontBase
from drawlib._core.l2_types import (
    Alpha,
    Angle,
    Angle90,
    ArrowHead,
    Bend,
    Bezier2,
    Bezier3,
    Color,
    ColorRGB,
    ColorRGBA,
    ColorType,
    Coordinate,
    Coordinates,
    FilePath,
    HAlign,
    IconStyle,
    ImageFormat,
    ImageQuality,
    ImageResample,
    ImageZoom,
    LineStyle,
    NegFloat,
    NegInt,
    NumVertex,
    PathPoint,
    PathPoints,
    PosFloat,
    PosInt,
    Size,
    TailEdge,
    VAlign,
)
from drawlib._core.l3_styles import (
    BaseColors,
    Style,
)

__all__ = [
    "Alpha",
    "Angle",
    "Angle90",
    "ArrowHead",
    "BaseColors",
    "Bend",
    "Bezier2",
    "Bezier3",
    "Color",
    "ColorRGB",
    "ColorRGBA",
    "ColorType",
    "Coordinate",
    "Coordinates",
    "FilePath",
    "FontBase",
    "HAlign",
    "IconStyle",
    "ImageFormat",
    "ImageQuality",
    "ImageResample",
    "ImageZoom",
    "LineStyle",
    "NegFloat",
    "NegInt",
    "NumVertex",
    "PathPoint",
    "PathPoints",
    "PosFloat",
    "PosInt",
    "Size",
    "Style",
    "TailEdge",
    "VAlign",
]
