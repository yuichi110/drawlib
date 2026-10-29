# MS Office 出力機能（Word / PowerPoint）実装計画書

- **作成日**: 2026-10-29
- **対象機能**:
  - **基盤整備 (Phase 0)**: `playwright` 標準依存化 ＋ Headless Chromium オンデマンド自動取得（PDF / PPTX 共通基盤）
  - **Phase 1**: `doc` プロジェクト向け MS Word (`.docx`) 出力機能 (`drawlib build docx`)
  - **Phase 2**: `slide` プロジェクト向け MS PowerPoint (`.pptx`) 出力機能 (`drawlib build pptx`)
- **位置づけ・基本方針**:
  - PDF 出力はほぼ全ユーザーが利用するため、`playwright>=1.49.0` をデフォルトの標準依存（`dependencies`）へ昇格させ、初回ビルド時に軽量な `chromium-headless-shell` を自動取得する仕組み（事前コマンド不要）に刷新する。
  - Word / PowerPoint 出力は HTML / PDF（メイン出力）に対する **オプション（おまけ）のエクスポート機能** として位置づける。
  - 本文・見出し・箇条書き・Markdown テーブル・コードブロック・スピーカーノート（`::: note`）は **Word / PowerPoint 上で編集可能なネイティブ要素** として出力する。
  - ```` ```drawlib ```` コードブロックで描画される図版は、閲覧者環境でのフォント・アイコン（Phosphor 等）の文字化けやパス崩れを確実に防ぐため、**高解像度 PNG 画像** として配置する。
  - 高速な起動時間（遅延ロード）を維持するため、Office 系ライブラリは `pyproject.toml` の `[project.optional-dependencies]` に分離し、既存の標準 `./build.sh` には強制組み込みしない（未導入環境でのビルド失敗を防ぐ）。

---

## 1. フェーズ全体構成

| フェーズ | 対象 | 主な変更・追加コマンド | 使用ライブラリ | 変換・動作アーキテクチャ | 難易度・リスク |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Phase 0: Playwright 標準化 & 自動取得基盤** | PDF / PPTX 共通基盤 (`exporter_pdf.py`, `cache.py`) | `drawlib cache download --browser`（`build pdf` 初回自動取得） | `playwright>=1.49.0`（標準 `dependencies` へ移行） | 初回ブラウザ未導入検知時に内部ドライバ経由で `--only-shell chromium` を自動取得（最小 Linux コンテナの共有ライブラリ不足時のみ手順案内） | 低 |
| **Phase 1: MS Word (`.docx`) 出力** | `doc` プロジェクト（および単一 `.md`） | `drawlib build docx` | `python-docx>=1.2.0` (`[docx]` / `[office]`) | `DrawlibBlockProcessor` (高解像度 PNG) + `markdown-it-py` トークン走査 + `pygments` → `python-docx`（ブラウザ不要） | 低 |
| **Phase 2: MS PowerPoint (`.pptx`) 出力** | `slide` プロジェクト | `drawlib build pptx` | `python-pptx>=1.0.2` (`[pptx]` / `[office]`) + 標準 `playwright` | `build_slide` (高解像度 PNG モード) → Headless Chromium `1920×1080` DOM 計測 → `python-pptx` (`0.5` 倍座標変換) | 中 |

---

## 2. 依存関係・Playwright 自動セットアップ設計 (`pyproject.toml`)

※ 実装時に新規依存を追加・変更する際は、事前にライセンス（`python-docx` / `python-pptx` は MIT、`playwright` は Apache-2.0）・脆弱性・Python 3.11〜3.13 互換性監査（`./dcli pypi deps` 等）を実施する。

```toml
dependencies = [
    "matplotlib>=3.8",
    "pydantic>=2.8",
    "pygments>=2.18",
    "markdown-it-py>=3.0",
    "jinja2>=3.1",
    "typer>=0.12.0",
    "rich>=13.0.0",
    "playwright>=1.49.0",
]

