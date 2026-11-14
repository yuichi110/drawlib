# 2. インストールとゼロ設定ツールチェイン

Drawlib `v0.3.10` は **Python `3.11+`（`3.11`・`3.12`・`3.13`・`3.14`）** で動作する自己完結型の純粋 Python ツールチェインであり、Linux・macOS・Windows のいずれの環境でも Graphviz 本体や LaTeX 環境、Node.js バンドラを別途インストールする必要はありません。

既存の Python プロジェクトへ `uv add drawlib` で依存追加する運用はもちろん、Go・Rust・TypeScript・Java などの多言語リポジトリで設定ファイルを一切作らず `uvx drawlib` から即時実行する運用にも同じ CLI とキャッシュ機構で対応します。

```drawlib align=center code=fold file=install_workflows_ja.png caption="図 2.1: 2つの導入ワークフロー — Python プロジェクト依存 (uv add) と多言語ゼロインストール実行 (uvx)"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, Node, NodeGroup, PhosphorIcon
from drawlib.styles import Styles

setup(width=148, height=62)

d = ArchitectureDiagram(
    node_style=Styles.PrimaryBold,
    node_text_style=Styles.DarkBold.patch(text_size=10.8),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

g_py = d.add(
    NodeGroup(
        title="1. Python リポジトリ (uv add)",
        width=50.0,
        height=23.0,
        style=Styles.PrimaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(3.0, 31.0),
)
g_py.add(
    Node(
        "pyproject.toml + .venv\nuv run drawlib ...",
        width=44.0,
        height=12.0,
        icon=PhosphorIcon.PACKAGE,
        icon_size=5.0,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(25.0, 8.8),
)

g_uvx = d.add(
    NodeGroup(
        title="2. 多言語・文書リポジトリ (uvx)",
        width=50.0,
        height=23.0,
        style=Styles.SecondaryNeutral.patch(shape_r=2.0),
        text_style=Styles.DarkBold.patch(text_size=10.8, halign="left"),
    ),
    xy=(3.0, 4.0),
)
g_uvx.add(
    Node(
        "Go / Rust / TS / Java\nuvx drawlib ... (設定不要)",
        width=44.0,
        height=12.0,
        icon=PhosphorIcon.TERMINAL_WINDOW,
        icon_size=5.0,
        card_style=Styles.White.patch(shape_r=1.6),
    ),
    xy=(25.0, 8.8),
)

cli_node = d.add(
    Node(
        "Drawlib v0.3.10\nCLI & コンパイラ",
        width=31.0,
        height=20.0,
        icon=PhosphorIcon.CPU,
        icon_size=5.8,
        style=Styles.WhiteBold,
        text_style=Styles.WhiteBold.patch(text_size=11.2),
        card_style=Styles.PrimaryFlat.patch(shape_r=2.2),
    ),
    xy=(78.5, 29.0),
)

cache_node = d.add(
    Node(
        "自動アセットキャッシュ\n(フォント・アイコン・ブラウザ)",
        width=39.0,
        height=15.0,
        icon=PhosphorIcon.DATABASE,
        icon_size=5.0,
        card_style=Styles.Neutral.patch(shape_r=1.8),
    ),
    xy=(122.5, 42.5),
)

out_node = d.add(
    Node(
        "マルチ形式の成果物\n(HTML / PDF / DOCX / PPTX)",
        width=39.0,
        height=15.0,
        icon=PhosphorIcon.EXPORT,
        icon_size=5.0,
        card_style=Styles.SecondaryNeutral.patch(shape_r=1.8),
    ),
    xy=(122.5, 15.5),
)

j_in_top = d.junction((58.0, 42.5))
j_in_mid = d.junction((58.0, 29.0))
j_in_bot = d.junction((58.0, 15.5))
d.connect(g_py, j_in_top, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(g_uvx, j_in_bot, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_in_top, j_in_mid, arrow="-", routing="direct")
d.connect(j_in_bot, j_in_mid, arrow="-", routing="direct")
d.connect(j_in_mid, cli_node, arrow="->", routing="direct", padding=(0.0, 0.8))

j_out_mid = d.junction((98.5, 29.0))
j_out_top = d.junction((98.5, 42.5))
j_out_bot = d.junction((98.5, 15.5))
d.connect(cli_node, j_out_mid, arrow="-", routing="direct", padding=(0.8, 0.0))
d.connect(j_out_mid, j_out_top, arrow="-", routing="direct")
d.connect(j_out_mid, j_out_bot, arrow="-", routing="direct")
d.connect(j_out_top, cache_node, arrow="->", routing="direct", padding=(0.0, 0.8))
d.connect(j_out_bot, out_node, arrow="->", routing="direct", padding=(0.0, 0.8))

d.draw(xy=(2.0, 2.0))
save()
```

