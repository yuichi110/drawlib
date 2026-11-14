::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch3_divider_ja.svg
import utils

utils.draw_chapter_divider(
    3,
    "SmartArts と標準チャート",
    subtitle="18種の構造化インフォグラフィックと10種の純Pythonチャート",
    topics=[
        "プロセス・サイクル・ロードマップ",
        "KPI・カードリスト・階層・マインドマップ",
        "テーブル・コード・カレンダー・世界地図",
        "10種の宣言的チャートとガント工程表",
    ],
    total_chapters=6,
    badge_text="Chapter 3 / 6",
)
```
:::

::: note
第3章では、Drawlib の高水準コンポーネント群である `drawlib.smartarts` と `drawlib.charts` を紹介します。
矩形や直線の座標を手作業で並べる代わりに、SmartArts が提供する18種類の構造化インフォグラフィックを使うことで、プロセスフロー、フィードバックサイクル、ロードマップ、KPIカード、機能リスト、階層ピラミッド、マインドマップ、テーブル、コードハイライト、カレンダー、世界地図を数行の Python コードで構築できます。後半では、外部グラフ描画ライブラリに一切依存せずキャンバスへ直接ベクター出力できる10種類の純Pythonチャートとガント工程表を解説します。
:::
