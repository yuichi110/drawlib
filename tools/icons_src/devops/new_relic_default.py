# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: new_relic (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(71.84, 62.62), (71.84, 37.39), (50.0, 24.77), (50.0, 9.0), (85.51, 29.5), (85.51, 70.5)], style=Icon.fill_style('#00AC69'))
polygon([(50.0, 75.23), (71.84, 62.62), (85.51, 70.5), (50.0, 91.0), (14.49, 70.5), (28.15, 62.62)], style=Icon.fill_style('#1CE783'))
polygon([(36.34, 42.11), (36.34, 16.88), (50.0, 9.0), (50.0, 50.0), (14.49, 70.5), (14.49, 54.73)], style=Icon.fill_style('#1D252C'))
save()
# fmt: on
