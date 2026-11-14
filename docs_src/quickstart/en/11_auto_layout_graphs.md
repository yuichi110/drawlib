# 11. Automatic Graph Layout Solvers

When diagrams grow beyond a handful of hand-placed nodes, manually maintaining `(x, y)` coordinates becomes tedious—yet opaque black-box graph renderers strip away control over iconography, typography, and design tokens. `drawlib.graph` bridges both worlds as a **pure deterministic coordinate calculator**: declare nodes, clusters, and edges topologically, call `layout = g.get_layout(...)`, and render the solved geometry using any Drawlib visual component.

```drawlib align=center code=fold file=layer_graph_dag.png caption="Figure 11.1: Data Lineage & Feature Pipeline DAG Solved with LayerGraph.get_layout() and Rendered onto Styled Cards"
from drawlib.canvas import save, setup
from drawlib.graph import LayerGraph
from drawlib.icons import phosphor
from drawlib.lines import lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=78)

# Step 1: Declare DAG topology & compute deterministic coordinates
g = LayerGraph(direction="LR", default_node_width=34.0, default_node_height=14.5)
g.node("ingest", layer=0)
g.tier("processing", ["transform", "validate"], layer=1)
g.cluster("etl_stage", ["transform", "validate"], padding=5.0, header_height=4.5)
g.tier("serving", ["feature", "warehouse"], layer=2)

g.edge("ingest", "transform")
g.edge("ingest", "validate")
g.edge("transform", "feature")
g.edge("transform", "warehouse")
g.edge("validate", "warehouse")

layout = g.get_layout(margin=13.0)

# Step 2: Render cluster boundary, orthogonal routed edges, and styled cards
stage = layout["etl_stage"]
rectangle(stage.xy, width=stage.width, height=stage.height, style=Styles.MutedDashed.patch(shape_r=2.2))
text(
    (stage.left + 2.5, stage.top - 2.8),
    "Processing Stage",
    style=Styles.DarkBold.patch(halign="left", text_size=10.2),
)

for edge in layout.edges:
    lines(edge.points, arrow_head="->", style=Styles.DarkBold)

cards = [
    ("ingest", "Event Ingest", "Kafka / PubSub", Styles.Neutral, Styles.DarkBold, Styles.Dark, phosphor.cloud_arrow_up),
    ("transform", "Stream Engine", "Stateful Flink", Styles.PrimaryFlat, Styles.WhiteBold, Styles.White, phosphor.lightning),
    ("validate", "Schema Gate", "Contract Check", Styles.PrimaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.shield_check),
    ("feature", "Feature Store", "Low-Latency KV", Styles.SecondaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.cpu),
    ("warehouse", "Analytics DWH", "Columnar SQL", Styles.Neutral, Styles.DarkBold, Styles.Dark, phosphor.database),
]

for nid, title, sub, card_st, title_st, sub_st, icon_fn in cards:
    n = layout[nid]
    rectangle(n.xy, width=n.width, height=n.height, style=card_st.patch(shape_r=1.8))
    icon_fn((n.x - 11.5, n.y), width=4.8, style=title_st)
    text((n.x + 2.2, n.y + 2.4), title, style=title_st.patch(text_size=10.6))
    text((n.x + 2.2, n.y - 2.8), sub, style=sub_st.patch(text_size=10.0))

save()
```

---

## 11.1 The Two-Step Layout Architecture (get_layout)

Unlike black-box layout engines, `drawlib.graph` has **no `.draw()` method** and stores zero visual styles. Instead, every graph follows a clean two-step separation between **geometry calculation** and **visual rendering**:

