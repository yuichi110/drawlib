# Sequence Diagram Design Document & Implementation Plan: `drawlib.diagrams.sequence`

This document specifies the technical design, object model, API contracts, and implementation plan for `drawlib.diagrams.sequence`, Drawlib's pure-Python sequence diagramming framework.

---

## 1. Overview and Objectives

### 1.1. Motivation & Vision
Sequence diagrams are essential for visualizing message flows, microservice interactions, protocol handshakes, and business logic execution over time.
External text-to-diagram tools (like Mermaid or PlantUML) rely on cryptic, hard-to-remember ASCII syntax (`->>`, `-->>`, `-)`, `activate`, `deactivate`), provide limited layout flexibility, and lack native integration with Python applications.

`drawlib.diagrams.sequence` provides a declarative, pure-Python sequence diagramming framework ("Sequence as Code") that runs directly on Drawlib's vector canvas with zero external binary dependencies.

### 1.2. Core Design Principles

1. **Pythonic API Ergonomics**:
   - Uses formal, domain-accurate sequence diagram terminology: `Participant`, `Message`, and `ParticipantGroup`.
   - Replaces arcane arrow symbols with natural, intuitive verbs: `a.request(b)` (solid call) and `b.reply(a)` (dashed response).
   - Keeps `a.connect(b, arrow="<->")` for bidirectional streams (WebSocket, P2P, sync) without confusion.
   - Eliminates reverse arrow confusion (`<-` is not needed; `b.reply(a)` or `b.request(a)` has clear grammatical subjects).
2. **Timeline Progression (Top-to-Bottom)**:
   - Events are recorded sequentially in declaration order.
   - Vertical timeline ($Y$-axis) advances downward with each message, note, or block boundary.
3. **Automatic Layout with Manual Fine-Tuning**:
   - **X-axis (Lifelines)**: Columns are spaced automatically based on participant label widths and message lengths, with support for manual `x` coordinate pinning.
   - **Y-axis (Steps)**: Step heights automatically adjust for multi-line labels and notes. Manual spacers (`d.space(dy)`) provide customized breathing room.
   - **Auto-Padding**: Outer dimensions and canvas margins are calculated automatically.
4. **Structured Blocks via Context Managers**:
   - Framing blocks (`loop`, `alt` / `else_`, `opt`, `par`) use Python's `with` statement, matching code indentation directly to visual nested boundaries.
5. **First-Class Icon & Style Integration**:
   - Participants support `PhosphorIcon`, `GcpIcon`, and `CustomIcon` alongside customizable `Style` objects.

---

## 2. Package Architecture

Following Drawlib's established single-package architecture (Pattern A):

```text
src/drawlib/
├── diagrams/
│   ├── __init__.py                    # Exports architecture and sequence modules
│   └── sequence/                      # Public sequence diagrams package
│       ├── __init__.py                # Exports Diagram, Participant, Message, Note, Block, ParticipantGroup
│       └── icons.py                   # Re-exports GcpIcon, PhosphorIcon, CustomIcon
└── _diagrams/
    └── sequence/                      # Internal implementation package
        ├── __init__.py
        ├── _types.py                  # Type definitions (ArrowType, NotePosition, BlockType, etc.)
        ├── _participant.py            # Participant & lifeline tracking
        ├── _message.py                # Message line & arrow modeling
        ├── _note.py                   # Note annotation component
        ├── _block.py                  # Block (loop/alt/opt) context manager
        ├── _group.py                  # ParticipantGroup (participant boundary box)
        ├── _diagram.py                # Diagram container & timeline recorder
        └── _renderer.py               # Auto-layout calculation & 2-pass drawing engine
```

### 2.1. Public Import Contracts

```python
# Standard recommended import
from drawlib.diagrams.sequence import (
    Block,
    CustomIcon,
    Diagram,
    GcpIcon,
    Message,
    Note,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
)

# Top-level module access
import drawlib.diagrams.sequence as ds
```

---

## 3. Core Class Specifications

### 3.1. `Diagram` (Top-Level Container & Timeline Recorder)

The `Diagram` class manages the participant lifelines, chronological events list, and overall diagram rendering.

#### Constructor
```python
class Diagram:
    def __init__(
        self,
        title: str = "",
        autonumber: bool = False,
        width: float | None = None,
        height: float | None = None,
        col_width: float = 20.0,
        step_y: float = 7.0,
        padding: float | tuple[float, float, float, float] = 5.0,
        style: Style | None = None,
    ) -> None: ...
```

#### Public Methods
- `add(participant: Participant, x: float | None = None) -> Participant`
  - Adds a participant to the diagram. If `x` is `None`, column position is calculated automatically.
