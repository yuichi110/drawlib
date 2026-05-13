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

from drawlib.v0_2.private.types.base import validate_literal

TypeImageFormat = Annotated[
    Literal["jpg", "png", "webp", "pdf"],
    BeforeValidator(lambda v: validate_literal(v, {"jpg", "png", "webp", "pdf"}, "ImageFormat")),
]

TypeImageZoom = Annotated[float, Field(gt=0.0)]
TypeImageQuality = Annotated[int, Field(ge=0, le=100)]
TypeImageResample = Annotated[
    Literal["nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"],
    BeforeValidator(
        lambda v: validate_literal(v, {"nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"}, "ImageResample")
    ),
]
