# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Workspace icon: google_docs (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()
polygon([(59.32, 91.0), (79.82, 70.5), (69.57, 68.64), (59.32, 70.5), (57.45, 80.75)], style=Icon.fill_style('#0C67D6', border_units=0.15))
polygon([(59.32, 70.5), (59.32, 91.0), (25.77, 91.0), (25.31, 90.98), (24.87, 90.93), (24.43, 90.84), (24.01, 90.72), (23.6, 90.56), (23.2, 90.38), (22.83, 90.16), (22.47, 89.92), (22.13, 89.65), (21.82, 89.36), (21.53, 89.05), (21.26, 88.71), (21.02, 88.35), (20.81, 87.98), (20.62, 87.59), (20.47, 87.18), (20.34, 86.75), (20.25, 86.32), (20.2, 85.87), (20.18, 85.41), (20.18, 14.59), (20.2, 14.13), (20.25, 13.68), (20.34, 13.25), (20.47, 12.82), (20.62, 12.41), (20.81, 12.02), (21.02, 11.65), (21.26, 11.29), (21.53, 10.95), (21.82, 10.64), (22.13, 10.35), (22.47, 10.08), (22.83, 9.84), (23.2, 9.62), (23.6, 9.44), (24.01, 9.28), (24.43, 9.16), (24.87, 9.07), (25.31, 9.02), (25.77, 9.0), (74.23, 9.0), (74.69, 9.02), (75.13, 9.07), (75.57, 9.16), (75.99, 9.28), (76.4, 9.44), (76.8, 9.62), (77.17, 9.84), (77.53, 10.08), (77.87, 10.35), (78.18, 10.64), (78.47, 10.95), (78.74, 11.29), (78.98, 11.65), (79.19, 12.02), (79.38, 12.41), (79.53, 12.82), (79.66, 13.25), (79.75, 13.68), (79.8, 14.13), (79.82, 14.59), (79.82, 70.5)], style=Icon.fill_style('#3086F6', border_units=0.15))
polygon([(66.77, 54.66), (33.23, 54.66), (33.23, 59.32), (66.77, 59.32)], style=Icon.fill_style(Icon.WHITE))
polygon([(66.77, 48.14), (33.23, 48.14), (33.23, 43.48), (66.77, 43.48)], style=Icon.fill_style(Icon.WHITE))
polygon([(57.45, 36.95), (33.23, 36.95), (33.23, 32.3), (57.45, 32.3)], style=Icon.fill_style(Icon.WHITE))
save()
# fmt: on
