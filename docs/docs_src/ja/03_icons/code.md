# コード・言語・フレームワークアイコン

Drawlib は、`drawlib.icons.code`（`CodeIcon`）に **97 種の公式プログラミング言語・フレームワーク・SDK ブランドアイコン**を、`drawlib.icons.original_code`（`OriginalCodeIcon`）に **121 種のフラット 2D パステルアイコン**（**97 種のブランドツイン**＋**24 種のベンダー中立ソフトウェアエンジニアリング・API コンセプトアイコン**）を提供しています。ティア間の使い分け指針については[アイコン概要](./overview.md)を、トポロジ図への組み込みについては[アーキテクチャ図](../06_diagrams/architecture.md)を参照してください。

```drawlib code=fold align=center file=icons_code_hero.png caption="公式ブランドアイコン (code)、オリジナル 2D パステルブランド (original_code)、オリジナル 2D パステルコンセプト (original_code) の比較"
from drawlib.canvas import save, setup
from drawlib.icons import code, original_code
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=70)

columns = [
    (
        26.0,
        "1. Official Code Brands",
        "drawlib.icons.code (97)",
        Styles.Neutral,
        [
            ("python", code.python),
            ("typescript", code.typescript),
            ("rust", code.rust),
            ("react", code.react),
        ],
    ),
    (
        72.0,
        "2. 2D Pastel Brands",
        "original_code Twins (97)",
        Styles.PrimaryNeutral,
        [
            ("python", original_code.python),
            ("typescript", original_code.typescript),
            ("rust", original_code.rust),
            ("react", original_code.react),
        ],
    ),
    (
        118.0,
        "3. 2D Pastel Concepts",
        "original_code Exclusive (24)",
        Styles.SecondaryNeutral,
        [
            ("rest_api", original_code.rest_api),
            ("microservice", original_code.microservice),
            ("worker", original_code.background_worker),
            ("sdk_library", original_code.sdk_library),
        ],
    ),
]

for cx, title, subtitle, card_style, icons_list in columns:
    rectangle((cx, 35.0), width=42.0, height=62.0, style=card_style.patch(shape_r=2.5))
    text((cx, 60.0), title, style=Styles.DarkBold.patch(text_size=11.0))
    text((cx, 54.8), subtitle, style=Styles.Muted.patch(text_size=10.0))

    offsets = [(-9.8, 41.5), (9.8, 41.5), (-9.8, 20.5), (9.8, 20.5)]
    sub_card_style = Styles.White.patch(shape_r=1.5, line_width=0.6)
    for (dx, iy), (lbl, fn) in zip(offsets, icons_list, strict=True):
        ix = cx + dx
        rectangle((ix, iy - 1.8), width=17.6, height=17.5, style=sub_card_style)
        fn((ix, iy + 1.5), width=7.5, style=Styles.Primary)
        text((ix, iy - 6.6), lbl, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

---

## 1. API シグネチャとツインモジュール構成

コード・言語・フレームワークアイコンスイートは、1 対 1 の正規命名規則を共有するツインモジュールペアとして構成されています。

- **`drawlib.icons.code`**（`CodeIcon` Enum）: プログラミング言語、フロントエンド／モバイル UI フレームワーク、バックエンドサーバー、パッケージマネージャ、API プロトコル、IDE を網羅する **97 種の公式ベンダーおよび OSS ブランドアイコン**（`512×512` RGBA PNG）。
- **`drawlib.icons.original_code`**（`OriginalCodeIcon` Enum）: 全 **97 種の対応するブランドツイン**に加え、**24 種のベンダー中立ソフトウェアエンジニアリング・API コンセプトアイコン**（`rest_api`、`graphql_api`、`rpc_call`、`microservice`、`background_worker`、`cli_tool` など）を含む合計 **121 種のフラット 2D パステルアイコン**（`512×512` RGBA PNG）。

```python
from drawlib.diagrams.architecture import CodeIcon, Node, OriginalCodeIcon
from drawlib.icons import code, original_code
from drawlib.styles import Styles

# 1. Direct canvas rendering (center-anchored at (cx, cy), 1:1 square aspect ratio)
code.python((30, 25), width=9.0, style=Styles.Primary)
original_code.python((60, 25), width=9.0, style=Styles.Primary)
original_code.rest_api((90, 25), width=9.0, style=Styles.Primary)

