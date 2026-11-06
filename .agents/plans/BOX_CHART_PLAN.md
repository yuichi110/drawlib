# BoxChart（箱ひげ図・ストリッププロット）設計・実装計画書

- **作成日**: 2026-11-06
- **対象モジュール**: `drawlib.charts.box`（内部実装: `src/drawlib/_charts/box_chart/`）
- **ステータス**: Completed（実装・検証完了）

---

## 1. 背景と目的

技術検証レポート・SRE ベンチマーク・LLM 応答性能評価などのエンジニアリング文書において、現在の `drawlib.charts`（8サブモジュール・9クラス）には**「カテゴリ × 数値分布（バラつき・四分位・テールレイテンシ）」**を標準表現するチャートが不足している。

本計画では、以下の3つの課題を解決するため **10個目のチャートクラス（9個目のサブモジュール）として `drawlib.charts.box.BoxChart`** を追加する。

1. **平均値（`BarChart`）では消えてしまう分散・テールレイテンシの可視化**:
   API レイテンシやクエリ応答時間では、平均値以上に中央値（p50）・四分位範囲（IQR）・p95 / 最大値の跳ね幅がアーキテクチャ選定の根拠となる。`Axis` の線形／対数スケール（`scale="log"`）と組み合わせることで、桁違いのテールスパイクも正確に表現できる。
2. **少〜中サンプル検証（$N = 5 \sim 30$）における「箱ひげ ＋ ストリップ重ね描き」の標準サポート**:
   実務の PoC・ベンチマークで最も多い $N = 5 \sim 30$ 規模の計測では、箱ひげ単体ではサンプル数の少なさが隠れ、ストリップ単体では中央値・四分位が読み取りづらい。1つの `BoxChart` クラスで **箱ひげ図・ストリッププロット・両者のオーバーレイ** をシームレスに切り替えられる設計とする。
3. **AI エージェントによる手組み崩れの防止**:
   公式の分布チャートを提供することで、AI エージェントが `ScatterChart` へ無理にカテゴリを詰め込んだり、`rectangle()` と `circle()` の座標を手計算して不自然な図を生成する問題を防ぐ。

---

## 2. コア設計方針

### 2.1. 1クラス3表現（`show_box` / `show_points`）＋ シリーズ単位の上書き
`BoxChart` コンストラクタでチャート全体のデフォルトを指定しつつ、`add_series()` ごとにも個別上書きできる2階層設計とする。

| モード | 設定 | 主な用途 |
| :--- | :--- | :--- |
| **箱ひげ図 (Box Plot)** | `show_box=True, show_points=False` *(デフォルト)* | 中〜大サンプル数、または集計済みパーセンタイル（`BoxStats`）の分布比較 |
| **ストリップ / ジッタープロット (Strip Plot)** | `show_box=False, show_points=True` | 少数サンプルの全実測値分布、または `jitter=0.0` による1次元ストリップ表示 |
| **箱ひげ ＋ 実測点オーバーレイ** | `show_box=True, show_points=True` | $N = 5 \sim 30$ のベンチマーク計測（要約統計量と実測密度を同時提示） |

- **外れ値の二重描画防止**:
  - `show_box=True, show_points=False` かつ `show_outliers=True` の場合、ひげの外側にある外れ値のみマーカー描画する。
  - `show_points=True` の場合は全生データ点をストリップ描画するため、外れ値マーカーの重複描画は自動的に抑止する（ただし `outlier_style` が明示指定されている場合は、外れ値に該当する点へ `outlier_style` を優先適用する）。
- **バリデーション**:
  - シリーズの実効設定が `show_box=False` かつ `show_points=False` になる場合は、意図しない空白描画を防ぐため `ValueError` を送出する。

### 2.2. 「生データ配列」と「集計済み `BoxStats`」のハイブリッド入力
`add_series(name, data, style, ...)` の `data` はカテゴリ順のシーケンスとし、要素ごとに以下を受け付ける。

1. **生データ配列 (`Sequence[float]`)**:
   - Pure Python（標準ライブラリのみ）で四分位数・ひげ範囲・外れ値・平均値を自動算出する。
   - 四分位・パーセンタイル計算は `statistics.quantiles(..., method="inclusive")` と同等の線形補間（NumPy / Pandas のデフォルト `"linear"` と一致）を実装し、$N = 1, 2, 3$ の少サンプルでも安全に動作させる（$N = 1$ の場合は `min = q1 = median = q3 = max = mean = x`）。
