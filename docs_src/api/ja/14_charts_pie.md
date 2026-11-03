# drawlib.charts.pie（円・ドーナツグラフ）

スライスの切り出し強調（`explode`）、ドーナツ中央の KPI テキスト（`center_text`）、狭小スライス（4% 未満）のラベル自動抑制、分離型凡例描画を備えた 2D 円・ドーナツグラフビルダーです。`drawlib.charts.pie` からインポートします（`from drawlib.charts.pie import PieChart, Slice`）。

```drawlib align=center code=fold file=14_charts_pie_hero.png caption="切り出し強調付きの円グラフと中央KPIテキスト付きドーナツグラフ"
from drawlib.canvas import save, setup
from drawlib.charts.pie import PieChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((31.5, 29.0), width=53.0, height=50.0, style=card_style)
rectangle((88.5, 29.0), width=53.0, height=50.0, style=card_style)

# Left: Solid Exploded PieChart
solid = PieChart(
    radius=12.5,
    width=48.0,
    height=37.0,
    hole_ratio=0.0,
    title="Exploded Budget Share",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    value_format="{:.0f}%",
)
solid.add_slice("AI Core", 44.0, style=Styles.PrimaryFlat, explode=1.8)
solid.add_slice("Infra", 32.0, style=Styles.PrimaryNeutral)
solid.add_slice("Tooling", 24.0, style=Styles.SecondaryNeutral)
solid.draw(xy=(7.5, 13.5))
solid.draw_legend(xy=(12.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.0)

# Right: Donut PieChart with Center KPI Badge
donut = PieChart(
    radius=12.5,
    width=48.0,
    height=37.0,
    hole_ratio=0.60,
    center_text="99.9%\nSLA",
    center_text_style=Styles.BlackBold.patch(text_size=10.5),
    title="Donut Traffic Mix",
    title_style=Styles.BlackBold.patch(text_size=11.5),
    value_text_style=Styles.BlackBold.patch(text_size=10.0),
    value_format="{:.0f}%",
)
donut.add_slice("Edge", 48.0, style=Styles.PrimaryFlat)
donut.add_slice("API", 32.0, style=Styles.PrimaryNeutral)
donut.add_slice("Batch", 20.0, style=Styles.SecondaryNeutral)
donut.draw(xy=(64.5, 13.5))
donut.draw_legend(xy=(71.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.2)

save()
```

---

## `type` DrawDirection

`Slice.draw_ratio`（`0.0`〜`1.0`）と組み合わせて円・ドーナツスライスの部分描画方向を指定するリテラル型です。

```python
DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| リテラル値 | `PieChart` での動作 |
| :--- | :--- |
| `"left_to_right"` | 開始角から `sweep_angle * draw_ratio` にわたって角度方向に扇形を展開します（`draw_ratio >= 0.6` でラベル表示、デフォルト）。 |
| `"bottom_to_top"` | 内側ホール端（`hole_ratio`）から外周 `radius` に向かって放射状に扇形を拡大します。 |

---

## `type` FormatterType

スライス上の構成比ラベル（`PieChart.value_format`）のフォーマットを指定するユニオン型です。

```python
FormatterType = str | Callable[[float], str] | None
```

- **`str`**: スライスの百分率（`0.0`〜`100.0`）を受け取る Python フォーマット文字列（デフォルトは `"{:.1f}%"`）。
- **`Callable[[float], str]`**: 百分率 `float` を受け取り文字列を返すカスタム関数（例: `lambda pct: f"{pct:.0f}%"`）。
- **`None`**: コンパクトな自動パーセンテージ表記を使用します。

---

## `class` PieChart

全体（$100\%$）に対する各要素の構成比を可視化する 2D 円グラフ・ドーナツグラフビルダーです。

- **座標アンカー**: `draw(xy=..., align="bottom_left")` のデフォルトは**左下 `(x0, y0)`**（`align="center"` 指定時は中心）。
- **狭小スライスの文字重なり防止**: 合計の $4\%$ 未満のスライスでは、ラベル同士の衝突を防ぐためインライン数値ラベル（`value_text_style`）が自動的に省略されます。

```python
class PieChart:
    def __init__(
        self,
        *,
        radius: float = 20.0,
        hole_ratio: float = 0.0,
        start_angle: float = 90.0,
        clockwise: bool = True,
        value_text_style: Style | None = None,
        value_format: FormatterType = "{:.1f}%",
        center_text: str = "",
        center_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
        width: float | None = None,
        height: float | None = None,
    ) -> None: ...
