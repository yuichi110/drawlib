# Drawlib Animation Design & Best Practices Guide

This guide defines the architectural principles, loop idioms, and component-specific patterns for creating multi-frame animations (`APNG` and `Animated WebP`) across all Drawlib modules.

*(For the core `Animation` class API, `with anim.frame()`, and file saving options, run `uv run drawlib rules show lib-anim`.)*

---

## 1. Core Animation Design Principles

### 1.1. Prefer Per-Frame Redraw (`clear=True`) Over Cumulative (`clear=False`)
When `with anim.frame():` executes with its default `clear=True`, Drawlib clears the canvas at the start of the frame and draws the complete scene for that instant.
- **Why `clear=True` is strongly recommended**:
  - Allows elements to move (`xy`), scale, or change style (`Styles.PrimaryFlat` -> `Styles.PrimaryNeutral`) without leaving behind stale drawings from previous frames.
  - Works seamlessly with all high-level components (`SmartArts`, `Charts`, `Diagrams`, `Graph`) via their `.show`, `.style`, and `.draw_ratio` controls.
- **When to use `clear=False`**:
  - Only when strictly appending static primitive shapes onto the canvas without ever moving, un-highlighting, or modifying previously drawn elements.

### 1.2. Poster Frame Principle (Static & PDF Compatibility)
Standard image viewers, GitHub file previews, and vector PDF compilation render **Frame 1** as the static fallback representation of an APNG file.
- **Never leave Frame 1 completely blank.**
- Ensure Frame 1 either shows the initial baseline architecture (e.g., entry node + container frame) or a complete overview frame before stepping through the sequence.

### 1.3. Target Frame Rates & Final Frame Hold Duration
| Animation Type | Recommended `fps` | Frame `duration` Strategy |
| :--- | :--- | :--- |
| **Continuous Motion / Transitions** (moving packets, growing bars, growing arrows, color fades, pan/zoom) | `fps=8.0` – `12.0` | Use default frame duration (`0.08s` – `0.12s`) during motion, and hold the final completed state with `duration=2.0` – `3.0`. |
| **Step-by-Step Architectural Walkthrough** (revealing pipeline stages, chart series, or diagram nodes one by one) | `fps=1.0` – `2.0` | Use `0.6s` – `1.0s` per step, and hold the final completed diagram with `duration=2.5` – `3.0` so viewers can read the full diagram before it loops. |

---

## 2. Two Standard Animation Loop Idioms

Drawlib's unified component lifecycle (`add()` -> `draw()`) supports two clean loop patterns depending on the module type:

