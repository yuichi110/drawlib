# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps icon: packer (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(24.66, 80.98), (51.52, 65.62), (51.52, 9.0), (24.66, 24.36)], style=fill_style('#1DAEFF'))
polygon([(64.82, 74.36), (35.62, 91.0), (35.62, 79.44), (55.48, 68.1), (55.48, 33.43), (64.82, 28.12), (65.68, 27.66), (66.52, 27.29), (67.34, 26.99), (68.14, 26.76), (68.91, 26.61), (69.64, 26.53), (70.35, 26.53), (71.02, 26.59), (71.66, 26.73), (72.25, 26.93), (72.8, 27.21), (73.3, 27.55), (73.76, 27.95), (74.16, 28.42), (74.51, 28.95), (74.8, 29.54), (75.03, 30.2), (75.2, 30.91), (75.3, 31.69), (75.34, 32.51), (75.34, 57.96), (75.3, 58.83), (75.2, 59.72), (75.03, 60.62), (74.8, 61.54), (74.51, 62.47), (74.16, 63.4), (73.76, 64.33), (73.3, 65.25), (72.8, 66.17), (72.25, 67.07), (71.66, 67.95), (71.02, 68.81), (70.35, 69.64), (69.64, 70.44), (68.91, 71.21), (68.14, 71.94), (67.34, 72.62), (66.52, 73.25), (65.68, 73.84), (64.82, 74.36)], style=fill_style('#1D94DD'))
save()
# fmt: on
