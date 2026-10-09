# Animations Overview (APNG & WebP)

Drawlib provides native support for generating multi-frame animations in both **Animated Portable Network Graphics (APNG)** and **Animated WebP** formats.  
Animations empower developers and AI coding agents to create clean, high-framerate, multi-step architectural illustrations, data visualizations, and interactive walkthroughs using declarative Python code.



<figure class="drawlib-image" style="text-align: center;">
  <img src="overview_images/animation_step_architecture.png" alt="overview_1" />
  <figcaption class="drawlib-caption">Step-by-Step Architecture Reveal</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=116, height=36)
anim = Animation(fps=1.0, loop=0)

# Step 1: Base Client
with anim.frame(clear=True, duration=0.9):
    rectangle((58, 22.0), width=110, height=23, style=Styles.MutedDashed.patch(shape_r=2.0))
    rectangle(
        (17.5, 22.0),
        width=21,
        height=16.5,
        style=Styles.Neutral.patch(shape_r=1.8),
        text="\nClient",
        text_style=Styles.DarkBold.patch(text_size=11.0),
    )
    phosphor.globe((17.5, 25.3), width=4.6, style=Styles.Dark)

# Step 2: Gateway appears (Hero focal node)
with anim.frame(clear=False, duration=0.9):
    rectangle(
        (44.5, 22.0),
        width=21,
        height=16.5,
        style=Styles.PrimaryFlat.patch(shape_r=1.8),
        text="\nGateway",
        text_style=Styles.WhiteBold.patch(text_size=11.0),
    )
    phosphor.shield_check((44.5, 25.3), width=4.6, style=Styles.White)
    line((28.0, 22.0), (34.0, 22.0), arrow_head="->", style=Styles.DarkBold)

# Step 3: Compute Service appears
with anim.frame(clear=False, duration=0.9):
    rectangle(
        (71.5, 22.0),
        width=21,
        height=16.5,
        style=Styles.PrimaryNeutral.patch(shape_r=1.8),
        text="\nCompute",
        text_style=Styles.DarkBold.patch(text_size=11.0),
    )
    phosphor.cpu((71.5, 25.3), width=4.6, style=Styles.Primary)
    line((55.0, 22.0), (61.0, 22.0), arrow_head="->", style=Styles.DarkBold)

# Step 4: Database & Completed State (Held for 2.5 seconds before looping)
with anim.frame(clear=False, duration=2.5):
    rectangle(
        (98.5, 22.0),
        width=21,
        height=16.5,
        style=Styles.SecondaryNeutral.patch(shape_r=1.8),
        text="\nDatabase",
        text_style=Styles.DarkBold.patch(text_size=11.0),
    )
    phosphor.database((98.5, 25.3), width=4.6, style=Styles.Secondary)
    line((82.0, 22.0), (88.0, 22.0), arrow_head="->", style=Styles.DarkBold)
    rectangle(
        (58, 5.2),
        width=58,
        height=6.0,
        style=Styles.PrimaryNeutral.patch(shape_r=1.5),
        text="Architecture Completed",
        text_style=Styles.DarkBold.patch(text_size=11.0),
    )

save()
```

</details>



---

## 1. Supported Animation Formats

| Format | Extension | Primary Advantage | Best Use Cases |
| :--- | :--- | :--- | :--- |
| **APNG** | `.png`, `.apng` | **Universal Compatibility**: Renders natively in all modern web browsers and GitHub Markdown previews. Safe static fallback to Frame 1 in PDF compilers and legacy viewers. | GitHub READMEs, markdown documentation, printable technical documents. |
| **Animated WebP** | `.webp` | **Ultra-Compact File Size**: Typically ~50% smaller than APNG with lossless quality. | Web-hosted documentation sites, high-performance web applications, mobile platforms. |

---

## 2. Imports & Canvas Lifecycle

All animation functionality is centered around the `Animation` class in `drawlib.anim`:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
```

### Automatic Canvas Coordination & Saving (`save()`)
When an `Animation` instance is initialized, it automatically registers itself with the active Drawlib canvas (`canvas._active_animation`). Calling standard `save()` captures all accumulated frames into an animated file without requiring separate export methods:

