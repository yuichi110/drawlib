# CLI リファレンス

Drawlib は、ドキュメントのコンパイル、単体の図解画像の抽出、キャッシュアセットの管理、リンク検証、および組み込みデザインシステムの確認を行うための統合コマンドラインインターフェース（`drawlib`）を提供します。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/09_doc_builder_and_cli/cli_reference/cli_command_taxonomy.png" alt="cli_reference_1" />
  <figcaption class="drawlib-caption">ワークフローステージ別に整理された Drawlib CLI の 9 つのサブコマンド</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=58)

# Top Row: Primary 4-Stage Authoring & Publishing Pipeline
stages = [
    (18.5, "1. init", "doc / site / slide", Styles.Neutral, Styles.DarkBold, Styles.Dark, phosphor.rocket_launch, Styles.PrimaryBold),
    (48.8, "2. show", "-g grid / -o export", Styles.PrimaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.grid_four, Styles.PrimaryBold),
    (79.2, "3. build", "html / pdf / office", Styles.PrimaryFlat, Styles.WhiteBold, Styles.White, phosphor.hammer, Styles.WhiteBold),
    (109.5, "4. serve", "--check link audit", Styles.SecondaryNeutral, Styles.DarkBold, Styles.Dark, phosphor.eye, Styles.PrimaryBold),
]
for sx, title, sub, st, tst, sub_st, icon_fn, icon_st in stages:
    rectangle((sx, 42.5), width=26, height=22, style=st.patch(shape_r=2.0))
    icon_fn((sx, 48.2), width=4.8, style=icon_st)
    text((sx, 41.2), title, style=tst.patch(text_size=11.0))
    text((sx, 35.8), sub, style=sub_st.patch(text_size=10.0))

line((31.5, 42.5), (35.8, 42.5), arrow_head="->", style=Styles.DarkBold)
line((61.8, 42.5), (66.2, 42.5), arrow_head="->", style=Styles.DarkBold)
line((92.2, 42.5), (96.5, 42.5), arrow_head="->", style=Styles.DarkBold)

# Bottom Row: Supporting Design Systems, Cache & AI Rules Subcommands
rectangle((64, 14.5), width=117, height=22, style=Styles.MutedDashed.patch(shape_r=2.0))
text((64, 22.8), "Cross-Cutting Design, Asset Cache & AI Knowledge", style=Styles.DarkBold.patch(text_size=11.0))

bottom_cards = [
    (25.5, "colors | styles | css", "Design Palettes", Styles.Neutral, phosphor.palette),
    (64.0, "drawlib cache", "Assets & Browser", Styles.PrimaryNeutral, phosphor.database),
    (102.5, "drawlib rules", "92 AI Manuals", Styles.SecondaryNeutral, phosphor.book_open),
]
for bx, btitle, bsub, bst, bicon in bottom_cards:
    rectangle((bx, 11.8), width=35, height=11.5, style=bst.patch(shape_r=1.5))
    bicon((bx - 12.5, 11.8), width=4.4, style=Styles.PrimaryBold)
    text((bx + 2.5, 13.8), btitle, style=Styles.DarkBold.patch(text_size=10.2))
    text((bx + 2.5, 9.2), bsub, style=Styles.Dark.patch(text_size=10.0))