| Target Module | Recommended Loop Pattern | Why |
| :--- | :--- | :--- |
| **Primitives** (`shapes`, `lines`, `text`, `icons`)<br>**SmartArts** (`ChevronProcess`, `Table`, `GridLayout`, etc.)<br>**Charts** (`BarChart`, `LineChart`, `PieChart`, etc.) | **Pattern A: In-Frame Build**<br>Instantiate and call `add(..., show=...)` -> `draw()` inside `with anim.frame():` | Lightweight builders that automatically preserve full container widths and chart axis scales even when items have `show=False`. |
| **Diagrams** (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`)<br>**Auto-Layout Graphs** (`ArchitectureGraph`, `LayerGraph`, etc.)<br>**Node Trees** (`TreeNode`, `MindMapNode`) | **Pattern B: Pre-Build & Mutate**<br>Build topology once outside the loop, then mutate `.show` / `.style` / `.draw_ratio` and call `draw()` inside `with anim.frame():` | Avoids re-declaring complex graph topologies or re-running layout solvers on every frame; automatically hides connected edges when `node.show = False`. |

### Three Universal Loop Rules
1. **Hoist Invariant Data Outside the Loop**: Define canvas `setup()`, `Animation()`, color palettes, coordinate arrays, and static data tables once before the `for` loop.
2. **Use `show=False` Instead of Omitting Elements**: In SmartArts, Charts, Diagrams, and Graphs, always register all elements and toggle `show=False` / `True` rather than omitting `add()` calls. Hidden elements still reserve their spatial layout slots and axis scales, preventing visual layout jumps across frames.
3. **Hold the Final Frame**: Always give the final frame an explicit hold duration (`duration=2.0` or `3.0`).

---

## 3. Primitives (`shapes`, `lines`, `text`, `icons`) & Smooth Color Transitions

When animating primitives (`rectangle`, `circle`, `line`, `text`, `phosphor`), compute per-frame coordinates, sizes, or colors and pass them to the drawing functions inside `with anim.frame():`.

### Smooth Color Interpolation (`get_intermediate_color` / `get_intermediate_colors`)
Drawlib provides pure functions in `drawlib.styles` (and `drawlib.preset_colors`) to compute intermediate `Color` objects between any two colors (`Color`, RGB/RGBA tuple, or hex string):
- `get_intermediate_color(color1, color2) -> Color`: Returns the exact 50% midpoint color.
- `get_intermediate_colors(color1, color2, num=1, *, include_ends=False) -> list[Color]`: Returns `num` evenly spaced intermediate colors. Pass `include_ends=True` to include `[color1, ..., color2]` (`num + 2` colors total) for direct iteration in an animation loop.

Combine `get_intermediate_colors(..., include_ends=True)` with `Style.patch(shape_fill_color=c)` to create smooth highlight or fade transitions:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.styles import Colors, Styles, get_intermediate_colors

setup(width=100, height=40)
anim = Animation(fps=10.0)

# Pre-calculate packet X coordinates and receiver color fade sequence
packet_xs = [25, 38, 52, 65, 75]
fade_colors = get_intermediate_colors(Colors.White, Colors.Primary, num=2, include_ends=True)

# Phase 1: Packet travels from Sender to Receiver
for pkt_x in packet_xs:
    with anim.frame():
        rectangle((20, 20), width=20, height=14, style=Styles.Neutral, text="Sender")
        rectangle((80, 20), width=20, height=14, style=Styles.Neutral, text="Receiver")
        line((30, 20), (70, 20), style=Styles.MutedDashed, arrow_head="->")
        circle((pkt_x, 20), radius=2.5, style=Styles.PrimaryFlat)

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

### 4.1. Builder-Based SmartArts (`ChevronProcess`, `Table`, `GridLayout`, `BulletList`, `CycleDiagram`)
All SmartArt builders accept `show: bool = True` on `add()` (or `add_row()` on `Table`) and defer rendering until `draw(xy=(x, y), ...)` is called.
- **Layout Preservation**: Items with `show=False` still occupy their calculated column/cell/angle slot. Revealing items step by step via `show=(i <= step)` never shifts or resizes already-visible items.
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
        proc = ChevronProcess(style=Styles.Neutral, text_style=Styles.DarkBold, flat_left_end=True)
        for i, name in enumerate(stages):
            style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
            t_style = Styles.WhiteBold if i == step else Styles.DarkBold
            proc.add(name, style=style, text_style=t_style, show=(i <= step))
        proc.draw(xy=(5, 10), width=100, height=15)

save("chevron_steps.png")
```

### 4.2. Node-Based Hierarchies (`TreeNode`, `MindMapNode`)
For `TreeNode` and `MindMapNode`, `add()` returns the child node instance. You can build the hierarchy once outside the loop and mutate `.show`, `.style`, and `.text_style` across frames before calling `root.draw(xy=...)`:
- When `child.show = False`, the child node, its connector branch from the parent, and its entire subtree are hidden while still reserving their layout space so sibling branches remain stationary.

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.smartarts import TreeNode
from drawlib.styles import Styles

setup(width=100, height=60)
anim = Animation(fps=1.5)

root = TreeNode("API Gateway", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold)
auth = root.add("Auth Service", style=Styles.PrimaryNeutral, show=False)
orders = root.add("Order Service", style=Styles.PrimaryNeutral, show=False)

for step in range(3):
    auth.show = (step >= 1)
    orders.show = (step >= 2)
    with anim.frame(duration=2.5 if step == 2 else 0.8):
        root.draw(xy=(50, 48))

save("tree_reveal.png")
```

---

## 5. Statistical & Project Charts (`drawlib.charts`) Animation Patterns

All 7 chart classes (`BarChart`, `LineChart`, `AreaChart`, `PieChart`, `RadarChart`, `ScatterChart`, `GanttChart`) separate data registration (`add()`) from rendering (`draw(xy, width, height)`).

### 5.1. Progressive Series / Task Reveal (`add(..., show=...)`)
Register all series, slices, or Gantt tasks in every frame and control visibility with `show=(i <= step)`:
- **Stable Axis Scaling**: Hidden series (`show=False`) are still included when Drawlib calculates automatic `max_value`, `xlim`/`ylim`, Radar polygon radius, or Gantt date ranges, ensuring the chart axes and gridlines never jump when a new series appears.

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts import LineChart
from drawlib.styles import Styles

setup(width=100, height=65)
anim = Animation(fps=1.2)

categories = ["Q1", "Q2", "Q3", "Q4"]
series_data = [
    ("2024 Baseline", [40, 48, 52, 60], Styles.Secondary),
    ("2025 Actual", [50, 68, 82, 95], Styles.Primary),
]

for step in range(len(series_data)):
    is_last = (step == len(series_data) - 1)
    with anim.frame(duration=2.5 if is_last else 1.0):
        chart = LineChart(title="Quarterly Revenue ($M)", categories=categories)
        for i, (label, values, style) in enumerate(series_data):
            chart.add(label, values, style=style, show=(i <= step))
        chart.draw(xy=(12, 10), width=78, height=45)

save("line_series_reveal.png")
```

### 5.2. Value Growth Animation (Pinning `max_value` / `ylim`)
When animating bar heights, line values, or radar polygons growing from `0%` to `100%` via `[v * r for v in targets]`, **always set an explicit `max_value=...` (or `ylim=...`) on the chart constructor**. Otherwise, automatic axis scaling will rescale the Y-axis to the scaled values on every frame:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.charts import BarChart
from drawlib.styles import Styles

setup(width=100, height=65)
anim = Animation(fps=10.0)
targets = [45, 85, 65]

for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
    with anim.frame(duration=2.0 if r == 1.0 else 0.12):
        chart = BarChart(title="Service Throughput (RPS)", categories=["v1", "v2", "v3"], max_value=100)
        chart.add("RPS", [round(v * r, 1) for v in targets], style=Styles.PrimaryFlat)
        chart.draw(xy=(12, 10), width=78, height=45)

save("bar_growth.png")
```

---

## 6. Diagrams (`drawlib.diagrams`) & Auto-Layout Graphs (`drawlib.graph`)

All 6 diagram engines (`FlowDiagram`, `ArchitectureDiagram`, `SequenceDiagram`, `StateDiagram`, `ClassDiagram`, `ERDiagram`) and all 5 auto-layout graph solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`) follow **Pattern B (Pre-Build & Mutate)**.

