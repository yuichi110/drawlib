# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: smart_tv."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w = Icon.ORIG_STROKE

# Left and right angled V-legs
for cx_top, dir_x in ((29.0, -1.0), (71.0, 1.0)):
    leg_pts = [
        (cx_top - 3.5, 32.0),
        (cx_top + 3.5, 32.0),
        (cx_top + dir_x * 9.0 + 2.8, 17.0),
        (cx_top + dir_x * 9.0 - 2.8, 17.0),
    ]
    polygon(leg_pts, style=Icon.fill_style(Icon.PASTEL_BLUE))
    Icon.draw_round_polyline(leg_pts, width_units=w, color=Icon.DARK, closed=True)

# Large cinematic TV bezel and WHITE screen
rectangle(
    (50.0, 56.0),
    width=76.0,
    height=48.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w, shape_r=4.5),
)
rectangle(
    (50.0, 56.0),
    width=66.0,
    height=38.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0, shape_r=2.0),
)

# Centered PASTEL_GREEN media play triangle
play_pts = [
    (43.0, 66.5),
    (43.0, 45.5),
    (61.5, 56.0),
]
polygon(play_pts, style=Icon.fill_style(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(play_pts, width_units=2.0, color=Icon.DARK, corner_r=1.8, closed=True)

save()
