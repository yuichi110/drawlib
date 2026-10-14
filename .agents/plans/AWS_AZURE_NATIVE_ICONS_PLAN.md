# AWS & Azure ネイティブアイコン実装計画書
(AWS & AZURE DRAWLIB-NATIVE ARCHITECTURE ICONS IMPLEMENTATION PLAN)

- **作成日**: 2026-10-14
- **親計画書**: [`.agents/plans/DRAWLIB_NATIVE_ICONS_PLAN.md`](./DRAWLIB_NATIVE_ICONS_PLAN.md)
- **対象モジュール**:
  - `tools/original_assets/aws/`, `tools/original_assets/azure/` (公式リファレンスアセット：作業完了後に削除)
  - `tools/icons_src/aws/*.py` (AWS 全 **329** スクリプト：サービス **303** 種 ＋ カテゴリ **26** 種)
  - `tools/icons_src/azure/*.py` (Azure 全 **250** スクリプト：主要クラウドサービス **250** 種)
  - `tools/icons_src/utils.py` (AWS 公式カテゴリカラー & Azure 公式マルチトーンパレット・共通ヘルパー追加)
  - `tools/release_assets/v0.3/icons/aws/`, `tools/release_assets/v0.3/icons/azure/` (`512×512` 正規化透過 PNG ＋ `manifest.json`)
  - `tools/dcli/codegen/` (`./dcli codegen icon-aws`, `./dcli codegen icon-azure`, `icons_build.py`)
  - `src/drawlib/_icons/png_icons/aws/`, `src/drawlib/_icons/png_icons/azure/` (`PngIconProvider` バインディング)
  - `src/drawlib/icons.py`, `src/drawlib/_diagrams/architecture/_icons.py`, `src/drawlib/diagrams/architecture.py` (`aws`, `azure`, `AwsIcon`, `AzureIcon`)

---

## 1. スコープと命名規則 (Scope & Naming Rules)

### 1.1. 収録アイコン数（GCP と同規模のフルラインナップ）

| プロバイダ | ソースディレクトリ | プライマリアイコン数 | 短縮・別名エイリアス数 | 合計関数 / Enum 数 | 内訳 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AWS (`drawlib.icons.aws`)** | `tools/icons_src/aws/` | **329 種** | **35 種** | **364 関数** | ・AWS Architecture Service Icons 全 24 カテゴリ・ユニーク **303 種** 全網羅<br>・AWS Category Icons (`category_*`) 全 **26 種** 全網羅 |
| **Azure (`drawlib.icons.azure`)** | `tools/icons_src/azure/` | **250 種** | **35 種** | **285 関数** | ・Azure Public Service Icons 全主要カテゴリから Classic/Deprecated・ポータル内部サブブレードを除いた **250 種**（GCP の 250 種と同規模） |

### 1.2. 関数名・ファイル名の命名規則
1. **冗長なベンダープレフィックスの除去**:
   - **AWS**: 公式ファイル名 `Arch_Amazon-<Name>_64.svg` / `Arch_AWS-<Name>_64.svg` / `Arch_<Name>_64.svg` から先頭の `Arch_`, `Amazon-`, `AWS-` を除去し、`snake_case` に正規化する。
     - 例: `Arch_Amazon-EC2_64` $\rightarrow$ `ec2_default.py` (`aws.ec2()`)
     - 例: `Arch_Amazon-RDS_64` $\rightarrow$ `rds_default.py` (`aws.rds()`)
     - 例: `Arch_Amazon-Aurora_64` $\rightarrow$ `aurora_default.py` (`aws.aurora()`)
     - 例: `Arch_Amazon-DynamoDB_64` $\rightarrow$ `dynamodb_default.py` (`aws.dynamodb()`)
     - 例: `Arch_Amazon-CloudFront_64` $\rightarrow$ `cloudfront_default.py` (`aws.cloudfront()`)
     - 例: `Arch_Amazon-Route-53_64` $\rightarrow$ `route_53_default.py` (`aws.route_53()`)
     - 例: `Arch_Amazon-API-Gateway_64` $\rightarrow$ `api_gateway_default.py` (`aws.api_gateway()`)
     - 例: `Arch_Amazon-Bedrock_64` $\rightarrow$ `bedrock_default.py` (`aws.bedrock()`)
     - **例外（Python 予約語・数字始まり）**: `Arch_AWS-Lambda_64` は Python 予約語 `lambda` と衝突するため **`aws_lambda_default.py` (`aws.aws_lambda()`)** とし、エイリアス `lambda_function` も提供する。
     - **カテゴリアイコン**: `Arch-Category_<Name>_64` $\rightarrow$ `category_<name>_default.py` (`aws.category_compute()`, `aws.category_storage()` 等、GCP の `category_*` と完全統一)。
   - **Azure**: 公式ファイル名 `<ID>-icon-service-<Name>.svg` から `<ID>-icon-service-` および先頭の `Azure-` / `Microsoft-` を除去し、`snake_case` に正規化する。
     - 例: `10021-icon-service-Virtual-Machine` $\rightarrow$ `virtual_machine_default.py` (`azure.virtual_machine()`)
     - 例: `10023-icon-service-Kubernetes-Services` $\rightarrow$ `kubernetes_services_default.py` (`azure.kubernetes_services()`)
     - 例: `10029-icon-service-Function-Apps` $\rightarrow$ `function_apps_default.py` (`azure.function_apps()`)
     - 例: `10035-icon-service-App-Services` $\rightarrow$ `app_services_default.py` (`azure.app_services()`)
     - 例: `10086-icon-service-Storage-Accounts` $\rightarrow$ `storage_accounts_default.py` (`azure.storage_accounts()`)
     - 例: `10121-icon-service-Azure-Cosmos-DB` $\rightarrow$ `cosmos_db_default.py` (`azure.cosmos_db()`)
     - 例: `10130-icon-service-SQL-Database` $\rightarrow$ `sql_database_default.py` (`azure.sql_database()`)
     - 例: `03438-icon-service-Azure-OpenAI` $\rightarrow$ `openai_default.py` (`azure.openai()`)
