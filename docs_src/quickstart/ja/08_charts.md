# 8. 定量チャート：10種の純粋 Python グラフ

技術白書・ベンチマークレポート・設計レビューでは、構成図だけでなく定量的なデータによる裏付けが不可欠です。`drawlib.charts` は Drawlib の描画エンジン上に構築された **全10種の純粋 Python チャート** を提供します。すべてのチャートが **左下アンカー `Bottom-Left (x0, y0)`**（`align="bottom_left"`）を既定としているため、`SmartArts`・アイコン・注釈矢印と同一キャンバス上で精密に組み合わせて配置できます。

```drawlib align=center code=fold file=charts_bar_line_ja.png caption="図 8.1: 定量ダッシュボード — BarChart によるスループット比較と LineChart による遅延推移"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.charts.line import LineChart
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=152, height=62)

card_bg = Styles.White.patch(shape_r=2.0, shape_line_color=Colors.Gray3)
rectangle((40.0, 31.0), width=68.0, height=50.0, style=card_bg)
rectangle((112.0, 31.0), width=68.0, height=50.0, style=card_bg)

bar = BarChart(
    axis_line_style=Styles.MutedDashed,
    categories=["白書", "サイト", "API辞書", "スライド"],
    width=62.0,
    height=38.0,
    bar_mode="group",
    bar_width_ratio=0.68,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    value_text_style=Styles.DarkBold.patch(text_size=10.0),
    value_format="{:.0f}",
    title="ビルド処理性能 (ページ / 秒)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
bar.add_series("v0.3.0 従来版", [18.0, 24.0, 21.0, 29.0], style=Styles.SecondaryNeutral)
bar.add_series("v0.3.10 高速版", [42.0, 56.0, 49.0, 64.0], style=Styles.PrimaryFlat)
bar.configure_y_axis(min_value=0.0, max_value=80.0, tick_step=20.0)
bar.draw(xy=(9.0, 14.0))
bar.draw_legend(
    xy=(15.0, 10.0),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=4.5,
)

line = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["10頁", "25頁", "50頁", "100頁", "200頁"],
    width=62.0,
    height=38.0,
    smooth=False,
    show_points=True,
    point_size=0.75,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="差分レンダリング遅延 (ms)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
line.add_series(
    "初回",
    [14.0, 22.0, 34.0, 52.0, 72.0],
    style=Styles.Muted6Flat,
    line_width=1.9,
    line_style="dashed",
    point_shape="square",
)
line.add_series(
    "v0.3.10",
    [6.0, 8.0, 11.0, 15.0, 21.0],
    style=Styles.PrimaryFlat,
    line_width=2.4,
    point_shape="circle",
)
line.add_series(
    "SLO上限",
    [60.0, 60.0, 60.0, 60.0, 60.0],
    style=Styles.Danger,
    line_width=1.5,
    line_style="dotted",
    point_shape="none",
)
line.configure_y_axis(min_value=0.0, max_value=80.0, tick_step=20.0, format="{:.0f}", unit="ms")
line.draw(xy=(81.0, 14.0))
line.draw_legend(
    xy=(84.5, 10.0),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=3.5,
)

save()
```

## 8.1 技術文書において `drawlib.charts` が Matplotlib に勝る理由

多言語対応の技術文書に外部の Matplotlib スクリプトを持ち込むと、フォントの不統一・煩雑な `rcParams` ボイラープレート・日本語の文字化け（豆腐 `□□□`）・他の構成図と組み合わせられない単体画像化といった問題が発生します。`drawlib.charts` はこれら4つの課題を根本から解決します。

- **完全に統一されたデカルト座標系**: すべてのチャートが同じキャンバス上の `xy=(x0, y0)` に直接描画されるため、複数チャートの並列ダッシュボードや `KpiCards`・注釈カードとの統合レイアウトが1つの座標グリッド上で完結します。
- **`GoogleStyles` デザイントークンと日本語フォントの自動継承**: プロジェクト共通の `Styles`・`Colors` および言語別フォント設定（`ja/styles.py`）をそのまま継承するため、`rcParams` の設定コードは一切不要です。
- **Presence-Based スタイル設計と分離型凡例**: オプションのスタイル引数（`grid_style`、`value_text_style`、`background_style`）を `None` のままにすれば不要な装飾が自動的に省略され、`chart.draw_legend(xy=...)` や `chart.draw_colorbar(xy=...)` によってデータ領域と重ならない正確な位置へ凡例を配置できます。
- **軸スケールを固定したアニメーション対応（`show` & `draw_ratio`）**: `series.show = False` や `series.draw_ratio`（`0.0`〜`1.0`）を変化させても全データセット基準の軸目盛りが固定されるため、棒の伸長や折れ線のスイープ描画が滑らかに作成できます。

## 8.2 全10種チャートカタログと使い分け

9つのサブモジュール（`drawlib.charts.*`）で提供される **全10種のチャートクラス** はすべて **左下アンカー `Bottom-Left (x0, y0)`** を既定とし、`align="center"` や比例スケーリング `scale: float = 1.0` にも対応しています。