- `add_group(group: ParticipantGroup) -> ParticipantGroup`
  - Adds a participant header group (e.g. `box "Internal Services"`).
- `request(source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style | None = None) -> Message`
  - Appends a synchronous or asynchronous request message (solid line `―▶` or `―>`).
- `reply(source: Participant, target: Participant, label: str = "", is_async: bool = False, style: Style | None = None) -> Message`
  - Appends a return/response message (dashed line `---▶` or `--->`).
- `connect(source: Participant, target: Participant, label: str = "", arrow: str = "->", is_async: bool = False, style: Style | None = None) -> Message`
  - Appends a custom connection line (e.g. bidirectional stream with `arrow="<->"`).
- `note(text: str, on: Participant | None = None, over: list[Participant] | None = None, pos: str = "right", style: Style | None = None) -> Note`
  - Appends a note annotation on a single participant or spanning multiple participants.
- `loop(label: str = "") -> Block`
  - Returns a context manager block for repeated actions (`with d.loop("Retry up to 3 times"): ...`).
- `alt(label: str = "") -> Block`
  - Returns a context manager block for alternative conditional branches (`with d.alt("Status == 200"): ...`).
- `else_(label: str = "") -> Block`
  - Returns a context manager block for else branches (`with d.else_("Error"): ...`).
- `opt(label: str = "") -> Block`
  - Returns a context manager block for optional steps (`with d.opt("Cache valid"): ...`).
- `par(label: str = "") -> Block`
  - Returns a context manager block for parallel actions.
- `space(dy: float = 5.0) -> None`
  - Advances timeline vertically by an extra `dy` units to create manual spacing.
- `draw(xy: tuple[float, float] = (0.0, 0.0)) -> None`
  - Executes the 2-pass layout calculation and renders the sequence diagram to canvas.

---

### 3.2. `Participant` (Lifeline Entity)

Represents an actor, service, microservice, or system component with a vertical lifeline.

#### Constructor
```python
class Participant:
    def __init__(
        self,
        text: str = "",
        icon: IconType = None,
        icon_size: float = 8.0,
        text_position: Literal["bottom", "top", "left", "right"] = "bottom",
        style: Style | None = None,
        icon_style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None: ...
```

#### Public Methods
- `request(target: Participant, label: str = "", is_async: bool = False, style: Style | None = None) -> Message`
  - Fluent shortcut: creates and records a request message to `target`.
- `reply(target: Participant, label: str = "", is_async: bool = False, style: Style | None = None) -> Message`
  - Fluent shortcut: creates and records a response message to `target`.
- `connect(target: Participant, label: str = "", arrow: str = "->", is_async: bool = False, style: Style | None = None) -> Message`
  - Fluent shortcut: creates and records a custom/bidirectional connection to `target`.
- `note(text: str, pos: Literal["left", "right"] = "right", style: Style | None = None) -> Note`
  - Fluent shortcut: attaches a note annotation to this participant's lifeline at the current step.
- `activate() -> None`
  - Starts an execution activation bar on this participant's lifeline.
- `deactivate() -> None`
  - Ends the current activation bar on this participant's lifeline.

---

### 3.3. `Message` (Interaction Arrow)

Represents a horizontal message communication between two lifelines (or a self-call loop).

#### Attributes & Methods
- `source: Participant`: Sending participant.
- `target: Participant`: Receiving participant.
- `label: str`: Message text description.
- `is_reply: bool`: Whether line is dashed (`True`) or solid (`False`).
- `is_async: bool`: Whether arrowhead is open stick (`True`) or filled triangular (`False`).
- `arrow: Literal["->", "<->", "-"]`: Arrowhead directionality.
- `padding: float | tuple[float, float]`: Gap clearance between lifelines and line endpoints.
- `set_label(text: str) -> Message`
- `set_async(is_async: bool = True) -> Message`
- `set_reply(is_reply: bool = True) -> Message`
- `set_arrow(arrow: str) -> Message`
- `set_style(style: Style) -> Message`
- `set_textstyle(textstyle: Style) -> Message`
- `set_padding(padding: float | tuple[float, float]) -> Message`

#### Self-Calls (`source == target`)
When `source` and `target` are identical (e.g., `auth.request(auth, "Verify Token")`), the message is automatically routed as a 3-segment orthogonal loop returning to the same lifeline:
$$(x, y) \longrightarrow (x + \text{loop\_w}, y) \longrightarrow (x + \text{loop\_w}, y - \Delta y) \longrightarrow (x, y - \Delta y)$$

---

### 3.4. `Note` (Text Annotation)

