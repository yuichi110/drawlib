# 14. CLI ツールチェインと自律型 AI エージェント協業

Drawlib は、人間のエンジニアだけでなくマルチモーダル AI コーディングエージェントとの協業を前提にゼロから設計されています。すべての図版・技術文書・スライドが決定論的な CLI（`drawlib`）を通じてヘッドレスにビルドできるため、AI エージェントが当て推量で座標を書いたり GUI 操作で詰まったりすることはありません。

AI エージェントは必要に応じて内蔵リファレンス（`drawlib rules show`）を参照し、プロジェクトを初期化（`drawlib init`）し、座標グリッド付きで単体プレビューを出力（`drawlib show -g`）して視覚的に自己検証し、文字重なりを 1 回で補正した上でリンク切れ検査（`drawlib serve --check`）までを自律的に完結させます。

```drawlib align=center code=fold file=ai_multimodal_loop_ja.png caption="図 14.1: 自律型 AI エージェントによる 3 段階マルチモーダル自己修正ループ"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line, lines
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=70)

text(
    (79.0, 63.8),
    "自律型 AI エージェントの 3 段階マルチモーダル自己修正ループ",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# Step 0: ルール参照 & コード執筆（Neutral）
rectangle((22.5, 39.5), width=32.5, height=33.0, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.book_open((22.5, 50.8), width=5.0, style=Styles.PrimaryBold)
text((22.5, 44.0), "0. 規約参照・執筆", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (22.5, 31.8),
    "• rules show <topic>\n• .md / .py を作成\n• styles.py・utils.py",
    style=Styles.Dark.patch(text_size=10.0),
)

# Stage 1: 静的・アンカー検査（PrimaryNeutral）
rectangle((60.2, 39.5), width=32.5, height=33.0, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.list_checks((60.2, 50.8), width=5.0, style=Styles.PrimaryBold)
text((60.2, 44.0), "Stage 1: 静的検査", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (60.2, 31.8),
    "• 2図以上・Hero L5-15\n• text_size >= 10.0\n• 座標アンカー確認",
    style=Styles.Dark.patch(text_size=10.0),
)

# Stage 2: グリッド視覚検証（焦点 PrimaryFlat）
rectangle((97.8, 39.5), width=32.5, height=33.0, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.grid_four((97.8, 50.8), width=5.0, style=Styles.WhiteBold)
text((97.8, 44.0), "Stage 2: Grid (-g)", style=Styles.WhiteBold.patch(text_size=11.0))
text(
    (97.8, 31.8),
    "• drawlib show -g\n• 10/5単位グリッド確認\n• 重なり・はみ出し検知",
    style=Styles.White.patch(text_size=10.0),
)

# Stage 3: マクロページ検証（SecondaryNeutral）
rectangle((135.5, 39.5), width=32.5, height=33.0, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.browser((135.5, 50.8), width=5.0, style=Styles.SecondaryBold)
text((135.5, 44.0), "Stage 3: 全体検証", style=Styles.DarkBold.patch(text_size=11.0))
text(
    (135.5, 31.8),
    "• build & serve --check\n• 1280x920 画面確認\n• PDF / DOCX / PPTX",
    style=Styles.Dark.patch(text_size=10.0),
)

# 前進パイプライン矢印
line((38.8, 39.5), (43.9, 39.5), arrow_head="->", style=Styles.DarkBold)
line((76.5, 39.5), (81.5, 39.5), arrow_head="->", style=Styles.DarkBold)
line((114.1, 39.5), (119.2, 39.5), arrow_head="->", style=Styles.DarkBold)

# Stage 2 から Step 0 への自己修正フィードバック経路
lines([(97.8, 22.8), (97.8, 11.0), (22.5, 11.0), (22.5, 22.2)], arrow_head="->", style=Styles.PrimaryBold)
rectangle((60.2, 11.0), width=64.0, height=7.6, style=Styles.White.patch(shape_r=1.5))
text(
    (60.2, 11.0),
    "自己修正ループ：グリッド目盛りで座標を一発補正",
    style=Styles.DarkBold.patch(text_size=10.2),
)

save()
```

