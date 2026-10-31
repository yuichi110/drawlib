# CardList（カードリスト）

`CardList` コンポーネントは、円形または角丸矩形のバッジ（`badge_shape`）、ベクターアイコン（`icon`）、番号・テキストラベル（`badge_text`）、カードタイトル（`text`）、複数行の説明文（`description`）、およびオプションのカード間接続矢印（`show_arrows=True`）を備えたリッチなカードを、垂直スタック（`direction="vertical"`）または水平ステップシーケンス（`direction="horizontal"`）として描画します。
隙間なく単一ラベルのボックスを並べる [`BoxList`](./box_list.md) や、大きな数値指標を強調する [`KpiCards`](./kpi_cards.md) とは異なり、`CardList` は**機能カタログ、多層防御レイヤーの解説、複数ステップのエンジニアリングワークフロー**に特化して設計されています。

```drawlib code=fold align=center file=smartarts_cardlist_hero.png caption="CardList の配置モード: 垂直機能スタックと矢印付き水平ワークフローシーケンス"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle
from drawlib.smartarts import CardList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=58)

# Subtle center divider
line((64.5, 4.0), (64.5, 54.0), style=Styles.MutedDashed)

# 1. Left Panel: Vertical Feature Stack (direction="vertical", badge_shape="rounded_rect")
phosphor.list_bullets(xy=(5.5, 51.0), width=3.4, style=Styles.PrimaryFlat)
text((10.0, 52.5), "1. Vertical Stack (direction='vertical')", style=Styles.BlackBold.patch(text_size=10.5, halign="left"))

cl_v = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=9.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=2.5,
)
cl_v.add(
    "Edge Anycast Scrubbing",
    "Drop volumetric UDP/SYN floods",
    badge_text="L1",
    icon=phosphor.shield_check,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
    icon_style=Styles.WhiteBold,
)
cl_v.add("WAF Rate Limiting", "Throttle suspicious ASN & JA3", badge_text="L2", icon=phosphor.funnel)
cl_v.add("Origin Zero-Trust mTLS", "Verify workload identity", badge_text="L3", icon=phosphor.lock_key)
cl_v.draw(xy=(5.0, 8.0), width=55.5, height=40.0)

circle((5.0, 8.0), radius=1.1, style=Styles.DangerFlat)
text((5.0, 3.8), "xy=(5, 8) [Bottom-Left]", style=Styles.DangerBold.patch(text_size=10.0, halign="left"))

# 2. Right Panel: Horizontal Step Sequence (direction="horizontal", show_arrows=True)
phosphor.arrows_left_right(xy=(68.5, 51.0), width=3.4, style=Styles.PrimaryFlat)
text((73.0, 52.5), "2. Horizontal Steps (show_arrows=True)", style=Styles.BlackBold.patch(text_size=10.5, halign="left"))

cl_h = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.0),
    description_style=Styles.Muted.patch(text_size=9.5),
    badge_shape="circle",
    badge_style=Styles.PrimaryNeutral,
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    show_arrows=True,
    arrow_style=Styles.Dark,
    spacing=4.2,
)
cl_h.add("1. Code", "Python API\nin Markdown", icon=phosphor.code)
cl_h.add("2. Build", "Headless SVG\n& HTML build", icon=phosphor.gear)
cl_h.add(
    "3. Review",
    "Grid check &\nself-healing",
    icon=phosphor.eye,
    badge_style=Styles.PrimaryFlat,
    icon_style=Styles.WhiteBold,
)
cl_h.draw(xy=(68.5, 11.0), width=58.5, height=35.0)

circle((68.5, 11.0), radius=1.1, style=Styles.DangerFlat)
text((68.5, 3.8), "xy=(68.5, 11) [Bottom-Left]", style=Styles.DangerBold.patch(text_size=10.0, halign="left"))

save()
```

---

## 1. 基本概念と基本的な使い方

