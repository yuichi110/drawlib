# drawlib.charts.bar（棒グラフ）

縦棒（カラム）・横棒グラフを構築するモジュールで、集合棒（グループ）・積み上げ棒（スタック）・外端角丸・向きに応じた軸プロパティ・分離型凡例描画をサポートします。`drawlib.charts.bar` からインポートします（`from drawlib.charts.bar import Axis, BarChart, Series`）。

```drawlib align=center code=fold file=11_charts_bar_hero.png caption="縦向きの集合棒グラフと横向きの積み上げ棒グラフのレイアウト"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=120, height=58)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
rectangle((31.5, 29.0), width=53.0, height=50.0, style=card_style)
rectangle((88.5, 29.0), width=53.0, height=50.0, style=card_style)

# Left: Vertical Grouped BarChart
v_bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Q1", "Q2", "Q3", "Q4"],
    width=48.0,
    height=37.0,
    orientation="vertical",
    bar_mode="group",
    bar_width_ratio=0.72,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Vertical Grouped ($M)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
v_bar.add_series("2025", [22.0, 28.0, 32.0, 38.0], style=Styles.SecondaryNeutral)
v_bar.add_series("2026", [30.0, 41.0, 48.0, 58.0], style=Styles.PrimaryFlat)
v_bar.draw(xy=(7.5, 13.5))
v_bar.draw_legend(xy=(19.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")

# Right: Horizontal Stacked BarChart
h_bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["Cache", "API", "DB"],
    width=48.0,
    height=37.0,
    orientation="horizontal",
    bar_mode="stack",
    bar_width_ratio=0.62,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="Horizontal Stacked (%)",
    title_style=Styles.BlackBold.patch(text_size=11.5),
)
h_bar.add_series("CPU", [35.0, 46.0, 50.0], style=Styles.PrimaryFlat)
h_bar.add_series("RAM", [30.0, 26.0, 28.0], style=Styles.PrimaryNeutral)
h_bar.add_series("I/O", [15.0, 16.0, 14.0], style=Styles.SecondaryNeutral)
h_bar.configure_x_axis(min_value=0.0, max_value=100.0, tick_step=50.0, unit="%")
h_bar.draw(xy=(64.5, 13.5))
h_bar.draw_legend(xy=(72.5, 8.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal", item_gap=2.2)

save()
```

---

## `class` Axis

