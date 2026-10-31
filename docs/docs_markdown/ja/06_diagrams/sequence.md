# シーケンス図 (SequenceDiagram): ライフライン・同期呼び出し・条件ブロック

`SequenceDiagram` は、協調して動作する参加者（Participant）間の時系列に沿った相互作用と通信プロトコルをモデル化します。時間は垂直なライフラインに沿って厳密に上から下へと進行し、水平方向の矢印がメッセージを表します。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/06_diagrams/sequence/sequence_overview_concepts.png" alt="sequence_1" />
  <figcaption class="drawlib-caption">SequenceDiagram のライフライン・アクティベーションバー・メッセージ表現</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=126, height=88)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    node_card_style=Styles.Neutral,
    col_width=40.0,
    step_y=8.5,
)

client = d.add(Participant("Client", width=22, height=15, icon=PhosphorIcon.LAPTOP, icon_size=6.5))
api = d.add(
    Participant("API Server", width=22, height=15, icon=PhosphorIcon.CLOUD, icon_size=6.5, card_style=Styles.PrimaryNeutral)
)
db = d.add(Participant("Database", width=22, height=15, icon=PhosphorIcon.DATABASE, icon_size=6.5))

client.request(api, "POST /login (Sync request)")
api.activate()

api.request(db, "SELECT user_record")
db.activate()
db.reply(api, "User row (Dashed reply)")
db.deactivate()

api.request(db, "INSERT audit_log (Async)", is_async=True)
api.reply(client, "200 OK + JWT")
api.deactivate()

client.connect(api, "WebSocket Stream (<->)", arrow="<->")

