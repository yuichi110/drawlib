# ClassDiagram: UML 2.0 Class Hierarchies & Relationships

`ClassDiagram` implements standard UML 2.0 Object-Oriented structural modeling. It features three-compartment class cards (class name, attributes, methods), stereotypes, abstract classes, and all 6 standard UML relationships.

```drawlib code=fold align=center file=class_diagram_overview_anatomy.png caption="Three-Compartment UML Class Cards with Realization and Composition"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=102, height=58)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
)

payment_svc = cd.add(
    ClassNode(name="PaymentService", stereotype="interface", width=30.0, style=Styles.PrimaryNeutral),
    xy=(20.0, 44.0),
)
payment_svc.add_method("pay", params="amount", return_type="bool")

stripe_svc = cd.add(
    ClassNode(name="StripeService", width=30.0, style=Styles.Neutral),
    xy=(20.0, 14.0),
)
stripe_svc.add_attribute("api_key", type="str", is_public=False)
stripe_svc.add_method("pay", params="amount", return_type="bool")

tx = cd.add(
    ClassNode(name="Transaction", width=28.0, style=Styles.SecondaryNeutral),
    xy=(81.0, 14.0),
)
tx.add_attribute("id", type="UUID", is_public=True)
tx.add_attribute("amount", type="Decimal", is_public=True)

cd.connect(
    stripe_svc,
    payment_svc,
    relationship_type="realization",
    start_side="top",
    end_side="bottom",
    label="realizes",
)
cd.connect(
    stripe_svc,
    tx,
    relationship_type="composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="records",
)

cd.draw(xy=(2.0, 2.0))
save()
```

---

## 1. Core Concepts & Basic Usage

`ClassDiagram` places three-compartment `ClassNode` cards by their **Center `(cx, cy)`** via `cd.add(node, xy=(cx, cy))`, dynamically expanding `effective_height` as attributes and methods with UML visibility modifiers (`+`, `-`, `#`, `~`) are registered. You can annotate headers with guillemet `stereotype` badges, `is_abstract`, and custom `header_style` fills, connect classes using all 6 standard UML `relationship_type` markers with multiplicities, and control port sides, `show=False` visibility, or `align="center"` placement:

