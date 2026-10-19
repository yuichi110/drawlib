# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: github."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_inner = 1.7

cx, cy = 50.0, 50.0
r_badge = 39.0
scale = r_badge / 41.0

# Raw Octocat contour from official SVG (centered around (50.0, 48.99), r=41.0)
_RAW_OCTOCAT: list[tuple[float, float]] = [
    (37.04, 10.08),
    (37.61, 10.01),
    (38.12, 10.04),
    (38.55, 10.14),
    (38.91, 10.30),
    (39.21, 10.52),
    (39.44, 10.78),
    (39.62, 11.08),
    (39.75, 11.39),
    (39.82, 11.72),
    (39.84, 12.22),
    (39.83, 13.82),
    (39.81, 16.25),
    (39.79, 19.69),
    (38.14, 19.39),
    (36.63, 19.22),
    (35.24, 19.17),
    (33.97, 19.24),
    (32.82, 19.40),
    (31.77, 19.64),
    (30.83, 19.95),
    (29.99, 20.32),
    (29.25, 20.73),
    (28.60, 21.18),
    (28.03, 21.64),
    (27.55, 22.11),
    (26.80, 23.01),
    (26.31, 23.78),
    (25.97, 24.52),
    (25.39, 25.84),
    (24.78, 26.97),
    (24.16, 27.91),
    (23.56, 28.68),
    (22.99, 29.30),
    (22.49, 29.78),
    (21.87, 30.25),
    (21.42, 30.52),
    (20.92, 30.89),
    (20.23, 31.50),
    (19.89, 31.99),
    (19.84, 32.18),
    (19.91, 32.50),
    (20.16, 32.72),
    (20.53, 32.87),
    (21.13, 32.98),
    (21.70, 33.02),
    (22.88, 32.83),
    (23.93, 32.46),
    (24.87, 31.97),
    (25.69, 31.40),
    (26.39, 30.80),
    (26.96, 30.19),
    (27.58, 29.41),
    (27.98, 28.79),
    (28.55, 27.91),
    (29.14, 27.14),
    (29.76, 26.48),
    (30.40, 25.93),
    (31.06, 25.47),
    (31.73, 25.09),
    (32.41, 24.80),
    (33.77, 24.43),
    (35.11, 24.31),
    (36.39, 24.38),
    (37.58, 24.59),
    (38.64, 24.89),
    (39.92, 25.38),
    (40.12, 26.52),
    (40.42, 27.54),
    (40.78, 28.45),
    (41.20, 29.25),
    (41.83, 30.16),
    (42.52, 30.87),
    (41.15, 31.04),
    (38.42, 31.53),
    (35.76, 32.26),
    (33.22, 33.28),
    (30.85, 34.66),
    (28.74, 36.44),
    (26.92, 38.70),
    (25.48, 41.48),
    (24.45, 44.85),
    (23.91, 48.86),
    (23.84, 51.13),
    (23.95, 53.09),
    (24.26, 54.93),
    (24.76, 56.68),
    (25.44, 58.31),
    (26.30, 59.83),
    (27.31, 61.25),
    (28.06, 62.13),
    (27.82, 62.80),
    (27.54, 63.86),
    (27.32, 65.28),
    (27.24, 67.02),
    (27.40, 69.05),
    (27.90, 71.33),
    (28.46, 72.98),
    (29.12, 73.07),
    (30.17, 73.03),
    (31.74, 72.73),
    (33.85, 72.03),
    (36.51, 70.76),
    (39.74, 68.78),
    (42.23, 69.38),
    (44.79, 69.80),
    (47.39, 70.07),
    (50.00, 70.16),
    (52.61, 70.07),
    (55.21, 69.80),
    (57.77, 69.38),
    (60.27, 68.78),
    (63.50, 70.76),
    (66.16, 72.03),
    (68.26, 72.73),
    (69.82, 73.03),
    (70.87, 73.07),
    (71.53, 72.98),
    (72.10, 71.33),
    (72.60, 69.05),
    (72.76, 67.02),
    (72.68, 65.28),
    (72.46, 63.86),
    (72.18, 62.80),
    (71.94, 62.13),
    (72.69, 61.25),
    (73.71, 59.83),
    (74.56, 58.31),
    (75.24, 56.68),
    (75.74, 54.93),
    (76.05, 53.09),
    (76.16, 51.13),
    (76.09, 48.85),
    (75.54, 44.84),
    (74.52, 41.47),
    (73.06, 38.68),
    (71.25, 36.43),
    (69.13, 34.65),
    (66.76, 33.28),
    (64.21, 32.27),
    (61.54, 31.55),
    (58.81, 31.07),
    (57.43, 30.90),
    (58.08, 30.24),
    (58.87, 29.11),
    (59.53, 27.67),
    (59.99, 25.93),
    (60.18, 24.41),
    (60.22, 23.30),
    (60.20, 17.36),
    (60.17, 12.28),
    (60.22, 11.55),
    (60.38, 11.07),
    (60.67, 10.64),
    (61.10, 10.29),
    (61.67, 10.07),
    (62.40, 10.01),
    (62.99, 10.09),
]

octocat_open: list[tuple[float, float]] = [
    (cx + (x - 50.0) * scale, cy + (y - 48.99) * scale)
    for x, y in _RAW_OCTOCAT
]

# Close Octocat along the bottom arc of the r_badge circle
ang_r = math.atan2(octocat_open[-1][1] - cy, octocat_open[-1][0] - cx)
ang_l = math.atan2(octocat_open[0][1] - cy, octocat_open[0][0] - cx)
bottom_arc: list[tuple[float, float]] = []
for i in range(1, 20):
    a = ang_r + (ang_l - ang_r) * (i / 20)
    bottom_arc.append((cx + r_badge * math.cos(a), cy + r_badge * math.sin(a)))

octocat_closed = [*octocat_open, *bottom_arc]

# 1. Colors.Gray6 circular badge fill
circle((cx, cy), radius=r_badge, style=Icon.no_border_fill(Colors.Gray6))

# 2. WHITE Octocat silhouette fill + DARK inner outline
polygon(octocat_closed, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(octocat_open, width_units=w_inner, color=Icon.DARK, closed=False)

# 3. Outer circular badge DARK w=1.9 outline
circle((cx, cy), radius=r_badge, style=Icon.stroke_style(Icon.DARK, width_units=w))

save()
