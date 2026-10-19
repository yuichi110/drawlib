# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Server icon: dell_nas_storage_default."""

from drawlib.canvas import save
from drawlib.shapes import arc, polygon
from drawlib.styles import Colors
from drawlib.utils import Dell, Icon

Icon.setup()

# Circular storage platter on top-left (cx=46.0, cy=54.0, outer r=35.0 -> centerline r=32.6)
cx, cy = 46.0, 54.0
r_outer = 32.6
r_hub = 8.2

# Platter outer DELL_BLUE ring (0 deg to 260 deg, stopping cleanly before the folder)
arc(
    (cx, cy),
    width=r_outer * 2.0,
    height=r_outer * 2.0,
    angle_start=0.0,
    angle_end=260.0,
    style=Icon.stroke_style(Dell.BLUE, width_units=4.8),
)

# Inner hub ring top semicircle (outer r=10.5 -> centerline r=8.2, 0 deg to 180 deg)
arc(
    (cx, cy),
    width=r_hub * 2.0,
    height=r_hub * 2.0,
    angle_start=0.0,
    angle_end=180.0,
    style=Icon.stroke_style(Dell.BLUE, width_units=4.6),
)

# Foreground shared file folder (outer x=46..89, y=12..46, tab y=46 stepping down to y=41)
folder_pts = [
    (48.4, 14.4),
    (86.6, 14.4),
    (86.6, 38.6),
    (66.0, 38.6),
    (61.5, 43.6),
    (48.4, 43.6),
]
polygon(
    folder_pts,
    style=Icon.fill_style(
        Colors.Transparent,
        border_color=Dell.BLUE,
        border_units=4.8,
        shape_r=(2.5, 2.5, 2.5, 1.5, 1.5, 2.5),
    ),
)

save()