`CardList` は `.add(...)` で段階的に構築した垂直方向の機能スタック（`direction="vertical"`）または水平方向のステップシーケンス（`direction="horizontal"`）を描画し、デフォルトでバウンディングボックスの**左下角 `(x, y)`**（`align="center"` の場合は中央）を基準に配置します。先頭バッジを `"rounded_rect"`・`"circle"`・`"none"` から選択できるほか、カード間のワークフロー矢印（`show_arrows=True`）の有効化や、他のカードのスロット位置を保ったまま `.items[i]` を個別変更・非表示化する操作に対応しています。

```drawlib code=fold align=center file=card_list_parameter_tour.png caption="基本的な使い方とパラメータツアー: 垂直・水平カード、バッジ形状、ワークフロー矢印、動的なアイテム制御（APNG アニメーション）"
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import code as code_icons
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import CardList, SourceCode, SourceCodeStyles
from drawlib.styles import Styles
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
    ("1. Stack & .add()", "badges, icons & text"),
    ("2. Badge Shapes", "rounded_rect, circle, none"),
    ("3. Flow & Arrows", "horizontal & show_arrows"),
    ("4. Focus & Align", "show=False & center"),
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
        "cardlist_tour.py",
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


TITLE_DARK = Styles.DarkBold.patch(text_size=10.2)
DESC_DARK = Styles.Muted.patch(text_size=9.5)
BADGE_TXT = Styles.PrimaryBold.patch(text_size=9.5)
TITLE_WHITE = Styles.WhiteBold.patch(text_size=10.2)
DESC_WHITE = Styles.White.patch(text_size=9.5)

# =========================================================================
# Part 1: Stack & .add() — Bottom-Left Anchor & Progressive Vertical Stack
# =========================================================================
STACK_STATES = [
    (
        1,
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral,",
            "    text_style=Styles.DarkBold,",
            "    description_style=Styles.Dark,",
            "    badge_style=(",
            "        Styles.PrimaryNeutral),",
            "    icon_style=Styles.PrimaryBold)",
            'cl.add("Edge WAF", "SYN filter",',
            '       badge_text="01", icon=waf)',
            "cl.draw((10, 12), width=45,",
            "        height=27)",
        ],
        (7, 10),
        "Card 1 / 3",
        "Step 1: Anchor Bottom-Left xy=(10, 12) in 45 × 27",
        "1. Bottom-Left Anchor & First Card",
        "xy=(x, y) pins the bottom-left bounding-box corner",
        "1 card fills height=27 until more cards are added",
    ),
    (
        2,
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...)",
            'cl.add("Edge WAF", "SYN filter",',
            '       badge_text="01", icon=waf)',
            "cl.add(",
            '    "Rate Limit",',
            '    "ASN throttle",',
            '    badge_text="02",',
            "    icon=phosphor.funnel)",
            "cl.draw((10, 12), width=45,",
            "        height=27)",
        ],
        (4, 8),
        "Card 2 / 3",
        "Step 2: Subdivide height=27 Top-to-Bottom",
        "2. Top-to-Bottom Subdivision (.add())",
        "Vertical stacks place items[0] at top, growing down",
        "Each card pairs badge_text, icon, title & description",
    ),
    (
        3,
        3.5,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...)",
            'cl.add("Edge WAF", ..., icon=waf)',
            'cl.add("Rate Limit", ...)',
            "cl.add(",
            '    "Zero-Trust",',
            '    "Verify mTLS",',
            '    badge_text="03",',
            "    icon=phosphor.lock_key)",
            "cl.draw((10, 12), width=45,",
            "        height=27)",
        ],
        (4, 8),
        "Card 3 / 3",
        "Step 3: 3-Card Stack With 1 Focal Primary Badge",
        "3. Complete 3-Card Feature Stack",
        "Neutral card surfaces keep multi-row lists calm",
        "Use PrimaryFlat on 1 badge to anchor visual entry",
    ),
]

for s_idx, (n_cards, dur, code_s, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(STACK_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(1, code_s, hl_rng, phosphor.rows, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["1 Card", "2 Cards", "3 Cards"], s_idx)

        px0, py0, pw_tot, ph_tot = 80.5, 20.0, 45.0, 27.0

        cl = CardList(
            style=Styles.Neutral,
            text_style=TITLE_DARK,
            description_style=DESC_DARK,
            badge_shape="rounded_rect",
            badge_style=Styles.PrimaryNeutral,
            badge_text_style=BADGE_TXT,
            icon_style=Styles.PrimaryBold,
            direction="vertical",
            spacing=1.8,
        )
        cl.add(
            "Edge WAF",
            "SYN filter",
            badge_text="01",
            icon=phosphor.shield_check,
            badge_style=Styles.PrimaryFlat,
            badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
            icon_style=Styles.WhiteBold,
        )
        if n_cards >= 2:
            cl.add("Rate Limit", "ASN throttle", badge_text="02", icon=phosphor.funnel)
        if n_cards >= 3:
            cl.add("Zero-Trust", "Verify mTLS", badge_text="03", icon=phosphor.lock_key)
        cl.draw(xy=(px0, py0), width=pw_tot, height=ph_tot)

        rectangle(
            (px0 + pw_tot / 2.0, py0 + ph_tot / 2.0),
            width=pw_tot,
            height=ph_tot,
            style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.2),
        )
        text(
            (px0 + pw_tot / 2.0, py0 + ph_tot + 1.45),
            "target: 45 × 27",
            style=Styles.PrimaryBold.patch(text_size=9.5),
        )

        # Bottom-Left xy anchor dot + +X / +Y Cartesian axes
        line(
            (px0, py0),
            (px0, py0 + 11.2),
            arrow_head="->",
            style=Styles.DangerBold.patch(line_width=1.4),
        )
        text(
            (px0 - 2.7, py0 + 10.6),
            "+Y",
            style=Styles.DangerBold.patch(text_size=9.5),
        )
        line(
            (px0, py0),
            (px0 + 11.2, py0),
            arrow_head="->",
            style=Styles.DangerBold.patch(line_width=1.4),
        )
        text(
            (px0 + 12.0, py0 - 2.0),
            "+X",
            style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
        )
        circle((px0, py0), radius=1.15, style=Styles.DangerFlat)
        text(
            (px0 + 19.5, py0 - 2.0),
            "xy=(10, 12) [bottom-left]",
            style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
        )

# =========================================================================
# Part 2: Badge Shapes — "rounded_rect", "circle", and "none"
# =========================================================================
BADGE_STATES = [
    (
        "rounded_rect",
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral,",
            "    text_style=Styles.DarkBold,",
            "    description_style=Styles.Dark,",
            '    badge_shape="rounded_rect",',
            "    badge_style=(",
            "        Styles.PrimaryNeutral),",
            "    icon_style=Styles.PrimaryBold)",
            'cl.add("Edge WAF", "SYN filter",',
            "       icon=phosphor.shield_check)",
            "cl.draw((10, 13), 45, 24)",
        ],
        (4, 4),
        "rounded_rect",
        'badge_shape="rounded_rect": Soft Square Badge',
        'Rounded Square Badge ("rounded_rect")',
        "Default badge container with subtle corner radius",
        "Pairs cleanly with vector icons or short L1/01 tags",
    ),
    (
        "circle",
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral,",
            "    text_style=Styles.DarkBold,",
            "    description_style=Styles.Dark,",
            '    badge_shape="circle",',
            "    badge_style=(",
            "        Styles.PrimaryNeutral),",
            "    icon_style=Styles.PrimaryBold)",
            'cl.add("Edge WAF", "SYN filter",',
            "       icon=phosphor.shield_check)",
            "cl.draw((10, 13), 45, 24)",
        ],
        (4, 4),
        'badge_shape="circle"',
        'badge_shape="circle": Circular Icon Medallion',
        'Circular Medallion Badge ("circle")',
        "Draws a circular badge container using badge_style",
        "Great for numbered step sequences and status icons",
    ),
    (
        "none",
        3.4,
        [
            "cl = CardList(",
            "    style=Styles.Neutral,",
            "    text_style=Styles.DarkBold,",
            "    description_style=Styles.Dark,",
            '    badge_shape="none",',
            "    icon_style=Styles.PrimaryBold)",
            'cl.add("Edge WAF", "SYN filter",',
            "       icon=phosphor.shield_check)",
            'cl.add("Zero-Trust", "mTLS auth",',
            "       icon=phosphor.lock_key)",
            "cl.draw((10, 13), 45, 24)",
        ],
        (4, 4),
        'badge_shape="none"',
        'badge_shape="none": Borderless Icon + Title',
        'Borderless Icon Mode ("none")',
        "Omits badge container shape; badge_style not needed",
        "Renders crisp standalone icons directly beside text",
    ),
]

for b_idx, (b_shape, dur, code_b, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(BADGE_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(2, code_b, hl_rng, phosphor.shapes, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["rounded_rect", "circle", "none"], b_idx)

        px0, py0, pw_tot, ph_tot = 79.5, 22.8, 45.0, 23.6

        cl = CardList(
            style=Styles.Neutral,
            text_style=TITLE_DARK,
            description_style=DESC_DARK,
            badge_shape=b_shape,  # type: ignore[arg-type]
            badge_style=Styles.PrimaryNeutral if b_shape != "none" else None,
            icon_style=Styles.PrimaryBold,
            direction="vertical",
            spacing=2.4,
        )
        cl.add(
            "Edge WAF",
            "Drop UDP & SYN floods",
            icon=phosphor.shield_check,
            badge_style=Styles.PrimaryFlat if b_shape != "none" else None,
            icon_style=Styles.WhiteBold if b_shape != "none" else Styles.PrimaryBold,
        )
        cl.add("Zero-Trust", "Verify workload mTLS", icon=phosphor.lock_key)
        cl.draw(xy=(px0, py0), width=pw_tot, height=ph_tot)

        # Callout to bottom card's badge zone
        bx_c, by_c = px0 + 1.8 + 3.15, py0 + 5.3
        line(
            (bx_c, by_c - 3.6),
            (bx_c + 3.5, 18.8),
            style=Styles.PrimaryBold.patch(line_width=1.2),
        )
        note_map = {
            "rounded_rect": 'badge_shape = "rounded_rect" (default)',
            "circle": 'badge_shape = "circle"',
            "none": 'badge_shape = "none" (no badge box)',
        }
        text(
            (bx_c + 4.3, 18.5),
            note_map[b_shape],
            style=Styles.PrimaryBold.patch(text_size=9.5, halign="left"),
        )

# =========================================================================
# Part 3: Flow & Arrows — direction="horizontal" & show_arrows=True
# =========================================================================
FLOW_STATES = [
    (
        "vertical",
        False,
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...,",
            '    badge_shape="circle",',
            '    direction="vertical",',
            "    spacing=2.2,",
            ")",
            'cl.add("Plan", "RFC", icon=i1)',
            'cl.add("Build", "Test", icon=i2)',
            'cl.add("Ship", "Prod", icon=i3)',
            "cl.draw((10, 13), 45, 25)",
        ],
        (3, 4),
        'direction="vertical"',
        'direction="vertical": Top-to-Bottom Card Stack',
        'Vertical Stack (direction="vertical")',
        "Stacks full-width cards with left-aligned badges",
        "Ideal for layered architectures & feature catalogs",
    ),
    (
        "horizontal",
        False,
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...,",
            '    badge_shape="circle",',
            '    direction="horizontal",',
            "    show_arrows=False,",
            "    spacing=2.6)",
            'cl.add("Plan", "RFC", icon=i1)',
            'cl.add("Build", "Test", icon=i2)',
            'cl.add("Ship", "Prod", icon=i3)',
            "cl.draw((9, 15), 47, 22)",
        ],
        (3, 5),
        'direction="horizontal"',
        'direction="horizontal": Left-to-Right Sequence',
        'Horizontal Sequence (direction="horizontal")',
        "Arranges equal-width cards left-to-right across width",
        "Centers badge on top with title & description below",
    ),
    (
        "horizontal",
        True,
        3.5,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...,",
            '    badge_shape="circle",',
            '    direction="horizontal",',
            "    show_arrows=True,",
            "    arrow_style=Styles.PrimaryBold",
            ")",
            'cl.add("Plan", "RFC", icon=i1)',
            'cl.add("Build", "Test", icon=i2)',
            'cl.add("Ship", "Prod", icon=i3)',
            "cl.draw((9, 15), 47, 22)",
        ],
        (3, 5),
        "show_arrows = True",
        "show_arrows=True: Inter-Card Workflow Arrows",
        "Workflow Arrows (show_arrows=True)",
        "Draws '->' connectors across inter-card spacing>=4.2",
        "Requires arrow_style when show_arrows=True",
    ),
]

for f_idx, (dir_mode, arrows_on, dur, code_f, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(FLOW_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(3, code_f, hl_rng, phosphor.arrows_left_right, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Vertical", "Horizontal", "show_arrows"], f_idx)

        cl = CardList(
            style=Styles.Neutral,
            text_style=TITLE_DARK,
            description_style=DESC_DARK,
            badge_shape="circle",
            badge_style=Styles.PrimaryNeutral,
            icon_style=Styles.PrimaryBold,
            direction=dir_mode,  # type: ignore[arg-type]
            spacing=4.2 if arrows_on else (2.0 if dir_mode == "vertical" else 2.6),
            show_arrows=arrows_on,
            arrow_style=Styles.PrimaryBold.patch(line_width=1.6) if arrows_on else None,
        )
        cl.add("Plan", "RFC", icon=phosphor.compass)
        cl.add(
            "Build",
            "Test",
            icon=phosphor.code,
            badge_style=Styles.PrimaryFlat,
            icon_style=Styles.WhiteBold,
        )
        cl.add("Ship", "Prod", icon=phosphor.rocket_launch)

        if dir_mode == "vertical":
            cl.draw(xy=(79.5, 22.0), width=45.0, height=25.0)
            text(
                (scx, 18.5),
                'direction = "vertical"  (top-to-bottom)',
                style=Styles.DarkBold.patch(text_size=9.5),
            )
        else:
            hx0, hy0, hw_tot, hh_tot = 78.5, 24.0, 47.0, 22.0
            cl.draw(xy=(hx0, hy0), width=hw_tot, height=hh_tot)
            if arrows_on:
                cw = (hw_tot - 8.4) / 3.0
                g1_x = hx0 + cw + 2.1
                g2_x = hx0 + 2.0 * cw + 4.2 + 2.1
                for gx_a in (g1_x, g2_x):
                    circle((gx_a, hy0 + hh_tot / 2.0), radius=2.1, style=Styles.DangerDashed.patch(
                        shape_fill_color=(0, 0, 0, 0),
                        shape_line_width=1.2,
                    ))
                    line((gx_a, hy0 + hh_tot / 2.0 - 2.3), (gx_a, 20.6), style=Styles.DangerBold.patch(line_width=1.1))
                text(
                    (scx, 18.6),
                    "show_arrows = True  (connecting '->' arrows)",
                    style=Styles.DangerBold.patch(text_size=9.5),
                )
            else:
                text(
                    (scx, 18.6),
                    'direction = "horizontal"  •  show_arrows = False',
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )

# =========================================================================
# Part 4: Focus & Align — items[1] Hero, show=False & align="center"
# =========================================================================
FOCUS_STATES = [
    (
        "hero_card",
        3.3,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...)",
            'cl.add("1. Plan", "Draft RFC")',
            'cl.add("2. Build", "CI checks")',
            'cl.add("3. Ship", "Canary")',
            "hero = cl.items[1]",
            "hero.style = Styles.PrimaryFlat",
            "hero.text_style = Styles.WhiteBold",
            "hero.description_style = (",
            "    Styles.White)",
            "cl.draw((10, 13), 44, 25)",
        ],
        (5, 9),
        "items[1].style",
        "cl.items[1].style = Styles.PrimaryFlat Hero Card",
        "Per-Card Hero Spotlight (.items[1])",
        "Keep 2/3 cards Neutral and highlight 1 focal card",
        "Pair PrimaryFlat fill with WhiteBold & White text",
    ),
    (
        "hide_card",
        3.4,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...)",
            'cl.add("1. Plan", "Draft RFC")',
            'cl.add("2. Build", "CI checks")',
            'cl.add("3. Ship", "Canary")',
            "",
            "# Hide card; sibling Y slots stay!",
            "cl.items[1].show = False",
            "",
            "cl.draw((10, 13), 44, 25)",
        ],
        (6, 7),
        "items[1].show=False",
        "cl.items[1].show = False: Preserves Sibling Slots",
        "Slot-Preserving Visibility (.show = False)",
        "Skips rendering items[1] (and any adjacent arrow)",
        "items[0] & items[2] hold exact Y coordinates",
    ),
    (
        "center_align",
        3.6,
        [
            "cl = CardList(",
            "    style=Styles.Neutral, ...)",
            'cl.add("1. Plan", "Draft RFC")',
            'cl.add("2. Build", "CI checks")',
            'cl.add("3. Ship", "Canary")',
            "",
            "# Center bounding box on (cx, cy)",
            "cl.draw(",
            "    xy=(32, 26),",
            "    width=44, height=25,",
            '    align="center")',
        ],
        (6, 10),
        'align = "center"',
        'align="center": Centers Bounding Box on (cx, cy)',
        'Centered Anchor (align="center")',
        "Centers overall (width, height) box on xy=(cx, cy)",
        "Handy for centering card stacks on canvas midlines",
    ),
]

for m_idx, (f_mode, dur, code_m, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(FOCUS_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(4, code_m, hl_rng, phosphor.sliders_horizontal, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Hero Card", ".show = False", 'align="center"'], m_idx)

        pw_tot, ph_tot, spc = 44.0, 24.6, 1.8
        card_h = (ph_tot - 2.0 * spc) / 3.0

        cl = CardList(
            style=Styles.Neutral,
            text_style=TITLE_DARK,
            description_style=DESC_DARK,
            badge_shape="rounded_rect",
            badge_style=Styles.PrimaryNeutral,
            icon_style=Styles.PrimaryBold,
            direction="vertical",
            spacing=spc,
        )
        cl.add("1. Plan", "Draft RFC", icon=phosphor.compass)
        cl.add("2. Build", "CI checks", icon=phosphor.code)
        cl.add("3. Ship", "Canary", icon=phosphor.rocket_launch, style=Styles.SecondaryNeutral)

        if f_mode == "hero_card":
            cl.items[1].style = Styles.PrimaryFlat
            cl.items[1].text_style = TITLE_WHITE
            cl.items[1].description_style = DESC_WHITE
            cl.items[1].badge_style = Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0)
            cl.items[1].icon_style = Styles.PrimaryBold
            cl.draw(xy=(80.0, 22.0), width=pw_tot, height=ph_tot)
            text(
                (scx, 18.5),
                "items[1].style = Styles.PrimaryFlat  (focal hero)",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        elif f_mode == "hide_card":
            cl.items[1].show = False
            px0, py0 = 80.0, 22.0
            cl.draw(xy=(px0, py0), width=pw_tot, height=ph_tot)
            rectangle(
                (px0 + pw_tot / 2.0, py0 + ph_tot / 2.0),
                width=pw_tot,
                height=card_h,
                style=Styles.MutedDashed.patch(
                    shape_fill_color=(248, 250, 252),
                    shape_line_color=(148, 163, 184),
                    shape_line_width=1.2,
                    shape_r=1.6,
                ),
                text="items[1] hidden — slot preserved",
                text_style=Styles.MutedBold.patch(text_size=9.5),
            )
            text(
                (scx, 18.5),
                "items[0] & items[2] hold exact Y positions",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            cx_a, cy_a = scx, 34.3
            cl.items[1].style = Styles.PrimaryNeutral
            cl.draw(xy=(cx_a, cy_a), width=pw_tot, height=ph_tot, align="center")
            rectangle(
                (cx_a, cy_a),
                width=pw_tot,
                height=ph_tot,
                style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.3),
            )
            # Red (cx, cy) crosshair extending cleanly outside bounding box
            line((cx_a - 24.8, cy_a), (cx_a - 22.0, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a + 22.0, cy_a), (cx_a + 24.8, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a + 12.3), (cx_a, cy_a + 14.1), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a - 14.1), (cx_a, cy_a - 12.3), style=Styles.DangerBold.patch(line_width=1.5))
            circle(
                (cx_a, cy_a),
                radius=1.6,
                style=Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0),
            )
            circle((cx_a, cy_a), radius=1.15, style=Styles.DangerFlat)
            text(
                (cx_a, 18.2),
                'xy = (32, 26)  •  align = "center"',
                style=Styles.DangerBold.patch(text_size=9.5),
            )

save()
```

