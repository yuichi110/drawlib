# 第9章: チャート描画（定量データの可視化）

`drawlib.charts` は、プロジェクトのロードマップ、スケジュール管理、パフォーマンスメトリクスを美麗にレンダリングするチャートモジュールです。すべてのチャートの `.draw(xy=...)` は、バウンディングボックスの **左下座標 `(x0, y0)`** を基準に配置します。

## 9.1 ガントチャート (`GanttChart`)

開発スケジュールやマイルストーン、タスク間の依存関係（先行タスクと後続タスクの矢印）を視覚化できます。

```drawlib align=center file=fig_gantt_roadmap.png caption="図 9.1: エンジニアリング開発ロードマップ"
from drawlib.canvas import save, setup
from drawlib.charts.gantt import GanttChart
from drawlib.styles import Styles

setup(width=112, height=62)

chart = GanttChart(
    columns=["4月", "5月", "6月", "7月"],
    width=102.0,
    label_width=32.0,
    title="コアプラットフォーム開発ロードマップ (2026)",
    title_style=Styles.DarkBold.patch(text_size=12.0),
    header_height=6.0,
    row_height=5.2,
    bar_radius=1.0,
    axis_line_style=Styles.Muted,
    axis_text_style=Styles.Dark.patch(text_size=10.0),
    header_style=Styles.PrimaryNeutral,
    grid_style=Styles.MutedDashed,
    zebra_style=Styles.Neutral,
    progress_text_style=Styles.WhiteBold.patch(text_size=9.5),
)

chart.add_section("1. 基盤開発", style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=10.0))
t1 = chart.add_task("要件定義 & アーキテクチャ", start="4月", end=0.9, style=Styles.PrimaryFlat, progress=1.0)
t2 = chart.add_task("コアエンジン実装", start=0.7, end=2.2, style=Styles.PrimaryFlat, progress=0.8)

chart.add_section("2. 結合 & リリース", style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=10.0))
t3 = chart.add_task("E2E テスト & ドッグフード", start=2.0, end=3.2, style=Styles.SecondaryFlat, progress=0.4)
t4 = chart.add_task("本番環境デプロイ", start=3.0, end=3.9, style=Styles.SecondaryFlat, progress=0.0)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_milestone("Alpha 版完了", at=2.0, style=Styles.AccentFlat)
chart.add_marker(at=1.8, style=Styles.Accent, label="現在地", label_style=Styles.WhiteBold.patch(text_size=9.5))

chart.draw(xy=(5.0, 5.0))
save()
```

## 9.2 その他のチャート

- **`BarChart`**: 垂直・水平棒グラフ、グループ化（`bar_mode="group"`）・積み上げ（`bar_mode="stack"`）、先端角丸（`bar_r`）、対数軸（`Axis(scale="log")`）対応。
- **`LineChart` / `AreaChart`**: 時系列推移や多系列プロット。スプライン曲線補間（`smooth=True`）やオーバーラップ・積み上げ面グラフに対応。
- **`PieChart`**: 構成比率の可視化。ドーナツチャート（`hole_ratio`）および中央 KPI バッジ（`center_text`）、特定スライスの切り出し強調（`explode`）に対応。
- **`RadarChart`**: 多変量評価、アーキテクチャのトレードオフ分析やスキルマトリクス（多角形・円形グリッド対応）。
- **`ScatterChart`**: 2 次元散布図および 3 変数バブルプロット（`(x, y, radius)`）、対数軸（`Axis(scale="log")`）によるレイテンシ・スループット相関の可視化。
