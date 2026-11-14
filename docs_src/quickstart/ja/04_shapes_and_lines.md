# 4. 基本図形・接続線・幾何計算ヘルパー

複数ノードの全体配置を自動化する高レベル描画エンジン（`ArchitectureDiagram`・`SmartArts`・`Charts`）に対し、`drawlib.shapes`・`drawlib.lines`・`drawlib.math` はカスタムバッジや吹き出し、3D コンテナ、滑らかな曲線コネクタをミリ単位の精度で自在に制御するためのベクター描画プリミティブを提供します。

```drawlib align=center code=fold file=shapes_gallery_ja.png caption="図 4.1: Drawlib が提供する全 43 種の基本図形から抜粋した代表プリミティブ一覧"
from drawlib.canvas import save, setup
from drawlib.shapes import (
    bubblespeech,
    chevron,
    circle,
    cloud,
    cylinder,
    document,
    rectangle,
    regularpolygon,
)
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=144, height=68)

xs = [21.0, 55.0, 89.0, 123.0]
ys = [49.5, 18.5]
slot_style = Styles.White.patch(
    shape_r=2.0,
    shape_line_color=Colors.Gray3,
    shape_line_width=1.0,
)

for ry in ys:
    for cx in xs:
        rectangle((cx, ry), width=31.0, height=26.5, style=slot_style)

label_style = Styles.DarkBold.patch(text_size=10.0)
body_dark = Styles.DarkBold.patch(text_size=10.5)

# 1段目: 角丸矩形・中抜きリング・正多角形・シェブロン矢印
rectangle(
    (xs[0], 52.8),
    width=23.0,
    height=12.0,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text="注目カード",
    text_style=Styles.WhiteBold.patch(text_size=10.8),
)
text((xs[0], 40.2), "rectangle (shape_r)", style=label_style)

circle(
    (xs[1], 52.8),
    radius=6.8,
    hole_ratio=0.48,
    style=Styles.PrimaryNeutral,
)
text((xs[1], 40.2), "circle (hole_ratio)", style=label_style)

regularpolygon(
    (xs[2], 52.8),
    6,
    7.2,
    style=Styles.SecondaryNeutral.patch(shape_r=0.9),
    text="六角形",
    text_style=body_dark,
)
text((xs[2], 40.2), "regularpolygon", style=label_style)

chevron(
    (xs[3], 52.8),
    width=20.5,
    height=11.0,
    corner_angle=48,
    style=Styles.Neutral,
    text="工程 1",
    text_style=body_dark,
)
text((xs[3], 40.2), "chevron", style=label_style)

# 2段目: 円柱ストレージ・クラウド境界・吹き出し・積層ドキュメント
cylinder(
    (xs[0], 22.0),
    width=18.5,
    height=13.0,
    disks=1,
    style=Styles.PrimaryNeutral,
    text="永続DB",
    text_style=Styles.DarkBold.patch(text_size=10.2, xy_abs_shift=(0, -1.5)),
)
text((xs[0], 9.2), "cylinder", style=label_style)

cloud(
    (xs[1], 22.0),
    width=23.5,
    height=13.5,
    style=Styles.Neutral,
    text="VPC 境界",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
text((xs[1], 9.2), "cloud", style=label_style)

bubblespeech(
    (xs[2] - 10.5, 19.2),
    width=21.0,
    height=9.5,
    tail_edge="bottom",
    tail_start_ratio=0.32,
    tail_vertex_xy=(85.0, 14.5),
    tail_end_ratio=0.55,
    style=Styles.SecondaryNeutral,
    text="応答 < 5ms",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((xs[2], 9.2), "bubblespeech", style=label_style)

document(
    (xs[3], 22.0),
    width=19.5,
    height=13.0,
    stacked=2,
    style=Styles.Neutral,
    text="設計仕様",
    text_style=Styles.DarkBold.patch(text_size=10.2, xy_abs_shift=(0, 0.8)),
)
text((xs[3], 9.2), "document", style=label_style)

save()
```

---

## 4.1 `drawlib.shapes` が提供する全 43 種の基本図形

