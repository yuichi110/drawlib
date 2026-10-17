# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Facility icon: megaport (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import WHITE, draw_compound_polygon, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
circle((50.0, 50.0), radius=41.0, style=fill_style('#E31B48'))
draw_compound_polygon([[(62.72, 47.66), (71.57, 38.81), (71.57, 25.04), (67.88, 22.58), (64.19, 25.04), (64.19, 35.86), (59.03, 41.02), (53.86, 35.86), (53.86, 25.04), (50.17, 22.58), (46.48, 25.04), (46.48, 35.86), (41.32, 41.02), (36.15, 35.86), (36.15, 25.04), (32.46, 22.58), (28.77, 25.04), (28.77, 38.81), (37.63, 47.66), (37.63, 61.44), (46.48, 70.29), (46.48, 81.36), (50.17, 83.82), (53.86, 81.36), (53.86, 70.54), (62.72, 61.68), (62.72, 61.63), (62.72, 61.54), (62.72, 61.34), (62.72, 61.09), (62.72, 60.77), (62.72, 60.38), (62.72, 59.96), (62.72, 59.49), (62.72, 58.98), (62.72, 58.44), (62.72, 57.85), (62.72, 57.26), (62.72, 56.62), (62.72, 55.98), (62.72, 55.34), (62.72, 54.67), (62.72, 54.01), (62.72, 53.37), (62.72, 52.73), (62.72, 52.09), (62.72, 51.5), (62.72, 50.91), (62.72, 50.37), (62.72, 49.85), (62.72, 49.39), (62.72, 48.97), (62.72, 48.57), (62.72, 48.25), (62.72, 48.01), (62.72, 47.81), (62.72, 47.71)], [(55.34, 58.49), (50.17, 63.65), (45.01, 58.49), (45.01, 47.66), (50.17, 42.5), (55.34, 47.66)]], color=WHITE)
save()
# fmt: on
