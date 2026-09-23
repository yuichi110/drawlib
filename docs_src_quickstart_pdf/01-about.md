# 1. About Drawlib

Drawlib is a pure Python drawing library designed to facilitate **Illustration as Code**. Instead of manually positioning shapes in GUI drawing tools that store opaque binary files, Drawlib generates crisp illustrations directly from readable, version-controlled Python scripts and Markdown documents.

## Why Illustration as Code?

1. **Git & Code Review Friendly**: Every diagram is plain Python text. Track changes with `git diff`, review architecture updates in pull requests, and automate builds in CI/CD.
2. **Visual Consistency via Themes**: Apply unified preset styles (`default`, `essentials`, `monochrome`, or custom themes) across hundreds of illustrations with zero manual formatting.
3. **Full Power of Python**: Use loops, helper functions, data structures, and full IDE type hints / autocompletion instead of learning a restricted Domain-Specific Language (DSL).

## First Example

Here is a simple example combining a styled circle, rectangle, and text label on a Drawlib canvas:

```python
from drawlib.canvas import config, save
from drawlib.colors import Colors140
from drawlib.shapes import circle
from drawlib.types import Style

config(width=100, height=50)
circle(
    xy=(50, 25),
    radius=18,
    style=Style(
        line_style="dashed",
        line_color=Colors140.BlueViolet,
        line_width=3,
        fill_color=Colors140.Turquoise,
    ),
)
save()
```

When compiled by Drawlib, this code renders the following illustration:

```drawlib 520px center caption:"Figure 1.1: Styled Circle Generated from Python Code"
from drawlib.canvas import config
from drawlib.colors import Colors140
from drawlib.shapes import circle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=50)
circle(
    xy=(50, 25),
    radius=18,
    style=Style(
        line_style="dashed",
        line_color=Colors140.BlueViolet,
        line_width=3,
        fill_color=Colors140.Turquoise,
    ),
)
text(xy=(50, 25), text="Hello drawlib!", size=14)
```
