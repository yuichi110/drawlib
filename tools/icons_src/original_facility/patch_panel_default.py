# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility concept icon: patch_panel."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6


def _bezier_pts(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 32,
) -> list[tuple[float, float]]:
    pts: list[tuple[float, float]] = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = (mt**3) * p0[0] + 3 * (mt**2) * t * p1[0] + 3 * mt * (t**2) * p2[0] + (t**3) * p3[0]
        y = (mt**3) * p0[1] + 3 * (mt**2) * t * p1[1] + 3 * mt * (t**2) * p2[1] + (t**3) * p3[1]
        pts.append((x, y))
    return pts


# 1. Rack-mounted patch panel chassis (PASTEL_BLUE)
panel_cy = 65.0
rectangle(
    (50.0, panel_cy),
    width=76.0,
    height=30.0,
    style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w_outer, shape_r=4.5),
)

# Rack mounting ears on left & right (PASTEL_BLUE_LIGHT)
for ear_x in (15.5, 84.5):
    rectangle(
        (ear_x, panel_cy),
        width=5.0,
        height=22.0,
        style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w_inner, shape_r=1.8),
    )
    for sy in (panel_cy + 6.5, panel_cy - 6.5):
        circle((ear_x, sy), radius=1.0, style=Icon.fill_style(Icon.DARK))

# 2. Inner port bank faceplate (WHITE)
rectangle(
    (50.0, panel_cy),
    width=57.0,
    height=20.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_inner, shape_r=2.5),
)

# 3. PASTEL_GREEN patch cord arc connecting port 1 (27.5) and port 4 (61.25)
# Drawn before the port jacks so the cable enters cleanly into the bottom of each jack
cord_pts = _bezier_pts((27.5, 60.0), (27.5, 16.0), (61.25, 16.0), (61.25, 60.0))
Icon.draw_round_polyline(cord_pts, width_units=6.8, color=Icon.DARK)
Icon.draw_round_polyline(cord_pts, width_units=3.4, color=Icon.PASTEL_GREEN)

# 4. Row of 5 modular RJ45/fiber ports
port_xs = [27.5, 38.75, 50.0, 61.25, 72.5]
for idx, px in enumerate(port_xs):
    is_plugged = idx in (0, 3)
    col = Icon.PASTEL_GREEN if is_plugged else Icon.PASTEL_BLUE_LIGHT
    rectangle(
        (px, panel_cy - 1.5),
        width=7.6,
        height=8.2,
        style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w_inner, shape_r=1.4),
    )
    # Small port number/label bar above each socket
    Icon.draw_round_segment((px - 2.2, panel_cy + 6.2), (px + 2.2, panel_cy + 6.2), width_units=1.5, color=Icon.DARK)

save()
