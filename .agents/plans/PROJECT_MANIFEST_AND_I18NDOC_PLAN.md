# `drawlib.toml` 統合プロジェクトマニフェスト & `doc` 多言語化（`i18ndoc`）設計・実装計画書

- **作成日**: 2026-11-01
- **対象スコープ**:
  - **Phase 1 (`drawlib.toml` 統合マニフェスト基盤)**: 暫定導入していた `i18n.toml` を廃止し、全4プロジェクト種別（`images`, `doc`, `site`, `slide`）共通の設定ファイル `drawlib.toml` を導入（`drawlib init` 自動生成・プロジェクト種別判定の厳密化・単一言語メタデータ活用）
  - **Phase 2 (`doc` プロジェクト多言語 `i18ndoc` 対応)**: リニアドキュメント（HTML / PDF / Word `.docx` / Markdown / Images）のマルチロケールビルド、目次見出し（TOC）の言語別ローカライズ、ロケール別 `styles.py` オーバーライド、言語切替スイッチャー UI、`drawlib init doc -l en,ja` スキャフォールド実装
  - **Phase 3 (公式 `docs/` 展開 & `drawlib-dogfooding` 日英集約)**: `docs/docs_src/i18n.toml` → `drawlib.toml` 移行、全 `docs/*_src/` への `drawlib.toml` 配置、および `docs/drawlib-dogfooding_src`（日本語）と `docs/drawlib-dogfooding-en_src`（英語）の単一多言語 `doc` プロジェクトへの統合
  - **Phase 4 (ルール・ドキュメント更新 & 総合検証)**: `src/drawlib/_rules/`・公式ドキュメント該当箇所の更新、全単体／結合テスト、全ターゲットビルドおよびブラウザ・PDF 視覚検証
- **基本方針**:
  - **外部依存追加ゼロ**: Python 3.11+ 標準ライブラリの `tomllib` で解析し、`pyproject.toml` への新規依存追加は行わない。
  - **既存プロジェクトとの 100% 後方互換**: `drawlib.toml` が存在しない既存のディレクトリや単一 `.md` 指定時は、従来のファイル構成ベースの自動判定（`navbar.md` や `slide.css` 等）へフォールバックしてそのまま動作させる。
  - **`i18n.toml` のクリーンな廃止**: `i18n.toml` はまだ PyPI 未リリースのため、レガシー互換分岐を残さず `drawlib.toml` の `[i18n]` セクションへ完全に一本化する。

---

## 1. フェーズ全体構成

| フェーズ | 対象領域 | 主な変更・追加内容 | 完了基準 | 難易度 |
| :--- | :--- | :--- | :--- | :---: |
| **Phase 1: `drawlib.toml` マニフェスト基盤** | `src/drawlib/_builder/`<br>`src/drawlib/_templates/`<br>`src/drawlib/_cli/commands/init.py` | ・`ProjectManifest` パーサ & バリデータ実装<br>・`i18n.toml` → `drawlib.toml` 全面置換<br>・全4種 `drawlib init` での `drawlib.toml` 生成<br>・`slide` / `site` / `doc` 判定のマニフェスト優先化 | `test_cli_init.py` / `test_site_i18n.py` 更新 & 新規マニフェスト単体テストパス | 中 |
| **Phase 2: `i18ndoc` コンパイラ & テンプレート実装** | `src/drawlib/_builder/doc_builder/`<br>`src/drawlib/_templates/langs/`<br>`src/drawlib/_templates/project/doc/` | ・`validate_i18n_project()`（`navbar.md` 不要モード）<br>・ロケール別 `<lang>/styles.py` 優先解決<br>・多言語 `doc` の HTML / MD / PDF / DOCX 一括出力<br>・TOC 見出し多言語化 & `doc` 用言語スイッチャー UI<br>・`drawlib init doc -l en,ja` スターター追加 | `test_doc_i18n.py`（HTML / PDF / DOCX / パリティ検証）パス、`./dcli code-check all` パス | 中〜高 |
| **Phase 3: 公式 `docs/` 移行 & `dogfooding` 集約** | `docs/*_src/`<br>`tools/dcli/docs/`<br>`README.md` | ・`docs_src/i18n.toml` → `drawlib.toml` 移行<br>・`drawlib-dogfooding_src` への日英統合（`en/`, `ja/`）と `drawlib-dogfooding-en_src` 廃止<br>・他6プロジェクトへの `drawlib.toml` 配置 & `dcli` 更新 | `./dcli docs build --all` 完走、リンク切れゼロ、PDF・HTML 生成確認 | 中 |
| **Phase 4: 組込みルール・ドキュメント更新 & 最終検証** | `src/drawlib/_rules/`<br>`docs/docs_src/{en,ja}/` | ・`project_overview.md`, `project_doc.md`, `project_site.md`, `cli.md` 等の `drawlib.toml` / `i18ndoc` 反映<br>・公式ドキュメント該当解説ページの更新 | `./dcli code-check all`、`./dcli test all`、ブラウザ・PDF Stage 3 視覚確認完了 | 低〜中 |

