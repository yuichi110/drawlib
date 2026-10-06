# Drawlib テンプレート・CSS・ドキュメント統合リファクタリング計画書
(TEMPLATE REFACTORING PLAN)

- **作成日**: 2026-10-04
- **対象バージョン**: Drawlib 次期リリース
- **前提条件**: **後方互換性の維持は不要**（最善のアーキテクチャ設計・DRY原則を最優先とする）

---

## 1. エグゼクティブサマリー & ゴール

Drawlib の機能拡充に伴い、テンプレート（`site`, `simple`, `pdf`, `slide`, `image`）、CSS（HTML用、PDF用、Slide用）、および言語マッピング（`_langs`）が複数のトップレベルディレクトリに分散し、コードの重複と概念の分断が顕著になっています。

本リファクタリングの目的は以下の4点です：

1. **CSS の共通化（3層レイヤードCSSアーキテクチャ）**:
   媒体ごとにコピー＆ペーストされていた Markdown 装飾、タイポグラフィ、コードハイライトを共通化し、テーマ（Google, Default, Monochrome 等）をデザイン・トークンとして一元化する。
2. **線形ドキュメントの統合（`simple` と `pdf` を `doc` に一本化）**:
   同じ「1本の線形ドキュメント（仕様書/レポート/論文）」である `simple`（HTML専用）と `pdf`（PDF専用）を統合し、同一ソースから HTML と PDF の両方をシームレスにビルド可能にする。
3. **ビルドスクリプトの明確化（`build_*.sh` への分割と出力ターゲットの体系化）**:
   単一の `build.sh` による暗黙的な挙動を改め、`build_image.sh`, `build_markdown.sh`, `build_html.sh`, `build_pdf.sh` と用途別のスクリプトを用意し、各プロジェクトで求められる出力を網羅する。
4. **テンプレート・リソース・i18n・ビルダーの完全集約 (`src/drawlib/_templates/`)**:
   `_project_templates/`、`_css_templates/`、およびテンプレート用言語定義 `_langs/` を新設の **`_templates/`** パッケージ配下に完全集約し、テンプレートの組み立て・展開責務を **`_templates/builder.py`** に統合する。また、JavaScript（`slide.js`）は CSS ではなく `project/slide/` 配下に正しく配置する。

---

## 2. 現状分析と課題 (As-Is Analysis)

### 2.1. CSS テンプレート (`src/drawlib/_css_templates/`) の課題

- **計 19 ファイルの分散と膨大な重複**:
  - `html/`: 9 ファイル（各 400〜500 行）
  - `pdf/`: 7 ファイル（各 200〜300 行）
  - `slide/`: 3 ファイル（各 458 行）
- **完全重複の放置**:
  - `slide/default.css.template` と `slide/google.css.template` は **100% 完全一致**。
  - `slide/monochrome.css.template` も `:root` の CSS 変数 15 行のみが異なるだけで、残りの 443 行（ビューポート、固定ステージ、操作UI、トランジション等）は全く同じコードが複製されている。
- **Markdown 装飾ルールの二重・三重管理**:
  - 見出し（H1〜H6）、表（Table）、引用（Blockquote）、注意書き（Admonition）、コードブロック（Pre/Code）のスタイルが `html/` と `pdf/` で重複実装されている。
  - 表の罫線やコードハイライトを修正する際、全媒体のファイルを個別に修正する必要があり、デザインの乖離が生じている。
- **HTML テンプレートへの CSS 直書き**:
  - `_project_templates/simple/template.html.template`（約 330 行）や `site/template.html.template`（約 490 行）に、フォールバック用の巨大な `<style>` タグがハードコードされている。
- **言語・関心事の混入**:
  - `_css_templates/slide/slide.js` のように、CSS ディレクトリの中に JavaScript ファイルが同居しており、責務が曖昧になっている。

### 2.2. プロジェクトテンプレートとビルドスクリプトの課題

