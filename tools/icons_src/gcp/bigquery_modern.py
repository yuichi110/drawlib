# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: bigquery."""

from drawlib.canvas import save
from drawlib.shapes import wedge
from drawlib.utils import Gcp, Icon

Icon.setup()

bar_width = 6.8
r_cap = bar_width / 2.0
bars = [
    (30.0, 26.0, 62.0 - r_cap),
    (45.0, 22.0, 74.0 - r_cap),
    (60.0, 26.0, 52.0 - r_cap),
]
for bx, y_bot, y_top in bars:
    Icon.draw_capsule(
        (bx, y_bot),
        (bx, y_top),
        width_units=bar_width,
        color=Gcp.GREEN,
        cap_start=False,
        cap_end=True,
    )

Icon.draw_capsule((69.0, 31.0), (90.0, 10.0), width_units=8.5, color=Gcp.BLUE)

ring_center = (45.0, 55.0)
ring_r = 38.0
ring_w = 8.5
wedge(ring_center, radius=ring_r, angle_start=45.0, angle_end=180.0, width=ring_w, style=Icon.fill_style(Gcp.RED))
wedge(ring_center, radius=ring_r, angle_start=180.0, angle_end=310.0, width=ring_w, style=Icon.fill_style(Gcp.YELLOW))
wedge(ring_center, radius=ring_r, angle_start=310.0, angle_end=405.0, width=ring_w, style=Icon.fill_style(Gcp.BLUE))

save()
