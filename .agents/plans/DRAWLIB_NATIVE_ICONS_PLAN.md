# Drawlib ネイティブアイコン移行 ＆ 概念アイコン・マルチクラウド・ITベンダー拡張計画書
(DRAWLIB NATIVE ICONS, VENDOR-NEUTRAL CONCEPT ICONS & IT ECOSYSTEM EXPANSION PLAN)

- **更新日**: 2026-10-12
- **対象バージョン**: Drawlib 次期マイナーリリース (`v0.3.x` / `v0.4.x`)
- **対象モジュール**:
  - `tools/dcli/codegen/icons/` (Drawlib 宣言的コードによるアイコン描画・512×512 PNG ビルダ基盤、共通幾何学ヘルパー、各プロバイダ/カテゴリ定義)
  - `tools/dcli/codegen/cli.py` (`./dcli codegen icon-architecture`, `icon-gcp`, `icon-aws`, `icon-azure`, および各 `*_icons` カテゴリ生成コマンド)
  - `src/drawlib/_icons/png_icons/` (プロバイダ実装および自動生成バインディング)
  - `src/drawlib/icons.py` (`architecture_icons` ＋ 3大クラウド `gcp`, `aws`, `azure` ＋ 14個の細分化ドメイン `*_icons` サブモジュール公開)
  - `src/drawlib/_diagrams/architecture/_icons.py`, `src/drawlib/diagrams/architecture.py` (`ArchitectureIcon` および各 `*Icon` Enum の公開と `Node` 統合)
  - `src/drawlib/_release_assets.py` (リリースアセットパッケージ定義)
  - `src/drawlib/_rules/` (`api.md`, `lib_icons.md`, `lib_diagrams.md` の更新)
  - `docs/` (公式ドキュメント・ショーケースおよびベンダー中立/マルチクラウド構成図のドッグフーディング)
  - `tests/` (各アイコンプロバイダおよび `ArchitectureDiagram` の単体テスト)

---

## 1. エグゼクティブサマリー & 設計原則 (Executive Summary & Design Principles)

### 1.1. 背景と目的
現在、`drawlib.icons.gcp` は Google Cloud 公式配布の ZIP アーカイブをダウンロードし、余白トリミングやリサイズ加工（[`tools/dcli/codegen/gcp_normalize.py`](../../tools/dcli/codegen/gcp_normalize.py)）を行って配布している。

今後、以下の3つの柱ですべてのアーキテクチャアイコンを **Drawlib 自身の Python コードで宣言的にデザイン・描画する「Drawlib ネイティブアイコン（Drawlib-Flavored Native Icons）」** として整備・拡張する：
1. **ベンダー非依存の Drawlib 独自アーキテクチャ概念アイコン (`drawlib.icons.architecture_icons` / `ArchitectureIcon`)**:
   - 初期設計書（RFP/RFC）、技術ブログ、書籍、ベンダー中立の標準構成図で最も需要が高い「Load Balancer」「Compute」「Database」「Message Queue」「Cache」「API Gateway」「AI Agent」等の一般概念を、Drawlib 公式ブランドトーン（[`case_study_brand_assets.md`](../../docs/docs_src/09_ai_agents_and_advanced/case_study_brand_assets.md)）でデザインしたオリジナルアイコン群。
2. **50個以上の3大パブリッククラウド独立モジュール (`gcp`, `aws`, `azure`)**:
   - Google Cloud、AWS、Microsoft Azure の主要サービス群。
3. **50個未満の IT トップベンダー・エコシステム別 14 カテゴリモジュール (`<category>_icons.<vendor>_<product>()`)**:
   - Cisco, VMware, Kubernetes, Docker, Linux, Apple/Mac, Microsoft Windows/M365, Google Chrome/Workspace, GitHub, HashiCorp, Cloudflare, 各種 DB, Datadog, OpenAI, Python 等を、AI が迷わず一発で推測できる 14 個の単一責務カテゴリモジュールとして提供。

---

### 1.2. 6つの基本設計原則

1. **Drawlib Dogfooding as Source of Truth（純 Python コードによるアイコン定義）**:
   - すべてのアイコンは `tools/dcli/codegen/icons/` 配下の Drawlib Python コード（`shapes`, `lines`, `lines_bezier`, `polygon`, `text`, `phosphor` 等の組み合わせ）を唯一の Source of Truth (SoT) とする。
   - 外部の公式アイコン ZIP ダウンロード処理（`tools/original_assets/gcp` 等）は廃止し、100% リポジトリ内の Python コードから再現可能にする。
2. **「普遍的メタファー × Drawlib ブランドトーン」によるベンダー非依存アイコン (`architecture_icons`)**:
   - 奇抜な抽象図形をゼロから発明するのではなく、世界中のエンジニアが共有している **普遍的な構造メタファー（シリンダー＝DB、1対3分岐＝LB、ICチップ＝Compute、パイプ内ブロック＝Queue 等）** を、Drawlib 公式デザイン言語（`Colors.Dark` `#323A48` の構造線 ＋ `Colors.Primary` / `Secondary` / `Accent` のフラット色面）で体系的にデザインする。
   - これにより、Drawlib のデフォルトカード（`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`）と 100% 調和し、かつクラウドベンダーのマイナーサービスに対する「カテゴリ共通フォールバックアイコン」の基礎構造としても再利用できる。
3. **AI が迷わず一発で推測できる「概念モジュール ＋ 3大クラウド ＋ 14個の細分化 `<category>_icons`」**:
   - **ベンダー非依存の一般概念**: `drawlib.icons.architecture_icons` (`ArchitectureIcon`) — ベンダープレフィックスなしの概念名（`load_balancer()`, `compute()`, `database()`, `message_queue()` 等）。
   - **50個以上の大規模クラウドプロバイダ**: `drawlib.icons.gcp` (`GcpIcon`), `drawlib.icons.aws` (`AwsIcon`), `drawlib.icons.azure` (`AzureIcon`)。
   - **50個未満の IT トップベンダー群**: 単一責務に細分化した 14 個の `<category>_icons` モジュール ＋ `<vendor>_<product>()` 関数名（例：`observability_icons.datadog_logo()`, `git_icons.github_actions()`, `virtualization_icons.vmware_vsphere()`, `network_icons.cisco_router()`, `programming_icons.python_logo()`）。
