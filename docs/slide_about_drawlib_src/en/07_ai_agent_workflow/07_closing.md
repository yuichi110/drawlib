::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# Start Drawing & Presenting as Code
:::

::: block xy=(80, 140) width=740 height=840 font_size=19px
## Unify Your Code, Diagrams, Docs & Slides

Stop context-switching between Git, GUI drawing tools, wikis, and slide editors. Bring your entire visual communication stack into version-controlled Python and Markdown.

### 3-Step Quickstart
```bash
# 1. Install Drawlib (PDF, DOCX & PPTX built in)
uv add drawlib   # or: pip install drawlib

# 2. Scaffold a 16:9 slide deck, doc, or site
uv run drawlib init slide my_deck -s default

# 3. Build HTML + PDF (auto Chromium) & preview
./my_deck_src/build.sh
./my_deck_src/serve.sh
```

### Core Takeaways
- **Batteries Included**: PDF (`build pdf`), MS Word (`build docx`), and 16:9 PowerPoint (`build pptx`) work out of the box—headless Chromium auto-downloads on first build (`cache download --all` / `--browser` for CI; `playwright install-deps chromium` on minimal Linux containers).
- **AI-Native Source of Truth**: Diagrams, docs, and slides live in Git with `drawlib rules` + headless grid review (`drawlib show -g`).
- **Explore & Contribute**: `https://github.com/yuichi110/drawlib`
:::

::: block xy=(860, 140) width=980 height=840
```drawlib file=closing_hero.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)

# Outer dark slate hero card with light inner cards
rectangle((49, 42), width=94, height=78, style=Styles.Neutral.patch(shape_r=3.0))

# Top Hero Banner
rectangle(
    (49, 67.5),
    width=86,
    height=18.0,
    style=Styles.WhiteFlat.patch(shape_fill_color=(15, 23, 42), shape_r=2.2),
)
text(
    (49, 71.0),
    "DRAWLIB  —  Illustration & Illustrated Documentation as Code",
    style=Styles.WhiteBold.patch(text_size=11.0),
)
text(
    (49, 63.5),
    "Pure Python 3.11+   •   Zero External Layout Binaries   •   Apache-2.0 Open Source",
    style=Styles.White.patch(text_size=8.5, text_color=(199, 210, 254)),
)

# Middle: 3-Step Quickstart ChevronProcess
proc = ChevronProcess(
    style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=9.2),
    description_style=Styles.Dark.patch(text_size=7.8),
    corner_angle=55.0,
    spacing=1.8,
    flat_left_end=True,
)
proc.add(
    "1. Install",
    description="uv add drawlib",
    style=Styles.PrimaryNeutral,
)
proc.add(
    "2. Scaffold",
    description="drawlib init slide",
    style=Styles.SecondaryNeutral,
)
proc.add(
    "3. Build & Present",
    description="./slide_src/build.sh",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.2),
    description_style=Styles.White.patch(text_size=7.8),
)
proc.draw(xy=(6.0, 39.5), width=86.0, height=15.0)

# Bottom 4 Pillar Summary Cards
pillars = [
    (16.5, "43 Primitives\n& 18 SmartArts", "Exact Cartesian\nGeometry"),
    (38.2, "6 Diagram Engines\n& 5 Graph Solvers", "Cloud, Flow, Seq,\nState, Class, ER"),
    (59.8, "9 Chart Types\n& APNG Animations", "Bar, Line, Area,\nPie, Radar, Gantt"),
    (81.5, "Built-in Exports\n& AI Agent Rules", "HTML, PDF, DOCX,\nPPTX, MD & PNG"),
]
for px, p_title, p_sub in pillars:
    rectangle((px, 24.5), width=19.8, height=18.0, style=Styles.White.patch(shape_r=1.5))
    text((px, 28.5), p_title, style=Styles.PrimaryBold.patch(text_size=8.0))
    text((px, 19.5), p_sub, style=Styles.Muted.patch(text_size=7.4))

# Bottom GitHub Call to Action Pill
rectangle(
    (49, 8.8),
    width=86,
    height=7.5,
    style=Styles.AccentFlat.patch(shape_r=2.0),
    text="GitHub Repository:   https://github.com/yuichi110/drawlib   —   Thank You!",
    text_style=Styles.WhiteBold.patch(text_size=9.5),
)

save()
```
:::

::: block xy=(80, 1010) width=820 height=30 font_size=14px
*Chapter 7: AI Agent Workflow & Ecosystem — Thank You & Getting Started*
:::

::: note
- Thank you for exploring Drawlib!
- Standard `uv add drawlib` / `pip install drawlib` includes HTML, vector PDF (`drawlib build pdf`), editable MS Word (`drawlib build docx`), and editable 16:9 MS PowerPoint (`drawlib build pptx`) export out of the box—automatically downloading headless Chromium on your first PDF or PPTX build (with `drawlib cache download --all` / `--browser` available for offline/CI pre-fetching and `playwright install-deps chromium` for minimal Linux Docker containers).
:::
