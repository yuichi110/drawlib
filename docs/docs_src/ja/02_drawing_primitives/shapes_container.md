# 3D コンテナ・フロー・グルーピング

`drawlib.shapes` の **3D コンテナ・フロー・グルーピング** カテゴリは、**6 種類のアーキテクチャ・パイプライン向けプリミティブ** を提供します。マルチディスク対応の 3D ストレージシリンダー（`cylinder`）、3 面シェーディング付きの 3D キューブ（`cube`）、単枚または積層ドキュメント／ファイルカード（`document`）、データフィルタリングおよびコンバージョンファネル（`funnel`）、3 次ベジェ曲線によるクラウドノード・VPC 境界（`cloud`）、そして波括弧・角括弧・丸括弧のグルーピング括弧（`brace`）を利用できます。

```drawlib code=fold align=center file=shapes_container_overview.png caption="クラウド Ingress・3D フィルタリングファネル・キューブ・DB シリンダー・ブレース・積層ドキュメントの組み合わせ"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import brace, cloud, cube, cylinder, document, funnel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=132, height=58)

lbl_dark = Styles.DarkBold.patch(text_size=10.0)
lbl_white = Styles.WhiteBold.patch(text_size=10.0)

# 1. Cloud Ingress
cloud(
    (17, 30),
    width=26,
    height=18,
    variant="flat",
    style=Styles.PrimaryNeutral,
    text="Cloud\nIngress",
    text_style=lbl_dark,
)

# 2. 3D Filtering Funnel
funnel(
    (49, 30),
    width=22,
    height=20,
    variant="3d",
    style=Styles.SecondaryNeutral,
    text="ETL\nFilter",
    text_style=lbl_dark.patch(xy_shift=(0, -1.8)),
)

# 3. 3D Worker Cube & 2-Disk State DB Cylinder
cube(
    (80, 42),
    width=22,
    height=17,
    depth_ratio=0.25,
    style=Styles.PrimaryFlat,
    text="Worker\nPod",
    text_style=lbl_white,
)
cylinder(
    (80, 18),
    width=21,
    height=17,
    disks=2,
    style=Styles.Neutral,
    text="State DB",
    text_style=lbl_dark,
)

# 4. Curly Brace + Stacked Audit Documents
brace(
    (95.5, 30),
    width=4.2,
    height=40,
    symbol="}",
    style=Styles.PrimaryBold.patch(line_width=2.2),
)
document(
    (115, 30),
    width=23,
    height=24,
    variant="folded_wave",
    stacked=3,
    style=Styles.SecondaryNeutral,
    text="Audit\nReports",
    text_style=lbl_dark,
)

line((30.5, 30), (37, 30), arrow_head="->", style=Styles.DarkBold)
line((60.5, 34), (68, 41), arrow_head="->", style=Styles.DarkBold)
line((60.5, 26), (68, 19), arrow_head="->", style=Styles.DarkBold)
line((99, 30), (102.5, 30), arrow_head="->", style=Styles.PrimaryBold)

save()
```

---

## 1. 基本の幾何構造とコンセプト

このカテゴリの全 6 プリミティブは、外接バウンディングボックスの中心座標 `xy` を基準（アンカー）とし、3D 投影・波形・クラウドのローブ・括弧のスパインをすべて厳密に `(width, height)` の内側へ正規化します。マルチプラッタの `disks` や `angle=-90` 回転、3 面自動陰影の `depth_ratio`、`document` の各バリエーションとシート積層、`funnel` のネック比率、正規化された `cloud` ローブ、そして先端位置をスライドできる `brace` が各コンポーネントをどのように変形させるかを確認してみましょう。

