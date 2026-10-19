# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Server concept icon: openbsd."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0
cx, cy = 48.0, 50.0
r_body = 29.0


def polar(r: float, deg: float) -> tuple[float, float]:
    """Convert polar offset around (cx, cy) to canvas coordinates."""
    rad = math.radians(deg)
    return (round(cx + r * math.cos(rad), 2), round(cy + r * math.sin(rad), 2))


def bezier3(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 16,
) -> list[tuple[float, float]]:
    """Sample a cubic Bezier curve."""
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        bx = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        by = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((round(bx, 2), round(by, 2)))
    return pts


# 1. Left small fin (drawn behind body)
left_fin = [
    *bezier3((19.8, 55.4), (14.5, 57.5), (11.5, 54.0), (11.5, 49.0), 12),
    *bezier3((11.5, 49.0), (11.5, 43.8), (14.5, 40.5), (20.2, 42.6), 12)[1:],
]
polygon(left_fin, style=Icon.no_border_fill(Colors.Amber3))
Icon.draw_round_polyline(left_fin, width_units=w, color=Icon.DARK, closed=True)

# 2. Right tail fin with 3 fin lines (drawn behind body)
right_tail = [
    *bezier3((75.8, 57.2), (83.2, 62.5), (88.4, 60.5), (88.6, 50.0), 14),
    *bezier3((88.6, 50.0), (88.4, 39.5), (83.2, 37.5), (75.8, 42.8), 14)[1:],
]
polygon(right_tail, style=Icon.no_border_fill(Colors.Amber3))
Icon.draw_round_polyline(right_tail, width_units=w, color=Icon.DARK, closed=True)
for y_in, y_out in ((53.0, 55.2), (50.0, 50.0), (47.0, 44.8)):
    Icon.draw_round_segment((77.2, y_in), (83.0, y_out), width_units=w, color=Icon.DARK)

# 3. 7 smaller background spikes around body perimeter (drawn behind body outline)
bg_spike_angles = [68.0, 108.0, 147.0, 210.0, 251.0, 290.0, 333.0]
for ang in bg_spike_angles:
    sp = [polar(r_body - 1.0, ang - 8.0), polar(r_body + 6.6, ang), polar(r_body - 1.0, ang + 8.0)]
    polygon(sp, style=Icon.no_border_fill(Colors.Amber3))
    Icon.draw_round_polyline(sp, width_units=w, color=Icon.DARK, closed=True)

# 4. Main Amber2 body circle fill + 7 foreground open-base spikes
circle((cx, cy), radius=r_body, style=Icon.no_border_fill(Colors.Amber3))

# Foreground spikes: (angle_deg, tip_radius, half_base_angle_deg)
fg_spikes = [
    (18.0, r_body + 8.2, 8.0),
    (45.0, r_body + 8.6, 8.6),
    (90.0, r_body + 8.6, 8.8),
    (126.0, r_body + 8.6, 8.6),
    (232.0, r_body + 8.6, 8.6),
    (270.0, r_body + 8.6, 8.8),
    (310.0, r_body + 8.6, 8.6),
]
for ang, r_tip, h_ang in fg_spikes:
    sp_fill = [polar(r_body - 1.8, ang - h_ang), polar(r_tip, ang), polar(r_body - 1.8, ang + h_ang)]
    polygon(sp_fill, style=Icon.no_border_fill(Colors.Amber3))

# Draw body circle DARK outline arcs between the 7 foreground spikes
n_fg = len(fg_spikes)
for i in range(n_fg):
    ang_start = fg_spikes[i][0] + fg_spikes[i][2]
    ang_end = fg_spikes[(i + 1) % n_fg][0] - fg_spikes[(i + 1) % n_fg][2]
    if ang_end <= ang_start:
        ang_end += 360.0
    steps = max(8, int((ang_end - ang_start) / 2.5))
    arc_pts = [polar(r_body, ang_start + (ang_end - ang_start) * (k / steps)) for k in range(steps + 1)]
    Icon.draw_round_polyline(arc_pts, width_units=w, color=Icon.DARK, closed=False)

# Draw foreground spike DARK V-outlines with short inward root ticks
for ang, r_tip, h_ang in fg_spikes:
    sp_stroke = [
        polar(r_body - 0.8, ang + h_ang),
        polar(r_tip, ang),
        polar(r_body - 0.8, ang - h_ang),
    ]
    Icon.draw_round_polyline(sp_stroke, width_units=w, color=Icon.DARK, closed=False)

