# SequenceDiagram: Lifelines, Synchronous Calls & Condition Blocks

`SequenceDiagram` models chronological interactions and communication protocols between collaborating participants over time. Time progresses strictly downwards along vertical lifelines, with horizontal arrows representing messages.

---

## 1. Overview & Key Concepts

```text
    Client               API Server            Database
      │                      │                    │
      │ ──POST /login───────►│                    │
      │                      │ ──SELECT user─────►│
      │                      │                    │ █ (Activation)
      │                      │ ◄──User Record─────│
      │ ◄──200 OK (JWT)──────│                    │
      │                      │                    │
```

- **Vertical Lifelines**: Participants are placed along the horizontal header band, with lifelines extending downwards.
- **Message Semantics**:
  - `request()`: Solid line with filled arrow (`―▶`). With `is_async=True`, renders an open arrow (`―>`).
  - `reply()`: Dashed line with filled arrow (`---▶`).
  - `connect()`: Bidirectional communication (`<->`), such as full-duplex WebSocket channels.
  - Self-Calls: `p.request(p, label)` loops back to the caller's own lifeline.
- **Activation Boxes**: `p.activate()` and `p.deactivate()` draw execution focus rectangles along lifelines.
- **Autonumbering**: Setting `autonumber=True` automatically numbers messages sequentially (`1.`, `2.`, `3.`, ...).
- **Pythonic Condition Frames (`with`)**: Use Python context managers (`with d.loop()`, `with d.alt()`, `with d.opt()`) to wrap structured interaction frames cleanly.

---

## 2. Constructor & Participant Management

```python
from drawlib.diagrams.sequence import (
    Block,
    GcpIcon,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)

d = SequenceDiagram(
    title="Checkout Transaction Pipeline",
    autonumber=True,            # Auto-number messages (1., 2., 3., ...)
)

# Participant group for clustered backend services
vpc = d.add_group(ParticipantGroup(title="Google Cloud VPC", padding=4.0))
api = vpc.add(Participant("Cloud Run\n(Gateway)", icon=GcpIcon.CLOUD_RUN))
db = vpc.add(Participant("Cloud SQL", icon=GcpIcon.CLOUD_SQL))

# External participant
client = d.add(Participant("Web Browser", icon=PhosphorIcon.BROWSER))
```

---

## 3. Distributed Transaction Pipeline

The following complete example showcases participant groups, cloud icons, activations, sticky notes, asynchronous dispatches, and a retry loop frame:

```drawlib 650px center caption:"Microservices Distributed Transaction Pipeline"
from drawlib import canvas
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=115, height=135)

d = SequenceDiagram(title="Microservices Distributed Transaction Pipeline", autonumber=True)

# 1. Clustered Backend Participant Group
backend = d.add_group(
    ParticipantGroup(
        title="Google Cloud VPC",
        padding=4.0,
        style=Styles.muted_dashed,
    )
)
api = backend.add(Participant("Cloud Run\n(Gateway)", icon=GcpIcon.CLOUD_RUN, icon_size=8.0))
worker = backend.add(Participant("GKE Pod\n(Worker)", icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=8.0))
db = backend.add(Participant("Cloud SQL\n(Database)", icon=GcpIcon.CLOUD_SQL, icon_size=8.0))

client = d.add(Participant("Web Browser", icon=PhosphorIcon.BROWSER, icon_size=8.0))

# 2. Client Initiates Checkout Request
client.request(api, "POST /api/v1/checkout")
api.activate()

# 3. Inventory Validation
api.request(db, "Check Inventory")
db.reply(api, "Stock Available")

# 4. Sticky Note Annotation
api.note("Dispatching background fulfillment job", pos="right")

# 5. Asynchronous Worker Dispatch
api.request(worker, "Enqueue Job (Pub/Sub)", is_async=True)
worker.reply(api, "Ack", is_async=True)

# 6. Immediate Response to Client
api.reply(client, "202 Accepted (Order ID)")
api.deactivate()

# 7. Background Processing Retry Loop
with d.loop("Retry up to 3 times on DB lock"):
    worker.request(db, "Deduct Inventory Rows")
    db.reply(worker, "Rows Committed")

d.draw(xy=(5.0, 5.0))
```

---

## 4. WebSocket Full-Duplex Streaming

For real-time bidirectional streams, use `connect()` with `arrow="<->"`:

```drawlib 650px center caption:"WebSocket Full-Duplex Telemetry Stream"
from drawlib import canvas
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram

canvas.clear()
canvas.setup(width=65, height=80)

d = SequenceDiagram(title="WebSocket Real-Time Live Sync")

app = d.add(Participant("Mobile App", icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.5))
gateway = d.add(Participant("WS Gateway", icon=PhosphorIcon.CLOUD, icon_size=7.5))

app.request(gateway, "GET /ws HTTP/1.1 (Upgrade: websocket)")
gateway.reply(app, "101 Switching Protocols")

# Bidirectional streaming channel
app.connect(gateway, "Full-Duplex JSON Stream", arrow="<->")

with d.loop("Every 500ms Ping Interval"):
    gateway.request(app, "PING", is_async=True)
    app.reply(gateway, "PONG", is_async=True)

d.draw(xy=(5.0, 5.0))
```

---

## 5. Condition Frames & Structured Blocks

Drawlib supports standard UML interaction operators using clean Python context managers:

| Frame Type | Syntax | Standard UML Operator |
|---|---|---|
| **Loop** | `with d.loop("condition"):` | `loop` |
| **Alternative** | `with d.alt("condition"):`<br>`with d.else_("condition"):` | `alt` / `else` |
| **Option** | `with d.opt("condition"):` | `opt` |
| **Parallel** | `with d.par("description"):` | `par` |

Frames automatically compute their enclosing bounding box around all enclosed message lines and draw the standard UML frame tag in the top-left corner.
