::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Sub-Millisecond Incremental Builds (SQLite Image Cache)
:::

::: block (80, 140) (740, 840) font:20px
## Instant Rebuilds for Large Decks & Docs

A comprehensive technical site or 64-slide presentation can contain **100+ embedded diagrams and multi-frame animations**. Re-executing every Python block on every edit would slow down live authoring.

### Deterministic SHA-256 Cache Key (`.drawlib/cache.sqlite3`)
Drawlib hashes four inputs before executing any ```` ```drawlib ```` block:
1. **Normalized Python Code Block**: Exact script source inside the fence.
2. **Global `styles.py` & `utils.py` Hashes**: Editing a shared helper or theme invalidates dependent diagrams automatically.
3. **Target Output Format**: `.svg`, `.png` (APNG), or `.webp`.
4. **Slide Context (`total_slides`)**: Ensures `current_slide.text` (`12 / 64`) stays accurate when slides are added or removed.

### Cache Hit Performance
- **Cold Build (64 Slides)**: Renders all SVGs & APNGs from scratch (~14s).
- **Warm Cache Build (1 Slide Edited)**: Restores 63 unchanged slides from SQLite in **< 1 ms per diagram**—completing the full deck build in **~1.1 seconds**!
:::

::: block (860, 140) (980, 840)
```drawlib file:sqlite_cache_arch.svg
from drawlib.canvas import clear, save, setup
from drawlib.charts.bar import BarChart
from drawlib.lines import line
from drawlib.shapes import cylinder, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=2.5))
text((49, 75), "SQLite Incremental Build Cache Architecture & Speedup", style=Styles.DarkBold.patch(text_size=11.5))

# Top Section: Hash Computation & Lookup Flow
rectangle((49, 58.0), width=86, height=24.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text((9.0, 67.0), "1. Deterministic SHA-256 Cache Key Pipeline", style=Styles.PrimaryBold.patch(text_size=8.8, halign="left"))

rectangle(
    (21.0, 55.5),
    width=24.0,
    height=13.0,
    style=Styles.White.patch(shape_r=1.5),
    text="Hash Inputs:\n• Code Block AST/Text\n• styles.py + utils.py\n• Format + total_slides",
    text_style=Styles.DarkBold.patch(text_size=7.6),
)
cylinder(
    (49.5, 55.5),
    width=21.0,
    height=13.5,
    style=Styles.PrimaryFlat,
    text=".drawlib/\ncache.sqlite3\n(SHA-256 BLOB)",
    text_style=Styles.WhiteBold.patch(text_size=8.0),
)
rectangle(
    (78.0, 59.0),
    width=22.0,
    height=6.0,
    style=Styles.SecondaryNeutral.patch(shape_r=1.2),
    text="HIT: Restore (< 1 ms)",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)
rectangle(
    (78.0, 51.5),
    width=22.0,
    height=6.0,
    style=Styles.White.patch(shape_r=1.2),
    text="MISS: Execute & Store",
    text_style=Styles.DarkBold.patch(text_size=8.0),
)

line((33.0, 55.5), (39.0, 55.5), arrow_head="->", style=Styles.DarkBold)
line((60.0, 57.5), (67.0, 59.0), arrow_head="->", style=Styles.DarkBold)
line((60.0, 53.5), (67.0, 51.5), arrow_head="->", style=Styles.DarkBold)

# Bottom Section: BarChart comparing Cold Build vs Warm Cache Build Times
rectangle((49, 24.5), width=86, height=37.0, style=Styles.White.patch(shape_r=2.0))

chart = BarChart(
    axis_line_style=Styles.Dark,
    categories=["64-Slide Deck", "Multi-Page Site", "Whitepaper Doc"],
    width=76.0,
    height=29.0,
    title="2. Build Duration Comparison: Cold Build vs Warm SQLite Cache (Seconds)",
    title_style=Styles.DarkBold.patch(text_size=9.2),
    bar_mode="group",
    bar_width_ratio=0.65,
    bar_r=0.8,
    axis_text_style=Styles.Muted.patch(text_size=8.0),
    grid_style=Styles.MutedDashed,
    value_text_style=Styles.DarkBold.patch(text_size=7.8),
    value_format="{:.1f}s",
)
chart.configure_y_axis(min_value=0, max_value=20, tick_step=5, unit="s")
chart.add_series("Cold Build (--no-cache)", [14.2, 18.5, 6.4], style=Styles.SecondaryNeutral)
chart.add_series("Warm Cache (Incremental)", [1.1, 1.4, 0.5], style=Styles.PrimaryFlat)
chart.draw(xy=(10.0, 8.0))
chart.draw_legend(xy=(24.0, 38.0), text_style=Styles.DarkBold.patch(text_size=8.0), orientation="horizontal")

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 7: AI Agent Workflow & Ecosystem — Sub-Millisecond SQLite Build Cache*
:::

::: note
- Notice the huge speedup shown in the bottom `BarChart`: when editing a single slide in a 64-slide presentation, `.drawlib/cache.sqlite3` restores all 63 unchanged diagrams in under a millisecond each, dropping total rebuild time from ~14 seconds to ~1.1 seconds!
- Passing `--no-cache` to `drawlib build` bypasses the SQLite cache whenever a full clean rebuild is desired.
:::
