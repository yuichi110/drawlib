::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch3_divider.svg
import utils

utils.draw_chapter_divider(
    3,
    "SmartArts & Pure-Python Charts",
    subtitle="18 Structured Infographics & 10 Zero-Dependency Plots",
    topics=[
        "Process Flows, Cycles & Roadmaps",
        "KPIs, CardLists, Pyramids & MindMaps",
        "Tables, SourceCode, Calendars & GeoMap",
        "10 Declarative Chart Types & Gantt",
    ],
    total_chapters=6,
)
```
:::

::: note
Chapter 3 introduces two of Drawlib's highest-leverage visual engines: `drawlib.smartarts` and `drawlib.charts`.
Instead of assembling infographics out of raw rectangles and manual coordinates, SmartArts provides 18 layout-aware components—covering pipelines, feedback loops, roadmaps, KPI cards, feature lists, pyramids, radial mindmaps, tables, syntax-highlighted code, schedule calendars, and vector world maps. Next, we explore Drawlib's 10 pure-Python chart classes, which render crisp vector plots directly onto the shared canvas with zero external plotting dependencies.
:::
