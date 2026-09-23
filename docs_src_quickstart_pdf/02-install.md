# 2. Installation & Setup

Drawlib requires **Python 3.11 or higher** and can be installed from PyPI using `pip` or `uv`.

## Installing with pip or uv

```bash
# Using pip
pip install drawlib

# Using uv
uv add drawlib
```

## Verifying the Installation

Once installed, both the Python package `drawlib` and the `drawlib` command-line tool are available:

```bash
$ drawlib --version
```

You can also invoke the CLI via Python's module runner:

```bash
$ python -m drawlib --version
```

## Semantic Versioning & Stability

Drawlib follows `<major>.<minor>.<patch>` semantic versioning:
- **Major Version**: Significant architectural or API changes
- **Minor Version**: New features and backward-compatible enhancements
- **Patch Version**: Bug fixes and internal optimizations without API changes

```drawlib 580px center caption:"Figure 2.1: Drawlib Release & Versioning Workflow"
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.shapes import chevron
from drawlib.text import text
from drawlib.types import Style

config(width=110, height=36)

steps = [
    ("1. Install", "pip / uv", Colors140.CornflowerBlue),
    ("2. Author", "Python / MD", Colors140.MediumSeaGreen),
    ("3. Preview", "drawlib show", Colors140.GoldenRod),
    ("4. Publish", "HTML / PDF", Colors140.Tomato),
]

for idx, (title_str, sub_str, fill_col) in enumerate(steps):
    cx = 16 + idx * 26
    chevron(
        xy=(cx, 18),
        width=23,
        height=18,
        corner_angle=50,
        style=Style(fill_color=fill_col, line_color=Colors.White, line_width=1.5),
    )
    text(xy=(cx, 20), text=title_str, style=Style(text_color=Colors.White, text_size=11))
    text(xy=(cx, 14), text=sub_str, style=Style(text_color=Colors.White, text_size=9))
```
