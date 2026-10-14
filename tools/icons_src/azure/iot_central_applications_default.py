# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: iot_central_applications (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import AZURE_CYAN, AZURE_GRAY, AZURE_LIGHT_CYAN, AZURE_TEAL, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(50.0, 92.0), (13.37, 71.05), (13.37, 57.05), (27.6, 48.41), (27.6, 56.81), (20.13, 61.11), (20.13, 66.89), (50.0, 84.16), (79.87, 66.85), (79.87, 33.34), (50.0, 16.07), (13.37, 37.03), (13.37, 29.19), (50.0, 8.0), (86.63, 28.95), (86.63, 70.95)], style=fill_style("#A3A3A3"))
polygon([(50.0, 92.0), (13.37, 71.05), (20.13, 66.89), (50.0, 84.16), (79.87, 66.89), (86.63, 71.05)], style=fill_style(AZURE_GRAY))
polygon([(69.83, 61.48), (69.83, 38.52), (50.0, 26.99), (50.0, 49.95)], style=fill_style(AZURE_TEAL))
polygon([(69.83, 61.48), (50.0, 49.95), (30.17, 61.48), (50.0, 73.01)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(50.0, 49.95), (50.0, 26.99), (30.17, 38.52), (30.17, 61.48)], style=fill_style(AZURE_CYAN))
polygon([(30.17, 38.52), (50.0, 49.95), (50.0, 26.99)], style=fill_style(AZURE_LIGHT_CYAN))
polygon([(69.83, 38.52), (50.0, 49.95), (50.0, 26.99)], style=fill_style(AZURE_CYAN))
save()
# fmt: on