| # | チャートクラス | サブモジュール | `.draw(xy=...)` 既定アンカー | 主なモードと機能 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **`BarChart`** | `drawlib.charts.bar` | **Bottom-Left** `(x0, y0)` | 縦棒／横棒、`"group"`／`"stack"`、角丸 `bar_r`、数値ラベル、`"log"` 対数軸 |
| **2** | **`BoxChart`** | `drawlib.charts.box` | **Bottom-Left** `(x0, y0)` | 生データ配列または `BoxStats`、`"iqr"`／`"percentile"` ひげ、`show_points` ジッター点群 |
| **3** | **`LineChart`** | `drawlib.charts.line` | **Bottom-Left** `(x0, y0)` | 複数系列折れ線・`smooth=True` スプライン、頂点マーカー、`point_shape="none"` 閾値線 |
| **4** | **`AreaChart`** | `drawlib.charts.area` | **Bottom-Left** `(x0, y0)` | `"overlap"` 重ね合わせ／`"stack"` 積み上げ面グラフ、透過度 `fill_alpha` 制御 |
| **5** | **`PieChart`** | `drawlib.charts.pie` | **Bottom-Left** `(x0, y0)` | 円グラフ（`hole_ratio=0.0`）とドーナツ型（`hole_ratio=0.5..0.7` + `center_text` 中央指標） |
| **6** | **`RadarChart`** | `drawlib.charts.radar` | **Bottom-Left** `(x0, y0)` | 多軸 `"polygon"`／`"circle"` レーダーチャート（`levels`、能力比較マトリクス） |
| **7** | **`ScatterChart`** | `drawlib.charts.scatter` | **Bottom-Left** `(x0, y0)` | 2次元 `(x, y)` 相関プロットおよび `Point(x, y, radius=...)` によるバブルチャート |
| **8** | **`GanttChart`** | `drawlib.charts.gantt` | **Bottom-Left** `(x0, y0)` | `Section`・進捗付き `Task`・`Milestone`・`Marker`・`Dependency` 矢印を備えた工程表 |
| **9** | **`HeatmapChart`** | `drawlib.charts.heatmap` | **Bottom-Left** `(x0, y0)` | 2次元強度マトリクス（`min_style`..`max_style`）、自動文字コントラスト、`draw_colorbar` |
| **10** | **`HeatmapOverlay`** | `drawlib.charts.heatmap` | **Bottom-Left** `(x0, y0)` | 地図や構成図上に重ねる空間密度 `Spot` オーバーレイ（`"smooth"`／`"contour"` 等高線） |

### 8.2.1 カテゴリ・統計分布・2次元マトリクス系チャート

- **`BarChart` & `BoxChart`**: 縦横の向きに自動追従する `value_axis` / `category_axis`（および `configure_x_axis(...)` / `configure_y_axis(...)`）を備え、線形目盛りだけでなく桁数の大きく異なるレイテンシ比較に適した常用対数軸（`scale="log"`）も1行で有効化できます。
- **`HeatmapChart` & `HeatmapOverlay`**: 数値強度をカラースケール（`min_style=Styles.White, max_style=Styles.PrimaryFlat` または複数段階の `styles=[...]`）へ変換します。`HeatmapChart` は背景濃度に応じてセル文字色を自動反転（`auto_contrast_text=True`）し、`HeatmapOverlay` は `GeoMap` や構成図の上に `Spot(x, y, value, radius=...)` のホットスポットを重ね描きします。

### 8.2.2 時系列推移・構成比・スケジュール系チャート

- **`LineChart`・`AreaChart`・`ScatterChart`**: 時系列メトリクス、帯域幅やメモリ消費量の積み上げ推移、2変数＋バブル半径の相関を可視化します。`LineChart` で `point_shape="none"` と `line_style="dotted"` を組み合わせれば、頂点マーカーのないスッキリした SLO 上限ラインを描けます。
- **`PieChart`・`RadarChart`・`GanttChart`**: 構成比の可視化（`PieChart` は `hole_ratio > 0.0` で中央 KPI バッジ付きドーナツグラフとなり、`4%` 未満の微小スライスのラベル重なりも自動抑止）、アーキテクチャ特性の多軸評価（`RadarChart`）、マイルストーン工程管理（`GanttChart`）を担います。

## 8.3 `BoxChart` による統計分布とデータストーリーテリング

説得力のある定量チャートを描く鉄則は **配色のストーリーテリング規律** です。5本のデータ系列に5色の原色を割り当てる虹色グラフは避け、比較対象の旧バージョン・ベースライン・周辺ティアには落ち着いたニュートラル系（`Styles.Neutral`、`Styles.PrimaryNeutral`、`Styles.SecondaryNeutral`、破線の `Styles.Muted`）を使い、強調したいターゲット系列1〜2本だけに `Styles.PrimaryFlat` や `Styles.AccentFlat` を割り当てます。

