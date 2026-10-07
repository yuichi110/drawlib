# Animations (APNG & WebP)

Drawlib provides native support for generating multi-frame animations in both **Animated Portable Network Graphics (APNG)** and **Animated WebP** formats.  
Animations empower developers and AI coding agents to create clean, high-framerate, multi-step architectural illustrations and animated technical visualizations using declarative Python code.

---

## 1. Supported Animation Formats

| Format | Extension | Primary Advantage | Best Use Cases |
| :--- | :--- | :--- | :--- |
| **APNG** | `.png` | **Universal Compatibility**: Renders natively in all modern web browsers and GitHub Markdown previews. Safe static fallback to 1st frame in PDF compilers and legacy viewers. | GitHub READMEs, markdown documentation, printable technical documents. |
| **Animated WebP** | `.webp` | **Ultra-Compact File Size**: Typically ~50% smaller than APNG with lossless quality. | Web-hosted documentation sites, high-performance web applications, mobile platforms. |

```drawlib 650px center file:animation_step_architecture.png caption:"Step-by-Step Architecture Reveal"
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=120, height=45)
anim = Animation(fps=1.0, loop=0)

# Step 1: Base Client
with anim.frame(clear=True, duration=1.2):
    rectangle((60, 22.5), width=116, height=38, style=Styles.MutedDashed)
    rectangle((25, 22.5), width=24, height=18, style=Styles.Neutral, text="Client App")

# Step 2: Gateway appears (Hero node)
with anim.frame(clear=False, duration=1.2):
    rectangle((60, 22.5), width=24, height=18, style=Styles.PrimaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
    line((37, 22.5), (48, 22.5), arrow_head="->", style=Styles.DarkBold)

# Step 3: Backend Services appear
with anim.frame(clear=False, duration=1.2):
    rectangle((95, 22.5), width=24, height=18, style=Styles.SecondaryNeutral, text="Service Cluster")
    line((72, 22.5), (83, 22.5), arrow_head="->", style=Styles.DarkBold)

# Step 4: Completed State (Held for 3 seconds before looping)
with anim.frame(clear=False, duration=3.0):
    rectangle((60, 6.0), width=60, height=7, style=Styles.PrimaryNeutral, text="Architecture Completed")

save()
```

---

## 2. Imports & Canvas Lifecycle

All animation functionality is centered around the `Animation` class in `drawlib.anim`:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle, circle
from drawlib.styles import Styles
```

### Automatic Canvas Coordination
When an `Animation` instance is initialized, it automatically registers itself with the active Drawlib canvas (`canvas._active_animation`). Calling standard `save()` captures all accumulated frames into an animated file without requiring separate export methods:

```python
anim = Animation(fps=10.0)

with anim.frame():
    circle((50, 50), radius=10, style=Styles.Primary)

# Saves as APNG:
save("animation.png")

