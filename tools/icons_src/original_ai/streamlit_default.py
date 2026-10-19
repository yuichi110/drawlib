# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: streamlit."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
w_seam = 1.6
scale = 0.945


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Scale points around canvas center (50.0, 50.0)."""
    return [(50.0 + (x - 50.0) * scale, 50.0 + (y - 50.0) * scale) for x, y in pts]


# Key crown vertices (unscaled)
v_left_valley = (35.62, 52.14)
v_right_valley = (64.38, 52.14)
v_fold_br_left = (77.24, 30.14)
v_fold_br_right = (78.26, 31.47)

# Left tip rounded arc (around (10.0, 64.5))
left_tip = [
    (10.57, 65.35),
    (10.07, 65.46),
    (9.61, 65.34),
    (9.25, 65.04),
    (9.03, 64.62),
    (9.02, 64.13),
    (9.07, 63.96),
]

# Bottom-left corner + gently curved bottom base + bottom-right corner
bottom_base = [
    (21.79, 31.53),
    (22.18, 30.80),
    (22.82, 30.11),
    (23.61, 29.59),
    (24.50, 29.24),
    (25.79, 29.02),
    (31.83, 28.44),
    (37.89, 28.03),
    (43.95, 27.78),
    (50.01, 27.70),
    (56.08, 27.78),
    (62.14, 28.03),
    (68.19, 28.44),
    (74.24, 29.02),
    (75.53, 29.19),
    (76.49, 29.61),
    v_fold_br_left,
]

# Right wing rounded tip (around (90.0, 64.5))
right_tip = [
    (90.94, 63.96),
    (91.00, 64.36),
    (90.90, 64.84),
    (90.61, 65.21),
    (90.20, 65.44),
    (89.71, 65.45),
    (89.34, 65.33),
]

# Center peak rounded tip (around (50.0, 72.3))
center_tip = [
    (48.68, 71.60),
    (49.10, 72.02),
    (49.62, 72.25),
    (50.00, 72.30),
    (50.37, 72.25),
    (50.90, 72.02),
    (51.32, 71.60),
]

# 1. Right side wing (#9E353F, softened #7D353B deep burgundy-red)
right_wing = _sc([v_right_valley, v_fold_br_right, *right_tip])
polygon(right_wing, style=Icon.no_border_fill("#9E353F"))

# 2. Center peak (Colors.Red4, softened #BD4043 medium crimson)
center_peak = _sc([v_left_valley, *center_tip, v_right_valley, v_fold_br_right, v_fold_br_left])
polygon(center_peak, style=Icon.no_border_fill(Colors.Red4))

# 3. Left front wing (Colors.Red3, softened #FF4B4B bright coral-red)
left_wing = _sc([v_left_valley, *left_tip, *bottom_base])
polygon(left_wing, style=Icon.no_border_fill(Colors.Red3))

# 4. Internal fold seams
p_lv, p_rv, p_fbl, p_fbr = _sc([v_left_valley, v_right_valley, v_fold_br_left, v_fold_br_right])
Icon.draw_round_segment(p_lv, p_fbl, width_units=w_seam, color=Icon.DARK)
Icon.draw_round_segment(p_rv, p_fbr, width_units=w_seam, color=Icon.DARK)

# 5. Unified outer crown silhouette
outer_crown = _sc(
    [
        v_left_valley,
        *left_tip,
        *bottom_base,
        v_fold_br_right,
        *right_tip,
        v_right_valley,
        *reversed(center_tip),
    ]
)
Icon.draw_round_polyline(outer_crown, width_units=w, color=Icon.DARK, closed=True)

save()