```drawlib code=fold align=center file=class_diagram_parameter_tour.png caption="Basic Usage & Parameter Tour: 3-Compartment Cards & Anchors, Stereotypes & Modifiers, UML Relationships & Multiplicity, and Routing & Reveal (APNG Animation)"
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.icons import code as code_icons
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
from drawlib.styles import Colors, Styles
from drawlib.text import text

W, H = 138.0, 82.0
setup(width=W, height=H)
anim = Animation(fps=10.0, loop=0)

CODE_TEXT_SIZE = 10.0
PT_TO_CANVAS = W / 720.0
FONT_CANVAS = CODE_TEXT_SIZE * PT_TO_CANVAS
LINE_H = FONT_CANVAS * 1.8
PAD_Y = FONT_CANVAS * 1.2

CODE_STYLES = SourceCodeStyles.get("default", font_lang="en", text_size=CODE_TEXT_SIZE).patch(
    box_style=Styles.Neutral.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=0),
)

PANE_HEADER = Styles.Neutral.patch(
    shape_fill_color=(238, 243, 250),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
EDITOR_BODY = Styles.Neutral.patch(
    shape_fill_color=(250, 252, 255),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
TAKEAWAY_BODY = Styles.Neutral.patch(
    shape_fill_color=(242, 246, 253),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)
STUDIO_BODY = Styles.Neutral.patch(
    shape_fill_color=(239, 243, 249),
    shape_line_color=(203, 213, 225),
    shape_line_width=1.2,
    shape_r=0.0,
)

PART_ITEMS = [
    ("1. Cards & Members", "Center xy & 3 compartments"),
    ("2. Stereotypes", "interface, abstract & header"),
    ("3. Relationships", "Realize, Compose & 1..*"),
    ("4. Ports & Reveal", "Sides, show=False & center"),
]


def draw_step_bar(active_part: int) -> None:
    """Draw top 4-part progress bar (active_part is 1..4)."""
    pill_w = 31.0
    pill_h = 7.4
    gap = 2.0
    start_x = 4.0 + pill_w / 2.0
    cy = 75.2

    for idx, (label, sublabel) in enumerate(PART_ITEMS, start=1):
        cx = start_x + (idx - 1) * (pill_w + gap)
        if idx > 1:
            prev_cx = cx - (pill_w + gap)
            line(
                (prev_cx + pill_w / 2.0 + 0.2, cy),
                (cx - pill_w / 2.0 - 0.2, cy),
                style=Styles.PrimaryBold if idx <= active_part else Styles.MutedThin,
            )

        if idx == active_part:
            st = Styles.PrimaryFlat.patch(shape_r=1.4)
            tst = Styles.WhiteBold.patch(text_size=10.3)
            sub_tst = Styles.White.patch(text_size=9.5)
        elif idx < active_part:
            st = Styles.PrimaryNeutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.PrimaryBold.patch(text_size=10.3)
            sub_tst = Styles.Primary.patch(text_size=9.5)
        else:
            st = Styles.Neutral.patch(shape_r=1.4, shape_line_width=1.1)
            tst = Styles.MutedBold.patch(text_size=10.3)
            sub_tst = Styles.Muted.patch(text_size=9.5)

        rectangle((cx, cy), width=pill_w, height=pill_h, style=st)
        text((cx, cy + 1.35), label, style=tst)
        text((cx, cy - 1.55), sublabel, style=sub_tst)


def draw_left_pane(
    active_part: int,
    code_lines: list[str],
    hl_range: tuple[int, int],
    icon_fn: object,
    summary_title: str,
    summary_line1: str,
    summary_line2: str,
) -> None:
    """Draw left Python code editor + bottom concept takeaway card."""
    x0, w = 4.0, 63.5
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    editor_h = 43.8
    takeaway_h = 15.8

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    code_icons.python((x0 + 3.6, top_y + header_h / 2.0), width=3.4, style=Styles.Neutral)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "class_tour.py",
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (x0 + w - 2.6, top_y + header_h / 2.0),
        f"Part {active_part} / 4",
        style=Styles.PrimaryBold.patch(text_size=9.8, halign="right"),
    )

    rectangle((cx, top_y - editor_h / 2.0), width=w, height=editor_h, style=EDITOR_BODY)

    hl_start, hl_end = hl_range
    hl_top = top_y - PAD_Y - hl_start * LINE_H
    hl_bot = top_y - PAD_Y - (hl_end + 1) * LINE_H
    hl_cy = (hl_top + hl_bot) / 2.0
    hl_h = hl_top - hl_bot
    rectangle(
        (cx, hl_cy),
        width=w - 0.6,
        height=hl_h,
        style=Styles.Neutral.patch(shape_fill_color=(229, 239, 255), shape_line_width=0),
    )
    rectangle(
        (x0 + 0.55, hl_cy),
        width=0.9,
        height=hl_h,
        style=Styles.PrimaryFlat.patch(shape_line_width=0),
    )

    SourceCode.draw(
        xy=(x0, top_y),
        width=w,
        code="\n".join(code_lines),
        styles=CODE_STYLES,
        code_lang="python",
        show_linenum=True,
        align="top_left",
    )

    take_cy = 3.6 + takeaway_h / 2.0
    rectangle((cx, take_cy), width=w, height=takeaway_h, style=TAKEAWAY_BODY)
    circle(
        (x0 + 6.4, take_cy),
        radius=3.3,
        style=Styles.PrimaryNeutral.patch(shape_line_width=1.2),
    )
    icon_fn((x0 + 6.4, take_cy), width=3.8, style=Styles.PrimaryBold)  # type: ignore[operator]
    text(
        (x0 + 11.4, take_cy + 3.6),
        summary_title,
        style=Styles.DarkBold.patch(text_size=10.4, halign="left"),
    )
    text(
        (x0 + 11.4, take_cy - 0.2),
        summary_line1,
        style=Styles.Dark.patch(text_size=9.7, halign="left"),
    )
    text(
        (x0 + 11.4, take_cy - 3.8),
        summary_line2,
        style=Styles.PrimaryBold.patch(text_size=9.6, halign="left"),
    )


def draw_geometry_studio(param_badge: str, footer_caption: str) -> tuple[float, float]:
    """Draw right geometry lab shell, inner coordinate sheet with subtle grid, and footer."""
    x0, w = 70.0, 64.0
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    body_h = 59.6

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    phosphor.ruler((x0 + 3.6, top_y + header_h / 2.0), width=3.4, style=Styles.Primary)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "Live Geometry & Guides",
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (x0 + w - 2.6, top_y + header_h / 2.0),
        param_badge,
        style=Styles.PrimaryBold.patch(text_size=9.6, halign="right"),
    )

    rectangle((cx, 3.6 + body_h / 2.0), width=w, height=body_h, style=STUDIO_BODY)

    sheet_cx, sheet_cy = cx, 36.2
    sheet_w, sheet_h = 54.0, 40.0
    sx0, sy0 = sheet_cx - sheet_w / 2.0, sheet_cy - sheet_h / 2.0
    rectangle(
        (sheet_cx, sheet_cy),
        width=sheet_w,
        height=sheet_h,
        style=Styles.Neutral.patch(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(180, 194, 214),
            shape_line_width=1.2,
        ),
    )
    g_st = Styles.MutedThin.patch(line_color=(232, 238, 246), line_width=0.8)
    for gx in range(1, 6):
        vx = sx0 + gx * (sheet_w / 6.0)
        line((vx, sy0), (vx, sy0 + sheet_h), style=g_st)
    for gy in range(1, 5):
        vy = sy0 + gy * (sheet_h / 5.0)
        line((sx0, vy), (sx0 + sheet_w, vy), style=g_st)

    rectangle(
        (cx, 8.4),
        width=59.2,
        height=5.2,
        style=Styles.Neutral.patch(
            shape_fill_color=(255, 255, 255),
            shape_line_color=(203, 213, 225),
            shape_line_width=1.1,
            shape_r=2.4,
        ),
        text=footer_caption,
        text_style=Styles.DarkBold.patch(text_size=9.8),
    )
    return sheet_cx, sheet_cy


def draw_sub_pills(scx: float, labels: list[str], active_idx: int) -> None:
    """Draw 3-step tracker pills near the top of the studio sheet."""
    pw, ph, pgap = 16.2, 4.2, 0.9
    p_start = scx - (3 * pw + 2 * pgap) / 2.0 + pw / 2.0
    for idx, lbl in enumerate(labels):
        px = p_start + idx * (pw + pgap)
        if idx == active_idx:
            pst = Styles.PrimaryFlat.patch(shape_r=1.2)
            ptst = Styles.WhiteBold.patch(text_size=9.5)
        elif idx < active_idx:
            pst = Styles.PrimaryNeutral.patch(shape_r=1.2, shape_line_width=1.0)
            ptst = Styles.PrimaryBold.patch(text_size=9.5)
        else:
            pst = Styles.Neutral.patch(shape_r=1.2, shape_line_width=1.0)
            ptst = Styles.Muted.patch(text_size=9.5)
        rectangle((px, 52.0), width=pw, height=ph, style=pst, text=lbl, text_style=ptst)


EDGE_TXT = Styles.Dark.patch(text_size=9.5)

# =========================================================================
# Part 1: Cards & Members — Center xy & 3-compartment effective_height
# =========================================================================
PART1_STATES = [
    (
        1,
        3.3,
        [
            "cd = ClassDiagram(",
            "    node_style=Styles.Neutral,",
            "    edge_style=Styles.DarkBold,",
            "    edge_text_style=Styles.Dark)",
            "order = cd.add(",
            '    ClassNode("Order", width=24),',
            "    xy=(16, 13))  # card center",
            "",
            "# Base bottom-left diagram origin",
            "cd.draw(xy=(4, 4))",
        ],
        (4, 9),
        "ClassNode + xy",
        "Step 1: Center ClassNode at xy=(16, 13), Draw at (4, 4)",
        "1. Center-Placed Card & Base Origin",
        "cd.add(node, xy) places each card by center (cx, cy)",
        "cd.draw(xy) shifts the diagram from bottom-left (x0, y0)",
    ),
    (
        2,
        3.3,
        [
            "cd = ClassDiagram(...)",
            "order = cd.add(",
            '    ClassNode("Order", width=24),',
            "    xy=(16, 13))",
            "order.add_attribute(",
            '    "id", type="UUID")',
            "order.add_attribute(",
            '    "total", type="float",',
            "    is_public=False)  # '-'",
            "cd.draw(xy=(4, 4))",
        ],
        (4, 8),
        "add_attribute()",
        "Step 2: Attributes Compartment & '+' / '-' Visibility",
        "2. Attribute Compartment & Modifiers",
        "add_attribute() opens the middle field compartment",
        "is_public=True -> '+' prefix; is_public=False -> '-'",
    ),
    (
        3,
        3.5,
        [
            "cd = ClassDiagram(...)",
            "order = cd.add(",
            '    ClassNode("Order", width=24),',
            "    xy=(16, 13))",
            'order.add_attribute("id", "UUID")',
            "order.add_attribute(",
            '    "total", "float", False)',
            "order.add_method(",
            '    "pay", return_type="bool")',
            "cd.draw(xy=(4, 4))",
        ],
        (7, 8),
        "add_method()",
        "Step 3: 3rd Method Compartment & Auto Height Expansion",
        "3. Three Compartments & effective_height",
        "add_method() adds a divider + operations compartment",
        "effective_height expands automatically (8.2 -> 17.8)",
    ),
]

for p1_idx, (step_n, dur, code_1, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART1_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(1, code_1, hl_rng, phosphor.cards, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["1. Header Card", "2. + Attributes", "3. + Methods"], p1_idx)

        bx, by = 83.0, 21.0
        cd = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.DarkBold,
            edge_text_style=EDGE_TXT,
            margin=3.0,
        )
        order = cd.add(
            ClassNode("Order", width=24.0, style=Styles.PrimaryNeutral),
            xy=(17.0, 14.0),
        )
        if step_n >= 2:
            order.add_attribute("id", type="UUID")
            order.add_attribute("total", type="float", is_public=False)
        if step_n >= 3:
            order.add_method("pay", return_type="bool")
        cd.draw(xy=(bx, by))

        card_cx, card_cy = bx + 17.0, by + 14.0
        eff_h = order.effective_height

        # Vertical effective_height callout on right of card
        dim_x = card_cx + 14.2
        line(
            (dim_x, card_cy - eff_h / 2.0),
            (dim_x, card_cy + eff_h / 2.0),
            arrow_head="<->",
            style=Styles.PrimaryBold.patch(line_width=1.2),
        )
        text(
            (dim_x + 1.2, card_cy),
            f"h={eff_h:.1f}",
            style=Styles.PrimaryBold.patch(text_size=9.5, halign="left"),
        )

        # Card center (cx, cy) indicator in Step 1
        if step_n == 1:
            circle((card_cx, card_cy - 1.6), radius=0.95, style=Styles.PrimaryFlat)
            text(
                (card_cx, card_cy + 6.2),
                "card center xy = (16, 13)",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )

        # Red base origin xy=(x0, y0) + +X / +Y axes
        line(
            (bx, by),
            (bx, by + 14.5),
            arrow_head="->",
            style=Styles.DangerBold.patch(line_width=1.3),
        )
        text(
            (bx - 1.0, by + 15.6),
            "+Y",
            style=Styles.DangerBold.patch(text_size=9.5, halign="center"),
        )
        line(
            (bx, by),
            (bx + 11.5, by),
            arrow_head="->",
            style=Styles.DangerBold.patch(line_width=1.3),
        )
        text(
            (bx + 12.3, by),
            "+X",
            style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
        )
        circle((bx, by), radius=1.1, style=Styles.DangerFlat)
        text(
            (bx + 1.8, 18.2),
            "cd.draw(xy=(4, 4))  (base origin)",
            style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
        )

# =========================================================================
# Part 2: Stereotypes — interface, is_abstract/visibility & header_style
# =========================================================================
PART2_STATES = [
    (
        "stereotype",
        3.3,
        [
            "cd = ClassDiagram(...)",
            "gw = cd.add(",
            "    ClassNode(",
            '        "Gateway",',
            '        stereotype="interface",',
            "        width=22),",
            "    xy=(14, 15))",
            "gw.add_method(",
            '    "charge", params="amt",',
            '    return_type="bool")',
        ],
        (2, 5),
        '«interface»',
        'stereotype="interface": Renders «interface» Guillemets',
        '1. UML Stereotypes («interface»)',
        "Adds guillemet badge above the class title",
        "Header compartment auto-expands from 5.2 to 6.5",
    ),
    (
        "abstract_mod",
        3.3,
        [
            "job = cd.add(ClassNode(",
            '    "BaseJob", is_abstract=True,',
            "    width=22), xy=(40, 15))",
            "job.add_attribute(",
            '    "retries", type="int",',
            '    visibility="#",',
            "    is_static=True)",
            "job.add_method(",
            '    "run", return_type="void",',
            "    is_abstract=True)",
        ],
        (1, 9),
        "abstract & '#'",
        "is_abstract=True + Protected '#' & Member Flags",
        "2. Abstract Classes & '#' / '~' Visibility",
        "is_abstract=True tags «abstract» when no stereotype",
        "visibility='#' or '~' overrides public/private prefix",
    ),
    (
        "header_style",
        3.5,
        [
            "HDR = Styles.PrimaryFlat.patch(",
            "    text_color=Colors.White)",
            "gw = cd.add(",
            "    ClassNode(",
            '        "Gateway",',
            '        stereotype="interface",',
            "        header_style=HDR),",
            "    xy=(14, 15))",
            'job = cd.add(ClassNode("BaseJob",',
            "    is_abstract=True), ...)",
        ],
        (0, 6),
        "header_style",
        "header_style: Hero PrimaryFlat Header on Focal Interface",
        "3. Custom Header Compartment Styling",
        "Override header_style per ClassNode or diagram-wide",
        "Keep 50%+ sibling classes grounded in Neutral styles",
    ),
]

for p2_idx, (s_mode, dur, code_2, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART2_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(2, code_2, hl_rng, phosphor.brackets_curly, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["«interface»", "is_abstract", "header_style"], p2_idx)

        cd = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.DarkBold,
            edge_text_style=EDGE_TXT,
        )
        hdr_st = Styles.PrimaryFlat.patch(text_color=Colors.White) if s_mode == "header_style" else None

        if s_mode == "stereotype":
            gw = cd.add(
                ClassNode("Gateway", stereotype="interface", width=26.0, style=Styles.PrimaryNeutral),
                xy=(scx, 34.5),
            )
            gw.add_method("charge", params="amt", return_type="bool")
            cd.draw(xy=(0.0, 0.0))
            text(
                (scx, 43.2),
                'stereotype="interface"  ->  «interface»',
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
            text(
                (scx, 19.2),
                "header_height auto-expands (5.2 -> 6.5) for guillemets",
                style=Styles.DarkBold.patch(text_size=9.5),
            )
        else:
            gw = cd.add(
                ClassNode(
                    "Gateway",
                    stereotype="interface",
                    width=21.5,
                    style=Styles.PrimaryNeutral if s_mode == "abstract_mod" else Styles.Neutral,
                    header_style=hdr_st,
                ),
                xy=(88.5, 34.5),
            )
            gw.add_method("charge", params="amt", return_type="bool")

            job = cd.add(
                ClassNode(
                    "BaseJob",
                    is_abstract=True,
                    header_height=6.5,
                    width=21.5,
                    style=Styles.SecondaryNeutral,
                ),
                xy=(115.2, 34.5),
            )
            job.add_attribute("retries", type="int", visibility="#", is_static=True)
            job.add_method("run", return_type="void", is_abstract=True)
            cd.draw(xy=(0.0, 0.0))

            if s_mode == "abstract_mod":
                text(
                    (115.2, 44.5),
                    "«abstract» + # retries",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )
                text(
                    (scx, 18.8),
                    "visibility: '+' public  •  '-' private  •  '#' protected  •  '~' pkg",
                    style=Styles.DarkBold.patch(text_size=9.5),
                )
            else:
                text(
                    (88.5, 43.2),
                    "PrimaryFlat header",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )
                text(
                    (115.2, 44.5),
                    "Calm Neutral sibling",
                    style=Styles.DarkBold.patch(text_size=9.5),
                )
                text(
                    (scx, 18.8),
                    "focal PrimaryFlat header + calm Neutral sibling (50%+ rule)",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )

# =========================================================================
# Part 3: Relationships — All 6 UML relationship_type markers & 1..*
# =========================================================================
PART3_STATES = [
    (
        "inherit_realize",
        3.3,
        [
            "# Generalization (solid triangle)",
            "cd.connect(",
            "    admin, user,",
            "    relationship_type=(",
            '        "inheritance"))',
            "# Interface impl (dashed)",
            "cd.connect(",
            "    stripe_svc, pay_port,",
            "    relationship_type=(",
            '        "realization"))',
        ],
        (1, 9),
        "Inherit / Realize",
        "inheritance (Solid) & realization (Dashed) Hollow Triangles",
        "1. Generalization & Interface Realization",
        "inheritance draws solid stroke + hollow triangle",
        "realization draws dashed stroke + hollow triangle",
    ),
    (
        "compose_agg",
        3.3,
        [
            "cd.connect(",
            "    order, line_item,",
            "    relationship_type=(",
            '        "composition"),',
            '    start_multiplicity="1",',
            '    end_multiplicity="*",',
            '    label="owns")',
            "cd.connect(",
            "    team, member,",
            '    "aggregation", ...)',
        ],
        (2, 6),
        "Compose & 1..*",
        "composition (Filled) & aggregation (Hollow) Diamonds + 1..*",
        "2. Whole-Part Diamonds & Multiplicities",
        "composition = filled diamond; aggregation = hollow",
        "start/end_multiplicity & label annotate endpoints",
    ),
    (
        "depend_assoc",
        3.5,
        [
            "# Uses-a (dashed + open arrow)",
            "cd.connect(",
            "    checkout, tax_api,",
            "    relationship_type=(",
            '        "dependency"),',
            '    label="uses")',
            "# Navigable association (->)",
            "cd.connect(",
            "    customer, cart,",
            '    "association",',
            "    directed=True)",
        ],
        (1, 10),
        "Depend & Assoc",
        "dependency (Dashed) & Directed association (Solid) Arrows",
        "3. Dependency & Navigable Association",
        "dependency renders dashed stroke + open arrowhead",
        "association adds open arrow when directed=True",
    ),
]

for p3_idx, (rel_mode, dur, code_3, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART3_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(3, code_3, hl_rng, phosphor.git_branch, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Inherit/Realize", "Compose + 1..*", "Depend & Assoc"], p3_idx)

        cd = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.DarkBold,
            edge_text_style=EDGE_TXT,
        )
        xl, xr = 84.8, 119.2
        yt, yb = 40.8, 25.0

        if rel_mode == "inherit_realize":
            n1 = cd.add(ClassNode("Admin", width=15.4, header_height=4.4, style=Styles.PrimaryNeutral), xy=(xl, yt))
            n2 = cd.add(ClassNode("User", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yt))
            cd.connect(n1, n2, relationship_type="inheritance", start_side="right", end_side="left")

            n3 = cd.add(ClassNode("StripeSvc", width=15.4, header_height=4.4, style=Styles.SecondaryNeutral), xy=(xl, yb))
            n4 = cd.add(ClassNode("PayPort", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yb))
            cd.connect(n3, n4, relationship_type="realization", start_side="right", end_side="left")
            cd.draw(xy=(0.0, 0.0))

            text((scx, 46.5), '"inheritance"  (solid + hollow triangle)', style=Styles.PrimaryBold.patch(text_size=9.5))
            text((scx, 18.6), '"realization"  (dashed + hollow triangle)', style=Styles.DarkBold.patch(text_size=9.5))
        elif rel_mode == "compose_agg":
            n1 = cd.add(ClassNode("Order", width=15.4, header_height=4.4, style=Styles.PrimaryNeutral), xy=(xl, yt))
            n2 = cd.add(ClassNode("LineItem", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yt))
            cd.connect(
                n1,
                n2,
                relationship_type="composition",
                start_side="right",
                end_side="left",
                start_multiplicity="1",
                end_multiplicity="*",
                label="owns",
            )

            n3 = cd.add(ClassNode("Team", width=15.4, header_height=4.4, style=Styles.SecondaryNeutral), xy=(xl, yb))
            n4 = cd.add(ClassNode("Member", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yb))
            cd.connect(
                n3,
                n4,
                relationship_type="aggregation",
                start_side="right",
                end_side="left",
                start_multiplicity="1",
                end_multiplicity="*",
                label="has",
            )
            cd.draw(xy=(0.0, 0.0))

            text((scx, 46.5), '"composition"  (filled diamond + 1..* owns)', style=Styles.PrimaryBold.patch(text_size=9.5))
            text((scx, 18.6), '"aggregation"  (hollow diamond + 1..* has)', style=Styles.DarkBold.patch(text_size=9.5))
        else:
            n1 = cd.add(ClassNode("Checkout", width=15.4, header_height=4.4, style=Styles.PrimaryNeutral), xy=(xl, yt))
            n2 = cd.add(ClassNode("TaxAPI", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yt))
            cd.connect(
                n1,
                n2,
                relationship_type="dependency",
                start_side="right",
                end_side="left",
                label="uses",
            )

            n3 = cd.add(ClassNode("Customer", width=15.4, header_height=4.4, style=Styles.SecondaryNeutral), xy=(xl, yb))
            n4 = cd.add(ClassNode("Cart", width=15.4, header_height=4.4, style=Styles.Neutral), xy=(xr, yb))
            cd.connect(
                n3,
                n4,
                relationship_type="association",
                directed=True,
                start_side="right",
                end_side="left",
            )
            cd.draw(xy=(0.0, 0.0))

            text((scx, 46.5), '"dependency"  (dashed + open arrow)', style=Styles.PrimaryBold.patch(text_size=9.5))
            text((scx, 18.6), '"association"  (solid + directed=True)', style=Styles.DarkBold.patch(text_size=9.5))

# =========================================================================
# Part 4: Ports & Reveal — start/end_side, routing, show=False & center
# =========================================================================
PART4_STATES = [
    (
        "ports_routing",
        3.3,
        [
            "# Orthogonal elbow vs direct line",
            "cd.connect(",
            '    svc, audit, "dependency",',
            '    start_side="right",',
            '    end_side="top",',
            '    routing="orthogonal")',
            "cd.connect(",
            '    repo, audit, "association",',
            "    directed=True,",
            '    routing="direct")',
        ],
        (3, 9),
        "Sides & Routing",
        'Explicit Port Sides + "orthogonal" vs "direct" Routing',
        "1. Explicit Port Sides & Routing Modes",
        "Pin start_side / end_side to top, bottom, left, right",
        "Choose crisp orthogonal elbows or direct rays",
    ),
    (
        "hide_node",
        3.3,
        [
            "audit = cd.add(",
            '    ClassNode("AuditLog"),',
            "    xy=(38, 14.5))",
            "cd.connect(",
            '    svc, audit, "dependency")',
            "cd.connect(",
            '    repo, audit, "association")',
            "# Hides card + incident edges!",
            "audit.show = False",
            "cd.draw(xy=(4, 4))",
        ],
        (7, 8),
        "show = False",
        "audit.show=False: Auto-Hides Card & Incident Relationships",
        "2. Layout-Stable Visibility (show = False)",
        "Hides AuditLog card and both connected UML edges",
        "Remaining cards stay locked at exact coordinates",
    ),
    (
        "center_align",
        3.5,
        [
            "cd = ClassDiagram(...)",
            'svc = cd.add(ClassNode("Svc"),',
            "    xy=(10, 22))",
            'repo = cd.add(ClassNode("Repo"),',
            "    xy=(10, 7))",
            "audit = cd.add(",
            '    ClassNode("AuditLog"), ...)',
            "# Center diagram bounds on xy",
            "cd.draw(",
            "    xy=(34, 20),",
            '    align="center")',
        ],
        (7, 10),
        'align="center"',
        'align="center": Centers Enclosing Bounds on xy=(cx, cy)',
        '3. Centered Placement (align="center")',
        "Centers cd.get_bounds() midpoint directly on xy",
        "Ideal for balanced cards, grids, and split panels",
    ),
]

for p4_idx, (p4_mode, dur, code_4, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART4_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(4, code_4, hl_rng, phosphor.crosshair, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Ports & Route", "show = False", 'align="center"'], p4_idx)

        cd = ClassDiagram(
            node_style=Styles.Neutral,
            edge_style=Styles.DarkBold,
            edge_text_style=EDGE_TXT,
            margin=0.0,
        )
        svc = cd.add(ClassNode("Svc", width=17.0, header_height=4.4, style=Styles.PrimaryNeutral), xy=(10.0, 22.0))
        repo = cd.add(ClassNode("Repo", width=17.0, header_height=4.4, style=Styles.SecondaryNeutral), xy=(10.0, 7.2))
        audit = cd.add(
            ClassNode("AuditLog", width=17.5, header_height=4.4, style=Styles.Neutral),
            xy=(38.0, 14.6),
            show=(p4_mode != "hide_node"),
        )
        cd.connect(svc, repo, relationship_type="composition", start_side="bottom", end_side="top")
        cd.connect(
            svc,
            audit,
            relationship_type="dependency",
            start_side="right",
            end_side="top",
            routing="orthogonal",
        )
        cd.connect(
            repo,
            audit,
            relationship_type="association",
            directed=True,
            start_side="right",
            end_side="left",
            routing="direct",
        )

        if p4_mode == "ports_routing":
            bx, by = 78.0, 19.6
            cd.draw(xy=(bx, by))
            for px, py in ((bx + 18.5, by + 22.0), (bx + 38.0, by + 18.3), (bx + 18.5, by + 7.2), (bx + 29.25, by + 14.6)):
                circle((px, py), radius=0.8, style=Styles.DangerFlat)
            text(
                (109.5, 44.3),
                'routing="orthogonal"',
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
            text(
                (113.5, 25.8),
                'routing="direct"',
                style=Styles.DarkBold.patch(text_size=9.5),
            )
            text(
                (scx, 18.5),
                "elbow (right->top) vs. direct ray (right->left)",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        elif p4_mode == "hide_node":
            bx, by = 78.0, 19.6
            cd.draw(xy=(bx, by))
            rectangle(
                (bx + 38.0, by + 14.6),
                width=17.5,
                height=7.4,
                style=Styles.MutedDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.1, shape_r=1.0),
            )
            text(
                (bx + 38.0, by + 14.6),
                "show=False",
                style=Styles.MutedBold.patch(text_size=9.5),
            )
            text(
                (scx, 18.5),
                "AuditLog + 2 edges auto-hide  •  Svc & Repo stay locked",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            cx_a, cy_a = scx, 34.2
            cd.draw(xy=(cx_a, cy_a), align="center")
            min_x, min_y, max_x, max_y = cd.get_bounds()
            bw, bh = max_x - min_x, max_y - min_y
            rectangle(
                (cx_a, cy_a),
                width=bw,
                height=bh,
                style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.2),
            )
            line((cx_a - bw / 2.0 - 2.3, cy_a), (cx_a - bw / 2.0, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a + bw / 2.0, cy_a), (cx_a + bw / 2.0 + 2.3, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a + bh / 2.0), (cx_a, cy_a + bh / 2.0 + 2.3), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a - bh / 2.0 - 2.3), (cx_a, cy_a - bh / 2.0), style=Styles.DangerBold.patch(line_width=1.5))
            circle(
                (cx_a, cy_a),
                radius=1.55,
                style=Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0),
            )
            circle((cx_a, cy_a), radius=1.1, style=Styles.DangerFlat)
            text(
                (cx_a, 18.5),
                'xy = (cx, cy)  •  align="center"',
                style=Styles.DangerBold.patch(text_size=9.5),
            )

save()
```