2. **集計済み統計オブジェクト (`BoxStats`)**:
   - BigQuery や Cloud Monitoring 等から取得した `p5 / p25 / p50 / p75 / p95` や `min / q1 / median / q3 / max` を生データなしで直接描画できる。
   - オプションで `outliers: Sequence[float]`、`mean: float`、およびオーバーレイ用の `points: Sequence[float]` も保持できる。
3. **欠損カテゴリ許容 (`None` または空配列 `[]`)**:
   - 特定シリーズで一部カテゴリの計測値が存在しない場合、例外にせず当該スロットの描画を安全にスキップする。

### 2.3. ひげ（Whisker）の3モードと平均値マーカー（`show_mean`）
生データ配列からの統計量算出において、用途に応じた3種類の `whisker_mode` と補助統計量を提供する。

- **`whisker_mode: WhiskerMode = "iqr"`（デフォルト / Tukey 方式）**:
  - `iqr_k: float = 1.5` を用い、$[Q_1 - k \cdot \text{IQR},\ Q_3 + k \cdot \text{IQR}]$ 内に収まる最小／最大実測値までひげを伸ばす。範囲外の実測値は `outliers` に分類する。
- **`whisker_mode = "min_max"`（最小〜最大値）**:
  - 外れ値を分離せず、実測値の最小値〜最大値（0〜100パーセンタイル）までひげを伸ばす（`outliers = []`）。
- **`whisker_mode = "percentile"`（パーセンタイル指定 / テールレイテンシ向け）**:
  - `whisker_percentiles: tuple[float, float] = (5.0, 95.0)`（例: p5〜p95、p10〜p90、p1〜p99）の位置までひげを伸ばし、さらに外側の極端値を `outliers` に分類する。
- **平均値マーカー (`show_mean: bool = False`)**:
  - 有効時、算術平均（`mean`）の位置にマーカー（デフォルト `mean_shape="rhombus"`）を描画し、歪んだ分布（ロングテール）における「中央値と平均値の乖離」を一目で示せるようにする。

### 2.4. プロセス間・アニメーション間で不変な決定論的 Jitter
- Python 組込みの `hash()` は `PYTHONHASHSEED` によりプロセスごとに値が変わるため使用しない。
- グローバルな `random` モジュール状態も一切変更せず、`(jitter_seed, series_idx, category_idx)` から固定整数ミキシング（例: `(jitter_seed * 1_000_003 + series_idx * 10_007 + category_idx * 1_009) & 0xFFFFFFFF`）でローカルの `random.Random` インスタンスを生成する。
- **メリット**:
  1. OS・Python プロセスを問わず常に完全同一の座標に点が配置され、Git 管理下の画像キャッシュ差分が発生しない。
  2. `drawlib.anim` やスライドのステップビルドで特定シリーズを `series.show = False` に切り替えても、他シリーズ・他カテゴリの点の位置が一切シャッフルされない。
  3. `jitter = 0.0` を指定すれば、横散らしのない一直線の1次元ストリッププロットになる。

### 2.5. 単一 `Style` からの高コントラスト自動導出（50%+ Neutral 準拠）
`Styles.PrimaryNeutral` / `Styles.Neutral`（淡色塗り＋濃色枠線）、`Styles.PrimaryFlat`（濃色ベタ塗り＋枠線なし）、`Styles.PrimaryOutline`（透明塗り＋色枠線）のいずれを `style` に1つ渡すだけでも美しく視認性の高い描画になるよう、未指定のサブスタイルを自動導出する。