```drawlib code=fold align=center file=shapes_container_parameter_tour.png caption="パラメータ＆ジオメトリツアー: cylinder・cube・document・funnel・cloud・brace のライブ変形（APNG アニメーション）"
from __future__ import annotations

from drawlib.anim import Animation
from drawlib.canvas import save, setup
from drawlib.icons import code as code_icons
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import brace, circle, cloud, cube, cylinder, document, funnel, rectangle
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
    ("1. cylinder & cube", "disks & depth_ratio"),
    ("2. document()", "variants & stacked"),
    ("3. funnel & cloud", "neck & lobe styles"),
    ("4. brace()", "symbol & tip pos"),
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
    """Draw left Python code editor + bottom geometric concept note."""
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
        "containers_3d.py",
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

    # Inner coordinate sheet (54 x 40) with subtle grid lines
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


GHOST_BOX = Styles.MutedDashed.patch(
    shape_fill_color=(0, 0, 0, 0),
    shape_line_color=(176, 192, 214),
    shape_line_width=1.1,
)

# =========================================================================
# Part 1: cylinder (disks & angle=-90 FIFO queue) and cube (depth_ratio)
# =========================================================================
for d_cnt, ang, dur in ((1, 0, 0.50), (2, -45, 0.50), (3, -90, 3.3)):
    code_cyl = [
        "from drawlib.shapes import cylinder",
        "from drawlib.styles import Styles",
        "",
        "cylinder(  # 1..3 storage platter seams",
        f"    (36, 30), 18, 25, disks={d_cnt},",
        "    style=Styles.PrimaryNeutral,",
        ")",
        "q_st = Styles.SecondaryNeutral.patch(",
        f"    angle={ang},  # Horizontal FIFO queue",
        ")",
        "cylinder((74, 30), 15, 22, style=q_st)",
    ]
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(
            1,
            code_cyl,
            (4, 8),
            phosphor.database,
            "Storage Stacks & Queues (cylinder)",
            "disks=1..3 adds curved platter divider seams",
            "angle=-90 rotates into a horizontal FIFO pipe",
        )
        scx, scy = draw_geometry_studio(
            f"disks={d_cnt} | {ang}°",
            f"disks={d_cnt} Platter Seams  •  angle={ang}° FIFO Queue",
        )
        cy_c = scy - 0.6
        lx, rx = scx - 13.8, scx + 12.2

        cylinder(
            (lx, cy_c),
            width=18.0,
            height=25.0,
            disks=d_cnt,
            style=Styles.PrimaryNeutral,
        )
        text((lx, cy_c + 15.6), f"disks = {d_cnt}", style=Styles.PrimaryBold.patch(text_size=9.6))
        text((lx, cy_c - 15.4), "Multi-Platter DB", style=Styles.MutedBold.patch(text_size=9.5))

        cylinder(
            (rx, cy_c),
            width=15.0,
            height=22.0,
            style=Styles.SecondaryNeutral.patch(angle=ang),
        )
        text((rx, cy_c + 15.6), f"angle = {ang}°", style=Styles.DarkBold.patch(text_size=9.6))
        if ang == -90:
            line(
                (rx - 9.0, cy_c - 11.6),
                (rx + 9.0, cy_c - 11.6),
                arrow_head="->",
                style=Styles.PrimaryBold.patch(line_width=1.5),
            )
            text((rx, cy_c - 15.4), "Left → Right FIFO", style=Styles.PrimaryBold.patch(text_size=9.5))

for dr, dur in ((0.15, 0.50), (0.28, 0.50), (0.40, 3.3)):
    code_cube = [
        "from drawlib.shapes import cube",
        "from drawlib.styles import Styles",
        "",
        "# Auto 3-face isometric shading",
        "cube(",
        "    (50, 30), width=28, height=24,",
        f"    depth_ratio={dr:.2f},",
        "    style=Styles.PrimaryFlat,",
        '    text="Worker",',
        ")",
    ]
    with anim.frame(duration=dur):
        draw_step_bar(1)
        draw_left_pane(
            1,
            code_cube,
            (6, 6),
            phosphor.cube,
            "3-Face Shaded Block (cube)",
            "Fits full 3D projection inside width × height",
            "Auto-shades front, +light top, and -dark side",
        )
        scx, scy = draw_geometry_studio(
            f"depth_ratio = {dr:.2f}",
            f"cube(depth_ratio={dr:.2f})  •  Auto 3-Face Shading",
        )
        cy_b = scy - 0.8
        rectangle((scx, cy_b), width=28.0, height=24.0, style=GHOST_BOX)
        cube(
            (scx, cy_b),
            width=28.0,
            height=24.0,
            depth_ratio=dr,
            style=Styles.PrimaryFlat,
            text="Worker",
            text_style=Styles.WhiteBold.patch(text_size=10.5),
        )
        if dr >= 0.40:
            text((scx, cy_b + 15.2), "Top Face (+28% Light)", style=Styles.PrimaryBold.patch(text_size=9.6))
            text(
                (scx + 15.6, cy_b + 1.0),
                "Right\n(×0.82)",
                style=Styles.DarkBold.patch(text_size=9.5, halign="left"),
            )
            text((scx, cy_b - 15.2), "Dashed = Exact 28 × 24 Box", style=Styles.MutedBold.patch(text_size=9.5))

# =========================================================================
# Part 2: document — variant ("wave" -> "folded" -> "folded_wave") & stacked
# =========================================================================
DOC_STATES = [
    ("wave", 1, "PrimaryNeutral", "Invoice", 3.2),
    ("folded", 2, "PrimaryNeutral", "Configs", 0.50),
    ("folded_wave", 3, "SecondaryNeutral", "Reports", 3.3),
]
for d_var, stk, st_name, d_lbl, dur in DOC_STATES:
    code_doc = [
        "from drawlib.shapes import document",
        "from drawlib.styles import Styles",
        "",
        "document(",
        "    (50, 30), width=25, height=27,",
        f'    variant="{d_var}",',
        f"    stacked={stk},",
        f"    style=Styles.{st_name},",
        f'    text="{d_lbl}",',
        ")",
    ]
    with anim.frame(duration=dur):
        draw_step_bar(2)
        draw_left_pane(
            2,
            code_doc,
            (5, 6),
            phosphor.files if stk > 1 else phosphor.file_text,
            "Silhouettes & Stacks (document)",
            "Variants mix bottom S-waves & dog-ear folds",
            "stacked=1..3 cascades lightened back sheets",
        )
        scx, scy = draw_geometry_studio(
            f'"{d_var}", ×{stk}',
            f'variant="{d_var}", stacked={stk}  •  Bounded Stack',
        )
        cy_d = scy - 0.6
        rectangle((scx, cy_d), width=25.0, height=27.0, style=GHOST_BOX)
        document(
            (scx, cy_d),
            width=25.0,
            height=27.0,
            variant=d_var,
            stacked=stk,
            style=getattr(Styles, st_name),
            text=d_lbl,
            text_style=Styles.DarkBold.patch(text_size=10.2),
        )
        if d_var == "wave":
            text((scx, cy_d + 16.0), "Straight Top Edge", style=Styles.MutedBold.patch(text_size=9.5))
            text((scx, cy_d - 16.2), "Cubic-Bézier S-Wave Base", style=Styles.PrimaryBold.patch(text_size=9.6))
        elif stk == 3:
            text((scx, cy_d + 16.0), "3 Cascading Sheets + Dog-Ear Flap", style=Styles.PrimaryBold.patch(text_size=9.6))
            text((scx, cy_d - 16.2), "All 3 Sheets Fit Exact 25 × 27 Box", style=Styles.DarkBold.patch(text_size=9.5))

# =========================================================================
# Part 3: funnel (neck ratios) & cloud (normalized lobe variants)
# =========================================================================
for nw_r, nh_r, dur in ((0.45, 0.25, 0.50), (0.22, 0.42, 3.3)):
    code_fun = [
        "from drawlib.shapes import funnel",
        "from drawlib.styles import Styles",
        "",
        "funnel(",
        "    (50, 30), width=30, height=25,",
        '    variant="3d",',
        f"    neck_width_ratio={nw_r:.2f},",
        f"    neck_height_ratio={nh_r:.2f},",
        "    style=Styles.PrimaryNeutral,",
        '    text="Ingest",',
        ")",
    ]
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(
            3,
            code_fun,
            (6, 7),
            phosphor.funnel,
            "3D Rim & Spout Ratios (funnel)",
            'variant="3d" adds a shaded elliptical top rim',
            "neck_width/height_ratio tune the lower spout",
        )
        scx, scy = draw_geometry_studio(
            f"neck_w = {nw_r:.2f}",
            f'funnel("3d")  •  neck_w={nw_r:.2f}, neck_h={nh_r:.2f}',
        )
        cy_f = scy + 0.8
        fw, fh = 30.0, 25.0
        funnel(
            (scx, cy_f),
            width=fw,
            height=fh,
            variant="3d",
            neck_width_ratio=nw_r,
            neck_height_ratio=nh_r,
            style=Styles.PrimaryNeutral,
            text="Ingest",
            text_style=Styles.DarkBold.patch(text_size=10.0, xy_shift=(0, -1.8)),
        )
        nw_half = 0.5 * fw * nw_r
        y_bot = cy_f - fh / 2.0
        y_neck = y_bot + fh * nh_r
        line(
            (scx - nw_half, y_bot - 2.4),
            (scx + nw_half, y_bot - 2.4),
            arrow_head="<->",
            style=Styles.DangerBold.patch(line_width=1.5),
        )
        text(
            (scx, y_bot - 5.4),
            f"neck_width_ratio = {nw_r:.2f}",
            style=Styles.DangerBold.patch(text_size=9.6),
        )
        line(
            (scx + nw_half + 2.8, y_bot),
            (scx + nw_half + 2.8, y_neck),
            arrow_head="<->",
            style=Styles.PrimaryBold.patch(line_width=1.5),
        )
        text(
            (scx + nw_half + 4.4, 0.5 * (y_bot + y_neck)),
            f"h×{nh_r:.2f}",
            style=Styles.PrimaryBold.patch(text_size=9.5, halign="left"),
        )

for c_var, dur in (("standard", 0.50), ("flat", 3.2), ("fluffy", 3.3)):
    code_cld = [
        "from drawlib.shapes import cloud",
        "from drawlib.styles import Styles",
        "",
        "# Normalized strictly to width × height",
        "cloud(",
        "    (50, 30), width=38, height=22,",
        f'    variant="{c_var}",',
        "    style=Styles.SecondaryNeutral,",
        f'    text="{c_var}",',
        ")",
    ]
    with anim.frame(duration=dur):
        draw_step_bar(3)
        draw_left_pane(
            3,
            code_cld,
            (6, 6),
            phosphor.cloud,
            "Normalized Bézier Lobes (cloud)",
            "standard (8), flat (grounded), fluffy (12)",
            "Every variant normalizes to exact width×height",
        )
        scx, scy = draw_geometry_studio(
            f'variant="{c_var}"',
            f'cloud(variant="{c_var}")  •  Normalized to 38 × 22',
        )
        cy_cl = scy - 0.8
        rectangle((scx, cy_cl), width=38.0, height=22.0, style=GHOST_BOX)
        cloud(
            (scx, cy_cl),
            width=38.0,
            height=22.0,
            variant=c_var,
            style=Styles.SecondaryNeutral,
            text=c_var,
            text_style=Styles.DarkBold.patch(text_size=10.5),
        )
        line(
            (scx - 19.0, cy_cl + 13.0),
            (scx + 19.0, cy_cl + 13.0),
            arrow_head="<->",
            style=Styles.PrimaryBold.patch(line_width=1.4),
        )
        text((scx, cy_cl + 16.0), "width = 38 (Exact Span)", style=Styles.PrimaryBold.patch(text_size=9.6))
        text((scx, cy_cl - 15.0), "Dashed = 38 × 22 Bounding Box", style=Styles.MutedBold.patch(text_size=9.5))

# =========================================================================
# Part 4: brace — symbol ("}" -> "]" -> ")") & tip_position_ratio
# =========================================================================
BRACE_STATES: list[tuple[str, float | None, float, tuple[int, int]]] = [
    ("}", 0.50, 3.2, (6, 6)),
    ("]", None, 0.50, (6, 6)),
    (")", None, 3.2, (6, 6)),
    ("}", 0.25, 3.2, (6, 7)),
    ("}", 0.75, 3.3, (6, 7)),
]
for sym, tpr, dur, hl in BRACE_STATES:
    tpr_line = f"    tip_position_ratio={tpr:.2f}," if tpr is not None else "    tip_position_ratio=None,"
    code_brc = [
        "from drawlib.shapes import brace",
        "from drawlib.styles import Styles",
        "",
        "# Wraps left stack; tip points right",
        "brace(",
        "    (50, 30), width=4.8, height=26.4,",
        f'    symbol="{sym}",',
        tpr_line,
        "    style=Styles.PrimaryBold,",
        ")",
    ]
    is_sliding = hl == (6, 7)
    with anim.frame(duration=dur):
        draw_step_bar(4)
        draw_left_pane(
            4,
            code_brc,
            hl,
            phosphor.brackets_curly,
            "Sliding Tip Position (brace)" if is_sliding else "Grouping Brackets (brace)",
            "tip_position_ratio moves tip bottom→top (0..1)"
            if is_sliding
            else '"}" curly, "]" square, and ")" round families',
            "0.25 targets bottom node; 0.75 targets top"
            if is_sliding
            else "Stroke uses style.line_color & style.line_width",
        )
        badge = f"tip_pos = {tpr:.2f}" if is_sliding and tpr is not None else f'symbol = "{sym}"'
        foot = (
            f'brace("}}", tip_position_ratio={tpr:.2f})  •  Aimed Tip'
            if tpr is not None
            else f'brace(symbol="{sym}")  •  Wraps Stacked Node Cards'
        )
        scx, scy = draw_geometry_studio(badge, foot)
        cy_br = scy - 0.8
        bh = 26.4

        # 3 stacked source node cards on the left
        for idx_c, c_lbl in enumerate(("Pod 1", "Pod 2", "Pod 3")):
            yc = cy_br + (1 - idx_c) * 7.6
            rectangle(
                (scx - 14.0, yc),
                width=14.8,
                height=5.8,
                style=Styles.Neutral.patch(shape_r=1.3),
                text=c_lbl,
                text_style=Styles.DarkBold.patch(text_size=9.6),
            )

        # Central grouping brace
        bx = scx - 1.5
        brace(
            (bx, cy_br),
            width=4.8,
            height=bh,
            symbol=sym,  # type: ignore[arg-type]
            tip_position_ratio=tpr,
            style=Styles.PrimaryBold,
        )

        # 3 target route nodes on the right (at +6.6, 0.0, -6.6 = exact 0.75, 0.50, 0.25 tip positions)
        targets = (("Node A", 0.75, 6.6), ("Node B", 0.50, 0.0), ("Node C", 0.25, -6.6))
        for t_lbl, t_ratio, dy in targets:
            yt = cy_br + dy
            is_hit = sym == "}" and tpr == t_ratio
            t_st = Styles.PrimaryFlat.patch(shape_r=1.3) if is_hit else Styles.PrimaryNeutral.patch(shape_r=1.3)
            t_tst = Styles.WhiteBold.patch(text_size=9.6) if is_hit else Styles.DarkBold.patch(text_size=9.6)
            rectangle((scx + 14.2, yt), width=15.4, height=5.2, style=t_st, text=t_lbl, text_style=t_tst)
            if is_hit:
                line(
                    (bx + 2.9, yt),
                    (scx + 6.0, yt),
                    arrow_head="->",
                    style=Styles.PrimaryBold.patch(line_width=1.8),
                )

        top_note = (
            f"tip_position_ratio = {tpr:.2f}"
            if tpr is not None
            else ('Square Bracket "]"' if sym == "]" else 'Round Parenthesis ")"')
        )
        text((scx, cy_br + 16.0), top_note, style=Styles.PrimaryBold.patch(text_size=9.6))

save()
```

