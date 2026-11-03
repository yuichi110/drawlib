# drawlib.charts.line（折れ線グラフ）

直線ポリラインまたは滑らかな 3 次スプライン曲線、頂点マーカー形状、線種パターン、分離型凡例描画を備えた 2D 折れ線グラフビルダーです。`drawlib.charts.line` からインポートします（`from drawlib.charts.line import Axis, LineChart, Series`）。

```drawlib align=center code=fold file=12_charts_line_hero.png caption="直線セグメント＋SLO閾値の折れ線グラフと滑らかなスプライン曲線の多系列折れ線グラフ"
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((31.5, 29.0), width=53.0, height=50.0, style=card_style)
rectangle((88.5, 29.0), width=53.0, height=50.0, style=card_style)

# Left: Straight Segments with Vertex Markers & SLO Ceiling
left = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["00h", "06h", "12h", "18h"],
    width=48.0,
    height=37.0,
    smooth=False,
    show_points=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="p95 Latency & SLO (ms)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
left.add_series("Primary", [24.0, 32.0, 64.0, 40.0], style=Styles.PrimaryFlat, line_width=2.2, point_shape="square")
left.add_series("SLO (80ms)", [80.0, 80.0, 80.0, 80.0], style=Styles.DarkFlat, line_width=1.8, line_style="dashdot", point_shape="none")
left.configure_y_axis(min_value=0.0, max_value=100.0, tick_step=50.0)
left.draw(xy=(7.5, 13.5))
left.draw_legend(xy=(14.0, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.5)

# Right: Smooth Spline Multi-Series Growth
right = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=48.0,
    height=37.0,
    smooth=True,
    show_points=True,
    point_size=0.75,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Smooth Spline MAU (k)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
right.add_series("2025", [36.0, 68.0, 52.0, 84.0], style=Styles.SecondaryNeutral, line_width=2.0, line_style="dashed")
right.add_series("2026", [44.0, 58.0, 128.0, 148.0], style=Styles.PrimaryFlat, line_width=2.4)
right.configure_y_axis(min_value=0.0, max_value=160.0, tick_step=80.0, unit="k")
right.draw(xy=(64.5, 13.5))
right.draw_legend(xy=(76.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

save()
```

---

## `class` Axis

直交座標チャートの座標軸（数値軸・カテゴリ軸）を表し、線形／対数スケーリング、値域、目盛り、グリッド線、書式設定を制御します。

```python
class Axis:
    def __init__(
        self,
        scale: ScaleType = "linear",
        min_value: float | None = None,
        max_value: float | None = None,
        ticks: list[float] | None = None,
        tick_step: float | None = None,
        format: FormatterType = None,
        unit: str = "",
        label: str = "",
        show_grid: bool = True,
        grid_style: Style | None = None,
        show_axis_line: bool = True,
        line_style: Style | None = None,
        show_ticks: bool = True,
        tick_label_style: Style | None = None,
        label_style: Style | None = None,
    ) -> None: ...
```

### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `scale` | `"linear" \| "log"` | `"linear"` | 線形スケールまたは常用対数（`log10`）スケール。 |
| `min_value` | `float \| None` | `None` | 軸の最小値。`None` の場合は自動算出されます。 |
| `max_value` | `float \| None` | `None` | 軸の最大値。`None` の場合は自動算出されます。 |
| `ticks` | `list[float] \| None` | `None` | 自動目盛り生成を上書きする明示的な目盛り値リスト。 |
| `tick_step` | `float \| None` | `None` | 線形スケールにおける目盛り間隔ステップ。 |
| `format` | `FormatterType` | `None` | 目盛りラベルおよび頂点値ラベルに使用するフォーマット文字列または `Callable[[float], str]`。 |
| `unit` | `str` | `""` | フォーマット済み目盛りラベルの末尾に付与する単位（例: `"ms"`, `"k"`）。 |
| `label` | `str` | `""` | 軸タイトル文字列。 |
| `show_grid` | `bool` | `True` | チャートの `grid_style` 指定時にグリッド線を描画するか。 |
| `grid_style` | `Style \| None` | `None` | この軸専用のグリッド線 [Style](05_styles_and_types.md) 上書き指定。 |
| `show_axis_line` | `bool` | `True` | 軸のベースライン線を描画するか。 |
| `line_style` | `Style \| None` | `None` | この軸専用のベースライン [Style](05_styles_and_types.md) 上書き指定。 |
| `show_ticks` | `bool` | `True` | 目盛りラベルを描画するか。 |
| `tick_label_style` | `Style \| None` | `None` | 目盛りラベル専用の [Style](05_styles_and_types.md) 上書き指定。 |
| `label_style` | `Style \| None` | `None` | 軸タイトル `label` 用の [Style](05_styles_and_types.md) 上書き指定。 |

### メソッド

#### `configure`

```python
def configure(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
    label_style: Style | None = None,
) -> None
```