- **Three-Compartment `ClassNode` & Dynamic Height (`xy`, `effective_height`)**: `cd.add(node, xy=(cx, cy))` places each class card by its center while `add_attribute(...)` and `add_method(...)` populate compartments and expand `node.effective_height` automatically.
- **Visibility, Stereotypes & Header Styling (`+`/`-`/`#`/`~`, `stereotype`, `is_abstract`, `header_style`)**: Format members with UML access modifiers, display guillemet headers (`«interface»`, `«abstract»`), and style focal headers via `header_style`.
- **Six Standard UML Relationships (`relationship_type`, Multiplicities & Roles)**: `cd.connect(...)` renders `"inheritance"`, `"realization"`, `"composition"`, `"aggregation"`, `"association"` (`directed=True`), and `"dependency"` with `start_multiplicity`, `end_multiplicity`, `start_role`, `end_role`, and `label`.
- **Port Routing, Progressive Reveal & Centering (`start_side`/`end_side`, `routing`, `show=False`, `align="center"`)**: Pin exact attachment sides with `"orthogonal"` or `"direct"` paths, hide nodes and incident edges in place via `show=False`, or center the diagram on `xy` via `align="center"`.

---

## 2. Constructor, `ClassNode` & Member Declarations

```drawlib code=show align=center file=class_diagram_basic_node.png caption="Basic Class and Interface Nodes"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=76, height=36)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    title="Domain Model",
    title_style=Styles.BlackBold.patch(text_size=13.5),
)

# Class with attributes and methods
user = cd.add(ClassNode(name="User", width=26.0), xy=(18.0, 13.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", params="password: str", return_type="bool")

# Interface with stereotype
gateway = cd.add(
    ClassNode(name="PaymentGateway", stereotype="interface", width=28.0, style=Styles.PrimaryNeutral),
    xy=(57.0, 13.0),
)
gateway.add_method("charge", params="amount: float", return_type="bool")

cd.draw(xy=(0.0, 0.0))
save()
```

