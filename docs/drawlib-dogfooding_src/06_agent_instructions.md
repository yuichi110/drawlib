# 第6章: AI エージェントとの連携・インストラクション

Drawlib は、AI コーディングアシスタント（Claude, Cursor, Gemini, Copilot）が自律的かつ正確に作図を行えるよう「Agent-First」で設計されています。エージェントに基本 instruction を登録した後は、AI が Drawlib CLI と自律的に対話して必要な機能を調査し、検証済みの図解ドキュメントを出力します。

```drawlib align=center file=fig_agent_interaction.png caption="図 6.1: Drawlib と AI Agent の自律対話・ドキュメント出力モデル"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=136, height=54)

header_ts = Styles.WhiteBold.patch(text_size=10.5)
ts_body = Styles.Dark.patch(text_size=10.0, halign="left")
ts_arrow_top = Styles.DarkBold.patch(text_size=10.0)
ts_arrow_sub = Styles.Dark.patch(text_size=9.5)

# 1. Drawlib (CLI & Knowledge Base)
rectangle((21.5, 27.0), width=35.0, height=44.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((21.5, 45.0), width=33.0, height=6.0, style=Styles.PrimaryFlat.patch(shape_r=1.5), text="1. Drawlib CLI", text_style=header_ts)

phosphor.book_bookmark(xy=(7.8, 35.0), width=4.4, style=Styles.Primary)
text((10.8, 35.0), text="drawlib rules\n仕様・作図ルール", style=ts_body)

phosphor.terminal_window(xy=(7.8, 23.5), width=4.4, style=Styles.Primary)
text((10.8, 23.5), text="drawlib show -g\nグリッド検証出力", style=ts_body)

phosphor.gear(xy=(7.8, 12.0), width=4.4, style=Styles.Primary)
text((10.8, 12.0), text="drawlib build\nPDF / HTML 変換", style=ts_body)

# 2. AI Agent (Cursor / Claude / Gemini)
rectangle((68.0, 27.0), width=35.0, height=44.0, style=Styles.Neutral.patch(shape_r=2.0))
rectangle((68.0, 45.0), width=33.0, height=6.0, style=Styles.AccentFlat.patch(shape_r=1.5), text="2. AI Agent", text_style=header_ts)

phosphor.chats(xy=(54.3, 35.0), width=4.4, style=Styles.Accent)
text((57.3, 35.0), text="1. 静的・座標確認\nアンカー・文字寸法", style=ts_body)

phosphor.code(xy=(54.3, 23.5), width=4.4, style=Styles.Accent)
text((57.3, 23.5), text="2. グリッド試作\nscratch で描画検証", style=ts_body)

phosphor.eye(xy=(54.3, 12.0), width=4.4, style=Styles.Accent)
text((57.3, 12.0), text="3. 視覚レビュー\n重なり・余白を修正", style=ts_body)

# 3. Docs / Illustration (最終成果物)
rectangle((114.5, 27.0), width=35.0, height=44.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
rectangle((114.5, 45.0), width=33.0, height=6.0, style=Styles.DarkFlat.patch(shape_r=1.5), text="3. 検証済ドキュメント", text_style=header_ts)

phosphor.file_text(xy=(100.8, 35.0), width=4.4, style=Styles.Dark)
text((103.8, 35.0), text="*.md 技術仕様書\nコード・図版を統合", style=ts_body)

phosphor.file_pdf(xy=(100.8, 23.5), width=4.4, style=Styles.Dark)
text((103.8, 23.5), text="PDF / Web / Slide\n高品質な配布成果物", style=ts_body)

phosphor.git_branch(xy=(100.8, 12.0), width=4.4, style=Styles.Dark)
text((103.8, 12.0), text="Git 差分管理\nPR でコードレビュー", style=ts_body)

# 接続線 (Drawlib <-> AI -> Docs)
line((39.5, 27.0), (50.0, 27.0), arrow_head="<->", style=Styles.DarkBold)
text((44.75, 31.5), text="対話", style=ts_arrow_top)
text((44.75, 22.0), text="グリッド", style=ts_arrow_sub)

line((86.0, 27.0), (96.5, 27.0), arrow_head="->", style=Styles.DarkBold)
text((91.25, 31.5), text="出力", style=ts_arrow_top)
text((91.25, 22.0), text="自動同期", style=ts_arrow_sub)

save()
```

## 6.1 組み込みルールシステムの活用 (`drawlib rules`)

