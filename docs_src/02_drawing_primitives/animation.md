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
    rectangle((25, 22.5), width=24, height=18, style=Styles.PrimaryFlat, text="Client App", text_style=Styles.WhiteBold)

# Step 2: Gateway appears
with anim.frame(clear=False, duration=1.2):
    rectangle((60, 22.5), width=24, height=18, style=Styles.SecondaryFlat, text="API Gateway", text_style=Styles.WhiteBold)
    line((37, 22.5), (48, 22.5), arrow_head="->", style=Styles.PrimaryBold)

# Step 3: Backend Services appear
with anim.frame(clear=False, duration=1.2):
    rectangle((95, 22.5), width=24, height=18, style=Styles.AccentFlat, text="Service Cluster", text_style=Styles.WhiteBold)
    line((72, 22.5), (83, 22.5), arrow_head="->", style=Styles.SecondaryBold)

# Step 4: Completed State (Held for 3 seconds before looping)
with anim.frame(clear=False, duration=3.0):
    rectangle((60, 6.0), width=60, height=7, style=Styles.SuccessFlat, text="Architecture Completed", text_style=Styles.WhiteBold)

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
    rectangle((20, 50), width=20, height=15, style=Styles.PrimaryFlat, text="Client")

# Stage 2: Gateway appears (Client remains)
with anim.frame(clear=False):
    rectangle((50, 50), width=20, height=15, style=Styles.SecondaryFlat, text="Gateway")

# Stage 3: Database appears (Client and Gateway remain)
with anim.frame(clear=False, duration=3.0):  # Hold final state for 3 seconds
    rectangle((80, 50), width=20, height=15, style=Styles.AccentFlat, text="Database")
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
    rectangle((50, 10), width=40, height=6, style=Styles.SuccessFlat, text="Deployment Complete")
```

---

## 7. Embedded Markdown Code Blocks

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
        rectangle((20, 20), width=18, height=16, style=Styles.PrimaryFlat, text="App")
        rectangle((80, 20), width=18, height=16, style=Styles.AccentFlat, text="Queue")
        line((29, 20), (71, 20), style=Styles.MutedDashed)
        circle((x, 20), radius=3, style=Styles.Secondary)
```
````

To output Animated WebP instead of APNG, specify a `.webp` extension in the `file:` attribute (e.g. `file:live_pipeline.webp`) or compile with `--format webp`.

---

## 8. Built-in Lossless Compression & Performance

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