```

### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `radius` | `float` | `20.0` | キャンバス単位での円・ドーナツの外周半径。 |
| `hole_ratio` | `float` | `0.0` | 内側ホールの半径比率（`0.0` で通常の円グラフ、`0.1`〜`0.9` でドーナツリング）。 |
| `start_angle` | `float` | `90.0` | 最初のスライスの開始角度（度数法。`90.0` が 12 時方向、`0.0` が 3 時方向）。 |
| `clockwise` | `bool` | `True` | `True` で時計回り、`False` で反時計回りにスライスを配置します。 |
| `value_text_style` | `Style \| None` | `None` | スライス上の構成比ラベル（$4\%$ 以上）の文字スタイル。`None` の場合は非表示。 |
| `value_format` | `FormatterType` | `"{:.1f}%"` | スライス構成比（`0.0`〜`100.0`）を受け取るフォーマット文字列または関数。 |
| `center_text` | `str` | `""` | ドーナツ中央ホール内に描画する KPI テキスト（`\n` 改行対応、`hole_ratio > 0` が必要）。 |
| `center_text_style` | `Style \| None` | `None` | `center_text` を描画するための文字スタイル。`None` の場合は非表示。 |
| `background_style` | `Style \| None` | `None` | チャート外枠カードのスタイル。`None` の場合は非表示。 |
| `title` | `str` | `""` | コンテナ上部に表示するチャートタイトル文字列。 |
| `title_style` | `Style \| None` | `None` | `title` を描画するための文字スタイル。`None` の場合は非表示。 |
| `width` | `float \| None` | `None` | コンテナ幅の明示的な上書き指定。`None` の場合は `radius` と `title` から自動算出。 |
| `height` | `float \| None` | `None` | コンテナ高さの明示的な上書き指定。`None` の場合は `radius` と `title` から自動算出。 |

### メソッド・プロパティ

#### `add_slice`

```python
def add_slice(
    self,
    name: str,
    value: float,
    style: Style,
    explode: float = 0.0,
    legend_text_style: Style | None = None,
    *,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: DrawDirection = "left_to_right",
) -> Slice
```

比率スライスを追加し、変更可能な [Slice](#slice) インスタンスを返します。`explode > 0.0` を指定すると二等分角方向に沿って外側へオフセット強調されます。

#### `draw`

```python
def draw(
    self,
    xy: tuple[float, float] = (0.0, 0.0),
    *,
    radius: float | None = None,
    width: float | None = None,
    height: float | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> None
```

基準座標 `xy`（デフォルトは**左下 `(x0, y0)`**、`align="center"` で中心）に円・ドーナツグラフを描画します。一時的な `radius`・`width`・`height`・`scale` 上書きに対応します。

#### `draw_legend`

```python
def draw_legend(
    self,
    xy: tuple[float, float],
    text_style: Style,
    orientation: Literal["vertical", "horizontal"] = "vertical",
    swatch_width: float = 2.4,
    swatch_height: float = 1.2,
    item_gap: float = 4.0,
    *,
    scale: float = 1.0,
) -> None
```

座標 `xy` に独立したスライス凡例を描画します（`"vertical"` または `"horizontal"`）。

#### `get_size`

```python
def get_size(self) -> tuple[float, float]
```

この円形チャートコンテナの全体寸法 `(width, height)` を算出して返します。

#### `slices` *(property)*

```python
@property
def slices(self) -> list[Slice]
```

登録済みの [Slice](#slice) インスタンスのリストコピーを返します。

---

## `class` Slice

[PieChart](#piechart) 内の単一スライス（扇形）を表す変更可能なデータモデルです。

```python
class Slice:
    def __init__(
        self,
        name: str,
        value: float,
        style: Style,
        explode: float = 0.0,
        legend_text_style: Style | None = None,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None: ...
```

### パラメータ・属性

| パラメータ／属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | **必須** | `draw_legend()` に表示されるスライス名。 |
| `value` | `float` | **必須** | 扇形の角度比率を決定する非負の数値。 |
| `style` | `Style` | **必須** | スライスの塗りおよび枠線 [Style](05_styles_and_types.md)。 |
| `explode` | `float` | `0.0` | 中心から外側へ切り出すオフセット距離（キャンバス単位、`0.0` で密着）。 |
| `legend_text_style` | `Style \| None` | `None` | `draw_legend()` におけるこのスライス専用の文字スタイル上書き指定。 |
| `show` | `bool` | `True` | 全スライスの合計（100%）を維持したまま表示／非表示を切り替えます。 |
| `draw_ratio` | `float` | `1.0` | アニメーション用の部分描画比率（`0.0`〜`1.0`）。 |
| `draw_direction` | `DrawDirection` | `"left_to_right"` | 部分描画方向（`"left_to_right"` 角度スイープ／`"bottom_to_top"` 放射拡大）。 |