- **段階的なカード追加とアンカー（`xy`, `align`）**: `.add(text, description, badge_text=..., icon=...)` でリッチなカードを追加し、デフォルトの**左下** `xy`（`align="bottom_left"`）または中央（`align="center"`）を基準に `(width, height)` 領域内へ描画します。
- **バッジ形状（`badge_shape`）**: 枠付きのアイコン／ラベルバッジには `"rounded_rect"`（デフォルト）または `"circle"` を選び、枠なしのアイコンをカードテキストの横に直接並べる場合は `"none"` を設定します。
- **配置方向とワークフロー矢印（`direction`, `show_arrows`）**: `direction="vertical"`（上から下へのスタック）から `direction="horizontal"`（左から右へのカード列）へ切り替えられるほか、`show_arrows=True` と `arrow_style` を設定して隣接する表示ステップ間を矢印で接続できます。
- **カード単位の強調とスロット維持（`.items[i]`, `.show`）**: `cards.items[i].style` を上書きして特定の注目カードをハイライトしたり、`cards.items[i].show = False` を設定して他のカードの位置をずらさずに該当カード（および隣接する矢印）を非表示にしたりできます。

---

## 2. 垂直方向の機能一覧・多層防御カード（`direction="vertical"`）

`direction="vertical"`（デフォルト）では、`(width, height)` のバウンディングボックス内にカードが**上から下へ**順に配置されます。各カードの左側にはバッジ（`badge_shape="rounded_rect"` または `"circle"`）が表示され、その横に太字のカードタイトル（`text`）と複数行対応の説明文（`description`）が続きます。

