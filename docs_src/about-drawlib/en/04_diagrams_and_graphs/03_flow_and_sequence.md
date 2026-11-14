::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — Illustration & Documentation as Code*
:::

::: block xy=(80, 36) width=1760 height=72
# Workflows & Protocols: Flow and Sequence
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=flow_and_sequence.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.diagrams.sequence import GcpIcon, Participant, PhosphorIcon, SequenceDiagram
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=176, height=82)

# Left Panel: FlowDiagram (CI/CD Validation Gate)
p_left = Panel(
    "FlowDiagram — CI/CD Validation",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    icon=phosphor.git_branch,
    icon_style=Styles.PrimaryBold,
    header_height=8.0,
)
p_left.draw((2.0, 2.0), width=81.0, height=78.0)

flow = FlowDiagram(
    node_style=Styles.Neutral.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
)
start = flow.add(
    Start("Start", width=22, height=9.0, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=11.5)),
    xy=(21.0, 58.0),
)
build = flow.add(
    Process("Build & Lint", width=26, height=11.0, style=Styles.PrimaryNeutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(21.0, 42.0),
)
check = flow.add(
    Decision("Grid Check\nOK?", width=28, height=15.0, style=Styles.WarningNeutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(21.0, 23.5),
)
deploy = flow.add(
    End("Deploy", width=23, height=9.5, style=Styles.SuccessFlat, text_style=Styles.WhiteBold.patch(text_size=11.5)),
    xy=(21.0, 5.5),
)
autofix = flow.add(
    Process("Auto-Fix\nLoop", width=23, height=12.0, style=Styles.SecondaryNeutral, text_style=Styles.DarkBold.patch(text_size=11.5)),
    xy=(58.5, 23.5),
)

start.connect(build, padding=0.8)
build.connect(check, padding=0.8)
check.connect(deploy, label="Yes", start_side="bottom", end_side="top", padding=0.8)
check.connect(autofix, label="No", start_side="right", end_side="left", routing="direct", padding=0.8)
autofix.connect(build, label="Retry", start_side="top", end_side="right", routing="orthogonal", padding=0.8)
flow.draw(xy=(5.5, 4.0))

# Right Panel: SequenceDiagram (4 Participants + Activation + Alt)
p_right = Panel(
    "SequenceDiagram — API Protocol",
    style=Styles.White,
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    icon=phosphor.arrows_left_right,
    icon_style=Styles.SecondaryBold,
    header_height=8.0,
)
p_right.draw((86.0, 2.0), width=88.0, height=78.0)

seq = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=11.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
    node_card_style=Styles.Neutral,
    col_width=20.0,
    step_y=6.8,
    margin=2.5,
)
client = seq.add(Participant("Client", width=16.5, height=12.0, icon=PhosphorIcon.USER, icon_size=5.0))
gw = seq.add(
    Participant("API Gateway", width=17.5, height=12.0, icon=GcpIcon.CLOUD_ENDPOINTS, icon_size=5.0, card_style=Styles.PrimaryNeutral)
)
auth = seq.add(Participant("Auth", width=16.5, height=12.0, icon=PhosphorIcon.SHIELD_CHECK, icon_size=5.0))
db = seq.add(
    Participant("Order DB", width=16.5, height=12.0, icon=GcpIcon.CLOUD_SQL, icon_size=5.0, card_style=Styles.SecondaryNeutral)
)

gw.activate()
client.request(gw, "POST /orders")
auth.activate()
gw.request(auth, "Verify JWT")
auth.deactivate()
auth.reply(gw, "200 OK")

with seq.alt("JWT OK") as blk:
    blk.style = Styles.MutedDashed
    seq.space(2.4)
    gw.request(db, "INSERT order", is_async=True)
    gw.deactivate()
    gw.reply(client, "201 Created")

(rx, ry), rw, rh = p_right.get_content_box((86.0, 2.0), width=88.0, height=78.0, padding=(2.0, 1.5))
seq.draw(xy=(rx + rw / 2.0, ry + rh / 2.0), align="center")
save()
```
:::

::: note
**Workflows & Interaction Protocols (`FlowDiagram` & `SequenceDiagram`)**:
- **Left (`FlowDiagram`)**: Implements ISO 5807 / JIS X 0121 flowchart shapes (`Start`, `Process`, `Decision`, `Data`, `End`) plus optional vertical or horizontal swimlanes (`Lane`). Explicit side anchoring (`start_side="right"`, `end_side="left"`) produces clean orthogonal decision branches and loopback paths—here illustrating Drawlib's own CI/CD visual grid-check loop.
- **Right (`SequenceDiagram`)**: Models chronological interactions across lifelines (`Client`, `API Gateway`, `Auth`, `Order DB`) without manual Y-axis calculation. Supports synchronous requests (`request`), dashed return messages (`reply`), asynchronous fire-and-forget calls (`is_async=True`), lifeline activation spans (`activate()` / `deactivate()`), and Python `with` context blocks (`alt`, `loop`, `opt`, `par`).
:::
