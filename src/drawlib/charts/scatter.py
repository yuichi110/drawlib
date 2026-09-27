# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public scatter charts module."""

from __future__ import annotations

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import (
    ColorType,
    LegendPosition,
    PointShape,
    ScaleType,
)
from drawlib._charts.scatter_chart import (
    ScatterChart,
    ScatterPoint,
    ScatterSeries,
)
from drawlib._charts.scatter_chart import (
    ScatterChart as Chart,
)
from drawlib._charts.scatter_chart import (
    ScatterPoint as Point,
)
from drawlib._charts.scatter_chart import (
    ScatterSeries as Series,
)

__all__ = [
    "Axis",
    "Chart",
    "ColorType",
    "LegendPosition",
    "Point",
    "PointShape",
    "ScaleType",
    "ScatterChart",
    "ScatterPoint",
    "ScatterSeries",
    "Series",
]
