# Slide & SVG Font Auto-Bundling Implementation Plan (`slide_font_bundle_plan.md`)

## 1. 背景と解決すべき課題

Drawlib のスライドビルド（`drawlib build slide`）および SVG 出力（`format:svg` / `--image-format svg`）では、`matplotlib.rcParams["svg.fonttype"] = "none"` によりテキストを `<text>` 要素として出力している。しかし現在、以下の **2つの根本課題** により、指定したフォントやアイコンフォント（`Phosphor` 等）が SVG 表示時に正しく反映されない状態にある。

### 課題 1: Matplotlib の SVG 出力仕様による `font-family` の欠落
- 現在 `TextUtil.get_font_properties()`（`src/drawlib/_core/l4_canvas/_text_util.py`）では、`FontProperties(size=style.text_size, fname=file_path)` のようにファイルパス（`fname`）のみを指定している。
- PNG / WebP（`backend_agg`）では `prop.get_file()` を直接参照して `.ttf` / `.otf` を描画するが、SVG（`backend_svg`）の `_draw_text_as_text()` は `fname` を無視し、`prop.get_family()` を参照して CSS の `font-family` を出力する。
- `family` が未指定のため、すべての `<text>` 要素が `<text style="font-family: 'DejaVu Sans', ..., sans-serif">` として出力されてしまっている。

### 課題 2: 出力先 `_assets/fonts/` へのフォント配置と `@font-face` 定義の欠如
- SVG の `<text>` に正しいフォント名が出力されても、閲覧環境の OS にそのフォント（特に `Phosphor` 等のアイコンフォントや、`Roboto`, `Poppins`, `Noto Sans CJK JP`, `M PLUS` 等の組み込みフォント、ユーザー指定の `FontFile`）がインストールされていなければ表示できない。
- また、Drawlib（Matplotlib）は描画時にローカルの `.ttf` / `.otf` の厳密なメトリクス（文字幅・ベースライン）を使って背景ボックスや中央揃え座標を計算するため、ブラウザ側で OS フォントにフォールバックすると座標ズレ（ボックスからのはみ出し等）が生じる。

---

## 2. 設計方針（フォント名・ファイル名の重複防止と汎用性）

将来フォントやアイコンフォントを追加した際にもコード改修なしで自動追従でき、かつ **フォント名・ファイル名の衝突が 100% 発生しない設計** とする。

### 2.1. CSS `font-family` 名の重複防止（1ファイル＝1固有エイリアス名）

同じフォントファミリーのウェイト違い（`thin.ttf`, `regular.ttf`, `bold.ttf`）や、内部 TTF ファミリー名が同一の複数カスタムフォント、あるいは HTML ページ側で読み込んでいる Google Fonts 等との干渉・ブラウザの擬似ボールド（faux-bold）を防ぐため、**フォントファイルと 1対1 で対応する固有の `font-family` 名** を付与する。

- **第1候補（固有エイリアス名）**: `drawlib-` プレフィックス付きのファイル固有識別子
- **第2候補（フォールバック名）**: フォントファイル内部の本来の TTF ファミリー名（`FT2Font(path).family_name`。単体 SVG 閲覧時のフォールバック用）

| フォント種別 | 元ファイルの相対/絶対パス | 第1候補（固有 `font-family`） | 第2候補（TTF 内部名） | `_assets/fonts/` 内の配置パス |
| :--- | :--- | :--- | :--- | :--- |
| **標準フォント** | `fonts/roboto/bold.ttf` | `'drawlib-roboto-bold'` | `'Roboto'` | `_assets/fonts/roboto/bold.ttf` |
| **日本語フォント** | `fonts/cjk_japanese_noto_sans/regular.otf` | `'drawlib-cjk_japanese_noto_sans-regular'` | `'Noto Sans CJK JP'` | `_assets/fonts/cjk_japanese_noto_sans/regular.otf` |
| **アイコンフォント**| `fonticons/phosphor/thin.ttf` | `'drawlib-phosphor-thin'` | `'Phosphor-Thin'` | `_assets/fonts/phosphor/thin.ttf` |
| **カスタム `FontFile`**| `/path/to/myfont.ttf` | `'drawlib-custom-<md5_8>'` | `'<TTF内部名>'` | `_assets/fonts/custom/<md5_8>_myfont.ttf` |

#### SVG 内の `<text>` 出力例
```xml
<text style="font-size: 16px; font-family: 'drawlib-roboto-bold', 'Roboto'; text-anchor: start" ...>Hello</text>
<text style="font-size: 24px; font-family: 'drawlib-phosphor-thin', 'Phosphor-Thin'; text-anchor: middle" ...>&#xe406;</text>
```

