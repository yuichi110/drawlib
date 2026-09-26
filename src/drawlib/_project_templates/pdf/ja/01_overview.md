# 第1章 プロジェクト概要

本ドキュメントはシステム全体の概要および設計仕様をまとめたものです。

## システムアーキテクチャ

```drawlib
setup(width=100, height=50)

rectangle((20, 25), width=25, height=18, style=styles.blue_flat, text="クライアント", textstyle=styles.white_bold)
rectangle((50, 25), width=25, height=18, style=styles.green_flat, text="サーバー", textstyle=styles.white_bold)
rectangle((80, 25), width=25, height=18, style=styles.red_flat, text="データベース", textstyle=styles.white_bold)

line((32.5, 25), (37.5, 25), arrowhead="->", style=styles.bold)
line((62.5, 25), (67.5, 25), arrowhead="->", style=styles.bold)
```