# 2. High-level ArchitectureDiagram / SequenceDiagram Enums
api_node = Node("FastAPI Service", width=25, height=18, icon=CodeIcon.FASTAPI, icon_size=7.5)
worker_node = Node("Job Worker", width=25, height=18, icon=OriginalCodeIcon.BACKGROUND_WORKER, icon_size=7.5)
```

| 項目 | 公式スイート (`drawlib.icons.code`) | オリジナル 2D パステルスイート (`drawlib.icons.original_code`) |
| :--- | :--- | :--- |
| **関数シグネチャ** | `code.<name>(xy, width, *, style, variant="default")` | `original_code.<name>(xy, width, *, style, variant="default")` |
| **ダイアグラム Enum** | `CodeIcon.<NAME>`（例: `CodeIcon.PYTHON`） | `OriginalCodeIcon.<NAME>`（例: `OriginalCodeIcon.REST_API`） |
| **正規アイコン数** | ブランドアイコン **97** 種 | 合計 **121** 種（ブランドツイン **97** 種 + コンセプトアイコン **24** 種） |
| **座標アンカー** | 中央基準 `(cx, cy)`（`halign="center"`, `valign="center"`） | 中央基準 `(cx, cy)`（`halign="center"`, `valign="center"`） |
| **アセットアーカイブ** | `icon_code`（`512×512` RGBA PNG） | `icon_original_code`（`512×512` RGBA PNG） |

---

## 2. 公式・パステルブランドアイコン一覧とリファレンス (`code` & `original_code`)

以下に示す **97 種のブランドアイコン名**は、`drawlib.icons.code`（公式ロゴ）と `drawlib.icons.original_code`（対応する 2D パステルブランドツイン）の両方に共通して収録されています。

```drawlib code=fold align=center file=icons_code_brands.png caption="drawlib.icons.code に収録された代表的なプログラミング言語・Web フレームワーク・ランタイム・API プロトコル"
from drawlib.canvas import save, setup
from drawlib.icons import code
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=64)

row1 = [
    ("python", "Language", code.python, Styles.PrimaryNeutral),
    ("typescript", "Language", code.typescript, Styles.Neutral),
    ("go", "Language", code.go, Styles.SecondaryNeutral),
    ("rust", "Language", code.rust, Styles.Neutral),
    ("java", "Language", code.java, Styles.PrimaryNeutral),
    ("cpp", "Language", code.cpp, Styles.Neutral),
]

row2 = [
    ("react", "Frontend UI", code.react, Styles.Neutral),
    ("nextjs", "Full-Stack", code.nextjs, Styles.PrimaryNeutral),
    ("fastapi", "Python API", code.fastapi, Styles.SecondaryNeutral),
    ("spring", "Java Backend", code.spring, Styles.Neutral),
    ("graphql", "Query API", code.graphql, Styles.PrimaryNeutral),
    ("grpc", "RPC Protocol", code.grpc, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 46.5 if row_idx == 0 else 17.5
    for col_idx, (name, cat, icon_fn, card_st) in enumerate(items):
        cx = 15.2 + col_idx * 23.5
        rectangle((cx, cy), width=21.8, height=25.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.8), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.4), name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.2), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 2.1. 共通ブランドアイコン全 97 種一覧 (`code.<name>` & `original_code.<name>`)

| カテゴリ | 数 | 正規関数名 (`code.<name>` & `original_code.<name>`) |
| :--- | :---: | :--- |
| **プログラミング言語・マークアップ言語** | 25 | `bash`, `c`, `cpp`, `csharp`, `css3`, `dart`, `elixir`, `go`, `html5`, `java`, `javascript`, `julia`, `kotlin`, `lua`, `php`, `python`, `r`, `ruby`, `rust`, `scala`, `solidity`, `sql`, `swift`, `typescript`, `zig` |
| **フロントエンド・モバイル・デスクトップ UI フレームワーク** | 18 | `angular`, `astro`, `blazor`, `electron`, `expo`, `flutter`, `htmx`, `jquery`, `nextjs`, `nuxt`, `react`, `react_native`, `remix`, `storybook`, `svelte`, `tailwind_css`, `tauri`, `vuejs` |
| **バックエンド・Web・システムフレームワーク** | 21 | `appwrite`, `axum`, `celery`, `convex`, `django`, `dotnet`, `echo`, `express`, `fastapi`, `firebase`, `flask`, `gin`, `hono`, `laravel`, `nestjs`, `pocketbase`, `quarkus`, `rails`, `spring`, `tokio`, `uvicorn` |
| **ランタイム・パッケージマネージャ・ビルドツールチェーン** | 14 | `biome`, `bun`, `cargo`, `deno`, `gradle`, `nodejs`, `npm`, `pnpm`, `poetry`, `pypi`, `uv`, `vite`, `webassembly`, `yarn` |
| **API・データアクセス・科学技術計算・テストライブラリ** | 14 | `apollo`, `graphql`, `grpc`, `hasura`, `numpy`, `openapi`, `pandas`, `prisma`, `protobuf`, `pydantic`, `pytest`, `sqlalchemy`, `trpc`, `vitest` |
| **IDE・エディタ・クラウドノートブック** | 5 | `android_studio`, `antigravity`, `colab`, `intellij`, `vscode` |