d.draw(xy=(4.0, 3.0))
save()
```

</details>



---

## 1. 基本概念と基本的な使い方

`SequenceDiagram` は、`Participant` ヘッダーカードを水平方向（`col_width`）に並べ、デフォルトの**左下 `(x0, y0)`** アンカー（または `align="center"`）を基準として、メッセージ矢印を時系列順に下方向（`step_y`）へと進めます。`.activate()` / `.deactivate()` で実行区間を強調したり、ライフライン上または複数ライフラインをまたぐ付箋ノートを配置したり、条件分岐や反復ステップを Python の `with` 複合フラグメントフレーム（`d.alt()`、`d.loop()`、`d.opt()`）で囲んだりできます。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/06_diagrams/sequence/sequence_parameter_tour.png" alt="sequence_2" />
  <figcaption class="drawlib-caption">基本的な使い方とパラメータツアー: ライフラインとアンカー、同期/非同期とアクティベーション、自己呼び出しとノート、条件フレームと段階的表示 (APNG アニメーション)</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import (
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)
from drawlib.icons import code as code_icons
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import SourceCode, SourceCodeStyles
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
    ("1. Lifelines & Grid", "Participants & step_y"),
    ("2. Calls & Active", "request, reply & async"),
    ("3. Self & Notes", "Loopback & sticky notes"),
    ("4. Frames & Reveal", "with d.alt(), show & center"),
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
        "sequence_tour.py",
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


NODE_TXT = Styles.DarkBold.patch(text_size=11.0)
MSG_TXT = Styles.Dark.patch(text_size=11.0, valign="top")
SYNC_EDGE = Styles.DarkBold.patch(line_arrow_head_fill=True)

# =========================================================================
# Part 1: Lifelines & Grid — Participants, ParticipantGroup & autonumber
# =========================================================================
PART1_STATES = [
    (
        "two_lifelines",
        3.3,
        [
            "d = SequenceDiagram(",
            "    col_width=20, step_y=5.2, ...)",
            "client = d.add(Participant(",
            '    "Client",',
            "    icon=PhosphorIcon.LAPTOP))",
            "api = d.add(Participant(",
            '    "API",',
            "    icon=PhosphorIcon.CLOUD))",
            'client.request(api, "GET /items")',
            'api.reply(client, "200 OK")',
            "d.draw(xy=(8, 6))",
        ],
        (8, 10),
        "Bottom-Left xy",
        "Step 1: Lifelines, col_width & Bottom-Left xy=(x0, y0)",
        "1. Lifelines, Spacing & Bottom-Left Anchor",
        "col_width spaces headers; step_y advances downward",
        "d.draw(xy) pins the bottom-left container corner",
    ),
    (
        "group",
        3.3,
        [
            "d = SequenceDiagram(",
            "    col_width=16, step_y=5.0, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "grp = d.add(ParticipantGroup(",
            '    title="Backend", padding=1.5))',
            'api = grp.add(Participant("API"))',
            'db = grp.add(Participant("DB"))',
            'client.request(api, "GET /items")',
            'api.request(db, "SELECT *")',
            "d.draw(xy=(8, 6))",
        ],
        (4, 7),
        "ParticipantGroup",
        'Step 2: Cluster Backend Lifelines via ParticipantGroup',
        "2. Clustered Lifelines (ParticipantGroup)",
        "Wraps API & DB header cards in a dashed boundary",
        "Automatically reserves top header padding for title",
    ),
    (
        "autonumber",
        3.5,
        [
            "d = SequenceDiagram(",
            "    autonumber=True,",
            "    col_width=16, step_y=4.8, ...)",
            'client = d.add(Participant("App"))',
            'api = d.add(Participant("API"))',
            'db = d.add(Participant("DB"))',
            'client.request(api, "GET /items")',
            'api.request(db, "SELECT *")',
            'db.reply(api, "rows")',
            'api.reply(client, "200 JSON")',
            "d.draw(xy=(8, 6))",
        ],
        (0, 2),
        "autonumber=True",
        "Step 3: Sequential Message Numbering (1., 2., 3., 4.)",
        "3. Automatic Step Numbering (autonumber=True)",
        "Prefixes every request/reply in chronological order",
        "Makes multi-hop API traces effortless to reference",
    ),
]

for p1_idx, (p1_mode, dur, code_1, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART1_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(1, code_1, hl_rng, phosphor.columns, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["2 Lifelines", "+ Group", "autonumber"], p1_idx)

        if p1_mode == "two_lifelines":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=10.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=9.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=21.0,
                step_y=5.0,
                margin=1.0,
                height=23.2,
            )
            client = d.add(Participant("Client", width=12.4, height=7.4, icon=PhosphorIcon.LAPTOP, icon_size=3.1))
            api = d.add(
                Participant(
                    "API",
                    width=12.4,
                    height=7.4,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=3.1,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            client.request(api, "GET /items")
            api.reply(client, "200 OK")

            dw, dh = d.get_size()
            dx0, dy0 = 81.5, 19.8
            d.draw(xy=(dx0, dy0))

            rectangle(
                (dx0 + dw / 2.0, dy0 + dh / 2.0),
                width=dw,
                height=dh,
                style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.0),
            )
            # col_width indicator between lifelines
            lx1, lx2 = dx0 + 7.2, dx0 + 28.2
            line((lx1, 44.8), (lx2, 44.8), arrow_head="<->", style=Styles.PrimaryBold.patch(line_width=1.1))
            text((0.5 * (lx1 + lx2), 46.8), "col_width", style=Styles.PrimaryBold.patch(text_size=9.5))

            # Downward time indicator on right
            line((122.2, 39.2), (122.2, 24.4), arrow_head="->", style=Styles.PrimaryBold.patch(line_width=1.2))
            text((122.2, 41.0), "time", style=Styles.PrimaryBold.patch(text_size=9.5))

            # Red bottom-left (x0, y0) anchor
            circle((dx0, dy0), radius=1.1, style=Styles.DangerFlat)
            text(
                (dx0 + 1.8, 17.9),
                "xy = (x0, y0)  (bottom-left)",
                style=Styles.DangerBold.patch(text_size=9.5, halign="left"),
            )
        elif p1_mode == "group":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=NODE_TXT,
                edge_style=SYNC_EDGE,
                edge_text_style=MSG_TXT,
                node_card_style=Styles.Neutral,
                col_width=15.6,
                step_y=4.8,
                margin=0.8,
                height=31.0,
            )
            client = d.add(Participant("Client", width=11.0, height=7.2, icon=PhosphorIcon.LAPTOP, icon_size=3.0))
            grp = d.add(
                ParticipantGroup(
                    title="Backend",
                    padding=1.2,
                    style=Styles.PrimaryDashed,
                    text_style=Styles.PrimaryBold.patch(text_size=11.0, halign="left", valign="bottom"),
                )
            )
            api = grp.add(
                Participant(
                    "API",
                    width=11.0,
                    height=7.2,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=3.0,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            db = grp.add(Participant("DB", width=11.0, height=7.2, icon=PhosphorIcon.DATABASE, icon_size=3.0))
            client.request(api, "GET /items")
            api.request(db, "SELECT *")
            d.draw(xy=(82.5, 20.4), scale=0.88)
            text(
                (scx, 18.2),
                'ParticipantGroup(title="Backend") clusters API + DB',
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=NODE_TXT,
                edge_style=SYNC_EDGE,
                edge_text_style=MSG_TXT,
                node_card_style=Styles.Neutral,
                autonumber=True,
                col_width=16.0,
                step_y=4.4,
                margin=0.8,
                height=31.0,
            )
            client = d.add(Participant("App", width=11.0, height=7.0, icon=PhosphorIcon.LAPTOP, icon_size=2.9))
            api = d.add(
                Participant(
                    "API",
                    width=11.0,
                    height=7.0,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=2.9,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            db = d.add(Participant("DB", width=11.0, height=7.0, icon=PhosphorIcon.DATABASE, icon_size=2.9))
            client.request(api, "GET /items")
            api.request(db, "SELECT *")
            db.reply(api, "rows")
            api.reply(client, "200 JSON")
            d.draw(xy=(82.5, 20.4), scale=0.88)
            text(
                (scx, 18.2),
                "autonumber=True  ->  1., 2., 3., 4. in call order",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )

# =========================================================================
# Part 2: Calls & Active — Sync/Reply, Async & Bidirectional Connect
# =========================================================================
PART2_STATES = [
    (
        "sync_active",
        3.3,
        [
            "d = SequenceDiagram(",
            "    col_width=22, step_y=5.4, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            'client.request(api, "POST /pay")',
            "api.activate()",
            'api.reply(client, "200 OK")',
            "api.deactivate()",
            "d.draw(xy=(8, 6))",
        ],
        (6, 9),
        "activate() + reply",
        "Step 1: Sync Request, Execution Bar & Dashed Reply",
        "1. Activation Span & Dashed Reply",
        "activate()/deactivate() draws execution focus bar",
        "reply() renders a dashed return arrow (200 OK)",
    ),
    (
        "async_call",
        3.3,
        [
            'client.request(api, "POST /pay")',
            "api.activate()",
            'api.request(worker, "SQL Write")',
            "worker.activate()",
            'worker.reply(api, "OK")',
            "worker.deactivate()",
            "api.request(",
            '    worker, "Audit",',
            "    is_async=True)",
            'api.reply(client, "200 OK")',
            "api.deactivate()",
        ],
        (6, 8),
        "is_async=True",
        "Step 2: Fire-and-Forget Async Call + Nested Activation",
        "2. Asynchronous Dispatch (is_async=True)",
        "Open stick arrowhead marks non-blocking dispatch",
        "Nested activation bars track downstream DB/Worker",
    ),
    (
        "bidir_ws",
        3.5,
        [
            "d = SequenceDiagram(",
            "    col_width=22, step_y=5.2, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            'client.request(api, "GET /ws")',
            'api.reply(client, "101 Upgrade")',
            "client.connect(",
            '    api, "WS Stream",',
            '    arrow="<->")',
        ],
        (8, 10),
        'arrow="<->"',
        'Step 3: Full-Duplex Channel via connect(..., arrow="<->")',
        '3. Bidirectional Channel (arrow="<->")',
        "connect() supports '<->', '->', and '-' line heads",
        "Ideal for WebSocket, gRPC, and TCP full-duplex flows",
    ),
]

for p2_idx, (p2_mode, dur, code_2, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART2_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(2, code_2, hl_rng, phosphor.arrows_left_right, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Sync + Active", "is_async=True", 'arrow="<->"'], p2_idx)

        if p2_mode == "sync_active":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=10.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=9.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=22.0,
                step_y=6.2,
                margin=1.0,
                height=26.5,
            )
            client = d.add(Participant("Client", width=12.4, height=7.6, icon=PhosphorIcon.LAPTOP, icon_size=3.2))
            api = d.add(
                Participant(
                    "API",
                    width=12.4,
                    height=7.6,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=3.2,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            api.activate()
            client.request(api, "POST /pay")
            api.deactivate()
            api.reply(client, "200 OK")

            dx0, dy0 = 80.5, 20.8
            d.draw(xy=(dx0, dy0))
            # Point to activation bar on API lifeline
            api_x = dx0 + 1.0 + 6.2 + 22.0
            line((api_x + 5.6, 30.2), (api_x + 1.8, 30.2), arrow_head="->", style=Styles.PrimaryBold.patch(line_width=1.2))
            text(
                (api_x + 6.2, 30.2),
                "active",
                style=Styles.PrimaryBold.patch(text_size=9.5, halign="left"),
            )
            text(
                (scx, 18.2),
                "solid request (->)  •  focus bar  •  dashed reply (-->)",
                style=Styles.DarkBold.patch(text_size=9.5),
            )
        elif p2_mode == "async_call":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=NODE_TXT,
                edge_style=SYNC_EDGE,
                edge_text_style=MSG_TXT,
                node_card_style=Styles.Neutral,
                col_width=16.2,
                step_y=4.2,
                margin=0.8,
                height=32.0,
            )
            client = d.add(Participant("Client", width=11.0, height=6.8, icon=PhosphorIcon.LAPTOP, icon_size=2.8))
            api = d.add(
                Participant(
                    "API",
                    width=11.0,
                    height=6.8,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=2.8,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            worker = d.add(Participant("Worker", width=11.0, height=6.8, icon=PhosphorIcon.GEAR, icon_size=2.8))

            api.activate()
            client.request(api, "POST /pay")
            worker.activate()
            api.request(worker, "SQL Write")
            worker.deactivate()
            worker.reply(api, "OK")
            api.request(
                worker,
                "Audit",
                is_async=True,
                style=Styles.PrimaryBold.patch(line_arrow_head_fill=False, line_width=1.5),
                text_style=Styles.PrimaryBold.patch(text_size=11.0, valign="top"),
            )
            api.deactivate()
            api.reply(client, "200 OK")

            d.draw(xy=(82.2, 20.2), scale=0.87)
            text(
                (scx, 18.2),
                "open stick arrow (is_async=True) + nested activation",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        else:
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=10.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=9.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=23.0,
                step_y=5.2,
                margin=1.0,
                height=26.8,
            )
            client = d.add(Participant("Client", width=12.4, height=7.4, icon=PhosphorIcon.LAPTOP, icon_size=3.1))
            api = d.add(
                Participant(
                    "API",
                    width=12.4,
                    height=7.4,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=3.1,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            client.request(api, "GET /ws")
            api.reply(client, "101 Upgrade")
            client.connect(
                api,
                "WS Stream",
                arrow="<->",
                style=Styles.PrimaryBold.patch(line_arrow_head_fill=True, line_width=1.6),
                text_style=Styles.PrimaryBold.patch(text_size=9.8, valign="top"),
            )
            d.draw(xy=(82.0, 20.6))
            text(
                (scx, 18.2),
                'connect(..., arrow="<->")  •  bidirectional stream',
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )

# =========================================================================
# Part 3: Self & Notes — Self-Call Loopback, Lifeline Note & Spanning Note
# =========================================================================
PART3_STATES = [
    (
        "self_call",
        3.3,
        [
            "d = SequenceDiagram(",
            "    col_width=20, step_y=5.0, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            'client.request(api, "POST /auth")',
            "api.activate()",
            'api.request(api, "validate()")',
            'api.reply(client, "200 JWT")',
            "api.deactivate()",
        ],
        (8, 8),
        "Self-Call Loop",
        'Step 1: Self-Call Loopback via api.request(api, "validate()")',
        "1. Recursive / Internal Self-Call",
        "Passing same source & target draws a 3-segment loop",
        "Timeline automatically reserves 1.8x step_y clearance",
    ),
    (
        "right_note",
        3.3,
        [
            "d = SequenceDiagram(",
            "    col_width=18, step_y=4.8, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            'client.request(api, "POST /auth")',
            "api.note(",
            '    "JWT verified", pos="right")',
            'api.reply(client, "200 JWT")',
            "d.draw(xy=(8, 6))",
        ],
        (7, 8),
        'pos="right"',
        'Step 2: Lifeline Sticky Note via api.note(..., pos="right")',
        "2. Participant Sticky Note (api.note)",
        'Attaches annotation card on pos="right" or "left"',
        "Diagram width expands automatically for side notes",
    ),
    (
        "over_note",
        3.5,
        [
            "d = SequenceDiagram(",
            "    col_width=22, step_y=4.8, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            "d.note(",
            '    "TLS 1.3 Session",',
            "    over=[client, api])",
            'client.request(api, "POST /auth")',
            'api.reply(client, "200 JWT")',
        ],
        (6, 8),
        "over=[client, api]",
        "Step 3: Multi-Lifeline Banner via d.note(..., over=[...])",
        "3. Spanning Note Across Lifelines (over=[...])",
        "Bridges two or more collaborating participants",
        "Great for protocol invariants and shared session state",
    ),
]

for p3_idx, (p3_mode, dur, code_3, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART3_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(3, code_3, hl_rng, phosphor.note, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["Self-Call", 'pos="right"', "over=[...]"], p3_idx)

        if p3_mode == "self_call":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=10.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=9.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=19.5,
                step_y=4.6,
                margin=0.8,
                height=27.2,
            )
            client = d.add(Participant("Client", width=11.8, height=7.2, icon=PhosphorIcon.LAPTOP, icon_size=3.0))
            api = d.add(
                Participant(
                    "API",
                    width=11.8,
                    height=7.2,
                    icon=PhosphorIcon.SHIELD_CHECK,
                    icon_size=3.0,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            api.activate()
            client.request(api, "POST /auth")
            api.request(
                api,
                "validate()",
                style=Styles.PrimaryBold.patch(line_arrow_head_fill=True),
                text_style=Styles.PrimaryBold.patch(text_size=9.6, halign="left", valign="center"),
            )
            api.deactivate()
            api.reply(client, "200 JWT")
            d.draw(xy=(79.5, 20.6))
            text(
                (scx, 18.2),
                "api.request(api, ...) loops back onto caller lifeline",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )
        elif p3_mode == "right_note":
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=NODE_TXT,
                edge_style=SYNC_EDGE,
                edge_text_style=MSG_TXT,
                node_card_style=Styles.Neutral,
                col_width=17.5,
                step_y=4.5,
                margin=0.8,
                height=29.8,
            )
            client = d.add(Participant("Client", width=11.4, height=7.0, icon=PhosphorIcon.LAPTOP, icon_size=2.9))
            api = d.add(
                Participant(
                    "API",
                    width=11.4,
                    height=7.0,
                    icon=PhosphorIcon.SHIELD_CHECK,
                    icon_size=2.9,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            client.request(api, "POST /auth")
            nt = api.note("JWT verified", pos="right")
            nt.set_text_style(Styles.DarkBold.patch(text_size=10.8))
            api.reply(client, "200 JWT")
            d.draw(xy=(80.5, 20.5), scale=0.89)
            text(
                (scx, 18.2),
                'api.note("JWT verified", pos="right") beside lifeline',
                style=Styles.DarkBold.patch(text_size=9.5),
            )
        else:
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=NODE_TXT,
                edge_style=SYNC_EDGE,
                edge_text_style=MSG_TXT,
                node_card_style=Styles.Neutral,
                col_width=22.0,
                step_y=4.5,
                margin=0.8,
                height=29.8,
            )
            client = d.add(Participant("Client", width=11.8, height=7.0, icon=PhosphorIcon.LAPTOP, icon_size=2.9))
            api = d.add(
                Participant(
                    "API",
                    width=11.8,
                    height=7.0,
                    icon=PhosphorIcon.SHIELD_CHECK,
                    icon_size=2.9,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            nt_over = d.note("TLS 1.3 Session", over=[client, api])
            nt_over.set_text_style(Styles.DarkBold.patch(text_size=10.8))
            client.request(api, "POST /auth")
            api.reply(client, "200 JWT")
            d.draw(xy=(84.5, 20.5), scale=0.89)
            text(
                (scx, 18.2),
                "d.note(..., over=[client, api]) spans both lifelines",
                style=Styles.PrimaryBold.patch(text_size=9.5),
            )

# =========================================================================
# Part 4: Frames & Reveal — with d.alt() / else_(), show=False & align
# =========================================================================
PART4_STATES = [
    (
        "alt_else",
        3.3,
        [
            "d = SequenceDiagram(...)",
            'client = d.add(Participant("App"))',
            'api = d.add(Participant("API"))',
            'with d.alt("cache hit"):',
            '    api.reply(client, "200 (mem)")',
            'with d.else_("miss"):',
            '    api.reply(client, "200 (DB)")',
            "d.draw(xy=(8, 6))",
        ],
        (3, 6),
        "with d.alt()",
        "Step 1: Pythonic Condition Frames (with d.alt / d.else_)",
        "1. Context-Manager Frames (alt / else_ / loop)",
        "Wraps enclosed steps in a labeled [ALT] / [ELSE] box",
        "Also supports d.loop(), d.opt(), d.par() & Block",
    ),
    (
        "show_false",
        3.3,
        [
            "d = SequenceDiagram(...)",
            'client = d.add(Participant("App"))',
            'api = d.add(Participant("API"))',
            'with d.alt("cache hit"):',
            '    api.reply(client, "200 (mem)")',
            "# Hide branch; bounds stay locked!",
            'with d.else_("miss", show=False):',
            "    api.reply(",
            '        client, "DB", show=False)',
            "d.draw(xy=(8, 6))",
        ],
        (5, 8),
        "show=False",
        "Step 2: Progressive Reveal (Lifelines & Bounds Stay Locked)",
        "2. Jitter-Free Reveal (show=False)",
        "Hides later messages/frames without shrinking lifelines",
        "Headers & active frames stay pixel-locked across steps",
    ),
    (
        "center_align",
        3.5,
        [
            "d = SequenceDiagram(",
            "    col_width=20, step_y=5.0, ...)",
            "client = d.add(",
            '    Participant("Client", ...))',
            "api = d.add(",
            '    Participant("API", ...))',
            'client.request(api, "GET /items")',
            'api.reply(client, "200 OK")',
            "# Center diagram on xy=(cx, cy)",
            "d.draw(",
            '    xy=(34, 24), align="center")',
        ],
        (8, 10),
        'align="center"',
        'Step 3: Center Diagram Container on xy=(cx, cy)',
        '3. Centered Placement (align="center")',
        "Centers total (width, height) diagram box on xy",
        "Ideal for centered slide panes and Studio cards",
    ),
]

for p4_idx, (p4_mode, dur, code_4, hl_rng, badge_txt, foot_txt, s_t, s_1, s_2) in enumerate(PART4_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(4, code_4, hl_rng, phosphor.crosshair, s_t, s_1, s_2)
        scx, scy = draw_geometry_studio(badge_txt, foot_txt)
        draw_sub_pills(scx, ["with d.alt()", "show=False", 'align="center"'], p4_idx)

        if p4_mode in {"alt_else", "show_false"}:
            show_else = p4_mode == "alt_else"
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=11.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=10.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=21.0,
                step_y=3.9,
                margin=0.6,
                height=32.0,
            )
            client = d.add(Participant("App", width=11.4, height=6.5, icon=PhosphorIcon.LAPTOP, icon_size=2.7))
            api = d.add(
                Participant(
                    "API",
                    width=11.4,
                    height=6.5,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=2.7,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            with d.alt(" cache hit  ") as blk_alt:
                blk_alt.text_style = Styles.PrimaryBold.patch(text_size=10.8)
                blk_alt.style = Styles.PrimaryDashed.patch(shape_fill_color=(239, 246, 255, 0.45))
                api.reply(client, "200 (mem)")
            with d.else_(" miss  ", show=show_else) as blk_else:
                blk_else.text_style = Styles.DarkBold.patch(text_size=10.8)
                api.reply(client, "200 (DB)", show=show_else)

            sc = 0.88
            dw, dh = d.get_size()
            dx0, dy0 = scx - (dw * sc) / 2.0, 19.9
            d.draw(xy=(dx0, dy0), scale=sc)
            rectangle(
                (dx0 + (dw * sc) / 2.0, dy0 + (dh * sc) / 2.0),
                width=dw * sc,
                height=dh * sc,
                style=Styles.MutedDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=0.9),
            )
            if show_else:
                text(
                    (scx, 18.0),
                    "[ALT] cache hit  +  [ELSE] miss condition frames",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )
            else:
                text(
                    (scx, 18.0),
                    "else_ hidden (show=False)  •  lifelines stay locked!",
                    style=Styles.PrimaryBold.patch(text_size=9.5),
                )
        else:
            d = SequenceDiagram(
                node_style=Styles.Primary,
                node_text_style=Styles.DarkBold.patch(text_size=10.0),
                edge_style=SYNC_EDGE,
                edge_text_style=Styles.Dark.patch(text_size=9.8, valign="top"),
                node_card_style=Styles.Neutral,
                col_width=20.5,
                step_y=6.8,
                margin=0.6,
                height=26.4,
            )
            client = d.add(Participant("Client", width=11.8, height=6.2, icon=PhosphorIcon.LAPTOP, icon_size=2.6))
            api = d.add(
                Participant(
                    "API",
                    width=11.8,
                    height=6.2,
                    icon=PhosphorIcon.CLOUD,
                    icon_size=2.6,
                    card_style=Styles.PrimaryNeutral,
                )
            )
            client.request(api, "GET /items")
            api.reply(client, "200 OK")

            cx_a, cy_a = scx, 34.3
            dw, dh = d.get_size()
            d.draw(xy=(cx_a, cy_a), align="center")

            rectangle(
                (cx_a, cy_a),
                width=dw,
                height=dh,
                style=Styles.PrimaryDashed.patch(shape_fill_color=(0, 0, 0, 0), shape_line_width=1.3),
            )
            line((cx_a - dw / 2.0 - 2.6, cy_a), (cx_a - dw / 2.0, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a + dw / 2.0, cy_a), (cx_a + dw / 2.0 + 2.6, cy_a), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a + dh / 2.0), (cx_a, cy_a + dh / 2.0 + 1.8), style=Styles.DangerBold.patch(line_width=1.5))
            line((cx_a, cy_a - dh / 2.0 - 1.8), (cx_a, cy_a - dh / 2.0), style=Styles.DangerBold.patch(line_width=1.5))
            circle(
                (cx_a, cy_a),
                radius=1.45,
                style=Styles.Neutral.patch(shape_fill_color=(255, 255, 255), shape_line_width=0),
            )
            circle((cx_a, cy_a), radius=1.1, style=Styles.DangerFlat)
            text(
                (cx_a, 17.9),
                'xy = (cx, cy)  •  align="center"',
                style=Styles.DangerBold.patch(text_size=9.5),
            )

save()
```

