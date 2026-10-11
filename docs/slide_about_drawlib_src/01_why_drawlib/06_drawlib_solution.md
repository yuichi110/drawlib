::: block (80, 50) (1760, 120)
# The Drawlib Solution: Declarative Python Architecture
Write clean, type-checked Python on the left—get publication-grade vector diagrams on the right.
:::

::: block (80, 190) (800, 770) compact
### 15 Lines of Declarative Python

```python
from drawlib.diagrams.architecture import (
    ArchitectureDiagram, GcpIcon, Node, NodeGroup, PhosphorIcon,
)
from drawlib.styles import Styles

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
)
vpc = d.add(NodeGroup("Production Cloud VPC", padding=7), (26, 8))
client = d.add(Node("Web Client", width=18, height=16, icon=PhosphorIcon.GLOBE), (8, 42))
gw = vpc.add(
    Node("API Gateway", width=20, height=16, icon=GcpIcon.CLOUD_API_GATEWAY,
         card_style=Styles.PrimaryFlat, text_style=Styles.WhiteBold),
    (16, 34),
)
sql = vpc.add(Node("Cloud SQL", width=20, height=16, icon=GcpIcon.CLOUD_SQL), (54, 50))
bq = vpc.add(Node("BigQuery", width=20, height=16, icon=GcpIcon.BIGQUERY), (54, 18))

d.connect(client, gw, label="HTTPS")
gw.fork([sql, bq], at_x=58, padding=1.5)
d.draw()
```

- **Auto-Bounding Containers**: `NodeGroup` wraps child nodes automatically.
- **Smart Orthogonal Edges**: `.connect()` and `.fork()` clip cleanly at node boundaries.
:::

::: block (920, 180) (920, 780)
```drawlib file:solution_demo.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.styles import Styles

clear()
setup(width=105, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=9),
    node_card_style=Styles.Neutral,
    title="Production Cloud VPC Architecture",
    title_style=Styles.DarkBold.patch(text_size=13),
)

vpc = d.add(
    NodeGroup(title="Production Cloud VPC (10.0.0.0/16)", padding=7.0, style=Styles.PrimaryNeutral),
    xy=(28.0, 10.0),
)
client = d.add(
    Node("Web Client", width=18, height=17, icon=PhosphorIcon.GLOBE, icon_size=9.0),
    xy=(9.0, 42.0),
)
gw = vpc.add(
    Node(
        "API Gateway",
        width=20,
        height=17,
        icon=GcpIcon.CLOUD_API_GATEWAY,
        icon_size=9.5,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10),
    ),
    xy=(15.0, 32.0),
)
sql = vpc.add(
    Node("Cloud SQL\n(Primary)", width=22, height=18, icon=GcpIcon.CLOUD_SQL, icon_size=9.0, card_style=Styles.SecondaryNeutral),
    xy=(50.0, 48.0),
)
bq = vpc.add(
    Node("BigQuery\n(Analytics)", width=22, height=18, icon=GcpIcon.BIGQUERY, icon_size=9.0, card_style=Styles.White),
    xy=(50.0, 16.0),
)

d.connect(client, gw, label="HTTPS", padding=1.5)
gw.fork([sql, bq], at_x=60.0, padding=1.5)

d.draw(xy=(4.0, 6.0))
save()
```
:::

::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: note
- Look at how clean the Drawlib solution is in practice.
- On the left is a 15-line declarative Python snippet using `ArchitectureDiagram`, `NodeGroup`, `Node`, and official `GcpIcon` / `PhosphorIcon` enums.
- On the right is the exact vector SVG output compiled from that snippet: `NodeGroup` automatically computes its bounding box around child nodes, `gw.fork([sql, bq])` routes a 1-to-2 orthogonal bus fan-out, and our 50%+ neutral baseline keeps the visual hierarchy crisp with `API Gateway` as the focal hero node.
:::
