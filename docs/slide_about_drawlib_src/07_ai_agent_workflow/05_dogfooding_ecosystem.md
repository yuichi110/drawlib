::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Live Dogfooding in the Drawlib Repository
:::

::: block (80, 140) (740, 840) font:20px
## Eating Our Own Cooking at 100% Scale

The `drawlib` repository is simultaneously the library codebase (`src/drawlib/`) and a **live production dogfooding environment** where every project archetype is continuously built and tested via `./dcli`:

```bash
# 1. Static analysis (Ruff lint/format, Ty type check, docstrings)
./dcli code-check all

# 2. Parallel unit & integration test suite
./dcli test all

# 3. Build all 6 live dogfooding documentation targets
./dcli docs build --all
./dcli docs serve site --check
```

### Six Live Dogfooding Targets in `docs/`
1. **`site` (`docs/docs_src/`)**: Multi-page documentation website (`docs_html/` & `docs_markdown/`).
2. **`quickstart` (`docs/quickstart_src/`)**: Quickstart guide & vector PDF (`doc` archetype).
3. **`dogfooding` & `dogfooding-en`**: Japanese & English architectural whitepapers (`doc` + `pdf`).
4. **`slide` (`docs/slide_about_drawlib_src/`)**: This 64-slide 16:9 showcase presentation deck!
5. **`readme` (`docs/readme_src/`)**: Standalone hero illustrations for `README.md`.
:::

::: block (860, 140) (980, 840)
```drawlib file:dogfooding_ecosystem.svg
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
text((49, 75), "Drawlib Repository Dogfooding & Quality Gate Ecosystem", style=Styles.DarkBold.patch(text_size=11.5))

# Top Center: Core Engine & ./dcli Orchestrator
rectangle(
    (49, 63.0),
    width=84,
    height=12.5,
    r=2.0,
    style=Styles.PrimaryFlat,
    text="Core Library (src/drawlib/)   +   Development CLI (./dcli)\ncode-check all (Ruff + Ty)   •   test all (pytest + xdist)   •   docs build --all",
    text_style=Styles.WhiteBold.patch(text_size=8.8),
)

# Middle: 5 Dogfooding Project Cards in docs/
targets = [
    (19.0, 41.5, "1. docs_src/ (site)", "Official Multi-Page\nDocs Portal + Markdown", Styles.PrimaryNeutral, Styles.DarkBold),
    (49.0, 41.5, "2. quickstart_src/ (doc)", "Quickstart Manual\nHTML + A4 Vector PDF", Styles.SecondaryNeutral, Styles.DarkBold),
    (79.0, 41.5, "3. dogfooding_src/ (doc)", "JP & EN Whitepapers\nHTML + A4 Vector PDF", Styles.BlueNeutral, Styles.DarkBold),
    (33.0, 21.5, "4. slide_about_drawlib_src/", "This 64-Slide 16:9 Deck!\nHTML + Vector slide.pdf", Styles.AccentFlat, Styles.WhiteBold),
    (65.0, 21.5, "5. readme_src/ (image)", "GitHub README.md\nHero Banner Scripts", Styles.TealNeutral, Styles.DarkBold),
]

for cx, cy, title_s, sub_s, st_c, st_t in targets:
    rectangle((cx, cy), width=26.5, height=15.0, r=1.8, style=st_c)
    text((cx, cy + 3.2), title_s, style=st_t.patch(text_size=8.5))
    sub_style = Styles.White.patch(text_size=7.6) if st_c == Styles.AccentFlat else Styles.Dark.patch(text_size=7.6)
    text((cx, cy - 2.8), sub_s, style=sub_style)

# Arrows from Core Engine down to Dogfooding Targets
for tx in [19.0, 49.0, 79.0]:
    line((tx, 56.5), (tx, 49.2), arrow_head="->", style=Styles.DarkBold)
line((33.0, 34.0), (33.0, 29.2), arrow_head="->", style=Styles.DarkBold)
line((65.0, 34.0), (65.0, 29.2), arrow_head="->", style=Styles.DarkBold)

# Bottom Feedback Loop Banner
rectangle(
    (49, 8.5),
    width=84,
    height=6.5,
    r=1.5,
    style=Styles.White,
    text="Continuous Feedback Loop: Every Library Change Is Verified Against Real Production Docs & Slides",
    text_style=Styles.PrimaryBold.patch(text_size=8.5),
)

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 7: AI Agent Workflow & Ecosystem — Live Repository Dogfooding*
:::

::: note
- Every feature you have seen in this presentation—from `ArchitectureDiagram` and `LayerGraph` to `BarChart`, `Animation`, and `build_slide`—is continuously dogfooded inside the Drawlib repository itself.
- Running `./dcli docs build --all` compiles the multi-page documentation site, the quickstart PDF, the Japanese and English dogfooding whitepapers, the README hero images, and this entire 64-slide presentation deck!
:::
