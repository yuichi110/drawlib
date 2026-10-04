# Drawlib 画像描画スクリプト

このディレクトリには、Drawlib を使用して画像ファイルを一括生成するスタンドアロン Python 描画スクリプトが含まれています。

> [!TIP]
> **詳細なルールや機能ガイドを確認したい場合**  
> 図面の描き方、API 仕様、推奨設計ガイドラインの詳細については、以下のコマンドを実行してください:
> - `uv run drawlib rules show overview` : 描画マニュアル & AI 自己修正ループ
> - `uv run drawlib rules show styles`    : 動的テーマ設定、`styles.py` および `utils.py` の詳細
> - `uv run drawlib rules show canvas`    : キャンバスサイズ、座標系原点、clear/save 仕様
> - `uv run drawlib rules show cli`       : CLI コマンド仕様 & 出力オプション
> - `uv run drawlib rules list`          : 利用可能な全ルールトピック一覧

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ソース Python 描画スクリプト (**正本**)。
  - `build.sh`: 描画スクリプトを実行して画像を生成するスクリプト。
  - `styles.py`: 全体描画テーマ、パレット、日本語フォント設定スクリプト。
  - `utils.py`: 再利用可能な描画ヘルパー関数、マクロ、プロジェクト共通定数。
  - `README.md`: 本カスタマイズガイド。
  - `sample1.py`: Drawlib の基本図形機能のみを使用した基本構成図スクリプト。
  - `sample2.py`: `utils.py` の共通ヘルパーと画像アセット (`_assets/`) を活用した構成図スクリプト。
- `__OUT_DIR__/`: 生成された画像出力ディレクトリ (**直接編集しないでください**)。

---

## 2. ビルド方法

### ビルドスクリプトの実行
プロジェクトルートまたは本ディレクトリから以下を実行します:
```bash
./build.sh
```

### drawlib コマンドを直接実行する場合
```bash
# ディレクトリ内の全 Python スクリプトを実行して画像を一括生成
drawlib build image __SRC_DIR__/ -o __OUT_DIR__/
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

BRAND_COLOR = "#0055ff"

def component_box(xy: tuple[float, float], label: str) -> None:
    rectangle(xy, width=28, height=16, r=2, style=Styles.BlueFlat)
    text(xy, label, style=Styles.WhiteBold)
```
スタンドアロンスクリプトから利用する例:
```python
from drawlib.utils import BRAND_COLOR, component_box
component_box((50, 30), "サービスワーカー")
```

### 3.3. 描画スクリプトの基本作法
- **座標原点**: `(0, 0)` は厳密に左下隅です。
- **中心配置**: デフォルトで図形やテキストは幾何中心を基準に配置されます。
- **キャンバスサイズ**: 各スクリプトの先頭で `setup(width=..., height=...)` を設定します。推奨サイズ:
  - `80x40` (バッジ、小型カード)
  - `140x70` (アーキテクチャ図、フロー図、シーケンス図)
  - `160x90` (16:9 ワイドスライド)
- **複数画像スクリプト**: 同一スクリプト内で連続して画像を出力する場合は、図面の間に `clear()` を呼び出します。

### 3.4. 図面開発の高速検証
特定の描画スクリプトをグリッド付き (`-g`) で画像出力してレイアウトを確認できます:
```bash
drawlib show __SRC_DIR__/sample1.py -g -o preview.png
```
キャッシュを無視して再ビルドする場合:
```bash
drawlib build image __SRC_DIR__/ -o __OUT_DIR__/ --no-cache
```
