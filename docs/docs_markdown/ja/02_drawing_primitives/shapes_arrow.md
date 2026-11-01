# ブロック矢印・シェブロン

1 次元の線コネクタ（`drawlib.lines`）に加え、`drawlib.shapes` の**ブロック矢印・シェブロン（Block Arrows & Chevrons）**カテゴリは、**6 種類の閉じた 2D 多角形矢印プリミティブ**を提供します。具体的には、2 点間を結ぶ直線ブロック矢印（`arrow`）、連続工程を表すプロセスシェブロン（`chevron`）、`90°` 直角に折れ曲がる L 字矢印（`arrow_l`）、`180°` 折り返す U ターンフィードバック矢印（`arrow_u`）、円弧・楕円弧の循環ブロック矢印（`arrow_arc`）、そして複数の経由点を通る折れ線ブロック矢印（`arrow_polyline`）が含まれます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_overview.png" alt="shapes_arrow_1" />
  <figcaption class="drawlib-caption">drawlib.shapes における 6 種類のブロック矢印・シェブロンプリミティブの概要</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, arrow_arc, arrow_l, arrow_polyline, arrow_u, chevron, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=124, height=62)

# Subtle background cards for 3x2 grid
for cx in (22, 62, 102):
    for cy in (45.5, 16.5):
        rectangle((cx, cy), width=36, height=25, style=Styles.Neutral.patch(shape_r=2))

lbl = Styles.DarkBold.patch(text_size=10.5)