### 6.1. Key Capabilities on Diagram Elements
1. **Visibility & Automatic Connected Edge Hiding (`.show`)**:
   - Every node, container, note, and connection has a mutable `.show: bool` attribute.
   - Setting `node.show = False` automatically hides any connected edges (`Edge`, `Transition`, `Relationship`).
   - For `Junction` routing points in `FlowDiagram` and `ArchitectureDiagram`, the upstream wire entering the junction is automatically hidden until at least one downstream target from that junction is visible.
2. **Dynamic Style Mutation (`.style`, `.text_style`)**:
   - Mutate `node.style = Styles.PrimaryFlat` or `edge.style = Styles.PrimaryBold` between frames to highlight active request paths.
3. **Progressive Arrow & Line Drawing (`edge.draw_ratio`, `edge.draw_direction`)**:
   - All connection objects (`Edge`, `Transition`, `Relationship`, `Message`, `Junction`) support `draw_ratio: float` (`0.0` to `1.0`) and `draw_direction: Literal["forward", "backward"]`.
   - Animating `edge.draw_ratio` across `[0.3, 0.6, 1.0]` smoothly grows the connector line and traveling arrowhead from source to target.
4. **Camera Pan & Zoom (`draw(xy=..., scale=...)`)**:
   - Calling `d.draw(xy=(ox, oy), scale=s)` translates and scales all diagram coordinates, dimensions, and font sizes—enabling smooth slide-in transitions or camera zoom-outs.

### 6.2. Diagram Walkthrough Example (`FlowDiagram`)
Build the topology once outside the loop, then mutate `.show`, `.draw_ratio`, and `.style` across frames:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=110, height=40)
anim = Animation(fps=8.0)

# 1. Build topology once outside the loop
flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark)
n1 = flow.add(Start("Start"), xy=(20, 20))
n2 = flow.add(Process("Validate", style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=(55, 20), show=False)
n3 = flow.add(End("Complete", style=Styles.SecondaryNeutral), xy=(90, 20), show=False)
e1 = n1.connect(n2)
e2 = n2.connect(n3)

# 2. Frame 1: Initial state (only Start node visible)
with anim.frame(duration=0.6):
    flow.draw()

# 3. Reveal n2 and progressively draw edge e1
n2.show = True
for r in [0.4, 0.8, 1.0]:
    with anim.frame(duration=0.15):
        e1.draw_ratio = r
        flow.draw()

# 4. Settle n2 style, reveal n3, and progressively draw edge e2
n2.style = Styles.PrimaryNeutral
n2.text_style = Styles.DarkBold
n3.show = True
for r in [0.4, 0.8, 1.0]:
    with anim.frame(duration=2.5 if r == 1.0 else 0.15):
        e2.draw_ratio = r
        flow.draw()

save("flow_walkthrough.png")
```

### 6.3. Auto-Layout Graph Animation (`drawlib.graph`)
For `drawlib.graph` solvers (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, `GridGraph`), run `layout = g.calc()` **once** before the animation loop to solve the layout, then mutate `layout.nodes[id]`, `layout.edges`, or `layout.clusters[id]` and call `layout.draw(xy=..., scale=...)` inside `with anim.frame():`:

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

setup(width=100, height=45)
anim = Animation(fps=1.5)

g = LayerGraph(direction="LR")
g.node("ingest", "Ingest", layer=0, style=Styles.PrimaryNeutral)
g.node("transform", "Transform", layer=1, style=Styles.PrimaryNeutral)
g.node("serve", "Serve", layer=2, style=Styles.PrimaryNeutral)
g.edge("ingest", "transform")
g.edge("transform", "serve")

# Compute layout once before the loop
layout = g.calc(xy=(10, 10), width=80, height=25)
order = ["ingest", "transform", "serve"]

for step, active_id in enumerate(order):
    for i, nid in enumerate(order):
        node = layout.nodes[nid]
        node.show = (i <= step)
        node.style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
        node.text_style = Styles.WhiteBold if i == step else Styles.DarkBold

    is_last = (step == len(order) - 1)
    with anim.frame(duration=2.5 if is_last else 0.8):
        layout.draw()

save("graph_layer_steps.png")
```
