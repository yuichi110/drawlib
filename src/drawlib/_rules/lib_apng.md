# Drawlib APNG Animation Guidelines

Drawlib provides native support for generating **Animated Portable Network Graphics (APNG)**.  
APNG enables developers and AI coding agents to create clean, high-framerate, multi-step architectural illustrations and animated technical visualizations using declarative Python code.

---

## 1. Why APNG in Drawlib?

Unlike legacy GIF animations (which are constrained to 256 indexed colors and binary transparency), APNG features:
* **24-bit RGB and 32-bit RGBA Full Color**: Gradients, soft drop shadows, and subtle fills remain crisp and uncompressed.
* **Alpha Channel Transparency**: Transparent backgrounds blend seamlessly into light and dark documentation themes.
* **Zero Extra Dependencies**: Relies on native Pillow (`save_all=True`), requiring no external binary packages like `ffmpeg`.
* **Universal Browser Support**: Supported natively by all modern web browsers (Chrome, Firefox, Safari, Edge) and GitHub Markdown previews.
* **Safe Static Fallback**: Standard PNG decoders (and PDF compilers) automatically display the 1st frame as a clean static image.

---

## 2. Imports & Core Architecture

All public APNG classes are imported from `drawlib.apng`:

```python
from drawlib.apng import Apng
from drawlib.canvas import setup, save
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
```

---

## 3. The `Apng` Class API

### 3.1. Initialization: `Apng()`

```python
anim = Apng(
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

When instantiated, `Apng` automatically registers itself with the active Drawlib canvas (`canvas._active_animation`), allowing standard canvas functions like `save()` to capture all accumulated frames.

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
anim = Apng(fps=10.0)

for x in range(10, 90, 10):
    with anim.frame():
        circle((x, 50), radius=5, style=Styles.Primary)
```

### 5.2. Cumulative / Step-by-Step Mode (`clear=False`)
Setting `clear=False` keeps elements from previous frames on the canvas. Ideal for architectural explanations that build up components step by step:

```python
anim = Apng(fps=1.0)

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

APNG animations are saved using Drawlib's universal `save()` function:

```python
from drawlib.canvas import save

# Save to explicit file
save("animation.png")

# Or omit arguments to save to <script_name>.png
save()
```

* Supported extensions: `.png` (recommended) or `.apng`.
* **CLI and Build Directory Awareness**: `save()` automatically honors `--output` (`-o`) directories specified via `drawlib build image` or `drawlib show`.
* **Built-in Lossless Compression**: `save()` automatically enables maximum zlib compression (`compress_level=9`), Huffman optimization (`optimize=True`), and sub-frame delta cropping without any quality degradation or external dependencies.
* After `save()` completes, the active animation registry is automatically reset.

---

## 7. Documentation as Code (Markdown Embedded Blocks)

You can embed APNG animations directly inside Markdown documents using the ````drawlib```` code fence. The document compiler automatically compiles the code block into an animated APNG file:

````markdown
# System Event Pipeline

The diagram below shows live packet progression through the pipeline:

```drawlib 600px center file:packet_pipeline.png caption:"Live Packet Flow"
from drawlib.apng import Apng
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

setup(width=100, height=40)
anim = Apng(fps=10.0)

for x in range(30, 75, 5):
    with anim.frame():
        rectangle((20, 20), width=18, height=16, style=Styles.PrimaryFlat, text="App")
        rectangle((80, 20), width=18, height=16, style=Styles.AccentFlat, text="Queue")
        line((29, 20), (71, 20), style=Styles.MutedDashed)
        circle((x, 20), radius=3, style=Styles.Secondary)
```
````

* When compiled via `drawlib build html` or `drawlib build markdown`, `packet_pipeline.png` is generated as an animated APNG in the document's companion image folder.
* Web browsers display the animation automatically with no extra JavaScript or plugins.

---

## 8. Practical Code Examples

### 8.1. Circular Orbit Animation (30 Frames, 10 FPS, 3 Seconds)

```python
import math
from drawlib.apng import Apng
from drawlib.canvas import save, setup
from drawlib.shapes import circle
from drawlib.styles import Styles

setup(width=100, height=100)

fps = 10
total_seconds = 3
total_frames = fps * total_seconds

anim = Apng(fps=fps, loop=0)

cx, cy = 50.0, 50.0
orbit_radius = 30.0

for i in range(total_frames):
    angle = 2.0 * math.pi * (i / total_frames)
    x = cx + orbit_radius * math.cos(angle)
    y = cy + orbit_radius * math.sin(angle)

    with anim.frame():
        circle((cx, cy), radius=orbit_radius, style=Styles.MutedDashed)
        circle((cx, cy), radius=3, style=Styles.Secondary)
        circle((x, y), radius=6, style=Styles.Primary)

save("circle_orbit.png")
```

### 8.2. Holding the Final Frame

To pause on the final frame (giving viewers time to read the completed diagram before looping), set `duration` on the final frame:

```python
anim = Apng(fps=5.0)  # Standard frames last 0.2s

for i in range(10):
    with anim.frame():
        draw_stage(i)

# Final completed state held for 2.5 seconds
with anim.frame(duration=2.5):
    draw_stage(10)
    text((50, 10), "Completed!", style=Styles.SuccessBold)

save("pipeline_complete.png")
```
