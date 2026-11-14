# 10. Software Design Diagrams: Sequence, Flow, State, Class & ER

Beyond cloud infrastructure topologies (`ArchitectureDiagram`), `drawlib.diagrams` provides five specialized software engineering engines—`SequenceDiagram`, `FlowDiagram`, `StateDiagram`, `ClassDiagram`, and `ERDiagram`—that render standard UML 2.x, ISO 5807, and Crow's Foot models directly from declarative Python code.

```drawlib align=center code=fold file=sequence_auth_flow.png caption="Figure 10.1: OAuth 2.0 & Token Verification RPC Sequence with ParticipantGroup, Activations, and Alt/Else Frame"
import math
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import (
    GcpIcon,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)
from drawlib.styles import Styles

d = SequenceDiagram(
    node_style=Styles.DarkBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    autonumber=True,
    col_width=36.0,
    step_y=5.6,
    margin=4.0,
)

client = d.add(
    Participant(
        "Client App",
        width=24.0,
        height=12.5,
        icon=PhosphorIcon.DEVICES,
        icon_size=5.0,
        card_style=Styles.Neutral,
    )
)

platform = d.add(
    ParticipantGroup(
        title="Core Auth & API Platform",
        padding=4.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="bottom"),
    )
)
gateway = platform.add(
    Participant(
        "API Gateway",
        width=26.0,
        height=12.5,
        icon=PhosphorIcon.CLOUD_CHECK,
        icon_size=5.0,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
auth = platform.add(
    Participant(
        "Auth Service",
        width=26.0,
        height=12.5,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=5.0,
        card_style=Styles.White,
    )
)
store = platform.add(
    Participant(
        "Session Cache",
        width=26.0,
        height=12.5,
        icon=GcpIcon.MEMORYSTORE,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral,
    )
)

client.request(gateway, "POST /v1/orders (Bearer JWT)")
gateway.activate()
gateway.request(auth, "VerifySignature(jwt)")
auth.activate()
auth.request(store, "GET session:jti")
store.reply(auth, "Session Claims")

with d.alt("") as alt_blk:
    alt_blk.style = Styles.MutedDashed
    alt_blk.text_style = Styles.DarkBold.patch(text_size=10.0)
    auth.reply(gateway, "200 Verified Claims", style=Styles.SuccessBold)
    gateway.request(store, "XADD audit_stream", is_async=True, style=Styles.SecondaryBold)
    gateway.reply(client, "200 OK (Order Accepted)", style=Styles.SuccessBold)
    d.note("Cached 300s", over=[gateway, auth], style=Styles.PrimaryNeutral.patch(text_size=10.0))

d.space(2.0)
with d.else_("") as else_blk:
    else_blk.style = Styles.MutedDashed
    else_blk.text_style = Styles.DarkBold.patch(text_size=10.0)
    auth.reply(
        gateway,
        "401 Invalid Token",
        style=Styles.DangerBold,
        text_style=Styles.DangerBold.patch(text_size=10.0),
    )
    gateway.reply(
        client,
        "401 Unauthorized",
        style=Styles.DangerBold,
        text_style=Styles.DangerBold.patch(text_size=10.0),
    )

auth.deactivate()
gateway.deactivate()

w, h = d.get_size()
setup(width=math.ceil(w) + 8, height=math.ceil(h) + 8)
d.draw(xy=(4.0, 4.0))
save()
```

---

## 10.1 Overview of the Five Software Modeling Engines

Each diagram engine in `drawlib.diagrams` shares a consistent builder lifecycle: configure base styles on the diagram constructor, register domain elements via `.add()`, connect them semantically, query `.get_size()` when exact bounding dimensions are needed, and render onto the canvas with `.draw(xy=(x0, y0))` (bottom-left anchored by default).

