# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Public area charts module."""

from __future__ import annotations

from drawlib._charts._common._axis import Axis
from drawlib._charts._common._types import (
    AreaMode,
    ColorType,
    FormatterType,
    LegendPosition,
)
from drawlib._charts._common._types import (
    AreaMode as Mode,
)
from drawlib._charts.line_chart import (
    AreaChart,
    AreaSeries,
)
from drawlib._charts.line_chart import (
    AreaChart as Chart,
)
from drawlib._charts.line_chart import (
    AreaSeries as Series,
)

__all__ = [
    "AreaChart",
    "AreaMode",
    "AreaSeries",
    "Axis",
    "Chart",
    "ColorType",
    "FormatterType",
    "LegendPosition",
    "Mode",
    "Series",
]
