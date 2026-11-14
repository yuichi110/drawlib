::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch1_divider_ja.svg
import utils

utils.draw_chapter_divider(
    1,
    "なぜ Drawlib なのか？",
    subtitle="AI時代の技術図解・ドキュメント分断を解決する",
    topics=[
        "従来ツール（GUI・DSL）の限界",
        "コードによる図解と文書の統合",
        "既存ツールとの機能比較マトリクス",
        "単一リポジトリからの多形式一括出力",
    ],
    total_chapters=6,
    section_label="CHAPTER",
    badge_text="Chapter 1 / 6",
)
```
:::

::: note
第1章「なぜ Drawlib なのか？」に入ります。
AIコーディングエージェントの普及によってソフトウェアの変更速度が飛躍的に高まる中、なぜ従来の図解や設計書だけがすぐ古くなってしまうのかを紐解き、図解とドキュメントを純粋なPythonコードとしてGitで一元管理する意義を解説します。
:::
