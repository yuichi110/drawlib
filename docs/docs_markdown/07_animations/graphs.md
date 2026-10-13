# Animating Auto-Layout Graphs

All 5 declarative auto-layout graph solvers in [`drawlib.graph`](../06_graph/overview.md) (`ArchitectureGraph`, `LayerGraph`, `TreeGraph`, `RadialGraph`, and `GridGraph`) are **pure coordinate & layout calculators** that pair naturally with **Pattern B (Solve Once via `get_layout()` & Mutate / Animate)**:



<figure class="drawlib-image" style="text-align: center;">
  <img src="graphs_images/anim_graphs_hero.png" alt="graphs_1" />
  <figcaption class="drawlib-caption">Auto-Layout Graph Animation: 100% Locked Node Coordinates Solved Once via get_layout() Across Progressive Reveal Frames</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.graph import TreeGraph
from drawlib.icons import phosphor
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=124, height=52)
anim = Animation(fps=2.0)

# 1. Declare full tree topology once & lock 100% of coordinates via get_layout()
g = TreeGraph(
    root="gw",
    direction="LR",
    default_node_width=26.0,
    default_node_height=12.5,
)
g.node("gw")
g.child("gw", "auth")
g.child("gw", "bill")
g.child("auth", "cache")
g.child("bill", "ledger")

layout = g.get_layout(margin=5.0)

node_meta = {
    "gw": ("\nAPI Gateway", Styles.PrimaryNeutral, phosphor.shield_check),
    "auth": ("\nAuth Service", Styles.PrimaryNeutral, phosphor.lock_key),
    "bill": ("\nBilling API", Styles.SecondaryNeutral, phosphor.credit_card),
    "cache": ("\nToken Cache", Styles.Neutral, phosphor.lightning),
    "ledger": ("\nLedger DB", Styles.Neutral, phosphor.database),
}


def draw_step(visible: set[str], focal: str) -> None:
    for e in layout.edges:
        if e.src in visible and e.dst in visible:
            lines(e.points, arrow_head="->", style=Styles.DarkBold)
    for nid in visible:
        label, base_st, icon_fn = node_meta[nid]
        nl = layout[nid]
        is_focal = nid == focal
        box_st = Styles.PrimaryFlat if is_focal else base_st
        txt_st = (Styles.WhiteBold if is_focal else Styles.DarkBold).patch(text_size=10.5)
        ic_st = Styles.White if is_focal else Styles.PrimaryFlat
        rectangle(nl.xy, width=nl.width, height=nl.height, style=box_st, text=label, text_style=txt_st)
        icon_fn((nl.x, nl.y + 2.4), width=4.2, style=ic_st)


# Frame 1: Root node at its final auto-solved position
with anim.frame(duration=0.7):
    draw_step({"gw"}, focal="gw")

# Frame 2: Reveal Tier 1 services (Auth Service highlighted)
with anim.frame(duration=0.7):
    draw_step({"gw", "auth", "bill"}, focal="auth")

# Frame 3: Reveal Leaf data stores (Ledger DB highlighted)
with anim.frame(duration=0.7):
    draw_step({"gw", "auth", "bill", "cache", "ledger"}, focal="ledger")

# Frame 4: Settled full hierarchy with Root Gateway as focal node
with anim.frame(duration=2.5):
    draw_step({"gw", "auth", "bill", "cache", "ledger"}, focal="gw")

