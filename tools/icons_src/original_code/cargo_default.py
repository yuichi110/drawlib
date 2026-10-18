# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Code icon: cargo."""

import math

from drawlib.canvas import save
from drawlib.shapes import polygon
from drawlib.utils import (
    DARK,
    draw_compound_polygon,
    draw_round_polyline,
    draw_round_segment,
    no_border_fill,
    setup_icon,
)

# ruff: noqa: E501
# fmt: off
setup_icon()

s = 40.0 / 41.0
w_outer = 2.0
w_seam = 1.2
w_tape = 0.85

CRATE_TOP = "#EDAD4F"
CRATE_LEFT = "#D99E4E"
CRATE_RIGHT = "#C7883B"
PALLET_TOP = "#C7883B"
PALLET_LEFT = "#B5782F"
PALLET_RIGHT = "#966020"
TAPE_FILL = "#F3C463"
STAMP_BROWN = "#8C5A20"


def _sc(pts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    return [(50.0 + (x - 50.0) * s, 50.0 + (y - 50.0) * s) for x, y in pts]


def _sc_pt(pt_xy: tuple[float, float]) -> tuple[float, float]:
    return (50.0 + (pt_xy[0] - 50.0) * s, 50.0 + (pt_xy[1] - 50.0) * s)


def _draw_iso_gear_stamp(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    skew_y: float,
) -> None:
    """Draw a clean flat isometric gear-ring decal with an 'R' center on a crate face."""
    def _iso(u: float, v: float) -> tuple[float, float]:
        dx = u * rx
        dy = v * ry + dx * skew_y
        return (cx + dx, cy + dy)

    n_teeth = 16
    pts_per_tooth = 4
    total = n_teeth * pts_per_tooth
    outer_ring: list[tuple[float, float]] = []
    for i in range(total):
        ang = 2.0 * math.pi * (i / total)
        phase = i % pts_per_tooth
        r_mult = 1.0 if phase in (0, 1) else 0.85
        outer_ring.append(_iso(r_mult * math.cos(ang), r_mult * math.sin(ang)))

    inner_ring: list[tuple[float, float]] = []
    for i in range(36):
        ang = 2.0 * math.pi * (i / 36.0)
        inner_ring.append(_iso(0.62 * math.cos(ang), 0.62 * math.sin(ang)))

    draw_compound_polygon([_sc(outer_ring), _sc(inner_ring)], color=STAMP_BROWN)

    # Isometric 'R' glyph inside the stamp ring
    r_outer = [
        _iso(-0.42, -0.38),
        _iso(-0.42, 0.38),
        _iso(0.14, 0.38),
        _iso(0.32, 0.24),
        _iso(0.32, 0.04),
        _iso(0.15, -0.06),
        _iso(0.38, -0.38),
        _iso(0.10, -0.38),
        _iso(-0.08, -0.08),
        _iso(-0.16, -0.08),
        _iso(-0.16, -0.38),
    ]
    r_hole = [
        _iso(-0.16, 0.07),
        _iso(-0.16, 0.22),
        _iso(0.06, 0.22),
        _iso(0.12, 0.14),
        _iso(0.06, 0.07),
    ]
    draw_compound_polygon([_sc(r_outer), _sc(r_hole)], color=STAMP_BROWN)


def _draw_tape(pts_raw: list[tuple[float, float]]) -> None:
    pts = _sc(pts_raw)
    polygon(pts, style=no_border_fill(TAPE_FILL))
    draw_round_polyline(pts, width_units=w_tape, color=DARK, closed=True)


def _draw_arrow(pts_raw: list[tuple[float, float]]) -> None:
    polygon(_sc(pts_raw), style=no_border_fill(DARK))


# 1. Wooden Pallet Polygons
pallet_polys = [
    (_sc([(44.32, 11.94), (44.3, 13.24), (80.95, 28.9), (86.74, 28.08), (86.71, 26.98), (50.06, 9.0)]), PALLET_LEFT),
    (_sc([(44.32, 13.08), (80.97, 29.78), (86.79, 27.9), (49.86, 10.12)]), PALLET_RIGHT),
    (_sc([(44.32, 17.34), (50.03, 14.24), (50.03, 10.21), (44.32, 13.31)]), PALLET_LEFT),
    (_sc([(86.36, 31.83), (82.05, 29.65), (82.05, 25.62), (86.36, 27.8)]), PALLET_LEFT),
    (_sc([(61.08, 25.3), (66.79, 22.2), (66.79, 18.17), (61.08, 21.26)]), PALLET_RIGHT),
    (_sc([(71.02, 24.44), (66.71, 22.27), (66.71, 18.23), (71.02, 20.41)]), PALLET_LEFT),
    (_sc([(28.47, 19.9), (28.45, 21.03), (65.09, 36.69), (70.89, 35.87), (70.86, 34.78), (34.21, 16.93)]), PALLET_RIGHT),
    (_sc([(28.47, 25.01), (34.18, 21.92), (34.18, 17.88), (28.47, 20.98)]), PALLET_LEFT),
    (_sc([(38.35, 24.16), (34.03, 21.98), (34.03, 17.95), (38.35, 20.13)]), PALLET_RIGHT),
    (_sc([(13.49, 27.28), (13.47, 28.28), (50.12, 43.93), (55.92, 43.11), (55.89, 42.02), (19.24, 24.32)]), PALLET_RIGHT),
    (_sc([(13.49, 32.4), (19.2, 29.3), (19.2, 25.27), (13.49, 28.36)]), PALLET_LEFT),
    (_sc([(23.52, 31.55), (19.2, 29.37), (19.2, 25.34), (23.52, 27.51)]), PALLET_RIGHT),
    (_sc([(13.07, 32.11), (13.07, 31.25), (50.0, 14.2), (86.93, 31.25), (86.93, 32.11), (50.0, 15.01)]), PALLET_LEFT),
    (_sc([(13.07, 32.11), (50.0, 44.96), (86.93, 32.11), (50.0, 15.01)]), PALLET_TOP),
]

for pts, col in pallet_polys:
    polygon(pts, style=no_border_fill(col))

for pts, _ in pallet_polys:
    draw_round_polyline(pts, width_units=w_seam * 0.9, color=DARK, closed=True)

# 2. Crates in Strict Back-to-Front Painter's Order
# 2a. Bottom-Left crate (back-left)
bl_left = _sc([(14.77, 33.00), (32.39, 24.87), (32.39, 47.05), (14.77, 54.09)])
bl_top = _sc([(14.77, 54.09), (32.39, 47.05), (50.00, 53.88), (32.39, 60.96)])
polygon(bl_left, style=no_border_fill(CRATE_LEFT))
polygon(bl_top, style=no_border_fill(CRATE_TOP))
_draw_tape([(21.5, 51.43), (25.71, 49.73), (32.39, 52.29), (32.39, 55.69)])
draw_round_segment(_sc_pt((23.44, 50.58)), _sc_pt((32.39, 54.02)), width_units=w_tape * 0.85, color=DARK)
_draw_tape([(25.62, 49.73), (21.5, 51.43), (21.5, 46.6), (22.07, 47.17), (22.58, 46.32), (22.87, 46.04), (23.27, 46.6), (23.66, 45.75), (24.03, 45.75), (24.54, 46.04), (25.23, 45.18), (25.62, 45.18)])
_draw_tape([(21.68, 29.84), (25.62, 28.14), (25.77, 32.97), (25.2, 32.68), (24.66, 33.25), (24.37, 33.53), (23.98, 33.25), (23.58, 33.82), (23.21, 33.82), (22.67, 33.53), (21.99, 34.39), (21.59, 34.39)])
_draw_arrow([(16.96, 47.42), (16.96, 49.31), (17.58, 48.94), (16.76, 51.31), (15.94, 49.91), (16.56, 49.54), (16.56, 47.66)])
_draw_arrow([(29.94, 42.31), (29.94, 44.19), (30.56, 43.83), (29.74, 46.19), (28.92, 44.8), (29.54, 44.43), (29.54, 42.54)])
draw_round_polyline(bl_left, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(bl_top, width_units=w_seam, color=DARK, closed=True)

# 2b. Bottom-Right crate (back-right)
br_right = _sc([(67.61, 25.17), (85.23, 33.45), (85.23, 54.22), (67.61, 47.05)])
polygon(br_right, style=no_border_fill(CRATE_RIGHT))
_draw_iso_gear_stamp(77.05, 39.85, 5.2, 5.8, 0.42)
_draw_tape([(79.83, 52.0), (75.57, 50.3), (75.57, 55.13), (76.14, 54.56), (76.71, 55.41), (76.99, 55.69), (77.56, 55.13), (77.84, 55.98), (78.13, 55.98), (78.69, 55.69), (79.26, 56.55), (79.83, 56.55)])
draw_round_polyline(br_right, width_units=w_seam, color=DARK, closed=True)

# 2c. Top-Back crate
tb_left = _sc([(32.39, 60.96), (50.00, 53.88), (50.00, 77.05), (32.39, 83.92)])
tb_top = _sc([(32.39, 83.92), (50.00, 77.05), (67.61, 83.65), (50.00, 90.92)])
polygon(tb_left, style=no_border_fill(CRATE_LEFT))
polygon(tb_top, style=no_border_fill(CRATE_TOP))
_draw_tape([(56.53, 88.31), (38.64, 81.26), (42.9, 79.59), (60.51, 86.58)])
draw_round_segment(_sc_pt((40.62, 80.50)), _sc_pt((58.24, 87.51)), width_units=w_tape * 0.85, color=DARK)
_draw_tape([(42.9, 79.67), (38.64, 81.29), (38.64, 76.6), (39.49, 77.0), (39.77, 76.18), (40.06, 76.06), (40.62, 76.41), (40.91, 75.75), (41.19, 75.61), (41.76, 76.09), (42.61, 75.16), (42.9, 75.01)])
_draw_arrow([(34.83, 77.39), (34.83, 79.28), (35.45, 78.91), (34.63, 81.28), (33.81, 79.88), (34.43, 79.52), (34.43, 77.63)])
draw_round_polyline(tb_left, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(tb_top, width_units=w_seam, color=DARK, closed=True)

# 2d. Top-Right crate
tr_right = _sc([(67.61, 47.05), (85.23, 54.22), (85.23, 76.72), (67.61, 70.00)])
tr_top = _sc([(50.00, 77.05), (67.61, 70.00), (85.23, 76.72), (67.61, 83.65)])
polygon(tr_right, style=no_border_fill(CRATE_RIGHT))
polygon(tr_top, style=no_border_fill(CRATE_TOP))
_draw_tape([(61.93, 81.46), (58.24, 79.99), (75.85, 73.11), (79.55, 74.62)])
draw_round_segment(_sc_pt((59.94, 80.72)), _sc_pt((77.84, 73.79)), width_units=w_tape * 0.85, color=DARK)
_draw_tape([(75.85, 73.05), (79.83, 74.59), (79.83, 69.93), (79.26, 70.3), (78.69, 69.5), (78.41, 69.39), (78.13, 69.76), (77.56, 69.1), (77.27, 68.96), (76.71, 69.45), (76.14, 68.51), (75.57, 68.37)])
_draw_arrow([(70.25, 64.49), (70.25, 66.38), (70.81, 66.72), (70.06, 68.15), (69.32, 65.82), (69.89, 66.16), (69.89, 64.27)])
_draw_arrow([(83.31, 69.83), (83.31, 71.72), (83.88, 72.06), (83.13, 73.49), (82.39, 71.16), (82.95, 71.5), (82.95, 69.61)])
draw_round_polyline(tr_right, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(tr_top, width_units=w_seam, color=DARK, closed=True)

# 2e. Bottom-Front crate
bf_left = _sc([(32.39, 24.87), (50.00, 16.55), (50.00, 39.85), (32.39, 47.05)])
bf_right = _sc([(50.00, 16.55), (67.61, 25.17), (67.61, 47.05), (50.00, 39.85)])
polygon(bf_left, style=no_border_fill(CRATE_LEFT))
polygon(bf_right, style=no_border_fill(CRATE_RIGHT))
_draw_iso_gear_stamp(41.15, 31.65, 5.2, 5.8, -0.44)
_draw_tape([(38.07, 44.61), (42.33, 42.91), (42.33, 47.74), (41.76, 47.17), (41.19, 48.02), (40.91, 48.02), (40.62, 47.74), (40.06, 48.31), (39.77, 48.59), (39.2, 48.02), (38.64, 48.88), (38.07, 49.16)])
_draw_tape([(61.65, 22.17), (57.67, 20.47), (57.67, 25.3), (58.24, 25.01), (58.81, 25.86), (59.09, 25.86), (59.38, 25.58), (59.94, 26.15), (60.23, 26.43), (60.8, 25.86), (61.36, 26.72), (61.65, 27.0)])
_draw_tape([(57.67, 42.91), (61.93, 44.33), (61.93, 39.79), (61.36, 40.07), (60.8, 39.22), (60.51, 39.22), (59.94, 39.5), (59.66, 38.93), (59.38, 38.65), (58.81, 39.22), (57.95, 38.36), (57.67, 38.08)])
_draw_arrow([(52.35, 35.23), (52.35, 37.11), (52.91, 37.45), (52.16, 38.88), (51.42, 36.56), (51.99, 36.9), (51.99, 35.01)])
_draw_arrow([(65.42, 40.34), (65.42, 42.23), (65.98, 42.57), (65.23, 44.0), (64.49, 41.67), (65.06, 42.01), (65.06, 40.13)])
draw_round_polyline(bf_left, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(bf_right, width_units=w_seam, color=DARK, closed=True)

# 2f. Top-Front crate (front-most top crate)
tf_left = _sc([(32.39, 47.05), (50.00, 39.85), (50.00, 63.08), (32.39, 70.15)])
tf_right = _sc([(50.00, 39.85), (67.61, 47.05), (67.61, 70.00), (50.00, 63.08)])
tf_top = _sc([(32.39, 70.15), (50.00, 63.08), (67.61, 70.00), (50.00, 77.05)])
polygon(tf_left, style=no_border_fill(CRATE_LEFT))
polygon(tf_right, style=no_border_fill(CRATE_RIGHT))
polygon(tf_top, style=no_border_fill(CRATE_TOP))
_draw_iso_gear_stamp(58.85, 54.85, 5.2, 5.8, 0.42)
_draw_tape([(55.68, 74.73), (38.07, 67.68), (42.05, 65.92), (59.66, 73.0)])
draw_round_segment(_sc_pt((40.06, 67.06)), _sc_pt((57.67, 73.93)), width_units=w_tape * 0.85, color=DARK)
_draw_tape([(42.33, 65.92), (38.07, 67.63), (38.07, 62.8), (38.64, 63.37), (39.2, 62.51), (39.49, 62.51), (39.77, 62.8), (40.34, 62.23), (40.62, 61.95), (41.19, 62.51), (41.76, 61.38), (42.33, 61.38)])
_draw_arrow([(34.54, 63.62), (34.54, 65.5), (35.17, 65.13), (34.34, 67.5), (33.52, 66.1), (34.15, 65.74), (34.15, 63.85)])
_draw_arrow([(47.33, 58.22), (47.33, 60.1), (47.95, 59.74), (47.13, 62.1), (46.31, 60.71), (46.93, 60.34), (46.93, 58.45)])
draw_round_polyline(tf_left, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(tf_right, width_units=w_seam, color=DARK, closed=True)
draw_round_polyline(tf_top, width_units=w_seam, color=DARK, closed=True)

# 3. Outer Crate Silhouette (w=1.8)
crate_outer = _sc([
    (14.77, 33.00),
    (32.39, 24.87),
    (50.00, 16.55),
    (67.61, 25.17),
    (85.23, 33.45),
    (85.23, 76.72),
    (67.61, 83.65),
    (50.00, 90.92),
    (32.39, 83.92),
    (32.39, 60.96),
    (14.77, 54.09),
])
draw_round_polyline(crate_outer, width_units=w_outer, color=DARK, closed=True)
# fmt: on

save()
