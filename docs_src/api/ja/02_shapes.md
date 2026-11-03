# drawlib.shapes（基本・矢印・立体・記号シェイプ）

`drawlib.shapes` は基本図形・多角形・ブロック矢印・3D コンテナ・バッジ・記号にわたる全 43 個のベクターシェイプ描画関数を提供します。すべての関数はキーワード専用の必須引数 `*, style: Style` を受け取り、`from drawlib.shapes import circle, cylinder, rectangle, ...` でインポートします。

```drawlib align=center code=fold file=02_shapes_hero.png caption="drawlib.shapes の 5 カテゴリ・全 43 ベクター図形プリミティブ"
from drawlib.canvas import save, setup
from drawlib.shapes import (
    chevron,
    circle,
    cloud,
    cylinder,
    gear,
    rectangle,
    regularpolygon,
    shield,
    star,
    tag,
)
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=62, dpi=150)

text(
    (60, 55.5),
    "drawlib.shapes — 43 Vector Primitives (5 Families)",
    style=Styles.DarkBold.patch(text_size=12.2),
)

# 1. Basic Shapes
rectangle((14.7, 27), width=20.4, height=44, style=Styles.Neutral.patch(shape_r=2.0))
text((14.7, 44.5), "Basic", style=Styles.DarkBold.patch(text_size=10.5))
rectangle((14.7, 32.5), width=13, height=7.8, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
circle((14.7, 16.5), radius=5.2, hole_ratio=0.5, style=Styles.SecondaryNeutral)

# 2. Polygons & Stars
rectangle((37.35, 27), width=20.4, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((37.35, 44.5), "Polygons", style=Styles.DarkBold.patch(text_size=10.5))
regularpolygon((37.35, 32.5), 6, 5.5, style=Styles.Neutral.patch(shape_r=0.8))
star((37.35, 16.5), 5, 5.8, 2.6, style=Styles.PrimaryNeutral)

# 3. 3D Containers (Focal Hero)
rectangle((60.0, 27), width=20.4, height=44, style=Styles.PrimaryFlat.patch(shape_r=2.0))
text(
    (60.0, 44.5),
    "Containers",
    style=Styles.WhiteBold.patch(text_size=10.5, text_color=Colors.White),
)
cylinder((60.0, 32.5), width=12, height=9.5, disks=2, style=Styles.Neutral)
cloud((60.0, 16.5), width=14, height=8.5, style=Styles.Neutral)

# 4. Badges & Callouts
rectangle((82.65, 27), width=20.4, height=44, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((82.65, 44.5), "Badges", style=Styles.DarkBold.patch(text_size=10.5))
shield((82.65, 32.5), width=10.8, height=10.2, style=Styles.PrimaryNeutral)
tag((82.65, 16.5), width=13.5, height=8.0, hole_ratio=0.22, style=Styles.Neutral)

# 5. Block Arrows & Symbols
rectangle((105.3, 27), width=20.4, height=44, style=Styles.Neutral.patch(shape_r=2.0))
text((105.3, 44.5), "Symbols", style=Styles.DarkBold.patch(text_size=10.5))
chevron((105.3, 32.5), width=13, height=7.8, corner_angle=55, style=Styles.PrimaryNeutral)
gear((105.3, 16.5), 8, 5.6, 4.0, hole_radius=1.8, style=Styles.SecondaryNeutral)

save()
```

### 座標アンカーとスタイル指定の共通原則

- **中心アンカー `(cx, cy)` が標準**: 39 種の図形（`bubblespeech` を除くすべての基本・多角形・3D コンテナ・バッジ・記号・矩形境界矢印）はデフォルトで **`xy = (cx, cy)`（中心）** に配置されます（`style.patch(halign=..., valign=...)` で変更可）。
- **中心以外のアンカー**: `arrow(xy1, xy2, ...)` は始点と先端、`arrow_polyline(xys, ...)` と `polygon(xys, ...)` は明示的な頂点リスト、`bubblespeech(xy, ...)` は吹き出し本体の**左下 `(x0, y0)`** を指定します。
- **共通スタイル拡張**: 角丸は `style.patch(shape_r=2.0)`、回転は `style.patch(angle=...)`、透明くり抜きは `hole_ratio` / `holes` で制御します。

