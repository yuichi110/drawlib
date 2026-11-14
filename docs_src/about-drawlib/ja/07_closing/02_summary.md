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
# まとめとクイックスタート
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=summary_takeaways_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.smartarts import CardList
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=81)

# Top 2x2 Grid of Takeaway Cards using two side-by-side CardList instances
left_cards = CardList(
    style=Styles.White.patch(shape_r=2.2),
    text_style=Styles.DarkBold.patch(text_size=14.4),
    description_style=Styles.Dark.patch(text_size=11.5),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=3.5,
)
left_cards.add(
    "1. Pure Python ＆ Git ネイティブ",
    "型安全なPython API・styles.py 共通設定と\nGit差分管理でGUIロックインを解消。",
    badge_text="01",
    icon=phosphor.git_branch,
)
left_cards.add(
    "3. 5つのプロジェクト種別とOffice出力",
    "Site・Catalog・Doc・Slide・Images から\nHTML・PDF・Word・PPTXを一括生成。",
    badge_text="03",
    icon=phosphor.browsers,
)
left_cards.draw(xy=(2.0, 26.5), width=84.5, height=52.0)

right_cards = CardList(
    style=Styles.White.patch(shape_r=2.2),
    text_style=Styles.DarkBold.patch(text_size=14.4),
    description_style=Styles.Dark.patch(text_size=11.5),
    badge_shape="rounded_rect",
    badge_style=Styles.PrimaryNeutral,
    badge_text_style=Styles.PrimaryBold.patch(text_size=11.5),
    icon_style=Styles.PrimaryBold,
    direction="vertical",
    spacing=3.5,
)
right_cards.add(
    "2. 豊富な高水準コンポーネント群",
    "18種SmartArts・10種Charts・6種Diagrams・\n5種Graph・34種アイコンを標準内蔵。",
    badge_text="02",
    icon=phosphor.cube,
)
right_cards.add(
    "4. 自律型AIエージェントに最適化",
    "50超の drawlib rules・show -g 視覚検品・\n1秒未満の .drawlib/cache.db 差分ビルド。",
    badge_text="04",
    icon=phosphor.robot,
    style=Styles.PrimaryNeutral.patch(shape_r=2.2),
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11.5),
    icon_style=Styles.WhiteBold,
)
right_cards.draw(xy=(89.5, 26.5), width=84.5, height=52.0)

# Bottom Dark/Primary Quickstart Banner (height ~22)
rectangle((88.0, 12.8), width=172.0, height=21.0, style=Styles.DarkFlat.patch(shape_r=2.5))
phosphor.terminal_window((9.5, 19.2), width=4.2, style=Styles.WhiteBold)
text(
    (14.5, 19.2),
    "30秒で始めるクイックスタート",
    style=Styles.WhiteBold.patch(text_size=12.2, halign="left"),
)
text(
    (170.0, 19.2),
    "Python 3.11+ / uv 環境に対応",
    style=Styles.White.patch(text_size=11.2, halign="right"),
)

# 3 Command Pills inside Quickstart Banner
rectangle((26.5, 9.2), width=40.0, height=9.2, style=Styles.WhiteFlat.patch(shape_r=1.6))
text((26.5, 9.2), "uv add drawlib", style=Styles.DarkBold.patch(text_size=13.0))

line((47.5, 9.2), (53.5, 9.2), arrow_head="->", style=Styles.WhiteBold)

rectangle((88.0, 9.2), width=66.0, height=9.2, style=Styles.WhiteFlat.patch(shape_r=1.6))
text(
    (88.0, 9.2),
    "uv run drawlib init project slide my-deck",
    style=Styles.DarkBold.patch(text_size=12.6),
)

line((122.0, 9.2), (128.0, 9.2), arrow_head="->", style=Styles.WhiteBold)

rectangle((149.5, 9.2), width=41.0, height=9.2, style=Styles.PrimaryFlat.patch(shape_r=1.6))
text((149.5, 9.2), "uv run drawlib serve", style=Styles.WhiteBold.patch(text_size=13.0))

save()
```
:::

::: note
Drawlibの4つのコアバリューを振り返ります。
1. **Pure Python ＆ Git ネイティブ**：すべての図解と原稿を型安全なPythonとMarkdownで記述し、`styles.py` のデザイントークンとGitのPull Requestで保守できます。
2. **豊富な高水準コンポーネント群**：18種のSmartArts、10種のCharts、6種のDiagrams、5種のグラフレイアウトソルバー、34種のアイコンパックにより、複雑な構成図も最小限のコードで美しく描画できます。
3. **5つのプロジェクト種別とOffice出力**：`site`・`catalog`・`doc`・`slide`・`images` を単一コンパイラでビルドし、HTML・ベクターPDF・Word（`.docx`）・PowerPoint（`.pptx`）へ出力できます。
4. **自律型AIエージェントに最適化**：50以上の `drawlib rules` トピック、`show -g` グリッド検品、`.drawlib/cache.db` SQLiteキャッシュにより、AIエージェントが自律的に高品質な図版を生成できます。
導入は `uv add drawlib`、`uv run drawlib init project slide my-deck`、`uv run drawlib serve` の3コマンドだけで完了します。
:::