- **3D の奥行きとプラッタ段数（`cylinder`, `cube`）**: `cylinder` は `disks` によって円弧状のディスク継ぎ目線を追加し（`angle=-90` で水平キューに回転可能）、`cube` は `depth_ratio` に応じて 3 面の陰影を自動付与します。
- **ドキュメント形状とシート積層（`document`）**: 波状の底辺や暗色化された右上の角折れフラップ（`"wave"`, `"folded"`, `"folded_wave"`）を組み合わせ、`stacked > 1` では明度を上げた背面シートをカスケード積層します。
- **注ぎ口比率と正規化されたクラウドローブ（`funnel`, `cloud`）**: `funnel` は `neck_width_ratio` と `neck_height_ratio` で下部スパウトの寸法を調整し、`cloud` の全 variant は 3 次ベジェ曲線のローブを厳密に `(width, height)` の内側へ正規化します。
- **グルーピング括弧とスライド可能な先端（`brace`）**: 波括弧（`"{}"`）、角括弧（`"[]"`、`shape_r` で `90°` 角を丸め可能）、丸括弧（`"()"`）に対応し、`tip_position_ratio`（`0.0`〜`1.0`）によって波括弧の先端突起を狙ったターゲットノードへ合わせられます。

---

## 2. 3D コンテナ・フロー・グルーピングプリミティブの早見表

