::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# Pipelines & Feedback Loops (`ChevronProcess` & `Cycle`)
:::

::: block (80, 140) (720, 840) compact
## Linear Stages vs. Continuous Iterations

### 1. `ChevronProcess` — Phased Pipelines
- **Interlocking Geometry**: Automatically computes chevron tip angles (`corner_angle=60.0`) and uniform item widths across total `width`.
- **Clean Entry Edge**: `flat_left_end=True` renders the first stage as a flat-backed pentagon while subsequent stages interlock seamlessly.
- **Dual-Line Labels**: Each stage supports a primary `text` heading and a secondary `description` subtitle with independent style overrides.

### 2. `Cycle` — Circular & Radial Workflows
- **Trigonometric Orbit**: Distributes `N` nodes (`"circle"`, `"rectangle"`, or `"none"`) evenly around orbit `radius` starting from `start_angle=90.0` (12 o'clock).
- **Curved Arc Connectors**: Connects steps with circular arc arrows (`arrow_type="arc"`) and configurable `arrow_color_mode` (`"monochrome"`, `"match_source"`, `"match_target"`).
- **Central Command Hub**: Calling `cycle.set_center(...)` places a central hub node inside the orbit for radial governance or SRE command loops.
:::

::: block (840, 140) (1000, 840)
```drawlib file:process_and_cycle.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess, Cycle
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=100, height=84)

# Top Panel: 5-Stage CI/CD ChevronProcess
rectangle((50, 70), width=96, height=24, r=2.0, style=Styles.NeutralFlat)
text(
    (6, 78.5),
    "Cloud CI/CD Release Pipeline — ChevronProcess(flat_left_end=True)",
    style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"),
)

pipeline = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=8.5),
    description_style=Styles.Muted.patch(text_size=7.2),
    corner_angle=60.0,
    spacing=1.6,
    flat_left_end=True,
)
pipeline.add("1. Commit", description="Lint & Hooks")
pipeline.add("2. Build", description="Container Image", style=Styles.PrimaryNeutral)
pipeline.add(
    "3. Security Gate",
    description="SAST & SBOM",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=8.5),
    description_style=Styles.White.patch(text_size=7.2),
)
pipeline.add("4. Canary", description="5% Traffic", style=Styles.SecondaryNeutral)
pipeline.add("5. Production", description="Global Rollout", style=Styles.TealNeutral)
pipeline.draw(xy=(6, 60.5), width=88.0, height=13.5)

# Bottom Panel: SRE Incident Response Cycle with set_center()
rectangle((50, 29), width=96, height=52, r=2.0, style=Styles.MutedOutline)
text(
    (6, 51.5),
    "SRE Incident Response Loop — Cycle() + set_center()",
    style=Styles.DarkBold.patch(text_size=9.5, text_halign="left"),
)

incident_cycle = Cycle(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=7.8),
    description_style=Styles.Muted.patch(text_size=6.3),
    arrow_style=Styles.DarkBold,
    clockwise=True,
    start_angle=90.0,
    node_shape="circle",
    node_radius=6.0,
    arrow_type="arc",
    arrow_width=1.3,
    arrow_head_width=3.2,
    arrow_color_mode="monochrome",
    description_placement="inside",
)
incident_cycle.add(
    "1. Detect",
    description="SLO Alert",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=7.8),
    description_style=Styles.White.patch(text_size=6.3),
)
incident_cycle.add("2. Triage", description="Blast Radius", style=Styles.PrimaryNeutral)
incident_cycle.add("3. Mitigate", description="Rollback/Drain", style=Styles.SecondaryNeutral)
incident_cycle.add("4. Resolve", description="Root Patch", style=Styles.BlueNeutral)
incident_cycle.add("5. Postmortem", description="Blameless RCA", style=Styles.Neutral)

incident_cycle.set_center(
    text="SRE",
    description="On-Call Hub",
    radius=7.2,
    style=Styles.AccentFlat,
    text_style=Styles.WhiteBold.patch(text_size=9.5),
    description_style=Styles.White.patch(text_size=6.5),
)
incident_cycle.draw(xy=(34, 24.5), radius=16.2, align="center")

# Right callout summary inside bottom panel
rectangle((77, 26.5), width=32, height=34, r=1.5, style=Styles.Neutral)
text((64, 39.5), "Cycle Highlights:", style=Styles.DarkBold.patch(text_size=8.5, text_halign="left"))
text((64, 34.0), "• Auto-distributed angles", style=Styles.Dark.patch(text_size=7.8, text_halign="left"))
text((64, 29.0), "• Curved arc connectors", style=Styles.Dark.patch(text_size=7.8, text_halign="left"))
text((64, 24.0), "• Center hub via set_center()", style=Styles.Dark.patch(text_size=7.8, text_halign="left"))
text((64, 19.0), "• Per-node show=True/False", style=Styles.Dark.patch(text_size=7.8, text_halign="left"))
text((64, 14.0), "• 50%+ neutral grounding", style=Styles.Dark.patch(text_size=7.8, text_halign="left"))

save()
```
:::

::: note
- This slide showcases two of the most frequently used process components in `drawlib.smartarts`: `ChevronProcess` and `Cycle`.
- In the top panel, `ChevronProcess` renders a 5-stage CI/CD pipeline with `flat_left_end=True`. Notice how Stage 3 ("Security Gate") uses `Styles.PrimaryFlat` with `Styles.WhiteBold` text as the primary focal point, while the remaining 80% of stages use calm neutral and tinted-neutral styles (`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`, `Styles.TealNeutral`).
- In the bottom panel, `Cycle` renders a 5-step SRE Incident Response loop around a central `set_center("SRE", description="On-Call Hub")` node. Drawlib automatically computes the 72-degree angular intervals and trims the circular arc arrows (`arrow_gap`) so arrowheads never collide with node borders.
:::
