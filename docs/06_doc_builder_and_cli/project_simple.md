# Simple Project Guide (`drawlib init simple`)

The `simple` starter template is tailored for single-document technical specifications, Request for Comments (RFCs), system design proposals, and repository README pages with embedded diagrams.

---

## 1. Project Initialization

Scaffold a single-document project using `drawlib init`:

```bash
# Create in a new subdirectory:
drawlib init simple my_rfc/

# Or scaffold directly in current working directory:
drawlib init simple --here
```

---

## 2. Directory Layout & Anatomy

```text
my_rfc/
├── docs_src/                  # [SOURCE OF TRUTH] Edit authoring Markdown here
│   ├── doc.md                 # Single document with embedded ```drawlib``` blocks
│   ├── template.html          # HTML layout template
│   ├── style.css              # Document stylesheet (responsive typography)
│   ├── config.py              # Global drawing settings
│   ├── build.sh               # Automation script for Markdown & HTML export
│   └── README.md              # Quickstart guide
├── docs/                      # [GENERATED] GitHub-flavored rendered Markdown
│   ├── doc.rendered.md
│   └── doc_images/            # Companion diagram images
└── docs_html/                 # [GENERATED] Responsive single-page HTML
    ├── index.html
    └── doc_images/
```

---

## 3. Authoring the Document

Edit `docs_src/doc.md`. Embed Python diagrams directly inline:

````markdown
# RFC 104: Asynchronous Order Ingestion Pipeline

## 1. Abstract
This document outlines the migration from synchronous HTTP checkout to event-driven Kafka messaging.

## 2. Proposed Architecture

```drawlib 650px center caption:"Target Event-Driven Architecture"
from drawlib import canvas, shapes, lines, styles

canvas.setup(width=100, height=45)
shapes.rectangle((20, 22.5), width=25, height=18, style=styles.Styles.AccentFlat, text="Client", text_style=styles.Styles.WhiteBold)
shapes.rectangle((50, 22.5), width=25, height=18, style=styles.Styles.PrimaryFlat, text="Ingest Gateway", text_style=styles.Styles.WhiteBold)
shapes.rectangle((80, 22.5), width=25, height=18, style=styles.Styles.SecondaryFlat, text="Kafka Queue", text_style=styles.Styles.WhiteBold)

lines.line((32.5, 22.5), (37.5, 22.5), arrowhead="->", style=styles.Styles.PrimaryBold)
lines.line((62.5, 22.5), (67.5, 22.5), arrowhead="->", style=styles.Styles.PrimaryBold)
```

## 3. Data Schema
...
````

---

## 4. Building & Publishing

Run the automated build script:

```bash
./docs_src/build.sh
```

This compiles:
1. `docs_html/index.html`: A self-contained, beautifully styled HTML document with responsive typography and embedded diagrams.
2. `docs/doc.rendered.md`: A standard GitHub-compatible Markdown document referencing rendered images in `docs/doc_images/`.
