# Drawlib テンプレート・CSS・ドキュメント統合リファクタリング計画書
(TEMPLATE REFACTORING PLAN)

- **作成日**: 2026-10-04
- **対象バージョン**: Drawlib 次期リリース
- **前提条件**: **後方互換性の維持は不要**（最善のアーキテクチャ設計・DRY原則を最優先とする）

---

## 1. エグゼクティブサマリー & ゴール

Drawlib の機能拡充に伴い、テンプレート（`site`, `simple`, `pdf`, `slide`, `image`）および CSS（HTML用、PDF用、Slide用）の種類が増加し、コードの重複と概念の分断が顕著になっています。

本リファクタリングの目的は以下の3点です：

1. **CSS の共通化（3層レイヤードCSSアーキテクチャ）**:
   媒体ごとにコピー＆ペーストされていた Markdown 装飾、タイポグラフィ、コードハイライトを共通化し、テーマ（Google, Default, Monochrome 等）をデザイン・トークンとして一元化する。
2. **線形ドキュメントの統合（`simple` と `pdf` を `doc` に一本化）**:
   同じ「1本の線形ドキュメント（仕様書/レポート/論文）」である `simple`（HTML専用）と `pdf`（PDF専用）を統合し、同一ソースから HTML と PDF の両方をシームレスにビルド可能にする。
3. **フォルダ構成の集約と責務の明確化**:
   `_project_templates`（プロジェクト初期化の足場）と `_css_templates`（描画エンジンのテーマ資産）の責務を整理し、重複アセットやインラインCSSの直書きを徹底的に排除する。

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

### 2.2. プロジェクトテンプレート (`src/drawlib/_project_templates/`) の課題

- **`simple` と `pdf` の不自然な分断**:
  - `simple`: `docs_src/doc.md` を起点に `drawlib build html` と `drawlib build markdown` を実行。PDF は出力できない。
  - `pdf`: `docs_src/00_cover.md`, `01_overview.md` などを起点に `drawlib build pdf` を実行。HTML は出力できない。
  - **実態**: 仕様書や技術文書、RFC、論文などを作成する場合、「Web で閲覧するための HTML」と「印刷・配布用の PDF」の両方を同一ソースから生成したいケースが標準的であり、媒体によってテンプレートを分ける必然性がない。
- **テンプレートファイルの重複**:
  - 各種別に `build.sh.template`、`serve.sh.template`、`template.html.template` が重複して配置されている。

### 2.3. CLI・ビルドエンジンの課題

- **入力の非対称性**:
  - `drawlib build pdf` はディレクトリしか入力に取れず、単一の `doc.md` を渡すとエラーになる。
  - `drawlib build html` は `navbar.md` がない場合は個別ファイルごとに単一 HTML を出力するが、章立ての複数 Markdown を結合した 1 本の HTML を出力する標準フローが存在しない。

---

## 3. 目指すアーキテクチャ (To-Be Architecture)

### 3.1. 3層レイヤード CSS アーキテクチャ

CSS の関心を **「テーマ・トークン」「コンポーネント装飾」「ターゲット・シェル」** の 3 層に分離します。

```text
src/drawlib/_css_templates/
├── themes/                 # [Layer 1] パレット・フォントのCSS変数（各約30行）
│   ├── default.css.template
│   ├── default-dark.css.template
│   ├── google.css.template
│   ├── google-dark.css.template
│   ├── monochrome.css.template
│   └── github.css.template
│
├── components/             # [Layer 2] 全媒体共通のコンテンツ装飾ルール
│   ├── markdown.css        #   見出し、段落、表、引用、リスト、Admonition
│   └── code.css            #   コードハイライト、行番号、インラインコード
│
├── targets/                # [Layer 3] 媒体固有のレイアウト・メディア制御
│   ├── site.css            #   サイドバー、階層ナビゲーション、レスポンシブWeb
│   ├── doc.css             #   単一ドキュメント用センタリング・リーディングビュー
│   ├── pdf.css             #   @page (A4), 改ページ制御, 印刷用フォントサイズ
│   └── slide.css           #   1920x1080固定ステージ、縮小拡大ビューポート、スライドUI
│
└── scripts/
    └── slide.js            #   スライドエンジン用 vanilla JavaScript
```

#### 合成・配信の仕組み (`get_css`)
`get_css(name=theme, target=target, lang=lang)` を呼び出すと、内部で以下をマージして単一のスタンドアロン CSS を生成します：

