::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
import utils

utils.draw_page_number()
```
:::

::: block xy=(80, 40) width=1760 height=60
# The 5 Specialized Graph Layout Solvers
:::

::: block xy=(80, 140) width=640 height=840 compact=true
## Choosing the Right Solver for Your Topology

Instead of forcing one generic algorithm onto every graph, `drawlib.graph` provides **5 domain-tuned layout solvers** sharing the `BaseGraph.get_layout()` API:

1. **`ArchitectureGraph` (Compass + Nested Packing)**:
   - 2-level macro/micro packer: nests child clusters inside parent containers (`parent="vpc"`) and positions top-level zones via compass coordinates (`pos="left" | "center" | "right" | "top" | "bottom"`).
2. **`LayerGraph` (Sugiyama Hierarchical DAG)**:
   - Cycle removal, longest-path rank assignment, `.tier()` rank pinning, and barycenter edge-crossing minimization.
3. **`TreeGraph` (Reingold-Tilford Compact Tree)**:
   - Proportional subtree contour spacing via `.child(parent, child)` so sibling branches never overlap.
4. **`RadialGraph` (Concentric Hub & Spoke)**:
   - Places a central `hub` at `ring=0`, allocates angular sectors across concentric rings, and exposes radii via `layout.ring_radii`.
5. **`GridGraph` (2D Matrix + Smart Channel Routing)**:
   - Places cells at `(row, col)` with `.cluster_row()` / `.cluster_column()` and routes non-adjacent edges through inter-cell channels.
:::

::: block xy=(760, 140) width=1080 height=840
```drawlib file=graph_solvers_compare.svg
from drawlib.canvas import clear, save, setup
from drawlib.graph import (
    ArchitectureGraph,
    GraphLayout,
    GridGraph,
    LayerGraph,
    RadialGraph,
    TreeGraph,
)
from drawlib.lines import line, lines
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=108, height=84)

txt_node = Styles.DarkBold.patch(text_size=6.2)
txt_hero = Styles.WhiteBold.patch(text_size=6.2)
txt_cluster = Styles.DarkBold.patch(text_size=6.0, halign="left")


def render_panel(
    layout: GraphLayout,
    ox: float,
    oy: float,
    labels: dict[str, tuple[str, object]],
    clusters: dict[str, str] | None = None,
    circle_ids: set[str] | None = None,
    scale: float = 1.0,
) -> None:
    if clusters:
        for cid, c_title in clusters.items():
            c = layout[cid]
            rectangle(
                (ox + c.cx * scale, oy + c.cy * scale),
                width=c.width * scale,
                height=c.height * scale,
                style=Styles.MutedDashed.patch(shape_r=1.2),
            )
            text((ox + c.left * scale + 1.0, oy + c.top * scale - 1.5), c_title, style=txt_cluster)
    for r in layout.ring_radii.values():
        hub = layout["hub"]
        circle((ox + hub.x * scale, oy + hub.y * scale), radius=r * scale, style=Styles.MutedDashed)
    for e in layout.edges:
        pts = [(ox + px * scale, oy + py * scale) for px, py in e.points]
        if len(pts) == 2:
            line(pts[0], pts[1], arrow_head="->", style=Styles.DarkBold)
        else:
            lines(pts, arrow_head="->", style=Styles.DarkBold)
    for nid, (lbl, st) in labels.items():
        n = layout[nid]
        ts = txt_hero if st == Styles.PrimaryFlat else txt_node
        if circle_ids and nid in circle_ids:
            circle((ox + n.x * scale, oy + n.y * scale), radius=(n.width / 2.0) * scale, style=st, text=lbl, text_style=ts)
        else:
            rectangle(
                (ox + n.x * scale, oy + n.y * scale),
                width=n.width * scale,
                height=n.height * scale,
                style=st.patch(shape_r=1.2),
                text=lbl,
                text_style=ts,
            )


