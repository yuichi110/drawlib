# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Workspace concept icon: google_slides."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

Icon.setup()
w = 2.0
w_frame = 1.6

page_pts = [
    (58.82, 88.80),
    (27.07, 88.80),
    (26.38, 88.75),
    (25.70, 88.62),
    (25.05, 88.40),
    (24.43, 88.09),
    (23.85, 87.71),
    (23.33, 87.25),
    (22.87, 86.73),
    (22.49, 86.15),
    (22.18, 85.53),
    (21.96, 84.88),
    (21.83, 84.20),
    (21.78, 83.51),
    (21.78, 16.49),
    (21.83, 15.80),
    (21.96, 15.12),
    (22.18, 14.47),
    (22.49, 13.85),
    (22.87, 13.27),
    (23.33, 12.75),
    (23.85, 12.29),
    (24.43, 11.91),
    (25.05, 11.60),
    (25.70, 11.38),
    (26.38, 11.25),
    (27.07, 11.20),
    (72.93, 11.20),
    (73.62, 11.25),
    (74.30, 11.38),
    (74.95, 11.60),
    (75.57, 11.91),
    (76.15, 12.29),
    (76.67, 12.75),
    (77.13, 13.27),
    (77.51, 13.85),
    (77.82, 14.47),
    (78.04, 15.12),
    (78.17, 15.80),
    (78.22, 16.49),
    (78.22, 69.40),
]
fold_pts = [
    (58.82, 88.80),
    (78.22, 69.40),
    (58.82, 69.40),
]

frame_outer = [
    (32.36, 58.38),
    (32.36, 33.69),
    (67.64, 33.69),
    (67.64, 58.38),
]
frame_hole = [
    (63.23, 38.10),
    (36.77, 38.10),
    (36.77, 53.97),
    (63.23, 53.97),
]

polygon(page_pts, style=Icon.no_border_fill("#F2C94F"))
Icon.draw_round_polyline(page_pts, width_units=w, color=Icon.DARK, closed=True)

polygon(fold_pts, style=Icon.no_border_fill("#F1B93F"))
Icon.draw_round_polyline(fold_pts, width_units=w, color=Icon.DARK, closed=True)

polygon(frame_outer, holes=[frame_hole], style=Icon.fill_style(Icon.WHITE))
Icon.draw_round_polyline(frame_outer, width_units=w_frame, color=Icon.DARK, closed=True)
Icon.draw_round_polyline(frame_hole, width_units=w_frame, color=Icon.DARK, closed=True)

save()
