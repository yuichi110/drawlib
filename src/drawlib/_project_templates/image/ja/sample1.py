# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib の基本図形描画機能のみを使用したシンプルな構成図スクリプト。"""

from __future__ import annotations

from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

# キャンバス設定: 幅 100 x 高さ 45
setup(width=100, height=45)

# 基本図形描画関数を使用したサービスノード
rectangle(
    (25, 22.5),
    width=28,
    height=18,
    style=Styles.primary_flat,
    text="クライアント",
    textstyle=Styles.white_bold,
)
rectangle(
    (75, 22.5),
    width=28,
    height=18,
    style=Styles.accent_flat,
    text="バックエンド API",
    textstyle=Styles.white_bold,
)

# 矢印付き接続線
line((39, 22.5), (61, 22.5), arrowhead="->", style=Styles.bold)

# 描画したキャンバス画像を保存
save()
