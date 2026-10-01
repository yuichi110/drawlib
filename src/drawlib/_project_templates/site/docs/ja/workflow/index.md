# 業務ワークフロー

処理の実行ライフサイクルについて解説します。

## 処理フロー

```drawlib 600px center caption:"処理ライフサイクルフロー"
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=100, height=40)

# 処理ステージ
circle((18, 20), radius=9, style=Styles.primary_flat, text="開始", textstyle=Styles.white_bold)
service_card((50, 20), title="処理実行", subtitle="ワーカージョブ", width=26, height=16, style=Styles.accent_flat)
circle((82, 20), radius=9, style=Styles.secondary_flat, text="完了", textstyle=Styles.white_bold)

# 状態遷移
connect((27, 20), (37, 20))
connect((63, 20), (73, 20))
```
