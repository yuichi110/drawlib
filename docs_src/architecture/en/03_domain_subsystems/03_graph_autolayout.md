# Declarative Graph Auto-Layout Engine (drawlib.graph)

Visualizing microservices topologies, data pipelines, and cluster networks manually requires calculating dozens of node coordinates and arrow trajectories. However, traditional graph visualization tools (like Graphviz or Cytoscape) rely on heavy external binary runtimes (C/C++ binaries, Java, or Node.js) that complicate CI/CD pipelines and trap layouts inside a rigid rendering black box.

To solve this, Drawlib includes `drawlib.graph`: a **pure-Python coordinate and layout calculator (`get_layout()`)** that solves topological coordinates, nested cluster boundaries, and edge waypoints in-memory without external dependencies, powering a clean **2-Step Workflow** with `drawlib.diagrams` and `drawlib.shapes`.

```drawlib align=center code=fold file=graph_layout_pipeline.png caption="Pure-Python Graph Auto-Layout Pipeline (drawlib.graph)"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=58)

rectangle((70, 29), width=136, height=54, style=Styles.Neutral.patch(shape_r=2.5))
text(
    (70, 50),
    "Pure-Python Graph Auto-Layout Pipeline (drawlib.graph)",
    style=Styles.DarkBold.patch(text_size=12.2),
)

stages = [
    (18.5, "1. Node/Edge Spec", "Declarative DAG\nNodes & Clusters", phosphor.graph, Styles.PrimaryNeutral, Styles.PrimaryBold),
    (52.5, "2. Topology Sort", "Layer assignment\nCompass & tree packing", phosphor.sort_ascending, Styles.SecondaryNeutral, Styles.SecondaryBold),
    (86.5, "3. Coord Solving", "xy, local_xy &\nCluster bottom_left", phosphor.bounding_box, Styles.Neutral, Styles.DarkBold),
    (120.5, "4. get_layout()", "GraphLayout output\nfor diagrams/shapes", phosphor.arrows_split, Styles.PrimaryFlat, Styles.WhiteBold),
]

for x, title, desc, icon_func, card_style, icon_style in stages:
    rectangle((x, 23.5), width=28, height=31, style=card_style.patch(shape_r=1.8))
    icon_func((x - 9.5, 33.5), width=3.4, style=icon_style)
    text((x - 5.5, 33.5), title, style=icon_style.patch(halign="left", text_size=9.5))
    sub_style = Styles.White if card_style == Styles.PrimaryFlat else Styles.Dark
    text((x, 18.5), desc, style=sub_style.patch(text_size=9.5))

for i in range(3):
    x_from = stages[i][0] + 14.0
    x_to = stages[i + 1][0] - 14.0
    line((x_from, 23.5), (x_to, 23.5), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 1. Concept: Pure Coordinate Calculator & 2-Step Workflow

Instead of coupling layout math to a rigid, un-customizable renderer, `drawlib.graph` is strictly a **pure coordinate calculator (`get_layout()` only)**. Developers and AI agents declare topological relationships in Step 1, and render with `drawlib.diagrams` (`ArchitectureDiagram`, `FlowDiagram`, etc.) or `drawlib.shapes` in Step 2:

```python
from drawlib.diagrams.flow import FlowDiagram, Process
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

# Step 1: Solve topology coordinates with LayerGraph.get_layout()
g = LayerGraph(direction="LR", default_node_width=24.0, default_node_height=12.0)
g.node("client")
g.node("gateway")
g.node("service")
g.edge("client", "gateway")
g.edge("gateway", "service")
layout = g.get_layout(width=120, height=40)

