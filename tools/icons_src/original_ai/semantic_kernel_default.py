# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon: semantic_kernel."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    draw_round_polyline,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
SCALE = 0.95


def _s(x: float, y: float) -> tuple[float, float]:
    """Scale point toward (50, 50) so outer border stays inside [9, 91]."""
    return (50.0 + SCALE * (x - 50.0), 50.0 + SCALE * (y - 50.0))


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 20,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3.0 * (mt**2) * t * p1[0] + 3.0 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3.0 * (mt**2) * t * p1[1] + 3.0 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


# Key perimeter landmarks in raw [9..91] icon space
p_left_waist = _s(27.2, 50.0)
p_right_waist = _s(72.8, 50.0)
p_tl_twist = _s(21.6, 80.0)
p_tr_twist = _s(78.4, 80.0)
p_bl_twist = _s(21.6, 20.0)
p_br_twist = _s(78.4, 20.0)
p_center = (50.0, 50.0)
p_inner_tl = _s(39.0, 61.0)
p_inner_br = _s(61.0, 39.0)

SKY_CYAN = "#78D2FA"

# 1. Top-left to top-right sweeping arch (SKY_CYAN, +45 deg loop upper)
top_arch = [
    p_left_waist,
    *_cubic(p_left_waist, _s(18.0, 62.5), _s(16.5, 73.5), p_tl_twist, 16),
    *_cubic(p_tl_twist, _s(31.0, 91.5), _s(69.0, 91.5), p_tr_twist, 24),
    *_cubic(p_tr_twist, _s(66.0, 79.5), _s(52.0, 72.0), p_inner_tl, 16),
]

# 2. Top-right lobe (Colors.Blue3, +45 deg loop right fold)
top_right_lobe = [
    p_inner_tl,
    *_cubic(p_inner_tl, _s(52.0, 72.0), _s(66.0, 79.5), p_tr_twist, 16),
    *_cubic(p_tr_twist, _s(83.5, 73.5), _s(82.0, 62.5), p_right_waist, 16),
    p_inner_br,
    p_center,
]

# 3. Bottom-right to bottom-left sweeping arch (Colors.Purple3, -45 deg loop lower)
bottom_arch = [
    p_right_waist,
    *_cubic(p_right_waist, _s(82.0, 37.5), _s(83.5, 26.5), p_br_twist, 16),
    *_cubic(p_br_twist, _s(69.0, 8.5), _s(31.0, 8.5), p_bl_twist, 24),
    *_cubic(p_bl_twist, _s(34.0, 20.5), _s(48.0, 28.0), p_inner_br, 16),
]

# 4. Bottom-left lobe (Colors.Purple2, -45 deg loop left fold)
bottom_left_lobe = [
    p_inner_br,
    *_cubic(p_inner_br, _s(48.0, 28.0), _s(34.0, 20.5), p_bl_twist, 16),
    *_cubic(p_bl_twist, _s(16.5, 26.5), _s(18.0, 37.5), p_left_waist, 16),
    p_inner_tl,
    p_center,
]

# Fill the four ribbon facets seamlessly
polygon(bottom_left_lobe, style=no_border_fill(Colors.Purple2))
polygon(bottom_arch, style=no_border_fill(Colors.Purple3))
polygon(top_right_lobe, style=no_border_fill(Colors.Blue3))
polygon(top_arch, style=no_border_fill(SKY_CYAN))

# Draw inner ribbon fold seams (1.6 DARK)
top_seam = [p_tr_twist, *_cubic(p_tr_twist, _s(66.0, 79.5), _s(52.0, 72.0), p_inner_tl, 16)]
bot_seam = [p_bl_twist, *_cubic(p_bl_twist, _s(34.0, 20.5), _s(48.0, 28.0), p_inner_br, 16)]
waist_left_seam = [p_left_waist, p_inner_tl]
waist_right_seam = [p_right_waist, p_inner_br]

for seam_pts in (top_seam, bot_seam, waist_left_seam, waist_right_seam):
    draw_round_polyline(seam_pts, width_units=1.6, color=DARK, closed=False)

# Draw outer figure-8 perimeter outline (w = 1.9 DARK)
outer_perimeter = [
    p_left_waist,
    *_cubic(p_left_waist, _s(18.0, 62.5), _s(16.5, 73.5), p_tl_twist, 16),
    *_cubic(p_tl_twist, _s(31.0, 91.5), _s(69.0, 91.5), p_tr_twist, 24),
    *_cubic(p_tr_twist, _s(83.5, 73.5), _s(82.0, 62.5), p_right_waist, 16),
    *_cubic(p_right_waist, _s(82.0, 37.5), _s(83.5, 26.5), p_br_twist, 16),
    *_cubic(p_br_twist, _s(69.0, 8.5), _s(31.0, 8.5), p_bl_twist, 24),
    *_cubic(p_bl_twist, _s(16.5, 26.5), _s(18.0, 37.5), p_left_waist, 16),
]
draw_round_polyline(outer_perimeter, width_units=w, color=DARK, closed=True)

# 5. Central sphere (Colors.Blue5)
circle(
    p_center,
    radius=16.4,
    style=fill_style(Colors.Blue5, border_color=DARK, border_units=w),
)

save()
