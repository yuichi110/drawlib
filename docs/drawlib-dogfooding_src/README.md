# Drawlib ドキュメントプロジェクト (`doc`)

このディレクトリには、Drawlib を使用して **HTML, PDF, Markdown, スタンドアロン画像** へ一括コンパイルされるドキュメントが含まれています。

> [!TIP]
> **詳細なルールや機能ガイドを確認したい場合**  
> 図面の描き方、API 仕様、推奨設計ガイドラインの詳細については、以下のコマンドを実行してください:
> - `uv run drawlib rules show overview` : 描画マニュアル & AI 自己修正ループ
> - `uv run drawlib rules show styles`    : 動的テーマ設定、`styles.py` および `utils.py` の詳細
> - `uv run drawlib rules show docs_build`: 複数チャプター構成、目次生成、PDF オプション
> - `uv run drawlib rules list`          : 利用可能な全ルールトピック一覧

---

## 1. ディレクトリ構成

- `drawlib-dogfooding_src/`: Markdown ソースドキュメントおよび図面コード (**正本**)。
  - `build.sh`: 全ターゲット（HTML, PDF, Markdown, Images）を一括ビルドするマスター実行スクリプト。
  - `build_html.sh`: スタンドアロン HTML ドキュメントをビルドするスクリプト。
  - `build_pdf.sh`: ベクター PDF レポートをビルドするスクリプト。
  - `build_markdown.sh`: GitHub 閲覧用 Markdown をビルドするスクリプト。
  - `build_image.sh`: 埋め込み図面ブロックを画像抽出するスクリプト。
  - `serve.sh`: ローカル HTML プレビュー用簡易サーバー起動スクリプト。
  - `styles.py`: 全体描画テーマ、パレット、日本語フォント設定スクリプト。
  - `utils.py`: 再利用可能な描画ヘルパー関数、マクロ、プロジェクト共通定数。
  - `style.css`: ドキュメント用スタイルシート。
  - `template.html`: HTML / PDF 用 Jinja2 HTML テンプレート。
  - `README.md`: 本カスタマイズガイド。
  - `00_cover.md`: 表紙ページ。
  - `01_ai_challenges.md`: 各チャプター Markdown ファイル。
- `drawlib-dogfooding_html/`: 生成された HTML ドキュメント (**直接編集しないでください**)。
- `drawlib-dogfooding.pdf`: 生成された PDF ドキュメント (**直接編集しないでください**)。
- `drawlib-dogfooding_markdown/`: 生成された Markdown ドキュメント (**直接編集しないでください**)。
- `drawlib-dogfooding_images/`: 抽出されたスタンドアロン図面画像 (**直接編集しないでください**)。

---

## 2. ビルド方法

### ビルドスクリプトの実行
プロジェクトルートまたは本ディレクトリから目的のスクリプトを実行します:
```bash
./build_html.sh       # 単一 HTML ドキュメントの生成 (drawlib-dogfooding_html/)
./build_pdf.sh        # ベクター PDF レポートの生成 (drawlib-dogfooding.pdf)
./build_markdown.sh   # GitHub 閲覧用 Markdown の生成 (drawlib-dogfooding_markdown/)
./build_image.sh      # 埋め込み図面画像の抽出 (drawlib-dogfooding_images/)
./build.sh            # 上記全ターゲットの一括順次ビルド
```

### プレビューサーバーの起動
```bash
./serve.sh            # http://localhost:8000 でプレビュー
```

### drawlib コマンドを直接実行する場合
```bash
drawlib build html drawlib-dogfooding_src/ -o drawlib-dogfooding_html/
drawlib build pdf drawlib-dogfooding_src/ -o drawlib-dogfooding.pdf --generate-index
drawlib build markdown drawlib-dogfooding_src/ -o drawlib-dogfooding_markdown/
drawlib build image drawlib-dogfooding_src/ -o drawlib-dogfooding_images/
```

---

## 3. カスタマイズガイド

### 3.1. テーマと全体スタイルの設定 (`styles.py`)
図面全体のスタイルや日本語フォントを一元管理します:
```python
from drawlib.fonts import FontJapanese
from drawlib.styles import Styles

Styles = Styles.patch_font(
    regular=FontJapanese.SANSSERIF_REGULAR,
    bold=FontJapanese.SANSSERIF_BOLD,
)
```

### 3.2. 共通ヘルパー関数と定数の定義 (`utils.py`)
繰り返し利用する図面コンポーネントや定数を定義します:
```python
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

REPORT_VERSION = "v1.0.0"

def chapter_banner(xy: tuple[float, float], title: str) -> None:
    rectangle(xy, width=100, height=12, style=Styles.BlueFlat)
    text(xy, title, style=Styles.WhiteBold)
```
Markdown 内の ````drawlib```` コードブロックから利用する例:
```python
from drawlib.utils import REPORT_VERSION, chapter_banner
chapter_banner((60, 20), f"システム設計書 ({REPORT_VERSION})")
```

### 3.3. チャプター構成と改ページ
- ファイル名順（`00_cover.md`, `01_overview.md`, `02_design.md` など）に結合されます。
- チャプター間の改ページには `<div class="page-break"></div>` または CSS の `page-break-before: always;` を使用します。
- `--generate-index` オプションにより、見出し階層から目次が自動生成されます。

### 3.4. 印刷スタイルとレイアウト (`style.css` & `template.html`)
- **`style.css`**: `@page` ルールで用紙サイズや余白、ヘッダー/フッター位置を調整できます:
  ```css
  @page {
      size: A4 portrait;
      margin: 20mm 15mm;
  }
  ```
- **`template.html`**: 表紙のレイアウト、ヘッダー・フッターのロゴやページ番号表示をカスタマイズできます。

### 3.5. 図面開発の高速検証
特定の図面ブロックのみをグリッド付き (`-g`) で画像出力してレイアウトを確認できます:
```bash
drawlib export drawlib-dogfooding_src/01_overview.md 1 -g -o preview.png
```
キャッシュを無視して再ビルドする場合:
```bash
drawlib build pdf drawlib-dogfooding_src/ -o drawlib-dogfooding.pdf --no-cache
```