全 6 関数のアンカー基準、主なアーキテクチャ上の役割、形状引数、自動シェーディング・テキスト配置を以下のマトリクスで比較できます。

| 関数 | デフォルトアンカー | 主なアーキテクチャ上の役割 | バリエーションと主要な形状引数 | シェーディングとテキスト配置 |
| :--- | :--- | :--- | :--- | :--- |
| **`cylinder`** | 中央 `(cx, cy)` | リレーショナル DB、ディスクアレイ、オブジェクトストレージ、FIFO キュー | `disks: int = 1`, `style.patch(angle=-90)` | 上部の楕円キャップを自動で明度アップ。テキストはボディ中央に配置。 |
| **`cube`** | 中央 `(cx, cy)` | 3D コンピュートノード、コンテナ、ハードウェアアプライアンス | `depth_ratio: float \| None = None`（デフォルト `0.25`） | 3 面の自動シェーディング（正面・明度アップ上面・暗色化右側面）。テキストは正面中央に配置。 |
| **`document`** | 中央 `(cx, cy)` | 帳票出力、設定ファイル、ログ断片、レポート束 | `variant`（`"wave"`, `"folded"`, `"double_wave"`, `"folded_wave"`）, `stacked: int = 1`, `wave_ratio`, `fold_ratio` | 暗色化された角折れフラップと明度アップした背面スタックシート。テキストは最前面シートの中央に配置。 |
| **`funnel`** | 中央 `(cx, cy)` | データフィルタリング段、イベント絞り込み、コンバージョンファネル | `variant`（`"standard"`, `"3d"`, `"curved"`）, `neck_width_ratio`, `neck_height_ratio` | `"3d"` は陰影付きの楕円上部リムを描画。テキストは上部コーン中央に配置。 |
| **`cloud`** | 中央 `(cx, cy)` | 外部クラウド／SaaS ノード、VPC／WAN の破線境界領域 | `variant`（`"standard"`, `"flat"`, `"fluffy"`, `"simple"`）, `bump_ratio` | `(width, height)` に厳密に正規化された滑らかな 3 次ベジェローブ。 |
| **`brace`** | 中央 `(cx, cy)` | 波括弧・角括弧・丸括弧によるグルーピング装飾 | `symbol`（`"{}"`, `"[]"`, `"()"`）, `direction`（`"left"`, `"right"`, `"top"`, `"bottom"`）, `tip_ratio`, `tip_position_ratio` | `style.line_width` と `style.line_color` で制御される開いたベクターストローク。 |

---

## 3. 3D シリンダーとデータベーススタック (`cylinder`)

リレーショナルデータベース、オブジェクトストレージバケット、ディスクアレイ、メッセージキュー向けに、`cylinder` は自動的に明るくシェーディングされた楕円形の上面キャップを持つ 3D 円筒コンテナを描画します。

```python
cylinder(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    style: Style,
    disks: int = 1,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータリファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | シリンダー外接バウンディングボックスの中心座標 `(x, y)`。 |
| `width` | `float` | *必須* | シリンダーの水平全幅（`> 0`）。 |
| `height` | `float` | *必須* | 上下の楕円キャップを含むシリンダーの垂直全高（`> 0`）。 |
| `disks` | `int` | `1` | 積層されるストレージディスクの段数（`>= 1`）。`disks >= 2` を指定すると、マルチプラッタのデータベースストレージを表す円弧状の水平分割線がボディに描画されます。 |
| `style` | `Style` | *必須* | 塗りつぶしと枠線のスタイル。上部の楕円キャップは `style.shape_fill_color` から自動的に明度アップされます。FIFO メッセージキューやパイプライン向けに水平横向きへ回転させるには `style.patch(angle=-90)` を指定します。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 中央配置されるテキストラベルと任意のタイポグラフィ上書き設定。 |

```drawlib code=show align=center file=shapes_domain_cylinder.png caption="単一シリンダー、3 ディスクのデータベーススタック、水平回転させたメッセージキュー"
from drawlib.canvas import save, setup
from drawlib.shapes import cylinder
from drawlib.styles import Styles

setup(width=118, height=48)

# 1. Single-tier cache cylinder
cylinder(
    (22, 24),
    width=26,
    height=34,
    style=Styles.Neutral,
    text="Cache",
    text_style=Styles.DarkBold.patch(text_size=11.5),
)

# 2. 3-disk database stack (disks=3)
cylinder(
    (60, 24),
    width=28,
    height=36,
    disks=3,
    style=Styles.PrimaryFlat,
    text="Primary\nDB",
    text_style=Styles.WhiteBold.patch(text_size=11.5),
)

# 3. Horizontal rotated cylinder (angle=-90 for message queue)
cylinder(
    (97, 24),
    width=20,
    height=32,
    style=Styles.SecondaryNeutral.patch(angle=-90),
    text="Queue",
    text_style=Styles.DarkBold.patch(text_size=11.5),
)

