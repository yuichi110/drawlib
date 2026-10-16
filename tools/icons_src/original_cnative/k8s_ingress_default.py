# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: k8s_ingress."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    draw_original_k8s_heptagon,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

draw_original_k8s_heptagon()

# Right white ingress gateway frame
rectangle(
    (56.0, 48.0),
    width=32.0,
    height=36.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.4, shape_r=6.0),
)

# Entry shaft entering the card and splitting into two internal routes
draw_round_segment((28.0, 48.0), (52.5, 48.0), width_units=2.3, color=DARK)
draw_round_segment((52.5, 48.0), (64.0, 57.0), width_units=2.2, color=DARK)
draw_round_segment((52.5, 48.0), (64.0, 39.0), width_units=2.2, color=DARK)

# Crisp entry arrowhead inside gateway frame before the route split
draw_round_polyline(
    [(43.5, 51.2), (47.2, 48.0), (43.5, 44.8)],
    width_units=2.2,
    color=DARK,
)

# Left green external entry circle
circle(
    (28.0, 48.0),
    radius=6.5,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.3),
)

# Two light-blue internal target dots inside gateway card
for y_dot in (57.0, 39.0):
    circle(
        (64.0, y_dot),
        radius=4.2,
        style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.0),
    )

save()
