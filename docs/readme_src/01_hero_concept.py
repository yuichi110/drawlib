# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Hero illustration demonstrating Python code to technical diagram generation."""

from drawlib.canvas import save, setup
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.icons import phosphor
from drawlib.images import get_dimage_from_code, image
from drawlib.shapes import arrow, rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=62, dpi=200, color=Colors.Canvas)

INNER_CODE = """from drawlib.canvas import setup, save
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=100, height=56)
rectangle((50, 28), 90, 44, r=3, style=Styles.MutedDashed)
rectangle((24, 28), 26, 20, r=2, style=Styles.Neutral,
          text="Client App")
rectangle((72, 28), 30, 20, r=2, style=Styles.PrimaryFlat,
          text="API Service", text_style=Styles.WhiteBold)
line((37, 28), (57, 28), arrow_head="->", style=Styles.DarkBold)
save()
"""

# Header banner
text(
    xy=(60, 55.5),
    text="Drawlib — Illustration & Documentation as Code",
    style=Styles.PrimaryBold.patch(text_size=18, text_font=FontRoboto.ROBOTO_BOLD),
)

# Left: Declarative Python Source Code (SourceCode.draw uses top-left anchor)
sc_styles = SourceCodeStyles.get("default", font_lang="en", font=FontSourceCode.ROBOTO_MONO, text_size=6.8)
SourceCode.draw(xy=(4, 48), width=50, code=INNER_CODE, styles=sc_styles)

# Middle: Transformation Arrow
arrow(
    (56.5, 31.5),
    (64.5, 31.5),
    tail_width=3.5,
    head_width=7.5,
    head_length=3.5,
    head="->",
    style=Styles.PrimaryFlat,
)

# Right: Rendered Output Card (image uses center anchor by default)
card_style = Styles.MutedOutline.patch(shape_fill_color=Colors.White, shape_line_width=1.2)
rectangle((91, 31.5), width=48, height=33, r=2, style=card_style)
inner_dimage = get_dimage_from_code(INNER_CODE)
image((91, 31.5), width=45, image=inner_dimage)

# Footer labels
label_style = Styles.DarkBold.patch(text_size=12, text_font=FontRoboto.ROBOTO_BOLD)
phosphor.file_py(xy=(18, 7.5), width=4.5, style=Styles.Primary)
text((31, 7.5), "Declarative Python", style=label_style)
phosphor.file_image(xy=(79, 7.5), width=4.5, style=Styles.Primary)
text((93, 7.5), "Publication Diagram", style=label_style)

save()
