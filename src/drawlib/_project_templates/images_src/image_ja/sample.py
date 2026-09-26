# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""サンプル図面スクリプト。"""

from drawlib.canvas import save, setup
from drawlib.config import styles
from drawlib.lines import line
from drawlib.shapes import rectangle

setup(width=100, height=50)

rectangle((20, 25), width=25, height=18, style=styles.blue_flat, text="クライアント", textstyle=styles.white_bold)
rectangle((50, 25), width=25, height=18, style=styles.green_flat, text="サーバー", textstyle=styles.white_bold)
rectangle((80, 25), width=25, height=18, style=styles.red_flat, text="データベース", textstyle=styles.white_bold)

line((32.5, 25), (37.5, 25), arrowhead="->", style=styles.bold)
line((62.5, 25), (67.5, 25), arrowhead="->", style=styles.bold)

save()