4. **「本家リスペクトの認知性」と「Drawlib 統一デザイン言語」の両立**:
   - ベンダーアイコンでは **「象徴的なブランド/カテゴリ配色」＋「核となる幾何学モチーフ」** を踏襲しつつ、公式 SVG の座標トレース（デッドコピー）を避け、細部を Drawlib 流のクリーンなフラット図形・統一された線幅・角丸へデフォルメ・再設計する。
5. **モジュール単位での `variant` 引数によるバリエーション吸収**:
   - 新旧デザインや表示形態のバリエーションが存在するモジュール（`gcp` など）では、**そのモジュール内で統一された `variant` 引数**（例：`gcp` なら `variant: Literal["modern", "legacy"] = "modern"`）を導入する。
   - 全モジュールで無理に共通の `variant` 型を強制するのではなく、**モジュールごとに意味のある `variant` のみを定義**する（バリエーションが不要なモジュールではシンプルに保つ）。
6. **ビルド時 PNG コンパイル方式の維持（`PngIconProvider` 100% 互換）＆ Tier 構成**:
   - 既存の [`PngIconProvider`](../../src/drawlib/_icons/png_icons/_base.py)・[`ArchitectureDiagram`](../../src/drawlib/_diagrams/architecture/_diagram.py)・`style.image_*` との完全互換性と高速レンダリングを維持するため、`./dcli codegen` 実行時に Drawlib で **`512×512` 透過 PNG** へ事前レンダリングして `tools/release_assets/` に出力する。

---

## 2. モジュール全体マップ（全18モジュール：概念アイコン ＋ 3大クラウド ＋ 14カテゴリ `*_icons`）

| # | モジュール名 (`drawlib.icons.*`) | `ArchitectureDiagram` Enum | 対象技術領域（混在なしの単一責務） | 代表的な呼び出し例 | 収録数目安 |
| :- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`architecture_icons`** | `ArchitectureIcon` | **ベンダー非依存のシステム設計・インフラ一般概念** | `architecture_icons.load_balancer()`, `architecture_icons.compute()`, `architecture_icons.database()` | 約 38 |
| **2** | **`gcp`** | `GcpIcon` | **Google Cloud Platform** (50+ 独立) | `gcp.compute_engine()`, `gcp.bigquery()` | 約 50+ |
| **3** | **`aws`** | `AwsIcon` | **Amazon Web Services** (50+ 独立) | `aws.ec2()`, `aws.s3()`, `aws.lambda_function()` | 約 52 |
| **4** | **`azure`** | `AzureIcon` | **Microsoft Azure** (50+ 独立) | `azure.virtual_machines()`, `azure.cosmos_db()` | 約 50 |
| **5** | **`network_icons`** | `NetworkIcon` | **ネットワーク機器・CDN・LB・プロキシ** | `network_icons.cisco_router()`, `network_icons.cloudflare_cdn()`, `network_icons.f5_big_ip()` | 約 28 |
| **6** | **`security_icons`** | `SecurityIcon` | **ファイアウォール・EDR・IDaaS・ゼロトラスト** | `security_icons.paloalto_firewall()`, `security_icons.okta_sso()`, `security_icons.crowdstrike_falcon()` | 約 22 |
| **7** | **`virtualization_icons`** | `VirtualizationIcon` | **仮想化・ハイパーバイザ・HCI・プライベートクラウド** | `virtualization_icons.vmware_vsphere()`, `virtualization_icons.nutanix_ahv()`, `virtualization_icons.openstack_logo()` | 約 18 |
| **8** | **`container_icons`** | `ContainerIcon` | **Kubernetes・Docker・サービスメッシュ** | `container_icons.k8s_pod()`, `container_icons.docker_container()`, `container_icons.istio_logo()` | 約 28 |
| **9** | **`hardware_icons`** | `HardwareIcon` | **物理サーバー・ストレージ機器・PC/スマホ端末枠** | `hardware_icons.dell_poweredge()`, `hardware_icons.hw_rack_server()`, `hardware_icons.hw_san_storage()` | 約 18 |
| **10** | **`os_icons`** | `OsIcon` | **OS (Linux/Windows/Mac/iOS/Android) & ブラウザ** | `os_icons.linux_ubuntu()`, `os_icons.apple_macos()`, `os_icons.microsoft_windows()`, `os_icons.google_chrome()` | 約 28 |
| **11** | **`workspace_icons`** | `WorkspaceIcon` | **M365・Google Workspace・チャット・業務 SaaS** | `workspace_icons.microsoft_teams()`, `workspace_icons.google_gmail()`, `workspace_icons.slack_logo()`, `workspace_icons.salesforce_logo()` | 約 36 |
| **12** | **`git_icons`** | `GitIcon` | **Git・GitHub・GitLab・Bitbucket** | `git_icons.github_logo()`, `git_icons.github_actions()`, `git_icons.gitlab_ci()`, `git_icons.git_pull_request()` | 約 18 |
| **13** | **`devops_icons`** | `DevopsIcon` | **IaC (Terraform/Ansible)・CI/CD 自動化** | `devops_icons.hashicorp_terraform()`, `devops_icons.ansible_logo()`, `devops_icons.jenkins_logo()`, `devops_icons.argocd_logo()` | 約 18 |
| **14** | **`observability_icons`** | `ObservabilityIcon` | **監視・APM・ログ分析・インシデント管理** | `observability_icons.datadog_logo()`, `observability_icons.grafana_logo()`, `observability_icons.prometheus_logo()`, `observability_icons.sentry_logo()` | 約 22 |
| **15** | **`database_icons`** | `DatabaseIcon` | **RDBMS・NoSQL・インメモリ DB・DWH** | `database_icons.oracle_db()`, `database_icons.postgresql_logo()`, `database_icons.redis_logo()`, `database_icons.snowflake_logo()` | 約 20 |
| **16** | **`data_pipeline_icons`** | `DataPipelineIcon` | **ストリーミング (Kafka)・分散処理 (Spark)・ETL** | `data_pipeline_icons.apache_kafka()`, `data_pipeline_icons.databricks_logo()`, `data_pipeline_icons.apache_airflow()` | 約 16 |
| **17** | **`ai_icons`** | `AiIcon` | **生成 AI・LLM・AI エージェント/フレームワーク** | `ai_icons.openai_logo()`, `ai_icons.anthropic_claude()`, `ai_icons.google_gemini()`, `ai_icons.langchain_logo()` | 約 18 |
| **18** | **`programming_icons`** | `ProgrammingIcon` | **プログラミング言語・Web FW・IDE** | `programming_icons.python_logo()`, `programming_icons.go_logo()`, `programming_icons.react_logo()`, `programming_icons.microsoft_vscode()` | 約 26 |

