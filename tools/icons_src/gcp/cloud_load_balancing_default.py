# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: cloud_load_balancing."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.utils import Gcp, Icon

Icon.setup()

rectangle((50.0, 61.0), width=8.5, height=18.0, style=Icon.fill_style(Gcp.TECH_MID))

leg_w = 9.0
leg_xs = (19.5, 50.0, 80.5)
rectangle((50.0, 48.0), width=70.0, height=8.0, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
for lx in leg_xs:
    rectangle((lx, 38.0), width=leg_w, height=12.0, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

rectangle((37.0, 81.0), width=26.0, height=22.0, style=Icon.fill_style(Gcp.TECH_LIGHT))
rectangle((63.0, 81.0), width=26.0, height=22.0, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

half_w = 12.5
block_h = 24.0
block_cy = 20.0
for cx in leg_xs:
    rectangle((cx - half_w / 2.0, block_cy), width=half_w, height=block_h, style=Icon.fill_style(Gcp.TECH_LIGHT))
    rectangle((cx + half_w / 2.0, block_cy), width=half_w, height=block_h, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

save()