save()
```

</details>



1. **Solve Full Topology Once (`layout = g.get_layout()`)**: Register all nodes (`g.node()`), clusters (`g.cluster()` / `g.group()`), and edges (`g.edge()`) **once** before the animation loop and call `layout = g.get_layout(margin=...)`.
2. **Mutate Diagram Items or Animate Along `edge_layout.points`**:
   - **Option 1 (`drawlib.diagrams`)**: Place `ArchitectureDiagram` or `FlowDiagram` nodes/groups at `layout` coordinates (`nl.xy`, `nl.local_xy`, `cl.bottom_left`) once outside the loop, then mutate `.show` and `.style` / `.card_style` inside `with anim.frame():` before calling `d.draw()`.
   - **Option 2 (`drawlib.shapes` & `drawlib.lines`)**: Render visible nodes (`layout[id].xy`) and polylines (`edge_layout.points`), or animate data packets along `edge_layout.points` using `get_intermediate_path_points()`.

*(For coordinate-controlled diagrams in `drawlib.diagrams`, see [Animating Technical Diagrams](./diagrams.md).)*

---

## 1. Deterministic Layout Locking (`layout = g.get_layout()`)

A core challenge when animating auto-layout graphs in traditional tools is **layout jumping**: adding a node on Frame 2 causes the layout engine to recompute all positions and shift Frame 1's nodes unpredictably.

Drawlib eliminates layout jumping by decoupling **coordinate solving (`g.get_layout()`)** from **per-frame rendering**:
- Calling `layout = g.get_layout(width=None, height=None, margin=10.0)` **once** outside the animation loop solves and locks every node center (`layout[id].xy` / `.local_xy`), cluster bounding box (`layout[cid].bottom_left` / `.size`), and orthogonal edge trajectory (`edge_layout.points`) across the entire topology.
- When rendered with `FlowDiagram` or `ArchitectureDiagram`, setting `node.show = False` skips the hidden node and **automatically hides any edges connected to that node**, so edges appear cleanly as soon as both endpoint nodes become visible.

| Layout / Diagram Property | Role in Animation |
| :--- | :--- |
| **`layout = g.get_layout(margin=...)`** | Computes and locks all node, cluster, and edge coordinates once before the animation loop begins. |
| **`node.show` / `group.show` / `edge.show`** | Toggle visibility per frame on `FlowDiagram` or `ArchitectureDiagram` items placed at `layout` coordinates while keeping positions 100% stationary. |
| **`node.style` / `node.card_style` / `node.text_style`** | Highlight the newly revealed or active step with `Styles.PrimaryFlat` (`Styles.WhiteBold` text) and settle previous steps into `Styles.PrimaryNeutral` or `Styles.Neutral`. |
| **`edge_layout.points`** | Complete auto-routed polyline (`[src_port, *waypoints, dst_port]`) ready for `lines(e.points)` or `get_intermediate_path_points(e.points, num=...)` packet animations. |

---

## 2. Step-by-Step Pipeline Reveal (`LayerGraph` + `FlowDiagram`)

After solving horizontal rank coordinates once with `LayerGraph.get_layout()`, place `Process` nodes into a `FlowDiagram` at `xy=layout[nid].xy`. Toggling `fn.show = (i <= step)` and updating `fn.style` inside the frame loop reveals each pipeline rank sequentially while keeping the horizontal layout locked:



```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import FlowDiagram, Process
from drawlib.graph import LayerGraph
from drawlib.styles import Styles

setup(width=124, height=34)
anim = Animation(fps=1.5)

# Step 1: Solve pipeline coordinates once via LayerGraph.get_layout()
g = LayerGraph(
    direction="LR",
    rank_sep=8.0,
    default_node_width=23.0,
    default_node_height=11.5,
)
stages = [
    ("edge", "Edge Router", 0),
    ("auth", "Auth Guard", 1),
    ("core", "Core API", 2),
    ("db", "Primary DB", 3),
]
for nid, _, layer_idx in stages:
    g.node(nid, layer=layer_idx)

g.edge("edge", "auth")
g.edge("auth", "core")
g.edge("core", "db")

layout = g.get_layout(margin=5.0)

