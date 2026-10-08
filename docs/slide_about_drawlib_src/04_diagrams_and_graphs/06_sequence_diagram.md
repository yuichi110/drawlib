::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# API Interactions & Lifelines (`SequenceDiagram`)
:::

::: block (80, 140) (640, 840) compact
## Chronological Protocols & Python Context Managers

`SequenceDiagram` turns protocol specifications into clean lifeline diagrams without manual Y-coordinate bookkeeping:

### Expressive Python Idioms
- **Participants & Groups**:
  - `d.add(Participant((18, 13), "Name", icon=GcpIcon.CLOUD_RUN))`
  - `vpc = d.add(ParticipantGroup(title="Zero-Trust Mesh", style=Styles.MutedDashed))`
- **Message Verbs (`autonumber=True`)**:
  - `a.request(b, "label")`: Solid synchronous call arrow (`―▶`).
  - `b.reply(a, "label")`: Dashed return arrow (`---▶`).
  - `is_async=True`: Open stick arrowhead (`―>`) for Pub/Sub or async events.
- **Execution & Annotations**:
  - `p.activate()` / `p.deactivate()` for lifeline execution bars.
  - `p.note("...", pos="right")` or `d.note("...", over=[p1, p2])` for sticky notes.
- **Python `with` Condition Frames**:
  - `with d.alt("Token Valid"): ... with d.else_("Expired"): ...`
  - `with d.loop("Retry"): ...`, `with d.opt(...):`, `with d.par(...):`
:::

::: block (760, 140) (1080, 840)
```drawlib file:sequence_oauth.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.sequence import (
    GcpIcon,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=7.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=6.8),
    node_card_style=Styles.Neutral,
    title="OAuth2 / JWT Microservice Request & Token Refresh Flow",
    title_style=Styles.DarkBold.patch(text_size=9.2),
    autonumber=True,
    col_width=24.0,
    step_y=6.2,
)

# 1. Participants & Mesh Group
client = d.add(Participant((18, 13), "SPA Client", icon=PhosphorIcon.BROWSER, icon_size=6.0))

mesh = d.add(
    ParticipantGroup(
        title="Internal Zero-Trust Service Mesh",
        padding=2.8,
        style=Styles.MutedDashed,
    )
)
gateway = mesh.add(
    Participant(
        (18, 13),
        "API Gateway",
        icon=GcpIcon.CLOUD_RUN,
        icon_size=6.0,
        card_style=Styles.PrimaryNeutral,
    )
)
auth = mesh.add(
    Participant(
        (18, 13),
        "Auth / JWKS",
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=6.0,
        card_style=Styles.SecondaryNeutral,
    )
)
orders = mesh.add(
    Participant(
        (18, 13),
        "Order Service",
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=6.0,
        card_style=Styles.Neutral,
    )
)

# 2. Chronological Message Exchange
client.request(gateway, "GET /v1/orders (Bearer JWT)")
gateway.activate()

gateway.request(auth, "Verify Signature & Claims")
auth.reply(gateway, "Claims Valid (sub=user_42)")

with d.loop("Up to 2 Retries on Transient Timeout"):
    gateway.request(orders, "FetchOrders(user_id=42)")
    orders.reply(gateway, "200 OK (Order Payload)")

gateway.note("Audit log emitted asynchronously", pos="right")
gateway.reply(client, "200 OK (JSON Response)")
gateway.deactivate()

d.draw(xy=(4.0, 2.0))

save()
```
:::

::: note
- This slide showcases `SequenceDiagram` modeling an OAuth2 / JWT microservice call flow with `autonumber=True`.
- Notice how Python's `with d.loop("Up to 2 Retries on Transient Timeout"):` context manager naturally scopes the retry frame around the `FetchOrders` request and reply!
- `ParticipantGroup(title="Internal Zero-Trust Service Mesh")` draws a dashed boundary enclosing `API Gateway`, `Auth / JWKS`, and `Order Service`, while `gateway.activate()` and `gateway.deactivate()` render the vertical execution bar along the gateway's lifeline.
:::