[project.optional-dependencies]
pdf = []  # 既存スクリプト・Dockerfile 向け後方互換エイリアス（空リスト）
docx = [
    "python-docx>=1.2.0",
]
pptx = [
    "python-pptx>=1.0.2",
]
office = [
    "python-docx>=1.2.0",
    "python-pptx>=1.0.2",
]
```

### 2.1. パッケージ構成と遅延ロード
- **`playwright` 標準依存化と互換維持**:
  - `uv add drawlib` だけで PDF 生成（`./build.sh`）が一発で通るように `playwright>=1.49.0` を標準 `dependencies` に入れる。既存の `pip install "drawlib[pdf]"` が警告を出さないよう `pdf = []` を互換エイリアスとして残す。
  - Word / PowerPoint の追加依存はそれぞれ `docx = ["python-docx>=1.2.0"]`、`pptx = ["python-pptx>=1.0.2"]`、一括導入用 `office` と非常にシンプルな 1 対 1 構成になる（`[dependency-groups] dev` にも両者を追加）。
- **遅延ロード（Lazy Import）の徹底**:
  - 標準依存に入った `playwright` も含め、`playwright` / `docx` / `pptx` はすべてエクスポータ関数内部でのみ遅延 import し、`import drawlib` や通常の画像・HTML ビルド時のオーバーヘッドを **0ms** に保つ（`tests/drawlib/test_lazy_imports.py` で検証）。

### 2.2. Headless Chromium オンデマンド自動取得 (`_builder/_common/browser.py` 新設)
ユーザーに手動で `uv run playwright install chromium` コマンドを叩かせる手間をなくし、フォント・アイコンキャッシュ（`l3_external`）と同じオンデマンド体験に統一する：

1. **通常起動（オーバーヘッドゼロ）**:
   - まずそのまま `p.chromium.launch(headless=True, ...)` を試行する（導入済み環境では事前チェックコスト 0ms）。
2. **初回オンデマンド自動取得（`--only-shell` 最適化）**:
   - 未導入エラー（`"Executable doesn't exist"`）を検知した場合、`playwright._impl._driver` の `compute_driver_executable()` / `get_driver_env()` を用いてパッケージ同梱ドライバを直接呼び出し（外部の `uv` / シェル非依存、`shell=False`）、ファイルロック下で **`install --only-shell chromium`**（軽量な `chromium-headless-shell` のみ）を自動ダウンロードしてそのまま起動をリトライする。
3. **CI / 最小構成 Linux コンテナ向けの適切なエラー案内とドキュメント**:
   - macOS / Windows / デスクトップ Linux では管理者権限なしで 100% 自動完結する。
   - CI パイプライン等の最小 Linux コンテナ（`python:3.12-slim` 等）で OS 共有ライブラリ（`libnss3`, `libgbm1` 等）が不足して起動エラーになった場合は、`sudo`/`apt` を勝手に実行せず、パワーユーザー向けに `playwright install --with-deps chromium`（または `playwright install-deps chromium`）の実行手順を明示した分かりやすいエラーメッセージを表示する。あわせて `installation.md` や CLI ドキュメントに CI / コンテナ環境向けのセットアップ手順を明記する。
4. **`drawlib cache` コマンド連携**:
   - オフライン環境や Docker イメージビルド時の事前キャッシュ用に、`drawlib cache download --browser`（および `--all` への統合）を追加する。

---

## 3. Phase 1 詳細仕様: `doc` → MS Word (`.docx`)

### 3.1. モジュール構成
- `src/drawlib/_builder/doc_builder/compiler/docx.py`
  - 公開ビルダ関数 `build_docx()`（入力パス検証、出力ファイルパス解決、`styles.py` / `utils.py` 解決、チャプター走査呼び出し）。
- `src/drawlib/_builder/doc_builder/exporter_docx.py`（複雑度 `C901` を抑えるため必要に応じて内部ヘルパー分割）
  - `markdown-it-py` AST（トークン列）から `python-docx` の `Document` オブジェクトを構築するエクスポータ。
- `src/drawlib/_builder/doc_builder/__init__.py` & `src/drawlib/_cli/commands/build.py`
  - `build_docx` の公開と CLI サブコマンド `drawlib build docx` の追加。

### 3.2. CLI インターフェース (`drawlib build docx`)
既存の `drawlib build pdf` とオプション体系を揃える：

```bash
uv run drawlib build docx <INPUT> \
    [-o / --output <file.docx>] \
    [--page-break / --no-page-break] \
    [--generate-index / --no-generate-index] \
    [--title <str>] \
    [--dpi <int>] \
    [-s / --styles <styles.py>] \
    [-u / --utils <utils.py>] \
    [--no-cache] \
    [--timestamp]