---

## 14.1 プロジェクトと AI ルールの初期化（`drawlib init`）

`drawlib init` コマンド群は、プロジェクト骨格の生成（`drawlib init project`）と、AI コーディングエージェント向けルールファイルの自動配置（`drawlib init agent`）の 2 つの役割を担います。

`drawlib init agent` を実行すると、Drawlib の設計規約・`720pt` タイポグラフィ計算式・座標アンカー規則・3 段階自己検証プロトコルが各 AI ツール固有のルール形式で書き出されます。Drawlib `v0.3.10` は以下の 9 つのエージェントターゲットを標準サポートしており、さらに共通規格である `AGENTS.md` を介して Kiro や OpenCode などの `AGENTS.md` 準拠エージェントともそのまま連携できます。

| CLI ターゲット | 対応 AI アシスタント | 生成されるワークスペースパス | ルール形式・読み込み挙動 |
| :--- | :--- | :--- | :--- |
| **`antigravity`** | Google Antigravity | `.agents/rules/drawlib.md` | YAML フロントマター（`trigger: model_decision` または `always_on`） |
| **`gemini`** | Gemini CLI | `GEMINI.md` | HTML コメントマーカーによる非破壊マージ（`--global` で `~/.gemini/GEMINI.md`） |
| **`claude`** | Claude Code | `.claude/rules/drawlib.md` | ルートの `CLAUDE.md` と競合しないモジュラールールファイル |
| **`cursor`** | Cursor | `.cursor/rules/drawlib.mdc` | MDC フロントマター（`description`, `alwaysApply`） |
| **`codex`** | OpenAI Codex / `AGENTS.md` | `AGENTS.md` | HTML マーカーによる非破壊追記（Codex・Kiro 等の `AGENTS.md` 対応ツール共通） |
| **`copilot`** | GitHub Copilot | `.github/instructions/drawlib.instructions.md` | YAML フロントマター（`applyTo: "**/*_src/**, **/*.md, **/*.py"`） |
| **`windsurf`** | Windsurf | `.windsurf/rules/drawlib.md` | YAML トリガー付き Cascade ワークスペースルール |
| **`cline`** | Cline | `.clinerules/drawlib.md` | `.clinerules/` 配下で個別に ON/OFF 可能なルールファイル |
| **`roo`** | Roo Code | `.roo/rules/drawlib.md` | ワークスペースまたは `--global` 対応のモジュラールール |

`--detect` フラグを渡せばリポジトリ内の既存エージェント設定フォルダを自動検出して最適なルールを生成でき、既定の `-m auto` モードにより作図・ドキュメント関連タスク時のみオンデマンドで読み込まれるためコンテキストトークンを無駄に消費しません。

```bash
# 対応する AI エージェント一覧と出力先パスを表示
uv run drawlib init agent list

# リポジトリ内で使用中の AI エージェントを自動検出してルールを生成
uv run drawlib init agent --detect

# 特定の AI エージェント向けにルールを一括生成（'all' でモジュラー 7 種を一括生成）
uv run drawlib init agent antigravity claude cursor copilot

# ドキュメント専用リポジトリ向けに常時読み込みモード（always）で生成
uv run drawlib init agent antigravity --mode always

# ユーザーホーム配下（~/.claude/rules/ 等）へグローバルルールとして導入
uv run drawlib init agent claude --global
```

---

## 14.2 マルチ形式ビルド・SHA-256 キャッシュ・検証サーバー

プロジェクト初期化後の日常開発・高速プレビュー・マルチ形式出版・CI 品質検査は、以下の 5 つの主要 CLI コマンドグループで完結します。

