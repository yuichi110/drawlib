# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security concept icon: passkey."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
w = Icon.ORIG_STROKE
# User silhouette on left
circle((38.0, 66.0), radius=14.0, style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=w))
body = [(14.0, 20.0), (62.0, 20.0), (56.0, 44.0), (20.0, 44.0)]
polygon(body, style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=w))
# Cryptographic passkey on right
circle((68.0, 56.0), radius=15.0, style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w))
circle((68.0, 56.0), radius=5.5, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
blade = [
    (64.0, 41.0),
    (72.0, 41.0),
    (72.0, 14.0),
    (80.0, 14.0),
    (80.0, 20.0),
    (72.0, 20.0),
    (72.0, 25.0),
    (78.0, 25.0),
    (78.0, 30.0),
    (72.0, 30.0),
    (64.0, 14.0),
]
polygon(blade, style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=w))
save()