---

## 2. `drawlib.toml` マニフェスト仕様

### 2.1. ファイル名と配置場所
- 各プロジェクトのソースディレクトリ直下（`<target>_src/drawlib.toml`）に配置する。
- サブディレクトリ内のファイル（例: `docs_src/ja/05_charts/bar.md`）を `drawlib show` や個別 `drawlib build pdf` に渡した際も、親ディレクトリ探索（`_find_project_search_dirs` 等）で `drawlib.toml` のあるディレクトリをプロジェクトルートとして自動認識する。

### 2.2. スキーマ定義

#### パターンA：単一言語プロジェクト（フラット構成 `<target>_src/*`）
`drawlib init {images,doc,site,slide} [target] [-l <lang>] [-s <style>]` 実行時に生成される。

```toml
[project]
name = "quickstart"
type = "doc"                  # "images" | "doc" | "site" | "slide"
title = ""                    # 任意: 明示指定時は自動推論タイトルより優先（空文字または省略時は自動推論）
description = ""              # 任意: 人間・AI エージェント向けのプロジェクト概要メモ
lang = "ja"                   # プロジェクトの言語コード（正規化済み: "en", "ja", "zh-cn" 等）
style = "default"             # 初期スタイルテーマ ("default", "google", "monochrome" 等)
```

#### パターンB：多言語プロジェクト（サブディレクトリ構成 `<target>_src/<lang>/*`）
`drawlib init {doc,site} [target] -l en,ja [-s <style>]` 実行時に生成される（`type` は `"doc"` または `"site"`）。

```toml
[project]
name = "drawlib-dogfooding"
type = "doc"                  # "doc" または "site"
title = ""
description = "Drawlib Dogfooding Whitepaper"
style = "google"

[i18n]
default_lang = "en"
langs = ["en", "ja"]
```

### 2.3. バリデーション & 判定ルール
1. **`[i18n]` セクションの有無による構造切り替え**:
   - `[i18n]` が**存在する**場合 → マルチロケール構成（`<src>/<lang>/`）として扱い、機械的パリティ検証・共有 `images/` 出力・言語スイッチャーを有効化する（`[project].lang` が併記されていても `[i18n].default_lang` を優先）。
   - `[i18n]` が**存在しない**場合 → 単一言語フラット構成（`<src>/*`）として扱い、`[project].lang`（省略時 `"en"`）をロケール設定（目次タイトル・HTML `lang` 属性・フォント解決等）に利用する。
2. **プロジェクト種別（`type`）の優先解決**:
   - `drawlib.toml` に `project.type` がある場合はヒューリスティック推測を行わず、その種別を確定値として使用する（例: `type = "doc"` のディレクトリに誤って `slide` 用の CSS 断片が入っていても `slide` と誤認しない。逆に `build docx` に `type = "slide"` や `type = "site"` を渡した場合は明快なエラーメッセージを返す）。
   - `drawlib.toml` が存在しないディレクトリに対しては、従来通り `navbar.md` の有無（`site` vs `doc`）および `_is_slide_project_dir()` による自動判定を行う。

---

## 3. `doc` プロジェクト多言語化（`i18ndoc`）仕様