save()
```

</details>



---

## 1. インタラクティブ CLI ワークフローツアー

プロジェクトの初期構築（`init` および `rules`）から、1 秒未満の座標グリッドプレビュー（`show -g`）、マルチフォーマットへのコンパイル（`build`）、さらに公開前のリンク・アセット検証（`serve --check` および `cache`）まで、9 つの `drawlib` サブコマンドすべてが一貫したループの中で連携します。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/09_doc_builder_and_cli/cli_reference/cli_workflow_tour.png" alt="cli_reference_2" />
  <figcaption class="drawlib-caption">Drawlib CLI 日常ワークフローツアー: スキャフォールディングと AI ルール、単一図解のグリッドプレビュー、7 種類のビルドターゲット、リンク監査とデザインインスペクタ (APNG アニメーション)</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import client, devops, phosphor, workspace
from drawlib.icons import code as code_icons
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
    ("1. init & rules", "Scaffold & 92 manuals"),
    ("2. show -g Loop", "Sub-second grid preview"),
    ("3. build Targets", "Web, PDF & MS Office"),
    ("4. serve & Inspect", "Link audit, CSS & cache"),
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
    """Draw left terminal CLI pane + bottom concept takeaway card."""
    x0, w = 4.0, 63.5
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    editor_h = 43.8
    takeaway_h = 15.8

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    phosphor.terminal_window((x0 + 3.6, top_y + header_h / 2.0), width=3.5, style=Styles.PrimaryBold)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "terminal — drawlib CLI",
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
        code_lang="bash",
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


def draw_output_studio(param_badge: str, footer_caption: str) -> tuple[float, float]:
    """Draw right CLI output & artifact inspector shell and footer."""
    x0, w = 70.0, 64.0
    cx = x0 + w / 2.0
    top_y = 63.2
    header_h = 5.4
    body_h = 59.6

    rectangle((cx, top_y + header_h / 2.0), width=w, height=header_h, style=PANE_HEADER)
    phosphor.eye((x0 + 3.6, top_y + header_h / 2.0), width=3.5, style=Styles.Primary)
    text(
        (x0 + 6.5, top_y + header_h / 2.0),
        "Live CLI Output & View",
        style=Styles.DarkBold.patch(text_size=10.2, halign="left"),
    )
    text(
        (x0 + w - 2.6, top_y + header_h / 2.0),
        param_badge,
        style=Styles.PrimaryBold.patch(text_size=9.6, halign="right"),
    )

    rectangle((cx, 3.6 + body_h / 2.0), width=w, height=body_h, style=STUDIO_BODY)

    sheet_cx, sheet_cy = cx, 36.2
    sheet_w, sheet_h = 55.6, 40.0
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
    g_st = Styles.MutedThin.patch(line_color=(236, 241, 248), line_width=0.8)
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
    pw, ph, pgap = 16.4, 4.2, 0.9
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


# =========================================================================
# Part 1: 1. init & rules (3 frames: 3.3 + 3.3 + 3.5 = 10.1s)
# =========================================================================
PART1_CODE = [
    "# 1a. List 4 starter archetypes",
    "drawlib init list",
    "",
    "# 1b. Scaffold site w/ Google CSS",
    "drawlib init site docs \\",
    "  -s google -l en",
    "",
    "# 1c. Read offline AI manuals",
    "drawlib rules show overview",
]

PART1_STATES = [
    (
        "1a",
        3.3,
        (0, 1),
        "init list",
        "4 Starter Archetypes: images, doc, site & slide",
        "1a. Project Archetype Catalog",
        "4 built-in project templates for any format",
        "Configures styles.py, utils.py & build.sh",
    ),
    (
        "1b",
        3.3,
        (3, 5),
        "init site -s",
        "Scaffolds docs_src/ With Google Theme & Fonts",
        "1b. Zero-Config Project Bootstrap",
        "Creates docs_src/, navbar.md & _assets/",
        "-s google syncs style.css and styles.py",
    ),
    (
        "1c",
        3.5,
        (7, 8),
        "92 AI Guides",
        "92 Offline Reference Guides + Companion PNGs",
        "1c. Embedded AI Knowledge Base",
        "92 offline manuals for geometry, styles & API",
        "Auto-renders companion illustrations locally",
    ),
]

for p1_idx, (mode, dur, hl_rng, badge, foot, s_t, s_1, s_2) in enumerate(PART1_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(1, PART1_CODE, hl_rng, phosphor.rocket_launch, s_t, s_1, s_2)
        scx, _ = draw_output_studio(badge, foot)
        draw_sub_pills(scx, ["1a. init list", "1b. init site", "1c. rules show"], p1_idx)

        if mode == "1a":
            archetypes = [
                (89.2, 41.0, "images", "*.py -> PNG/SVG", phosphor.images, Styles.Neutral),
                (114.8, 41.0, "doc", "Spec -> PDF/DOCX", phosphor.file_pdf, Styles.PrimaryNeutral),
                (89.2, 25.5, "site", "Multi-page HTML", phosphor.globe, Styles.PrimaryNeutral),
                (114.8, 25.5, "slide", "16:9 HTML & PPTX", phosphor.presentation_chart, Styles.SecondaryNeutral),
            ]
            for ax, ay, name, desc, ic_fn, cst in archetypes:
                rectangle((ax, ay), width=24.0, height=12.6, style=cst.patch(shape_r=1.5))
                ic_fn((ax - 7.8, ay + 1.8), width=4.0, style=Styles.PrimaryBold)
                text((ax - 4.2, ay + 2.0), name, style=Styles.DarkBold.patch(text_size=10.4, halign="left"))
                text((ax, ay - 3.2), desc, style=Styles.Dark.patch(text_size=9.5))
        elif mode == "1b":
            rectangle(
                (scx, 44.5),
                width=50.0,
                height=5.6,
                style=Styles.PrimaryFlat.patch(shape_r=1.3),
            )
            phosphor.folder_open((79.8, 44.5), width=3.6, style=Styles.WhiteBold)
            text((82.6, 44.5), "docs_src/", style=Styles.WhiteBold.patch(text_size=10.2, halign="left"))
            text((124.8, 44.5), "-s google", style=Styles.White.patch(text_size=9.5, halign="right"))

            rows = [
                (37.6, "styles.py & utils.py", "Tokens & helpers", "py", Styles.PrimaryNeutral),
                (31.6, "navbar.md & index.md", "Sidebar & hero", "md", Styles.Neutral),
                (25.6, "_assets/ & style.css", "Media & CSS", "folder", Styles.Neutral),
                (19.6, "build.sh", "1-cmd compiler", "sh", Styles.SecondaryNeutral),
            ]
            for ry, rname, rdesc, rkind, rst in rows:
                rectangle((scx, ry), width=50.0, height=5.0, style=rst.patch(shape_r=1.1))
                if rkind == "py":
                    code_icons.python((79.8, ry), width=3.0, style=Styles.Neutral)
                elif rkind == "md":
                    phosphor.file_text((79.8, ry), width=3.1, style=Styles.PrimaryBold)
                elif rkind == "folder":
                    phosphor.folder((79.8, ry), width=3.1, style=Styles.PrimaryBold)
                else:
                    phosphor.file_code((79.8, ry), width=3.1, style=Styles.PrimaryBold)
                text((82.6, ry), rname, style=Styles.DarkBold.patch(text_size=9.6, halign="left"))
                text((125.0, ry), rdesc, style=Styles.Dark.patch(text_size=9.5, halign="right"))
        else:
            rectangle((89.8, 33.0), width=26.6, height=27.0, style=Styles.Neutral.patch(shape_r=1.5))
            phosphor.book_open((80.2, 42.6), width=3.8, style=Styles.PrimaryBold)
            text((83.2, 42.6), "overview", style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
            text((89.8, 36.8), "92 AI Rule Guides", style=Styles.PrimaryBold.patch(text_size=9.6))
            text((89.8, 31.8), "• (0,0) Bottom-Left", style=Styles.Dark.patch(text_size=9.5))
            text((89.8, 27.4), "• 50%+ Neutral Card", style=Styles.Dark.patch(text_size=9.5))
            text((89.8, 23.0), "• 720pt Font Math", style=Styles.Dark.patch(text_size=9.5))

            line((103.3, 33.0), (106.8, 33.0), arrow_head="->", style=Styles.DarkBold)

            rectangle((117.4, 33.0), width=20.4, height=27.0, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
            phosphor.images((117.4, 42.4), width=4.0, style=Styles.PrimaryBold)
            text((117.4, 37.2), "rules/*.png", style=Styles.DarkBold.patch(text_size=9.7))
            rectangle((117.4, 28.4), width=15.0, height=10.5, style=Styles.White.patch(shape_r=1.0))
            line((112.0, 25.0), (112.0, 32.0), arrow_head="->", style=Styles.PrimaryBold)
            line((112.0, 25.0), (123.0, 25.0), arrow_head="->", style=Styles.PrimaryBold)
            text((118.2, 29.0), "(0,0)", style=Styles.PrimaryBold.patch(text_size=9.5))

# =========================================================================
# Part 2: 2. show -g Loop (3 frames: 3.3 + 3.3 + 3.5 = 10.1s)
# =========================================================================
PART2_CODE = [
    "# 2a. Index blocks in Markdown",
    "drawlib show page.md",
    "",
    "# 2b. Fast 10u/5u grid preview",
    "drawlib show page.md arch.png \\",
    "  -g -o .drawlib/scratch/g.png",
    "",
    "# 2c. Standalone .py w/ styles",
    "drawlib show script.py \\",
    "  -s styles.py -u utils.py \\",
    "  -o out.png",
]

PART2_STATES = [
    (
        "2a",
        3.3,
        (0, 1),
        "Block Table",
        "Lists Embedded Blocks (#0 hero.png, #1 arch.png)",
        "2a. Inspect Embedded Blocks",
        "Omitting target prints indexed block table",
        "Shows block index, filename & fence mode",
    ),
    (
        "2b",
        3.3,
        (3, 5),
        "-g < 1s Grid",
        "Renders 10u/5u Coordinate Grid to .drawlib/scratch/",
        "2b. Sub-Second Grid Preview (-g)",
        "Target by explicit filename (arch.png)",
        "10u/5u grid catches clipping & margins fast",
    ),
    (
        "2c",
        3.5,
        (7, 10),
        "-s & -u Parity",
        "Previews Standalone .py With Project styles.py",
        "2c. Standalone Script Export",
        "-s styles.py & -u utils.py inject tokens",
        "Guarantees 100% parity with full builds",
    ),
]

for p2_idx, (mode, dur, hl_rng, badge, foot, s_t, s_1, s_2) in enumerate(PART2_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(2, PART2_CODE, hl_rng, phosphor.grid_four, s_t, s_1, s_2)
        scx, _ = draw_output_studio(badge, foot)
        draw_sub_pills(scx, ["2a. Block Index", "2b. Grid (-g)", "2c. .py Preview"], p2_idx)

        if mode == "2a":
            rectangle(
                (scx, 44.2),
                width=50.0,
                height=5.2,
                style=Styles.Neutral.patch(shape_fill_color=(232, 238, 248), shape_r=1.1),
            )
            text((79.5, 44.2), "Idx", style=Styles.DarkBold.patch(text_size=9.6, halign="left"))
            text((89.0, 44.2), "Block File", style=Styles.DarkBold.patch(text_size=9.6, halign="left"))
            text((124.5, 44.2), "Fence", style=Styles.DarkBold.patch(text_size=9.6, halign="right"))

            rectangle((scx, 37.6), width=50.0, height=5.8, style=Styles.Neutral.patch(shape_r=1.1))
            text((79.5, 37.6), "#0", style=Styles.DarkBold.patch(text_size=9.6, halign="left"))
            text((89.0, 37.6), "hero.png", style=Styles.DarkBold.patch(text_size=9.7, halign="left"))
            text((124.5, 37.6), "code=fold", style=Styles.Dark.patch(text_size=9.5, halign="right"))

            rectangle((scx, 30.8), width=50.0, height=5.8, style=Styles.PrimaryNeutral.patch(shape_r=1.1))
            text((79.5, 30.8), "#1", style=Styles.PrimaryBold.patch(text_size=9.6, halign="left"))
            text((89.0, 30.8), "arch.png", style=Styles.PrimaryBold.patch(text_size=9.7, halign="left"))
            text((124.5, 30.8), "code=show", style=Styles.PrimaryBold.patch(text_size=9.5, halign="right"))

            rectangle((scx, 22.4), width=50.0, height=6.4, style=Styles.SecondaryNeutral.patch(shape_r=1.3))
            phosphor.check_circle((80.2, 22.4), width=3.6, style=Styles.PrimaryBold)
            text(
                (83.2, 22.4),
                "Target arch.png directly in < 1s",
                style=Styles.DarkBold.patch(text_size=9.6, halign="left"),
            )
        elif mode == "2b":
            gx0, gy0, gw, gh = 80.0, 22.5, 45.0, 22.5
            rectangle(
                (gx0 + gw / 2.0, gy0 + gh / 2.0),
                width=gw,
                height=gh,
                style=Styles.White.patch(shape_line_color=(96, 165, 250), shape_line_width=1.3),
            )
            for step in range(1, 5):
                vx = gx0 + step * 9.0
                st_g = (
                    Styles.Primary.patch(line_width=0.9)
                    if step % 2 == 0
                    else Styles.MutedDashed.patch(line_width=0.7)
                )
                line((vx, gy0), (vx, gy0 + gh), style=st_g)
            for step in range(1, 3):
                hy = gy0 + step * 7.5
                line((gx0, hy), (gx0 + gw, hy), style=Styles.Primary.patch(line_width=0.9))

            text((gx0, gy0 - 2.3), "0", style=Styles.PrimaryBold.patch(text_size=9.5))
            text((gx0 + 18.0, gy0 - 2.3), "20", style=Styles.PrimaryBold.patch(text_size=9.5))
            text((gx0 + 36.0, gy0 - 2.3), "40", style=Styles.PrimaryBold.patch(text_size=9.5))
            text((gx0 - 2.4, gy0 + 7.5), "10", style=Styles.PrimaryBold.patch(text_size=9.5))
            text((gx0 - 2.4, gy0 + 15.0), "20", style=Styles.PrimaryBold.patch(text_size=9.5))

            rectangle(
                (91.5, 33.8),
                width=14.0,
                height=8.5,
                style=Styles.Neutral.patch(shape_r=1.2),
                text="Gateway",
                text_style=Styles.DarkBold.patch(text_size=9.6),
            )
            rectangle(
                (113.5, 33.8),
                width=14.0,
                height=8.5,
                style=Styles.PrimaryNeutral.patch(shape_r=1.2),
                text="SQL DB",
                text_style=Styles.DarkBold.patch(text_size=9.6),
            )
            line((98.5, 33.8), (106.5, 33.8), arrow_head="->", style=Styles.DarkBold)
            rectangle(
                (116.8, 44.8),
                width=16.5,
                height=4.0,
                style=Styles.PrimaryFlat.patch(shape_r=1.0),
                text="-g 10u/5u",
                text_style=Styles.WhiteBold.patch(text_size=9.5),
            )
        else:
            inputs = [
                (42.5, "script.py", code_icons.python, Styles.PrimaryNeutral, True),
                (33.2, "-s styles.py", phosphor.palette, Styles.Neutral, False),
                (23.9, "-u utils.py", phosphor.sliders, Styles.Neutral, False),
            ]
            for iy, ilbl, i_fn, ist, is_png in inputs:
                rectangle((86.2, iy), width=19.8, height=6.8, style=ist.patch(shape_r=1.2))
                if is_png:
                    i_fn((78.8, iy), width=3.0, style=Styles.Neutral)
                else:
                    i_fn((78.8, iy), width=3.2, style=Styles.PrimaryBold)
                text((81.2, iy), ilbl, style=Styles.DarkBold.patch(text_size=9.5, halign="left"))
                line((96.1, iy), (100.8, 33.2), arrow_head="->", style=Styles.DarkBold)

            rectangle(
                (105.8, 33.2),
                width=10.0,
                height=10.0,
                style=Styles.PrimaryFlat.patch(shape_r=1.4),
                text="show",
                text_style=Styles.WhiteBold.patch(text_size=9.8),
            )
            line((110.8, 33.2), (114.4, 33.2), arrow_head="->", style=Styles.DarkBold)
            rectangle((121.0, 33.2), width=13.2, height=19.0, style=Styles.SecondaryNeutral.patch(shape_r=1.4))
            phosphor.images((121.0, 37.8), width=4.2, style=Styles.PrimaryBold)
            text((121.0, 31.8), "out.png", style=Styles.DarkBold.patch(text_size=9.8))
            text((121.0, 27.2), "Synced!", style=Styles.PrimaryBold.patch(text_size=9.5))

# =========================================================================
# Part 3: 3. build Targets (3 frames: 3.3 + 3.3 + 3.5 = 10.1s)
# =========================================================================
PART3_CODE = [
    "# 3a. Web & GitHub Markdown",
    "drawlib build html docs_src/",
    "drawlib build markdown docs_src/",
    "# 3b. Vector PDF & MS Word",
    "drawlib build pdf doc_src/ --toc",
    "drawlib build docx doc_src/",
    "# 3c. 16:9 Slide Deck & PPTX",
    "drawlib build slide slide_src/",
    "drawlib build pptx slide_src/",
    "# (+ build image scripts/ -g)",
]

PART3_STATES = [
    (
        "3a",
        3.3,
        (0, 2),
        "Web + GitHub",
        "Compiles Static Website + GitHub-Flavored Markdown",
        "3a. Web & Repository Targets",
        "build html generates searchable static site",
        "build markdown exports GFM + <doc>_images/",
    ),
    (
        "3b",
        3.3,
        (3, 5),
        "PDF + Word",
        "Compiles Vector A4 PDF (--toc) + Native Word (.docx)",
        "3b. Linear Spec & Office Docs",
        "build pdf renders vector A4 w/ auto TOC",
        "build docx produces editable native MS Word",
    ),
    (
        "3c",
        3.5,
        (6, 9),
        "16:9 + PPTX",
        "7 Build Targets: HTML, MD, PDF, DOCX, Slide, PPTX, Img",
        "3c. Presentations & Batch Images",
        "build slide adds ?presenter=1 dual view",
        "build pptx exports editable 16:9 slides + notes",
    ),
]

for p3_idx, (mode, dur, hl_rng, badge, foot, s_t, s_1, s_2) in enumerate(PART3_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(3, PART3_CODE, hl_rng, phosphor.hammer, s_t, s_1, s_2)
        scx, _ = draw_output_studio(badge, foot)
        draw_sub_pills(scx, ["3a. HTML & MD", "3b. PDF & DOCX", "3c. Slide & PPTX"], p3_idx)

        if mode == "3a":
            rectangle((83.6, 33.4), width=15.0, height=19.0, style=Styles.Neutral.patch(shape_r=1.4))
            phosphor.folder_open((83.6, 38.2), width=4.0, style=Styles.PrimaryBold)
            text((83.6, 32.2), "docs_src/", style=Styles.DarkBold.patch(text_size=9.7))
            text((83.6, 27.6), "*.md", style=Styles.Dark.patch(text_size=9.5))

            line((91.1, 37.5), (98.4, 40.8), arrow_head="->", style=Styles.DarkBold)
            line((91.1, 29.5), (98.4, 26.0), arrow_head="->", style=Styles.DarkBold)

            rectangle((113.0, 40.8), width=29.0, height=11.6, style=Styles.PrimaryNeutral.patch(shape_r=1.4))
            phosphor.globe((102.5, 40.8), width=4.2, style=Styles.PrimaryBold)
            text((106.2, 42.8), "docs_html/", style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
            text((106.2, 38.4), "Sidebar & Search", style=Styles.Dark.patch(text_size=9.5, halign="left"))

            rectangle((113.0, 26.0), width=29.0, height=11.6, style=Styles.SecondaryNeutral.patch(shape_r=1.4))
            devops.github((102.5, 26.0), width=3.9, style=Styles.Neutral)
            text((106.2, 28.0), "docs/ (*.md)", style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
            text((106.2, 23.6), "GFM + _images/", style=Styles.Dark.patch(text_size=9.5, halign="left"))
        elif mode == "3b":
            rectangle((83.6, 33.4), width=15.0, height=19.0, style=Styles.Neutral.patch(shape_r=1.4))
            phosphor.folder_open((83.6, 38.2), width=4.0, style=Styles.PrimaryBold)
            text((83.6, 32.2), "doc_src/", style=Styles.DarkBold.patch(text_size=9.7))
            text((83.6, 27.6), "chapters", style=Styles.Dark.patch(text_size=9.5))

            line((91.1, 37.5), (98.4, 40.8), arrow_head="->", style=Styles.DarkBold)
            line((91.1, 29.5), (98.4, 26.0), arrow_head="->", style=Styles.DarkBold)

            rectangle((113.0, 40.8), width=29.0, height=11.6, style=Styles.PrimaryNeutral.patch(shape_r=1.4))
            phosphor.file_pdf((102.5, 40.8), width=4.2, style=Styles.PrimaryBold)
            text((106.2, 42.8), "manual.pdf", style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
            text((106.2, 38.4), "Vector A4 + TOC", style=Styles.Dark.patch(text_size=9.5, halign="left"))

            rectangle((113.0, 26.0), width=29.0, height=11.6, style=Styles.Neutral.patch(shape_r=1.4))
            workspace.word((102.5, 26.0), width=4.0, style=Styles.Neutral)
            text((106.2, 28.0), "manual.docx", style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
            text((106.2, 23.6), "Editable MS Word", style=Styles.Dark.patch(text_size=9.5, halign="left"))
        else:
            rectangle((83.6, 36.2), width=15.0, height=16.5, style=Styles.Neutral.patch(shape_r=1.4))
            phosphor.presentation_chart((83.6, 40.2), width=4.0, style=Styles.PrimaryBold)
            text((83.6, 34.6), "slide_src/", style=Styles.DarkBold.patch(text_size=9.6))
            text((83.6, 30.6), "16:9 *.md", style=Styles.Dark.patch(text_size=9.5))

            line((91.1, 39.8), (98.4, 42.2), arrow_head="->", style=Styles.DarkBold)
            line((91.1, 32.8), (98.4, 30.2), arrow_head="->", style=Styles.DarkBold)

            rectangle((113.0, 42.2), width=29.0, height=10.0, style=Styles.PrimaryNeutral.patch(shape_r=1.3))
            phosphor.globe((102.5, 42.2), width=3.9, style=Styles.PrimaryBold)
            text((106.2, 44.0), "slide_html/", style=Styles.DarkBold.patch(text_size=10.0, halign="left"))
            text((106.2, 40.0), "16:9 + ?presenter=1", style=Styles.Dark.patch(text_size=9.5, halign="left"))

            rectangle((113.0, 30.2), width=29.0, height=10.0, style=Styles.SecondaryNeutral.patch(shape_r=1.3))
            workspace.powerpoint((102.5, 30.2), width=3.9, style=Styles.Neutral)
            text((106.2, 32.0), "deck.pptx", style=Styles.DarkBold.patch(text_size=10.0, halign="left"))
            text((106.2, 28.0), "960x540pt + Notes", style=Styles.Dark.patch(text_size=9.5, halign="left"))

            rectangle((scx, 20.4), width=50.0, height=5.2, style=Styles.Neutral.patch(shape_r=1.1))
            phosphor.images((79.8, 20.4), width=3.2, style=Styles.PrimaryBold)
            text(
                (82.8, 20.4),
                "+ build image -> batch PNG/SVG/WebP",
                style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
            )

# =========================================================================
# Part 4: 4. serve & Inspect (3 frames: 3.3 + 3.3 + 3.5 = 10.1s)
# =========================================================================
PART4_CODE = [
    "# 4a. Headless link & img audit",
    "drawlib serve docs_html/ --check",
    "",
    "# 4b. Design token inspectors",
    "drawlib colors list",
    "drawlib styles show google 1",
    "drawlib css list",
    "# 4c. Offline asset & browser",
    "drawlib cache list",
    "drawlib cache download --all",
]

PART4_STATES = [
    (
        "4a",
        3.3,
        (0, 1),
        "Exit Code 0",
        "Headless Pre-Flight Audit: 0 Broken Links -> Exit 0",
        "4a. Broken-Link Quality Gate",
        "Scans all HTML hrefs, anchors & image src",
        "Exits 0 when clean, 1 on any missing link",
    ),
    (
        "4b",
        3.3,
        (3, 6),
        "Design Tokens",
        "Inspect Color Palettes, Style Matrices & CSS Themes",
        "4b. Built-In Design Inspectors",
        "Preview color swatches & style matrices",
        "Export Google / Default HTML & PDF CSS",
    ),
    (
        "4c",
        3.5,
        (7, 9),
        "Offline Cache",
        "Warms Fonts, 34 Icon Suites, Maps & Chromium Offline",
        "4c. Asset & Browser Cache",
        "Audits & pre-warms fonts, icons & GeoMaps",
        "Provisions headless Chromium for PDF/PPTX",
    ),
]

for p4_idx, (mode, dur, hl_rng, badge, foot, s_t, s_1, s_2) in enumerate(PART4_STATES):
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(4, PART4_CODE, hl_rng, phosphor.shield_check, s_t, s_1, s_2)
        scx, _ = draw_output_studio(badge, foot)
        draw_sub_pills(scx, ["4a. --check", "4b. Tokens & CSS", "4c. cache --all"], p4_idx)

        if mode == "4a":
            rectangle((scx, 43.6), width=50.0, height=6.4, style=Styles.SecondaryNeutral.patch(shape_r=1.3))
            phosphor.check_circle((80.2, 43.6), width=3.8, style=Styles.PrimaryBold)
            text(
                (83.4, 43.6),
                "Audit Passed: 0 Broken Links (Exit 0)",
                style=Styles.DarkBold.patch(text_size=9.8, halign="left"),
            )

            checks = [
                (35.4, "Internal HTML Hrefs", "0 broken", Styles.Neutral),
                (28.6, "Diagram Image Assets", "100% found", Styles.Neutral),
                (21.8, "Local Dev Preview", "localhost:8000", Styles.PrimaryNeutral),
            ]
            for cy_row, clbl, cval, cst in checks:
                rectangle((scx, cy_row), width=50.0, height=5.4, style=cst.patch(shape_r=1.1))
                text((79.6, cy_row), clbl, style=Styles.DarkBold.patch(text_size=9.6, halign="left"))
                text((124.8, cy_row), cval, style=Styles.PrimaryBold.patch(text_size=9.5, halign="right"))
        elif mode == "4b":
            inspectors = [
                (42.4, "drawlib colors", "default | google | mono | css", phosphor.palette, Styles.Neutral),
                (33.2, "drawlib styles", "Neutral, PrimaryNeutral, Flat", phosphor.squares_four, Styles.PrimaryNeutral),
                (24.0, "drawlib css list", "HTML & PDF theme presets", phosphor.file_code, Styles.SecondaryNeutral),
            ]
            for iy, ititle, isub, i_fn, ist in inspectors:
                rectangle((scx, iy), width=50.0, height=7.4, style=ist.patch(shape_r=1.3))
                i_fn((80.4, iy), width=3.8, style=Styles.PrimaryBold)
                text((83.8, iy + 1.5), ititle, style=Styles.DarkBold.patch(text_size=9.9, halign="left"))
                text((83.8, iy - 1.8), isub, style=Styles.Dark.patch(text_size=9.5, halign="left"))
        else:
            packs = [
                (89.2, 41.0, "Fonts", "font_* • Roboto/CJK", phosphor.book_open, Styles.Neutral, False),
                (114.8, 41.0, "34 Icons", "Phosphor, Cloud, 2D", phosphor.package, Styles.PrimaryNeutral, False),
                (89.2, 25.5, "GeoMaps", "map_* • World/Cities", phosphor.globe, Styles.Neutral, False),
                (114.8, 25.5, "Chromium", "PDF & PPTX Shell", client.chromium, Styles.SecondaryNeutral, True),
            ]
            for px, py, ptitle, psub, p_fn, pst, is_png in packs:
                rectangle((px, py), width=24.0, height=12.6, style=pst.patch(shape_r=1.5))
                if is_png:
                    p_fn((px - 7.6, py + 1.8), width=3.6, style=Styles.Neutral)
                else:
                    p_fn((px - 7.6, py + 1.8), width=3.8, style=Styles.PrimaryBold)
                text((px - 4.2, py + 2.0), ptitle, style=Styles.DarkBold.patch(text_size=10.2, halign="left"))
                text((px, py - 3.2), psub, style=Styles.Dark.patch(text_size=9.5))

save()
```