### Parameter Reference Tables

#### `ClassDiagram` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `node_style` | `Style` | *(Required)* | Base `Style` object for class cards in the diagram. |
| `edge_style` | `Style` | *(Required)* | Base `Style` object for relationship lines and UML markers. |
| `edge_text_style` | `Style` | *(Required)* | Base `Style` object for relationship labels, roles, and multiplicities. |
| `title` | `str` | `""` | Optional title displayed above the diagram. |
| `title_style` | `Style \| None` | `None` | Optional `Style` object for the diagram title. |
| `style` | `Style \| None` | `None` | Optional `Style` overriding the overall diagram background. |
| `width` | `float \| None` | `None` | Optional fixed canvas width (auto-calculated from content if `None`). |
| `height` | `float \| None` | `None` | Optional fixed canvas height (auto-calculated from content if `None`). |
| `margin` | `float` | `5.0` | Outer margin padding surrounding all classes when auto-calculating size. |
| `header_style` | `Style \| None` | `None` | Optional `Style` overriding class card header compartments across the diagram. |

#### `ClassNode` Class
| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | *(Required)* | Class or interface name. |
| `stereotype` | `str` | `""` | Optional UML stereotype rendered as `«stereotype»` (e.g. `"interface"`, `"abstract"`, `"enumeration"`). |
| `is_abstract` | `bool` | `False` | When `True`, renders the class name in italic font. |
| `width` | `float` | `28.0` | Width of the class card in canvas units. |
| `height` | `float \| None` | `None` | Optional minimum height override (auto-expands to fit attributes/methods if `None` or smaller). |
| `size` | `tuple[float, float] \| None` | `None` | Optional `(width, height)` shorthand tuple overriding `width` and `height`. |
| `header_height` | `float \| None` | `None` | Height of the header compartment (`6.5` when `stereotype` is set, otherwise `5.2`). |
| `row_height` | `float` | `3.2` | Vertical height of each attribute and method line. |
| `style` | `Style \| None` | `None` | Optional `Style` override for the card border and body fill. |
| `header_style` | `Style \| None` | `None` | Optional `Style` override for this card's header compartment background and text. |
| `show` | `bool` | `True` | Visibility flag (connected `ClassRelationship` edges auto-hide when `False`). |