```drawlib code=show align=center file=smartarts_cardlist_vertical.png caption="垂直方向の CardList によるゼロトラストセキュリティ多層防御アーキテクチャ"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=120, height=58)

text((6.0, 52.5), "Zero-Trust Cloud Security — 3-Layer Defense Controls", style=Styles.DarkBold.patch(text_size=11.0, halign="left"))

layers = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=9.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=2.8,
)
layers.add(
    "Layer 1: Global Anycast Edge & DDoS Protection",
    "Absorbs L3/L4 volumetric floods across 48 PoPs before traffic reaches regional VPCs",
    badge_text="L1",
    icon=phosphor.globe_hemisphere_east,
)
layers.add(
    "Layer 2: Identity-Aware Proxy & WAF Policy Engine",
    "Enforces OIDC device posture, rate limiting, and OWASP Top-10 signature inspection",
    badge_text="L2",
    icon=phosphor.shield_check,
)
layers.add(
    "Layer 3: SPIFFE/SPIRE Service Mesh & Envelope KMS",
    "Short-lived X.509 mTLS workload certificates with hardware-backed key rotation",
    badge_text="L3",
    icon=phosphor.lock_key,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=9.5),
    icon_style=Styles.WhiteBold,
)
layers.draw(xy=(6.0, 5.0), width=108.0, height=44.0)

save()
```

