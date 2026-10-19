# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: instagram (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
rectangle((50.0, 50.0), width=76.0, height=76.0, style=Icon.fill_style((228, 64, 95), shape_r=20.0))
rectangle(
    (50.0, 50.0),
    width=52.0,
    height=52.0,
    style=Icon.fill_style((228, 64, 95), border_color=Icon.WHITE, border_units=5.2, shape_r=14.0),
)
circle((50.0, 50.0), radius=12.5, style=Icon.fill_style((228, 64, 95), border_color=Icon.WHITE, border_units=5.2))
circle((64.5, 64.5), radius=3.4, style=Icon.fill_style(Icon.WHITE))
save()
