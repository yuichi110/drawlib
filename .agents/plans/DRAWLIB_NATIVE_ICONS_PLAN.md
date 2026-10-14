# Drawlib ネイティブアイコン移行 ＆ 概念アイコン・マルチクラウド・ITベンダー拡張計画書
(DRAWLIB NATIVE ICONS, VENDOR-NEUTRAL CONCEPT ICONS & IT ECOSYSTEM EXPANSION PLAN)

- **更新日**: 2026-10-14
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `tools/icons_src/` (Drawlib `images` プロジェクトとしてのアイコン描画ソース：`styles.py`, `utils.py`, `build.sh`, `original/*.py`, `gcp/*.py`, 等)
  - `tools/release_assets/v0.3/icons/` (`512×512` 透過 PNG 出力先：`original/*.png`, `gcp/*.png`, 等 ＋ `manifest.json`)
  - `tools/dcli/codegen/` (`./dcli codegen icon-original`, `icon-gcp`, `icon-aws`, `icon-azure`, および各 `*_icons` カテゴリ生成コマンド)
  - `src/drawlib/_icons/png_icons/` (プロバイダ実装および自動生成バインディング)
  - `src/drawlib/icons.py` (`architecture_icons` / `original` ＋ 3大クラウド `gcp`, `aws`, `azure` ＋ 14個の細分化ドメイン `*_icons` サブモジュール公開)
  - `src/drawlib/_diagrams/architecture/_icons.py`, `src/drawlib/diagrams/architecture.py` (`ArchitectureIcon` および各 `*Icon` Enum の公開と `Node` 統合)
  - `src/drawlib/_release_assets.py` (リリースアセットパッケージ定義)
  - `src/drawlib/_rules/` (`api.md`, `lib_icons.md`, `lib_diagrams.md` の更新)
  - `docs/` (公式ドキュメント・ショーケースおよびベンダー中立/マルチクラウド構成図のドッグフーディング)
  - `tests/` (各アイコンプロバイダおよび `ArchitectureDiagram` の単体テスト)

---

## 1. エグゼクティブサマリー & 設計原則 (Executive Summary & Design Principles)

### 1.1. 背景と目的
現在、`drawlib.icons.gcp` は Google Cloud 公式配布の ZIP アーカイブをダウンロードし、余白トリミングやリサイズ加工（[`tools/dcli/codegen/gcp_normalize.py`](../../tools/dcli/codegen/gcp_normalize.py)）を行って配布している。

今後、以下の3つの柱ですべてのアーキテクチャアイコンを **Drawlib 自身の `images` プロジェクト（`tools/icons_src/`）で宣言的にデザイン・描画する「Drawlib ネイティブアイコン（Drawlib-Flavored Native Icons）」** として整備・拡張する：
1. **ベンダー非依存の Drawlib オリジナル概念アイコン (`tools/icons_src/original/*.py` $\rightarrow$ `tools/release_assets/v0.3/icons/original/*.png`)**:
   - 初期設計書（RFP/RFC）、技術ブログ、書籍、ベンダー中立の標準構成図で最も需要が高い「Load Balancer」「Compute」「Database」「Message Queue」「Cache」「API Gateway」「AI Agent」等の一般概念を、洗練された **パステル 3色（Pastel Blue `#86A4F7`・Pastel Green `#7AD69E`・White `#FFFFFF`）＋ 細めダーク構造線（`Colors.Dark` `#323A48`, `2.7` units）** で統一デザインしたオリジナルアイコン群。
2. **Google Cloud 全アイコン完全ネイティブ移行 (`tools/icons_src/gcp/*.py` $\rightarrow$ `tools/release_assets/v0.3/icons/gcp/*.png`) ＆ AWS / Azure 独立モジュール**:
   - **GCP 全網羅（プラン A）**: 現行の 252 種（`core_products` 19種、`category_*` 26種、`legacy` 207種の現役＋廃止済みサービスすべて）に加え、4色モダンアイコンに対する **レガシー青六角形配色バリエーション** もすべて Drawlib ネイティブコードで作成し、外部 ZIP ダウンロード（`tools/original_assets/gcp`）を完全廃止する。
   - **AWS / Azure**: 各 50 種以上の主要クラウドサービス群。
