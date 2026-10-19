# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original IT Service brand icon: accenture (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(11.26, 33.09), (56.5, 49.92), (11.26, 67.59), (11.26, 91.0), (88.75, 59.8), (88.75, 40.39), (11.26, 9.0)], style=Icon.fill_style('#CC75FF'))
Icon.draw_round_polyline([(11.26, 33.09), (56.5, 49.92), (11.26, 67.59), (11.26, 91.0), (88.75, 59.8), (88.75, 40.39), (11.26, 9.0)], width_units=1.6, color=Icon.DARK, closed=True)
save()
# fmt: on