---

## 3. 技術アーキテクチャ & ビルドパイプライン仕様

### 3.1. アイコン描画キャンバスの標準規格

| 項目 | 規格値 | 説明 |
| :--- | :--- | :--- |
| **論理キャンバス座標系** | `width=100, height=100` | 原点 `(0, 0)` が左下、中心が `(50, 50)`。直感的に座標計算できる 100×100 空間。 |
| **出力ピクセル解像度** | `512 × 512 px` (透過 RGBA) | 高解像度レンダリング＋ `460×460` 内枠正規化で出力。 |
| **セーフエリア（内枠）** | `x, y ∈ [5.0, 95.0]` (`90×90`) | `512×512` における `460×460`（上下左右約 5% マージン）に相当。すべての図形要素をこの範囲内に収める。 |
| **基本ストローク幅** | 太線 `3.5–4.5` / 中線 `2.2–3.0` | 図面上で `width=7.5〜12.0` units に縮小配置された際にも潰れず鮮明に視認できる線幅。 |
| **最小ディテール制約** | 要素間ギャップ `>= 2.5` units | 縮小時に線同士が癒着しないよう、細かすぎる網目や極小テキストを排除する。 |

### 3.2. 共通幾何学パーツライブラリ (`tools/dcli/codegen/icons/_primitives.py`)
1. **ベースプレート / コンテナ系**:
   - `draw_hex_plate(xy, radius, *, fill_color, border_color=None, corner_r=4.0)`: GCP 等で使われる角丸六角形プレートおよび2分割/3分割シェード。
   - `draw_squircle_badge(xy, size, *, fill_color, border_color=None, corner_r=16.0)`: AWS カテゴリバッジや SaaS/OS アプリアイコン用の角丸スクエア。
   - `draw_shield_base(xy, width, height, *, fill_color, split_shade=True)`: セキュリティ・認証系シールド。
2. **立体・インフラモチーフ系**:
   - `draw_iso_cube(xy, radius, *, top_color, left_color, right_color, stroke_color=None, stroke_width=0)`: GKE、K8s、VMware、コンテナ等で多用するアイソメトリック（等角投影）キューブ。
   - `draw_cylinder_stack(xy, width, height, *, tiers=3, fill_color, top_color, gap=2.5)`: データベース、ストレージ、Cisco ルーター等で多用する円筒・積層ディスク。
   - `draw_chip_pins(xy, core_size, *, pin_count_per_side=3, pin_length=8.0, pin_width=3.5, color)`: Compute / CPU / AI アクセラレータ用の IC チップピン配列。
   - `draw_server_rack(xy, width, height, *, slots=3, color, led_color)`: 物理サーバー・ESXi・ベアメタル用のラックブレード。
3. **ネットワーク・デバイス・ドキュメント・記号系**:
   - `draw_cloud_silhouette(xy, width, height, *, fill_color, stroke_color=None)`: クラウド境界・CDN・SaaS 用の黄金比クラウド形状。
   - `draw_device_frame(xy, width, height, *, variant="laptop" | "monitor" | "phone" | "tablet")`: Mac / Windows / iOS / Android 端末フレーム。
   - `draw_doc_sheet(xy, width, height, *, fold_size, color, accent_color)`: Office (Word/Excel/PPT) や Google Docs/Sheets/Slides 用のドキュメントシート基底。
   - `draw_magnifying_glass(...)`, `draw_node_tree(...)`, `draw_directional_arrows(...)`

### 3.3. モジュール単位の `variant` によるバリエーション吸収

`variant` は全モジュール横断で無理に共通化せず、**各モジュール（`gcp` 等）の単位で意味のあるバリエーションを定義・統一**する：

```python
# 例: drawlib.icons.gcp モジュール内の定義
GcpIconVariant = Literal["modern", "legacy"]

def compute_engine(
    xy: Coordinate,
    width: PosFloat,
    *,
    variant: GcpIconVariant = "modern",
    style: Style,
) -> None:
    _write(xy=xy, width=width, name="compute_engine", variant=variant, style=style)
```

- **モジュール別の `variant` 設計例**:
  - **`gcp`**: `variant: Literal["modern", "legacy"] = "modern"`
    - `"modern"`（デフォルト）：現行の Google 4色マルチカラー（GCE, BigQuery, Cloud Run, GCS, Cloud SQL, Vertex AI 等）および現行フラットアイコン。
    - `"legacy"`：伝統的な **GCP ブルー六角形プレート＋白抜きシンボル**（またはブルートーン構造体）。図面全体を落ち着いた GCP ブルーの六角形バッジで統一したい場合に最適。
  - **`architecture_icons`**: `variant: Literal["color", "mono"] = "color"`
    - `"color"`（デフォルト）：Drawlib セマンティックカラー（`Primary`, `Secondary`, `Accent`, `Dark`）によるマルチトーンアイコン。
    - `"mono"`：単色スレートダーク（`Colors.Dark`）のクリーンな構造アイコン。
  - **単一スタイルで十分な `*_icons` モジュール**: 不要な `variant` を無理に持たせず、必要が生じたモジュールのみそのモジュール固有の `Literal` を定義する。
- **ファイル解決と安全なフォールバック規則**:
  - デフォルト時は `{icon_name}.png`、非デフォルトの `variant` 指定時は `{icon_name}__{variant}.png` を探し、もし該当ファイルが存在しないアイコンでは自動的に `{icon_name}.png` へフォールバックする。

---

## 4. ベンダー非依存の Drawlib 独自概念アイコン詳細：`drawlib.icons.architecture_icons` (`ArchitectureIcon` — 約 38 種)

### 4.1. デザイン言語（Drawlib Visual Identity 準拠）
- **構造線とベースカラー**: [`case_study_brand_assets.md`](../../docs/docs_src/09_ai_agents_and_advanced/case_study_brand_assets.md) の公式ブランドロゴと同一の **`Colors.Dark` (`#323A48`)** を構造アウトラインに使用。
- **カテゴリ別セマンティックカラー割り当て**:
  - **Compute & Workloads**: `Colors.Primary` (`#4862DA`) & `Colors.Primary1` (`#E3E8FA`)
  - **Networking & Traffic**: `Colors.Secondary` (`#2A989A`) & `Colors.Secondary1` (`#DCF2F2`)
  - **Database & Storage**: `Colors.Primary` × `Colors.Secondary` ツートーン
  - **Messaging & Streaming**: `Colors.Accent` (`#8037C3`) & `Colors.Accent1` (`#EDE2F8`)
  - **Security & Observability**: `Colors.Error` / `Colors.Warning` / `Colors.Success` アクセント