# Or saves as Animated WebP:
save("animation.webp")
```

---

## 3. The `Animation` Class API

### 3.1. Initialization

```python
anim = Animation(
    fps: float | None = None,
    frame_rate: float | None = None,
    loop: int = 0,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `fps` | `float \| None` | `10.0` | Target playback frame rate in frames per second (e.g. `10.0` means 10 fps). |
| `frame_rate` | `float \| None` | `10.0` | Alias for `fps`. If both are specified, `fps` takes precedence. |
| `loop` | `int` | `0` | Number of animation loops. `0` means continuous infinite looping. |

---

## 4. Defining Frames

### 4.1. Context Manager: `with anim.frame()` (Recommended)

The `with anim.frame()` context manager captures the canvas state at the end of each block.

```python
with anim.frame(
    duration: float | None = None,
    clear: bool = True,
):
    # Standard Drawlib drawing calls
    circle((50, 50), radius=10, style=Styles.Primary)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `duration` | `float \| None` | `None` | Display duration for this frame in **seconds** (e.g. `1.5` for 1.5 seconds). If `None`, defaults to `1 / fps` (e.g. 0.1s for 10fps). |
| `clear` | `bool` | `True` | Whether to clear existing canvas shapes before drawing this frame. Defaults to `True`. |

### 4.2. Imperative Method: `anim.add_frame()`

For procedural code or loops where context managers are less convenient:

```python
circle((x, y), radius=5, style=Styles.Primary)
anim.add_frame(duration=0.5, clear=True)
```

---

## 5. Animation Modes

Drawlib supports two fundamental animation paradigms:

### 5.1. Independent Frame Mode (`clear=True`, Default)
Each frame starts with an empty canvas. This mode is ideal for moving objects, rotating elements, or physics simulations:

```python
anim = Animation(fps=10.0)

for x in range(10, 90, 10):
    with anim.frame():
        circle((x, 50), radius=5, style=Styles.Primary)
```

### 5.2. Cumulative / Step-by-Step Mode (`clear=False`)
Setting `clear=False` keeps shapes from preceding frames on the canvas. This mode is exceptionally effective for architectural explanations that reveal components stage by stage:

```python
anim = Animation(fps=1.0)

# Stage 1: Ingress
with anim.frame(clear=True):
    rectangle((20, 50), width=20, height=15, style=Styles.Neutral, text="Client")

# Stage 2: Gateway appears (Client remains)
with anim.frame(clear=False):
    rectangle((50, 50), width=20, height=15, style=Styles.PrimaryFlat, text="Gateway", text_style=Styles.WhiteBold)

# Stage 3: Database appears (Client and Gateway remain)
with anim.frame(clear=False, duration=3.0):  # Hold final state for 3 seconds
    rectangle((80, 50), width=20, height=15, style=Styles.SecondaryNeutral, text="Database")
```

---

## 6. Timing & Duration Control

### Frame Duration in Seconds
Frame timing is configured directly in **seconds** (e.g. `duration=0.25` for a quarter of a second, `duration=2.0` for two seconds).

### Holding the Final Frame
To give readers sufficient time to inspect a completed diagram before the animation loops, specify an extended `duration` on the final frame:

```python
anim = Animation(fps=5.0)  # Standard frames display for 0.2s

for i in range(10):
    with anim.frame():
        draw_stage(i)

# Hold final completed architecture for 3.0 seconds
with anim.frame(duration=3.0):
    draw_stage(10)
    rectangle((50, 10), width=40, height=6, style=Styles.PrimaryNeutral, text="Deployment Complete")
```

---

## 7. Component Animation Best Practices & Loop Idioms

Drawlib's high-level components (`smartarts`, `charts`, `diagrams`, and `graph`) are designed from the ground up to work seamlessly with `Animation`. Depending on the module, use one of two clean loop patterns with `clear=True` (default):

| Module Category | Recommended Loop Idiom | Key Benefit |
| :--- | :--- | :--- |
| **Primitives / SmartArts / Charts** | **In-Frame Build**: Construct inside `with anim.frame():` using `add(..., show=...)` and `draw()`. | Hidden items (`show=False`) automatically reserve layout slots and chart axis limits (`max_value`, `xlim`/`ylim`). |
| **Diagrams / Auto-Layout Graphs** | **Pre-Build & Mutate**: Construct once before the loop, then mutate `.show`, `.style`, or `.draw_ratio` inside `with anim.frame():`. | Avoids re-declaring topologies; connected edges and dangling junctions hide automatically when a node is hidden. |

### 7.1. Primitives & Smooth Color Transitions (`get_intermediate_colors`)
Use `get_intermediate_colors(color1, color2, num=..., include_ends=True)` from `drawlib.styles` with `.patch(shape_fill_color=c)` to animate smooth color fades:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors

setup(width=80, height=35)
anim = Animation(fps=10.0)

for i, bg in enumerate(get_intermediate_colors(Colors.White, Colors.Primary, num=4, include_ends=True)):
    with anim.frame(duration=1.5 if i == 4 else 0.12):
        card_style = Styles.Neutral.patch(shape_fill_color=bg)
        text_style = Styles.WhiteBold if i >= 3 else Styles.DarkBold
        rectangle((40, 17.5), width=40, height=16, style=card_style, text="Active Node", text_style=text_style)

save()
```

### 7.2. SmartArts Progressive Reveal (`add(..., show=...)`)
Pass `show=(i <= step)` when adding stages or rows, and highlight the active step via conditional styles:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=110, height=35)
anim = Animation(fps=1.5)
stages = ["Plan", "Build", "Test", "Deploy"]

