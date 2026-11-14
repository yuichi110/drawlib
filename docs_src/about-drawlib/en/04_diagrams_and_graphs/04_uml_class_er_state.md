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
# Domain Modeling: Class, ER & State Diagrams
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=uml_class_er_state.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.diagrams.er import Entity, ERDiagram
from drawlib.diagrams.state import FinalState, InitialState, State, StateDiagram
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=176, height=82)

# 1. Left Panel: ClassDiagram
p_cls = Panel(
    "ClassDiagram (UML 2.0)",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    icon=phosphor.cube,
    icon_style=Styles.PrimaryBold,
    header_height=8.0,
)
p_cls.draw((2.0, 2.0), width=55.5, height=78.0)

cd = ClassDiagram(
    node_style=Styles.Neutral.patch(text_size=11.0),
    header_style=Styles.PrimaryFlat.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
    margin=1.5,
)
base = cd.add(
    ClassNode("Exporter", is_abstract=True, width=36.0, header_height=7.8, row_height=4.2)
    .add_attribute("dpi", "int")
    .add_method("render", "", "bytes", is_abstract=True),
    xy=(25.5, 48.0),
)
svg_c = cd.add(
    ClassNode("SvgExporter", width=23.0, header_height=5.8, row_height=4.2, header_style=Styles.SecondaryNeutral.patch(text_size=11.5))
    .add_attribute("xml", "bool")
    .add_method("render", "", "bytes"),
    xy=(12.5, 16.0),
)
pdf_c = cd.add(
    ClassNode("PdfExporter", width=23.0, header_height=5.8, row_height=4.2, header_style=Styles.SecondaryNeutral.patch(text_size=11.5))
    .add_attribute("cmyk", "bool")
    .add_method("render", "", "bytes"),
    xy=(38.5, 16.0),
)
cd.connect(svg_c, base, "inheritance", start_side="top", end_side="bottom")
cd.connect(pdf_c, base, "inheritance", start_side="top", end_side="bottom")

(cx, cy), cw, ch = p_cls.get_content_box((2.0, 2.0), width=55.5, height=78.0, padding=(1.5, 1.5))
cd.draw(xy=(cx + cw / 2.0, cy + ch / 2.0), align="center")

# 2. Center Panel: ERDiagram
p_er = Panel(
    "ERDiagram (Schema)",
    style=Styles.White,
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    icon=phosphor.database,
    icon_style=Styles.SecondaryBold,
    header_height=8.0,
)
p_er.draw((60.25, 2.0), width=55.5, height=78.0)

erd = ERDiagram(
    node_style=Styles.Neutral.patch(text_size=11.0),
    header_style=Styles.SecondaryNeutral.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
)
users = erd.add(
    Entity("USERS", width=38.0, header_height=4.8, row_height=3.8)
    .add_column("id", "UUID", pk=True)
    .add_column("email", "TEXT"),
    xy=(25.0, 54.5),
)
orders = erd.add(
    Entity("ORDERS", width=38.0, header_height=4.8, row_height=3.8, header_style=Styles.PrimaryNeutral.patch(text_size=11.5))
    .add_column("id", "UUID", pk=True)
    .add_column("user_id", "UUID", fk=True),
    xy=(25.0, 31.5),
)
items = erd.add(
    Entity("ORDER_ITEMS", width=38.0, header_height=4.8, row_height=3.8)
    .add_column("id", "INT", pk=True)
    .add_column("order_id", "UUID", fk=True),
    xy=(25.0, 8.5),
)
erd.connect(users, orders, cardinality="1:*", start_side="bottom", end_side="top", label="places")
erd.connect(orders, items, cardinality="1:1..*", start_side="bottom", end_side="top", label="contains")

(ex, ey), ew, eh = p_er.get_content_box((60.25, 2.0), width=55.5, height=78.0, padding=(1.5, 1.5))
erd.draw(xy=(ex + ew / 2.0, ey + eh / 2.0), align="center")

# 3. Right Panel: StateDiagram
p_st = Panel(
    "StateDiagram (FSM)",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    icon=phosphor.git_commit,
    icon_style=Styles.PrimaryBold,
    header_height=8.0,
)
p_st.draw((118.5, 2.0), width=55.5, height=78.0)

sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
    margin=1.5,
)
init = sd.add(InitialState(), xy=(25.5, 60.5))
queued = sd.add(State("Queued", width=22.0, height=7.8, style=Styles.Neutral.patch(text_size=11.5)), xy=(25.5, 49.5))
rendering = sd.add(State("Rendering", width=22.0, height=7.8, style=Styles.PrimaryNeutral.patch(text_size=11.5)), xy=(25.5, 34.0))
cached = sd.add(State("Cached", width=22.0, height=7.8, style=Styles.SuccessNeutral.patch(text_size=11.5)), xy=(12.0, 17.5))
failed = sd.add(State("Failed", width=22.0, height=7.8, style=Styles.DangerNeutral.patch(text_size=11.5)), xy=(39.0, 17.5))
final = sd.add(FinalState(), xy=(25.5, 4.5))

sd.connect(init, queued, routing="direct", padding=0.6)
sd.connect(
    queued,
    rendering,
    label="start",
    routing="direct",
    text_style=Styles.DarkBold.patch(text_size=11.0, xy_shift=(4.5, 0.5)),
    padding=0.6,
)
sd.connect(
    rendering,
    cached,
    label="ok",
    start_side="left",
    end_side="top",
    routing="orthogonal",
    text_style=Styles.DarkBold.patch(text_size=11.0, xy_shift=(-3.5, -1.5)),
    padding=0.6,
)
sd.connect(
    rendering,
    failed,
    label="err",
    start_side="right",
    end_side="top",
    routing="orthogonal",
    style=Styles.DangerBold,
    text_style=Styles.DangerBold.patch(text_size=11.0, xy_shift=(3.8, -1.5)),
    padding=0.6,
)
sd.connect(cached, final, start_side="bottom", end_side="left", routing="orthogonal", padding=0.6)
sd.connect(failed, final, start_side="bottom", end_side="right", routing="orthogonal", padding=0.6)

(sx, sy), sw, sh = p_st.get_content_box((118.5, 2.0), width=55.5, height=78.0, padding=(1.5, 1.5))
sd.draw(xy=(sx + sw / 2.0, sy + sh / 2.0), align="center")
save()
```
:::

::: note
**Domain Modeling with `ClassDiagram`, `ERDiagram`, and `StateDiagram`**:
- **`ClassDiagram` (Left)**: Renders three-compartment UML 2.0 classes (`ClassNode`) with stereotypes (`<<abstract>>`, `<<interface>>`), member visibility (`+`, `-`, `#`, `~`), and all 6 canonical UML relationships (`inheritance`, `realization`, `composition`, `aggregation`, `dependency`, `association`).
- **`ERDiagram` (Center)**: Models relational database schemas (`USERS`, `ORDERS`, `ORDER_ITEMS`) using Information Engineering Crow's Foot notation (`1:*`, `1:1..*`) with aligned `PK` / `FK` constraint columns and optional row-level foreign key anchoring.
- **`StateDiagram` (Right)**: Expresses UML 2.x finite state machines (`InitialState` → `Queued` → `Rendering` → `Cached` / `Failed` → `FinalState`) with pseudo-states, `entry/do/exit` compartments, and orthogonal or curved transitions.
:::
