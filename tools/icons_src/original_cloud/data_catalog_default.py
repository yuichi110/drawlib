# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original concept icon: data_catalog."""

from drawlib.canvas import save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Style
from drawlib.utils import Gcp, Icon

Icon.setup()

w = Icon.ORIG_STROKE

# 1. Three index tabs sticking out on the right edge (y=66, 50, 34)
tabs = [
    (66.0, Icon.PASTEL_BLUE),
    (50.0, Icon.PASTEL_GREEN),
    (34.0, Icon.PASTEL_BLUE),
]
for ty, tcol in tabs:
    rectangle(
        (74.5, ty),
        width=15.0,
        height=11.0,
        style=Icon.fill_style(tcol, border_color=Icon.DARK, border_units=w, shape_r=3.0),
    )

# 2. Structured catalog binder/book cover at (46, 50), width=54, height=68
book_cx, book_cy = 46.0, 50.0
book_w, book_h = 54.0, 68.0
book_r = 5.0
x_left = book_cx - book_w / 2.0
y_bot = book_cy - book_h / 2.0
y_top = book_cy + book_h / 2.0
spine_w = 12.0
x_spine = x_left + spine_w

rectangle(
    (book_cx, book_cy),
    width=book_w,
    height=book_h,
    style=Icon.fill_style(Icon.WHITE, shape_r=book_r),
)

Gcp.draw_rounded_corner_block(
    x_left,
    y_bot,
    x_spine,
    y_top,
    r=book_r,
    round_tl=True,
    round_bl=True,
    color=Icon.PASTEL_BLUE,
)

Icon.draw_round_segment((x_spine, y_bot), (x_spine, y_top), width_units=w, color=Icon.DARK)

rectangle(
    (book_cx, book_cy),
    width=book_w,
    height=book_h,
    style=Style(
        shape_fill_color=Colors.Transparent,
        shape_line_color=Icon.DARK,
        shape_line_width=Icon.pt(w),
        shape_line_style="solid",
        shape_r=book_r,
    ),
)

# 3. Metadata lines inside the catalog cover
for ym, x_end in ((72.0, 64.0), (63.5, 60.0), (26.0, 48.0)):
    Icon.draw_round_segment((38.0, ym), (x_end, ym), width_units=2.0, color=Icon.DARK)

# 4. Magnifying glass loupe at (52, 43) inspecting metadata lines
lens_xy = (51.5, 43.5)
p_handle_start = (59.5, 35.5)
p_handle_end = (69.0, 26.0)
Icon.draw_capsule(p_handle_start, p_handle_end, width_units=7.8, color=Icon.DARK)
Icon.draw_capsule(p_handle_start, p_handle_end, width_units=7.8 - 2.0 * w, color=Icon.PASTEL_GREEN)

circle(
    lens_xy,
    radius=13.0,
    style=Icon.fill_style(Icon.PASTEL_GREEN, border_color=Icon.DARK, border_units=w),
)
circle(
    lens_xy,
    radius=8.0,
    style=Icon.fill_style(Icon.WHITE, border_color=Icon.DARK, border_units=2.0),
)
rectangle(
    lens_xy,
    width=7.5,
    height=4.5,
    style=Icon.fill_style(Icon.PASTEL_BLUE_LIGHT, border_color=Icon.DARK, border_units=1.8, shape_r=1.2),
)

save()