</details>



- **垂直ライフラインとグループ (`Participant`, `ParticipantGroup`, `col_width`, `step_y`)**: ヘッダーカードが上端に整列し、垂直の破線ライフラインが時系列に沿って下方向へ伸びます。`ParticipantGroup` を使うと関連するバックエンドサービス群をラベル付き境界枠でグループ化できます。
- **メッセージ表現 (`request`, `reply`, `connect`, 自己呼び出し)**: `request()` は同期呼び出し（`is_async=True` で開いた矢印の非同期送信）、`reply()` は破線の応答矢印、`connect(..., arrow="<->")` は全二重ストリームを描画し、`p.request(p, ...)` は自身のライフラインへ戻る自己呼び出しループを描画します。
- **実行フォーカス・付箋ノート・自動採番 (`activate`, `note`, `autonumber=True`)**: `p.activate()` / `p.deactivate()` で実行区間を表すアクティベーションバーを描画し、`p.note()` / `d.note(..., over=[...])` でライフライン横または複数ライフライン横断の付箋ノートを追加できます。`autonumber=True` で各ステップに連番（`1.`、`2.`、`3.`、...）を自動付与します。
- **コンテキストマネージャフレームと安定した段階表示 (`with d.alt()`, `show=False`, `align`)**: 条件分岐や反復処理を `with d.alt()` / `d.else_()` / `d.loop()` / `d.opt()` で囲み、`show=False` でライフライン位置をずらさずに段階的なステップ表示を行えます。配置基準は左下または `align="center"` を選択できます。

