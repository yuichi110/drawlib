# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: compute_engine (default 3-tone blue variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon, rectangle
from drawlib.utils import Gcp, Icon

Icon.setup()

pin_w = 9.0
pin_coords = (31.5, 50.0, 68.5)

# 1. Top and Left pins in GCP_TECH_MED_LIGHT
for pos in pin_coords:
    rectangle((pos, 86.0), width=pin_w, height=12.0, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
    rectangle((14.0, pos), width=12.0, height=pin_w, style=Icon.fill_style(Gcp.TECH_MED_LIGHT))

# 2. Bottom and Right pins in GCP_TECH_MID
for pos in pin_coords:
    rectangle((pos, 14.0), width=pin_w, height=12.0, style=Icon.fill_style(Gcp.TECH_MID))
    rectangle((86.0, pos), width=12.0, height=pin_w, style=Icon.fill_style(Gcp.TECH_MID))

# 3. Outer square frame in GCP_TECH_LIGHT with white interior cutout
rectangle((50.0, 50.0), width=60.0, height=60.0, style=Icon.fill_style(Gcp.TECH_LIGHT))
rectangle((50.0, 50.0), width=42.0, height=42.0, style=Icon.fill_style(Icon.WHITE))

# 4. Inner 3-tone faceted core ([36.5, 63.5])
c0, c1 = 36.5, 63.5
polygon([(c0, c0), (c0, c1), (c1, c1)], style=Icon.fill_style(Gcp.TECH_LIGHT))
polygon([(c0, c0), (c1, c0), (50.0, 50.0)], style=Icon.fill_style(Gcp.TECH_MED_LIGHT))
polygon([(c1, c0), (c1, c1), (50.0, 50.0)], style=Icon.fill_style(Gcp.TECH_MID))

save()
