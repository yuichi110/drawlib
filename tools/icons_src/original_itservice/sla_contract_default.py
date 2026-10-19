# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service concept icon: sla_contract (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import arc, circle, polygon, rectangle, regularpolygon, star
from drawlib.utils import Icon

# ruff: noqa: E501, F401
# fmt: off
Icon.setup()
w_outer, w_inner = 2.0, 1.6

# Contract Document
rectangle((42, 52), width=52, height=72, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0))
rectangle((42, 78), width=36, height=6, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.5, shape_r=1.5))
for ly in (64, 54, 44):
    Icon.draw_round_segment((25, ly), (58, ly), width_units=1.8, color=Icon.DARK)
# Ribbon Seal on Contract
seal_pts: list[tuple[float, float]] = [(26, 26), (22, 12), (28, 16), (34, 12), (30, 26)]
polygon(seal_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(seal_pts, width_units=1.5, color=Icon.DARK, closed=True)
circle((28, 28), radius=7.5, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner))
# SLA Stopwatch / Target Gauge on bottom-right
circle((74, 34), radius=17.0, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer))
circle((74, 34), radius=12.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.5))
Icon.draw_round_polyline([(74, 42), (74, 34), (81, 34)], width_units=2.0, color=Icon.DARK)
rectangle((74, 54), width=8, height=4, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.5, shape_r=1.0))
save()
# fmt: on
