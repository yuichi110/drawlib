# Drawlib ドキュメントサイト

このディレクトリには、ドキュメントサイト用の Markdown ソースファイルと各種設定が含まれています。

## ディレクトリ構成

- `__SRC_DIR__/`: Markdown ソースドキュメントおよび図面コード (**正本**)
  - `build.sh`: Markdown および HTML サイトをビルドするスクリプト
  - `config.py`: グローバル設定スクリプト (テーマ、スタイル、日本語フォントなど)
  - `style.css`: HTML サイト用スタイルシート
  - `template.html`: HTML サイト用 Jinja2 テンプレート
  - `README.md`: 本ガイド
  - `index.md`: トップページ
  - `navbar.md`: ナビゲーションサイドバー定義
  - `architecture/index.md`: アーキテクチャ解説
  - `workflow/index.md`: ワークフロー解説
- `__OUT_DIR__/`: 生成された Markdown ドキュメント (**直接編集しないでください**)
- `__OUT_HTML_DIR__/`: 生成された静的 HTML サイト (**直接編集しないでください**)

## ビルド方法

プロジェクトルートまたは本ディレクトリから以下を実行します:

```bash
./build.sh
```

または drawlib コマンドを直接実行します:

```bash
drawlib build html __SRC_DIR__/ -o __OUT_HTML_DIR__/
drawlib build markdown __SRC_DIR__/ -o __OUT_DIR__/
```

## HTML プレビュー

ビルドされた HTML サイトをローカルで確認するには:

```bash
drawlib serve __OUT_HTML_DIR__/
```
