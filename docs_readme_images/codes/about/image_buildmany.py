# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import config, save
from drawlib.colors import Colors, ColorsThemeEssentials
from drawlib.fonts import FontRoboto
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.preset_styles import default_styles
from drawlib.shapes import arrow, rectangle
from drawlib.text import text

ps = default_styles
config(height=60)

rect_width = 20
rect_height = 38

line_thin = ps.primary.patch(line_width=0.5)
ts_left = ps.primary.patch(text_size=12, text_halign="left")
ts_left_red = ps.primary.patch(text_size=12, text_halign="left", text_color=ColorsThemeEssentials.Red)
icon_thin = ps.primary.patch(icon_style="thin")
icon_thin_red = ps.primary.patch(icon_style="thin", icon_color=ColorsThemeEssentials.Red)

tscenter16 = ps.primary.patch(text_halign="center", text_size=16)
tscenter16r = ps.primary.patch(text_halign="center", text_size=16, text_color=ColorsThemeEssentials.Red)


def left():
    text((15, 54), "Drawlib's\nDocument Source", style=tscenter16)

    rectangle(
        xy=(15, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style=ps.dashed,
    )

    x = 8
    phosphor.folder((x, 45), width=3, style=icon_thin)
    text((x + 2.5, 45), "docs", style=ts_left)
    line((x, 43), (x, 13), style=line_thin)

    line((x, 42), (x + 1, 42), style=line_thin)
    phosphor.folder((x + 3, 42), width=3, style=icon_thin)
    text((x + 5.5, 42), "commons", style=ts_left)
    line((x + 3, 40), (x + 3, 35), style=line_thin)
    phosphor.file_py((x + 6, 39), width=3, style=icon_thin_red)
    text((x + 8.5, 39), "style.py", style=ts_left_red)
    line((x + 3, 39), (x + 4, 39), style=line_thin)
    phosphor.file_py((x + 6, 36), width=3, style=icon_thin_red)
    text((x + 8.5, 36), "util.py", style=ts_left_red)
    line((x + 3, 36), (x + 4, 36), style=line_thin)

    line((x, 30), (x + 1, 30), style=line_thin)
    phosphor.folder((x + 3, 30), width=3, style=icon_thin)
    text((x + 5.5, 30), "chapter1", style=ts_left)
    line((x + 3, 28), (x + 3, 19), style=line_thin)
    phosphor.file_md((x + 6, 27), width=3, style=icon_thin)
    text((x + 8.5, 27), "doc.md", style=ts_left)
    line((x + 3, 27), (x + 4, 27), style=line_thin)
    phosphor.file_py((x + 6, 24), width=3, style=icon_thin_red)
    text((x + 8.5, 24), "img1.py", style=ts_left_red)
    line((x + 3, 24), (x + 4, 24), style=line_thin)
    phosphor.file_py((x + 6, 21), width=3, style=icon_thin_red)
    text((x + 8.5, 21), "img2.py", style=ts_left_red)
    line((x + 3, 21), (x + 4, 21), style=line_thin)

    line((x, 15), (x + 1, 15), style=line_thin)
    phosphor.folder((x + 3, 15), width=3, style=icon_thin)
    text((x + 5.5, 15), "chapter2", style=ts_left)


def center():
    text((50, 54), "Traditional\nDocument Source", style=tscenter16)
    rectangle(
        xy=(50, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style=ps.dashed,
    )

    x = 43
    phosphor.folder((x, 45), width=3, style=icon_thin)
    text((x + 2.5, 45), "docs", style=ts_left)
    line((x, 43), (x, 13), style=line_thin)

    line((x, 30), (x + 1, 30), style=line_thin)
    phosphor.folder((x + 3, 30), width=3, style=icon_thin)
    text((x + 5.5, 30), "chapter1", style=ts_left)
    line((x + 3, 28), (x + 3, 19), style=line_thin)
    phosphor.file_md((x + 6, 27), width=3, style=icon_thin)
    text((x + 8.5, 27), "doc.md", style=ts_left)
    line((x + 3, 27), (x + 4, 27), style=line_thin)
    phosphor.file_image((x + 6, 24), width=3, style=icon_thin_red)
    text((x + 8.5, 24), "img1.png", style=ts_left_red)
    line((x + 3, 24), (x + 4, 24), style=line_thin)
    phosphor.file_image((x + 6, 21), width=3, style=icon_thin_red)
    text((x + 8.5, 21), "img2.png", style=ts_left_red)
    line((x + 3, 21), (x + 4, 21), style=line_thin)

    line((x, 15), (x + 1, 15), style=line_thin)
    phosphor.folder((x + 3, 15), width=3, style=icon_thin)
    text((x + 5.5, 15), "chapter2", style=ts_left)


def right():
    text((85, 54), "Output Documents", style=tscenter16)

    rectangle(
        xy=(85, 30),
        width=rect_width,
        height=rect_height,
        r=2,
        style=ps.dashed,
    )

    phosphor.file_pdf((85, 43), width=6, style=icon_thin)
    phosphor.file_html((85, 35), width=6, style=icon_thin)
    phosphor.file_ppt((85, 27), width=6, style=icon_thin)
    phosphor.book_bookmark((85, 19), width=6, style=icon_thin)
    text((85, 14.5), text="eBook", style=tscenter16)


def bottom():
    rectangle(
        xy=(50, 5),
        width=90,
        height=6,
        r=2,
        style=ps.solid,
    )
    phosphor.github_logo((17, 5), width=5, style=icon_thin)
    text(
        (53, 5),
        "Illustration and doc text versioning with CI/CD automation",
        style=tscenter16,
    )


left()
arrow(
    (28, 35),
    (37, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style=ps.red_flat,
    text="Drawlib",
    textstyle=ps.primary.patch(
        text_size=14,
        text_color=Colors.White,
        text_font=FontRoboto.ROBOTO_BOLD,
        text_xy_shift=(-0.5, -0.1),
    ),
)
text((32, 25), "Build\nImages", style=tscenter16r)
center()
arrow(
    (63, 35),
    (72, 35),
    tail_width=3,
    head_width=6,
    head_length=3,
    style=ps.solid,
)
text((67, 25), "Build\nDocs", style=tscenter16)
right()
bottom()
save()
