# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: vault (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
st = Icon.fill_style('#FFD814')
polygon([(9.0, 91.0), (49.86, 9.0), (91.0, 91.0)], holes=[[(40.49, 74.54), (59.47, 74.54), (59.47, 55.52), (52.42, 55.52), (52.42, 48.4), (47.68, 48.4), (47.68, 55.53), (40.49, 55.53)]], style=Icon.fill_style('#FFD814'))
polygon([(59.47, 55.0), (68.0, 55.0), (76.0, 75.0), (59.47, 75.0)], style=st)
polygon([(45.24, 55.0), (47.0, 55.0), (47.68, 55.53), (47.68, 75.0), (45.24, 75.0)], style=st)
polygon([(52.42, 55.52), (53.0, 55.0), (54.71, 55.0), (54.71, 75.0), (52.42, 75.0)], style=st)
polygon([(40.0, 67.4), (60.0, 67.4), (60.0, 69.78), (40.0, 69.78)], style=st)
polygon([(40.0, 60.28), (53.0, 60.28), (53.0, 62.66), (40.0, 62.66)], style=st)
polygon([(52.42, 60.26), (60.0, 60.26), (60.0, 62.65), (52.42, 62.65)], style=st)
polygon([(47.0, 53.16), (53.0, 53.16), (53.0, 55.53), (47.0, 55.53)], style=st)
save()
# fmt: on