---

## 2. コンストラクタと参加者 (`Participant`) の管理

```python
from drawlib.diagrams.sequence import (
    Block,
    GcpIcon,
    Participant,
    ParticipantGroup,
    PhosphorIcon,
    SequenceDiagram,
)
from drawlib.styles import Styles

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark,
    node_card_style=Styles.Neutral,
    title="Checkout Transaction Pipeline",
    autonumber=True,            # Auto-number messages (1., 2., 3., ...)
)

# Participant group for clustered backend services
vpc = d.add(ParticipantGroup(title="Google Cloud VPC", padding=4.0))
api = vpc.add(Participant("Cloud Run\n(Gateway)", width=22, height=16, icon=GcpIcon.CLOUD_RUN, card_style=Styles.PrimaryNeutral))
db = vpc.add(Participant("Cloud SQL", width=22, height=16, icon=GcpIcon.CLOUD_SQL))

# External participant
client = d.add(Participant("Web Browser", width=22, height=16, icon=PhosphorIcon.BROWSER))
```

### パラメータリファレンス

#### `SequenceDiagram` クラス
| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `node_style` | `Style` | *(必須)* | 参加者アイコンおよび画像のベース `Style` オブジェクト。 |
| `node_text_style` | `Style` | *(必須)* | 参加者テキストラベルのベース `Style` オブジェクト。 |
| `edge_style` | `Style` | *(必須)* | メッセージ矢印およびライフラインのベース `Style` オブジェクト。 |
| `edge_text_style` | `Style` | *(必須)* | メッセージラベルのベース `Style` オブジェクト。 |
| `node_card_style` | `Style \| None` | `None` | 参加者ヘッダーカードのベース `Style`（`None` の場合は背景透明）。 |
| `title` | `str` | `""` | ダイアグラム上部に表示する任意のバナータイトル。 |
| `autonumber` | `bool` | `False` | `True` の場合、メッセージラベルの先頭に連番（`1.`、`2.`、`3.`、...）を自動付与。 |
| `width` | `float \| None` | `None` | 固定キャンバス幅（`None` の場合はライフライン群から自動計算）。 |
| `height` | `float \| None` | `None` | 固定キャンバス高さ（`None` の場合はタイムラインステップ数から自動計算）。 |
| `col_width` | `float` | `20.0` | 参加者ライフライン間のデフォルト水平中心間隔。 |
| `step_y` | `float` | `7.0` | 時系列メッセージまたはノート 1 ステップあたりの下方向進行距離。 |
| `margin` | `float` | `5.0` | 全ライフラインおよびヘッダー周囲の外側マージン。 |
| `style` | `Style \| None` | `None` | ダイアグラム全体の背景カード用 `Style`（任意）。 |
| `title_style` | `Style \| None` | `None` | ダイアグラムタイトルテキストの `Style` オーバーライド（任意）。 |

