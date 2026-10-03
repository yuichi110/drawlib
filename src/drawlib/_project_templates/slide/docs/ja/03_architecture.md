---
layout: default
header: "アーキテクチャ"
---

::: box (80, 140) (740, 840) font:22px
# Pythonコードで描くマイクロサービス

- **宣言的Python**: 変更履歴がGitで管理できるクリーンなコード
- **ネイティブSVG**: 拡大してもクリア、Ctrl+Fによる文字検索に対応
- **インタラクティブなスライド**: 全画面表示、ショートカット、一覧モーダル
:::

```drawlib (860, 140) (980, 840) z:5 file:microservices.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

clear()
setup(width=100, height=60)
rectangle((25, 30), width=30, height=20, style=Styles.PrimaryFlat, text="Client SPA", text_style=Styles.WhiteBold)
rectangle((75, 30), width=30, height=20, style=Styles.SecondaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
line((40, 30), (60, 30), arrow_head="->", style=Styles.PrimaryBold)
save()
```
