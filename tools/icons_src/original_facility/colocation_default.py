# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: colocation."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _top_rounded_box(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = [(x0, y0), (x1, y0)]
    steps = 10
    for i in range(steps + 1):
        ang = math.radians(0.0 + 90.0 * (i / steps))
        pts.append((x1 - r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    for i in range(steps + 1):
        ang = math.radians(90.0 + 90.0 * (i / steps))
        pts.append((x0 + r + r * math.cos(ang), y1 - r + r * math.sin(ang)))
    return pts


# 1. Central Meet-Me Room link spine behind the two tenant towers
spine_pts = _top_rounded_box(42.0, 14.0, 58.0, 74.0, 3.0)
polygon(spine_pts, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(spine_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 2. Left Tenant A building wing (PASTEL_BLUE)
left_pts = _top_rounded_box(15.0, 14.0, 46.0, 82.0, 4.0)
polygon(left_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE))
Icon.draw_round_polyline(left_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 3. Right Tenant B building wing (PASTEL_BLUE_LIGHT)
right_pts = _top_rounded_box(54.0, 14.0, 85.0, 82.0, 4.0)
polygon(right_pts, style=Icon.no_border_fill(Icon.PASTEL_BLUE_LIGHT))
Icon.draw_round_polyline(right_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 4. Tenant rack bays in top and bottom of each wing
for cx in (30.5, 69.5):
    for cy in (71.0, 60.0, 24.5):
        rectangle(
            (cx, cy),
            width=18.0,
            height=6.0,
            style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=2.0),
        )

# 5. Cross-connect links reaching from center ring into left and right tenant wings
hub_cy = 43.0
Icon.draw_round_segment((28.0, hub_cy), (72.0, hub_cy), width_units=w_outer, color=Icon.DARK)
for node_x in (26.5, 73.5):
    circle(
        (node_x, hub_cy),
        radius=3.8,
        style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_inner),
    )

# 6. Central PASTEL_GREEN cross-connect hub ring
circle(
    (50.0, hub_cy),
    radius=14.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)
circle(
    (50.0, hub_cy),
    radius=6.8,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_outer),
)

# 7. Ground foundation line
Icon.draw_round_segment((11.5, 14.0), (88.5, 14.0), width_units=w_outer, color=Icon.DARK)

save()
