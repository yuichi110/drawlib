# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: workflow_automation."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
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

# 1. Orthogonal DARK connectors between trigger, hub, and action
draw_round_polyline(
    [(26.0, 65.0), (26.0, 50.0), (33.5, 50.0)],
    width_units=w_outer,
    color=DARK,
    corner_r=4.0,
)
draw_round_polyline(
    [(29.0, 53.2), (32.8, 50.0), (29.0, 46.8)],
    width_units=w_inner,
    color=DARK,
)

draw_round_polyline(
    [(66.5, 50.0), (74.0, 50.0), (74.0, 35.0)],
    width_units=w_outer,
    color=DARK,
    corner_r=4.0,
)
draw_round_polyline(
    [(70.8, 39.2), (74.0, 35.4), (77.2, 39.2)],
    width_units=w_inner,
    color=DARK,
)

# 2. Top-left PASTEL_BLUE_LIGHT trigger node (x=13.0..39.0, y=65.0..83.0)
rectangle(
    (26.0, 74.0),
    width=26.0,
    height=18.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=w_outer, shape_r=4.5),
)
circle((20.0, 74.0), radius=2.3, style=fill_style(WHITE, border_color=DARK, border_units=w_inner))
draw_round_segment((25.0, 74.0), (33.5, 74.0), width_units=w_inner, color=DARK)

# 3. Bottom-right PASTEL_BLUE action node (x=61.0..87.0, y=17.0..35.0)
rectangle(
    (74.0, 26.0),
    width=26.0,
    height=18.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w_outer, shape_r=4.5),
)
circle((68.0, 26.0), radius=2.3, style=fill_style(WHITE, border_color=DARK, border_units=w_inner))
draw_round_segment((73.0, 26.0), (81.5, 26.0), width_units=w_inner, color=DARK)

# 4. Central circular PASTEL_GREEN automation hub (radius=16.5)
circle(
    (50.0, 50.0),
    radius=16.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=w_outer),
)

# 5. Crisp WHITE lightning bolt inside hub
bolt_pts = [
    (52.8, 60.5),
    (43.2, 48.8),
    (49.5, 48.8),
    (47.2, 39.5),
    (56.8, 51.2),
    (50.5, 51.2),
]
polygon(bolt_pts, style=no_border_fill(WHITE))
draw_round_polyline(bolt_pts, width_units=w_inner, color=DARK, closed=True)

save()