| 描画パーツ | 個別上書き引数 | 未指定（`None`）時の自動導出ルール |
| :--- | :--- | :--- |
| **箱 (Q1–Q3)** | `style` | `ensure_shape_style(style)`（`box_r > 0` かつ `style.shape_r is None` なら角丸 `box_r` を適用） |
| **ひげ・キャップ** | `whisker_style` | `style.line_color` → 可視の `style.shape_line_color` → `style.shape_fill_color` の優先順で実線スタイルを導出（`PrimaryFlat` でも透明にならず主色で描画） |
| **中央値ライン** | `median_style` | 箱の塗りが濃色ベタ塗り（`PrimaryFlat` 等の低輝度塗りかつ枠線なし）の場合は白系高コントラスト線（太さ `1.4x`、最小 `2.0pt`）、それ以外（`PrimaryNeutral` 等）は `text_color` / `shape_line_color` 系の濃色太線を導出 |
| **データ点 (Strip)** | `point_style` | `PrimaryNeutral` 等の淡色箱の上でも埋もれないよう、`text_color` / `line_color` / `shape_fill_color` から濃色アクセントを抽出し、塗りアルファ `0.72` ＋ 実線枠（濃色箱重なり時は白縁取り）を導出 |
| **外れ値マーカー** | `outlier_style` | `point_style` と同系色の輪郭強調マーカー（中抜きまたは半透明塗り）を導出 |
| **平均値マーカー** | `mean_style` | 中央値ラインと同系色（濃色箱の上では白塗り＋濃色枠、淡色箱の上では濃色塗り＋白枠）のマーカーを導出 |

### 2.6. 既存 `AxisChartMixin`・軸スケーリング・アニメーション仕様との完全統一
- **`AxisChartMixin` 継承**: `x_axis`, `y_axis`, `configure_x_axis()`, `configure_y_axis()`, `value_axis`, `category_axis`, `get_size()`, `draw()`, `draw_legend()` を `BarChart` と完全に同じインターフェースで提供する。
- **`is_bar=False` による分布向けスケーリング**:
  - `calculate_axis_range_and_ticks(..., is_bar=False)` を使用し、正の値であっても強制的に `0` 起点には固定せず、データの最小〜最大値（ひげ・外れ値・生データ点・平均値の全範囲）に合わせて Nice Numbers で適切にズームする（ゼロ起点にしたい場合は `configure_y_axis(min_value=0)` で指定可能）。
  - `configure_y_axis(scale="log")`（横向き時は `configure_x_axis(scale="log")`）で対数軸がそのまま動作する。
- **アニメーション対応 (`show`, `draw_ratio`, `draw_direction`)**:
  - 自動軸範囲計算は `show=False` や `draw_ratio < 1.0` のシリーズも含めた **全登録データ（100%状態）** から算出し、アニメーション中の軸ガタつきを防止する。
  - **数値軸方向の展開**（縦向き時の `"bottom_to_top"` / 横向き時の `"left_to_right"`、デフォルト）: 各箱・ひげ・データ点が中央値（`median`）から上下（左右）に向かって `draw_ratio` に応じて展開する。
  - **カテゴリ軸方向の順次出現**（縦向き時の `"left_to_right"` / 横向き時の `"bottom_to_top"`）: カテゴリ `0` から `N-1` へ順番に出現する（`BarChart` と同一挙動）。

---

## 3. 公開 API 仕様 (`drawlib.charts.box`)

### 3.1. エクスポート一覧
- **`src/drawlib/charts/__init__.py`**:
  - `_LAZY_MODULES` および `__all__` に `"box"` を追加。
- **`src/drawlib/charts/box.py`**:
  ```python
  __all__ = [
      "Axis",
      "BoxChart",
      "BoxStats",
      "DrawDirection",
      "FormatterType",
      "LegendPosition",
      "Orientation",
      "PointShape",
      "ScaleType",
      "Series",
      "WhiskerMode",
  ]
  ```
- **`src/drawlib/_charts/_common/_types.py`**:
  ```python
  WhiskerMode = Literal["iqr", "min_max", "percentile"]
  ```

### 3.2. `BoxStats` クラス
```python
class BoxStats:
    """Pre-aggregated or computed summary statistics for a single box-plot category slot."""

    @validate_call
    def __init__(
        self,
        *,
        min: float,  # noqa: A002
        q1: float,
        median: float,
        q3: float,
        max: float,  # noqa: A002
        mean: float | None = None,
        outliers: Sequence[float] | None = None,
        points: Sequence[float] | None = None,
    ) -> None: ...

    @classmethod
    @validate_call
    def from_values(
        cls,
        values: Sequence[float],
        *,
        whisker_mode: Literal["iqr", "min_max", "percentile"] = "iqr",
        iqr_k: float = 1.5,
        whisker_percentiles: tuple[float, float] = (5.0, 95.0),
    ) -> BoxStats: ...
```
- **制約**: `min <= q1 <= median <= q3 <= max` および全数値が有限値（`math.isfinite`）であることを検証し、違反時は `ValueError` を送出する。`from_values()` に空配列を渡した場合も `ValueError` を送出する（チャート側の空カテゴリスキップは `_series.py` で事前にハンドリング）。

