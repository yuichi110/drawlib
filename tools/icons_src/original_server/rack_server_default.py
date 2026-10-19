# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: rack_server."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Main 2U rackmount server chassis
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=34.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=6.0),
)

# Left and right rack mounting ears with screw dots
for ear_x in (16.8, 83.2):
    rectangle(
        (ear_x, 50.0),
        width=4.8,
        height=24.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
    )
    for screw_y in (57.5, 42.5):
        circle((ear_x, screw_y), radius=1.1, style=Icon.fill_style(Icon.DARK))

# 3 side-by-side hot-swap drive bays on left/center
for bay_x in (28.5, 41.5, 54.5):
    rectangle(
        (bay_x, 50.0),
        width=9.5,
        height=20.0,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.5),
    )
    Icon.draw_round_segment((bay_x - 2.0, 44.5), (bay_x + 2.0, 44.5), width_units=1.8, color=Icon.DARK)
    circle((bay_x, 55.0), radius=1.3, style=Icon.fill_style(Icon.DARK))

# Right-side power LED and ventilation slots
circle(
    (71.5, 55.5),
    radius=4.2,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0),
)
for vent_y in (46.0, 41.5):
    Icon.draw_round_segment((65.0, vent_y), (77.5, vent_y), width_units=2.0, color=Icon.DARK)

save()