$$\text{Output CSS} = \text{Layer 1 (Theme)} + \text{Layer 2 (Components)} + \text{Layer 3 (Target Layout)}$$

- **効果**:
  - 新規テーマ（例: `nord`, `dracula`）を追加する場合、`themes/` に 1 ファイル（約 30 行）追加するだけで、**HTML・PDF・Slide の全媒体で即座に利用可能** になる。
  - 表や Admonition のデザイン修正が全媒体に自動反映される。
  - テンプレート内の CSS コード総量を約 **70% 削減**。

---

### 3.2. プロジェクト種別の集約（4つの直交モデル）

プロジェクト種別を、明確に用途が異なる **4 つの種別** に再編します。

| プロジェクト種別 | 用途・特徴 | 主な出力物 |
| :--- | :--- | :--- |
| **`site`** | 階層構造とサイドバーナビ（`navbar.md`）を持つドキュメントサイト | `docs_html/` (複数ページ HTML), `docs/` |
| **`doc`** *(新設・統合)* | 仕様書、レポート、論文、RFC などの線形ドキュメント | `doc.html` (Web), `doc.pdf` (Print), `doc.md` |
| **`slide`** | 16:9 スライドプレゼンテーションデッキ | `slide/index.html`, `slide/images/` |
| **`image`** | Python スクリプトによる純粋なイラスト・図版一括生成 | `images/*.png`, `images/*.webp` |

#### `doc` テンプレートの柔軟性
- **単一ファイル構成**: `docs_src/doc.md`
- **章立て構成**: `docs_src/00_cover.md`, `docs_src/01_overview.md`, `docs_src/02_architecture.md`
- どちらの構成でも同一の `doc` テンプレートとして動作し、`build.sh` 1 回で HTML / PDF / Markdown のすべてを生成可能。

---

### 3.3. `_project_templates/` の新ディレクトリ構成

```text
src/drawlib/_project_templates/
├── _assets/                # 共通画像アセット (linux.png 等)
├── _shared/                # 共通 Python スクリプト (styles.py.template, utils.py)
│
├── site/                   # Web ドキュメントサイト
│   ├── docs/ (en, ja)
│   ├── build.sh.template
│   ├── serve.sh.template
│   └── template.html.template (※インラインCSS直書きを廃止したクリーンなHTML)
│
├── doc/                    # [統合] 線形ドキュメント (旧 simple + pdf)
│   ├── docs/ (en, ja)
│   │   ├── en/ (00_cover.md, 01_overview.md, 02_design.md, README.md)
│   │   └── ja/ (00_cover.md, 01_overview.md, 02_design.md, README.md)
│   ├── build.sh.template   # HTML, PDF, Markdown を一括生成
│   ├── serve.sh.template
│   └── template.html.template
│
├── slide/                  # スライドプレゼンテーション
│   ├── docs/ (en, ja)
│   ├── utils/              # スタイル別 utils.py テンプレート
│   ├── build.sh.template
│   └── serve.sh.template
│
└── image/                  # Python 画像バッチ生成
    ├── docs/ (en, ja)
    └── build.sh.template
```

---

## 4. 詳細実装タスク (Action Items & WBS)

### Phase 1: CSS のリファクタリングと 3 層レイヤー化

1. **デザイン・トークン体系の標準化 (`themes/`)**:
   - 変数プレフィックスを統一（`--dl-brand`, `--dl-brand-dark`, `--dl-text`, `--dl-bg`, `--dl-border`, `--dl-code-*`, `--dl-font`, `--dl-mono-font`）。
   - `themes/default.css.template`, `google.css.template`, `monochrome.css.template`, `github.css.template`, `*-dark.css.template` を作成。
2. **共通コンポーネントの抽出 (`components/`)**:
   - `components/markdown.css`: H1〜H6、Table、Blockquote、List、Admonition (`.admonition`, `.note`, `.tip`, `.warning` 等)、画像キャプション。
   - `components/code.css`: シンタックスハイライト、行番号表示、インラインコードタグ。
3. **ターゲット・シェルの抽出 (`targets/`)**:
   - `targets/site.css`: サイドバー、検索、ハンバーガーメニュー、レスポンシブコンテナ。
   - `targets/doc.css`: 単一ドキュメント用の美しい中央揃えレイアウト（最大幅 900px、クリーンな読書ビュー）。
   - `targets/pdf.css`: `@page { size: A4; margin: 18mm 16mm; }`、`break-inside: avoid;`、ページフッター/ヘッダー。
   - `targets/slide.css`: 1920x1080 固定ステージ、全画面縮小拡大ビューポート、ナビゲーション操作UI。