```python
anim = Animation(fps=10.0)

with anim.frame():
    circle((50, 50), radius=10, style=Styles.Primary)

# Saves as APNG (.png or .apng):
save("animation.png")
save("animation.apng")

# Saves as Animated WebP (.webp):
save("animation.webp")

# Or specify format explicitly ("webp", "png", or "apng"):
save("pipeline", format="webp")
```

> **Note**: Animations are raster frame sequences and cannot be exported as SVG. Calling `save("out.svg")` or `save("out", format="svg")` while an `Animation` is active raises a `ValueError`. Calling `save()` when zero frames have been captured also raises a `ValueError`.

---

## 3. The `Animation` Class API

### 3.1. Initialization & Read-Only Properties

```python
anim = Animation(
    fps: float | None = None,
    frame_rate: float | None = None,
    loop: int = 0,
)
```

| Parameter / Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `fps` | `float \| None` | `10.0` | Target playback frame rate in frames per second (e.g. `10.0` means 10 fps). Must be `> 0`. |
| `frame_rate` | `float \| None` | `10.0` | Alias for `fps`. If both are specified, `fps` takes precedence. |
| `loop` | `int` | `0` | Number of animation loops (`>= 0`). `0` means continuous infinite looping. |
| `anim.fps` | `float` *(read-only)* | — | Returns the active playback frame rate in frames per second. |
| `anim.frame_rate` | `float` *(read-only)* | — | Read-only alias for `anim.fps`. |

---

## 4. Defining Frames

### 4.1. Context Manager: `with anim.frame()` (Recommended)

The `with anim.frame()` context manager clears the canvas at the start of the block (when `clear=True`) and captures the rendered frame at the end of the block:

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

For procedural code where context managers are less convenient:

```python
circle((x, y), radius=5, style=Styles.Primary)
anim.add_frame(duration=0.5, clear=True)
```

---

## 5. Two Standard Animation Loop Idioms

When animating technical illustrations, **prefer `clear=True` (default per-frame redraw)** over `clear=False` whenever elements move, change styles, or toggle highlights. Drawlib's unified component lifecycle (`add()` -> `draw()`) provides two clean loop patterns depending on the module:

