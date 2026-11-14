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
# KPIs, Feature Cards, Pyramids & MindMaps
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=cards_kpi_hierarchy.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList, KpiCards, MindMapNode, Panel, Pyramid
from drawlib.styles import Styles

clear()
setup(width=176, height=81)

# 1. Top-Left Panel: KpiCards (2x2 Grid)
p_tl = Panel(
    "KpiCards — Metric Grid",
    "2x2 Layout",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.gauge,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tl.draw((1.5, 42.2), width=84.5, height=37.5)
tl_xy, tl_w, tl_h = p_tl.get_content_box((1.5, 42.2), width=84.5, height=37.5, padding=(3.0, 2.2))

kpi = KpiCards(
    style=Styles.White.patch(shape_r=1.8),
    metric_style=Styles.PrimaryBold.patch(text_size=16.5),
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.8),
    accent_style=Styles.PrimaryFlat,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.32,
    spacing=2.4,
)
kpi.add("18", "SmartArt Types", "Tables to GeoMaps")
kpi.add("34", "Icon Suites", "Cloud & Phosphor", accent_style=Styles.SecondaryFlat)
kpi.add("0", "GUI Lock-In", "100% Git Python", accent_style=Styles.DarkFlat)
kpi.add("4", "Theme Palettes", "Instant re-skin", accent_style=Styles.AccentFlat)
kpi.draw(tl_xy, width=tl_w, height=tl_h, columns=2)

# 2. Top-Right Panel: CardList (3 Icon/Badge Feature Cards)
p_tr = Panel(
    "CardList — Feature Stack",
    "Icon + Badge",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.stack,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_tr.draw((90.0, 42.2), width=84.5, height=37.5)
tr_xy, tr_w, tr_h = p_tr.get_content_box((90.0, 42.2), width=84.5, height=37.5, padding=(3.0, 2.2))

cl = CardList(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=11.8),
    description_style=Styles.Muted.patch(text_size=10.6),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.0),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=1.8,
)
cl.add(
    "Declarative Item Lifecycle",
    "Register via .add() and chain .draw()",
    badge_text="L1",
    icon=phosphor.code,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.0),
    icon_style=Styles.WhiteBold,
)
cl.add("Semantic Design Tokens", "50%+ neutral base with focal highlights", badge_text="L2", icon=phosphor.palette)
cl.add("Animation-Ready Visibility", "Toggle item.show without shifting layout", badge_text="L3", icon=phosphor.eye)
cl.draw(tr_xy, width=tr_w, height=tr_h)

# 3. Bottom-Left Panel: Pyramid (3 Architectural Tiers)
p_bl = Panel(
    "Pyramid — Layered Hierarchy",
    "3 Tiers",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.sliders,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_bl.draw((1.5, 1.5), width=84.5, height=37.5)
bl_xy, _, bl_h = p_bl.get_content_box(
    (1.5, 1.5), width=84.5, height=37.5, padding=(6.0, 2.2), content_align="center"
)

pyr = Pyramid(
    style=Styles.White,
    text_style=Styles.DarkBold.patch(text_size=12.0),
)
pyr.add(
    "Deck",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=11.2),
)
pyr.add("SmartArts", style=Styles.PrimaryNeutral)
pyr.add("Vector Canvas", style=Styles.SecondaryNeutral)
pyr.draw(bl_xy, width=68.0, height=bl_h, margin=1.4, direction="bottom", order="vertex_to_base", align="center")

# 4. Bottom-Right Panel: MindMapNode (Root + 2 Left & 2 Right Leaves)
p_br = Panel(
    "MindMapNode — Radial Tree",
    "2-Pass Layout",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.0),
    description_style=Styles.Muted.patch(text_size=11.2),
    icon=phosphor.tree_structure,
    icon_style=Styles.PrimaryBold,
    header_height=6.4,
)
p_br.draw((90.0, 1.5), width=84.5, height=37.5)
br_xy, _, _ = p_br.get_content_box(
    (90.0, 1.5), width=84.5, height=37.5, padding=(3.0, 2.2), content_align="center"
)

leaf_left_style = Styles.PrimaryNeutral.patch(shape_r=1.5)
leaf_right_style = Styles.SecondaryNeutral.patch(shape_r=1.5)
leaf_txt = Styles.DarkBold.patch(text_size=11.5)

mm = MindMapNode(
    "Drawlib",
    shape="ellipse",
    width=21.0,
    height=9.2,
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=12.5),
    line_style=Styles.DarkBold,
    line_length=6.2,
    horizontal_margin=3.0,
    vertical_margin=3.6,
    children=[
        MindMapNode("SmartArts", branch="left", shape="rectangle", width=21.0, height=7.8, style=leaf_left_style, text_style=leaf_txt),
        MindMapNode("10 Charts", branch="left", shape="rectangle", width=21.0, height=7.8, style=leaf_left_style, text_style=leaf_txt),
        MindMapNode("Diagrams", branch="right", shape="rectangle", width=21.0, height=7.8, style=leaf_right_style, text_style=leaf_txt),
        MindMapNode("Slide & Doc", branch="right", shape="rectangle", width=21.0, height=7.8, style=leaf_right_style, text_style=leaf_txt),
    ],
)
mm.draw(xy=br_xy)

save()
```
:::

::: note
Here we see four high-density summary and hierarchy components arranged in a 2×2 `Panel` dashboard:
- **`KpiCards`** renders multi-column executive scorecards with accent pills and dedicated metric columns.
- **`CardList`** pairs numbered or labeled badges and Phosphor vector icons with concise feature descriptions.
- **`Pyramid`** builds clean proportional hierarchies from apex to foundation—ideal for testing pyramids, defense-in-depth layers, or architectural stacks.
- **`MindMapNode`** uses a two-pass layout solver to route right-angled connectors symmetrically across left and right branches around a central root node.
:::