### 3.1. ソースディレクトリ構造（例: `docs/drawlib-dogfooding_src/`）

```text
drawlib-dogfooding_src/
├── drawlib.toml                  # type = "doc", [i18n] default_lang = "en", langs = ["en", "ja"]
├── README.md                     # プロジェクトビルド手順・構成ガイド
├── _assets/                      # [全言語共有] ロゴ・favicon・静的画像
├── styles.py                     # [デフォルト共有] 描画テーマ (GoogleStyles 欧文ベース)
├── utils.py                      # [全言語共有] 描画ヘルパー関数
├── style.css                     # [全言語共有] ベース CSS テーマ (Google doc テーマ)
├── template.html                 # [全言語共有] Jinja2 レイアウト（言語スイッチャー対応）
├── build.sh                      # HTML + PDF + Markdown + Images 一括ビルド
├── build_html.sh
├── build_pdf.sh
├── build_markdown.sh
├── build_image.sh
├── serve.sh
│
├── en/                           # 英語版チャプター群 (default_lang)
│   ├── 00_cover.md
│   ├── 01_ai_challenges.md
│   └── ... (〜 12_slide_presentation.md)
│
└── ja/                           # 日本語版チャプター群（en/ と骨格・図版整合を機械検証）
    ├── styles.py                 # [任意オーバーライド] 日本語図版用 FontJapanese パッチ適用スタイル
    ├── 00_cover.md
    ├── 01_ai_challenges.md
    └── ... (〜 12_slide_presentation.md)
```

### 3.2. ロケール別 `styles.py` / `utils.py` オーバーライド仕様（`site` / `doc` 共通）
- ホワイトペーパー等の `doc` プロジェクトでは、API リファレンスとは異なり「図の中のラベル自体も英語／日本語に翻訳したい（＝英語図は欧文フォント、日本語図は `FontJapanese` で描画したい）」ケースが多い。
- そのため、明示的な `--styles` / `--utils` CLI 引数がない場合、各ロケール `<lang>` のビルド時に **`<src>/<lang>/styles.py` が存在すればそれを優先し、存在しなければルートの `<src>/styles.py` を使用する**（`utils.py` も同様）。
  - 既存の `resolve_styles_and_utils(os.path.join(input_abs, lang))` が親ディレクトリ探索を備えているため、これをマルチロケールビルダ側でロケール単位に呼び出すだけで一貫して動作し、`BuildImageCache` の `config_hash` にも自動で反映される。
- 図ファイル名の規約は `site` と 100% 統一する：
  - **言語間で共通の図**: 同じ `file=fig_xxx.png` を指定（Python コードの 1文字単位の完全一致を強制し、1回だけ描画して共有）。
  - **図内テキストを翻訳した言語固有図**: `<lang>` 側で `file=fig_xxx_<lang>.png`（例: `file=fig_solution_comparison_ja.png`）を指定（独自 Python コードを許可）。

### 3.3. 機械的整合性検証（`validate_i18n_project`）
既存の `validate_i18n_site()` を `validate_i18n_project(input_dir, i18n_cfg, *, project_type="site" | "doc", default_format="png")` に汎用化する（後方互換エイリアスとして `validate_i18n_site` も維持）：
- **Check 1（ファイル集合一致）**: `en/` と `ja/` で章ファイル一覧（`00_cover.md`〜`12_*.md`）が完全一致すること（章の抜け・ファイル名ズレによる結合順序崩壊を防止）。
- **Check 2（`navbar.md` 一致）**: `project_type == "site"` のときのみ実行し、`project_type == "doc"` ではスキップする（誤って `doc` 側に `navbar.md` が置かれていた場合は警告または明示エラーとする）。
- **Check 3（章内骨格シーケンス一致）**: 各章の `H1..H3`・`MarkdownText`・`DrawlibBlock`・`CodeBlock` の順序が一致すること。
- **Check 4（描画コード完全一致 & `_<lang>.<ext>` 独自図規約）**: `site` と同一ルールで検証。

### 3.4. 各ビルドコマンドの出力構造仕様

`<base>` をプロジェクトベース名（例: `drawlib-dogfooding`）とする。

