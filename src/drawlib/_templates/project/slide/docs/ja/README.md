# Drawlib スライドプレゼンテーションプロジェクト

このディレクトリには、Drawlib を使用してインタラクティブな HTML プレゼンテーションスライドおよびベクター PDF にコンパイルされるスライド用 Markdown と作図コードが含まれています。

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: スライドソースおよび設定ファイル (**編集対象 / Source of Truth**)。
  - `drawlib.toml`: プロジェクトマニフェスト (`[project]` 設定および `[i18n]` 言語構成)。
  - `__DEFAULT_LANG__/`: デフォルト言語のスライド Markdown ディレクトリ (多言語化する場合は `<lang>/` を追加し `drawlib.toml` の `langs` に追記):
    - `01_title.md`: タイトルスライド。
    - `02_agenda.md`: アジェンダスライド。
    - `03_architecture.md`: アーキテクチャ・図版スライド。
  - `_assets/`: 全言語で共有される画像アセット (`favicon.png`, `linux.png`)。
  - `build.sh`: 全ビルドを一括実行するマスタービルドスクリプト。
  - `build_html.sh`: HTML スライドデッキの高速ビルド。
  - `build_pdf.sh`: 提出・配布用ベクター PDF ビルド (1スライド1ページ)。
  - `build_image.sh`: 単体図解画像の抽出スクリプト。
  - `serve.sh`: ローカルプレビューサーバーの起動。
  - `styles.py`: 全体スタイル設定 (テーマ、カラー、フォント。言語別の `<lang>/styles.py` 上書きも可能)。
  - `utils.py`: スライド用作図マクロ (カード、表、タイムライン等)。
  - `style.css`: スライド装飾およびテーマ変数 CSS。
  - `README.md`: このカスタマイズガイド。
- `__OUT_HTML_DIR__/`: 生成されたインタラクティブ HTML スライド (`__OUT_HTML_DIR__/index.html`, `__OUT_HTML_DIR__/<lang>/index.html`)。
- `__TARGET___<lang>.pdf` (例: `__TARGET_____DEFAULT_LANG__.pdf`): 言語ごとに生成されたベクター PDF プレゼンテーション。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像群。

---

## 2. スライドのビルド

### スクリプトの実行
```bash
./build_html.sh   # HTML スライドデッキの生成
./build_pdf.sh    # ベクター PDF (<base>_<lang>.pdf) の生成
./build_image.sh  # 単体図解画像の抽出
./build.sh        # 全ビルドの順次実行
```

### プレビュー
```bash
./serve.sh        # ローカルプレビューサーバーの起動
```
