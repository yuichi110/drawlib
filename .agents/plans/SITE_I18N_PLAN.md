# `site` プロジェクト多言語化（i18n）および公式ドキュメント展開計画書

- **作成日**: 2026-10-31
- **対象スコープ**:
  - **Phase 1 (`drawlib` 本体 i18n 基盤)**: `doc_builder` マルチロケール対応（共有 `images/` 出力・4段階の機械的整合性検証・言語切替スイッチャー UI）および `drawlib init site` テンプレート（`src/drawlib/_templates/project/site`）の複数言語スキャフォールド対応
  - **Phase 2 (`docs/docs_src` 構造移行)**: 公式ドキュメントサイト（`docs/docs_src/`、全111ページ・466図版）のマルチロケール構造（`en/` + `ja/`）への移行およびルール・`dcli` 更新
  - **Phase 3 (`docs/docs_src/ja` 段階的翻訳)**: 機械的整合性チェックを有効化した状態での並列サブエージェントによる日本語翻訳ロールアウト
- **位置づけ・基本方針**:
  - **外部依存追加ゼロ**: 設定ファイルには Python 3.11+ 標準ライブラリの `tomllib` で読める `i18n.toml` を用い、`pyproject.toml` への新規パッケージ追加は行わない。
  - **単一言語プロジェクトとの 100% 後方互換**: `i18n.toml` が存在しない既存の単一言語 `site` プロジェクト（`docs/architecture_src/` 等）や `drawlib init site [-l ja]` のフラット構造は一切変更せずそのまま動作させる。
  - **ファイル分離＋自己完結 Markdown**: 特殊な1ファイル内多言語構文や暗黙の空ブロック継承は導入せず、言語ごとにディレクトリ（`en/`, `ja/`）を分けた通常の自己完結した Drawlib Markdown ファイルとして管理する。
  - **画像の物理共有による容量・ビルド時間の最小化**: コンパイル後の生成画像は `images/<doc_rel_path>/<img_name>` に一元集約し、言語間で同名の図は1回だけレンダリングして全言語から共有参照する（何言語増やしても約200MBの画像バイナリ重複をゼロに抑える）。
  - **「構造とコードは機械検証、自然言語は AI」の役割分担**: ファイル過不足・サイドバー構造・ページ内の骨格シーケンス・描画コードの一致はすべてビルド時に機械チェックで強制し、文章および `caption` の翻訳品質に AI と人間が集中できる仕組みにする。

---

## 1. フェーズ全体構成

| フェーズ | 対象領域 | 主な変更・追加コンポーネント | ゴール・完了基準 | 難易度 |
| :--- | :--- | :--- | :--- | :---: |
| **Phase 1: `site` i18n エンジン & テンプレート実装** | `src/drawlib/_builder/doc_builder/`<br>`src/drawlib/_templates/project/site/`<br>`src/drawlib/_cli/commands/init.py` | ・`i18n.toml` パーサ & マルチロケールビルダ<br>・4種の機械的整合性チェッカー (`i18n.py`)<br>・`images/` 集約出力 & ルート `index.html` 生成<br>・言語スイッチャー UI & `drawlib init site -l en,ja` | 単体・結合テスト完備、`./dcli code-check all` & `./dcli test all` パス | 中 |
| **Phase 2: 公式 `docs/docs_src` マルチロケール基盤移行** | `docs/docs_src/`<br>`tools/dcli/docs/`<br>`src/drawlib/_rules/` | ・`docs_src/` → `docs_src/en/` 移行 + `ja/` 初期クローン作成<br>・`404.html` 旧URL転送対応<br>・組込みエージェントルール (`project_site.md` 等) 更新 | `./dcli docs build site` & `./dcli docs serve site --check` がエラーゼロで完走し、画像重複が増えていないこと | 低〜中 |
| **Phase 3: 公式 `docs/docs_src/ja` 日本語翻訳展開** | `docs/docs_src/ja/**/*.md` | ・`ja/navbar.md` + 章単位での並列サブエージェント翻訳<br>・必要箇所のみ `_ja.png` 独自図対応 & Stage 2/3 視覚検証 | 全章で機械的骨格・コード検証パス ＋ ブラウザ `1280×920` 表示検証完了 | 中 |

---

