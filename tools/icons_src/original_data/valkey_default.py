# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data concept icon: valkey."""

import math

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0


def _svg_pt(sx: float, sy: float) -> tuple[float, float]:
    """Map Valkey 256x295 SVG coordinates to centered 100x100 bottom-up canvas."""
    scale = 82.0 / 295.0
    x = 50.0 + (sx - 128.0) * scale
    y = 50.0 + (147.5 - sy) * scale
    return (x, y)


# 1. Inner hexagon facet around the keyhole (Colors.Blue3)
inner_hex_pts = [
    _svg_pt(83.1, 199.5),
    _svg_pt(58.8, 184.2),
    _svg_pt(58.8, 107.4),
    _svg_pt(128.8, 67.2),
    _svg_pt(197.2, 107.4),
    _svg_pt(197.2, 187.6),
    _svg_pt(143.0, 218.1),
    _svg_pt(143.0, 185.9),
]
kh_cx, kh_cy = _svg_pt(127.7, 144.7)
kh_r = 43.0 * (82.0 / 295.0)
for i in range(25):
    ang = math.radians(-69.5 + (249.5 - (-69.5)) * (i / 24))
    inner_hex_pts.append((kh_cx + kh_r * math.cos(ang), kh_cy + kh_r * math.sin(ang)))
inner_hex_pts.extend(
    [
        _svg_pt(112.5, 185.9),
        _svg_pt(112.5, 218.1),
        _svg_pt(83.1, 199.5),
    ]
)
polygon(inner_hex_pts, style=Icon.no_border_fill(Colors.Blue3))

# 3. Outer folded hexagonal ribbon frame (Colors.Purple3)
outer_frame_pts = [
    _svg_pt(53.1, 248.7),
    _svg_pt(0.0, 215.3),
    _svg_pt(0.0, 74.0),
    _svg_pt(130.0, 0.0),
    _svg_pt(256.0, 74.0),
    _svg_pt(256.0, 222.7),
    _svg_pt(127.7, 295.0),
    _svg_pt(83.1, 267.3),
    _svg_pt(83.1, 199.5),
    _svg_pt(112.5, 218.1),
    _svg_pt(112.5, 247.5),
    _svg_pt(127.7, 257.1),
    _svg_pt(222.7, 203.4),
    _svg_pt(222.7, 92.1),
    _svg_pt(128.8, 36.7),
    _svg_pt(32.2, 92.1),
    _svg_pt(32.2, 196.7),
    _svg_pt(52.6, 209.7),
]
polygon(outer_frame_pts, style=Icon.no_border_fill(Colors.Purple3))

# 4. Central keyhole core circle (Colors.Purple2)
circle(
    (kh_cx, kh_cy),
    radius=20.0 * (82.0 / 295.0),
    style=Icon.fill_style(Colors.Purple2, border_color=Icon.DARK, border_units=1.7),
)

# 5. Crisp structural outlines
# Collinear isometric seam between outer frame and inner hexagon
Icon.draw_round_segment(_svg_pt(83.1, 199.5), _svg_pt(112.5, 218.1), width_units=1.6, color=Icon.DARK)

# Full Valkey outer + keyhole contour
full_contour = [
    _svg_pt(53.1, 248.7),
    _svg_pt(0.0, 215.3),
    _svg_pt(0.0, 74.0),
    _svg_pt(130.0, 0.0),
    _svg_pt(256.0, 74.0),
    _svg_pt(256.0, 222.7),
    _svg_pt(127.7, 295.0),
    _svg_pt(83.1, 267.3),
    _svg_pt(83.1, 199.5),
    _svg_pt(58.8, 184.2),
    _svg_pt(58.8, 107.4),
    _svg_pt(128.8, 67.2),
    _svg_pt(197.2, 107.4),
    _svg_pt(197.2, 187.6),
    _svg_pt(143.0, 218.1),
    _svg_pt(143.0, 185.9),
]
for i in range(25):
    ang = math.radians(-69.5 + (249.5 - (-69.5)) * (i / 24))
    full_contour.append((kh_cx + kh_r * math.cos(ang), kh_cy + kh_r * math.sin(ang)))
full_contour.extend(
    [
        _svg_pt(112.5, 185.9),
        _svg_pt(112.5, 247.5),
        _svg_pt(127.7, 257.1),
        _svg_pt(222.7, 203.4),
        _svg_pt(222.7, 92.1),
        _svg_pt(128.8, 36.7),
        _svg_pt(32.2, 92.1),
        _svg_pt(32.2, 196.7),
        _svg_pt(52.6, 209.7),
    ]
)
Icon.draw_round_polyline(full_contour, width_units=w, color=Icon.DARK, closed=True)

save()