3. **50個未満の IT トップベンダー・エコシステム別 14 カテゴリモジュール (`<category>_icons.<vendor>_<product>()`)**:
   - Cisco, VMware, Kubernetes, Docker, Linux, Apple/Mac, Microsoft Windows/M365, Google Chrome/Workspace, GitHub, HashiCorp, Cloudflare, 各種 DB, Datadog, OpenAI, Python 等を、AI が迷わず一発で推測できる 14 個の単一責務カテゴリモジュールとして提供。

---

### 1.2. 6つの基本設計原則

1. **Drawlib `images` プロジェクト (`tools/icons_src/`) による完全ドッグフーディング**:
   - すべてのアイコンは `tools/icons_src/<provider>/*.py` 配下の **1アイコン＝1 `.py` スクリプト** として管理し、`uv run drawlib build image tools/icons_src/ -o tools/release_assets/v0.3/icons/` でビルドする。
   - 1アイコン＝1 `.py` ファイル（単一 `save()` 呼び出し）とすることで、`tools/icons_src/.drawlib/cache.db` による **SQLite 差分キャッシュ** が 100% 機能し、2回目以降のビルドは変更ファイルのみ数秒で完了する。また、`uv run drawlib show tools/icons_src/gcp/compute_engine.py -g` で任意の1アイコンを即座にグリッド検証できる。
2. **「単一シルエット × パステル3色 × 細め構造線 (`2.7` units)」による洗練されたオリジナルアイコン (`original`)**:
   - 試作プロトタイプ（先行10個）の視覚検証を経て確定したデザイン言語を採用：
     - **造形密度**: `database` アイコンと同等の「単一シルエット＋最小限のインジケータ」に絞り、背景のレンガ壁や過剰な装飾・多色使いを排除する。
     - **構造線**: `Colors.Dark` (`#323A48`)、線幅 **`2.7` units**（細部インジケータは `2.0〜2.4` units）。
     - **配色**: **Pastel Blue (`#86A4F7`)**、**Pastel Green (`#7AD69E`)**、**White (`#FFFFFF`)** の3色パレットに統一し、`Styles.Neutral` / `PrimaryNeutral` / `SecondaryNeutral` のカード上で上品に調和させる。
3. **GCP は廃止サービス・レガシー配色を含め全数（252種＋レガシー版）を完全再現**:
   - 幾何学プリミティブ（六角プレート、等角キューブ、円弧＋カプセル線、3トーン青 `#5C85DE` / `#3367D6` / `#85A4E6` ＋ Google 4色）の再利用性が高いため、現行 `manifest.json` に存在する全 252 種（廃止・旧名称サービス含む）＋ 4色モダンアイコンのレガシー青配色版を余さず作成し、既存の全生成関数との後方互換性を 100% 維持する。
4. **AI が迷わず一発で推測できるモジュール体系**:
   - **ベンダー非依存の一般概念**: `drawlib.icons.architecture_icons` (`ArchitectureIcon`) — ベンダープレフィックスなしの概念名（`load_balancer()`, `compute()`, `database()`, `message_queue()` 等）。
   - **50個以上の大規模クラウドプロバイダ**: `drawlib.icons.gcp` (`GcpIcon`), `drawlib.icons.aws` (`AwsIcon`), `drawlib.icons.azure` (`AzureIcon`)。
   - **50個未満の IT トップベンダー群**: 単一責務に細分化した 14 個の `<category>_icons` モジュール ＋ `<vendor>_<product>()` 関数名。
5. **モジュール単位での `variant` 引数によるバリエーション吸収**:
   - 新旧デザインや表示形態のバリエーションが存在するモジュール（`gcp` など）では、**そのモジュール内で統一された `variant` 引数**（例：`gcp` なら `variant: Literal["modern", "legacy"] = "modern"`）を導入する。
6. **ビルド時 `512×512` PNG 正規化 ＆ `PngIconProvider` 100% 互換**:
   - `drawlib build image` で出力された透過 PNG に対し、アセット正規化ステップで **`512×512` 透過 PNG（内枠 `460×460` バウンディングボックス正規化）** と `manifest.json`（SHA256・bbox 記録）を生成し、既存の [`PngIconProvider`](../../src/drawlib/_icons/png_icons/_base.py)・[`ArchitectureDiagram`](../../src/drawlib/_diagrams/architecture/_diagram.py)・`style.image_*` と 100% 互換を維持する。

