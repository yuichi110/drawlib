# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Cloud vendor icon: vercel."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

p1 = [(50.0, 85.5), (91.0, 14.5), (9.0, 14.5)]
polygon(p1, style=Icon.no_border_fill('#5F6B7D'))
Icon.draw_round_polyline(p1, width_units=w, color=Icon.DARK, closed=True)

save()
# fmt: on
