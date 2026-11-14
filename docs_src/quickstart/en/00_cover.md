# Drawlib Quickstart Guide

**Illustration as Code & Illustrated Documentation as Code in Pure Python**

Drawlib unifies declarative pure-Python illustrations and Markdown technical writing into a single Git-native source of truth—compiling documentation portals (`site`), searchable API references (`catalog`), multi-chapter whitepapers (`doc`), interactive 16:9 presentations (`slide`), standalone image/animation suites (`images`), vector PDFs, and editable Microsoft Office deliverables (`.docx` & `.pptx`).

```drawlib align=center code=hide file=cover_workflow.png caption="Figure 0.1: Drawlib Single Source of Truth — Declarative Python & Markdown to Multi-Target Deliverables"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=144, height=56)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

repo = d.add(
    NodeGroup(
        title="Git Repository (Source of Truth)",
        width=41.0,
        height=44.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.2),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(1.5, 4.0),
)
py_src = repo.add(
    Node(
        "Python Visuals\n(*.py & blocks)",
        width=33.0,
        height=14.0,
        icon=PhosphorIcon.CODE,
        icon_size=5.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(20.5, 28.5),
)
md_src = repo.add(
    Node(
        "Markdown Prose\n(en/ & ja/)",
        width=33.0,
        height=14.0,
        icon=PhosphorIcon.FILE_TEXT,
        icon_size=5.2,
        card_style=Styles.White.patch(shape_r=1.8),
    ),
    xy=(20.5, 10.5),
)

compiler = d.add(
    Node(
        "Drawlib Compiler\n& AI Grid Loop",
        width=32.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=6.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=11.5),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(66.0, 26.0),
)

out_web = d.add(
    Node(
        "Docs Site & Catalog\n(HTML / SEO / llms.txt)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.GLOBE,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 41.5),
)
out_doc = d.add(
    Node(
        "Whitepaper & Spec\n(Vector PDF & DOCX)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.FILE_PDF,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 26.0),
)
out_slide = d.add(
    Node(
        "16:9 Slides & Assets\n(PPTX / PNG / WebP / GIF)",
        width=40.0,
        height=13.0,
        icon=PhosphorIcon.PRESENTATION_CHART,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(118.0, 10.5),
)

d.connect(repo, compiler, routing="direct", padding=0.8)
j_hub = d.junction((90.0, 26.0))
j_top = d.junction((90.0, 41.5))
j_bot = d.junction((90.0, 10.5))
d.connect(compiler, j_hub, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_hub, j_top, arrow="-", routing="direct")
d.connect(j_hub, j_bot, arrow="-", routing="direct")
d.connect(j_top, out_web, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_hub, out_doc, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_bot, out_slide, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

---

### Document Overview & Roadmap

This 16-chapter handbook guides software engineers, technical writers, and AI coding agents from Drawlib fundamentals to multi-target publishing:

- **Chapters 1–3 (Foundations)**: Core motivation, zero-config installation (`uv` & `uvx`), and Cartesian `(0, 0)` canvas geometry.
- **Chapters 4–6 (Primitives, Styles & Icons)**: 43 geometric shapes, curved/orthogonal lines, `GoogleStyles` neutral token discipline, universal CJK/Latin typography, and 34 vector icon suites.
- **Chapters 7–11 (High-Level Visual Engines)**: 18 SmartArts, 10 quantitative charts (including `BoxChart` & `HeatmapChart`), `ArchitectureDiagram`, UML/software models, and 5 `drawlib.graph` automatic layout solvers.
- **Chapters 12–15 (Animations, Publishing & AI Loops)**: Multi-frame `APNG`/`WebP`/`GIF` animations, 16:9 slides, the 5 project archetypes (`site`, `catalog`, `doc`, `slide`, `images`), CLI caching, and autonomous 3-stage AI visual verification.

| Document Metadata | Value |
| :--- | :--- |
| **Drawlib Version** | `0.3.10` |
| **Visual Theme** | `GoogleStyles` & `GoogleColors` (`style = "google"`) |
| **Languages (`[i18n]`)** | English (`en`) & Japanese (`ja`) |
| **Official Website** | `https://www.drawlib.com/` |
| **Source Repository** | `https://github.com/yuichi110/drawlib` |
| **License** | Apache License 2.0 |