---

## 2.1 動作要件と 2 つの実行モード

Drawlib は現行の CPython ランタイムをサポートしており、高速なパッケージマネージャである `uv` と組み合わせることでロックファイル管理もゼロインストール実行もシームレスに行えます。

| 要件項目 | サポート仕様 | 備考 |
| :--- | :--- | :--- |
| **Python バージョン** | **Python `3.11+`（`3.11`・`3.12`・`3.13`・`3.14`）** | Linux（`x86_64` / `aarch64`）・macOS・Windows 対応 |
| **推奨ランナー** | **`uv`（`uv add` / `uv run` / `uvx`）** | 仮想環境の高速構築および多言語リポジトリでの即時実行に対応 |
| **標準代替手段** | **`pip`（`venv` + `pip install drawlib`）** | 追加の extra 指定なしで全機能が標準インストール可能 |

### 2.1.1 方法 1：Python プロジェクトへの導入（`uv add drawlib`）

Python アプリケーションやデータ分析基盤、あるいは `pyproject.toml` と `uv.lock` でバージョンを厳密に固定したいドキュメント専用リポジトリでは、`uv add drawlib` による導入を推奨します。

```bash
# 新規 uv プロジェクトの作成と drawlib の追加（既存 Python リポジトリ内でも同様）
uv init my_project
uv add drawlib
uv run drawlib --version

# uv を使用しない環境での標準 venv + pip フォールバック
python3 -m venv .venv
.venv/bin/pip install drawlib
.venv/bin/drawlib --version
```

プロジェクト依存として追加すると、エディタ（`Pyright`・`Pylance`・`Ruff`）上で `drawlib.shapes`・`drawlib.smartarts`・`drawlib.charts`・`drawlib.diagrams` の型補完が完全に効き、CI でも `uv sync --frozen` で再現性の高いビルドが可能になります。

### 2.1.2 方法 2：多言語リポジトリでのゼロインストール実行（`uvx drawlib`）

**Go・Rust・TypeScript・Java・C++ リポジトリや純粋な Markdown 文書リポジトリ**では、ルート直下に `pyproject.toml` や `.venv/` を作る必要はありません。`uvx` を付けて実行するだけで、隔離されたツールキャッシュ環境から Drawlib CLI を即座に呼び出せます。

```bash
# ローカル設定ファイル一切不要でバージョン確認
uvx drawlib --version

# Go / Rust / TS リポジトリ内に多言語ドキュメント基盤を初期化して HTML ビルド
uvx drawlib init project site docs -l en,ja -s google
uvx drawlib build html docs_src/ -o docs_html/
```

---

## 2.2 同梱ランタイム基盤と自動アセットキャッシュ

図表描画・PDF 変換・Word/PowerPoint 出力ごとに別々のプラグイン導入を強いる従来のツールとは異なり、**`drawlib v0.3.10` は単一パッケージにすべての描画・出版エンジンを標準同梱**しています（`drawlib[pdf]` のようなオプション指定は不要です）。

```drawlib align=center code=fold file=toolchain_batteries_ja.png caption="図 2.2: Drawlib v0.3.10 のゼロ設定ランタイム構成と自動キャッシュ基盤"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import KpiCards
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=66)

rectangle((74.0, 56.5), width=136.0, height=8.6, style=Styles.PrimaryFlat.patch(shape_r=2.0))
phosphor.package((13.5, 56.5), width=5.0, style=Styles.WhiteBold)
text(
    (18.5, 56.5),
    "drawlib v0.3.10 — 単一パッケージに全機能を標準同梱 (Python 3.11–3.14)",
    style=Styles.WhiteBold.patch(text_size=11.5, halign="left"),
)

stack = KpiCards(
    style=Styles.White.patch(shape_r=1.8),
    metric_style=Styles.DarkBold.patch(text_size=13.0),
    text_style=Styles.DarkBold.patch(text_size=11.2),
    description_style=Styles.Dark.patch(text_size=10.0),
    accent_style=Styles.Neutral,
    icon_style=Styles.PrimaryBold,
    accent_position="left_pill",
    metric_layout="left_column",
    metric_width_ratio=0.22,
    spacing=3.5,
)
stack.add(
    "Core",
    "純粋 Python 宣言的 API",
    "基本図形・18種 SmartArts・10種チャート・\n6種ダイアグラム・5種グラフソルバー",
    icon=phosphor.code,
    style=Styles.PrimaryNeutral.patch(shape_r=1.8),
)
stack.add(
    "Pillow",
    "ラスター画像 & アニメ基盤",
    "高精細 PNG/WebP 生成・Dimage 変換・\nAPNG / WebP / GIF フレーム合成",
    icon=phosphor.images,
    style=Styles.Neutral.patch(shape_r=1.8),
)
stack.add(
    "Cache",
    "Google/CJK フォント & アイコン",
    "Noto CJK フォント・34種アイコン自動取得\n& SQLite 差分キャッシュ (.drawlib)",
    icon=phosphor.database,
    style=Styles.Neutral.patch(shape_r=1.8),
)
stack.add(
    "Export",
    "Chromium & Office 出力器",
    "Playwright Chromium 自動取得 (PDF)\n+ python-docx / python-pptx 標準搭載",
    icon=phosphor.file_pdf,
    style=Styles.SecondaryNeutral.patch(shape_r=1.8),
)
stack.draw((6.0, 5.5), width=136.0, height=43.0, columns=2)

save()
```

