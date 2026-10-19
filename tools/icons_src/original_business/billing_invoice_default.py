# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Business concept icon: billing_invoice."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Gcp, Icon

Icon.setup()

w_outer = 2.0
w_inner = 1.6

# 1. Invoice receipt sheet (WHITE with zigzag bottom, x=15.0..71.0, y=16.0..85.0)
x0, x1 = 15.0, 71.0
y_bot_tip = 16.0
y_bot_val = 21.5
y_top = 85.0
r_top = 5.5

receipt_pts: list[tuple[float, float]] = []
n_zig = 8
for i in range(n_zig + 1):
    zx = x0 + (x1 - x0) * (i / n_zig)
    zy = y_bot_tip if i % 2 == 0 else y_bot_val
    receipt_pts.append((zx, zy))

steps = 12
for i in range(steps + 1):
    ang = math.radians(0.0 + 90.0 * (i / steps))
    receipt_pts.append((x1 - r_top + r_top * math.cos(ang), y_top - r_top + r_top * math.sin(ang)))
for i in range(steps + 1):
    ang = math.radians(90.0 + 90.0 * (i / steps))
    receipt_pts.append((x0 + r_top + r_top * math.cos(ang), y_top - r_top + r_top * math.sin(ang)))

polygon(receipt_pts, style=Icon.no_border_fill(Icon.WHITE))

# 2. Top PASTEL_BLUE header bar (y=71.0..85.0)
Gcp.draw_rounded_corner_block(
    x0,
    71.0,
    x1,
    y_top,
    r=r_top,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 3. Header divider and outer receipt border
Icon.draw_round_segment((x0, 71.0), (x1, 71.0), width_units=w_outer, color=Icon.DARK)
Icon.draw_round_polyline(receipt_pts, width_units=w_outer, color=Icon.DARK, closed=True)

# 4. Horizontal line items inside receipt (clear of bottom-right coin badge)
for y_item in (60.0, 50.0):
    Icon.draw_round_segment((23.0, y_item), (46.0, y_item), width_units=w_inner, color=Icon.DARK)
    Icon.draw_round_segment((53.0, y_item), (62.0, y_item), width_units=w_inner, color=Icon.DARK)

Icon.draw_round_segment((23.0, 40.0), (46.0, 40.0), width_units=w_inner, color=Icon.DARK)
Icon.draw_round_segment((23.0, 30.5), (46.0, 30.5), width_units=w_outer, color=Icon.DARK)

# 5. PASTEL_GREEN circular coin/currency badge at bottom-right
coin_cx, coin_cy = 71.5, 29.0
circle(
    (coin_cx, coin_cy),
    radius=14.5,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w_outer),
)

# 6. Currency ($) glyph inside coin badge
Icon.draw_round_segment((coin_cx, 20.5), (coin_cx, 37.5), width_units=w_inner, color=Icon.DARK)

s_pts: list[tuple[float, float]] = []
for i in range(15):
    ang = math.radians(25.0 + (245.0 * i / 14))
    s_pts.append((coin_cx + 4.2 * math.cos(ang), 32.0 + 2.8 * math.sin(ang)))
for i in range(15):
    ang = math.radians(90.0 - (245.0 * i / 14))
    s_pts.append((coin_cx + 4.2 * math.cos(ang), 26.0 + 2.8 * math.sin(ang)))

Icon.draw_round_polyline(s_pts, width_units=w_inner, color=Icon.DARK)

save()
