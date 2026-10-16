# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: llamaindex."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = 1.9
SCALE = 0.95
# Diagonal normal matching official SVG linearGradient (4.021, 2.02) -> (24.613, 19.277)
SLOPE_X = 20.592 / 17.257

# Softened Drawlib-toned stops matching official LlamaIndex SVG offsets
STOPS: list[tuple[float, tuple[float, float, float]]] = [
    (0.062, (248.0, 224.0, 224.0)),  # softened #F6DCD9 (warm blush)
    (0.326, (246.0, 175.0, 226.0)),  # softened #FFA5EA (pastel pink)
    (0.589, (110.0, 220.0, 238.0)),  # softened #45DFF8 (pastel cyan)
    (1.000, (195.0, 152.0, 238.0)),  # softened #BC8DEB (pastel purple)
]


def _scale_pt(x: float, y: float) -> tuple[float, float]:
    """Scale raw icon point toward (50, 50) so outer border stays inside [9, 91]."""
    return (50.0 + SCALE * (x - 50.0), 50.0 + SCALE * (y - 50.0))


def _diag_val(pt: tuple[float, float]) -> float:
    return SLOPE_X * pt[0] - pt[1]


def _clip_halfplane(
    pts: list[tuple[float, float]],
    c_thresh: float,
    *,
    keep_ge: bool,
) -> list[tuple[float, float]]:
    """Sutherland-Hodgman polygon clip against SLOPE_X * x - y >= c_thresh (or <=)."""
    if not pts:
        return []
    out: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        v1 = _diag_val(p1) - c_thresh
        v2 = _diag_val(p2) - c_thresh
        in1 = v1 >= 0.0 if keep_ge else v1 <= 0.0
        in2 = v2 >= 0.0 if keep_ge else v2 <= 0.0
        if in1 and in2:
            out.append(p2)
        elif in1 and not in2:
            t = v1 / (v1 - v2)
            out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
        elif not in1 and in2:
            t = v1 / (v1 - v2)
            out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
            out.append(p2)
    return out


def _sample_llamaindex_hex(x: float, y: float) -> str:
    """Evaluate 4-stop LlamaIndex gradient at canvas point (x, y)."""
    x_raw = 50.0 + (x - 50.0) / SCALE
    y_raw = 50.0 + (y - 50.0) / SCALE
    sx = 12.0 + (x_raw - 50.0) / (82.0 / 24.0)
    sy = 12.0 - (y_raw - 50.0) / (82.0 / 24.0)

    dx = 24.613 - 4.021
    dy = 19.277 - 2.020
    t = ((sx - 4.021) * dx + (sy - 2.020) * dy) / (dx * dx + dy * dy)

    if t <= STOPS[0][0]:
        r, g, b = STOPS[0][1]
    elif t >= STOPS[-1][0]:
        r, g, b = STOPS[-1][1]
    else:
        r, g, b = STOPS[-1][1]
        for k in range(len(STOPS) - 1):
            t0, c0 = STOPS[k]
            t1, c1 = STOPS[k + 1]
            if t <= t1:
                u = (t - t0) / (t1 - t0)
                r = (1.0 - u) * c0[0] + u * c1[0]
                g = (1.0 - u) * c0[1] + u * c1[1]
                b = (1.0 - u) * c0[2] + u * c1[2]
                break

    return f"#{round(r):02X}{round(g):02X}{round(b):02X}"


