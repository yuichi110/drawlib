# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Azure icon: app_registrations (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Azure, Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(34.46, 42.49), (54.67, 42.49), (54.67, 22.33), (34.46, 22.33)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(11.13, 69.37), (31.33, 69.37), (31.33, 89.53), (13.74, 89.53), (13.02, 89.43), (12.34, 89.15), (11.76, 88.71), (11.32, 88.13), (11.04, 87.45), (10.94, 86.73)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(13.93, 22.33), (31.33, 22.33), (31.33, 42.49), (10.94, 42.49), (10.94, 25.13), (11.04, 24.4), (11.32, 23.73), (11.76, 23.15), (12.34, 22.7), (13.02, 22.42), (13.74, 22.33)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(11.13, 45.66), (31.33, 45.66), (31.33, 66.01), (10.94, 66.01)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(58.17, 22.33), (75.53, 22.33), (76.25, 22.42), (76.93, 22.7), (77.51, 23.15), (77.95, 23.73), (78.23, 24.4), (78.33, 25.13), (78.33, 42.49), (57.98, 42.49)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(34.83, 45.66), (54.67, 45.66), (54.67, 66.01), (34.46, 66.01)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(58.17, 45.66), (78.0, 45.66), (78.0, 66.01), (57.98, 66.01)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(58.17, 89.34), (58.17, 69.37), (78.0, 69.37), (78.0, 86.73), (77.9, 87.45), (77.62, 88.13), (77.18, 88.71), (76.6, 89.15), (75.92, 89.43), (75.2, 89.53)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(34.83, 69.18), (54.67, 69.18), (54.67, 89.53), (34.46, 89.53)], style=Icon.fill_style(Azure.LIGHT_BLUE))
polygon([(89.06, 42.07), (89.06, 21.02), (71.0, 10.47), (71.0, 31.52)], style=Icon.fill_style(Azure.TEAL))
polygon([(89.06, 42.07), (71.0, 31.47), (52.94, 42.07), (71.0, 52.61)], style=Icon.fill_style(Azure.LIGHT_CYAN))
polygon([(71.0, 31.47), (71.0, 10.47), (52.94, 21.02), (52.94, 42.07)], style=Icon.fill_style(Azure.CYAN))
polygon([(52.94, 21.02), (71.0, 31.52), (71.0, 10.47)], style=Icon.fill_style(Azure.LIGHT_CYAN))
polygon([(89.06, 21.02), (71.0, 31.52), (71.0, 10.47)], style=Icon.fill_style(Azure.CYAN))
save()
# fmt: on