#### `Participant` クラス
| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `text` | `str` | `""` | 参加者ヘッダーカードに表示する名前（`\n` による改行に対応）。 |
| `width` | `float` | `20.0` | ヘッダーカードの幅（キャンバス単位）。 |
| `height` | `float` | `16.0` | ヘッダーカードの高さ（キャンバス単位）。 |
| `icon` | `IconType` | `None` | 34 種類の `*Icon` Enum（`PhosphorIcon`、`GcpIcon`、`AwsIcon`、`AzureIcon`、`AiIcon`〜`OriginalWorkspaceIcon`。詳細は[アイコン概要](../03_icons/overview.md)を参照）、`CustomIcon`、`Dimage`、`PIL.Image`、ファイルパス、またはアイコン関数。 |
| `icon_size` | `float` | `8.0` | アイコンの幅・高さ（座標単位）。 |
| `style` | `Style \| None` | `None` | 参加者アイコン／画像の `Style` オーバーライド（任意）。 |
| `text_style` | `Style \| None` | `None` | 参加者ラベルテキストの `Style` オーバーライド（任意）。 |
| `card_style` | `Style \| None` | `None` | 参加者ヘッダーカードの背景・枠線の `Style` オーバーライド（任意）。 |
| `lifeline_style` | `Style \| None` | `None` | 垂直破線ライフラインの `Style` オーバーライド（任意）。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、ヘッダー・ライフライン・接続メッセージ／ノートを非表示）。 |

