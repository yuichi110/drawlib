# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Color type definitions for drawlib."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

Alpha = Annotated[float, Field(ge=0.0, le=1.0)]
RGBChannel = Annotated[int, Field(ge=0, le=255)]
ColorRGB = tuple[RGBChannel, RGBChannel, RGBChannel]
ColorRGBA = tuple[RGBChannel, RGBChannel, RGBChannel, Alpha]

__all__ = [
    "Alpha",
    "ColorRGB",
    "ColorRGBA",
    "RGBChannel",
]