平均値だけの棒グラフでは見逃されがちなテールレイテンシのばらつきも、`BoxChart` を使えば中央値・四分位範囲（`Q1`〜`Q3`）・ひげ・外れ値を一目で比較できます。生のサンプル配列（`list[float]`）と集計済み統計モデル（`BoxStats`）の両方を直接渡すことができ、濃色ボックス上の白太字中央値ラインも自動導出されます。

```drawlib align=center code=fold file=charts_box_distribution_ja.png caption="図 8.2: BoxChart と BoxStats によるサービス層別のレイテンシ統計分布比較"
from drawlib.canvas import save, setup
from drawlib.charts.box import BoxChart, BoxStats
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

setup(width=148, height=62)

rectangle(
    (74.0, 31.0),
    width=136.0,
    height=50.0,
    style=Styles.White.patch(shape_r=2.0, shape_line_color=Colors.Gray3),
)

box = BoxChart(
    axis_line_style=Styles.MutedDashed,
    categories=["エッジ CDN", "認証 API", "注文エンジン", "ベクトル検索"],
    width=124.0,
    height=38.0,
    box_width_ratio=0.62,
    box_r=0.6,
    show_outliers=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="サービス層別レスポンス時間分布 (ms) — 従来プール vs. v0.3.10 非同期ランタイム",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
box.add_series(
    "従来プール (p5–p95 + p99外れ値)",
    [
        BoxStats(min=5.0, q1=8.0, median=11.0, q3=15.0, max=24.0, outliers=[34.0]),
        BoxStats(min=12.0, q1=18.0, median=24.0, q3=33.0, max=48.0, outliers=[66.0]),
        BoxStats(min=16.0, q1=24.0, median=32.0, q3=44.0, max=62.0, outliers=[76.0]),
        BoxStats(min=22.0, q1=32.0, median=43.0, q3=56.0, max=70.0, outliers=[78.0]),
    ],
    style=Styles.SecondaryNeutral,
)
box.add_series(
    "v0.3.10 非同期ランタイム (注目対象)",
    [
        BoxStats(min=3.0, q1=4.5, median=6.0, q3=8.0, max=12.0, outliers=[16.0]),
        BoxStats(min=6.0, q1=9.0, median=12.0, q3=16.0, max=22.0, outliers=[29.0]),
        BoxStats(min=8.0, q1=12.0, median=15.5, q3=20.0, max=28.0, outliers=[36.0]),
        BoxStats(min=11.0, q1=16.0, median=21.0, q3=27.0, max=38.0, outliers=[46.0]),
    ],
    style=Styles.PrimaryFlat,
)
box.configure_y_axis(
    min_value=0.0,
    max_value=85.0,
    tick_step=20.0,
    format="{:.0f}",
    unit="ms",
)
box.draw(xy=(12.0, 14.0))
box.draw_legend(
    xy=(36.0, 9.8),
    text_style=Styles.DarkBold.patch(text_size=10.0),
    orientation="horizontal",
    item_gap=6.0,
)

save()
```

試行回数 `N = 8..25` 程度の実測ベンチマークでは、生の `list[float]` とともに `show_box=True, show_points=True, jitter=0.42` を指定すれば決定論的シードによるストリップ点群を重ね描きできます。また、`LineChart` や `BarChart` の `draw_ratio`（`0.0`〜`1.0`）を制御すれば、`drawlib.anim` による段階的アニメーションも簡単に構築できます。

```python
from drawlib.canvas import save, setup
from drawlib.charts.line import LineChart
from drawlib.styles import Styles

setup(width=110, height=56)

trend = LineChart(
    axis_line_style=Styles.MutedDashed,
    categories=["T1", "T2", "T3", "T4", "T5"],
    width=90.0,
    height=38.0,
    smooth=True,
    axis_text_style=Styles.Muted.patch(text_size=10.0),
    grid_style=Styles.MutedThin,
    title="カナリアロールアウト処理性能推移 (60% 描画フレーム)",
    title_style=Styles.DarkBold.patch(text_size=11.5),
)
trend.add_series("従来版", [40, 42, 41, 43, 42], style=Styles.SecondaryNeutral, line_style="dashed")
# T1..T5 の全体軸スケールを固定したまま、左から60%地点まで曲線をスイープ描画
focal = trend.add_series("v0.3.10 カナリア", [42, 58, 74, 89, 96], style=Styles.PrimaryFlat, draw_ratio=0.6)

trend.configure_y_axis(min_value=0, max_value=100, tick_step=25, unit="k rps")
trend.draw(xy=(10.0, 10.0))
save()
```

各チャートの軸設定・凡例・カラーバー・コンストラクタ引数の詳細は、`uv run drawlib rules show lib-charts-overview`（または `lib-charts-bar`、`lib-charts-box`、`lib-charts-line`、`lib-charts-pie`、`lib-charts-gantt`、`lib-charts-heatmap`）で確認できます。
