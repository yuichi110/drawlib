::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# The 5 Specialized Graph Layout Solvers
:::

::: block (80, 140) (640, 840) compact
## Choosing the Right Solver for Your Topology

Instead of forcing one generic algorithm onto every graph, `drawlib.graph` provides **5 domain-tuned layout solvers** sharing the `BaseGraph` API:

1. **`ArchitectureGraph` (Compass + Nested Packing)**:
   - 2-level macro/micro packer: nests child clusters inside parent containers (`parent="vpc"`) and positions top-level zones via compass coordinates (`pos="left" | "center" | "right" | "top" | "bottom"`).
2. **`LayerGraph` (Sugiyama Hierarchical DAG)**:
   - Cycle removal, longest-path rank assignment, `.tier()` rank pinning, and barycenter edge-crossing minimization.
3. **`TreeGraph` (Reingold-Tilford Compact Tree)**:
   - Proportional subtree contour spacing via `.child(parent, child)` so sibling branches never overlap.
4. **`RadialGraph` (Concentric Hub & Spoke)**:
   - Places a central `hub` at `ring=0` and allocates angular sectors across concentric rings (`draw_ring_guides=True`).
5. **`GridGraph` (2D Matrix + Smart Channel Routing)**:
   - Places cells at `(row, col)` with `.cluster_row()` / `.cluster_column()` and routes non-adjacent edges through inter-cell channels.
:::

