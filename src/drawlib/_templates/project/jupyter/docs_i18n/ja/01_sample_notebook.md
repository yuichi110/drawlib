# 図解付きノートブック クイックスタート

**Drawlib Jupyter & Google Colab** プロジェクトへようこそ！この Markdown ファイルは、スタンドアロンの `.ipynb` ノートブックと HTML プレビューページの両方にコンパイルされます。

```drawlib align=center code=fold file=pipeline_overview.png caption="データ＆可視化パイプライン"
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=100, height=28)

proc = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold,
    description_style=Styles.Muted,
    flat_left_end=True,
)
proc.add("1. Author .md")
proc.add("2. Dry-Run Cells", style=Styles.PrimaryNeutral)
proc.add("3. Export .ipynb", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
proc.draw((8, 8), width=84, height=12)

save()
```

## 1. Python セルの順次実行

通常の `python` コードブロックは `.ipynb` の実行可能コードセルとなり、`drawlib build jupyter` 実行時に上から順番に自動検証されます。

```python
dataset = [12, 28, 35, 49, 64]
summary = {
    "count": len(dataset),
    "mean": sum(dataset) / len(dataset),
    "max": max(dataset),
}
print(f"Loaded {summary['count']} records (mean={summary['mean']:.1f})")
summary
```

## 2. ライブ Drawlib コードセル (`cell=code`)

`drawlib` コードブロックに `cell=code` を付与すると、ノートブック内で実行可能なコードセルとして出力され、`save()` は自動的に `show()` に変換されます。

```drawlib cell=code file=live_bar_chart.png caption="ライブ棒グラフセル"
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=80, height=40)

chart = BarChart(
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted,
    width=64,
    height=28,
    categories=["Q1", "Q2", "Q3", "Q4", "Q5"],
    title="Throughput by Stage",
    title_style=Styles.DarkBold,
)
chart.add_series("Throughput", dataset, style=Styles.PrimaryFlat)
chart.draw((10, 6))

save()
```
