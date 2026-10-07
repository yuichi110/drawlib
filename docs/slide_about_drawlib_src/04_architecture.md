::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Cloud & Microservices
:::

::: block (80, 140) (740, 840) font:22px
## Scalable Topologies in Code

Drawlib provides high-level domain modules for cloud architecture with vector and official cloud icons:

- **Client Ingress**: Web SPA, Mobile App, Edge Workers terminating TLS
- **Kubernetes Cluster**: Isolated container pods with auto-scaling
- **Data Persistence**: Sharded primary database + Pub/Sub event streaming
- **Clean Syntax**: Connect nodes with labels and automatic orthogonal routing
:::

::: block (860, 140) (980, 840) z:5
```drawlib file:arch_diagram.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup
from drawlib.styles import Styles

clear()
setup(width=115, height=75)
arch = ArchitectureDiagram(
    node_style=Styles.PrimaryFlat,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.Primary,
    edge_text_style=Styles.Dark,
    title="Scalable Microservices Topology (GCP)",
)

client = arch.add(Node("Client App", icon=GcpIcon.APP_ENGINE, icon_size=7.5), (14.0, 42.0))
gateway = arch.add(Node("API Gateway", icon=GcpIcon.CLOUD_API_GATEWAY, icon_size=7.5), (38.0, 42.0))

cluster = arch.add(NodeGroup(title="Kubernetes Service Cluster", padding=4.5), (63.0, 20.0))
auth = cluster.add(Node("Auth Service", icon=GcpIcon.COMPUTE_ENGINE, icon_size=6.5), (13.0, 36.0))
orders = cluster.add(Node("Order Service", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=6.5), (13.0, 16.0))

db = arch.add(Node("Cloud SQL", icon=GcpIcon.CLOUD_SQL, icon_size=7.5), (98.0, 52.0))
queue = arch.add(Node("Pub/Sub Queue", icon=GcpIcon.PUBSUB, icon_size=7.5), (98.0, 24.0))

arch.connect(client, gateway, label="HTTPS/REST", routing="orthogonal")
arch.connect(gateway, auth, label="Token", routing="orthogonal")
arch.connect(gateway, orders, label="Order", routing="orthogonal")
arch.connect(orders, db, label="Commit Tx", routing="orthogonal")
arch.connect(orders, queue, label="Publish", routing="orthogonal")

arch.draw(xy=(3.0, 3.0))
save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Drawlib: Illustration as Code*
:::
