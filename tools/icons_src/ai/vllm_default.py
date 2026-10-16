# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AI icon: vllm (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(10.11, 73.27), (43.35, 73.27), (43.35, 9.0)], style=fill_style('#FDB515'))
polygon([(59.97, 75.49), (89.89, 91.0), (67.73, 9.0), (43.35, 9.0)], style=fill_style('#30A2FF'))
save()
# fmt: on
