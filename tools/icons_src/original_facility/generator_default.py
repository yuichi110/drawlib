# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: generator."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Top cylindrical exhaust muffler and chunky exhaust stack
Icon.draw_round_polyline([(28.0, 77.0), (28.0, 84.5), (22.5, 84.5)], width_units=4.8, color=Icon.DARK)
Icon.draw_round_polyline([(28.0, 77.0), (28.0, 84.5), (22.5, 84.5)], width_units=2.0, color=Icon.PASTEL_BLUE_LIGHT)
rectangle(
    (40.0, 75.5),
    width=28.0,
    height=8.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)

# 2. Right-side cylindrical alternator / radiator cowling (PASTEL_BLUE_LIGHT)
rectangle(
    (80.0, 46.5),
    width=12.0,
    height=39.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=3.0),
)
for vy in (58.0, 50.5, 43.0, 35.5):
    Icon.draw_round_segment((77.5, vy), (83.5, vy), width_units=w_inner, color=Icon.DARK)

# 3. Main industrial generator engine canopy housing (PASTEL_BLUE)
rectangle(
    (45.0, 47.5),
    width=62.0,
    height=48.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.0),
)

# 4. Left-side air intake louver lines on engine canopy
for ly in (58.0, 51.0, 44.0, 37.0):
    Icon.draw_round_segment((19.5, ly), (25.5, ly), width_units=w_inner, color=Icon.DARK)

# 5. Central WHITE circular turbine / alternator dial
circle(
    (47.5, 47.5),
    radius=16.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# 6. PASTEL_GREEN lightning bolt inside the circular alternator face
bolt_pts = [
    (50.5, 59.5),
    (40.0, 47.0),
    (47.0, 47.0),
    (44.5, 35.5),
    (55.0, 48.0),
    (48.0, 48.0),
]
polygon(bolt_pts, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(bolt_pts, width_units=w_inner, color=Icon.DARK, closed=True)

# 7. Heavy steel skid base frame at bottom
rectangle(
    (50.0, 19.5),
    width=76.0,
    height=8.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_outer, shape_r=2.5),
)
for pocket_x in (27.0, 73.0):
    rectangle(
        (pocket_x, 19.5),
        width=8.0,
        height=3.2,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=1.0),
    )

save()