- **`simple` と `pdf` の不自然な分断**:
  - `simple`: `docs_src/doc.md` を起点に `drawlib build html` と `drawlib build markdown` を実行。PDF は出力できない。
  - `pdf`: `docs_src/00_cover.md`, `01_overview.md` などを起点に `drawlib build pdf` を実行。HTML は出力できない。
  - **実態**: 仕様書や技術文書、RFC、論文などを作成する場合、「Web で閲覧するための HTML」と「印刷・配布用の PDF」の両方を同一ソースから生成したいケースが標準的であり、媒体によってテンプレートを分ける必然性がない。
- **ビルドスクリプトの不透明さと開発テンポの阻害**:
  - 各プロジェクトに置かれた `build.sh` が何を出力するかがファイル名から読み取れない。
  - PDF ビルド（Playwright / Headless Chromium 起動）は HTML ビルドに比べて実行時間がかかるため、執筆中に「HTML だけ高速に再ビルドしたい」というケースに対応できない。
- **スライドの PDF 出力欠如**:
  - `slide` テンプレートには HTML 出力しかなく、社内勉強会や登壇、クライアント配布で最も求められる「1スライド1ページの配布用 PDF」を出力する標準スクリプトがない。
- **ドキュメント内図版の素材再利用の難しさ**:
  - `doc` や `site` の Markdown 内に埋め込んだアーキテクチャ図やシーケンス図を、Google Slides / PowerPoint プレゼンや Slack、PR に貼るために「画像ファイル単体として抽出したい」という強い需要があるが、専用の出力導線がない。

### 2.3. 言語・フォント定義 (`src/drawlib/_langs/`) の独立過剰

- **利用者が 100% テンプレート関連のみ**:
  - `_langs` は、`_map_html.py`（Google Fonts リンクや `lang="ja"` 属性）、`_map_css.py`（CSS テンプレート内のフォント置換）、`_map_style_font.py`（`styles.py.template` 用の Font 設定）など、**テンプレートの初期化と CSS 合成のためだけに存在** している。
  - Drawlib のコア描画エンジン（`_core`）や CLI、チャート、ダイアグラムなどは `_langs` を一切使用していない。
  - これが独立したトップレベルパッケージとして存在しているため、関心事が不要に分散している。

### 2.4. コード配置と責務のねじれ (Architecture Disconnect)

- **リソースとロジックの乖離**:
  - プロジェクトリソースは `_project_templates/` にあるが、それを展開するコードは遠く離れた `_builder/project_init.py` に置かれている。
  - 本来 `_builder` はコンテンツ（Markdown や Python コード）のコンパイルエンジンであるべきなのに、プロジェクト初期化の足場ロジックが混ざり込んでいる。
- **CSS エンジンの混在**:
  - `_css_templates/` は静的な CSS テンプレートと Python コード（`__init__.py`）が同一階層に同居している。

---

## 3. 目指すアーキテクチャ (To-Be Architecture)

### 3.1. `src/drawlib/_templates/` への完全集約と `builder.py` の責務

すべてのテンプレートリソース（CSS・Project）、i18n 言語/フォント定義（langs）、およびその組み立て・展開ロジックを **`_templates/`** パッケージに集約します。