raw_llama = [
    (17.42, 80.98),
    (18.08, 82.78),
    (19.63, 83.64),
    (21.92, 83.96),
    (23.57, 84.92),
    (23.95, 85.82),
    (23.64, 88.77),
    (23.08, 91.00),
    (24.70, 90.40),
    (26.66, 88.21),
    (26.66, 91.00),
    (29.37, 89.39),
    (31.75, 87.21),
    (33.85, 84.06),
    (34.94, 80.98),
    (35.75, 76.50),
    (36.42, 71.06),
    (36.91, 65.69),
    (37.22, 61.42),
    (44.80, 61.60),
    (53.03, 61.51),
    (58.50, 60.76),
    (63.67, 59.15),
    (68.80, 56.96),
    (71.33, 56.49),
    (74.16, 56.90),
    (76.93, 57.47),
    (79.13, 56.82),
    (80.73, 55.10),
    (82.07, 51.97),
    (82.58, 48.46),
    (82.04, 45.38),
    (80.32, 43.71),
    (79.13, 43.34),
    (78.58, 39.41),
    (79.13, 35.45),
    (79.94, 33.32),
    (79.94, 27.08),
    (80.74, 25.15),
    (81.08, 22.48),
    (80.56, 19.28),
    (79.94, 18.04),
    (80.16, 15.30),
    (79.79, 11.63),
    (79.13, 9.16),
    (74.74, 9.16),
    (75.56, 10.38),
    (76.53, 10.81),
    (76.92, 15.15),
    (76.66, 18.57),
    (76.36, 20.01),
    (74.32, 21.61),
    (72.59, 23.73),
    (71.82, 25.10),
    (71.51, 21.75),
    (70.48, 18.17),
    (69.14, 15.58),
    (67.43, 13.60),
    (67.43, 10.15),
    (63.05, 10.15),
    (63.72, 12.19),
    (64.83, 12.61),
    (66.42, 15.37),
    (67.43, 20.17),
    (66.81, 22.99),
    (64.98, 25.80),
    (63.21, 28.39),
    (62.70, 30.43),
    (63.05, 32.50),
    (60.35, 31.52),
    (56.33, 30.70),
    (52.55, 30.52),
    (48.22, 30.92),
    (45.17, 31.68),
    (45.11, 28.26),
    (44.92, 24.47),
    (44.21, 21.42),
    (43.39, 19.84),
    (43.43, 16.35),
    (43.23, 12.12),
    (42.16, 9.69),
    (41.60, 9.00),
    (37.21, 9.00),
    (38.20, 11.17),
    (39.81, 12.61),
    (39.92, 14.84),
    (39.64, 18.67),
    (39.00, 21.49),
    (38.15, 18.61),
    (36.73, 14.42),
    (35.00, 11.04),
    (34.29, 9.98),
    (31.04, 9.98),
    (31.53, 12.04),
    (32.67, 12.61),
    (33.75, 15.55),
    (34.47, 20.32),
    (34.25, 23.88),
    (33.64, 28.06),
    (33.64, 35.13),
    (31.04, 36.70),
    (28.47, 38.82),
    (26.33, 41.55),
    (24.86, 44.83),
    (24.46, 48.66),
    (24.71, 51.73),
    (23.66, 53.87),
    (22.93, 57.07),
    (22.86, 60.54),
    (23.08, 62.24),
    (22.47, 63.88),
    (22.12, 67.59),
    (22.40, 71.58),
    (23.51, 74.58),
    (23.89, 75.06),
    (23.89, 76.87),
    (21.79, 77.25),
    (19.52, 78.21),
    (17.83, 79.59),
]

llama_pts = [_scale_pt(x, y) for x, y in raw_llama]

# 1. Render smooth diagonal gradient strips clipped to the llama silhouette
c_vals = [_diag_val(p) for p in llama_pts]
c_min = min(c_vals) - 0.5
c_max = max(c_vals) + 0.5
num_bands = 84
c_step = (c_max - c_min) / num_bands
overlap = 0.22

for i in range(num_bands):
    c0_base = c_min + i * c_step
    c1_base = c_min + (i + 1) * c_step
    c0 = c0_base if i == 0 else c0_base - overlap
    c1 = c1_base if i == num_bands - 1 else c1_base + overlap

    band = _clip_halfplane(_clip_halfplane(llama_pts, c0, keep_ge=True), c1, keep_ge=False)
    if len(band) >= 3:
        mx = sum(p[0] for p in band) / len(band)
        my = sum(p[1] for p in band) / len(band)
        col_hex = _sample_llamaindex_hex(mx, my)
        polygon(band, style=fill_style(col_hex))

# 2. Single outer llama silhouette contour (no interior black seam lines)
draw_round_polyline(llama_pts, width_units=w, color=DARK, closed=True)

save()
