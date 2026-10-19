# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: nvidia."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_seam = 1.6
scale = 0.945
NVIDIA_GREEN = "#7CC242"


def _sc_pt(x: float, y: float) -> tuple[float, float]:
    """Scale a point around canvas center (50.0, 50.0)."""
    return (50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale)


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale a list of points around canvas center (50.0, 50.0)."""
    return [_sc_pt(x, y) for x, y in pts]


x_split = 39.60
y_badge_bot = 22.04
y_badge_top = 77.95
x_badge_right = 91.00
r_corner = 3.6

# Rounded right-side corners for the green badge rectangle (unscaled)
right_bot_corner: list[tuple[float, float]] = []
right_top_corner: list[tuple[float, float]] = []
for i in range(13):
    ang_b = math.radians(-90.0 + 90.0 * (i / 12))
    right_bot_corner.append(
        (x_badge_right - r_corner + r_corner * math.cos(ang_b), y_badge_bot + r_corner + r_corner * math.sin(ang_b))
    )
    ang_t = math.radians(0.0 + 90.0 * (i / 12))
    right_top_corner.append(
        (x_badge_right - r_corner + r_corner * math.cos(ang_t), y_badge_top - r_corner + r_corner * math.sin(ang_t))
    )

# Spiral curves on left (x <= 39.60) and right (x >= 39.60)
left_outer_arch = [
    (39.60, 70.41),
    (36.55, 70.01),
    (33.57, 69.35),
    (30.68, 68.46),
    (27.90, 67.39),
    (25.24, 66.18),
    (22.71, 64.86),
    (20.34, 63.48),
    (18.15, 62.08),
    (16.15, 60.69),
    (14.36, 59.35),
    (12.79, 58.12),
    (11.48, 57.01),
    (10.42, 56.09),
    (9.64, 55.37),
    (9.00, 54.76),
    (9.39, 53.72),
    (10.61, 50.98),
    (12.73, 47.06),
    (15.84, 42.51),
    (17.79, 40.16),
    (20.01, 37.85),
    (22.51, 35.65),
    (25.30, 33.62),
    (28.40, 31.84),
    (31.81, 30.36),
    (35.54, 29.27),
    (39.60, 28.61),
]

left_inner_arch = [
    (39.60, 32.96),
    (36.62, 33.54),
    (33.89, 34.47),
    (31.41, 35.68),
    (29.15, 37.13),
    (27.12, 38.75),
    (25.30, 40.51),
    (23.69, 42.35),
    (22.29, 44.22),
    (21.08, 46.06),
    (20.05, 47.82),
    (19.21, 49.46),
    (18.53, 50.91),
    (18.02, 52.13),
    (17.66, 53.07),
    (17.38, 53.89),
    (18.41, 55.21),
    (19.51, 56.47),
    (20.66, 57.66),
    (21.87, 58.78),
    (23.13, 59.83),
    (24.44, 60.81),
    (25.80, 61.72),
    (27.20, 62.55),
    (28.64, 63.30),
    (30.12, 63.98),
    (31.63, 64.58),
    (33.17, 65.10),
    (34.74, 65.53),
    (36.34, 65.88),
    (37.96, 66.15),
    (39.60, 66.32),
]

left_crescent_outer = [
    (39.60, 37.61),
    (37.36, 38.17),
    (35.32, 38.95),
    (33.48, 39.91),
    (31.82, 41.03),
    (30.35, 42.27),
    (29.04, 43.59),
    (27.90, 44.95),
    (26.92, 46.32),
    (26.08, 47.66),
    (25.38, 48.94),
    (24.80, 50.13),
    (24.36, 51.18),
    (24.02, 52.05),
    (23.62, 53.30),
    (25.27, 54.87),
    (27.04, 56.29),
    (28.93, 57.56),
    (30.92, 58.66),
    (33.00, 59.59),
    (35.15, 60.34),
    (37.35, 60.90),
    (39.60, 61.27),
]

left_crescent_inner = [
    (39.60, 56.90),
    (38.61, 56.87),
    (37.65, 56.77),
    (36.70, 56.58),
    (35.76, 56.31),
    (34.86, 55.97),
    (33.98, 55.56),
    (33.14, 55.08),
    (32.34, 54.53),
    (31.59, 53.91),
    (30.89, 53.24),
    (30.25, 52.51),
    (30.51, 51.72),
    (31.00, 50.47),
    (31.78, 48.86),
    (32.87, 47.05),
    (34.31, 45.21),
    (36.12, 43.50),
    (38.33, 42.11),
    (39.60, 41.59),
]

right_cutout_upper = [
    (39.60, 70.41),
    (41.04, 70.50),
    (44.46, 70.43),
    (47.72, 70.01),
    (50.81, 69.29),
    (53.72, 68.31),
    (56.45, 67.13),
    (58.98, 65.80),
    (61.31, 64.36),
    (63.43, 62.87),
    (65.33, 61.36),
    (67.01, 59.90),
    (68.45, 58.53),
    (69.65, 57.30),
    (70.59, 56.26),
    (71.83, 54.75),
    (70.45, 53.13),
    (68.16, 50.69),
    (64.94, 47.64),
    (60.97, 44.38),
    (56.40, 41.32),
    (51.37, 38.88),
    (48.74, 38.02),
    (46.06, 37.46),
    (43.35, 37.27),
    (41.46, 37.35),
    (39.60, 37.61),
]

right_cutout_lower = [
    (39.60, 32.95),
    (42.72, 32.74),
    (45.21, 32.82),
    (47.62, 33.06),
    (49.95, 33.45),
    (52.21, 33.98),
    (54.41, 34.65),
    (56.53, 35.43),
    (58.61, 36.34),
    (60.63, 37.35),
    (62.60, 38.46),
    (64.53, 39.66),
    (66.42, 40.94),
    (68.28, 42.30),
    (70.11, 43.72),
    (71.92, 45.19),
    (73.71, 46.71),
    (75.49, 48.28),
    (78.09, 46.63),
    (81.70, 44.56),
    (84.82, 42.45),
    (82.99, 41.01),
    (80.92, 39.61),
    (78.63, 38.27),
    (76.14, 36.98),
    (73.51, 35.75),
    (70.74, 34.60),
    (67.88, 33.52),
    (64.95, 32.52),
    (61.99, 31.62),
    (59.03, 30.81),
    (56.10, 30.11),
    (53.22, 29.52),
    (50.43, 29.05),
    (47.77, 28.71),
    (45.25, 28.49),
    (42.92, 28.42),
    (39.60, 28.60),
]

right_island_outer = [
    (39.60, 66.32),
    (41.05, 66.40),
    (43.51, 66.34),
    (45.86, 66.02),
    (48.08, 65.47),
    (50.18, 64.73),
    (52.14, 63.84),
    (53.97, 62.84),
    (55.65, 61.76),
    (57.18, 60.63),
    (58.56, 59.50),
    (59.77, 58.40),
    (60.81, 57.37),
    (61.67, 56.45),
    (62.36, 55.67),
    (63.26, 54.53),
    (62.31, 53.28),
    (60.74, 51.38),
    (58.54, 49.01),
    (55.81, 46.47),
    (52.65, 44.09),
    (49.17, 42.20),
    (47.34, 41.52),
    (45.47, 41.09),
    (43.57, 40.94),
    (41.56, 41.10),
    (39.60, 41.59),
]

right_island_inner = [
    (39.60, 56.91),
    (40.54, 56.77),
    (42.14, 56.35),
    (43.47, 55.75),
    (44.59, 54.96),
    (45.57, 53.94),
    (46.49, 52.70),
    (47.43, 51.21),
    (49.01, 48.49),
    (55.99, 54.56),
    (54.96, 55.75),
    (53.82, 56.85),
    (52.60, 57.84),
    (51.29, 58.73),
    (49.91, 59.50),
    (48.47, 60.15),
    (46.98, 60.67),
    (45.45, 61.06),
    (43.89, 61.32),
    (42.31, 61.44),
    (39.60, 61.27),
]

# 1. Left spiral bands (NVIDIA_GREEN)
polygon(_sc([*left_outer_arch, *left_inner_arch]), style=Icon.no_border_fill(NVIDIA_GREEN))
polygon(_sc([*left_crescent_outer, *left_crescent_inner]), style=Icon.no_border_fill(NVIDIA_GREEN))

# 3. Right green badge minus white spiral cutout + inner green spiral island (NVIDIA_GREEN)
badge_green = _sc(
    [
        (x_split, y_badge_top),
        *right_cutout_upper,
        *right_cutout_lower,
        (x_split, y_badge_bot),
        *right_bot_corner,
        *right_top_corner,
    ]
)
polygon(badge_green, style=Icon.no_border_fill(NVIDIA_GREEN))
polygon(_sc([*right_island_outer, *right_island_inner]), style=Icon.no_border_fill(NVIDIA_GREEN))

# 4. Crisp structural seam along vertical split line x = 39.60
Icon.draw_round_segment(_sc_pt(x_split, y_badge_bot), _sc_pt(x_split, y_badge_top), width_units=w_seam, color=Icon.DARK)

# 5. Outer badge border (top, rounded right, bottom)
badge_outer_border = _sc(
    [
        (x_split, y_badge_top),
        *reversed(right_top_corner),
        *reversed(right_bot_corner),
        (x_split, y_badge_bot),
    ]
)
Icon.draw_round_polyline(badge_outer_border, width_units=w, color=Icon.DARK)

# 6. Continuous spiral eye borders
for curve in (
    left_outer_arch,
    left_inner_arch,
    left_crescent_outer,
    left_crescent_inner,
    right_cutout_upper,
    right_cutout_lower,
    right_island_outer,
    right_island_inner,
):
    Icon.draw_round_polyline(_sc(curve), width_units=w, color=Icon.DARK)

save()