for step in range(len(stages)):
    with anim.frame(duration=2.5 if step == len(stages) - 1 else 0.8):
        proc = ChevronProcess(style=Styles.Neutral, text_style=Styles.DarkBold, flat_left_end=True)
        for i, name in enumerate(stages):
            style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
            t_style = Styles.WhiteBold if i == step else Styles.DarkBold
            proc.add(name, style=style, text_style=t_style, show=(i <= step))
        proc.draw(xy=(5, 10), width=100, height=15)

save()
```

### 7.3. Charts: Series Reveal vs. Value Growth
- **Series Reveal**: Add all series and toggle `show=(i <= step)`. Even when `show=False`, the chart includes all series when computing axis bounds so the Y-axis never jumps.
- **Value Growth**: Pin `max_value` (or `ylim`) on the chart constructor and multiply values by a progress ratio `r`:

```python
for r in [0.25, 0.5, 0.75, 1.0]:
    with anim.frame(duration=2.0 if r == 1.0 else 0.15):
        chart = BarChart(title="Score", categories=["A", "B", "C"], max_value=100)
        chart.add("2026", [round(v * r, 1) for v in [45, 85, 65]], style=Styles.PrimaryFlat)
        chart.draw(xy=(12, 10), width=78, height=45)
```

### 7.4. Diagrams & Graphs: Mutating `.show`, `.style`, `.draw_ratio`, and `scale`
Pre-build the diagram once, keep references to nodes and edges, and mutate their attributes per frame:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=110, height=40)
anim = Animation(fps=8.0)

flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark)
n1 = flow.add(Start("Start"), xy=(20, 20))
n2 = flow.add(Process("Validate", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=(55, 20), show=False)
n3 = flow.add(End("Done", style=Styles.SecondaryNeutral), xy=(90, 20), show=False)
e1 = n1.connect(n2)
e2 = n2.connect(n3)

with anim.frame(duration=0.5):
    flow.draw()

n2.show = True
for r in [0.4, 0.8, 1.0]:
    with anim.frame(duration=0.15):
        e1.draw_ratio = r
        flow.draw()

n2.style = Styles.PrimaryNeutral
n2.text_style = Styles.DarkBold
n3.show = True
for r in [0.4, 0.8, 1.0]:
    with anim.frame(duration=2.0 if r == 1.0 else 0.15):
        e2.draw_ratio = r
        flow.draw()

save()
```

---

## 8. Embedded Markdown Code Blocks

You can embed animations directly inside Markdown documents using the ````drawlib```` code fence. The document compiler automatically compiles the code block into an animated file:

````markdown
# Live Event Pipeline

```drawlib 600px center file:live_pipeline.png caption:"Event Progression"
from drawlib.anim import Animation
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

setup(width=100, height=40)
anim = Animation(fps=10.0)

for x in range(30, 75, 5):
    with anim.frame():
        rectangle((20, 20), width=18, height=16, style=Styles.Neutral, text="App")
        rectangle((80, 20), width=18, height=16, style=Styles.PrimaryFlat, text="Queue", text_style=Styles.WhiteBold)
        line((29, 20), (71, 20), style=Styles.MutedDashed)
        circle((x, 20), radius=3, style=Styles.Dark)
```
````

To output Animated WebP instead of APNG, specify a `.webp` extension in the `file:` attribute (e.g. `file:live_pipeline.webp`) or compile with `--format webp`.

---

## 9. Built-in Lossless Compression & Performance

Drawlib automatically applies multi-tier lossless optimization when saving animations:

1. **APNG Compression**:
   - Sub-frame delta bounding box cropping (`delta.getbbox()`).
   - Maximum Zlib compression level (`compress_level=9`).
   - Huffman tree optimization (`optimize=True`).
2. **Animated WebP Compression**:
   - Fully lossless encoding (`lossless=True`).
   - Automatic delta sub-frame size minimization (`minimize_size=True`).
   - Generates files approximately 40%–60% smaller than APNG.

### Best Practice for Animation Performance
* **Frame Rate (`fps`)**: For technical diagrams, a frame rate of **5 to 10 FPS** provides fluid motion while maintaining compact file sizes (typically under 100 KB) and fast build times.