| コマンド群 | 主なサブコマンド・オプション | 主な役割 |
| :--- | :--- | :--- |
| **`drawlib build`** | `html`, `pdf`, `docx`, `slide`, `pptx`, `markdown`, `image`（`-s`, `-u`, `--no-cache`） | `<target>_src/` から HTML サイト／白書／スライド・ベクター PDF・編集可能な `.docx`／`.pptx`・GitHub Markdown・PNG/WebP/GIF 画像を一括コンパイルします。 |
| **`drawlib show`** | `<file> [target] -s styles.py -u utils.py -g -o preview.png` | 単一の `.py` または Markdown 内の名前付きブロック（`file=arch.png`）だけを `10/5` 単位グリッド（`-g`）付きで高速ヘッドレス出力します。 |
| **`drawlib serve`** | `<html_dir> [-p 8000] [--no-browser] [--check]` | 依存ゼロのローカル確認用 HTTP サーバーを起動します。`--check` を付けると `<a href>` リンク切れと `<img src>` 欠損を検査して終了コードを返します。 |
| **`drawlib cache`** | `list`, `clear --images`, `clear --all`, `download --all`, `download --browser` | `.drawlib/cache.db` の画像キャッシュ管理に加え、フォント・34 種アイコン・地図データ・Playwright ヘッドレス Chromium の事前取得を行います。 |
| **`drawlib rules`** | `list`, `show <topic> [--raw \| --rebuild]`, `build --all`, `clear` | 人間と LLM の双方がターミナル上で即座に参照できる自己文書化マニュアル（`overview`, `cli`, `style-guide`, `review-guide`, `lib-*`）を提供します。 |

### `.drawlib/cache.db` の仕組み：SHA-256 コンテンツアドレス型キャッシュ

本文の誤字を 1 文字直すたびに 50 枚の Python 図版を再描画していては執筆サイクルが滞ります。Drawlib は各 `drawlib` ブロックや `.py` スクリプトを実行する前に、以下の 4 要素から決定論的な **SHA-256 ハッシュキー**を算出します。
1. ブロックまたは `.py` スクリプトの正確な Python 作図コード。
2. `styles.py`（`-s`）および `utils.py`（`-u`）のファイル内容全体。
3. コード内の文字列リテラルで参照されたローカル静的ファイル（`"_assets/logo.png"` など）。
4. 出力画像フォーマット（`png` / `webp` / `svg`）・相対パス・総スライド数。

`.drawlib/cache.db` 内に一致するハッシュが存在すれば、Matplotlib を一切起動せず **1 ミリ秒未満**でキャッシュ済みバイナリを復元します。キャッシュ DB は自動で `.drawlib/.gitignore`（`*`）を生成し、`drawlib` や `matplotlib` のバージョン更新時の自動無効化と `1 GiB` 超過時の古いエントリ 50% 自動削除（LRU）も備えています。`styles.py` / `utils.py` 以外の外部自作モジュールを `import` して編集した場合は、`--no-cache` または `drawlib cache clear --images` で再描画を強制できます。

```bash
# 1. Markdown 内の特定図版だけを 10/5 単位の座標グリッド (-g) 付きで高速出力
uv run drawlib show doc_src/en/01_overview.md system_arch.png \
    -s doc_src/styles.py -u doc_src/utils.py -g --no-cache -o .drawlib/scratch/arch_grid.png

# 2. マルチ形式ビルド（HTML・目次付き A4 PDF・Word .docx・16:9 スライド・PowerPoint .pptx）
uv run drawlib build html docs_src/ -o docs_html/ -s docs_src/styles.py -u docs_src/utils.py
uv run drawlib build pdf doc_src/ -o manual.pdf --page-break --generate-index -s doc_src/styles.py
uv run drawlib build docx doc_src/ -o manual.docx --page-break --generate-index --dpi 200
uv run drawlib build slide slide_src/ -o slide_html/ -s slide_src/styles.py
uv run drawlib build pptx slide_src/ -o slide.pptx --dpi 240 -s slide_src/styles.py
uv run drawlib build markdown docs_src/ -o docs_markdown/
uv run drawlib build image images_src/ -o images/ -f webp

# 3. CI 用アセット事前取得・画像キャッシュ削除・リンク切れ検査・オンデマンド規約参照
uv run drawlib cache download --all
uv run drawlib cache clear --images
uv run drawlib serve docs_html/ --check
uv run drawlib rules list
uv run drawlib rules show lib-smartarts-overview --raw
```

