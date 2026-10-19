# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: cyberark."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0
s = 40.0 / 41.0


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


face_tl_top = _sc([(32.77, 59.94), (50.0, 69.92), (50.0, 91.0), (14.45, 70.45)])
face_tr_top = _sc([(49.99, 69.92), (67.25, 59.95), (85.5, 70.5), (50.0, 91.0)])
face_br_bot = _sc([(50.06, 9.0), (50.04, 30.07), (67.3, 40.02), (85.55, 50.57), (85.55, 29.5)])
face_bl_bot = _sc([(50.04, 30.07), (32.77, 40.02), (14.53, 29.47), (50.08, 9.01)])
face_left_v = _sc([(32.77, 40.02), (32.77, 59.94), (14.45, 70.45), (14.52, 29.47)])
inner_right = _sc([(50.0, 69.92), (67.26, 59.95), (67.26, 40.02), (50.0, 49.99)])
inner_left = _sc([(50.0, 69.92), (50.0, 49.99), (32.77, 40.02), (32.77, 59.94)])
# fmt: on

# 1. Isometric cube segment fills in pastel blue & slate
polygon(inner_right, style=Icon.no_border_fill(Colors.Gray3))
polygon(inner_left, style=Icon.no_border_fill(Colors.Gray3))
polygon(face_tl_top, style=Icon.no_border_fill(Colors.Blue2))
polygon(face_bl_bot, style=Icon.no_border_fill(Colors.Blue2))
polygon(face_tr_top, style=Icon.no_border_fill(Colors.Blue3))
polygon(face_br_bot, style=Icon.no_border_fill(Colors.Blue3))
polygon(face_left_v, style=Icon.no_border_fill(Colors.Blue3))

# 2. DARK 1.7 outlines for every isometric cube face
for face_pts in (
    inner_right,
    inner_left,
    face_tl_top,
    face_bl_bot,
    face_tr_top,
    face_br_bot,
    face_left_v,
):
    Icon.draw_round_polyline(face_pts, width_units=w, color=Icon.DARK, closed=True)

save()