---

## 2. ビルドパイプライン & ディレクトリ構成 (`tools/icons_src/`)

### 2.1. ディレクトリツリー

```text
tools/
├── icons_src/                        # Drawlib `images` プロジェクト (uv run drawlib init images tools/icons_src)
│   ├── .drawlib/
│   │   └── cache.db                  # 単一 save() スクリプト単位のインクリメンタルビルドキャッシュ
│   ├── styles.py                     # 共通カラーパレット (Pastel Blue/Green, GCP 4色 & 3トーン青 等) & Style ヘルパー
│   ├── utils.py                      # 共通幾何学プリミティブ (draw_iso_cube, draw_cylinder_tier, draw_capsule 等)
│   ├── build.sh                      # build_image.sh 実行 + 512x512 正規化 & manifest.json 更新
│   ├── build_image.sh                # uv run drawlib build image tools/icons_src/ -o tools/release_assets/v0.3/icons/
│   ├── original/                     # オリジナル概念アイコン (*.py -> release_assets/v0.3/icons/original/*.png)
│   │   ├── compute.py
│   │   ├── container.py
│   │   ├── load_balancer.py
│   │   ├── api_gateway.py
│   │   ├── database.py
│   │   ├── object_storage.py
│   │   ├── message_queue.py
│   │   ├── firewall.py
│   │   ├── monitoring.py
│   │   ├── ai_agent.py
│   │   └── ... (約38種)
│   └── gcp/                          # GCP 全アイコン (*.py -> release_assets/v0.3/icons/gcp/*.png)
│       ├── compute_engine.py         # Modern 4色版 (core_products)
│       ├── compute_engine__legacy.py # Legacy 青六角形プレート版
│       ├── google_kubernetes_engine.py
│       ├── google_kubernetes_engine__legacy.py
│       ├── cloud_run.py
│       ├── cloud_run__legacy.py
│       ├── bigquery.py
│       ├── bigquery__legacy.py
│       ├── category_compute.py       # Category アイコン (26種)
│       ├── cloud_functions.py        # Legacy / 3トーン青アイコン (207種: 現役 + 廃止サービス網羅)
│       ├── pubsub.py
│       ├── stackdriver.py            # 廃止・旧名称サービスも含め全数収録
│       └── ... (全252種 + レガシー配色版)
└── release_assets/v0.3/icons/
    ├── original/                     # 512x512 透過 PNG + manifest.json
    └── gcp/                          # 512x512 透過 PNG + manifest.json
```

### 2.2. アイコン描画キャンバスの標準規格

| 項目 | 規格値 | 説明 |
| :--- | :--- | :--- |
| **論理キャンバス座標系** | `width=100, height=100, dpi=200` | 原点 `(0, 0)` が左下、中心が `(50, 50)`。`alpha=0.0` の透過キャンバス。 |
| **出力ピクセル解像度** | `512 × 512 px` (透過 RGBA) | `2000×2000 px` (4× スーパーサンプリング) で描画後、`LANCZOS` リサンプリングで内枠 `460×460 px` に正規化して `512×512 px` で保存。 |
| **セーフエリア（内枠）** | `x, y ∈ [8.0, 92.0]` | `512×512` における `460×460`（上下左右 26px マージン）に相当。すべての図形要素をこの範囲内に収める。 |
| **オリジナル基本ストローク幅** | 構造線 `2.7` units / 細部 `2.0–2.4` units | `Colors.Dark` (`#323A48`)。縮小配置時（`width=8.5`）にも線が重ならず軽快に見える太さ。 |

### 2.3. 共通カラーパレット & 幾何学プリミティブ (`styles.py` / `utils.py`)