## 2. ディレクトリ構造仕様（ソース & コンパイル出力）

### 2.1. ソースディレクトリ構造 (`docs_src/`)

複数言語 `site` プロジェクトでは、プロジェクト共有設定・アセットをルート直下に置き、各言語の Markdown ツリーを `<lang>/` サブディレクトリに対称配置する。

```text
docs_src/
├── i18n.toml                     # マルチロケール定義 (default_lang / langs)
├── _assets/                      # [全言語共有] ロゴ・favicon・静的画像・カスタム .ttf
├── styles.py                     # [全言語共有] 描画テーマ・スタイル定義
├── utils.py                      # [全言語共有] 描画ヘルパー関数
├── style.css                     # [全言語共有] ベース CSS テーマ
├── template.html                 # [全言語共有] Jinja2 レイアウト（言語スイッチャー対応）
├── build.sh                      # 一括ビルドスクリプト (HTML + Markdown + Images)
├── build_html.sh
├── build_markdown.sh
├── build_image.sh
├── serve.sh
│
├── en/                           # デフォルト言語 (default_lang = "en")
│   ├── navbar.md                 # 英語サイドバー定義
│   ├── index.md                  # 英語トップページ
│   ├── 01_getting_started/
│   │   ├── overview.md
│   │   └── ...
│   └── 04_smartarts/
│       ├── table.md
│       └── ...
│
└── ja/                           # 追加言語（en/ とファイル構成・骨格・図コードを機械突合）
    ├── navbar.md                 # 日本語サイドバー定義
    ├── index.md                  # 日本語トップページ
    ├── 01_getting_started/
    │   ├── overview.md
    │   └── ...
    └── 04_smartarts/
        ├── table.md
        └── ...
```

#### `i18n.toml` のフォーマット仕様
```toml
default_lang = "en"
langs = ["en", "ja"]
```
- `langs` に列挙されたディレクトリのみをロケールとして扱うため、`docs/docs_src/pypi/` のような補助ディレクトリが同居していても言語ディレクトリと誤認しない。
- 各言語コードは既存の `drawlib._templates.langs.normalize_language()` で検証し、サポート済み 16 言語（`en`, `ja`, `zh-cn`, `zh-tw`, `ko`, `es`, `fr`, `de` 等）のフォント・HTML 属性定義と自動連携する。

---

### 2.2. コンパイル後 HTML ディレクトリ構造 (`docs_html/`)

```text
docs_html/
├── index.html                           # デフォルト言語 (en/index.md) の実体 HTML（ルート相対パス解決済み）
├── 404.html                             # (任意/公式用) 旧URL (/04_smartarts/...) を /en/... へ自動転送
├── _assets/                             # 共通ロゴ・favicon・アセット（1箇所のみ）
├── images/                              # ★ 全言語共有の生成画像ディレクトリ
│   ├── index/
│   │   └── hero_ai_doc_loop.png         # en/index.md & ja/index.md & root index.html から共有参照
│   └── 04_smartarts/
│       └── table/
│           ├── table_hero.png
│           └── table_parameter_tour.png
├── en/
│   ├── style.css                        # en 用 CSS
│   ├── index.html                       # -> ../images/index/hero_ai_doc_loop.png を参照
│   └── 04_smartarts/
│       └── table.html                   # -> ../../images/04_smartarts/table/table_hero.png を参照
└── ja/
    ├── style.css                        # ja 用 CSS (Noto Sans JP 適用)
    ├── index.html                       # -> ../images/index/hero_ai_doc_loop.png を参照
    └── 04_smartarts/
        └── table.html                   # -> ../../images/04_smartarts/table/table_hero.png を参照
```

- **ルート `index.html` の実体出力**:
  - クライアントサイド JS リダイレクトによるチラつきや SEO / OGP 低下を避けるため、`default_lang` の `index.md` をルート階層用の相対パス（画像: `images/index/...`、ナビゲーション・本文リンク: `en/...`、言語スイッチャー: `ja/index.html`）でレンダリングして直接配置する。
- **画像パスの命名規則 (`images/<doc_rel_stem>/<img_name>`)**:
  - `<lang>/index.md` の図 → `images/index/<img_name>`
  - `<lang>/04_smartarts/table.md` の図 → `images/04_smartarts/table/<img_name>`
  - 章ごとに `overview.md` 等の同名ファイルが存在しても衝突せず、かつ `en/`・`ja/` 配下が純粋な `.html` ファイルのみで構成される。
