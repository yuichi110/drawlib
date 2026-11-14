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
# 多言語タイポグラフィと画像処理
:::

::: block xy=(80, 145) width=680 height=790
## 多言語フォントと Dimage 処理

- **和欧混植に標準対応**: 標準 `Font` で英数字と日本語を同時に描画。
- **地域別・等幅パック**: `FontJapanese`・`FontArabic`・`FontSourceCode`。
- **精密アンカー制御**: `halign` / `valign` で基準点からの配置を指定。
- **`Dimage` 画像処理**: 切り抜き・セピア・モザイクと自動キャッシュ。
:::

::: block xy=(800, 140) width=1040 height=800
```drawlib file=typography_i18n_ja.svg
from drawlib.canvas import clear, setup
from drawlib.fonts import Font, FontJapanese, FontSourceCode
from drawlib.images import Dimage, image
from drawlib.lines import line
from drawlib.shapes import circle, rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=104, height=80)

# Top Panel: Multilingual Typography Cards
Panel(
    "多言語フォントファミリーとオンデマンド自動キャッシュ",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    header_height=7.6,
).draw(xy=(2.0, 42.5), width=100.0, height=35.5)

cards = [
    (18.5, Styles.White, "Font.SANSSERIF_BOLD", "English & 日本語", Font.SANSSERIF_BOLD, "標準 和欧混植ゴシック"),
    (52.0, Styles.PrimaryNeutral, "FontJapanese.SERIF", "美しい明朝体表現", FontJapanese.SERIF_BOLD, "地域別・日本語明朝"),
    (85.5, Styles.SecondaryNeutral, "FontSourceCode", "setup(104, 80)", FontSourceCode.SOURCECODEPRO, "ソースコード等幅"),
]
for cx, card_st, badge, sample, fnt, desc in cards:
    rectangle((cx, 56.2), width=30.2, height=22.6, style=card_st.patch(shape_r=1.6))
    text((cx, 63.4), badge, style=Styles.PrimaryBold.patch(text_size=13.5))
    text((cx, 56.2), sample, style=Styles.DarkBold.patch(text_font=fnt, text_size=14.8))
    text((cx, 49.0), desc, style=Styles.Muted.patch(text_size=13.5))

# Bottom Panel: halign Anchor Control + Raster Image / Dimage
Panel(
    "配置アンカー制御 (halign) とラスター画像処理 (Dimage)",
    style=Styles.Neutral.patch(shape_r=2.0),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=16.0),
    header_height=7.6,
).draw(xy=(2.0, 2.0), width=100.0, height=38.0)

# Left Sub-card: halign (left / center / right) with clear vertical offset above dot
rectangle((29.5, 17.0), width=49.0, height=25.0, style=Styles.White.patch(shape_r=1.6))
ax = 29.5
line((ax, 5.6), (ax, 15.2), style=Styles.PrimaryDashed.patch(line_width=1.4))
line((ax, 19.2), (ax, 28.0), style=Styles.PrimaryDashed.patch(line_width=1.4))

anchors = [
    (22.5, "left", "halign='left'", Styles.DarkBold),
    (14.5, "center", "halign='center'", Styles.PrimaryBold),
    (6.5, "right", "halign='right'", Styles.DarkBold),
]
for ay, ha, lbl, st_txt in anchors:
    circle((ax, ay), radius=0.85, style=Styles.DangerFlat)
    text((ax, ay + 1.5), lbl, style=st_txt.patch(text_size=13.8, halign=ha, valign="bottom"))

# Right Sub-card: _assets/linux.png via image() & Dimage.sepia()
rectangle((78.0, 17.0), width=42.0, height=25.0, style=Styles.White.patch(shape_r=1.6))
text((78.0, 26.5), "_assets/linux.png", style=Styles.SecondaryBold.patch(text_size=13.5))
image((68.5, 17.2), width=8.4, image="_assets/linux.png")
text((68.5, 8.2), "image()", style=Styles.DarkBold.patch(text_size=13.5))

sepia_img = Dimage("_assets/linux.png").sepia()
image((87.5, 17.2), width=8.4, image=sepia_img)
text((87.5, 8.2), ".sepia()", style=Styles.DarkBold.patch(text_size=13.5))
```
:::

::: note
技術図解ツールで課題になりやすい日本語の文字化けやフォント差異に対し、Drawlib はデフォルトの `Font` クラスで欧文と日本語（CJK）の美しい混植を標準サポートしています。さらに `FontJapanese`（ゴシック・明朝・M PLUS・さわらび等）、`FontArabic`、`FontSourceCode` などのフォントパックも初回利用時に自動ダウンロード・キャッシュされます。また `halign` / `valign` による精密な文字アンカー制御に加え、`_assets/linux.png` のような外部ラスター画像を `image()` と不変モデル `Dimage` で読み込み、リサイズ・トリミング・セピア・モザイク等のフィルタ処理をコード内で完結できます。
:::
