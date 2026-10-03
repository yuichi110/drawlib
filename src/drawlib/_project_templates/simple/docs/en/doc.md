# Simple Document

This is an example document created with [Drawlib](https://github.com/yuichi110/drawlib).

## 1. Quick Overview (Primitive API)

This diagram demonstrates standard diagramming using Drawlib's core primitives without external helpers:

```drawlib 600px center file:basic_architecture.png caption:"Basic Architecture Diagram"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="Client App", text_style=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="Backend API", text_style=Styles.WhiteBold)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrow_head="->", style=Styles.PrimaryBold)
```

## 2. Advanced Overview (Utilities & Assets)

This diagram demonstrates reusable drawing components defined in `utils.py` and local image assets stored in `_assets/`:

```drawlib 600px center file:reusable_helpers_architecture.png caption:"Architecture with Reusable Helpers & Local Assets"
from drawlib.canvas import setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=110, height=52)

# Service nodes drawn using reusable helper from utils.py
service_card((20, 24), title="Web Client", subtitle="Browser / App")
service_card((55, 24), title="Linux Server", subtitle="Ubuntu / Nginx", style=Styles.AccentFlat)
service_card((90, 24), title="Database", subtitle="PostgreSQL", style=Styles.SecondaryFlat)

# Connections with protocol labels
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# Embedded local image asset from docs_src/_assets/ directory
image((55, 41), width=8, image="_assets/linux.png")
```

Drawlib allows you to write illustrations as code directly embedded in Markdown.