[BarChart](#barchart)・[BoxChart](18b_charts_box.md)・[LineChart](12_charts_line.md)・[AreaChart](13_charts_area.md)・[ScatterChart](16_charts_scatter.md) で共有される直交座標軸（数値軸・カテゴリ軸）モデルです。線形／対数スケール、値域、目盛り生成、グリッド線の表示、ラベルの書式設定を制御します。

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
| `scale` | `"linear" \| "log"` | `"linear"` | 線形スケール（キリの良い数値間隔）または常用対数（`log10`）スケール。 |
| `min_value` | `float \| None` | `None` | 軸の最小値。`None` の場合はデータから自動算出されます。 |
| `max_value` | `float \| None` | `None` | 軸の最大値。`None` の場合はデータから自動算出されます。 |
| `ticks` | `list[float] \| None` | `None` | 自動目盛り生成を上書きする明示的な目盛り位置リスト。 |
| `tick_step` | `float \| None` | `None` | 線形スケールにおける隣接目盛り間のステップ間隔。 |
| `format` | `FormatterType` | `None` | 目盛りラベルのフォーマット文字列（例: `"{:.1f}%"`, `"${:,.0f}"`）または `Callable[[float], str]`。 |
| `unit` | `str` | `""` | フォーマット済み目盛りラベルの末尾に付与する単位サフィックス（例: `"ms"`, `"%"`）。 |
| `label` | `str` | `""` | 軸タイトルの説明テキスト。 |
| `show_grid` | `bool` | `True` | チャートの `grid_style` 指定時にこの軸のグリッド線を描画するか。 |
| `grid_style` | `Style \| None` | `None` | この軸専用のグリッド線 [Style](05_styles_and_types.md) 上書き指定。 |
| `show_axis_line` | `bool` | `True` | 軸のベースライン線を描画するか。 |
| `line_style` | `Style \| None` | `None` | この軸専用のベースライン [Style](05_styles_and_types.md) 上書き指定。 |
| `show_ticks` | `bool` | `True` | この軸の目盛りラベルを描画するか。 |
| `tick_label_style` | `Style \| None` | `None` | 目盛りラベル専用の [Style](05_styles_and_types.md) 上書き指定（回転は `text_angle` で設定）。 |
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

`None` 以外の軸設定オプションをインプレースで一括更新します。

#### `format_value`

```python
def format_value(self, value: float) -> str
```

数値 `value` を `format` および `unit` に基づいて表示用ラベル文字列へ変換します。

---

## `class` BarChart

縦棒（カラム）および横棒グラフを構築・描画するコンテナ／ビルダーです。

- **座標アンカー**: `draw(xy=..., align="bottom_left")` のデフォルトは**左下 `(x0, y0)`**（`align="center"` 指定時は全体境界ボックスの中心）。

```python
class BarChart:
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 60.0,
        height: float = 40.0,
        categories: list[str] | None = None,
        orientation: Orientation = "vertical",
        bar_mode: Mode = "group",
        bar_width_ratio: float = 0.7,
        bar_r: float = 0.0,
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None: ...
```

### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `axis_line_style` | `Style` | **必須** | 直交座標軸のベースラインおよび目盛り線の必須スタイル。 |
| `width` | `float` | `60.0` | キャンバス単位でのチャート全体の幅。 |
| `height` | `float` | `40.0` | キャンバス単位でのチャート全体の高さ。 |
| `categories` | `list[str] \| None` | `None` | カテゴリ軸（縦棒時は `x_axis`、横棒時は `y_axis`）に並べるカテゴリ名リスト。 |
| `orientation` | `Orientation` | `"vertical"` | 棒の伸びる方向（`"vertical"` 縦棒または `"horizontal"` 横棒）。 |
| `bar_mode` | `Mode` | `"group"` | 複数系列の配置モード（`"group"` 並列グループまたは `"stack"` 累積スタック）。 |
| `bar_width_ratio` | `float` | `0.7` | 各カテゴリスロットに対する棒の太さ比率（`0.1`〜`1.0`）。 |
| `bar_r` | `float` | `0.0` | 棒の外側先端 2 角のみに適用される角丸半径。 |
| `axis_text_style` | `Style \| None` | `None` | 目盛り値およびカテゴリ名の文字スタイル。`None` の場合は非表示。 |
| `grid_style` | `Style \| None` | `None` | 数値軸グリッド線のスタイル。`None` の場合は非表示。 |
| `value_text_style` | `Style \| None` | `None` | 棒の先端・内部に描画する数値ラベルの文字スタイル。`None` の場合は非表示。 |
| `value_format` | `FormatterType` | `None` | 棒の数値ラベル用フォーマット文字列（例: `"{:.1f}M"`）または呼び出し可能オブジェクト。 |
| `background_style` | `Style \| None` | `None` | チャート外枠カードの背景・枠線スタイル。`None` の場合は非表示。 |
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
    legend_text_style: Style | None = None,
    *,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: DrawDirection | None = None,
) -> Series
```

データ系列を追加し、変更可能な [Series](#series) インスタンスを返します。`draw_direction=None` の場合、縦棒では `"bottom_to_top"`、横棒では `"left_to_right"` が自動選択されます。

#### `category_axis` *(property)*

```python
@property
def category_axis(self) -> Axis
```

向きに応じたカテゴリ軸（`"vertical"` 時は `x_axis`、`"horizontal"` 時は `y_axis`）の [Axis](#axis) を返します。

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

水平 X 軸のパラメータを一括設定し、更新後の [Axis](#axis) を返します。

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

垂直 Y 軸のパラメータを一括設定し、更新後の [Axis](#axis) を返します。

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

基準座標 `xy`（`align="bottom_left"` で**左下 `(x0, y0)`**、`align="center"` で中心）に棒グラフを描画します。一時的なサイズ上書きや比例スケーリング `scale` に対応します。

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

座標 `xy`（`"vertical"` は左上起点、`"horizontal"` は左中央起点）に独立した凡例を描画します。`show=False` の系列は自動的に除外されます。

#### `get_size`

```python
def get_size(self) -> tuple[float, float]
```

スケール変換前のチャートコンテナの `(width, height)` をキャンバス単位で返します。

#### `series` *(property)*

```python
@property
def series(self) -> list[Series]
```

登録済みの [Series](#series) インスタンスのリストコピーを返します。

#### `value_axis` *(property)*

```python
@property
def value_axis(self) -> Axis
```

向きに応じた数値軸（`"vertical"` 時は `y_axis`、`"horizontal"` 時は `x_axis`）の [Axis](#axis) を返します。

---

## `type` DrawDirection

アニメーション用の `draw_ratio`（`0.0`〜`1.0`）と組み合わせて部分描画の進行方向を指定するリテラル型です。

```python
DrawDirection = Literal["bottom_to_top", "left_to_right"]
```

| リテラル値 | 縦棒（`vertical`）での動作 | 横棒（`horizontal`）での動作 |
| :--- | :--- | :--- |
| `"bottom_to_top"` | すべての棒がベースラインから上方向へ同時に伸長（`v * draw_ratio`）。 | 下側のカテゴリから上側へ順番に棒が出現。 |
| `"left_to_right"` | 左側のカテゴリから右側へ順番に棒が出現。 | すべての棒がベースラインから右方向へ同時に伸長（`v * draw_ratio`）。 |

---

## `type` FormatterType

軸目盛り（`Axis.format`）および棒ラベル（`BarChart.value_format`）の数値フォーマットを指定するユニオン型です。

```python
FormatterType = str | Callable[[float], str] | None
```

- **`str`**: Python のフォーマット文字列（例: `"{:.1f}M"`, `"${:,.0f}"`, `"{:.0f}%"`）。
- **`Callable[[float], str]`**: 数値 `float` を受け取り表示文字列を返すカスタム関数。
- **`None`**: Drawlib 標準のコンパクト数値フォーマットを使用します。

---

## `type` LegendPosition

チャートレイアウト補助用の凡例配置プリセットを表すリテラル型です。

```python
LegendPosition = Literal["top", "bottom", "right", "none", "auto"]
```

- 補足: `BarChart` ではダッシュボード上で自由な座標に配置できるよう [`BarChart.draw_legend()`](#barchart) で明示座標に凡例を描画します。

---

## `type` Mode

各カテゴリスロット内での複数系列の配置モード（`BarChart.bar_mode`）を表すリテラル型です。

```python
Mode = Literal["group", "stack"]
```

| リテラル値 | 説明 |
| :--- | :--- |
| `"group"` | 各カテゴリスロット内で系列の棒を横並びに配置します（デフォルト）。 |
| `"stack"` | 系列の棒を累積的に積み上げ、合計量と内訳構成比を同時に表現します。 |

---

## `type` Orientation

棒の成長方向（`BarChart.orientation`）および凡例アイテムの並び方向（`draw_legend`）を表すリテラル型です。

```python
Orientation = Literal["vertical", "horizontal"]
```

| リテラル値 | 説明 |
| :--- | :--- |
| `"vertical"` | 縦棒が `y_axis` に沿って上方向へ伸びます。凡例では上から下へ並びます。 |
| `"horizontal"` | 横棒が `x_axis` に沿って右方向へ伸びます。凡例では左から右へ並びます。 |

---

## `class` Series

[BarChart](#barchart) に登録された単一データ系列を表す変更可能なデータモデルです。

```python
class Series:
    def __init__(
        self,
        name: str,
        values: list[float],
        style: Style,
        legend_text_style: Style | None = None,
        *,
        show: bool = True,
        draw_ratio: float = 1.0,
        draw_direction: DrawDirection = "bottom_to_top",
    ) -> None: ...
```

### パラメータ・属性

| パラメータ／属性 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | `str` | **必須** | `draw_legend()` に表示される系列名。 |
| `values` | `list[float]` | **必須** | `BarChart.categories` に対応する数値リスト。 |
| `style` | `Style` | **必須** | この系列の棒に適用する塗り・枠線 [Style](05_styles_and_types.md)。 |
| `legend_text_style` | `Style \| None` | `None` | `draw_legend()` におけるこの系列専用の文字スタイル上書き指定。 |
| `show` | `bool` | `True` | 全データセットの軸スケールを維持したまま系列の表示／非表示を切り替えます。 |
| `draw_ratio` | `float` | `1.0` | キーフレームアニメーション用の部分描画比率（`0.0`〜`1.0`）。 |
| `draw_direction` | `DrawDirection` | `"bottom_to_top"` | 部分空間描画の進行方向（`"bottom_to_top"` または `"left_to_right"`）。 |