```

- `<INPUT>` にはチャプター群を含む `doc_src/` ディレクトリ、または単一の `.md` ファイルを受け付ける。
- `slide_src/` ディレクトリが渡された場合（`_is_slide_project_dir()` で判定）は、`drawlib build pptx` の使用を促す明確なエラーメッセージを返す。
- `-o` 省略時は `<base_name>.docx`（例: `doc_src/` → 親ディレクトリに `doc.docx`）へ出力する。

### 3.3. 変換パイプラインとマッピング仕様
1. **図版の高解像度 PNG レンダリングとキャッシュ活用**:
   - `merger.py` の `expand_input_files()` で辞書順にチャプターを収集する。
   - `DrawlibBlockProcessor` を用いて ```` ```drawlib ```` コードブロックを高解像度 PNG（デフォルト `dpi=200`〜`240` 相当、`.drawlib/cache.db` キャッシュ対応）として一時ディレクトリに描画する。
   - コード可視性属性の扱い：
     - `code=hide` / `code=fold`（デフォルト含む）：Word には折りたたみ UI がないため、PDF 印刷時（`doc.css` の `@media print`）と同様にコードは出力せず、図版 PNG と `caption` のみを出力する。
     - `code=show`：シンタックスハイライト済みコード枠と図版 PNG の双方を出力する。
2. **A4 ページ設定とテーマ・CJK フォント制御**:
   - 用紙サイズ：A4（`210mm × 297mm`）、余白：上下 `18mm`・左右 `16mm`（`doc.css` と同一、本文有効幅 `178mm`）。
   - `style.css`（またはテーマプリセット `default` / `google` / `monochrome`）の見出し色・アクセント色を抽出し、`Heading 1`〜`Heading 4`、`Normal`、`Caption` スタイルに反映する。
   - **東アジアフォント (`w:eastAsia`) 対応**: `run.font.name` だけでは日本語が MS 明朝 / 游明朝にフォールバックするため、OpenXML の `w:rFonts` に対して欧文（`w:ascii`, `w:hAnsi`）と和文（`w:eastAsia`、例: `Noto Sans JP` / `Yu Gothic` / `Meiryo`）を明示設定するヘルパーを実装する。
