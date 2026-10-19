# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: waf."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.styles import Colors
from drawlib.utils import Gcp, Icon

Icon.setup()

w_shape = 2.0
w_line = 2.0

# 1. Web browser window base fill (x=12..78, y=24..84)
rectangle(
    (45.0, 54.0),
    width=66.0,
    height=60.0,
    style=Icon.no_border_fill(Icon.WHITE, shape_r=6.5),
)

# 2. Top header bar fill (y=70..84)
Gcp.draw_rounded_corner_block(
    12.0,
    70.0,
    78.0,
    84.0,
    r=6.5,
    round_tl=True,
    round_tr=True,
    color=Icon.PASTEL_BLUE,
)

# 3. Header divider and outer browser frame border
Icon.draw_round_segment((12.0, 70.0), (78.0, 70.0), width_units=w_shape, color=Icon.DARK)
rectangle(
    (45.0, 54.0),
    width=66.0,
    height=60.0,
    style=Icon.fill_style(Colors.Transparent, border_color=Icon.DARK, border_units=w_shape, shape_r=6.5),
)

# 4. Two small WHITE window dots on left of header bar
for x_dot in (21.0, 29.5):
    circle(
        (x_dot, 77.0),
        radius=2.4,
        style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
    )

# 5. DARK `</>` code brackets in upper-left of browser body
Icon.draw_round_polyline(
    [(24.5, 57.5), (19.5, 52.5), (24.5, 47.5)],
    width_units=w_line,
    color=Icon.DARK,
)
Icon.draw_round_segment((29.5, 46.5), (33.5, 58.5), width_units=w_line, color=Icon.DARK)
Icon.draw_round_polyline(
    [(38.5, 57.5), (43.5, 52.5), (38.5, 47.5)],
    width_units=w_line,
    color=Icon.DARK,
)

# 6. Bottom-right overlapping PASTEL_GREEN shield (cx=68, y_bot=12, y_top=56, half_w=19)
cx = 68.0
y_bot, y_top = 12.0, 56.0
half_w = 19.0

left_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="left")
right_pts = Icon.build_shield_half_points(cx, y_bot, y_top, half_w, side="right")
full_outline = left_pts + list(reversed(right_pts[1:-1]))

polygon(full_outline, style=Icon.no_border_fill(Icon.PASTEL_GREEN))
Icon.draw_round_polyline(full_outline, width_units=w_shape, color=Icon.DARK, closed=True)

# 7. Inner WHITE circle and DARK checkmark inside shield
circle(
    (cx, 36.0),
    radius=8.5,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w_shape),
)
Icon.draw_round_polyline(
    [(64.2, 35.8), (67.2, 32.8), (72.0, 38.8)],
    width_units=w_line,
    color=Icon.DARK,
)

save()