save()
```

---

## 4. 3D キューブと直方体ブロック (`cube`)

`cylinder` を補完するプリミティブとして、`cube` は中心座標 `xy` のバウンディングボックス `(width, height)` に厳密に収まる斜投影（オブリーク）の 3D キューブまたは直方体ボックスを描画します。

```python
cube(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    depth_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータリファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | 外接 3D バウンディングボックスの中心座標 `(x, y)`。 |
| `width` | `float` | *必須* | 右側面への斜投影部分を含む 3D ボックスの厳密な外接水平幅（`> 0`）。 |
| `height` | `float` | *必須* | 上面への斜投影部分を含む 3D ボックスの厳密な外接垂直高さ（`> 0`）。 |
| `depth_ratio` | `float \| None` | `None` | `min(width, height)` に対する 3D 斜投影の奥行き比率を `(0.0, 1.0)` で指定します。`None` の場合はデフォルトの `0.25` になります。小さい値（`0.15`）では薄い 3D カードになり、大きい値（`0.40`）では奥行きのある立体ブロックになります。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線（`shape_line_color`, `shape_line_width`, `shape_line_style`）、および回転（`angle`）を制御するスタイル。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 外接ボックス全体ではなく **正面（フロントフェイス）** の中央に自動配置されるラベル。3D の稜線とテキストが干渉しません。 |

### 3 面の自動シェーディングとストロークの仕組み
- **3 面の自動陰影付け**: `style.shape_fill_color` を基に、Drawlib が 3 つの面の明度を自動計算します。
  1. **正面（Front Face）**: 基準となる `style.shape_fill_color`。
  2. **上面（Top Face）**: 上方からのライティングを再現するよう白方向へ明度アップ（標準塗りで `+28%`、高輝度なニュートラル塗りで `+55%`）。
  3. **右側面（Right Side Face）**: 自然な立体影を生むよう暗色化（標準塗りで `×0.82`、ニュートラル塗りで `×0.92`）。
- **単一統合ストロークパス**: 外周の輪郭線と内部の 3 本の Y 字稜線は単一の統合 `PathPatch` として描画されるため、`Dashed` や `Dotted` の破線・点線スタイルでも共有辺で線が二重に重なることはありません。

```drawlib code=show align=center file=shapes_domain_cube.png caption="多様なスタイルと depth_ratio による 3D キューブおよび直方体ブロック"
from drawlib.canvas import save, setup
from drawlib.shapes import cube
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

# 1. Standard Flat Cube (depth_ratio=0.25 default)
cube(
    (18, 27),
    width=23,
    height=23,
    style=Styles.PrimaryFlat,
    text="Pod A",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
text((18, 9), "depth_ratio=0.25 (Flat)", style=Styles.DarkBold.patch(text_size=9.5))

# 2. Shallow 3D Block (depth_ratio=0.15)
cube(
    (49, 27),
    width=23,
    height=23,
    depth_ratio=0.15,
    style=Styles.PrimaryNeutral,
    text="Shallow",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
text((49, 9), "depth_ratio=0.15", style=Styles.DarkBold.patch(text_size=9.5))

# 3. Deep 3D Cube (depth_ratio=0.40)
cube(
    (80, 27),
    width=23,
    height=23,
    depth_ratio=0.40,
    style=Styles.SecondaryNeutral,
    text="Deep",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
text((80, 9), "depth_ratio=0.40", style=Styles.DarkBold.patch(text_size=9.5))

# 4. Wide Hardware Appliance Block (26x19, dashed)
cube(
    (111, 27),
    width=26,
    height=19,
    depth_ratio=0.24,
    style=Styles.Neutral.patch(shape_line_style="dashed"),
    text="Appliance",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((111, 9), "Wide Block (Dashed)", style=Styles.DarkBold.patch(text_size=9.5))

save()
```

---

## 5. ドキュメント・ファイル・複数枚スタック (`document`)

フローチャートの出力工程、設定／ソースファイル、ログストリームの断片、複数ページのレポート束向けに、`document` は 4 種類の `variant` シルエットと複数シートのカスケード積層（`stacked >= 1`）を提供します。

```python
document(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal[
        "wave", "standard",
        "folded", "page", "note",
        "double_wave", "snippet",
        "folded_wave", "report",
    ] = "wave",
    stacked: int = 1,
    wave_ratio: float | None = None,
    fold_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータリファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | 外接ドキュメントバウンディングボックス（積層された全シートを含む）の中心座標 `(x, y)`。 |
| `width` | `float` | *必須* | ドキュメントバウンディングボックスの水平全幅（`> 0`）。 |
| `height` | `float` | *必須* | ドキュメントバウンディングボックスの垂直全高（`> 0`）。 |
| `variant` | `DocumentVariant` | `"wave"` | ドキュメントシートのシルエットスタイル（下記の **Document の `variant` リファレンス** を参照）。 |
| `stacked` | `int` | `1` | 重ねて表示するドキュメントシートの枚数（`>= 1`）。`stacked > 1`（例: `2` や `3`）を指定すると、`(width, height)` の内側に収まるよう奥の右上から手前の左下へ向かってシートがカスケード配置され、背面シートは自動的に明るくシェーディングされます。 |
| `wave_ratio` | `float \| None` | `None` | シート高さに対する波形の上下振幅比率を `(0.0, 1.0)` で指定します。デフォルトは `0.14`。`"wave"`, `"double_wave"`, `"folded_wave"` で有効です。 |
| `fold_ratio` | `float \| None` | `None` | `min(sheet_w, sheet_h)` に対する右上の角折れ（ドッグイヤー）サイズ比率を `(0.0, 1.0)` で指定します。デフォルトは `0.24`。`"folded"` および `"folded_wave"` で有効です。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、および回転（`angle`）を制御するスタイル。角折れ付きの variant では、立体的なコントラストを生むよう三角形の折り返しフラップが自動的に暗色化されます。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | **最前面のシート** 上で視覚的に中央配置されるテキストラベル（下端の波や右上の角折れと干渉しないよう自動オフセット補正されます）。 |

### Document の `variant` リファレンス

| `variant` | 使用可能なエイリアス | 上辺 | 下辺 | 有効な比率引数 | 主なユースケース |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`"wave"`** *(デフォルト)* | `"standard"` | 直線 | 3 次ベジェ S 字波形 | `wave_ratio` | 定番の ISO フローチャート帳票／出力シンボル、請求書、生成アーティファクト。 |
| **`"folded"`** | `"page"`, `"note"` | 右上の角折れ（ドッグイヤー） | 直線 | `fold_ratio` | 設定ファイル（`config.yaml`）、ソースコードファイル、Markdown／PDF ページ、UML ノート。 |
| **`"double_wave"`** | `"snippet"` | 3 次ベジェ S 字波形 | 3 次ベジェ S 字波形 | `wave_ratio` | 連続するログストリーム（`access.log`）、抜粋テキスト断片、データストリームチャンク。 |
| **`"folded_wave"`** | `"report"` | 右上の角折れ（ドッグイヤー） | 3 次ベジェ S 字波形 | `wave_ratio`, `fold_ratio` | ファイルらしさと帳票の波形表現を兼ね備えた複数ページの技術レポート、仕様書、監査ログ。 |

```drawlib code=show align=center file=shapes_domain_document.png caption="4 種類のドキュメント variant（上段）と複数枚スタック・比率のカスタマイズ（下段）"
from drawlib.canvas import save, setup
from drawlib.shapes import document
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=78)

