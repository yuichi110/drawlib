# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: gpu_cluster."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# High-speed NVLink triangle interconnect bus between the 3 GPU modules
p_top = (50.0, 72.0)
p_bl = (27.0, 28.0)
p_br = (73.0, 28.0)
p_hub = (50.0, 46.5)

draw_round_polyline([p_top, p_bl, p_br], width_units=2.5, color=DARK, closed=True)
for pt_node in (p_top, p_bl, p_br):
    draw_round_segment(p_hub, pt_node, width_units=2.4, color=DARK)

# Outer IC pins on the 3 GPU modules
for dy_pin in (-5.5, 5.5):
    # Top module left & right pins
    draw_round_segment((31.0, p_top[1] + dy_pin), (36.0, p_top[1] + dy_pin), width_units=2.2, color=DARK)
    draw_round_segment((64.0, p_top[1] + dy_pin), (69.0, p_top[1] + dy_pin), width_units=2.2, color=DARK)
    # Bottom-left module outer left pins
    draw_round_segment((8.0 + 3.0, p_bl[1] + dy_pin), (14.0, p_bl[1] + dy_pin), width_units=2.2, color=DARK)
    # Bottom-right module outer right pins
    draw_round_segment((86.0, p_br[1] + dy_pin), (89.0, p_br[1] + dy_pin), width_units=2.2, color=DARK)

# Central NVSwitch / high-speed link hub
polygon(
    [(50.0, 53.5), (57.0, 46.5), (50.0, 39.5), (43.0, 46.5)],
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.2, shape_r=2.0),
)
circle((50.0, 46.5), radius=2.1, style=fill_style(WHITE, border_color=DARK, border_units=1.6))

# 3 GPU processor modules with 2x2 shader core grids
for gx, gy in (p_top, p_bl, p_br):
    rectangle(
        (gx, gy),
        width=28.0,
        height=26.0,
        style=fill_style(WHITE, border_color=DARK, border_units=w, shape_r=4.5),
    )

    sub_cores = [
        (gx - 5.2, gy + 4.8, PASTEL_BLUE),
        (gx + 5.2, gy + 4.8, PASTEL_BLUE),
        (gx - 5.2, gy - 4.8, PASTEL_BLUE),
        (gx + 5.2, gy - 4.8, PASTEL_GREEN),
    ]
    for cx, cy, col in sub_cores:
        rectangle(
            (cx, cy),
            width=7.6,
            height=6.8,
            style=fill_style(col, border_color=DARK, border_units=1.8, shape_r=1.5),
        )

save()