---

## `def` arc(xy, width, height, *, style, ...)

**中心 `(cx, cy)`** を基準に、塗りを持たない楕円／円弧シェイプを描画します（`style` の `line_color`・`line_width`・`line_style` を使用）。

```python
def arc(xy: Coordinate, width: PosFloat, height: PosFloat, *, style: Style, angle_start: Angle = 0.0, angle_end: Angle = 360.0, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 基準楕円の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 円弧楕円の水平幅および垂直高さ。 |
| `angle_start / angle_end` | `Angle` | `0.0 / 360.0` | 反時計回りの開始角度および終了角度（度：`0°`＝右）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` arrow(xy1, xy2, tail_width, head_width, head_length, ...)

始点 **`xy1`** から先端 **`xy2`** へ向かう直線の 2D 塗りつぶしブロック矢印を描画します。

```python
def arrow(xy1: Coordinate, xy2: Coordinate, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy1 / xy2` | `Coordinate` | *必須* | 矢印の始点 `(x1, y1)` および先端 `(x2, y2)` 座標。 |
| `tail_width` | `PosFloat` | *必須* | 矢印シャフト（軸）の太さ。 |
| `head_width / head_length` | `PosFloat` | *必須* | 矢じり部分の幅および長さ。 |
| `head` | `ArrowHead` | `'->'` | 矢じりの向き（`'->'`, `'<-'`, `'<->'`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` arrow_arc(xy, width, height, tail_width, head_width, ...)

**中心 `(cx, cy)`** を基準とする楕円軌道に沿った曲線 2D ブロック矢印を描画します。

```python
def arrow_arc(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_angle: Angle = 10, head: ArrowHead = ->, angle_start: Angle = 0, angle_end: Angle = 180, *, style: Style) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 円弧外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 円弧楕円の外径幅および高さ。 |
| `tail_width / head_width` | `PosFloat` | *必須* | シャフト幅および矢じり幅。 |
| `head_angle` | `Angle` | `10` | 矢じり部分の中心角（度）。 |
| `head` | `ArrowHead` | `'->'` | 矢じりの向き（`'->'`, `'<-'`, `'<->'`）。 |
| `angle_start / angle_end` | `Angle` | `0 / 180` | 反時計回りの開始角度・終了角度（度）。 |
| `style` | `Style` | *必須* | 塗り色・枠線・回転 `angle`・位置揃えを制御するキーワード専用の図形 `Style`。 |

---

## `def` arrow_l(xy, width, height, tail_width, head_width, head_length, ...)

**中心 `(cx, cy)`** を基準に、直角に折れ曲がる L 字型 2D ブロック矢印を描画します。