### 4.2. 収録概念アイコンと視覚モチーフ一覧

| カテゴリ | 関数名 (`architecture_icons.<name>`) | 短縮エイリアス | 誰が見ても一目でわかる視覚モチーフ設計 |
| :--- | :--- | :--- | :--- |
| **Compute & Workloads** | `compute`, `virtual_machine`, `container`, `container_cluster`, `serverless_function`, `worker_job`, `autoscaling` | `vm` -> `virtual_machine`, `cluster` -> `container_cluster`, `function` -> `serverless_function`, `worker` -> `worker_job` | ・`compute`: 四辺に3本ずつピンが出た IC チップ＋中央 `Primary` コア<br>・`container`: 縦リブ溝付きのアイソメトリック立方体<br>・`container_cluster`: ピラミッド状に結合した3つのアイソメキューブ<br>・`serverless_function`: 角丸プレート内の稲妻ボルト＋`{ }` ブラケット<br>・`worker_job`: 2枚重なったジョブカード＋前面の回転ギア |
| **Networking & Traffic** | `load_balancer`, `api_gateway`, `reverse_proxy`, `service_mesh`, `cdn`, `dns`, `router`, `switch`, `virtual_network`, `vpn_tunnel` | `lb` -> `load_balancer`, `apigw` -> `api_gateway`, `vpc` -> `virtual_network`, `vpn` -> `vpn_tunnel` | ・`load_balancer`: 1つの入口ノードから3つのバックエンドへ均等分岐する矢印ツリー<br>・`api_gateway`: 2本のゲート門柱の間を通過する双方向パケット矢印<br>・`cdn`: 経緯線入り地球（グローブ）の周囲に配置された3つの配信エッジノード<br>・`dns`: 上部のドメインブロックと下部の IP ノードを繋ぐ解決矢印<br>・`router`: 円筒上面の中心向き/外向き4方向クロス矢印<br>・`switch`: フラット筐体上の左右交互4本平行矢印 |
| **Database & Storage** | `database`, `nosql_database`, `in_memory_cache`, `object_storage`, `block_storage`, `file_storage`, `data_warehouse`, `vector_database`, `search_engine` | `db` / `rdbms` -> `database`, `nosql` -> `nosql_database`, `cache` -> `in_memory_cache`, `bucket` -> `object_storage`, `disk` -> `block_storage`, `dwh` -> `data_warehouse`, `vector_db` -> `vector_database` | ・`database`: 3段積み円筒シリンダー＋右側稼働インジケータドット<br>・`nosql_database`: シリンダー前面に JSON ドキュメント `{ }` バッジ<br>・`in_memory_cache`: 高速メモリチップ＋右下の稲妻バッジ<br>・`object_storage`: 台形バケット容器の中に収まった丸・三角・四角のオブジェクト<br>・`data_warehouse`: DB シリンダーの手前に3本棒グラフ入り虫眼鏡<br>・`vector_database`: 3次元座標軸（X/Y/Z）空間に浮かぶクラスタドット |
| **Messaging & Streaming** | `message_queue`, `pub_sub`, `event_stream`, `etl_pipeline`, `webhook`, `scheduler` | `queue` / `mq` -> `message_queue`, `stream` -> `event_stream`, `pipeline` -> `etl_pipeline`, `cron` -> `scheduler` | ・`message_queue`: 横向きパイプ筒の中に一列に整列して流れる3つのメッセージブロック<br>・`pub_sub`: 中央のハブ円から右側3つの購読ノードへ放射状に飛ぶ矢印<br>・`event_stream`: 滑らかな3本のS字ウェーブ線を高速に流れるデータドット<br>・`etl_pipeline`: 漏斗（ファネル）合流 → 変換ギア → 整列出力<br>・`scheduler`: 時計盤＋トリガー矢印 |
| **Security & Observability** | `firewall`, `waf`, `identity_auth`, `secret_vault`, `certificate_tls`, `monitoring`, `logging`, `distributed_tracing`, `alert_incident` | `auth` / `iam` -> `identity_auth`, `vault` / `kms` -> `secret_vault`, `tls` -> `certificate_tls`, `metrics` -> `monitoring`, `tracing` -> `distributed_tracing`, `alert` -> `alert_incident` | ・`firewall`: レンガ壁の手前に配置された防御シールド<br>・`identity_auth`: 人物アバター＋鍵/チェックマーク付きシールドバッジ<br>・`secret_vault`: 南京錠（パドロック）＋暗号キー<br>・`monitoring`: モニター枠内のパルス波形（折れ線グラフ）<br>・`logging`: 複数行のログシート＋調査用虫眼鏡<br>・`distributed_tracing`: 段違いに並んだ3本のウォーターフォール・スパンバー |
| **Clients, Users & AI** | `user`, `user_group`, `web_browser`, `mobile_app`, `iot_device`, `llm_model`, `ai_agent` | `users` -> `user_group`, `browser` -> `web_browser`, `mobile` -> `mobile_app`, `llm` -> `llm_model`, `agent` -> `ai_agent` | ・`user` / `user_group`: クリーンな人物アバター（単体／3人重なり）<br>・`web_browser`: 上部3色ドット＋URLバー付きのブラウザウィンドウ枠<br>・`mobile_app`: スマートフォン筐体＋画面内UIカード<br>・`llm_model`: 4芒星スパークルとニューラルネットワーク結合ノード<br>・`ai_agent`: AI スパークルコアの周囲を回る自律ループ矢印とツールギア |

---

## 5. 独立モジュール詳細（50個以上）：`gcp`, `aws`, `azure`