| Target Module | Recommended Loop Pattern | Guide |
| :--- | :--- | :--- |
| **Primitives** (`shapes`, `lines`, `text`, `icons`, `styles`) | **Pattern A: In-Frame Build**<br>Compute per-frame coordinates (`get_intermediate_points`, `get_intermediate_paths`) or interpolated colors (`get_intermediate_colors`) and draw inside `with anim.frame():`. | [Animating Primitives & Colors](./primitives.md) |
| **SmartArts** (`ChevronProcess`, `Table`, `TreeNode`, etc.) | **Pattern B: Pre-Build & Mutate** (or Pattern A)<br>Register items once via `item = comp.add(...)` and mutate `item.show`, `item.style`, `item.text_style`, or `item.text` before `draw(..., scale=1.0)`. Hidden items still reserve layout slots. | [Animating SmartArts](./smartarts.md) |
| **Charts** (`BarChart`, `LineChart`, `PieChart`, `GanttChart`, etc.) | **Pattern B: Pre-Build & Mutate**<br>Register series/slices/tasks once outside the loop (`s = chart.add_series(...)`), then mutate `s.show`, `s.draw_ratio`, `s.draw_direction`, or `s.style` inside `with anim.frame():` before `chart.draw()`. Auto-scales remain 100% locked. | [Animating Charts](./charts.md) |
| **Technical Diagrams** (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`, etc.) | **Pattern B: Pre-Build & Mutate**<br>Build topology once outside the loop, then mutate `.show` (auto-hides incident edges and dangling `Junction` wires), `.style`, `.text_style`, or `.set_label()` and call `draw(xy, scale)` in each frame. | [Animating Technical Diagrams](./diagrams.md) |
| **Auto-Layout Graphs** (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, etc.) | **Pattern B: Pre-Build & Mutate**<br>`g.calc()` solves coordinates across the full topology regardless of `show=False`; mutate `node.show`, `cluster.show`, or `edge.style` and call `g.draw()`, or animate packets along `edge_layout.points`. | [Animating Auto-Layout Graphs](./graphs.md) |



<figure class="drawlib-image" style="text-align: center;">
  <img src="overview_images/anim_overview_patterns_workflow.png" alt="overview_2" />
  <figcaption class="drawlib-caption">Pattern A (In-Frame Build) vs. Pattern B (Pre-Build Outside Loop & Mutate Inside Frame)</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=68)

# Left Panel: Pattern A (In-Frame Build)
rectangle((32.5, 34.0), width=57, height=60, style=Styles.Neutral.patch(shape_r=2.5))
phosphor.play_circle((9.5, 58.5), width=4.6, style=Styles.Primary)
text((34.5, 58.5), "Pattern A: In-Frame", style=Styles.DarkBold.patch(text_size=11.0))
text((32.5, 53.0), "Primitives (shapes, lines)", style=Styles.Dark.patch(text_size=10.0))

rectangle((32.5, 43.0), width=51, height=11.0, style=Styles.White.patch(shape_r=1.8))
text((32.5, 43.0), "1. Pre-compute points\n& interpolated colors", style=Styles.DarkBold.patch(text_size=10.0))

line((32.5, 37.5), (32.5, 33.5), arrow_head="->", style=Styles.DarkBold)

rectangle((32.5, 24.5), width=51, height=17.5, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
text((32.5, 29.8), "2. with anim.frame():", style=Styles.PrimaryBold.patch(text_size=10.0))
rectangle((32.5, 21.0), width=46, height=8.5, style=Styles.White.patch(shape_r=1.2))
text((32.5, 21.0), "Draw shapes at xy_i", style=Styles.Dark.patch(text_size=10.0))

line((32.5, 15.7), (32.5, 12.2), arrow_head="->", style=Styles.DarkBold)

rectangle((32.5, 8.5), width=42, height=7.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
text((32.5, 8.5), "3. save() -> APNG/WebP", style=Styles.DarkBold.patch(text_size=10.0))

# Right Panel: Pattern B (Pre-Build & Mutate)
rectangle((93.5, 34.0), width=57, height=60, style=Styles.Neutral.patch(shape_r=2.5))
phosphor.tree_structure((70.0, 58.5), width=4.6, style=Styles.Primary)
text((95.5, 58.5), "Pattern B: Pre-Build", style=Styles.DarkBold.patch(text_size=11.0))
text((93.5, 53.0), "SmartArts, Charts, Graphs", style=Styles.Dark.patch(text_size=10.0))

rectangle((93.5, 43.0), width=51, height=11.0, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
text((93.5, 43.0), "1. Build topology once\noutside loop (locks layout)", style=Styles.DarkBold.patch(text_size=10.0))

line((93.5, 37.5), (93.5, 33.5), arrow_head="->", style=Styles.DarkBold)

rectangle((93.5, 24.5), width=51, height=17.5, style=Styles.PrimaryFlat.patch(shape_r=1.8))
text((93.5, 29.8), "2. with anim.frame():", style=Styles.WhiteBold.patch(text_size=10.0))
rectangle((93.5, 21.0), width=46, height=8.5, style=Styles.White.patch(shape_r=1.2))
text((93.5, 21.0), "Mutate .show / .style -> draw()", style=Styles.DarkBold.patch(text_size=10.0))

line((93.5, 15.7), (93.5, 12.2), arrow_head="->", style=Styles.DarkBold)

rectangle((93.5, 8.5), width=42, height=7.0, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
text((93.5, 8.5), "3. save() -> APNG/WebP", style=Styles.DarkBold.patch(text_size=10.0))

save()
```

</details>



---

## 6. Design Principles & Recommended `fps` / Frame `duration` Strategy

| Animation Type | Recommended `fps` | Frame `duration` Strategy | Final Hold `duration` |
| :--- | :--- | :--- | :--- |
| **Continuous Motion / Transitions** (moving packets, growing chart series via `draw_ratio`, color fades, camera pan/zoom) | `fps=8.0` – `12.0` | `0.08s` – `0.14s` per motion frame (or default `1 / fps`) | `duration=2.0` – `3.0` |
| **Step-by-Step Architectural Walkthrough** (revealing pipeline stages, chart series, or diagram/graph nodes one by one) | `fps=1.0` – `2.0` | `0.6s` – `1.0s` per step | `duration=2.5` – `3.0` |

1. **Poster Frame Principle (Static & PDF Compatibility)**:
   Standard image viewers and vector PDF exports render **Frame 1** as a static fallback image. Never leave Frame 1 completely blank—always show the baseline container or initial node on Frame 1.
2. **Hold the Final Completed Frame**:
   To give readers time to absorb the completed diagram before the loop restarts, set an extended `duration` (`2.0` to `3.0` seconds) on the final frame.
3. **Embedded Markdown Blocks**:
   Any ````drawlib```` block that initializes `Animation()` automatically outputs an animated `.png` (APNG) or `.webp` file during `drawlib build`.
4. **Built-in Lossless Compression**:
   - **APNG (`.png` / `.apng`)**: Automatically crops sub-frame delta bounding boxes and applies maximum Zlib (`compress_level=9`) + Huffman (`optimize=True`) compression.
   - **Animated WebP (`.webp`)**: Encodes with lossless sub-frame minimization (`lossless=True`, `minimize_size=True`), typically ~50% smaller than APNG.

---

## 7. Interactive Playback Control in Presentation Slides (`slide`)

In 16:9 presentation slide decks (`drawlib init slide`), animated `.png` (APNG) and `.webp` blocks can be controlled interactively via `<canvas>` playback options on the ````drawlib```` fence:

````markdown
```drawlib file:pipeline.webp anim-trigger:click anim-loop:once anim-pause:2,4
from drawlib.anim import Animation
...
```
````

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| **`anim-trigger`** | `auto` \| `click` | `auto` | `auto` starts playback as soon as the slide appears; `click` holds on Frame 0 (`READY`) until the presenter clicks the diagram. |
| **`anim-loop`** | `once` \| `infinite` | `infinite` (`once` when `anim-pause` is set) | `once` stops on the final frame (`ENDED`, click to replay from Frame 0); `infinite` loops continuously. |
| **`anim-pause`** | Comma-separated 0-based frame indices (e.g. `2,4`) | `None` | Pauses playback (`PAUSED`) immediately upon rendering each listed frame index. Clicking the diagram resumes playback from `frame + 1` until the next pause point or end. |



<figure class="drawlib-image" style="text-align: center;">
  <img src="overview_images/anim_overview_slide_playback_states.png" alt="overview_3" />
  <figcaption class="drawlib-caption">Interactive Slide Animation Playback State Machine (READY, PLAYING, PAUSED, ENDED)</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.state import InitialState, State, StateDiagram
from drawlib.styles import Styles

setup(width=126, height=62)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

init = sd.add(InitialState(), xy=(6.0, 39.0))
ready = sd.add(
    State("READY", shape="box", entry="Frame 0", width=23.0, style=Styles.Neutral.patch(text_size=10.5)),
    xy=(28.0, 39.0),
)
playing = sd.add(
    State("PLAYING", shape="box", do="render", width=26.0, style=Styles.PrimaryNeutral.patch(text_size=10.5)),
    xy=(69.0, 39.0),
)
paused = sd.add(
    State("PAUSED", shape="box", entry="pause:2,4", width=26.0, style=Styles.SecondaryNeutral.patch(text_size=10.5)),
    xy=(69.0, 11.0),
)
ended = sd.add(
    State("ENDED", shape="box", entry="Final", width=23.0, style=Styles.Neutral.patch(text_size=10.5)),
    xy=(110.0, 39.0),
)

sd.connect(init, ready, label="init")
sd.connect(ready, playing, label="click")
sd.connect(
    playing,
    paused,
    label="pause",
    bend=0.5,
    start_side="bottom_left",
    end_side="top_left",
)
sd.connect(
    paused,
    playing,
    label="resume",
    bend=0.5,
    start_side="top_right",
    end_side="bottom_right",
)
sd.connect(playing, ended, label="end")
sd.connect(
    ended,
    playing,
    label="replay",
    bend=0.35,
    start_side="top",
    end_side="top",
    style=Styles.PrimaryBold,
)

sd.draw()
save()
```

</details>



