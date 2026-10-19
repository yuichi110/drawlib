# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: circleci."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
scale = 0.94


def _sc(x: float, y: float) -> tuple[float, float]:
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


_RAW_C_RING: list[tuple[float, float]] = [
    (9.70, 60.31),
    (9.59, 59.84),
    (9.64, 59.38),
    (9.79, 58.95),
    (10.04, 58.56),
    (10.37, 58.25),
    (10.77, 58.01),
    (11.24, 57.88),
    (11.58, 57.85),
    (28.09, 57.85),
    (28.56, 57.90),
    (28.97, 58.06),
    (29.32, 58.30),
    (29.61, 58.63),
    (29.85, 59.02),
    (30.99, 61.19),
    (32.36, 63.20),
    (33.93, 65.04),
    (35.70, 66.67),
    (37.64, 68.10),
    (39.74, 69.30),
    (41.97, 70.26),
    (44.32, 70.97),
    (46.77, 71.41),
    (49.30, 71.55),
    (52.77, 71.27),
    (56.07, 70.46),
    (59.15, 69.16),
    (61.95, 67.42),
    (64.45, 65.27),
    (66.60, 62.78),
    (68.34, 59.97),
    (69.64, 56.89),
    (70.45, 53.59),
    (70.73, 50.12),
    (70.45, 46.64),
    (69.64, 43.35),
    (68.34, 40.27),
    (66.60, 37.46),
    (64.45, 34.96),
    (61.95, 32.82),
    (59.15, 31.07),
    (56.07, 29.77),
    (52.77, 28.96),
    (49.30, 28.68),
    (46.74, 28.83),
    (44.27, 29.28),
    (41.92, 29.99),
    (39.69, 30.96),
    (37.60, 32.16),
    (35.67, 33.59),
    (33.91, 35.21),
    (32.35, 37.02),
    (30.99, 38.98),
    (29.85, 41.10),
    (29.61, 41.55),
    (29.32, 41.91),
    (28.97, 42.17),
    (28.56, 42.33),
    (28.09, 42.39),
    (11.58, 42.39),
    (11.11, 42.33),
    (10.68, 42.18),
    (10.30, 41.93),
    (9.99, 41.60),
    (9.75, 41.20),
    (9.61, 40.74),
    (9.59, 40.29),
    (9.70, 39.93),
    (11.41, 34.73),
    (13.75, 29.87),
    (16.69, 25.40),
    (20.15, 21.35),
    (24.11, 17.79),
    (28.50, 14.76),
    (33.28, 12.31),
    (38.39, 10.51),
    (43.79, 9.39),
    (49.42, 9.00),
    (56.06, 9.54),
    (62.36, 11.09),
    (68.24, 13.58),
    (73.61, 16.92),
    (78.39, 21.02),
    (82.49, 25.80),
    (85.83, 31.17),
    (88.32, 37.06),
    (89.87, 43.36),
    (90.41, 50.00),
    (89.87, 56.64),
    (88.32, 62.95),
    (85.83, 68.83),
    (82.49, 74.20),
    (78.39, 78.98),
    (73.61, 83.08),
    (68.24, 86.42),
    (62.36, 88.91),
    (56.06, 90.46),
    (49.42, 91.00),
    (43.79, 90.62),
    (38.39, 89.49),
    (33.28, 87.69),
    (28.50, 85.26),
    (24.11, 82.24),
    (20.15, 78.70),
    (16.69, 74.69),
    (13.75, 70.25),
    (11.41, 65.44),
]

c_ring_pts = [_sc(x, y) for x, y in _RAW_C_RING]
dot_center = _sc(49.42, 50.0)
dot_radius = 9.72 * scale

# 1. C-ring (Colors.Gray6) with transparent C-gap and inner aperture
polygon(c_ring_pts, style=Icon.fill_style(Colors.Gray6))
Icon.draw_round_polyline(c_ring_pts, width_units=w, color=Icon.DARK, closed=True)

# 2. Center dot (Colors.Gray6) with DARK w=1.9 outline
circle(
    dot_center,
    radius=dot_radius,
    style=Icon.fill_style(Colors.Gray6, border_color=Icon.DARK, border_units=w),
)

save()
