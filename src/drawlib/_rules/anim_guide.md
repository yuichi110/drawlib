# Drawlib Animation Design & Best Practices Guide

This guide defines the architectural principles, loop idioms, and component-specific patterns for creating multi-frame animations (`APNG` and `Animated WebP`) across all Drawlib modules.

*(For the core `Animation` class API, `with anim.frame()`, and file saving options, run `uv run drawlib rules show lib-anim`.)*

---

## 1. Core Animation Design Principles

### 1.1. Prefer Per-Frame Redraw (`clear=True`) Over Cumulative (`clear=False`)
When `with anim.frame():` executes with its default `clear=True`, Drawlib clears the canvas at the start of the frame and draws the complete scene for that instant.
- **Why `clear=True` is strongly recommended**:
  - Allows elements to move (`xy`), scale, or change style (`Styles.PrimaryFlat` -> `Styles.PrimaryNeutral`) without leaving behind stale drawings from previous frames.
  - Works seamlessly with all high-level components (`SmartArts`, `Charts`, `Diagrams`, `Graph`) via their `.show` and `.style` controls (plus `.draw_ratio` / `.draw_direction` on `Charts`).
- **When to use `clear=False`**:
  - Only when strictly appending static primitive shapes onto the canvas without ever moving, un-highlighting, or modifying previously drawn elements.

### 1.2. Poster Frame Principle (Static & PDF Compatibility)
Standard image viewers, GitHub file previews, and vector PDF compilation render **Frame 1** as the static fallback representation of an APNG file.
- **Never leave Frame 1 completely blank.**
- Ensure Frame 1 either shows the initial baseline architecture (e.g., entry node + container frame) or a complete overview frame before stepping through the sequence.

### 1.3. Target Frame Rates & Final Frame Hold Duration
| Animation Type | Recommended `fps` | Frame `duration` Strategy |
| :--- | :--- | :--- |
| **Continuous Motion / Transitions** (moving packets, growing chart bars/lines via `draw_ratio`, color fades, pan/zoom) | `fps=8.0` – `12.0` | Use default frame duration (`0.08s` – `0.14s`) during motion, and hold the final completed state with `duration=2.0` – `3.0`. |
| **Step-by-Step Architectural Walkthrough** (revealing pipeline stages, chart series, or diagram nodes one by one) | `fps=1.0` – `2.0` | Use `0.6s` – `1.0s` per step, and hold the final completed diagram with `duration=2.5` – `3.0` so viewers can read the full diagram before it loops. |

---

## 2. Two Standard Animation Loop Idioms

Drawlib's unified component lifecycle (`add()` -> `draw()`) supports two clean loop patterns depending on the module type:

