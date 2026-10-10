# Drawlib ドキュメントサイト

このディレクトリには、マルチページ構成のドキュメントサイト用の Markdown ソース、図面コード、および各種設定が含まれています。

> [!TIP]
> **詳細なルールや機能ガイドを確認したい場合**  
> 図面の描き方、API 仕様、推奨設計ガイドラインの詳細については、以下のコマンドを実行してください:
> - `uv run drawlib rules show overview` : 描画マニュアル & AI 自己修正ループ
> - `uv run drawlib rules show docs_build`: 複数ページ構成、navbar ルール、ビルド仕様
> - `uv run drawlib rules show styles`    : 動的テーマ設定、`styles.py` および `utils.py` の詳細
> - `uv run drawlib rules list`          : 利用可能な全 20 以上のルールトピック一覧

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: Markdown ソースドキュメントおよび図面コード (**正本**)。
  - `build.sh`: HTML、Markdown、画像を順次ビルドするマスター統合スクリプト。
  - `build_html.sh`: 静的 HTML サイトのビルドスクリプト。
  - `build_markdown.sh`: GitHub 閲覧用 Markdown のビルドスクリプト。
  - `build_image.sh`: 単体図解画像の一括抽出スクリプト。
  - `serve.sh`: ローカルプレビュー用 HTTP サーバースクリプト。
  - `styles.py`: 全体描画テーマ、パレット、日本語フォント設定スクリプト。
  - `utils.py`: 再利用可能な描画ヘルパー関数、マクロ、プロジェクト共通定数。
  - `style.css`: HTML サイト用カスタム CSS スタイルシート。
  - `template.html`: HTML サイト用 Jinja2 テンプレート。
  - `navbar.md`: ナビゲーションサイドバーの階層構造定義。
  - `README.md`: 本カスタマイズガイド。
  - `index.md`: トップページ。
  - `architecture/index.md`: アーキテクチャ解説ページ。
  - `workflow/index.md`: ワークフロー解説ページ。
- `__OUT_MARKDOWN_DIR__/`: 生成された Markdown ドキュメント (**直接編集しないでください**)。
- `__OUT_HTML_DIR__/`: 生成された静的 HTML サイト (**直接編集しないでください**)。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像群 (**直接編集しないでください**)。

---

## 2. ビルドとプレビュー

### ビルドスクリプトの実行
```bash
./build_html.sh       # HTML サイトの生成
./build_markdown.sh   # Markdown の生成
./build_image.sh      # 図解画像の抽出
./build.sh            # 全ビルドの順次実行
```

### drawlib コマンドを直接実行する場合
```bash
# レスポンシブな静的 HTML サイトの生成
drawlib build html __SRC_DIR__/ -o __OUT_HTML_DIR__/

# GitHub 閲覧用 Markdown (画像リンク付き) の生成
drawlib build markdown __SRC_DIR__/ -o __OUT_MARKDOWN_DIR__/

# 図解画像の抽出
drawlib build image __SRC_DIR__/ -o __OUT_IMAGES_DIR__/
```

### HTML サイトのローカルプレビュー
組み込みの開発用 HTTP サーバーでサイトをローカル確認します:
```bash
./serve.sh
# または drawlib コマンドを直接実行:
drawlib serve __OUT_HTML_DIR__/
```

---

## 3. カスタマイズガイド

### 3.1. テーマと全体スタイルの設定 (`styles.py`)
`styles.py` はサイト全体の図面スタイルやフォントを一元管理します。ビルド時に自動検出されます。

```python
from drawlib.fonts import FontJapanese
from drawlib.styles import Styles

# 日本語フォントのデフォルト適用やスタイルの上書き
Styles = Styles.patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
)
```

別テーマでビルドしたい場合は、`--styles` / `-s` オプションで外部ファイルを指定できます:
```bash
drawlib build html __SRC_DIR__/ -o __OUT_HTML_DIR__/ -s custom_styles.py
```

### 3.2. 共通ヘルパー関数と定数の定義 (`utils.py`)
`utils.py` では、繰り返し利用する図面コンポーネントやマクロ関数、定数を定義します。定義したシンボルは自動的に `drawlib.utils` にロードされます。

