# 5. スタイルシステム・デザイントークン・多言語フォント

Drawlib は、イミュータブルな `Style` / `Color` モデル、セマンティックなデザイントークン（`Styles.*`・`Colors.*`）、およびオンデマンド自動キャッシュ対応の多言語フォントエンジン（`drawlib.fonts`）によって、座標ロジックと視覚デザインを完全に分離します。

```drawlib align=center code=fold file=style_tokens_matrix_ja.png caption="図 5.1: GoogleStyles トークン一覧 — ニュートラル基盤・外枠／基本ロール・強調 Flat・線種バリエーション"
from drawlib.canvas import save, setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=74)

row_hdr = Styles.DarkBold.patch(text_size=10.2, halign="left")
dark_lbl = Styles.DarkBold.patch(text_size=10.0)
white_lbl = Styles.WhiteBold.patch(text_size=10.0)
xs = [45.5, 72.2, 98.9, 125.6]
sw_w, sw_h = 24.2, 10.8

# 1段目: ニュートラル基盤（全図の 50% 以上を構成）
text((6.0, 61.0), "1. ニュートラル基盤\n   (50%以上原則)", style=row_hdr)
r1 = [
    ("Neutral", Styles.Neutral),
    ("PrimaryNeutral", Styles.PrimaryNeutral),
    ("SecondaryNeutral", Styles.SecondaryNeutral),
    ("White", Styles.White),
]
for cx, (name, st) in zip(xs, r1):
    rectangle((cx, 61.0), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=dark_lbl)

# 2段目: 外枠線（Outline）と基本ロール
text((6.0, 44.5), "2. 外枠・基本ロール\n   (*Outline / *)", style=row_hdr)
r2 = [
    ("PrimaryOutline", Styles.PrimaryOutline, Styles.PrimaryBold.patch(text_size=10.0)),
    ("SecondaryOutline", Styles.SecondaryOutline, Styles.SecondaryBold.patch(text_size=10.0)),
    ("AccentOutline", Styles.AccentOutline, Styles.DarkBold.patch(text_size=10.0)),
    ("Primary", Styles.Primary, white_lbl),
]
for cx, (name, st, ts) in zip(xs, r2):
    rectangle((cx, 44.5), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=ts)

# 3段目: 強調ベタ塗りトークン（*Flat + WhiteBold）
text((6.0, 28.0), "3. 強調ベタ塗り\n   (*Flat + 白文字)", style=row_hdr)
r3 = [
    ("PrimaryFlat", Styles.PrimaryFlat),
    ("AccentFlat", Styles.AccentFlat),
    ("SuccessFlat", Styles.SuccessFlat),
    ("DangerFlat", Styles.DangerFlat),
]
for cx, (name, st) in zip(xs, r3):
    rectangle((cx, 28.0), width=sw_w, height=sw_h, style=st.patch(shape_r=1.8), text=name, text_style=white_lbl)

# 4段目: 接続線・境界線種バリエーション
text((6.0, 11.5), "4. 線種トークン\n   (Bold / Dashed)", style=row_hdr)
r4 = [
    ("DarkBold", Styles.DarkBold),
    ("PrimaryBold", Styles.PrimaryBold),
    ("SecondaryDashed", Styles.SecondaryDashedBold),
    ("MutedDotted", Styles.MutedDottedBold),
]
for cx, (name, st) in zip(xs, r4):
    line((cx - 10.5, 14.2), (cx + 10.5, 14.2), arrow_head="->", style=st)
    text((cx, 8.2), name, style=dark_lbl)

save()
```

---

## 5.1 動的テーマ注入: `drawlib.styles` と `preset_styles` の分離

作図スクリプトおよび Markdown の `drawlib` ブロック内では、常に `drawlib.styles` から **PascalCase の `Colors` と `Styles`** をインポートします。

```python
from drawlib.styles import Colors, Styles
```

モジュール名と衝突する小文字の `styles` / `colors` は使わず、また各図のコード内で `GoogleStyles` などの具象プリセットを直接インポートしないのが鉄則です。`drawlib.styles` はプロジェクト直下の `styles.py`（および多言語構成における `ja/styles.py` などの言語別スタイル定義）から動的に注入されるファサードとして機能します。