複数の軸設定オプションをインプレースで一括更新します。

#### `format_value`

```python
def format_value(self, value: float) -> str
```

数値 `value` を `format` と `unit` に従って表示用文字列へ変換します。

---

## `type` DrawDirection

`Series.draw_ratio`（`0.0`〜`1.0`）と組み合わせて折れ線アニメーションの進行方向を指定するリテラル型です。

```python
DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| リテラル値 | `LineChart` での動作 |
| :--- | :--- |
| `"left_to_right"` | 弧長に沿って左から右へ連続的に線を伸ばし、到達した頂点からマーカーを表示します（デフォルト）。 |
| `"bottom_to_top"` | すべての頂点をベースラインから目標の `y` 値へ向かって同時に上昇させます。 |

---

## `type` FormatterType

軸目盛りおよび頂点数値ラベル（`y_axis.format`）のフォーマットを指定するユニオン型です。

```python
FormatterType = str | Callable[[float], str] | None
```

- **`str`**: Python フォーマット文字列（例: `"{:.1f}"`, `"${:,.0f}"`）。
- **`Callable[[float], str]`**: `float` を受け取り `str` を返すカスタム関数。
- **`None`**: コンパクトな自動数値フォーマット。

---

## `type` LegendPosition

凡例配置プリセット識別子を表すリテラル型です。

```python
LegendPosition = Literal["top", "bottom", "right", "none", "auto"]
```

- 補足: `LineChart` では [`LineChart.draw_legend()`](#linechart) を用いてキャンバス上の任意座標に凡例を描画します。

---

## `class` LineChart

順序付きカテゴリ上の直線セグメント（`smooth=False`）および滑らかなスプライン曲線（`smooth=True`）を描画する 2D 折れ線グラフビルダーです。

- **座標アンカー**: `draw(xy=..., align="bottom_left")` のデフォルトは**左下 `(x0, y0)`**（`align="center"` 指定時は中心）。
- **頂点値の書式設定**: `value_text_style` 指定時、頂点ラベルは `y_axis.format_value(v)`（`configure_y_axis(format=..., unit=...)` で設定）を用いてフォーマットされます。

```python
class LineChart:
    def __init__(
        self,
        *,
        axis_line_style: Style,
        categories: list[str],
        width: float = 80.0,
        height: float = 50.0,
        show_points: bool = True,
        point_shape: PointShape = "circle",
        point_size: float = 0.7,
        smooth: bool = False,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None: ...
```

### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `axis_line_style` | `Style` | **必須** | 直交座標軸のベースラインおよび目盛り線の必須スタイル。 |
| `categories` | `list[str]` | **必須** | 水平 X 軸に沿った順序付きカテゴリ名リスト。 |
| `width` | `float` | `80.0` | キャンバス単位でのチャート全体の幅。 |
| `height` | `float` | `50.0` | キャンバス単位でのチャート全体の高さ。 |
| `show_points` | `bool` | `True` | 各頂点座標にマーカーを描画するか。 |
| `point_shape` | `PointShape` | `"circle"` | デフォルトの頂点マーカー形状（`"circle"`, `"square"`, `"rhombus"`, `"triangle"`, `"none"`）。 |
| `point_size` | `float` | `0.7` | キャンバス単位でのデフォルトマーカー半径（または半幅）。 |
| `smooth` | `bool` | `False` | `True` の場合、頂点間（3 点以上）を滑らかなスプライン曲線で補間します。 |
| `axis_text_style` | `Style \| None` | `None` | Y 軸目盛り値および X 軸カテゴリ名の文字スタイル。`None` の場合は非表示。 |
| `grid_style` | `Style \| None` | `None` | 水平 Y 軸グリッド線のスタイル。`None` の場合は非表示。 |
| `value_text_style` | `Style \| None` | `None` | 頂点マーカー上部に描画する数値ラベルの文字スタイル。`None` の場合は非表示。 |
| `background_style` | `Style \| None` | `None` | チャート外枠カードのスタイル。`None` の場合は非表示。 |
| `title` | `str` | `""` | コンテナ上部に表示するチャートタイトル文字列。 |
| `title_style` | `Style \| None` | `None` | `title` を描画するための文字スタイル。`None` の場合は非表示。 |

### メソッド・プロパティ

#### `add_series`

```python
def add_series(
    self,
    name: str,
    values: list[float],
    style: Style,
    line_width: float = 2.0,
    line_style: LineStyle = "solid",
    point_shape: PointShape | None = None,
    point_size: float | None = None,
    legend_text_style: Style | None = None,
    *,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: DrawDirection = "left_to_right",
) -> Series
```

折れ線系列を追加し、変更可能な [Series](#series) インスタンスを返します。`point_shape="none"` を渡すと、その系列の頂点マーカーと `value_text_style` 数値ラベルの両方が抑制されるため、水平な目標値・SLO 閾値ラインの表現に適しています。

#### `configure_x_axis`

```python
def configure_x_axis(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
) -> Axis
```

水平 X 軸のパラメータを一括設定し、`x_axis` を返します。

#### `configure_y_axis`

```python
def configure_y_axis(
    self,
    scale: ScaleType | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
    ticks: list[float] | None = None,
    tick_step: float | None = None,
    format: FormatterType = None,
    unit: str | None = None,
    label: str | None = None,
    show_grid: bool | None = None,
    grid_style: Style | None = None,
    show_axis_line: bool | None = None,
    line_style: Style | None = None,
    show_ticks: bool | None = None,
    tick_label_style: Style | None = None,
) -> Axis
```

垂直 Y 軸のスケール・値域・目盛り・書式・タイトルを一括設定し、`y_axis` を返します。

#### `draw`

```python
def draw(
    self,
    xy: tuple[float, float] = (0.0, 0.0),
    *,
    width: float | None = None,
    height: float | None = None,
    align: Literal["bottom_left", "center"] = "bottom_left",
    scale: float = 1.0,
) -> None
```

基準座標 `xy`（デフォルトは**左下 `(x0, y0)`**、`align="center"` で中心）に折れ線グラフを描画します。

#### `draw_legend`

```python
def draw_legend(
    self,
    xy: tuple[float, float],
    text_style: Style,
    orientation: Orientation = "vertical",
    swatch_width: float = 2.4,
    swatch_height: float = 1.2,
    item_gap: float = 4.0,
    *,
    scale: float = 1.0,
) -> None
```

座標 `xy` に独立した系列凡例を描画します（`"vertical"` または `"horizontal"`）。

#### `get_size`

```python
def get_size(self) -> tuple[float, float]
```

チャートコンテナの `(width, height)` をキャンバス単位で返します。

#### `series` *(property)*

```python
@property
def series(self) -> list[Series]
```

登録済みの [Series](#series) インスタンスのリストコピーを返します。

---

## `type` LineStyle

系列のストローク線種パターン（`add_series(..., line_style=...)`）を指定するリテラル型です。

```python
LineStyle = Literal["solid", "dashed", "dotted", "dashdot"]
```

| リテラル値 | 説明 |
| :--- | :--- |
| `"solid"` | 連続した実線（デフォルト）。 |
| `"dashed"` | 破線（`-- -- --`）。前年比較などのベースライン表現に適しています。 |
| `"dotted"` | 点線（`· · · ·`）。補助系列やレプリカ系列に適しています。 |
| `"dashdot"` | 一点鎖線（`-·-·`）。SLA／SLO 上限などの閾値ラインに適しています。 |

---

## `type` PointShape

系列の各頂点に描画するマーカー形状を指定するリテラル型です。

```python
PointShape = Literal["circle", "square", "rhombus", "triangle", "none"]
```

| リテラル値 | 説明 |
| :--- | :--- |
| `"circle"` | 円形マーカー（デフォルト）。 |
| `"square"` | 正方形マーカー。 |
| `"rhombus"` | 45° 回転したひし形（ダイヤ）マーカー。 |
| `"triangle"` | 上向き正三角形マーカー。 |
| `"none"` | 頂点マーカーを非表示にします（その系列の `value_text_style` ラベルも抑制されます）。 |

---

## `class` Series

[LineChart](#linechart) に登録された折れ線データ系列を表す変更可能なデータモデルです。

```python
class Series:
    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        line_width: float = 2.0,
        line_style: LineStyle = "solid",
        point_shape: PointShape = "circle",
        point_size: float = 0.7,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "left_to_right",
    ) -> None: ...
