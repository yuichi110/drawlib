# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Code icon: axum (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 91.0), (85.78, 70.5), (85.78, 29.5), (50.0, 9.0), (14.22, 29.5), (14.22, 70.5)], style=Icon.fill_style('#1E293B'))
polygon([(50.0, 80.56), (75.35, 31.36), (62.67, 31.36), (50.0, 56.71), (37.33, 31.36), (24.65, 31.36)], style=Icon.fill_style('#F97316'))
polygon([(36.58, 42.55), (63.42, 42.55), (69.38, 31.36), (30.62, 31.36)], style=Icon.fill_style('#38BDF8'))
save()
# fmt: on