</details>



---

## 2. クイックコマンド一覧

```bash
# Compilation
drawlib build html docs_src/ -o docs_html/                  # Responsive static HTML website
drawlib build markdown docs_src/ -o docs/                  # GitHub-ready Markdown
drawlib build pdf doc_src/ -o manual.pdf --toc              # High-fidelity vector PDF
drawlib build docx doc_src/ -o manual.docx --generate-index # Editable MS Word (.docx) document
drawlib build slide slide_src/ -o slide_html/               # Interactive 16:9 HTML slide deck
drawlib build pptx slide_src/ -o deck.pptx                  # Editable 16:9 MS PowerPoint (.pptx) deck
drawlib build image scripts/ -o assets/ -g                  # Batch Python image rendering

# Scaffolding
drawlib init list                                          # List starter project templates (site, doc, slide, images)
drawlib init doc my_doc                                    # Scaffold linear document project (HTML, PDF, DOCX, MD, images)
drawlib init site my_site                                  # Scaffold documentation site
drawlib init slide my_deck -s google                       # Scaffold 16:9 presentation slide deck
drawlib init images my_images                              # Scaffold standalone images project (alias: image)

# Inspection & Preview
drawlib show doc.md                                        # List all drawlib code blocks in doc.md
drawlib show doc.md arch.png -o .drawlib/scratch/arch.png          # Headless extraction by explicit filename (Recommended)
drawlib show doc.md arch.png -g -o .drawlib/scratch/arch_grid.png  # Export named block with coordinate grid
drawlib show script.py -o .drawlib/scratch/fig.png                 # Export standalone Python script

# Local Server & Verification
drawlib serve docs_html/                                   # Local preview on http://localhost:8000
drawlib serve docs_html/ --check                           # Pre-flight broken link/asset audit

# Design Systems, Cache & AI Rules
drawlib colors list                                        # List color catalogs (default, google, monochrome, css)
drawlib styles list                                        # List style catalogs (default, google, monochrome)
drawlib css list                                           # List CSS presets for HTML and PDF
drawlib cache list                                         # Inspect cached fonts, icons, and maps
drawlib cache download --all                               # Pre-download fonts, icons, maps, and headless Chromium
drawlib rules list                                         # List 92 AI rule instruction manuals
```