```

### パラメータ・属性

| パラメータ／属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | **必須** | `draw_legend()` に表示される系列名。 |
| `values` | `list[float]` | **必須** | `LineChart.categories` に対応する数値リスト。 |
| `style` | `Style` | **必須** | 線およびマーカーの [Style](05_styles_and_types.md)（`line_color` / `shape_fill_color`）。 |
| `line_width` | `float` | `2.0` | 折れ線またはスプライン曲線の線幅。 |
| `line_style` | `LineStyle` | `"solid"` | 線種パターン（`"solid"`, `"dashed"`, `"dotted"`, `"dashdot"`）。 |
| `point_shape` | `PointShape` | `"circle"` | 各頂点に描画するマーカー形状。 |
| `point_size` | `float` | `0.7` | キャンバス単位でのマーカー半径（または半幅）。 |
| `legend_text_style` | `Style \| None` | `None` | `draw_legend()` におけるこの系列専用の文字スタイル上書き指定。 |
| `show` | `bool` | `True` | 全データの軸スケールを維持したまま表示／非表示を切り替えます。 |
| `draw_ratio` | `float` | `1.0` | アニメーション用の部分描画比率（`0.0`〜`1.0`）。 |
| `draw_direction` | `DrawDirection` | `"left_to_right"` | 部分描画の進行方向（`"left_to_right"` または `"bottom_to_top"`）。 |
