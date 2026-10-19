# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Social icon: substack (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(16.62, 53.76), (16.62, 12.0), (50.0, 30.65), (83.38, 12.0), (83.38, 53.76), (16.62, 53.76)], style=Icon.fill_style((255, 103, 25)))
polygon([(83.37, 61.9), (16.62, 61.9), (16.62, 70.88), (83.38, 70.88), (83.38, 61.9)], style=Icon.fill_style((255, 103, 25)))
polygon([(83.38, 88.0), (16.62, 88.0), (16.62, 79.02), (83.38, 79.02), (83.38, 88.0)], style=Icon.fill_style((255, 103, 25)))
save()
# fmt: on
