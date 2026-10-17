# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: vagrant."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)


def _s(pt: tuple[float, float], factor: float = 0.94) -> tuple[float, float]:
    """Scale point around (50, 50) by factor."""
    return (50.0 + (pt[0] - 50.0) * factor, 50.0 + (pt[1] - 50.0) * factor)


def _s_list(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [_s(p) for p in pts]


setup_icon()

w = 1.9
w_inner = 1.6

# 1. Sunlit top & front isometric faces (Colors.Blue2)
left_top = _s_list([
    (21.20, 91.00),
    (10.40, 84.69),
    (28.40, 74.22),
    (39.21, 80.44),
])
right_top = _s_list([
    (78.80, 91.00),
    (60.80, 80.45),
    (71.60, 74.22),
    (89.60, 84.69),
])
front_face = _s_list([
    (10.40, 84.69),
    (10.40, 76.95),
    (34.71, 17.84),
    (50.00, 9.00),
    (50.00, 31.21),
    (57.20, 35.39),
    (71.60, 67.86),
    (71.60, 74.22),
    (60.80, 80.45),
    (60.80, 73.25),
    (50.00, 48.00),
    (50.00, 39.57),
    (42.80, 35.39),
    (28.40, 67.86),
    (28.40, 74.22),
])

# 2. Shaded side & inner valley faces (Colors.Blue3)
left_inner_shade = _s_list([
    (39.21, 80.44),
    (28.40, 74.22),
    (28.40, 67.86),
    (42.80, 35.39),
    (50.00, 39.57),
    (50.00, 48.00),
    (39.20, 73.25),
])
right_outer_shade = _s_list([
    (89.60, 84.69),
    (71.60, 74.22),
    (71.60, 67.86),
    (57.20, 35.39),
    (50.00, 31.21),
    (50.00, 9.00),
    (65.42, 17.91),
    (89.60, 77.18),
])

for pts in (left_top, right_top, front_face):
    polygon(pts, style=no_border_fill(Colors.Blue2))
for pts in (left_inner_shade, right_outer_shade):
    polygon(pts, style=no_border_fill(Colors.Blue3))

# 3. Inner isometric crease lines (DARK, 1.6)
creases = [
    _s_list([(10.40, 84.69), (28.40, 74.22), (39.21, 80.44)]),
    _s_list([(60.80, 80.45), (71.60, 74.22), (89.60, 84.69)]),
    _s_list([(28.40, 74.22), (28.40, 67.86), (42.80, 35.39), (50.00, 39.57), (50.00, 48.00)]),
    _s_list([(71.60, 74.22), (71.60, 67.86), (57.20, 35.39), (50.00, 31.21), (50.00, 9.00)]),
]
for c_pts in creases:
    draw_round_polyline(c_pts, width_units=w_inner, color=DARK, closed=False)

# 4. Outer silhouette border (DARK, w=1.9)
outer_silhouette = _s_list([
    (21.20, 91.00),
    (10.40, 84.69),
    (10.40, 76.95),
    (34.71, 17.84),
    (50.00, 9.00),
    (65.42, 17.91),
    (89.60, 77.18),
    (89.60, 84.69),
    (78.80, 91.00),
    (60.80, 80.45),
    (60.80, 73.25),
    (50.00, 48.00),
    (39.20, 73.25),
    (39.21, 80.44),
])
draw_round_polyline(outer_silhouette, width_units=w, color=DARK, closed=True)

save()
