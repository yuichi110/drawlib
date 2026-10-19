# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: note (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.utils import Icon

Icon.setup()
rectangle((50.0, 50.0), width=76.0, height=76.0, style=Icon.fill_style((65, 201, 180), shape_r=18.0))
rectangle((35.0, 48.0), width=11.0, height=34.0, style=Icon.fill_style(Icon.WHITE, shape_r=2.0))
circle((51.5, 51.0), radius=14.0, style=Icon.fill_style(Icon.WHITE))
circle((51.5, 47.0), radius=9.0, style=Icon.fill_style((65, 201, 180)))
rectangle((51.5, 38.0), width=18.0, height=18.0, style=Icon.fill_style((65, 201, 180)))
rectangle((62.0, 43.0), width=11.0, height=24.0, style=Icon.fill_style(Icon.WHITE, shape_r=2.0))
save()