```python
def arrow_l(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | L 字矢印全体の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | L 字矢印全体の幅および高さ。 |
| `tail_width / head_width / head_length` | `PosFloat` | *必須* | シャフト幅・矢じり幅・矢じり長。 |
| `head` | `ArrowHead` | `'->'` | 矢じりの向き（`'->'`, `'<-'`, `'<->'`）。 |
| `style` | `Style` | *必須* | 塗り色・枠線・回転 `angle`・位置揃えを制御するキーワード専用の図形 `Style`。 |

---

## `def` arrow_polyline(xys, tail_width, head_width, head_length, ...)

明示的な**頂点列 `xys`** に沿って折れ曲がるマルチセグメント 2D ブロック矢印を描画します。

```python
def arrow_polyline(xys: Coordinates, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xys` | `Coordinates` | *必須* | シャフト中心線に沿う 2 点以上の**頂点座標リスト**。 |
| `tail_width / head_width / head_length` | `PosFloat` | *必須* | シャフト幅・矢じり幅・矢じり長。 |
| `head` | `ArrowHead` | `'->'` | 矢じりの向き（`'->'`, `'<-'`, `'<->'`）。 |
| `style` | `Style` | *必須* | 塗り色・枠線・回転 `angle`・位置揃えを制御するキーワード専用の図形 `Style`。 |

---

## `def` arrow_u(xy, width, height, tail_width, head_width, head_length, ...)

**中心 `(cx, cy)`** を基準に、180 度折り返す U 字型 2D ブロック矢印を描画します。

```python
def arrow_u(xy: Coordinate, width: PosFloat, height: PosFloat, tail_width: PosFloat, head_width: PosFloat, head_length: PosFloat, head: ArrowHead = ->, *, style: Style) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | U 字矢印全体の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | U 字矢印全体の幅および高さ。 |
| `tail_width / head_width / head_length` | `PosFloat` | *必須* | シャフト幅・矢じり幅・矢じり長。 |
| `head` | `ArrowHead` | `'->'` | 矢じりの向き（`'->'`, `'<-'`, `'<->'`）。 |
| `style` | `Style` | *必須* | 塗り色・枠線・回転 `angle`・位置揃えを制御するキーワード専用の図形 `Style`。 |

---

## `def` brace(xy, width, height, *, symbol='{', ...)

**中心 `(cx, cy)`** を基準に、波括弧・角括弧・丸括弧のグルーピング記号を描画します（`style.line_*` による線描画）。

```python
def brace(xy: Coordinate, width: PosFloat, height: PosFloat, *, symbol: BraceSymbol = {, direction: BraceDirection | None = None, tip_ratio: Ratio | None = None, tip_position_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 括弧外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 括弧の外接幅および高さ。 |
| `symbol` | `BraceSymbol` | `'{'` | 括弧種別（波括弧 `'{'`/`'}'`/`'curly'`、角括弧 `'['`/`']'`、丸括弧 `'('`/`')'` 等）。 |
| `direction` | `BraceDirection \| None` | `None` | 括弧の向き（`'left'`, `'right'`, `'top'`, `'bottom'`。省略時は `symbol` から自動決定）。 |
| `tip_ratio / tip_position_ratio` | `Ratio \| None` | `None` | 波括弧の中央突起の深さ比率および位置比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` bubblespeech(xy, width, height, tail_edge, tail_start_ratio, tail_vertex_xy, tail_end_ratio, *, style, ...)

吹き出し本体の**左下座標 `(x0, y0)`** を基準とし、指定辺から `tail_vertex_xy` へ伸びるポインタ付きの吹き出しを描画します。

```python
def bubblespeech(xy: Coordinate, width: PosFloat, height: PosFloat, tail_edge: TailEdge, tail_start_ratio: Ratio, tail_vertex_xy: Coordinate, tail_end_ratio: Ratio, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 吹き出し本体矩形の**左下座標 `(x0, y0)`**。 |
| `width / height` | `PosFloat` | *必須* | 吹き出し本体の幅および高さ（しっぽを除く）。 |
| `tail_edge` | `TailEdge` | *必須* | しっぽが出る辺（`'left'`, `'top'`, `'right'`, `'bottom'`）。 |
| `tail_start_ratio / tail_end_ratio` | `Ratio` | *必須* | `tail_edge` 上でのしっぽ開始比率・終了比率（`0.0..1.0`, `start < end`）。 |
| `tail_vertex_xy` | `Coordinate` | *必須* | しっぽ先端が指し示すキャンバス座標 `(tx, ty)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` checkmark(xy, width, height=None, *, variant='standard', ...)

**中心 `(cx, cy)`** を基準に、チェックマーク記号または円形承認バッジを描画します。

```python
def checkmark(xy: Coordinate, width: PosFloat, height: PosFloat | None = None, *, variant: CheckmarkVariant = standard, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | チェックマークの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat / PosFloat \| None` | *必須* / None | 外接幅および高さ（`height=None` 時は正方形 `width`）。 |
| `variant` | `CheckmarkVariant` | `'standard'` | 形状バリアント（`'standard'`, `'check'`, `'circle'`, `'solid_circle'`）。 |
| `thickness_ratio` | `Ratio \| None` | `None` | 線の太さ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` chevron(xy, width, height, corner_angle, mirror=False, *, style, ...)

**中心 `(cx, cy)`** を基準に、プロセス段階を表すシェブロン（矢羽根ブロック）を描画します（`shape_r` 角丸対応）。

```python
def chevron(xy: Coordinate, width: PosFloat, height: PosFloat, corner_angle: Angle90, mirror: bool = False, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心 `(cx, cy)`**（`halign`/`valign` で変更可）。 |
| `width / height` | `PosFloat` | *必須* | シェブロンの外接幅および高さ。 |
| `corner_angle` | `Angle90` | *必須* | 先端の角度 `(0, 90)` 度。 |
| `mirror` | `bool` | `False` | `True` で左右反転（左向き）にします。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` circle(xy, radius, *, hole_ratio=None, style, ...)

**中心 `(cx, cy)`** を基準に、円または中空リング（`hole_ratio` 指定時）を描画します。

```python
def circle(xy: Coordinate, radius: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 円の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 外周半径（キャンバス単位）。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空リングにする場合の内径比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` clock(xy, radius, *, variant='standard', hour=10.0, minute=10.0, ...)

**中心 `(cx, cy)`** を基準に、アナログ時計・ストップウォッチ・デジタル時計シェイプを描画します。

```python
def clock(xy: Coordinate, radius: PosFloat, *, variant: ClockVariant = standard, hour: float = 10.0, minute: float = 10.0, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 時計の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 文字盤の半径（`'digital'` 時はサイズ基準）。 |
| `variant` | `ClockVariant` | `'standard'` | 時計バリアント（`'standard'`, `'ticks'`, `'dial'`, `'stopwatch'`, `'timer'`, `'alarm'`, `'digital'`）。 |
| `hour / minute` | `float` | `10.0 / 10.0` | 表示する「時」および「分」の値。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` cloud(xy, width, height, *, variant='standard', bump_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、クラウド境界・ネットワークシルエットを描画します。

```python
def cloud(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: CloudVariant = standard, bump_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | クラウド外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | クラウド全体の幅および高さ。 |
| `variant` | `CloudVariant` | `'standard'` | シルエット種別（`'standard'`, `'flat'`, `'fluffy'`, `'simple'`）。 |
| `bump_ratio` | `Ratio \| None` | `None` | 雲の膨らみ深さ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` cube(xy, width, height, *, depth_ratio=None, style, ...)

**中心 `(cx, cy)`** を基準に、3D キューブ（直方体ノード）を描画します。

```python
def cube(xy: Coordinate, width: PosFloat, height: PosFloat, *, depth_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 3D 外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 奥行き面を含む全体の外接幅および高さ。 |
| `depth_ratio` | `Ratio \| None` | `None` | `min(width, height)` に対する 3D 奥行き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` cylinder(xy, width, height, *, style, disks=1, ...)

**中心 `(cx, cy)`** を基準に、データベースやストレージを表す 3D 円柱シェイプを描画します。

```python
def cylinder(xy: Coordinate, width: PosFloat, height: PosFloat, *, style: Style, disks: PosInt = 1, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 円柱の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 円柱全体の幅および高さ。 |
| `disks` | `PosInt` | `1` | 上部の積層ディスク段数（`>= 1`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` document(xy, width, height, *, variant='wave', stacked=1, ...)

**中心 `(cx, cy)`** を基準に、波形下端・折れ角・複数枚重ね対応のドキュメント図形を描画します。

```python
def document(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: DocumentVariant = wave, stacked: PosInt = 1, wave_ratio: Ratio | None = None, fold_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | ドキュメント外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `DocumentVariant` | `'wave'` | 形状バリアント（`'wave'`, `'folded'`, `'page'`, `'note'`, `'report'` 等 9 種）。 |
| `stacked` | `PosInt` | `1` | 重ねるシート枚数（`1` で単票、`>= 2` で複数枚スタック）。 |
| `wave_ratio / fold_ratio` | `Ratio \| None` | `None` | 下端の波振幅比率および右上折れ角サイズ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` ellipse(xy, width, height, *, hole_ratio=None, style, ...)

**中心 `(cx, cy)`** を基準に、楕円または中空オーバルリング（`hole_ratio`）を描画します。

```python
def ellipse(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 楕円の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 水平直径（`2 * rx`）および垂直直径（`2 * ry`）。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空リングにする場合の内径比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` explosion(xy, width, height, *, variant='standard', style, ...)

**中心 `(cx, cy)`** を基準に、障害発生や強調を表す爆発・インパクト図形を描画します。

```python
def explosion(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: ExplosionVariant = standard, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `ExplosionVariant` | `'standard'` | シルエット種別（`'standard'`, `'irregular'`, `'heavy'`, `'wild'`, `'curved'`, `'comic'`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` face(xy, radius, *, variant='smile', style, ...)

**中心 `(cx, cy)`** を基準に、感情やステータスを表すフェイス記号を描画します。

```python
def face(xy: Coordinate, radius: PosFloat, *, variant: FaceVariant = smile, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 円の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | フェイス円の半径。 |
| `variant` | `FaceVariant` | `'smile'` | 表情バリアント（`'smile'`, `'neutral'`, `'sad'`, `'angry'`, `'skull'` 等 9 種）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` fan(xy, radius, *, style, angle_start=0, angle_end=180, ...)

**中心 `(cx, cy)`** を基準に、塗りつぶされた扇形（パイセクター）を描画します。

```python
def fan(xy: Coordinate, radius: PosFloat, *, style: Style, angle_start: Angle = 0, angle_end: Angle = 180, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 扇形円の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 扇形の半径。 |
| `angle_start / angle_end` | `Angle` | `0 / 180` | 反時計回りの開始角度・終了角度（度）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` forbidden(xy, radius, *, variant='slash', thickness_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、禁止・拒否・進入禁止マークを描画します。

```python
def forbidden(xy: Coordinate, radius: PosFloat, *, variant: ForbiddenVariant = slash, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 禁止マークの**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 外周円の半径。 |
| `variant` | `ForbiddenVariant` | `'slash'` | バリアント（`'slash'`, `'standard'`, `'backslash'`, `'cross'`, `'no_entry'`, `'minus'`）。 |
| `thickness_ratio` | `Ratio \| None` | `None` | リングおよび斜線の太さ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` funnel(xy, width, height, *, variant='standard', ...)

**中心 `(cx, cy)`** を基準に、フィルタリングや変換パイプラインを表す漏斗（ファネル）を描画します。

```python
def funnel(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: FunnelVariant = standard, neck_width_ratio: Ratio | None = None, neck_height_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 漏斗全体の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 上部開口幅および全体の高さ。 |
| `variant` | `FunnelVariant` | `'standard'` | 形状バリアント（`'standard'`, `'flat'`, `'3d'`, `'cylinder'`, `'curved'`）。 |
| `neck_width_ratio / neck_height_ratio` | `Ratio \| None` | `None` | 下部ノズルの幅比率および高さ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` gear(xy, num_teeth, radius_ext, radius_int, *, hole_radius=None, ...)

**中心 `(cx, cy)`** を基準に、設定・ワーカーエンジンを表す歯車（ギア）を描画します。

```python
def gear(xy: Coordinate, num_teeth: NumVertex, radius_ext: PosFloat, radius_int: PosFloat, *, tooth_ext_ratio: Ratio | None = None, tooth_int_ratio: Ratio | None = None, hole_radius: PosFloat | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 歯車の**中心座標 `(cx, cy)`**。 |
| `num_teeth` | `NumVertex` | *必須* | 歯の数（`>= 3`）。 |
| `radius_ext / radius_int` | `PosFloat` | *必須* | 歯先の外半径および歯底の内半径。 |
| `tooth_ext_ratio / tooth_int_ratio` | `Ratio \| None` | `None (0.35 / 0.55)` | 1 ピッチ角に対する歯先幅・歯元幅の比率（既定 `0.35` / `0.55`）。 |
| `hole_radius` | `PosFloat \| None` | `None` | 中央の丸穴半径（`None` で穴なし）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` heart(xy, width, height, *, variant='standard', style, ...)

**中心 `(cx, cy)`** を基準に、ヘルスチェックや好感度を表すハート／ブロークンハートを描画します。

```python
def heart(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: HeartVariant = standard, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | ハート外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `HeartVariant` | `'standard'` | 形状バリアント（`'standard'`, `'classic'`, `'broken'`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` lightning(xy, width, height, *, variant='standard', mirror=False, ...)

**中心 `(cx, cy)`** を基準に、高速処理・イベント発火・電力を表す稲妻シェイプを描画します。

```python
def lightning(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: LightningVariant = standard, mirror: bool = False, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 稲妻外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `LightningVariant` | `'standard'` | バリアント（`'standard'`, `'flat'`, `'double'`, `'flat_double'`, `'angled'`, `'slanted'`）。 |
| `mirror` | `bool` | `False` | `True` で左右反転します。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` math_symbol(xy, symbol, width, height=None, *, thickness_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、算術演算子シェイプ（`+`, `-`, `×`, `÷`, `=`, `≠`）を描画します。

```python
def math_symbol(xy: Coordinate, symbol: MathSymbol, width: PosFloat, height: PosFloat | None = None, *, thickness_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 演算子シェイプの**中心座標 `(cx, cy)`**。 |
| `symbol` | `MathSymbol` | *必須* | 演算子記号（`'+'`, `'-'`, `'×'`, `'÷'`, `'='`, `'≠'` 等）。 |
| `width / height` | `PosFloat / PosFloat \| None` | *必須* / None | 外接幅および高さ（`height=None` 時は `width` と同値）。 |
| `thickness_ratio` | `Ratio \| None` | `None (0.28)` | バー太さ比率（既定 `0.28`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` moon(xy, width, height, *, variant='crescent', mirror=False, ...)

**中心 `(cx, cy)`** を基準に、三日月・半月シェイプ（夜間バッチ・ダークモード表現など）を描画します。

```python
def moon(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: MoonVariant = crescent, mirror: bool = False, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 月シェイプ外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `MoonVariant` | `'crescent'` | 形状バリアント（`'crescent'`, `'standard'`, `'thin'`, `'waxing'`, `'half'`）。 |
| `mirror` | `bool` | `False` | `True` で左右反転します。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` parallelogram(xy, width, height, corner_angle, *, hole_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、平行四辺形（フローチャートの入出力ブロック等）を描画します（`shape_r`・`hole_ratio` 対応）。

```python
def parallelogram(xy: Coordinate, width: PosFloat, height: PosFloat, corner_angle: Angle90, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 平行四辺形の幅および高さ。 |
| `corner_angle` | `Angle90` | *必須* | 左下角の傾斜角度 `(0, 90)` 度。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` pin(xy, width, height, *, variant='pointer', hole_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、マップピンまたはティアドロップ型ポインタバッジを描画します。

```python
def pin(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: PinVariant = pointer, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | ピン外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `PinVariant` | `'pointer'` | バリアント（`'pointer'`, `'standard'`, `'teardrop'`, `'drop'`, `'pin'`, `'badge'`）。 |
| `hole_ratio` | `Ratio \| None` | `None` | ピン頭部の中央丸穴比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` plaque(xy, width, height, *, variant='concave', cut_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、四隅を内反り・面取り加工したプラーク（飾り板）を描画します。

```python
def plaque(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: PlaqueVariant = concave, cut_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | プラークの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `PlaqueVariant` | `'concave'` | 四隅バリアント（`'concave'`, `'standard'`, `'chamfered'`, `'octagon'`, `'notched'`）。 |
| `cut_ratio` | `Ratio \| None` | `None` | 四隅カットサイズの比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` polygon(xys, *, holes=None, style, ...)

明示的な**外周頂点列 `xys`** を結ぶ任意の多角形を描画します（内部くり抜き穴 `holes` および角丸 `shape_r` 対応）。

```python
def polygon(xys: Coordinates, *, holes: list[Coordinates] | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xys` | `Coordinates` | *必須* | 外周輪郭を構成する**頂点座標リスト** `[(x1, y1), ...]`。 |
| `holes` | `list[Coordinates] \| None` | `None` | 内部を透明にくり抜く穴の頂点リスト群 `[[(x, y), ...], ...]`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` rectangle(xy, width, height, *, hole_ratio=None, style, ...)

**中心 `(cx, cy)`** を基準に、矩形・角丸カード（`style.patch(shape_r=...)`）・中空フレーム（`hole_ratio`）を描画します。

```python
def rectangle(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心 `(cx, cy)`**（`halign`/`valign` で変更可）。 |
| `width / height` | `PosFloat` | *必須* | 矩形の幅および高さ（キャンバス単位）。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空フレームにする場合の内枠くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` regularpolygon(xy, num_vertex, radius, *, hole_ratio=None, style, ...)

**中心 `(cx, cy)`** と外接円半径 `radius` を基準に、正多角形（正五角形・正六角形・正八角形など）を描画します。

```python
def regularpolygon(xy: Coordinate, num_vertex: NumVertex, radius: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 外接円の**中心座標 `(cx, cy)`**。 |
| `num_vertex` | `NumVertex` | *必須* | 頂点数（`>= 3`）。 |
| `radius` | `PosFloat` | *必須* | 外接円の半径。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` rhombus(xy, width, height, *, hole_ratio=None, style, ...)

**中心 `(cx, cy)`** を基準に、水平対角線 `width`・垂直対角線 `height` のひし形（条件分岐ノード等）を描画します。

```python
def rhombus(xy: Coordinate, width: PosFloat, height: PosFloat, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 水平対角線の長さおよび垂直対角線の長さ。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` ribbon(xy, width, height, *, variant='down', ...)

**中心 `(cx, cy)`** を基準に、タイトル見出しや受賞バッジ用のリボンバナーを描画します。

```python
def ribbon(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: RibbonVariant = down, tail_width_ratio: Ratio | None = None, drop_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | リボン全体の**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 外接幅および高さ。 |
| `variant` | `RibbonVariant` | `'down'` | リボン種別（`'down'`, `'standard'`, `'up'`, `'flat'`, `'banner'`）。 |
| `tail_width_ratio / drop_ratio` | `Ratio \| None` | `None` | 両端しっぽ幅の比率および段差ドロップ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` shape(xy, path_points, *, style, ..., is_default_center=False)

直線頂点および 2 次／3 次ベジェ制御点を含む `path_points` から任意の閉じたカスタム図形を描画する低レベルプリミティブです（デフォルトは**中心 `(cx, cy)`** 配置）。

```python
def shape(xy: Coordinate, path_points: PathPoints, *, style: Style, text: str = , text_style: Style | None = None, is_default_center: bool = False) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 配置アンカー座標（デフォルトは**中心 `(cx, cy)`**）。 |
| `path_points` | `PathPoints` | *必須* | 直線 `(x, y)`、2 次 `(cp, end)`、3 次 `(cp1, cp2, end)` のパス定義リスト。 |
| `is_default_center` | `bool` | `False` | 明示的な `halign`/`valign` 指定時の基準オフセットモードフラグ。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` shield(xy, width, height, *, variant='classic', style, ...)

**中心 `(cx, cy)`** を基準に、セキュリティ・WAF・認証保護を表すシールド（盾）を描画します。

```python
def shield(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: ShieldVariant = classic, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | シールド外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | シールドの幅および高さ。 |
| `variant` | `ShieldVariant` | `'classic'` | シルエット種別（`'classic'`, `'standard'`, `'flat'`, `'heater'`, `'round'`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` star(xy, num_vertex, radius_ext, radius_int, *, style, ...)

**中心 `(cx, cy)`** を基準に、外半径 `radius_ext`・内半径 `radius_int` の星形を描画します（`shape_r` 角丸対応）。

```python
def star(xy: Coordinate, num_vertex: NumVertex, radius_ext: PosFloat, radius_int: PosFloat, *, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 星形の**中心座標 `(cx, cy)`**。 |
| `num_vertex` | `NumVertex` | *必須* | 星の頂点数（`>= 3`）。 |
| `radius_ext / radius_int` | `PosFloat` | *必須* | 外側の頂点半径および内側の谷半径。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` sun(xy, radius, *, variant='rays', num_rays=8, ...)

**中心 `(cx, cy)`** を基準に、周囲に光線を持つ太陽シェイプを描画します。

```python
def sun(xy: Coordinate, radius: PosFloat, *, variant: SunVariant = rays, num_rays: NumVertex = 8, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | 太陽の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 光線先端までの外半径。 |
| `variant` | `SunVariant` | `'rays'` | バリアント（`'rays'`, `'standard'`, `'ring'`, `'beams'`）。 |
| `num_rays` | `NumVertex` | `8` | 周囲の光線の数（`>= 3`）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` tag(xy, width, height, *, variant='angled', mirror=False, hole_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、バージョンやメタデータ表示に適した穴あきラベルタグを描画します。

```python
def tag(xy: Coordinate, width: PosFloat, height: PosFloat, *, variant: TagVariant = angled, mirror: bool = False, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | タグ外接ボックスの**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | タグの幅および高さ。 |
| `variant` | `TagVariant` | `'angled'` | 先端形状バリアント（`'angled'`, `'standard'`, `'chamfered'`, `'beveled'`, `'rounded'`）。 |
| `mirror` | `bool` | `False` | `True` で先端の向きを左右反転します。 |
| `hole_ratio` | `Ratio \| None` | `None` | パンチ穴のサイズ比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` trapezoid(xy, height, bottomedge_width, topedge_width, topedge_x=None, *, hole_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、対称または非対称の台形を描画します（`shape_r`・`hole_ratio` 対応）。

```python
def trapezoid(xy: Coordinate, height: PosFloat, bottomedge_width: PosFloat, topedge_width: PosFloat, topedge_x: float | None = None, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心座標 `(cx, cy)`**。 |
| `height` | `PosFloat` | *必須* | 台形の垂直高さ。 |
| `bottomedge_width / topedge_width` | `PosFloat` | *必須* | 下底および上底の長さ。 |
| `topedge_x` | `float \| None` | `None` | 上底左端の X オフセット（`None` 時は左右対称）。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` triangle(xy, width, height, topvertex_x=None, *, hole_ratio=None, ...)

**中心 `(cx, cy)`** を基準に、二等辺三角形または任意頂点位置の三角形を描画します（`shape_r`・`hole_ratio` 対応）。

```python
def triangle(xy: Coordinate, width: PosFloat, height: PosFloat, topvertex_x: float | None = None, *, hole_ratio: Ratio | None = None, style: Style, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | デフォルトは**中心座標 `(cx, cy)`**。 |
| `width / height` | `PosFloat` | *必須* | 底辺の幅および垂直高さ。 |
| `topvertex_x` | `float \| None` | `None` | 左端からの頂点 X オフセット（`None` 時は `width / 2` の二等辺三角形）。 |
| `hole_ratio` | `Ratio \| None` | `None` | 中空くり抜き比率 `(0.0, 1.0)`。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |

---

## `def` wedge(xy, radius, *, style, width=None, angle_start=0, angle_end=360, ...)

**中心 `(cx, cy)`** を基準に、扇形ウェッジまたはドーナツ弧セクター（リング幅 `width`）を描画します。

```python
def wedge(xy: Coordinate, radius: PosFloat, *, style: Style, width: PosFloat | None = None, angle_start: Angle = 0, angle_end: Angle = 360, text: str = , text_style: Style | None = None) -> None
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `Coordinate` | *必須* | ウェッジ円の**中心座標 `(cx, cy)`**。 |
| `radius` | `PosFloat` | *必須* | 外周半径。 |
| `width` | `PosFloat \| None` | `None` | ドーナツ弧のリング幅（`None` 時は中心まで塗りつぶし）。 |
| `angle_start / angle_end` | `Angle` | `0 / 360` | 反時計回りの開始角度・終了角度（度）。 |
| `style` | `Style` | *必須* | キーワード専用の図形 `Style`（塗り色・枠線・角丸 `shape_r`・回転 `angle`・位置揃え）。 |
| `text` | `str` | `''` | 図形内部に中央配置するオプション文字列（`\n` 改行対応）。 |
| `text_style` | `Style \| None` | `None` | ラベル文字列用のオプション `Style`（例: `Styles.WhiteBold`）。 |
