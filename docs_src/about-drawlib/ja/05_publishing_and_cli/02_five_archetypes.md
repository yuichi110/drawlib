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
# 用途に応じた5つのプロジェクト種別
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=five_archetypes_grid_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

# Top unified scaffolding command banner
rectangle((88.0, 75.8), width=172.0, height=7.4, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.terminal_window((10.5, 75.8), width=4.6, style=Styles.PrimaryBold)
text(
    (16.0, 75.8),
    "uv run drawlib init project <type> <dir>",
    style=Styles.PrimaryBold.patch(text_size=13.5, halign="left"),
)
text(
    (170.5, 75.8),
    "単一コンパイラ  •  5つの専用テンプレート  •  Web・PDF・Office対応",
    style=Styles.Muted.patch(text_size=11.5, halign="right"),
)

archetypes = [
    {
        "name": "site",
        "icon": phosphor.globe,
        "featured": False,
        "src": "docs_src/<lang>/",
        "use_case": "体系的ガイドサイト\nnavbar.md・全文検索\nダークモード・多言語",
        "example": "例: www.drawlib.com",
        "outputs": ["HTML", "Search", "SVG"],
    },
    {
        "name": "catalog",
        "icon": phosphor.list_magnifying_glass,
        "featured": True,
        "src": "catalog_src/<lang>/",
        "use_case": "2カラムAPI辞書\nH1/H2自動カテゴリ\n/ キー即時フィルタ",
        "example": "例: drawlib.com/api",
        "outputs": ["HTML", "/ Filter", "SVG"],
    },
    {
        "name": "doc",
        "icon": phosphor.file_text,
        "featured": False,
        "src": "doc_src/<lang>/",
        "use_case": "単一長文仕様書・白書\n--generate-index\n表紙・目次自動生成",
        "example": "設計書・RFC・提案書",
        "outputs": ["HTML", "PDF", "DOCX"],
    },
    {
        "name": "slide",
        "icon": phosphor.presentation_chart,
        "featured": False,
        "src": "slide_src/<lang>/",
        "use_case": "16:9 スライド画面\n?presenter=1 同期\n::: note 発表原稿",
        "example": "登壇資料・勉強会",
        "outputs": ["HTML", "PDF", "PPTX"],
    },
    {
        "name": "images",
        "icon": phosphor.images,
        "featured": False,
        "src": "images_src/*.py",
        "use_case": "Python図解バッチ\nベクター＆ラスター\nCIアセット一括生成",
        "example": "README・論文図版",
        "outputs": ["SVG", "PNG", "WebP"],
    },
]

card_w = 32.4
card_h = 66.8
gap = 2.5

for idx, item in enumerate(archetypes):
    x0 = 2.0 + idx * (card_w + gap)
    cx = x0 + card_w / 2.0
    is_feat = item["featured"]

    panel = Panel(
        item["name"],
        style=(Styles.PrimaryNeutral if is_feat else Styles.White).patch(shape_r=2.2),
        header_style=Styles.PrimaryFlat if is_feat else Styles.SecondaryNeutral,
        text_style=(Styles.WhiteBold if is_feat else Styles.DarkBold).patch(text_size=15.5),
        header_variant="filled",
        header_height=9.2,
        header_align="center",
    )
    panel.draw(xy=(x0, 2.5), width=card_w, height=card_h)

    if is_feat:
        rectangle((cx, 56.8), width=18.5, height=3.8, style=Styles.AccentFlat.patch(shape_r=1.8))
        text((cx, 56.8), "v0.3.10 新機能", style=Styles.WhiteBold.patch(text_size=10.5))

    circle_y = 48.8 if is_feat else 51.0
    circle(
        (cx, circle_y),
        radius=5.0,
        style=Styles.WhiteFlat if is_feat else Styles.PrimaryNeutral,
    )
    item["icon"]((cx, circle_y), width=5.6, style=Styles.PrimaryBold)

    # Source folder badge
    src_y = 39.2
    rectangle(
        (cx, src_y),
        width=28.4,
        height=5.6,
        style=(Styles.WhiteFlat if is_feat else Styles.Neutral).patch(shape_r=1.4),
    )
    text((cx, src_y), item["src"], style=Styles.PrimaryBold.patch(text_size=11.2))

    # Primary use case lines
    text((cx, 28.0), item["use_case"], style=Styles.Dark.patch(text_size=11.4))
    text((cx, 18.8), item["example"], style=Styles.Muted.patch(text_size=10.6))

    line((x0 + 2.4, 15.6), (x0 + card_w - 2.4, 15.6), style=Styles.Muted)

    # Output format badges
    outs = item["outputs"]
    bw = 8.8
    bgap = 1.0
    start_bx = cx - (len(outs) * bw + (len(outs) - 1) * bgap) / 2.0 + bw / 2.0
    for b_idx, out_label in enumerate(outs):
        bx = start_bx + b_idx * (bw + bgap)
        is_primary_out = is_feat and b_idx == 1
        rectangle(
            (bx, 9.2),
            width=bw,
            height=5.2,
            style=(Styles.PrimaryFlat if is_primary_out else Styles.SecondaryNeutral).patch(shape_r=1.2),
        )
        text(
            (bx, 9.2),
            out_label,
            style=(Styles.WhiteBold if is_primary_out else Styles.DarkBold).patch(text_size=10.5),
        )

save()
```
:::

::: note
Drawlibでは `uv run drawlib init project <type> <dir>` コマンド1つで、用途に最適化された5つのプロジェクト種別を生成できます。すべて共通のPython描画エンジンと `drawlib.toml` 設定で動作します。
1. **`site`**：`docs_src/<lang>/` と `navbar.md` から、全文検索・ダークモード・多言語切替を備えた複数ページ構成の技術ドキュメントサイトを生成します（`www.drawlib.com` で採用）。
2. **`catalog`**（v0.3.10新機能）：`catalog_src/<lang>/` から `1 Markdown = 1 HTML` の2カラムAPI・スキーマ辞書を生成します。`navbar.md` 不要で `# H1` とバッジ付き `## H2` を自動抽出し、`/` キーで瞬時に絞り込めます（`www.drawlib.com/api` で採用）。
3. **`doc`**：`doc_src/<lang>/` の複数章を統合し、HTMLに加えて `--generate-index` による表紙・目次付きA4ベクターPDFと、編集可能なWord（`.docx`）を出力します。
4. **`slide`**：`slide_src/<lang>/` から `1920×1080` スライドHTML、`?presenter=1` 同期発表者ビュー、ベクターPDF、編集可能なPowerPoint（`.pptx`）を生成します。
5. **`images`**：`images_src/*.py` から `SVG`・`PNG`・`WebP`・`PDF` アセットを一括生成します。
:::