- **ライフライン水平位置の固定とサイズ取得**:
  - `d.add(participant, x: float | None = None, *, show: bool | None = None) -> Participant`: 参加者を登録します。任意でライフラインの水平座標 `x` を明示固定できます。
  - `participant.set_x(x: float) -> Participant`: 参加者のライフライン水平位置 `x` を明示固定し、`self` を返します。
  - `participant.activate() -> None` / `participant.deactivate() -> None`: ライフライン上の実行フォーカス（アクティベーションバー）を開始・終了します。
  - `participant.get_size() -> tuple[float, float]` / `participant.get_header_size() -> tuple[float, float]`: `(width, height)` を返します。

#### `ParticipantGroup` クラス
| パラメータ | 型 | デフォルト | 説明 |
|---|---|---|---|
| `title` | `str` | `""` | 参加者グループ境界ボックスのヘッダータイトル。 |
| `padding` | `float` | `4.0` | 囲まれた参加者ヘッダーカード周囲の内側余白。 |
| `style` | `Style \| None` | `None` | グループ境界ボックスの `Style`（任意）。 |
| `text_style` | `Style \| None` | `None` | グループタイトルテキストの `Style`（任意）。 |
| `show` | `bool` | `True` | 表示フラグ（`False` の場合、列間隔を維持したままグループ枠のみを非表示）。 |

