# API Overview

Welcome to the **__TARGET__** API & SDK Reference. Every endpoint and SDK symbol is documented alongside declarative [Drawlib](https://github.com/yuichi110/drawlib) architecture and sequence diagrams maintained as a single source of truth in Git.

```drawlib align=center code=fold file=api_gateway_topology.png caption="Platform API Gateway & Service Topology"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=120, height=50)

d = ArchitectureDiagram(
    node_style=Styles.Dark,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.Dark.patch(line_width=1.5),
    edge_text_style=Styles.Muted.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

sdk = d.add(
    Node("Client / SDK", icon=PhosphorIcon.TERMINAL_WINDOW, width=22, height=15, card_style=Styles.PrimaryNeutral),
    xy=(16, 25),
)

vpc = d.add(
    NodeGroup(
        "API Platform",
        width=78,
        height=42,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=11.0, halign="left", valign="top"),
    ),
    xy=(36, 4),
)
gw = vpc.add(
    Node(
        "API Gateway",
        icon=PhosphorIcon.SHIELD_CHECK,
        width=22,
        height=15,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    ),
    xy=(20, 21),
)
svc = vpc.add(
    Node("Users Service", icon=PhosphorIcon.USERS, width=22, height=15, card_style=Styles.Neutral),
    xy=(58, 30),
)
db = vpc.add(
    Node("Primary DB", icon=PhosphorIcon.DATABASE, width=22, height=15, card_style=Styles.Neutral),
    xy=(58, 11),
)

sdk.connect(gw, label="HTTPS")
gw.connect(svc, label="gRPC")
svc.connect(db, label="SQL")

d.draw(xy=(0, 0))
save()
```

## Authentication

All requests to `/v1/*` endpoints must include a bearer API key in the `Authorization` HTTP header:

```http
Authorization: Bearer sk_live_98a7b6c5d4e3f2a1
Content-Type: application/json
```

| Header | Required | Description |
| :--- | :--- | :--- |
| `Authorization` | Yes | Format: `Bearer <api_key>`. Keys are scoped per environment (`sk_test_*` or `sk_live_*`). |
| `Idempotency-Key` | Optional | Unique UUIDv4 token for safe retries on `POST` and `PATCH` mutations (24-hour TTL). |
| `X-Request-Id` | Returned | Correlation identifier echoed on every response for distributed tracing. |

## Rate Limits & Errors

Standard rate limits apply per API key using a sliding token bucket:

| Tier | Requests / Minute | Burst Allowance | Retry Header |
| :--- | :--- | :--- | :--- |
| Standard | `600 req/min` | `100 req` | `Retry-After` (seconds) |
| Enterprise | `6,000 req/min` | `1,000 req` | `Retry-After` (seconds) |

Non-2xx responses return a structured JSON envelope documented in [SDK & Data Models](02_models.md#apierror). Explore the endpoint specifications in [Users API](01_users.md).
