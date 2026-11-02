# AI エージェント指示とルール体系

Drawlib は、AI 支援エンジニアリング時代のためにゼロから設計されました。大規模言語モデル（LLM）に何千行もの壊れやすい生 SVG パス文字列や複雑な Matplotlib のボイラープレートを生成させる代わりに、ゼロショットで高品質なアーキテクチャ図を描画できる、明快で高水準な宣言的 Python API を AI エージェントに提供します。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/10_ai_agents_and_advanced/ai_agent_instructions/ai_agent_project_first_workflow.png" alt="ai_agent_instructions_1" />
  <figcaption class="drawlib-caption">Drawlib を使用する自律型 AI コーディングエージェントの4つの基本原則</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess
from drawlib.styles import Styles
from drawlib.text import text

setup(width=126, height=48)

rectangle((63, 24), width=120, height=42, style=Styles.MutedDashed.patch(shape_r=2.0))
text((63, 40.5), "Four Core Directives for Autonomous AI Coding Agents", style=Styles.DarkBold.patch(text_size=11.5))

# Stage Icons above ChevronProcess
icons = [
    (19.5, phosphor.folder_plus),
    (48.5, phosphor.book_open),
    (77.5, phosphor.cube),
    (106.5, phosphor.palette),
]
for ix, icon_fn in icons:
    icon_fn((ix, 31.8), width=5.0, style=Styles.PrimaryBold)