# 1. Straight Block Arrow (Hero)
arrow(
    (9, 49.5),
    (35, 49.5),
    tail_width=5.0,
    head_width=10.5,
    head_length=7.5,
    style=Styles.PrimaryFlat,
    text="arrow",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
text((22, 37.5), "1. arrow()", style=lbl)

# 2. Chevron
chevron(
    (62, 49.5),
    width=25,
    height=11.5,
    corner_angle=60,
    style=Styles.SecondaryNeutral.patch(shape_r=1),
    text="chevron",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
text((62, 37.5), "2. chevron()", style=lbl)

# 3. L-shaped Arrow
arrow_l(
    (102, 50.5),
    width=20,
    height=12,
    tail_width=3.2,
    head_width=8,
    head_length=6,
    style=Styles.DarkBold.patch(shape_r=2.5),
)
text((102, 37.5), "3. arrow_l()", style=lbl)

# 4. U-turn Arrow
arrow_u(
    (22, 20.5),
    width=20,
    height=12,
    tail_width=3.2,
    head_width=8,
    head_length=6,
    style=Styles.DarkBold.patch(shape_r=3),
)
text((22, 8.5), "4. arrow_u()", style=lbl)

# 5. Arrow Arc (Circular flow)
arrow_arc(
    (62, 23.5),
    width=20,
    height=14,
    angle_start=180,
    angle_end=0,
    tail_width=3.2,
    head_width=8,
    head_angle=14,
    style=Styles.SecondaryNeutral,
)
text((62, 8.5), "5. arrow_arc()", style=lbl)

# 6. Multi-Point Polyline Arrow
arrow_polyline(
    [(90, 15.5), (101, 15.5), (101, 23.5), (114, 23.5)],
    tail_width=3.2,
    head_width=8,
    head_length=6,
    style=Styles.PrimaryNeutral.patch(shape_r=2),
)
text((102, 8.5), "6. arrow_polyline()", style=lbl)

save()
```

</details>



---

## 1. 基本となるジオメトリ概念

1 次元の線ストロークコネクタとは異なり、Drawlib の 6 種類のブロック矢印プリミティブは、明示的なシャフト幅（`tail_width`）と矢羽根の寸法（`head_width`、`head_length`、または `head_angle`）を持つ閉じた 2D 多角形を構築します。これにより、状態遷移やデータフロー自体に鮮やかな塗りつぶしや枠線、埋め込みラベルを持たせることができます。シャフトや矢印ヘッドのサイズ指定、向きの制御（`head`, `mirror`）、角丸フィレット（`shape_r`）、楕円弧の角度スイープ（`angle_start`..`angle_end`）、および多点経由ルーティング（`xys`）によって各プリミティブがどのように変化するかを以下のアニメーションで確認できます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/shapes_arrow_parameter_tour.png" alt="shapes_arrow_2" />
  <figcaption class="drawlib-caption">パラメータ・ジオメトリツアー: arrow, chevron, arrow_l, arrow_u, arrow_arc, arrow_polyline のライブ変形（APNG アニメーション）</figcaption>
</figure>



<div class="drawlib-source-link">
  <a href="https://github.com/yuichi110/drawlib/blob/main/docs/docs_src/ja/02_drawing_primitives/shapes_arrow.md" target="_blank" rel="noopener noreferrer">GitHub でアニメーションのソースコードを見る &rarr;</a>
</div>

- **シャフト・矢羽根・端点ジオメトリ (`arrow`)**: `xy1` → `xy2` 間を結び、`tail_width`、`head_width`、`head_length`、`head`（`"->"`, `"<-"`, `"<->"`）、およびシャフト角度に沿って自動回転する埋め込み `text` を備えています。
- **V 字ノッチ付きステージバナー (`chevron`)**: `corner_angle`（`0°`〜`90°`）で先端および背面ノッチの鋭さを調整でき、`shape_r` で全 6 頂点の角丸化、`mirror=True` で `-X` 方向への反転が可能です。
- **直交 `90°`・`180°` ターン (`arrow_l`, `arrow_u`)**: `(width, height)` 内の中心 `xy` を基準とし、屈曲部・折り返し部の滑らかな角丸（`shape_r`）や象限単位の回転（`style.angle`）に対応します。
- **楕円弧スイープと経由点ルーティング (`arrow_arc`, `arrow_polyline`)**: `arrow_arc` は `+X` 基準で `angle_start` から `angle_end` まで反時計回りに伸び、`arrow_polyline` は任意の `xys` 経由点リストをマイター結合または角丸（`shape_r`）関節で結びます。

---

## 2. ブロック矢印プリミティブの比較早見表

全 6 種類のブロック矢印プリミティブにおける基準座標、向き制御、角丸対応、および埋め込みテキスト対応を以下の表にまとめます。

| 関数 | 基準座標（アンカー） | 向きの制御 | 角丸 (`style.shape_r`) | 埋め込み `text` 対応 |
| :--- | :--- | :--- | :--- | :--- |
| **`arrow`** | `xy1`（始点）→ `xy2`（先端） | `head`: `"->"`, `"<-"`, `"<->"` | — | **対応**（シャフトに沿って自動回転） |
| **`chevron`** | 中心 `xy` (`width`, `height`) | `mirror=False \| True`, `style.angle` | スカラー `float` または 6 要素タプル | **対応**（シェブロン中央に配置） |
| **`arrow_l`** | 中心 `xy` (`width`, `height`) | `head`: `"->"`, `"<-"`, `"<->"`, `style.angle` | スカラー `float` または 1 要素タプル（屈曲部） | **非対応**（スタンドアロンの `text()` を使用） |
| **`arrow_u`** | 中心 `xy` (`width`, `height`) | `head`: `"->"`, `"<-"`, `"<->"`, `style.angle` | スカラー `float` または 2 要素タプル `(r1, r2)` | **非対応**（スタンドアロンの `text()` を使用） |
| **`arrow_arc`** | 中心 `xy` (`width`, `height`) | `angle_start`, `angle_end`, `head`, `style.angle` | —（滑らかな楕円弧） | **非対応**（スタンドアロンの `text()` を使用） |
| **`arrow_polyline`** | 経由点 `xys=[(x1,y1), ...]` | `head`: `"->"`, `"<-"`, `"<->"` | スカラー `float` または `(len(xys)-2)` 要素タプル | **非対応**（スタンドアロンの `text()` を使用） |

> [!TIP]
> **ブロック矢印と `drawlib.lines`・`ChevronProcess` の使い分け**:
> - 遷移そのものを視覚的なコンテナとして強調したい場合（例: `"ETL Stream"` のようなラベルを内包する太いデータバス、目立つステージ間遷移、力強い循環矢印など）には、**ブロック矢印 (`drawlib.shapes`)** を使用します。
> - コンポーネントカード間を結ぶ細いポイントツーポイントのネットワーク/API 接続線には、**[線とコネクタ (`drawlib.lines`)](./lines.md)** を使用します。
> - 自動間隔調整・説明文・テーマカラーの交互配色を備えた多段階の水平パイプラインを構築する場合には、**[`ChevronProcess` (`drawlib.smartarts`)](../04_smartarts/chevron_process.md)** を使用します。

---

## 3. 直線ブロック矢印 (`arrow`)

`arrow` は任意の 2 座標 `xy1` と `xy2` の間に有向 2D ブロック矢印を描画します。シャフトの角度は自動計算され、埋め込まれた `text` もシャフトの向きに合わせて自動的に回転します。

```python
arrow(
    xy1: tuple[float, float],
    xy2: tuple[float, float],
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy1` | `tuple[float, float]` | *必須* | 矢印始点（テール）端の中心座標 `(x1, y1)`（`head="<-"` または `"<->"` の場合は逆向き矢印ヘッドの先端座標）。 |
| `xy2` | `tuple[float, float]` | *必須* | 順方向矢印ヘッドの先端座標 `(x2, y2)`。 |
| `tail_width` | `float` | *必須* | 矩形シャフトの太さ（横断幅、`> 0`）。 |
| `head_width` | `float` | *必須* | 矢印ヘッド底辺の全幅（`> tail_width`）。 |
| `head_length` | `float` | *必須* | 矢印ヘッドの底辺から先端までの軸方向の長さ（`> 0`）。2 点間の距離 `distance(xy1, xy2)` より短くする必要があります。 |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | 矢印ヘッドの向き。`xy2` 側の順方向（`"->"`）、`xy1` 側の逆方向（`"<-"`）、または両端の双方向（`"<->"`）。 |
| `style` | `Style` | *必須* | 図形の塗りつぶし（`shape_fill_color`）および枠線（`shape_line_color`, `shape_line_width`, `shape_line_style`）。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | `xy1` と `xy2` の中点に配置され、シャフトに沿って自動回転する埋め込みラベル。 |



```python
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import arrow, circle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=50)

# Primary straight block arrow from xy1=(28, 24) to xy2=(84, 24)
arrow(
    (28, 24),
    (84, 24),
    tail_width=8.5,
    head_width=18,
    head_length=14,
    head="->",  # "->", "<-", or "<->"
    style=Styles.PrimaryFlat,
    text="Data Ingestion",
    text_style=Styles.WhiteBold.patch(text_size=11.0),
)

# Endpoint markers for xy1 and xy2
circle((28, 24), radius=1.2, style=Styles.DangerFlat)
line((28, 24), (28, 11), style=Styles.DangerDashed)
text((28, 7.0), "xy1 (28, 24)", style=Styles.DangerBold.patch(text_size=10.5))

circle((84, 24), radius=1.2, style=Styles.DangerFlat)
line((84, 24), (84, 11), style=Styles.DangerDashed)
text((84, 7.0), "xy2 (84, 24)", style=Styles.DangerBold.patch(text_size=10.5))

# Dimension: tail_width (shaft y = 19.75..28.25)
line((18, 19.75), (28, 19.75), style=Styles.MutedDashed)
line((18, 28.25), (28, 28.25), style=Styles.MutedDashed)
line((20, 19.75), (20, 28.25), arrow_head="<->", style=Styles.DarkBold)
text((10, 24), "tail_width", style=Styles.DarkBold.patch(text_size=10.5))

# Dimension: head_length (x = 70..84)
line((70, 33), (70, 41), style=Styles.MutedDashed)
line((84, 24), (84, 41), style=Styles.MutedDashed)
line((70, 39), (84, 39), arrow_head="<->", style=Styles.DarkBold)
text((77, 43.5), "head_length", style=Styles.DarkBold.patch(text_size=10.5))

# Dimension: head_width (arrowhead base y = 15..33)
line((70, 15), (96, 15), style=Styles.MutedDashed)
line((70, 33), (96, 33), style=Styles.MutedDashed)
line((94, 15), (94, 33), arrow_head="<->", style=Styles.DarkBold)
text((107, 24), "head_width", style=Styles.DarkBold.patch(text_size=10.5))

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_straight.png" alt="shapes_arrow_3" />
  <figcaption class="drawlib-caption">直線ブロック矢印の各部寸法構造</figcaption>
</figure>



---

## 4. プロセスシェブロン (`chevron`) と向きの反転 (`head`, `mirror`)

`chevron` は、背面に V 字の切り込みを持ち前後に噛み合う 6 頂点の矢羽根型ブロックを描画します。連続する工程・ステージ図に最適です。

```python
chevron(
    xy: tuple[float, float],
    width: float,
    height: float,
    corner_angle: float,
    mirror: bool = False,
    *,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | 基準座標 `(x, y)`（プリセットの `Styles.*` 使用時は中心基準）。 |
| `width` / `height` | `float` | *必須* | 本体の水平幅および垂直高さ（`> 0`）。 |
| `corner_angle` | `float` | *必須* | 先端および背面 V 字ノッチの傾斜角度（度数法、`0 < corner_angle < 90`、一般的には `55`〜`70`）。 |
| `mirror` | `bool` | `False` | `True` の場合、シェブロンを水平方向に反転させて左向き（`-X`）にします。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、回転角（`style.angle`）、および頂点の角丸（`style.shape_r` にスカラー `float` または頂点ごとの 6 要素タプルを指定）。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 中央配置されるテキストラベルおよび任意のタイポグラフィ上書きスタイル。 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import chevron
from drawlib.styles import Styles

setup(width=100, height=36)
chevron(
    (50, 18),
    width=42,
    height=20,
    corner_angle=60,  # Tip acute angle
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="Stage 1",
    text_style=Styles.WhiteBold.patch(text_size=12.0),
)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_chevron.png" alt="shapes_arrow_4" />
  <figcaption class="drawlib-caption">角丸を施したプロセスシェブロン</figcaption>
</figure>



### 矢印ヘッドの向き (`head`) と反転シェブロン (`mirror=True`)

向きを持つ 5 種類のブロック矢印（`arrow`, `arrow_l`, `arrow_u`, `arrow_arc`, `arrow_polyline`）はすべて `head="->"`、`head="<-"`、`head="<->"` をサポートしており、`chevron()` は `mirror=True` による水平方向の反転をサポートしています。



```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow, chevron
from drawlib.styles import Styles

setup(width=124, height=52)

# Top row: head="->", head="<-", head="<->"
arrow(
    (6, 39),
    (41, 39),
    tail_width=5.5,
    head_width=11,
    head_length=7,
    head="->",
    style=Styles.PrimaryFlat,
    text='head="->"',
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
arrow(
    (44.5, 39),
    (79.5, 39),
    tail_width=5.5,
    head_width=11,
    head_length=7,
    head="<-",
    style=Styles.Neutral,
    text='head="<-"',
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
arrow(
    (83, 39),
    (118, 39),
    tail_width=5.5,
    head_width=11,
    head_length=7,
    head="<->",
    style=Styles.SecondaryNeutral,
    text='head="<->"',
    text_style=Styles.DarkBold.patch(text_size=10.5),
)

# Bottom row: Standard chevron (mirror=False) vs Mirrored chevron (mirror=True)
chevron(
    (35, 15),
    width=36,
    height=16,
    corner_angle=60,
    mirror=False,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="mirror=False",
    text_style=Styles.DarkBold.patch(text_size=11.0),
)
chevron(
    (89, 15),
    width=36,
    height=16,
    corner_angle=60,
    mirror=True,
    style=Styles.PrimaryNeutral.patch(shape_r=1.5),
    text="mirror=True",
    text_style=Styles.DarkBold.patch(text_size=11.0),
)

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_heads_and_mirror.png" alt="shapes_arrow_5" />
  <figcaption class="drawlib-caption">矢印ヘッドの向き (head='->', '<-', '<->') と反転シェブロン (mirror=True)</figcaption>
</figure>



---

## 5. 直交折れ曲がりブロック矢印 (`arrow_l`, `arrow_u`)

> [!NOTE]
> `arrow_l()` および `arrow_u()` は `text` や `text_style` を**受け取りません**。屈曲部（エルボー）やシャフト付近にラベルを配置する場合は、スタンドアロンの `drawlib.text.text()` を使用してください。

### 5.1. L 字コーナー矢印 (`arrow_l`)
バウンディングボックス `(width, height)` の中心 `xy` を基準とする `90°` 直角のブロック矢印を描画します。デフォルト（`angle=0`）では、始点（テール）が左上から始まり、左下で右方向へ折れ曲がって右下へ向かいます。任意の象限に向きを変えるには `style.patch(angle=90 | 180 | 270)` を使用します。

```python
arrow_l(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | L 字矢印のバウンディングボックスの中心座標 `(x, y)`。 |
| `width` / `height` | `float` | *必須* | バウンディングボックスの水平幅および垂直高さ（`> 0`）。 |
| `tail_width` | `float` | *必須* | シャフトの幅（`> 0`）。 |
| `head_width` / `head_length` | `float` | *必須* | 矢印ヘッド底辺の幅および軸方向の長さ（`> 0`）。 |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | 矢印ヘッドの向き（`"->"`, `"<-"`, `"<->"`）。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、回転角（`style.angle`）、および屈曲部の角丸半径（`style.shape_r` にスカラー `float` または 1 要素タプルを指定）。 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_l
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_l(
    (50, 30),
    width=40,
    height=35,
    tail_width=4,
    head_width=11,
    head_length=8,
    # Corner rounding radius
    style=Styles.DarkBold.patch(shape_r=5),
)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_l.png" alt="shapes_arrow_6" />
  <figcaption class="drawlib-caption">屈曲部を角丸にした直角コーナーブロック矢印 (arrow_l)</figcaption>
</figure>



### 5.2. U ターンフィードバック矢印 (`arrow_u`)
中心 `xy` を基準とする `180°` 折り返しブロック矢印を描画します。リトライループ、ロールバック、リクエスト・レスポンスの折り返し経路などに最適です。

```python
arrow_u(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | U 字矢印のバウンディングボックスの中心座標 `(x, y)`。 |
| `width` / `height` | `float` | *必須* | バウンディングボックスの水平幅および垂直高さ（`> 0`）。 |
| `tail_width` | `float` | *必須* | シャフトの幅（`> 0`）。 |
| `head_width` / `head_length` | `float` | *必須* | 矢印ヘッドの幅および軸方向の長さ（`> 0`）。 |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | 矢印ヘッドの向き（`"->"`, `"<-"`, `"<->"`）。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、回転角（`style.angle`）、および折り返しコーナーの角丸半径（`style.shape_r` にスカラー `float` または 2 つのコーナーに対応する 2 要素タプル `(r1, r2)` を指定）。 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_u
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_u(
    (50, 30),
    width=35,
    height=40,
    tail_width=4,
    head_width=11,
    head_length=8,
    # Corner rounding radius (scalar or 2-tuple)
    style=Styles.DarkBold.patch(shape_r=6),
)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_u.png" alt="shapes_arrow_7" />
  <figcaption class="drawlib-caption">折り返し角を丸めた 180 度 U ターンブロック矢印 (arrow_u)</figcaption>
</figure>



---

## 6. 円弧・多点折れ線ブロック矢印 (`arrow_arc`, `arrow_polyline`)

> [!NOTE]
> `arrow_arc()` および `arrow_polyline()` は `text` や `text_style` を**受け取りません**。円弧の内側や経路の横にラベルを添える場合は、スタンドアロンの `drawlib.text.text()` を使用してください。

### 6.1. 円弧・楕円弧ブロック矢印 (`arrow_arc`)
楕円の外周に沿って `angle_start` から `angle_end` まで反時計回りに伸びる曲線 2D ブロック矢印を描画します（角度は `+X` 方向を基準とした度数法で、`angle_start > angle_end` の場合は `0°` を跨いで周回します。時計回りに向ける場合は `head="<-"` を使用します）。

```python
arrow_arc(
    xy: tuple[float, float],
    width: float,
    height: float,
    tail_width: float,
    head_width: float,
    head_angle: float = 10,
    head: Literal["->", "<-", "<->"] = "->",
    angle_start: float = 0,
    angle_end: float = 180,
    *,
    style: Style,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | 基準となる楕円の中心座標 `(x, y)`。 |
| `width` / `height` | `float` | *必須* | 円弧楕円の水平直径および垂直直径（`> 0`）。 |
| `tail_width` / `head_width` | `float` | *必須* | 曲線シャフトの幅および矢印ヘッド底辺の幅（`> 0`）。 |
| `head_angle` | `float` | `10` | 矢印ヘッドが占める角度幅（度数法、`> 0`）。 |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | 矢印ヘッドの向き（`"->"`, `"<-"`, `"<->"`）。 |
| `angle_start` / `angle_end` | `float` | `0` / `180` | 反時計回り（CCW）の開始角度および終了角度（度数法）。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、および円弧全体の回転角（`style.angle`）。 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_arc
from drawlib.styles import Styles

setup(width=100, height=35)
arrow_arc(
    (50, 26),
    width=45,
    height=32,
    tail_width=4,
    head_width=11,
    head_angle=12,
    head="->",
    angle_start=180,
    angle_end=0,
    style=Styles.DarkBold,
)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_arc.png" alt="shapes_arrow_8" />
  <figcaption class="drawlib-caption">円弧ブロック矢印 (arrow_arc)</figcaption>
</figure>



### 6.2. 多点折れ線ブロック矢印 (`arrow_polyline`)
任意の経由点（ウェイポイント）座標リスト `xys=[(x1, y1), (x2, y2), ...]` を通過する複雑な折れ線 2D ブロック矢印を描画します。各中間コーナーは自動的にマイター結合または角丸フィレットで接続されます。

```python
arrow_polyline(
    xys: list[tuple[float, float]],
    tail_width: float,
    head_width: float,
    head_length: float,
    head: Literal["->", "<-", "<->"] = "->",
    *,
    style: Style,
) -> None
```

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xys` | `list[tuple[float, float]]` | *必須* | 2 点以上の経由点座標のシーケンス `[(x1, y1), (x2, y2), ...]`。 |
| `tail_width` | `float` | *必須* | 折れ線シャフトの幅（`> 0`）。 |
| `head_width` / `head_length` | `float` | *必須* | 矢印ヘッドの幅および軸方向の長さ（`> 0`）。 |
| `head` | `Literal["->", "<-", "<->"]` | `"->"` | 矢印ヘッドの向き（`"->"`, `"<-"`, `"<->"`）。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、および中間関節の角丸半径（`style.shape_r` にスカラー `float` または中間関節ごとの `(len(xys) - 2)` 要素タプルを指定）。 |



```python
from drawlib.canvas import save, setup
from drawlib.shapes import arrow_polyline
from drawlib.styles import Styles

setup(width=100, height=60)
arrow_polyline(
    [(15, 15), (50, 15), (50, 45), (85, 45)],
    tail_width=4,
    head_width=11,
    head_length=8,
    head="->",
    # Uniform scalar radius or (len(xys) - 2)-tuple per intermediate joint
    style=Styles.PrimaryFlat.patch(shape_r=(3, 6)),
)
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/02_drawing_primitives/shapes_arrow/arrow_polyline.png" alt="shapes_arrow_9" />
  <figcaption class="drawlib-caption">関節ごとに角丸を指定した多点折れ線ブロック矢印 (arrow_polyline)</figcaption>
</figure>


