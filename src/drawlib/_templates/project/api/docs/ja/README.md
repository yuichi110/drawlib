# Drawlib API リファレンスプロジェクト

このディレクトリには、図解付き API リファレンスサイト（`type = "api"`）の Markdown 原稿、Drawlib 図解コード、および設定ファイルが含まれています。

> [!TIP]
> **詳細なルールとガイドの参照**  
> Drawlib CLI から組み込みマニュアルをいつでも確認できます:
> - `uv run drawlib rules show project-api`      : `api` プロジェクトの構成、`# H1` / `## H2` ナビゲーション規約、`[api]` 設定
> - `uv run drawlib rules show overview`         : 左下原点 `(0, 0)` の座標系と描画ライフサイクル
> - `uv run drawlib rules show style-guide`      : 50% 以上ニュートラル配色のスタイル規約
> - `uv run drawlib rules list`                  : 全コンポーネント・ダイアグラムのマニュアル一覧

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ソース Markdown と描画コード（**編集対象 / Single Source of Truth**）。
  - `drawlib.toml`: プロジェクトマニフェスト（`[project]`、`[i18n]`、`[api]`、および任意の `[seo]`）。
  - `__DEFAULT_LANG__/`: API リファレンス原稿（**1 Markdown = 1 HTML ページ**）:
    - `00_overview.md`: API 概要、認証方式、システム構成図（`# H1` カテゴリ + `## H2` セクション）。
    - `01_users.md`: REST エンドポイント定義（`GET`、`POST`、`DELETE` セマンティックバッジ付き）。
    - `02_models.md`: SDK クラス・関数・ER データモデル定義（`class`、`def` バッジ付き）。
  - `_assets/`: 共通静的アセット（`favicon.png`、`logo.png`、`logo_dark.png`）。
  - `styles.py` / `utils.py`: 共通スタイル定義と再利用可能な描画ヘルパー。
  - `style.css` / `template.html`: 2 カラム API リファレンス用 CSS と Jinja2 テンプレート。
  - `build.sh`, `build_html.sh`, `build_markdown.sh`, `build_image.sh`, `serve.sh`: ビルド・プレビュー用スクリプト。
- `__OUT_HTML_DIR__/`: 生成された静的 HTML リファレンス（**直接編集禁止**）。
- `__OUT_MARKDOWN_DIR__/`: 生成された Markdown リファレンス（**直接編集禁止**）。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像ファイル群（**直接編集禁止**）。

---

## 2. 左ナビゲーションペインの仕組み（`1 MD = 1 ページ`）

`__SRC_DIR__/<lang>/` 配下の各 `.md` ファイルが 1 つの HTML ページにコンパイルされます:
1. **`# H1` 見出し -> カテゴリ / モジュール名**: 左ペインのアコーディオン見出しとして表示されます。
2. **`## H2` 見出し -> シンボル / エンドポイント一覧**: `# H1` 配下のリストとして自動抽出され、`#slug` アンカーとスクロール追従ハイライトが自動付与されます。
3. **セマンティックバッジ**: `## H2` の先頭にバッククォートで種別を書くと、色分けバッジが自動付与されます:
   - **コード / SDK**: `` ## `def` verify_signature(payload, header, secret) ``, `` ## `class` User ``, `` ## `method` client.send(req) ``, `` ## `const` DEFAULT_TIMEOUT ``, `` ## `type` UserRole ``, `` ## `cmd` sync ``
   - **REST HTTP**: `` ## `GET` /v1/users ``, `` ## `POST` /v1/users ``, `` ## `PUT` /v1/users/<id> ``, `` ## `PATCH` /v1/users/<id> ``, `` ## `DELETE` /v1/users/<id> ``

---

## 3. `drawlib.toml` の `[api]` 設定

左ペインの初期開閉状態（ブラウザの `Ctrl+F` / `Cmd+F` ページ内検索への対応）や、バッジ・右上リンクを `drawlib.toml` で制御できます:

```toml
[api]
# デフォルトで左ペインの全カテゴリを展開（Ctrl+F で全シンボルを即検索可能）
sidebar_expanded = true

# ロゴ直下のバージョンバッジと GitHub リポジトリリンク（任意）
badge_text = "v1.0"
repo_url = "https://github.com/example/my-api"

# 右上ヘッダーバーの外部・相対リンク（任意）
header_links = [
  { label = { en = "Guides", ja = "ガイド" }, url = "https://docs.example.com" },
]
```

---

## 4. ビルドとプレビュー

```bash
./__SRC_DIR__/build.sh          # HTML・Markdown・画像の一括ビルド
./__SRC_DIR__/serve.sh          # ローカルプレビューサーバーの起動
./__SRC_DIR__/serve.sh --check  # 内部リンクと #slug アンカーの整合性検証
```