# Step 2: Register Process nodes at locked layout[nid].xy coordinates
fd = FlowDiagram(
    node_style=Styles.PrimaryNeutral.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
flow_nodes = []
for nid, label, _ in stages:
    nl = layout[nid]
    flow_nodes.append(fd.add(Process(label, width=nl.width, height=nl.height), xy=nl.xy))

for i in range(len(flow_nodes) - 1):
    fd.connect(flow_nodes[i], flow_nodes[i + 1])

# Step 3: Reveal stages one by one without layout jumping
for step in range(len(flow_nodes)):
    for i, fn in enumerate(flow_nodes):
        fn.show = (i <= step)
        fn.style = Styles.PrimaryFlat if i == step else Styles.PrimaryNeutral
        fn.text_style = (Styles.WhiteBold if i == step else Styles.DarkBold).patch(text_size=10.5)

    is_last = (step == len(flow_nodes) - 1)
    with anim.frame(duration=2.5 if is_last else 0.8):
        fd.draw()

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="graphs_images/anim_diagrams_graph_layers.png" alt="graphs_2" />
  <figcaption class="drawlib-caption">Auto-Layout LayerGraph Step-by-Step Reveal Rendered with FlowDiagram</figcaption>
</figure>



---

## 3. Progressive Cluster & Edge Reveal (`ArchitectureGraph` + `ArchitectureDiagram`)

With `ArchitectureGraph`, calling `layout = g.get_layout()` computes both outer container bounding boxes (`cl.bottom_left`, `cl.width`, `cl.height`) and relative child node coordinates (`nl.local_xy`). Populating an `ArchitectureDiagram` with those locked coordinates lets you progressively reveal cloud zones (`group.show`), service nodes (`node.show`), and active request paths (`edge.style`):



```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=138, height=42)
anim = Animation(fps=1.5)

# Step 1: Solve multi-zone container and node coordinates once
g = ArchitectureGraph(
    direction="LR",
    container_sep=6.0,
    default_node_width=18.0,
    default_node_height=10.5,
)
g.cluster("ext", ["client"], pos="left", padding=3.5)
g.node("client")

g.cluster("app", ["gw", "worker"], pos="center", padding=4.0)
g.node("gw")
g.node("worker")

g.cluster("data", ["db"], pos="right", padding=3.5)
g.node("db")

g.edge("client", "gw")
g.edge("gw", "worker")
g.edge("worker", "db")

layout = g.get_layout()

# Step 2: Populate ArchitectureDiagram at solved layout coordinates
d = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)


def make_group(cid: str, title: str, *, show: bool = True) -> NodeGroup:
    cl = layout.clusters[cid]
    return d.add(
        NodeGroup(title=title, width=cl.width, height=cl.height, style=Styles.MutedDashed, show=show),
        xy=cl.bottom_left,
    )


def make_node(grp: NodeGroup, nid: str, label: str, card_st, txt_st, *, show: bool = True) -> Node:
    nl = layout[nid]
    return grp.add(
        Node(
            label,
            width=nl.width,
            height=nl.height,
            card_style=card_st,
            text_style=txt_st.patch(text_size=10.5),
            show=show,
        ),
        xy=nl.local_xy,
    )


c_ext = make_group("ext", "External", show=True)
n_client = make_node(c_ext, "client", "Client App", Styles.Neutral, Styles.DarkBold, show=True)

c_app = make_group("app", "Compute VPC", show=False)
n_gw = make_node(c_app, "gw", "API Gateway", Styles.PrimaryFlat, Styles.WhiteBold, show=False)
n_worker = make_node(c_app, "worker", "Task Worker", Styles.PrimaryNeutral, Styles.DarkBold, show=False)

c_data = make_group("data", "Data Tier", show=False)
n_db = make_node(c_data, "db", "Primary DB", Styles.SecondaryNeutral, Styles.DarkBold, show=False)

e1 = d.connect(n_client, n_gw, label="HTTPS")
e2 = d.connect(n_gw, n_worker, label="Queue")
e3 = d.connect(n_worker, n_db, label="Write")

# Frame 1: External Client entry point
with anim.frame(duration=0.8):
    d.draw()

# Frame 2: Reveal Compute VPC & API Gateway with active incoming edge
c_app.show = True
n_gw.show = True
e1.style = Styles.PrimaryBold
with anim.frame(duration=0.8):
    d.draw()

# Frame 3: Reveal Task Worker inside Compute VPC
e1.style = Styles.DarkBold
n_gw.card_style = Styles.PrimaryNeutral
n_gw.text_style = Styles.DarkBold.patch(text_size=10.5)
n_worker.show = True
n_worker.card_style = Styles.PrimaryFlat
n_worker.text_style = Styles.WhiteBold.patch(text_size=10.5)
e2.style = Styles.PrimaryBold
with anim.frame(duration=0.8):
    d.draw()

# Frame 4: Reveal Data Tier and complete architecture (hold final frame)
e2.style = Styles.DarkBold
n_worker.card_style = Styles.PrimaryNeutral
n_worker.text_style = Styles.DarkBold.patch(text_size=10.5)
c_data.show = True
n_db.show = True
n_gw.card_style = Styles.PrimaryFlat
n_gw.text_style = Styles.WhiteBold.patch(text_size=10.5)
e3.style = Styles.PrimaryBold
with anim.frame(duration=2.5):
    d.draw()

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="graphs_images/anim_graphs_architecture_reveal.png" alt="graphs_3" />
  <figcaption class="drawlib-caption">ArchitectureGraph + ArchitectureDiagram Progressive Cluster, Node, and Edge Reveal</figcaption>
</figure>



---

## 4. Animating Packets Along Auto-Routed Edges (`g.get_layout()` & `edge_layout.points`)

Every `EdgeLayout` in `layout.edges` exposes `edge_layout.points: list[tuple[float, float]]` (`[src_port, *waypoints, dst_port]`), representing the complete auto-routed polyline trajectory between node borders.

Pass `edge_layout.points` to `get_intermediate_path_points(edge_layout.points, num=..., include_ends=True)` to animate a data packet (`circle`) traveling smoothly along an auto-routed graph edge:



```python
from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.lines import lines
from drawlib.math import get_intermediate_path_points
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=118, height=38)
anim = Animation(fps=10.0)

