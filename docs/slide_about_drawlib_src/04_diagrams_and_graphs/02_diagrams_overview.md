::: block (1700, 1010) (140, 30)
```drawlib file:page.svg
import utils

utils.draw_page_number()
```
:::

::: block (80, 40) (1760, 60)
# The 6 Domain Diagram Engines (`drawlib.diagrams`)
:::

::: block (80, 140) (680, 840) compact
## Purpose-Built Engines with Shared Architecture

Unlike black-box text-to-diagram tools (PlantUML, Mermaid) that scramble your layout whenever a label changes, `drawlib.diagrams` combines **deterministic coordinate placement** with **intelligent boundary & wire automation**:

### 4 Shared Architectural Guarantees
1. **Center & Icon Coordinate Anchoring**: Passing `xy=(x, y)` to `d.add(...)` anchors the exact geometric center of the card or icon—ensuring aligned nodes always connect with perfectly straight horizontal or vertical wires.
2. **Universal `Connectable` Protocol**: Nodes, groups, entities, classes, states, and `Junction` waypoints share dynamic boundary clipping, `start_side`/`end_side` port selection, and smart `"orthogonal"` / `"direct"` / curved `bend` routing.
3. **Layout-Preserving `show=True/False`**: Hiding any node (`node.show = False`) automatically hides its connected edges and dangling `fork()` stems while **keeping `NodeGroup` bounds, swimlanes, and lifeline spacing 100% locked**.
4. **Uniform `draw(xy, scale=1.0)`**: Scales the entire diagram proportionally around bottom-left `xy`.
:::

::: block (800, 140) (1040, 840)
```drawlib file:diagrams_taxonomy.svg
from drawlib.canvas import clear, save, setup
from drawlib.shapes import rectangle
from drawlib.smartarts import GridLayout
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=84)

# Outer taxonomy frame
rectangle((52, 42), width=100, height=80, r=2.0, style=Styles.MutedOutline)
text(
    (6, 77.5),
    "drawlib.diagrams — 6 Specialized Software Engineering Engines",
    style=Styles.DarkBold.patch(text_size=9.8, halign="left"),
)

# 3 Columns x 2 Rows Matrix of the 6 Engines
cards = [
    # Top Row (y = 54)
    (
        20.0,
        54.0,
        "1. ArchitectureDiagram",
        "System & Cloud Topology",
        "• Official GcpIcon & PhosphorIcon\n• Auto-bounding NodeGroup\n• 1-to-N node.fork() bus fan-out\n• Icon-centric wire alignment",
        Styles.PrimaryFlat,
        Styles.PrimaryNeutral,
    ),
    (
        52.0,
        54.0,
        "2. FlowDiagram",
        "Workflows & Swimlanes",
        "• ISO 5807 Start/Process/Decision\n• Vertical & horizontal add_lane()\n• Shared global coordinate plane\n• Orthogonal L/Z-bend routing",
        Styles.SecondaryFlat,
        Styles.SecondaryNeutral,
    ),
    (
        84.0,
        54.0,
        "3. SequenceDiagram",
        "API Lifelines & Frames",
        "• Sync request() & dashed reply()\n• ParticipantGroup boundaries\n• Python 'with' loop/alt/opt/par\n• Activation bars & sticky notes",
        Styles.AccentFlat,
        Styles.BlueNeutral,
    ),
    # Bottom Row (y = 22)
    (
        20.0,
        22.0,
        "4. ERDiagram",
        "Relational Schemas",
        "• IE / Crow's Foot cardinalities\n• PK / FK / NOT NULL badges\n• Row-exact start_column anchor\n• Auto-height entity tables",
        Styles.PrimaryFlat,
        Styles.Neutral,
    ),
    (
        52.0,
        22.0,
        "5. ClassDiagram",
        "UML 2.0 OOP Models",
        "• 3-compartment ClassNode cards\n• «interface» & «abstract» headers\n• 6 UML relationship connectors\n• Multiplicity & role labels",
        Styles.SecondaryFlat,
        Styles.Neutral,
    ),
    (
        84.0,
        22.0,
        "6. StateDiagram",
        "FSM & Statecharts",
        "• Initial, Final, Choice & ForkJoin\n• entry / do / exit compartments\n• event [guard] / action labels\n• Curved bidirectional bend arcs",
        Styles.AccentFlat,
        Styles.Neutral,
    ),
]

for cx, cy, title_str, sub_str, bullets, hdr_style, body_style in cards:
    # Card body
    rectangle((cx, cy), width=29.0, height=27.0, r=1.8, style=body_style)
    # Header banner
    rectangle(
        (cx, cy + 10.0),
        width=29.0,
        height=7.0,
        r=1.5,
        style=hdr_style,
        text=title_str,
        text_style=Styles.WhiteBold.patch(text_size=7.6),
    )
    # Subtitle badge
    text(
        (cx, cy + 4.2),
        sub_str,
        style=Styles.DarkBold.patch(text_size=7.2),
    )
    # Bullet lines
    for idx, line_str in enumerate(bullets.split("\n")):
        text(
            (cx - 13.0, cy + 0.5 - idx * 3.4),
            line_str,
            style=Styles.Dark.patch(text_size=6.5, halign="left"),
        )

save()
```
:::

::: note
- `drawlib.diagrams` provides 6 specialized domain diagram engines organized into three families:
  1. **System & Architecture**: `ArchitectureDiagram` for cloud infrastructure, VPCs, and microservice meshes.
  2. **Behavior & Process**: `FlowDiagram` (ISO 5807 flowcharts with cross-functional swimlanes), `SequenceDiagram` (chronological lifelines and `with` condition frames), and `StateDiagram` (UML statecharts and FSMs).
  3. **Structural & Data Models**: `ERDiagram` (Crow's Foot database schemas with column-level anchoring) and `ClassDiagram` (UML 2.0 3-compartment class models).
- All 6 engines share the `Connectable` routing engine, `show=True/False` layout-preserving visibility for animations, and `draw(xy, scale=1.0)`.
:::
