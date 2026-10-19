# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: envoy."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE
cx, cy = 50.0, 50.0
r_out = 40.0
r_in = 17.0

angles = [90.0, 30.0, -30.0, -90.0, -150.0, 150.0]
v_out = [(cx + r_out * math.cos(math.radians(a)), cy + r_out * math.sin(math.radians(a))) for a in angles]
v_in = [(cx + r_in * math.cos(math.radians(a)), cy + r_in * math.sin(math.radians(a))) for a in angles]

# 3 outer hexagonal ribbon facets
facet_tr = [v_in[0], v_out[0], v_out[1], v_out[2], v_in[2], v_in[1]]
facet_bot = [v_in[2], v_out[2], v_out[3], v_out[4], v_in[4], v_in[3]]
facet_tl = [v_in[4], v_out[4], v_out[5], v_out[0], v_in[0], v_in[5]]

polygon(facet_tr, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
polygon(facet_bot, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
polygon(facet_tl, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))

# Seam lines between the 3 ribbon facets
for idx in (0, 2, 4):
    Icon.draw_round_segment(v_in[idx], v_out[idx], width_units=2.0, color=Icon.DARK)

# Inner and outer hexagon borders
Icon.draw_round_polyline(v_in, width_units=2.0, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(v_out, width_units=w, color=Icon.DARK, closed=True)

save()