`drawlib.shapes` は用途別に整理された **6 ファミリー・全 43 種のベクター図形関数**を提供します。すべての図形関数はキーワード専用の必須引数 `*, style: Style` を受け取り、座標ジオメトリと視覚スタイルを明確に分離します。

| ファミリー | 数 | `drawlib.shapes` の関数名 | 主なエンジニアリング用途 |
| :--- | :---: | :--- | :--- |
| **基本図形 (Basic)** | 6 | `rectangle`, `circle`, `ellipse`, `arc`, `fan`, `wedge` | サービスカード（`rectangle` + `shape_r`）、ノード、ドーナツ／リング（`circle` の `hole_ratio` や `wedge` の `width`）、扇形 |
| **多角形・自由パス (Polygons)** | 9 | `triangle`, `rhombus`, `parallelogram`, `trapezoid`, `regularpolygon`, `star`, `plaque`, `polygon`, `shape` | 条件分岐（`rhombus`）・入出力（`parallelogram`）、五角形／六角形／八角形（`regularpolygon(xy, n, r)`）、任意の中抜き多角形（`polygon` + `holes`） |
| **ブロック矢印・シェブロン (Arrows)** | 6 | `arrow`, `arrow_polyline`, `arrow_arc`, `arrow_l`, `arrow_u`, `chevron` | フェーズ見出し（`chevron`）、片方向／双方向ブロック矢印（`arrow(..., head="<->")`）、L 字・U 字ターン矢印 |
| **3D コンテナ・境界 (Containers)** | 6 | `cylinder`, `cube`, `document`, `funnel`, `cloud`, `brace` | データベース（`cylinder` の `disks=2`）、3D ノード（`cube`）、波形／折り返し文書（`document`）、クラウド境界、波括弧（`brace`） |
| **バッジ・吹き出し (Badges)** | 8 | `bubblespeech`, `ribbon`, `shield`, `tag`, `pin`, `checkmark`, `forbidden`, `explosion` | 注釈コールアウト（`bubblespeech`）、セキュリティ盾（`shield`）、リリースタグ（`tag`・`ribbon`）、位置ピン（`pin`）、合否ステータス |
| **記号・フロー演算子 (Symbols)** | 8 | `clock`, `face`, `gear`, `heart`, `lightning`, `math_symbol`, `moon`, `sun` | スケジューラ／遅延（`clock`）、ワーカー処理（`gear`）、十字／四則演算記号（`math_symbol`）、イベント発火（`lightning`） |

システム構成図や業務フローチャートで頻出する標準記号も、これらのプリミティブにそのまま対応します（分岐判定は `rhombus`、データ入出力は `parallelogram`、帳票・仕様書は `document`、永続ストレージは `cylinder`、処理ステップは角丸 `rectangle`）。大規模なフロー図は `drawlib.diagrams.flow.FlowDiagram` で自動レイアウトすることも可能です。

---

## 4.2 中心アンカー `(cx, cy)`・インラインテキスト・角丸・回転

HTML/DOM の左上基準やチャートの左下基準とは異なり、**`drawlib.shapes` の平面図形は幾何学的な中心座標 `xy = (cx, cy)` をアンカーとします**（始点・頂点列を指定する `arrow(xy1, xy2, ...)`・`arrow_polyline(xys, ...)`・`polygon(xys, ...)` および吹き出し本体の左下 `(x0, y0)` を指定する `bubblespeech(xy, ...)` が例外です）。幅や高さの半分を引き算する必要がなく、共通の `y = 20` を指定するだけで異種図形の中心軸がピタリと揃います。

さらに以下の 3 つの仕組みにより、ボイラープレートのない簡潔な記述が可能です。