g = LayerGraph(
    direction="LR",
    default_node_width=24.0,
    default_node_height=12.0,
)
g.node("ingest", layer=0)
g.node("worker", layer=1)
g.node("store", layer=2)
g.edge("ingest", "worker")
g.edge("worker", "store")

# 1. Solve layout once to inspect auto-routed edge polylines
layout = g.get_layout(margin=5.0)
pts_e0 = get_intermediate_path_points(layout.edges[0].points, num=4, include_ends=False)
pts_e1 = get_intermediate_path_points(layout.edges[1].points, num=4, include_ends=False)

edge_labels = {("ingest", "worker"): "Events", ("worker", "store"): "Batch"}
base_nodes = [
    ("ingest", "Ingest API", Styles.PrimaryNeutral),
    ("worker", "Stream Worker", Styles.Neutral),
    ("store", "Data Warehouse", Styles.SecondaryNeutral),
]


def draw_pipeline(active_id: str | None = None) -> None:
    for e in layout.edges:
        lines(e.points, arrow_head="->", style=Styles.DarkBold)
        lbl = edge_labels[(e.src, e.dst)]
        text((e.mid_xy[0], e.mid_xy[1] + 2.4), lbl, style=Styles.Dark.patch(text_size=10.0))
    for nid, label, base_st in base_nodes:
        nl = layout[nid]
        is_active = nid == active_id
        st = Styles.PrimaryFlat if is_active else base_st
        tst = (Styles.WhiteBold if is_active else Styles.DarkBold).patch(text_size=10.5)
        rectangle(nl.xy, width=nl.width, height=nl.height, style=st, text=label, text_style=tst)


# 2. Hop 1: Packet travels along layout.edges[0].points
for pkt_xy in pts_e0:
    with anim.frame(duration=0.12):
        draw_pipeline(active_id="ingest")
        circle(pkt_xy, radius=2.2, style=Styles.PrimaryFlat)

# 3. Hop 2: Highlight worker and move packet along layout.edges[1].points
for pkt_xy in pts_e1:
    with anim.frame(duration=0.12):
        draw_pipeline(active_id="worker")
        circle(pkt_xy, radius=2.2, style=Styles.PrimaryFlat)

# 4. Final settled frame: Data Warehouse active
with anim.frame(duration=2.2):
    draw_pipeline(active_id="store")

save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="graphs_images/anim_graphs_edge_packet.png" alt="graphs_4" />
  <figcaption class="drawlib-caption">Animating a Data Packet Along an Auto-Routed Graph Edge via layout = g.get_layout() and edge_layout.points</figcaption>
</figure>