Represents an informative sticky memo or explanatory text block.

#### Types of Notes
1. **Single-Participant Note**: Positioned to the `"left"` or `"right"` of a participant's lifeline.
2. **Multi-Participant Note**: Positioned `"over"` multiple participants, centered and spanning their lifelines.

#### Constructor & API
```python
class Note:
    def __init__(
        self,
        text: str,
        on: Participant | None = None,
        over: list[Participant] | None = None,
        pos: Literal["left", "right", "over"] = "right",
        style: Style | None = None,
        textstyle: Style | None = None,
    ) -> None: ...
```

---

### 3.5. `Block` (Context Manager Framing Box)

Represents grouped boundaries such as condition branches (`alt` / `else`), loops (`loop`), optionals (`opt`), or parallel executions (`par`).

#### Usage with Python `with`
```python
with d.loop("Retry 3 times"):
    client.request(server, "Ping")
    server.reply(client, "503 Error")

with d.alt("Authorized"):
    server.reply(client, "200 OK (Token)")
with d.else_("Unauthorized"):
    server.reply(client, "401 Unauthorized")
```

---

### 3.6. `ParticipantGroup` (Participant Boundary Box)

Represents a top-level grouping box enclosing a subset of participant headers (equivalent to Mermaid's `box "Group" ... end`).

```python
vpc = d.add_group(ParticipantGroup("VPC Backend", style=Style(fill_color=(240, 245, 255, 0.5))))
vpc.add(api)
vpc.add(db)
```

---

## 4. Arrow and Message Semantics Summary

| Method / Call | Visual Appearance | Meaning / Intent |
|---|---|---|
| `a.request(b, "Call")` | 実線 ＋ 塗り矢印 `―▶` | 通常の同期リクエスト（Call / Invoke） |
| `a.request(b, "Call", is_async=True)` | 実線 ＋ 開き矢印 `―>` | 非同期リクエスト（Fire-and-forget / Push） |
| `b.reply(a, "Result")` | 破線 ＋ 塗り矢印 `---▶` | 戻り値・正常応答（Response / Return） |
| `b.reply(a, "Callback", is_async=True)` | 破線 ＋ 開き矢印 `--->` | 非同期応答・コールバック |
| `a.connect(b, "Sync", arrow="<->")` | 実線 ＋ 両端矢印 `◀―▶` | 双方向ストリーム（WebSocket, Session Sync） |
| `a.request(a, "Internal")` | 3辺ループ ＋ 矢印 | 内部処理・自己呼び出し（Self-Call） |

---

## 5. Layout and Rendering Engine

### 5.1. Pass 1: Timeline & Geometry Resolution
1. **$X$-Axis Resolution**:
   - Order of participants in `d.participants`.
   - Calculate column width $W_{\text{col}} = \max(\text{col\_width}, \text{header\_width})$.
   - Compute coordinate $x_i = \text{pad\_left} + i \cdot W_{\text{col}}$ for each participant.
2. **$Y$-Axis Progression**:
   - Start from $y = H_{\text{header}}$.
   - For each chronological event:
     - Message: $y \leftarrow y - \Delta y_{\text{step}}$. If label has multiple lines, expand $\Delta y$.
     - Note: $y \leftarrow y - \Delta y_{\text{note}}$ based on note height.
     - Block entry / exit: Record $y$-boundary markers.
     - Spacer: $y \leftarrow y - \Delta y_{\text{space}}$.
3. **Total Diagram Sizing**:
   - Compute total $W_{\text{total}}$ and $H_{\text{total}}$ from resolved coordinates plus padding.

### 5.2. Pass 2: Multi-Layer Canvas Drawing
- **Layer 0: Background & Group Boxes**:
  - Participant header group boxes (`ParticipantGroup`).
  - Framing boundary boxes (`Block`: `alt`, `loop`, etc.) with title tab in upper-left.
- **Layer 1: Lifelines**:
  - Vertical dashed lines extending from each participant header to the bottom of the diagram.
- **Layer 2: Activation Bars**:
  - Slender filled vertical rectangles drawn along lifelines over active ranges.
- **Layer 3: Messages & Arrows**:
  - Horizontal lines / self-call loops with arrowheads.
  - Centered text labels with clean background backplates.
  - Automatic step numbering (`autonumber=True` renders `1. Label`, `2. Label`, ...).
- **Layer 4: Notes**:
  - Rectangular callout boxes with text placed beside or across lifelines.
- **Layer 5: Participant Headers (and Optional Footers)**:
  - Header cards, icons, and titles drawn at the top.

---

<p align="center"><em>Approved technical specification for drawlib sequence diagrams.</em></p>