- **`DefaultStyles` / `DefaultColors`**: 6 段階の明度スケール（`DefaultStyles1`〜`DefaultStyles6`）を備える標準技術ドキュメント向けテーマ。
- **`GoogleStyles` / `GoogleColors`**: Google スライド／Workspace 準拠のプレゼンテーション配色（`drawlib.toml` の `style = "google"`、本書で採用）。
- **`MonochromeStyles` / `MonochromeColors`**: モノクロ印刷・学術論文・特許図面に適した 8 階調グレースケールテーマ（さらに W3C 標準 140 色を網羅する `CssColors` も利用可能）。

すべてのテーマが同一のトークン名を備えているため、`styles.py` を 1 箇所変更するだけで全ページの図表テーマを一括で切り替えられます。

---

## 5.2 セマンティックトークン体系と「`50%+` ニュートラル」原則

読みやすいアーキテクチャ図は、虹色の乱用を避けた明確な視覚階層から生まれます。各テーマは意味的ロールと直交サフィックスの組み合わせで構成されています。

| トークン種別・サフィックス | 代表トークン | 視覚効果とコントラスト規律 |
| :--- | :--- | :--- |
| **ニュートラル基盤** | `Neutral`, `PrimaryNeutral`, `SecondaryNeutral`, `White` | 落ち着いた淡色背景と控えめな枠線。**全ノード・カードの `50%` 以上をこの層で構成します。** `Styles.White` 上の文字には必ず `text_style=Styles.DarkBold` を指定します。 |
| **セマンティックロール** | `Primary`, `Secondary`, `Accent`, `Warning`, `Success`, `Danger`, `Muted` | 青（`Primary`）・紫／藍（`Secondary`）・橙（`Accent`）・緑（`Success`）・赤（`Danger`）・灰（`Muted`）に加え、淡色 `Primary1`〜濃色 `Primary6` の明度段階を提供します。 |
| **外枠線（`*Outline` / `*Solid`）** | `PrimaryOutline`, `SecondaryOutline`, `AccentOutline` | 塗りつぶしなしの透過内部＋色付き実線枠（線幅 `1.5`）。論理ゾーンや軽量バッジに最適です。 |
| **強調ベタ塗り（`*Flat`）** | `PrimaryFlat`, `AccentFlat`, `SuccessFlat`, `DangerFlat` | 枠線なしの高彩度ベタ塗り（`shape_line_width=0`）。**図内で 1〜2 個の主役要素に限定し、必ず `Styles.WhiteBold` の白太字と組み合わせます。** |
| **太さ・線種サフィックス** | `*Bold`, `*Thin`, `*Dashed`, `*Dotted` | 線幅とフォントウェイト（`Bold=2.5`・`Thin=0.75`、単体ロール `Styles.Light` もあり）や破線・点線（`MutedDashed`・`SecondaryDashedBold`・`PrimaryDotted`）を切り替えます。 |

---

## 5.3 イミュータブルな `.patch()`・`.patch_font()` と多言語フォント

すべての `Style` および `Color` インスタンスは**完全にイミュータブル（不変）**です。角丸・線幅・文字サイズ・揃え位置・不透明度を調整する際は、素の `Style(...)` をゼロから生成するのではなく、必ず既存の `Styles.*` トークンに対して `.patch(...)` を呼び出します。これにより、フォントファミリーやアイコンウェイト、テーマ切り替え時の互換性が安全に継承されます。

```python
from drawlib.canvas import save, setup
from drawlib.fonts import FontFile, FontJapanese, FontMonoSpace
from drawlib.preset_styles import GoogleStyles
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles

# ja/styles.py で用いられる言語別フォント一括差し替えパターン:
JaStyles = GoogleStyles().patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
    thin=FontJapanese.SANSSERIF_THIN,
)
# ローカルの .ttf / .otf ファイルも FontFile("_assets/brand.ttf") で読み込み可能
_ = FontFile

setup(width=120, height=36)

card_style = Styles.PrimaryNeutral.patch(
    shape_r=2.8,
    shape_line_width=2.0,
    alpha=0.95,
)
mono_label = Styles.DarkBold.patch(
    text_font=FontMonoSpace.ROBOTO_MONO_BOLD,
    text_size=11.0,
    halign="center",
    valign="center",
)
glass_tint = Colors.Primary.patch(alpha=0.15)
_ = (JaStyles, glass_tint)

rectangle((60, 18), width=56, height=18, style=card_style, text="api.internal:8443", text_style=mono_label)
save()
```