- **図形内蔵のインラインラベル（`text` & `text_style`）**: 43 種中 39 種の図形が `text="..."` と `text_style=...` を直接受け取るため、別途 `text()` を呼び出す手間が省けます。`pin` や `gear` などの小アイコン下にラベルを添える際は `text_style=Styles.DarkBold.patch(xy_abs_shift=(0, -12))` が便利です。
- **滑らかな角丸フィレット（`shape_r`）**: `style.patch(shape_r=2.5)` を指定すると、`rectangle`・`triangle`・`rhombus`・`parallelogram`・`trapezoid`・`regularpolygon`・`star`・`polygon` の頂点が二次ベジェ曲線で滑らかに丸められます。
- **反時計回りの回転（`angle`）と中抜き（`hole_ratio`）**: `style.patch(angle=30)` で中心 `(cx, cy)` まわりに反時計回りで回転でき（文字を水平に保つには `text_style` 側で `angle=0` を上書き）、`hole_ratio=0.5` で背景を透過させたドーナツ状のリングを切り抜けます。

```python
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle, regularpolygon
from drawlib.styles import Styles

setup(width=120, height=40)

# すべて y=20 の中心アンカーで一列に整列し、テキスト・角丸・回転を宣言的に適用
rectangle(
    (25, 20),
    width=30,
    height=16,
    style=Styles.PrimaryFlat.patch(shape_r=2.5),
    text="入口GW",
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)
regularpolygon(
    (65, 20),
    6,
    10.0,
    style=Styles.PrimaryNeutral.patch(angle=15, shape_r=1.0),
    text="ルーター",
    text_style=Styles.DarkBold.patch(text_size=10.5, angle=0),
)
circle(
    (100, 20),
    radius=9.5,
    hole_ratio=0.5,
    style=Styles.Neutral,
    text="50%",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

save()
```

---

## 4.3 ベクター接続線（`drawlib.lines`）と幾何計算（`drawlib.math`）

配置した図形同士を美しく結ぶため、`drawlib.lines` は多彩な 1 次元ストローク接続線を提供し、`drawlib.math` は三角関数の手計算を不要にする幾何計算ヘルパーを提供します。

- **直線・折れ線・角丸ルーティング（`line`, `lines`, `lines_curved`）**: `line(xy1, xy2, *, style, arrow_head="->")` は 2 点間の直線、`lines(xys, ...)` は直角マンハッタン折れ線、`lines_curved(xys, r=3.5, ...)` は折れ線の各頂点を半径 `r` で自動的に丸めたフィレット経路を描画します（$r < \frac{1}{2}\min \|P_{i+1} - P_i\|$ を満たす値を指定）。すべての線関数で `arrow_head`（`""`, `"-"`, `"->"`, `"<-"`, `"<->"`）を利用できます。
- **円弧スプライン・ベジェ曲線（`line_curved`, `line_bezier1`, `line_bezier2`, `lines_bezier`, `line_arc`）**: `line_curved(xy1, xy2, bend=0.22, ...)` は進行方向に対して左（`bend > 0`）または右（`bend < 0`）へ緩やかな弧を描き、リクエスト／レスポンスの往復表現に最適です。`lines_bezier(xy, path_points, ...)` は直線 `(x, y)`・二次ベジェ `(cp, end)`・三次ベジェ `(cp1, cp2, end)` を 1 本のパスに自在に連結できます。
- **座標補間・放射配置ヘルパー（`drawlib.math`）**:
  - `get_intermediate_point(xy1, xy2)` & `get_intermediate_points(xy1, xy2, num=3)`: 線分上の等間隔ウェイポイント座標を算出します（折れ線全体の弧長に沿う `get_intermediate_path_points(xys, num=...)` も完備）。
  - `rotate_point(xy, angle, center)` & `get_point_on_ellipse(center, width, height, angle)`: `sin` / `cos` を手書きせずに放射状ノード配置や楕円外周上の接続点を正確に求められます。
  - `get_angle(xy1, xy2)`・`get_distance(xy1, xy2)`・`get_center_and_size(xys)`・`compute_orthogonal_path(...)`: 傾斜角・距離の計測やクラスタ外枠の自動算出、直交経路の自動生成を担います。