- **`group.add(participant: Participant, *, show: bool | None = None) -> Participant`**: グループに参加者を追加します（親ダイアグラムへも自動登録されます）。

---

### メッセージ・ノート・スペース調整・描画 API

- **参加者レベルおよびダイアグラムレベルのメッセージ**:
  - **`a.request(b, label="", is_async=False, style=None, text_style=None, show=True) -> Message`** または **`d.request(a, b, ...) -> Message`**: 実線のリクエスト矢印（`->`）を描画します。同一の参加者を指定（`a.request(a, "...")`）すると、3 線分の**自己呼び出し (self-call)** ループ（`msg.is_self_call == True`）を描画します。
  - **`b.reply(a, label="", is_async=False, style=None, text_style=None, show=True) -> Message`** または **`d.reply(b, a, ...) -> Message`**: 破線の応答矢印（`-->`）を描画します。
  - **`a.connect(b, label="", arrow="->", is_async=False, style=None, text_style=None, show=True) -> Message`** または **`d.connect(a, b, ...) -> Message`**: 任意の向きまたは双方向（`arrow="<->" | "->" | "-"`）のメッセージを描画します。
- **`Message` のメソッドチェーン用ミューテータ**:
  - `msg.set_label(text: str) -> Message`
  - `msg.set_reply(is_reply: bool = True) -> Message`
  - `msg.set_async(is_async: bool = True) -> Message`
  - `msg.set_arrow(arrow: Literal["->", "<->", "-"]) -> Message`
  - `msg.set_style(style: Style) -> Message`
  - `msg.set_text_style(text_style: Style) -> Message`
  - `msg.set_padding(padding: float | tuple[float, float]) -> Message`
- **付箋ノート (`d.note` & `p.note`)**:
  - **`d.note(text: str, on: Participant | None = None, over: list[Participant] | None = None, pos: Literal["left", "right", "over"] = "right", style: Style | None = None, show: bool = True) -> Note`**: 単一ライフラインの横（`on=p, pos="left"|"right"`）または複数ライフラインを横断する形（`over=[p1, p2]`）で付箋ノートを配置します。
  - **`p.note(text: str, pos: Literal["left", "right"] = "right", style: Style | None = None, show: bool = True) -> Note`**: `d.note(text, on=p, pos=pos, ...)` の便利なショートハンドです。
  - **`Note` ミューテータ**: `note.set_text(text) -> Note`、`note.set_style(style) -> Note`、`note.set_text_style(text_style) -> Note`。
- **タイムライン間隔調整・サイズ取得・描画**:
  - **`d.space(dy: float = 5.0) -> None`**: 垂直タイムラインを追加で `dy` 単位進め、フェーズ間に視覚的な余白を設けます。
  - **`d.get_size() -> tuple[float, float]`**: シーケンス図全体の `(width, height)` を計算して返します。
  - **`d.draw(xy=(0.0, 0.0), *, scale: float = 1.0) -> None`**: 左下 `xy` を基準として、列幅、垂直ステップ、アイコン、タイポグラフィを `scale` 倍に比例スケーリングしてシーケンス図を描画します。

---

## 3. 分散トランザクションパイプライン

次の完全なサンプルでは、参加者グループ、クラウドアイコン、アクティベーションバー、非同期ディスパッチ、およびリトライループフレームを組み合わせています。