| Module | Primary Class | Core Elements | Coordinate Strategy | Primary Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| `drawlib.diagrams.sequence` | `SequenceDiagram` | `Participant`, `ParticipantGroup`, `Message`, `Note`, `Block` | Auto-advances `col_width` (X) and `step_y` (Y) | RPC/REST call timelines, OAuth handshakes, async messaging |
| `drawlib.diagrams.flow` | `FlowDiagram` | `Start`, `End`, `Process`, `Decision`, `Data`, `Lane`, `Junction` | Center `xy=(cx, cy)` across shared global/swimlane space | CI/CD gates, business workflows, cross-team swimlanes |
| `drawlib.diagrams.state` | `StateDiagram` | `State`, `InitialState`, `FinalState`, `ChoiceState`, `ForkJoinState` | Center `xy=(cx, cy)` with curved/orthogonal transitions | Protocol FSMs, worker lifecycles, concurrent statecharts |
| `drawlib.diagrams.class_diagram` | `ClassDiagram` | `ClassNode`, `AttributeInfo`, `MethodInfo`, `ClassRelationship` | Center `xy=(cx, cy)` with auto-sized 3-compartment boxes | OOP domain models, interface contracts, package hierarchies |
| `drawlib.diagrams.er` | `ERDiagram` | `Entity`, `ColumnInfo`, `Relationship` | Center `xy=(cx, cy)` with row-accurate `start_column` / `end_column` | Relational SQL schemas, PK/FK constraints, Crow's Foot models |

---

## 10.2 API Interactions with SequenceDiagram

`SequenceDiagram` (`from drawlib.diagrams.sequence import SequenceDiagram, Participant, ParticipantGroup`) eliminates manual vertical coordinate math for chronological protocols:

- **Participants, Groups & Icons**: Register endpoints left-to-right with `d.add(Participant(...))` or group backend services inside `ParticipantGroup(title=..., padding=4.0)`. All 33 icon enums (`PhosphorIcon`, `GcpIcon`, `AwsIcon`, `AzureIcon`, etc.) are re-exported directly from `drawlib.diagrams.sequence`.
- **Sync, Async & Return Messages**: Call `a.request(b, "label")` for solid synchronous calls, pass `is_async=True` for open-arrow asynchronous events, call `b.reply(a, "label")` for dashed return arrows, or call `a.request(a, "Validate")` for self-invocations. Set `autonumber=True` on `SequenceDiagram` to prefix steps automatically (`1.`, `2.`, ...).
- **Lifeline Activations & Notes**: Bracket active execution spans with `p.activate()` and `p.deactivate()`, and attach timeline annotations via `p.note("text", pos="right")` or spanning `d.note("text", over=[p1, p2])`.
- **Combined Fragments (`alt`, `else_`, `loop`, `opt`, `par`)**: Wrap conditional or repetitive flows in Python `with` blocks (`with d.alt("Guard"):` / `with d.else_("Fallback"):`, `with d.loop("Every 30s"):`, `with d.opt("2FA"):`, `with d.par("Fan-out"):`).
- **Zero-Waste Canvas Sizing**: Query `w, h = d.get_size()` after recording messages and pass integer bounds `setup(width=math.ceil(w) + 8, height=math.ceil(h) + 8)` before `d.draw(xy=(4.0, 4.0))` so the canvas wraps the lifelines tightly without blank half-canvas margins.

---

## 10.3 Workflows & State Lifecycles: FlowDiagram & StateDiagram

`FlowDiagram` models operational decisions and swimlanes, while `StateDiagram` models event-driven object lifecycles and finite state machines:

- **`FlowDiagram` (`drawlib.diagrams.flow`)**:
  - **ISO 5807 Symbols**: `Start` and `End` (stadium terminals), `Process` (action rectangle), `Decision` (branching diamond), and `Data` (I/O parallelogram), plus `Junction` (`flow.junction(xy)` or `node.fork([...])`) for clean wire merges.
  - **Swimlanes (`flow.add_lane`)**: Add vertical columns (`lane_orientation="vertical"`) or horizontal rows (`"horizontal"`). All lanes share a single global coordinate plane, so assigning the same `y` coordinate aligns cross-lane steps effortlessly.
  - **High-Contrast Node Styling**: Ground standard steps in `Styles.Neutral` or `Styles.PrimaryNeutral` with `Styles.DarkBold` text. When highlighting a focal step with `Styles.PrimaryFlat` or `Styles.AccentFlat`, **always set `text_style=Styles.WhiteBold`**—never leave dark or blue `PrimaryBold` text on a dark `PrimaryFlat` fill.
- **`StateDiagram` (`drawlib.diagrams.state`)**:
  - **State & Pseudo-State Classes**: Use `State(name, entry=..., do=..., exit=...)` (plus fluent `.add_action(kind, action)` for `StateAction` rows), `InitialState()`, `FinalState()`, `ChoiceState()` (guard diamond), and `ForkJoinState(orientation="horizontal" | "vertical")` (concurrency bar).
  - **UML Transitions (`sd.connect`)**: Pass `event="...", guard="...", action="..."` to format `"event [guard] / action"` labels automatically, use `bend=0.25` with `routing="curved"` to separate bidirectional arcs, and connect a state to itself (`sd.connect(s, s, side="top")`) for self-transitions.

