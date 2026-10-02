# Drawlib 単一ドキュメント

このディレクトリには、Drawlib 図面が埋め込まれた単一の Markdown ドキュメントが含まれています。スタンドアロン HTML および GitHub 閲覧用 Markdown にコンパイルできます。

> [!TIP]
> **詳細なルールや機能ガイドを確認したい場合**  
> 図面の描き方、API 仕様、推奨設計ガイドラインの詳細については、以下のコマンドを実行してください:
> - `uv run drawlib rules show overview` : 描画マニュアル & AI 自己修正ループ
> - `uv run drawlib rules show styles`    : 動的テーマ設定、`styles.py` および `utils.py` の詳細
> - `uv run drawlib rules show cli`       : CLI コマンド仕様 & 出力オプション
> - `uv run drawlib rules list`          : 利用可能な全ルールトピック一覧

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ソースドキュメントおよび図面コード (**正本**)。
  - `build.sh`: Markdown および HTML をビルドするスクリプト。
  - `serve.sh`: ローカルプレビュー用 HTTP サーバースクリプト。
  - `styles.py`: 全体描画テーマ、パレット、日本語フォント設定スクリプト。
  - `utils.py`: 再利用可能な描画ヘルパー関数、マクロ、プロジェクト共通定数。
  - `style.css`: スタンドアロン HTML 出力用カスタム CSS。
  - `template.html`: HTML 出力用 Jinja2 テンプレート。
  - `README.md`: 本カスタマイズガイド。
  - `doc.md`: 図面が埋め込まれたサンプルドキュメント。
- `__OUT_DIR__/`: 生成された Markdown ドキュメント (**直接編集しないでください**)。
- `__OUT_HTML_DIR__/`: 生成された HTML ドキュメント (**直接編集しないでください**)。

---

## 2. ビルドとプレビュー方法

### ビルドスクリプトの実行
プロジェクトルートまたは本ディレクトリから以下を実行します:
```bash
./build.sh
```

### HTML ドキュメントのローカルプレビュー
組み込みの開発用 HTTP サーバーでドキュメントをローカル確認します:
```bash
./serve.sh
# または drawlib コマンドを直接実行:
drawlib serve __OUT_HTML_DIR__/
```

### drawlib コマンドを直接実行する場合
```bash
# GitHub 閲覧用 Markdown (画像リンク付き) の生成
drawlib build markdown __SRC_DIR__/doc.md -o __OUT_DIR__/doc.md

# スタンドアロン HTML の生成
drawlib build html __SRC_DIR__/doc.md -o __OUT_HTML_DIR__/doc.html
```

---

## 3. カスタマイズガイド

### 3.1. テーマと全体スタイルの設定 (`styles.py`)
図面全体のスタイルやフォントを一元管理します:
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

PROJECT_NAME = "システム設計仕様書"

def node(xy: tuple[float, float], label: str) -> None:
    rectangle(xy, width=24, height=14, r=1, style=Styles.BlueFlat)
    text(xy, label, style=Styles.WhiteBold)
```
Markdown 内の ````drawlib```` コードブロックから利用する例:
```python
from drawlib.utils import PROJECT_NAME, node
node((40, 20), "コアエンジン")
```

### 3.3. デザインとテンプレートの変更 (`style.css` & `template.html`)
- **`style.css`**: HTML 出力の余白、配色、フォントを微調整できます。
- **`template.html`**: HTML のヘッダー、フッター、外部ライブラリの読み込みをカスタマイズできます。

### 3.4. 図面開発の高速検証
特定の図面ブロックのみをグリッド付き (`-g`) で画像出力してレイアウトを確認できます:
```bash
drawlib export __SRC_DIR__/doc.md 1 -g -o preview.png
```
キャッシュを無視して再ビルドする場合:
```bash
drawlib build html __SRC_DIR__/doc.md -o __OUT_HTML_DIR__/doc.html --no-cache
```