---

## 3. 接続矢印付きの水平ステップシーケンス（`direction="horizontal"`）

`direction="horizontal"` を設定すると、カードが**左から右へ**並び、各カード上部の中央にバッジ／アイコンが配置され、その下にタイトル（`text`）と説明文（`description`）が縦に積まれます。`show_arrows=True`（および `arrow_style`）を有効にすると、`spacing` の間隔をまたいで隣接するカード間に接続矢印（`->`）が描画されます。

```drawlib code=show align=center file=smartarts_cardlist_horizontal.png caption="水平方向の CardList による 4 段階 CI/CD ドキュメント構築・検証パイプライン"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.smartarts import CardList
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=52)

text((6.0, 46.5), "Autonomous Illustrated Documentation Pipeline", style=Styles.DarkBold.patch(text_size=11.0, halign="left"))

workflow = CardList(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=11.5),
    description_style=Styles.Muted.patch(text_size=10.0),
    badge_shape="circle",
    badge_style=Styles.PrimaryNeutral,
    icon_style=Styles.PrimaryBold,
    direction="horizontal",
    show_arrows=True,
    arrow_style=Styles.Dark,
    spacing=4.5,
)
workflow.add(
    "1. Scaffold",
    "Run drawlib init\nsite or doc",
    icon=phosphor.folder_open,
)
workflow.add(
    "2. Author",
    "Write Markdown &\ndrawlib blocks",
    icon=phosphor.code,
)
workflow.add(
    "3. Grid Review",
    "Inspect -g grid\n& self-heal",
    icon=phosphor.magnifying_glass,
    style=Styles.PrimaryNeutral,
    badge_style=Styles.PrimaryFlat,
    icon_style=Styles.WhiteBold,
)
workflow.add(
    "4. Publish",
    "Export HTML site\n& vector PDF",
    icon=phosphor.rocket_launch,
)
workflow.draw(xy=(6.0, 5.0), width=114.0, height=38.0)

save()
```

