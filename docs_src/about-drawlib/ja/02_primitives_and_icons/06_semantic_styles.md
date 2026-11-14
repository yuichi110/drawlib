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
# 8色セマンティックスタイルとプリセットテーマ
:::

::: block xy=(80, 130) width=1760 height=115
- **8色ロール体系**: `Styles.<Color><Variant>` が `Primary`〜`Dark` の8色と `Flat`・`Bold`・`Dashed`・`Neutral` を統合。
- **不変 `.patch()` とテーマ**: `style.patch(...)` で安全に派生作成し、`drawlib.toml` で全体の配色テーマを一括切替。
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=semantic_styles_matrix_ja.svg
from drawlib.canvas import clear, setup
from drawlib.preset_styles import DefaultStyles, GoogleStyles, MonochromeStyles
from drawlib.shapes import rectangle
from drawlib.smartarts import Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=69)

# Left Panel: 8x3 Semantic Swatch Matrix (width=108)
Panel(
    "8色ロール × バリアント行列 (Styles.<Color><Variant>)",
    style=Styles.Neutral.patch(shape_r=1.8),
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.5),
    header_height=7.0,
).draw(xy=(1.5, 1.5), width=108.0, height=66.0)

col_x = [34.5, 61.5, 91.5]
text((5.5, 56.8), "ロール", style=Styles.MutedBold.patch(text_size=12.0, halign="left"))
text((col_x[0], 56.8), "Default", style=Styles.MutedBold.patch(text_size=12.0))
text((col_x[1], 56.8), "Flat", style=Styles.MutedBold.patch(text_size=12.0))
text((col_x[2], 56.8), "Neutral / Dashed", style=Styles.MutedBold.patch(text_size=12.0))

roles = ["Primary", "Secondary", "Accent", "Success", "Warning", "Danger", "Neutral", "Dark"]
for idx, role in enumerate(roles):
    ry = 50.6 - idx * 6.4
    text((5.5, ry), role, style=Styles.DarkBold.patch(text_size=12.2, halign="left"))

    is_light_role = role == "Neutral"
    fg_solid = Styles.DarkBold if is_light_role else Styles.WhiteBold

    # Column 1: Default (Bordered)
    st_def = getattr(Styles, role).patch(shape_r=1.1)
    rectangle((col_x[0], ry), width=23.5, height=4.8, style=st_def)
    text((col_x[0], ry), f".{role}", style=fg_solid.patch(text_size=11.5))

    # Column 2: Flat
    st_flat = getattr(Styles, f"{role}Flat").patch(shape_r=1.1)
    rectangle((col_x[1], ry), width=23.5, height=4.8, style=st_flat)
    text((col_x[1], ry), f".{role}Flat", style=fg_solid.patch(text_size=11.5))

    # Column 3: Neutral (for 6 hues) or Dashed (for Neutral & Dark)
    v3_suffix = "Neutral" if role not in ("Neutral", "Dark") else "Dashed"
    st_v3 = getattr(Styles, f"{role}{v3_suffix}").patch(shape_r=1.1)
    rectangle((col_x[2], ry), width=29.0, height=4.8, style=st_v3)
    text((col_x[2], ry), f".{role}{v3_suffix}", style=Styles.DarkBold.patch(text_size=11.5))

# Right Panel: 3 Preset Theme Cards (width=62)
Panel(
    "プリセットテーマ (drawlib.toml)",
    style=Styles.Neutral.patch(shape_r=1.8),
    header_style=Styles.SecondaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.5),
    header_height=7.0,
).draw(xy=(112.5, 1.5), width=62.0, height=66.0)

themes = [
    (49.8, 'style = "default"', "標準インディゴ配色", DefaultStyles(), ["PrimaryFlat", "SecondaryFlat", "AccentFlat", "SuccessFlat"]),
    (30.8, 'style = "google"', "Google ブルー配色", GoogleStyles(), ["PrimaryFlat", "SecondaryFlat", "AccentFlat", "SuccessFlat"]),
    (11.8, 'style = "monochrome"', "印刷向けグレースケール", MonochromeStyles(), ["DarkFlat", "Primary", "Secondary", "Neutral"]),
]
for cy, toml_key, subtitle, theme_obj, chip_names in themes:
    rectangle((143.5, cy), width=56.4, height=16.4, style=Styles.White.patch(shape_r=1.6))
    text((118.5, cy + 4.8), toml_key, style=Styles.DarkBold.patch(text_size=12.8, halign="left"))
    text((118.5, cy + 1.0), subtitle, style=Styles.Muted.patch(text_size=11.5, halign="left"))
    for c_i, c_name in enumerate(chip_names):
        cx = 124.2 + c_i * 12.8
        chip_st = getattr(theme_obj, c_name).patch(shape_r=0.9)
        rectangle((cx, cy - 4.4), width=10.8, height=4.2, style=chip_st)
```
:::

::: note
図解スクリプトごとにカラーコードを直接書き込むのではなく、Drawlib では `Styles.<Color><Variant>` によるセマンティックなデザイントークンを採用しています。`Primary`・`Secondary`・`Accent`・`Success`・`Warning`・`Danger`・`Neutral`・`Dark` の8色ロールに、`Flat`・`Bold`・`Dashed`・`Neutral` などの派生バリアントが直交して組み合わさります。`Style` オブジェクトはイミュータブル設計のため、`.patch()` で元の定義を壊さずに角丸や文字サイズを上書きでき、`drawlib.toml` の `style` を `"default"`・`"google"`・`"monochrome"` に変えるだけでデッキ全体のテーマを一括変更できます。
:::
