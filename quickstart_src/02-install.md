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
from drawlib.canvas import setup
from drawlib.shapes import chevron
from drawlib.styles import Styles
from drawlib.text import text

setup(width=110, height=36)

steps = [
    ("1. Install", "pip / uv", Styles.Primary),
    ("2. Author", "Python / MD", Styles.Secondary),
    ("3. Preview", "drawlib show", Styles.Accent),
    ("4. Publish", "HTML / PDF", Styles.Success),
]

for idx, (title_str, sub_str, step_style) in enumerate(steps):
    cx = 16 + idx * 26
    chevron(
        xy=(cx, 18),
        width=23,
        height=18,
        corner_angle=50,
        style=step_style,
    )
    text(xy=(cx, 20), text=title_str, style=Styles.WhiteBold, size=11)
    text(xy=(cx, 14), text=sub_str, style=Styles.White, size=9)
```