---

## 3. グローバル CLI オプション

グローバルフラグは、すべてのトップレベルコマンドの前に指定します（`drawlib [GLOBAL_OPTIONS] COMMAND ...`）。

| フラグ | 説明 |
|---|---|
| `-v`, `--version` | インストールされている `drawlib` のバージョンを表示し、ステータス `0` で終了します。 |
| `-h`, `--help` | コンテキストに応じたヘルプメッセージと利用可能なサブコマンドを表示します。 |
| `--quiet` | 重要でない標準出力を抑制します（警告とエラーのみを出力します）。 |
| `--verbose` / `--debug` | 診断ログ、実行時間メトリクス、キャッシュヒット／ミスの詳細出力を有効にします。 |
| `--developer` | 詳細ログを有効にし、ユーザー向けのエラーラッパーを無効化して Python の完全なスタックトレースをそのまま送出します。 |

*（注: `--quiet` は `--verbose`、`--debug`、`--developer` と同時に指定できません。併用した場合は終了コード `2` で終了します。）*

---

## 4. コンパイルサブシステム (`drawlib build`)



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/09_doc_builder_and_cli/cli_reference/cli_build_and_show_targets.png" alt="cli_reference_3" />
  <figcaption class="drawlib-caption">単一図解のインタラクティブプレビュー (drawlib show) とプロジェクト全体のコンパイル (drawlib build) の比較</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=58)