```text
src/drawlib/_templates/
├── __init__.py           # パッケージの公開 API
│                         # (init_project, get_css, list_css, export_css, list_project_types)
├── builder.py            # ★テンプレート組み立てエンジン
│                         #   - ProjectTemplateBuilder: project/ の展開、置換、スクリプト配置
│                         #   - CssTemplateBuilder: css/ の 3層合成 (theme + component + target)
│
├── langs/                # ★テンプレート用 i18n & フォントマッピング (旧 _langs)
│   ├── __init__.py       #   get_font_replacements, normalize_language 等
│   ├── _map_html.py      #   HTML 用 lang 属性 / Google Fonts 定義
│   ├── _map_css.py       #   CSS 用フォントファミリー定義
│   ├── _map_style_font.py#   styles.py 用 Font 定義
│   ├── _models.py
│   ├── _patch.py
│   └── _registry.py
│
├── css/                  # ★100% 純粋な CSS のみ
│   ├── themes/           #   Layer 1: カラーパレット・フォントの CSS 変数
│   │   ├── default.css.template
│   │   ├── default-dark.css.template
│   │   ├── google.css.template
│   │   ├── google-dark.css.template
│   │   ├── monochrome.css.template
│   │   └── github.css.template
│   ├── components/       #   Layer 2: 全媒体共通の Markdown・コード装飾ルール
│   │   ├── markdown.css
│   │   └── code.css
│   └── targets/          #   Layer 3: 媒体固有のレイアウト制御
│       ├── site.css      #     サイドバー、ナビゲーション、Webコンテナ
│       ├── doc.css       #     単一ドキュメント用中央揃え・読書ビュー
│       ├── pdf.css       #     @page (A4), 改ページ制御
│       └── slide.css     #     1920x1080固定ステージ、縮小拡大ビューポート
│
└── project/              # ★プロジェクト初期化用スターターリソース
    ├── _assets/          #   共通画像 (linux.png 等)
    ├── _shared/          #   共通 Python (styles.py.template, utils.py)
    │
    ├── doc/              #   [統合] 線形ドキュメント用 (旧 simple + pdf)
    │   ├── docs/ (en, ja)#     00_cover.md, 01_overview.md, 02_design.md
    │   ├── build.sh.template         # Master (一括フルビルド)
    │   ├── build_html.sh.template    # 高速プレビュー HTML
    │   ├── build_pdf.sh.template     # 印刷・提出用 PDF
    │   ├── build_markdown.sh.template# GitHub閲覧用 Markdown
    │   ├── build_image.sh.template   # 図版素材エクスポート
    │   ├── serve.sh.template
    │   └── template.html.template    # クリーンな Jinja2 テンプレート
    │
    ├── site/             #   Web ドキュメントサイト用
    │   ├── docs/ (en, ja)
    │   ├── build.sh.template         # Master (一括フルビルド)
    │   ├── build_html.sh.template    # 静的サイト HTML
    │   ├── build_markdown.sh.template# Markdown
    │   ├── serve.sh.template
    │   └── template.html.template
    │
    ├── slide/            #   プレゼンテーションスライド用
    │   ├── slide.js      #   ★スライド専用実行エンジン JS（ここに配置）
    │   ├── docs/ (en, ja)
    │   ├── utils/        #   スタイル別 utils.py テンプレート
    │   ├── build.sh.template         # Master (一括フルビルド)
    │   ├── build_html.sh.template    # HTML スライドデッキ
    │   ├── build_pdf.sh.template     # 配布用 PDF (1スライド1ページ)
    │   └── serve.sh.template
    │
    └── image/            #   Python イラスト画像バッチ用
        ├── docs/ (en, ja)
        ├── build.sh.template         # Master
        └── build_image.sh.template   # Python 画像ビルド
```

#### `_templates/builder.py` が担う 2 つのビルド責務
1. **CSS テンプレートのビルド（合成）**:
   - `themes/<theme>.css` ＋ `components/markdown.css` ＋ `targets/<target>.css` を読み込み、`langs/` の言語別フォント置換を施して **1 本の完成した CSS を組み立てる（ビルドする）**。
   - `get_css(theme, target, lang)` や `export_css()` を提供。
2. **プロジェクトテンプレートのビルド（初期化・展開）**:
   - `project/<type>/` からファイルを読み込み、プレースホルダー（`__SRC_DIR__`, `__OUT_DIR__`、`langs/` のフォント設定等）を置換し、対応する `build_*.sh` やスタイルシートを組み合わせて、**指定ディレクトリに完成したプロジェクトを組み立てる（ビルドする）**。
   - `init_project()` や `list_project_types()` を提供。
   - これにより、`_builder/` はコンテンツコンパイル処理のみに専念できる。

---

### 3.2. 3層レイヤード CSS アーキテクチャ

CSS の関心を **「テーマ・トークン」「コンポーネント装飾」「ターゲット・シェル」** の 3 層に分離します。

$$\text{Output CSS} = \text{Layer 1 (Theme)} + \text{Layer 2 (Components)} + \text{Layer 3 (Target Layout)}$$

- **効果**:
  - 新規テーマ（例: `nord`, `dracula`）を追加する場合、`themes/` に 1 ファイル（約 30 行）追加するだけで、**HTML・PDF・Slide の全媒体で即座に利用可能** になる。
  - 表や Admonition のデザイン修正が全媒体に自動反映される。
  - テンプレート内の CSS コード総量を約 **70% 削減**。
  - `css/` ディレクトリ内は 100% 純粋な CSS のみとなり、JavaScript などの混入を排除。