Drawlib には、ライブラリ仕様や作図ベストプラクティスが最初からルールとして組み込まれています。ターミナルからオンデマンドでエージェントに知識を提供できます:

```bash
# 利用可能なルール一覧
uv run drawlib rules list

# エージェント用指示マニュアル・基本原則
uv run drawlib rules show agent-instruction

# キャンバス座標系 (原点左下) と描画ライフサイクル
uv run drawlib rules show overview

# 配色・タイポグラフィ・50%+ ニュートラルルール
uv run drawlib rules show style-guide

# 自律 3 ステージ検証ループと 720pt フォントサイズ計算
uv run drawlib rules show review-guide

# プロジェクト構成ガイド (doc / site / slide / images)
uv run drawlib rules show project-overview
uv run drawlib rules show project-doc
uv run drawlib rules show project-site
uv run drawlib rules show project-slide
uv run drawlib rules show project-images

# 全 API シンボル一覧と各モジュールの詳細仕様
uv run drawlib rules show api
uv run drawlib rules show lib-smartarts-overview
uv run drawlib rules show lib-diagrams-overview
uv run drawlib rules show lib-graph-overview
uv run drawlib rules show lib-charts-overview
```

## 6.2 プロジェクトルールファイルへの設定

Cursor（`.cursorrules`）や Claude Code / Gemini（`.agents/rules/`）に以下の基本ルールを登録しておくと、AI が自動的に Drawlib `v0.3.0` の作図原則に従うようになります:

```markdown
# Drawlib 作図ルール
- Project-First Rule: 裸の `.py` ファイルを直接作らず、必ず `uv run drawlib init <doc|site|slide|images>` でプロジェクトを初期化すること。
- 生 SVG や低レベル matplotlib は書かず、drawlib の高レベルモジュール（smartarts, diagrams, graph, charts）を使用すること。
- キャンバスの原点 (0, 0) は「左下」である。
- スタイルとカラーは常に PascalCase（`Styles`, `Colors`）でインポート・参照すること。
- 50%+ Neutral Baseline: 図形要素の 50% 以上に落ち着いたニュートラルカード（`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`）を使用し、濃い塗り（`Styles.PrimaryFlat`, `Styles.AccentFlat`）は 1〜2 個の主役要素やヘッダーに限定すること。
- フォントサイズは `text_size >= 10.0`（標準 10.0〜11.5、見出し 11.5〜12.5）を維持すること。
- Markdown 内のコードブロックには `file=<名前>.png` と `caption="..."`（および必要に応じて `code=fold` / `code=show`）を `=` 構文で指定し、狭いピクセル幅指定（`width=600px` 等）は省くこと。
```

## 6.3 エージェントの自律 3 ステージ検証ループ (Autonomous 3-Stage Review Loop)

AI エージェントが図版やドキュメントを作成する際は、以下の **自律 3 ステージ検証ループ** を実行させることで、座標ズレや文字切れ、リンク切れのない高品質な成果物が得られます:

1. **Stage 1 — 静的・座標アンカー検証**:
   - プリミティブ要素（`shapes`, `text`, `icons`）は **中心座標 `(cx, cy)`**、高レベルコンポーネント（`SmartArts`, `Charts`, `Diagrams`）は **左下座標 `(x0, y0)`** というアンカー仕様の違いを確認します。
   - キャンバス幅（`120〜136` 前後）に対して `text_size >= 10.0` が確保されているか、`save()` が呼ばれているかを検査します。
2. **Stage 2 — マイクロジオメトリ・グリッド検証 (`drawlib show -g`)**:
   ```bash
   uv run drawlib show doc.md arch.png -s styles.py -u utils.py -g -o .drawlib/scratch/arch_grid.png
   ```
   - 10 単位（実線）および 5 単位（破線）の座標グリッドを重ねたプレビュー画像を出力し、マルチモーダル画像確認ツールでテキストのはみ出し、矢印の交差、余白バランス（外周 4〜6 単位以上）、50%+ ニュートラル配色を視覚検査して即座に座標を微調整します。
3. **Stage 3 — マクロページ・ブラウザ HTML / PDF 検証**:
   ```bash
   ./build.sh
   uv run drawlib serve report_html/ --check
   ```
   - 全体ビルド後に `drawlib serve <html_dir> --check` でリンク切れや画像欠損がないことを検証し、ブラウザレンダリング画面で本文テキストと図版内ラベルのサイズ感の調和を確認します。
