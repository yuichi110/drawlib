# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Common charting utilities and models."""

from drawlib._charts._common._axis import Axis, calculate_axis_range_and_ticks, value_to_ratio
from drawlib._charts._common._legend import draw_legend
from drawlib._charts._common._style_utils import ensure_line_style, ensure_shape_style, ensure_text_style
from drawlib._charts._common._types import BarMode, ColorType, FormatterType, LegendPosition, Orientation, ScaleType

__all__ = [
    "Axis",
    "BarMode",
    "ColorType",
    "FormatterType",
    "LegendPosition",
    "Orientation",
    "ScaleType",
    "calculate_axis_range_and_ticks",
    "draw_legend",
    "ensure_line_style",
    "ensure_shape_style",
    "ensure_text_style",
    "value_to_ratio",
]
