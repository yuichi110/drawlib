::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Cloud Topology with ArchitectureDiagram
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=cloud_arch_showcase.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=176, height=82)

panel = Panel(
    "Multi-Tier Cloud Platform Topology",
    "GcpIcon + PhosphorIcon + Nested NodeGroup + Orthogonal Bus Routing",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.5),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.cloud,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
panel.draw((2.0, 2.0), width=172.0, height=78.0)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
    node_card_style=Styles.Neutral,
)

users = d.add(
    Node("Global Users\n& Devices", width=21, height=17.5, icon=PhosphorIcon.DEVICES, icon_size=7.0),
    xy=(11.5, 31.0),
)
edge = d.add(
    Node(
        "Cloud CDN\n& Armor WAF",
        width=22,
        height=17.5,
        icon=GcpIcon.CLOUD_ARMOR,
        icon_size=7.0,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(42.5, 31.0),
)

vpc = d.add(
    NodeGroup(
        title="Production VPC (10.0.0.0/16)",
        width=44.0,
        height=58.0,
        padding=5.0,
        style=Styles.MutedDashed,
        text_style=Styles.DarkBold.patch(text_size=12.0, halign="left"),
    ),
    xy=(66.5, 2.0),
)
gke = vpc.add(
    Node(
        "GKE API\nMicroservices",
        width=28,
        height=16.5,
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=7.0,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=11.5),
    ),
    xy=(22.0, 41.0),
)
run = vpc.add(
    Node(
        "Cloud Run\nAsync Workers",
        width=28,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=7.0,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(22.0, 13.5),
)

sql = d.add(
    Node(
        "Cloud SQL\n(PostgreSQL)",
        width=25,
        height=15.5,
        icon=GcpIcon.CLOUD_SQL,
        icon_size=6.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(150.5, 51.5),
)
pubsub = d.add(
    Node(
        "Pub/Sub\nEvent Bus",
        width=25,
        height=15.5,
        icon=GcpIcon.PUBSUB,
        icon_size=6.5,
        card_style=Styles.Neutral,
    ),
    xy=(150.5, 33.5),
)
bq = d.add(
    Node(
        "BigQuery\nData Warehouse",
        width=25,
        height=15.5,
        icon=GcpIcon.BIGQUERY,
        icon_size=6.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(150.5, 15.5),
)

d.connect(users, edge, label="HTTPS", padding=1.2)
edge.fork([gke, run], at_x=60.5, padding=1.2)
d.connect(gke, run, label="gRPC", padding=1.0)
d.connect(gke, sql, label="SQL", padding=1.2)
d.connect(gke, pubsub, label="Events", padding=1.2)
d.connect(run, bq, label="Stream", padding=1.2)

d.draw(xy=(6.0, 4.5))
save()
```
:::

::: note
**Cloud Infrastructure Topology with `ArchitectureDiagram`**:
- **33 Built-In Icon Catalogs**: `ArchitectureDiagram` integrates official cloud provider icons (`GcpIcon`, `AwsIcon`, `AzureIcon`), technology domain logos (`CnativeIcon`, `DataIcon`, `DevopsIcon`), and 1,500+ monochrome UI symbols (`PhosphorIcon`) directly inside `Node` cards.
- **Hierarchical Network Boundaries (`NodeGroup`)**: Here, `Production VPC (10.0.0.0/16)` encloses both `GKE API Microservices` (focal hero node in `Styles.PrimaryFlat`) and `Cloud Run Async Workers` using clean group-local coordinates relative to the VPC's bottom-left origin.
- **Orthogonal Bus Fan-Out & Clean Routing**: Calling `edge.fork([gke, run], at_x=60.5)` creates an automatic T-junction bus from the `Cloud CDN & Armor WAF` edge tier into the VPC compute services, while non-crossing Manhattan edges connect compute tiers to `Cloud SQL`, `Pub/Sub`, and `BigQuery`.
:::