---

### 3.3. プロジェクト種別とビルドスクリプト体系

プロジェクト種別を、明確に用途が異なる **4 つの種別** に集約し、各プロジェクトに用途別のビルドスクリプトを明示的に配置します。

#### プロジェクト種別と出力マトリクス

| プロジェクト種別 | 概要・用途 | 配置するビルドスクリプト | 出力対象 |
| :--- | :--- | :--- | :--- |
| **`image`** | Python スクリプトによる純粋なイラスト・図版一括生成 | `build_image.sh`<br>`build.sh` | `images/*.png`, `images/*.webp` |
| **`doc`** *(新設・統合)* | 仕様書、レポート、論文、RFC などの線形ドキュメント | `build_html.sh`<br>`build_pdf.sh`<br>`build_markdown.sh`<br>**`build_image.sh`**<br>`build.sh` | `doc.html` (Web)<br>`doc.pdf` (Print)<br>`doc.md` (GitHub)<br>`images/*.png` (素材)<br>(Master: 全種一括) |
| **`site`** | 階層構造とサイドバーナビ（`navbar.md`）を持つドキュメントサイト | `build_html.sh`<br>`build_markdown.sh`<br>`build.sh` | `docs_html/` (Webサイト)<br>`docs/` (GitHub)<br>(Master: 全種一括) |
| **`slide`** | 16:9 スライドプレゼンテーションデッキ | `build_html.sh`<br>**`build_pdf.sh`**<br>`build.sh` | `slide/index.html` (Web)<br>**`slide.pdf`** (配布・印刷)<br>(Master: 全種一括) |

#### 各スクリプトの役割設計

1. **`build_html.sh`**:
   - 高速な HTML ビルド。執筆中のプレビューやローカル検証、Web 公開用。
2. **`build_pdf.sh`**:
   - Playwright / Headless Chromium を用いた高品質 PDF 出力。
   - `doc`: A4 ページネーション、章立て改ページ、目次（TOC）付きドキュメント。
   - `slide`: 1 ページ 1 スライドの 16:9 プレゼンテーション配布資料。
3. **`build_markdown.sh`**:
   - Drawlib コードブロックを描画済み画像参照に置換した Markdown 出力（GitHub レポジトリ直読用）。
4. **`build_image.sh`**:
   - `image` プロジェクト: Python スクリプトを実行して画像を生成。
   - `doc` プロジェクト: **Markdown 内に埋め込まれた図版（```drawlib ブロック）だけを単体画像として `images/` フォルダへ一括抽出・エクスポート**。
5. **`build.sh` (Master Script)**:
   - 各プロジェクトがサポートする出力をまとめて一括生成するオーケストレーションスクリプト。

---

### 3.4. 特筆すべき機能要件とその価値

#### ① `doc project -> image`（図版素材の一括エクスポート）
- **背景と需要**:
  - 設計書（`doc`）を作成したエンジニアは、次に社内スライド（Google Slides, PowerPoint, Keynote）でレビュー発表を行うことが多い。
  - その際、「設計書に書いたアーキテクチャ図やシーケンス図だけをプレゼン資料にドラッグ＆ドロップしたい」という要求が必ず発生する。
  - さらに、Slack や GitHub PR、社内 Wiki (Notion, Confluence) に「図解だけを直接貼る」シーンでも画像単体ファイルが不可欠。
- **実装方針**:
  - `drawlib build image <markdown_file_or_dir> -o <images_dir>` をサポート。
  - Markdown ファイルを解析し、含まれる ```drawlib コードブロックを抽出・実行して独立した PNG/SVG 画像群を出力。

#### ② `slide project -> pdf`（スライドの配布用 PDF 出力）
- **背景と需要**:
  - 登壇や社内勉強会、顧客への提案資料送付において、「Web スライド（HTML）ではなく PDF 形式で提出・共有する」ことは業界標準の必須要件。
  - Marp や Slidev などの先進プレゼンツールでも最重要機能として位置づけられている。
