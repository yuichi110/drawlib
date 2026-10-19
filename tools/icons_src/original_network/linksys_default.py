# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Network vendor icon: linksys (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.styles import Colors
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w = 2.0

outer_l_pts: list[tuple[float, float]] = [(9.11, 87.27), (9.0, 9.0), (87.27, 9.0), (87.27, 22.05), (23.91, 22.05), (23.91, 87.27)]
inner_l_pts: list[tuple[float, float]] = [(35.09, 87.27), (35.09, 33.1), (87.27, 33.1), (87.27, 46.27), (50.0, 46.27), (50.0, 87.27)]
dot_pts: list[tuple[float, float]] = [(77.95, 91.0), (76.87, 90.96), (75.81, 90.81), (74.75, 90.61), (73.72, 90.29), (72.72, 89.9), (71.75, 89.43), (70.82, 88.88), (69.94, 88.24), (69.12, 87.55), (68.36, 86.79), (67.67, 85.97), (67.03, 85.09), (66.47, 84.16), (66.01, 83.19), (65.62, 82.19), (65.3, 81.16), (65.1, 80.1), (64.95, 79.04), (64.91, 77.95), (64.97, 76.82), (65.11, 75.68), (65.36, 74.58), (65.69, 73.5), (66.14, 72.44), (66.66, 71.43), (67.28, 70.46), (67.97, 69.57), (68.73, 68.73), (69.57, 67.97), (70.48, 67.28), (71.43, 66.66), (72.44, 66.14), (73.5, 65.69), (74.58, 65.36), (75.68, 65.11), (76.82, 64.97), (77.95, 64.91), (79.09, 64.97), (80.23, 65.11), (81.33, 65.36), (82.41, 65.69), (83.47, 66.14), (84.48, 66.66), (85.43, 67.28), (86.34, 67.97), (87.18, 68.73), (87.94, 69.57), (88.63, 70.46), (89.25, 71.43), (89.77, 72.44), (90.22, 73.5), (90.55, 74.58), (90.8, 75.68), (90.94, 76.82), (91.0, 77.95), (90.96, 79.04), (90.81, 80.1), (90.61, 81.16), (90.29, 82.19), (89.9, 83.19), (89.43, 84.16), (88.88, 85.09), (88.24, 85.97), (87.55, 86.79), (86.79, 87.55), (85.97, 88.24), (85.09, 88.88), (84.16, 89.43), (83.19, 89.9), (82.19, 90.29), (81.16, 90.61), (80.1, 90.81), (79.04, 90.96)]

polygon(outer_l_pts, style=Icon.no_border_fill(Colors.Blue3))
Icon.draw_round_polyline(outer_l_pts, width_units=w, color=Icon.DARK, closed=True)

polygon(inner_l_pts, style=Icon.no_border_fill(Colors.Blue2))
Icon.draw_round_polyline(inner_l_pts, width_units=w, color=Icon.DARK, closed=True)

polygon(dot_pts, style=Icon.no_border_fill(Colors.Blue2))
Icon.draw_round_polyline(dot_pts, width_units=w, color=Icon.DARK, closed=True)

save()
# fmt: on
