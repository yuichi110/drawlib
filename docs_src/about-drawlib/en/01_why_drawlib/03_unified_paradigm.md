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
# Illustration & Documentation as Code
:::

::: block xy=(80, 145) width=680 height=790
## Pure Python + Markdown

- **Turing-Complete Layout**: Loops, variables, and shared `utils.py` helpers

- **Inline Code Blocks**: Embed `drawlib` visuals directly inside Markdown

- **Deterministic PR Diffs**: Review prose and diagram updates together

```python
setup(width=120, height=32)
p = ChevronProcess(style=Styles.Neutral)
for s in ("Code", "Build", "Ship"): p.add(s)
p.draw((6, 8), width=108, height=16)
save()
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=unified_paradigm.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=104, height=80)

panel = Panel(
    "Unified Code-to-Artifact Pipeline",
    "Code -> Visuals & Docs",
    style=Styles.Neutral.patch(shape_r=2.5),
    header_style=Styles.PrimaryBold,
    text_style=Styles.DarkBold.patch(text_size=15.2),
    description_style=Styles.Muted.patch(text_size=12.5),
    icon=phosphor.code,
    icon_style=Styles.PrimaryBold,
    header_variant="underline",
    header_height=9.5,
)
panel.draw((2.0, 2.0), width=100.0, height=76.0)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=14.0),
    edge_style=Styles.PrimaryBold,
    edge_text_style=Styles.PrimaryBold.patch(text_size=12.5),
    node_card_style=Styles.White,
)

pr_group = d.add(
    NodeGroup(
        title="Single Git Pull Request",
        width=88.0,
        height=21.5,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=13.5, halign="left"),
    ),
    xy=(3.0, 41.5),
)
md_node = pr_group.add(
    Node(
        "Markdown (.md)\nNarrative & Stage",
        width=38.0,
        height=13.5,
        icon=PhosphorIcon.FILE_TEXT,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(22.5, 8.5),
)
py_node = pr_group.add(
    Node(
        "Python (drawlib)\nVisual Logic & Styles",
        width=38.0,
        height=13.5,
        icon=PhosphorIcon.CODE,
        icon_size=5.8,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(65.5, 8.5),
)

compiler = d.add(
    Node(
        "Drawlib Compiler  (Headless Render + Cache)",
        width=66.0,
        height=14.5,
        icon=PhosphorIcon.CPU,
        icon_size=6.2,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=14.0),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.0),
    ),
    xy=(47.0, 27.5),
)

out_vis = d.add(
    Node(
        "Vector Visuals\nSVG · PNG · APNG",
        width=40.0,
        height=14.0,
        icon=PhosphorIcon.IMAGES,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(24.0, 7.5),
)
out_docs = d.add(
    Node(
        "Published Docs\nHTML · Slide · PDF · Office",
        width=42.0,
        height=14.0,
        icon=PhosphorIcon.BOOK_OPEN,
        icon_size=5.8,
        card_style=Styles.PrimaryNeutral.patch(shape_r=1.8),
    ),
    xy=(71.0, 7.5),
)

j_in_l = d.junction((25.5, 38.0))
j_in_r = d.junction((68.5, 38.0))
j_in_m = d.junction((47.0, 38.0))
d.connect(md_node, j_in_l, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(py_node, j_in_r, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_in_l, j_in_m, arrow="-", routing="direct")
d.connect(j_in_r, j_in_m, arrow="-", routing="direct")
d.connect(j_in_m, compiler, arrow="->", routing="direct", padding=(0.0, 0.8))

j_out_m = d.junction((47.0, 17.8))
j_out_l = d.junction((24.0, 17.8))
j_out_r = d.junction((71.0, 17.8))
d.connect(compiler, j_out_m, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_out_m, j_out_l, arrow="-", routing="direct")
d.connect(j_out_m, j_out_r, arrow="-", routing="direct")
d.connect(j_out_l, out_vis, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_out_r, out_docs, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(5.0, 4.0))
save()
```
:::

::: note
Drawlib resolves the tooling dilemma through a unified paradigm: Illustration and Documentation as Code.
Instead of inventing yet another limited domain-specific syntax, Drawlib gives you the full power of pure Python—loops, functions, type hints, IDE autocomplete, and shared `styles.py` and `utils.py` modules—embedded directly inside standard Markdown fenced blocks.
When an engineer or an AI agent updates a microservice architecture, both the prose explanation and the Python diagram code change in the exact same Git pull request, compiling deterministically into crisp vector graphics and published documents.
:::
