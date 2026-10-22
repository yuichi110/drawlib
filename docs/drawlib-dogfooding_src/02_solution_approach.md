# 第2章: 解決アプローチ: Illustrated Documentation as Code

Drawlib は、ソフトウェアエンジニアと AI コーディングエージェントのための **"Illustrated Documentation as Code" (IDaC)** を実現する Python ライブラリです。従来の Documentation as Code（DaC）がテキスト中心であったのに対し、Drawlib は「図解・設計図がファーストクラスで統合された技術文書」をコードだけで構築します。

## 2.1 "Illustrated Documentation as Code" のコア思想

Drawlib のアプローチはシンプルです:
1. **宣言的 Python スクリプト**: 直感的な高レベル API でアーキテクチャ図・フロー図・チャート・構造化図解を定義します。
2. **Markdown への直接インライン埋め込み**: ドキュメントの中に ````drawlib```` コードブロックとして作図コードを直接記述します。
3. **完全なバージョン管理**: 図版の定義コードが Markdown テキストとして Git で管理され、プルリクエストでコード差分としてレビュー可能です。
4. **マルチフォーマット自動コンパイルと差分キャッシュ**: CLI ビルド（`drawlib build`）によって、マルチページ HTML サイト（`site`）、A4 ベクター PDF・単一 HTML レポート（`doc`）、16:9 ワイドスクリーンスライドデッキ（`slide`）、および GitHub 向け Markdown へと自動コンパイルされます。また、SQLite ベースの差分ビルドキャッシュ（`.drawlib/cache.db`）により、変更された図版のみを高速に再レンダリングします。

## 2.2 従来のアプローチとの比較

```drawlib align=center file=fig_solution_comparison.png caption="図 2.1: 従来の手動管理と Drawlib アプローチの比較"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=116, height=44)

# Left: Traditional Approach (Neutral card)
rectangle((28.0, 22.0), width=48, height=36, style=Styles.Neutral.patch(shape_r=2.0))
text((28.0, 35.0), text="従来の手動アプローチ", style=Styles.DarkBold.patch(text_size=11.5))
line((6.0, 30.0), (50.0, 30.0), style=Styles.Muted)
phosphor.file_x(xy=(11.5, 17.0), width=6.5, style=Styles.Secondary)
text((17.0, 17.0), text="・Figma / draw.io で手書き\n・バイナリ PNG を Git 管理\n・コード変更時に更新漏れ", style=Styles.Dark.patch(text_size=10.5, halign="left"))

# Right: Drawlib Approach (PrimaryNeutral card + PrimaryFlat header banner)
rectangle((88.0, 22.0), width=48, height=36, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((88.0, 35.0), width=48, height=10, style=Styles.PrimaryFlat.patch(shape_r=2.0))
text((88.0, 35.0), text="Illustrated Doc as Code", style=Styles.WhiteBold.patch(text_size=11.5))
phosphor.code(xy=(71.5, 17.0), width=6.5, style=Styles.Primary)
text((77.0, 17.0), text="・Python コードで図版定義\n・Markdown 内に直接埋め込み\n・差分レビュー・自動ビルド", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

line((53.5, 22.0), (62.5, 22.0), arrow_head="->", style=Styles.DarkBold)

save()
```

## 2.3 AI ペアプログラミングとの相乗効果

コードとして表現できることで、AI コーディングエージェント（Claude Code, Cursor, Gemini CLI, GitHub Copilot 等）との協調作業が飛躍的に容易になります:
- **AI が仕様から図を自動生成**: 新しい API エンドポイントやデータモデルを実装した際、AI に「アーキテクチャ図を更新して」と指示するだけで図版コードが生成されます。
- **マルチモーダル検証**: AI Agent は自身が生成した図版を座標グリッド付き画像（`drawlib show -g`）としてレンダリングし、配置やテキストの重なりを視覚的にセルフレビューして修正できます。
- **再現性（100% Deterministic）**: 同じコードからは常にピクセル単位で同一の図版が再現されます。
