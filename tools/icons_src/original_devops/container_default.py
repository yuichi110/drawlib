# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: container."""

from drawlib.canvas import save
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_segment,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE
verts = draw_iso_cube(
    50.0,
    50.0,
    radius=40.0,
    top_color=WHITE,
    left_color=PASTEL_BLUE,
    right_color=PASTEL_GREEN,
    border_color=DARK,
    border_units=w,
)

v_tl = verts["tl"]
v_bl = verts["bl"]
v_tr = verts["tr"]
v_br = verts["br"]
v_center = verts["center"]
v_bottom = verts["bottom"]

for t in (0.35, 0.67):
    x = (1.0 - t) * v_tl[0] + t * v_center[0]
    y_top = (1.0 - t) * v_tl[1] + t * v_center[1] - 8.0
    y_bot = (1.0 - t) * v_bl[1] + t * v_bottom[1] + 8.0
    draw_round_segment((x, y_bot), (x, y_top), width_units=2.0, color=DARK)

for t in (0.33, 0.65):
    x = (1.0 - t) * v_center[0] + t * v_tr[0]
    y_top = (1.0 - t) * v_center[1] + t * v_tr[1] - 8.0
    y_bot = (1.0 - t) * v_bottom[1] + t * v_br[1] + 8.0
    draw_round_segment((x, y_bot), (x, y_top), width_units=2.0, color=DARK)

save()
