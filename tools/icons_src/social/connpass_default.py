# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: connpass (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import circle, polygon
from drawlib.utils import Icon

Icon.setup()
circle((50.0, 50.0), radius=39.0, style=Icon.fill_style((200, 22, 29)))
circle((50.0, 50.0), radius=30.0, style=Icon.fill_style(Icon.WHITE))
polygon([(50.0, 76.0), (60.0, 50.0), (50.0, 55.0), (40.0, 50.0)], style=Icon.fill_style((200, 22, 29)))
polygon([(50.0, 24.0), (60.0, 50.0), (50.0, 45.0), (40.0, 50.0)], style=Icon.fill_style((55, 65, 81)))
circle((50.0, 50.0), radius=4.2, style=Icon.fill_style((200, 22, 29)))
save()