### 3.3. `BoxChart` コンストラクタとメソッド
```python
class BoxChart(AxisChartMixin):
    """Configurable container and builder for box plots, strip/jitter plots, and hybrid overlays."""

    @validate_call
    def __init__(
        self,
        *,
        axis_line_style: Style,
        width: float = 68.0,
        height: float = 44.0,
        categories: list[str] | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        show_box: bool = True,
        show_points: bool = False,
        show_outliers: bool = True,
        show_mean: bool = False,
        whisker_mode: Literal["iqr", "min_max", "percentile"] = "iqr",
        iqr_k: float = 1.5,
        whisker_percentiles: tuple[float, float] = (5.0, 95.0),
        box_width_ratio: float = 0.65,
        cap_width_ratio: float = 0.45,
        box_r: float = 0.0,
        jitter: float = 0.45,
        jitter_seed: int = 42,
        point_radius: float = 0.58,
        point_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "circle",
        outlier_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "circle",
        mean_shape: Literal["circle", "square", "rhombus", "triangle", "none"] = "rhombus",
        axis_text_style: Style | None = None,
        grid_style: Style | None = None,
        value_text_style: Style | None = None,
        value_format: FormatterType = None,
        background_style: Style | None = None,
        title: str = "",
        title_style: Style | None = None,
    ) -> None: ...
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `axis_line_style` | `Style` | **必須** | 座標軸ベースラインのスタイル（他チャートと共通の必須アンカー） |
| `width` / `height` | `float` | `68.0` / `44.0` | チャート全体のバウンディングボックス寸法 |
| `categories` | `list[str] \| None` | `None` | カテゴリ軸ラベル一覧（未指定時はデータ長から空文字スロット生成） |
| `orientation` | `"vertical"` \| `"horizontal"` | `"vertical"` | 分布の描画方向（縦向き／横向き） |
| `show_box` | `bool` | `True` | 箱・ひげ・中央値ラインのデフォルト表示フラグ |
| `show_points` | `bool` | `False` | 生データ点（ストリップ／ジッター）のデフォルト表示フラグ |
| `show_outliers` | `bool` | `True` | `show_box=True` かつ `show_points=False` 時の外れ値マーカー表示フラグ |
| `show_mean` | `bool` | `False` | 平均値マーカーの表示フラグ |
| `whisker_mode` | `WhiskerMode` | `"iqr"` | 生データ配列からのひげ算出方式（`"iqr"`, `"min_max"`, `"percentile"`） |
| `iqr_k` | `float` | `1.5` | `whisker_mode="iqr"` 時の IQR 倍率（`>= 0.0`） |
| `whisker_percentiles` | `tuple[float, float]` | `(5.0, 95.0)` | `whisker_mode="percentile"` 時の下限・上限パーセンタイル |
| `box_width_ratio` | `float` | `0.65` | カテゴリスロット幅に対する箱クラスタ全体の幅比率（`(0.0, 1.0]`） |
| `cap_width_ratio` | `float` | `0.45` | 個々の箱幅に対するひげ先端キャップ線の幅比率（`[0.0, 1.0]`、`0.0` でキャップなし） |
| `box_r` | `float` | `0.0` | 箱（Q1–Q3 矩形）の4隅の角丸半径 |
| `jitter` | `float` | `0.45` | 個々の箱スロット幅に対する点の散らし幅比率（`[0.0, 1.0]`、`0.0` で中央整列） |
| `jitter_seed` | `int` | `42` | ジッター座標生成の固定乱数シード |
| `point_radius` | `float` | `0.58` | ストリップ点・外れ値・平均値マーカーの基本半径 |
| `point_shape` | `PointShape` | `"circle"` | ストリップ点のマーカー形状 |
| `outlier_shape` | `PointShape` | `"circle"` | 外れ値のマーカー形状 |
| `mean_shape` | `PointShape` | `"rhombus"` | 平均値のマーカー形状 |
| `value_text_style` | `Style \| None` | `None` | 指定時、各箱の中央値（`median`）ラベルを描画（`None` なら非表示） |
| `value_format` | `FormatterType` | `None` | `value_text_style` 用の数値フォーマット（例: `"{:.0f}ms"`） |

#### `add_series()` メソッド
```python
@validate_call
def add_series(
    self,
    name: str,
    data: Sequence[Sequence[float] | BoxStats | None],
    style: Style,
    legend_text_style: Style | None = None,
    *,
    show_box: bool | None = None,
    show_points: bool | None = None,
    show_outliers: bool | None = None,
    show_mean: bool | None = None,
    median_style: Style | None = None,
    whisker_style: Style | None = None,
    point_style: Style | None = None,
    outlier_style: Style | None = None,
    mean_style: Style | None = None,
    point_radius: float | None = None,
    point_shape: Literal["circle", "square", "rhombus", "triangle", "none"] | None = None,
    jitter: float | None = None,
    show: bool = True,
    draw_ratio: float = 1.0,
    draw_direction: Literal["bottom_to_top", "left_to_right"] | None = None,
) -> Series: ...
```

### 3.4. コード記述イメージ

#### ① PoC ベンチマーク（箱ひげ ＋ ストリップ重ね描き）
```python
from drawlib.charts.box import BoxChart
from drawlib.styles import Styles

