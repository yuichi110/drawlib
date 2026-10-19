# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: saml."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# Federation triangle connecting IdP, SP, and User
tri = [(50.0, 82.0), (18.0, 24.0), (82.0, 24.0)]
polygon(tri, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w))
inner = [(50.0, 66.0), (31.0, 32.0), (69.0, 32.0)]
polygon(inner, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
for x, y, col in ((50.0, 82.0, Icon.PASTEL_BLUE), (18.0, 24.0, Icon.PASTEL_GREEN), (82.0, 24.0, Icon.PASTEL_GREEN)):
    circle((x, y), radius=10.5, style=Icon.fill_style(col, border_color=Icon.DARK, border_units=w))
    circle((x, y), radius=4.0, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w * 0.8))
save()
