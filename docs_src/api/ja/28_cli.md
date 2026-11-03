# CLI リファレンス (drawlib)

`drawlib` コマンドラインインターフェース（CLI）は、多言語対応ドキュメントサイト・API リファレンス・A4 PDF・MS Word（`.docx`）・16:9 HTML/PowerPoint（`.pptx`）スライドデッキ・単体 Python イラストレーションのコンパイルに加え、プロジェクトスキャフォールド、AI コーディングエージェント向けルール生成、プリセットカタログ表示、ローカルアセットキャッシュ管理を提供します。各サブコマンドは [`drawlib.tools`](27_tools.md) で公開されている Python API 関数と 1 対 1 で対応しています。

```drawlib align=center code=fold file=28_cli_hero.png caption="Drawlib CLI のサブコマンド階層と基本オーサリングワークフロー"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.shapes import rectangle
from drawlib.smartarts import ChevronProcess, Table
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=134, height=66)

rectangle(
    (67, 33),
    width=124,
    height=56,
    style=Styles.Neutral.patch(shape_fill_color=Colors.Transparent, line_style="dashed", shape_r=2.5),
)
phosphor.terminal_window((16.5, 57.0), width=4.4, style=Styles.PrimaryBold)
text(
    (67.0, 57.0),
    "drawlib CLI · Subcommand Groups & Authoring Workflow",
    style=Styles.DarkBold.patch(text_size=11.5),
)
phosphor.rocket_launch((117.5, 57.0), width=4.4, style=Styles.SecondaryBold)

workflow = ChevronProcess(
    style=Styles.Neutral,
    text_style=Styles.DarkBold.patch(text_size=10.5),
    description_style=Styles.Dark.patch(text_size=10.0),
    corner_angle=60.0,
    spacing=1.8,
    flat_left_end=True,
)
workflow.add("1. init", description="project / agent")
workflow.add("2. show", description="grid review (-g)", style=Styles.PrimaryNeutral)
workflow.add(
    "3. build",
    description="html / pdf / pptx",
    style=Styles.PrimaryFlat,
    text_style=Styles.WhiteBold.patch(text_size=10.5),
    description_style=Styles.White.patch(text_size=10.0),
)
workflow.add("4. serve", description="preview & --check", style=Styles.SecondaryNeutral)
workflow.draw(xy=(9.0, 39.5), width=116.0, height=13.5)

summary = Table(
    cell_style=Styles.Neutral.patch(shape_fill_color=Colors.White),
    text_style=Styles.Dark.patch(text_size=10.0),
    header_cell_style=Styles.PrimaryNeutral,
    header_text_style=Styles.PrimaryBold.patch(text_size=10.5),
    border_style=Styles.Neutral.patch(line_width=1.0),
    has_header=True,
)
summary.draw_flexible(
    xy=(9.0, 36.5),
    column_widths=[34.0, 40.0, 42.0],
    row_heights=[7.0, 7.0, 7.0, 7.0],
    data=[
        ["Command Group", "Key Subcommands", "Primary Deliverable"],
        ["build / show / serve", "html, pdf, docx, slide, pptx", "Sites, PDFs, Decks & Live Preview"],
        ["init / rules", "project (5 types), agent, show", "Project Scaffolds & Agent Manuals"],
        ["styles / colors / css / cache", "list, show, download, clear", "Design Catalogs, Themes & Assets"],
    ],
    align="top_left",
)

save()
```

---

## `cmd` drawlib

Drawlib CLI のルートエントリポイントです（`drawlib`、`uv run drawlib`、`uvx drawlib`、または `python -m drawlib` で実行）。グローバルなログ制御フラグおよびバージョン表示フラグはサブコマンド名の前に指定します。

```bash
drawlib [OPTIONS] COMMAND [ARGS]...

# インストール済みバージョンやトップレベルコマンド一覧の確認
uv run drawlib --version
uv run drawlib --help

# 詳細ログや開発者向けトレースバックを有効にしてサブコマンドを実行
uv run drawlib --verbose build html docs_src
uv run drawlib --developer show docs_src/en/index.md 1 -g -o preview.png
```

| オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `-v, --version` | `bool` | `False` | `drawlib version <X.Y.Z>` を出力して即座に終了します。 |
| `--quiet` | `bool` | `False` | エラーメッセージのみを出力する静音モードを有効化します。`--verbose`・`--debug`・`--developer` とは併用できません（併用時は終了コード `2`）。 |
| `--verbose` | `bool` | `False` | ビルドやレンダリング各段階の詳細な診断ログを出力します。 |
| `--debug` | `bool` | `False` | `--verbose` のエイリアスとして詳細診断ログを有効化します。 |
| `--developer` | `bool` | `False` | 詳細ログを有効化し、内部デバッグ向けにユーザー向けトレースバック抑制を解除します。 |
| `-h, --help` | `flag` | — | ルートコマンドのヘルプ一覧を表示して終了します。 |

---

## `cmd` drawlib build

ドキュメントソースディレクトリ（`site`・`catalog`・`doc`・`slide`）のコンパイル、または単体 Python 描画スクリプト（`images`）の実行を行うコマンドグループです。サブコマンドなしで `drawlib build` を実行するとヘルプ一覧を表示します。

```bash
drawlib build COMMAND [ARGS]...
```

