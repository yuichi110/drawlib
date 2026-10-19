# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: qdrant."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 3-unit isometric lattice centered at (50.0, 50.0)
u = 12.6
dx = u * math.cos(math.radians(30.0))


def _iso(ix: float, iy: float) -> tuple[float, float]:
    """Convert lattice coordinates (ix, iy) to canvas coordinates."""
    return (50.0 + ix * dx, 50.0 + iy * u)


# Outer hexagon & bottom-right Q-tail vertices (radius 3)
p_top_out = _iso(0.0, 3.0)
p_tr_out = _iso(3.0, 1.5)
p_br_out = _iso(3.0, -2.5)
p_tail_br = _iso(2.0, -3.0)
p_tail_bl = _iso(1.0, -2.5)
p_bot_out = _iso(0.0, -3.0)
p_bl_out = _iso(-3.0, -1.5)
p_tl_out = _iso(-3.0, 1.5)

# Middle Q-ring outer boundary (radius 2)
p_top_mid = _iso(0.0, 2.0)
p_tr_mid = _iso(2.0, 1.0)
p_tail_notch = _iso(1.0, -1.5)
p_bot_mid = _iso(0.0, -2.0)
p_bl_mid = _iso(-2.0, -1.0)
p_tl_mid = _iso(-2.0, 1.0)

# Inner small cube boundary (radius 1)
p_top_in = _iso(0.0, 1.0)
p_tr_in = _iso(1.0, 0.5)
p_br_in = _iso(1.0, -0.5)
p_bot_in = _iso(0.0, -1.0)
p_bl_in = _iso(-1.0, -0.5)
p_tl_in = _iso(-1.0, 0.5)
p_center = _iso(0.0, 0.0)

# 1. Top chevron roof facet (Colors.Gray3)
roof_facet = [p_tl_out, p_top_out, p_tr_out, p_tr_mid, p_top_mid, p_tl_mid]
polygon(roof_facet, style=Icon.no_border_fill(Colors.Gray3))

# 2. Left outer L-wall facet (WHITE)
left_wall = [p_tl_out, p_tl_mid, p_bl_mid, p_bot_mid, p_bot_out, p_bl_out]
polygon(left_wall, style=Icon.no_border_fill(Icon.WHITE))

# 3. Right outer vertical wall + bottom-middle recess wall (Colors.Gray6)
right_wall = [p_tr_out, p_br_out, p_tail_br, p_tr_mid]
polygon(right_wall, style=Icon.no_border_fill(Colors.Gray6))

bot_recess_wall = [p_bot_mid, p_tail_notch, p_tail_bl, p_bot_out]
polygon(bot_recess_wall, style=Icon.no_border_fill(Colors.Gray6))

# 4. Iconic front "Q" ribbon facet (Colors.Red3) as single compound polygon with hole
q_outer = [
    p_tail_bl,
    p_tail_br,
    p_tr_mid,
    p_top_mid,
    p_tl_mid,
    p_bl_mid,
    p_bot_mid,
    p_tail_notch,
]
q_hole = [p_top_in, p_tr_in, p_br_in, p_bot_in, p_bl_in, p_tl_in]
polygon(q_outer, holes=[q_hole], style=Icon.fill_style(Colors.Red3))

# 5. Inner center cube (WHITE top, Colors.Pink3 left, Colors.Red2 right)
polygon([p_center, p_tl_in, p_top_in, p_tr_in], style=Icon.no_border_fill(Icon.WHITE))
polygon([p_center, p_bot_in, p_bl_in, p_tl_in], style=Icon.no_border_fill(Colors.Pink3))
polygon([p_center, p_tr_in, p_br_in, p_bot_in], style=Icon.no_border_fill(Colors.Red2))

# 6. Structural seam lines & outer silhouette border
Icon.draw_round_polyline(q_hole, width_units=1.6, color=Icon.DARK, closed=True)
for v_in in (p_tl_in, p_tr_in, p_bot_in):
    Icon.draw_round_segment(p_center, v_in, width_units=1.5, color=Icon.DARK)

Icon.draw_round_polyline(q_outer, width_units=1.7, color=Icon.DARK, closed=True)
Icon.draw_round_segment(p_tl_out, p_tl_mid, width_units=1.7, color=Icon.DARK)
Icon.draw_round_segment(p_tr_out, p_tr_mid, width_units=1.7, color=Icon.DARK)
Icon.draw_round_segment(p_bot_out, p_bot_mid, width_units=1.7, color=Icon.DARK)

outer_outline = [p_top_out, p_tr_out, p_br_out, p_tail_br, p_tail_bl, p_bot_out, p_bl_out, p_tl_out]
Icon.draw_round_polyline(outer_outline, width_units=w, color=Icon.DARK, closed=True)

save()