### Attribute & Method Declaration API (`AttributeInfo` & `MethodInfo`)

```python
from drawlib.diagrams.class_diagram import AttributeInfo, MethodInfo

# Single attribute & batch attributes
node.add_attribute(
    name: str,
    type: str = "",
    is_public: bool = True,
    visibility: str | None = None,      # "+", "-", "#", or "~" (overrides is_public if set)
    default_value: str = "",            # Rendered as " = <default_value>"
    is_static: bool = False,
) -> ClassNode

node.add_attributes(
    attributes: Sequence[Sequence[Any] | AttributeInfo],
    # Each tuple is (name, [type, is_public, visibility, default_value]) or an AttributeInfo instance
) -> ClassNode

# Single method & batch methods
node.add_method(
    name: str,
    params: str = "",
    return_type: str = "",
    is_public: bool = True,
    visibility: str | None = None,      # "+", "-", "#", or "~" (overrides is_public if set)
    is_static: bool = False,
    is_abstract: bool = False,
) -> ClassNode

node.add_methods(
    methods: Sequence[Sequence[Any] | MethodInfo],
    # Each tuple is (name, [return_type, params, is_public, visibility]) or a MethodInfo instance
) -> ClassNode
```

---

## 3. The 6 UML Relationship Types (`ClassRelationship`)