`drawlib.fonts` の内蔵フォント群は初回参照時に自動ダウンロード＆ローカルキャッシュされ、OS ごとのフォント差異による文字化け（豆腐化）を根絶します（オフライン環境では `uv run drawlib cache download --all` で事前取得可能）。

- **ユニバーサル・欧文フォント**: `Font`（欧文＋CJK を網羅する Noto Sans / Serif）、`FontSansSerif`（Lato・Montserrat・Poppins 等）、`FontSerif`（Merriweather・Playfair Display 等）、`FontRoboto`（Roboto・Condensed・Slab）。
- **等幅コード・数値フォント**: `FontMonoSpace`（`ROBOTO_MONO_REGULAR`・`SOURCECODEPRO_REGULAR`・日本語等幅 `SOURCEHANCODEJP_REGULAR`）および `FontSourceCode`。
- **CJK・地域言語・カスタムフォント**: `FontJapanese`・`FontChinese`（簡体字／繁体字／香港）・`FontKorean`・`FontArabic`・`FontThai`・`FontBrahmic`、および任意の `.ttf` / `.otf` を読み込む `FontFile("_assets/custom.ttf")`。

```drawlib align=center code=fold file=typography_and_patch_ja.png caption="図 5.2: .patch() による段階的スタイル派生と多言語フォント見本"
from drawlib.canvas import save, setup
from drawlib.fonts import FontJapanese, FontMonoSpace, FontRoboto, FontSerif
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=66)

sec_hdr = Styles.DarkBold.patch(text_size=10.8, halign="left")
xs = [26.0, 72.0, 118.0]

# 上段: .patch() による段階的スタイル変換
text((8.5, 59.5), "A. イミュータブルな Style.patch() 派生チェーン", style=sec_hdr)

rectangle(
    (xs[0], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.Neutral,
    text="Styles.Neutral\n(基本矩形カード)",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
line((44.5, 46.5), (53.5, 46.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (xs[1], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.PrimaryNeutral.patch(shape_r=3.0),
    text=".patch(shape_r=3.0)\n(角丸フィレット適用)",
    text_style=Styles.DarkBold.patch(text_size=10.2),
)
line((90.5, 46.5), (99.5, 46.5), arrow_head="->", style=Styles.DarkBold)

rectangle(
    (xs[2], 46.5),
    width=35.0,
    height=15.0,
    style=Styles.SecondaryNeutral.patch(
        shape_r=3.0,
        shape_line_style="dashed",
        shape_line_width=2.0,
    ),
    text='+ line_style="dashed"\n(破線ゾーン境界)',
    text_style=Styles.DarkBold.patch(text_size=10.2),
)

# 下段: 内蔵フォント見本
text((8.5, 29.0), "B. 自動キャッシュ対応の多言語フォント見本 (drawlib.fonts)", style=sec_hdr)

rectangle((xs[0], 15.5), width=35.0, height=16.0, style=Styles.White.patch(shape_r=2.2))
text((xs[0], 18.8), "FontSerif", style=Styles.DarkBold.patch(text_font=FontSerif.MERRIWEATHER_BOLD, text_size=11.0))
text((xs[0], 12.2), "Merriweather & Roboto", style=Styles.Dark.patch(text_font=FontRoboto.ROBOTO_REGULAR, text_size=10.0))

rectangle((xs[1], 15.5), width=35.0, height=16.0, style=Styles.Neutral.patch(shape_r=2.2))
text((xs[1], 18.8), "FontMonoSpace", style=Styles.DarkBold.patch(text_font=FontMonoSpace.ROBOTO_MONO_BOLD, text_size=10.8))
text((xs[1], 12.2), "10.0.4.12:8443", style=Styles.Dark.patch(text_font=FontMonoSpace.ROBOTO_MONO_REGULAR, text_size=10.0))

rectangle((xs[2], 15.5), width=35.0, height=16.0, style=Styles.PrimaryFlat.patch(shape_r=2.2))
text((xs[2], 18.8), "FontJapanese", style=Styles.WhiteBold.patch(text_font=FontJapanese.SANSSERIF_BOLD, text_size=11.0))
text((xs[2], 12.2), "日本語・CJK ゴシック", style=Styles.White.patch(text_font=FontJapanese.SANSSERIF_REGULAR, text_size=10.2))

save()
```