| サブコマンド | 生成される成果物 |
| :--- | :--- |
| [`drawlib build docx`](#drawlib-build-docx) | 高 DPI ラスタライズ図版を埋め込んだ編集可能な Microsoft Word（`.docx`）文書。 |
| [`drawlib build html`](#drawlib-build-html) | 複数ページまたは単一ページの静的 HTML ドキュメントサイト（`site`・`catalog`・`doc`）。 |
| [`drawlib build image`](#drawlib-build-image) | `.py` 描画スクリプトから生成される単体 `.png`・`.webp`・`.jpg`・`.pdf` 画像。 |
| [`drawlib build markdown`](#drawlib-build-markdown) | `drawlib` コードフェンスを画像リンクへ置換したレンダリング済み Markdown ファイル群。 |
| [`drawlib build pdf`](#drawlib-build-pdf) | Headless Chromium で組版される印刷対応ベクター PDF（`doc`・`.md`・`slide`）。 |
| [`drawlib build pptx`](#drawlib-build-pptx) | 編集可能な Microsoft PowerPoint（`.pptx`）ワイドスクリーン資料（`960×540 pt` 16:9）。 |
| [`drawlib build slide`](#drawlib-build-slide) | スピーカーノートとアニメーションを備えたインタラクティブ 16:9 HTML スライドデッキ。 |

---

## `cmd` drawlib build docx

Markdown チャプターディレクトリ（`doc` プロジェクト）または単一の `.md` ファイルを、編集可能な Microsoft Word（`.docx`）文書へコンパイルします。多言語 `[i18n]` プロジェクトでは、図版レンダリング結果を言語間で共有しつつ `<stem>_<lang>.docx` を出力します。

```bash
drawlib build docx [OPTIONS] INPUT

# doc プロジェクトを目次付き・240 DPI で Word 文書へコンパイル（drawlib.toml 等を自動検出）
uv run drawlib build docx doc_src -o doc.docx --generate-index --dpi 240
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `INPUT` | `str` *(必須)* | — | Markdown チャプターを格納したディレクトリ（`doc_src/`）または単一 `.md` ファイルパス。 |
| `-o, --output` | `str \| None` | `None` | 出力 `.docx` ファイルパス（多言語 `doc` プロジェクトではベースパスまたは出力先ディレクトリ）。省略時は `<base>.docx`。 |
| `--page-break / --no-page-break` | `bool` | `True` | 結合される各チャプター間に Word の改ページを挿入します。 |
| `--generate-index / --no-generate-index` | `bool` | `False` | 目次（Table of Contents）を自動生成し、第 1 章と第 2 章の間に挿入します。 |
| `--title` | `str \| None` | `None` | Word コアメタデータに設定する文書タイトルを上書きします。 |
| `--dpi` | `int` | `200` | 埋め込み `drawlib` 図版のラスタライズ解像度（DPI）。 |
| `-s, --styles` | `str \| None` | `None` | カスタム `styles.py` のパス（`INPUT` 内に存在する場合は自動検出）。 |
| `-u, --utils` | `str \| None` | `None` | カスタム `utils.py` のパス（`INPUT` 内に存在する場合は自動検出）。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュ（`.drawlib/cache.db`）の読み書きを無効化します。 |
| `--timestamp` | `bool` | `False` | 決定論的ビルド用の固定日時ではなく、現在時刻を OpenXML メタデータに記録します。 |

---

## `cmd` drawlib build html

Markdown/HTML ドキュメントソースディレクトリ（`site`・`catalog`・`doc`）を、図版レンダリング・サイドバーナビゲーション・クライアントサイド検索インデックス・SEO メタデータ付きの静的 HTML サイトへコンパイルします。

> **注記 (v0.3.5 で導入予定):** `drawlib build html` における `catalog` カタログ／リファレンスプロジェクト（`project_type = "catalog"`、H1 カテゴリ＋H2 セマンティックバッジ構成）のコンパイル対応は *(v0.3.5 で導入予定)* です。

```bash
drawlib build html [OPTIONS] DIR

# docs_src/ を docs_html/ へコンパイル（WebP 図版フォーマット指定）
uv run drawlib build html docs_src -o docs_html -f webp
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `DIR` | `str` *(必須)* | — | Markdown/HTML ファイルおよび任意の `drawlib.toml` を含むソースディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 出力先 HTML ディレクトリパス（省略時は `<base>_html/` または `drawlib.toml` の `[build].html_dir`）。 |
| `-f, --format` | `'png' \| 'webp'` | `'png'` | 拡張子未指定の `drawlib` コードブロックに適用するデフォルト画像フォーマット。 |
| `-s, --styles` | `str \| None` | `None` | 各 `drawlib` ブロック実行前に読み込む `styles.py` のパス。 |
| `-u, --utils` | `str \| None` | `None` | 各 `drawlib` ブロック実行前に読み込む `utils.py` のパス。 |
| `--no-cache` | `bool` | `False` | `.drawlib/cache.db` の読み書きをバイパスします。 |

---

## `cmd` drawlib build image

単体の Python 描画スクリプト（`.py`）、またはディレクトリ内のすべての描画スクリプト（`images` プロジェクト）を再帰的に実行して画像を生成します。ディレクトリスキャン時、`styles.py`・`utils.py` および `_` で始まるヘルパーファイルは自動的にスキップされます。

```bash
drawlib build image [OPTIONS] INPUT

# images_src/ 全体を描画し、レビュー用の *_grid.png も同時出力
uv run drawlib build image images_src -o images -g

# 単一スクリプトをベクター PDF として出力
uv run drawlib build image images_src/architecture.py -o out/architecture.pdf
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `INPUT` | `str` *(必須)* | — | 対象の Python 描画スクリプト（`.py`）またはスクリプト格納ディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 出力画像ファイルパス（単一 `.py` 指定時）または出力ディレクトリパス。 |
| `-f, --format` | `'png' \| 'webp' \| 'jpg' \| 'pdf' \| None` | `None` | スクリプト内の `save()` で指定された出力フォーマットを一括上書きします。 |
| `-s, --styles` | `str \| None` | `None` | 各描画スクリプト実行前に読み込む共通 `styles.py` のパス。 |
| `-u, --utils` | `str \| None` | `None` | 各描画スクリプト実行前に読み込む共通 `utils.py` のパス。 |
| `-g, --grid` | `bool` | `False` | 座標グリッドを重ねた確認用画像 `*_grid.<ext>` を併せて保存します。 |
| `--disable-auto-clear` | `bool` | `False` | 連続するスクリプト実行間の自動 `clear()` 呼び出しを無効化します。 |
| `--enable-auto-initialize` | `bool` | `False` | 各スクリプト実行前にグローバル `config()` 設定を初期状態へリセットします。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |

---

## `cmd` drawlib build markdown

`drawlib` コードフェンスを含む Markdown ディレクトリをコンパイルし、生成された図版ファイル群と標準画像リンクに置換済みの Markdown ファイル群を出力します（GitHub/GitLab リポジトリや外部静的サイトジェネレーター連携に最適）。

```bash
drawlib build markdown [OPTIONS] DIR

uv run drawlib build markdown doc_src -o doc_markdown -f png
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `DIR` | `str` *(必須)* | — | Markdown（`.md`）ソースファイルを格納したディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 出力先 Markdown ディレクトリパス（省略時は `<base>_markdown/`）。 |
| `-f, --format` | `'png' \| 'webp'` | `'png'` | `drawlib` ブロックのデフォルト出力画像フォーマット。 |
| `-s, --styles` | `str \| None` | `None` | Python `styles.py` スクリプトのパス。 |
| `-u, --utils` | `str \| None` | `None` | Python `utils.py` スクリプトのパス。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |

---

## `cmd` drawlib build pdf

Markdown チャプターディレクトリ（`doc` プロジェクト）、単一 Markdown ファイル、または 16:9 スライドディレクトリ（`slide` プロジェクト）を Playwright Headless Chromium で組版し、印刷対応のベクター PDF を生成します。`drawlib.toml` で `[project].type = "slide"` が検出された場合は自動的に 16:9 横向きスライド PDF モードで出力します。

```bash
drawlib build pdf [OPTIONS] INPUT

# 自動目次付きの A4 技術仕様書 PDF をビルド
uv run drawlib build pdf doc_src -o specification.pdf --generate-index

# slide プロジェクトから 16:9 配布資料 PDF をビルド
uv run drawlib build pdf slide_src -o presentation.pdf
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `INPUT` | `str` *(必須)* | — | Markdown チャプターディレクトリ、単一 `.md` ファイル、または `slide` プロジェクトディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 出力 PDF ファイルパス（多言語 `doc` / `slide` プロジェクトではベースパスまたはディレクトリ）。 |
| `--page-break / --no-page-break` | `bool` | `True` | 結合される Markdown チャプター間に CSS 改ページを挿入します（`doc` モード）。 |
| `--generate-index / --no-generate-index` | `bool` | `False` | 目次を生成して第 1 ドキュメントと第 2 ドキュメントの間に挿入します（`doc` モード）。 |
| `--title` | `str \| None` | `None` | PDF メタデータに埋め込む文書タイトルを上書きします。 |
| `-s, --styles` | `str \| None` | `None` | Python `styles.py` スクリプトのパス。 |
| `-u, --utils` | `str \| None` | `None` | Python `utils.py` スクリプトのパス。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |
| `--timestamp` | `bool` | `False` | PDF メタデータ（`/CreationDate`・`/ModDate`）の正規化を行わず現在時刻を記録します。 |

---

## `cmd` drawlib build pptx

`slide` プロジェクトディレクトリを、Headless Chromium の `1920×1080` ステージ計測に基づいて `960×540 pt`（0.5 倍スケール）の編集可能なネイティブ Microsoft PowerPoint（`.pptx`）デッキへコンパイルします。複数フレームの `Animation` 図版は `'first'` または `'last'` フレームの静止画として埋め込まれます。

```bash
drawlib build pptx [OPTIONS] DIR

uv run drawlib build pptx slide_src -o deck.pptx --theme google --dpi 240 --anim-frame last
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `DIR` | `str` *(必須)* | — | `drawlib.toml` と Markdown スライドファイルを含む `slide` プロジェクトルート。 |
| `-o, --output` | `str \| None` | `None` | 出力 `.pptx` ファイルパス（または各言語 `<stem>_<lang>.pptx` を出力するベースパス）。 |
| `-t, --theme` | `str \| None` | `None` | スライド CSS テーマの上書き（`'google'`・`'default'`・`'google-dark'`・`'default-dark'`・`'monochrome'`）。 |
| `--title` | `str \| None` | `None` | PowerPoint メタデータに設定するプレゼンテーションタイトル。 |
| `--dpi` | `int` | `240` | 埋め込み `drawlib` 図版のラスタライズ解像度（DPI）。 |
| `--anim-frame` | `'first' \| 'last'` | `'last'` | `Animation` ブロックを静止画化する際に抽出するキーフレーム（先頭または最終フレーム）。 |
| `-s, --styles` | `str \| None` | `None` | Python `styles.py` スクリプトのパス。 |
| `-u, --utils` | `str \| None` | `None` | Python `utils.py` スクリプトのパス。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |
| `--timestamp` | `bool` | `False` | PowerPoint OpenXML メタデータに現在時刻のビルドタイムスタンプを含めます。 |

---

## `cmd` drawlib build slide

Markdown スライドファイル群（`---` スライド区切り、`::: block` 段組み、`::: note` スピーカーノート）から構成される `slide` プロジェクトを、キーボード操作・プレゼンタービュー・言語切替対応の 16:9 HTML スライドデッキへコンパイルします。

```bash
drawlib build slide [OPTIONS] DIR

uv run drawlib build slide slide_src -o slide_html --theme google -f svg
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `DIR` | `str` *(必須)* | — | `drawlib.toml` と `.md` スライドファイルを含む `slide` ソースディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | コンパイル済み HTML デッキの出力先ディレクトリ（省略時は `<base>_html/`）。 |
| `-t, --theme` | `str \| None` | `None` | スライド CSS テーマプリセット（`'google'`・`'default'`・`'google-dark'`・`'default-dark'`・`'monochrome'`）。 |
| `-f, --format` | `'svg' \| 'webp' \| 'png'` | `'svg'` | 図版のデフォルト画像形式（`'svg'` はプロジェクター拡大時もベクター品質を維持）。 |
| `-s, --styles` | `str \| None` | `None` | Python `styles.py` スクリプトのパス。 |
| `-u, --utils` | `str \| None` | `None` | Python `utils.py` スクリプトのパス。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |

---

## `cmd` drawlib cache

フォント・アイコンパック・GeoJSON 地図データ・Headless Chromium バイナリおよびワークスペース SQLite ビルドキャッシュの確認・事前ダウンロード・削除を行うコマンドグループです。

```bash
drawlib cache COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib cache clear`](#drawlib-cache-clear) | キャッシュ済みフォント／アイコン／地図データや `.drawlib/cache.db` を削除します。 |
| [`drawlib cache download`](#drawlib-cache-download) | オフラインビルド向けにフォント・アイコン・地図・Headless Chromium を事前取得します。 |
| [`drawlib cache list`](#drawlib-cache-list) | 外部フォント・アイコン・地図パッケージの一覧とローカルキャッシュ状態を表示します。 |

---

## `cmd` drawlib cache clear

ローカルにキャッシュされたフォント・アイコン・地図アーカイブ（`~/.drawlib/`）や、現在ワークスペースの SQLite 図版ビルドキャッシュ（`.drawlib/cache.db`）を削除します。`--all` も `--images` も指定しない場合は、ワークスペースの画像キャッシュを残したままグローバルのフォント／アイコン／地図キャッシュを削除します。

```bash
drawlib cache clear [OPTIONS]

# 外部ヘルパー編集後にワークスペースの SQLite 図版キャッシュのみをクリア
uv run drawlib cache clear --images

# グローバルのフォント／アイコン／地図キャッシュとワークスペース画像キャッシュをすべて削除
uv run drawlib cache clear --all
```

| オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `-a, --all` | `bool` | `False` | グローバルのフォント・アイコン・地図キャッシュおよびワークスペース `.drawlib/cache.db` をすべて削除します。 |
| `-i, --images` | `bool` | `False` | ワークスペースの SQLite ビルド画像キャッシュ（`.drawlib/cache.db`）のみを削除します。 |

---

## `cmd` drawlib cache download

外部フォント・アイコンスイート・GeoMap 地図データ・Playwright Headless Chromium をローカルキャッシュへ事前ダウンロードし、CI 環境・Docker イメージ・オフライン環境でネットワーク接続なしのビルドを可能にします。カテゴリ個別フラグ（`--fonts`・`--icons`・`--maps`・`--browser`）を指定した場合は該当カテゴリのみを取得し、省略時はすべて（`--all`）を取得します。

```bash
drawlib cache download [OPTIONS]

# フォント・アイコン・地図・Headless Chromium をすべて事前ダウンロード
uv run drawlib cache download --all

# フォントとアイコンパッケージのみをダウンロード（Chromium バイナリはスキップ）
uv run drawlib cache download --fonts --icons
```

| オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `--all` | `bool` | `True` | フォント・アイコン・地図・Headless Chromium の全アセットを一括取得します（個別フラグ未指定時の既定動作）。 |
| `--fonts` | `bool` | `False` | フォントパッケージのみをダウンロードします。 |
| `--icons` | `bool` | `False` | アイコンパッケージ（`phosphor`・`gcp`・`aws`・`azure`・各種ドメインパック）のみをダウンロードします。 |
| `--maps` | `bool` | `False` | `GeoMap` 用の地理境界データパッケージのみをダウンロードします。 |
| `--browser` | `bool` | `False` | Playwright Headless Chromium ブラウザバイナリのみをダウンロードします。 |

---

## `cmd` drawlib cache list

ダウンロード可能なすべてのフォント・アイコン・地図パッケージと、それぞれのローカルキャッシュ済み状態を Rich テーブル形式で一覧表示します。

```bash
uv run drawlib cache list
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib colors

Drawlib 組み込みのカラーパレット（`default`・`google`・`monochrome`・`css`）の一覧確認とビジュアルチャート出力を行うコマンドグループです。

```bash
drawlib colors COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib colors list`](#drawlib-colors-list) | 組み込みカラープリセットカタログの一覧テーブルを表示します。 |
| [`drawlib colors show`](#drawlib-colors-show) | 指定したカラープリセットの色見本チャートを表示または画像出力します。 |

---

## `cmd` drawlib colors list

利用可能な組み込みカラープリセットカタログ（`default`・`default1`〜`default6`・`google`・`monochrome`・`css`）とその説明を一覧表示します。

```bash
uv run drawlib colors list
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib colors show

指定したカラープリセットの全カラートークン名と RGB/16進カラーコードを描画した色見本チャートを表示（または `-o` でヘッドレス画像保存）します。

```bash
drawlib colors show [OPTIONS] PRESET

# Google パレットを HSV 色相順で PNG 画像へエクスポート
uv run drawlib colors show google --sort hsv -o google_colors.png
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `PRESET` | `str` *(必須)* | — | プリセット名：`'default'`（別名 `'def'`、`'default1'`〜`'default6'`）、`'google'`、`'monochrome'`（別名 `'mono'`）、`'css'`。 |
| `-o, --output` | `str \| None` | `None` | GUI ビューアを開かずに色見本チャートを指定ファイルパスへ保存します。 |
| `--sort` | `'hsv' \| 'name' \| 'raw'` | `'hsv'` | 並び順：知覚的な HSV 色相順（`'hsv'`）、名前順（`'name'`）、定義順（`'raw'`）。 |
| `-g, --grid` | `bool` | `False` | チャート上に Drawlib 座標グリッドを重ねて描画します。 |
| `--no-cache` | `bool` | `False` | カラーチャート画像キャッシュの読み書きをバイパスします。 |

---

## `cmd` drawlib css

HTML サイト・カタログ／リファレンスサイト・スライドデッキ・PDF 文書向けの組み込み CSS テーマプリセットを一覧・表示・エクスポートするコマンドグループです。

```bash
drawlib css COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib css list`](#drawlib-css-list) | HTML・Catalog・Slide・PDF 向けの組み込み CSS プリセット一覧を表示します。 |
| [`drawlib css show`](#drawlib-css-show) | 合成された CSS スタイルシートを標準出力へ表示、または `.css` ファイルへ保存します。 |

---

## `cmd` drawlib css list

組み込み CSS プリセット（`default`・`google`・`monochrome`・`default-dark`・`google-dark` など）を、全ターゲット横断のサマリー表または特定ターゲット別のテーブルとして一覧表示します。

> **注記 (v0.3.5 で導入予定):** `'catalog'` ターゲット指定（`drawlib css list catalog`）によるカタログ／リファレンス向け CSS 一覧表示は *(v0.3.5 で導入予定)* です。

```bash
drawlib css list [TARGET]

# HTML & PDF 対応状況のサマリーマトリクスを表示
uv run drawlib css list

# 特定のターゲット形式のプリセット一覧を表示
uv run drawlib css list slide
uv run drawlib css list catalog
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str \| None` | `None` | 絞り込み対象ターゲット：`'html'`・`'pdf'`・`'site'`・`'doc'`・`'slide'`・`'catalog'` *(v0.3.5 で導入予定)*・`'all'`。省略時はサマリー表を表示します。 |

---

## `cmd` drawlib css show

組み込み CSS プリセットの内容をターミナルへ表示（TTY 接続時はシンタックスハイライト付き）、または `-o / --output` 指定で言語別フォントスタックを反映した `.css` ファイルとして書き出します。

> **注記 (v0.3.5 で導入予定):** `'catalog'` ターゲットのスタイルシート表示・エクスポート（`drawlib css show catalog <PRESET>`）は *(v0.3.5 で導入予定)* です。

```bash
drawlib css show [OPTIONS] [TARGET] PRESET

# Google HTML テーマの CSS を標準出力へ表示
uv run drawlib css show google

# 日本語フォントスタック付きの PDF 用スタイルシートを書き出し
uv run drawlib css show pdf google -l ja -o doc_src/pdf_style.css --force

# カタログ／リファレンス用スタイルシートを書き出し（v0.3.5 で導入予定）
uv run drawlib css show catalog google -o catalog_src/style.css --force
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `[TARGET] PRESET` | `str` *(必須)* | — | `<PRESET>` 単体指定（`TARGET` は `'html'` 扱い）、または `<TARGET> <PRESET>` の 2 引数指定。`TARGET` は `'html'`・`'catalog'` *(v0.3.5 で導入予定)*・`'site'`・`'doc'`・`'slide'`・`'pdf'`。 |
| `PRESET` | `str \| None` | `None` | 第 1 引数に `TARGET` を指定した場合の CSS プリセット名（`'default'`・`'google'`・`'monochrome'`・`'default-dark'`・`'google-dark'` 等）。 |
| `-o, --output` | `str \| None` | `None` | 保存先 `.css` ファイルパス。省略時は標準出力へ CSS 全文を出力します。 |
| `-f, --force` | `bool` | `False` | 保存先ファイルが既に存在する場合に上書きします。 |
| `-l, --lang` | `str` | `'en'` | タイポグラフィ用フォントスタックを切り替える言語コード（`'en'`・`'ja'`・`'zh-cn'`・`'ko'`・`'th'` 等）。 |

---

## `cmd` drawlib init

Drawlib スタータープロジェクト（`doc`・`site`・`catalog`・`slide`・`images`）のスキャフォールド生成、および AI コーディングエージェント向けルール定義ファイルの生成を行うコマンドグループです。

```bash
drawlib init COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib init agent`](#drawlib-init-agent) | AI コーディングエージェント（`claude`・`cursor`・`antigravity`・`gemini` 等）向けルールを生成します。 |
| [`drawlib init agents`](#drawlib-init-agents) | `drawlib init agent` の複数形エイリアス。 |
| [`drawlib init project`](#drawlib-init-project) | 5 種類の Drawlib プロジェクト構成を初期化するサブグループ。 |

---

## `cmd` drawlib init agent

各種 AI コーディングエージェント向けの Drawlib 指示ファイル（`.agents/rules/`、`CLAUDE.md` / `.claude/rules/`、`.cursor/rules/`、`.github/copilot-instructions.md`、`GEMINI.md` など）を生成し、座標系・スタイル規約・3 段階マルチモーダルレビュー手順を自動適用できるようにします。

```bash
drawlib init agent [OPTIONS] [AGENTS...]

# 対応している AI コーディングエージェント一覧と出力先を表示
uv run drawlib init agent --list

# ワークスペース内の既存エージェント設定フォルダを自動検出して初期化
uv run drawlib init agent --detect

# Claude Code と Antigravity/Jetski 向けルールを上書き生成
uv run drawlib init agent claude antigravity --mode auto --force
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `AGENTS...` | `list[str] \| None` | `None` | 対象エージェント（複数指定可）：`'antigravity'`・`'claude'`・`'cursor'`・`'copilot'`・`'windsurf'`・`'cline'`・`'roo'`・`'codex'`・`'gemini'`・`'all'`・`'list'`。 |
| `-m, --mode` | `'auto' \| 'always'` | `'auto'` | フロントマター対応エージェントの発火モード：`'auto'`（オンデマンド）または `'always'`（常時読み込み）。 |
| `-g, --global` | `bool` | `False` | `--dir` ではなくユーザーホーム配下のグローバル設定ディレクトリへ書き込みます。 |
| `--detect` | `bool` | `False` | `--dir` 内の既存エージェント設定ディレクトリ／ファイルを検出し、該当ターゲットを一括初期化します。 |
| `--list` | `bool` | `False` | 対応エージェント名・出力パス・形式の一覧テーブルを表示して終了します。 |
| `-d, --dir` | `str` | `'.'` | 対象ワークスペースのルートディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 明示的な出力ファイルパス（単一エージェント指定時のみ有効）。 |
| `-f, --force` | `bool` | `False` | 既存ルールファイルの上書き、または共有ファイル内の Drawlib マーカーブロックを更新します。 |

---

## `cmd` drawlib init agents

[`drawlib init agent`](#drawlib-init-agent) の複数形エイリアスです。位置引数 `AGENTS...` およびすべてのオプションは `drawlib init agent` と同一です。

```bash
uv run drawlib init agents all --force
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `AGENTS...` | `list[str] \| None` | `None` | 対象エージェント名、`'all'`、または `'list'`（`drawlib init agent` と同一）。 |
| `-m, --mode` | `'auto' \| 'always'` | `'auto'` | ルール発火モード（`'auto'` または `'always'`）。 |
| `-g, --global` | `bool` | `False` | ユーザーホームのグローバル設定ディレクトリへ出力します。 |
| `--detect` | `bool` | `False` | `--dir` 内の既存エージェント設定を自動検出します。 |
| `--list` | `bool` | `False` | 対応エージェント一覧を表示して終了します。 |
| `-d, --dir` | `str` | `'.'` | 対象ワークスペースのルートディレクトリ。 |
| `-o, --output` | `str \| None` | `None` | 明示的な出力先ファイルパス（単一エージェント指定時のみ）。 |
| `-f, --force` | `bool` | `False` | 既存ルールファイルを上書きまたは更新します。 |

---

## `cmd` drawlib init project

`drawlib.toml`・`styles.py`・`utils.py`・`_assets/`・スターターコンテンツ・`build.sh` / `serve.sh` を一式備えた `<target>_src/` プロジェクトを生成するコマンドグループです。

```bash
drawlib init project COMMAND [ARGS]...
```

| サブコマンド | 既定フォルダ | プロジェクトアーキタイプ |
| :--- | :--- | :--- |
| [`drawlib init project catalog`](#drawlib-init-project-catalog) | `catalog_src/` | 図解付きカタログ & リファレンスサイト（API・CLI・スキーマ・サービス台帳・ランブック） *(v0.3.5 で導入予定)*。 |
| [`drawlib init project doc`](#drawlib-init-project-doc) | `doc_src/` | 章立て技術ドキュメント（`HTML`・`PDF`・`.docx`・`Markdown`）。 |
| [`drawlib init project image`](#drawlib-init-project-image) | `images_src/` | `drawlib init project images` の単数形エイリアス。 |
| [`drawlib init project images`](#drawlib-init-project-images) | `images_src/` | 単体 Python イラストレーションスクリプト集。 |
| [`drawlib init project list`](#drawlib-init-project-list) | — | 全 5 種類のプロジェクトタイプと生成成果物を一覧表示。 |
| [`drawlib init project site`](#drawlib-init-project-site) | `docs_src/` | `navbar.md` サイドバー付きのマルチページドキュメントサイト。 |
| [`drawlib init project slide`](#drawlib-init-project-slide) | `slide_src/` | 16:9 プレゼンテーションスライドデッキ（`HTML`・`PDF`・`.pptx`）。 |

---

## `cmd` drawlib init project catalog

H1 カテゴリと H2 セマンティックバッジ見出しで構成される図解付きカタログ & リファレンスサイト（`project_type = "catalog"`、API・CLI オプション・データスキーマ・サービス台帳・エラー辞書などに対応）を `<target>_src/` にスキャフォールド生成します（`drawlib.toml`・`styles.py`・`utils.py`・`style.css`・`template.html`・`build.sh`・`serve.sh` を作成） *(v0.3.5 で導入予定)*。

> **注記 (v0.3.5 で導入予定):** `drawlib init project catalog` スキャフォールドサブコマンドは *(v0.3.5 で導入予定)* です。

```bash
drawlib init project catalog [OPTIONS] [TARGET]

# 日英バイリンガルの API／サービスカタログを Google テーマで api_src/ に作成
uv run drawlib init project catalog api -l en,ja -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'catalog'` | カタログプロジェクトのベース名（`<target>_src/` を作成し、`<target>_html/` へ出力）。 |
| `-s, --style` | `str \| None` | `None` | 組み込みテーマプリセット（`'default'`・`'google'`・`'monochrome'`）またはカスタム CSS パス。 |
| `-l, --lang` | `str` | `'en'` | 単一言語コード（`'en'`・`'ja'` 等）またはカンマ区切りの多言語指定（`'en,ja'`）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib init project doc

A4 PDF・MS Word（`.docx`）・単一ページ HTML・Markdown へ一括出力できる章立て技術ドキュメントプロジェクト（`project_type = "doc"`）を `<target>_src/` に生成します（`drawlib.toml`・`styles.py`・`utils.py`・`build.sh`・`build_docx.sh`・`serve.sh` 付き）。

```bash
drawlib init project doc [OPTIONS] [TARGET]

uv run drawlib init project doc spec -l en,ja -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'doc'` | ドキュメントプロジェクトのベース名（`<target>_src/` を作成）。 |
| `-s, --style` | `str \| None` | `None` | スタイルプリセットテーマ（`'default'`・`'google'`・`'monochrome'`）またはカスタム CSS パス。 |
| `-l, --lang` | `str` | `'en'` | 単一言語コード（`'en'`・`'ja'`）またはカンマ区切りの多言語コード（`'en,ja'`）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib init project image

[`drawlib init project images`](#drawlib-init-project-images) の単数形エイリアスです。`<target>_src/` に単体 Python イラストレーションプロジェクトを生成します。

```bash
uv run drawlib init project image diagrams -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'images'` | イラストレーションプロジェクトのベース名（`<target>_src/` を作成）。 |
| `-s, --style` | `str \| None` | `None` | スタイルプリセットテーマ（`'default'`・`'google'`・`'monochrome'`）。 |
| `-l, --lang` | `str` | `'en'` | スターターテンプレートおよびフォント設定の言語コード（`'en'`・`'ja'`・`'zh-cn'`・`'ko'` 等）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib init project images

ドキュメントページを伴わず、純粋な `.png`・`.webp`・`.jpg`・`.pdf` 図版アセットを生成するための単体 Python イラストレーションプロジェクト（`project_type = "images"`、`drawlib.toml`・`styles.py`・`utils.py`・`_assets/`・`sample.py`・`build.sh`）を `<target>_src/` に作成します。

```bash
drawlib init project images [OPTIONS] [TARGET]

uv run drawlib init project images arch_diagrams -l ja -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'images'` | イラストレーションリポジトリおよびソースフォルダのベース名（`<target>_src/` を作成）。 |
| `-s, --style` | `str \| None` | `None` | スタイルプリセットテーマ（`'default'`・`'google'`・`'monochrome'`）またはカスタム CSS パス。 |
| `-l, --lang` | `str` | `'en'` | `styles.py` の CJK 等フォント設定に用いる単一言語コード（`'en'`・`'ja'`・`'zh-cn'`・`'ko'` 等）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib init project list

利用可能な Drawlib プロジェクトアーキタイプ（`doc`・`site`・`catalog`・`slide`・`images`）、既定のソースディレクトリ名、および出力フォーマット一覧を表示します。

```bash
uv run drawlib init project list
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib init project site

`navbar.md` によるサイドバーナビゲーションを備えたマルチページドキュメントサイト（`project_type = "site"`、`drawlib.toml`・`styles.py`・`utils.py`・`style.css`・`build.sh`・`serve.sh`）を `<target>_src/` に生成します。

```bash
drawlib init project site [OPTIONS] [TARGET]

uv run drawlib init project site docs -l en,ja -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'docs'` | ドキュメントサイトのベース名（`<target>_src/` を作成し、`<target>_html/` へ出力）。 |
| `-s, --style` | `str \| None` | `None` | スタイルプリセットテーマ（`'default'`・`'google'`・`'monochrome'`）またはカスタム CSS パス。 |
| `-l, --lang` | `str` | `'en'` | 単一言語コード（`'en'`・`'ja'`）またはカンマ区切りの多言語コード（`'en,ja'`）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib init project slide

インタラクティブ HTML スライド・ベクター PDF 配布資料・編集可能な MS PowerPoint（`.pptx`）へ出力できる 16:9 プレゼンテーションスライドプロジェクト（`project_type = "slide"`、`drawlib.toml`・`styles.py`・`utils.py`・`style.css`・`build.sh`・`build_pptx.sh`・`serve.sh`）を `<target>_src/` に生成します。

```bash
drawlib init project slide [OPTIONS] [TARGET]

uv run drawlib init project slide pitch -l en,ja -s google
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TARGET` | `str` | `'slide'` | プレゼンテーションデッキのベース名（`<target>_src/` を作成）。 |
| `-s, --style` | `str \| None` | `None` | スライドテーマ（`'default'`・`'default-dark'`・`'google'`・`'google-dark'`・`'monochrome'`）。 |
| `-l, --lang` | `str` | `'en'` | 単一言語コード（`'en'`・`'ja'`）またはカンマ区切りの多言語コード（`'en,ja'`）。 |
| `-f, --force` | `bool` | `False` | `<target>_src/` 内の既存ファイルを上書きします。 |

---

## `cmd` drawlib rules

Drawlib に組み込まれた AI エージェント向けマニュアル・モジュール別 API ガイド・座標サンプル図版（`~/.drawlib/cache/rules/`）の閲覧・事前ビルド・キャッシュ管理を行うコマンドグループです。

```bash
drawlib rules COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib rules build`](#drawlib-rules-build) | 指定トピックまたは全トピックのサンプル図版を事前レンダリングしてキャッシュします。 |
| [`drawlib rules clear`](#drawlib-rules-clear) | `~/.drawlib/cache/rules/` 配下のルール図版キャッシュを削除します。 |
| [`drawlib rules list`](#drawlib-rules-list) | 利用可能な全ルールトピック名・概要・図版キャッシュ状況を一覧表示します。 |
| [`drawlib rules show`](#drawlib-rules-show) | 指定トピックの Markdown マニュアル全文とサンプル画像パスを表示します。 |

---

## `cmd` drawlib rules build

指定したトピックまたは全トピック（`'all'`）の組み込みルール図版を `~/.drawlib/cache/rules/` に事前ビルド・キャッシュし、以降の `drawlib rules show` を高速化します。

```bash
drawlib rules build [OPTIONS] [TOPIC]

# 全ルールトピックの図版を一括で事前ビルド
uv run drawlib rules build all

# 特定トピックの図版を強制再ビルド
uv run drawlib rules build lib-smartarts-overview --force
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TOPIC` | `str \| None` | `None` | ビルド対象のルールトピック名（`'overview'`・`'style-guide'` 等）または `'all'`（省略時は `'all'`）。 |
| `-f, --force` | `bool` | `False` | キャッシュ済み画像が存在する場合でも強制的に再レンダリングして上書きします。 |

---

## `cmd` drawlib rules clear

キャッシュ済みのルール図版ディレクトリ（`~/.drawlib/cache/rules/`）を削除します。

```bash
uv run drawlib rules clear
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib rules list

組み込まれているすべてのルールマニュアルトピック（ワークフロー指針・プロジェクト構成・CLI リファレンス・`lib-*` モジュールマニュアル）を説明および図版キャッシュ状態とともに一覧表示します。

```bash
uv run drawlib rules list
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib rules show

指定したルールトピック（`overview`・`style-guide`・`review-guide`・`project-catalog`・`cli`・`lib-graph-overview` など）の Markdown マニュアルとローカル図版パスを表示します。

```bash
drawlib rules show [OPTIONS] TOPIC

uv run drawlib rules show overview
uv run drawlib rules show lib-diagrams-overview --raw
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `TOPIC` | `str` *(必須)* | — | 表示するルールトピック識別子（全一覧は `drawlib rules list` で確認可能）。 |
| `-r, --rebuild` | `bool` | `False` | キャッシュが存在する場合でもルール内サンプル図版を強制再生成します。 |
| `--raw` | `bool` | `False` | 図版のビルドやキャッシュ解決を行わず、生の Markdown ソースを即座に出力します。 |

---

## `cmd` drawlib serve

ビルド済み HTML ドキュメント（`docs_html/`・`catalog_html/`・`slide_html/`）を確認するためのローカル HTTP プレビューサーバーを起動します。また `--check` を指定すると、サーバーを起動せずにリンク切れ・欠損アセット検証のみをヘッドレス実行できます（CI/CD や Stage 3 レビューに最適）。

```bash
drawlib serve [OPTIONS] DIRECTORY

# ブラウザ自動起動なしでポート 8080 のプレビューサーバーを起動
uv run drawlib serve docs_html -p 8080 --no-browser

# リンク切れ・欠損アセット検証のみを実行して終了（不整合検出時は終了コード 1）
uv run drawlib serve docs_html --check
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `DIRECTORY` | `str` *(必須)* | — | 配信またはリンク検証対象のビルド済み HTML ディレクトリ。 |
| `-p, --port` | `int` | `8000` | ローカル HTTP サーバーが待ち受ける TCP ポート番号。 |
| `--no-browser` | `bool` | `False` | サーバー起動時に OS 既定の Web ブラウザを自動で開きません。 |
| `--skip-check` | `bool` | `False` | サーバー起動前のリンク切れ・アセット欠損スキャンをスキップします。 |
| `--check` | `bool` | `False` | `DIRECTORY` 内のリンク切れ・欠損アセットを検査し、サーバーを起動せず即座に終了します。 |

---

## `cmd` drawlib show

Markdown/HTML ファイル内の単一 `drawlib` コードブロック、または単体 `.py` スクリプトを実行し、GUI プレビューウィンドウに表示するか `-o / --output` で指定ファイルへヘッドレス保存します。`-g / --grid` と `-o` の組み合わせは Stage 2 マイクロジオメトリレビューの標準コマンドです。

```bash
drawlib show [OPTIONS] FILE [TARGET]

# ファイル名指定で対象ブロックに 10/5 単位の座標グリッドを重ねて画像出力
uv run drawlib show docs_src/en/architecture.md hero.png -s docs_src/styles.py -u docs_src/utils.py -g -o .drawlib/scratch/hero_grid.png

# 1 始まりのブロック番号で先頭の drawlib ブロックをグリッド付き出力
uv run drawlib show docs_src/en/architecture.md 1 -g -o .drawlib/scratch/block1_grid.png
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `FILE` | `str` *(必須)* | — | 対象の Markdown（`.md`）・HTML（`.html`）・Python 描画スクリプト（`.py`）のパス。 |
| `TARGET` | `str \| None` | `None` | 複数ブロックを含むファイルでの対象指定：1 始まりの番号（例：`1`）または `file=...` 名（例：`hero.png`）。 |
| `-o, --output` | `str \| None` | `None` | GUI ウィンドウを開かず、指定パスへレンダリング画像（または `.webp`/`.png` アニメーション）を保存します。 |
| `-g, --grid` | `bool` | `False` | ジオメトリ検査用に Drawlib 座標グリッド（`10` 単位主線／`5` 単位補助線）を重ねて描画します。 |
| `-s, --styles` | `str \| None` | `None` | 対象ブロック実行前に読み込む `styles.py` のパス。 |
| `-u, --utils` | `str \| None` | `None` | 対象ブロック実行前に読み込む `utils.py` のパス。 |
| `--no-cache` | `bool` | `False` | SQLite ビルド画像キャッシュの読み書きを無効化します。 |

---

## `cmd` drawlib styles

Drawlib のプリセット `Styles.*` デザインマトリクス（`default`・`monochrome`・`google`）の一覧表示およびビジュアル確認を行うコマンドグループです。

```bash
drawlib styles COMMAND [ARGS]...
```

| サブコマンド | 説明 |
| :--- | :--- |
| [`drawlib styles list`](#drawlib-styles-list) | 利用可能なすべての組み込みスタイルプリセット一覧を表示します。 |
| [`drawlib styles show`](#drawlib-styles-show) | 指定プリセットの `Styles.*` トークン見本マトリクスを表示または画像出力します。 |

---

## `cmd` drawlib styles list

利用可能な組み込みスタイルプリセットカタログ（`default`・`default1`〜`default6`・`monochrome`・`google`）を一覧表示します。

```bash
uv run drawlib styles list
```

位置引数およびコマンド固有オプションはありません（`-h, --help` のみ）。

---

## `cmd` drawlib styles show

シェイプ塗り・枠線・ライン・テキストの各 `Styles.*` トークンを一覧できるビジュアルスタイルマトリクスを表示または画像保存します（1 ページあたり 25 ベースカラー、または `-c / --color` で特定色相のみ抽出可能）。

```bash
drawlib styles show [OPTIONS] PRESET [PAGE]

# Google スタイルマトリクスの 1 ページ目を PNG にエクスポート
uv run drawlib styles show google 1 -o styles_google_p1.png

# 青系カラーのスタイルトークンのみを抽出して保存
uv run drawlib styles show google --color blue -o styles_google_blue.png
```

| 引数 / オプション | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `PRESET` | `str` *(必須)* | — | スタイルプリセット名：`'default'`（別名 `'def'`、`'default1'`〜`'default6'`）、`'monochrome'`（別名 `'mono'`）、`'google'`。 |
| `PAGE` | `int` | `1` | 1 始まりのページ番号（1 ページあたり `25` カラー行）。 |
| `-a, --all` | `bool` | `False` | 全ページを一括エクスポートします（例：`styles_google_1.png`、`styles_google_2.png`、...）。 |
| `-o, --output` | `str \| None` | `None` | GUI ビューアを開かずにマトリクス画像を指定パスへ保存します。 |
| `-c, --color` | `str \| None` | `None` | ベースカラー名または色相の部分一致で表示行を絞り込みます（例：`'blue'`・`'red'`・`'neutral'`）。 |
| `-g, --grid` | `bool` | `False` | スタイルマトリクス上に Drawlib 座標グリッドを重ねて描画します。 |
| `--no-cache` | `bool` | `False` | スタイルマトリクス画像キャッシュの読み書きをバイパスします。 |