- **コンパイル後 Markdown (`docs_markdown/`)**:
  - `docs_html/` と同様に `index.md`（デフォルト言語）、`en/`、`ja/`、`images/`、`_assets/` を出力する。これにより GitHub リポジトリ上での Markdown 閲覧でも画像バイナリの重複がゼロになる。

---

## 3. 複数言語間の機械的整合性検証（i18n Parity Validator）仕様

`src/drawlib/_builder/doc_builder/i18n.py` を新設し、`drawlib build html` および `drawlib build markdown` の冒頭（画像レンダリング前の高速プリフライト段階）で以下の **4つの機械チェック** を自動実行する。

### 3.1. Check 1: ファイル存在一致チェック（File Set Parity）
- `default_lang`（例: `en/`）配下の対象 `.md`（および `.html`）の相対パス集合 $F_{\text{default}}$ と、各翻訳言語 `<lang>/` 配下の相対パス集合 $F_{\text{lang}}$ を比較する。
- 不足ファイル（$F_{\text{default}} - F_{\text{lang}}$）または余剰ファイル（$F_{\text{lang}} - F_{\text{default}}$）が1つでも存在する場合は、対象パス一覧を表示して `ValueError` で即座にビルドを停止する。

### 3.2. Check 2: `navbar.md` 構造・リンク先一致チェック（Navbar Parity）
- 全言語の `<lang>/navbar.md` を `parse_navbar_markdown()` でパースし、`default_lang/navbar.md` と以下を比較する：
  1. セクション数（`len(sections)`）および各セクションの見出し有無（`section.title is not None`）の一致
  2. 各セクション内のリンク数および各アイテムのリンク先（内部リンクの正規化相対パス＋アンカー、または外部 URL）の完全一致
- サイトブランド名（H1）およびセクション見出し・リンク表示文字列のみ翻訳を許容し、リンク漏れや順序入れ替わりを機械的にブロックする。