# Row 1: The 4 Document Variants (stacked=1)
row1 = [
    ("wave", "Invoice", 18, Styles.PrimaryFlat, Styles.WhiteBold.patch(text_size=10.5), 'variant="wave"'),
    ("folded", "config.yaml", 49, Styles.PrimaryNeutral, Styles.DarkBold.patch(text_size=10.0), 'variant="folded"'),
    ("double_wave", "access.log", 80, Styles.SecondaryNeutral, Styles.DarkBold.patch(text_size=10.0), 'variant="double_wave"'),
    ("folded_wave", "Audit\nReport", 110, Styles.Neutral, Styles.DarkBold.patch(text_size=10.0), 'variant="folded_wave"'),
]
for var, lbl, cx, st, tst, cap in row1:
    document((cx, 59), width=22, height=25, variant=var, style=st, text=lbl, text_style=tst)
    text((cx, 42.5), cap, style=Styles.DarkBold.patch(text_size=9.5))

# Row 2: Multi-sheet stacking (stacked=3) and wave_ratio / fold_ratio customization
document(
    (18, 22),
    width=23,
    height=25,
    variant="wave",
    stacked=3,
    style=Styles.PrimaryNeutral,
    text="Batch\n(x3)",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((18, 5.5), "wave, stacked=3", style=Styles.DarkBold.patch(text_size=9.5))

document(
    (49, 22),
    width=23,
    height=25,
    variant="folded",
    stacked=3,
    style=Styles.SecondaryNeutral,
    text="Pages\n(x3)",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((49, 5.5), "folded, stacked=3", style=Styles.DarkBold.patch(text_size=9.5))

document(
    (80, 22),
    width=22,
    height=25,
    variant="wave",
    wave_ratio=0.25,
    style=Styles.Neutral,
    text="Deep\nWave",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((80, 5.5), "wave_ratio=0.25", style=Styles.DarkBold.patch(text_size=9.5))

document(
    (110, 22),
    width=22,
    height=25,
    variant="folded",
    fold_ratio=0.36,
    style=Styles.PrimaryNeutral,
    text="Large\nFold",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((110, 5.5), "fold_ratio=0.36", style=Styles.DarkBold.patch(text_size=9.5))

save()
```

---

## 6. データフィルタリングとコンバージョンファネル (`funnel`)

ETL データフィルタリングパイプライン、イベント重複排除ステージ、レートリミッタ、コンバージョンファネル向けに、`funnel` は広い上部コーンから細い下部スパウト（注ぎ口）へと絞り込まれる漏斗形状を描画します。

```python
funnel(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal[
        "standard", "flat",
        "3d", "cylinder",
        "curved",
    ] = "standard",
    neck_width_ratio: float | None = None,
    neck_height_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータおよび `variant` リファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | ファネルバウンディングボックスの中心座標 `(x, y)`。 |
| `width` / `height` | `float` | *必須* | 上端リムの水平全幅（`> 0`）と垂直全高（`> 0`）。 |
| `variant` | `FunnelVariant` | `"standard"` | ファネルのシルエットおよびシェーディング形式（下記の表を参照）。 |
| `neck_width_ratio` | `float \| None` | `None` | `width` に対する下部ネック幅の比率を `[0.08, 0.85]` で指定します。`None` の場合はデフォルトの `0.28` になります。 |
| `neck_height_ratio` | `float \| None` | `None` | `height` に対する下部ネック高さの比率を `[0.05, 0.75]` で指定します。`None` の場合はデフォルトの `0.36` になります。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線、および回転（`angle`、例: 左から右への水平フィルタには `angle=90` または `-90`）を制御するスタイル。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 広い上部コーン領域に自動で中央配置されるテキストラベルと任意のスタイル。 |

| `variant` | 使用可能なエイリアス | 幾何構造とシェーディング | 主なユースケース |
| :--- | :--- | :--- | :--- |
| **`"standard"`** *(デフォルト)* | `"flat"` | フラットな 2D 台形の上部コーン＋垂直な矩形スパウト | すっきりした 2D フローチャートのフィルタゲート、SQL `WHERE` フィルタ、水平パイプラインの絞り込み段。 |
| **`"3d"`** | `"cylinder"` | 暗色シェーディングされた楕円形の上部開口リムを持つ 3D ファネル | データレイクのインジェストファネル、テレメトリコレクタ、`cylinder` や `cube` と並べる 3D アーキテクチャ図。 |
| **`"curved"`** | — | ネック部へ滑らかに繋がる 3 次ベジェ S 字カーブの側壁 | マーケティング／分析のコンバージョンファネル、滑らかなストリーム集約ノード。 |

```drawlib code=show align=center file=shapes_container_funnel.png caption="3 種類のファネル variant（standard・3d・curved）、ネック比率の調整、水平回転"
from drawlib.canvas import save, setup
from drawlib.shapes import funnel
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=48)

lbl = Styles.DarkBold.patch(text_size=9.5)

# 1. Standard 2D funnel
funnel(
    (18, 27),
    width=24,
    height=23,
    variant="standard",
    style=Styles.PrimaryFlat,
    text="Filter",
    text_style=Styles.WhiteBold.patch(text_size=10.5),
)
text((18, 8.5), 'variant="standard"', style=lbl)

# 2. 3D shaded elliptical-top funnel
funnel(
    (49, 27),
    width=24,
    height=23,
    variant="3d",
    style=Styles.PrimaryNeutral,
    text="Ingest",
    text_style=Styles.DarkBold.patch(text_size=10.5),
)
text((49, 8.5), 'variant="3d"', style=lbl)

# 3. Smooth cubic-Bézier curved funnel
funnel(
    (80, 27),
    width=24,
    height=23,
    variant="curved",
    style=Styles.SecondaryNeutral,
    text="Convert",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((80, 8.5), 'variant="curved"', style=lbl)

# 4. Horizontal rotated funnel (angle=90 -> left-to-right reducer)
funnel(
    (111, 27),
    width=22,
    height=24,
    variant="standard",
    neck_width_ratio=0.35,
    neck_height_ratio=0.28,
    style=Styles.Neutral.patch(angle=90),
    text="Sample",
    text_style=Styles.DarkBold.patch(text_size=9.5, angle=0, xy_shift=(0, 1.5)),
)
text((111, 8.5), "angle=90 (Horizontal)", style=lbl)

save()
```

---

## 7. クラウドノードとネットワーク境界 (`cloud`)

`cloud` は、中心座標 `xy` の外接バウンディングボックス `(width, height)` に厳密に収まるよう正規化された滑らかな 3 次ベジェ曲線のクラウドシルエットを描画します。

```python
cloud(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    variant: Literal[
        "standard",
        "flat", "flat_bottom",
        "fluffy", "dense",
        "simple", "minimal",
    ] = "standard",
    bump_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータリファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | クラウドバウンディングボックスの中心座標 `(x, y)`。 |
| `width` | `float` | *必須* | クラウドの厳密な外接水平幅（`> 0`）。 |
| `height` | `float` | *必須* | クラウドの厳密な外接垂直高さ（`> 0`）。 |
| `variant` | `CloudVariant` | `"standard"` | クラウドのシルエットスタイル（下記の **Cloud の `variant` リファレンス** を参照）。 |
| `bump_ratio` | `float \| None` | `None` | 外向きローブ（もこもこした膨らみ）の深さ比率を `(0.0, 1.0)` で指定します。`None` の場合は選択した `variant` に最適なデフォルト値（`0.20`〜`0.24`）が使用されます。小さい値（`0.12`）では控えめで浅いクラウドになり、大きい値（`0.34`）では深く際立ったローブになります。 |
| `style` | `Style` | *必須* | 塗りつぶし、枠線（VPC／サブネット境界には `Dashed` が最適）、および回転（`angle`）を制御するスタイル。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | 中央配置されるテキストラベルと任意のタイポグラフィ上書き設定。 |

### Cloud の `variant` リファレンス

| `variant` | 使用可能なエイリアス | ローブ構造 | デフォルト `bump_ratio` | 主なユースケース |
| :--- | :--- | :--- | :---: | :--- |
| **`"standard"`** *(デフォルト)* | — | 全周にわたる 8 個の非対称ローブ | `0.22` | 汎用的な「インターネット」、SaaS、外部ネットワークノード。 |
| **`"flat"`** | `"flat_bottom"` | 平坦な水平底辺＋上部の 4 個のドーム | `0.24` | 内部のテキストやアイコンに高い視覚的安定感を与える独立クラウドサービスカードやゲートウェイノード。 |
| **`"fluffy"`** | `"dense"` | 全周にわたる 12 個の細かいローブ | `0.20` | 大規模な VPC、WAN、マルチノードクラスタの境界領域（特に `shape_line_style="dashed"` との併用が効果的）。 |
| **`"simple"`** | `"minimal"` | 幅広で対称な 6 個のローブ | `0.24` | コンパクトなクラウドバッジ、小型アイコン、思考の吹き出し。 |

```drawlib code=show align=center file=shapes_domain_cloud.png caption="4 種類のクラウド variant（上段）と bump_ratio の比較・破線 VPC 境界での利用例（下段）"
from drawlib.canvas import save, setup
from drawlib.shapes import cloud, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=74)

# Row 1: The 4 Cloud Variants
variants = [
    ("standard", 18, Styles.PrimaryFlat, Styles.WhiteBold.patch(text_size=10.5)),
    ("flat", 48, Styles.PrimaryNeutral, Styles.DarkBold.patch(text_size=10.5)),
    ("fluffy", 78, Styles.SecondaryNeutral, Styles.DarkBold.patch(text_size=10.5)),
    ("simple", 108, Styles.Neutral, Styles.DarkBold.patch(text_size=10.5)),
]
for v_name, cx, st, tst in variants:
    cloud((cx, 57), width=26, height=17, variant=v_name, style=st, text=v_name, text_style=tst)
    text((cx, 43), f'variant="{v_name}"', style=Styles.DarkBold.patch(text_size=9.5))

# Row 2 Left: Shallow vs Deep bump_ratio
cloud(
    (20, 22),
    width=26,
    height=17,
    variant="standard",
    bump_ratio=0.12,
    style=Styles.Neutral,
    text="Shallow",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((20, 7.5), "bump_ratio=0.12", style=Styles.DarkBold.patch(text_size=9.5))

cloud(
    (52, 22),
    width=26,
    height=17,
    variant="standard",
    bump_ratio=0.35,
    style=Styles.PrimaryNeutral,
    text="Deep Lobes",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
text((52, 7.5), "bump_ratio=0.35", style=Styles.DarkBold.patch(text_size=9.5))

# Row 2 Right: Large fluffy dashed VPC enclosure containing service cards
cloud((96, 22), width=50, height=24, variant="fluffy", style=Styles.SecondaryNeutral.patch(shape_line_style="dashed"))
rectangle((86, 21), width=14, height=10, style=Styles.Neutral.patch(shape_r=1.5), text="API", text_style=Styles.DarkBold.patch(text_size=9.5))
rectangle((106, 21), width=14, height=10, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="App", text_style=Styles.WhiteBold.patch(text_size=9.5))
text((96, 7.5), 'variant="fluffy" (Dashed VPC Boundary)', style=Styles.DarkBold.patch(text_size=9.5))

save()
```

---

## 8. グルーピング用の波括弧・角括弧・丸括弧 (`brace`)

`brace` は、波括弧（`{`, `}`）・角括弧（`[`, `]`）・丸括弧（`(`, `)`）のグルーピング括弧を上下左右の 4 方向（`"left"`, `"right"`, `"top"`, `"bottom"`）のいずれにも描画します。線の太さは `style.line_width` で制御します。

```python
brace(
    xy: tuple[float, float],
    width: float,
    height: float,
    *,
    symbol: Literal[
        "{", "}", "{}", "curly",
        "[", "]", "[]", "square",
        "(", ")", "()", "round",
    ] = "{",
    direction: Literal["left", "right", "top", "bottom"] | None = None,
    tip_ratio: float | None = None,
    tip_position_ratio: float | None = None,
    style: Style,
    text: str = "",
    text_style: Style | None = None,
) -> None
```

### パラメータリファレンス

| パラメータ | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | ブレースの外接バウンディングボックスの中心座標 `(x, y)`。 |
| `width` | `float` | *必須* | バウンディングボックスの水平幅（`> 0`）。縦向きブレース（`"left"` / `"right"`）では括弧の奥行き、横向きブレース（`"top"` / `"bottom"`）ではスパン長になります。 |
| `height` | `float` | *必須* | バウンディングボックスの垂直高さ（`> 0`）。縦向きブレース（`"left"` / `"right"`）ではスパン長、横向きブレース（`"top"` / `"bottom"`）では括弧の奥行きになります。 |
| `symbol` | `BraceSymbol` | `"{"` | 括弧ファミリーおよびデフォルトの向き（下記の **`symbol` と `direction` のバリエーション** を参照）。 |
| `direction` | `BraceDirection \| None` | `None` | グループ対象領域のどの辺に括弧を配置するか（外側の背／先端が向く方向）を `"left"`, `"right"`, `"top"`, `"bottom"` から指定します（下記の表を参照）。 |
| `tip_ratio` | `float \| None` | `None` | **波括弧（`{}`）専用**: 括弧の奥行きのうち中央の外向き突起（ティップ）が占める割合を `(0.0, 1.0)` で指定します。デフォルトは `0.50`。大きい値（`0.70`）では鋭く突き出た先端になり、小さい値（`0.25`）では控えめな先端になります。 |
| `tip_position_ratio` | `float \| None` | `None` | **波括弧（`{}`）専用**: スパン軸に沿った中央突起の位置を `(0.0, 1.0)` で指定します（`"left"` / `"right"` では下から上、`"top"` / `"bottom"` では左から右へ計測）。デフォルトは `0.50`（対称な中央）。 |
| `style` | `Style` | *必須* | 線の太さは `style.line_width`（または `style.shape_line_width`）、色は `style.line_color`（または `style.shape_line_color`）、線種は `style.line_style`、回転は `style.angle` で制御します。角括弧 `"square"`（`[`, `]`）では、`style.shape_r` により 2 つの `90°` 角を丸められます。 |
| `text` / `text_style` | `str` / `Style \| None` | `""` / `None` | `xy` の中央に配置される任意のテキストラベルとタイポグラフィ上書き設定。 |

### `symbol` と `direction` のバリエーション

| `symbol` の値 | 括弧ファミリー | 自動 `direction`（`direction=None` 時） | 対応する形状モディファイア |
| :--- | :--- | :--- | :--- |
| **`"{"`**, **`"{}"`**, **`"curly"`** | 波括弧 `{` | `"left"`（先端が左を向き、両端が右へカール） | `tip_ratio`, `tip_position_ratio` |
| **`"}"`** | 波括弧 `}` | `"right"`（先端が右を向き、両端が左へカール） | `tip_ratio`, `tip_position_ratio` |
| **`"["`**, **`"[]"`**, **`"square"`** | 角括弧 `[` | `"left"`（背が左側、両端が右向き） | `style.patch(shape_r=...)` による角丸め |
| **`"]"`** | 角括弧 `]` | `"right"`（背が右側、両端が左向き） | `style.patch(shape_r=...)` による角丸め |
| **`"("`**, **`"()"`**, **`"round"`** | 丸括弧 `(` | `"left"`（弧が左へ膨らみ、両端が右向き） | 滑らかな 3 次ベジェ曲線アーチ |
| **`")"`** | 丸括弧 `)` | `"right"`（弧が右へ膨らみ、両端が左向き） | 滑らかな 3 次ベジェ曲線アーチ |

| `direction` の値 | 向き | 背／先端が向く方向 | 開口端が向く方向 |
| :--- | :--- | :--- | :--- |
| **`"left"`** | 縦向き（`span = height`） | 左（`-X`） | 右（`+X`、右側の要素群を囲む） |
| **`"right"`** | 縦向き（`span = height`） | 右（`+X`） | 左（`-X`、左側の要素群を囲む） |
| **`"top"`** | 横向き（`span = width`） | 上（`+Y`） | 下（`-Y`、下側の要素群を囲む） |
| **`"bottom"`** | 横向き（`span = width`） | 下（`-Y`） | 上（`+Y`、上側の要素群を囲む） |

```drawlib code=show align=center file=shapes_domain_brace.png caption="括弧ファミリー（{}, [], ()）、4 方向の配置（left, right, top, bottom）、波括弧の先端比率"
from drawlib.canvas import save, setup
from drawlib.shapes import brace, rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=74)

# Row 1 Left: Three Bracket Families: { } , [ ] , ( )
families = [
    ("{}", "{", "}", 15, Styles.PrimaryBold.patch(line_width=2.5)),
    ("[]", "[", "]", 38, Styles.DarkBold.patch(line_width=2.5, shape_r=1.5)),
    ("()", "(", ")", 61, Styles.SecondaryBold.patch(line_width=2.5)),
]
for label, sym_l, sym_r, cx, st in families:
    brace((cx - 5, 57), width=4.0, height=21, symbol=sym_l, style=st)
    brace((cx + 5, 57), width=4.0, height=21, symbol=sym_r, style=st)
    text((cx, 57), label, style=Styles.DarkBold.patch(text_size=10.5))
    text((cx, 41.5), f'symbol="{sym_l}" / "{sym_r}"', style=Styles.DarkBold.patch(text_size=9.5))

# Row 1 Right: All 4 Directions (top, bottom, left, right) around a card group
for idx, name in enumerate(("API", "App", "DB")):
    rx = 88 + idx * 12
    rectangle((rx, 57), width=10, height=12, style=Styles.Neutral.patch(shape_r=1.5), text=name, text_style=Styles.DarkBold.patch(text_size=9.5))

brace((100, 66.5), width=34, height=3.8, symbol="{", direction="top", style=Styles.PrimaryBold.patch(line_width=2.0))
text((100, 71.0), 'direction="top"', style=Styles.PrimaryBold.patch(text_size=9.5))

brace((100, 47.5), width=34, height=3.8, symbol="{", direction="bottom", style=Styles.SecondaryBold.patch(line_width=2.0))
text((100, 41.5), 'direction="bottom"', style=Styles.SecondaryBold.patch(text_size=9.5))

# Row 2: Curly brace tip_ratio & tip_position_ratio variations
brace((22, 23), width=30, height=6.0, symbol="{", direction="top", tip_ratio=0.25, style=Styles.DarkBold.patch(line_width=2.2))
text((22, 11), "tip_ratio=0.25 (Shallow)", style=Styles.DarkBold.patch(text_size=9.5))

brace((62, 23), width=30, height=6.0, symbol="{", direction="top", tip_ratio=0.75, style=Styles.PrimaryBold.patch(line_width=2.2))
text((62, 11), "tip_ratio=0.75 (Sharp)", style=Styles.DarkBold.patch(text_size=9.5))

brace((104, 23), width=34, height=6.0, symbol="{", direction="top", tip_position_ratio=0.25, style=Styles.AccentBold.patch(line_width=2.2))
text((104, 11), "tip_position_ratio=0.25", style=Styles.DarkBold.patch(text_size=9.5))

save()
```