Relationships between classes are registered at the diagram level via `cd.connect(source, target, relationship_type=...)` (or `cd.add_relationship(rel: ClassRelationship) -> ClassRelationship`):

| `relationship_type` | Shorthand Alias | Relationship | Line Stroke | Marker | Semantic Meaning |
|---|---|---|---|---|---|
| `"inheritance"` | `"inherit"` | **Inheritance** | Solid | Hollow Triangle (at `target`) | Superclass generalization |
| `"realization"` | `"realize"` | **Realization** | Dashed | Hollow Triangle (at `target`) | Interface implementation |
| `"composition"` | `"composite"` | **Composition** | Solid | Filled Diamond (at `source`) | Strong lifecycle ownership |
| `"aggregation"` | `"aggregate"` | **Aggregation** | Solid | Hollow Diamond (at `source`) | Shared lifecycle / part-whole |
| `"association"` | `"associate"` | **Association** | Solid | None (or Open Arrow if `directed=True`) | Structural reference |
| `"dependency"` | `"depend"` | **Dependency** | Dashed | Open Arrow (at `target`) | Uses-a dependency |

```drawlib code=show align=center file=class_diagram_relationship_types.png caption="All Six UML Relationship Types and Marker Styles in ClassDiagram"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=128, height=84)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
)

# 2x3 Grid of the 6 UML Relationship Types
specs = [
    # Left column (x_src=14, x_dst=49)
    ("1. Inheritance (solid + hollow triangle)", "inheritance", False, 14.0, 49.0, 64.0, "SubClass", "SuperClass"),
    ("3. Composition (solid + filled diamond)", "composition", False, 14.0, 49.0, 38.0, "Order", "LineItem"),
    ("5. Association (directed=True)", "association", True, 14.0, 49.0, 12.0, "Customer", "Cart"),
    # Right column (x_src=79, x_dst=114)
    ("2. Realization (dashed + hollow triangle)", "realization", False, 79.0, 114.0, 64.0, "Impl", "Interface"),
    ("4. Aggregation (solid + hollow diamond)", "aggregation", False, 79.0, 114.0, 38.0, "Team", "Member"),
    ("6. Dependency (dashed + open arrow)", "dependency", False, 79.0, 114.0, 12.0, "Client", "Service"),
]

lbl_style = Styles.DarkBold.patch(text_size=10.5, text_color=Colors.Primary5)

for _title_str, rel_type, is_dir, x1, x2, y, src_name, dst_name in specs:
    n_src = cd.add(ClassNode(name=src_name, width=17.0, style=Styles.PrimaryNeutral), xy=(x1, y))
    n_dst = cd.add(ClassNode(name=dst_name, width=17.0, style=Styles.Neutral), xy=(x2, y))
    cd.connect(
        n_src,
        n_dst,
        relationship_type=rel_type,
        directed=is_dir,
        start_side="right",
        end_side="left",
    )

cd.draw(xy=(0.0, 0.0))

for title_str, _rel_type, _is_dir, x1, x2, y, _src_name, _dst_name in specs:
    text(((x1 + x2) / 2.0, y + 8.0), title_str, style=lbl_style)

save()
```

