# Drawlib SmartArts Guidelines

SmartArts provide structured diagrams including tables, hierarchy trees, mindmaps, process chevrons, and code blocks.

## 1. Imports
```python
from drawlib.smartarts import (
    BoxList,
    BoxTreeNode,
    BulletPoints,
    ChevronProcess,
    Cycle,
    GridLayout,
    MindMapNode,
    Pyramid,
    SourceCode,
    Table,
    TreeNode,
    bubblespeech,
)
```

## 2. Core Components
- `Table(data, xy, width=None, height=None, ...).draw()`:
  - `data`: 2D list `[["Col1", "Col2"], ["Val1", "Val2"]]`.
  - `xy`: Center coordinate `(x, y)` of the table.
- `TreeNode(title, children=[...]).draw(xy, width, height)`:
  - Organizational and classification trees.
- `MindMapNode(title, children=[...]).draw(xy, width, height)`:
  - Mindmaps radiating outward from a central concept.
- `ChevronProcess(items, xy, width, height, ...).draw()`:
  - Step-by-step sequential pipeline with arrow chevrons.
- `BulletPoints(items, xy, width, height, ...).draw()`:
  - Bulleted list cards with icon support.
- `SourceCode(code, language="python", ...).draw(xy, width, height)`:
  - Syntax-highlighted code container with line numbers.

## 3. Minimal Example
```python
from drawlib.canvas import config, save
from drawlib.smartarts import ChevronProcess, Table

config(width=120, height=60)
ChevronProcess(
    items=["1. Plan", "2. Build", "3. Test", "4. Deploy"],
    xy=(60, 45), width=100, height=15
).draw()

Table(
    data=[["Task", "Owner", "Status"], ["Backend", "Alice", "Done"], ["Frontend", "Bob", "In Progress"]],
    xy=(60, 18), width=100, height=22
).draw()
save()
```