`drawlib` をインストールすると、以下の 4 つのランタイム基盤が追加設定なしで連携して動作します。

- **Pillow ラスター描画・アニメーション基盤（`pillow`）**: ベクター描画コアと連携し、高解像度な `PNG` / `WebP` 画像出力、`Dimage` によるトリミング・合成処理、およびマルチフレームのアニメーション生成（`APNG`・アニメーション `WebP`・`GIF`）を担います。
- **Playwright ヘッドレス Chromium（`playwright`）**: 高精細なベクター `PDF`（`drawlib build pdf`）および `16:9` スライド出力（`drawlib build pptx`）のために標準依存として組み込まれています。初回の PDF / PPTX ビルド時に `chromium-headless-shell` が自動ダウンロードされるため手動セットアップは不要です。
- **Microsoft Office ネイティブ出力器（`python-docx` / `python-pptx`）**: 技術文書プロジェクト（`doc`）から編集可能な Word 文書（`.docx`）、プレゼンプロジェクト（`slide`）から編集可能な PowerPoint（`.pptx`）を直接出力します。
- **Google / CJK フォント・アイコン自動取得と SQLite キャッシュ**: OS 固有フォントに依存せず **Noto Sans CJK** 日本語フォントや Google Fonts、全 34 種のアイコンスイートを初回利用時に自動キャッシュして文字化け（豆腐化）を防止し、さらに `.drawlib/cache.db` が変更のない図表ブロックの再描画を自動的にスキップします。

オフライン環境や CI ランナー、および共有ライブラリを含まない最小構成の Linux コンテナ（`python:3.12-slim` 等）では、以下のコマンドで事前取得を行えます。

```bash
# ローカルのフォント・アイコン・地図・ブラウザのキャッシュ状態を確認
uv run drawlib cache list

# 日本語/欧文フォント・34種アイコン・地図・ヘッドレス Chromium を一括事前取得
uv run drawlib cache download --all

# PDF / PPTX ビルド用のヘッドレス Chromium のみを事前取得
uv run drawlib cache download --browser

# 最小 Linux コンテナ等で OS 共有ライブラリ (libnss3, libgbm1 等) が不足している場合
uv run playwright install-deps chromium
```

---

## 2.3 クイックテスト：最初のプロジェクト作成

Drawlib では裸の `.py` スクリプトを手作業で作るのではなく、必ず `drawlib init project` でプロジェクト雛形を生成してから執筆を始めます。これにより `drawlib.toml`・`styles.py`・`utils.py`・`_assets/`・各種 `build*.sh` が一括で構成されます。

```bash
# 1. CLI バージョンの確認
uv run drawlib --version

# 2. 日英バイリンガル (en,ja) かつ Google テーマの技術文書プロジェクトを初期化
uv run drawlib init project doc my_docs -l en,ja -s google

# 3. HTML・ベクター PDF・GitHub Markdown・単体画像を一括ビルド
./my_docs_src/build.sh
```

`drawlib init project doc my_docs -l en,ja -s google` を実行すると、`my_docs_src/` 配下に `drawlib.toml`（`[project]` と `[i18n]` 設定）・`styles.py`（`GoogleStyles`）・`ja/styles.py`（`FontJapanese` オーバーライド）・`utils.py`・`_assets/`・`en/` と `ja/` の初期章ファイル、そして用途別のビルドスクリプト（`build.sh`・`build_html.sh`・`build_pdf.sh`・`build_docx.sh`・`serve.sh`）が即座に生成されます。
