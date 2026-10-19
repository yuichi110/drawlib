# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: redpanda."""

from drawlib.canvas import save
from drawlib.shapes import circle, ellipse, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon


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
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


Icon.setup()

w = 2.0

# 1. Pointed red panda ears with fluffy inner pads
left_ear = [
    (20.0, 56.0),
    *_cubic((20.0, 56.0), (13.0, 68.0), (14.0, 82.0), (22.5, 86.0), 12),
    *_cubic((22.5, 86.0), (30.5, 84.5), (38.0, 76.0), (41.0, 66.0), 12),
]
right_ear = [(100.0 - x, y) for x, y in left_ear]

for ear in (left_ear, right_ear):
    polygon(ear, style=Icon.no_border_fill(Colors.Orange3))
    Icon.draw_round_polyline(ear, width_units=w, color=Icon.DARK, closed=True)

left_inner_ear = [
    (23.5, 60.0),
    *_cubic((23.5, 60.0), (19.5, 68.0), (20.5, 76.5), (24.5, 79.0), 10),
    *_cubic((24.5, 79.0), (29.0, 77.5), (33.5, 71.5), (35.5, 64.5), 10),
]
right_inner_ear = [(100.0 - x, y) for x, y in left_inner_ear]

for ie in (left_inner_ear, right_inner_ear):
    polygon(ie, style=Icon.no_border_fill(Icon.WHITE))
    Icon.draw_round_polyline(ie, width_units=1.5, color=Icon.DARK, closed=True)

# 2. Wide cheek-fluffed red panda head dome (Colors.Red3)
head_pts = [
    (50.0, 74.0),
    *_cubic((50.0, 74.0), (68.0, 74.0), (80.0, 62.0), (84.5, 46.0), 16),
    *_cubic((84.5, 46.0), (88.0, 33.5), (81.5, 21.0), (67.5, 16.5), 14),
    *_cubic((67.5, 16.5), (58.0, 13.5), (42.0, 13.5), (32.5, 16.5), 12),
    *_cubic((32.5, 16.5), (18.5, 21.0), (12.0, 33.5), (15.5, 46.0), 14),
    *_cubic((15.5, 46.0), (20.0, 62.0), (32.0, 74.0), (50.0, 74.0), 16),
]
polygon(head_pts, style=Icon.no_border_fill(Colors.Red3))
Icon.draw_round_polyline(head_pts, width_units=w, color=Icon.DARK, closed=True)

# 3. Signature white cheek fur patches + eyebrow tear-drop ovals
left_cheek = [
    (36.0, 44.5),
    *_cubic((36.0, 44.5), (26.5, 46.5), (19.0, 40.5), (20.0, 31.5), 12),
    *_cubic((20.0, 31.5), (21.0, 24.0), (29.5, 21.0), (38.0, 24.5), 12),
    *_cubic((38.0, 24.5), (41.5, 26.5), (41.0, 39.5), (36.0, 44.5), 10),
]
right_cheek = [(100.0 - x, y) for x, y in left_cheek]

for cheek in (left_cheek, right_cheek):
    polygon(cheek, style=Icon.no_border_fill(Icon.WHITE))
    Icon.draw_round_polyline(cheek, width_units=1.6, color=Icon.DARK, closed=True)

for bx, bang in ((38.5, -18.0), (61.5, 18.0)):
    ellipse(
        (bx, 56.5),
        width=10.5,
        height=6.2,
        style=Icon.fill_style(Colors.Orange2, border_color=Icon.DARK, border_units=1.5, angle=bang),
    )

# 4. Rounded muzzle oval (WHITE)
ellipse(
    (50.0, 29.0),
    width=25.0,
    height=17.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=1.7),
)

# 5. Friendly dark eyes with white catchlights
for ex, px in ((37.0, 37.8), (63.0, 62.2)):
    circle(
        (ex, 44.5),
        radius=5.0,
        style=Icon.fill_style(Icon.DARK),
    )
    circle((px - 1.2, 46.0), radius=1.5, style=Icon.fill_style(Icon.WHITE))

# 6. Cute dark oval nose + smiling mouth
ellipse((50.0, 32.8), width=8.5, height=5.5, style=Icon.fill_style(Icon.DARK))
Icon.draw_round_polyline(
    [(44.5, 26.5), (50.0, 29.2), (55.5, 26.5)],
    width_units=1.6,
    color=Icon.DARK,
)

save()
