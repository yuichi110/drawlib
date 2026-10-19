# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: osquery (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(90.95, 91.0), (90.95, 70.48), (70.48, 50.0), (70.48, 70.56), (90.95, 91.0)], style=Icon.fill_style('#A596FF'))
polygon([(50.0, 91.0), (50.0, 70.48), (70.48, 50.0), (70.48, 70.56), (50.0, 91.0)], style=Icon.fill_style('#000000'))
polygon([(91.0, 9.05), (70.48, 9.05), (50.0, 29.52), (70.56, 29.52), (91.0, 9.05)], style=Icon.fill_style('#A596FF'))
polygon([(91.0, 50.0), (70.48, 50.0), (50.0, 29.52), (70.56, 29.52), (91.0, 50.0)], style=Icon.fill_style('#000000'))
polygon([(9.04, 9.0), (9.04, 29.52), (29.52, 50.0), (29.52, 29.44), (9.04, 9.0)], style=Icon.fill_style('#A596FF'))
polygon([(50.0, 9.0), (50.0, 29.52), (29.52, 50.0), (29.52, 29.44), (50.0, 9.0)], style=Icon.fill_style('#000000'))
polygon([(9.0, 90.96), (29.52, 90.96), (50.0, 70.48), (29.44, 70.48), (9.0, 90.96)], style=Icon.fill_style('#A596FF'))
polygon([(9.0, 50.0), (29.52, 50.0), (50.0, 70.48), (29.44, 70.48), (9.0, 50.0)], style=Icon.fill_style('#000000'))
save()
# fmt: on
