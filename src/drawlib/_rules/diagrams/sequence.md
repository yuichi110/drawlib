# Drawlib SequenceDiagram Guidelines (`lib-diagrams-sequence`)

`drawlib.diagrams.sequence` models chronological message interactions between services, actors, databases, and external APIs. It automatically manages vertical time progression (`step_y`), horizontal participant spacing (`col_width`), lifeline dashed stems, participant boundary groups (`ParticipantGroup`), timeline annotations (`Note`), and nested UML interaction frames (`loop`, `alt`, `else_`, `opt`, `par`).

```text
  ┌──────────┐          ┌──────────┐          ┌──────────┐
  │  Client  │          │   Auth   │          │ Database │
  └────┬─────┘          └────┬─────┘          └────┬─────┘
       │  1: POST /login     │                     │
       ├────────────────────►│  2: SELECT user     │
       │                     ├────────────────────►│
       │                     │  3: Row Record      │
       │  4: 200 OK (JWT)    │◄ - - - - - - - - - -┤
       │◄ - - - - - - - - - -┤                     │
      ─┴─                   ─┴─                   ─┴─
```

---

## 1. Public Exports & Imports

```python
from drawlib.diagrams.sequence import (
    Block,
    CustomIcon,
    Message,
    Note,
    Participant,
    ParticipantGroup,
    SequenceDiagram,
    icons,
    # Plus all 33 built-in icon enums (same as ArchitectureDiagram):
    AiIcon,
    AwsIcon,
    AzureIcon,
    BusinessIcon,
    ClientIcon,
    CloudIcon,
    CnativeIcon,
    CodeIcon,
    DataIcon,
    DevopsIcon,
    FacilityIcon,
    GcpIcon,
    ItserviceIcon,
    NetworkIcon,
    OriginalAiIcon,
    OriginalBusinessIcon,
    OriginalClientIcon,
    OriginalCloudIcon,
    OriginalCnativeIcon,
    OriginalCodeIcon,
    OriginalDataIcon,
    OriginalDevopsIcon,
    OriginalFacilityIcon,
    OriginalItserviceIcon,
    OriginalNetworkIcon,
    OriginalSecurityIcon,
    OriginalServerIcon,
    OriginalSocialIcon,
    OriginalWorkspaceIcon,
    PhosphorIcon,
    SecurityIcon,
    ServerIcon,
    SocialIcon,
    WorkspaceIcon,
)
```

---

## 2. Core Classes & Constructor Parameters

### 2.1 `SequenceDiagram`

```python
d = SequenceDiagram(
    *,
    node_style: Style,
    node_text_style: Style,
    edge_style: Style,
    edge_text_style: Style,
    node_card_style: Style | None = None,
    title: str = "",
    autonumber: bool = False,
    width: float | None = None,
    height: float | None = None,
    col_width: float = 20.0,
    step_y: float = 7.0,
    margin: float = 5.0,
    style: Style | None = None,
    title_style: Style | None = None,
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | `Style` | *(Required)* | Default style for participant icons and lifeline strokes (keyword-only). |
| `node_text_style` | `Style` | *(Required)* | Default typography style for participant labels and fallback group titles (keyword-only). |
| `edge_style` | `Style` | *(Required)* | Default stroke style for message arrows (keyword-only). |
| `edge_text_style` | `Style` | *(Required)* | Default typography style for message labels, block tags, and notes (keyword-only). |
| `node_card_style` | `Style \| None` | `None` | Default style for participant header card backgrounds/borders. |
| `title` | `str` | `""` | Optional diagram title rendered at the top center. |
| `autonumber` | `bool` | `False` | Automatically prefixes each message label with `"1. "`, `"2. "`, `"3. "`, etc. |
| `width` | `float \| None` | `None` | Optional explicit diagram width override. |
| `height` | `float \| None` | `None` | Optional explicit diagram height override. |
| `col_width` | `float` | `20.0` | Default horizontal spacing between auto-placed participants. |
| `step_y` | `float` | `7.0` | Vertical distance advanced per timeline event (message, note, or block boundary). |
| `margin` | `float` | `5.0` | Outer margin around participants and timeline elements. |
| `style` | `Style \| None` | `None` | Optional outer container card background/border style. |
| `title_style` | `Style \| None` | `None` | Optional typography style for the diagram title. |

#### Diagram Registration & Sizing Methods:
- **`d.add(participant, x=None, *, show=None) -> Participant | ParticipantGroup`**:
  Registers a `Participant` or `ParticipantGroup`. If `x: float | None = None` is provided for a `Participant`, pins its horizontal lifeline center to `x`; otherwise auto-spaces participants using `col_width`.
- **`d.get_size() -> tuple[float, float]`**:
  Returns the total `(width, height)` of the sequence diagram in unscaled local units.
- **`d.draw(xy=(0.0, 0.0), *, align="bottom_left", scale=1.0) -> None`**:
  Renders the sequence diagram onto the active canvas anchored at `xy` (`align: Literal["bottom_left", "center"] = "bottom_left"`, `scale: float = 1.0`).

---

### 2.2 `Participant` & `ParticipantGroup`

```python
p = Participant(
    text: str = "",
    width: float = 16.0,
    height: float = 12.0,
    icon: IconType = None,
    icon_size: float = 6.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    show: bool = True,
)

