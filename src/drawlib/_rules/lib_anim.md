# Drawlib Animation Guidelines

Drawlib provides native support for generating multi-frame animations in both **Animated Portable Network Graphics (APNG)** and **Animated WebP** formats.  
Animations empower developers and AI coding agents to create clean, high-framerate, multi-step architectural illustrations and animated technical visualizations using declarative Python code.

---

## 1. Supported Animation Formats

| Format | File Extension | Primary Strength | Use Cases |
| :--- | :--- | :--- | :--- |
| **APNG** | `.png` | **Universal Compatibility**: Renders natively in all modern browsers and GitHub Markdown. Safe static fallback to frame 1 in PDF or legacy viewers. | GitHub READMEs, markdown documentation, printable technical documents. |
| **Animated WebP** | `.webp` | **Ultra-Compact File Size**: Typically ~50% smaller than APNG with lossless quality. Lossy compression also available. | Modern web applications, mobile platforms, web-hosted documentation sites. |

---

## 2. Imports & Canvas Lifecycle

All public animation classes are imported from `drawlib.anim`:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
```

### Universal Canvas Coordination
When an `Animation` instance is initialized, it automatically registers itself with the active Drawlib canvas (`canvas._active_animation`). Calling standard `save()` automatically captures all accumulated frames into an animated file based on the file extension:

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

### 3.1. Initialization: `Animation()`

```python
anim = Animation(
    fps: float | None = None,
    frame_rate: float | None = None,
    loop: int = 0,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `fps` | `float \| None` | `10.0` | Target frame rate in frames per second (e.g. `10.0` = 10 fps). |
| `frame_rate` | `float \| None` | `10.0` | Alias for `fps`. If both are specified, `fps` takes precedence. |
| `loop` | `int` | `0` | Number of animation playback loops. `0` means infinite continuous loop. |

---

## 4. Defining Frames

### 4.1. Context Manager (Recommended): `with anim.frame()`

Use the `with anim.frame()` context manager to define what is drawn in each frame.

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
| `duration` | `float \| None` | `None` | Display duration for this specific frame in **seconds** (e.g. `2.0` for 2 seconds). If `None`, defaults to `1 / fps` (e.g. 0.1s for 10fps). |
| `clear` | `bool` | `True` | Whether to clear existing canvas shapes before drawing this frame. Defaults to `True`. |

### 4.2. Imperative Method: `anim.add_frame()`

For procedural or loop-based drawing without `with` blocks:

```python
circle((x, y), radius=5, style=Styles.Primary)
anim.add_frame(duration=0.5, clear=True)
```

---

## 5. Animation Modes

### 5.1. Independent Frame Mode (`clear=True`, Default)
Each frame starts with an empty canvas. Ideal for moving objects, rotating elements, or physics simulations:

```python
anim = Animation(fps=10.0)

for x in range(10, 90, 10):
    with anim.frame():
        circle((x, 50), radius=5, style=Styles.Primary)
```

### 5.2. Cumulative / Step-by-Step Mode (`clear=False`)
Setting `clear=False` keeps elements from previous frames on the canvas. Ideal for architectural explanations that build up components step by step:

```python
anim = Animation(fps=1.0)

# Step 1: Base Client
with anim.frame(clear=True):
    rectangle((20, 50), width=20, height=15, style=Styles.PrimaryFlat, text="Client")

# Step 2: Gateway appears (Client remains!)
with anim.frame(clear=False):
    rectangle((50, 50), width=20, height=15, style=Styles.SecondaryFlat, text="Gateway")

# Step 3: Database appears (Client and Gateway remain!)
with anim.frame(clear=False, duration=3.0):  # Hold final completed diagram for 3 seconds
    rectangle((80, 50), width=20, height=15, style=Styles.AccentFlat, text="Database")
```

---

## 6. Saving Animations (`save()`)

Animations are saved using Drawlib's universal `save()` function:

```python
from drawlib.canvas import save

# Save as APNG
save("architecture_flow.png")

# Save as Animated WebP
save("architecture_flow.webp")

# Or explicit format override
save("pipeline", format="webp")
```

* Supported extensions: `.png` (APNG), `.webp` (Animated WebP), `.apng`.
* **Automatic Lossless Compression**:
  - **APNG**: Encoded with maximum zlib compression (`compress_level=9`), Huffman optimization (`optimize=True`), and native delta bounding box cropping.
  - **WebP**: Encoded with lossless compression (`lossless=True`) and size minimization (`minimize_size=True`).
* After `save()` completes, the active animation registry is automatically reset.

---

## 7. Documentation as Code (Markdown Embedded Blocks)

You can embed animations directly inside Markdown documents using the ````drawlib```` code fence. The document compiler automatically compiles the code block into an animated file:

````markdown
# System Event Pipeline

```drawlib 600px center file:packet_pipeline.png caption:"Live Packet Flow"
from drawlib.anim import Animation
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

setup(width=100, height=40)
anim = Animation(fps=10.0)

for x in range(30, 75, 5):
    with anim.frame():
        rectangle((20, 20), width=18, height=16, style=Styles.PrimaryFlat, text="App")
        rectangle((80, 20), width=18, height=16, style=Styles.AccentFlat, text="Queue")
        line((29, 20), (71, 20), style=Styles.MutedDashed)
        circle((x, 20), radius=3, style=Styles.Secondary)
```
````

To output WebP animations in Markdown, simply name the target file with `.webp` (e.g. `file:packet_pipeline.webp`) or specify `--format webp` in `drawlib build`.

---

## 8. Cross-Component Animation Design & Loop Best Practices (`anim-guide`)

For complete animation loop idioms and component-specific animation patterns across **Primitives** (`get_intermediate_colors`), **SmartArts** (`show=False` slot reservation), **Charts** (`max_value` pinning & series reveal), **Diagrams** (`.show`, `.draw_ratio`, pan/zoom), and **Auto-Layout Graphs** (`layout = g.calc()`), consult the dedicated Animation Guide:

```bash
uv run drawlib rules show anim-guide
```


