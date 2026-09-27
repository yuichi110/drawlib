# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Drawlib ユーザー定義ユーティリティ・定数設定ファイル。"""

from __future__ import annotations

# プロジェクト共通のヘルパー関数、マクロ描画コンポーネント、定数などをここで定義します。
#
# このファイル内でトップレベルに定義された関数や変数は、
# 各図面コードから `drawlib.utils` 経由で自動的にインポート・利用できます。
#
# 例:
#
# from drawlib.shapes import rectangle
# from drawlib.styles import styles
# from drawlib.text import text
#
# PROJECT_NAME = "ドキュメントプロジェクト"
# BRAND_PRIMARY = "#1a73e8"
#
# def service_card(xy: tuple[float, float], title: str, subtitle: str = "") -> None:
#     """再利用可能なサービスカード描画コンポーネント。"""
#     x, y = xy
#     rectangle(xy, width=32, height=18, r=2, style="blue_flat")
#     text((x, y + 3), title, style="white_bold")
#     if subtitle:
#         text((x, y - 3), subtitle, style="white_light")
#
# 各図面スクリプトや Markdown 内の drawlib コードブロックでの利用例:
#     from drawlib.utils import PROJECT_NAME, service_card
#     service_card((50, 50), "認証サービス")
