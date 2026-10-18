# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: megaport."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import (
    DARK,
    WHITE,
    draw_compound_polygon,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

w_outer = 2.0
w_inner = 1.5

m_outer = [(62.41, 47.72), (71.04, 39.08), (71.04, 25.65), (67.44, 23.25), (63.84, 25.65), (63.84, 36.2), (58.81, 41.24), (53.77, 36.2), (53.77, 25.65), (50.17, 23.25), (46.57, 25.65), (46.57, 36.2), (41.53, 41.24), (36.49, 36.2), (36.49, 25.65), (32.89, 23.25), (29.29, 25.65), (29.29, 39.08), (37.93, 47.72), (37.93, 61.16), (46.57, 69.8), (46.57, 80.6), (50.17, 83.0), (53.77, 80.6), (53.77, 70.04), (62.41, 61.4), (62.41, 61.35), (62.41, 61.26), (62.41, 61.06), (62.41, 60.82), (62.41, 60.51), (62.41, 60.13), (62.41, 59.72), (62.41, 59.26), (62.41, 58.76), (62.41, 58.23), (62.41, 57.66), (62.41, 57.08), (62.41, 56.46), (62.41, 55.83), (62.41, 55.21), (62.41, 54.56), (62.41, 53.91), (62.41, 53.29), (62.41, 52.66), (62.41, 52.04), (62.41, 51.46), (62.41, 50.89), (62.41, 50.36), (62.41, 49.85), (62.41, 49.4), (62.41, 49.0), (62.41, 48.6), (62.41, 48.29), (62.41, 48.06), (62.41, 47.86), (62.41, 47.77)]
m_hole = [(55.21, 58.28), (50.17, 63.32), (45.13, 58.28), (45.13, 47.72), (50.17, 42.68), (55.21, 47.72)]

circle((50.0, 50.0), radius=40.0, style=fill_style("#EC6A86", border_color=DARK, border_units=w_outer))
draw_compound_polygon([m_outer, m_hole], color=WHITE)
draw_round_polyline(m_outer, width_units=w_inner, color=DARK, closed=True)
draw_round_polyline(m_hole, width_units=w_inner, color=DARK, closed=True)

save()
# fmt: on
