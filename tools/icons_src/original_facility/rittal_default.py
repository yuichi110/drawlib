# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Facility icon: rittal."""

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import Icon

# ruff: noqa: E501
# fmt: off
Icon.setup()

w_emblem = 2.0
w_band = 1.1
w_text = 0.9

emblem = [(20.48, 91.0), (79.52, 91.0), (79.52, 9.0), (20.48, 9.0)]
polygon(emblem, style=Icon.no_border_fill(Icon.WHITE))
Icon.draw_round_polyline(emblem, width_units=w_emblem, color=Icon.DARK, closed=True)

band_1 = [(21.61, 58.31), (46.61, 58.31), (46.61, 46.6), (21.61, 46.6)]
polygon(band_1, style=Icon.no_border_fill("#5EC28E"))
Icon.draw_round_polyline(band_1, width_units=w_band, color=Icon.DARK, closed=True)
band_2 = [(21.61, 20.16), (46.61, 20.16), (46.61, 10.12), (21.61, 10.12)]
polygon(band_2, style=Icon.no_border_fill("#5EC28E"))
Icon.draw_round_polyline(band_2, width_units=w_band, color=Icon.DARK, closed=True)
band_3 = [(47.42, 46.6), (54.56, 46.6), (54.56, 66.19), (21.61, 66.19), (21.61, 59.1), (47.42, 59.1)]
polygon(band_3, style=Icon.no_border_fill("#4FAEE7"))
Icon.draw_round_polyline(band_3, width_units=w_band, color=Icon.DARK, closed=True)
band_4 = [(47.41, 20.16), (54.56, 20.16), (54.56, 10.12), (47.41, 10.12)]
polygon(band_4, style=Icon.no_border_fill("#4FAEE7"))
Icon.draw_round_polyline(band_4, width_units=w_band, color=Icon.DARK, closed=True)
band_5 = [(55.35, 46.6), (62.5, 46.6), (62.5, 74.09), (21.61, 74.09), (21.61, 67.0), (55.35, 67.0)]
polygon(band_5, style=Icon.no_border_fill("#5E90CA"))
Icon.draw_round_polyline(band_5, width_units=w_band, color=Icon.DARK, closed=True)
band_6 = [(55.35, 20.16), (62.5, 20.16), (62.5, 10.12), (55.35, 10.12)]
polygon(band_6, style=Icon.no_border_fill("#5E90CA"))
Icon.draw_round_polyline(band_6, width_units=w_band, color=Icon.DARK, closed=True)
band_7 = [(63.3, 46.6), (70.44, 46.6), (70.44, 81.98), (21.61, 81.98), (21.61, 74.89), (63.3, 74.89)]
polygon(band_7, style=Icon.no_border_fill("#B86CA8"))
Icon.draw_round_polyline(band_7, width_units=w_band, color=Icon.DARK, closed=True)
band_8 = [(63.3, 20.16), (70.44, 20.16), (70.44, 10.12), (63.3, 10.12)]
polygon(band_8, style=Icon.no_border_fill("#B86CA8"))
Icon.draw_round_polyline(band_8, width_units=w_band, color=Icon.DARK, closed=True)
band_9 = [(21.61, 89.88), (21.61, 82.78), (71.25, 82.78), (71.25, 46.6), (78.39, 46.6), (78.39, 89.88)]
polygon(band_9, style=Icon.no_border_fill("#EF4C74"))
Icon.draw_round_polyline(band_9, width_units=w_band, color=Icon.DARK, closed=True)
band_10 = [(71.25, 20.16), (78.39, 20.16), (78.39, 10.12), (71.25, 10.12)]
polygon(band_10, style=Icon.no_border_fill("#EF4C74"))
Icon.draw_round_polyline(band_10, width_units=w_band, color=Icon.DARK, closed=True)