---

## 3. ベンダー中立コンセプトアイコン一覧とリファレンス (`original_code`)

97 種のブランドツインに加え、`drawlib.icons.original_code`（`OriginalCodeIcon`）には **24 種の専用ベンダー中立ソフトウェアエンジニアリング・API コンセプトアイコン**が収録されており、マイクロサービス、REST/GraphQL/RPC エンドポイント、バックグラウンドワーカー、ビルドツールチェーン、SDK モジュールを図解できます。

```drawlib code=fold align=center file=icons_code_concepts.png caption="drawlib.icons.original_code に収録された代表的なベンダー中立ソフトウェアエンジニアリング＆API コンセプトアイコン 12 選"
from drawlib.canvas import save, setup
from drawlib.icons import original_code
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=88)

rows = [
    [
        ("rest_api", "HTTP / JSON Endpoint", original_code.rest_api, Styles.PrimaryNeutral),
        ("graphql_api", "Federated Graph API", original_code.graphql_api, Styles.Neutral),
        ("rpc_call", "Low-Latency RPC", original_code.rpc_call, Styles.SecondaryNeutral),
        ("websocket", "Full-Duplex Stream", original_code.websocket, Styles.Neutral),
    ],
    [
        ("webhook", "Event Callback", original_code.webhook, Styles.Neutral),
        ("microservice", "Domain Service", original_code.microservice, Styles.PrimaryNeutral),
        ("background_worker", "Async Queue Worker", original_code.background_worker, Styles.Neutral),
        ("serverless_func", "Event Function", original_code.serverless_func, Styles.SecondaryNeutral),
    ],
    [
        ("cron_job", "Scheduled Task", original_code.cron_job, Styles.SecondaryNeutral),
        ("sdk_library", "Shared Client SDK", original_code.sdk_library, Styles.Neutral),
        ("cli_tool", "Developer CLI", original_code.cli_tool, Styles.PrimaryNeutral),
        ("unit_test", "Automated Test Suite", original_code.unit_test, Styles.Neutral),
    ],
]

for row_idx, items in enumerate(rows):
    cy = 71.5 - row_idx * 27.5
    for col_idx, (title, sub, icon_fn, card_st) in enumerate(items):
        cx = 20.5 + col_idx * 33.0
        rectangle((cx, cy), width=30.5, height=24.5, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.6), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.4), title, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.2), sub, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 3.1. ベンダー中立コンセプトアイコン全 24 種一覧 (`original_code.<name>`)

| 正規関数名 (`original_code.*`) | `OriginalCodeIcon` Enum メンバー | アーキテクチャ上の役割 |
| :--- | :--- | :--- |
| `background_worker` | `OriginalCodeIcon.BACKGROUND_WORKER` | 非同期キューコンシューマおよびバックグラウンドジョブワーカー |
| `binary_executable` | `OriginalCodeIcon.BINARY_EXECUTABLE` | コンパイル済みネイティブバイナリまたは単体実行ファイル成果物 |
| `cli_tool` | `OriginalCodeIcon.CLI_TOOL` | コマンドラインインターフェース（CLI）ユーティリティおよび開発者向けシェルツール |
| `compiler_build` | `OriginalCodeIcon.COMPILER_BUILD` | ソースコンパイル・バンドル・成果物ビルドステージ |
| `cron_job` | `OriginalCodeIcon.CRON_JOB` | 時間起動の定期バッチタスクまたは Cron ジョブ |
| `debugger` | `OriginalCodeIcon.DEBUGGER` | ブレークポイント検証・プロファイリング・ランタイム診断 |
| `graphql_api` | `OriginalCodeIcon.GRAPHQL_API` | フェデレーテッド GraphQL クエリ／ミューテーションエンドポイント |
| `ide_editor` | `OriginalCodeIcon.IDE_EDITOR` | 統合開発環境（IDE）またはコードエディタ |
| `json_schema` | `OriginalCodeIcon.JSON_SCHEMA` | 構造化 JSON ペイロード契約およびスキーマバリデータ |
| `linter_formatter` | `OriginalCodeIcon.LINTER_FORMATTER` | 静的コード解析・フォーマッタ・型チェックゲート |
| `microservice` | `OriginalCodeIcon.MICROSERVICE` | 独立してデプロイ可能なドメインマイクロサービス |
| `monolith` | `OriginalCodeIcon.MONOLITH` | 単一構成のモノリシックアプリケーションサーバー |
| `package_module` | `OriginalCodeIcon.PACKAGE_MODULE` | 配布可能なソフトウェアパッケージまたは再利用モジュール |
| `regex_parser` | `OriginalCodeIcon.REGEX_PARSER` | 正規表現マッチャ・字句解析器（レクサ）・テキストパーサ |
| `rest_api` | `OriginalCodeIcon.REST_API` | 標準的な RESTful HTTP/JSON API エンドポイント |
| `rpc_call` | `OriginalCodeIcon.RPC_CALL` | 高性能なリモートプロシージャコール（RPC）インターフェース |
| `runtime_vm` | `OriginalCodeIcon.RUNTIME_VM` | マネージド言語仮想マシン（VM）またはバイトコードランタイム |
| `sdk_library` | `OriginalCodeIcon.SDK_LIBRARY` | 共通クライアント SDK または社内プラットフォームライブラリ |
| `serverless_func` | `OriginalCodeIcon.SERVERLESS_FUNC` | イベント駆動型のサーバーレス関数ハンドラ |
| `source_code` | `OriginalCodeIcon.SOURCE_CODE` | アプリケーションソースファイルまたはリポジトリモジュール |
| `unit_test` | `OriginalCodeIcon.UNIT_TEST` | 自動化された単体テスト・結合テストランナー |
| `webhook` | `OriginalCodeIcon.WEBHOOK` | アウトバウンド HTTP イベント通知コールバック |
| `websocket` | `OriginalCodeIcon.WEBSOCKET` | 永続的な全二重 WebSocket ストリーミングチャネル |
| `xml_markup` | `OriginalCodeIcon.XML_MARKUP` | XML/HTML 構造化ドキュメントマークアップ |

---

## 4. 実践的なアーキテクチャ図 (`CodeIcon` & `OriginalCodeIcon`)

以下の例では、[`ArchitectureDiagram`](../06_diagrams/architecture.md) 内で `CodeIcon`（`Next.js`、`FastAPI`、`Rust`）と `OriginalCodeIcon`（`BACKGROUND_WORKER`）を組み合わせ、ポリグロットなフルスタック Web・マイクロサービス構成を表現しています。

```drawlib code=show align=center file=icons_code_arch.png caption="CodeIcon と OriginalCodeIcon を用いたポリグロット・フルスタック＆マイクロサービストポロジ"
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    CodeIcon,
    Node,
    NodeGroup,
    OriginalCodeIcon,
)
from drawlib.styles import Styles

clear()
setup(width=128, height=64)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Polyglot Full-Stack Web & Backend Microservice Topology",
)

backend = d.add(NodeGroup(title="Polyglot Web & Backend Services", padding=5.0), xy=(4.0, 4.0))
web = backend.add(
    Node(
        "Next.js\nWeb App",
        width=25,
        height=18,
        icon=CodeIcon.NEXTJS,
        icon_size=7.5,
    ),
    xy=(12.0, 18.0),
)
api = backend.add(
    Node(
        "FastAPI\nGateway",
        width=25,
        height=18,
        icon=CodeIcon.FASTAPI,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(56.0, 18.0),
)
engine = backend.add(
    Node(
        "Rust Core\nEngine",
        width=25,
        height=18,
        icon=CodeIcon.RUST,
        icon_size=7.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(98.0, 28.0),
)
worker = backend.add(
    Node(
        "Background\nWorker",
        width=25,
        height=18,
        icon=OriginalCodeIcon.BACKGROUND_WORKER,
        icon_size=7.5,
    ),
    xy=(98.0, 8.0),
)

d.connect(web, api, label="REST / JSON", padding=1.5)
api.fork([engine, worker], at_x=88.0, padding=1.5)

d.draw(xy=(4.0, 4.0))
save()
```