3. **Markdown 要素 → Word ネイティブ要素マッピング**:
   - **見出し (`#`〜`######`)**: Word ネイティブの `Heading 1`〜`Heading 6`（Word のナビゲーションウィンドウおよびアウトライン表示に自動対応）。チャプター先頭に内部リンク用ブックマークを付与する。
   - **段落・インライン装飾**: 太字 (`**`)、斜体 (`*`)、取り消し線 (`~~`)、インラインコード (`` `code` ``：等幅フォント＋淡色背景シェーディング `w:shd`)、外部 URL ハイパーリンクおよびチャプター間内部リンク (`02_arch.md` → 章ブックマークへのジャンプ)。
   - **箇条書き・番号付きリスト**: ネスト階層に応じたインデントとリストスタイルを適用。
   - **引用・コールアウト (`> ...`)**: 左アクセント罫線 (`w:pBdr/w:left`) ＋ 背景シェーディング付きの引用段落として表現。
   - **GFM テーブル**: `doc.add_table()` で生成し、ヘッダー行の背景色・太字、セル余白、水平罫線、改ページ時のヘッダー行繰り返し (`w:tblHeader`)、行内改ページ防止 (`w:cantSplit`) を設定。
   - **コードブロック (```` ```python ```` 等)**: `highlight.py` の `resolve_lexer()` と `pygments.lex()` を再利用し、トークンごとの色付き Run を背景色付き 1×1 テーブル枠（または枠線付きシェーディング段落）内に出力する。
   - **画像・図版 (`![alt](...)` および `drawlib` 図版)**: 本文幅（最大 `178mm`）に収まるようアスペクト比を維持して中央配置し、`caption` 指定時は直下に `Caption` スタイル段落を配置（画像段落に `keep_with_next = True` を設定して画像とキャプションのページ分断を防止）。
   - **改ページ・目次 (`--page-break`, `--generate-index`)**:
     - `--page-break` 有効時（デフォルト `True`）はチャプター境界および `<div class="page-break"></div>` で改ページを挿入。
     - `--generate-index` 有効時は第1チャプター（`00_cover.md`）直後に目次ページ（各章タイトルへの内部リンク一覧）を挿入。
   - **決定論的メタデータ**: `--timestamp` 未指定時は `core_properties.created` / `modified` を固定日時（`SOURCE_DATE_EPOCH` 対応）に正規化する。

### 3.4. Phase 1 テスト・検証計画
- `tests/drawlib/doc_builder/test_docx.py`:
  - 見出し・装飾・ネストリスト・テーブル・コードハイライト・`drawlib` 図版埋め込み・チャプター結合・目次生成・日本語フォント `w:eastAsia` 設定・決定論的タイムスタンプの単体テスト（生成された `.docx` を `python-docx` で再読み込みして構造検証）。
- `tests/drawlib/cli/test_build.py` & `tests/drawlib/test_lazy_imports.py`:
  - CLI オプション動作検証、および遅延 import 検証。
- ドッグフーディング検証：
  - `docs/quickstart_src/` および `docs/drawlib-dogfooding_src/` から `.docx` を生成し、表示崩れがないことを確認。

---

## 4. Phase 2 詳細仕様: `slide` → MS PowerPoint (`.pptx`)

### 4.1. アーキテクチャ選定理由（HTML + Playwright DOM 計測方式）
- `drawlib` のスライド（`slide_src/*.md`）は `::: block xy=(x, y) width=W height=H` によりブロック外枠の座標を持つが、1つのブロック内部に見出し・箇条書き・Markdown テーブル・コードブロック・`<hr>` 区切り線・インライン CSS（`style="background: ...; border-radius: ..."`）が混在する。
- PowerPoint (`python-pptx`) では TextBox 内に Table や背景枠を入れ子にできず、すべての要素に個別の絶対座標 `(left, top, width, height)` が必要となるため、Markdown だけから和欧混植テキストの折り返し高さを推測すると要素重なりが発生する。
- そのため、`build_slide()` で生成した HTML を Headless Chromium（Playwright）で `1920×1080` 等倍描画し、ブラウザが計算した正確な `getBoundingClientRect()` と `getComputedStyle()` を抽出して `python-pptx` に `0.5` 倍スケールで配置する方式を採用する。

### 4.2. モジュール構成
- `src/drawlib/_slide/compiler_pptx.py`
  - 公開関数 `build_pptx()`（一時ディレクトリでの PNG モード HTML ビルド、DOM 抽出呼び出し、`.pptx` 書き出し統括）。
- `src/drawlib/_slide/_pptx_dom.py`
  - Playwright で `index.html` を開き、全 `<section class="slide">` の計算済みレイアウト・スタイル・スピーカーノートを構造化データ（dataclass）として抽出するモジュール。
- `src/drawlib/_slide/_pptx_writer.py`
  - 抽出した構造化データから `python-pptx` を用いて `16:9` スライド（背景・角丸カード・TextBox・Table・高解像度 PNG・Speaker Notes）を生成するモジュール。
- `src/drawlib/_slide/__init__.py` & `src/drawlib/_cli/commands/build.py`
  - `build_pptx` の公開と CLI サブコマンド `drawlib build pptx` の追加。

### 4.3. CLI インターフェース (`drawlib build pptx`)

```bash
uv run drawlib build pptx <DIR> \
    [-o / --output <file.pptx>] \
    [-t / --theme <theme>] \
    [--dpi <int>] \
    [--anim-frame <first|last>] \
    [-s / --styles <styles.py>] \
    [-u / --utils <utils.py>] \
    [--no-cache] \
    [--timestamp]
```

- `<DIR>` にはスライドソースディレクトリ（例: `slide_src/`）を受け付ける。
- `-o` 省略時は `<base_name>.pptx`（例: `slide_src/` → 親ディレクトリに `slide.pptx`）へ出力する。

### 4.4. 変換パイプラインとマッピング仕様
1. **高解像度 PNG モードでのスライド HTML 一時ビルド**:
   - 一時ディレクトリに出力先を設定し、既存の `build_slide(..., image_format="png")` を拡張（図版レンダリング時の高 DPI 指定、例: デフォルト `dpi=240`）して呼び出す。
   - これにより `draw_section_header()` や `draw_page_number()` を含むすべての ```` ```drawlib ```` 図版がフォント化けのない鮮明な透過/不透過 PNG として生成され、`.drawlib/cache.db` も活用される。
   - `Animation()` ブロック（APNG / WebP）が含まれる場合は、Pillow で指定フレーム（`--anim-frame last` または `first`）を静止 PNG として切り出して配置する。
2. **Playwright による `1920×1080` ステージ DOM 計測 (`_pptx_dom.py`)**:
   - Chromium を `viewport={"width": 1920, "height": 1080}` で起動し、`file://<tmp>/index.html` をロード後 `document.fonts.ready` を待機する。
   - `.presentation-stage` の `transform: none !important` を適用してスケーリングを解除し、各 `<section class="slide">` を順次アクティブ化して以下を計測する：
     - **スライド背景**: `.slide` の計算済み `backgroundColor`。
     - **コンテナ装飾 (`div.slide-block`, `.callout-card`, `<pre>`)**: 非透明な `backgroundColor`、`border`、`borderRadius` を持つ場合は背面シェイプ（矩形 / 角丸矩形）として記録。`z-index` と DOM 順でレイヤー順序を保持する。
     - **テキストブロック (`h1`〜`h6`, `p`, `ul`, `ol`, `blockquote`, `pre code`)**:
       - 各ブロック要素（または連続するテキスト要素群）の `(x, y, width, height)`、テキストアライメント、行間、リスト階層・番号有無。
       - インライン Run 単位（通常テキスト、`<strong>`, `<em>`, `<code>`, `<a>`、および Pygments の `<span class="...">`）の文字列・計算済み文字色・フォントサイズ・太字・斜体・フォントファミリ・リンク先 URL。
     - **区切り線 (`<hr>`)**: `(x, y, width, height)` と背景色。
     - **テーブル (`<table>`)**: テーブル全体の座標、各行の高さ、各列の幅、各セル (`<th>`/`<td>`) の背景色・罫線・パディング・セル内テキスト Run。
     - **画像・図版 (`<img>`, `<canvas>`)**: `object-fit: contain` 適用後の実際の描画領域（自然サイズ比率と要素矩形からレターボックスを除いた正確な矩形）と画像ファイルパス。
     - **スピーカーノート (`<aside class="slide-notes">`)**: 段落・箇条書き構造を保ったプレーンテキスト。
3. **`python-pptx` への `0.5` 倍マッピングとレイアウト崩れ対策 (`_pptx_writer.py`)**:
   - **座標系変換**:
     - スライドサイズを標準ワイド画面 **`13.333 inch × 7.5 inch` (`960 pt × 540 pt`)** に設定。
     - すべてのピクセル値 `v_px`（座標・幅・高さ・フォントサイズ・角丸半径・線幅）を **`Pt(v_px * 0.5)`** に変換する（`1920×1080 px` と `960×540 pt` が完全な `2:1` 対応となる）。
   - **フォント置換による折り返し溢れ防止**:
     - 閲覧者の PC に Web フォント（`Google Sans`, `Inter` 等）が無い場合の代替フォント膨張を吸収するため、TextBox の内部マージンをすべて `0` に設定したうえで `word_wrap = True` とし、スライド右端を超えない範囲で TextBox 幅に `+3%` 程度の安全バッファを持たせる。
     - Phase 1 と同様、Run の XML に東アジアフォント属性 (`a:ea`) を設定して日本語フォント崩れを防ぐ。
   - **半透明色 (`rgba`) 対応**:
     - CSS の `rgba(r, g, b, a)`（例: フローティングコールアウトカードの半透明スレート背景）は、基本 RGB 色に加えて DrawingML の `<a:alpha>` 要素を設定して透過度を再現する。
   - **スピーカーノート出力**:
     - `slide.notes_slide.notes_text_frame` に `::: note` の内容を格納し、PowerPoint の発表者ツールでそのまま利用可能にする。

### 4.5. Phase 2 テスト・検証計画
- `tests/drawlib/slide/test_pptx.py`:
  - `::: block` 座標変換、`z_index` 重ね順、見出し・箇条書き・インライン装飾、Markdown テーブル、コードブロック、インライン `style="..."` カード、図版 PNG 配置、`Animation()` 静止フレーム抽出、`::: note` スピーカーノート格納のテスト。
- ドッグフーディング検証：
  - `docs/slide_about_drawlib_src/`（全 60+ スライド）および `docs/slide_ddos_incident_response_src/` を実際に `.pptx` へビルドし、テキスト重なり・画像アスペクト比崩れ・文字化けがないことを確認。

---

## 5. ドキュメント・AI ルール更新・品質基準

Phase 1・Phase 2 の実装にあわせて以下を更新・検証する：

1. **テンプレート・スクリプト方針**:
   - オプション機能であるため、既存の `init doc` / `init slide` が生成する標準 `build.sh` は変更しない（`drawlib[office]` 未インストール環境でも `./build.sh` がそのまま成功することを保証する）。
   - `src/drawlib/_rules/cli.md`, `project_doc.md`, `project_slide.md`、および公式ドキュメント（`docs/docs_src/01_getting_started/installation.md`, `09_doc_builder_and_cli/`）にオプションの MS Office エクスポート手順（`drawlib[docx]`, `drawlib[pptx]`, `drawlib[office]`）を追記する。
2. **完了チェックリスト**:
   - `./dcli code-check all`（Ruff lint/format、Ty 型チェック、Docstring チェック）がエラーゼロでパスすること。
   - `./dcli test all`（新規単体テストおよび `test_lazy_imports.py` を含む全テスト）がパスすること。
   - `./dcli docs build --all` および `./dcli docs serve site --check` がエラー・リンク切れゼロで完了すること。