- **実装方針**:
  - `drawlib build pdf <slide_dir> -o <output.pdf>` をサポート。
  - 内部で Headless Chromium を起動し、スライドの各ページ要素（1920x1080）を 1 ページごとにキャプチャして単一のプレゼン用 PDF を合成。

#### ③ `slide.js` の `project/slide/` への配置とカスタマイズ性
- **背景と価値**:
  - `slide.js` はスライド固有のキーボード操作、縮小拡大ビューポート、全画面/一覧モードを制御する専用 JavaScript。
  - `_templates/project/slide/slide.js` に配置することで、`css/` を汚染せず、スライド関連ファイルを一箇所にカプセル化。
  - `drawlib build slide` はデフォルトでこの組み込み `slide.js` を配備するが、ユーザーが `slide_src/slide.js` を自前で配置した場合はそれを優先（オーバーライド）できるようにし、上級者の独自拡張にも対応。

---

## 4. 詳細実装タスク (Action Items & WBS)

### Phase 1: `_templates` パッケージの新設、`_langs` 移行、CSS 3層レイヤー化

1. **`src/drawlib/_templates/` の新設**:
   - `_templates/__init__.py` の作成。
   - `_templates/builder.py` の骨格作成。
2. **`_langs` の `_templates/langs/` への移行**:
   - `src/drawlib/_langs/` の内容を `src/drawlib/_templates/langs/` に移行。
   - 旧 `src/drawlib/_langs/` を削除。
   - 内部参照パスを更新。
3. **デザイン・トークン体系の標準化 (`_templates/css/themes/`)**:
   - 変数プレフィックスを統一（`--dl-brand`, `--dl-brand-dark`, `--dl-text`, `--dl-bg`, `--dl-border`, `--dl-code-*`, `--dl-font`, `--dl-mono-font`）。
   - `themes/default.css.template`, `google.css.template`, `monochrome.css.template`, `github.css.template`, `*-dark.css.template` を作成。
4. **共通コンポーネントの抽出 (`_templates/css/components/`)**:
   - `components/markdown.css`: H1〜H6、Table、Blockquote、List、Admonition (`.admonition`, `.note`, `.tip`, `.warning` 等)、画像キャプション。
   - `components/code.css`: シンタックスハイライト、行番号表示、インラインコードタグ。
5. **ターゲット・シェルの抽出 (`_templates/css/targets/`)**:
   - `targets/site.css`: サイドバー、検索、ハンバーガーメニュー、レスポンシブコンテナ。
   - `targets/doc.css`: 単一ドキュメント用の美しい中央揃えレイアウト（最大幅 900px、クリーンな読書ビュー）。
   - `targets/pdf.css`: `@page { size: A4; margin: 18mm 16mm; }`、`break-inside: avoid;`、ページフッター/ヘッダー。
   - `targets/slide.css`: 1920x1080 固定ステージ、全画面縮小拡大ビューポート、ナビゲーション操作UI。
6. **CSS 合成ビルダーの実装 (`_templates/builder.py`)**:
   - `get_css(name, target, lang)` の実装（トークン + コンポーネント + ターゲットレイアウトの連結合成、`langs/` フォント置換）。
   - `list_css(target)`、`export_css()` の実装。
7. **旧 `_css_templates/` の削除**:
   - 旧フォルダを完全に削除し、参照先を `_templates` に切り替え。

---

### Phase 2: プロジェクトテンプレートの移行と `builder.py` への統合

1. **`_templates/project/` の配備**:
   - `_templates/project/_assets/` および `_shared/` の移行。
   - `_templates/project/slide/slide.js` の配置。
2. **線形ドキュメント `doc` テンプレートの作成**:
   - `_templates/project/doc/` を新設。
   - 日本語・英語のスターター文書（カバー、概要、アーキテクチャ設計サンプル）を配備。
3. **目的別 `build_*.sh.template` の作成と配備**:
   - `doc`: `build.sh.template`, `build_html.sh.template`, `build_pdf.sh.template`, `build_markdown.sh.template`, `build_image.sh.template`
   - `site`: `build.sh.template`, `build_html.sh.template`, `build_markdown.sh.template`
   - `slide`: `build.sh.template`, `build_html.sh.template`, `build_pdf.sh.template`
   - `image`: `build.sh.template`, `build_image.sh.template`
