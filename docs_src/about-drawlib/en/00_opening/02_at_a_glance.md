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
# Drawlib at a Glance
:::

::: block xy=(80, 140) width=640 height=800
```drawlib file=glance_kpis.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=64, height=80)

utils.draw_kpi_cards(
    [
        ("4,500+", "Vector Icons", "Across 34 official & neutral suites"),
        ("39+", "High-Level Visuals", "18 SmartArts, 10 Charts,\n6 Diagrams, 5 Graphs"),
        ("5", "Project Archetypes", "site, catalog, doc, slide, images"),
        ("100%", "Pure Python & Git", "Zero GUI lock-in, AI self-verifiable"),
    ],
    width=64,
    height=80,
)
save()
```
:::

::: block xy=(760, 140) width=1080 height=800
```drawlib file=ecosystem_layers.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles

clear()
setup(width=108, height=80)

panel = Panel(
    "Four-Layer Architecture Stack",
    "From AI CLI & Primitives to Multi-Target Publishing",
    style=Styles.Neutral.patch(shape_r=2.5),
    header_style=Styles.PrimaryBold,
    text_style=Styles.DarkBold.patch(text_size=15.5),
    description_style=Styles.Muted.patch(text_size=12.8),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_variant="underline",
    header_height=9.5,
)
panel.draw((2.0, 2.0), width=104.0, height=76.0)
inner_xy, inner_w, inner_h = panel.get_content_box(
    (2.0, 2.0),
    width=104.0,
    height=76.0,
    padding=(3.5, 2.8),
)

layers = CardList(
    style=Styles.White.patch(shape_r=2.0),
    text_style=Styles.DarkBold.patch(text_size=14.5),
    description_style=Styles.Dark.patch(text_size=13.0),
    badge_shape="rounded_rect",
    badge_style=Styles.SecondaryNeutral,
    badge_text_style=Styles.DarkBold.patch(text_size=12.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=2.6,
)
layers.add(
    "Layer 4 · Multi-Target Compiler",
    "HTML · Catalog · Slide · PDF · DOCX · PPTX",
    badge_text="L4",
    icon=phosphor.rocket_launch,
    style=Styles.PrimaryNeutral.patch(shape_r=2.0),
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=12.5),
    icon_style=Styles.WhiteBold,
)
layers.add(
    "Layer 3 · Declarative Visual Engines",
    "SmartArts · Charts · Diagrams · Graphs · Anim",
    badge_text="L3",
    icon=phosphor.chart_bar,
)
layers.add(
    "Layer 2 · Primitives, 34 Icon Suites & Semantic Styles",
    "43 Shapes · 4,500+ Vector Icons · Theme Presets",
    badge_text="L2",
    icon=phosphor.paint_brush,
)
layers.add(
    "Layer 1 · AI Agent CLI",
    "rules · show -g Grid Inspection · SQLite Cache",
    badge_text="L1",
    icon=phosphor.robot,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=12.5),
    icon_style=Styles.WhiteBold,
)
layers.draw(inner_xy, width=inner_w, height=inner_h)
save()
```
:::

::: note
Here is Drawlib at a glance.
On the left, four key numbers capture the breadth of the ecosystem: over 4,500 vector icons across 34 official cloud and domain-neutral suites; 39+ high-level visual components spanning 18 SmartArts, 10 pure-Python chart types, 6 technical diagram engines, and 5 automatic graph layout solvers; 5 first-class project archetypes; and a 100% pure-Python, Git-native workflow.
On the right, Drawlib is organized into four cohesive layers: an AI-ready CLI and SQLite caching foundation at Layer 1, primitives and semantic styles at Layer 2, declarative visual engines at Layer 3, and the multi-target document and presentation compiler at Layer 4.
:::
