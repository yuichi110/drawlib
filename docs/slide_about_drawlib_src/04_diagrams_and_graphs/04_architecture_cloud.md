::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Multi-Tier Production Cloud Topology (`GcpIcon` & `PhosphorIcon`)
:::

::: block (80, 140) (620, 840) compact
## Official Cloud & Interface Icons Built In

`drawlib.diagrams.architecture` integrates directly with Drawlib's icon ecosystem:
- **`GcpIcon` (259 Official Icons)**:
  - Compute & Containers: `GcpIcon.GOOGLE_KUBERNETES_ENGINE`, `GcpIcon.CLOUD_RUN`, `GcpIcon.COMPUTE_ENGINE`
  - Networking & Security: `GcpIcon.CLOUD_LOAD_BALANCING`, `GcpIcon.CLOUD_ARMOR`, `GcpIcon.CLOUD_CDN`
  - Databases & Storage: `GcpIcon.CLOUD_SQL`, `GcpIcon.CLOUD_SPANNER`, `GcpIcon.CLOUD_STORAGE`, `GcpIcon.BIGQUERY`
- **`PhosphorIcon` (1,531 Vector Icons)**:
  - Clients, browsers, devices, locks, queues, and generic infrastructure symbols.

### Nested Hierarchical `NodeGroup`s
- Nest `Public Subnet` and `Private Subnet` groups inside an outer `VPC Network` group (`vpc.add(NodeGroup(...), xy=...)`).
- Child coordinates inside a `NodeGroup` are local to that group's origin, making subnet refactoring effortless.
:::

::: block (740, 140) (1100, 840)
```drawlib file:arch_cloud_vpc.svg
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
setup(width=110, height=84)

d = ArchitectureDiagram(
    node_style=Styles.Neutral,
    node_text_style=Styles.DarkBold.patch(text_size=7.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=6.8),
    title="Production Multi-Subnet Google Cloud VPC Architecture",
    title_style=Styles.DarkBold.patch(text_size=9.5),
)

# Outer VPC Network boundary
vpc = d.add(
    NodeGroup(
        title="VPC Network (10.0.0.0/16)",
        padding=5.5,
        style=Styles.MutedDashed,
    ),
    xy=(22.0, 6.0),
)

# Public Subnet with Cloud Load Balancing
public_subnet = vpc.add(
    NodeGroup(
        title="Public Subnet (10.0.1.0/24)",
        padding=4.5,
        style=Styles.PrimaryNeutral,
    ),
    xy=(5.0, 5.0),
)
lb = public_subnet.add(
    Node(
        "Cloud Load\nBalancing",
        icon=GcpIcon.CLOUD_LOAD_BALANCING,
        icon_size=7.0,
    ),
    xy=(11.0, 24.0),
)

# Private Subnet with GKE Application Pods
private_subnet = vpc.add(
    NodeGroup(
        title="Private Subnet (10.0.2.0/24)",
        padding=4.5,
        style=Styles.SecondaryNeutral,
    ),
    xy=(33.0, 5.0),
)
gke1 = private_subnet.add(
    Node(
        "GKE API Pod 1",
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=7.0,
    ),
    xy=(12.0, 35.0),
)
gke2 = private_subnet.add(
    Node(
        "GKE API Pod 2",
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=7.0,
    ),
    xy=(12.0, 13.0),
)

# External Client & Managed Data Tier
user = d.add(
    Node("Client User", icon=PhosphorIcon.USER, icon_size=7.0),
    xy=(6.0, 35.0),
)
db = d.add(
    Node(
        "Cloud SQL\n(PostgreSQL)",
        icon=GcpIcon.CLOUD_SQL,
        icon_size=7.0,
    ),
    xy=(94.0, 46.0),
)
storage = d.add(
    Node(
        "Cloud Storage\n(Object Store)",
        icon=GcpIcon.CLOUD_STORAGE,
        icon_size=7.0,
    ),
    xy=(94.0, 24.0),
)

# Orthogonal connections & fan-out
d.connect(user, lb, label="HTTPS", padding=1.5)
lb.fork([gke1, gke2], at_x=48.0, padding=1.5)
d.connect(gke1, db, label="SQL", padding=1.5)
d.connect(gke2, storage, label="GCS Sync", padding=1.5)

d.draw(xy=(2.0, 6.0))

save()
```
:::

::: note
- Here we see a complete production Google Cloud VPC topology rendered with `ArchitectureDiagram`.
- Notice the nested `NodeGroup` hierarchy:
  - The outer `VPC Network (10.0.0.0/16)` group encloses two inner groups: `Public Subnet (10.0.1.0/24)` (styled in `Styles.PrimaryNeutral`) and `Private Subnet (10.0.2.0/24)` (styled in `Styles.SecondaryNeutral`).
  - Official `GcpIcon` assets (`GcpIcon.CLOUD_LOAD_BALANCING`, `GcpIcon.GOOGLE_KUBERNETES_ENGINE`, `GcpIcon.CLOUD_SQL`, `GcpIcon.CLOUD_STORAGE`) are paired with `PhosphorIcon.USER` for external client traffic.
  - `lb.fork([gke1, gke2], at_x=48.0)` cleanly splits traffic across the subnet boundary into both GKE pods.
:::
