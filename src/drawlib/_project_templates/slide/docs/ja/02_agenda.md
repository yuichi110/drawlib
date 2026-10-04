---
header: "Agenda"
layout: default
---

::: block (80, 140) (700, 840)
# アジェンダ

- **アーキテクチャ概要**: 宣言的描画エンジンの構造
- **ネイティブSVG出力**: 高解像度ベクターと文字検索
- **モジュール化描画**: 再利用可能なユーティリティ
- **動的アニメーション**: WebPキーフレーム生成
- **今後の展望**: 拡張性の高い設計ワークフロー
:::

::: block (820, 140) (1020, 840)
```drawlib file:agenda.svg
from drawlib.canvas import clear, setup
from utils import draw_curved_agenda

clear()
setup(width=102, height=84)
draw_curved_agenda(
    [
        ("Architecture Overview", "設計概要"),
        ("Native SVG Output", "検索可能テキスト"),
        ("Modular Drawing", "再利用可能関数"),
        ("Dynamic Animations", "WebPアニメーション"),
        ("Next Steps", "ロードマップ"),
    ],
    width=102,
    height=84,
)
```
:::
