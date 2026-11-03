# Drawlib カタログ・リファレンスプロジェクト

このディレクトリには、図解付きカタログ・リファレンスサイト（`type = "catalog"`）の Markdown 原稿、Drawlib 図解コード、および設定ファイルが含まれています。

> [!TIP]
> **詳細なルールとガイドの参照**  
> Drawlib CLI から組み込みマニュアルをいつでも確認できます:
> - `uv run drawlib rules show project-catalog`  : `catalog` プロジェクトの構成、`# H1` / `## H2` ナビゲーション規約、`[catalog]` 設定
> - `uv run drawlib rules show overview`         : 左下原点 `(0, 0)` の座標系と描画ライフサイクル
> - `uv run drawlib rules show style-guide`      : 50% 以上ニュートラル配色のスタイル規約
> - `uv run drawlib rules list`                  : 全コンポーネント・ダイアグラムのマニュアル一覧

---

## 1. ディレクトリ構成

- `__SRC_DIR__/`: ソース Markdown と描画コード（**編集対象 / Single Source of Truth**）。
  - `drawlib.toml`: プロジェクトマニフェスト（`[project]`、`[i18n]`、`[catalog]`、および任意の `[seo]`）。
  - `__DEFAULT_LANG__/`: カタログ原稿（**1 Markdown = 1 HTML ページ**）:
    - `00_overview.md`: システム概要、認証方式、トポロジ図（`# H1` カテゴリ + `## H2` セクション）。
    - `01_users.md`: REST エンドポイント定義（`GET`、`POST`、`DELETE` セマンティックバッジ付き）。
    - `02_models.md`: SDK クラス・関数・ER データモデル定義（`class`、`def` バッジ付き）。
  - `_assets/`: 共通静的アセット（`favicon.png`、`logo.png`、`logo_dark.png`）。
  - `styles.py` / `utils.py`: 共通スタイル定義と再利用可能な描画ヘルパー。
  - `style.css` / `template.html`: 2 カラムカタログ・リファレンス用 CSS と Jinja2 テンプレート。
  - `build.sh`, `build_html.sh`, `build_markdown.sh`, `build_image.sh`, `serve.sh`: ビルド・プレビュー用スクリプト。
- `__OUT_HTML_DIR__/`: 生成された静的 HTML カタログ（**直接編集禁止**）。
- `__OUT_MARKDOWN_DIR__/`: 生成された Markdown カタログ（**直接編集禁止**）。
- `__OUT_IMAGES_DIR__/`: 抽出された図解画像ファイル群（**直接編集禁止**）。

---

## 2. 左ナビゲーションペインの仕組み（`1 MD = 1 ページ`）

`__SRC_DIR__/<lang>/` 配下の各 `.md` ファイルが 1 つの HTML ページにコンパイルされます:
1. **`# H1` 見出し -> カテゴリ / ドメイン名**: 左ペインのアコーディオン見出しとして表示されます。
2. **`## H2` 見出し -> 項目 / シンボル / エンドポイント一覧**: `# H1` 配下のリストとして自動抽出され、`#slug` アンカーとスクロール追従ハイライトが自動付与されます。
3. **セマンティックバッジ**: `## H2` の先頭にバッククォートで種別を書くと、色分けバッジが自動付与されます:
   - **コード / SDK / CLI**: `` ## `def` verify_signature(payload, header, secret) ``, `` ## `class` User ``, `` ## `method` client.send(req) ``, `` ## `const` DEFAULT_TIMEOUT ``, `` ## `type` UserRole ``, `` ## `cmd` sync ``
   - **REST HTTP**: `` ## `GET` /v1/users ``, `` ## `POST` /v1/users ``, `` ## `PUT` /v1/users/<id> ``, `` ## `PATCH` /v1/users/<id> ``, `` ## `DELETE` /v1/users/<id> ``
   - **汎用カタログ（サービス・DB・設定・ルール・運用）**: `` ## `service` billing-api ``, `` ## `table` users ``, `` ## `schema` OrderEvent ``, `` ## `config` server.port ``, `` ## `env` LOG_LEVEL ``, `` ## `rule` DL001 ``, `` ## `error` E1004 ``, `` ## `token` PrimaryFlat ``, `` ## `adr` ADR-004 ``

---

## 3. `drawlib.toml` の `[catalog]` 設定

左ペインの初期開閉状態（ブラウザの `Ctrl+F` / `Cmd+F` ページ内検索への対応）や、パンくずのルート名、バッジ・右上リンクを `drawlib.toml` で制御できます:

```toml
[catalog]
# デフォルトで左ペインの全カテゴリを展開（Ctrl+F で全項目を即検索可能）
sidebar_expanded = true

# パンくずリスト先頭のルート名（未指定時は "Catalog" / "カタログ"）
breadcrumb_root = "カタログ"

# ロゴ直下のバージョンバッジと GitHub リポジトリリンク（任意）
badge_text = "Catalog · v1.0"
repo_url = "https://github.com/example/my-catalog"

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