# Step 2: Render with FlowDiagram (or inspect via print(layout))
flow = FlowDiagram(node_style=Styles.Neutral, edge_style=Styles.DarkBold, edge_text_style=Styles.Dark)
c = flow.add(Process("Web Browser", width=24, height=12), xy=layout["client"].xy)
gw = flow.add(Process("API Gateway", width=24, height=12, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold), xy=layout["gateway"].xy)
svc = flow.add(Process("Auth Service", width=24, height=12), xy=layout["service"].xy)
flow.connect(c, gw)
flow.connect(gw, svc)
flow.draw()
```

### Key Architectural Advantages:
- **Strict Separation of Layout and Rendering**: `drawlib.graph` contains zero visual styling parameters (`style`, `label`, `shape`, `draw()` do not exist on `drawlib.graph`), eliminating redundant rendering code and letting `drawlib.diagrams` handle icons, cards, and connectors.
- **No External Binaries**: Runs anywhere standard Python runs—including lightweight Docker images and air-gapped CI environments.
- **Seamless Local & Global Coordinates**: `GraphLayout` provides both global canvas coordinates (`.xy`, `.bottom_left`) and cluster-relative coordinates (`.local_xy`, `.local_bottom_left`) that map directly into `ArchitectureDiagram`'s nested `NodeGroup` hierarchy.

---

## 2. Positioning: The 5 Graph Layout Engines

All solvers in `drawlib.graph` inherit from the abstract base class `BaseGraph(ABC)` (`_common/_base.py`). `BaseGraph` defines the standard lifecycle:
1. **Specification Phase**: Registering nodes (`g.node(id, *, width=..., height=...)`), edges (`g.edge(src, dst)`), and nested boundaries (`g.cluster(id, nodes=[...], *, padding=4.0, header_height=3.5)` or `g.group(id, ...)`).
2. **Solve Phase (`get_layout(width=..., height=..., margin=10.0)`)**: Returns a `GraphLayout` container holding `NodeLayout`, `ClusterLayout`, and `EdgeLayout` objects, supporting `layout["id"]` lookup, `print(layout)` tabular inspection, and `layout.offset(id, dx=..., dy=...)` post-solve adjustments.
3. **Render Phase (Externalized to `drawlib.diagrams` / `drawlib.shapes`)**: Solved coordinates are passed to `ArchitectureDiagram`, `FlowDiagram`, or `drawlib.shapes` / `drawlib.lines`.

`drawlib.graph` provides **five specialized layout solvers**:

1. **`LayerGraph` (Ranked DAG Layout)**:
   - Uses an adapted Sugiyama-style layering algorithm:
     - Assigns nodes to horizontal or vertical layers (ranks) based on topological sorting, longest-path analysis, and `.tier()` stage pinning.
     - Orders nodes within each layer via barycenter crossing minimization.
     - Solves coordinate positions and computes orthogonal or straight edge waypoints.
2. **`ArchitectureGraph` (2-Level Macro/Micro Compound Topology)**:
   - Specialized layout solver designed for cloud architectures and distributed microservices.
   - Solves layouts across two coupled geometric tiers:
     - **Macro Level**: Arranges top-level containers (VPCs, cloud regions, client tiers, observability zones) across a 5-zone compass (`pos="left"|"center"|"right"|"top"|"bottom"`) or along the macro flow direction (`LR` or `TB`).
     - **Micro Level**: Packs internal services and nested subnets (`parent=...`) within their enclosing container boundaries and computes `.local_xy` and `.local_bottom_left`.
3. **`TreeGraph` (Hierarchical Directory / Org Layout)**:
   - Optimized for single-parent trees, directory trees, and organizational hierarchies (`.child(parent, child_id)`).
   - Computes subtree widths recursively via Reingold-Tilford contours to prevent node overlaps.
4. **`RadialGraph` (Central Hub & Spoke Layout)**:
   - Distributes peripheral nodes (`.spoke(parent, spoke_id, ring=...)`) in concentric angular orbits around a central hub and exposes ring radii in `layout.ring_radii`.
5. **`GridGraph` (Matrix / Cluster Topology)**:
   - Aligns nodes on a 2D coordinate grid (`.cell()`, `.cluster_row()`, `.cluster_column()`) with smart channel edge routing.

---

## 3. Details: ArchitectureGraph & 2-Level Compound Layout

### 3.1. The Macro/Micro Compound Layout Problem
Traditional graph algorithms (like standard Sugiyama layering or force-directed placement) treat all nodes and clusters homogeneously. In cloud architecture diagrams, this creates severe layout failure modes:
- Subnets inside a VPC become stretched across distant columns to align with unrelated external nodes.
- High-level containers collapse or overlap because the solver lacks hierarchical rank separation.

### 3.2. Two-Stage Decomposition in `ArchitectureGraph`
`ArchitectureGraph` (`_architecture/_solver.py`) resolves this via **two-stage geometric decomposition**:
1. **Container Abstraction**: Top-level containers (e.g. `Client Zone`, `VPC`, `External SaaS`) are treated as macro nodes in an overarching container dependency DAG.
2. **Micro Layout & Dimension Solving**: Inside each container, child nodes are resolved locally. The container's intrinsic bounding box is calculated using bottom-up envelope expansion:
   $$\text{width}_{\text{container}} = \max(x_1) - \min(x_0) + 2 \times \text{padding}$$
3. **Macro Positioning & Flow**: Containers are positioned sequentially along the macro axis (`direction="LR"` or `"TB"`), respecting inter-container dependencies and user-configured `container_sep`.
4. **Global Edge Routing**: Edges crossing container boundaries calculate entry and exit boundary anchor points, routing cleanly through inter-container channels.

---

## 4. Details: Nested Cluster Boundary Computation

A standout architectural capability of `drawlib.graph` is **automatic recursive cluster boundary expansion**:

```drawlib align=center code=fold file=graph_cluster_boundaries.png caption="Hierarchical Nested Cluster Bounding Box Calculation"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=62)

