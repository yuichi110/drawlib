::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Two-Tier Caching & Unified CLI
:::

::: block xy=(80, 140) width=640 height=800
```drawlib file=cache_kpis.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=64, height=80)
utils.draw_kpi_cards(
    [
        ("< 1s", "Incremental Builds", "SQLite SHA-256 .drawlib/cache.db"),
        ("50+", "Agent Rule Topics", "On-demand via drawlib rules show"),
        ("Zero", "Broken Links", "Built-in drawlib serve --check"),
    ],
    width=64,
    height=80,
)
save()
```
:::

::: block xy=(760, 140) width=1080 height=800
```drawlib file=two_tier_cache_cli.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import ChevronProcess, Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=108, height=80)

# ==============================================================================
# Top Panel: Two-Tier Cache Architecture
# ==============================================================================
top_panel = Panel(
    "Two-Tier Cache Architecture",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.5),
    icon=phosphor.database,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=9.2,
)
top_panel.draw(xy=(2.0, 38.5), width=104.0, height=38.5)

# Tier 1 Card: Package Asset Cache
rectangle((28.8, 53.2), width=47.5, height=23.5, style=Styles.Neutral.patch(shape_r=1.8))
circle((11.5, 58.8), radius=4.2, style=Styles.WhiteFlat)
phosphor.package((11.5, 58.8), width=4.8, style=Styles.PrimaryBold)
text((17.2, 60.2), "Tier 1: Asset Cache", style=Styles.DarkBold.patch(text_size=15.0, halign="left"))
text((17.2, 56.2), "drawlib cache list / download", style=Styles.PrimaryBold.patch(text_size=12.8, halign="left"))
text(
    (7.8, 47.0),
    "On-demand fonts, 34 icon packs\n& headless Chromium binary",
    style=Styles.Dark.patch(text_size=13.2, halign="left"),
)

# Tier 2 Card: SQLite Build Cache (.drawlib/cache.db)
rectangle((79.2, 53.2), width=47.5, height=23.5, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
circle((62.0, 58.8), radius=4.2, style=Styles.WhiteFlat)
phosphor.lightning((62.0, 58.8), width=4.8, style=Styles.PrimaryBold)
text((67.8, 60.2), "Tier 2: Build Cache", style=Styles.DarkBold.patch(text_size=15.0, halign="left"))
text((67.8, 56.2), ".drawlib/cache.db (SQLite)", style=Styles.PrimaryBold.patch(text_size=12.8, halign="left"))
text(
    (58.2, 47.0),
    "SHA-256 content + style hash\nShared by HTML/PDF/Office",
    style=Styles.Dark.patch(text_size=13.2, halign="left"),
)

# ==============================================================================
# Bottom Panel: Unified CLI Workflow (uv run drawlib ...)
# ==============================================================================
bot_panel = Panel(
    "Unified CLI  —  uv run drawlib <command>",
    style=Styles.White.patch(shape_r=2.2),
    header_style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=16.5),
    icon=phosphor.terminal_window,
    icon_style=Styles.WhiteBold,
    header_variant="filled",
    header_height=9.2,
)
bot_panel.draw(xy=(2.0, 3.0), width=104.0, height=32.0)

cli_flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.8),
    corner_angle=62.0,
    spacing=1.4,
    flat_left_end=True,
)
cli_flow.add("init", description="5 Types")
cli_flow.add("rules", description="list / show")
cli_flow.add("show -g", description="Grid QA", style=Styles.PrimaryNeutral)
cli_flow.add("build", description="Web/Office")
cli_flow.add(
    "serve",
    description="--check",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=14.0),
    description_style=Styles.White.patch(text_size=11.8),
)
cli_flow.draw(xy=(4.5, 6.2), width=99.0, height=16.8)

save()
```
:::

::: note
Fast feedback loops are essential for both interactive authoring and autonomous AI agents. Drawlib achieves sub-second incremental rebuilds through a Two-Tier Caching architecture:
- **Tier 1 — Package Asset Cache (`drawlib cache list / download / clear`)**: Downloads typography fonts, 34 cloud and Phosphor icon packs, and headless Chromium on demand into `_cached_assets/`, keeping the base `pip` / `uv` install lightweight while supporting air-gapped CI prefetching.
- **Tier 2 — Project Diagram Build Cache (`.drawlib/cache.db`)**: A content-addressed SQLite database keyed by the SHA-256 hash of each diagram's code, `styles.py`, `utils.py`, and output format. Unchanged diagrams resolve in milliseconds across HTML, PDF, DOCX, and PPTX builds, while `--no-cache` enforces clean verification in CI.
Every stage runs through one consistent `uv run drawlib` CLI: `init`, `rules`, `show -g`, `build`, and `serve --check` for automated link and asset validation.
:::
