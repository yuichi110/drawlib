# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data icon: tidb (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(14.49, 70.5), (14.49, 29.5), (50.0, 9.0), (85.51, 29.5), (85.51, 70.5), (50.0, 91.0)], style=Icon.fill_style("#E30C34"))
polygon([(49.98, 77.31), (26.39, 63.7), (26.39, 50.08), (38.19, 56.9), (38.19, 29.48), (49.98, 22.69), (49.98, 63.7), (61.77, 70.51), (49.98, 77.32)], style=Icon.fill_style(Icon.WHITE))
polygon([(61.84, 56.82), (61.84, 29.5), (73.67, 36.33), (73.67, 63.67)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
