# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code concept icon: package_module."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_iso_cube,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_shape = 1.8
w_line = 2.7

# 1. Isometric 3D parcel cube (PASTEL_BLUE top, WHITE left, PASTEL_BLUE_LIGHT right)
v = draw_iso_cube(
    50.0,
    50.0,
    radius=36.0,
    top_color=PASTEL_BLUE,
    left_color=WHITE,
    right_color=PASTEL_BLUE_LIGHT,
    border_color=DARK,
    border_units=w_shape,
)

v_top = v["top"]
v_tl = v["tl"]
v_tr = v["tr"]
v_center = v["center"]


def _lerp(p1: tuple[float, float], p2: tuple[float, float], t: float) -> tuple[float, float]:
    return (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)


# 2. PASTEL_GREEN packing tape strip across top face and down front-right face
t_a, t_b = 0.36, 0.64
p_bl_1 = _lerp(v_tl, v_top, t_a)
p_bl_2 = _lerp(v_tl, v_top, t_b)
p_fr_1 = _lerp(v_center, v_tr, t_a)
p_fr_2 = _lerp(v_center, v_tr, t_b)

flap_h = 13.0
p_flap_1 = (p_fr_1[0], p_fr_1[1] - flap_h)
p_flap_2 = (p_fr_2[0], p_fr_2[1] - flap_h)

tape_outline = [p_bl_1, p_bl_2, p_fr_2, p_flap_2, p_flap_1, p_fr_1]
polygon(tape_outline, style=no_border_fill(PASTEL_GREEN))
draw_round_polyline(tape_outline, width_units=w_shape, color=DARK, closed=True)
draw_round_segment(p_fr_1, p_fr_2, width_units=w_shape, color=DARK)

# 3. Small DARK code chevron mark `< >` on WHITE left parcel face
# Left face center is roughly (34.4, 41.0), sloped along (-cos30, sin30) = (-0.866, 0.5)
# Left `<` chevron
draw_round_polyline(
    [(30.5, 48.0), (25.5, 44.5), (30.5, 36.5)],
    width_units=w_line,
    color=DARK,
)
# Right `>` chevron
draw_round_polyline(
    [(37.5, 44.0), (42.5, 35.5), (37.5, 32.5)],
    width_units=w_line,
    color=DARK,
)

save()
