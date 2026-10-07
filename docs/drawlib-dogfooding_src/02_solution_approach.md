# 第2章: 解決アプローチ: Illustrated Documentation as Code

Drawlib は、ソフトウェアエンジニアと AI コーディングエージェントのための **"Illustrated Documentation as Code" (IDaC)** を実現する Python ライブラリです。従来の Documentation as Code（DaC）がテキスト中心であったのに対し、Drawlib は「図解・設計図がファーストクラスで統合された技術文書」をコードだけで構築します。

## 2.1 "Illustrated Documentation as Code" のコア思想

Drawlib のアプローチはシンプルです:
1. **宣言的 Python スクリプト**: 直感的な高レベル API で図版を定義します。
2. **Markdown への直接インライン埋め込み**: ドキュメントの中に ````drawlib```` ブロックとして作図コードを直接記述します。
3. **完全なバージョン管理**: 図版の定義コードが Markdown テキストとして Git で管理され、プルリクエストでコード差分としてレビュー可能です。
4. **自動コンパイル**: CLI ビルド（`drawlib build`）によって、静的 HTML サイト、GitHub 向け Markdown、高品質な PDF レポートへと自動レンダリングされます。

## 2.2 従来のアプローチとの比較

```drawlib 640px center file:fig_solution_comparison.png caption:"図 2.1: 従来の手動管理と Drawlib アプローチの比較"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=110, height=45)

# Left: Traditional Approach
rectangle((28, 22.5), width=48, height=36, r=2, style=Styles.MutedDashed)
text((28, 36), text="従来の手動アプローチ", style=Styles.MutedBold.patch(text_size=11))
phosphor.file_x(xy=(16, 24), width=8, style=Styles.Muted)
text((33, 24), text="・Figma / draw.io で手書き\n・PNG 画像を Git で管理\n・コード変更時に更新漏れ・腐敗", style=Styles.Muted.patch(text_size=9))

# Right: Drawlib Approach
rectangle((82, 22.5), width=48, height=36, r=2, style=Styles.PrimaryOutline)
text((82, 36), text="Illustrated Doc as Code (Drawlib)", style=Styles.DarkBold.patch(text_size=10.5))
phosphor.code(xy=(70, 24), width=8, style=Styles.Primary)
text((87, 24), text="・Python コードで図版を定義\n・Markdown 内に直接埋め込み\n・Git で差分レビュー・CI 自動ビルド", style=Styles.Dark.patch(text_size=9))

line((53, 22.5), (57, 22.5), arrow_head="->", style=Styles.DarkBold)
```

## 2.3 AI ペアプログラミングとの相乗効果

コードとして表現できることで、AI Agent（Cursor, Claude, Gemini 等）との協調作業が飛躍的に容易になります:
- **AI が仕様から図を自動生成**: 新しい API エンドポイントやデータモデルを実装した際、AI に「アーキテクチャ図を更新して」と指示するだけで図版コードが生成されます。
- **マルチモーダル検証**: AI Agent は自身が生成した図版を画像としてレンダリングし、配置やテキストの重なりを視覚的にセルフレビューして修正できます。
- **再現性（100% Deterministic）**: 同じコードからは常にピクセル単位で同一の図版が再現されます。
