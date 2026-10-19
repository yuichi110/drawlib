# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: compute_engine."""

from drawlib.canvas import save
from drawlib.utils import Gcp, Icon

Icon.setup()

w = 7.6
r_corner = 4.2
pin_ext_low = 7.0
pin_ext_high = 93.0

# 1. Central green hollow square
g_out0, g_out1 = 33.2, 66.8
g_in0, g_in1 = 41.0, 59.0
g_r = 4.0
Gcp.draw_rounded_corner_block(g_out0, g_in1 - 0.5, g_out1, g_out1, r=g_r, round_tl=True, round_tr=True, color=Gcp.GREEN)
Gcp.draw_rounded_corner_block(g_out0, g_out0, g_out1, g_in0 + 0.5, r=g_r, round_bl=True, round_br=True, color=Gcp.GREEN)
Gcp.draw_rounded_corner_block(g_out0, g_in0, g_in0, g_in1, r=0.0, color=Gcp.GREEN)
Gcp.draw_rounded_corner_block(g_in1, g_in0, g_out1, g_in1, r=0.0, color=Gcp.GREEN)

# 2. Outer frame & pins: YELLOW (Top-left quadrant)
Gcp.draw_rounded_corner_block(18.6, 25.8, 26.2, 81.4, r=r_corner, round_tl=True, color=Gcp.YELLOW)
Gcp.draw_rounded_corner_block(18.6, 73.8, 46.6, 81.4, r=r_corner, round_tl=True, color=Gcp.YELLOW)
for yc in (30.0, 50.0, 70.0):
    Gcp.draw_pin_h(22.0, pin_ext_low, yc, w, Gcp.YELLOW)
Gcp.draw_pin_v(30.0, 78.0, pin_ext_high, w, Gcp.YELLOW)

# 3. Outer frame & pins: RED (Top-right quadrant)
Gcp.draw_rounded_corner_block(46.2, 73.8, 81.4, 81.4, r=r_corner, round_tr=True, color=Gcp.RED)
Gcp.draw_rounded_corner_block(73.8, 33.4, 81.4, 81.4, r=r_corner, round_tr=True, color=Gcp.RED)
for xc in (50.0, 70.0):
    Gcp.draw_pin_v(xc, 78.0, pin_ext_high, w, Gcp.RED)
for yc in (50.0, 70.0):
    Gcp.draw_pin_h(78.0, pin_ext_high, yc, w, Gcp.RED)

# 4. Outer frame & pins: BLUE (Bottom section)
Gcp.draw_rounded_corner_block(18.6, 18.6, 81.4, 26.2, r=r_corner, round_bl=True, round_br=True, color=Gcp.BLUE)
Gcp.draw_rounded_corner_block(73.8, 18.6, 81.4, 33.8, r=r_corner, round_br=True, color=Gcp.BLUE)
for xc in (30.0, 50.0, 70.0):
    Gcp.draw_pin_v(xc, 22.0, pin_ext_low, w, Gcp.BLUE)
Gcp.draw_pin_h(78.0, pin_ext_high, 30.0, w, Gcp.BLUE)

save()
