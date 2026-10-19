# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: terraform."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

t30 = math.tan(math.radians(30.0))
dx = 20.6
dy = dx * t30
h = 23.6
gx = 4.0
gy = 4.5

x_l0 = 15.1
x_l1 = x_l0 + dx
x_c0 = x_l1 + gx
x_c1 = x_c0 + dx
x_r0 = x_c1 + gx
x_r1 = x_r0 + dx

y_l_tl = 88.9
y_l_tr = y_l_tl - dy
y_l_bl = y_l_tl - h
y_l_br = y_l_tr - h

# Center face continues the -30 deg top slope across the gap gx
y_c_tl = y_l_tl - (x_c0 - x_l0) * t30
y_c_tr = y_c_tl - dy
y_c_bl = y_c_tl - h
y_c_br = y_c_tr - h

# Bottom face sits gy units below the center face
y_b_tl = y_c_bl - gy
y_b_tr = y_c_br - gy
y_b_bl = y_b_tl - h
y_b_br = y_b_tr - h

# Right face mirrors the center face across the right gap
y_r_tl = y_c_tr
y_r_bl = y_c_br
y_r_tr = y_r_tl + dy
y_r_br = y_r_bl + dy

left_face = [(x_l0, y_l_tl), (x_l1, y_l_tr), (x_l1, y_l_br), (x_l0, y_l_bl)]
center_face = [(x_c0, y_c_tl), (x_c1, y_c_tr), (x_c1, y_c_br), (x_c0, y_c_bl)]
bottom_face = [(x_c0, y_b_tl), (x_c1, y_b_tr), (x_c1, y_b_br), (x_c0, y_b_bl)]
right_face = [(x_r0, y_r_tl), (x_r1, y_r_tr), (x_r1, y_r_br), (x_r0, y_r_bl)]

# 1. Fill 3 left/center faces in Colors.Purple3 and right face in Colors.Purple4
for pts in (left_face, center_face, bottom_face):
    polygon(pts, style=Icon.no_border_fill(Colors.Purple3))
polygon(right_face, style=Icon.no_border_fill(Colors.Purple4))

# 2. Crisp DARK w=1.9 outlines on all 4 parallelograms
for pts in (left_face, center_face, bottom_face, right_face):
    Icon.draw_round_polyline(pts, width_units=w, color=Icon.DARK, closed=True)

save()