2. **直感的な略称エイリアス (`PROVIDER_ALIASES`)**:
   - **AWS**:
     - `s3` $\rightarrow$ `simple_storage_service`, `s3_glacier` $\rightarrow$ `simple_storage_service_glacier`
     - `sqs` $\rightarrow$ `simple_queue_service`, `sns` $\rightarrow$ `simple_notification_service`, `ses` $\rightarrow$ `simple_email_service`
     - `vpc` $\rightarrow$ `virtual_private_cloud`, `elb` / `alb` / `nlb` $\rightarrow$ `elastic_load_balancing`
     - `ecs` $\rightarrow$ `elastic_container_service`, `eks` $\rightarrow$ `elastic_kubernetes_service`, `ecr` $\rightarrow$ `elastic_container_registry`
     - `ebs` $\rightarrow$ `elastic_block_store`, `efs` $\rightarrow$ `elastic_file_system`
     - `iam` $\rightarrow$ `identity_and_access_management`, `kms` $\rightarrow$ `key_management_service`, `acm` $\rightarrow$ `certificate_manager`
     - `lambda_function` $\rightarrow$ `aws_lambda`, `sagemaker` $\rightarrow$ `sagemaker_ai`, `step_functions_workflow` $\rightarrow$ `step_functions`
   - **Azure**:
     - `vm` / `virtual_machines` $\rightarrow$ `virtual_machine`, `vmss` $\rightarrow$ `vm_scale_sets`
     - `aks` $\rightarrow$ `kubernetes_services`, `aci` $\rightarrow$ `container_instances`, `acr` $\rightarrow$ `container_registries`, `aca` / `container_apps` $\rightarrow$ `worker_container_app`
     - `functions` $\rightarrow$ `function_apps`, `blob_storage` $\rightarrow$ `storage_container`, `azure_files` $\rightarrow$ `storage_azure_files`
     - `vnet` $\rightarrow$ `virtual_networks`, `lb` $\rightarrow$ `load_balancers`, `appgw` / `application_gateway` $\rightarrow$ `application_gateways`, `front_door` / `cdn` $\rightarrow$ `front_door_and_cdn_profiles`, `nat_gateway` $\rightarrow$ `nat`, `bastion` $\rightarrow$ `bastions`, `expressroute` $\rightarrow$ `expressroute_circuits`
     - `apim` / `api_management` $\rightarrow$ `api_management_services`, `waf` $\rightarrow$ `web_application_firewall_policies_waf`
     - `key_vault` / `kv` $\rightarrow$ `key_vaults`, `aad` / `active_directory` $\rightarrow$ `entra_id`, `redis` $\rightarrow$ `cache_redis`
     - `adf` / `data_factory` $\rightarrow$ `data_factories`, `synapse` $\rightarrow$ `synapse_analytics`, `event_grid` $\rightarrow$ `event_grid_topics`, `ai_search` $\rightarrow$ `cognitive_search`
     - `app_insights` $\rightarrow$ `application_insights`, `log_analytics` $\rightarrow$ `log_analytics_workspaces`, `avd` $\rightarrow$ `virtual_desktop`

---

## 2. デザイン規格とカラーパレット (`tools/icons_src/utils.py`)

