# Welcome to the Drawlib Documentation!

Drawlib is a pure Python drawing library crafted to facilitate **Illustration as Code** rather than focusing solely on creating polished illustrations manually.



```python
from drawlib.canvas import config
from drawlib.colors import Colors, Colors140
from drawlib.shapes import circle, rectangle
from drawlib.text import text
from drawlib.types import Style

config(width=100, height=40)

circle(xy=(25, 20), radius=12, style=Style(fill_color=Colors140.Turquoise, line_color=Colors.Navy, line_width=2))
text(xy=(25, 20), text="Circle", style=Style(text_color=Colors.White, text_size=16))

rectangle(xy=(75, 20), width=24, height=24, style=Style(fill_color=Colors140.Coral, line_color=Colors.Navy, line_width=2))
text(xy=(75, 20), text="Rectangle", style=Style(text_color=Colors.White, text_size=16))
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="index_images/1.png" alt="index_1" style="width: 600px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Code makes Illustration</figcaption>
</figure>



---

## Documentation Navigation

### 1. Introductions
- [About Drawlib](./introductions/about.md)
- [Installation Guide](./introductions/install.md)
- [Library Design Philosophy](./introductions/lib_design.md)
- [Quick Start Guide](./introductions/quick_start.md)
- [Release Notes](./introductions/release_note.md)
- [Other Version Documentation](./introductions/other_version_docs.md)
- [Useful Links](./introductions/links.md)

### 2. Foundations
- [Canvas & Coordinate System](./foundations/canvas.md)
- [Coordinate Alignment](./foundations/coordinate_align.md)
- [Icons Guide](./foundations/icon.md)
- [Images Guide](./foundations/image.md)
- [Lines Guide](./foundations/line.md)
- [Line Styles](./foundations/line_style.md)
- [Shapes Overview](./foundations/shape.md)
- [Circle Shapes](./foundations/shape_circle.md)
- [Rectangle Shapes](./foundations/shape_rectangle.md)
- [Arrow Shapes](./foundations/shape_arrow.md)
- [Shape Styling](./foundations/shape_style.md)
- [Text Guide](./foundations/text.md)
- [Preset Styles Guide](./foundations/preset_styles.md)
- [Building Multiple Images](./foundations/build_many.md)
- [Programming Practices](./foundations/programming.md)

### 3. SmartArts Diagrams
- [SmartArts Overview](./smartarts/index.md)
- [SourceCode Highlighting](./smartarts/sourcecode.md)
- [Table Component](./smartarts/table.md)
- [Tree Component](./smartarts/tree.md)
- [BoxList Component](./smartarts/boxlist.md)
- [BubbleSpeech Component](./smartarts/bubblespeech.md)
- [BulletPoints Component](./smartarts/bulletpoints.md)
- [GridLayout Component](./smartarts/gridlayout.md)
- [Pyramid Component](./smartarts/pyramid.md)

### 4. Architecture Diagrams
- [Architecture Diagrams Guide](./diagrams/architecture.md)

### 5. Preset Styles
- [Official Default Preset Styles](./preset_styles/official_default.md)
- [Official Essentials Preset Styles](./preset_styles/official_essentials.md)
- [Official Monochrome Preset Styles](./preset_styles/official_monochrome.md)
- [Advanced Preset Styles Topics](./preset_styles/advanced_topics.md)
- [Creating Custom Preset Styles](./preset_styles/create.md)

### 6. Advanced Topics
- [Colors System](./advanced_topics/color.md)
- [Fonts System](./advanced_topics/font.md)
- [Dimage Image Processing](./advanced_topics/dimage.md)
- [Debugging Tools](./advanced_topics/debug.md)
- [Global Settings](./advanced_topics/settings.md)
- [CLI Options](./advanced_topics/cli_options.md)
- [Example Workflow](./advanced_topics/example_flow.md)
- [API Versioning](./advanced_topics/api_version.md)
- [Disable Linting](./advanced_topics/disable_lint.md)
- [Utility Functions](./advanced_topics/util.md)

---

<p align="center"><em>© 2026 drawlib by Yuichi Ito. Released under the Apache 2.0 License.</em></p>

