# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Image type definitions for drawlib."""

from typing import Annotated, Literal

from pydantic import BeforeValidator, Field

from drawlib._core.l2_types._primitive import _normalize_str

ImageFormat = Annotated[
    Literal["jpg", "png", "webp", "pdf", "svg"],
    BeforeValidator(_normalize_str),
]

ImageZoom = Annotated[float, Field(gt=0.0)]
ImageQuality = Annotated[int, Field(ge=0, le=100)]
ImageResample = Annotated[
    Literal["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"],
    BeforeValidator(_normalize_str),
]
