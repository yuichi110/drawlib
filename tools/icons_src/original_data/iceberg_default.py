# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: iceberg."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


def _arc_points(
    cx: float,
    cy: float,
    radius: float,
    deg_start: float,
    deg_end: float,
    steps: int = 32,
) -> list[tuple[float, float]]:
    """Sample circular arc points from deg_start to deg_end inclusive."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        ang = math.radians(deg_start + (deg_end - deg_start) * t)
        pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
    return pts


Icon.setup()

w = 2.0
cx, cy = 50.0, 50.0
r = 40.5
y_water = 67.5

# Angle where horizontal waterline y = 67.5 intersects circle of radius 40.5
ang_water = math.degrees(math.asin((y_water - cy) / r))  # ~25.60 deg
deg_wl = 180.0 - ang_water
deg_wr = ang_water

# 1. Sky cap above waterline (Colors.Blue1) and deep ocean below (Colors.Blue4)
sky_pts = _arc_points(cx, cy, r, deg_wr, deg_wl, steps=32)
ocean_pts = _arc_points(cx, cy, r, deg_wl, 360.0 + deg_wr, steps=56)

polygon(sky_pts, style=Icon.no_border_fill(Colors.Blue1))
polygon(ocean_pts, style=Icon.no_border_fill(Colors.Blue4))

# 2. Iceberg vertices (peak above waterline + deep faceted underwater mass below)
p_wl = (29.0, y_water)
p_wc = (50.0, y_water)
p_wr = (71.0, y_water)

p_top_l = (38.0, 78.5)
p_top_c = (51.5, 80.5)
p_top_r = (63.5, 77.5)

p_ul = (23.5, 54.0)
p_uc = (50.0, 48.0)
p_ur = (76.5, 55.0)

p_ml = (35.5, 34.5)
p_mc = (50.0, 32.0)
p_mr = (64.5, 35.5)

p_bot = (50.0, 15.5)

# Above-water snow facets (WHITE sunlit left + Colors.Blue2 shadow right)
polygon([p_wl, p_top_l, p_top_c, p_wc], style=Icon.no_border_fill(Icon.WHITE))
polygon([p_wc, p_top_c, p_top_r, p_wr], style=Icon.no_border_fill(Colors.Blue2))

# Underwater sunlit left facets (Colors.Teal3)
polygon([p_wl, p_wc, p_uc, p_ul], style=Icon.no_border_fill(Colors.Teal3))
polygon([p_ul, p_uc, p_mc, p_ml], style=Icon.no_border_fill(Colors.Teal3))
polygon([p_ml, p_mc, p_bot], style=Icon.no_border_fill(Colors.Teal3))

# Underwater shaded right facets (Colors.Blue3)
polygon([p_wc, p_wr, p_ur, p_uc], style=Icon.no_border_fill(Colors.Blue3))
polygon([p_uc, p_ur, p_mr, p_mc], style=Icon.no_border_fill(Colors.Blue3))
polygon([p_mc, p_mr, p_bot], style=Icon.no_border_fill(Colors.Blue3))

# 3. Waterline, internal facet seams, iceberg contour, and outer circular badge border
x_water_r = cx + r * math.cos(math.radians(ang_water))
x_water_l = cx - r * math.cos(math.radians(ang_water))
Icon.draw_round_segment((x_water_l, y_water), (x_water_r, y_water), width_units=1.8, color=Icon.DARK)

# Internal facet lines
seams = [
    (p_top_c, p_wc),
    (p_wc, p_uc),
    (p_uc, p_mc),
    (p_mc, p_bot),
    (p_ul, p_uc),
    (p_uc, p_ur),
    (p_ml, p_mc),
    (p_mc, p_mr),
    (p_wl, p_uc),
    (p_uc, p_mr),
]
for p1, p2 in seams:
    Icon.draw_round_segment(p1, p2, width_units=1.5, color=Icon.DARK)

# Outer iceberg silhouette border
iceberg_outer = [p_wl, p_top_l, p_top_c, p_top_r, p_wr, p_ur, p_mr, p_bot, p_ml, p_ul]
Icon.draw_round_polyline(iceberg_outer, width_units=1.8, color=Icon.DARK, closed=True)

# Outer circular badge border
circle_outer = _arc_points(cx, cy, r, 0.0, 360.0, steps=72)
Icon.draw_round_polyline(circle_outer[:-1], width_units=w, color=Icon.DARK, closed=True)

save()
