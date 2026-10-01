# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

from drawlib.canvas import save, setup
from drawlib.fonts import FontFile
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=100, height=50, color=Colors.Canvas)
text(
    (50, 25),
    "Hello Drawlib!",
    style=Styles.Primary.patch(
        text_size=36,
        text_font=FontFile("../_assets/avenger/regular.ttf"),
    ),
)
save()
