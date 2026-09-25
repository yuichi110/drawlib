# Code Block Syntax & Options

Drawlib's document builder parses embedded drawing code blocks directly within Markdown and HTML documents. This page describes the supported syntax, header options, and execution rules.

---

## 1. Basic Syntax

Embedded drawing code blocks in Markdown use the `drawlib` language identifier:

````markdown
```drawlib
from drawlib.canvas import config
from drawlib.shapes import circle

config(width=100, height=100)
circle((50, 50), radius=30, style=styles.primary)
```
````

### Automatic Namespace Injection
To minimize repetitive boilerplate in documentation, Drawlib's compiler automatically injects core domain modules into every code block's global namespace:
- `canvas`, `shapes`, `lines`, `text`, `icons`, `images`
- `colors`, `preset_styles`, `fonts`, `types`, `math`
- `smartarts`, `diagrams`, `charts`

You can call primitives directly without needing `import` statements in every block.

---

## 2. Block Header Options

Options can be specified on the opening block line as space-separated tokens, `key:value` pairs, or `key=value` pairs:

````markdown
```drawlib 500px center show-code caption:"Figure 1: System Overview" file:arch.png
config(width=100, height=60)
# Drawing code...
```
````

### Supported Options Reference

| Option | Syntax Variations | Default | Description |
| :--- | :--- | :--- | :--- |
| **Code Visibility** | `show-code`, `fold-code`, `hide-code`<br>`code:show`, `code:fold`, `code:hide` | `hide` | Controls how the source code is displayed. `hide`: renders image only. `show-code`: renders syntax-highlighted code followed by image. `fold-code`: renders image followed by a collapsed `<details>` dropdown. |
| **Image Width** | `500px`, `100%`, `w:500px`, or integer `500` | `auto` | Maximum display width of the rendered image in HTML output. |
| **Image Height** | `300px`, `h:300px` | `auto` | Maximum display height of the rendered image. |
| **Alignment** | `center`, `left`, `right`<br>`a:center`, `align:center` | `center` | Horizontal alignment of the figure within the page. |
| **Filename** | `file:custom_name.png` | Auto-numbered (`1.png`, etc.) | Custom output filename for the rendered illustration file. |
| **Caption** | `caption:"Figure text"` | *None* | Descriptive caption displayed beneath the illustration in a `<figcaption>`. |
| **CSS Class** | `class:"shadow rounded border"` | *None* | Custom CSS classes applied to the wrapping `<figure>` element. |
| **Output Format** | `format:png`, `format:webp` | `png` | Image format for the rendered illustration file. |

---

## 3. Code Visibility Modes

### 3.1 `hide-code` (Default)
Renders only the final illustration without displaying the Python source code. Ideal for end-user documentation, architecture manuals, and slides.

### 3.2 `show-code`
Displays the syntax-highlighted Python code block followed immediately by the rendered illustration. Ideal for developer tutorials and API reference guides.

### 3.3 `fold-code`
Renders the illustration first, followed by a collapsible dropdown (`<details><summary>View Python Source Code</summary>...</details>`) containing the drawing code. In PDF export, the folded dropdown is cleanly omitted to preserve layout.

---

## 4. Alternative HTML Syntax

For authors writing raw HTML documentation or slides, Drawlib also supports native `<drawlib>` custom tags:

```html
<drawlib width="600px" align="center" caption="Microservices Architecture">
config(width=100, height=50)
rectangle((50, 25), width=80, height=30, text="API Gateway", style=styles.primary)
</drawlib>
```

Alternatively, `<script type="text/drawlib">` can be used:

```html
<script type="text/drawlib" data-width="500px" data-align="center">
circle((50, 50), radius=25, style=styles.primary)
</script>
```

---

## 5. Execution Context & Isolation

When compiling code blocks, `drawlib.doc_builder` guarantees complete isolation between illustrations:

1. **Canvas Clearing**: The drawing canvas is automatically reset before and after each block execution. Variables or shapes from earlier blocks do not leak into subsequent diagrams.
2. **Working Directory & Relative Assets**: The execution working directory is temporarily switched (`os.chdir`) to the document's parent directory. Relative file references (e.g. `image(xy=(50, 50), image="diagram.png")`) resolve reliably against the document's location.
3. **Deterministic Filename Generation**: Unless an explicit `file:name.png` option is provided, illustrations are assigned deterministic sequential names (`1.png`, `2.png`, ...) within a document-specific directory (e.g. `index_images/1.png`).

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>