chart = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["① Baseline", "② Streaming", "③ Blocking"],
    width=86.0,
    height=50.0,
    show_box=True,
    show_points=True,
    jitter=0.42,
    jitter_seed=42,
    box_r=0.6,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="LLM Response Latency Distribution (N=12 per mode)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
)
chart.add_series("Cold Cache", [cold_a, cold_b, cold_c], style=Styles.SecondaryNeutral)
chart.add_series("Warm Cache", [warm_a, warm_b, warm_c], style=Styles.PrimaryNeutral)
chart.configure_y_axis(unit="ms", label="Latency (ms)")
chart.draw(xy=(8.0, 10.0))
chart.draw_legend(xy=(24.0, 62.5), text_style=Styles.DarkBold.patch(text_size=10.0), orientation="horizontal")
```

#### ② Cloud Monitoring / BigQuery 集計値からの描画（`BoxStats` ＋ 対数軸）
```python
from drawlib.charts.box import BoxChart, BoxStats
from drawlib.styles import Styles

chart = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["API Gateway", "Auth Service", "Vector Search"],
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
)
chart.add_series(
    "Latency (p5–p95)",
    [
        BoxStats(min=8.0, q1=12.0, median=16.0, q3=24.0, max=65.0, outliers=[140.0]),
        BoxStats(min=11.0, q1=15.0, median=21.0, q3=30.0, max=88.0),
        BoxStats(min=35.0, q1=52.0, median=74.0, q3=120.0, max=480.0, outliers=[920.0, 1250.0]),
    ],
    style=Styles.PrimaryNeutral,
)
chart.configure_y_axis(scale="log", unit="ms")
chart.draw(xy=(8.0, 8.0))
```

---

## 4. 内部アーキテクチャ・描画レイヤー設計

### 4.1. ディレクトリ・モジュール構成
```text
src/drawlib/
├── charts/
│   ├── __init__.py          # "box" の遅延ロード登録
│   └── box.py               # 公開ファサード (BoxChart, BoxStats, Series, Axis, ...)
└── _charts/
    ├── __init__.py          # BoxChart, BoxStats, WhiskerMode 再エクスポート
    ├── _common/
    │   └── _types.py        # WhiskerMode リテラル型追加
    └── box_chart/
        ├── __init__.py      # BoxChart, BoxStats, Series 公開
        ├── _stats.py        # BoxStats クラス、線形補間パーセンタイル計算、決定論的ジッター生成
        ├── _series.py       # Series コンテナ（カテゴリ別 BoxStats 正規化・シリーズ別上書き設定保持）
        ├── _chart.py        # BoxChart(AxisChartMixin) 本体
        └── _renderer.py     # 縦向き・横向き描画エンジン、スタイル自動導出、部分描画アニメーション