::: block (760, 140) (1080, 840)
```drawlib file:graph_solvers_compare.svg
from drawlib.canvas import clear, save, setup
from drawlib.graph import (
    ArchitectureGraph,
    GridGraph,
    LayerGraph,
    RadialGraph,
    TreeGraph,
)
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=108, height=84)

txt_node = Styles.DarkBold.patch(text_size=5.8)
txt_hero = Styles.WhiteBold.patch(text_size=5.8)
txt_cluster = Styles.DarkBold.patch(text_size=5.8)

# 1. Top-Left Panel: ArchitectureGraph (Compass + Nested Containers)
rectangle((28, 63), width=50, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((5, 79.5), "1. ArchitectureGraph (Compass + VPC)", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_arch = ArchitectureGraph(
    direction="LR",
    container_sep=3.5,
    default_node_width=8.0,
    default_node_height=4.2,
    default_node_text_style=txt_node,
)
g_arch.cluster("ext", ["cli"], label="Client", pos="left", padding=1.8, text_style=txt_cluster)
g_arch.node("cli", "App", style=Styles.Neutral)
g_arch.group("vpc", "Cloud VPC", pos="center", padding=1.8, text_style=txt_cluster)
g_arch.cluster("compute", ["api", "wrk"], label="Compute", parent="vpc", order=1, padding=1.6, text_style=txt_cluster)
g_arch.node("api", "API", style=Styles.PrimaryFlat, text_style=txt_hero)
g_arch.node("wrk", "Worker", style=Styles.PrimaryNeutral)
g_arch.edge("cli", "api")
g_arch.edge("api", "wrk")
g_arch.draw(xy=(4.5, 45.5), width=60.0, height=38.0, margin=3.0, scale=0.78)

# 2. Top-Right Panel: LayerGraph (Sugiyama Layered DAG)
rectangle((80, 63), width=50, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((57, 79.5), "2. LayerGraph (Sugiyama DAG)", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_layer = LayerGraph(
    direction="LR",
    rank_sep=5.0,
    node_sep=3.0,
    default_node_width=9.5,
    default_node_height=4.8,
    default_node_text_style=txt_node,
)
g_layer.node("src", "Ingest", style=Styles.Neutral)
g_layer.node("a", "Parse", style=Styles.PrimaryNeutral)
g_layer.node("b", "Enrich", style=Styles.SecondaryNeutral)
g_layer.node("sink", "Index", style=Styles.PrimaryFlat, text_style=txt_hero)
g_layer.tier("mid", ["a", "b"], layer=1)
g_layer.edge("src", "a")
g_layer.edge("src", "b")
g_layer.edge("a", "sink")
g_layer.edge("b", "sink")
g_layer.draw(xy=(55.0, 44.0), width=50.0, height=33.0, margin=3.5)

# 3. Bottom-Left Panel: TreeGraph (Reingold-Tilford Hierarchy)
rectangle((19, 21), width=32, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((5, 37.5), "3. TreeGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_tree = TreeGraph(
    root="root",
    direction="TB",
    default_node_width=8.5,
    default_node_height=4.5,
    default_node_text_style=txt_node,
)
g_tree.node("root", "Root", style=Styles.PrimaryFlat, text_style=txt_hero)
g_tree.child("root", "c1", "plat", style=Styles.PrimaryNeutral)
g_tree.child("root", "c2", "app", style=Styles.SecondaryNeutral)
g_tree.child("c1", "l1", "k8s", style=Styles.Neutral)
g_tree.child("c1", "l2", "iam", style=Styles.Neutral)
g_tree.draw(xy=(3.0, 2.0), width=32.0, height=33.0, margin=3.0)

# 4. Bottom-Center Panel: RadialGraph (Concentric Hub & Spoke)
rectangle((54, 21), width=34, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((39, 37.5), "4. RadialGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_rad = RadialGraph(
    hub="hub",
    radius_step=9.5,
    draw_ring_guides=True,
    default_node_width=7.0,
    default_node_height=4.0,
    default_node_text_style=txt_node,
)
g_rad.node("hub", "Mesh", shape="circle", width=7.5, height=7.5, style=Styles.PrimaryFlat, text_style=txt_hero)
g_rad.spoke("hub", "s1", "Auth", style=Styles.PrimaryNeutral)
g_rad.spoke("hub", "s2", "Pay", style=Styles.SecondaryNeutral)
g_rad.spoke("hub", "s3", "Log", style=Styles.Neutral)
g_rad.spoke("hub", "s4", "DB", style=Styles.BlueNeutral)
g_rad.draw(xy=(37.0, 2.0), width=34.0, height=33.0, margin=3.5)

# 5. Bottom-Right Panel: GridGraph (2D Matrix + Channel Routing)
rectangle((89, 21), width=32, height=38, style=Styles.MutedOutline.patch(shape_r=1.5))
text((75, 37.5), "5. GridGraph", style=Styles.DarkBold.patch(text_size=7.5, halign="left"))

g_grid = GridGraph(
    columns=2,
    default_node_width=9.5,
    default_node_height=5.0,
    default_node_text_style=txt_node,
)
g_grid.cell("w1", row=0, col=0, label="Web", style=Styles.Neutral)
g_grid.cell("w2", row=0, col=1, label="CLI", style=Styles.Neutral)
g_grid.cell("s1", row=1, col=0, label="API", style=Styles.PrimaryFlat, text_style=txt_hero)
g_grid.cell("s2", row=1, col=1, label="DB", style=Styles.SecondaryNeutral)
g_grid.edge("w1", "s1")
g_grid.edge("w2", "s1")
g_grid.edge("s1", "s2")
g_grid.draw(xy=(73.0, 2.0), width=32.0, height=33.0, margin=4.0)

save()
```
:::

::: note
- This final slide of Chapter 4 renders all **5 specialized graph layout solvers** side-by-side on a single 108x84 canvas—demonstrating that even auto-layout graphs can be composed into multi-panel dashboards using `g.draw(xy=..., width=..., height=...)`:
  1. **`ArchitectureGraph` (Top-Left)**: Packs nested containers (`Compute` inside `Cloud VPC`) and aligns top-level compass zones (`Client` on the left, `Cloud VPC` in the center).
  2. **`LayerGraph` (Top-Right)**: Runs the Sugiyama hierarchical DAG pipeline (`Ingest -> [Parse, Enrich] -> Index`).
  3. **`TreeGraph` (Bottom-Left)**: Balances parent-child subtrees symmetrically using Reingold-Tilford contours.
  4. **`RadialGraph` (Bottom-Center)**: Places the circular `"Mesh"` hub at `ring=0` with dashed concentric ring guides (`draw_ring_guides=True`) and evenly spaced spokes.
  5. **`GridGraph` (Bottom-Right)**: Maps nodes onto a 2x2 matrix (`row`, `col`) with smart channel edge routing.
:::
