# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save, setup
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.icons import phosphor
from drawlib.images import get_dimage_from_code, image
from drawlib.preset_colors import CssColors
from drawlib.shapes import arrow
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(height=60, dpi=200, color=Colors.Canvas)
INNER_CODE = """from drawlib.canvas import save
from drawlib.shapes import circle
from drawlib.styles import Colors, Styles

circle(
    xy=(50, 50),
    radius=30,
    style=Styles.PrimaryDashed.patch(
        shape_line_color=Colors.Blue,
        shape_line_width=5,
        shape_fill_color=Colors.Teal,
    ),
)
save()
"""


def upper():
    y = 52
    text(
        xy=(20, y),
        text="Drawlib",
        style=Styles.Primary.patch(text_size=28, text_font=FontRoboto.ROBOTO_BOLD),
    )
    phosphor.heart(
        xy=(38, y),
        width=7,
        style=Styles.Primary.patch(icon_color=CssColors.Pink, icon_style="fill"),
    )
    text(
        xy=(70, y),
        text="Illustration as Code",
        style=Styles.Primary.patch(text_size=28, text_font=FontRoboto.ROBOTO_BOLD),
    )


def middle():
    image_y = 12
    arrow_y = 28
    style = Styles.Primary.patch(image_border_width=1)

    sc_styles = SourceCodeStyles.get("default", font_lang="en", font=FontSourceCode.ROBOTO_MONO, text_size=7.5)
    SourceCode.draw(xy=(5, 44), width=40, code=INNER_CODE, styles=sc_styles)

    arrow((50, arrow_y), (60, arrow_y), tail_width=5, head_width=10, head_length=5, head="->", style=Styles.PrimarySolid)

    inner_dimage = get_dimage_from_code(INNER_CODE)
    image((64.25, image_y), width=31.5, image=inner_dimage, style=style)


def lower():
    y = 6
    style = Styles.Primary.patch(text_size=20, text_font=FontRoboto.ROBOTO_REGULAR)
    phosphor.file_py(xy=(15, y), width=5, style=Styles.Primary)
    text((28, y), "Python Code", style=style)
    text((55, y), "to", style=style)
    phosphor.file_image(xy=(72, y), width=5, style=Styles.Primary)
    text((83, y), "Illustration", style=style)


upper()
middle()
lower()

save()
