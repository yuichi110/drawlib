# 11. Documentation as Code: Embedded Drawlib Blocks

Drawlib unifies technical writing and architectural illustrations into a single, cohesive **Documentation as Code** workflow. Instead of exporting static PNG files that must be re-uploaded whenever code changes, you embed declarative drawing blocks directly within your Markdown documents.

## The ````drawlib```` Code Fence

Write diagrams inline within Markdown using the ````drawlib```` tag:

````markdown
# System Architecture

The following diagram illustrates our microservice communication topology:

```drawlib 600px center file:event_microservices.png caption:"Figure 1.1: Event-Driven Order Processing"
from drawlib.canvas import setup
from drawlib.shapes import rectangle
from drawlib.lines import line
from drawlib.styles import Styles

setup(width=100, height=40)
rectangle((25, 20), width=30, height=18, style=Styles.PrimaryFlat, text="Publisher", text_style=Styles.WhiteBold)
rectangle((75, 20), width=30, height=18, style=Styles.SecondaryFlat, text="Consumer", text_style=Styles.WhiteBold)
line((40, 20), (60, 20), arrow_head="->", style=Styles.DarkBold)
```
````

```drawlib 600px center file:doc_code_inline_block.png caption:"Figure 11.1: Embedded Drawlib Block Rendered Inline"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=36)
rectangle((25, 18), width=30, height=18, style=Styles.PrimaryFlat.patch(shape_r=2), text="Publisher", text_style=Styles.WhiteBold)
rectangle((75, 18), width=30, height=18, style=Styles.SecondaryFlat.patch(shape_r=2), text="Consumer", text_style=Styles.WhiteBold)
line((40, 18), (60, 18), arrow_head="->", style=Styles.DarkBold)
```

## Block Header Options

Drawlib's code fence header accepts flexible options:

| Option Category | Allowed Tokens | Description |
| :--- | :--- | :--- |
| **Code Visibility** | `hide-code` *(default)*, `show-code`, `fold-code` | Controls whether Python source is hidden, shown above image, or placed in a collapsible `<details>` dropdown. |
| **Dimensions** | `400px`, `600px`, `100%`, `w:500 h:300` | Target display width or CSS dimension string. |
| **Alignment** | `center` *(default)*, `left`, `right` | Horizontal image alignment. |
| **Figure Caption** | `caption:"Descriptive title"` | Renders a semantic `<figcaption>` below the illustration. |
| **Output File** | `file:custom_name.png` | Names the generated output image file instead of using index numbers (`1.png`). |

## Sandbox Isolation & Explicit Imports

- **Automatic Clear**: Drawlib invokes `canvas.clear()` before executing each embedded block. State, shapes, and variables from preceding diagrams will never leak into subsequent blocks.
- **Explicit Imports**: Every block explicitly imports what it needs (e.g. `from drawlib.shapes import circle`, `from drawlib.styles import Styles`). This guarantees reproducible compilation, full IDE autocompletion, and robust static type validation.
