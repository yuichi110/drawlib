# Illustrated Notebook Quickstart

Welcome to your **Drawlib Jupyter & Google Colab** project! This Markdown file compiles into both a standalone `.ipynb` notebook and an interactive HTML preview page.

```drawlib align=center code=fold file=pipeline_overview.png caption="Data & Visualization Pipeline"
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

## 1. Sequential Python Execution

Standard `python` code blocks become executable code cells in `.ipynb` and are verified sequentially during `drawlib build jupyter`:

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

## 2. Live Drawlib Code Cell (`cell=code`)

Adding `cell=code` to a `drawlib` code block emits an executable code cell inside the notebook where `save()` is automatically converted to `show()`:

```drawlib cell=code file=live_bar_chart.png caption="Live Bar Chart Cell"
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
