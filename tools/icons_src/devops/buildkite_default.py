# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: buildkite (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(9.0, 77.33), (36.33, 63.94), (36.33, 36.61), (9.0, 50.0)], style=fill_style('#30F2A2'))
polygon([(63.94, 77.33), (91.0, 63.94), (63.94, 50.0)], style=fill_style('#30F2A2'))
polygon([(63.94, 77.33), (36.33, 63.94), (36.33, 36.61), (63.94, 50.0)], style=fill_style('#14CC80'))
polygon([(91.0, 63.94), (63.94, 50.0), (63.94, 22.67), (91.0, 36.61)], style=fill_style('#14CC80'))
save()
# fmt: on
