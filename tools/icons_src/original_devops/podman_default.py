# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps concept icon: podman."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_round_polyline,
    no_border_fill,
    setup_icon,
)

setup_icon()

w = 2.0
WATER_SKY = "#D6F0FF"


def _cubic(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample cubic Bezier curve excluding p0."""
    pts: list[tuple[float, float]] = []
    for i in range(1, steps + 1):
        t = i / steps
        mt = 1.0 - t
        pts.append(
            (
                (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0],
                (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1],
            )
        )
    return pts


def _round_corners(verts: list[tuple[float, float]], r: float, steps: int = 8) -> list[tuple[float, float]]:
    """Round polygon vertices by distance r along adjacent edges."""
    n = len(verts)
    out: list[tuple[float, float]] = []
    for i in range(n):
        p_prev = verts[(i - 1) % n]
        p_curr = verts[i]
        p_next = verts[(i + 1) % n]
        dx1, dy1 = p_prev[0] - p_curr[0], p_prev[1] - p_curr[1]
        dx2, dy2 = p_next[0] - p_curr[0], p_next[1] - p_curr[1]
        l1 = math.hypot(dx1, dy1)
        l2 = math.hypot(dx2, dy2)
        d = min(r, l1 * 0.4, l2 * 0.4)
        a = (p_curr[0] + dx1 / l1 * d, p_curr[1] + dy1 / l1 * d)
        b = (p_curr[0] + dx2 / l2 * d, p_curr[1] + dy2 / l2 * d)
        for s in range(steps + 1):
            t = s / steps
            mt = 1.0 - t
            out.append(
                (
                    (mt**2) * a[0] + 2.0 * mt * t * p_curr[0] + (t**2) * b[0],
                    (mt**2) * a[1] + 2.0 * mt * t * p_curr[1] + (t**2) * b[1],
                )
            )
    return out


def _inset_poly(verts: list[tuple[float, float]], dist: float) -> list[tuple[float, float]]:
    """Inset a CW polygon inward by dist perpendicular to each edge."""
    n = len(verts)
    lines_list: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for i in range(n):
        p1 = verts[i]
        p2 = verts[(i + 1) % n]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = math.hypot(dx, dy)
        # Inward normal for CW polygon is (dy / length, -dx / length)
        nx, ny = dy / length, -dx / length
        lines_list.append(((p1[0] + nx * dist, p1[1] + ny * dist), (dx, dy)))

    res: list[tuple[float, float]] = []
    for i in range(n):
        (p1, d1) = lines_list[(i - 1) % n]
        (p2, d2) = lines_list[i]
        det = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(det) < 1e-9:
            res.append(p2)
        else:
            t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / det
            res.append((p1[0] + t * d1[0], p1[1] + t * d1[1]))
    return res


def _clip_half_y(pts: list[tuple[float, float]], ym: float, *, keep_le: bool) -> list[tuple[float, float]]:
    """Clip polygon against horizontal line y = ym."""
    out: list[tuple[float, float]] = []
    n = len(pts)
    for i in range(n):
        a = pts[i]
        b = pts[(i + 1) % n]
        in_a = a[1] <= ym if keep_le else a[1] >= ym
        in_b = b[1] <= ym if keep_le else b[1] >= ym
        if in_a and in_b:
            out.append(b)
        elif in_a != in_b:
            t = (ym - a[1]) / (b[1] - a[1])
            out.append((a[0] + t * (b[0] - a[0]), ym))
            if in_b:
                out.append(b)
    return out


def _clip_y_between(
    poly: list[tuple[float, float]],
    y_min: float,
    y_max: float,
) -> list[tuple[float, float]]:
    """Clip polygon to horizontal band y_min <= y <= y_max."""
    step1 = _clip_half_y(poly, y_max, keep_le=True)
    return _clip_half_y(step1, y_min, keep_le=False) if step1 else []


def _clip_to_cw_convex(
    subj: list[tuple[float, float]],
    clip_cw: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    """Clip polygon subj against a clockwise convex polygon clip_cw."""
    out = list(subj)
    for i in range(len(clip_cw)):
        if not out:
            break
        c1 = clip_cw[i]
        c2 = clip_cw[(i + 1) % len(clip_cw)]
        dx_c = c2[0] - c1[0]
        dy_c = c2[1] - c1[1]
        inp = out
        out = []
        n = len(inp)
        for j in range(n):
            a = inp[j]
            b = inp[(j + 1) % n]
            ca = dx_c * (a[1] - c1[1]) - dy_c * (a[0] - c1[0])
            cb = dx_c * (b[1] - c1[1]) - dy_c * (b[0] - c1[0])
            in_a = ca <= 1e-9
            in_b = cb <= 1e-9
            if in_a and in_b:
                out.append(b)
            elif in_a and not in_b:
                t = ca / (ca - cb)
                out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            elif not in_a and in_b:
                t = ca / (ca - cb)
                out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
                out.append(b)
    return out


# 1. Outer 7-sided Podman shield (Colors.Purple3) and inner sky (WHITE)
raw_outer = [
    (32.2, 89.2),
    (67.8, 89.2),
    (89.5, 61.2),
    (82.0, 26.5),
    (50.0, 10.8),
    (18.0, 26.5),
    (10.5, 61.2),
]
raw_inner = _inset_poly(raw_outer, 4.5)

outer_shield = _round_corners(raw_outer, 3.6, 10)
inner_shield = _round_corners(raw_inner, 1.8, 8)

polygon(outer_shield, style=no_border_fill(Colors.Purple3))
polygon(inner_shield, style=no_border_fill(WHITE))

# 2. Pastel sky-blue water fill (#D6F0FF) in the lower half of inner shield
water_poly = _clip_y_between(inner_shield, 10.0, 50.8)
polygon(water_poly, style=no_border_fill(WATER_SKY))


def _wave_bar(x0: float, x1: float, yc: float, h: float = 2.0) -> None:
    """Draw a crisp flat horizontal wave bar in Colors.Blue3 clipped to inner shield."""
    raw = [(x0, yc - h / 2.0), (x1, yc - h / 2.0), (x1, yc + h / 2.0), (x0, yc + h / 2.0)]
    clipped = _clip_to_cw_convex(raw, inner_shield)
    if len(clipped) >= 3:
        polygon(clipped, style=no_border_fill(Colors.Blue3))


# 3. Background wave bars (Colors.Blue3) behind seals
_wave_bar(14.0, 29.0, 50.0, 2.0)
_wave_bar(68.5, 76.5, 50.0, 2.0)
_wave_bar(19.0, 26.5, 45.2, 2.0)
_wave_bar(70.0, 80.5, 45.2, 2.0)
_wave_bar(44.0, 53.0, 40.2, 2.0)
_wave_bar(73.5, 84.5, 40.2, 2.0)


def _draw_seal_eye(xc: float, yc: float, r_ring: float, r_pupil: float, r_light: float) -> None:
    """Draw a Podman seal eye: Colors.Purple3 ring + DARK pupil + WHITE catchlight."""
    circle((xc, yc), radius=r_ring, style=no_border_fill(Colors.Purple3))
    circle((xc, yc), radius=r_pupil, style=no_border_fill(DARK))
    circle((xc - r_pupil * 0.3, yc + r_pupil * 0.3), radius=r_light, style=no_border_fill(WHITE))


def _draw_eyebrow(xc: float, yc: float, half_w: float, arch_h: float, stroke_w: float) -> None:
    """Draw a cute arched eyebrow."""
    pts = [
        (xc - half_w, yc),
        *_cubic(
            (xc - half_w, yc),
            (xc - half_w * 0.4, yc + arch_h),
            (xc + half_w * 0.4, yc + arch_h),
            (xc + half_w, yc),
            10,
        ),
    ]
    draw_round_polyline(pts, width_units=stroke_w, color=DARK)


def _draw_nose_and_smile(
    xc: float, yc_nose: float, nw: float, nh: float, sw: float, sh: float, stroke_w: float
) -> None:
    """Draw a rounded triangular seal nose and W-shaped smile."""
    hw = nw / 2.0
    hh = nh / 2.0
    nose_pts = [
        (xc, yc_nose + hh),
        *_cubic(
            (xc, yc_nose + hh),
            (xc + hw, yc_nose + hh),
            (xc + hw * 1.1, yc_nose + hh * 0.1),
            (xc + hw * 0.7, yc_nose - hh * 0.5),
            8,
        ),
        (xc, yc_nose - hh),
        (xc - hw * 0.7, yc_nose - hh * 0.5),
        *_cubic(
            (xc - hw * 0.7, yc_nose - hh * 0.5),
            (xc - hw * 1.1, yc_nose + hh * 0.1),
            (xc - hw, yc_nose + hh),
            (xc, yc_nose + hh),
            8,
        ),
    ]
    polygon(nose_pts, style=no_border_fill(DARK))
    # W-smile below nose
    y_top = yc_nose - hh + 0.2
    y_bot = y_top - sh
    smile_l = [
        (xc - sw, y_top + sh * 0.35),
        *_cubic((xc - sw, y_top + sh * 0.35), (xc - sw * 0.9, y_bot), (xc - sw * 0.2, y_bot), (xc, y_top), 10),
    ]
    smile_r = [
        (xc, y_top),
        *_cubic((xc, y_top), (xc + sw * 0.2, y_bot), (xc + sw * 0.9, y_bot), (xc + sw, y_top + sh * 0.35), 10),
    ]
    draw_round_polyline(smile_l, width_units=stroke_w, color=DARK)
    draw_round_polyline(smile_r, width_units=stroke_w, color=DARK)


# 4. Back (big) seal pup (Colors.Gray3)
big_seal_arch = [
    (25.8, 41.2),
    *_cubic((25.8, 41.2), (27.8, 56.0), (28.5, 67.5), (32.5, 73.5), 14),
    *_cubic((32.5, 73.5), (36.8, 79.8), (42.5, 81.2), (49.0, 81.2), 12),
    *_cubic((49.0, 81.2), (55.5, 81.2), (61.2, 79.8), (65.5, 73.5), 12),
    *_cubic((65.5, 73.5), (69.5, 67.5), (70.2, 56.0), (72.2, 41.2), 14),
]
polygon(big_seal_arch, style=no_border_fill(Colors.Gray3))
draw_round_polyline(big_seal_arch, width_units=w, color=DARK)

_draw_eyebrow(36.8, 72.2, 3.0, 2.2, 1.8)
_draw_eyebrow(60.5, 72.2, 3.0, 2.2, 1.8)
_draw_seal_eye(37.5, 64.0, 4.5, 3.0, 1.0)
_draw_seal_eye(60.5, 64.0, 4.5, 3.0, 1.0)

# Cheek dots & muzzle on big seal
circle((37.5, 56.4), radius=2.5, style=no_border_fill(WHITE))
circle((60.5, 56.4), radius=2.5, style=no_border_fill(WHITE))
circle((49.0, 58.0), radius=6.8, style=no_border_fill(WHITE))
_draw_nose_and_smile(49.0, 59.6, 7.2, 4.8, 4.4, 2.5, 1.8)

# 5. Front-left (small) seal pup (Colors.Gray3) emerging from y=34.5
y_fl = 34.5
fl_arch = [
    (21.4, y_fl),
    *_cubic((21.4, y_fl), (22.4, 45.2), (27.2, 49.8), (34.0, 49.8), 14),
    *_cubic((34.0, 49.8), (40.8, 49.8), (45.6, 45.2), (46.6, y_fl), 14),
]
polygon(fl_arch, style=no_border_fill(Colors.Gray3))
draw_round_polyline(fl_arch, width_units=w, color=DARK)

_draw_eyebrow(27.2, 43.8, 2.3, 1.7, 1.6)
_draw_eyebrow(40.8, 43.8, 2.3, 1.7, 1.6)
_draw_seal_eye(27.4, 38.6, 3.1, 2.0, 0.7)
_draw_seal_eye(40.6, 38.6, 3.1, 2.0, 0.7)

# Half-visible muzzle and nose on front-left seal (clipped above y_fl)
fl_muzzle = [
    (34.0 + 4.3 * math.cos(math.radians(a)), 34.6 + 4.3 * math.sin(math.radians(a)))
    for a in range(0, 181, 10)
]
polygon(fl_muzzle, style=no_border_fill(WHITE))
fl_nose = [
    (34.0 + 2.4 * math.cos(math.radians(a)), 34.6 + 2.4 * math.sin(math.radians(a)))
    for a in range(0, 181, 12)
]
polygon(fl_nose, style=no_border_fill(DARK))

# Wave bar right under front-left seal
_wave_bar(17.5, 51.0, 33.6, 2.0)

# 6. Front-right (medium) seal pup (Colors.Gray3) emerging from y=28.4
y_fr = 28.4
fr_arch = [
    (47.6, y_fr),
    *_cubic((47.6, y_fr), (48.9, 41.8), (53.6, 47.8), (60.6, 47.8), 14),
    *_cubic((60.6, 47.8), (67.6, 47.8), (72.3, 41.8), (73.6, y_fr), 14),
]
polygon(fr_arch, style=no_border_fill(Colors.Gray3))
draw_round_polyline(fr_arch, width_units=w, color=DARK)

_draw_eyebrow(53.8, 41.5, 2.4, 1.8, 1.6)
_draw_eyebrow(67.4, 41.5, 2.4, 1.8, 1.6)
_draw_seal_eye(53.8, 36.2, 3.1, 2.05, 0.75)
_draw_seal_eye(67.4, 36.2, 3.1, 2.05, 0.75)

# Cheek dots, muzzle & nose on front-right seal
circle((53.8, 30.8), radius=1.65, style=no_border_fill(WHITE))
circle((67.4, 30.8), radius=1.65, style=no_border_fill(WHITE))

fr_muzzle_raw = [
    (60.6 + 4.5 * math.cos(2.0 * math.pi * i / 36), 31.8 + 4.5 * math.sin(2.0 * math.pi * i / 36))
    for i in range(36)
]
fr_muzzle = _clip_y_between(fr_muzzle_raw, y_fr, 90.0)
polygon(fr_muzzle, style=no_border_fill(WHITE))
_draw_nose_and_smile(60.6, 33.1, 4.6, 3.3, 2.9, 1.65, 1.5)

# 7. Foreground wave bars (Colors.Blue3)
_wave_bar(34.5, 81.8, 27.5, 2.0)
_wave_bar(30.5, 53.0, 22.2, 2.0)
_wave_bar(43.5, 61.5, 17.5, 2.0)

# 8. Crisp DARK outer and inner shield outlines (w=1.9) on top of everything
draw_round_polyline(outer_shield, width_units=w, color=DARK, closed=True)
draw_round_polyline(inner_shield, width_units=w, color=DARK, closed=True)

save()
