# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: prefect (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 63.66), (23.65, 77.33), (50.0, 91.0), (76.35, 77.33), (76.35, 49.99), (50.0, 36.33), (50.0, 9.0), (23.66, 22.67), (23.66, 50.0), (50.0, 36.33)], style=Icon.fill_style('#024DFD'))
save()
# fmt: on