4. **合成ローダー (`_css_templates/__init__.py`) の改修**:
   - `get_css(name, target, lang)` の実装を「トークン + コンポーネント + ターゲットレイアウト」の連結合成に変更。
   - `list_css(target)` を更新。
   - 既存の冗長な 19 個の CSS テンプレートファイルを安全に削除。

---

### Phase 2: 線形ドキュメント `doc` の統合とテンプレート整備

1. **`doc` テンプレートの作成**:
   - `_project_templates/doc/` を新設。
   - 日本語・英語のスターター文書（カバー、概要、アーキテクチャ設計サンプル）を配備。
2. **統合 `build.sh.template` の作成**:
   - Markdown 生成（`drawlib build markdown`）
   - HTML 生成（`drawlib build html`）
   - PDF 生成（`drawlib build pdf`）
   をシームレスに実行するスクリプトを記述。
3. **`template.html.template` のクリーン化**:
   - `site/template.html.template` および `doc/template.html.template` 内の数百行に及ぶフォールバック `<style>` 直書きを削除。
   - `css_href` または合成された `custom_css` のみを読み込む簡潔なテンプレートに統一。
4. **旧テンプレートの削除**:
   - `_project_templates/simple/` を削除。
   - `_project_templates/pdf/` を削除。
5. **`project_init.py` の更新**:
   - `PROJECT_TYPES` の定義を `site`, `doc`, `slide`, `image` の 4 種に更新。
   - `init_project(project_type="doc", ...)` の初期化ルーチンを実装。

---

### Phase 3: ビルドエンジンおよび CLI の機能拡張

1. **`drawlib build pdf` の単一ファイル対応**:
   - `src/drawlib/_builder/doc_builder/compiler/pdf.py` および `merger.py`:
     ディレクトリだけでなく、単一の Markdown ファイル（例: `doc.md`）も引数として直接受け取れるように拡張。
2. **`drawlib build html` の線形ドキュメント対応**:
   - ディレクトリ内に `navbar.md` が存在しない場合でも、章立てファイル群（`00_cover.md`, `01_...`）を検出した際に、単一の結合 HTML（`doc.html`）を生成可能にする（または結合 HTML 出力オプションの提供）。
3. **CLI コマンド・ヘルプの更新**:
   - `drawlib init list` の出力更新（`simple`, `pdf` を削除し `doc` を表示）。
   - `drawlib build` の引数検証メッセージの整備。

---

### Phase 4: テスト・ドキュメント・サンプルの更新

1. **テストコードの改修**:
   - `tests/cli/test_cli_init.py`: `simple`, `pdf` 関連テストを `doc` に更新。
   - `tests/cli/test_cli_css.py`, `tests/doc_builder/test_css.py`: 新しい CSS プリセット構造（`themes/`, `components/`, `targets/`）に対応するテストへ更新。
2. **内部ルール（Rules）ドキュメントの更新**:
   - `src/drawlib/_rules/project.md`
   - `src/drawlib/_rules/cli.md`
   - `src/drawlib/_rules/agent_instruction.md`
   に記載されているテンプレート種別・コマンド例を更新。
3. **品質検証**:
   - `./dcli check all` (Ruff lint, Pyright, docstrings) が Exit Code 0 で通過することを確認。
   - `./dcli test all` (全ユニット・結合テスト) がパスすることを確認。

---

## 5. 移行に伴う変更点 (Breaking Changes Summary)

後方互換性を考慮しないため、以下のクリーンな仕様変更が適用されます：

1. **プロジェクト初期化コマンド**:
   - 廃止: `drawlib init simple`, `drawlib init pdf`
   - 新設: `drawlib init doc`（仕様書、RFC、レポート、論文用）
2. **CSS プリセット管理**:
   - ターゲット別ファイル管理（`html/default.css` 等）から、統合テーマ（`default`, `google`, `monochrome`, `github` 等）× ターゲット（`site`, `doc`, `pdf`, `slide`）の直交マトリクスへ移行。
3. **テンプレート HTML**:
   - `template.html` 内のインライン CSS ハードコードを完全撤廃。すべてのスタイル定義は `style.css` / `slide.css` に集約。
