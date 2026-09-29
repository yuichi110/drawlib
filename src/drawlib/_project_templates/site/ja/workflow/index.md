# 業務ワークフロー

リクエストの処理ライフサイクルについて説明します。

## 処理フロー

```drawlib
setup(width=100, height=40)

circle((20, 20), radius=10, style=Styles.blue_flat, text="開始", textstyle=Styles.white_bold)
rectangle((50, 20), width=24, height=16, style=Styles.green_flat, text="処理実行", textstyle=Styles.white_bold)
circle((80, 20), radius=10, style=Styles.red_flat, text="完了", textstyle=Styles.white_bold)

line((30, 20), (38, 20), arrowhead="->", style=Styles.bold)
line((62, 20), (70, 20), arrowhead="->", style=Styles.bold)
```