group = ParticipantGroup(
    title: str = "",
    padding: float = 4.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
)
```

- **Positioning Participants**:
  - Auto-spaced left-to-right via `d.add(p)` or `group.add(p)` (spaced by `col_width`, default `20.0`).
  - Explicitly positioned via `d.add(p, x=45.0)`, `group.add(p, x=45.0)`, or fluent `p.set_x(45.0) -> Participant`.
- **`ParticipantGroup`**:
  - Encloses child participants added via `group.add(participant, x=None, *, show=None)` inside a labeled vertical boundary box with inner `padding` (default `4.0`), `style`, and `text_style`.

---

### 2.3 Messages (`request`, `reply`, `connect`)

Messages can be recorded either via participant methods (`a.request(b, ...)`) or diagram methods (`d.request(a, b, ...)`), advancing the vertical timeline by `step_y` and returning the mutable `Message` object:

| Method (on `Participant` `a` or `SequenceDiagram` `d`) | Signature | Visual Rendering |
| :--- | :--- | :--- |
| **`a.request(b, ...)`** / **`d.request(a, b, ...)`** | `(target, label="", is_async=False, style=None, text_style=None, show=True) -> Message` | Solid line with `"->"` arrowhead (`line_style="solid"`). Supports self-calls (`a.request(a, "Validate")`). |
| **`b.reply(a, ...)`** / **`d.reply(b, a, ...)`** | `(target, label="", is_async=False, style=None, text_style=None, show=True) -> Message` | Dashed return line with `"->"` arrowhead (`line_style="dashed"`). |
| **`a.connect(b, ...)`** / **`d.connect(a, b, ...)`** | `(target, label="", arrow="->", is_async=False, style=None, text_style=None, show=True) -> Message` | Custom arrow (`"->"`, `"<-"`, `"<->"`, `"-"`; default `arrow="->"`). |

- **`Message` Fluent Methods**:
  - `msg.set_label(text: str) -> Self`
  - `msg.set_style(style: Style) -> Self`
  - `msg.set_text_style(text_style: Style) -> Self`

---

### 2.4 Timeline Notes (`p.note()` & `d.note()`)

Attach explanatory notes at the current vertical point in the timeline:

```python
# On a single Participant (pos: Literal["left", "right"] = "right"):
note1 = p.note(
    text: str,
    pos: Literal["left", "right"] = "right",
    style: Style | None = None,
    show: bool = True,
) -> Note

# On SequenceDiagram (supports single participant via on=... or spanning via over=[p1, p2]):
note2 = d.note(
    text: str,
    on: Participant | None = None,
    over: Participant | list[Participant] | None = None,
    pos: Literal["left", "right", "over"] = "right",
    style: Style | None = None,
    show: bool = True,
) -> Note
```

---

### 2.5 Interaction Frames / Combined Fragments (`Block`: `loop`, `alt`, `else_`, `opt`, `par`)

Use Python `with` context managers to wrap message sequences inside standard UML 2.0 combined fragments:

```python
with d.loop(label="Every 30s", *, show=True) as blk:
    ...
with d.alt(label="Cache Hit", *, show=True) as alt_blk:
    ...
    d.else_(label="Cache Miss")  # Inserts dashed horizontal divider inside active alt block
    ...
with d.opt(label="2FA Enabled", *, show=True):
    ...
with d.par(label="Async Fan-Out", *, show=True):
    ...
```

- **Styling Interaction Blocks (`Block`)**:
  - `Block(block_type, label="", diagram=None, style=None, text_style=None, show=True)` exposes `.style` (border/fill style of the frame) and `.text_style` (typography of the pentagon tag and condition guard), which can be assigned on the context manager variable (`blk.style = Styles.PrimaryNeutral`, `blk.text_style = Styles.PrimaryBold`).

---

## 3. Production Examples

### Example 3.1: OAuth 2.0 / JWT Login Flow with `ParticipantGroup`, `alt`/`else_`, and `note()`
```drawlib align=center code=fold file=seq_oauth_jwt_flow.png caption="OAuth 2.0 Authentication Sequence with Alt/Else and ParticipantGroup"
from drawlib import canvas
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

canvas.clear()
canvas.setup(width=145, height=112)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="OAuth 2.0 & JWT Session Verification",
    autonumber=True,
    col_width=32.0,
    step_y=6.8,
)

# Register participants and a backend ParticipantGroup
client = d.add(Participant("Mobile App", width=20, height=14, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=6.5))

backend = d.add(ParticipantGroup(title="Core Cloud Platform", padding=4.5, style=Styles.Neutral, text_style=Styles.DarkBold))
gateway = backend.add(Participant("API Gateway", width=22, height=14, icon=GcpIcon.CLOUD_ENDPOINTS, icon_size=6.5))
auth = backend.add(
    Participant("Auth Service", width=22, height=14, icon=PhosphorIcon.SHIELD_CHECK, icon_size=6.5, card_style=Styles.PrimaryNeutral)
)
db = backend.add(Participant("User DB", width=20, height=14, icon=GcpIcon.CLOUD_SQL, icon_size=6.5))

# Message timeline
client.request(gateway, "POST /v1/auth/token")
gateway.request(auth, "Verify Credentials")
auth.request(db, "SELECT id, password_hash")
db.reply(auth, "User Record")
auth.request(auth, "Verify Argon2id Hash")

with d.alt("Valid Credentials") as alt_block:
    alt_block.style = Styles.Neutral.patch(line_style="dashed")
    auth.reply(gateway, "Signed JWT + Refresh Token", style=Styles.Success)
    gateway.reply(client, "200 OK (Bearer JWT)", style=Styles.Success)
    d.note("JWT cached in Keychain", on=client, pos="right", style=Styles.PrimaryNeutral)

    d.else_("Invalid Password")
    auth.reply(gateway, "401 Unauthorized", style=Styles.Danger, text_style=Styles.Danger)
    gateway.reply(client, "401 Error Payload", style=Styles.Danger, text_style=Styles.Danger)

d.draw(xy=(6.0, 4.0))
canvas.save()
```