### 5.1. Google Cloud (`drawlib.icons.gcp` / `GcpIcon` — 50+ icons)
- **配色**: Google 4色（`#4285F4`, `#EA4335`, `#FBBC04`, `#34A853`）および GCP Tech Blues（`#3367D6`, `#4285F4`, `#669DF6`, `#AECBFA`）。
- **バリエーション**: `variant: Literal["modern", "legacy"] = "modern"`
- **Tier 1 専用アイコン（約 50 種）**:
  - **Compute**: `compute_engine` (`gce`), `app_engine`, `batch`, `vmware_engine`, `bare_metal_solutions`
  - **Containers & Serverless**: `google_kubernetes_engine` (`gke`), `cloud_run`, `cloud_functions` (`functions`), `anthos`, `cloud_run_jobs`
  - **Storage**: `cloud_storage` (`gcs`), `filestore`, `persistent_disk`, `local_ssd`
  - **Databases**: `cloud_sql`, `cloud_spanner`, `bigtable`, `firestore`, `memorystore`, `alloydb`
  - **Networking**: `virtual_private_cloud` (`vpc`), `cloud_load_balancing`, `cloud_cdn`, `cloud_dns`, `cloud_nat`, `cloud_interconnect`, `cloud_vpn`, `cloud_router`, `cloud_domains`, `service_directory`
  - **Data & Analytics**: `bigquery` (`bq`), `pubsub`, `dataflow`, `dataproc`, `cloud_composer`, `looker`, `dataplex`, `datastream`, `data_catalog`
  - **AI & ML**: `vertex_ai`, `automl`, `document_ai`, `cloud_vision_api`, `speech_to_text`, `text_to_speech`, `cloud_translation_api`, `cloud_natural_language_api`
  - **Security & Ops**: `cloud_armor`, `identity_and_access_management` (`iam`), `secret_manager`, `key_management_service` (`kms`), `cloud_monitoring`, `cloud_logging`, `cloud_trace`, `cloud_build`, `artifact_registry`, `cloud_deploy`, `cloud_api_gateway`, `apigee`, `cloud_scheduler`, `cloud_tasks`, `workflows`
- **Tier 2 カテゴリ共通アイコン（24 種）＆ 既存 `GcpIcon` 全メンバー互換エイリアス**。

### 5.2. Amazon Web Services (`drawlib.icons.aws` / `AwsIcon` — 52 icons)
- **配色**: Compute Orange `#ED7100`, Storage Green `#3F8624`, Database Blue `#3B48CC`, Networking Purple `#8C4FFF`, Security Red `#DD344C`, Analytics Magenta `#E7157B`, AI/ML Teal `#01A88D`。
- **収録アイコン**:
  - **Compute**: `ec2`, `auto_scaling`, `lightsail`, `elastic_beanstalk`, `batch`, `outposts`, `wavelength`
  - **Containers & Serverless**: `ecs`, `eks`, `fargate`, `ecr`, `lambda_function` (`awslambda`), `step_functions`, `app_runner`
  - **Storage**: `s3`, `ebs`, `efs`, `fsx`, `glacier`, `backup`, `storage_gateway`
  - **Databases**: `rds`, `aurora`, `dynamodb`, `elasticache`, `redshift`, `neptune`, `documentdb`, `keyspaces`
  - **Networking**: `vpc`, `elb`, `alb`, `nlb`, `cloudfront`, `route53`, `api_gateway`, `direct_connect`, `transit_gateway`, `nat_gateway`, `vpn`, `global_accelerator`
  - **Analytics & Integration**: `sqs`, `sns`, `eventbridge`, `kinesis`, `athena`, `glue`, `emr`, `opensearch`, `msk`, `quicksight`
  - **AI & ML**: `sagemaker`, `bedrock`, `rekognition`, `comprehend`, `lex`, `polly`
  - **Security & Management**: `iam`, `kms`, `secrets_manager`, `waf`, `shield`, `cognito`, `guardduty`, `inspector`, `cloudwatch`, `cloudtrail`, `config`, `systems_manager`, `cloudformation`, `codepipeline`, `codebuild`

### 5.3. Microsoft Azure (`drawlib.icons.azure` / `AzureIcon` — 50 icons)
- **配色**: Azure Primary Blue `#0078D4`, Deep Blue `#005BA1`, Cyan Highlight `#50E6FF`, Teal `#00B7C3`, Purple `#773ADC`。
- **収録アイコン**:
  - **Compute & Containers**: `virtual_machines` (`vm`), `vm_scale_sets`, `app_service`, `aks`, `container_apps`, `container_instances`, `container_registry`, `functions`, `batch`, `avs_vmware_solution`
  - **Storage**: `storage_accounts`, `blob_storage`, `managed_disks`, `files`, `data_lake_storage`, `netapp_files`, `backup`
  - **Databases**: `sql_database`, `sql_managed_instance`, `cosmos_db`, `postgresql`, `mysql`, `redis_cache`, `synapse_analytics`
  - **Networking**: `virtual_network` (`vnet`), `load_balancer`, `application_gateway`, `front_door`, `cdn`, `dns`, `private_link`, `expressroute`, `vpn_gateway`, `firewall`, `nat_gateway`, `bastion`, `traffic_manager`
  - **Integration & Analytics**: `event_hubs`, `service_bus`, `event_grid`, `logic_apps`, `api_management`, `databricks`, `data_factory`, `fabric`, `stream_analytics`
  - **AI & ML**: `openai`, `ai_studio`, `machine_learning`, `cognitive_services`, `ai_search`, `bot_service`
  - **Security & Management**: `entra_id` (`active_directory`), `key_vault`, `defender`, `sentinel`, `ddos_protection`, `monitor`, `log_analytics`, `application_insights`, `devops`, `arm_templates`

---

## 6. 細分化 `<category>_icons` モジュール詳細（全 14 カテゴリ）

### 6.1. `drawlib.icons.network_icons` (`NetworkIcon` — 約 28 種)
ネットワーク機器（ルーター、スイッチ、無線AP）、CDN、ロードバランサ、リバースプロキシ。
| ベンダープレフィックス | 収録関数名 (`network_icons.<name>`) |
| :--- | :--- |
| **`cisco_*`** | `cisco_logo`, `cisco_router`, `cisco_core_router`, `cisco_edge_router`, `cisco_switch_l2` (`cisco_switch`), `cisco_switch_l3` (`cisco_multilayer_switch`), `cisco_vswitch`, `cisco_wireless_router`, `cisco_access_point`, `cisco_wlc`, `cisco_vpn_gateway`, `cisco_load_balancer`, `cisco_meraki` |
| **`juniper_*` / `arista_*`** | `juniper_logo`, `juniper_router`, `juniper_switch`, `arista_logo`, `arista_switch` |
| **`f5_*` / `nginx_*` / `haproxy_*`** | `f5_logo`, `f5_big_ip`, `nginx_logo`, `haproxy_logo` |
| **`cloudflare_*`** | `cloudflare_logo`, `cloudflare_cdn`, `cloudflare_dns`, `cloudflare_workers`, `cloudflare_r2`, `cloudflare_tunnel` |

