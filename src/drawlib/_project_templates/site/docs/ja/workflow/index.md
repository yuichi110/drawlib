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
circle((18, 20), radius=9, style=Styles.PrimaryFlat, text="開始", textstyle=Styles.WhiteBold)
service_card((50, 20), title="処理実行", subtitle="ワーカージョブ", width=26, height=16, style=Styles.AccentFlat)
circle((82, 20), radius=9, style=Styles.SecondaryFlat, text="完了", textstyle=Styles.WhiteBold)

# 状態遷移
connect((27, 20), (37, 20))
connect((63, 20), (73, 20))
```
