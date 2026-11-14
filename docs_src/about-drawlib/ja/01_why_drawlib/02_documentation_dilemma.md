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
# 従来の作図・ドキュメントツールの限界
:::

::: block xy=(80, 130) width=1760 height=115
開発現場は **差分管理できないGUIツール**、**表現力が限定されたテキストDSL**、**文書と分断された描画ライブラリ** の三択を強いられ、リリースのたびに設計図が実装から乖離します。
:::

::: block xy=(80, 260) width=1760 height=685
```drawlib file=dilemma_three_traps_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import CardList, Panel
from drawlib.styles import Styles
from drawlib.text import text

clear()
setup(width=176, height=69)

traps = [
    (
        2.0,
        "GUI ツール (Figma / Draw.io)",
        phosphor.cursor_click,
        [
            ("不透明なバイナリ形式", "Git PR 上で差分比較が不可能"),
            ("手動の PNG 書き出し", "仕様変更ですぐ陳腐化する"),
            ("GUI 操作への依存", "AI エージェントが編集不可"),
        ],
    ),
    (
        60.5,
        "テキスト DSL (Mermaid 等)",
        phosphor.brackets_curly,
        [
            ("硬直的な自動配置", "(x, y) 座標の微調整が不可"),
            ("狭い図解ボキャブラリ", "KPI・表・地図表現に不向き"),
            ("図単体のスニペット", "PDF / PPTX 統合出力がない"),
        ],
    ),
    (
        119.0,
        "描画ライブラリ (Matplotlib)",
        phosphor.chart_bar,
        [
            ("数値プロット専用", "クラウド構成図や UML 非対応"),
            ("煩雑なスタイル記述", "書体や配色の統一が困難"),
            ("ドキュメントとの分断", "資料へ手作業で画像を転記"),
        ],
    ),
]

for px, title, hdr_icon, items in traps:
    p = Panel(
        title,
        style=Styles.Neutral.patch(shape_r=2.2),
        header_style=Styles.SecondaryNeutral.patch(shape_line_width=1.0),
        text_style=Styles.DarkBold.patch(text_size=12.4),
        icon=hdr_icon,
        icon_style=Styles.PrimaryBold,
        header_variant="filled",
        header_height=9.5,
    )
    p.draw((px, 16.5), width=55.0, height=50.0)
    c_xy, c_w, c_h = p.get_content_box(
        (px, 16.5),
        width=55.0,
        height=50.0,
        padding=(2.0, 2.2),
    )

    cl = CardList(
        style=Styles.White.patch(shape_r=1.8),
        text_style=Styles.DarkBold.patch(text_size=12.6),
        description_style=Styles.Muted.patch(text_size=11.5),
        badge_shape="circle",
        badge_style=Styles.DangerNeutral,
        icon_style=Styles.DangerBold,
        direction="vertical",
        spacing=2.0,
    )
    for item_title, item_desc in items:
        cl.add(item_title, item_desc, icon=phosphor.x_circle)
    cl.draw(c_xy, width=c_w, height=c_h)

rectangle(
    (88.0, 7.5),
    width=172.0,
    height=11.5,
    style=Styles.PrimaryFlat.patch(shape_r=2.2),
)
phosphor.sparkle((10.5, 7.5), width=5.4, style=Styles.WhiteBold)
text(
    (91.5, 7.5),
    "求められていた統合基盤：精密な空間制御 × Git差分レビュー × 文書・図表統合 × AI視覚検証ループ",
    style=Styles.WhiteBold.patch(text_size=12.8),
)
save()
```
:::

::: note
なぜ技術ドキュメントやアーキテクチャ図は、リリースを重ねるたびに実装から乖離してしまうのでしょうか。
理由は、既存のツールが3つのジレンマを抱えているためです。
第一に、Figma や Draw.io などのGUIホワイトボードは自由な配置ができる反面、Gitのプルリクエストで論理的な差分レビューができず、AIエージェントによる自律的な保守も困難です。
第二に、Mermaid や PlantUML などのテキストDSLはGit管理できるものの、自動レイアウトに縛られてミリ単位の座標制御ができず、インフォグラフィックやスライド・Office出力には対応できません。
第三に、Matplotlib などのプロットライブラリは統計グラフ専用であり、構成図やドキュメント全体のビルドとは分断されています。
Drawlib は、この空白地帯を一挙に埋めるために設計されました。
:::
