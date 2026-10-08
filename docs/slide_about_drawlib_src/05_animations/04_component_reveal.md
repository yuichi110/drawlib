::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Progressive Component Reveal (`.show = False` → `True`)
:::

::: block (80, 140) (740, 840) font:20px
## Zero Layout Jump Across Keyframes

Every element in `drawlib.smartarts`, `drawlib.diagrams`, and `drawlib.graph` supports a mutable **`.show: bool`** property.

```python
# Build full topology once outside the loop
d = ArchitectureDiagram(...)
vpc = d.add(NodeGroup("Cloud VPC"), xy=(6, 8))
n1 = vpc.add(Node("1. Edge LB", ...), xy=(14, 24))
n2 = vpc.add(Node("2. App Tier", ...), xy=(42, 24), show=False)
n3 = vpc.add(Node("3. Storage", ...), xy=(70, 24), show=False)
d.connect(n1, n2, label="gRPC")
d.connect(n2, n3, label="SQL")

# Reveal progressively across frames
for step in range(3):
    n2.show = (step >= 1)
    n3.show = (step >= 2)
    with anim.frame(duration=0.8):
        d.draw()
```

### Why `.show` Beats Omitting `.add()`
- **Fixed Container Bounds**: `NodeGroup`, `ChevronProcess`, `GridLayout`, and `LayerGraph` compute full bounding boxes across all registered items—even when `show=False`.
- **Automatic Edge Hiding**: Hiding a diagram node (`n3.show = False`) automatically hides its incoming/outgoing edges and dangling junctions.
:::

::: block (860, 140) (980, 840)
```drawlib file:progressive_arch_anim.png anim:click anim-loop:once anim-pause:1,2,3
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)
anim = Animation(fps=1.25, loop=0)

stages = [
    ("1. Ingest", "Edge CDN"),
    ("2. Route", "API Gateway"),
    ("3. Process", "Cloud Run"),
    ("4. Persist", "Cloud SQL"),
    ("5. Analyze", "BigQuery"),
]

# Pre-build ArchitectureDiagram once outside the frame loop
diag = ArchitectureDiagram(
    node_style=Styles.Neutral,
    node_text_style=Styles.DarkBold.patch(text_size=8.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=8.0),
)
vpc = diag.add(
    NodeGroup(title="Google Cloud Production Environment (Auto-Bounded)", padding=6.5, style=Styles.PrimaryNeutral),
    xy=(22.0, 10.0),
)

n_edge = diag.add(Node("1. Edge CDN", icon=PhosphorIcon.GLOBE, icon_size=7.0), xy=(9.0, 26.0))
n_gw = vpc.add(Node("2. API Gateway", icon=GcpIcon.CLOUD_API_GATEWAY, icon_size=7.0), xy=(10.0, 16.0))
n_run = vpc.add(Node("3. Cloud Run", icon=GcpIcon.CLOUD_RUN, icon_size=7.0), xy=(30.0, 16.0))
n_sql = vpc.add(Node("4. Cloud SQL", icon=GcpIcon.CLOUD_SQL, icon_size=7.0), xy=(50.0, 25.0))
n_bq = vpc.add(Node("5. BigQuery", icon=GcpIcon.BIGQUERY, icon_size=7.0), xy=(50.0, 7.0))

diag.connect(n_edge, n_gw, label="HTTPS", padding=1.5)
diag.connect(n_gw, n_run, label="gRPC", padding=1.5)
diag.connect(n_run, n_sql, label="Write", padding=1.5)
diag.connect(n_run, n_bq, label="Stream", padding=1.5)

arch_nodes = [n_edge, n_gw, n_run, n_sql, n_bq]

for step in range(5):
    is_last = step == 4
    with anim.frame(duration=2.5 if is_last else 0.8):
        rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
        text(
            (49, 75),
            f"Progressive Reveal — Stage {step + 1} of 5  (Click or Press 'A' to Step)",
            style=Styles.DarkBold.patch(text_size=11.0),
        )

        # Top: ChevronProcess with layout-preserving show=(i <= step)
        proc = ChevronProcess(
            style=Styles.Neutral,
            text_style=Styles.DarkBold.patch(text_size=8.8),
            description_style=Styles.Muted.patch(text_size=7.5),
            corner_angle=55.0,
            spacing=1.2,
            flat_left_end=True,
        )
        for i, (title_s, desc_s) in enumerate(stages):
            is_curr = i == step
            proc.add(
                title_s,
                description=desc_s,
                style=Styles.PrimaryFlat if is_curr else Styles.PrimaryNeutral,
                text_style=Styles.WhiteBold.patch(text_size=8.8) if is_curr else Styles.DarkBold.patch(text_size=8.8),
                description_style=Styles.White.patch(text_size=7.5) if is_curr else Styles.Muted.patch(text_size=7.5),
                show=(i <= step),
            )
        proc.draw(xy=(6.0, 54.0), width=86.0, height=14.0)

        # Bottom: Mutate .show on ArchitectureDiagram nodes (VPC box never shifts!)
        for i, node in enumerate(arch_nodes):
            node.show = i <= step
            node.text_style = (
                Styles.PrimaryBold.patch(text_size=9.0) if i == step else Styles.DarkBold.patch(text_size=8.5)
            )
        diag.draw(xy=(2.0, 2.0))

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Layout-Preserving Progressive Reveal*
:::

::: note
- Click the diagram (or press `A`) to step through the 5 stages interactively!
- Notice two critical behaviors:
  1. In the top `ChevronProcess`, Stage 1 already has its exact 1/5th width on Frame 0 because stages 2–5 are registered with `show=False`.
  2. In the bottom `ArchitectureDiagram`, the `Google Cloud Production Environment` VPC boundary stays 100% locked at its full size from Frame 0, and edges appear automatically as their target nodes turn `.show = True`.
:::
