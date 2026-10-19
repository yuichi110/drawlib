# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: tver (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon, rectangle
from drawlib.utils import Icon

Icon.setup()
rectangle((50.0, 50.0), width=80.0, height=66.0, style=Icon.fill_style((0, 178, 229), shape_r=15.0))
polygon(
    [(17.0, 65.0), (43.0, 65.0), (43.0, 56.5), (34.5, 56.5), (34.5, 34.0), (25.5, 34.0), (25.5, 56.5), (17.0, 56.5)],
    style=Icon.fill_style(Icon.WHITE),
)
polygon(
    [(45.0, 65.0), (54.0, 65.0), (60.5, 44.5), (67.0, 65.0), (76.0, 65.0), (65.0, 34.0), (56.0, 34.0)],
    style=Icon.fill_style(Icon.WHITE),
)
circle((80.0, 39.0), radius=4.8, style=Icon.fill_style(Icon.WHITE))
save()
