# Drawlib Markdown 構文統一計画書 (`key=value` キーワード引数スタイルへの刷新)
(DRAWLIB MARKDOWN SYNTAX UNIFICATION PLAN)

- **作成日**: 2026-10-11
- **対象バージョン**: Drawlib 次期リリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール・ディレクトリ**:
  - `src/drawlib/_builder/doc_builder/processor/options.py` (```` ```drawlib ```` / `<script type="text/drawlib">` オプションパーサー)
  - `src/drawlib/_builder/doc_builder/processor/parser.py` (コードブロック抽出・バリデーションエラーメッセージ)
  - `src/drawlib/_slide/_blocks.py` (`::: block` / `::: note` コンテナパーサー)
  - `src/drawlib/_slide/compiler.py` (スライドコンパイラのデフォルト `::: block` 自動ラップ)
  - `src/drawlib/_templates/project/` (`doc`, `site`, `slide` 初期テンプレート群)
  - `src/drawlib/_rules/` & `.agents/rules/` (AIエージェント向け組み込みルール・ガイドライン)
  - `docs/*_src/` (公式ドキュメント・ホワイトペーパー・スライドデッキ全ソース)
  - `tests/drawlib/doc_builder/`, `tests/drawlib/slide/`, `tests/drawlib/cli/` (単体テスト群)

---

## 1. エグゼクティブサマリー & 設計原則 (Executive Summary & Design Principles)

### 1.1. 背景と課題
Drawlib の Python API 側では、図形やコンポーネントの配置・サイズ指定を `xy=(x, y), width=w, height=h` という明示的なキーワード引数（`key=value`）に統一した。しかし、Markdown 内で使用する拡張構文（```` ```drawlib ```` コードフェンスおよび `::: block` スライドコンテナ）には以下の不整合が残っている。

1. **区切り文字・位置フラグ・無名タプルの混在**:
   - ```` ```drawlib center fold-code file:arch.png caption:"..." 650px no-cache ```` のように、キーなしの裸のフラグ（`center`, `fold-code`, `650px`）とコロン区切り（`file:arch.png`）が混在している。
   - `::: block (80, 140) (740, 840) font:22px center compact z:5` のように、2つの無名タプル `(x, y) (w, h)`（Python API で廃止した `size` タプル相当）とコロン区切り・位置フラグが混在している。
   - HTML 埋め込み（`<script type="text/drawlib" file="arch.png" width="650px">`）では `=` を使っており、Markdown（`:`）と記法が分裂している。
2. **部分指定の不可能性と自己記述性の欠如**:
   - `::: block (80, 140) (740, 840)` では、座標 `(80, 140)` をデフォルトのままにして `width` だけを変更するといった部分指定ができない。
3. **未使用のレガシーオプション（デッドコード）の残存**:
   - `DrawlibBlockOptions` に `slot`, `xy`, `size`, `z_index` が定義されているが、スライドのレイアウトが `::: block` に移行した現在、どこからも参照されていない。

### 1.2. 4つの基本設計原則（決定事項）

| # | 原則 | 内容 |
| :---: | :--- | :--- |
| **(1)** | **位置フラグ（短縮記法）の完全廃止** | `center`, `fold-code`, `compact`, `650px` などのキーなしフラグ記法を廃止し、**すべてのオプションを `key=value` 形式に一本化**する。 |
| **(2)** | **クォートの省略ルール** | `caption="Service Architecture"` のように**スペースを含む文字列はクォート必須**とし、`file=arch.png` や `align=center` のように**スペースを含まない値ではクォートあり・なしのどちらも許容**する（タプル `xy=(80, 140)` は括弧内スペースを許容）。 |
| **(3)** | **キー名の `snake_case` 統一** | Python の関数引数に合わせて、キー名はハイフンではなく **`snake_case`**（`font_size`, `z_index`, `no_cache`, `anim_trigger`, `anim_loop`, `anim_pause`）に統一する。 |
| **(4)** | **旧構文・別名の完全廃止** | コロン区切り（`key:value`）、無名タプル（`::: block (x, y) (w, h)`）、短縮キー別名（`w`, `h`, `z`, `fs`, `pos`, `dim` 等）は後方互換を残さず**完全廃止**する。 |

---

## 2. 新構文の完全仕様 (Complete Syntax Specification)

### 2.1. ```` ```drawlib ```` コードフェンス & `<script type="text/drawlib">`

#### 基本構文
````markdown
```drawlib file=service_arch.png caption="Service Architecture" align=center code=fold width=650px
from drawlib.canvas import save, setup
...
```
````

HTML `<script>` タグでもまったく同じ `key=value` 文法で記述する：
```html
<script type="text/drawlib" file="service_arch.png" caption="Service Architecture" align="center" code="fold">
from drawlib.canvas import save, setup
...
</script>
```

#### オプション一覧 (`DrawlibBlockOptions`)

| キー名 (`snake_case`) | 許容される値 | デフォルト値 | 説明 (`旧構文からの移行`) |
| :--- | :--- | :--- | :--- |
| **`file`** | 文字列 (例: `arch.png`, `"sub/arch.svg"`) | `None` (`doc`/`site` では必須) | 出力画像ファイル名（旧: `file:arch.png`） |
| **`caption`** | 文字列 (例: `"Service Architecture"`) | `None` | `<figcaption>` キャプション文字列（旧: `caption:"..."`） |
| **`align`** | `left` \| `center` \| `right` | `None` | 図表ブロックの水平配置（旧: 裸の `center` / `align:center`） |
| **`code`** | `hide` \| `show` \| `fold` | `"hide"` | Python ソースコードの表示モード（旧: `hide-code` / `show-code` / `fold-code`） |
| **`width`** | 数値または単位付き (例: `650px`, `80%`, `650`) | `None` | 表示幅。数値のみの場合は `px` を補完（旧: 裸の `650px` / `width:650px`） |
| **`height`** | 数値または単位付き (例: `400px`, `400`) | `None` | 表示高さ。数値のみの場合は `px` を補完（旧: `height:400px`） |
| **`format`** | `png` \| `webp` \| `svg` \| `apng` | `None` (ビルド設定に従う) | 出力画像フォーマット（旧: 裸の `webp` / `format:webp`） |
| **`class`** | 文字列 (例: `hero-fig`, `"hero-fig shadow"`) | `None` | ラッパー要素に付与する追加 CSS クラス（旧: `class:hero-fig`） |
| **`no_cache`** | `true` \| `false` | `false` | `true` のときビルドキャッシュを無効化（旧: 裸の `no-cache` / `cache:false`） |
| **`anim_trigger`** | `auto` \| `click` | `None` (`"auto"`) | アニメーション再生トリガー（旧: `anim-trigger:click` / `anim:click`） |
| **`anim_loop`** | `once` \| `infinite` | `None` (`"infinite"`) | アニメーションループ設定（旧: `anim-loop:once` / `loop:once`） |
| **`anim_pause`** | タプルまたは整数 (例: `(2, 4)` または `2`) | `None` | 一時停止するフレーム番号（旧: `anim-pause:2,4`） |

#### ```` ```drawlib ```` から削除する旧仕様・デッドコード
- **未使用フィールドの削除**: `DrawlibBlockOptions` の `slot`, `xy`, `size`, `z_index` フィールドおよびそのパース処理を削除。
- **裸のフラグ・位置トークンの削除**: `show-code`, `fold-code`, `hide-code`, `left`, `center`, `right`, `png`, `webp`, `svg`, `apng`, `no-cache`, 裸の `650px` / `80%`、無名タプル `(x, y)` / `(w, h)` を削除。
- **コロン区切り・別名キーの削除**: `:` 区切り、および `w`, `h`, `a`, `fmt`, `s`, `pos`, `dim`, `cache`, `anim`, `loop`, `pause` やハイフンつなぎキー（`anim-trigger`, `anim-loop`, `anim-pause`, `no-cache`）を削除。

---

### 2.2. `::: block`（スライド用ステージコンテナ）

#### 基本構文
```markdown
::: block xy=(80, 140) width=740 height=840 font_size=22px align=center compact=true z_index=5 class="card" style="padding: 16px;"
### セクション見出し
- 箇条書きアイテム
:::
```

引数をすべて省略した場合は、デフォルトのコンテンツ領域 `xy=(80, 140) width=1760 height=840` として配置される：
```markdown
::: block
### デフォルト領域 (xy=(80, 140), width=1760, height=840)
:::
```

#### オプション一覧 (`SlideBlockOptions`)

| キー名 (`snake_case`) | 許容される値 | デフォルト値 | 説明 (`旧構文からの移行`) |
| :--- | :--- | :--- | :--- |
| **`xy`** | 2要素数値タプル (例: `xy=(80, 140)`) | `(80.0, 140.0)` | ステージ左上 `(0, 0)` からの `(x, y)` ピクセル座標（旧: 第1無名タプル `(80, 140)`） |
| **`width`** | 数値または単位付き (例: `width=740`, `width=740px`) | `1760.0` | コンテナ幅（旧: 第2無名タプル `(740, 840)` の第1要素） |
| **`height`** | 数値または単位付き (例: `height=840`, `height=840px`) | `840.0` | コンテナ高さ（旧: 第2無名タプル `(740, 840)` の第2要素） |
| **`align`** | `left` \| `center` \| `right` | `None` | テキスト水平配置（旧: 裸の `center` / `align:center`） |
| **`font_size`** | 数値または単位付き (例: `font_size=22px`, `font_size=22`) | `None` | フォントサイズ上書き。数値のみの場合は `px` を補完（旧: `font:22px` / 裸の `22px`） |
| **`compact`** | `true` \| `false` | `false` | `true` のとき `.compact` クラスを付与し余白を圧縮（旧: 裸の `compact`） |
| **`z_index`** | 整数 (例: `z_index=5`) | `None` | CSS `z-index` レイヤー順序（旧: `z:5` / `z-index:5`） |
| **`class`** | 文字列 (例: `class=card`, `class="card highlight"`) | `None` | 追加 CSS クラス（旧: `class:"..."`） |
| **`style`** | 文字列 (例: `style="padding: 16px;"`) | `None` | 追加インライン CSS スタイル（旧: `style:"..."`） |

#### `::: block` から削除する旧仕様
- **無名タプル構文の削除**: `(x, y) (w, h)` の位置タプルパース（`parse_box_coordinates`）を削除。
- **裸のフラグの削除**: `compact`, `left`, `center`, `right`, 裸の `22px` 等（`handle_pos_box_token`）を削除。
- **コロン区切り・別名キーの削除**: `:` 区切り、および `font`, `font-size`, `fontsize`, `fs`, `z`, `z-index`, `text-align`, `css` を削除。
- **コンテナ別名 `::: box` の廃止**: `::: block` に一本化。

---

### 2.3. `::: note`（スライド用スピーカーノート）

- **基本構文**:
  ```markdown
  ::: note
  プレゼンタービューに表示するスピーカーノート。
  :::
  ```
- 別名 `::: notes` を廃止し、`::: note` に統一する。

---

## 3. パーサー実装設計 (Parser Implementation Design)

### 3.1. 共通 `key=value` トークナイザーの設計
`xy=(80, 140)` や `anim_pause=(2, 4)` のように、丸括弧 `(...)` の内部にカンマとスペースを含むタプル表現を `shlex.split` で分割させないため、以下の2ステップでトークン化するヘルパー関数を作成する。

```python
_PAREN_GROUP_RE = re.compile(r"\([^()]*\)")

def tokenize_kv_pairs(info_str: str) -> list[tuple[str, str]]:
    """Parse space-separated key=value tokens while preserving whitespace inside parentheses (...) and quotes."""
    # 1. Normalize spaces inside (...) so shlex treats key=(a, b) as a single token
    normalized = _PAREN_GROUP_RE.sub(lambda m: re.sub(r"\s+", "", m.group(0)), info_str.strip())
    if not normalized:
        return []
    try:
        tokens = shlex.split(normalized, posix=True)
    except ValueError:
        tokens = normalized.split()

    pairs: list[tuple[str, str]] = []
    for token in tokens:
        if "=" not in token:
            continue
        key, val = token.split("=", 1)
        key_clean = key.strip()
        val_clean = val.strip().strip('"').strip("'")
        if key_clean:
            pairs.append((key_clean, val_clean))
    return pairs
```
- これにより：
  - `xy=(80, 140)` → `("xy", "(80,140)")` として安全に1トークンで抽出される。
  - `caption="Service Architecture"` → `("caption", "Service Architecture")` として抽出される。
  - `file=arch.png` も `file="arch.png"` も → `("file", "arch.png")` として同一に抽出される。
  - `=` を含まない裸のフラグ（`center`, `fold-code`, `(80, 140)` 等）は無視（または廃止）される。

### 3.2. `src/drawlib/_builder/doc_builder/processor/options.py` の刷新
- `DrawlibBlockOptions` から `slot`, `xy`, `size`, `z_index` を削除。
- `parse_block_info(info_str: str) -> DrawlibBlockOptions` を上記 `tokenize_kv_pairs` ベースに書き換え、Section 2.1 の12個の正規キーのみを処理するシンプルで明快な関数（約80行）にスリム化する。
- `resolve_block_image_paths` および `parser.py` の必須ファイル名エラーメッセージを以下のように更新：
  - `"Missing required 'file=<filename.ext>' option in drawlib code block at line {line_number}. Example: ```drawlib file=my_diagram.png"`

### 3.3. `src/drawlib/_slide/_blocks.py` & `compiler.py` の刷新
- `PATTERN_CONTAINER_BOX` を `r"(?:\n|^)[ \t]*:::+[ \t]*block(?:\s+([^\n]*))?\n(.*?)\n[ \t]*:::+"` に変更（`box` 別名を廃止）。
- `PATTERN_SLIDE_NOTE` を `r"(?:\n|^)[ \t]*:::+[ \t]*note(?:[ \t]+[^\n]*)?\n(.*?)\n[ \t]*:::+"` に変更（`notes` 別名を廃止）。
- `parse_box_coordinates` と `parse_box_tokens` を統合し、`SlideBlockOptions`（または `parse_block_container_options(header_opts: str)`）として `xy`, `width`, `height`, `align`, `font_size`, `compact`, `z_index`, `class`, `style` を `key=value` でパースする。
- `src/drawlib/_slide/compiler.py` (L299) の自動ラップ処理を以下に更新：
  ```python
  text_to_search = f"::: block xy=(80, 140) width=1760 height=840\n{text_to_search.strip()}\n:::"
  ```

---

## 4. 影響範囲と移行対象ファイル一覧 (Impact & Migration Scope)

### 4.1. ライブラリ本体 (`src/drawlib/`)
1. [`src/drawlib/_builder/doc_builder/processor/options.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_builder/doc_builder/processor/options.py)
2. [`src/drawlib/_builder/doc_builder/processor/parser.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_builder/doc_builder/processor/parser.py)
3. [`src/drawlib/_slide/_blocks.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_slide/_blocks.py)
4. [`src/drawlib/_slide/compiler.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/src/drawlib/_slide/compiler.py)

### 4.2. プロジェクトテンプレート (`src/drawlib/_templates/project/`)
- `doc/docs/{en,ja}/*.md` 内の ```` ```drawlib ```` ヘッダー更新
- `site/docs/{en,ja}/**/*.md` 内の ```` ```drawlib ```` ヘッダー更新
- `slide/docs/{en,ja}/*.md` 内の `::: block` および ```` ```drawlib ```` ヘッダー更新

### 4.3. AIエージェントルール (`src/drawlib/_rules/` & `.agents/rules/`)
- `.agents/rules/drawlib.md`, `.agents/rules/docs.md`
- `src/drawlib/_rules/agent_instruction.md`
- `src/drawlib/_rules/overview.md`, `review_guide.md`, `style_guide.md`, `anim_guide.md`, `slide_guide.md`
- `src/drawlib/_rules/project_overview.md`, `project_doc.md`, `project_site.md`, `project_slide.md`, `project_images.md`
- `src/drawlib/_rules/cli.md`, `api.md`, `lib_*.md` 内の ```` ```drawlib ```` / `::: block` サンプルコード

### 4.4. 公式ドキュメント・ドッグフーディングプロジェクト (`docs/*_src/`)
1. `docs/docs_src/`（全章の ```` ```drawlib ```` フェンス、特に `08_doc_builder_and_cli/code_blocks.md`, `slide_layout_and_api.md`, `project_*.md` の構文解説ページ）
2. `docs/quickstart_src/`
3. `docs/drawlib-dogfooding_src/` & `docs/drawlib-dogfooding-en_src/`
4. `docs/architecture_src/`
5. `docs/slide_about_drawlib_src/`（全スライドの `::: block` と ```` ```drawlib ````）
6. `docs/slide_ddos_incident_response_src/`（全スライドの `::: block` と ```` ```drawlib ````）

### 4.5. テストスイート (`tests/drawlib/`)
1. [`tests/drawlib/doc_builder/test_processor.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/doc_builder/test_processor.py)
2. [`tests/drawlib/doc_builder/test_compiler.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/doc_builder/test_compiler.py)
3. [`tests/drawlib/doc_builder/test_build_cache.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/doc_builder/test_build_cache.py)
4. [`tests/drawlib/slide/test_slide.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/slide/test_slide.py)
5. [`tests/drawlib/cli/test_cli_build.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/cli/test_cli_build.py), [`test_cli_show.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/cli/test_cli_show.py), [`test_cli_export.py`](file:///usr/local/google/home/yuichiito/git_github/drawlib/tests/drawlib/cli/test_cli_export.py)

---

## 5. 実装フェーズと検証計画 (Implementation & Verification Roadmap)

1. **Phase 1: パーサーの刷新 (`options.py`, `parser.py`, `_blocks.py`, `compiler.py`)**
   - `tokenize_kv_pairs` の実装と、`DrawlibBlockOptions` / `::: block` パーサーの `key=value` 化および旧構文削除。
2. **Phase 2: 単体テストの更新と実行 (`tests/drawlib/`)**
   - `doc_builder`, `slide`, `cli` の単体テストを新構文に合わせて更新し、旧構文が受け付けられないことも検証。
   - `./dcli test target doc-builder`, `./dcli test target slide`, `./dcli test target cli` を実行。
3. **Phase 3: テンプレートと組み込みルールの更新 (`_templates/`, `_rules/`, `.agents/rules/`)**
   - `drawlib init` で生成されるすべてのテンプレート Markdown と、`drawlib rules` の全ドキュメントを新構文（`file=... caption="..." align=center code=fold` / `::: block xy=(...) width=... height=...`）に一括更新。
4. **Phase 4: ドッグフーディング・ドキュメント (`docs/*_src/`) の全面移行**
   - `docs/*_src/` 配下の全 Markdown ファイルの ```` ```drawlib ```` ヘッダーおよび `::: block` ヘッダーを新構文に変換。
   - 構文リファレンスページ（[`code_blocks.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/docs/docs_src/08_doc_builder_and_cli/code_blocks.md), [`slide_layout_and_api.md`](file:///usr/local/google/home/yuichiito/git_github/drawlib/docs/docs_src/08_doc_builder_and_cli/slide_layout_and_api.md) 等）の解説表と図解内ラベルを新構文に更新。
5. **Phase 5: 全体品質チェック・全ドキュメントビルド・テスト検証**
   - `./dcli code-check all`
   - `./dcli test all --no-cov`
   - `./dcli docs build --all`
   - `./dcli docs serve site --check`
