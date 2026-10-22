# 第7章: ベーシックな描画（Primitives）

Drawlib の基本描画レイヤー（`shapes`, `lines`, `text`, `icons`）を使用すると、任意の幾何学図形や自由なレイアウトを自在に構築できます。

## 7.1 キャンバスの座標系とアンカー基準

Drawlib は、数学的な **直交座標系（デカルト座標系）** を採用しています:
- **原点 `(0, 0)`**: キャンバスの **左下** です（画面描画系の左上原点とは異なります）。
- **サイズ指定**: `setup(width=W, height=H)` でキャンバスサイズを定義し、描画の最後に `save()` を呼び出します。
- **中心座標アンカー `(cx, cy)`**: 基本描画プリミティブ（`shapes`, `text`, `icons`, `images`）はすべて **中心座標 `(cx, cy)`** を基準に配置します（高レベルモジュールの `smartarts`, `charts`, `diagrams` が左下 `(x0, y0)` を基準とする点と対比されます）。

## 7.2 基本図形（Shapes）と矢印（Lines）

**43 種類**の図形プリミティブ（`rectangle`, `circle`, `ellipse`, `polygon`, `star`, `donuts`, `fan`, `bubblespeech`, `cylinder`, `parallelogram`, `trapezoid`, `chevron`、およびブロック矢印 `arrow_polyline`, `arrow_l`, `arrow_u`, `arrow_arc` など）が用意されています。

```drawlib align=center file=fig_basic_drawing.png caption="図 7.1: 基本図形・矢印・アイコンを組み合わせたサービス連携図"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=105, height=44)

# クライアントノード (Neutral ベース)
rectangle(
    (20, 20),
    width=24,
    height=18,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="Client App",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
phosphor.device_mobile(xy=(20, 34), width=6, style=Styles.Secondary)

# API Gateway ノード (PrimaryFlat による主役強調)
rectangle(
    (54, 20),
    width=26,
    height=20,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="API Gateway",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
phosphor.cloud(xy=(54, 35), width=6, style=Styles.Primary)

# データベースノード (SecondaryNeutral ベース)
circle(
    (87, 20),
    radius=10,
    style=Styles.SecondaryNeutral,
    text="DB Cluster",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
phosphor.database(xy=(87, 35), width=6, style=Styles.Secondary)

# 接続線と矢印
line((32, 20), (41, 20), arrow_head="->", style=Styles.DarkBold)
text((36.5, 23.5), "HTTPS", style=Styles.DarkBold.patch(text_size=10.5))

line((67, 20), (77, 20), arrow_head="->", style=Styles.DarkBold)
text((72, 23.5), "SQL", style=Styles.DarkBold.patch(text_size=10.5))

save()
```

## 7.3 主要な描画関数一覧

- **`rectangle(xy, width, height, style=...)`**: 長方形（`style.shape_r` で角丸対応）
- **`circle(xy, radius, style=...)`**: 円
- **`line(start_xy, end_xy, arrow_head="->", style=...)`**: 矢印付き直線
- **`line_curved(start_xy, end_xy, bend=0.2, ...)`**: 滑らかな曲線
- **`text(xy, text="...", style=...)`**: スタイル付きテキスト
- **`phosphor.<icon_name>(xy, width, style=...)`**: Phosphor ベクターアイコン（`drawlib.icons.phosphor`）
- **`fontawesome.<icon_name>(xy, width, style=...)`**: FontAwesome アイコン（`drawlib.icons.fontawesome`）
- **`gcp.<icon_name>(xy, width, ...)`**: Google Cloud 公式アーキテクチャアイコン（`drawlib.icons.gcp`）
