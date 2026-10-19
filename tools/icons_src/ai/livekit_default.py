# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: livekit (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(74.6, 74.6), (58.2, 74.6), (58.2, 58.2), (74.6, 58.2), (74.6, 74.6)], holes=[[(58.2, 58.2), (41.8, 58.2), (41.8, 41.8), (58.2, 41.8)]], style=Icon.fill_style('#1FD5F9'))
polygon([(74.6, 41.8), (58.2, 41.8), (58.2, 25.4), (74.6, 25.4)], style=Icon.fill_style('#1FD5F9'))
polygon([(91.0, 91.0), (74.6, 91.0), (74.6, 74.6), (91.0, 74.6)], style=Icon.fill_style('#1FD5F9'))
polygon([(91.0, 25.4), (74.6, 25.4), (74.6, 9.0), (91.0, 9.0)], style=Icon.fill_style('#1FD5F9'))
polygon([(25.4, 25.4), (25.4, 91.0), (9.0, 91.0), (9.0, 9.0), (58.2, 9.0), (58.2, 25.4)], style=Icon.fill_style('#1E40AF'))
save()
# fmt: on
