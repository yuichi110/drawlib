# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Business icon: marketo (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(85.11, 25.69), (85.11, 79.61), (64.17, 91.0), (64.17, 9.0)], style=Icon.fill_style('#5C4C9F'))
polygon([(37.55, 83.87), (54.42, 78.88), (54.42, 26.91), (37.55, 19.54)], style=Icon.fill_style('#5C4C9F'))
polygon([(27.8, 73.27), (14.95, 75.34), (14.89, 28.8), (27.8, 32.21)], style=Icon.fill_style('#5C4C9F'))
save()
# fmt: on
