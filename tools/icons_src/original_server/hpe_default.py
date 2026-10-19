# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server vendor icon: hpe (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

h_pts: list[tuple[float, float]] = [(33.6, 61.71), (33.6, 38.29), (28.91, 38.29), (28.91, 47.89), (13.69, 47.89), (13.69, 38.29), (9.0, 38.29), (9.0, 61.71), (13.69, 61.71), (13.69, 52.38), (28.91, 52.38), (28.91, 61.71)]

p_outer: list[tuple[float, float]] = [(54.01, 61.71), (39.49, 61.71), (39.49, 38.29), (44.18, 38.29), (44.18, 44.24), (53.94, 44.24), (54.85, 44.27), (55.71, 44.34), (56.54, 44.47), (57.32, 44.65), (58.06, 44.87), (58.76, 45.14), (59.41, 45.45), (60.03, 45.81), (60.59, 46.21), (61.11, 46.65), (61.58, 47.12), (62.01, 47.64), (62.39, 48.19), (62.72, 48.77), (63.0, 49.39), (63.24, 50.04), (63.42, 50.72), (63.55, 51.43), (63.63, 52.17), (63.65, 52.93), (63.63, 53.7), (63.55, 54.44), (63.42, 55.16), (63.24, 55.84), (63.0, 56.5), (62.72, 57.12), (62.39, 57.72), (62.02, 58.27), (61.59, 58.79), (61.12, 59.28), (60.6, 59.72), (60.04, 60.12), (59.43, 60.48), (58.78, 60.8), (58.09, 61.07), (57.36, 61.3), (56.58, 61.48), (55.77, 61.61), (54.91, 61.69)]

p_hole: list[tuple[float, float]] = [(53.71, 48.73), (44.18, 48.73), (44.18, 57.28), (53.71, 57.28), (54.24, 57.26), (54.75, 57.23), (55.22, 57.17), (55.65, 57.08), (56.06, 56.97), (56.43, 56.84), (56.78, 56.68), (57.09, 56.51), (57.38, 56.31), (57.64, 56.09), (57.87, 55.86), (58.07, 55.6), (58.25, 55.33), (58.4, 55.03), (58.52, 54.72), (58.62, 54.4), (58.7, 54.05), (58.75, 53.69), (58.79, 53.32), (58.8, 52.93), (58.79, 52.54), (58.75, 52.18), (58.7, 51.82), (58.62, 51.49), (58.52, 51.17), (58.4, 50.87), (58.25, 50.59), (58.07, 50.32), (57.87, 50.08), (57.64, 49.85), (57.38, 49.64), (57.09, 49.46), (56.78, 49.29), (56.43, 49.14), (56.06, 49.02), (55.65, 48.92), (55.22, 48.84), (54.75, 48.78), (54.24, 48.74)]

e_top_pts: list[tuple[float, float]] = [(72.65, 55.1), (67.96, 55.1), (67.96, 61.71), (91.0, 61.71), (91.0, 57.28), (72.65, 57.28)]

e_bottom_pts: list[tuple[float, float]] = [(72.65, 48.49), (72.65, 42.72), (91.0, 42.72), (91.0, 38.29), (67.96, 38.29), (67.96, 52.93), (91.0, 52.93), (91.0, 48.49)]

# 1. H, P (with transparent hole), and E top bar in flat dark slate-gray (#4A5568)
polygon(h_pts, style=Icon.no_border_fill("#4A5568"))
polygon(p_outer, holes=[p_hole], style=Icon.fill_style("#4A5568"))
polygon(e_top_pts, style=Icon.no_border_fill("#4A5568"))

# 2. E lower wide rectangular frame in pastel emerald-teal (#4DB6AC)
polygon(e_bottom_pts, style=Icon.no_border_fill("#4DB6AC"))

# 3. DARK w=1.9 outlines on all contours
for ring in (h_pts, p_outer, p_hole, e_top_pts, e_bottom_pts):
    Icon.draw_round_polyline(ring, width_units=w, color=Icon.DARK, closed=True)

save()
# fmt: on