```drawlib align=center code=fold file=flow_and_state.png caption="Figure 10.2: Side-by-Side Software Modeling — CI/CD Canary FlowDiagram (Left) and Worker Lifecycle StateDiagram (Right)"
from drawlib.canvas import save, setup
from drawlib.diagrams.flow import Data, Decision, End, FlowDiagram, Process, Start
from drawlib.diagrams.state import ChoiceState, FinalState, InitialState, State, StateDiagram
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=160, height=78)

# Left Panel: FlowDiagram
rectangle((41, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.git_branch((9.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (13.5, 68.0),
    "FlowDiagram: Canary Release Gate",
    style=Styles.DarkBold.patch(text_size=11.2, halign="left"),
)

flow = FlowDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
)
f_start = flow.add(
    Start("Git Merge", width=23, height=9.0, style=Styles.Neutral, text_style=Styles.DarkBold.patch(text_size=10.2)),
    xy=(22, 54),
)
f_canary = flow.add(
    Process(
        "Deploy Canary",
        width=26,
        height=10.0,
        style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=10.2),
    ),
    xy=(58, 54),
)
f_check = flow.add(
    Decision(
        "SLO Pass?",
        width=25,
        height=13.0,
        style=Styles.PrimaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    ),
    xy=(58, 35),
)
f_alert = flow.add(
    Data(
        "Rollback & Page",
        width=26,
        height=10.0,
        style=Styles.DangerNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.0),
    ),
    xy=(22, 35),
)
f_prod = flow.add(
    End(
        "Promote 100%",
        width=25,
        height=9.5,
        style=Styles.SecondaryNeutral,
        text_style=Styles.DarkBold.patch(text_size=10.2),
    ),
    xy=(58, 14),
)

f_start.connect(f_canary, padding=0.6)
f_canary.connect(f_check, start_side="bottom", end_side="top", padding=0.6)
f_check.connect(
    f_alert,
    label="No",
    start_side="left",
    end_side="right",
    style=Styles.DangerBold,
    text_style=Styles.DangerBold.patch(text_size=10.0),
    padding=0.6,
)
f_check.connect(f_prod, label="Yes", start_side="bottom", end_side="top", padding=0.6)
flow.draw()

# Right Panel: StateDiagram
rectangle((119, 39), width=74, height=68, style=Styles.MutedDashed.patch(shape_r=2.2))
phosphor.arrows_clockwise((87.5, 68.0), width=4.2, style=Styles.DarkBold)
text(
    (91.5, 68.0),
    "StateDiagram: Worker Lifecycle",
    style=Styles.DarkBold.patch(text_size=11.2, halign="left"),
)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.2),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
s_init = sd.add(InitialState(), xy=(89, 53))
s_warm = sd.add(
    State("Warming", entry="loadModel()", width=28, style=Styles.Neutral.patch(text_size=10.2)),
    xy=(114, 53),
)
s_active = sd.add(
    State(
        "Active",
        do="serveGrpc()",
        exit="drainPool()",
        width=28,
        style=Styles.PrimaryNeutral.patch(text_size=10.2),
    ),
    xy=(114, 29),
)
s_choice = sd.add(ChoiceState(), xy=(146, 29))
s_final = sd.add(FinalState(), xy=(114, 11))

sd.connect(s_init, s_warm, start_side="right", end_side="left", routing="direct", padding=0.8)
sd.connect(
    s_warm,
    s_active,
    label="  ready",
    start_side="bottom",
    end_side="top",
    routing="direct",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_active,
    s_choice,
    event="err",
    start_side="right",
    end_side="left",
    routing="direct",
    style=Styles.WarningBold,
    padding=0.8,
)
sd.connect(
    s_choice,
    s_warm,
    label="  [retry]",
    start_side="top",
    end_side="right",
    routing="orthogonal",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_choice,
    s_final,
    label="  [fatal]",
    start_side="bottom",
    end_side="right",
    routing="orthogonal",
    style=Styles.DangerBold,
    text_style=Styles.DangerBold.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.connect(
    s_active,
    s_final,
    label="  stop",
    start_side="bottom",
    end_side="top",
    routing="direct",
    text_style=Styles.Dark.patch(text_size=10.0, halign="left"),
    padding=0.8,
)
sd.draw()

save()
```

---

## 10.4 Object-Oriented Models with ClassDiagram