# 1. Top-Left Panel: ArchitectureGraph (Compass + Nested Containers)
rectangle((28, 63), width=50, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((5, 79.5), "1. ArchitectureGraph (Compass + VPC)", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_arch = ArchitectureGraph(
    direction="LR",
    container_sep=3.5,
    default_node_width=9.0,
    default_node_height=4.8,
)
g_arch.cluster("ext", ["cli"], pos="left", padding=2.4, header_height=5.0)
g_arch.group("vpc", pos="center", padding=2.0, header_height=5.0)
g_arch.cluster("compute", ["api", "wrk"], parent="vpc", order=1, padding=3.4, header_height=5.0)
g_arch.edge("cli", "api")
g_arch.edge("api", "wrk")
l_arch = g_arch.get_layout(width=62.0, height=40.0, margin=3.0)
for nid in ("api", "wrk", "cli"):
    l_arch.offset(nid, dy=-1.3)
render_panel(
    l_arch,
    2.0,
    46.0,
    {"cli": ("App", Styles.Neutral), "api": ("API", Styles.PrimaryFlat), "wrk": ("Worker", Styles.PrimaryNeutral)},
    {"ext": "Client", "vpc": "Cloud VPC", "compute": "Compute"},
    scale=0.72,
)

# 2. Top-Right Panel: LayerGraph (Sugiyama Layered DAG)
rectangle((80, 63), width=50, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((57, 79.5), "2. LayerGraph (Sugiyama DAG)", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_layer = LayerGraph(direction="LR", rank_sep=5.0, node_sep=3.0, default_node_width=9.5, default_node_height=5.0)
g_layer.node("src")
g_layer.node("a")
g_layer.node("b")
g_layer.node("sink")
g_layer.tier("mid", ["a", "b"], layer=1)
g_layer.edge("src", "a")
g_layer.edge("src", "b")
g_layer.edge("a", "sink")
g_layer.edge("b", "sink")
l_layer = g_layer.get_layout(width=48.0, height=32.0, margin=3.0)
render_panel(
    l_layer,
    56.0,
    44.5,
    {"src": ("Ingest", Styles.Neutral), "a": ("Parse", Styles.PrimaryNeutral), "b": ("Enrich", Styles.SecondaryNeutral), "sink": ("Index", Styles.PrimaryFlat)},
)

# 3. Bottom-Left Panel: TreeGraph (Reingold-Tilford Hierarchy)
rectangle((19, 21), width=32, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((5, 37.5), "3. TreeGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_tree = TreeGraph(root="root", direction="TB", default_node_width=8.0, default_node_height=4.5)
g_tree.node("root")
g_tree.child("root", "c1")
g_tree.child("root", "c2")
g_tree.child("c1", "l1")
g_tree.child("c1", "l2")
l_tree = g_tree.get_layout(width=30.0, height=32.0, margin=2.5)
render_panel(
    l_tree,
    4.0,
    2.5,
    {"root": ("Root", Styles.PrimaryFlat), "c1": ("plat", Styles.PrimaryNeutral), "c2": ("app", Styles.SecondaryNeutral), "l1": ("k8s", Styles.Neutral), "l2": ("iam", Styles.Neutral)},
)

# 4. Bottom-Center Panel: RadialGraph (Concentric Hub & Spoke)
rectangle((54, 21), width=34, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((39, 37.5), "4. RadialGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_rad = RadialGraph(hub="hub", radius_step=9.5, default_node_width=7.0, default_node_height=4.2)
g_rad.node("hub", width=7.6, height=7.6)
g_rad.spoke("hub", "s1")
g_rad.spoke("hub", "s2")
g_rad.spoke("hub", "s3")
g_rad.spoke("hub", "s4")
l_rad = g_rad.get_layout(width=32.0, height=32.0, margin=3.0)
render_panel(
    l_rad,
    38.0,
    2.5,
    {"hub": ("Mesh", Styles.PrimaryFlat), "s1": ("Auth", Styles.PrimaryNeutral), "s2": ("Pay", Styles.SecondaryNeutral), "s3": ("Log", Styles.Neutral), "s4": ("DB", Styles.BlueNeutral)},
    circle_ids={"hub"},
)

# 5. Bottom-Right Panel: GridGraph (2D Matrix + Channel Routing)
rectangle((89, 21), width=32, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((75, 37.5), "5. GridGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_grid = GridGraph(columns=2, default_node_width=9.5, default_node_height=5.0)
g_grid.cell("w1", row=0, col=0)
g_grid.cell("w2", row=0, col=1)
g_grid.cell("s1", row=1, col=0)
g_grid.cell("s2", row=1, col=1)
g_grid.edge("w1", "s1")
g_grid.edge("w2", "s1")
g_grid.edge("s1", "s2")
l_grid = g_grid.get_layout(width=30.0, height=32.0, margin=3.5)
render_panel(
    l_grid,
    74.0,
    2.5,
    {"w1": ("Web", Styles.Neutral), "w2": ("CLI", Styles.Neutral), "s1": ("API", Styles.PrimaryFlat), "s2": ("DB", Styles.SecondaryNeutral)},
)

save()
```
:::

::: note
- This final slide of Chapter 4 solves and renders all **5 specialized graph layout solvers** side-by-side on a single 108x84 canvas using `get_layout(width=..., height=...)`:
  1. **`ArchitectureGraph` (Top-Left)**: Packs nested containers (`Compute` inside `Cloud VPC`) and aligns top-level compass zones (`Client` on the left, `Cloud VPC` in the center).
  2. **`LayerGraph` (Top-Right)**: Runs the Sugiyama hierarchical DAG pipeline (`Ingest -> [Parse, Enrich] -> Index`).
  3. **`TreeGraph` (Bottom-Left)**: Balances parent-child subtrees symmetrically using Reingold-Tilford contours.
  4. **`RadialGraph` (Bottom-Center)**: Places the circular `"Mesh"` hub at `ring=0` with dashed concentric ring guides (`layout.ring_radii`) and evenly spaced spokes.
  5. **`GridGraph` (Bottom-Right)**: Maps nodes onto a 2x2 matrix (`row`, `col`) with smart channel edge routing.
:::
