# Drawlib Quickstart Guide

**Illustration as Code & Documentation as Code in Pure Python**

Drawlib is a pure-Python library designed to bridge technical system design, cloud architecture diagrams, quantitative charts, and publication-grade engineering documentation. Instead of maintaining fragile binary drawings or low-level plotting code, Drawlib enables developers and AI agents to express architecture and workflows declaratively in Python.

```drawlib 640px center caption:"Figure 0.1: Drawlib End-to-End Workflow — Code to Publication"
from drawlib.canvas import setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=48)

# 1. Stage: Source Code & Markdown
rectangle(xy=(18, 24), width=26, height=32, r=2.5, style=Styles.primary_outline)
phosphor.code(xy=(18, 30), width=9, style=Styles.primary)
text(xy=(18, 16), text="Declarative Python\n& Markdown", style=Styles.primary_bold, size=9.5)

# Transition 1
line((31, 24), (43, 24), arrowhead="->", style=Styles.bold)

# 2. Stage: Drawlib Engine
circle(xy=(56, 24), radius=13, style=Styles.secondary_outline)
phosphor.cpu(xy=(56, 29), width=8, style=Styles.secondary)
text(xy=(56, 18), text="drawlib\nEngine", style=Styles.secondary_bold, size=10)

# Transition 2
line((69, 24), (81, 24), arrowhead="->", style=Styles.bold)

# 3. Stage: Unified Publication Outputs
rectangle(xy=(98, 35), width=26, height=12, r=2, style=Styles.accent_flat)
text(xy=(98, 35), text="Static Site / HTML", style=Styles.white_bold, size=9)

rectangle(xy=(98, 24), width=26, height=12, r=2, style=Styles.secondary_flat)
text(xy=(98, 24), text="Design Spec / PDF", style=Styles.white_bold, size=9)

rectangle(xy=(98, 13), width=26, height=12, r=2, style=Styles.primary_flat)
text(xy=(98, 13), text="Image Batch / PNG", style=Styles.white_bold, size=9)
```

---

### Document Overview & Navigation

This guide serves as a comprehensive handbook for developers and AI agents adopting Drawlib:

- **Chapters 1–3**: Foundations — Design philosophy, installation, and Cartesian canvas coordinate system.
- **Chapters 4–6**: Core Primitives & Styling — Shapes, lines, GoogleStyles, fonts, icons, and external images.
- **Chapters 7–10**: High-Level Graphics — SmartArts components, declarative charts, cloud diagrams, and software models.
- **Chapters 11–12**: Documentation as Code & CLI — Markdown integration, code fence options, and build automation.
- **Chapters 13–15**: AI Collaboration & Engineering Practice — Autonomous agent workflows, scaffolding templates, and design rules.

| Document Metadata | Value |
| :--- | :--- |
| **Document Version** | `0.2.0` |
| **Theme** | GoogleStyles & GoogleColors |
| **Source Repository** | `https://github.com/yuichi110/drawlib` |
| **Author** | Yuichi Ito |
| **License** | Apache License 2.0 |