#### 1. HTML 出力 (`drawlib build html <src>/ -o <base>_html/`)
```text
drawlib-dogfooding_html/
├── index.html                    # default_lang (en) の全章マージ単一 HTML（ルート相対パス解決済み）
├── _assets/                      # 共有アセット
├── images/                       # 共有 & 言語別レンダリング画像（<chapter_stem>/<img_name>）
├── en/
│   ├── style.css                 # 英語フォント CSS
│   └── index.html                # 英語版マージ単一 HTML（右上に言語スイッチャー付き）
└── ja/
    ├── style.css                 # 日本語フォント (Noto Sans JP) CSS
    └── index.html                # 日本語版マージ単一 HTML（右上に言語スイッチャー付き）
```
- **UI**: `doc/template.html.template` および `doc` 用ベース CSS に、画面右上のコンパクトな `<details class="lang-dropdown">` + `<a href>` 言語スイッチャーを追加する。`@media print` では `display: none !important` とし、ブラウザ印刷や PDF 変換時には一切表示されないようにする。
- `drawlib serve <base>_html/ --check` でルート `index.html`・`en/index.html`・`ja/index.html` 間の言語切替リンク・章内アンカー・画像参照をすべて自動検証できる。

#### 2. PDF 出力 (`drawlib build pdf <src>/ [-o <base>.pdf] [--generate-index]`)
- マルチロケール `doc` ディレクトリが指定された場合、**全言語分の A4 ベクター PDF を順番に生成し、言語サフィックス `_{lang}` 付きで並列出力**する：
  - `-o` 省略時または `-o drawlib-dogfooding.pdf` 指定時：
    - `drawlib-dogfooding_en.pdf`
    - `drawlib-dogfooding_ja.pdf`
  - ディレクトリ `-o dist/` 指定時：
    - `dist/drawlib-dogfooding_en.pdf`
    - `dist/drawlib-dogfooding_ja.pdf`
- もし共通画像（同名 `file=`）が含まれる場合も、同一 `BuildImageCache` を介するため 2言語目での再レンダリングは発生しない。
- 各言語の PDF 生成時には、その言語に対応する Google Fonts / ローカルフォント CSS（`localize_css_for_language`）および言語別目次タイトル（`"Table of Contents"` / `"目次"`）を自動適用する。
- 1言語だけ個別に出力したい場合は `drawlib build pdf <src>/ja/ -o custom_ja.pdf` のようにサブディレクトリを指定すれば単一 PDF として出力できる。

#### 3. MS Word 出力 (`drawlib build docx <src>/ [-o <base>.docx] [--generate-index]`)
- PDF と完全に同じ命名規則で全言語分の `.docx` を並列出力する：
  - `drawlib-dogfooding_en.docx`
  - `drawlib-dogfooding_ja.docx`

#### 4. Markdown 出力 (`drawlib build markdown <src>/ -o <base>_markdown/`)
- `site` のマルチロケール Markdown 出力と同様に、`<base>_markdown/en/*.md`、`<base>_markdown/ja/*.md`、共有 `<base>_markdown/images/<chapter_stem>/...`、`_assets/` を出力する（`doc` には `index.md` 単体トップがないため、ルートには `README.md` または先頭章への案内のみ、あるいは `en/`・`ja/` ツリーをそのままクリーンに配置）。

#### 5. 画像抽出 (`drawlib build image <src>/ -o <base>_images/`)
- `image_builder.py` の既存マルチロケール抽出処理（パリティ検証後に `<base>_images/<chapter_stem>/<img_name>` へ集約出力）をそのまま `i18ndoc` でも利用し、ロケール別 `<lang>/styles.py` 解決のみ追加反映する。

