# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: replicate (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(91.0, 55.94), (91.0, 46.67), (58.48, 46.67), (58.48, 9.0), (48.11, 9.0), (48.11, 55.94)], style=Icon.fill_style('#18181B'))
polygon([(91.0, 91.0), (91.0, 81.72), (19.36, 81.72), (19.36, 9.0), (9.0, 9.0), (9.0, 91.0)], style=Icon.fill_style('#18181B'))
polygon([(91.0, 73.47), (91.0, 64.19), (38.91, 64.19), (38.91, 9.0), (28.55, 9.0), (28.55, 73.47)], style=Icon.fill_style('#18181B'))
save()
# fmt: on
