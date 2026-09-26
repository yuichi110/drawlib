# Drawlib Simple Project

This is a single-document technical documentation project created with [Drawlib](https://github.com/yuichi110/drawlib).

It is designed for single-page technical specifications, README illustrations, standalone design documents, or quick diagram prototyping without the overhead of multi-page sidebar navigation.

## 1. Project Structure

- `docs_src/`: Source authoring directory containing your document (**Source of Truth**).
  - `doc.md`: Primary Markdown document containing embedded Drawlib illustration code blocks.
- `docs_config.py`: Global configuration script executed before code blocks (custom styles, default fonts, canvas options).
- `docs_build.sh`: Automated shell script to compile Markdown and HTML targets.
- `docs/`: Generated Markdown document with rendered illustration images (**Never edit directly!**).
  - `doc.md`: Rendered Markdown file with relative image links, optimized for GitHub repository browsing.
  - `doc_images/`: Directory containing generated PNG/SVG illustration images.
- `docs_html/`: Generated static HTML document (**Never edit directly!**).
  - `doc.html`: Self-contained responsive HTML file with embedded styling.

## 2. Embedding Drawlib Illustrations

Write standard Markdown text and embed drawing code using ````drawlib```` code blocks:

````markdown
# Architecture Overview

Here is the high-level service design:

```drawlib 500px center show-code caption:"Figure 1: Service Architecture"
setup(width=100, height=50)

rectangle((25, 25), width=28, height=18, style="blue_flat", text="API Gateway", textstyle="white_bold")
rectangle((75, 25), width=28, height=18, style="green_flat", text="Core Service", textstyle="white_bold")

line((39, 25), (61, 25), arrowhead="->", style="bold")
text((50, 28), "REST / HTTPS")
```
````

### Block Header Options:
- **Image Width**: `500px`, `100%`, or integer (e.g. `400`).
- **Alignment**: `center`, `left`, or `right` (default: `center`).
- **Code Display Mode**:
  - `hide-code` (default): Renders illustration image only.
  - `show-code`: Displays Python source code block followed by the rendered image.
  - `fold-code`: Renders the image followed by a collapsed `<details>` source code dropdown.
- **Caption**: `caption:"Figure Title"` rendered in a `<figcaption>`.
- **Custom Filename**: `file:my_diagram.png` for an explicit output filename.

Drawlib automatically injects domain modules (`canvas`, `shapes`, `lines`, `text`, `icons`, `smartarts`, `charts`, `colors`, etc.) into the block namespace, so import statements are completely optional.

## 3. Building Documents

Compile both Markdown and HTML targets using the automated build script:

```bash
./docs_build.sh
```

Or run manual compilation via the Drawlib CLI:

```bash
# Build rendered Markdown for GitHub browsing:
drawlib build markdown docs_src/doc.md -o docs/doc.md -c docs_config.py

# Build self-contained HTML page:
drawlib build html docs_src/doc.md -o docs_html/doc.html -c docs_config.py
```

## 4. Rapid Illustration Development

During diagram iteration, avoid rebuilding the entire document. Use `drawlib export` or `drawlib show` to quickly test individual illustrations:

```bash
# Export block 1 with coordinate grid overlay for alignment:
drawlib export docs_src/doc.md 1 -g -o scratch/test.png

# Preview block 1 in a local desktop GUI window:
drawlib show docs_src/doc.md 1 --grid
```

## 5. Learning & Guidelines

For comprehensive syntax rules, component references, and styling guides, use the built-in CLI rules browser:

```bash
# List all available rule topics:
drawlib rules list

# View guidelines for specific topics:
drawlib rules show overview
drawlib rules show shapes
drawlib rules show lines
drawlib rules show docs_build
```