### 3.5. 自動生成目次（TOC 見出し）の多言語ローカライズ
- 現在 `merger.py`（PDF 用）・`compiler/html.py`（HTML 用）・`exporter_docx.py`（Word 用）で `"Table of Contents"` がハードコードされている箇所を、`LanguageConfig.toc_title` から取得するよう統一する。
- 全16サポート言語のデフォルト値（例: `en`: `"Table of Contents"`, `ja`: `"目次"`, `zh-cn`: `"目录"`, `zh-tw`: `"目錄"`, `ko`: `"목차"`, `de`: `"Inhaltsverzeichnis"`, `fr`: `"Table des matières"`, `es`: `"Índice"` 等）を `src/drawlib/_templates/langs/` に定義する。
- これにより、多言語 `i18ndoc` だけでなく、単一言語の `drawlib init doc -l ja` プロジェクトでも `drawlib.toml` の `lang = "ja"` を読み取って自動的に `"目次"` が出力されるようになる。

---

## 4. 公式リポジトリ（`docs/`）への適用・集約計画

### 4.1. `docs/drawlib-dogfooding_src/` への日英ホワイトペーパー統合
1. **ファイル移行**:
   - `docs/drawlib-dogfooding-en_src/00_cover.md`〜`12_slide_presentation.md` を `docs/drawlib-dogfooding_src/en/` へ移動。
   - 既存の日本語版 `docs/drawlib-dogfooding_src/00_cover.md`〜`12_slide_presentation.md` を `docs/drawlib-dogfooding_src/ja/` へ移動。
