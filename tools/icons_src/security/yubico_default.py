# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: yubico (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import WHITE, fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(91.0, 50.0), (90.81, 45.98), (90.21, 42.0), (89.24, 38.1), (87.88, 34.31), (86.16, 30.68), (84.08, 27.22), (81.69, 23.99), (78.99, 21.01), (76.01, 18.31), (72.78, 15.92), (69.32, 13.84), (65.69, 12.12), (61.9, 10.76), (58.0, 9.79), (54.02, 9.19), (50.0, 9.0), (45.98, 9.19), (42.0, 9.79), (38.1, 10.76), (34.31, 12.12), (30.68, 13.84), (27.22, 15.92), (23.99, 18.31), (21.01, 21.01), (18.31, 23.99), (15.92, 27.22), (13.84, 30.68), (12.12, 34.31), (10.76, 38.1), (9.79, 42.0), (9.19, 45.98), (9.0, 50.0), (9.19, 54.02), (9.79, 58.0), (10.76, 61.9), (12.12, 65.69), (13.84, 69.32), (15.92, 72.78), (18.31, 76.01), (21.01, 78.99), (23.99, 81.69), (27.22, 84.08), (30.68, 86.16), (34.31, 87.88), (38.1, 89.24), (42.0, 90.21), (45.98, 90.81), (50.0, 91.0), (54.02, 90.81), (58.0, 90.21), (61.9, 89.24), (65.69, 87.88), (69.32, 86.16), (72.78, 84.08), (76.01, 81.69), (78.99, 78.99), (81.69, 76.01), (84.08, 72.78), (86.16, 69.32), (87.88, 65.69), (89.24, 61.9), (90.21, 58.0), (90.81, 54.02)], style=fill_style('#84BD00'))
polygon([(50.31, 51.23), (57.86, 72.63), (68.76, 72.63), (50.37, 27.37), (38.85, 27.37), (44.12, 39.76), (31.24, 72.6), (42.37, 72.6)], style=fill_style(WHITE))
save()
# fmt: on