### `cd.connect(...)` Signature
```python
cd.connect(
    source: ClassNode,
    target: ClassNode,
    relationship_type: RelationshipType = "association",
    *,
    type: RelationshipType | None = None,              # Keyword alias for relationship_type
    label: str = "",
    start_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
    end_side: Literal["left", "right", "top", "bottom", "auto"] = "auto",
    start_multiplicity: str = "",                      # e.g. "1", "0..1"
    end_multiplicity: str = "",                        # e.g. "*", "1..*"
    start_role: str = "",
    end_role: str = "",
    directed: bool = False,                            # Draws open navigability arrow at target
    style: Style | None = None,
    text_style: Style | None = None,
    routing: Literal["orthogonal", "direct"] = "orthogonal",
    padding: float | tuple[float, float] = 0.0,
    show: bool = True,
) -> ClassRelationship
```

### Registration, Sizing & Rendering Lifecycle
- **`cd.add(class_node, xy=(cx, cy), show: bool | None = None) -> ClassNode`**: Registers a class card centered at `(cx, cy)` and returns the mutable `ClassNode` (`node.show`, `node.style`, `node.header_style`). Hiding a class (`show=False`) also automatically hides all `ClassRelationship` edges connected to it while keeping diagram bounds fixed.
- **`cd.get_bounds() -> tuple[float, float, float, float]`**: Returns `(min_x, min_y, max_x, max_y)` enclosing all registered classes.
- **`cd.get_size() -> tuple[float, float]`**: Returns `(width, height)` of the diagram (including `margin`).
- **`cd.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: Renders the class diagram anchored at bottom-left `xy`, proportionally scaling card widths, compartment heights, UML markers, and typography by `scale`.

---

## 4. E-Commerce Domain Model

The following example combines inheritance, composition, and interface dependency:

```drawlib code=show align=center file=class_diagram_ecommerce_domain.png caption="E-Commerce Domain Class Hierarchy"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=94, height=74)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    title="E-Commerce Domain Class Model",
    title_style=Styles.BlackBold.patch(text_size=13.5),
)