# Top Panel: Fast Interactive Loop (drawlib show)
rectangle((63, 42.5), width=118, height=23, style=Styles.MutedDashed.patch(shape_r=2.0))
phosphor.grid_four((13, 50.2), width=4.4, style=Styles.PrimaryBold)
text(
    (66, 50.2),
    "Fast Interactive Loop: drawlib show (Single-Diagram Preview)",
    style=Styles.DarkBold.patch(text_size=11.0),
)

show_flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)
show_flow.add("1. Source", description="doc.md / .py")
show_flow.add(
    "2. drawlib show",
    description="-g -o preview.png",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
show_flow.add("3. Grid Review", description="Inspect Coords", style=Styles.PrimaryNeutral)
show_flow.draw(xy=(8, 33.0), width=110, height=13.5)

# Bottom Panel: Full Project Compilation (drawlib build)
rectangle((63, 15.0), width=118, height=23, style=Styles.MutedDashed.patch(shape_r=2.0))
phosphor.hammer((13, 22.8), width=4.4, style=Styles.PrimaryBold)
text(
    (66, 22.8),
    "Full Project Compilation: drawlib build (Multi-Target Output)",
    style=Styles.DarkBold.patch(text_size=11.0),
)

build_flow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)
build_flow.add("1. Project + Cache", description="docs_src/ & cache.db")
build_flow.add(
    "2. drawlib build",
    description="html | pdf | docx | pptx",
    style=Styles.SecondaryNeutral,
)
build_flow.add("3. Deliverables", description="Web, PDF & Office", style=Styles.PrimaryNeutral)
build_flow.draw(xy=(8, 5.5), width=110, height=13.5)