### 2.1. AWS 公式カラーパレット（全 8 色 ＋ 白線画）
- **Service Icons (303種)**: `100×100` 論理キャンバスのセーフエリア `[8.0, 92.0]`（`84×84` プレート）にカテゴリ背景色の正方形タイルを描画し、内部に `WHITE` (`#FFFFFF`) でベクター図形を描画する。
- **Category Icons (26種)**: 外枠グレー（`#7D8998`、`[8.0, 92.0]`）＋白フレーム（`[10.5, 89.5]`）＋カテゴリ色コア（`[15.5, 84.5]`）＋内部 `WHITE` 図形。
- **カラー定数**:
  - `AWS_ORANGE = "#ED7100"` (Compute, Containers, Media Services, Blockchain, Quantum, Serverless)
  - `AWS_TEAL = "#01A88D"` (Artificial Intelligence, Migration & Modernization, End-User Computing)
  - `AWS_RED = "#DD344C"` (Security, Identity & Compliance, Front-End Web & Mobile, Business Applications)
  - `AWS_PURPLE = "#8C4FFF"` (Networking & Content Delivery, Analytics, Games)
  - `AWS_PINK = "#E7157B"` (Application Integration, Management & Governance)
  - `AWS_MAGENTA = "#C925D1"` (Databases, Developer Tools, Customer Enablement, Satellite)
  - `AWS_GREEN = "#7AA116"` (Storage, Internet of Things, Cloud Financial Management)
  - `AWS_SQUID_INK = "#232F3E"` (General / Marketplace)
  - `AWS_GRAY_BORDER = "#7D8998"` (Category Icon outer frame)

### 2.2. Azure 公式カラーパレット（透過背景 ＋ マルチトーンベクター）
- **Service Icons (250種)**: `100×100` 透過キャンバスのセーフエリア `[8.0, 92.0]` 内に、公式 SVG の配色と造形（グラデーションは対応する代表フラット色または段階ポリゴン）を忠実に再現する。
- **カラー定数**:
  - `AZURE_BLUE = "#0078D4"`, `AZURE_DARK_BLUE = "#005BA1"`, `AZURE_LIGHT_BLUE = "#5EA0EF"`, `AZURE_PALE_BLUE = "#83B9F9"`
  - `AZURE_CYAN = "#50E6FF"`, `AZURE_LIGHT_CYAN = "#9CEBFF"`, `AZURE_PALE_CYAN = "#C3F1FF"`, `AZURE_TEAL = "#32BEDD"`, `AZURE_DARK_TEAL = "#198AB3"`
  - `AZURE_PURPLE = "#773ADC"`, `AZURE_LIGHT_PURPLE = "#A67AF4"`, `AZURE_DARK_PURPLE = "#341A6E"`
  - `AZURE_GREEN = "#76BC2D"`, `AZURE_LIGHT_GREEN = "#86D633"`, `AZURE_DARK_GREEN = "#5E9624"`
  - `AZURE_ORANGE = "#F78D1E"`, `AZURE_YELLOW = "#FFB900"`, `AZURE_RED = "#E62325"`
  - `AZURE_GRAY = "#949494"`, `AZURE_DARK_GRAY = "#707070"`, `AZURE_LIGHT_GRAY = "#CCCCCC"`, `AZURE_PALE_GRAY = "#F2F2F2"`

---

## 3. 実装フェーズとマルチエージェント並列実行手順

1. **Step 1: 共通基盤 & バッチマニフェスト準備**
   - `tools/icons_src/utils.py` に AWS / Azure カラー定数・プレート描画ヘルパーを追加。
   - `.gitignore` に `tools/original_assets/aws/` と `tools/original_assets/azure/` を追加。
   - AWS 全 329 種（8 バッチ）および Azure 全 250 種（6 バッチ）のマニフェストと `512×512` リファレンス PNG を `.drawlib/scratch/ref_aws/`, `.drawlib/scratch/ref_azure/` に生成。
2. **Step 2: AWS 全 329 アイコンの作成 & 視覚検証（並列サブエージェント）**
   - `tools/icons_src/aws/*_default.py` 全 329 スクリプトを作成し、公式リファレンス PNG と比較検証。
3. **Step 3: Azure 全 250 アイコンの作成 & 視覚検証（並列サブエージェント）**
   - `tools/icons_src/azure/*_default.py` 全 250 スクリプトを作成し、公式リファレンス PNG と比較検証。
4. **Step 4: ビルド・コード生成・リリースアセット・テスト統合**
   - `tools/icons_src/build.sh` で `tools/release_assets/v0.3/icons/{aws,azure}/` に `512×512` 正規化 PNG と `manifest.json` を出力。
   - `./dcli codegen icon-aws` / `./dcli codegen icon-azure` で `drawlib.icons.aws`, `drawlib.icons.azure`, `AwsIcon`, `AzureIcon` を生成。
   - `./dcli code-check all` および単体テストを実行して品質を確認。