| Target Module | Recommended Loop Pattern | Why |
| :--- | :--- | :--- |
| **Primitives** (`shapes`, `lines`, `text`, `icons`)<br>**SmartArts** (`ChevronProcess`, `Table`, `GridLayout`, `Cycle`, etc.) | **Pattern A / B**: Compute per-frame coordinates for primitives, or register SmartArt items once via `add()` and mutate `.show` / `.style` before `draw()` | Lightweight builders that automatically preserve full container widths, row heights, and cycle slots even when items have `show=False`. |
| **Charts** (`BarChart`, `LineChart`, `PieChart`, `GanttChart`, etc.)<br>**Diagrams** (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`)<br>**Auto-Layout Graphs** (`ArchitectureGraph`, `LayerGraph`, etc.)<br>**Node Trees** (`TreeNode`, `MindMapNode`) | **Pattern B: Pre-Build & Mutate**<br>Build topology/series once outside the loop, then mutate `.show` / `.style` (and `.draw_ratio` / `.draw_direction` on `Charts`) and call `draw()` inside `with anim.frame():` | Avoids re-declaring series or topologies on every frame; locks automatic chart axes (`min_value`/`max_value`) and graph node coordinates; automatically hides connected diagram/graph edges when `node.show = False`. |

### Three Universal Loop Rules
1. **Hoist Invariant Data Outside the Loop**: Define canvas `setup()`, `Animation()`, color palettes, coordinate arrays, and static data tables once before the `for` loop.
2. **Use `show=False` Instead of Omitting Elements**: In SmartArts, Charts, Diagrams, and Graphs, always register all elements and toggle `show=False` / `True` rather than omitting `add()` calls. Hidden elements still reserve their spatial layout slots and axis scales, preventing visual layout jumps across frames.
3. **Hold the Final Frame**: Always give the final frame an explicit hold duration (`duration=2.0` or `3.0`).

---

## 3. Primitives (`shapes`, `lines`, `text`, `icons`) — Coordinate & Color Interpolation

When animating primitives (`rectangle`, `circle`, `arrow`, `line`, `text`, `phosphor`), compute per-frame coordinates, sizes, or colors and pass them to the drawing functions inside `with anim.frame():`.

### 3.1. Coordinate & Path Interpolation (`get_intermediate_points` / `get_intermediate_paths`)
Drawlib provides pure coordinate and polyline-trajectory interpolation functions in `drawlib.math`:
- `get_intermediate_point(xy1, xy2) -> tuple[float, float]`: Returns the exact 50% midpoint `(mx, my)`.
- `get_intermediate_points(xy1, xy2, num=1, *, include_ends=False) -> list[tuple[float, float]]`: Returns `num` evenly spaced intermediate points between `xy1` and `xy2` (or `num + 2` points including `[xy1, ..., xy2]` when `include_ends=True`).
- `get_intermediate_path_point(xys) -> tuple[float, float]`: Returns the 50% arc-length midpoint along a multi-point polyline `xys`.
- `get_intermediate_path_points(xys, num=1, *, include_ends=False) -> list[tuple[float, float]]`: Returns `num` evenly spaced coordinates along the arc length of `xys` (for moving a packet/marker along an L- or U-shaped trajectory).
- `get_intermediate_paths(xys, num=1, *, include_ends=False) -> list[list[tuple[float, float]]]`: Returns progressive prefix sub-paths `[(x0, y0), ..., (xt, yt)]` along `xys` (with full `xys` appended when `include_ends=True`), ready to pass directly to `lines()`, `lines_curved()`, or `arrow_polyline()`.

Use `get_intermediate_points()` to animate moving packets (`circle(pt, ...)`) or progressively growing block arrows (`arrow(start_xy, pt, ...)`):

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.math import get_intermediate_points
from drawlib.shapes import arrow, rectangle
from drawlib.styles import Styles

setup(width=100, height=40)
anim = Animation(fps=10.0)

start_xy, end_xy = (32, 20), (68, 20)
tips = [*get_intermediate_points(start_xy, end_xy, num=5), end_xy]

for i, tip_xy in enumerate(tips):
    is_last = (i == len(tips) - 1)
    with anim.frame(duration=2.0 if is_last else 0.12):
        rectangle((20, 20), width=20, height=14, style=Styles.Neutral.patch(shape_r=2), text="Source")
        dst_style = Styles.PrimaryFlat if is_last else Styles.Neutral
        dst_text = Styles.WhiteBold if is_last else Styles.Dark
        rectangle((80, 20), width=20, height=14, style=dst_style.patch(shape_r=2), text="Target", text_style=dst_text)
        arrow(start_xy, tip_xy, tail_width=2.5, head_width=6.0, head_length=4.5, style=Styles.PrimaryFlat)

save("growing_arrow.png")
```

### 3.2. Smooth Color Interpolation (`get_intermediate_color` / `get_intermediate_colors`)
Drawlib provides pure functions in `drawlib.styles` (and `drawlib.preset_colors`) to compute intermediate `Color` objects between any two colors (`Color`, RGB/RGBA tuple, or hex string):
- `get_intermediate_color(color1, color2) -> Color`: Returns the exact 50% midpoint color.
- `get_intermediate_colors(color1, color2, num=1, *, include_ends=False) -> list[Color]`: Returns `num` evenly spaced intermediate colors. Pass `include_ends=True` to include `[color1, ..., color2]` (`num + 2` colors total) for direct iteration in an animation loop.

Combine `get_intermediate_points()` and `get_intermediate_colors(..., include_ends=True)` with `Style.patch(shape_fill_color=c)` to create multi-phase motion and highlight transitions:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.math import get_intermediate_points
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors

setup(width=100, height=40)
anim = Animation(fps=10.0)

# Pre-calculate packet waypoints and receiver color fade sequence
packet_pts = get_intermediate_points((25, 20), (75, 20), num=3, include_ends=True)
fade_colors = get_intermediate_colors(Colors.White, Colors.Primary, num=2, include_ends=True)

# Phase 1: Packet travels from Sender to Receiver
for pkt_xy in packet_pts:
    with anim.frame():
        rectangle((20, 20), width=20, height=14, style=Styles.Neutral, text="Sender")
        rectangle((80, 20), width=20, height=14, style=Styles.Neutral, text="Receiver")
        line((30, 20), (70, 20), style=Styles.MutedDashed, arrow_head="->")
        circle(pkt_xy, radius=2.5, style=Styles.PrimaryFlat)

# Phase 2: Receiver smoothly transitions from White to Primary
for i, bg_color in enumerate(fade_colors):
    is_last = (i == len(fade_colors) - 1)
    with anim.frame(duration=2.0 if is_last else 0.12):
        rectangle((20, 20), width=20, height=14, style=Styles.Neutral, text="Sender")
        recv_style = Styles.Neutral.patch(shape_fill_color=bg_color)
        recv_text = Styles.WhiteBold if i >= 2 else Styles.Dark
        rectangle((80, 20), width=20, height=14, style=recv_style, text="Receiver", text_style=recv_text)
        line((30, 20), (70, 20), style=Styles.MutedDashed, arrow_head="->")

save("primitive_packet_fade.png")
```

---

## 4. SmartArts (`drawlib.smartarts`) Animation Patterns

### 4.1. Builder-Based SmartArts (`ChevronProcess`, `Table`, `GridLayout`, `BulletPoints`, `Cycle`)
All SmartArt builders accept `show: bool = True` on `add()` and defer rendering until `draw(xy=(x, y), ..., scale=1.0)` is called.
- **Layout Preservation**: Items with `show=False` still occupy their calculated column/row/cell/angle slot. Revealing items step by step via `show=(i <= step)` never shifts or resizes already-visible items.
- **Active Step Highlighting**: Highlight the newly revealed step (`i == step`) with `Styles.PrimaryFlat` (`Styles.WhiteBold` text) and settle previous steps (`i < step`) into calm `Styles.PrimaryNeutral` (`Styles.DarkBold` text).

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles

setup(width=110, height=35)
anim = Animation(fps=1.5)
stages = ["Plan", "Build", "Test", "Deploy"]

for step in range(len(stages)):
    is_last = (step == len(stages) - 1)
    with anim.frame(duration=2.5 if is_last else 0.8):
        proc = ChevronProcess(
            style=Styles.Neutral,
            text_style=Styles.DarkBold,
            description_style=Styles.Dark,
            flat_left_end=True,
        )
        for i, name in enumerate(stages):
            style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
            t_style = Styles.WhiteBold if i == step else Styles.DarkBold
            proc.add(name, style=style, text_style=t_style, show=(i <= step))
        proc.draw(xy=(5, 10), width=100, height=15)

save("chevron_steps.png")
```

### 4.2. Node-Based Hierarchies (`TreeNode`, `MindMapNode`)
For `TreeNode` and `MindMapNode`, you can instantiate the node hierarchy once outside the loop and mutate `.show` across frames before calling `root.draw(xy=..., scale=1.0)`:
- When `child.show = False`, the child node, its incoming connector branch from the parent, and its entire subtree are hidden while still reserving their vertical/radial layout slots so sibling branches remain stationary.

---

## 5. Statistical & Project Charts (`drawlib.charts`) Animation Patterns

All 7 chart classes (`BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`) return mutable element objects (`Series`, `Slice`, `Task`, `Point`) from their registration methods (`add_series`, `add_slice`, `add_task`, `add`).

### 5.1. Progressive Series Reveal (`s.show`)
Build the chart once outside the loop and toggle `s.show = (i <= step)` across frames. Because Drawlib calculates automatic `min_value` / `max_value`, pie proportions, and Gantt row heights across **all registered elements regardless of `show=False`**, the chart axes and gridlines remain 100% locked across frames.

### 5.2. Partial Spatial Growth (`s.draw_ratio` & `s.draw_direction`)
Every `Series`, `Slice`, and `Task` supports `draw_ratio: float` (`0.0` to `1.0`) and `draw_direction: DrawDirection` (`"bottom_to_top"` or `"left_to_right"`):
- **`BarChart` / `RadarChart`**: Default `"bottom_to_top"` grows bars vertically from the baseline (or expands the radar polygon radially outward).
- **`LineChart` / `AreaChart` / `PieChart` / `GanttChart`**: Default `"left_to_right"` sweeps curves, wedges, or task bars progressively along the axis/angle.

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts.bar import BarChart
from drawlib.styles import Styles

setup(width=105, height=64)
anim = Animation(fps=10.0)

chart = BarChart(
    categories=["v1", "v2", "v3"],
    axis_line_style=Styles.MutedDashed,
    axis_text_style=Styles.Muted.patch(text_size=9.5),
    grid_style=Styles.MutedThin,
    width=80,
    height=44,
    title="Service Throughput (RPS)",
    title_style=Styles.BlackBold.patch(text_size=12.5),
)
chart.configure_y_axis(min_value=0, max_value=100)
s1 = chart.add_series("RPS", [45, 85, 65], style=Styles.PrimaryFlat)

for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
    s1.draw_ratio = r
    with anim.frame(duration=2.0 if r == 1.0 else 0.12):
        chart.draw(xy=(12, 8))

save("bar_growth.png")
```

---

## 6. Diagrams (`drawlib.diagrams`) & Auto-Layout Graphs (`drawlib.graph`)

All 6 diagram engines (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`) and all 5 auto-layout graph solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`) follow **Pattern B (Pre-Build & Mutate)**.

### 6.1. Key Capabilities on Diagram Elements
1. **Visibility & Automatic Connected Edge Hiding (`.show`)**:
   - Every node, container (`NodeGroup`, `ParticipantGroup`, `Lane`), block (`Block` from `loop`/`alt`/`opt`/`par`), note (`Note`), and connection (`Edge`, `Message`, `Transition`, `Relationship`) has a mutable `.show: bool` attribute.
   - Setting `node.show = False` automatically hides any connected edges (`Edge`, `Transition`, `Relationship`).
   - For `Junction` routing points in `FlowDiagram` and `ArchitectureDiagram`, the upstream wire entering the junction is automatically hidden until at least one downstream target from that junction is visible.
2. **Dynamic Style & Label Mutation (`.style`, `.text_style`, `.set_label()`, `.set_style()`)**:
   - Mutate `node.style = Styles.PrimaryFlat` (with `Styles.WhiteBold`) or `edge.style = Styles.PrimaryBold` (or `msg.set_style(...)` / `msg.set_label(...)`) between frames to highlight active request paths and settle visited steps into `Styles.PrimaryNeutral`.
3. **Camera Pan & Zoom (`draw(xy=..., scale=...)`)**:
   - Calling `d.draw(xy=(ox, oy), scale=s)` translates and scales all diagram coordinates, dimensions, and font sizes—enabling smooth slide-in transitions or camera zoom-outs.

### 6.2. Diagram Walkthrough Example (`FlowDiagram`)
Build the topology once outside the loop, then mutate `.show`, `node.style`, and `edge.style` across frames:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=110, height=40)
anim = Animation(fps=1.5)

# 1. Build topology once outside the loop
flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark)
n1 = flow.add(Start("Start"), xy=(20, 20))
n2 = flow.add(Process("Validate", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=(55, 20), show=False)
n3 = flow.add(End("Complete", style=Styles.SecondaryNeutral), xy=(90, 20), show=False)
e1 = n1.connect(n2)
e2 = n2.connect(n3)

# 2. Frame 1: Initial state (only Start node visible; e1 and e2 are auto-hidden)
with anim.frame(duration=0.8):
    flow.draw()

# 3. Frame 2: Reveal n2 (e1 automatically appears and highlights active path)
n2.show = True
e1.style = Styles.PrimaryBold
with anim.frame(duration=0.8):
    flow.draw()

# 4. Frame 3: Settle n2 style, reveal n3, and highlight e2
e1.style = Styles.DarkBold
n2.style = Styles.PrimaryNeutral
n2.text_style = Styles.DarkBold
n3.show = True
e2.style = Styles.PrimaryBold
with anim.frame(duration=2.5):
    flow.draw()

save("flow_walkthrough.png")
```