workflow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.6,
    flat_left_end=True,
)
workflow.add("1. Init Project", description="drawlib init project")
workflow.add("2. Query Rules", description="rules show", style=Styles.SecondaryNeutral)
workflow.add(
    "3. High-Level",
    description="Graph & SmartArt",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
workflow.add("4. Grid Repair", description="show -g & Fix", style=Styles.PrimaryNeutral)
workflow.draw(xy=(6, 7.5), width=114, height=18.5)

save()
```

</details>



---

## 1. AI エージェントに Drawlib が最適である理由

1. **決定論的な幾何座標系**: ラベルを少し変えただけで図全体の配置が予測不能に崩れるヒューリスティックな自動レイアウトエンジン（Graphviz や PlantUML など）とは異なり、Drawlib は左下を原点 `(0, 0)` とする予測可能なデカルト座標系を採用しています。
2. **高水準なドメイン抽象コンポーネント**: エンタープライズアーキテクチャ構成図、UML クラスモデル、定量データチャートを20行未満の Python コードで簡潔に構築できます。
3. **オンデマンドの知識取得機構**: Drawlib にはターミナルから参照できるルールカタログ（`drawlib rules show <topic>`）が組み込まれています。巨大なマニュアルを最初からプロンプトに詰め込んで貴重なコンテキストウィンドウを消費することなく、必要な API 仕様だけをオンデマンドで取得できます。

---

## 2. コマンド1行でのエージェント指示セットアップ（`drawlib init agent`）

プロンプトスニペットを手動でコピー＆ペーストしたり、ツールごとの YAML フロントマターを手書きしたりする必要はありません。`drawlib init agent` コマンドで、各 AI コーディングエージェントに最適化された Drawlib 指示ファイルを直接生成できます。

```bash
# 構文:
# uv run drawlib init agent <antigravity|claude|cursor|copilot|windsurf|cline|roo|codex|gemini|all|list> [-m <auto|always>] [-d <dir>] [-f]

# 対応 AI コーディングエージェント・出力先・フォーマット一覧を表示:
uv run drawlib init agent list

# 指定した AI エージェント向けにルールを生成（既定は --mode auto）:
uv run drawlib init agent antigravity
uv run drawlib init agent claude cursor copilot

# リポジトリ内の既存エージェント設定フォルダ・ファイルを自動検出して生成:
uv run drawlib init agent --detect

# ドキュメント・図解専用リポジトリ向けに常時読込（always）モードで生成:
uv run drawlib init agent antigravity --mode always

# 既存のルールファイルやマーカーブロックを上書き更新（-f / --force）、または別ワークスペースを指定（-d）:
uv run drawlib init agent antigravity --force
uv run drawlib init agent codex -d ./my-service --force

# モジュール分離型7種を一括生成、または個人グローバル設定へ配置:
uv run drawlib init agent all
uv run drawlib init agent antigravity --global
```

| ターゲット（`<agent>`） | プロジェクト出力先 | グローバル出力先（`-g`） | フォーマット・フロントマター仕様 |
| :--- | :--- | :--- | :--- |
| **`antigravity`** | `.agents/rules/drawlib.md` *（既存 `.agent/` がある場合は `.agent/rules/drawlib.md`）* | `~/.gemini/config/rules/drawlib.md` | YAML フロントマター必須（`auto` は `trigger: model_decision`、`always` は `always_on`） |
| **`claude`** | `.claude/rules/drawlib.md` | `~/.claude/rules/drawlib.md` | ルートの `CLAUDE.md` を汚さず安全に共存するモジュール式 Markdown |
| **`cursor`** | `.cursor/rules/drawlib.mdc` | *（IDE 設定画面管理）* | MDC フロントマター（`description`、`auto` は `alwaysApply: false` / `always` は `true`） |
| **`copilot`** | `.github/instructions/drawlib.instructions.md` | *（IDE / GitHub 設定）* | YAML フロントマター（`description`、`auto` は対象 glob の `applyTo` / `always` は `"**"`） |
| **`windsurf`** | `.windsurf/rules/drawlib.md` | `~/.codeium/windsurf/memories/global_rules.md` | 12,000文字上限に準拠した YAML `trigger` 付きルール（グローバルはマーカーマージ） |
| **`cline`** | `.clinerules/drawlib.md` | `~/Documents/Cline/Rules/drawlib.md` | Cline の Rules UI から個別 ON/OFF 可能なモジュール式 Markdown |
| **`roo`** | `.roo/rules/drawlib.md` | `~/.roo/rules/drawlib.md` | Roo Code 用モジュール式 Markdown ルール |
| **`codex`** *（別名 `agents-md`）* | `AGENTS.md` | `~/.codex/AGENTS.md` | `<!-- drawlib-agent-instruction:start/end -->` で非破壊マージされる共有 Markdown |
| **`gemini`** *（別名 `gemini-md`）* | `GEMINI.md` | `~/.gemini/GEMINI.md` | `<!-- drawlib-agent-instruction:start/end -->` で非破壊マージされる共有 Markdown |

### 2.1 トリガーモード切替と共有ファイルの非破壊マージ

- **省トークンな `auto` モード（既定）と `always` モード**: 既定の `--mode auto` では、フロントマター対応ツール（`antigravity`、`cursor`、`copilot`、`windsurf`）において「図解・チャート・スライド・`*_src/` ドキュメントの作成や編集」に関わるタスクの時だけオンデマンドでルールを読み込み、通常のアプリケーション実装時のコンテキスト消費（約 2,500 トークン）を抑えます。ドキュメント・図解専用リポジトリでは `--mode always`（`-m always`）を指定してください。
- **`AGENTS.md` / `GEMINI.md` の安全なマーカーブロック更新**: モジュール分離ファイル（`.agents/rules/drawlib.md` や `.claude/rules/drawlib.md` など）は既存の `CLAUDE.md` や `.github/copilot-instructions.md` に一切影響を与えません。また、ルート共有ファイル（`codex` -> `AGENTS.md`、`gemini` -> `GEMINI.md`）へ出力する際は `<!-- drawlib-agent-instruction:start -->` 〜 `<!-- drawlib-agent-instruction:end -->` のマーカーで囲んで既存ファイル末尾へ安全に追記し、`--force`（`-f`）再実行時は Drawlib ブロックのみをインプレース更新します。
- **Python API（`drawlib.tools`）**: 自動化スクリプトや CI からは `drawlib.tools` の `init_agent_instruction()`、`detect_agent_targets()`、`get_agent_instruction()`、`list_agent_targets()` を直接呼び出せます。

---

## 3. 動的な知識取得 (`drawlib rules`)

ドキュメントマニュアル全体をプロンプトへ貼り付ける代わりに、必要に応じて `drawlib rules` を実行して仕様を取得するようエージェントを訓練しましょう。Drawlib には**全31種類のモジュール別ルールマニュアル**（全般ガイドライン12項目 ＋ ライブラリモジュール仕様19項目）が内蔵されています。



<figure class="drawlib-image" style="text-align: center;">
  <img src="../../images/10_ai_agents_and_advanced/ai_agent_instructions/ai_agent_on_demand_rules_architecture.png" alt="ai_agent_instructions_2" />
  <figcaption class="drawlib-caption">AI コーディングエージェントによるオンデマンドのルール取得ワークフロー</figcaption>
</figure>

<details class="drawlib-code-details">
<summary>Source Code</summary>

```python
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=128, height=58)