#### `@font-face` の出力例（`style.css`）
各フォントファイルが固有の `font-family` 名を持つため、`font-weight: normal; font-style: normal;` で統一でき、ブラウザによる意図しない擬似ボールド合成やウェイト番号の不一致を完全に排除できる。

```css
/* Auto-bundled Drawlib SVG Fonts */
@font-face {
  font-family: 'drawlib-roboto-bold';
  src: url('_assets/fonts/roboto/bold.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}
@font-face {
  font-family: 'drawlib-phosphor-thin';
  src: url('_assets/fonts/phosphor/thin.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
  font-display: block;
}
```

### 2.2. `_assets/fonts/` 内のファイル名重複防止
- Drawlib のフォントファイルはすべて `thin.ttf`, `regular.ttf`, `bold.ttf` という同名ファイルであるため、フラットにコピーせず **サブディレクトリ構造（`<family_dir>/<weight>.ttf`）を維持** して `_assets/fonts/` 配下に配置する。
- ユーザー指定の `FontFile` については、ファイル内容（またはパス）の MD5 先頭8文字を付与し、`_assets/fonts/custom/<md5_8>_<basename>` として配置することで、異なるディレクトリにある同名ファイル同士の衝突も防ぐ。
- プロジェクトのソースディレクトリ（`input_dir/_assets/`）にユーザー自身の静的アセットが存在する場合は、それを先にコピーした上で、不足しているフォントファイルを `_assets/fonts/` にマージ追加する（既存ファイルを消去しない）。

---

## 3. 実装アーキテクチャ（3ステップ）

### Step 1: フォント識別子解決と `FontProperties` 生成の拡張
**対象ファイル**: `src/drawlib/_core/l4_canvas/_text_util.py`（および補助モジュール）

1. フォントファイルの絶対パス `abs_path` から以下の情報を解決するキャッシュ付き関数 `resolve_svg_font_info(abs_path: str) -> SvgFontInfo` を実装する：
   - `unique_family`: CSS 用の固有ファミリー名（例: `'drawlib-roboto-bold'`, `'drawlib-phosphor-thin'`, `'drawlib-custom-a1b2c3d4'`）
   - `ttf_family`: `matplotlib.ft2font.FT2Font(abs_path).family_name` から取得した本来のファミリー名
   - `rel_bundle_path`: 出力先ディレクトリからの相対パス（例: `_assets/fonts/roboto/bold.ttf`）
   - `abs_source_path`: コピー元の絶対パス `abs_path`
   - `font_format`: `'truetype'` (`.ttf`), `'opentype'` (`.otf`), `'woff'` (`.woff`), `'woff2'` (`.woff2`)
2. `TextUtil.get_font_properties(style)` において、`FontProperties` を生成する際に `fname=file_path` と合わせて `family=[info.unique_family, info.ttf_family]` を設定する。
   - ※ Matplotlib の `findfont()` は `fname`（`prop.get_file()`）が設定されている場合は最優先で `fname` を返すため、既存の PNG / WebP 描画および SVG の文字幅・座標計算には一切影響しない。

### Step 2: SVG 保存時の使用フォントメタデータ埋め込み（ビルドキャッシュ対応）
**対象ファイル**: `src/drawlib/_core/l4_canvas/_canvas.py`, `src/drawlib/_builder/doc_builder/processor/processor.py`

1. **課題**: 2回目以降のビルドでは `BuildImageCache`（SQLite）からキャッシュ済みの `.svg` バイト列が直接ファイルに書き出されるため、Python コードブロックが再実行されない。
2. **解決策**:
   - `Canvas.save()` で `.svg` ファイルを保存する際、`self._artists` 内のすべての `matplotlib.text.Text` オブジェクトを走査し、使用されているフォントの `SvgFontInfo` リストを収集する。
   - 保存された `.svg` ファイルの末尾（`</svg>` の直前）に、使用フォント情報を JSON コメント（例: `<!-- drawlib-svg-fonts: [{"family": "drawlib-phosphor-thin", "rel_path": "_assets/fonts/phosphor/thin.ttf", "src_path": "...", "format": "truetype"}] -->`）として埋め込む。
   - ※ `src_path` について、ポータビリティ（別マシンや環境でのキャッシュ利用）を考慮し、Drawlib 組み込みフォント（`_assets/fonts/`）・アイコンフォント（`_assets/fonticons/`）はパッケージ相対識別子（`builtin:fonts/roboto/bold.ttf`, `builtin:fonticons/phosphor/thin.ttf`）として記録し、展開時に現在の `drawlib._assets` パスへ解決する。必要であれば `download_if_not_exist()` も自動実行する。
   - ※ `BuildImageCache` のキャッシュキー計算（またはバージョンソルト）に SVG フォントメタデータ対応の識別子を含め、旧形式のキャッシュ（`DejaVu Sans` になっている SVG）が自動的に再生成されるようにする。