```drawlib align=center code=fold file=lines_and_math_ja.png caption="図 4.2: ベクター接続線（line・lines_curved・line_curved・lines_bezier）と幾何補間ヘルパー"
from drawlib.canvas import save, setup
from drawlib.lines import line, line_curved, lines_bezier, lines_curved
from drawlib.math import get_intermediate_points, rotate_point
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=68)

hdr = Styles.DarkBold.patch(text_size=10.5, halign="left")
note = Styles.Dark.patch(text_size=10.0)
node_light = Styles.White.patch(shape_r=1.8)
node_sec = Styles.SecondaryNeutral.patch(shape_r=1.8)
lbl_dark = Styles.DarkBold.patch(text_size=10.2)

# ゆとりある 4 分割ニュートラルパネル
rectangle((37.5, 49.5), width=64.0, height=26.5, style=Styles.PrimaryNeutral.patch(shape_r=2.2))
rectangle((106.5, 49.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((37.5, 18.5), width=64.0, height=26.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((106.5, 18.5), width=64.0, height=26.5, style=Styles.SecondaryNeutral.patch(shape_r=2.2))

# パネル 1: 双方向直線 "<->" + get_intermediate_points()
text((9.0, 59.0), '1. line("<->") + get_intermediate_points()', style=hdr)
rectangle(
    (16.0, 48.0),
    width=12.5,
    height=8.2,
    style=Styles.PrimaryFlat.patch(shape_r=1.8),
    text="送信",
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)
rectangle((59.0, 48.0), width=12.5, height=8.2, style=node_light, text="受信", text_style=lbl_dark)
line((22.5, 48.0), (52.5, 48.0), arrow_head="<->", style=Styles.DarkBold)
for pt in get_intermediate_points((22.5, 48.0), (52.5, 48.0), num=3):
    circle(pt, radius=1.3, style=Styles.AccentFlat)
text((37.5, 39.8), "num=3 の等間隔補間点", style=note)

# パネル 2: lines_curved(r=3.5) による角丸マンハッタン経路
text((78.0, 59.0), '2. lines_curved(xys, r=3.5, arrow_head="->")', style=hdr)
rectangle((85.5, 51.8), width=14.0, height=7.8, style=node_light, text="受付GW", text_style=lbl_dark)
rectangle((127.5, 42.2), width=14.0, height=7.8, style=node_sec, text="処理系", text_style=lbl_dark)
route = [(92.5, 51.8), (106.5, 51.8), (106.5, 42.2), (120.5, 42.2)]
lines_curved(route, r=3.5, arrow_head="->", style=Styles.DarkBold)
text((91.5, 41.2), "r=3.5 の角丸フィレット", style=note)

# パネル 3: line_curved(bend=...) による往復円弧スプライン
text((9.0, 28.0), "3. line_curved(bend=-0.22) による往復経路", style=hdr)
rectangle((16.0, 16.0), width=13.0, height=8.2, style=node_light, text="アプリ", text_style=lbl_dark)
rectangle((59.0, 16.0), width=13.0, height=8.2, style=node_sec, text="キャッシュ", text_style=lbl_dark)
line_curved((22.8, 18.2), (52.2, 18.2), bend=-0.22, arrow_head="->", style=Styles.PrimaryBold)
line_curved((52.2, 13.8), (22.8, 13.8), bend=-0.22, arrow_head="->", style=Styles.DarkBold)
text((37.5, 16.0), "bend = -0.22", style=note)

# パネル 4: lines_bezier() の S 字曲線 + rotate_point() の放射配置
text((78.0, 28.0), "4. lines_bezier() + rotate_point()", style=hdr)
rectangle((85.5, 20.8), width=13.5, height=7.6, style=node_light, text="イベント", text_style=lbl_dark)
hub = (125.5, 16.0)
circle(hub, radius=4.8, style=Styles.White, text="ハブ", text_style=lbl_dark)
for deg in [35, 145, 270]:
    sat = rotate_point((hub[0] + 7.2, hub[1]), deg, center=hub)
    circle(sat, radius=1.2, style=Styles.PrimaryFlat)
lines_bezier(
    (92.5, 20.8),
    [((107.0, 20.8), (106.0, 16.0), (120.4, 16.0))],
    arrow_head="->",
    style=Styles.DarkBold,
)
text((92.0, 10.2), "三次ベジェ S 字曲線", style=note)

save()
```
