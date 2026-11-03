# drawlib.diagrams.sequence

Chronological UML sequence diagrams with auto-spaced lifelines, participant groups, activation spans, sticky notes, and combined interaction blocks (`alt`, `loop`, `opt`, `par`). Canonical import: `from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram`.

```drawlib align=center code=fold file=21_diagrams_sequence_hero.png caption="Token Verification Sequence with ParticipantGroup, Activation Span, and Alt Block"
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Colors, Styles

setup(width=120, height=78)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    autonumber=True,
    col_width=34.0,
    step_y=7.0,
    margin=4.0,
)

client = d.add(Participant("Web App", width=22, height=15, icon=PhosphorIcon.BROWSER, icon_size=6.5))

platform = d.add(
    ParticipantGroup(
        title="Auth Platform",
        padding=4.0,
        style=Styles.PrimaryNeutral.patch(line_style="dashed"),
        text_style=Styles.PrimaryBold.patch(text_size=10.5, halign="left"),
    )
)
api = platform.add(
    Participant(
        "Auth API",
        width=22,
        height=15,
        icon=PhosphorIcon.SHIELD_CHECK,
        icon_size=6.5,
        style=Styles.White,
        text_style=Styles.WhiteBold.patch(text_color=Colors.White, text_size=10.5),
        card_style=Styles.PrimaryFlat,
    )
)
db = platform.add(
    Participant("User DB", width=22, height=15, icon=GcpIcon.CLOUD_SQL, icon_size=6.5, card_style=Styles.SecondaryNeutral)
)

api.activate()
client.request(api, "POST /v1/token")
api.request(db, "SELECT user_hash")
db.reply(api, "Row record")

with d.alt("Valid hash") as blk:
    blk.style = Styles.Neutral.patch(line_style="dashed")
    api.reply(client, "200 OK (JWT)")

api.deactivate()

d.draw(xy=(60.0, 39.0), align="center")
save()
```

---

## `class` SequenceDiagram

Top-level container and vertical timeline manager for sequence diagrams. Automatically spaces participants horizontally by `col_width` and advances time downward by `step_y` per event.

```python
SequenceDiagram(
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
) -> None
```

