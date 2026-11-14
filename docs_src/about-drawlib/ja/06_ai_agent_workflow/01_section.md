::: block xy=(0, 0) width=1920 height=1080
```drawlib file=ch06_section_ja.svg
import utils

utils.draw_chapter_divider(
    6,
    "AIエージェント自律ワークフロー",
    subtitle="Rules CLI・視覚的自己修正ループ・SQLiteキャッシュ",
    topics=[
        "Rules CLIによるオンデマンド参照",
        "-g グリッドによる自律視覚検証ループ",
        "2層アセット＆SQLiteビルドキャッシュ",
    ],
    total_chapters=6,
    badge_text="Chapter 6 / 6",
)
```
:::

::: note
第6章「AIエージェント自律ワークフロー」に入ります。
Drawlibは人間のエンジニアにとって書きやすいだけでなく、Gemini・Claude Code・CursorといったマルチモーダルAIコーディングエージェントが自律的に美しい図解とドキュメントを生成できるよう設計されています。
本章では、プロンプト肥大化を防ぐ `drawlib rules` のオンデマンド知識参照、`drawlib show -g` 座標グリッドを用いた視覚的自己修正ループ、そして1秒未満の差分ビルドを実現する2層キャッシュ機構と統合CLIを解説します。
:::