# 1. Define classes
user = cd.add(ClassNode(name="User", width=26.0), xy=(18.0, 51.0))
user.add_attribute("id", type="int", is_public=True)
user.add_attribute("email", type="str", is_public=True)
user.add_attribute("password_hash", type="str", is_public=False)
user.add_method("login", return_type="bool")

customer = cd.add(ClassNode(name="Customer", width=26.0, style=Styles.SecondaryNeutral), xy=(18.0, 14.0))
customer.add_attribute("shipping_address", type="str")
customer.add_method("checkout", return_type="Order")

order = cd.add(ClassNode(name="Order", width=28.0, style=Styles.PrimaryNeutral), xy=(73.0, 14.0))
order.add_attribute("order_id", type="str")
order.add_attribute("total", type="float")
order.add_method("calculate_tax", return_type="float")

iface = cd.add(ClassNode(name="PaymentGateway", stereotype="interface", width=30.0), xy=(73.0, 51.0))
iface.add_method("process_charge", params="amount: float", return_type="bool")

# 2. Connect relationships using diagram.connect
cd.connect(customer, user, "inheritance", start_side="top", end_side="bottom")
cd.connect(
    customer,
    order,
    "composition",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    label="places",
)
cd.connect(order, iface, "dependency", start_side="top", end_side="bottom", label="uses")

cd.draw(xy=(0.0, 0.0))
save()
```

---

## 5. Design Pattern Modeling: Observer Pattern

Class diagrams excel at illustrating software design patterns such as the Observer pattern:

```drawlib code=show align=center file=class_diagram_observer_pattern.png caption="UML Observer Design Pattern"
from drawlib.canvas import save, setup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.styles import Styles

setup(width=92, height=68)

cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    title="UML Observer Design Pattern",
    title_style=Styles.BlackBold.patch(text_size=13.5),
)

subj_iface = cd.add(
    ClassNode(name="Subject", stereotype="interface", width=28.0, style=Styles.PrimaryNeutral),
    xy=(19.0, 47.0),
)
subj_iface.add_method("attach", params="o: Observer", return_type="void")
subj_iface.add_method("notify", return_type="void")

obs_iface = cd.add(
    ClassNode(name="Observer", stereotype="interface", width=28.0, style=Styles.SecondaryNeutral),
    xy=(73.0, 47.0),
)
obs_iface.add_method("update", return_type="void")

concrete_subj = cd.add(ClassNode(name="NewsPublisher", width=28.0), xy=(19.0, 14.0))
concrete_subj.add_attribute("state", type="str", is_public=False)
concrete_subj.add_method("get_state", return_type="str")

concrete_obs = cd.add(ClassNode(name="EmailSubscriber", width=28.0), xy=(73.0, 14.0))
concrete_obs.add_method("update", return_type="void")

cd.connect(concrete_subj, subj_iface, "realization", start_side="top", end_side="bottom")
cd.connect(concrete_obs, obs_iface, "realization", start_side="top", end_side="bottom")
cd.connect(
    subj_iface,
    obs_iface,
    "aggregation",
    start_side="right",
    end_side="left",
    start_multiplicity="1",
    end_multiplicity="*",
    start_role="subject",
    end_role="observers",
)

cd.draw(xy=(0.0, 0.0))
save()
```

---

## 6. Best Practices & Guidelines

1. **Card Width Sizing**: Choose a consistent card width (`26.0` to `30.0` units) across horizontally aligned classes to maintain visual balance.
2. **Explicit Connection Sides**: Specifying `start_side` and `end_side` ensures orthogonal lines route cleanly around cards without cutting through text compartments.
