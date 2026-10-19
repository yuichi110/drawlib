# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cisco network topology icon: WAN cloud (default classic 3D variant)."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Cisco, Icon

Icon.setup()

# 7 clockwise perimeter puffs (cx, cy, r) forming the classic Cisco WAN cloud
puffs: list[tuple[float, float, float]] = [
    (21.5, 48.0, 12.5),  # 0: Left lobe
    (33.5, 61.0, 14.5),  # 1: Upper-left lobe
    (54.5, 63.0, 16.0),  # 2: Upper-center crown
    (75.0, 56.5, 13.0),  # 3: Upper-right lobe
    (78.5, 42.5, 12.5),  # 4: Lower-right lobe
    (63.5, 33.5, 13.5),  # 5: Bottom-right lobe
    (39.5, 34.0, 14.0),  # 6: Bottom-left lobe
]

n_puffs = len(puffs)
intersections: list[tuple[float, float]] = []
for i in range(n_puffs):
    cx1, cy1, r1 = puffs[i]
    cx2, cy2, r2 = puffs[(i + 1) % n_puffs]
    dx = cx2 - cx1
    dy = cy2 - cy1
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    a = (r1 * r1 - r2 * r2 + d * d) / (2.0 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    intersections.append((cx1 + a * ux - h * uy, cy1 + a * uy + h * ux))


def _sample_puff_arc(idx: int, *, steps: int = 20) -> list[tuple[float, float]]:
    cx, cy, r = puffs[idx]
    p_start = intersections[(idx - 1) % n_puffs]
    p_end = intersections[idx]
    a_start = math.atan2(p_start[1] - cy, p_start[0] - cx)
    a_end = math.atan2(p_end[1] - cy, p_end[0] - cx)
    while a_end > a_start:
        a_end -= 2.0 * math.pi
    return [
        (
            cx + r * math.cos(a_start + (a_end - a_start) * (s / steps)),
            cy + r * math.sin(a_start + (a_end - a_start) * (s / steps)),
        )
        for s in range(steps)
    ]


outer_pts: list[tuple[float, float]] = []
for i in range(n_puffs):
    outer_pts.extend(_sample_puff_arc(i))

# 1. Base cloud fill in CISCO_BLUE
polygon(outer_pts, style=Icon.no_border_fill(Cisco.BLUE))

# 2. Top highlight band in CISCO_LIGHT_BLUE hugging puffs 1, 2, 3
top_outer = [*_sample_puff_arc(1), *_sample_puff_arc(2), *_sample_puff_arc(3), intersections[3]]
top_inner = [(x - 1.2, y - 5.8) for x, y in reversed(top_outer[3:-3])]
polygon([*top_outer, *top_inner], style=Icon.no_border_fill(Cisco.LIGHT_BLUE))

# 3. Lower-right shadow band in CISCO_DARK_BLUE hugging puffs 4, 5
bot_outer = [*_sample_puff_arc(4), *_sample_puff_arc(5)[:-3]]
bot_inner = [(x - 4.6, y + 4.2) for x, y in reversed(bot_outer[2:-4])]
polygon([*bot_outer, *bot_inner], style=Icon.no_border_fill(Cisco.DARK_BLUE))

# 4. Crisp WHITE inner puff highlight/crease arcs with rounded end caps
for puff_idx, deg_start, deg_end, r_inset in [
    (1, 78.0, 158.0, 3.2),
    (2, 42.0, 128.0, 3.4),
    (0, 125.0, 215.0, 3.0),
]:
    cx, cy, r = puffs[puff_idx]
    arc_r = r - r_inset
    arc_pts = [
        (
            cx + arc_r * math.cos(math.radians(deg_start + (deg_end - deg_start) * (k / 14))),
            cy + arc_r * math.sin(math.radians(deg_start + (deg_end - deg_start) * (k / 14))),
        )
        for k in range(15)
    ]
    Icon.draw_round_polyline(arc_pts, width_units=1.6, color=Icon.WHITE)

# 5. Outer silhouette contour in CISCO_BORDER
Icon.draw_round_polyline(outer_pts, width_units=2.0, color=Cisco.BORDER, closed=True)

save()