### 6.2. `drawlib.icons.security_icons` (`SecurityIcon` — 約 22 種)
次世代ファイアウォール (NGFW)、WAF、EDR、ゼロトラスト、IDaaS（SSO/MFA 認証）、シークレット保護。
| ベンダープレフィックス | 収録関数名 (`security_icons.<name>`) |
| :--- | :--- |
| **`paloalto_*` / `fortinet_*` / `cisco_*`** | `paloalto_logo`, `paloalto_firewall`, `paloalto_prisma`, `fortinet_logo`, `fortinet_fortigate`, `cisco_firewall` (`cisco_asa`), `cisco_ngfw`, `cisco_ise`, `cloudflare_waf`, `cloudflare_zero_trust` |
| **`okta_*` / `auth0_*`** | `okta_logo`, `okta_sso`, `okta_mfa`, `auth0_logo`, `keycloak_logo` |
| **`crowdstrike_*` / `zscaler_*` / `hashicorp_*`** | `crowdstrike_logo`, `crowdstrike_falcon`, `zscaler_logo`, `zscaler_zia`, `zscaler_zpa`, `hashicorp_vault`, `letsencrypt_logo` |

### 6.3. `drawlib.icons.virtualization_icons` (`VirtualizationIcon` — 約 18 種)
オンプレミス仮想化、ハイパーバイザ、HCI、プライベートクラウド基盤。
| ベンダープレフィックス | 収録関数名 (`virtualization_icons.<name>`) |
| :--- | :--- |
| **`vmware_*`** | `vmware_logo`, `vmware_vsphere`, `vmware_esxi`, `vmware_vcenter`, `vmware_nsx`, `vmware_vsan`, `vmware_tanzu`, `vmware_horizon`, `vmware_workstation` |
| **`nutanix_*` / `openstack_*`** | `nutanix_logo`, `nutanix_ahv`, `nutanix_prism`, `openstack_logo`, `openstack_nova`, `openstack_neutron`, `openstack_cinder` |
| **その他ハイパーバイザ** | `linux_kvm`, `proxmox_ve`, `citrix_vdi` |

### 6.4. `drawlib.icons.container_icons` (`ContainerIcon` — 約 28 種)
Kubernetes コンポーネント、Docker コンテナ、CNCF サービスメッシュ・パッケージ管理。
| ベンダープレフィックス | 収録関数名 (`container_icons.<name>`) |
| :--- | :--- |
| **`k8s_*`** | `k8s_logo` (`kubernetes_logo`), `k8s_pod`, `k8s_deployment`, `k8s_replicaset`, `k8s_statefulset`, `k8s_daemonset`, `k8s_job`, `k8s_cronjob`, `k8s_service`, `k8s_ingress`, `k8s_node`, `k8s_ns`, `k8s_pv`, `k8s_pvc`, `k8s_configmap`, `k8s_secret`, `k8s_etcd` |
| **`docker_*`** | `docker_logo`, `docker_container`, `docker_image`, `docker_compose`, `docker_registry` (`docker_hub`), `docker_swarm` |
| **CNCF / Container Ecosystem** | `helm_logo`, `istio_logo`, `envoy_logo`, `containerd_logo`, `podman_logo`, `redhat_openshift` |

### 6.5. `drawlib.icons.hardware_icons` (`HardwareIcon` — 約 18 種)
物理サーバー（Dell / HPE / Cisco UCS）、エンタープライズストレージ（SAN/NAS）、クライアント端末機器。
| ベンダープレフィックス | 収録関数名 (`hardware_icons.<name>`) |
| :--- | :--- |
| **`dell_*` / `hpe_*` / `cisco_*`** | `dell_logo`, `dell_poweredge`, `hpe_logo`, `hpe_proliant`, `cisco_ucs_server` |
| **`hw_*` (汎用データセンター・端末機器)** | `hw_rack_server`, `hw_blade_server`, `hw_san_storage`, `hw_nas_storage`, `hw_tape_backup`, `hw_ups`, `hw_desktop_pc`, `hw_laptop`, `hw_smartphone`, `hw_tablet`, `hw_printer`, `hw_ip_phone`, `cisco_ip_phone` |

### 6.6. `drawlib.icons.os_icons` (`OsIcon` — 約 28 種)
サーバー/デスクトップ/モバイル OS（Linux, Windows, Mac, iOS, Android）および主要 Web ブラウザ。
| ベンダープレフィックス | 収録関数名 (`os_icons.<name>`) |
| :--- | :--- |
| **`linux_*`** | `linux_tux` (`linux_logo`), `linux_ubuntu`, `linux_redhat` (`linux_rhel`), `linux_debian`, `linux_alpine`, `linux_rocky`, `linux_suse`, `linux_arch` |
| **`apple_*`** | `apple_logo`, `apple_macos`, `apple_ios`, `apple_ipados`, `apple_safari` |
| **`microsoft_*`** | `microsoft_logo`, `microsoft_windows`, `microsoft_windows_server`, `microsoft_active_directory`, `microsoft_powershell`, `microsoft_edge`, `microsoft_iis` |
| **`google_*` / ブラウザ** | `google_logo`, `google_chrome`, `google_android`, `google_chromeos`, `mozilla_firefox`, `brave_browser` |

### 6.7. `drawlib.icons.workspace_icons` (`WorkspaceIcon` — 約 36 種)
Microsoft 365 (O365)、Google Workspace、ビジネスチャット、Web会議、ドキュメント、CRM/ITSM SaaS。
| ベンダープレフィックス | 収録関数名 (`workspace_icons.<name>`) |
| :--- | :--- |
| **`microsoft_*` (M365 / Office)** | `microsoft_m365` (`microsoft_office`), `microsoft_teams`, `microsoft_outlook`, `microsoft_word`, `microsoft_excel`, `microsoft_powerpoint`, `microsoft_sharepoint`, `microsoft_onedrive`, `microsoft_onenote`, `microsoft_power_bi`, `microsoft_power_automate`, `microsoft_dynamics365` |
| **`google_*` (Workspace)** | `google_workspace`, `google_gmail`, `google_drive`, `google_docs`, `google_sheets`, `google_slides`, `google_meet`, `google_calendar`, `google_chat`, `google_forms`, `google_admin`, `google_maps`, `google_youtube` |
| **`slack_*` / `zoom_*` / `cisco_*`** | `slack_logo`, `slack_bot`, `slack_webhook`, `zoom_logo`, `cisco_webex` |
| **`atlassian_*` / `notion_*`** | `atlassian_jira`, `atlassian_confluence`, `atlassian_trello`, `atlassian_statuspage`, `notion_logo` |
| **`salesforce_*` / `servicenow_*`** | `salesforce_logo`, `salesforce_mulesoft`, `salesforce_tableau`, `servicenow_logo`, `servicenow_cmdb` |

