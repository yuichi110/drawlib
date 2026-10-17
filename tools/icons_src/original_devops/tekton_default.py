# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: tekton."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    draw_round_segment,
    fill_style,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 1.9
w_inner = 1.75

CORAL_PINK = "#F79B86"
ROSE_PINK = "#F4B0C2"
cx = 41.5


def _mir(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Mirror point list horizontally across cx."""
    return [(2.0 * cx - x, y) for x, y in pts]


def _quad(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    steps: int = 14,
) -> list[tuple[float, float]]:
    """Sample quadratic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**2) * p0[0] + 2.0 * mt * t * p1[0] + (t**2) * p2[0],
                (mt**2) * p0[1] + 2.0 * mt * t * p1[1] + (t**2) * p2[1],
            )
        )
    return pts


def _cubic_pt(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    t: float,
) -> tuple[float, float]:
    mt = 1.0 - t
    return (
        (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
        (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
    )


def _arc(xc: float, yc: float, r: float, deg0: float, deg1: float, steps: int = 14) -> list[tuple[float, float]]:
    return [
        (
            xc + r * math.cos(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
            yc + r * math.sin(math.radians(deg0 + (deg1 - deg0) * (i / steps))),
        )
        for i in range(steps + 1)
    ]


# 1. Curved segmented tail behind right hip (alternating Colors.Purple2 and CORAL_PINK)
t_p0 = (55.5, 28.0)
t_p1 = (64.5, 45.0)
t_p2 = (79.5, 48.0)
t_p3 = (84.2, 35.5)
r_tail = 4.2
tail_steps = 48

tail_top: list[tuple[float, float]] = []
tail_bot: list[tuple[float, float]] = []
for i in range(tail_steps + 1):
    t = i / tail_steps
    px, py = _cubic_pt(t_p0, t_p1, t_p2, t_p3, t)
    dt = 1e-3
    t_next = min(1.0, t + dt)
    t_prev = max(0.0, t - dt)
    nx_p, ny_p = _cubic_pt(t_p0, t_p1, t_p2, t_p3, t_next)
    px_p, py_p = _cubic_pt(t_p0, t_p1, t_p2, t_p3, t_prev)
    dx, dy = nx_p - px_p, ny_p - py_p
    length = math.hypot(dx, dy)
    ux, uy = -dy / length, dx / length
    tail_top.append((px + r_tail * ux, py + r_tail * uy))
    tail_bot.append((px - r_tail * ux, py - r_tail * uy))

# Rounded tip cap at t=1.0
ang_top = math.degrees(math.atan2(tail_top[-1][1] - t_p3[1], tail_top[-1][0] - t_p3[0]))
ang_bot = math.degrees(math.atan2(tail_bot[-1][1] - t_p3[1], tail_bot[-1][0] - t_p3[0]))
if ang_bot > ang_top:
    ang_bot -= 360.0
tip_cap = _arc(t_p3[0], t_p3[1], r_tail, ang_top, ang_bot, steps=16)

# Split tail into 4 alternating color segments
seg_splits = [0, 13, 25, 37, tail_steps]
seg_colors = [Colors.Purple2, CORAL_PINK, Colors.Purple2, CORAL_PINK]
for idx in range(4):
    i0 = seg_splits[idx]
    i1 = seg_splits[idx + 1]
    if idx < 3:
        seg_poly = [*tail_top[i0 : i1 + 1], *reversed(tail_bot[i0 : i1 + 1])]
    else:
        seg_poly = [*tail_top[i0 : i1 + 1], *tip_cap[1:-1], *reversed(tail_bot[i0 : i1 + 1])]
    polygon(seg_poly, style=no_border_fill(seg_colors[idx]))

for split_i in seg_splits[1:-1]:
    p_top = tail_top[split_i]
    p_bot = tail_bot[split_i]
    mid_x = (p_top[0] + p_bot[0]) / 2.0
    mid_y = (p_top[1] + p_bot[1]) / 2.0
    dx, dy = p_bot[0] - p_top[0], p_bot[1] - p_top[1]
    ctrl = (mid_x - dy * 0.18, mid_y + dx * 0.18)
    seam_pts = [p_top, *_quad(p_top, ctrl, p_bot, 8)]
    draw_round_polyline(seam_pts, width_units=w_inner, color=DARK, closed=False)

tail_outline = [*tail_top, *tip_cap[1:-1], *reversed(tail_bot)]
draw_round_polyline(tail_outline, width_units=w, color=DARK, closed=True)

# 2. Hind legs & outer paws (symmetric around cx)
hind_hip_l = [
    (25.2, 32.5),
    *_quad((25.2, 32.5), (19.0, 29.5), (18.0, 24.0), 10),
    (25.8, 20.5),
]
hind_paw_l = [
    (18.0, 24.0),
    *_quad((18.0, 24.0), (17.5, 20.5), (19.8, 17.8), 8),
    *_quad((19.8, 17.8), (13.8, 16.5), (13.8, 11.8), 10),
    (27.5, 11.8),
    (25.8, 20.5),
]
for h_hip, h_paw in ((hind_hip_l, hind_paw_l), (_mir(hind_hip_l), _mir(hind_paw_l))):
    polygon(h_hip, style=no_border_fill(ROSE_PINK))
    polygon(h_paw, style=no_border_fill(WHITE))
    draw_round_polyline(h_hip, width_units=w, color=DARK, closed=True)
    draw_round_polyline(h_paw, width_units=w, color=DARK, closed=True)

draw_round_segment((19.8, 17.8), (23.8, 16.0), width_units=w_inner, color=DARK)
draw_round_segment((2.0 * cx - 19.8, 17.8), (2.0 * cx - 23.8, 16.0), width_units=w_inner, color=DARK)

# 3. Torso, front legs, collar & center chest
torso_bg = [
    (27.0, 48.8),
    (56.0, 48.8),
    (58.0, 32.0),
    (55.0, 14.0),
    (28.0, 14.0),
    (25.0, 32.0),
]
polygon(torso_bg, style=no_border_fill(WHITE))

# 4. Front legs & shoulders (WHITE)
front_leg_l = [
    (27.5, 48.8),
    *_quad((27.5, 48.8), (24.5, 40.2), (24.8, 30.5), 10),
    *_quad((24.8, 30.5), (25.2, 24.0), (27.2, 18.5), 8),
    (37.8, 18.5),
    (36.2, 31.2),
    (34.2, 48.8),
]
for f_leg in (front_leg_l, _mir(front_leg_l)):
    polygon(f_leg, style=no_border_fill(WHITE))
    draw_round_polyline(f_leg[:-1], width_units=w, color=DARK, closed=False)

# Center chest upper plate (ROSE_PINK) & lower belly (CORAL_PINK)
chest_upper = [(36.2, 31.2), (46.8, 31.2), (45.8, 24.2), (37.2, 24.2)]
chest_lower = [(37.2, 24.2), (45.8, 24.2), (43.5, 13.5), (39.5, 13.5)]
polygon(chest_upper, style=no_border_fill(ROSE_PINK))
polygon(chest_lower, style=no_border_fill(CORAL_PINK))
draw_round_polyline(chest_upper, width_units=w, color=DARK, closed=True)
draw_round_polyline(chest_lower, width_units=w, color=DARK, closed=True)

# Collar trapezoid (ROSE_PINK) + vertical chest stem
collar_pts = [
    (31.8, 48.5),
    (51.2, 48.5),
    (48.8, 39.8),
    *_quad((48.8, 39.8), (48.0, 38.8), (46.5, 38.8), 4),
    (36.5, 38.8),
    *_quad((36.5, 38.8), (35.0, 38.8), (34.2, 39.8), 4),
]
polygon(collar_pts, style=no_border_fill(ROSE_PINK))
draw_round_polyline(collar_pts, width_units=w, color=DARK, closed=True)
draw_round_segment((cx, 38.8), (cx, 31.2), width_units=w, color=DARK)

# Shoulder & knee seam arcs on front legs
for sign in (-1.0, 1.0):
    s_p0 = (cx + sign * 16.0, 39.5)
    s_p1 = (cx + sign * 10.0, 36.2)
    s_p2 = (cx + sign * 5.3, 31.2)
    draw_round_polyline([s_p0, *_quad(s_p0, s_p1, s_p2, 8)], width_units=w, color=DARK, closed=False)

    k_p0 = (cx + sign * 15.8, 24.5)
    k_p1 = (cx + sign * 10.2, 26.8)
    k_p2 = (cx + sign * 4.5, 24.2)
    draw_round_polyline([k_p0, *_quad(k_p0, k_p1, k_p2, 8)], width_units=w_inner, color=DARK, closed=False)

# Round front paws (WHITE) + 2 toe cleft lines each
paw_l = [
    (25.8, 13.5),
    *_quad((25.8, 13.5), (25.8, 19.8), (33.2, 19.8), 10),
    *_quad((33.2, 19.8), (40.6, 19.8), (40.6, 13.5), 10),
    *_quad((40.6, 13.5), (40.6, 10.8), (37.5, 10.8), 6),
    (28.9, 10.8),
    *_quad((28.9, 10.8), (25.8, 10.8), (25.8, 13.5), 6),
]
for p_pts in (paw_l, _mir(paw_l)):
    polygon(p_pts, style=no_border_fill(WHITE))
    draw_round_polyline(p_pts, width_units=w, color=DARK, closed=True)

for tx in (30.8, 35.6, 2.0 * cx - 35.6, 2.0 * cx - 30.8):
    draw_round_segment((tx, 10.8), (tx, 14.2), width_units=w_inner, color=DARK)

# 5. Ears (CORAL_PINK, behind head hood)
ear_l = [
    (16.0, 66.5),
    *_quad((16.0, 66.5), (10.5, 76.5), (12.0, 86.2), 12),
    *_quad((12.0, 86.2), (12.5, 88.8), (15.5, 88.5), 6),
    *_quad((15.5, 88.5), (22.5, 87.5), (28.5, 83.2), 10),
]
for e_pts in (ear_l, _mir(ear_l)):
    polygon(e_pts, style=no_border_fill(CORAL_PINK))
    draw_round_polyline(e_pts, width_units=w, color=DARK, closed=True)

# 6. Head hood (CORAL_PINK) & lower cheeks (WHITE)
head_top_arc = [
    (15.6, 58.2),
    *_quad((15.6, 58.2), (15.2, 72.0), (24.5, 80.5), 12),
    *_quad((24.5, 80.5), (32.5, 86.2), (cx, 86.2), 12),
    *_quad((cx, 86.2), (2.0 * cx - 32.5, 86.2), (2.0 * cx - 24.5, 80.5), 12),
    *_quad((2.0 * cx - 24.5, 80.5), (2.0 * cx - 15.2, 72.0), (2.0 * cx - 15.6, 58.2), 12),
]
head_bot_arc = [
    (2.0 * cx - 15.6, 58.2),
    *_quad((2.0 * cx - 15.6, 58.2), (2.0 * cx - 18.0, 48.0), (cx, 44.5), 14),
    *_quad((cx, 44.5), (18.0, 48.0), (15.6, 58.2), 14),
]
cheek_seam_l = [(15.6, 58.2), *_quad((15.6, 58.2), (23.5, 55.2), (32.5, 54.5), 10)]
cheek_seam_r = [(50.5, 54.5), *_quad((50.5, 54.5), (2.0 * cx - 23.5, 55.2), (2.0 * cx - 15.6, 58.2), 10)]

hood_poly = [*head_top_arc, *reversed(cheek_seam_r), *reversed(cheek_seam_l)]
cheeks_poly = [*cheek_seam_l, *cheek_seam_r, *head_bot_arc[1:]]

polygon(hood_poly, style=no_border_fill(CORAL_PINK))
polygon(cheeks_poly, style=no_border_fill(WHITE))
draw_round_polyline(cheek_seam_l, width_units=w, color=DARK, closed=False)
draw_round_polyline(cheek_seam_r, width_units=w, color=DARK, closed=False)
draw_round_polyline([*head_top_arc, *head_bot_arc[1:]], width_units=w, color=DARK, closed=True)

# Forehead vertical center seam + 4 tiny DARK dots
draw_round_segment((cx, 75.2), (cx, 86.2), width_units=w_inner, color=DARK)
for dx_off in (-2.8, 2.8):
    for dy_pos in (78.6, 82.2):
        circle((cx + dx_off, dy_pos), radius=0.85, style=no_border_fill(DARK))

# 7. Soft rose-pink eye mask (ROSE_PINK) & happy smiling eyes
mask_pts = [
    (22.5, 60.5),
    *_quad((22.5, 60.5), (23.5, 75.2), (cx, 75.2), 14),
    *_quad((cx, 75.2), (2.0 * cx - 23.5, 75.2), (2.0 * cx - 22.5, 60.5), 14),
    *_quad((2.0 * cx - 22.5, 60.5), (2.0 * cx - 22.2, 57.2), (50.5, 56.5), 8),
    (32.5, 56.5),
    *_quad((32.5, 56.5), (22.2, 57.2), (22.5, 60.5), 8),
]
polygon(mask_pts, style=no_border_fill(ROSE_PINK))
draw_round_polyline(mask_pts, width_units=w, color=DARK, closed=True)

for eye_cx in (31.5, 51.5):
    eye_arc = _arc(eye_cx, 63.2, 3.6, 15.0, 165.0, steps=12)
    draw_round_polyline(eye_arc, width_units=2.1, color=DARK, closed=False)

# 8. White muzzle (WHITE) & pink nose (Colors.Pink3)
muzzle_pts = [
    (32.2, 55.2),
    *_quad((32.2, 55.2), (32.8, 61.5), (cx, 61.5), 10),
    *_quad((cx, 61.5), (2.0 * cx - 32.8, 61.5), (50.8, 55.2), 10),
    *_quad((50.8, 55.2), (50.5, 50.8), (45.8, 50.8), 8),
    *_quad((45.8, 50.8), (42.8, 50.8), (cx, 53.6), 6),
    *_quad((cx, 53.6), (40.2, 50.8), (37.2, 50.8), 6),
    *_quad((37.2, 50.8), (32.5, 50.8), (32.2, 55.2), 8),
]
polygon(muzzle_pts, style=no_border_fill(WHITE))
draw_round_polyline(muzzle_pts, width_units=w, color=DARK, closed=True)

ellipse(
    (cx, 57.0),
    width=8.0,
    height=4.4,
    style=fill_style(Colors.Pink3, border_color=DARK, border_units=w_inner),
)
draw_round_segment((cx, 54.8), (cx, 53.6), width_units=w_inner, color=DARK)

save()
