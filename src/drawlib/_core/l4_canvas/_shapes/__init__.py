# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas shape feature package aggregating all shape drawing capabilities."""

from drawlib._core.l4_canvas._shapes._arrow import (
    CanvasOriginalArrowFeature,
    CanvasShapeArrowFeature,
)
from drawlib._core.l4_canvas._shapes._basic import CanvasShapeBasicFeature
from drawlib._core.l4_canvas._shapes._polygon import (
    CanvasOriginalPolygonFeature,
    CanvasShapePolygonFeature,
)
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeFeature(
    CanvasShapePolygonFeature,
    CanvasShapeArrowFeature,
    CanvasShapeBasicFeature,
):
    """Unified canvas shape feature class combining basic, polygon, and arrow shapes."""

    pass


__all__ = [
    "CanvasOriginalArrowFeature",
    "CanvasOriginalPolygonFeature",
    "CanvasShapeArrowFeature",
    "CanvasShapeBasicFeature",
    "CanvasShapeFeature",
    "CanvasShapePolygonFeature",
    "ShapeUtil",
]