```drawlib align=center code=fold file=cli_command_map_ja.png caption="図 14.2: Drawlib CLI コマンド体系と SHA-256 SQLite キャッシュパイプライン"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=158, height=76)

text(
    (79.0, 70.2),
    "Drawlib CLI コマンド体系と SHA-256 差分ビルドキャッシュ機構",
    style=Styles.DarkBold.patch(text_size=12.8),
)

# 上段: init / rules / show（ニュートラル基調カード 3 枚）
rectangle((29.0, 56.5), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.folder_plus((11.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((31.5, 60.5), "drawlib init", style=Styles.DarkBold.patch(text_size=11.2))
text((29.0, 52.2), "project (5種別) | agent (--detect)", style=Styles.Dark.patch(text_size=10.0))

rectangle((79.0, 56.5), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.book_open((61.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((81.5, 60.5), "drawlib rules", style=Styles.DarkBold.patch(text_size=11.2))
text((79.0, 52.2), "list | show <topic> (--raw)", style=Styles.Dark.patch(text_size=10.0))

rectangle((129.0, 56.5), width=46.0, height=16.5, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
phosphor.grid_four((111.5, 60.5), width=4.6, style=Styles.PrimaryBold)
text((131.5, 60.5), "drawlib show", style=Styles.DarkBold.patch(text_size=11.2))
text((129.0, 52.2), "<file> [target] -g -o preview.png", style=Styles.Dark.patch(text_size=10.0))

# 中段: build（焦点 PrimaryFlat） / serve / cache
rectangle((29.0, 37.0), width=46.0, height=16.5, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.cpu((11.5, 41.0), width=4.6, style=Styles.WhiteBold)
text((31.5, 41.0), "drawlib build", style=Styles.WhiteBold.patch(text_size=11.2))
text((29.0, 32.7), "html | pdf | docx | slide | pptx | image", style=Styles.White.patch(text_size=10.0))

rectangle((79.0, 37.0), width=46.0, height=16.5, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
phosphor.globe((61.5, 41.0), width=4.6, style=Styles.SecondaryBold)
text((81.5, 41.0), "drawlib serve", style=Styles.DarkBold.patch(text_size=11.2))
text((79.0, 32.7), "<dir> -p 8000 | --check (CI 検証)", style=Styles.Dark.patch(text_size=10.0))

rectangle((129.0, 37.0), width=46.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.0))
phosphor.database((111.5, 41.0), width=4.6, style=Styles.SecondaryBold)
text((131.5, 41.0), "drawlib cache", style=Styles.DarkBold.patch(text_size=11.2))
text((129.0, 32.7), "list | clear --images | download --all", style=Styles.Dark.patch(text_size=10.0))

# 下段: .drawlib/cache.db SHA-256 キャッシュパイプライン
rectangle((79.0, 14.0), width=146.0, height=16.5, style=Styles.Neutral.patch(shape_r=2.2))
rectangle((31.0, 14.0), width=42.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
text((31.0, 14.0), "コード + styles/utils + 素材", style=Styles.DarkBold.patch(text_size=10.0))

line((52.0, 14.0), (59.5, 14.0), arrow_head="->", style=Styles.DarkBold)

rectangle((78.5, 14.0), width=36.0, height=11.5, style=Styles.PrimaryNeutral.patch(shape_r=1.5))
text((78.5, 14.0), "SHA-256 cache.db", style=Styles.DarkBold.patch(text_size=10.2))

line((96.5, 14.0), (104.0, 14.0), arrow_head="->", style=Styles.DarkBold)

rectangle((126.5, 14.0), width=43.0, height=11.5, style=Styles.White.patch(shape_r=1.5))
text((126.5, 14.0), "Hit: <1ms復元 | Miss: 再描画", style=Styles.DarkBold.patch(text_size=10.0))

# build からキャッシュ機構外枠への接続
line((29.0, 28.5), (29.0, 22.6), arrow_head="->", style=Styles.DarkBold)

save()
```

---

## 14.3 徹底解説：AI エージェントの 3 段階自律検証ループ

