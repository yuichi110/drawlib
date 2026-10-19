# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Security icon: ory (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(50.0, 70.0), (46.1, 69.62), (42.35, 68.48), (38.89, 66.63), (35.86, 64.14), (33.37, 61.11), (31.52, 57.65), (30.38, 53.9), (30.0, 50.0), (30.38, 46.1), (31.52, 42.35), (33.37, 38.89), (35.86, 35.86), (38.89, 33.37), (42.35, 31.52), (46.1, 30.38), (50.0, 30.0), (53.9, 30.38), (57.65, 31.52), (61.11, 33.37), (64.14, 35.86), (66.63, 38.89), (68.48, 42.35), (69.62, 46.1), (70.0, 50.0), (69.62, 53.9), (68.48, 57.65), (66.63, 61.11), (64.14, 64.14), (61.11, 66.63), (57.65, 68.48), (53.9, 69.62)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(30.0, 72.5), (30.0, 80.0), (50.0, 90.0), (70.0, 80.0), (70.0, 72.5), (50.0, 82.5)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
polygon([(70.0, 27.5), (70.0, 20.0), (50.0, 10.0), (30.0, 20.0), (30.0, 27.5), (50.0, 17.5)], style=Icon.fill_style(Icon.PASTEL_BLUE, border_color=Icon.DARK, border_units=1.8))
save()
# fmt: on
