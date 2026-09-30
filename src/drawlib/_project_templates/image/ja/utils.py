# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib ユーザーユーティリティ関数および定数定義ファイル。"""

from __future__ import annotations

from typing import Literal

from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Style, Styles
from drawlib.text import text

# このファイルでは、プロジェクト全体で再利用する作図ヘルパー関数、マクロコンポーネント、
# またはプロジェクト固有の定数を定義します。
#
# ここで定義したトップレベルの関数・クラス・変数は、作図コード内から
# `drawlib.utils` 経由で自動的に利用できます。


def service_card(
    xy: tuple[float, float],
    title: str,
    subtitle: str = "",
    width: float = 24.0,
    height: float = 16.0,
    style: Style = Styles.primary_flat,
) -> None:
    """タイトルと任意のサブタイトルを持つ標準サービスカードを描画します。

    Args:
        xy: 中心座標 (x, y)。
        title: サービス名（例: 'API Gateway'）。
        subtitle: 補足説明や技術スタック（例: 'FastAPI / :8000'）。
        width: カードの幅。
        height: カードの高さ。
        style: カードの形状スタイル。
    """
    x, y = xy
    rectangle(xy, width=width, height=height, r=2.0, style=style)
    if subtitle:
        text((x, y + 2.5), title, style=Styles.white_bold.patch(text_size=11))
        text((x, y - 3.5), subtitle, style=Styles.white.patch(text_size=8))
    else:
        text((x, y), title, style=Styles.white_bold)


def connect(
    start: tuple[float, float],
    end: tuple[float, float],
    label: str = "",
    arrowhead: Literal["", "->", "<-", "<->"] = "->",
    style: Style = Styles.bold,
) -> None:
    """2点間を結ぶ接続線と、任意の中央プロトコルラベルを描画します。

    Args:
        start: 始点座標 (x, y)。
        end: 終点座標 (x, y)。
        label: プロトコルや説明テキスト（例: 'HTTPS', 'gRPC'）。
        arrowhead: 矢印スタイル ('->', '<->', '-')。
        style: 線のスタイル。
    """
    line(start, end, arrowhead=arrowhead, style=style)
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        text((mid_x, mid_y + 3.0), label, style=Styles.primary.patch(text_size=9))
