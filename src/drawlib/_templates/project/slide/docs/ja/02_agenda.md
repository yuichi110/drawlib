::: block xy=(80, 40) width=1760 height=60
# アジェンダ
:::

::: block xy=(80, 140) width=700 height=840
- **アーキテクチャ概要**: 宣言的描画エンジンの構造
- **ネイティブSVG出力**: 高解像度ベクターと文字検索
- **モジュール化描画**: 再利用可能なユーティリティ
- **動的アニメーション**: WebPキーフレーム生成
- **今後の展望**: 拡張性の高い設計ワークフロー
:::

::: block xy=(820, 140) width=1020 height=840
```drawlib file=agenda.svg
from drawlib.canvas import clear, save, setup
from drawlib.smartarts import Roadmap
from drawlib.styles import Styles

clear()
setup(width=102, height=84)
rm = Roadmap(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=12),
    description_style=Styles.Muted.patch(text_size=10),
    spine_style=Styles.PrimaryBold,
    badge_style=Styles.PrimaryFlat,
    badge_text_style=Styles.WhiteBold.patch(text_size=11),
    curve_bend=-0.18,
    card_shape="pill",
)
for title, sub in [
    ("Architecture Overview", "設計概要"),
    ("Native SVG Output", "検索可能テキスト"),
    ("Modular Drawing", "再利用可能関数"),
    ("Dynamic Animations", "WebPアニメーション"),
    ("Next Steps", "ロードマップ"),
]:
    rm.add(title, sub)
rm.draw(xy=(4, 4), width=94, height=76)
save()
```
:::

::: block xy=(80, 1010) width=1580 height=30 font_size=14px
*Drawlib プレゼンテーション*
:::

::: block xy=(1700, 1010) width=140 height=30
```drawlib file=page.svg
from drawlib.slide import draw_page_number

draw_page_number()
```
:::
