# 第9章: チャート描画（定量データの可視化）

`drawlib.charts` は、プロジェクトのロードマップ、スケジュール管理、パフォーマンスメトリクスを美麗にレンダリングするチャートモジュールです。

## 9.1 ガントチャート (`GanttChart`)

開発スケジュールやマイルストーン、タスク間の依存関係（先行タスクと後続タスクの矢印）を視覚化できます。

```drawlib 620px center file:fig_gantt_roadmap.png caption:"図 9.1: エンジニアリング開発ロードマップ"
from drawlib.canvas import setup
from drawlib.charts.gantt import GanttChart

setup(width=108, height=58)

chart = GanttChart(
    columns=["4月", "5月", "6月", "7月"],
    width=96.0,
    label_width=28.0,
    title="コアプラットフォーム開発ロードマップ (2026)",
    header_height=6.0,
    row_height=5.0,
    bar_radius=1.0,
)

chart.add_section("1. 基盤開発")
t1 = chart.add_task("要件定義 & アーキテクチャ", start="4月", end=0.9, progress=1.0)
t2 = chart.add_task("コアエンジン実装", start=0.7, end=2.2, progress=0.8)

chart.add_section("2. 結合 & リリース")
t3 = chart.add_task("E2E テスト & ドッグフード", start=2.0, end=3.2, progress=0.4)
t4 = chart.add_task("本番環境デプロイ", start=3.0, end=3.9, progress=0.0)

chart.add_dependency(t1, t2)
chart.add_dependency(t2, t3)
chart.add_milestone("Alpha 版完了", at=2.0)
chart.add_marker(at=1.8, label="現在地")

chart.draw(xy=(6.0, 5.0))
```

## 9.2 その他のチャート

- **`BarChart`**: 垂直・水平棒グラフ、グループ化・積み上げ対応。
- **`LineChart` / `AreaChart`**: 時系列推移、多系列プロット。
- **`PieChart`**: 構成比率（4% 未満の微小スライスは自動でテキスト重なり防止）。
- **`RadarChart`**: 多変量評価、スキルマトリクス。