```

### 4.2. 描画 Z オーダー（背面 → 前面）
1. **Layer 0**: `background_style` 外枠カード矩形
2. **Layer 1**: 数値軸グリッド線（`grid_style`）および目盛りラベル（`axis_text_style` / `tick_label_style`）
3. **Layer 2**: ひげ（Q1 → `min`、Q3 → `max` の2線分 — 箱の内部を貫通させないことで半透明塗りの箱でも線が透けないようにする）＋ ひげ先端 T キャップ線
4. **Layer 3**: 箱本体（Q1〜Q3 矩形、`box_r` 対応；`q1 == q3` の縮退ケースでも最小厚みまたは線分として安全に描画）
5. **Layer 4**: 中央値ライン（`median` 線分、箱の両端幅いっぱい）
6. **Layer 5**: 平均値マーカー（`show_mean=True` 時、カテゴリ・シリーズスロット中心軸上）
7. **Layer 6**: 外れ値マーカー（`show_points=False` & `show_outliers=True` 時）またはストリップ／ジッターデータ点（`show_points=True` 時）
8. **Layer 7**: 中央値テキストバッジ（`value_text_style` 指定時）
9. **Layer 8**: X/Y 軸ベースライン（`axis_line_style`）、カテゴリラベル、X/Y 軸タイトルラベル（`Axis.label`）、チャートタイトル（`title`）

### 4.3. マージン計算の改善
`BarChart` のマージン計算に `ScatterChart` と同様の **軸タイトル（`x_axis.label` / `y_axis.label`）余白加算** を組み込み、`configure_y_axis(label="Latency (ms)")` 指定時に目盛り数値と軸タイトルが重ならないようにする。また、複数シリーズグループ化時にはスロット間に視覚的なセパレーション（クラスタ内シリーズ間隔 `gap_ratio`）を設け、隣接する箱やストリップ点同士が接触しないようレイアウトする。

---

## 5. 実装フェーズ計画

| フェーズ | 対象ファイル | 作業内容 |
| :--- | :--- | :--- |
| **Phase 1: コア実装** | `src/drawlib/_charts/_common/_types.py`<br>`src/drawlib/_charts/box_chart/*`<br>`src/drawlib/_charts/__init__.py`<br>`src/drawlib/charts/box.py`<br>`src/drawlib/charts/__init__.py` | `BoxStats` 統計エンジン、決定論的ジッター、`Series`、`BoxChart`、縦横レンダラ、自動スタイル導出、対数軸・アニメーション対応の実装 |
| **Phase 2: 単体テスト & 静的解析** | `tests/drawlib/charts/test_box_chart.py` | 統計計算テスト（$N=1,2,3,4,20$、`iqr`/`min_max`/`percentile`、`BoxStats` バリデーション）、ジッター再現性・`show=False` 不変性テスト、3表示モード・縦横・複数シリーズ・対数軸・アニメーション描画テスト追加。`./dcli code-check all` 完全パス確認 |
| **Phase 3: AI ルール更新** | `src/drawlib/_rules/charts/box.md`<br>`src/drawlib/_rules/charts/overview.md`<br>`src/drawlib/_rules/{api,cli,agent_instruction,overview,anim_guide}.md`<br>`src/drawlib/_builder/rules_builder.py`<br>`src/drawlib/_cli/commands/rules.py`<br>`.agents/rules/drawlib.md` | `lib-charts-box` ルールトピック新設・CLI 登録、チャート総数（9 → 10 クラス / 8 → 9 サブモジュール）およびチートシートの同期 |
| **Phase 4: ドキュメント（Dogfooding）** | `docs_src/site/{en,ja}/05_charts/box.md`<br>`docs_src/site/{en,ja}/05_charts/overview.md`<br>`docs_src/site/{en,ja}/08_animations/charts.md`<br>`docs_src/site/{en,ja}/navbar.md`<br>`docs_src/api/{en,ja}/18b_charts_box.md`<br>`docs_src/api/{en,ja}/00_overview.md`<br>`tests/drawlib/doc_builder/test_api_docs_completeness.py`<br>`docs_src/architecture/en/03_domain_subsystems/02_high_level_components.md` | 公式ドキュメント（日英完全パリティ、Top Hero + 実践チュートリアル）、API カタログリファレンス（既存 `19_diagrams_*` URL を壊さない `18b_charts_box.md` 配置＋完全性テスト登録）、アーキテクチャ仕様書の更新（※未リリース版の場合は `docs.md` 指針に従い Upcoming 注記を判断） |
| **Phase 5: 視覚検証 & 全体ビルド検証** | `.drawlib/scratch/*`（グリッド検証用）<br>`docs/`（ビルド成果物） | `drawlib show ... -g` によるグリッド幾何レビュー、`view_file` マルチモーダル検査、`./dcli test all`、`./dcli docs build` & `./dcli docs serve --check`、ブラウザ HTML フォントサイズ整合性確認 |

---

## 6. 検証・品質・セキュリティ計画 (Verification & Security Plan)

### 6.1. 自動テスト・品質ゲート
1. **統計・境界値ユニットテスト (`./dcli test target charts`)**:
   - $N = 1$（全統計量が同一値）、$N = 2, 3$（線形補間）、すべて同一値（$\text{IQR} = 0$ の箱縮退ケース）、負数を含む分布、外れ値あり／なしの検証。
   - `whisker_mode` 3種（`"iqr"`, `"min_max"`, `"percentile"`）の境界値検証。
   - `BoxStats` の順序逆転（`q1 > median` 等）や `NaN` / `inf` 入力に対する `ValueError` 検証。
   - 空配列 `[]` / `None` カテゴリスロット混在時の安全なスキップ検証。
   - `jitter_seed` 同一時の完全一致検証、および先行シリーズを `show=False` にした際の後続シリーズ点座標の不変性検証。
2. **API ドキュメント完全性・リンク検証 (`./dcli test target doc-builder`)**:
   - `test_api_docs_completeness.py` により `drawlib.charts.box` の全公開シンボル（`__all__`）が `en/`・`ja/` 双方の API リファレンスで漏れなく解説されていることを機械検証。
3. **静的解析 (`./dcli code-check all`)**:
   - `ruff`（lint / format, 120文字制限）、`ty`（静的型検査）、および `docstring` チェッカー（`@validate_call` 付与関数の docstring に内部型エイリアスを含めないこと）をエラーゼロで通過。

### 6.2. 3段階マルチモーダル視覚検証
1. **Stage 1（構造・タイポグラフィ確認）**: `text_size >= 10.0`、50%+ Neutral カラートークン比率、Top Hero（Lines 6–15, `code=fold`）配置を確認。
2. **Stage 2（`-g` グリッド微細幾何確認）**: 縦向き・横向き、複数シリーズグループ、箱＋ストリップ重ね描き、対数軸、平均値マーカーの各画像で文字切れ・ラベル重なり・箱からの点のはみ出しがないことを `view_file` で目視確認。
3. **Stage 3（HTML ページ全体確認）**: `./dcli docs build site` & `api` 実行後、`./dcli docs serve site --check` / `./dcli docs serve api --check` でリンク整合性を検証し、HTML 上の `16px` 本文と図内ラベルのサイズバランスを確認。

### 6.3. セキュリティ・安全性検証 (Security Verification)
本機能はオフライン／ローカル完結の Pure Python ベクター描画コンポーネントであり、Web バックエンド認証・セッション管理・SQL データベース・ファイルアップロード処理は含まない（該当 Web セキュリティ項目は対象外）。以下の適用対象項目を計画・検証する。
- **厳格な入力バリデーション (`@validate_call` & 値域検査)**: すべての公開 API 引数に対して Pydantic `@validate_call` による型検証を行い、`NaN` / `Inf`、不正な比率（`box_width_ratio`, `cap_width_ratio`, `jitter`）、不正なパーセンタイル範囲、逆転した `BoxStats` 統計量をフェイルセーフに `ValueError` で拒否する。
- **安全な乱数分離とコード実行排除**: ジッター計算はローカルの `random.Random` インスタンスに閉じ込め、動的コード評価（`eval` / `exec`）や安全でないデシリアライズを一切使用しない。
- **新規外部依存パッケージなし**: Python 標準ライブラリ（`math`, `random`）と既存の `drawlib` 内部プリミティブのみで実装し、サプライチェーンリスクを追加しない。
- **ローカルプレビューのバインド制限と出力エスケープ**: ドキュメント検証時のローカルサーバー（`./dcli docs serve`）は `127.0.0.1` / `localhost` のみにバインドし（`0.0.0.0` 禁止）、ドキュメント HTML 生成時も既存の安全なエスケープパイプライン（生 DOM `innerHTML` 不使用・外部 CDN 不使用）を維持する。

### 6.4. Automated Security Check
- **Security Scanner**: 新規作成ファイルすべてに対して `run-security-scanner` を実行し、脆弱性（XSS、インジェクション、ハードコード秘密情報等）がないことを確認する。検出時は修正して記録する。
- **Security Audit**: 設計レベルのセキュリティ確認（入力バリデーション、乱数分離、依存関係）を実施し、`generate-security-audit-report` スキルに沿って監査結果を記録する。