# 5. Sleepy half-lidded circular eyes on the left
r_eye = 6.6
for ex, ey in ((25.2, 59.5), (43.5, 59.5)):
    circle((ex, ey), radius=r_eye, style=Icon.no_border_fill(Icon.WHITE))
    lid_pts = [
        (
            round(ex + r_eye * math.cos(math.radians(a)), 2),
            round(ey + r_eye * math.sin(math.radians(a)), 2),
        )
        for a in range(0, 181, 6)
    ]
    polygon(lid_pts, style=Icon.no_border_fill(Colors.Amber3))
    pupil_pts = [
        (
            round(ex + 0.8 + 2.6 * math.cos(math.radians(a)), 2),
            round(ey + 2.6 * math.sin(math.radians(a)), 2),
        )
        for a in range(180, 361, 10)
    ]
    polygon(pupil_pts, style=Icon.no_border_fill(Icon.DARK))
    Icon.draw_round_segment((ex - r_eye, ey), (ex + r_eye, ey), width_units=w, color=Icon.DARK)
    circle((ex, ey), radius=r_eye, style=Icon.stroke_style(Icon.DARK, width_units=w))

# 6. Plump yellow lips (Colors.Amber4 fill + DARK outline)
lip_mid = [
    *bezier3((26.5, 47.0), (28.5, 48.0), (31.5, 47.2), (33.5, 46.6), 8),
    *bezier3((33.5, 46.6), (35.5, 47.2), (38.5, 47.6), (41.2, 46.7), 8)[1:],
]
upper_lip_top = [
    *bezier3((41.2, 46.7), (39.5, 49.5), (37.0, 51.2), (35.2, 50.8), 8),
    *bezier3((35.2, 50.8), (34.2, 50.5), (33.8, 50.0), (33.3, 50.0), 6)[1:],
    *bezier3((33.3, 50.0), (32.8, 50.0), (32.2, 50.5), (31.0, 50.9), 6)[1:],
    *bezier3((31.0, 50.9), (28.8, 51.3), (26.2, 49.5), (26.5, 47.0), 8)[1:],
]
lower_lip_bot = bezier3((41.2, 46.7), (38.8, 41.8), (28.0, 41.8), (26.5, 47.0), 16)

upper_lip = [*lip_mid, *upper_lip_top[1:-1]]
lower_lip = [*lip_mid, *lower_lip_bot[1:-1]]
polygon(upper_lip, style=Icon.no_border_fill(Colors.Amber4))
polygon(lower_lip, style=Icon.no_border_fill(Colors.Amber4))
Icon.draw_round_polyline(upper_lip, width_units=w, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(lower_lip, width_units=w, color=Icon.DARK, closed=True)

# 7. Small side pectoral fin with 3 fin lines
pectoral_fin = [
    *bezier3((56.8, 54.4), (63.0, 58.6), (67.8, 57.5), (68.2, 49.5), 12),
    *bezier3((68.2, 49.5), (67.8, 41.5), (63.0, 40.4), (56.5, 45.2), 12)[1:],
]
Icon.draw_round_polyline(pectoral_fin, width_units=w, color=Icon.DARK, closed=False)
for x_in, y_in, x_out, y_out in (
    (61.4, 52.5, 67.6, 54.0),
    (61.8, 49.5, 68.1, 49.5),
    (61.4, 46.5, 67.6, 45.0),
):
    Icon.draw_round_segment((x_in, y_in), (x_out, y_out), width_units=w, color=Icon.DARK)

# 8. 9 small bold V-shaped spike marks well inside the body
inner_v_marks = [
    [(40.5, 69.5), (42.2, 74.2), (45.2, 70.0)],
    [(51.8, 69.8), (55.2, 73.8), (56.2, 68.8)],
    [(59.5, 64.5), (64.5, 66.2), (62.8, 61.5)],
    [(70.8, 57.4), (73.4, 56.6), (71.6, 54.4)],
    [(71.6, 50.8), (74.2, 49.5), (71.6, 48.2)],
    [(64.5, 38.8), (66.8, 34.4), (62.0, 35.8)],
    [(57.8, 32.5), (57.8, 27.6), (54.0, 30.2)],
    [(50.4, 30.0), (48.0, 25.4), (45.6, 30.0)],
    [(36.0, 34.2), (35.6, 29.4), (39.6, 31.8)],
]
for v_pts in inner_v_marks:
    Icon.draw_round_polyline(v_pts, width_units=w, color=Icon.DARK, closed=False)

save()
