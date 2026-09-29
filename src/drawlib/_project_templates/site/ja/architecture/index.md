# システムアーキテクチャ

システムの内部構成とコンポーネント間の連携について説明します。

## コンポーネント構成

```drawlib
setup(width=120, height=60)

rectangle((30, 40), width=35, height=20, style=Styles.blue_flat, text="フロントエンド (UI)", textstyle=Styles.white_bold)
rectangle((30, 15), width=35, height=20, style=Styles.green_flat, text="認証サービス", textstyle=Styles.white_bold)
rectangle((90, 27.5), width=35, height=40, style=Styles.purple_flat, text="コアバックエンド", textstyle=Styles.white_bold)

line((47.5, 40), (72.5, 35), arrowhead="->", style=Styles.bold)
line((47.5, 15), (72.5, 20), arrowhead="->", style=Styles.bold)
```
