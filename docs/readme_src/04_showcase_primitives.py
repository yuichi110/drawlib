# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Showcase of Drawlib primitives (Icons, Images, Lines, Shapes, Text) and semantic styles."""

from drawlib.canvas import save, setup
from drawlib.fonts import FontJapanese, FontRoboto, FontSerif
from drawlib.icons import gcp, phosphor
from drawlib.images import Dimage, image
from drawlib.lines import line, line_curved, lines, lines_curved
from drawlib.shapes import circle, ellipse, rectangle, rhombus, star
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=62, dpi=200, color=Colors.Canvas)

LABEL_X = 12
row_title_style = Styles.DarkBold.patch(text_size=14, text_font=FontRoboto.ROBOTO_BOLD)
row_card_style = Styles.MutedOutline.patch(shape_fill_color=Colors.White, shape_line_width=1.0)

# Background card rows
for ry in [52, 40, 28, 16, 5.5]:
    rectangle((60, ry), width=112, height=9.5, style=row_card_style.patch(shape_r=1.5))

# 1. Icons (Phosphor & GCP)
y_icon = 52
text((LABEL_X, y_icon), "Icons", style=row_title_style)
phosphor.rocket_launch((32, y_icon), width=6.5, style=Styles.Primary)
phosphor.shield_check((45, y_icon), width=6.5, style=Styles.Success.patch(icon_style="fill"))
phosphor.database((58, y_icon), width=6.5, style=Styles.Secondary)
phosphor.cpu((71, y_icon), width=6.5, style=Styles.Accent)
gcp.cloud_run((84, y_icon), width=6.5, style=Styles.Primary)
gcp.bigquery((97, y_icon), width=6.5, style=Styles.Success)
gcp.pubsub((109, y_icon), width=6.5, style=Styles.Secondary)

# 2. Images & Dimage Filters
y_img = 40
w_img = 6.2
text((LABEL_X, y_img), "Images", style=row_title_style)
dimg = Dimage("_assets/linux.png")
image((32, y_img), w_img, image=dimg)
image((45, y_img), w_img, image=dimg, style=Styles.Primary.patch(image_border_width=1))
image((58, y_img), w_img, image=dimg, style=Styles.Primary.patch(angle=330))
image((71, y_img), w_img, image=dimg.sepia())
image((84, y_img), w_img, image=dimg.grayscale())
image((97, y_img), w_img, image=dimg.mosaic(20))
image((109, y_img), w_img, image=dimg.mirror())

# 3. Lines & Connectors
y_line = 28
text((LABEL_X, y_line), "Lines", style=row_title_style)
line((29, y_line), (36, y_line), style=Styles.DarkBold)
line((41, y_line), (49, y_line), arrow_head="->", style=Styles.PrimaryBold)
line((54, y_line), (62, y_line), arrow_head="<->", style=Styles.SecondaryDashed)
line_curved((67, y_line - 2), (75, y_line + 2), bend=0.35, arrow_head="->", style=Styles.AccentBold)
lines([(80, y_line - 3), (84, y_line + 3), (88, y_line - 3), (92, y_line + 3)], style=Styles.WarningBold)
lines_curved(
    [(98, y_line - 3), (98, y_line + 3), (110, y_line + 3), (110, y_line - 3)],
    r=2.0,
    arrow_head="->",
    style=Styles.SuccessBold,
)

# 4. Shapes & Semantic Styles
y_shape = 16
text((LABEL_X, y_shape), "Shapes", style=row_title_style)
rectangle(
    (33, y_shape),
    width=12,
    height=6.5,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Primary",
    text_style=Styles.WhiteBold.patch(text_size=8),
)
rectangle(
    (49, y_shape),
    width=12,
    height=6.5,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="Neutral",
    text_style=Styles.DarkBold.patch(text_size=8),
)
rectangle(
    (65, y_shape),
    width=12,
    height=6.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="Secondary",
    text_style=Styles.SecondaryBold.patch(text_size=8),
)
circle((79, y_shape), radius=3.4, style=Styles.SuccessNeutral)
rhombus((91, y_shape), width=8, height=6.8, style=Styles.WarningNeutral)
star((102, y_shape), num_vertex=5, radius_ext=3.6, radius_int=1.6, style=Styles.AccentFlat)
ellipse((111, y_shape), width=6, height=4.5, style=Styles.DangerDashed)

# 5. Multilingual Typography
y_text = 5.5
text((LABEL_X, y_text), "Text", style=row_title_style)
text((37, y_text), "Roboto Bold", style=Styles.PrimaryBold.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=12))
text((64, y_text), "Serif Typography", style=Styles.Secondary.patch(text_font=FontSerif.COURIER_BOLD, text_size=12))
text(
    (96, y_text),
    "日本語テキスト対応 (CJK)",
    style=Styles.Dark.patch(text_font=FontJapanese.MPLUS1P_REGULAR, text_size=11),
)

save()