### 6.3. Auto-Layout Graph Animation (`drawlib.graph`)
For `drawlib.graph` solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`), `g.node(id, label, ...)` returns a mutable `Node` declaration (`node.show`, `node.style`, `node.text_style`).
- Because `g.calc()` solves coordinates across the full topology regardless of `show=False`, mutating `node.show` / `node.style` and calling `g.draw(*, xy=(0, 0), width=None, height=None, margin=10.0, scale=1.0)` inside `with anim.frame():` keeps all node coordinates and cluster boxes fixed.
- To animate a data packet (`circle`) traveling along an auto-routed graph edge, pre-calculate `layout = g.calc(margin=...)` and pass `edge_layout.points` (`list[tuple[float, float]]`) to `get_intermediate_path_points(edge_layout.points, num=..., include_ends=True)`:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

setup(width=110, height=42)
anim = Animation(fps=1.5)

g = LayerGraph(direction="LR")
nodes = [
    g.node("ingest", "Ingest", layer=0),
    g.node("transform", "Transform", layer=1),
    g.node("serve", "Serve", layer=2),
]
g.edge("ingest", "transform")
g.edge("transform", "serve")

for step in range(len(nodes)):
    for i, node in enumerate(nodes):
        node.show = (i <= step)
        node.style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
        node.text_style = Styles.WhiteBold if i == step else Styles.DarkBold

    is_last = (step == len(nodes) - 1)
    with anim.frame(duration=2.5 if is_last else 0.8):
        g.draw(margin=8.0)

save("graph_layer_steps.png")
```

---

## 7. Slide Presentation Playback Controls (`anim-trigger`, `anim-loop`, `anim-pause`)

When embedding animated `.png` (APNG) or `.webp` blocks inside a `slide` presentation project (`drawlib build slide`), use code-fence options to control interactive `<canvas>` playback in `slide.js`:

````markdown
```drawlib file:pipeline.webp anim-trigger:click anim-loop:once anim-pause:2,4
```
````

- **`anim-trigger: auto | click`**: `click` holds on Frame 0 (`READY`) until the presenter clicks the diagram; `auto` starts playback on slide entry.
- **`anim-loop: once | infinite`**: `once` stops on the final frame (`ENDED`, click to replay from Frame 0); `infinite` loops continuously.
- **`anim-pause: <frame_indices>`**: Comma-separated 0-based frame indices (e.g. `anim-pause:2,4`) where playback pauses (`PAUSED`) until the next click.

