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
# 技術白書：HTML・ベクターPDF・Word出力
:::

::: block xy=(80, 145) width=680 height=790
## 長文仕様書・白書 (`type = "doc"`)

- **章ファイルの自動結合**: `00_cover.md`, `01_intro.md` を単一文書へ統合
- **表紙・目次の自動生成**: `--generate-index` で表紙とリンク目次を構築
- **3形式へ同時出力**: HTML・A4ベクターPDF・編集可能な `.docx` を生成

```bash
# doc_src/ から3形式を一括ビルド
uv run drawlib build html
uv run drawlib build pdf --generate-index
uv run drawlib build docx --generate-index
```
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=doc_multi_export_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

# Left Panel: Linear Markdown Source Repository
src_panel = Panel(
    "doc_src/{en,ja}/",
    style=Styles.Neutral.patch(shape_r=2.2),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.5),
    icon=phosphor.folder_open,
    icon_style=Styles.PrimaryBold,
    header_variant="filled",
    header_height=9.2,
)
src_panel.draw(xy=(2.0, 11.0), width=33.0, height=58.0)

files = [
    ("00_cover.md", "表紙・メタ情報"),
    ("01_intro.md", "背景と目的"),
    ("02_arch.md", "```drawlib 構成図"),
    ("03_security.md", "脅威分析・表"),
]
for idx, (fname, fdesc) in enumerate(files):
    fy = 52.0 - idx * 9.2
    rectangle((18.5, fy), width=28.6, height=7.4, style=Styles.White.patch(shape_r=1.4))
    phosphor.file_text((7.2, fy), width=3.8, style=Styles.PrimaryBold)
    text((10.2, fy + 1.4), fname, style=Styles.DarkBold.patch(text_size=13.5, halign="left"))
    text((10.2, fy - 1.9), fdesc, style=Styles.Muted.patch(text_size=11.6, halign="left"))

rectangle((18.5, 16.2), width=28.6, height=6.6, style=Styles.PrimaryFlat.patch(shape_r=1.4))
text((18.5, 16.2), "--generate-index", style=Styles.WhiteBold.patch(text_size=13.5))

# Routing Spine from Source to 3 Artifact Cards
line((35.0, 40.0), (40.5, 40.0), style=Styles.PrimaryBold)
line((40.5, 14.5), (40.5, 65.5), style=Styles.PrimaryBold)
circle((40.5, 40.0), radius=1.1, style=Styles.PrimaryFlat)

outputs = [
    {
        "yc": 65.5,
        "title": "単一ページ HTML",
        "badge": "WEB",
        "icon": phosphor.globe,
        "card_style": Styles.White,
        "badge_style": Styles.SecondaryNeutral,
        "badge_text_style": Styles.DarkBold,
        "desc": "追従目次サイドバー・ダークモード\nインラインSVGの拡大表示に対応",
    },
    {
        "yc": 40.0,
        "title": "A4 ベクター PDF",
        "badge": "PRINT",
        "icon": phosphor.file_pdf,
        "card_style": Styles.PrimaryNeutral,
        "badge_style": Styles.PrimaryFlat,
        "badge_text_style": Styles.WhiteBold,
        "desc": "表紙・リンク付き目次を自動生成\n拡大しても劣化しないベクター図解",
    },
    {
        "yc": 14.5,
        "title": "MS Word 文書 (.docx)",
        "badge": "OFFICE",
        "icon": phosphor.file_doc,
        "card_style": Styles.White,
        "badge_style": Styles.SecondaryNeutral,
        "badge_text_style": Styles.DarkBold,
        "desc": "ネイティブ見出し・表・高精細図版\n社内外のWordレビューにそのまま対応",
    },
]

for out in outputs:
    yc = out["yc"]
    line((40.5, yc), (46.0, yc), arrow_head="->", style=Styles.PrimaryBold)
    rectangle((74.0, yc), width=56.0, height=21.5, style=out["card_style"].patch(shape_r=2.2))

    circle((53.5, yc), radius=5.2, style=Styles.WhiteFlat if out["card_style"] == Styles.PrimaryNeutral else Styles.PrimaryNeutral)
    out["icon"]((53.5, yc), width=5.6, style=Styles.PrimaryBold)

    text((61.2, yc + 4.8), out["title"], style=Styles.DarkBold.patch(text_size=15.5, halign="left"))
    rectangle((94.8, yc + 4.8), width=10.2, height=4.4, style=out["badge_style"].patch(shape_r=1.2))
    text((94.8, yc + 4.8), out["badge"], style=out["badge_text_style"].patch(text_size=11.5))

    text((61.2, yc - 3.2), out["desc"], style=Styles.Dark.patch(text_size=13.0, halign="left"))

save()
```
:::

::: note
設計仕様書・RFC・セキュリティ白書・顧客向け提案書など、最初から最後まで通読する長文ドキュメントには `type = "doc"` を使用します。
番号付きの章ファイル（`00_cover.md`, `01_intro.md`, `02_arch.md`）が単一の整合した仕様書へ自動結合され、`--generate-index` オプションを付けるだけで美しい表紙ページとクリック可能な目次（ページ番号付き）が自動生成されます。
最大の強みは、Git上の同じ `doc_src/` 原稿から、Web閲覧用の単一ページHTML、印刷・配布用のA4ベクターPDF、そして法務や取引先レビューで求められるネイティブ編集可能なMicrosoft Word（`.docx`）の3形式を同時にコンパイルできる点です。
:::
