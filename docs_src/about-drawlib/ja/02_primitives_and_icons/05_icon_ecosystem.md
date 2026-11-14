::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# 34スイート・4,500種超のベクターアイコン
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=icon_suites_gallery_ja.svg
from drawlib.canvas import clear, setup
from drawlib.icons import (
    ai,
    aws,
    azure,
    cnative,
    data,
    devops,
    gcp,
    original_ai,
    original_cloud,
    original_network,
    original_security,
    original_server,
    phosphor,
    security,
)
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=82)

pw, ph, hh = 84.8, 38.0, 7.2
cols = [1.5, 89.7]
rows = [42.5, 1.5]

panel_titles = [
    ["1. Phosphor ベクターアイコン (5ウェイト)", "2. 公式クラウドスイート (gcp · aws · azure)"],
    ["3. 15種の公式ドメインブランドスイート", "4. 15種のベンダー中立2Dスイート (original_*)"],
]
for r_idx, y0 in enumerate(rows):
    h_st = Styles.PrimaryNeutral if r_idx == 0 else Styles.SecondaryNeutral
    for c_idx, x0 in enumerate(cols):
        Panel(
            panel_titles[r_idx][c_idx],
            style=Styles.Neutral.patch(shape_r=1.8),
            header_style=h_st,
            text_style=Styles.DarkBold.patch(text_size=14.6),
            header_height=hh,
        ).draw(xy=(x0, y0), width=pw, height=ph)

# 1. Phosphor Vector Font Icons (5 weights)
x0, y0 = cols[0], rows[0]
p1_items = [
    (phosphor.rocket_launch, "thin", "rocket_launch"),
    (phosphor.cpu, "light", "cpu"),
    (phosphor.globe, "regular", "globe"),
    (phosphor.sparkle, "bold", "sparkle"),
    (phosphor.shield_check, "fill", "shield_check"),
]
for idx, (fn, w_name, lbl) in enumerate(p1_items):
    cx = x0 + 9.6 + idx * 16.4
    is_hero = w_name == "fill"
    tile_st = Styles.PrimaryFlat if is_hero else Styles.White
    ic_st = (Styles.White if is_hero else Styles.Primary).patch(icon_style=w_name)
    text((cx, y0 + 25.8), w_name, style=Styles.PrimaryBold.patch(text_size=11.6))
    rectangle((cx, y0 + 16.5), width=11.4, height=11.4, style=tile_st.patch(shape_r=1.8))
    fn((cx, y0 + 16.5), width=7.2, style=ic_st)
    text((cx, y0 + 6.2), lbl, style=Styles.Dark.patch(text_size=11.5))

# 2. Official Cloud Suites (gcp, aws, azure)
x0, y0 = cols[1], rows[0]
p2_items = [
    (gcp.cloud_run, "gcp", "Cloud Run"),
    (gcp.bigquery, "gcp", "BigQuery"),
    (aws.aws_lambda, "aws", "Lambda"),
    (aws.simple_storage_service, "aws", "Amazon S3"),
    (azure.cosmos_db, "azure", "Cosmos DB"),
]
for idx, (fn, suite, lbl) in enumerate(p2_items):
    cx = x0 + 9.6 + idx * 16.4
    text((cx, y0 + 25.8), suite, style=Styles.PrimaryBold.patch(text_size=11.6))
    rectangle((cx, y0 + 16.5), width=11.4, height=11.4, style=Styles.White.patch(shape_r=1.8))
    fn((cx, y0 + 16.5), width=7.4, style=Styles.Primary)
    text((cx, y0 + 6.2), lbl, style=Styles.Dark.patch(text_size=11.5))

# 3. 15 Official Domain Brand Suites (ai, cnative, devops, data, security)
x0, y0 = cols[0], rows[1]
p3_items = [
    (ai.gemini, "ai", "Gemini"),
    (cnative.kubernetes, "cnative", "Kubernetes"),
    (devops.github, "devops", "GitHub"),
    (data.postgresql, "data", "PostgreSQL"),
    (security.cloudflare, "security", "Cloudflare"),
]
for idx, (fn, suite, lbl) in enumerate(p3_items):
    cx = x0 + 9.6 + idx * 16.4
    text((cx, y0 + 25.8), suite, style=Styles.SecondaryBold.patch(text_size=11.6))
    rectangle((cx, y0 + 16.5), width=11.4, height=11.4, style=Styles.White.patch(shape_r=1.8))
    fn((cx, y0 + 16.5), width=7.4, style=Styles.Primary)
    text((cx, y0 + 6.2), lbl, style=Styles.Dark.patch(text_size=11.5))

# 4. 15 Vendor-Neutral Original 2D Suites (original_*)
x0, y0 = cols[1], rows[1]
p4_items = [
    (original_cloud.multi_cloud, "cloud", "multi_cloud"),
    (original_ai.ai_agent, "ai", "ai_agent"),
    (original_server.gpu_server, "server", "gpu_server"),
    (original_network.firewall, "network", "firewall"),
    (original_security.zero_trust, "security", "zero_trust"),
]
for idx, (fn, suite, lbl) in enumerate(p4_items):
    cx = x0 + 9.6 + idx * 16.4
    text((cx, y0 + 25.8), suite, style=Styles.SecondaryBold.patch(text_size=11.6))
    rectangle((cx, y0 + 16.5), width=11.4, height=11.4, style=Styles.PrimaryNeutral.patch(shape_r=1.8))
    fn((cx, y0 + 16.5), width=7.6, style=Styles.Primary)
    text((cx, y0 + 6.2), lbl, style=Styles.Dark.patch(text_size=11.5))
```
:::

::: note
`drawlib.icons` は全34モジュール・合計4,500種類を超えるアイコンを共通の中心アンカー API `(xy, width, *, style)` と型安全な `StrEnum` で統合しています。第1層の Phosphor アイコンは1,512種×5ウェイト（`thin`・`light`・`regular`・`bold`・`fill`、計7,560グリフ）をベクターフォントとして描画し、`style.icon_color` で自在に着色できます。第2層は `gcp`・`aws`・`azure` の公式クラウドアイコンと15分野のブランドスイート（`ai`・`cnative`・`devops`・`data`・`security` 等）、第3層は特定のベンダーに依存しない概念図解に最適な15種の `original_*` 2Dパステルスイートを提供します。
:::
