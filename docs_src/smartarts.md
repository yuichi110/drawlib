# SmartArts Guide

SmartArts in Drawlib provide high-level, automated diagram components for structural content like code syntax highlighting, list trees, tables, and pyramids.

---

## 1. Code Syntax Highlighting (`sourcecode`)

`sourcecode()` renders syntax-highlighted code blocks with line numbers directly on the canvas:

```drawlib
from drawlib.canvas import config
from drawlib.smartarts import SourceCode

config(width=120, height=60)

code_snippet = """def calculate_area(radius: float) -> float:
    # Compute circle area
    return 3.14159 * radius ** 2
"""

sc = SourceCode(language="python")
sc.draw(xy=(60, 30), width=100, code=code_snippet)
```

---

## 2. Structured SmartArts

Drawlib includes several automated diagram templates:
- **`boxlist()`**: Sequential process/step boxes.
- **`boxtree()` / `tree()`**: Hierarchical tree structures.
- **`table()`**: Formatted tabular data.
- **`pyramid()`**: Multi-level pyramid diagrams.
- **`bulletpoints()`**: Categorized bullet lists.

---

## Navigation

- [Back to Index](./index.md)
- [Next: Document Builder](./doc_builder.md)