### 3.3. Check 3: ページ内骨格シーケンス一致チェック（Markdown Skeleton Sequence Parity）
- `preserve_outer_fences()` で外側フェンス（4連バッククォート等の解説用ネストフェンス）を保護した上で、各 `.md` ファイルを上から走査し、以下の **骨格トークン列** に変換する：
  1. **`Heading(level=1..3)`**: `#`, `##`, `###` の見出し階層（後半セクションの翻訳抜け・出力途切れを検知するため `H1`〜`H3` を骨格に含める）。
  2. **`MarkdownText`**: 見出しやコードブロックの間に存在する非空の地の文・箇条書き・表・引用・水平線などの連続領域。連続する複数段落や箇条書き行数の増減は **単一の `MarkdownText` トークン** に畳み込むことで、自然な翻訳表現の自由度を 100% 保ちつつ、「図と図の間の説明文が丸ごと消えた」「末尾の解説が消えた」ケースを確実に検知する。
  3. **`DrawlibBlock(file_name, code_mode, align, has_caption)`**: ```` ```drawlib ```` コードブロックの位置、`file=` 指定、`code=` モード（`show` / `fold` / `hide`）、`align=`、および `caption=` 指定の有無。
  4. **`CodeBlock(lang)`**: ```` ```python ```` や ```` ```bash ```` など通常のコードブロックの位置と言語識別子（API シグネチャや CLI 例の削除ミスを検知）。
- `default_lang` のトークン列と `<lang>` のトークン列を先頭から順に比較し、不一致があれば **ファイル名・行番号・期待された要素と実際の要素** を明示してエラー終了する。

### 3.4. Check 4: `drawlib` 描画コード完全一致チェック & 言語固有図の例外規約（Code Parity）
- 骨格シーケンス上で同じ位置に対応する `DrawlibBlock` ペア（`default_block`, `lang_block`）について、画像ファイル名と Python コードを検証する：
  1. **標準ケース（共通画像：`lang_block.file_name == default_block.file_name`）**:
     - `lang_block.code.strip() == default_block.code.strip()`（1文字単位の完全一致）を強制する。
     - もし1文字でも異なっていた場合は、「`en` 側のコード更新が `<lang>` に未反映、または翻訳中に誤ってコードが改変された」と判定し、行番号付きでエラー終了する。
     - ビルド時は `images/<doc_rel_stem>/<file_name>` へ **1回だけレンダリング** し、2言語目以降はレンダリング処理自体をスキップして同一画像パスを参照させる。
  2. **言語固有図ケース（命名規約：`<stem>_<lang>.<ext>`）**:
     - 例: `en` が `file=hero.png` の位置で、`ja` が `file=hero_ja.png` を指定している場合。
     - ベース名 `<stem>` と拡張子 `<ext>` が `default_block` と一致し、直後に `_{lang}` が付いている場合のみ「意図的な言語別図版」として独自 Python コードを許可し、`images/<doc_rel_stem>/hero_ja.png` に個別レンダリングする。
     - それ以外の無関係なファイル名（例: `file=other.png`）は貼り間違いとしてエラーにする。
- **`styles.py` の扱い**:
  - 共通画像が言語間で完全に同一の見た目になるよう、プロジェクトルートの `docs_src/styles.py` を全言語共通で使用する。言語固有図（`*_ja.png`）で日本語フォントが必要な場合は、当該コードブロック内または `utils.py` のヘルパーで `FontJapanese` 等を適用する。

---

## 4. HTML テンプレート・CSS・CLI 拡張仕様

### 4.1. 言語別フォント・HTML 属性と Language Switcher UI
- **HTML / CSS のロケール適応**:
  - `drawlib._templates.langs.get_language_config(lang)`（各言語のネイティブ表記 `native_name`: `"English"`, `"日本語"`, `"简体中文"` 等を追加）を利用し、各 `<lang>/` のビルド時に以下を自動反映する：
    - `<html lang="{{ html_lang }}" dir="{{ html_dir }}">`（例: `ja`, `zh-CN`）
    - `<head>` 内への Google Fonts リンク（例: `Noto Sans JP`）および SEO 用 `<link rel="alternate" hreflang="{{ l.html_lang }}" href="{{ l.url }}">` の自動注入
    - `<lang>/style.css` への言語別 `font-family` 適用
- **Language Switcher（画面右上・`<a href>` ドロップダウン UI）**:
  - **配置場所（画面右上：`<header class="top-bar">` 右端）**:
    - メインカラム最上部の `<header class="top-bar">` を `display: flex; align-items: center; justify-content: space-between; gap: 1rem;` とし、左側の `.breadcrumbs`（`min-width: 0`）と対向する右端に `.lang-switcher`（`flex-shrink: 0`）を配置する（モバイル `<= 768px` でもメニューを開かず1タップで切替可能）。
  - **UI 要素構造（`<select>` ではなく `<details>` ＋ `<a href="...">` メニュー）**:
    - 見た目は地球儀 SVG アイコン付きのセレクトボックス風ボタン（`[ 🌐 English ▾ ]` / `[ 🌐 日本語 ▾ ]`）としつつ、HTML 要素としては `<details class="lang-dropdown">` 内に `<a href="{{ l.url }}" lang="{{ l.html_lang }}">` リストを展開する方式を採用する（外側クリック・`Escape` キーで閉じる軽量 JS 付き、印刷 `@media print` 時は非表示）。
    - **`<a href>` 採用の利点**:
      1. `drawlib serve --check`（`scan_broken_links()`）が全ページの言語切替リンクを自動走査し、リンク切れを機械保証できる。
      2. `Cmd/Ctrl + クリック` で他言語ページを別タブで開いて並べて比較できる。
      3. OS 依存の `<select>` ポップアップを使わないため、ライト／ダークモード（`data-theme="dark"`）の配色と 100% 調和する。
      4. 検索エンジンクローラーが `<a href>` を辿って全言語ページを巡回できる。
  - **テンプレート連携**:
    - `render_html_document()` から `languages` リスト（各要素: `{"code": "ja", "html_lang": "ja", "label": "日本語", "url": "../../ja/04_smartarts/table.html", "active": False}` 等）を渡す。
    - Check 1（ファイル存在一致チェック）により全言語に対訳ページが必ず存在するため、どのページで言語を切り替えても **404 にならず同じページの別言語版へ直接遷移** できる。
    - 単一言語サイトでは `languages` を空リストとし、UI 上にスイッチャーを表示しない。

### 4.2. CLI コマンド対応 (`init` / `build` / `show` / `serve`)
1. **`drawlib init site`**:
   - `-l / --lang` オプションでカンマ区切りの複数言語指定（例: `drawlib init site docs -l en,ja`）をサポートする。
   - 1言語のみ指定時（デフォルト `-l en` や `-l ja`）：現行と同一のフラットな `docs_src/` を生成。
   - 2言語以上指定時（`-l en,ja`）：先頭言語を `default_lang` とする `i18n.toml` を生成し、`docs_src/en/`・`docs_src/ja/` にサンプルページと `navbar.md` を展開する。
2. **`drawlib show`**:
   - `uv run drawlib show docs_src/ja/04_smartarts/table.md table_hero.png -g` のようにサブディレクトリ内のファイルを直接指定した際も、親ディレクトリ（`docs_src/`）にある `styles.py`・`utils.py`・`_assets/` を自動解決してプレビューできるようにする。
3. **`drawlib serve --check`**:
   - `docs_html/` 全体（ルート `index.html`、`en/**`、`ja/**`、`images/**`、`_assets/**`）に対して既存の `scan_broken_links()` を走らせ、リンク切れ・画像参照切れゼロを検証する。

---

## 5. 公式ドキュメント (`docs/docs_src/`) への段階的導入手順

### Step 1: Phase 1 実装 & テスト検証
1. `doc_builder/i18n.py`（`i18n.toml` 読み込み＋Check 1〜4 バリデータ）を実装し、正常系および各違反ケース（ファイル欠落、`navbar` ズレ、見出し抜け、説明文消失、コード不一致、`_<lang>` 独自図許容）の単体テストを `tests/drawlib/doc_builder/` に追加する。
2. `compiler/html.py`・`compiler/markdown.py`・`exporter_html.py` にマルチロケールビルド（共有 `images/` 出力＋ルート `index.html` 出力＋言語スイッチャー変数注入）を実装する。
3. `_templates/project/site/` および `_templates/_project.py`・`_cli/commands/init.py` を更新し、`drawlib init site -l en,ja` のスキャフォールドとビルドの結合テストを追加する。
4. `./dcli code-check all` および `./dcli test all` をすべてパスさせる。

### Step 2: Phase 2 `docs/docs_src/` の構造移行（英語＋日本語クローン初期化）
1. `docs/docs_src/` の既存コンテンツ（`index.md`, `navbar.md`, `01_getting_started/`〜`10_ai_agents_and_advanced/`）を `docs/docs_src/en/` へ移動する。
2. `docs/docs_src/en/` を `docs/docs_src/ja/` へ初期コピーし、`docs/docs_src/i18n.toml`（`default_lang = "en"`, `langs = ["en", "ja"]`）および言語スイッチャー対応版 `template.html` / `style.css` を配置する。
3. 旧サブページ URL（`/04_smartarts/table.html` 等）から `/en/...` へ誘導する軽量な `404.html` を追加する。
4. `./dcli docs build site` および `./dcli docs serve site --check` を実行し、全機械チェックのパスと、画像出力が `docs_html/images/`・`docs_markdown/images/` の1箇所のみに集約されていることを確認する。
5. `src/drawlib/_rules/project_site.md`・`cli.md` 等の組込みルールを更新する。

### Step 3: Phase 3 並列サブエージェントによる日本語翻訳ロールアウト
1. 先行して `ja/navbar.md` と `ja/index.md`、`ja/01_getting_started/*.md` を翻訳し、ブラウザ（`1280×920`）で言語スイッチャー・日本語フォント（`Noto Sans JP`）・レイアウトを Stage 3 検証する。
2. 残りの `02_drawing_primitives/`〜`10_ai_agents_and_advanced/` を章単位で複数のサブエージェントに排他割り当てし、本文・見出し・表・`caption="..."` を並列翻訳する（描画 Python コードは原則そのまま保持し、日本語独自図が必要な箇所のみ `_*_ja.png` として Stage 2 `-g` グリッド検証を実施）。
3. 親オーケストレータで `./dcli docs build site` と `./dcli docs serve site --check` を実行し、4段階の機械的整合性検証によって全111ページの構造・コード完全一致を保証する。