```python
# utils.py 内:
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

PROJECT_NAME = "基幹プラットフォーム"

def service_card(xy: tuple[float, float], title: str) -> None:
    rectangle(xy, width=32, height=18, style=Styles.BlueFlat.patch(shape_r=2))
    text(xy, title, style=Styles.WhiteBold)
```

Markdown 内の ````drawlib```` コードブロックから利用する例:
```python
from drawlib.utils import PROJECT_NAME, service_card

service_card((50, 25), "認証ゲートウェイ")
```

### 3.3. ナビゲーションサイドバーの編集 (`navbar.md`)
`navbar.md` は HTML サイトのサイドバー構成を定義します:

1. **ブランド名**: 最初の `# 見出し 1` がサイト上部のブランドタイトルになります。
2. **カテゴリ**: 各 `## 見出し 2` がセクションの区切り見出しになります。
3. **リンク**: `- [ページ名](path/to/file.md)` の箇条書きで各ページへリンクします。

```markdown
# マイプロジェクト ドキュメント

- [ホーム](index.md)

## 1. アーキテクチャ
- [システム構成](architecture/index.md)

## 2. ワークフロー
- [開発フロー](workflow/index.md)
```

> **厳密なリンク検証**: `navbar.md` 内に記述されたすべてのリンクは、ビルド時にファイル存在確認が行われます。存在しないファイルへのリンクがあるとエラーが発生しビルドが中断します。

### 3.4. デザインとレイアウトの変更 (`style.css` & `template.html`)
- **`style.css`**: CSS 変数を上書きして、ブランドカラーやレイアウト幅を調整できます:
  ```css
  :root {
      --dl-color-primary: #1a73e8;
      --dl-sidebar-width: 280px;
  }
  ```
- **`template.html`**: Jinja2 テンプレートを編集して、ヘッダー、フッター、ファビコン、独自スクリプトの追加が可能です。

### 3.5. ブランド名・ファビコン・ロゴ画像の設定 (`_assets/`)
サイドバー上部のブランドヘッダーは、テキスト表示と画像ロゴの両方に対応しています:

- **ブラウザタブのファビコン (`_assets/favicon.png`)**:
  - デフォルトで配置されています。全 HTML ページの `<head>` 内でブラウザタブ用アイコンとして自動適用されます。
- **ヘッダーブランドの表示切り替え**:
  - **テキスト表示（デフォルト）**: デフォルトでは、`navbar.md` の最初の `# 見出し 1` に設定されたタイトル文字列がそのままサイドバー上部に表示されます。
  - **画像ロゴ表示**: `_assets/logo.png`（ライトモード用）および `_assets/logo_dark.png`（ダークモード用）を配置すると、自動的にテキストから画像ロゴ表示へ切り替わります。
  - **見本テンプレート**: プロジェクト初期化時は、見本画像が `_assets/_logo.png` および `_assets/_logo_dark.png` として配置されています。画像ロゴを使用する場合は、ファイル名先頭の `_` を削除して `logo.png` / `logo_dark.png` にリネームするか、自前のロゴ画像を配置してください。

### 3.6. 新しいチャプターやページの追加
1. `__SRC_DIR__/` 配下に新規ディレクトリや Markdown ファイルを作成します。
2. `navbar.md` に作成したファイルへのリンクを追加します。
3. ````drawlib```` コードブロックを記述して図面を配置します。
4. `./build.sh` を実行して反映します。

### 3.7. 図面開発の高速検証
図面の座標合わせを行う際は、座標グリッド表示 (`-g`) を使って対象ブロックのみを高速出力できます:
```bash
# index.md 内の 1 番目のブロックをグリッド付きでプレビュー画像に出力
drawlib export __SRC_DIR__/index.md 1 -g -o preview.png
```
キャッシュを無視して全ドキュメントを再ビルドする場合:
```bash
drawlib build html __SRC_DIR__/ -o __OUT_HTML_DIR__/ --no-cache
```