### Step 3: スライド・HTML ビルド時の `_assets/fonts/` バンドルと `@font-face` 注入
**対象ファイル**:
- `src/drawlib/_slide/_assets.py`
- `src/drawlib/_slide/compiler.py`
- `src/drawlib/_builder/doc_builder/compiler/html.py`

1. 共通ユーティリティ関数 `bundle_svg_fonts(output_abs: str, svg_files: Iterable[str], css_file_path: str) -> None` を作成する：
   - 出力ディレクトリ内の生成された `.svg` ファイル群から `<!-- drawlib-svg-fonts: ... -->` メタデータを抽出・集約する（重複は `unique_family` キーで排除）。
   - 各フォントについて、コピー元ファイル（未ダウンロードの場合は `download_if_not_exist` で取得）を `<output_abs>/_assets/fonts/...` へコピーする。
   - 出力先の `style.css` に対して、集約されたフォントの `@font-face` ルールを生成して追記する（`css_file_path` からの相対 URL `url('_assets/fonts/...')` を使用）。
2. **`build_slide` での呼び出し**:
   - 全スライドの描画ブロック処理および `deploy_slide_assets()` 完了後に、出力ディレクトリ内の全 `.svg` を対象として `bundle_svg_fonts()` を実行する。
   - ※ `deploy_slide_assets()` で `input_abs/_assets` をコピーした後に実行するため、`_assets/fonts/` が上書き消去されることはない。
3. **`build_html` での呼び出し**:
   - ドキュメントサイト（`site` / `doc`）でも `format:svg` や `--image-format svg` が使われた場合に、出力先ディレクトリ内の `.svg` を走査して同様に `_assets/fonts/` へのコピーと `style.css`（またはインライン `<style>`）への `@font-face` 注入を行う。

---

## 4. 変更対象ファイル一覧

| ファイルパス | 変更内容 |
| :--- | :--- |
| `src/drawlib/_core/l4_canvas/_text_util.py` | `resolve_svg_font_info()` の実装、`TextUtil.get_font_properties()` で `family=[unique_family, ttf_family]` を設定 |
| `src/drawlib/_core/l4_canvas/_canvas.py` | SVG 保存時に `self._artists` から使用フォントを収集し、`<!-- drawlib-svg-fonts: ... -->` を SVG に埋め込む処理を追加 |
| `src/drawlib/_builder/_common/cache.py` | キャッシュキー計算に SVG フォント仕様バージョンソルトを追加（旧 SVG キャッシュの自動無効化） |
| `src/drawlib/_slide/_assets.py` | SVG からのフォントメタデータ抽出、`_assets/fonts/` へのファイルコピー、`style.css` への `@font-face` 注入関数を追加 |
| `src/drawlib/_slide/compiler.py` | スライドビルド完了時に SVG フォントバンドル処理を呼び出し |
| `src/drawlib/_builder/doc_builder/compiler/html.py` | HTML ドキュメントビルド時にも SVG が存在する場合はフォントバンドル処理を呼び出し |
| `tests/drawlib/` | SVG 出力時の `font-family` 検証、スライドビルド時の `_assets/fonts/` 生成および `style.css` の `@font-face` 出力のユニットテスト追加 |

---

## 5. 検証ステップ

1. **ユニットテスト (`./dcli test target ...`)**:
   - 通常フォント（`Font.SANSSERIF_REGULAR`, `FontRoboto.ROBOTO_BOLD` 等）、アイコンフォント（`phosphor`）、カスタム `FontFile` を用いて SVG 保存した際、`<text>` の `font-family` に固有エイリアス名が出力され、メタデータコメントが記録されることを確認。
   - `build_slide` 実行時に、使用されたフォントのみが `<output_dir>/_assets/fonts/` にコピーされ、`style.css` に `@font-face` が記述されることを確認。
   - 2回目の `build_slide`（キャッシュヒット時）でも同じく `_assets/fonts/` と `@font-face` が正しく生成されることを確認。
2. **コード品質チェック (`./dcli code-check all`)**:
   - Ruff lint / format、Ty 型チェック、docstring チェックをすべてパスすることを確認。
3. **ドッグフーディング & 視覚確認 (`./dcli docs build slide`)**:
   - `slide_about_drawlib_src/` をビルドし、`slide_about_drawlib_html/_assets/fonts/` に使用フォントが配置され、ブラウザおよび PDF 出力でテキスト・アイコンフォントが正確に表示されることを確認。
