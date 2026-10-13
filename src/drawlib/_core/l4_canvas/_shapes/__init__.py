# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Canvas shape feature package aggregating all shape drawing capabilities."""

from __future__ import annotations

from drawlib._core.l4_canvas._shapes._arrow import CanvasShapeArrowFeature
from drawlib._core.l4_canvas._shapes._badge import CanvasShapeBadgeFeature
from drawlib._core.l4_canvas._shapes._basic import CanvasShapeBasicFeature
from drawlib._core.l4_canvas._shapes._container import CanvasShapeContainerFeature
from drawlib._core.l4_canvas._shapes._polygon import CanvasShapePolygonFeature
from drawlib._core.l4_canvas._shapes._symbol import CanvasShapeSymbolFeature
from drawlib._core.l4_canvas._shapes._util import ShapeUtil


class CanvasShapeFeature(
    CanvasShapeArrowFeature,
    CanvasShapeBadgeFeature,
    CanvasShapeContainerFeature,
    CanvasShapeSymbolFeature,
    CanvasShapePolygonFeature,
    CanvasShapeBasicFeature,
):
    """Unified canvas shape feature class combining all 6 shape categories."""

    pass


__all__ = [
    "CanvasShapeArrowFeature",
    "CanvasShapeBadgeFeature",
    "CanvasShapeBasicFeature",
    "CanvasShapeContainerFeature",
    "CanvasShapeFeature",
    "CanvasShapePolygonFeature",
    "CanvasShapeSymbolFeature",
    "ShapeUtil",
]