txt_11 = [(21.61, 25.77), (78.39, 25.77), (78.39, 23.51), (21.61, 23.51)]
polygon(txt_11, style=Icon.no_border_fill("#4A5568"))
Icon.draw_round_polyline(txt_11, width_units=w_text, color=Icon.DARK, closed=True)
txt_rings_12 = [[(35.29, 41.3), (35.06, 41.55), (34.81, 41.77), (34.55, 41.97), (34.26, 42.14), (33.98, 42.3), (33.67, 42.43), (33.35, 42.53), (33.03, 42.6), (32.7, 42.65), (32.37, 42.67), (32.03, 42.66), (26.39, 42.66), (24.8, 36.77), (21.61, 36.77), (21.61, 33.75), (23.99, 33.75), (22.49, 28.19), (25.95, 28.19), (27.43, 33.7), (28.83, 33.7), (30.12, 28.19), (33.91, 28.19), (32.38, 34.21), (32.81, 34.4), (33.24, 34.62), (33.64, 34.88), (34.02, 35.17), (34.37, 35.49), (34.69, 35.85), (34.98, 36.23), (35.23, 36.63), (35.45, 37.06), (35.63, 37.5), (35.77, 37.96), (35.86, 38.27), (35.92, 38.58), (35.96, 38.9), (35.97, 39.21), (35.95, 39.53), (35.9, 39.85), (35.83, 40.15), (35.73, 40.46), (35.61, 40.75), (35.46, 41.04)], [(32.41, 38.3), (32.35, 38.13), (32.29, 37.97), (32.21, 37.81), (32.12, 37.67), (32.01, 37.53), (31.89, 37.4), (31.76, 37.28), (31.62, 37.17), (31.48, 37.08), (31.33, 36.99), (31.16, 36.92), (31.0, 36.86), (30.83, 36.82), (30.66, 36.8), (30.48, 36.78), (30.3, 36.78), (28.26, 36.78), (28.99, 39.48), (31.41, 39.48), (31.51, 39.49), (31.62, 39.48), (31.71, 39.47), (31.81, 39.45), (31.91, 39.42), (32.01, 39.39), (32.1, 39.34), (32.19, 39.29), (32.27, 39.23), (32.35, 39.17), (32.39, 39.09), (32.42, 39.0), (32.44, 38.91), (32.46, 38.83), (32.47, 38.74), (32.48, 38.65), (32.47, 38.56), (32.45, 38.47), (32.44, 38.39)]]
polygon(txt_rings_12[0], holes=[txt_rings_12[1]], style=Icon.fill_style("#4A5568"))
for r in txt_rings_12:
    Icon.draw_round_polyline(r, width_units=w_text, color=Icon.DARK, closed=True)
txt_13 = [(34.87, 28.19), (38.32, 28.19), (42.23, 42.66), (38.77, 42.66)]
polygon(txt_13, style=Icon.no_border_fill("#4A5568"))
Icon.draw_round_polyline(txt_13, width_units=w_text, color=Icon.DARK, closed=True)
txt_14 = [(73.09, 31.37), (76.13, 42.66), (72.68, 42.66), (68.78, 28.19), (78.39, 28.19), (78.39, 31.37)]
polygon(txt_14, style=Icon.no_border_fill("#4A5568"))
Icon.draw_round_polyline(txt_14, width_units=w_text, color=Icon.DARK, closed=True)
txt_rings_15 = [[(66.95, 42.66), (64.32, 42.66), (55.07, 28.19), (58.87, 28.19), (60.49, 30.81), (64.63, 30.81), (64.83, 28.19), (68.38, 28.19)], [(62.2, 33.86), (64.36, 37.42), (64.53, 33.86)]]
polygon(txt_rings_15[0], holes=[txt_rings_15[1]], style=Icon.fill_style("#4A5568"))
for r in txt_rings_15:
    Icon.draw_round_polyline(r, width_units=w_text, color=Icon.DARK, closed=True)
txt_16 = [(51.51, 42.66), (43.43, 42.66), (42.57, 39.48), (45.11, 39.48), (42.07, 28.19), (45.53, 28.19), (48.57, 39.48), (50.66, 39.48)]
polygon(txt_16, style=Icon.no_border_fill("#4A5568"))
Icon.draw_round_polyline(txt_16, width_units=w_text, color=Icon.DARK, closed=True)
txt_17 = [(52.29, 42.66), (51.43, 39.48), (53.76, 39.48), (50.71, 28.19), (54.17, 28.19), (57.22, 39.48), (59.48, 39.48), (60.33, 42.66)]
polygon(txt_17, style=Icon.no_border_fill("#4A5568"))
Icon.draw_round_polyline(txt_17, width_units=w_text, color=Icon.DARK, closed=True)

save()
# fmt: on