# Left: AI Coding Agent
rectangle((20, 29), width=30, height=40, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.cpu((20, 42.5), width=5.0, style=Styles.WhiteBold)
text((20, 34.5), "AI Coding Agent", style=Styles.WhiteBold.patch(text_size=11.0))
text((20, 21.5), "1. Inspect Repo\n2. Query Rule\n3. Author Code", style=Styles.White.patch(text_size=10.2))

# Center: On-Demand CLI Dispatcher
rectangle((62, 29), width=26, height=22, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.terminal_window((62, 35.2), width=4.6, style=Styles.PrimaryBold)
text((62, 24.8), "CLI Rules\nrules show", style=Styles.DarkBold.patch(text_size=10.5))

# Right: 31 Modular Manuals Container
rectangle((104, 29), width=40, height=50, style=Styles.MutedDashed.patch(shape_r=2.5))
phosphor.book_open((88.5, 49.5), width=4.4, style=Styles.PrimaryBold)
text((106.5, 49.5), "31 Rule Manuals", style=Styles.DarkBold.patch(text_size=10.8))

rectangle(
    (104, 36.8),
    width=35,
    height=15.5,
    style=Styles.Neutral.patch(shape_r=1.5),
    text="12 General Manuals\noverview, style-guide,\nreview-guide, project-*",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)
rectangle(
    (104, 16.5),
    width=35,
    height=17.5,
    style=Styles.SecondaryNeutral.patch(shape_r=1.5),
    text="19 lib-* Manuals\nlib-graph, lib-diagrams,\nlib-smartarts, lib-charts",
    text_style=Styles.DarkBold.patch(text_size=10.0),
)

# Connectors
line((35, 33), (49, 33), arrow_head="->", style=Styles.DarkBold)
text((42, 36.8), "Query", style=Styles.DarkBold.patch(text_size=10.0))

line((49, 25), (35, 25), arrow_head="->", style=Styles.DarkBold)
text((42, 20.5), "Manual", style=Styles.Muted.patch(text_size=10.0))

line((75, 33), (86.5, 36.8), arrow_head="<->", style=Styles.DarkBold)
line((75, 25), (86.5, 16.5), arrow_head="<->", style=Styles.DarkBold)

save()
```

</details>



```bash
# List all 31 modular rule topics and cache status:
uv run drawlib rules list

# Retrieve targeted manuals:
uv run drawlib rules show agent-instruction    # Workflow loop & bootstrap rules
uv run drawlib rules show overview             # Cartesian geometry & canvas lifecycle
uv run drawlib rules show style-guide          # 6-color semantic system & 50%+ neutral baseline
uv run drawlib rules show review-guide         # 3-stage multimodal review loop & 720pt font math
uv run drawlib rules show anim-guide           # Animation loop idioms & component patterns
uv run drawlib rules show project-overview     # 4 project archetypes & decision matrix
uv run drawlib rules show project-images       # Standalone images project (images_src/*.py)
uv run drawlib rules show project-doc          # Linear document & PDF project (doc_src/*.md)
uv run drawlib rules show project-site         # Multi-page documentation website (docs_src/**/*.md)
uv run drawlib rules show project-slide        # 1920x1080 slide stage authoring & templates (slide_src/*.md)
uv run drawlib rules show api                  # Complete API index & symbol cheat sheet
```

### 3.1 `drawlib rules` トピックカタログ一覧

#### 全般ガイドライン（12トピック）:

| トピック名 | 主な内容 |
| :--- | :--- |
| **`agent-instruction`** | AI エージェントの初期指示、プロジェクトファースト原則、マルチモーダル検証ワークフローループ。 |
| **`overview`** | キャンバスライフサイクル（`setup`、`clear`、`save`）、左下 `(0, 0)` 原点の座標系、基本インポート。 |
| **`style-guide`** | 視覚的階層、50%以上をニュートラルスタイルにする原則、6つのセマンティックカラー、文字サイズ設計。 |
| **`review-guide`** | 自律3段階マルチモーダル検証ループ、`720pt` 基準の文字スケーリング、座標アンカー対応表。 |
| **`anim-guide`** | プリミティブ・SmartArts・Charts・Diagrams・Graphs にわたるアニメーションループの実装イディオム（再描画 vs 状態更新）。 |
| **`project-overview`** | 4つのプロジェクトアーキタイプ（`images`、`doc`、`site`、`slide`）の構成、共通ファイル、キャッシュ機構。 |
| **`project-images`** | スタンドアロン画像プロジェクト（`images_src/*.py` -> `images/*.png`）、`save()` の出力先自動制御、グリッド検証。 |
| **`project-doc`** | リニア技術文書・PDF プロジェクト（`doc_src/*.md`）、`00_cover.md`、`--toc`、改ページを考慮した図のサイズ設計。 |
| **`project-site`** | マルチページ Web サイト（`docs_src/**/*.md`）、`navbar.md` 構文、トップヒーロー原則、`drawlib serve --check`。 |
| **`project-slide`** | 16:9 スライドステージ（`1920x1080`）、`::: block` / `::: note` 構文、レイアウトテンプレート、発表者ビュー。 |
| **`cli`** | 全 CLI コマンド・フラグ・終了コードのリファレンスマニュアル。 |
| **`api`** | 全 `drawlib.*` モジュールを網羅した API インデックスとシンボルシグネチャ早見表。 |

#### ライブラリモジュール仕様（19個の `lib-*` トピック）:

| トピック名 | 対象モジュール | 主な内容 |
| :--- | :--- | :--- |
| **`lib-canvas`** | `drawlib.canvas` | `setup()`、`clear()`、`save()`、`show()`、`get_dimage()`、グリッドおよび背景スタイル設定。 |
| **`lib-anim`** | `drawlib.anim` | `Animation(fps)`、`add()`、`save()`（APNG・アニメーション WebP）、`fps` / `frame_rate`。 |
| **`lib-shapes`** | `drawlib.shapes` | 30種類の幾何プリミティブ（`rectangle`、`circle`、`cylinder`、`cube`、`document`、`cloud`、`brace`、`gear`、`math_symbol`、`arrow` など）。 |
| **`lib-lines`** | `drawlib.lines` | `line()`、`lines()`、`line_curved()`、`lines_curved()`、`line_arc()`、ベジェ曲線、矢尻スタイル。 |
| **`lib-text`** | `drawlib.text` | `text()`、`text_vertical()`、配置揃え（`halign`、`valign`）、回転、フォントサイズ補助関数。 |
| **`lib-preset-colors`** | `drawlib.preset_colors` | `DefaultColors`、`GoogleColors`、`MonochromeColors`、`CssColors`、RGB / RGBA タプル。 |
| **`lib-styles`** | `drawlib.styles` | `Styles`・`Colors` の動的ファサード、および `styles.py` / `utils.py` 注入アーキテクチャ。 |
| **`lib-preset-styles`** | `drawlib.preset_styles` | 6つのテーマにわたる10種類の直交スタイル修飾子（`Flat`、`Neutral`、`Outline`、`Dashed` など）。 |
| **`lib-fonts`** | `drawlib.fonts` | `Font`、`FontRoboto`、`FontMonoSpace`、`FontSourceCode`、CJK・多言語フォントファミリー、`FontFile`。 |
| **`lib-images`** | `drawlib.images` | `image()`、`Dimage` 画像変換（`trim`、`fill`、`alpha`、`resize`）、`get_dimage_from_code()`。 |
| **`lib-icons`** | `drawlib.icons` | `phosphor`（1,512種のベクターアイコン）、`fontawesome`（5ブランド）、`gcp`（212種の公式クラウドアイコン）。 |
| **`lib-math`** | `drawlib.math` | 距離、角度、バウンディングボックス、直線・折れ線経路の補間、回転、直交ウェイポイントルーティング。 |
| **`lib-types`** | `drawlib.types` | `Style`、`Color`、`FontBase`、配置・線種のリテラル型、`.patch()` によるイミュータブル更新。 |
| **`lib-smartarts`** | `drawlib.smartarts` | `ChevronProcess`、`Cycle`、`GridLayout`、`Pyramid`、`BoxList`、`BulletPoints`、`TreeNode`、`MindMapNode`、`Table`、`SourceCode`、`MonthCalendar`、`WeekCalendar`、`DayCalendar`。 |
| **`lib-charts`** | `drawlib.charts` | `BarChart`、`LineChart`、`AreaChart`、`PieChart`、`RadarChart`、`ScatterChart`、`GanttChart`、`HeatmapChart`、`HeatmapOverlay`。 |
| **`lib-diagrams`** | `drawlib.diagrams` | `ArchitectureDiagram`、`FlowDiagram`、`SequenceDiagram`、`ClassDiagram`、`ERDiagram`、`StateDiagram`。 |
| **`lib-graph`** | `drawlib.graph` | `ArchitectureGraph`、`LayerGraph`、`TreeGraph`、`RadialGraph`、`GridGraph`、`get_layout()`、`GraphLayout`。 |
| **`lib-tools`** | `drawlib.tools` | `build_*`、`export_code_block`、`init_project`、`init_agent_instruction`、`serve_docs`、`list_cache` などのプログラマティック Python API。 |
| **`lib-slide`** | `drawlib.slide` | `current_slide`、`SlideContext`、`BoundingBox`、および `build_slide()`。 |

---

## 4. プロンプト設計とマルチエージェント並列化のベストプラクティス

AI エージェントにダイアグラムや複数ページのドキュメント生成を依頼する際は、以下のポイントを押さえると効果的です。
- **実際のコードコンテキストを渡す**: 実在するソースファイルを具体的に指定します（例：「`src/services/order.py` を調査し、上流・下流の依存関係を示す `ArchitectureDiagram` を描いてください」）。
- **対象のプロジェクトやドキュメントを明示する**: 既存の Markdown ページ（`docs_src/architecture.md`）に埋め込むのか、スタンドアロンの `images_src/` スクリプトとして作成するのかを伝えます。
- **マルチモーダル検証を指示する**: 完了前に `-g` 付きで `.drawlib/scratch/` へ出力し、生成画像を目視検証するようエージェントに促します。
- **複数ファイルの作業は並列サブエージェントへ分散する**: マルチモーダルな `drawlib show -g` と画像検査のサイクルはコンテキストウィンドウのトークンを消費するため、複数章のドキュメント（`doc_src/*.md`）、マルチページサイト（`docs_src/**/*.md`）、スライドデッキ（`slide_src/*.md`）、一括画像スクリプト（`images_src/*.py`）の作成では、**3フェーズのオーケストレータ・サブエージェント協調プロトコル**を実行します。
  1. **フェーズ 1（親オーケストレータ）**: `drawlib init project <doc|site|slide|images>` を実行し、共通の `drawlib.toml`、`styles.py`、`utils.py`、`_assets/`、および `navbar.md`（または章・スライド構成案）を確定します。
  2. **フェーズ 2（並列サブエージェント）**: 重複しない `.py` または `.md` ファイル群を各サブエージェントへ割り当てます。各サブエージェントは担当ファイルを執筆し、**一意なスクラッチファイル名**（`-o .drawlib/scratch/<file_or_block>_grid.png`）を使ってステージ 1・ステージ 2 のグリッド検証を完了させます。
  3. **フェーズ 3（親オーケストレータ）**: 全サブエージェントの完了後に `./build.sh` を1回だけ実行し、リンク検証（`drawlib serve --check`）およびステージ 3 の HTML / PDF 外観検証を行います。
