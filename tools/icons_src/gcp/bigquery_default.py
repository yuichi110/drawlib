# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon: bigquery (default 3-tone blue variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon, wedge
from drawlib.utils import Gcp, Icon

Icon.setup()

cx, cy = 45.0, 55.0
r_clip = 25.0


def _draw_clipped_bar(x0: float, x1: float, y_top: float, color: str) -> None:
    pts: list[tuple[float, float]] = [(x0, y_top), (x1, y_top)]
    steps = 16
    for i in range(steps + 1):
        x = x1 - (x1 - x0) * (i / steps)
        dx = x - cx
        dy = math.sqrt(max(0.0, r_clip * r_clip - dx * dx))
        pts.append((x, cy - dy))
    polygon(pts, style=Icon.fill_style(color))


# 1. Three interior vertical bars clipped cleanly along a concentric bottom arc
_draw_clipped_bar(27.5, 35.0, 54.0, Gcp.TECH_LIGHT)
_draw_clipped_bar(40.5, 49.5, 66.0, Gcp.TECH_MED_LIGHT)
_draw_clipped_bar(55.0, 62.5, 50.0, Gcp.TECH_LIGHT)

# 2. Diagonal handle at bottom-right in GCP_TECH_MID
polygon(
    [(67.0, 26.0), (74.0, 33.0), (92.0, 15.0), (85.0, 8.0)],
    style=Icon.fill_style(Gcp.TECH_MID, shape_r=(0.0, 0.0, 2.5, 2.5)),
)

# 3. Magnifying glass ring in GCP_TECH_MED_LIGHT
wedge(
    (cx, cy),
    radius=37.0,
    angle_start=0.0,
    angle_end=360.0,
    width=8.5,
    style=Icon.fill_style(Gcp.TECH_MED_LIGHT),
)

save()
