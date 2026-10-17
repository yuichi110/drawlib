# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Client concept icon: webcam."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_BLUE_LIGHT,
    PASTEL_GREEN,
    WHITE,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# 1. Monitor-clip base foot (PASTEL_BLUE)
rectangle(
    (50.0, 17.5),
    width=48.0,
    height=9.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=4.0),
)

# 2. Monitor-clip hinge neck (PASTEL_BLUE_LIGHT)
rectangle(
    (50.0, 26.0),
    width=24.0,
    height=12.0,
    style=fill_style(PASTEL_BLUE_LIGHT, border_color=DARK, border_units=2.2, shape_r=3.0),
)

# 3. Circular webcam body (WHITE)
circle(
    (50.0, 56.5),
    radius=30.5,
    style=fill_style(WHITE, border_color=DARK, border_units=w),
)

# 4. Outer lens ring (PASTEL_BLUE)
circle(
    (50.0, 55.5),
    radius=17.5,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w),
)

# 5. Inner optical lens glass (DARK) + specular glint (WHITE)
circle(
    (50.0, 55.5),
    radius=9.5,
    style=fill_style(DARK),
)
circle(
    (46.5, 59.0),
    radius=2.8,
    style=fill_style(WHITE),
)

# 6. Top status LED indicator (PASTEL_GREEN)
circle(
    (50.0, 80.0),
    radius=3.4,
    style=fill_style(PASTEL_GREEN, border_color=DARK, border_units=2.0),
)

save()
