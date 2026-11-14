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
# 本プレゼンテーションの構成
:::

::: block xy=(80, 150) width=640 height=780
## 全6章のロードマップ

- **背景と課題 (第1章)**: 図解の形骸化を防ぐ Python × Git の統合アプローチ

- **描画エンジン (第2〜4章)**: 基本図形・34種アイコン群・SmartArts・Charts・構成図

- **多形式出力とAI連携 (第5〜6章)**: 5つのプロジェクト型・Office出力・AI自己検証ループ
:::

::: block xy=(760, 135) width=1080 height=820
```drawlib file=agenda_roadmap_ja.svg
from drawlib.canvas import clear, save, setup
import utils

clear()
setup(width=108, height=82)

utils.draw_curved_agenda(
    [
        ("1. なぜ Drawlib なのか？", "図解とドキュメントの形骸化・分断を解決"),
        ("2. 基本図形と34種のアイコン群", "キャンバス・43図形・スタイル・4,500+アイコン"),
        ("3. 18 SmartArts & 10 Charts", "インフォグラフィック・地図・純粋Pythonグラフ"),
        ("4. Diagrams・Graphs・Animation", "クラウド構成図・UML・自動レイアウト・APNG"),
        ("5. 5つのプロジェクト型と多形式出力", "site / catalog / doc / slide・PDF / Office"),
        ("6. AIネイティブな自律作図フロー", "rules CLI・-g グリッド検証・SQLiteキャッシュ"),
    ],
    width=108,
    height=82,
)
save()
```
:::

::: note
本プレゼンテーションは全6章で構成されています。
まず第1章では、従来のGUIツールやテキストDSLで技術図解が形骸化する原因を整理し、コードによる統合アプローチを解説します。
続く第2章から第4章では、基本図形と34種のアイコンスイート、18種のSmartArtsと10種のCharts、さらにクラウド構成図・UML・自動グラフレイアウト・APNGアニメーションまで、段階的に描画エンジンを見ていきます。
最後の第5章・第6章では、5つのプロジェクトアーキタイプからのWeb・PDF・Office一括出力と、AIコーディングエージェントが `-g` グリッド画像を用いて自律的にレイアウトを検証・修正するワークフローをご紹介します。
:::
