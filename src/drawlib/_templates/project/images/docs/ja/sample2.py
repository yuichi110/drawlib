# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""utils.py の共通ヘルパーと画像アセットを活用した構成図スクリプト。"""

from __future__ import annotations

from drawlib.canvas import save, setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

# キャンバス設定: 幅 110 x 高さ 52
setup(width=110, height=52)

# utils.py の共通ヘルパー関数によるサービス描画
service_card((20, 24), title="Web クライアント", subtitle="Browser / App")
service_card((55, 24), title="Linux サーバー", subtitle="Ubuntu / Nginx", style=Styles.AccentFlat)
service_card((90, 24), title="データベース", subtitle="PostgreSQL", style=Styles.SecondaryFlat)

# プロトコルラベル付き接続線
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# _assets/ 配下のローカル画像アセットの埋め込み
image((55, 41), width=8, image="_assets/linux.png")

# 描画したキャンバス画像を保存
save()
