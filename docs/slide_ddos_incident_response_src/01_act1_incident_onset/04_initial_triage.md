::: block (80, 40) (1760, 70)
# Initial Triage: Origin Clamping vs. Edge Filtering
:::

::: block (80, 130) (1760, 170)
- **Tactic A (`max-instances=1` + App Rate Limit)**: Caps runaway Cloud bill immediately, but **starves legitimate users (504 Gateway Timeout)** as bots fill the queue.
- **Tactic B (Dedicated Edge WAF Layer)**: Drops malicious floods at the **Anycast POP (403 Forbidden)** so only clean traffic reaches the Cloud Run container.
:::

::: block (80, 320) (1760, 630)
```drawlib
from drawlib.canvas import setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Colors, Styles

setup(width=176, height=63)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.5),
    lane_orientation="horizontal",
    width=172.0,
    height=59.0,
)

flow.add_lane("Tactic A:\nOrigin Clamp", height=29.5, header_size=26.0, text_style=Styles.DarkBold.patch(text_size=11.5))
flow.add_lane("Tactic B:\nEdge WAF", height=29.5, header_size=26.0, text_style=Styles.DarkBold.patch(text_size=11.5))

# Lane 1 (Top): Origin Clamping Failure
s1 = flow.add(
    Start("Bot Flood\n+ Real Users", width=26.0, height=14.0, style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(43.0, 44.5),
)
p1 = flow.add(
    Process("Cloud Run Ingress\n(max-instances = 1)", width=32.0, height=14.0, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(81.0, 44.5),
)
p2 = flow.add(
    Process("App-Level IP Limit\n(Shares 1 vCPU Pool)", width=32.0, height=14.0, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(121.0, 44.5),
)
e1 = flow.add(
    End("Queue Exhausted\n504 Outage!", width=27.0, height=14.0, style=Styles.AccentFlat, text_style=Styles.WhiteBold.patch(text_size=11.5)),
    xy=(157.5, 44.5),
)

s1.connect(p1)
p1.connect(p2)
p2.connect(e1, style=Styles.AccentBold)

# Lane 2 (Bottom): Anycast Edge WAF Filtering
s2 = flow.add(
    Start("Bot Flood\n+ Real Users", width=26.0, height=13.5, style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(43.0, 11.5),
)
d2 = flow.add(
    Decision("Anycast Edge\nWAF Check", width=29.0, height=12.5, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=11.5)),
    xy=(81.0, 11.5),
)
drop2 = flow.add(
    End("403 Edge Drop\n(0 Origin CPU)", width=28.0, height=11.5, style=Styles.SecondaryNeutral, text_style=Styles.AccentBold.patch(text_size=11.5)),
    xy=(125.0, 23.0),
)
ok2 = flow.add(
    End("200 OK Audio\n(100% Uptime)", width=28.0, height=11.5, style=Styles.PrimaryNeutral, text_style=Styles.PrimaryBold.patch(text_size=11.5)),
    xy=(157.5, 11.5),
)

s2.connect(d2)
d2.connect(
    drop2,
    label="Bot",
    start_side="top",
    end_side="left",
    style=Styles.AccentBold,
    text_style=Styles.AccentBold.patch(text_size=11.5, xy_shift=(14.0, 3.0)),
)
d2.connect(ok2, label="Human", start_side="right", end_side="left", style=Styles.PrimaryBold)

flow.draw(xy=(2.0, 2.0))
```
:::

::: block (1720, 995) (140, 30)
```drawlib
import utils
utils.draw_page_number()
```
:::

::: note
During the first hour of emergency triage, we implemented two stopgap measures directly on the Cloud Run service:
1. **Clamping `max-instances = 1`**: To stop the financial bleeding immediately, we restricted Cloud Run auto-scaling to a single container instance. While this guaranteed our compute bill could not exceed a single instance's cost, the botnet immediately saturated that single container's request queue, causing **504 Gateway Timeouts** for all legitimate users.
2. **In-App IP Rate Limiting**: Next, we added an in-memory per-IP rate limiter inside the Python application to return `429 Too Many Requests`. However, in a serverless environment without an upstream edge proxy, every `429` response still consumes Cloud Run ingress bandwidth, TLS termination overhead, and container request-handling threads.
- **Architectural Lesson**: You cannot mitigate a volumetric L7 flood inside the origin container. Malicious requests must be dropped at an upstream **Anycast Edge WAF** before they ever reach the origin.
:::