2. **図版ファイル名とスタイルの整理**:
   - 日本語版全10図版は図内テキスト自体が日本語化されているため、`ja/*.md` 内の ```` ```drawlib ```` フェンスの `file=<stem>.png` を `file=<stem>_ja.png` に更新する。
   - ルートの `docs/drawlib-dogfooding_src/styles.py` は欧文 `GoogleStyles()` とし、`docs/drawlib-dogfooding_src/ja/styles.py` に `FontJapanese` パッチ版 `GoogleStyles()` を配置する。
3. **マニフェスト・テンプレート・スクリプト更新 & 旧ディレクトリ削除**:
   - `docs/drawlib-dogfooding_src/drawlib.toml`（`type = "doc"`, `style = "google"`, `[i18n]` `default_lang = "en"`, `langs = ["en", "ja"]`）を作成。
   - 言語スイッチャー対応版 `template.html` / `style.css` を適用。
   - `docs/drawlib-dogfooding-en_src/` および旧出力物（`docs/drawlib-dogfooding.pdf`, `docs/drawlib-dogfooding-en.pdf`, `docs/drawlib-dogfooding-en.docx`, `docs/drawlib-dogfooding-en_*`）を削除し、新出力物（`drawlib-dogfooding_en.pdf`, `drawlib-dogfooding_ja.pdf`, `drawlib-dogfooding_html/`, `drawlib-dogfooding_markdown/`, `drawlib-dogfooding_images/`）へ統一する。
4. **`dcli` および `README.md` の更新**:
   - `tools/dcli/docs/builder.py`・`cli.py`：`dogfooding` ターゲットの `clean_paths` を更新し、`dogfooding-en` 個別ターゲットを削除（必要に応じ `TARGET_MAP["dogfooding-en"] = TARGET_MAP["dogfooding"]` のエイリアスのみ残す）。
   - ルート `README.md` のホワイトペーパー PDF リンクを `docs/drawlib-dogfooding_en.pdf` / `docs/drawlib-dogfooding_ja.pdf` に更新する。

### 4.2. その他すべての公式プロジェクトへの `drawlib.toml` 配置
リポジトリ内の全8プロジェクトで `drawlib.toml` がドッグフーディングされる状態に揃える：

| プロジェクトディレクトリ | `project.type` | 言語構成 |
| :--- | :--- | :--- |
| `docs/docs_src/` | `"site"` | `[i18n]` `default_lang = "en"`, `langs = ["en", "ja"]`（`i18n.toml` から移行） |
| `docs/drawlib-dogfooding_src/` | `"doc"` | `[i18n]` `default_lang = "en"`, `langs = ["en", "ja"]`（日英統合） |
| `docs/quickstart_src/` | `"doc"` | 単一言語 `lang = "en"` |
| `docs/architecture_src/` | `"site"` | 単一言語 `lang = "en"` |
| `docs/slide_about_drawlib_src/` | `"slide"` | 単一言語 `lang = "en"` |
| `docs/slide_ddos_incident_response_src/`| `"slide"` | 単一言語 `lang = "en"` |
| `docs/readme_src/` | `"images"` | 単一言語 `lang = "en"` |
| `docs/logo_src/` | `"images"` | 単一言語 `lang = "en"` |

---

## 5. 主な変更対象ファイル一覧

1. **マニフェスト & 共通ビルダ層**:
   - `src/drawlib/_builder/_common/manifest.py` *(新規: `ProjectManifest`, `ProjectMetadata`, `I18nConfig`, `load_project_manifest`, `find_project_manifest`)*
   - `src/drawlib/_builder/_common/cache.py`, `styles_loader.py`（プロジェクトルート判定を `drawlib.toml` 対応に更新）
   - `src/drawlib/_builder/doc_builder/i18n.py`（`drawlib.toml` 連携、`validate_i18n_project` による `doc` モード対応）
   - `src/drawlib/_builder/doc_builder/compiler/{base,html,markdown,pdf,docx}.py`, `merger.py`, `exporter_docx.py`
   - `src/drawlib/_builder/image_builder.py`
2. **テンプレート & CLI スキャフォールド層**:
   - `src/drawlib/_templates/langs/{_models,_map_html}.py`（全16言語の `toc_title` 追加）
   - `src/drawlib/_templates/_css.py` / `doc` ベース CSS（`doc` 用 `.lang-switcher` & `@media print` 非表示スタイル）
   - `src/drawlib/_templates/_project.py`（`drawlib.toml` 生成、`doc` での複数言語 `-l en,ja` 解禁）
   - `src/drawlib/_templates/project/doc/template.html.template` & `docs_i18n/{en,ja}/` *(新規スターター)*
   - `src/drawlib/_cli/commands/init.py`（`drawlib init doc` の `--lang` ヘルプ更新）
3. **ルール・ツール・ドキュメント・テスト層**:
   - `src/drawlib/_rules/{project_overview,project_doc,project_site,cli}.md` および `.agents/rules/dcli.md`
   - `tools/dcli/docs/{builder,cli}.py`、`README.md`、`docs/*_src/drawlib.toml`、`docs/docs_src/{en,ja}/09_doc_builder_and_cli/project_{doc,site}.md`
   - `tests/drawlib/doc_builder/test_site_i18n.py`, `tests/drawlib/doc_builder/test_doc_i18n.py` *(新規)*, `tests/drawlib/cli/test_cli_init.py`

---

## 6. テスト・検証計画

1. **単体・結合テスト (`./dcli test all`)**:
   - `drawlib.toml` の正常系・異常系（TOML 構文エラー、不正な `project.type`、未対応言語コード、`default_lang` 不整合、ロケールディレクトリ欠落）の検証。
   - `drawlib init {images,doc,site,slide}`（単一言語および `doc`/`site` の `-l en,ja`）での `drawlib.toml` 生成テスト。
   - `i18ndoc` の HTML / Markdown / PDF (`_en.pdf`, `_ja.pdf`) / DOCX (`_en.docx`, `_ja.docx`) / Image ビルド結合テスト、TOC 見出しローカライズ（`"Table of Contents"` / `"目次"`）検証、ロケール別 `ja/styles.py` 優先適用テスト、`drawlib.toml` 無しレガシーディレクトリの後方互換テスト。
2. **静的解析 (`./dcli code-check all`)**:
   - Ruff lint/format、Ty 型チェック、`@validate_call` docstring チェックの全パス。
3. **実プロジェクトビルド & Stage 3 視覚検証**:
   - `./dcli docs build dogfooding` および `./dcli docs build --all` の完走確認。
   - `./dcli docs serve dogfooding --check`・`./dcli docs serve site --check` によるリンク切れゼロ検証。
   - ヘッドレスブラウザ（Playwright `1280×920`）で `drawlib-dogfooding_html/en/index.html`・`ja/index.html`（言語スイッチャー動作・日本語フォント・図版表示）および生成された `drawlib-dogfooding_en.pdf`・`drawlib-dogfooding_ja.pdf`（印刷時にスイッチャーが消えていること、目次が `"目次"` になっていること、日本語図版のフォント崩れがないこと）を `view_file` で目視確認する。
