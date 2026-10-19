# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: onnx."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_chord = 1.65

# 6 outer perimeter vertices and 2 interior vertices (scaled to fit cleanly with vertex dots)
v_tl = (37.9, 85.4)
v_tr = (69.8, 78.2)
v_r = (86.5, 49.1)
v_br = (66.5, 14.5)
v_bl = (27.7, 19.1)
v_l = (13.5, 51.3)

v_in_l = (31.9, 61.7)
v_in_r = (64.5, 33.8)

# 1. 8 triangular crystal facets in monochrome grays matching official shading
polygon([v_in_l, v_tr, v_in_r], style=Icon.no_border_fill(Colors.Gray3))
polygon([v_bl, v_in_l, v_in_r], style=Icon.no_border_fill(Colors.Gray4))
polygon([v_tl, v_tr, v_in_l], style=Icon.no_border_fill(Colors.Gray5))
polygon([v_tr, v_r, v_in_r], style=Icon.no_border_fill(Colors.Gray5))
polygon([v_bl, v_l, v_in_l], style=Icon.no_border_fill(Colors.Gray5))
polygon([v_bl, v_in_r, v_br], style=Icon.no_border_fill(Colors.Gray5))
polygon([v_l, v_tl, v_in_l], style=Icon.no_border_fill(Colors.Gray6))
polygon([v_r, v_br, v_in_r], style=Icon.no_border_fill(Colors.Gray6))

# 2. Inner wireframe chords
chords = [
    (v_in_l, v_tl),
    (v_in_l, v_tr),
    (v_in_l, v_in_r),
    (v_in_l, v_bl),
    (v_in_l, v_l),
    (v_in_r, v_tr),
    (v_in_r, v_r),
    (v_in_r, v_br),
    (v_in_r, v_bl),
]
for p1, p2 in chords:
    Icon.draw_round_segment(p1, p2, width_units=w_chord, color=Icon.DARK)

# 3. Outer perimeter outline
outer_ring = [v_tl, v_tr, v_r, v_br, v_bl, v_l]
Icon.draw_round_polyline(outer_ring, width_units=w, color=Icon.DARK, closed=True)

# 4. Crisp circular vertex dots at all 8 polyhedron nodes
dot_style = Icon.fill_style(Icon.DARK)
for v in (*outer_ring, v_in_l, v_in_r):
    circle(v, radius=2.7, style=dot_style)

save()