1. **`tools/icons_src/styles.py`（確定カラーパレット）**:
   - **Original Icons (`original/`)**:
     - `ORIG_STROKE = 2.7`
     - `DARK = Colors.Dark` (`#323A48`)
     - `PASTEL_BLUE = "#86A4F7"` (メイン面：パステルコーンフラワーブルー)
     - `PASTEL_BLUE_LIGHT = "#ACC2FA"` (サブ面：淡いパステルブルー)
     - `PASTEL_GREEN = "#7AD69E"` (アクセント・稼働インジケータ面：パステルミントグリーン)
     - `WHITE = Colors.White` (`#FFFFFF`：カード背景・上面キャップ・抜け面)
   - **Google Cloud Icons (`gcp/`)**:
     - **Google 4-Color Palette (`modern`)**: `GCP_BLUE = "#4285F4"`, `GCP_RED = "#EA4335"`, `GCP_YELLOW = "#FBBC04"`, `GCP_GREEN = "#34A853"`, `GCP_DARK_BLUE = "#1A73E8"`
     - **GCP Tech 3-Tone Blues (`legacy` & 青系サービス)**: `GCP_TECH_MID = "#5C85DE"`, `GCP_TECH_DARK = "#3367D6"`, `GCP_TECH_LIGHT = "#85A4E6"`
     - **Hexagonal Plate Split Colors**: 左半分 `#4285F4` / 右半分 `#3367D6`（または `#5C85DE` / `#4285F4`）＋ 斜めドロップシャドウ `#2A56C6` ＋ 白抜き (`#FFFFFF`) センターシンボル。

2. **`tools/icons_src/utils.py`（共通幾何学プリミティブ）**:
   - `setup_icon_canvas()`: `setup(width=100, height=100, dpi=200, color=Colors.Canvas, alpha=0.0)` を呼び出す標準初期化関数。
   - `pt(units)`: 100×100 空間の線幅 `units` を Matplotlib ポイント単位（`units * 7.2`）へ変換。
   - `fill_style(fill_color, border_color=None, border_units=0.0, shape_r=0.0)` / `stroke_style(color, width_units)`
   - `draw_capsule(xy, width, height, color, border_color=None, border_units=0.0)`: 両端完全半円のカプセルバー。
   - `draw_round_segment(p1, p2, width_units, color)` / `draw_round_polyline(points, width_units, color, corner_r=0.0)`: ラウンドキャップ線分・折れ線。
   - `draw_iso_cube(cx, cy, radius, *, top_color, left_color, right_color, border_color=None, border_units=0.0)`: 等角投影キューブ。
   - `draw_cylinder_tier(cx, y_bottom, width, body_h, ry, *, body_color, top_color=None, border_color=DARK, border_units=2.7, draw_top_cap=True)`: 3D 円筒ティア。
   - `draw_sparkle_4pt(cx, cy, outer_r, inner_r, *, fill_color, border_color=None, border_units=0.0)`: AI/LLM 用の4芒星スパークル。
   - `draw_gcp_hex_badge(cx=50.0, cy=50.0, radius=42.0, *, variant="legacy")`: GCP レガシーアイコン共通の角丸六角形2トーンプレート。

---

## 3. モジュール全体マップ（全18モジュール：概念アイコン ＋ 3大クラウド ＋ 14カテゴリ `*_icons`）