### 6.8. `drawlib.icons.git_icons` (`GitIcon` — 約 18 種)
Git バージョン管理、GitHub、GitLab、Bitbucket。
| ベンダープレフィックス | 収録関数名 (`git_icons.<name>`) |
| :--- | :--- |
| **`git_*`** | `git_logo`, `git_branch`, `git_commit`, `git_pull_request`, `git_merge`, `git_tag` |
| **`github_*`** | `github_logo`, `github_actions`, `github_copilot`, `github_codespaces`, `github_dependabot`, `github_packages` |
| **`gitlab_*` / `atlassian_*`** | `gitlab_logo`, `gitlab_ci`, `gitlab_runner`, `gitlab_registry`, `atlassian_bitbucket` |

### 6.9. `drawlib.icons.devops_icons` (`DevopsIcon` — 約 18 種)
IaC（Infrastructure as Code）、構成管理、CI/CD デプロイ自動化ツール。
| ベンダープレフィックス | 収録関数名 (`devops_icons.<name>`) |
| :--- | :--- |
| **`hashicorp_*`** | `hashicorp_logo`, `hashicorp_terraform`, `hashicorp_consul`, `hashicorp_packer`, `hashicorp_nomad`, `hashicorp_vagrant` |
| **`ansible_*` / `jenkins_*` / CI・GitOps** | `ansible_logo`, `jenkins_logo`, `argocd_logo`, `fluxcd_logo`, `circleci_logo`, `pulumi_logo`, `spinnaker_logo`, `sonarqube_logo` |

### 6.10. `drawlib.icons.observability_icons` (`ObservabilityIcon` — 約 22 種)
クラウド監視、メトリクス可視化、ログ集約、APM トレーシング、インシデント通知。
| ベンダープレフィックス | 収録関数名 (`observability_icons.<name>`) |
| :--- | :--- |
| **`datadog_*`** | `datadog_logo`, `datadog_agent`, `datadog_apm`, `datadog_logs` |
| **`grafana_*` / `prometheus_*` / `opentelemetry_*`** | `grafana_logo`, `grafana_loki`, `grafana_tempo`, `grafana_mimir`, `prometheus_logo`, `prometheus_alertmanager`, `opentelemetry_logo` |
| **`elastic_*`** | `elastic_logo`, `elastic_elasticsearch`, `elastic_kibana`, `elastic_logstash` |
| **`splunk_*` / `sentry_*` / `pagerduty_*` / `newrelic_*`** | `splunk_logo`, `sentry_logo`, `pagerduty_logo`, `newrelic_logo`, `dynatrace_logo`, `zabbix_logo` |

### 6.11. `drawlib.icons.database_icons` (`DatabaseIcon` — 約 20 種)
リレーショナル DB (RDBMS)、NoSQL、インメモリキャッシュ、クラウド DWH、ベクトル DB。
| ベンダープレフィックス | 収録関数名 (`database_icons.<name>`) |
| :--- | :--- |
| **`oracle_*`** | `oracle_logo`, `oracle_db`, `oracle_exadata`, `oracle_autonomous_db` |
| **RDBMS** | `postgresql_logo`, `mysql_logo`, `mariadb_logo`, `microsoft_sql_server`, `sqlite_logo`, `cockroachdb_logo` |
| **NoSQL / In-Memory / DWH / Vector** | `mongodb_logo`, `redis_logo`, `cassandra_logo`, `clickhouse_logo`, `neo4j_logo`, `snowflake_logo`, `pinecone_logo`, `milvus_logo`, `qdrant_logo` |

### 6.12. `drawlib.icons.data_pipeline_icons` (`DataPipelineIcon` — 約 16 種)
イベントストリーミング、メッセージキュー、分散データ処理、データレイクハウス、ETL/ELT オーケストレーション。
| ベンダープレフィックス | 収録関数名 (`data_pipeline_icons.<name>`) |
| :--- | :--- |
| **Streaming & Messaging** | `apache_kafka`, `confluent_logo`, `rabbitmq_logo`, `apache_pulsar`, `nats_logo` |
| **Big Data & Orchestration** | `databricks_logo`, `apache_spark`, `apache_flink`, `apache_airflow`, `apache_hadoop`, `apache_beam`, `dbt_logo`, `trino_logo`, `presto_logo`, `delta_lake` |

### 6.13. `drawlib.icons.ai_icons` (`AiIcon` — 約 18 種)
生成 AI / LLM プロバイダ、モデルハブ、ローカル LLM、AI エージェント・RAG フレームワーク。
| ベンダープレフィックス | 収録関数名 (`ai_icons.<name>`) |
| :--- | :--- |
| **LLM Providers** | `openai_logo`, `openai_chatgpt`, `anthropic_logo`, `anthropic_claude`, `google_gemini`, `meta_llama`, `mistral_logo`, `cohere_logo` |
| **AI Ecosystem & Frameworks** | `huggingface_logo`, `ollama_logo`, `langchain_logo`, `llamaindex_logo`, `mcp_logo`, `vllm_logo`, `pytorch_logo`, `tensorflow_logo` |

### 6.14. `drawlib.icons.programming_icons` (`ProgrammingIcon` — 約 26 種)
プログラミング言語、ランタイム、主要 Web / API フレームワーク、IDE。
| ベンダープレフィックス | 収録関数名 (`programming_icons.<name>`) |
| :--- | :--- |
| **Languages** | `python_logo`, `go_logo`, `nodejs_logo`, `typescript_logo`, `javascript_logo`, `java_logo`, `kotlin_logo`, `rust_logo`, `cpp_logo`, `csharp_logo`, `php_logo`, `ruby_logo`, `swift_logo`, `dart_logo` |
| **Frameworks & Protocols** | `react_logo`, `nextjs_logo`, `vue_logo`, `angular_logo`, `flutter_logo`, `fastapi_logo`, `django_logo`, `spring_logo`, `dotnet_logo`, `graphql_logo`, `grpc_logo` |
| **IDEs** | `microsoft_vscode`, `jetbrains_intellij` |

---

## 7. 公開 API & `ArchitectureDiagram` 統合イメージ