---

## 4. バッジモードと向きのジオメトリ

- **左下アンカーまたは中央アンカー（`xy`, `align`）**: `CardList.draw(xy=(x, y), width=W, height=H, align="bottom_left")` はバウンディングボックスの左下角を `(x, y)` に配置し、右方向（`+x`）に `W` 単位、上方向（`+y`）に `H` 単位の領域へ展開します。`align="center"` の場合はバウンディングボックス全体を `(x, y)` の中央に配置します。
- **バッジ形状（`badge_shape`）**:
  - `"rounded_rect"` *（デフォルト）*: 控えめな角丸を持つ正方形バッジコンテナを描画します（`badge_style` が必須）。
  - `"circle"`: 円形のバッジコンテナを描画します（`badge_style` が必須）。
  - `"none"`: バッジ背景図形を描画せず、`icon` または `badge_text` を直接描画します。
- **バッジ内容の描画ルール**:
  - `icon` を指定した場合、`icon_style` を用いてベクターアイコンを描画します。
  - `badge_text` を指定した場合、`badge_text_style` を用いてバッジラベルを描画します。
  - `icon` と `badge_text` の両方を指定した場合、バッジ内部の上部にアイコンを、その下部に `badge_text` を並べて描画します。

---

## 5. API リファレンス

### コンストラクタ
```python
CardList(
    *,
    style: Style,
    text_style: Style,
    description_style: Style | None = None,
    badge_shape: Literal["circle", "rounded_rect", "none"] = "rounded_rect",
    badge_style: Style | None = None,
    badge_text_style: Style | None = None,
    icon_style: Style | None = None,
    direction: Literal["vertical", "horizontal"] = "vertical",
    spacing: float = 2.5,
    show_arrows: bool = False,
    arrow_style: Style | None = None,
)
```

### メソッドとプロパティ
- **`add(text: str, description: str = "", *, badge_text: str | None = None, icon: Callable | None = None, style: Style | None = None, text_style: Style | None = None, description_style: Style | None = None, badge_style: Style | None = None, badge_text_style: Style | None = None, icon_style: Style | None = None, show: bool = True) -> CardListItem`**:
  カード項目（`text` がカードの主タイトル）を末尾に追加し、変更可能な `CardListItem` を返します。`item.show = False` を設定すると、他のすべてのカードの座標を維持したまま、該当カード（および隣接する矢印）を非表示にします。
- **`cardlist.items -> list[CardListItem]`**:
  事後変更用の登録済み `CardListItem` インスタンスのリストを返します。
- **`draw(xy: tuple[float, float], width: float = 90.0, height: float = 50.0, *, align: Literal["bottom_left", "center"] = "bottom_left", scale: float = 1.0) -> Self`**:
  左下角 `xy`（`align="center"` の場合は中央 `xy`）を基準とする `(width, height)` のバウンディングボックス内にカード列を描画します。

