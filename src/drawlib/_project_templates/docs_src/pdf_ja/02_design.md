# 第2章 詳細設計

各コンポーネントの詳細設計および処理フローです。

```drawlib
setup(width=100, height=40)

circle((20, 20), radius=10, style=styles.blue_flat, text="受信", textstyle=styles.white_bold)
rectangle((50, 20), width=24, height=16, style=styles.green_flat, text="解析・変換", textstyle=styles.white_bold)
circle((80, 20), radius=10, style=styles.red_flat, text="保存", textstyle=styles.white_bold)

line((30, 20), (38, 20), arrowhead="->", style=styles.bold)
line((62, 20), (70, 20), arrowhead="->", style=styles.bold)
```