4. **`template.html.template` のクリーン化**:
   - `site` および `doc` 内の数百行に及ぶフォールバック `<style>` 直書きを削除し、簡潔なテンプレートに統一。
5. **プロジェクト初期化ビルダーの実装 (`_templates/builder.py`)**:
   - `_builder/project_init.py` の全ロジックを `_templates/builder.py` に移行・リファクタリング。
   - `PROJECT_TYPES` を `site`, `doc`, `slide`, `image` の 4 種に更新。
   - `_builder/project_init.py` を削除。
6. **旧 `_project_templates/` の削除**:
   - `_project_templates/` を完全に削除。

---

### Phase 3: ビルドエンジンおよび CLI の機能拡張

1. **`drawlib build pdf` の拡張**:
   - 単一 Markdown ファイル（例: `doc.md`）の直接コンパイルに対応。
   - `slide` ディレクトリの 1 スライド 1 ページ PDF 出力に対応。
2. **`drawlib build image` の拡張（Markdown からの画像抽出）**:
   - Markdown ファイルまたはディレクトリ内の ```drawlib ブロックを抽出・実行し、画像ファイルとして一括保存する機能をサポート。
3. **`drawlib build html` の線形ドキュメント対応**:
   - ディレクトリ内に `navbar.md` が存在しない場合でも、章立てファイル群（`00_cover.md`, `01_...`）を検出した際に、単一の結合 HTML（`doc.html`）を生成可能にする。
4. **CLI コマンド・ヘルプの更新**:
   - `drawlib init list` の出力更新（`simple`, `pdf` を削除し `doc` を表示）。
   - `drawlib build` の引数検証メッセージの整備。
   - 各種インポートパス（`_css_templates`, `_project_templates`, `_langs`, `_builder.project_init` → `_templates`）を更新。

---

### Phase 4: テスト・ドキュメント・サンプルの更新

1. **テストコードの改修**:
   - `tests/cli/test_cli_init.py`: `doc` テンプレートの初期化、全 `build_*.sh` の生成を検証。
   - `tests/cli/test_cli_css.py`, `tests/doc_builder/test_css.py`: 新しい `_templates` パッケージ構造に対応するテストへ更新。
   - `tests/l1_core/test_langs.py`: `drawlib._templates.langs` からのインポートに修正。
2. **内部ルール（Rules）ドキュメントの更新**:
   - `src/drawlib/_rules/project.md`
   - `src/drawlib/_rules/cli.md`
   - `src/drawlib/_rules/agent_instruction.md`
   に記載されているテンプレート種別・コマンド例・スクリプト一覧を更新。
3. **品質検証**:
   - `./dcli check all` (Ruff lint, Pyright, docstrings) が Exit Code 0 で通過することを確認。
   - `./dcli test all` (全ユニット・結合テスト) がパスすることを確認。

---

## 5. 移行に伴う変更点 (Breaking Changes Summary)

後方互換性を考慮しないため、以下のクリーンな仕様変更が適用されます：

1. **内部パッケージ構成**:
   - 廃止: `drawlib._css_templates`, `drawlib._project_templates`, `drawlib._langs`, `drawlib._builder.project_init`
   - 新設: `drawlib._templates`（公開 API、`builder.py`、`langs/`、`css/`、`project/`）
2. **プロジェクト初期化コマンド**:
   - 廃止: `drawlib init simple`, `drawlib init pdf`
   - 新設: `drawlib init doc`（仕様書、RFC、レポート、論文用）
3. **ビルドスクリプト構成**:
   - 各プロジェクト種別に用途別の `build_html.sh`, `build_pdf.sh`, `build_markdown.sh`, `build_image.sh` を配備。
   - `build.sh` はそれらを束ねる Master スクリプトとして機能。
4. **JavaScript エンジンの配置**:
   - `slide.js` は `css/` ではなく `_templates/project/slide/slide.js` に配置。
5. **テンプレート HTML**:
   - `template.html` 内のインライン CSS ハードコードを完全撤廃。すべてのスタイル定義は `style.css` / `slide.css` に集約。
