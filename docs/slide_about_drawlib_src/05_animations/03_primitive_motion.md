::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils
utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Animating Primitives & Packet Traffic
:::

::: block (80, 140) (740, 840) font:20px
## Coordinate & Color Interpolation

By computing coordinates `(x, y)` or interpolating colors via `get_intermediate_colors()` across frames, primitive shapes illustrate live request flows, heartbeats, and state transitions.

```python
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.shapes import circle, rectangle
from drawlib.styles import Styles

clear()
setup(width=98, height=84)
anim = Animation(fps=8.0, loop=0)

# Interpolate packet X across 4 microservice hops
hops = [(16, "Client"), (38, "API Gateway"),
        (60, "Worker Pool"), (82, "Database")]

for pkt_x, active_hop in packet_schedule:
    with anim.frame(duration=0.14):
        # Redraw static topology + active node highlight
        # Draw traveling request packet at (pkt_x, 46)
        circle((pkt_x, 46), radius=2.2, style=Styles.AccentFlat)
```

### Best Practices for Motion Loops
- **Hoist Invariant Coordinates**: Calculate node anchors and packet waypoints before entering the frame loop.
- **Highlight Active Receiver**: Use `Styles.PrimaryFlat` on the node currently processing the request while keeping idle nodes in `Styles.Neutral`.
- **Smooth Color Fades**: Use `get_intermediate_colors(c1, c2, num=3, include_ends=True)` for gradual heatmaps or status transitions.
:::

::: block (860, 140) (980, 840)
```drawlib file:packet_flow_anim.png anim:auto
from drawlib.anim import Animation
from drawlib.canvas import clear, save, setup
from drawlib.lines import line
from drawlib.shapes import circle, cylinder, rectangle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=98, height=84)
anim = Animation(fps=8.0, loop=0)

nodes = [
    (15.0, "Client\nApp", "neutral"),
    (38.0, "API\nGateway", "primary"),
    (61.0, "Worker\nPool", "neutral"),
    (83.0, "Primary\nDB", "db"),
]

# 10-frame schedule: (packet_x, active_node_idx, status_text, frame_duration)
schedule = [
    (15.0, 0, "1. Client dispatches HTTPS POST /orders", 0.25),
    (26.5, 0, "1. Packet in transit -> API Gateway (TLS 1.3)", 0.14),
    (38.0, 1, "2. API Gateway authenticates JWT & rate-limits", 0.25),
    (49.5, 1, "2. Forwarding gRPC payload -> Worker Pool", 0.14),
    (61.0, 2, "3. Worker Pool validates inventory & pricing", 0.25),
    (72.0, 2, "3. Executing transactional INSERT -> Primary DB", 0.14),
    (83.0, 3, "4. Primary DB commits WAL & returns ACK", 0.30),
    (61.0, 2, "5. Worker Pool emits OrderCreated event", 0.16),
    (38.0, 1, "6. API Gateway serializes 201 Created response", 0.16),
    (15.0, 0, "7. Client receives 201 Created (14.2 ms E2E)", 1.80),
]

for step_idx, (pkt_x, active_idx, status_msg, dt) in enumerate(schedule):
    with anim.frame(duration=dt):
        # Outer card & title
        rectangle((49, 42), width=94, height=78, r=2.5, style=Styles.Neutral)
        text((49, 73), "Live Microservice Request & ACK Packet Flow", style=Styles.DarkBold.patch(text_size=12.0))

        # VPC Container around Gateway, Worker, DB
        rectangle((60.5, 45), width=62, height=34, r=2.0, style=Styles.PrimaryNeutral)
        text((32.5, 58.5), "Production VPC (10.0.0.0/16)", style=Styles.MutedBold.patch(text_size=8.5, text_halign="left"))

        # Connectors between hops
        for i in range(len(nodes) - 1):
            x1 = nodes[i][0] + 8.0
            x2 = nodes[i + 1][0] - 8.0
            line((x1, 43), (x2, 43), arrow_head="<->", style=Styles.DarkBold)

        # Draw 4 service nodes
        for i, (nx, label, kind) in enumerate(nodes):
            is_active = i == active_idx
            n_style = Styles.PrimaryFlat if is_active else (Styles.SecondaryNeutral if kind == "db" else Styles.White)
            t_style = Styles.WhiteBold.patch(text_size=9.5) if is_active else Styles.DarkBold.patch(text_size=9.5)
            if kind == "db":
                cylinder((nx, 43), width=15, height=16, style=n_style, text=label, text_style=t_style)
            else:
                rectangle((nx, 43), width=16, height=16, r=2.0, style=n_style, text=label, text_style=t_style)

        # Draw traveling packet badge
        is_return = step_idx >= 7
        pkt_style = Styles.SecondaryFlat if is_return else Styles.AccentFlat
        circle((pkt_x, 43), radius=2.6, style=pkt_style)
        rectangle(
            (pkt_x, 54.0),
            width=12.0,
            height=4.2,
            r=1.0,
            style=pkt_style,
            text="ACK" if is_return else "REQ",
            text_style=Styles.WhiteBold.patch(text_size=7.5),
        )

        # Status telemetry bar at bottom
        rectangle(
            (49, 14.5),
            width=84,
            height=9.0,
            r=1.5,
            style=Styles.White,
            text=f"[Frame {step_idx + 1}/10]  {status_msg}",
            text_style=Styles.DarkBold.patch(text_size=9.5),
        )

save()
```
:::

::: block (80, 1010) (820, 30) font:14px
*Chapter 5: Multi-Frame Animations — Animating Primitives & Packet Traffic*
:::

::: note
- Here we see an actual 10-frame APNG animation running automatically on the slide (`anim:auto`).
- Notice how the request packet (`REQ` in Amber) travels left-to-right from the Client through the API Gateway and Worker Pool to the Primary DB, and then returns (`ACK` in Green) while the active node highlights in Indigo (`Styles.PrimaryFlat`).
:::