save()
```

</details>



### 4.1 `drawlib build html`
Markdown ドキュメントまたはディレクトリをコンパイルし、レスポンシブな静的 HTML ドキュメントサイト（`navbar.md` が存在する場合は `site`）または結合された単一ページ HTML ドキュメント（`navbar.md` が存在しない場合は `doc`）を生成します。

```bash
drawlib build html <INPUT> [OPTIONS]
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output` | `-o` | `<input_dir>` または `<name>.html` | 出力先ディレクトリまたは HTML ファイルパス。 |
| `--format` | `-f` | `png` | 埋め込み図解の画像フォーマット（`png` または `webp`）。 |
| `--styles` | `-s` | 自動解決された `styles.py` | プロジェクトのスタイル定義スクリプトへのパス。 |
| `--utils` | `-u` | 自動解決された `utils.py` | 描画ヘルパースクリプトへのパス。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` を無視し、すべての図解をクリーンに再レンダリングします。 |

### 4.2 `drawlib build markdown`
埋め込み ````drawlib```` ブロックを含むソース Markdown を、標準的な GitHub Flavored Markdown（GFM）へコンパイルします。レンダリングされた図解は、付属の画像フォルダ（`<doc>_images/`）に出力されます。

```bash
drawlib build markdown docs_src/ -o docs/ [OPTIONS]
```

- `-o/--output`、`-f/--format <png|webp>`、`-s/--styles`、`-u/--utils`、`--no-cache` をサポートします。
- **上書き保護**: ソースファイルのインプレース上書き（`src_abs == dest_abs`）は拒否されます。必ずソースとは別の出力ディレクトリ（例: `docs/` や `docs_markdown/`）を指定してください。

### 4.3 `drawlib build pdf`
Playwright 経由のヘッドレス Chromium を使用し、複数の Markdown 章ディレクトリ、単一の Markdown ファイル、または 16:9 スライドデッキを高精細なベクター PDF へ結合・出力します（`chromium-headless-shell` は初回実行時に自動インストールされるほか、`drawlib cache download --browser` で事前ダウンロード可能です）。