| # | モジュール名 (`drawlib.icons.*`) | `tools/icons_src/` ディレクトリ | `ArchitectureDiagram` Enum | 対象技術領域（混在なしの単一責務） | 収録数目安 |
| :- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`architecture_icons`** | `tools/icons_src/original/` | `ArchitectureIcon` | **ベンダー非依存のシステム設計・インフラ一般概念** | 約 38 |
| **2** | **`gcp`** | `tools/icons_src/gcp/` | `GcpIcon` | **Google Cloud Platform** (現行全252種＋レガシー配色版＋エイリアス) | 252 + Legacy版 |
| **3** | **`aws`** | `tools/icons_src/aws/` | `AwsIcon` | **Amazon Web Services** (50+ 独立) | 約 52 |
| **4** | **`azure`** | `tools/icons_src/azure/` | `AzureIcon` | **Microsoft Azure** (50+ 独立) | 約 50 |
| **5** | **`network_icons`** | `tools/icons_src/network/` | `NetworkIcon` | **ネットワーク機器・CDN・LB・プロキシ** | 約 28 |
| **6** | **`security_icons`** | `tools/icons_src/security/` | `SecurityIcon` | **ファイアウォール・EDR・IDaaS・ゼロトラスト** | 約 22 |
| **7** | **`virtualization_icons`** | `tools/icons_src/virtualization/` | `VirtualizationIcon` | **仮想化・ハイパーバイザ・HCI・プライベートクラウド** | 約 18 |
| **8** | **`container_icons`** | `tools/icons_src/container/` | `ContainerIcon` | **Kubernetes・Docker・サービスメッシュ** | 約 28 |
| **9** | **`hardware_icons`** | `tools/icons_src/hardware/` | `HardwareIcon` | **物理サーバー・ストレージ機器・PC/スマホ端末枠** | 約 18 |
| **10** | **`os_icons`** | `tools/icons_src/os/` | `OsIcon` | **OS (Linux/Windows/Mac/iOS/Android) & ブラウザ** | 約 28 |
| **11** | **`workspace_icons`** | `tools/icons_src/workspace/` | `WorkspaceIcon` | **M365・Google Workspace・チャット・業務 SaaS** | 約 36 |
| **12** | **`git_icons`** | `tools/icons_src/git/` | `GitIcon` | **Git・GitHub・GitLab・Bitbucket** | 約 18 |
| **13** | **`devops_icons`** | `tools/icons_src/devops/` | `DevopsIcon` | **IaC (Terraform/Ansible)・CI/CD 自動化** | 約 18 |
| **14** | **`observability_icons`** | `tools/icons_src/observability/` | `ObservabilityIcon` | **監視・APM・ログ分析・インシデント管理** | 約 22 |
| **15** | **`database_icons`** | `tools/icons_src/database/` | `DatabaseIcon` | **RDBMS・NoSQL・インメモリ DB・DWH** | 約 20 |
| **16** | **`data_pipeline_icons`** | `tools/icons_src/data_pipeline/` | `DataPipelineIcon` | **ストリーミング (Kafka)・分散処理 (Spark)・ETL** | 約 16 |
| **17** | **`ai_icons`** | `tools/icons_src/ai/` | `AiIcon` | **生成 AI・LLM・AI エージェント/フレームワーク** | 約 18 |
| **18** | **`programming_icons`** | `tools/icons_src/programming/` | `ProgrammingIcon` | **プログラミング言語・Web FW・IDE** | 約 26 |

---

## 4. ベンダー非依存の Drawlib オリジナル概念アイコン詳細 (`tools/icons_src/original/` — 約 38 種)

### 4.1. デザイン言語（先行10個のプロトタイプ検証で確定）
- **単一シルエット原則**: `database` アイコンと同等のシンプルな情報密度を維持する（背景のレンガ壁や不要な小パーツを重ねない）。
- **構造線**: `Colors.Dark` (`#323A48`)、標準線幅 **`ORIG_STROKE = 2.7` units**（細部インジケータ・チェックマーク等は `2.0〜2.4` units）。
- **パステル3色パレット**:
  - **Pastel Blue (`#86A4F7`)**: 主要な構造面・コア要素
  - **Pastel Green (`#7AD69E`)**: サブ要素・分岐先ノード・稼働インジケータ・チェックマーク
  - **White (`#FFFFFF`)**: 筐体ベース面・円筒上面キャップ・内部カード面

### 4.2. 収録概念アイコンと視覚モチーフ一覧

