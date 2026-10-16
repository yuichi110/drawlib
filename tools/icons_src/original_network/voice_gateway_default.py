# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: voice_gateway."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import (
    DARK,
    ORIG_STROKE,
    PASTEL_BLUE,
    PASTEL_GREEN,
    WHITE,
    draw_cisco_arrow,
    draw_round_polyline,
    fill_style,
    setup_icon,
)

setup_icon()

w = ORIG_STROKE

# Rounded square gateway card
rectangle(
    (50.0, 50.0),
    width=76.0,
    height=76.0,
    style=fill_style(PASTEL_BLUE, border_color=DARK, border_units=w, shape_r=12.0),
)

# 4 cardinal routing arrows on the frame (2 horizontal inward, 2 vertical outward)
draw_cisco_arrow((14.0, 50.0), (24.0, 50.0), shaft_w=2.6, head_len=5.0, head_w=6.8, color=DARK)
draw_cisco_arrow((86.0, 50.0), (76.0, 50.0), shaft_w=2.6, head_len=5.0, head_w=6.8, color=DARK)
draw_cisco_arrow((50.0, 76.0), (50.0, 86.0), shaft_w=2.6, head_len=5.0, head_w=6.8, color=DARK)
draw_cisco_arrow((50.0, 24.0), (50.0, 14.0), shaft_w=2.6, head_len=5.0, head_w=6.8, color=DARK)

# Inner white circle
circle(
    (50.0, 50.0),
    radius=24.0,
    style=fill_style(WHITE, border_color=DARK, border_units=2.2),
)


# 2D telephone handset tilted at 45 degrees inside the white circle
def _build_handset_pts() -> list[tuple[float, float]]:
    # Local handset coords: u along handset axis, v perpendicular (v > 0 outer back, v < 0 cups)
    local_pts: list[tuple[float, float]] = []

    def _arc_pts(
        cx_l: float,
        cy_l: float,
        r_l: float,
        deg_start: float,
        deg_end: float,
        steps: int = 8,
    ) -> list[tuple[float, float]]:
        return [
            (
                cx_l + r_l * math.cos(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
                cy_l + r_l * math.sin(math.radians(deg_start + (deg_end - deg_start) * (i / steps))),
            )
            for i in range(steps + 1)
        ]

    # Outer arch: center (0, -9.8), radius 16.0, from u=-13.8 to u=+13.8
    # At u=+-13.8, y = -9.8 + sqrt(16^2 - 13.8^2) = -9.8 + 8.097 = -1.703
    ang_left = math.degrees(math.atan2(8.097, -13.8))
    ang_right = math.degrees(math.atan2(8.097, 13.8))
    local_pts.extend(_arc_pts(0.0, -9.8, 16.0, ang_left, ang_right, steps=24))

    # Right cup rounded bottom-right corner at (12.0, -4.0), r=1.8 -> bottom y=-5.8, right x=13.8
    local_pts.extend(_arc_pts(12.0, -4.0, 1.8, 0.0, -90.0, steps=6))
    # Right cup rounded bottom-left corner at (8.4, -4.0), r=1.8 -> bottom y=-5.8, left x=6.6
    local_pts.extend(_arc_pts(8.4, -4.0, 1.8, -90.0, -180.0, steps=6))

    # Inner arch: center (0, -9.8), radius 12.0, from u=+6.6 back to u=-6.6
    # At u=+-6.6, y = -9.8 + sqrt(12^2 - 6.6^2) = -9.8 + 10.022 = +0.222
    ang_in_right = math.degrees(math.atan2(10.022, 6.6))
    ang_in_left = math.degrees(math.atan2(10.022, -6.6))
    local_pts.extend(_arc_pts(0.0, -9.8, 12.0, ang_in_right, ang_in_left, steps=18))

    # Left cup rounded bottom-right corner at (-8.4, -4.0), r=1.8 -> left x=-6.6, bottom y=-5.8
    local_pts.extend(_arc_pts(-8.4, -4.0, 1.8, 0.0, -90.0, steps=6))
    # Left cup rounded bottom-left corner at (-12.0, -4.0), r=1.8 -> bottom y=-5.8, left x=-13.8
    local_pts.extend(_arc_pts(-12.0, -4.0, 1.8, -90.0, -180.0, steps=6))

    # Rotate by +135 degrees so outer back faces bottom-left and cups face top-right
    theta = math.radians(135.0)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    cx, cy = 50.0, 50.0
    return [(cx + u * cos_t - v * sin_t, cy + u * sin_t + v * cos_t) for u, v in local_pts]


handset_pts = _build_handset_pts()
polygon(handset_pts, style=fill_style(PASTEL_GREEN))
draw_round_polyline(handset_pts, width_units=2.2, color=DARK, closed=True)

save()
