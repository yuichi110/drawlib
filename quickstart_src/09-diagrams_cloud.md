# 9. Cloud & Distributed Architecture Diagrams

Designing scalable cloud infrastructures, microservices, and distributed topologies is one of Drawlib's primary strengths. Drawlib provides tailored containers, directional network connectors, and standardized vector icons to depict complex systems with clarity.

## Blueprint Structure & Boundary Containers

Cloud architecture diagrams follow a standard hierarchy:

1. **Outer Cloud Boundary / Region**: A subtle, dashed boundary container (`Styles.MutedDashed`).
2. **Virtual Private Cloud (VPC) / Subnets**: Structured network zones separating public ingress from private compute tiers.
3. **Managed Services & Workloads**: High-level icons from `drawlib.icons.gcp` or `drawlib.icons.phosphor`.
4. **Data Flows & Protocols**: Directional connectors with protocol labels (`HTTPS`, `gRPC`, `SQL`).

```drawlib 640px center caption:"Figure 9.1: Serverless Cloud Event-Driven Architecture on GCP"
from drawlib.canvas import setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=62)

# Outer Region Boundary
rectangle((60, 31), width=110, height=54, r=3, style=Styles.MutedDashed)
text((24, 54), "Google Cloud (us-central1)", style=Styles.MutedBold, size=9)

# 1. Ingress Client
rectangle((15, 31), width=18, height=24, r=2, style=Styles.AccentOutline)
phosphor.globe(xy=(15, 37), width=8, style=Styles.Accent)
text((15, 24), "Web & Mobile\nClients", style=Styles.PrimaryBold, size=8)

line((24, 31), (34, 31), arrowhead="->", style=Styles.PrimaryBold)
text((29, 34), "HTTPS", style=Styles.PrimaryBold, size=7.5)

# 2. Cloud Run API Gateway
rectangle((45, 31), width=20, height=28, r=2, style=Styles.PrimaryOutline)
gcp.cloud_run(xy=(45, 37), width=9, style=Styles.Primary)
text((45, 23), "Order API\n(Cloud Run)", style=Styles.PrimaryBold, size=8)

line((55, 31), (65, 31), arrowhead="->", style=Styles.PrimaryBold)
text((60, 34), "Publish", style=Styles.PrimaryBold, size=7.5)

# 3. Pub/Sub Event Queue
rectangle((75, 31), width=18, height=28, r=2, style=Styles.SecondaryOutline)
gcp.pubsub(xy=(75, 37), width=9, style=Styles.Secondary)
text((75, 23), "Order Events\n(Pub/Sub)", style=Styles.SecondaryBold, size=8)

line((84, 37), (94, 43), arrowhead="->", style=Styles.PrimaryBold)
line((84, 25), (94, 19), arrowhead="->", style=Styles.PrimaryBold)

# 4. Storage & Analytics Consumers
# Top: Cloud SQL OLTP
rectangle((103, 44), width=18, height=18, r=2, style=Styles.PrimaryOutline)
gcp.cloud_sql(xy=(103, 48), width=8, style=Styles.Primary)
text((103, 38), "Cloud SQL", style=Styles.PrimaryBold, size=7.5)

# Bottom: BigQuery Warehouse
rectangle((103, 18), width=18, height=18, r=2, style=Styles.SuccessOutline)
gcp.bigquery(xy=(103, 22), width=8, style=Styles.Success)
text((103, 12), "BigQuery", style=Styles.PrimaryBold, size=7.5)
```

## Architectural Guidelines for Cloud Blueprints

- **Anchor Primary Services**: Place entry points (clients, API gateways) on the left and progress toward data stores on the right.
- **Color Discipline**: Avoid rainbow diagrams. Use `accent` for entry points, `primary` for services, `secondary` for queues/caches, and `muted` for perimeter network boundaries.
