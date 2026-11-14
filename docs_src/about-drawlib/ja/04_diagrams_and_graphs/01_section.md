::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch4_divider_ja.svg
import utils

utils.draw_chapter_divider(
    4,
    "技術ダイアグラム・自動配置・アニメ",
    subtitle="6種の設計図エンジン・5種のグラフソルバー・APNG",
    topics=[
        "クラウド構成・ネットワーク図",
        "業務フロー図と通信シーケンス図",
        "UMLクラス図・ER図・状態遷移図",
        "自動グラフレイアウトとアニメーション",
    ],
    total_chapters=6,
    badge_text="Chapter 4 / 6",
)
```
:::

::: note
**第4章の概要 — 技術ダイアグラム・自動配置ソルバー・アニメーション**:
- 第3章では SmartArt と統計チャートを扱いましたが、第4章ではソフトウェア設計やインフラ構成を記述する**本格的なエンジニアリング作図機能**に入ります。
- 前半では **`drawlib.diagrams` の6種の専用設計図エンジン**を紹介します。クラウド構成を描く `ArchitectureDiagram`、業務フローとAPI通信プロトコルを表す `FlowDiagram`・`SequenceDiagram`、そしてドメイン設計に不可欠な `ClassDiagram`・`ERDiagram`・`StateDiagram` です。
- 後半では、煩雑な座標計算を自動化する **`drawlib.graph` の5種類のグラフレイアウトソルバー**と、`offset()` による手動微調整のハイブリッド設計を解説します。
- 最後に **`drawlib.anim`** を用いて、すべてのモジュールを APNG / Animated WebP の宣言的アニメーションとして動かし、HTMLスライドでの対話再生と PDF / PPTX への静的フレーム自動抽出を両立する仕組みを紹介します。
:::