単体 PNG 画像を 1 回眺めるだけでは、出版品質は保証できません。キャンバス内部での微妙なラベル重なり（ミクロ幾何の欠陥）と、HTML カラムや 16:9 スライドに埋め込んだ際の文字縮小・ファーストビュー崩れ（マクロページの欠陥）は性質が異なるためです。AI エージェントは以下の 3 段階検証を順に実行することで両方の欠陥を自律的に解消します。

1. **Stage 1 — 静的コード・座標アンカー事前検査**:
   - 各ドキュメントページに `2` 個以上の `drawlib` 図版が含まれ、**5〜15 行目に `code=fold` の Top Hero 図**が配置されていることを確認します。
   - フェンスへの狭いピクセル幅指定（`width=500px` / `600px`）がないこと、`text_size >= 10.0` であること、相対パスのみが使われていること、および各コンポーネントの座標アンカー仕様（`Center` / `Bottom-Left` / `Top-Left`）の計算が正しいことを確認します。
2. **Stage 2 — 座標グリッドによるミクロ幾何レビュー（`drawlib show -g`）**:
   - 作成・変更した各図版を `-g` 付きで個別出力（`uv run drawlib show <file> <target.png> -s styles.py -u utils.py -g -o .drawlib/scratch/<unique>_grid.png`）し、マルチモーダル視覚ツールで確認します。
   - `-g` オーバーレイには数値ラベル付きの **10 単位主グリッド線**と **5 単位補助破線**が描画されるため、テキストの枠線はみ出し・矢印との干渉・外周マージン不足（`< 4〜6` 単位）・虹色過多（ニュートラル比率 `< 50%`）を見つけた際、正確な修正先座標を 1 回で読み取って修正できます。
3. **Stage 3 — マクロページ・最終成果物レビュー**:
   - `./<target>_src/build.sh` でビルド後、`uv run drawlib serve <target>_html/ --check` でリンク切れと画像欠損がゼロであることを検証し、**`1280×920` デスクトップ画面のヘッドレス Chromium スクリーンショット**（および生成された `PDF` / `DOCX` / `PPTX`）を視覚確認します。
   - スクロールなしで Top Hero 図がファーストビューに収まり、図中テキストが周囲の `16px` HTML 本文（`1920×1080` スライドでは `26px` 本文）と同等の視認性を持っていることを確認し、最後に `.drawlib/scratch/` を削除します。

---

## 14.4 並列サブエージェント委譲による大規模ドキュメント構築

全 16 章の技術書（`doc`）や数十ページのポータル（`site` / `catalog`）、20 枚超のスライド（`slide`）を単一エージェントのコンテキスト内で直列に執筆・画像確認すると、高解像度プレビュー画像でコンテキストウィンドウが圧迫されます。Drawlib のファイル分割構造は、**3 フェーズの親オーケストレータ・並列サブエージェント委譲パターン**にそのまま適合します。

- **Phase 1 — 親エージェントによる共通基盤の確立**: 親エージェントが先に `drawlib init project` を実行し、`drawlib.toml`・`styles.py`（および `ja/styles.py`）・`utils.py`・`_assets/`・`<lang>/navbar.md` や章ファイル名一覧を確定させます。
- **Phase 2 — サブエージェントによる排他的ファイル執筆（`--no-cache`）**: 各サブエージェントは互いに重複しない `.md` / `.py` ファイル群だけを担当し（共通設定ファイルは読み取り専用）、**固有のスクラッチ出力名**（`drawlib show ... -g --no-cache -o .drawlib/scratch/<worker>_<stem>.png`）を使って Stage 1・Stage 2 の視覚検証を独立コンテキスト内で完了させます。`.drawlib/cache.db` の SQLite 書き込み競合を防ぐため、サブエージェント内では `./build.sh` を実行しません。
- **Phase 3 — 親エージェントによる統合ビルドとリンク検査**: 全サブエージェントの完了後、親エージェントが `./<target>_src/build.sh` を 1 回実行し、`drawlib serve --check` と Stage 3 ブラウザ／PDF 検証を行って `.drawlib/scratch/` をクリーンアップします。
