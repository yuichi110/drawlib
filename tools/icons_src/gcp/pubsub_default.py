# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: pubsub."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.utils import Gcp, Icon

Icon.setup()

cx, cy = 50.0, 50.0
orbit_r = 32.5

main_angles = (90.0, 210.0, 330.0)
for deg in main_angles:
    Gcp.draw_radial_spoke(
        cx,
        cy,
        deg,
        r_inner=15.5,
        r_outer=orbit_r,
        width_units=7.2,
        color=Gcp.TECH_MID,
    )

circle((cx, cy), radius=12.0, style=Icon.fill_style(Gcp.TECH_LIGHT))

for deg in main_angles:
    rad = math.radians(deg)
    ox = cx + orbit_r * math.cos(rad)
    oy = cy + orbit_r * math.sin(rad)
    circle((ox, oy), radius=9.5, style=Icon.fill_style(Gcp.TECH_LIGHT))

sat_angles = (30.0, 150.0, 270.0)
for deg in sat_angles:
    rad = math.radians(deg)
    sx = cx + orbit_r * math.cos(rad)
    sy = cy + orbit_r * math.sin(rad)
    circle((sx, sy), radius=7.5, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

save()
