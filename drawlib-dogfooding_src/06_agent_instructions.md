# 第6章: AI エージェントとの連携・インストラクション

Drawlib は、AI コーディングアシスタント（Claude, Cursor, Gemini, Copilot）が自律的かつ正確に作図を行えるよう「Agent-First」で設計されています。エージェントに基本 instruction を登録した後は、AI が Drawlib CLI と自律的に対話して必要な機能を調査し、検証済みの図解ドキュメントを出力します。

```drawlib 640px center file:fig_agent_interaction.png caption:"図 6.1: Drawlib と AI Agent の自律対話・ドキュメント出力モデル"
from drawlib.canvas import setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=142, height=54)

header_ts = Styles.white_bold.patch(text_size=10.0)
ts_pri_body = Styles.primary.patch(text_size=7.8, text_halign="left")
ts_acc_body = Styles.accent.patch(text_size=7.8, text_halign="left")
ts_suc_body = Styles.success.patch(text_size=7.8, text_halign="left")

# 1. Drawlib (CLI & Knowledge Base)
rectangle((22.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.primary_outline)
rectangle((22.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.primary_flat, text="Drawlib (CLI & ナレッジ)", textstyle=header_ts)

phosphor.book_bookmark(xy=(9.5, 31.0), width=4.5, style=Styles.primary)
text((13.5, 31.0), text="drawlib rules show\nAPI仕様・作図ルールを提供", style=ts_pri_body)

phosphor.terminal_window(xy=(9.5, 21.5), width=4.5, style=Styles.primary)
text((13.5, 21.5), text="drawlib show -g\nミリ単位の座標グリッド出力", style=ts_pri_body)

phosphor.gear(xy=(9.5, 12.0), width=4.5, style=Styles.primary)
text((13.5, 12.0), text="drawlib build\nPDF / HTML の自動コンパイル", style=ts_pri_body)

# 2. AI Agent (Cursor / Claude / Gemini)
rectangle((71.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.accent_outline)
rectangle((71.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.accent_flat, text="AI Agent (自律パートナー)", textstyle=header_ts)

phosphor.chats(xy=(58.5, 31.0), width=4.5, style=Styles.accent)
text((62.5, 31.0), text="1. 知識のオンデマンド対話\nDrawlib から必要な構文を調査", style=ts_acc_body)

phosphor.code(xy=(58.5, 21.5), width=4.5, style=Styles.accent)
text((62.5, 21.5), text="2. スクラッチで安全に試作\n.drawlib/scratch/ で描画テスト", style=ts_acc_body)

phosphor.eye(xy=(58.5, 12.0), width=4.5, style=Styles.accent)
text((62.5, 12.0), text="3. 視覚的セルフレビュー\n重なり・文字溢れを自動検知修正", style=ts_acc_body)

# 3. Docs / Illustration (最終成果物)
rectangle((120.0, 24.0), width=32.0, height=38.0, r=2.0, style=Styles.success_outline)
rectangle((120.0, 40.0), width=30.0, height=5.5, r=1.5, style=Styles.success_flat, text="Docs / Illustration", textstyle=header_ts)

phosphor.file_text(xy=(107.5, 31.0), width=4.5, style=Styles.success)
text((111.5, 31.0), text="*.md 技術仕様書\nインライン ```drawlib``` 統合", style=ts_suc_body)

phosphor.file_pdf(xy=(107.5, 21.5), width=4.5, style=Styles.success)
text((111.5, 21.5), text="*.pdf / Web サイト\n美しい図解入りの配布成果物", style=ts_suc_body)

phosphor.git_branch(xy=(107.5, 12.0), width=4.5, style=Styles.success)
text((111.5, 12.0), text="Git バージョン管理\nPR で図版のコード差分レビュー", style=ts_suc_body)

# 接続線 (Drawlib <-> AI -> Docs)
line((39.5, 24.0), (53.5, 24.0), arrowhead="<->", style=Styles.bold)
text((46.5, 28.5), text="Rules 検索 & 対話", style=Styles.primary_bold, size=8.0)
text((46.5, 19.5), text="仕様 / 座標グリッド", style=Styles.accent_bold, size=7.5)

line((88.5, 24.0), (102.5, 24.0), arrowhead="->", style=Styles.bold)
text((95.5, 28.5), text="確定コード出力", style=Styles.success_bold, size=8.0)
text((95.5, 19.5), text="ドキュメント自動同期", style=Styles.muted_bold, size=7.5)
```

## 6.1 組み込みルールシステムの活用 (`drawlib rules`)

Drawlib には、ライブラリ仕様や作図ベストプラクティスが最初からルールとして組み込まれています。ターミナルからオンデマンドでエージェントに知識を提供できます:

```bash
# 利用可能なルール一覧
uv run drawlib rules list

# エージェント用指示マニュアル
uv run drawlib rules show agent-instruction

# キャンバス座標系と描画ライフサイクル
uv run drawlib rules show overview

# 各モジュールの詳細仕様
uv run drawlib rules show lib-smartarts
uv run drawlib rules show lib-diagrams
uv run drawlib rules show lib-charts
```

## 6.2 プロジェクトルールファイルへの設定

Cursor（`.cursorrules`）や Claude Code / Gemini（`.agents/rules/`）に以下の基本ルールを登録しておくと、AI が自動的に Drawlib の作図原則に従うようになります:

```markdown
# Drawlib 作図ルール
- 原則として生 SVG や低レベル matplotlib は書かず、drawlib の高レベルモジュール（smartarts, diagrams, charts）を使用すること。
- キャンバスの原点 (0, 0) は「左下」である。
- スタイルとカラーは常に PascalCase（Styles, Colors）でインポート・参照すること。
- Markdown 内のコードブロックには必ず `file:<名前>.png` と `caption:"..."` を指定すること。
```

## 6.3 エージェントの自律フィードバックループ

AI エージェントが図版を作成する際は、以下のセルフレビュー手順を踏ませることで、位置ズレや重なりのない完璧な図版が得られます:

1. **コードの記述**: Markdown 内に ````drawlib```` ブロックを記述。
2. **グリッド付きプレビュー出力**:
   ```bash
   uv run drawlib show doc.md arch.png -g -o .drawlib/scratch/arch.png
   ```
3. **画像ツールの確認**: エージェントが画像ファイルを視覚的に確認し、テキストのはみ出しや余白の不均等さを検査。
4. **座標の微調整**: 必要に応じて座標を修正し、再確認。