```bash
drawlib build pdf doc_src/ -o report.pdf --toc --page-break
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output` | `-o` | `<first_stem>.pdf` | 出力先 PDF ファイルパス。 |
| `--title` | | H1 見出しから自動抽出 | 表紙およびランニングヘッダーに表示されるドキュメント全体のタイトル。 |
| `--generate-index` | `--toc` | `False` | 1 番目の章（`00_cover.md`）と 2 番目の章の間に自動生成された目次（TOC）を挿入します。 |
| `--page-break` / `--no-page-break` | | `True` | 各章の間に CSS 改ページ（`page-break-before: always`）を挿入します。 |
| `--styles` / `--utils` | `-s` / `-u` | 自動解決 | `styles.py` および `utils.py` へのパス。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` をバイパスし、すべての図解を再レンダリングします。 |
| `--timestamp` | | `False` | PDF メタデータに現在のビルド日時を記録します（決定論的ビルドのためデフォルトでは省略されます）。 |

### 4.4 `drawlib build docx`
Markdown の章ディレクトリ（`doc` プロジェクト）または単一の `.md` ファイルを、ネイティブに編集可能な MS Word（`.docx`）ドキュメント（見出し、本文、箇条書き・番号付きリスト、テーブル、引用ブロック、シンタックスハイライト付きコードブロック、任意の表紙ページ、目次）へコンパイルします。````drawlib```` ブロック（SVG、WebP、アニメーションブロックを含む）は鮮明な高 DPI 静止画 PNG としてレンダリングされます。

```bash
drawlib build docx doc_src/ -o report.docx --generate-index --page-break
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output` | `-o` | `<first_stem>.docx` | 出力する MS Word（`.docx`）ファイルパス。 |
| `--page-break` / `--no-page-break` | | `True` | 結合された各章の間に改ページを挿入します。 |
| `--generate-index` / `--no-generate-index` | | `False` | 目次（インデックス）を生成し、1 番目の文書（`00_cover.md`）と 2 番目の文書の間に挿入します。 |
| `--title` | | H1 見出しから自動抽出 | 結合される Word ドキュメントのタイトルを上書き指定します。 |
| `--dpi` | | `200` | 埋め込み `drawlib` 図解のラスタライズ DPI。 |
| `--styles` / `--utils` | `-s` / `-u` | 自動解決 | `styles.py` および `utils.py` へのパス。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` の読み書きを無効化します。 |
| `--timestamp` | | `False` | 正規化する代わりに、Word メタデータへ現在のビルド日時を記録します。 |

### 4.5 `drawlib build slide`
Markdown スライドファイルのディレクトリ（`slide_src/`）を、デュアルウィンドウ対応の発表者ビュー（`?presenter=1`）を備えたスタンドアロン 16:9 HTML プレゼンテーションデッキ（`index.html`）へコンパイルします。

```bash
drawlib build slide slide_src/ -o slide_html/ [OPTIONS]
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output` | `-o` | `<dir>_html/` | プレゼンテーションデッキの出力先ディレクトリパス。 |
| `--theme` | `-t` | 自動 / `default` | CSS テーマプリセット（`google`、`default`、`google-dark`、`default-dark`）。 |
| `--format` | `-f` | `svg` | 埋め込み図解のデフォルト画像フォーマット（`svg`、`webp`、`png`）。 |
| `--styles` / `--utils` | `-s` / `-u` | 自動解決 | `styles.py` および `utils.py` へのパス。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` の読み書きを無効化します。 |

### 4.6 `drawlib build pptx`
ヘッドレス Chromium で `1920×1080` スライドレイアウトと計算済み CSS スタイルを計測し、Markdown スライドファイルのディレクトリ（`slide_src/`）をネイティブに編集可能な 16:9（`960×540 pt`）MS PowerPoint（`.pptx`）デッキへコンパイルします（`rgba` アルファ対応の `::: block` カード、テキストボックス、箇条書き・番号付きリスト、テーブル、インラインコード、`::: note` スピーカーノートを変換し、````drawlib```` 図解は高 DPI 静止画 PNG として埋め込みます）。

```bash
drawlib build pptx slide_src/ -o deck.pptx --dpi 240 --anim-frame last
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output` | `-o` | `<dir_name>.pptx` | 出力する MS PowerPoint（`.pptx`）ファイルパス。 |
| `--theme` | `-t` | 自動 / `default` | CSS テーマプリセット（`google`、`default`、`google-dark`、`default-dark`）。 |
| `--title` | | デッキから自動抽出 | PowerPoint メタデータのプレゼンテーションタイトルを上書き指定します。 |
| `--dpi` | | `240` | 埋め込み `drawlib` 図解のラスタライズ DPI。 |
| `--anim-frame` | | `last` | アニメーション図解から抽出するフレーム（`first` または `last`）。 |
| `--styles` / `--utils` | `-s` / `-u` | 自動解決 | `styles.py` および `utils.py` へのパス。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` の読み書きを無効化します。 |
| `--timestamp` | | `False` | 正規化する代わりに、PowerPoint メタデータへ現在のビルド日時を記録します。 |

### 4.7 `drawlib build image`
スタンドアロンの Python 図解スクリプト（`.py`）を一括実行するか、Markdown ファイル（`.md`）内の埋め込み描画ブロックを抽出して、画像アセットを生成します。

```bash
drawlib build image images_src/ -o images/ --grid
```

| オプション | 短縮形 | デフォルト値 | 説明 |
|---|---|---|---|
| `--output`, `--output-dir` | `-o` | `None` | 出力ファイルパス（単一スクリプト時）または出力先ディレクトリ。 |
| `--format` | `-f` | スクリプト設定（`png`） | 出力画像フォーマットの一括上書き指定（`png`、`webp`、`jpg`、`pdf`）。 |
| `--styles` / `--utils` | `-s` / `-u` | 自動解決 | `styles.py` および `utils.py` へのパス。 |
| `--grid` | `-g` | `False` | 座標グリッドを重ね合わせた補助画像 `*_grid.<ext>` を同時に保存します。 |
| `--disable-auto-clear` | | `False` | 実行される `.py` ファイル間の自動 `canvas.clear()` を無効化します。 |
| `--enable-auto-initialize` | | `False` | 実行される `.py` ファイル間でキャンバスの完全な再初期化を有効化します。 |
| `--no-cache` | | `False` | `.drawlib/cache.db` をバイパスします。 |

- **Python スクリプト**: ネストされたサブディレクトリ構造を自動的にミラーリングしながら、`save()` の出力先を `-o` 配下へリダイレクトします。実行前に全スクリプトへ静的 AST 解析を行い、複数のスクリプトが同一の出力ファイルへ書き込もうとしている場合は即座に中断します。
- **Markdown ファイル**: 埋め込み ````drawlib```` ブロックを `<markdown_name>_images/<image_file>` サブディレクトリへ抽出します。

