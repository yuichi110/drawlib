# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: gpu_server."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# High-density AI/GPU server chassis
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=60.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=7.0),
)

# Inner white motherboard tray
rectangle(
    (50.0, 50.0),
    width=66.0,
    height=46.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=4.0),
)

# Top high-speed NVLink / GPU interconnect bridge bar
Icon.draw_round_segment((27.5, 68.0), (72.5, 68.0), width_units=2.0, color=Icon.DARK)

# 4 parallel vertical GPU accelerator modules
for gx in (27.5, 42.5, 57.5, 72.5):
    Icon.draw_round_segment((gx, 65.0), (gx, 68.0), width_units=2.0, color=Icon.DARK)
    rectangle(
        (gx, 48.0),
        width=11.0,
        height=34.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
    )
    # Pastel green GPU processor die at top of module
    rectangle(
        (gx, 57.0),
        width=6.8,
        height=6.8,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=1.8, shape_r=1.5),
    )
    # Horizontal heatsink fins on lower half of module
    for fin_y in (48.5, 43.5, 38.5):
        Icon.draw_round_segment((gx - 3.0, fin_y), (gx + 3.0, fin_y), width_units=1.8, color=Icon.DARK)

save()
