# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: oracle_db."""

from drawlib.canvas import save
from drawlib.shapes import rectangle
from drawlib.styles import Colors
from drawlib.utils import (
    DARK,
    WHITE,
    draw_cylinder_tier,
    fill_style,
    setup_icon,
)

setup_icon()

w = 2.0
cx = 50.0
cyl_w = 68.0
ry = 10.5

# 1. Bottom tier of 2-tier enterprise database cylinder
draw_cylinder_tier(
    cx=cx,
    y_bottom=22.0,
    width=cyl_w,
    body_h=25.0,
    ry=ry,
    body_color=Colors.Red3,
    border_color=DARK,
    border_units=w,
    draw_top_cap=False,
)

# 2. Top tier of 2-tier enterprise database cylinder
draw_cylinder_tier(
    cx=cx,
    y_bottom=47.0,
    width=cyl_w,
    body_h=25.0,
    ry=ry,
    body_color=Colors.Red3,
    top_color=Colors.Red2,
    border_color=DARK,
    border_units=w,
    draw_top_cap=True,
)

# 3. Iconic stadium / capsule "O" ring badge centered across cylinder front
badge_cy = 43.0
rectangle(
    (cx, badge_cy),
    width=48.0,
    height=25.0,
    style=fill_style(WHITE, border_color=DARK, border_units=1.8, shape_r=12.5),
)
rectangle(
    (cx, badge_cy),
    width=30.0,
    height=10.0,
    style=fill_style(Colors.Red3, border_color=DARK, border_units=1.6, shape_r=5.0),
)

save()
