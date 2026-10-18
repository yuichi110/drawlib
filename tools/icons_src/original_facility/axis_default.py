# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: axis."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import DARK, draw_round_polyline, no_border_fill, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()

w = 2.0

tri_yellow = [(24.64, 42.47), (50.0, 81.97), (91.0, 18.03), (63.09, 18.03), (47.45, 42.47)]
tri_slate = [(47.45, 42.47), (43.28, 42.47), (59.03, 18.03), (63.09, 18.03)]
tri_red = [(43.28, 42.47), (59.03, 18.03), (9.0, 18.03), (24.64, 42.47)]

polygon(tri_yellow, style=no_border_fill("#F2CE4E"))
polygon(tri_slate, style=no_border_fill("#546072"))
polygon(tri_red, style=no_border_fill("#F24F61"))

for tri in (tri_yellow, tri_slate, tri_red):
    draw_round_polyline(tri, width_units=w, color=DARK, closed=True)

save()
# fmt: on
