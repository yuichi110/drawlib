# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud Native concept icon: cilium."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()

r_hex = 13.5
dist = 27.0


def build_flat_hex(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    """Build flat-top hexagon vertices centered at (cx, cy) with circumradius r."""
    return [(cx + r * math.cos(math.radians(60.0 * k)), cy + r * math.sin(math.radians(60.0 * k))) for k in range(6)]


# Center hexagon in pastel green
polygon(
    build_flat_hex(50.0, 50.0, r_hex),
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=2.0, shape_r=1.2),
)

# Six outer honeycomb hexagons with 3-fold rotational symmetry
outer_specs = [
    (90.0, Icon.PASTEL_BLUE),
    (30.0, Icon.WHITE),
    (330.0, Icon.PASTEL_BLUE),
    (270.0, Icon.WHITE),
    (210.0, Icon.PASTEL_BLUE),
    (150.0, Icon.WHITE),
]

for angle_deg, color in outer_specs:
    rad = math.radians(angle_deg)
    hx = 50.0 + dist * math.cos(rad)
    hy = 50.0 + dist * math.sin(rad)
    polygon(
        build_flat_hex(hx, hy, r_hex),
        style=Icon.fill_style(color, border_color=Icon.DARK, border_units=2.0, shape_r=1.2),
    )

save()