---

## 5. スキャフォールディングサブシステム（`drawlib init`）

標準化されたフォルダ構成、設定スクリプト、ビルド自動化スクリプトを備えた新規プロジェクトを初期生成します。

```bash
drawlib init <TYPE> [target] [OPTIONS]
drawlib init list
```

- `<TYPE>`: プロジェクト種別を選択するサブコマンド: `doc`、`site`、`slide`、`images`（エイリアス: `image`）、または `list`。
- `[target]`: プロジェクトおよびソースフォルダのベース名（`<target>_src/` を作成します）。デフォルト値: `doc` は `doc`、`site` は `docs`、`slide` は `slide`、`images` は `images`。
- `-s`, `--style <theme>`: スタイルプリセットテーマ（`default`、`google`、`monochrome` など）。`style.css` と `styles.py` の両方を同期して設定します。
- `-l`, `--lang <code>`: スターターコンテンツおよびフォント設定の言語（`en`、`ja`、`zh-cn`、`ko`、`th`、`hi` など）。デフォルト: `en`。
- `-f`, `--force`: 出力先ディレクトリが既に存在する場合に既存ファイルを上書きします。

---

## 6. 単一図解の抽出とプレビュー（`drawlib show`）

ドキュメント内の埋め込みブロック一覧を表示したり、デスクトップ GUI ウィンドウで図解をプレビューしたり、`-o` 指定時にヘッドレスでディスクへ書き出したりします。

```bash
# 1. List all drawlib blocks in a Markdown document (when [TARGET] is omitted):
drawlib show docs_src/overview.md

# 2. Export block by explicit filename with coordinate grid (Recommended):
drawlib show docs_src/overview.md arch.png -g -o .drawlib/scratch/arch_grid.png

# 3. Export block by 1-based index (or -1 for the last block in the file):
drawlib show docs_src/overview.md 1 -g -o .drawlib/scratch/fig1.png
drawlib show docs_src/overview.md -1 -o .drawlib/scratch/last_fig.png

# 4. Preview standalone Python script in interactive GUI window:
drawlib show my_drawing.py
```

`-o/--output`、`-g/--grid`、`-s/--styles`、`-u/--utils`、`--no-cache` をサポートします。

---

## 7. ローカルサーバーと事前リンク検証（`drawlib serve`）

ビルド済みの HTML ドキュメントをプレビューするため、外部依存ゼロのローカル HTTP 開発サーバー（`Cache-Control: no-store`）を起動します。

```bash
# Start server on default port 8000 (runs link check first and opens browser):
drawlib serve docs_html/

# Custom port without opening browser:
drawlib serve docs_html/ -p 8080 --no-browser

# Pre-flight broken link and missing asset check only (exits 0 if clean, 1 if broken):
drawlib serve docs_html/ --check

# Start server immediately without running pre-flight link scan:
drawlib serve docs_html/ --skip-check
```

---

## 8. デザインシステム・スタイルシート・アセットキャッシュ（`css`, `colors`, `styles`, `cache`）

### 8.1 CSS スタイルシートプリセット（`drawlib css`）
```bash
drawlib css list [html|pdf]                            # List built-in CSS themes and target support
drawlib css show html google                           # Print synthesized Google HTML CSS to terminal
drawlib css show html google -o docs_src/style.css --force  # Export preset to file
```

### 8.2 カラー・スタイルのビジュアルカタログ（`drawlib colors` & `drawlib styles`）
```bash
# Color palettes (default, google, monochrome, css):
drawlib colors list
drawlib colors show google --sort hsv -g -o .drawlib/scratch/colors_google.png

# Style matrices (default, google, monochrome):
drawlib styles list
drawlib styles show google 1 -o .drawlib/scratch/styles_google_p1.png
drawlib styles show default --all -o .drawlib/scratch/styles_default.png
drawlib styles show default -c blue -o .drawlib/scratch/styles_blue.png
```

### 8.3 キャッシュ管理（`drawlib cache`）
```bash
drawlib cache list                  # Inspect font, icon, and map packages and local cache size
drawlib cache download --all        # Pre-download all font, icon, map, and headless Chromium assets
drawlib cache download --fonts      # Pre-download font packages only
drawlib cache download --icons      # Pre-download icon packages only
drawlib cache download --maps       # Pre-download GeoMap packages only
drawlib cache download --browser    # Pre-download headless Chromium browser only
drawlib cache clear --images        # Clear SQLite build & CLI image cache (.drawlib/cache.db)
drawlib cache clear --all           # Clear all caches (fonts, icons, maps, and .drawlib/cache.db)
```

---

## 9. AI ルールカタログ（`drawlib rules`）

組み込みのアーキテクチャ・ライブラリマニュアル（オンデマンドで `_cached_assets/rules/` に付属の図解も自動生成）をターミナルから直接参照できます。

```bash
drawlib rules list                            # List all 92 rule topics and cache status
drawlib rules show agent-instruction          # View AI agent bootstrap manual
drawlib rules show overview                   # View Cartesian geometry principles
drawlib rules show style-guide                # View 50%+ neutral baseline & semantic color rules
drawlib rules show review-guide               # View 3-stage multimodal review loop & 720pt font math
drawlib rules show anim-guide                 # View animation idioms across all modules
drawlib rules show project-overview           # View 4 project archetypes & shared architecture
drawlib rules show project-site               # View multi-page website authoring & navbar.md rules
drawlib rules show project-slide              # View 1920x1080 slide authoring & stage rules
drawlib rules show lib-graph-overview         # View declarative graph layout solvers overview
drawlib rules show lib-diagrams-overview --raw # Output raw Markdown without building/checking cache
drawlib rules show lib-shapes-overview --rebuild # Force regenerate companion rule illustrations
drawlib rules build --all                     # Pre-build illustrations for all 92 rule topics
drawlib rules clear                           # Delete cached rule documents and generated images
```

---

## 10. CLI 終了コード

| 終了コード | 意味 | 主な原因 |
| :---: | :--- | :--- |
| **`0`** | 正常終了 | コマンドが正常に完了した場合（`--check` がリンク切れ 0 件で通過した場合を含む）。 |
| **`1`** | ビルド / 実行エラー | 必須ファイル（`index.md`、`navbar.md`）の欠落、````drawlib```` ブロック内の Python 例外、出力ファイル名の衝突、または `drawlib serve --check` によるリンク切れ検出。 |
| **`2`** | パラメータ不正 / 使用法エラー | 競合する CLI フラグの同時指定（例: `--quiet` と `--verbose` の併用）、不明なサブコマンド、または必須引数の不足。 |