1. **Declare Topology & Solve (`layout = g.get_layout(...)`)**: Register nodes (`g.node("id", width=..., height=...)`), directed edges (`g.edge("src", "dst")`), and optional grouping containers (`g.cluster("id", nodes=[...], padding=..., header_height=...)`). Calling `g.get_layout(width=..., height=..., margin=10.0)` returns an immutable-style `GraphLayout` dictionary (`layout["id"]`).
2. **Render with Full Visual Control**: Map the solved coordinates onto `ArchitectureDiagram`, `FlowDiagram`, `SmartArts`, or primitive `shapes`, `icons`, and `lines`:
   - **Center Coordinates (`.xy` and `.local_xy`)**: Every `NodeLayout` and `ClusterLayout` exposes `.xy` (`(cx, cy)` global center) for `rectangle()`, `circle()`, `FlowDiagram` nodes, and standalone `ArchitectureDiagram` nodes, plus `.local_xy` (center relative to its parent cluster's bottom-left corner) for nodes nested inside an `ArchitectureDiagram` `NodeGroup`.
   - **Bottom-Left Corners (`.bottom_left` and `.local_bottom_left`)**: Ready to pass directly to bottom-left anchored components such as top-level `NodeGroup(..., xy=cl.bottom_left)`, nested `parent_grp.add(NodeGroup(...), xy=cl.local_bottom_left)`, `SmartArts`, and `Charts`.
   - **Routed Edge Polylines (`edge.points`, `edge.src_port`, `edge.dst_port`, `edge.mid_xy`)**: Each `EdgeLayout` in `layout.edges` provides boundary-clipped port coordinates and intermediate Manhattan waypoints ready for `lines(edge.points, arrow_head="->")`.
   - **Inspecting & Freezing Coordinates (`print(layout)` & `layout.offset()`)**: When transitioning from an automatic layout to fine-tuned manual code, call `print(layout)` (`str(layout)`) to dump a human-readable coordinate table of every solved cluster, node `.xy` / `.bottom_left`, and edge path for copy-pasting into explicit Python code, or chain `layout.offset("node_id", dx=0.0, dy=-5.0)` to nudge individual nodes while automatically recalculating attached edge ports.

---

## 11.2 Choosing Among the Five Graph Solvers

`drawlib.graph` provides five specialized layout engines inheriting from `BaseGraph`, each tailored to a distinct structural topology:

| Solver Class | Core Layout Algorithm | Topology Helpers | Ideal Architectural Use Cases |
| :--- | :--- | :--- | :--- |
| **`ArchitectureGraph`** | 2-level macro/micro container packing + 5-zone compass placement | `g.group()`, `g.cluster(..., parent=..., pos="left"\|"center"\|..., order=...)` | Multi-zone cloud VPCs, nested subnets, microservice ecosystems (`ArchitectureDiagram`) |
| **`LayerGraph`** | Sugiyama hierarchical DAG (cycle breaking, longest-path ranks, barycenter crossing minimization) | `g.tier(name, nodes, layer=...)`, `g.cluster()`, `direction="LR"\|"TB"` | ETL/data lineage pipelines, CI/CD stages, build & package dependency DAGs |
| **`TreeGraph`** | Reingold-Tilford / Buchheim compact symmetrical subtree layout | `g.child(parent, child_id)`, `root=...`, `direction="TB"\|"LR"` | Engineering org charts, ASTs, fault trees, strict single-parent taxonomies |
| **`RadialGraph`** | Concentric BFS rings + subtree-weighted angular sector allocation | `g.spoke(parent, spoke_id, ring=...)`, `hub=...`, `layout.ring_radii` | Event meshes, Pub/Sub hub-and-spoke topologies, API platform ecosystems |
| **`GridGraph`** | 2D `(row, col)` matrix slot placement + corridor channel routing | `g.cell(id, row=..., col=...)`, `g.cluster_row()`, `g.cluster_column()`, `edge_routing="smart"` | Tiered service catalogs, state matrices, uniform multi-column architectures |

---

## 11.3 Hierarchical Trees & Concentric Hub-and-Spoke Topologies

For strict hierarchies and central message brokers, `TreeGraph` and `RadialGraph` eliminate manual trigonometry and subtree width balancing:

- **`TreeGraph`**: Enforces acyclic single-parent tree invariants (raising a helpful `ValueError` if a diamond DAG is accidentally passed), centers every parent cleanly over its children, and routes orthogonal step connectors (`edge_routing="orthogonal"`) or straight branches (`"straight"`).
- **`RadialGraph`**: Places `hub` at `ring=0`, distributes connected spokes across concentric rings (`ring=1, 2, ...`), and populates `layout.ring_radii: dict[int, float]` so dashed orbital guide circles (`circle(hub.xy, radius=r, style=Styles.MutedDashed)`) align perfectly behind the spoke cards.

```drawlib align=center code=fold file=tree_or_radial_graph.png caption="Figure 11.2: Automatic Non-Linear Layouts — Balanced Rooted TreeGraph (Left) and Concentric RadialGraph Event Mesh (Right)"
from drawlib.canvas import save, setup
from drawlib.graph import RadialGraph, TreeGraph
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=160, height=78)

# Left Panel: TreeGraph (Rooted Taxonomy)
rectangle((41, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.tree_structure((9.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (13.5, 68.0),
    "TreeGraph: Service Taxonomy",
    style=Styles.DarkBold.patch(text_size=11.2, halign="left"),
)

tg = TreeGraph(root="root", direction="TB", sibling_sep=3.2, default_node_width=16.5, default_node_height=9.0)
tg.node("root", width=22.5, height=9.5)
tg.child("root", "compute", width=19.5, height=9.0)
tg.child("root", "data", width=19.5, height=9.0)
tg.child("compute", "k8s", width=16.5, height=9.0)
tg.child("compute", "jobs", width=16.5, height=9.0)
tg.child("data", "sql", width=16.5, height=9.0)

t_layout = tg.get_layout(width=60.0, height=52.0, margin=4.0)
ox1, oy1 = 11.0, 7.0

for e in t_layout.edges:
    pts = [(px + ox1, py + oy1) for px, py in e.points]
    lines(pts, arrow_head="->", style=Styles.DarkBold)

tree_nodes = [
    ("root", "Cloud Platform", Styles.PrimaryFlat, Styles.WhiteBold),
    ("compute", "Compute Tier", Styles.PrimaryNeutral, Styles.DarkBold),
    ("data", "Storage Tier", Styles.SecondaryNeutral, Styles.DarkBold),
    ("k8s", "GKE Pods", Styles.Neutral, Styles.DarkBold),
    ("jobs", "Batch Jobs", Styles.Neutral, Styles.DarkBold),
    ("sql", "Cloud SQL", Styles.Neutral, Styles.DarkBold),
]
for nid, label, st, txt_st in tree_nodes:
    n = t_layout[nid]
    rectangle(
        (n.x + ox1, n.y + oy1),
        width=n.width,
        height=n.height,
        style=st.patch(shape_r=1.6),
        text=label,
        text_style=txt_st.patch(text_size=10.0),
    )

# Right Panel: RadialGraph (Hub-and-Spoke Mesh)
rectangle((119, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.share_network((87.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (91.5, 68.0),
    "RadialGraph: Hub & Spoke Mesh",
    style=Styles.DarkBold.patch(text_size=11.2, halign="left"),
)

rg = RadialGraph(
    hub="hub",
    center=(35.0, 26.5),
    radius_step=22.0,
    start_angle=18.0,
    default_node_width=17.5,
    default_node_height=8.5,
)
rg.node("hub", width=15.0, height=15.0)
for sid in ["auth", "orders", "billing", "notify", "search"]:
    rg.spoke("hub", sid)

r_layout = rg.get_layout(width=70.0, height=54.0, margin=4.0)
ox2, oy2 = 84.0, 7.0
hub_n = r_layout["hub"]
hub_xy = (hub_n.x + ox2, hub_n.y + oy2)

for r in r_layout.ring_radii.values():
    circle(hub_xy, radius=r, style=Styles.MutedDashed)

for e in r_layout.edges:
    sp = (e.src_port[0] + ox2, e.src_port[1] + oy2)
    dp = (e.dst_port[0] + ox2, e.dst_port[1] + oy2)
    line(sp, dp, arrow_head="->", style=Styles.DarkBold)

circle(
    hub_xy,
    radius=hub_n.width / 2,
    style=Styles.PrimaryFlat,
    text="Event\nMesh",
    text_style=Styles.WhiteBold.patch(text_size=10.0),
)

spokes = [
    ("auth", "Auth API", Styles.PrimaryNeutral),
    ("orders", "Orders", Styles.Neutral),
    ("billing", "Billing", Styles.SecondaryNeutral),
    ("notify", "Notify", Styles.Neutral),
    ("search", "Search", Styles.PrimaryNeutral),
]
for sid, label, st in spokes:
    n = r_layout[sid]
    rectangle(
        (n.x + ox2, n.y + oy2),
        width=n.width,
        height=n.height,
        style=st.patch(shape_r=1.6),
        text=label,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    )

save()
```

---

## 11.4 Clustered Cloud Topologies & Matrix Grids

When building multi-zone cloud architectures or tabular service catalogs, `ArchitectureGraph` and `GridGraph` compute nested container boxes alongside node placements:

- **`ArchitectureGraph` + `ArchitectureDiagram` Synergy**: Pin macro zones with `pos="left" | "center" | "right" | "top" | "bottom"` and sequence nested subnets with `parent="vpc", order=1, 2`. Feed top-level clusters via `xy=layout["vpc"].bottom_left`, nested subnets via `xy=layout["app"].local_bottom_left`, and enclosed nodes via `xy=layout["api"].local_xy`—matching the exact `padding` and `(width, height)` values across both steps.
- **`GridGraph` Smart Corridor Routing**: Place nodes into `(row, col)` matrix cells with `g.cell("id", row=0, col=1)`, wrap rows or columns in dashed bands via `g.cluster_row(0, "fe_tier")` or `g.cluster_column(col, id)`, and rely on `edge_routing="smart"` to route non-adjacent connections cleanly through inter-row and inter-column corridors without crossing intermediate cards.

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.graph import ArchitectureGraph
from drawlib.styles import Styles

setup(width=168, height=78)

# Step 1: Solve nested VPC & subnet coordinates with ArchitectureGraph
g = ArchitectureGraph(direction="LR", container_sep=14.0, default_node_width=24.0, default_node_height=14.0)
g.cluster("edge", ["client"], pos="left", padding=5.0)
g.group("vpc", pos="center", padding=5.0)
g.cluster("app_tier", ["api", "worker"], parent="vpc", order=1, padding=5.0)
g.cluster("data_tier", ["db"], parent="vpc", order=2, padding=5.0)

g.edge("client", "api")
g.edge("api", "worker")
g.edge("worker", "db")

layout = g.get_layout(margin=8.0)

# Step 2: Render using .bottom_left, .local_bottom_left, and .local_xy
d = ArchitectureDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

edge_grp = d.add(NodeGroup(title="External", padding=5.0, style=Styles.MutedDashed), xy=layout["edge"].bottom_left)
vpc_grp = d.add(NodeGroup(title="Production VPC", padding=5.0, style=Styles.MutedDashed), xy=layout["vpc"].bottom_left)
app_grp = vpc_grp.add(NodeGroup(title="Compute", padding=5.0, style=Styles.PrimaryNeutral), xy=layout["app_tier"].local_bottom_left)
data_grp = vpc_grp.add(NodeGroup(title="Storage", padding=5.0, style=Styles.SecondaryNeutral), xy=layout["data_tier"].local_bottom_left)

client = edge_grp.add(Node("Client", width=24, height=14, icon=PhosphorIcon.DEVICES), xy=layout["client"].local_xy)
api = app_grp.add(
    Node(
        "API Gateway",
        width=24,
        height=14,
        icon=GcpIcon.CLOUD_API_GATEWAY,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    ),
    xy=layout["api"].local_xy,
)
worker = app_grp.add(Node("Worker", width=24, height=14, icon=GcpIcon.CLOUD_RUN), xy=layout["worker"].local_xy)
db = data_grp.add(Node("Cloud SQL", width=24, height=14, icon=GcpIcon.CLOUD_SQL), xy=layout["db"].local_xy)

d.connect(client, api, label="HTTPS")
d.connect(api, worker)
d.connect(worker, db)

d.draw()
save("arch_graph_vpc.png")
```
