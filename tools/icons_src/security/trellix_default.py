# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Security icon: trellix (default variant)."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import fill_style, setup_icon

# ruff: noqa: E501
# fmt: off
setup_icon()
polygon([(45.06, 50.57), (41.76, 50.57), (43.34, 52.59)], style=fill_style('#2814FF'))
polygon([(46.86, 50.57), (44.27, 50.57), (42.96, 52.1), (44.2, 53.69)], style=fill_style('#2814FF'))
polygon([(48.67, 50.57), (46.07, 50.57), (43.83, 53.2), (45.07, 54.79)], style=fill_style('#2814FF'))
polygon([(50.47, 50.57), (47.87, 50.57), (44.69, 54.31), (45.93, 55.9)], style=fill_style('#2718FF'))
polygon([(52.27, 50.57), (49.67, 50.57), (45.55, 55.41), (46.79, 57.0)], style=fill_style('#2421FF'))
polygon([(54.07, 50.57), (51.48, 50.57), (46.41, 56.52), (47.65, 58.11)], style=fill_style('#222AFF'))
polygon([(55.87, 50.57), (53.28, 50.57), (47.27, 57.62), (48.52, 59.21)], style=fill_style('#1F33FF'))
polygon([(57.67, 50.57), (55.08, 50.57), (48.14, 58.72), (49.38, 60.31)], style=fill_style('#1D3CFF'))
polygon([(59.25, 50.83), (59.04, 50.57), (56.88, 50.57), (49.0, 59.83), (50.24, 61.42)], style=fill_style('#1A45FF'))
polygon([(60.11, 51.94), (59.04, 50.57), (58.68, 50.57), (49.86, 60.93), (51.1, 62.52)], style=fill_style('#184EFF'))
polygon([(60.98, 53.04), (59.73, 51.45), (50.72, 62.04), (51.97, 63.62)], style=fill_style('#1557FF'))
polygon([(61.84, 54.14), (60.6, 52.55), (51.59, 63.14), (52.83, 64.73)], style=fill_style('#1360FF'))
polygon([(62.7, 55.25), (61.46, 53.66), (52.45, 64.24), (53.69, 65.83)], style=fill_style('#1168FF'))
polygon([(63.56, 56.35), (62.32, 54.76), (53.31, 65.35), (54.55, 66.94)], style=fill_style('#0E70FF'))
polygon([(64.43, 57.45), (63.18, 55.86), (54.17, 66.45), (55.42, 68.04)], style=fill_style('#0C78FF'))
polygon([(65.29, 58.56), (64.05, 56.97), (55.04, 67.55), (56.28, 69.14)], style=fill_style('#0A81FF'))
polygon([(66.15, 59.66), (64.91, 58.07), (55.9, 68.66), (57.14, 70.25)], style=fill_style('#0887FF'))
polygon([(67.01, 60.77), (65.77, 59.18), (56.76, 69.76), (58.0, 71.35)], style=fill_style('#078DFF'))
polygon([(67.88, 61.87), (66.63, 60.28), (57.62, 70.87), (58.87, 72.46)], style=fill_style('#0593FF'))
polygon([(68.74, 62.97), (67.5, 61.38), (58.49, 71.97), (59.73, 73.56)], style=fill_style('#0399FF'))
polygon([(69.6, 64.08), (68.36, 62.49), (59.35, 73.07), (60.59, 74.66)], style=fill_style('#029EFF'))
polygon([(70.46, 65.18), (69.22, 63.59), (60.21, 74.18), (61.45, 75.77)], style=fill_style('#01A3FF'))
polygon([(71.33, 66.29), (70.08, 64.7), (61.07, 75.28), (62.32, 76.87)], style=fill_style('#00A6F9'))
polygon([(72.19, 67.39), (70.95, 65.8), (61.94, 76.39), (63.18, 77.98)], style=fill_style('#00A8EE'))
polygon([(73.05, 68.49), (71.81, 66.9), (62.8, 77.49), (64.04, 79.08)], style=fill_style('#00AAE2'))
polygon([(73.91, 69.6), (72.67, 68.01), (63.66, 78.59), (64.9, 80.18)], style=fill_style('#00ABD6'))
polygon([(74.77, 70.7), (73.53, 69.11), (64.52, 79.7), (65.77, 81.29)], style=fill_style('#00ADCB'))
polygon([(75.64, 71.8), (74.4, 70.22), (65.39, 80.8), (66.63, 82.39)], style=fill_style('#00AFBF'))
polygon([(76.5, 72.91), (75.26, 71.32), (66.25, 81.91), (67.49, 83.49)], style=fill_style('#00B1B4'))
polygon([(77.36, 74.01), (76.12, 72.42), (67.11, 83.01), (68.35, 84.6)], style=fill_style('#00B3A8'))
polygon([(78.22, 75.12), (76.98, 73.53), (67.97, 84.11), (69.22, 85.7)], style=fill_style('#00B49C'))
polygon([(79.09, 76.22), (77.85, 74.63), (68.84, 85.22), (70.08, 86.81)], style=fill_style('#00B691'))
polygon([(79.95, 77.32), (78.71, 75.73), (69.7, 86.32), (70.94, 87.91)], style=fill_style('#00B885'))
polygon([(80.81, 78.43), (79.57, 76.84), (70.56, 87.42), (71.8, 89.01)], style=fill_style('#00BA7A'))
polygon([(81.67, 79.53), (80.43, 77.94), (71.42, 88.53), (72.66, 90.12)], style=fill_style('#00BC6E'))
polygon([(82.54, 80.64), (81.29, 79.05), (72.29, 89.63), (73.35, 91.0), (73.72, 91.0)], style=fill_style('#00BE63'))
polygon([(83.4, 81.74), (82.16, 80.15), (73.15, 90.74), (73.35, 91.0), (75.52, 91.0)], style=fill_style('#00BF57'))
polygon([(84.26, 82.84), (83.02, 81.25), (74.73, 91.0), (77.32, 91.0)], style=fill_style('#00C14B'))
polygon([(85.12, 83.95), (83.88, 82.36), (76.53, 91.0), (79.12, 91.0)], style=fill_style('#00C340'))
polygon([(85.99, 85.05), (84.74, 83.46), (78.33, 91.0), (80.92, 91.0)], style=fill_style('#00C534'))
polygon([(86.85, 86.16), (85.61, 84.57), (80.13, 91.0), (82.73, 91.0)], style=fill_style('#00C729'))
polygon([(87.71, 87.26), (86.47, 85.67), (81.93, 91.0), (84.53, 91.0)], style=fill_style('#00C81D'))
polygon([(88.57, 88.36), (87.33, 86.77), (83.73, 91.0), (86.33, 91.0)], style=fill_style('#00CA11'))
polygon([(85.54, 91.0), (90.63, 91.0), (88.19, 87.88)], style=fill_style('#00CC06'))
polygon([(74.49, 9.0), (26.65, 70.21), (9.37, 70.21), (33.28, 39.62), (9.37, 9.0), (26.65, 9.0), (41.92, 28.56), (57.21, 9.0)], style=fill_style('#1A1A1A'))
save()
# fmt: on