| カテゴリ | 関数名 (`architecture_icons.<name>`) | 短縮エイリアス | シンプル化された視覚モチーフ設計（Pastel Blue / Green / White） |
| :--- | :--- | :--- | :--- |
| **Compute & Workloads** | `compute` *(済)*, `virtual_machine`, `container` *(済)*, `container_cluster`, `serverless_function`, `worker_job`, `autoscaling` | `vm` -> `virtual_machine`, `cluster` -> `container_cluster`, `function` -> `serverless_function`, `worker` -> `worker_job` | ・`compute`: 四辺に3本ずつピンが出た白枠 IC チップ＋中央 Pastel Blue コア＋右下 Pastel Green ドット<br>・`container`: 上面 White・左面 Pastel Blue・右面 Pastel Green のアイソメ立方体＋縦リブ線2本ずつ<br>・`container_cluster`: ピラミッド状に並んだ3つのアイソメキューブ<br>・`serverless_function`: 角丸白プレート内の Pastel Blue 稲妻ボルト<br>・`worker_job`: 白角丸ジョブカード＋Pastel Blue ギア |
| **Networking & Traffic** | `load_balancer` *(済)*, `api_gateway` *(済)*, `reverse_proxy`, `service_mesh`, `cdn`, `dns`, `router`, `switch`, `virtual_network`, `vpn_tunnel` | `lb` -> `load_balancer`, `apigw` -> `api_gateway`, `vpc` -> `virtual_network`, `vpn` -> `vpn_tunnel` | ・`load_balancer`: 左の Pastel Blue 入口円ノードから右の3つの Pastel Green 円ノードへ分岐するツリー<br>・`api_gateway`: 左右2本の白カプセルピラーの間を通過する上段右向き Pastel Blue 矢印＆下段左向き Pastel Green 矢印<br>・`cdn`: 白グローブ球体＋外周3つの Pastel Blue/Green エッジドット<br>・`dns`: ドメインバーと IP ノードを繋ぐ解決矢印<br>・`router`: 円筒上面の4方向矢印<br>・`switch`: フラット筐体上の左右交互矢印 |
| **Database & Storage** | `database` *(済)*, `nosql_database`, `in_memory_cache`, `object_storage` *(済)*, `block_storage`, `file_storage`, `data_warehouse`, `vector_database`, `search_engine` | `db` / `rdbms` -> `database`, `nosql` -> `nosql_database`, `cache` -> `in_memory_cache`, `bucket` -> `object_storage`, `disk` -> `block_storage`, `dwh` -> `data_warehouse`, `vector_db` -> `vector_database` | ・`database`: 3段積み Pastel Blue 円筒シリンダー（上面 White）＋各段右側に Pastel Green ドット<br>・`object_storage`: 上部ハンドル弧＋白リムバー＋Pastel Blue 台形バケット＋右下 Pastel Green ドット<br>・`nosql_database`: 円筒シリンダー＋`{ }` シンボル<br>・`in_memory_cache`: メモリカード＋稲妻シンボル<br>・`data_warehouse`: シリンダー＋分析バー<br>・`vector_database`: 3軸座標空間と Pastel Blue/Green ノード |
| **Messaging & Streaming** | `message_queue` *(済)*, `pub_sub`, `event_stream`, `etl_pipeline`, `webhook`, `scheduler` | `queue` / `mq` -> `message_queue`, `stream` -> `event_stream`, `pipeline` -> `etl_pipeline`, `cron` -> `scheduler` | ・`message_queue`: 上下2本の水平レール間に整列した3つの角丸縦ブロック（左2つ Pastel Blue、右先頭 Pastel Green）<br>・`pub_sub`: 中央ハブ円から放射状に広がる購読ノード<br>・`event_stream`: 2本の滑らかなウェーブ線とストリームドット<br>・`etl_pipeline`: 漏斗（ファネル）＋出力ブロック<br>・`scheduler`: シンプルな時計盤＋トリガー矢印 |
| **Security & Observability** | `firewall` *(済)*, `waf`, `identity_auth`, `secret_vault`, `certificate_tls`, `monitoring` *(済)*, `logging`, `distributed_tracing`, `alert_incident` | `auth` / `iam` -> `identity_auth`, `vault` / `kms` -> `secret_vault`, `tls` -> `certificate_tls`, `metrics` -> `monitoring`, `tracing` -> `distributed_tracing`, `alert` -> `alert_incident` | ・`firewall`: Pastel Blue の単一シールド＋中央 White 円バッジ＋Pastel Green チェックマーク<br>・`monitoring`: White モニター画面（Pastel Blue スタンド）＋パルス波形折れ線＋ピーク頂点 Pastel Green ドット<br>・`identity_auth`: 人物シルエット＋バッジ<br>・`secret_vault`: シンプルな南京錠（パドロック）<br>・`logging`: ログシート＋虫眼鏡<br>・`distributed_tracing`: 段違いに並んだ3本のウォーターフォール・スパンバー |
| **Clients, Users & AI** | `user`, `user_group`, `web_browser`, `mobile_app`, `iot_device`, `llm_model`, `ai_agent` *(済)* | `users` -> `user_group`, `browser` -> `web_browser`, `mobile` -> `mobile_app`, `llm` -> `llm_model`, `agent` -> `ai_agent` | ・`ai_agent`: 3本の軌道アークで結ばれた3つの Pastel Green 外周ノード＋中央 Pastel Blue 4芒星スパークル（中心 White ドット）<br>・`user` / `user_group`: 人物アバター<br>・`web_browser`: ブラウザウィンドウ枠<br>・`mobile_app`: スマートフォン筐体<br>・`llm_model`: スパークル＋ニューラルノード |

---

