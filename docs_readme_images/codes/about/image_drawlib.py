# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.icons import icon_phosphor
from drawlib.images import image
from drawlib.shapes import arrow
from drawlib.smartarts import SourceCode
from drawlib.text import text
from drawlib.types import IconStyle, ImageStyle, TextStyle

config(height=60, dpi=200)


def upper():
    y = 52
    text(
        xy=(20, y),
        text="Drawlib",
        style=TextStyle(text_size=28, text_font=FontRoboto.ROBOTO_BOLD),
    )
    icon_phosphor.heart(
        xy=(38, y),
        width=7,
        style=IconStyle(text_color=Colors140.Pink, icon_style="fill"),
    )
    text(
        xy=(70, y),
        text="Illustration as Code",
        style=TextStyle(text_size=28, text_font=FontRoboto.ROBOTO_BOLD),
    )


def middle():
    image_y = 12
    arrow_y = 28
    style = ImageStyle(line_width=1, text_valign="bottom")

    sc = SourceCode(style="default", font=FontSourceCode.ROBOTO_MONO)
    text_content = SourceCode.get_text("inside.py")
    sc.draw((25, image_y), width=40, code=text_content, style=style)

    arrow((50, arrow_y), (60, arrow_y), tail_width=5, head_width=10, head_length=5, head="->")

    image((80, image_y), width=31.5, image="inside.png", style=style)


def lower():
    y = 6
    style = TextStyle(text_size=20, text_font=FontRoboto.ROBOTO_REGULAR)
    icon_phosphor.file_py(xy=(15, y), width=5)
    text((28, y), "Python Code", style=style)
    text((55, y), "to", style=style)
    icon_phosphor.file_image(xy=(72, y), width=5)
    text((83, y), "Illustration", style=style)


upper()
middle()
lower()

save()
