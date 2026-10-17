# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: cargo_plane."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w_outer = 2.0
w_inner = 1.6

# 1. Far-side upper wing (PASTEL_BLUE_LIGHT, behind fuselage)
far_wing = [
    (43.0, 56.0),
    (33.0, 73.0),
    (41.5, 73.0),
    (55.0, 56.0),
]
polygon(far_wing, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(far_wing, width_units=w_outer, color=DARK, closed=True)

# 2. Vertical tail fin (PASTEL_BLUE)
tail_fin = [
    (13.0, 53.0),
    (11.0, 80.0),
    (20.5, 80.0),
    (33.0, 57.0),
]
polygon(tail_fin, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(tail_fin, width_units=w_outer, color=DARK, closed=True)
draw_round_segment((16.5, 58.0), (15.0, 76.0), width_units=w_inner, color=DARK)

# 3. Wide-body cargo fuselage (WHITE, x=12..89, y=40..58)
# Smooth nose arc + tail cone
nose_arc: list[tuple[float, float]] = []
steps = 14
for i in range(steps + 1):
    ang = math.radians(65.0 - 155.0 * (i / steps))
    nose_arc.append((81.0 + 8.0 * math.cos(ang), 47.0 + 7.0 * math.sin(ang)))

fuselage_pts = [
    (12.0, 53.0),
    (22.0, 58.0),
    (73.0, 58.0),
    *nose_arc,
    (28.0, 40.0),
]
polygon(fuselage_pts, style=no_border_fill(WHITE))
draw_round_polyline(fuselage_pts, width_units=w_outer, color=DARK, closed=True)

# Cockpit windshield (PASTEL_BLUE_LIGHT)
cockpit_pts = [
    (74.0, 53.5),
    (80.5, 53.5),
    (84.0, 49.0),
    (74.0, 49.0),
]
polygon(cockpit_pts, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(cockpit_pts, width_units=w_inner, color=DARK, closed=True)

# 4. PASTEL_GREEN main-deck cargo door on fuselage side
rectangle(
    (63.0, 50.5),
    width=13.0,
    height=10.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer, shape_r=1.8),
)
draw_round_segment((59.0, 53.5), (67.0, 53.5), width_units=w_inner, color=DARK)

# 5. Near-side swept main wing (PASTEL_BLUE, extending down-left)
near_wing = [
    (36.0, 45.0),
    (54.0, 45.0),
    (36.0, 18.0),
    (25.0, 18.0),
]
polygon(near_wing, style=no_border_fill(PASTEL_BLUE))
draw_round_polyline(near_wing, width_units=w_outer, color=DARK, closed=True)

# Underwing turbofan engine pod (PASTEL_BLUE_LIGHT + WHITE intake)
rectangle(
    (45.5, 29.0),
    width=13.0,
    height=6.8,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=2.5),
)
rectangle(
    (50.5, 29.0),
    width=3.5,
    height=6.8,
    style=fill_style(WHITE, border_color=DARK, border_units=w_inner, shape_r=1.0),
)

# 6. Rear horizontal tailplane (PASTEL_BLUE_LIGHT)
h_stab = [
    (17.0, 51.0),
    (12.0, 44.0),
    (19.5, 44.0),
    (26.0, 51.0),
]
polygon(h_stab, style=no_border_fill(PASTEL_BLUE_LIGHT))
draw_round_polyline(h_stab, width_units=w_outer, color=DARK, closed=True)

save()
