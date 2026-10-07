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
from drawlib.styles import Styles

d = SequenceDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    title="Checkout Transaction Pipeline",
    autonumber=True,            # Auto-number messages (1., 2., 3., ...)
)

# Participant group for clustered backend services
vpc = d.add(ParticipantGroup(title="Google Cloud VPC", padding=4.0))
api = vpc.add(Participant("Cloud Run\n(Gateway)", icon=GcpIcon.CLOUD_RUN, style=Styles.PrimaryNeutral))
db = vpc.add(Participant("Cloud SQL", icon=GcpIcon.CLOUD_SQL))

# External participant
client = d.add(Participant("Web Browser", icon=PhosphorIcon.BROWSER))
```

### Registration, Message & Rendering Methods
- **`d.add(item, *, show: bool = True) -> Participant | ParticipantGroup`** (and `group.add(participant, *, show: bool = True) -> Participant`): Registers a participant or group (`show=False` hides the lifeline/group and any attached messages while keeping horizontal column spacing fixed).
- **`a.request(b, label="", is_async=False, show: bool = True) -> Message`**, **`b.reply(a, label="", is_async=False, show: bool = True) -> Message`**, **`a.connect(b, label="", arrow="<->", show: bool = True) -> Message`**: Records a chronological message step and returns a mutable `Message` instance (`msg.show`, `msg.style`, `msg.draw_ratio`, `msg.draw_direction`). Hidden messages (`show=False`) keep their vertical `step_y` row reserved.
- **`p.note(text, pos="left"|"right", show: bool = True) -> Note`** and **`d.note(text, over=[p1, p2], show: bool = True) -> Note`**: Attaches a sticky note and returns a mutable `Note` instance.
- **`with d.loop(cond, show=True) as blk:`** (also `alt`, `opt`, `par`): Yields a mutable `Block` instance (`blk.show`, `blk.style`).
- **`d.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the sequence diagram at `xy`, proportionally scaling column widths, vertical steps, icons, and typography by `scale`.

---

## 3. Distributed Transaction Pipeline

The following complete example showcases participant groups, cloud icons, activations, sticky notes, asynchronous dispatches, and a retry loop frame:



<figure class="drawlib-image" style="text-align: center;">
  <img src="sequence_images/sequence_distributed_transaction.png" alt="sequence_1" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">Microservices Distributed Transaction Pipeline</figcaption>
</figure>



---

## 4. WebSocket Full-Duplex Streaming

For real-time bidirectional streams, use `connect()` with `arrow="<->"`:



<figure class="drawlib-image" style="text-align: center;">
  <img src="sequence_images/sequence_websocket_telemetry.png" alt="sequence_2" style="width: 650px; max-width: 100%;" />
  <figcaption class="drawlib-caption">WebSocket Full-Duplex Telemetry Stream</figcaption>
</figure>



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