`ClassDiagram` (`drawlib.diagrams.class_diagram`) builds three-compartment UML 2.0 class boxes (`ClassNode`) whose heights expand automatically to fit their stereotypes (`stereotype="interface"` or `is_abstract=True`), attributes, and methods:

- **Fluent Member Registration**: Chain `.add_attribute(name, type, visibility="-", default_value=..., is_static=...)` and `.add_method(name, params, return_type, visibility="+", is_abstract=...)` with standard UML visibility markers (`"+"` public, `"-"` private, `"#"` protected, `"~"` package).
- **Six Canonical UML Relationships**: Call `cd.connect(source, target, relationship_type=...)` with `"inheritance"` (solid line, hollow triangle), `"realization"` (dashed line, hollow triangle), `"composition"` (solid diamond at owner), `"aggregation"` (hollow diamond), `"dependency"` (dashed open arrow), or `"association"` (solid link), complete with `start_multiplicity`, `end_multiplicity`, and `end_role`.

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

setup(width=140, height=64)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

repo = cd.add(
    ClassNode("PaymentGateway", stereotype="interface", width=44, header_style=Styles.SecondaryNeutral)
    .add_method("authorize", "amount: Decimal", "AuthReceipt"),
    xy=(32, 42),
)
stripe_gw = cd.add(
    ClassNode("StripeGateway", width=44)
    .add_attribute("api_client", "HttpClient", visibility="-")
    .add_method("authorize", "amount: Decimal", "AuthReceipt"),
    xy=(32, 16),
)
invoice = cd.add(
    ClassNode(
        "Invoice",
        width=40,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Styles.WhiteBold.text_color,
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=10.8,
        ),
    )
    .add_attribute("id", "UUID", visibility="+")
    .add_attribute("status", "InvoiceState", visibility="#")
    .add_method("capture", "gw: PaymentGateway", "bool"),
    xy=(106, 29),
)

cd.connect(stripe_gw, repo, "realization", start_side="top", end_side="bottom")
cd.connect(invoice, repo, "dependency", label="<<uses>>", start_side="left", end_side="right")

cd.draw(xy=(4.0, 4.0))
save("class_model.png")
```

---

## 10.5 Relational Schemas with ERDiagram

`ERDiagram` (`drawlib.diagrams.er`) renders Information Engineering (Crow's Foot) database schemas where each `Entity` formats its columns into three aligned sub-columns (`PK`/`FK` key badges, column name, and SQL type with `(NN)` non-null markers):

- **Table Definition (`Entity`)**: Chain `.add_column(name, type, pk=False, fk=False, nullable=True)` onto `Entity("table_name", width=38)`.
- **Crow's Foot Cardinalities & Row Anchoring**: Connect tables via `erd.connect(parent, child, cardinality="1:*", start_column="id", end_column="user_id")` (supporting `"1:1"`, `"1:0..1"`, `"0..1:1"`, `"1:*"`, `"1:1..*"`, `"0..1:*"`, and `"*:*"`). Passing `start_column` and `end_column` snaps each foreign-key line directly to the exact vertical row of the referenced column.

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.fonts import FontRoboto, FontSourceCode
from drawlib.styles import Styles

setup(width=136, height=52)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_font=FontSourceCode.ROBOTO_MONO, text_size=10.0),
    header_style=Styles.PrimaryNeutral.patch(text_font=FontRoboto.ROBOTO_BOLD, text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)

tenants = erd.add(
    Entity("tenants", width=40)
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("slug", "VARCHAR(64)", nullable=False)
    .add_column("created_at", "TIMESTAMPTZ", nullable=False),
    xy=(30, 26),
)
api_keys = erd.add(
    Entity(
        "api_keys",
        width=42,
        header_style=Styles.PrimaryFlat.patch(
            text_color=Styles.WhiteBold.text_color,
            text_font=FontRoboto.ROBOTO_BOLD,
            text_size=10.8,
        ),
    )
    .add_column("id", "UUID", pk=True, nullable=False)
    .add_column("tenant_id", "UUID", fk=True, nullable=False)
    .add_column("key_hash", "CHAR(64)", nullable=False)
    .add_column("revoked_at", "TIMESTAMPTZ", nullable=True),
    xy=(102, 26),
)

tenants.connect(
    api_keys,
    cardinality="1:*",
    start_column="id",
    end_column="tenant_id",
    start_side="right",
    end_side="left",
)

erd.draw(xy=(4.0, 4.0))
save("er_schema.png")
```