- **Coordinate Anchor**: `draw(xy=(0.0, 0.0), align="bottom_left")` places the bottom-left corner of the sequence diagram at canvas coordinate `xy` (or centers the diagram bounding box at `xy` when `align="center"`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `node_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base style for participant vector icons and fallback lifeline strokes (keyword-only). |
| `node_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style for participant labels and group headers (keyword-only). |
| `edge_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base stroke and arrowhead style for message lines (keyword-only). |
| `edge_text_style` | [`Style`](05_styles_and_types.md#style) | *(Required)* | Base typography style for message labels, block headers, and notes (keyword-only). |
| `node_card_style` | `Style \| None` | `None` | Optional default background/border style for [`Participant`](#participant) header cards (`None` renders transparent cards). |
| `title` | `str` | `""` | Optional diagram title rendered centered above the top headers. |
| `autonumber` | `bool` | `False` | When `True`, prefixes message labels sequentially (`1.`, `2.`, `3.`, ...). |
| `width` | `float \| None` | `None` | Optional fixed diagram width override in local units. |
| `height` | `float \| None` | `None` | Optional fixed diagram height override in local units. |
| `col_width` | `float` | `20.0` | Default center-to-center horizontal spacing between auto-placed participants. |
| `step_y` | `float` | `7.0` | Vertical distance advanced downward for each message, note, or block step. |
| `margin` | `float` | `5.0` | Outer perimeter padding around participants and lifelines. |
| `style` | `Style \| None` | `None` | Optional outer background card style for the diagram container. |
| `title_style` | `Style \| None` | `None` | Optional typography style override for `title`. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, item: Participant \| ParticipantGroup, x: float \| None = None, *, show: bool \| None = None) -> Participant \| ParticipantGroup` | Register a [`Participant`](#participant) (optionally pinned at horizontal `x`) or [`ParticipantGroup`](#participantgroup). |
| `alt` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | Return an `alt` [`Block`](#block) context manager for conditional branching (`with d.alt("guard"):`). |
| `connect` | `method` | `(self, source: Participant, target: Participant, label: str = "", arrow: ArrowType = "->", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Record a custom arrow [`Message`](#message) (e.g., bidirectional `"<->"`). |
| `draw` | `method` | `(self, xy: tuple[float, float] = (0.0, 0.0), *, align: Literal["bottom_left", "center"] = "bottom_left", scale: PosFloat = 1.0) -> None` | Render the complete sequence diagram onto the active canvas. |
| `else_` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | Insert a dashed `else` divider branch inside an active `alt` block (or use as a context manager). |
| `events` | `property` | `-> list[object]` | Return the recorded timeline event sequence in declaration order. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Estimate the total `(width, height)` of the diagram in unscaled local units. |
| `groups` | `property` | `-> list[ParticipantGroup]` | Return registered [`ParticipantGroup`](#participantgroup) boundary boxes. |
| `loop` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | Return a `loop` [`Block`](#block) context manager for repeated message steps. |
| `note` | `method` | `(self, text: str, on: Participant \| None = None, over: list[Participant] \| None = None, pos: NotePosition = "right", style: Style \| None = None, show: bool = True) -> Note` | Record a [`Note`](#note) card beside `on` or spanning across `over` participants at the current step. |
| `opt` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | Return an `opt` [`Block`](#block) context manager for optional single-branch steps. |
| `par` | `method` | `(self, label: str = "", *, show: bool = True) -> Block` | Return a `par` [`Block`](#block) context manager for parallel interactions. |
| `participants` | `property` | `-> list[Participant]` | Return the ordered list of registered [`Participant`](#participant) instances. |
| `reply` | `method` | `(self, source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Record a dashed return/response [`Message`](#message) from `source` to `target`. |
| `request` | `method` | `(self, source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Record a solid request [`Message`](#message) from `source` to `target` (supports self-calls when `source is target`). |
| `space` | `method` | `(self, dy: float = 5.0) -> None` | Advance the vertical timeline by an extra `dy` units without drawing an event. |

---

## `class` Participant

Actor, service, API endpoint, or database column in a sequence diagram with a top header card and a vertical dashed lifeline.

```python
Participant(
    text: str = "",
    width: float = 20.0,
    height: float = 16.0,
    icon: IconType = None,
    icon_size: float = 8.0,
    style: Style | None = None,
    text_style: Style | None = None,
    card_style: Style | None = None,
    lifeline_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Auto-spaced left-to-right along the top header row by `diagram.col_width`, or pinned horizontally at local `x` via `d.add(p, x=...)` / `p.set_x(x)`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | `""` | Display label inside the participant header card (supports `\n`). |
| `width` | `float` | `20.0` | Header card width in local units. |
| `height` | `float` | `16.0` | Header card height in local units. |
| `icon` | `IconType` | `None` | Any of the [34 icon enums](#icon-enums), icon callable, [`CustomIcon`](#customicon), [`Dimage`](04_images_and_math.md#dimage), `PIL.Image.Image`, or image path. |
| `icon_size` | `float` | `8.0` | Rendered icon width/height in local units. |
| `style` | `Style \| None` | `None` | Optional vector icon style override (falls back to `diagram.node_style`). |
| `text_style` | `Style \| None` | `None` | Optional label typography style override (falls back to `diagram.node_text_style`). |
| `card_style` | `Style \| None` | `None` | Optional header card background/border style override (falls back to `diagram.node_card_style`). |
| `lifeline_style` | `Style \| None` | `None` | Optional stroke style override for the vertical dashed lifeline stem. |
| `show` | `bool` | `True` | Visibility flag (`False` hides the participant, lifeline, and incident messages). |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `activate` | `method` | `(self) -> None` | Begin an active execution bar rectangle on this participant's lifeline at the current timeline step. |
| `connect` | `method` | `(self, target: Participant, label: str = "", arrow: ArrowType = "->", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Send a custom arrow [`Message`](#message) from `self` to `target`. |
| `deactivate` | `method` | `(self) -> None` | Close the current active execution bar on this participant's lifeline. |
| `get_header_size` | `method` | `(self) -> tuple[float, float]` | Return `(width, height)` of the participant header card. |
| `get_size` | `method` | `(self) -> tuple[float, float]` | Alias returning `(width, height)` of the participant header card. |
| `note` | `method` | `(self, text: str, pos: Literal["left", "right"] = "right", style: Style \| None = None, show: bool = True) -> Note` | Attach a [`Note`](#note) annotation card to the `"left"` or `"right"` of this lifeline. |
| `reply` | `method` | `(self, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Send a dashed return/response [`Message`](#message) from `self` to `target`. |
| `request` | `method` | `(self, target: Participant, label: str = "", is_async: bool = False, style: Style \| None = None, text_style: Style \| None = None, show: bool = True) -> Message` | Send a solid request [`Message`](#message) from `self` to `target`. |
| `set_x` | `method` | `(self, x: float) -> Participant` | Explicitly pin this participant's horizontal lifeline coordinate to `x` and return `self`. |

---

## `class` ParticipantGroup

Labeled boundary box enclosing a contiguous set of [`Participant`](#participant) header cards at the top of a sequence diagram.

```python
ParticipantGroup(
    title: str = "",
    padding: float = 4.0,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Automatically spans horizontally and vertically around the header cards of all member participants added via `group.add(participant)`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `title` | `str` | `""` | Group banner title rendered above the enclosed participant headers. |
| `padding` | `float` | `4.0` | Clearance padding around enclosed participant header cards. |
| `style` | `Style \| None` | `None` | Optional boundary box fill and stroke style. |
| `text_style` | `Style \| None` | `None` | Optional typography style override for `title`. |
| `show` | `bool` | `True` | Whether to render the group boundary box and title. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `add` | `method` | `(self, participant: Participant, *, show: bool \| None = None) -> Participant` | Add `participant` to this group (and register it on the parent `SequenceDiagram` if attached). |
| `participants` | `property` | `-> list[Participant]` | Return the ordered list of member [`Participant`](#participant) instances in this group. |

---

## `class` Message

Recorded horizontal (or self-looping) interaction arrow between two [`Participant`](#participant) lifelines. Returned by `request()`, `reply()`, and `connect()`.

```python
Message(
    source: Participant,
    target: Participant,
    label: str = "",
    is_reply: bool = False,
    is_async: bool = False,
    arrow: ArrowType = "->",
    style: Style | None = None,
    text_style: Style | None = None,
    padding: PaddingType = 0.0,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Spans horizontally from `source`'s lifeline X to `target`'s lifeline X at the timeline Y position of its step (or loops to the right when `source is target`).

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `source` | [`Participant`](#participant) | *(Required)* | Sending participant. |
| `target` | [`Participant`](#participant) | *(Required)* | Receiving participant (pass `source` for a recursive self-call loop). |
| `label` | `str` | `""` | Message signature or payload description rendered above the arrow. |
| `is_reply` | `bool` | `False` | When `True`, renders a dashed return line instead of a solid request line. |
| `is_async` | `bool` | `False` | When `True`, renders an open stick arrowhead instead of a filled triangle. |
| `arrow` | `Literal["->", "<-", "<->", "-"]` | `"->"` | Arrowhead direction configuration. |
| `style` | `Style \| None` | `None` | Optional line stroke style override (falls back to `diagram.edge_style`). |
| `text_style` | `Style \| None` | `None` | Optional label typography style override (falls back to `diagram.edge_text_style`). |
| `padding` | `float \| tuple[float, float]` | `0.0` | Clearance offset from the source/target lifelines. |
| `show` | `bool` | `True` | Whether to render this message arrow and label. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `is_self_call` | `property` | `-> bool` | `True` when `source is target` (rendered as a right-hand loopback arrow). |
| `set_arrow` | `method` | `(self, arrow: ArrowType) -> Message` | Update arrowhead marker and return `self`. |
| `set_async` | `method` | `(self, is_async: bool = True) -> Message` | Toggle asynchronous open arrowhead styling and return `self`. |
| `set_label` | `method` | `(self, text: str) -> Message` | Update message label text and return `self`. |
| `set_padding` | `method` | `(self, padding: PaddingType) -> Message` | Update lifeline endpoint clearance padding and return `self`. |
| `set_reply` | `method` | `(self, is_reply: bool = True) -> Message` | Toggle dashed reply line rendering and return `self`. |
| `set_style` | `method` | `(self, style: Style) -> Message` | Override message line [`Style`](05_styles_and_types.md#style) and return `self`. |
| `set_text_style` | `method` | `(self, text_style: Style) -> Message` | Override message label [`Style`](05_styles_and_types.md#style) and return `self`. |

---

## `class` Block

UML 2.0 combined interaction fragment (`loop`, `alt`, `else`, `opt`, `par`) used as a Python `with` context manager via `d.loop()`, `d.alt()`, `d.else_()`, `d.opt()`, and `d.par()`.

```python
Block(
    block_type: BlockType,
    label: str = "",
    diagram: SequenceDiagram | None = None,
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Automatically encloses the horizontal lifeline span and vertical timeline range of all messages recorded inside its `with` block.

### Constructor Parameters & Mutable Attributes

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `block_type` | `Literal["loop", "alt", "else", "opt", "par"]` | *(Required)* | Combined fragment operator badge displayed in the top-left pentagon tab. |
| `label` | `str` | `""` | Guard condition or iteration expression rendered next to the operator badge. |
| `diagram` | `SequenceDiagram \| None` | `None` | Owning [`SequenceDiagram`](#sequencediagram) timeline manager. |
| `style` | `Style \| None` | `None` | Frame border and fill style (can be assigned inside `with d.alt(...) as blk: blk.style = ...`). |
| `text_style` | `Style \| None` | `None` | Operator tag and guard condition typography style. |
| `show` | `bool` | `True` | Whether to render the block frame boundary and label tag. |

---

## `class` Note

Sticky note annotation card attached beside a single [`Participant`](#participant) lifeline or spanning across multiple lifelines at the current timeline step.

```python
Note(
    text: str,
    on: Participant | None = None,
    over: list[Participant] | None = None,
    pos: NotePosition = "right",
    style: Style | None = None,
    text_style: Style | None = None,
    show: bool = True,
) -> None
```

- **Coordinate Anchor**: Positioned at the current vertical timeline step to the `"left"` / `"right"` of `on`, or centered `"over"` the lifeline span of `over`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *(Required)* | Annotation text displayed inside the note card (supports `\n`). |
| `on` | `Participant \| None` | `None` | Target [`Participant`](#participant) when anchoring to a single lifeline. |
| `over` | `list[Participant] \| None` | `None` | List of participants to span across horizontally. |
| `pos` | `Literal["left", "right", "over"]` | `"right"` | Placement relative to `on` (`"left"`, `"right"`, or `"over"`). |
| `style` | `Style \| None` | `None` | Optional note card background and border style override. |
| `text_style` | `Style \| None` | `None` | Optional note text typography style override. |
| `show` | `bool` | `True` | Whether to render this note card. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `set_style` | `method` | `(self, style: Style) -> Note` | Override note card background/border [`Style`](05_styles_and_types.md#style) and return `self`. |
| `set_text` | `method` | `(self, text: str) -> Note` | Replace note content text and return `self`. |
| `set_text_style` | `method` | `(self, text_style: Style) -> Note` | Override note text [`Style`](05_styles_and_types.md#style) and return `self`. |

---

## `class` CustomIcon

Adapter wrapping raster image files, [`Dimage`](04_images_and_math.md#dimage) objects, or `PIL.Image.Image` instances for use as `Participant(..., icon=CustomIcon(...))`.

```python
CustomIcon(
    image: str | Path | Dimage | Image | CustomIcon,
) -> None
```

- **Coordinate Anchor**: Centered automatically inside the [`Participant`](#participant) header card's icon slot at `icon_size`.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `image` | `str \| Path \| Dimage \| Image \| CustomIcon` | *(Required)* | Image file path, [`Dimage`](04_images_and_math.md#dimage) object, `PIL.Image.Image`, or existing `CustomIcon`. |

### Public Methods & Properties

| Member | Kind | Signature | Description |
| :--- | :--- | :--- | :--- |
| `copy` | `method` | `(self) -> CustomIcon` | Return an independent deep copy of this `CustomIcon`. |
| `dimage` | `property` | `-> Dimage` | Return the underlying [`Dimage`](04_images_and_math.md#dimage) instance. |

---

## `type` icons

Re-exported icon namespace submodule (`drawlib.diagrams.sequence.icons`, shared with [`drawlib.diagrams.architecture.icons`](19_diagrams_architecture.md#icons)) providing [`CustomIcon`](#customicon), `IconType`, and all 34 diagram icon enums.

```python
from drawlib.diagrams.sequence import icons

api = Participant("Gateway", icon=icons.GcpIcon.CLOUD_ENDPOINTS)
```

- **Coordinate Anchor**: Not applicable (namespace module re-exporting 40 icon types and helpers).

| Export Group | Exported Symbols | Description |
| :--- | :--- | :--- |
| **Icon Enums (34)** | `icons.AiIcon` .. `icons.WorkspaceIcon` | All 34 `StrEnum` icon catalogs listed in [`Icon Enums (34 Suites)`](#icon-enums). |
| **Custom Wrapper** | `icons.CustomIcon` | Alias of [`CustomIcon`](#customicon) for custom participant header icons. |
| **Type Aliases & Helpers** | `icons.IconType`, `icons.draw_node_icon` | Union type alias accepted by `Participant(icon=...)` and internal icon renderer helper. |

---

## `enum` Icon Enums (34 Suites)

All 34 standardized icon `StrEnum` classes re-exported directly from `drawlib.diagrams.sequence` (and `drawlib.diagrams.sequence.icons`) for declarative `Participant(..., icon=<Enum>.<MEMBER>)` headers. `PhosphorIcon` glyphs are tinted by `participant.style` / `diagram.node_style`; the remaining 33 suites render PNG assets from [`drawlib.icons`](08_icons.md).

| Icon Enum | Corresponding `drawlib.icons` Suite | Category & Asset Style |
| :--- | :--- | :--- |
| `AiIcon` | [`drawlib.icons.ai`](08_icons.md#ai) | Official AI, LLM, and ML platform icons |
| `AwsIcon` | [`drawlib.icons.aws`](08_icons.md#aws) | Official Amazon Web Services architecture icons |
| `AzureIcon` | [`drawlib.icons.azure`](08_icons.md#azure) | Official Microsoft Azure architecture icons |
| `BusinessIcon` | [`drawlib.icons.business`](08_icons.md#business) | Enterprise SaaS, ERP, CRM, and FinTech brand icons |
| `ClientIcon` | [`drawlib.icons.client`](08_icons.md#client) | Browsers, mobile/desktop OS, and client device icons |
| `CloudIcon` | [`drawlib.icons.cloud`](08_icons.md#cloud) | Cloud, PaaS, CDN, and hosting provider brand icons |
| `CnativeIcon` | [`drawlib.icons.cnative`](08_icons.md#cnative) | Kubernetes and CNCF cloud-native ecosystem icons |
| `CodeIcon` | [`drawlib.icons.code`](08_icons.md#code) | Programming languages, frameworks, and runtime icons |
| `DataIcon` | [`drawlib.icons.data`](08_icons.md#data) | Relational/NoSQL databases, caches, and streaming icons |
| `DevopsIcon` | [`drawlib.icons.devops`](08_icons.md#devops) | CI/CD, IaC, containers, and observability tool icons |
| `FacilityIcon` | [`drawlib.icons.facility`](08_icons.md#facility) | Datacenter, racks, telecom carriers, and hardware icons |
| `GcpIcon` | [`drawlib.icons.gcp`](08_icons.md#gcp) | Official Google Cloud Platform architecture icons |
| `ItserviceIcon` | [`drawlib.icons.itservice`](08_icons.md#itservice) | IT service management, consulting, and enterprise vendor icons |
| `NetworkIcon` | [`drawlib.icons.network`](08_icons.md#network) | Routers, switches, firewalls, DNS, and network topology icons |
| `OriginalAiIcon` | [`drawlib.icons.original_ai`](08_icons.md#original-ai) | Drawlib vendor-neutral flat AI & ML icons |
| `OriginalBusinessIcon` | [`drawlib.icons.original_business`](08_icons.md#original-business) | Drawlib vendor-neutral flat business & office icons |
| `OriginalClientIcon` | [`drawlib.icons.original_client`](08_icons.md#original-client) | Drawlib vendor-neutral flat client & device icons |
| `OriginalCloudIcon` | [`drawlib.icons.original_cloud`](08_icons.md#original-cloud) | Drawlib vendor-neutral flat cloud service icons |
| `OriginalCnativeIcon` | [`drawlib.icons.original_cnative`](08_icons.md#original-cnative) | Drawlib vendor-neutral flat cloud-native & container icons |
| `OriginalCodeIcon` | [`drawlib.icons.original_code`](08_icons.md#original-code) | Drawlib vendor-neutral flat code & SDK icons |
| `OriginalDataIcon` | [`drawlib.icons.original_data`](08_icons.md#original-data) | Drawlib vendor-neutral flat database & storage icons |
| `OriginalDevopsIcon` | [`drawlib.icons.original_devops`](08_icons.md#original-devops) | Drawlib vendor-neutral flat DevOps & pipeline icons |
| `OriginalFacilityIcon` | [`drawlib.icons.original_facility`](08_icons.md#original-facility) | Drawlib vendor-neutral flat building & facility icons |
| `OriginalItserviceIcon` | [`drawlib.icons.original_itservice`](08_icons.md#original-itservice) | Drawlib vendor-neutral flat IT operations & support icons |
| `OriginalNetworkIcon` | [`drawlib.icons.original_network`](08_icons.md#original-network) | Drawlib vendor-neutral flat network appliance icons |
| `OriginalSecurityIcon` | [`drawlib.icons.original_security`](08_icons.md#original-security) | Drawlib vendor-neutral flat security & IAM icons |
| `OriginalServerIcon` | [`drawlib.icons.original_server`](08_icons.md#original-server) | Drawlib vendor-neutral flat server & compute icons |
| `OriginalSocialIcon` | [`drawlib.icons.original_social`](08_icons.md#original-social) | Drawlib vendor-neutral flat social & messaging icons |
| `OriginalWorkspaceIcon` | [`drawlib.icons.original_workspace`](08_icons.md#original-workspace) | Drawlib vendor-neutral flat workspace & collaboration icons |
| `PhosphorIcon` | [`drawlib.icons.phosphor`](08_icons.md#phosphor) | 1,530+ tintable monochrome Phosphor UI vector font icons |
| `SecurityIcon` | [`drawlib.icons.security`](08_icons.md#security) | Official cybersecurity, IAM, and compliance brand icons |
| `ServerIcon` | [`drawlib.icons.server`](08_icons.md#server) | Linux/Windows OS, hypervisors, and server hardware icons |
| `SocialIcon` | [`drawlib.icons.social`](08_icons.md#social) | Social platforms, developer communities, and messaging icons |
| `WorkspaceIcon` | [`drawlib.icons.workspace`](08_icons.md#workspace) | Productivity suites, docs, and team collaboration SaaS icons |