## 5. Google Cloud 完全ネイティブ移行詳細 (`tools/icons_src/gcp/` — 全252種＋レガシー配色版)

### 5.1. 収録範囲（プラン A：全数網羅＋レガシー配色）
既存の [`tools/release_assets/v0.3/icons/gcp/manifest.json`](../../tools/release_assets/v0.3/icons/gcp/manifest.json) に収録されている **全 252 種のプライマリアイコン ＋ 8 エイリアス** を 1 つも欠けさせることなく `tools/icons_src/gcp/*.py` で完全再現し、さらにモダン4色アイコンにはレガシー青配色版も用意する：

1. **Core Products（19 種 — Modern 4色版 ＆ Legacy 青配色版の両方を作成）**:
   - `ai_hypercomputer`, `alloydb`, `anthos`, `apigee`, `bigquery`, `cloud_run`, `cloud_spanner`, `cloud_sql`, `cloud_storage`, `compute_engine`, `distributed_cloud`, `gke` (`google_kubernetes_engine`), `hyperdisk`, `looker`, `mandiant`, `security_command_center`, `security_operations`, `threat_intelligence`, `vertex_ai`
   - それぞれ `<name>.py`（現行の Google 4色マルチカラー版）と `<name>__legacy.py`（GCP ブルー六角形プレートまたは3トーン青によるレガシー配色版）の両方を作成する。
2. **Category Icons（26 種 — Modern 4色版 ＆ Legacy 青配色版）**:
   - `category_ai_machine_learning`, `category_agents`, `category_business_intelligence`, `category_collaboration`, `category_compute`, `category_containers`, `category_data_analytics`, `category_databases`, `category_developer_tools`, `category_devops`, `category_hybrid_multicloud`, `category_integration_services`, `category_management_tools`, `category_maps_geospatial`, `category_marketplace`, `category_media_services`, `category_migration`, `category_mixed_reality`, `category_networking`, `category_observability`, `category_operations`, `category_security_identity`, `category_serverless_computing`, `category_storage`, `category_web3`, `category_web_mobile`
3. **Legacy / 3-Tone Blue Icons（207 種 — 現役サービス＋廃止・旧名称サービスすべて網羅）**:
   - **現役の主要サービス**: `app_engine`, `artifact_registry`, `automl`, `bare_metal_solutions`, `batch`, `bigtable`, `cloud_api_gateway`, `cloud_armor`, `cloud_build`, `cloud_cdn`, `cloud_composer`, `cloud_data_fusion`, `cloud_deploy`, `cloud_dns`, `cloud_domains`, `cloud_endpoints`, `cloud_External_ip_addresses`, `cloud_firewall_rules`, `cloud_functions`, `cloud_interconnect`, `cloud_load_balancing`, `cloud_logging`, `cloud_monitoring`, `cloud_nat`, `cloud_natural_language_api`, `cloud_network`, `cloud_router`, `cloud_routes`, `cloud_scheduler`, `cloud_security_scanner`, `cloud_tasks`, `cloud_translation_api`, `cloud_vision_api`, `cloud_vpn`, `data_catalog`, `dataflow`, `datalab`, `dataplex`, `dataprep`, `dataproc`, `datastream`, `dialogflow`, `document_ai`, `eventarc`, `filestore`, `firestore`, `identity_and_access_management`, `identity_Aware_proxy`, `identity_platform`, `key_management_service`, `memorystore`, `network_connectivity_center`, `network_intelligence_center`, `network_security`, `network_tiers`, `network_topology`, `persistent_disk`, `private_service_connect`, `pubsub`, ` Recommendations_ai`, `secret_manager`, `service_directory`, `speech_to_text`, `text_to_speech`, `traffic_director`, `transfer_appliance`, `virtual_private_cloud`, `vmware_engine`, `workflows` 等。
   - **廃止・統合済み・旧名称サービス（後方互換のため全数収録）**: `stackdriver`, `container_builder`, `google_container_registry`, `cloud_iot_core`, `ai_hub`, `ai_platform`, `ai_platform_unified`, `automl_natural_language`, `automl_tables`, `automl_translation`, `automl_video_intelligence`, `automl_vision`, `cloud_inference_api`, `data_labeling`, `genomics`, `apigee_sense`, `anthos_config_management`, `anthos_service_mesh` 等を含む残り全アイコン。

