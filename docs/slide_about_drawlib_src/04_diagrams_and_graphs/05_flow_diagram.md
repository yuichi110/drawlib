::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Workflows & Swimlanes (`FlowDiagram`)
:::

::: block (80, 140) (640, 840) compact
## ISO 5807 Flowcharts with Cross-Lane Coordinates

`FlowDiagram` models operational workflows, CI/CD release gates, and approval processes across organizational or system swimlanes:

### Standard Flowchart Node Classes
- **`Start` / `End`**: Rounded stadium/pill terminals (`r=5.0`).
- **`Process`**: Rectangular execution step (`24 x 12`).
- **`Decision`**: Diamond conditional gate (`22 x 14`) with explicit `start_side="right" | "bottom" | "left"` branch routing.
- **`Data`**: Slanted parallelogram for I/O artifacts or payloads (`24 x 12`).

### Unified Swimlane Coordinate System
- Call `flow.add_lane(name, width=...)` for vertical columns or set `lane_orientation="horizontal"` for horizontal rows.
- **Global Coordinate Plane**: All nodes share the exact same global `(x, y)` canvas space—so placing steps across different lanes at the same `y` coordinate guarantees horizontal alignment!
:::

::: block (760, 140) (1080, 840)
```drawlib file:flow_swimlanes.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

clear()
setup(width=108, height=84)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=7.5),
    title="Automated Canary Deployment & Rollback Gate",
    title_style=Styles.DarkBold.patch(text_size=9.5),
    width=100.0,
    height=74.0,
)

# 1. Define 3 vertical swimlanes (total width = 32 + 34 + 34 = 100)
flow.add_lane("CI Build Pipeline", width=32.0)
flow.add_lane("Canary Verifier", width=34.0)
flow.add_lane("Production Fleet", width=34.0)

# 2. Place nodes on shared global coordinate plane
# Lane 1 center X = 16.0 | Lane 2 center X = 49.0 | Lane 3 center X = 83.0
git_push = flow.add(
    Start("Git Tag Push", width=22.0, height=8.5, text_style=Styles.DarkBold.patch(text_size=7.8)),
    xy=(16.0, 58.0),
)
artifact = flow.add(
    Data(
        "Signed Container\nImage & SBOM",
        width=24.0,
        height=10.0,
        style=Styles.PrimaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=7.5),
    ),
    xy=(16.0, 41.0),
)

canary = flow.add(
    Process(
        "Deploy 5% Canary",
        width=25.0,
        height=10.0,
        style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=7.8),
    ),
    xy=(49.0, 41.0),
)
slo_gate = flow.add(
    Decision(
        "p99 < 50ms &\nErr < 0.1%?",
        width=26.0,
        height=13.5,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=7.2),
    ),
    xy=(49.0, 21.0),
)

rollback = flow.add(
    Process(
        "Auto-Rollback &\nPage On-Call",
        width=24.0,
        height=10.0,
        style=Styles.WarningNeutral,
        text_style=Styles.DarkBold.patch(text_size=7.5),
    ),
    xy=(16.0, 21.0),
)
promote = flow.add(
    Process(
        "Promote 100%\nGlobal Traffic",
        width=25.0,
        height=10.0,
        style=Styles.TealNeutral,
        text_style=Styles.DarkBold.patch(text_size=7.8),
    ),
    xy=(83.0, 21.0),
)
done = flow.add(
    End("Release Live", width=22.0, height=8.5, text_style=Styles.DarkBold.patch(text_size=7.8)),
    xy=(83.0, 7.0),
)

# 3. Connect workflow edges
git_push.connect(artifact)
artifact.connect(canary)
canary.connect(slo_gate)

slo_gate.connect(rollback, label="No (Breach)", start_side="left", end_side="right")
slo_gate.connect(promote, label="Yes (Healthy)", start_side="right", end_side="left")
promote.connect(done, start_side="bottom", end_side="top")

flow.draw(xy=(4.0, 5.0))

save()
```
:::

::: note
- This slide demonstrates `FlowDiagram` modeling an automated canary deployment and rollback workflow across three vertical swimlanes: `CI Build Pipeline`, `Canary Verifier`, and `Production Fleet`.
- Notice how all five ISO 5807 symbol types (`Start`, `Data`, `Process`, `Decision`, and `End`) are used with semantic styling:
  - `Deploy 5% Canary` is highlighted in `Styles.PrimaryFlat` as the hero action.
  - `p99 < 50ms & Err < 0.1%?` uses a `Decision` diamond (`Styles.SecondaryNeutral`) that routes left to `Auto-Rollback` (`Styles.WarningNeutral`) on failure or right to `Promote 100% Global Traffic` (`Styles.TealNeutral`) on success.
  - Because `rollback`, `slo_gate`, and `promote` all share `y=21.0`, the horizontal decision branches across all three swimlanes are perfectly level.
:::
