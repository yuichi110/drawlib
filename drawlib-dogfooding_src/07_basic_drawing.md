# 第7章: ベーシックな描画（Primitives）

Drawlib の基本描画レイヤー（`shapes`, `lines`, `text`, `icons`）を使用すると、任意の幾何学図形や自由なレイアウトを自在に構築できます。

## 7.1 キャンバスの座標系

Drawlib は、数学的な **直交座標系（デカルト座標系）** を採用しています:
- **原点 `(0, 0)`**: キャンバスの **左下** です（画面描画系の左上原点とは異なります）。
- **サイズ指定**: `setup(width=W, height=H)` でキャンバスサイズを定義します。

## 7.2 基本図形（Shapes）と矢印（Lines）

22 種類の図形プリミティブ（四角形、円、楕円、扇形、ドーナツ、矢印ポリゴン、星型など）が用意されています。

```drawlib 600px center file:fig_basic_drawing.png caption:"図 7.1: 基本図形・矢印・アイコンを組み合わせたサービス連携図"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=105, height=42)

# クライアントノード
rectangle((20, 21), width=24, height=18, r=1.5, style=Styles.SecondaryFlat, text="Client App", text_style=Styles.WhiteBold)
phosphor.device_mobile(xy=(20, 34), width=6, style=Styles.Secondary)

# API Gateway ノード
rectangle((55, 21), width=26, height=20, r=1.5, style=Styles.PrimaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
phosphor.cloud(xy=(55, 35), width=6, style=Styles.Primary)

# データベースノード
circle((88, 21), radius=9, style=Styles.AccentFlat, text="DB Cluster", text_style=Styles.WhiteBold)
phosphor.database(xy=(88, 34), width=6, style=Styles.Accent)

# 接続線と矢印
line((32, 21), (42, 21), arrowhead="->", style=Styles.PrimaryBold)
text((37, 24), "HTTPS", style=Styles.Primary, size=9)

line((68, 21), (79, 21), arrowhead="->", style=Styles.PrimaryBold)
text((73.5, 24), "SQL", style=Styles.Accent, size=9)
```

## 7.3 主要な描画関数一覧

- **`rectangle(xy, width, height, r=0, style=...)`**: 角丸対応の長方形
- **`circle(xy, radius, style=...)`**: 円
- **`line(start_xy, end_xy, arrowhead="->", style=...)`**: 矢印付き直線
- **`line_curved(start_xy, end_xy, bend=0.2, ...)`**: 滑らかな曲線
- **`text(xy, text="...", style=..., size=12)`**: スタイル付きテキスト
- **`phosphor.<icon_name>(xy, width, style=...)`**: Phosphor ベクターアイコン