### 7.1. `drawlib.icons` での呼び出し
```python
from drawlib.icons import (
    ai_icons,
    architecture_icons,
    aws,
    azure,
    container_icons,
    data_pipeline_icons,
    database_icons,
    devops_icons,
    gcp,
    git_icons,
    hardware_icons,
    network_icons,
    observability_icons,
    os_icons,
    phosphor,
    programming_icons,
    security_icons,
    virtualization_icons,
    workspace_icons,
)
from drawlib.styles import Styles

# 1. ベンダー非依存の Drawlib 独自アーキテクチャ概念アイコン
architecture_icons.load_balancer((20, 65), width=9.0, style=Styles.Primary)
architecture_icons.compute((45, 65), width=9.0, style=Styles.Primary)
architecture_icons.database((70, 65), width=9.0, style=Styles.Primary)
architecture_icons.message_queue((95, 65), width=9.0, style=Styles.Primary)

# 2. 50個以上の3大クラウド（gcp は variant="modern" / "legacy" 切り替え対応）
gcp.compute_engine((20, 40), width=9.0, style=Styles.Primary)  # default: variant="modern" (4色)
gcp.compute_engine((45, 40), width=9.0, variant="legacy", style=Styles.Primary)  # GCPブルー六角形
aws.ec2((70, 40), width=9.0, style=Styles.Primary)
azure.virtual_machines((95, 40), width=9.0, style=Styles.Primary)

# 3. 細分化された *_icons モジュール（AI が用途から一発で推測可能）
network_icons.cisco_router((20, 15), width=9.0, style=Styles.Primary)
virtualization_icons.vmware_vsphere((45, 15), width=9.0, style=Styles.Primary)
os_icons.google_chrome((70, 15), width=9.0, style=Styles.Primary)
workspace_icons.microsoft_teams((95, 15), width=9.0, style=Styles.Primary)
observability_icons.datadog_logo((120, 15), width=9.0, style=Styles.Primary)
git_icons.github_actions((145, 15), width=9.0, style=Styles.Primary)
programming_icons.python_logo((170, 15), width=9.0, style=Styles.Primary)
```

### 7.2. `ArchitectureDiagram` での呼び出し
```python
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    ArchitectureIcon,
    GcpIcon,
    NetworkIcon,
    Node,
    NodeGroup,
    ObservabilityIcon,
    OsIcon,
    VirtualizationIcon,
)

# ベンダー非依存の概念ノード (ArchitectureIcon) と特定ベンダーノードを自在に組み合わせ可能
lb = d.add(Node("Load Balancer", width=24, height=18, icon=ArchitectureIcon.LOAD_BALANCER), xy=(8, 20))
api = d.add(Node("API Server", width=24, height=18, icon=ArchitectureIcon.COMPUTE), xy=(42, 20))
db = d.add(Node("Primary DB", width=24, height=18, icon=ArchitectureIcon.DATABASE), xy=(76, 20))
dd = d.add(Node("Datadog APM", width=24, height=18, icon=ObservabilityIcon.DATADOG_LOGO), xy=(110, 20))
```

---

## 8. 段階的実装ロードマップ (Phased Rollout Plan)

| フェーズ | マイルストーン | 主な作業内容と完了基準 |
| :--- | :--- | :--- |
| **Phase 1: 共通幾何学ビルダ基盤 ＆ Drawlib 独自概念アイコン (`architecture_icons`) の構築** | 共通パーツ実装 ＆ `architecture_icons` (約38種) 完成 | 1. `tools/dcli/codegen/icons/_primitives.py`（六角プレート、アイソメキューブ、円筒、チップ、バケット、矢印ツリー等）と `_renderer.py`（100×100 → 512×512 PNG 出力）を実装。<br>2. ベンダー非依存の `drawlib.icons.architecture_icons`（`load_balancer`, `compute`, `database`, `message_queue`, `cache`, `api_gateway`, `ai_agent` 等 約38種）を実装。<br>3. `view_file` によるマルチモーダル視覚レビューを実施し、Drawlib ネイティブアイコンの基礎造形・線幅・余白を確立する。 |
| **Phase 2: GCP アイコンの Drawlib ネイティブ完全移行 (`modern` & `legacy`)** | `icon_gcp` の自前生成化 ＆ 外部アセット廃止 | 1. Phase 1 の幾何学パーツを応用し、GCP の Tier 1 コアアイコン（約 50 種、`modern` 4色 & `legacy` 青六角形）とカテゴリ共通アイコン（24 種）を実装。<br>2. Tier 2 マイナーサービスのエイリアス定義と `manifest.json` / `_generated.py` 生成を統合。<br>3. `./dcli docs build site` で実図面での視認性を検証し、`tools/dcli/codegen/gcp_download.py` / `gcp_normalize.py` を置き換える。 |
| **Phase 3: インフラ・OS・業務系 7 カテゴリの新設** | `network_icons`, `security_icons`, `virtualization_icons`, `container_icons`, `hardware_icons`, `os_icons`, `workspace_icons` | 1. オンプレ・ネットワーク・セキュリティ・仮想化・コンテナ・OS・業務スイートの7モジュールを実装。<br>2. `./dcli codegen` で PNG・バインディング・Enum を生成し、ドキュメントと単体テストを追加。 |
| **Phase 4: 開発・データ・AI系 7 カテゴリ ＆ `aws` / `azure` の新設** | `git_icons`, `devops_icons`, `observability_icons`, `database_icons`, `data_pipeline_icons`, `ai_icons`, `programming_icons` ＋ `aws`, `azure` | 1. 開発・監視・DB・データ基盤・AI・言語の7モジュールおよび 50個以上の独立モジュール `aws`, `azure` を実装。<br>2. `src/drawlib/_rules/` および公式ドキュメントを更新し、`./dcli code-check all` と `./dcli test all` をパスさせる。 |

---

## 9. 品質保証・検証チェックリスト (Verification Criteria)

1. **視覚レビュー基準（Multimodal Review）**:
   - `width=7.5`〜`12.0` units（実図面での標準サイズ）に縮小して配置した際、アイコン内部の線が潰れたり文字と干渉したりしないこと。
   - 50%+ Neutral Baseline のカード（`Styles.Neutral`, `Styles.PrimaryNeutral`, `Styles.SecondaryNeutral`）上に配置した際、十分なコントラストと視認性があること。
   - 一目でどの概念（またはベンダー／製品）か判別できる象徴性を備えていること。
2. **技術・互換性基準**:
   - `style.alpha`、`style.image_tint_color`、`style.image_border_*`、`style.angle` がすべての生成アイコンで正常に機能すること。
   - 既存の全テスト（`./dcli test all`）および全ドキュメントビルド（`./dcli docs build --all`）がエラーなく完了すること。
