# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: memcached."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Icon


def _bezier(
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

# 1. Outer rounded square badge (Colors.Gray5)
rectangle(
    (50.0, 50.0),
    width=78.0,
    height=78.0,
    style=Icon.fill_style(Colors.Gray5, border_color=Icon.DARK, border_units=w, shape_r=17.0),
)

# 2. Stylized Memcached 'M' with curved legs (Colors.Teal3)
p_tl = (27.2, 74.5)
p_bl = (25.2, 26.5)
p_bl_in = (37.2, 26.5)
p_arch_l = (35.2, 61.2)
p_mid_bl = (46.2, 37.8)
p_mid_br = (53.8, 37.8)
p_arch_r = (64.8, 61.2)
p_br_in = (62.8, 26.5)
p_br = (74.8, 26.5)
p_tr = (72.8, 74.5)
p_tr_in = (61.2, 74.5)
p_top_v = (50.0, 58.2)
p_tl_in = (38.8, 74.5)

m_pts = [
    p_tl,
    *_bezier(p_tl, (24.0, 57.0), (24.2, 39.0), p_bl, 16),
    p_bl_in,
    *_bezier(p_bl_in, (35.5, 38.0), (33.8, 53.0), p_arch_l, 14),
    *_bezier(p_arch_l, (36.8, 61.2), (43.5, 45.0), p_mid_bl, 14),
    *_bezier(p_mid_bl, (48.5, 38.2), (51.5, 38.2), p_mid_br, 6),
    *_bezier(p_mid_br, (56.5, 45.0), (63.2, 61.2), p_arch_r, 14),
    *_bezier(p_arch_r, (66.2, 53.0), (64.5, 38.0), p_br_in, 14),
    p_br,
    *_bezier(p_br, (75.8, 39.0), (76.0, 57.0), p_tr, 16),
    p_tr_in,
    *_bezier(p_tr_in, (58.0, 74.5), (52.5, 61.5), p_top_v, 12),
    *_bezier(p_top_v, (47.5, 61.5), (42.0, 74.5), p_tl_in, 12),
]

polygon(m_pts, style=Icon.no_border_fill(Colors.Teal3))
Icon.draw_round_polyline(m_pts, width_units=1.8, color=Icon.DARK, closed=True)

# 3. Two circular cache nodes below the center arch (Colors.Orange3)
circle((44.2, 29.5), radius=4.0, style=Icon.fill_style(Colors.Orange3, border_color=Icon.DARK, border_units=1.5))
circle((55.8, 29.5), radius=4.0, style=Icon.fill_style(Colors.Orange3, border_color=Icon.DARK, border_units=1.5))

save()
