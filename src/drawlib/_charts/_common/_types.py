# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Type definitions for charts module."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal, Union

# Primary orientation of the chart
Orientation = Literal["vertical", "horizontal"]

# Bar layout mode
BarMode = Literal["group", "stack"]

# Legend box position
LegendPosition = Literal["top", "bottom", "right", "none", "auto"]

# Scaling algorithm for value axes
ScaleType = Literal["linear", "log"]

# Value label and tick formatter
FormatterType = Union[str, Callable[[float], str], None]

# Color specification type: RGB or RGBA tuple
ColorType = Union[tuple[int, int, int], tuple[int, int, int, float]]

# Data point marker shape
PointShape = Literal["circle", "square", "none"]

# Area chart layout mode
AreaMode = Literal["overlap", "stack"]

# Line pattern style
LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]

# Radar chart grid shape
GridShape = Literal["polygon", "circle"]