rectangle((70, 31), width=136, height=58, style=Styles.Neutral.patch(shape_r=2.5))
text(
    (70, 54),
    "Hierarchical Nested Cluster Bounding Box Calculation",
    style=Styles.DarkBold.patch(text_size=12.2),
)

# Outer Cluster (VPC)
rectangle((70, 27), width=126, height=42, style=Styles.MutedDashed.patch(shape_r=2.0))
phosphor.cloud((15, 43.5), width=3.8, style=Styles.PrimaryBold)
text((20, 43.5), "Outer Cluster (e.g. VPC Network)", style=Styles.PrimaryBold.patch(halign="left", text_size=9.5))

# Inner Cluster 1 (Public Subnet)
rectangle((40, 24), width=58, height=27, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
text((16, 33), "Subnet A (Public)", style=Styles.DarkBold.patch(halign="left", text_size=8.8))

rectangle((28, 20), width=20, height=12, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.globe((21, 22.5), width=3.0, style=Styles.PrimaryBold)
text((30, 22.5), "Web App", style=Styles.DarkBold.patch(text_size=8.2))

rectangle((52, 20), width=20, height=12, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.shield_check((45, 22.5), width=3.0, style=Styles.PrimaryBold)
text((54, 22.5), "API Gateway", style=Styles.DarkBold.patch(text_size=8.2))

# Inner Cluster 2 (Private Subnet)
rectangle((100, 24), width=58, height=27, style=Styles.SecondaryNeutral.patch(shape_r=1.5))
text((76, 33), "Subnet B (Private Data)", style=Styles.DarkBold.patch(halign="left", text_size=8.8))

rectangle((88, 20), width=20, height=12, style=Styles.Neutral.patch(shape_r=1.2))
phosphor.database((81, 22.5), width=3.0, style=Styles.SecondaryBold)
text((90, 22.5), "Postgres", style=Styles.DarkBold.patch(text_size=8.2))

rectangle((112, 20), width=20, height=12, style=Styles.PrimaryFlat.patch(shape_r=1.2))
phosphor.hard_drives((105, 22.5), width=3.0, style=Styles.WhiteBold)
text((114, 22.5), "Redis Cache", style=Styles.WhiteBold.patch(text_size=8.2))

# Connecting line between clusters
line((62, 20), (78, 20), arrow_head="->", style=Styles.DarkBold)

save()
```

### Bottom-Up Geometric Solving
When clusters contain child nodes or sub-clusters:
1. **Leaf Node Positioning**: Leaf nodes are positioned first within their local rank coordinate space.
2. **Cluster Bounding Box Calculation**: The enclosing cluster iterates over all member bounding boxes to compute the minimum enclosing envelope:
   $$x_0 = \min_{i}(x_{0,i}) - \text{padding}$$
   $$y_0 = \min_{i}(y_{0,i}) - \text{padding}$$
   $$\text{width} = \max_{i}(x_{1,i}) - x_0 + \text{padding}$$
   $$\text{height} = \max_{i}(y_{1,i}) - y_0 + \text{padding}$$
3. **Parent Propagation**: Parent clusters recursively absorb child cluster envelopes, rendering grouped cloud topologies with balanced padding and zero boundary collisions.

Next, proceed to Chapter 4: **[Compilation Pipeline](../04_doc_builder_and_compiler/01_compilation_pipeline.md)**.

