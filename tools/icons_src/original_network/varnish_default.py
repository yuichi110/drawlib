# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network concept icon: varnish."""

from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors
from drawlib.utils import Icon

Icon.setup()

w = 2.0

# 3 circles from Varnish logo geometry
circle((71.33, 71.69), radius=19.31, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))
circle((40.73, 22.92), radius=13.92, style=Icon.fill_style(Colors.Blue2, border_color=Icon.DARK, border_units=w))
circle((17.40, 54.67), radius=8.04, style=Icon.fill_style(Colors.Blue3, border_color=Icon.DARK, border_units=w))

save()