---

## 6. 段階的実装ロードマップ (Phased Rollout Plan)

| フェーズ | マイルストーン | 主な作業内容と完了基準 |
| :--- | :--- | :--- |
| **Phase 1: `tools/icons_src/` 基盤構築 ＆ 先行 20 個の移行** | `tools/icons_src/` 初期化 ＆ パイプライン確立 | 1. `uv run drawlib init images tools/icons_src` でプロジェクトを初期化。<br>2. `tools/icons_src/styles.py` と `tools/icons_src/utils.py` に確定したパステルパレット・GCP パレット・共通幾何学プリミティブを配置。<br>3. [`.drawlib/scratch/icon_proto/`](../../.drawlib/scratch/icon_proto) の先行 20 個（`original` 10個 ＋ `gcp` 10個）を `tools/icons_src/{original,gcp}/*.py`（1アイコン＝1 `.py` ファイル）へ移植。<br>4. `tools/icons_src/build.sh`（`drawlib build image` ＋ `512×512` 正規化 ＆ `manifest.json` 更新）を構築し、動作と出力画像を検証。 |
| **Phase 2: オリジナル概念アイコン (`original/`) 全 38 種の完成** | `tools/icons_src/original/` 全数完成 ＆ バインディング統合 | 1. 残りのオリジナル概念アイコン（約 28 種）をパステル3色（`#86A4F7` / `#7AD69E` / `#FFFFFF`）＋ `2.7`-unit ダーク構造線で並列作成・視覚レビュー。<br>2. `tools/release_assets/v0.3/icons/original/` の生成、`drawlib.icons.architecture_icons`（または `original`）および `ArchitectureIcon` Enum のコード生成・単体テスト実装。 |
| **Phase 3: GCP アイコン (`gcp/`) 全 252 種＋レガシー配色の完全ネイティブ化** | `tools/icons_src/gcp/` 全数完成 ＆ 外部アセット廃止 | 1. `core_products` 残り 9 種＋レガシー配色 19 種、`category_*` 26 種、`legacy` 205 種をサブエージェント並列バッチで `tools/icons_src/gcp/*.py` として作成・視覚レビュー。<br>2. `tools/release_assets/v0.3/icons/gcp/` を 100% `tools/icons_src/gcp/` からのビルド出力で置き換え、`variant: Literal["modern", "legacy"] = "modern"` 対応を追加。<br>3. `tools/original_assets/gcp/` および `gcp_download.py` を廃止し、`./dcli test target icons` と `./dcli docs build site` で完全互換を検証。 |
| **Phase 4: `aws`, `azure` および 14 カテゴリ `*_icons` の順次拡張** | マルチクラウド ＆ IT ベンダーアイコン拡張 | 1. `tools/icons_src/{aws,azure,<category>}/` サブディレクトリを追加し、同一の `images` プロジェクト基盤上で順次ビルド・公開。<br>2. `src/drawlib/_rules/` および公式ドキュメントを更新し、`./dcli code-check all` と `./dcli test all` をパスさせる。 |

---

## 7. 品質保証・検証チェックリスト (Verification Criteria)

1. **視覚レビュー基準（Multimodal Review）**:
   - 各アイコンを `512×512` 単体画像および `width=8.5` の実ノード縮小プレビューの両方で `view_file` 確認し、線の癒着・文字干渉・余白偏りがないこと。
   - オリジナルアイコンは `database` アイコンを基準としたシンプルさ（単一シルエット、線幅 `2.7` units、Pastel Blue `#86A4F7` / Pastel Green `#7AD69E` / White `#FFFFFF`）を厳守すること。
   - GCP アイコンは [`tools/original_assets/gcp/`](../../tools/original_assets/gcp) の公式モチーフの象徴性と色分けを忠実に再現しつつ、シャープなベクター品質を実現すること。
2. **技術・互換性基準**:
   - `1 icon = 1 .py file`（単一 `save()`）により `tools/icons_src/.drawlib/cache.db` の差分キャッシュが有効に機能すること。
   - `style.alpha`、`style.image_tint_color`、`style.image_border_*`、`style.angle` がすべての生成アイコンで正常に機能すること。
   - 既存の全テスト（`./dcli test all`）および全ドキュメントビルド（`./dcli docs build --all`）がエラーなく完了すること。