```python
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import GcpIcon, Participant, ParticipantGroup, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=132, height=128)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Microservices Distributed Transaction Pipeline",
    autonumber=True,
    col_width=30.5,
    step_y=9.0,
)

# 1. Participants: Client on the left, Backend services in VPC group on the right
client = d.add(Participant("Web Browser", width=22, height=16, icon=PhosphorIcon.BROWSER, icon_size=6.5))

backend = d.add(
    ParticipantGroup(
        title="Google Cloud VPC",
        padding=3.0,
        style=Styles.MutedDashed,
        text_style=Styles.DarkBold.patch(text_size=10.5, halign="left", valign="top"),
    )
)
api = backend.add(
    Participant("Cloud Run\n(Gateway)", width=22, height=16, icon=GcpIcon.CLOUD_RUN, icon_size=6.5, card_style=Styles.PrimaryNeutral)
)
worker = backend.add(Participant("GKE Pod\n(Worker)", width=22, height=16, icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE, icon_size=6.5))
db = backend.add(Participant("Cloud SQL\n(Database)", width=22, height=16, icon=GcpIcon.CLOUD_SQL, icon_size=6.5))

# 2. Interactions
client.request(api, "POST /api/v1/checkout")
api.activate()

api.request(db, "Check Inventory")
db.reply(api, "Stock Available")

api.request(worker, "Enqueue Job (Pub/Sub)", is_async=True)
worker.reply(api, "Ack", is_async=True)

api.reply(client, "202 Accepted (Order ID)")
api.deactivate()

with d.loop("Retry up to 3 times on DB lock"):
    worker.request(db, "Deduct Inventory Rows")
    db.reply(worker, "Rows Committed")

d.draw(xy=(3.0, 2.5))
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/06_diagrams/sequence/sequence_distributed_transaction.png" alt="sequence_3" />
  <figcaption class="drawlib-caption">マイクロサービス分散トランザクションパイプライン</figcaption>
</figure>



---

## 4. WebSocket 全二重ストリーミング

リアルタイムの双方向ストリームを表現する場合は、`connect()` に `arrow="<->"` を指定します。



```python
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=92, height=82)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.5),
    node_card_style=Styles.Neutral,
    title="WebSocket Real-Time Live Sync",
    col_width=40.0,
)

app = d.add(Participant("Mobile App", width=22, height=15, icon=PhosphorIcon.DEVICE_MOBILE, icon_size=7.0))
gateway = d.add(
    Participant("WS Gateway", width=22, height=15, icon=PhosphorIcon.CLOUD, icon_size=7.0, card_style=Styles.PrimaryNeutral)
)

app.request(gateway, "GET /ws HTTP/1.1 (Upgrade: websocket)")
gateway.reply(app, "101 Switching Protocols")

# Bidirectional streaming channel
app.connect(gateway, "Full-Duplex JSON Telemetry Stream", arrow="<->")

with d.loop("Every 500ms Ping Interval"):
    gateway.request(app, "PING", is_async=True)
    app.reply(gateway, "PONG", is_async=True)

d.draw(xy=(6.0, 4.0))
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/06_diagrams/sequence/sequence_websocket_telemetry.png" alt="sequence_4" />
  <figcaption class="drawlib-caption">WebSocket 全二重テレメトリストリーム</figcaption>
</figure>



---

## 5. 条件フレーム（`alt` / `else_`）・自己呼び出し・付箋ノート

Drawlib は、`SequenceDiagram` のコンテキストマネージャまたは `Block(block_type, label="", diagram=d, style=None, text_style=None, show=True)` の直接インスタンス化によって、標準 UML の 7 種類の複合フラグメント演算子（`BlockType = Literal["loop", "alt", "else", "opt", "par", "critical", "break"]`）をすべてサポートしています。

| フレーム種別 | コンテキストマネージャ / コンストラクタ | 標準 UML 演算子 |
|---|---|---|
| **ループ (Loop)** | `with d.loop("condition", show=True):` | `loop` |
| **条件分岐 (Alternative)** | `with d.alt("condition", show=True):`<br>`with d.else_("fallback", show=True):` | `alt` / `else` |
| **任意実行 (Option)** | `with d.opt("condition", show=True):` | `opt` |
| **並列実行 (Parallel)** | `with d.par("description", show=True):` | `par` |
| **クリティカル領域 (Critical Region)** | `with Block("critical", "atomic lock", diagram=d):` | `critical` |
| **中断 (Break)** | `with Block("break", "fatal error", diagram=d):` | `break` |

フレームは内部に含まれるすべてのメッセージやノートを囲む外接矩形を自動計算し、左上に `[OPERATOR] label` タグを描画します。

次の例では、**自己呼び出し**（`auth.request(auth, ...)`）、**付箋ノート**（`auth.note(...)` および `d.note(..., over=[...])`）、そして **`alt` / `else_`** 条件分岐フレームを組み合わせています。



```python
from drawlib.canvas import save, setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=128, height=134)

d = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="JWT Authentication & Conditional Token Refresh",
    col_width=37.0,
    step_y=8.2,
)

client = d.add(Participant("Client App", width=23, height=16, icon=PhosphorIcon.LAPTOP, icon_size=7.0))
auth = d.add(
    Participant("Auth Service", width=23, height=16, icon=PhosphorIcon.SHIELD_CHECK, icon_size=7.0, card_style=Styles.PrimaryNeutral)
)
idp = d.add(Participant("OAuth IdP", width=23, height=16, icon=PhosphorIcon.KEY, icon_size=7.0))

client.request(auth, "POST /verify (Bearer JWT)")
auth.activate()

# Self-call for local signature verification + attached participant note
auth.request(auth, "Verify JWT")
auth.note("Local public key cache", pos="right")

# Conditional alt / else_ blocks
with d.alt("Token Valid & Unexpired"):
    auth.reply(client, "200 OK (Claims Payload)")

with d.else_("Token Expired (Refresh Flow)"):
    auth.request(idp, "POST /oauth/token (refresh_token)")
    idp.reply(auth, "New Access JWT")
    auth.reply(client, "200 OK (Rotated JWT)")

auth.deactivate()

# Spanning note across multiple participants
d.note("All token exchanges require TLS 1.3 mTLS", over=[client, auth])

d.draw(xy=(4.0, 3.5))
save()
```

<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/06_diagrams/sequence/sequence_auth_alt_notes.png" alt="sequence_5" />
  <figcaption class="drawlib-caption">自己呼び出し・付箋ノート・alt/else_ 条件フレームを用いた認証フロー</figcaption>
</figure>


