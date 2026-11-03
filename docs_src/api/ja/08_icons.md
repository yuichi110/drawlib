# drawlib.icons（34 アイコンスイートとフォントアイコン）

遅延ロードされる全 34 種類の標準アイコンスイート（単色ベクター `phosphor`、`gcp` / `aws` / `azure` ＋ 15 ドメインの公式マルチカラー PNG スイート、および 15 種類のフラット 2D パステル版 `original_*` スイート）とカスタムフォントアイコン描画関数 `font_icon()` を提供します。`from drawlib.icons import ai, aws, azure, font_icon, gcp, phosphor` でインポートし、中心基準 `(cx, cy)`・正方形 `1:1` サイズ・必須キーワード引数 `style` で描画します。

```drawlib align=center code=fold file=08_icons_hero.png caption="3 階層・全 34 スイートの標準アイコン体系 — ベクターグリフ・公式クラウド／ベンダーロゴ・2D パステルアイコン"
from drawlib.canvas import save, setup
from drawlib.icons import (
    ai,
    aws,
    cnative,
    gcp,
    original_ai,
    original_data,
    original_devops,
    original_security,
    phosphor,
)
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58)

text(
    (60.0, 52.5),
    "34 Standardized Icon Suites Across 3 Visual Tiers",
    style=Styles.DarkBold.patch(text_size=12.2),
)

# Tier 1: Vector Font Glyphs (phosphor / font_icon)
rectangle((22.5, 25.5), width=35, height=42, style=Styles.Neutral.patch(shape_r=2.0))
rectangle(
    (22.5, 42.0),
    width=31,
    height=6.2,
    style=Styles.PrimaryFlat.patch(shape_r=1.5),
    text="1. Vector (phosphor)",
    text_style=Styles.WhiteBold.patch(text_size=10.2),
)
phosphor.cpu((14.2, 32.2), width=6.0, style=Styles.PrimaryBold)
text((14.2, 26.2), "Bold", style=Styles.Dark.patch(text_size=10.0))
phosphor.shield_check((30.8, 32.2), width=6.0, style=Styles.Primary.patch(icon_style="fill"))
text((30.8, 26.2), "Fill", style=Styles.Dark.patch(text_size=10.0))
phosphor.database((14.2, 16.8), width=6.0, style=Styles.Secondary)
text((14.2, 10.8), "Regular", style=Styles.Dark.patch(text_size=10.0))
phosphor.git_branch((30.8, 16.8), width=6.0, style=Styles.DarkThin)
text((30.8, 10.8), "Thin", style=Styles.Dark.patch(text_size=10.0))

# Tier 2: Official Cloud & Vendor PNG Suites
rectangle((60.0, 25.5), width=35, height=42, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
text((60.0, 42.0), "2. Cloud & Vendor PNG", style=Styles.DarkBold.patch(text_size=10.2))
gcp.cloud_run((51.7, 32.2), width=6.6, style=Styles.Neutral)
text((51.7, 26.2), "gcp", style=Styles.Dark.patch(text_size=10.0))
aws.aws_lambda((68.3, 32.2), width=6.6, style=Styles.Neutral)
text((68.3, 26.2), "aws", style=Styles.Dark.patch(text_size=10.0))
ai.openai((51.7, 16.8), width=6.6, style=Styles.Neutral)
text((51.7, 10.8), "ai", style=Styles.Dark.patch(text_size=10.0))
cnative.kubernetes((68.3, 16.8), width=6.6, style=Styles.Neutral)
text((68.3, 10.8), "cnative", style=Styles.Dark.patch(text_size=10.0))

# Tier 3: Original 2D Pastel Twin & Concept PNG Suites
rectangle((97.5, 25.5), width=35, height=42, style=Styles.SecondaryNeutral.patch(shape_r=2.0))
text((97.5, 42.0), "3. Pastel (original_*)", style=Styles.DarkBold.patch(text_size=10.2))
original_ai.ai_agent((89.2, 32.2), width=6.6, style=Styles.Neutral)
text((89.2, 26.2), "ai_agent", style=Styles.Dark.patch(text_size=10.0))
original_data.data_lakehouse((105.8, 32.2), width=6.6, style=Styles.Neutral)
text((105.8, 26.2), "lakehouse", style=Styles.Dark.patch(text_size=10.0))
original_devops.cicd_pipeline((89.2, 16.8), width=6.6, style=Styles.Neutral)
text((89.2, 10.8), "pipeline", style=Styles.Dark.patch(text_size=10.0))
original_security.ddos_protection((105.8, 16.8), width=6.6, style=Styles.Neutral)
text((105.8, 10.8), "security", style=Styles.Dark.patch(text_size=10.0))

save()
```

---

## `type` ai

AI・LLM・機械学習エコシステムの公式マルチカラー `512×512` RGBA PNG アイコンスイート（`drawlib.icons.ai`、全 `60` 関数）です。公式ブランド色をそのまま保持して描画します（`style.icon_color` は非適用、`angle`・`alpha`・`image_tint_color`・`image_border_*` が有効）。

```python
from drawlib.icons import ai
from drawlib.styles import Styles

# 共通シグネチャ: ai.<icon_name>(xy, width, *, style, variant="default") -> None
ai.openai((30, 25), width=8.0, style=Styles.Neutral)
ai.claude((50, 25), width=8.0, style=Styles.Neutral.patch(angle=15))
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `ai.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **引数** | `xy`: 中心座標 `(cx, cy)`、`width`: 正方形 `1:1` の横幅、`style`: 必須 [`Style`](05_styles_and_types.md)（`angle`, `alpha`, `image_tint_color`, `image_border_*`）、`variant`: `"default"`。 |
| **収録数・配色特性** | 全 `60` 個 · マルチカラー RGBA PNG（単色ティント不可・公式色を保持。2D パステル版は `original_ai`）。 |
| **代表的なアイコン関数** | `openai`, `claude`, `gemini`, `pytorch`, `huggingface`, `autogen`, `crewai`, `arize_phoenix` |
| **連携 Enum・キャッシュ** | `AiIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_ai` |

---

## `type` aws

Amazon Web Services 公式サービス `512×512` RGBA PNG アイコンスイート（`drawlib.icons.aws`、全 `329` 関数）です。コンピューティング・サーバーレス・ストレージ・DB・ネットワーク等の主要 AWS サービスを網羅します。

```python
from drawlib.icons import aws
from drawlib.styles import Styles

aws.aws_lambda((30, 25), width=9.0, style=Styles.Neutral)
aws.simple_storage_service((55, 25), width=9.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `aws.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **引数** | `xy`: 中心座標 `(cx, cy)`、`width`: `1:1` 幅、`style`: 必須 `Style`、`variant`: `"default"`。 |
| **収録数・配色特性** | 全 `329` 個 · 公式マルチカラー AWS RGBA PNG（単色ティント不可）。 |
| **代表的なアイコン関数** | `aws_lambda`, `simple_storage_service`, `ec2`, `rds`, `dynamodb`, `api_gateway`, `app_runner` |
| **連携 Enum・キャッシュ** | `AwsIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_aws` |

---

## `type` azure

Microsoft Azure 公式アーキテクチャ `512×512` RGBA PNG アイコンスイート（`drawlib.icons.azure`、全 `250` 関数）です。

```python
from drawlib.icons import azure
from drawlib.styles import Styles

azure.function_apps((30, 25), width=9.0, style=Styles.Neutral)
azure.cosmos_db((55, 25), width=9.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `azure.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **引数** | `xy`: 中心座標 `(cx, cy)`、`width`: `1:1` 幅、`style`: 必須 `Style`、`variant`: `"default"`。 |
| **収録数・配色特性** | 全 `250` 個 · 公式マルチカラー Azure RGBA PNG（単色ティント不可）。 |
| **代表的なアイコン関数** | `function_apps`, `kubernetes_services`, `sql_database`, `cosmos_db`, `storage_accounts`, `ai_foundry` |
| **連携 Enum・キャッシュ** | `AzureIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_azure` |

---

## `type` business

決済・FinTech・CRM・EC・業務 SaaS プラットフォームの公式マルチカラー `512×512` RGBA PNG アイコンスイート（`drawlib.icons.business`、全 `48` 関数）です。

```python
from drawlib.icons import business
from drawlib.styles import Styles

business.stripe((30, 25), width=8.0, style=Styles.Neutral)
business.salesforce((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `business.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `48` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_business`）。 |
| **代表的なアイコン関数** | `stripe`, `shopify`, `salesforce`, `hubspot`, `zendesk`, `adyen`, `algolia` |
| **連携 Enum・キャッシュ** | `BusinessIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_business` |

---

## `type` client

クライアント OS・Web ブラウザ・モバイル端末・ハードウェアメーカーの公式マルチカラー `512×512` RGBA PNG アイコンスイート（`drawlib.icons.client`、全 `60` 関数）です。

```python
from drawlib.icons import client
from drawlib.styles import Styles

client.apple((30, 25), width=8.0, style=Styles.Neutral)
client.chrome((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `client.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `60` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_client`）。 |
| **代表的なアイコン関数** | `apple`, `android`, `windows`, `chrome`, `firefox`, `app_store`, `arc` |
| **連携 Enum・キャッシュ** | `ClientIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_client` |

---

## `type` cloud

主要パブリッククラウド事業者・CDN・エッジ PaaS の公式ブランドロゴ `512×512` RGBA PNG アイコンスイート（`drawlib.icons.cloud`、全 `45` 関数）です。

```python
from drawlib.icons import cloud
from drawlib.styles import Styles

cloud.cloudflare((30, 25), width=8.0, style=Styles.Neutral)
cloud.vercel((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `cloud.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `45` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_cloud`）。 |
| **代表的なアイコン関数** | `aws`, `google_cloud`, `azure`, `cloudflare`, `vercel`, `akamai`, `alibaba_cloud` |
| **連携 Enum・キャッシュ** | `CloudIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_cloud` |

---

## `type` cnative

Kubernetes リソース（`k8s_*`）・CNCF プロジェクト・サービスメッシュ・クラウドネイティブ基盤の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.cnative`、全 `73` 関数）です。

```python
from drawlib.icons import cnative
from drawlib.styles import Styles

cnative.kubernetes((30, 25), width=8.5, style=Styles.Neutral)
cnative.k8s_pod((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `cnative.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `73` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_cnative`）。 |
| **代表的なアイコン関数** | `kubernetes`, `k8s_pod`, `docker`, `helm`, `prometheus`, `argo`, `cilium`, `backstage` |
| **連携 Enum・キャッシュ** | `CnativeIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_cnative` |

---

## `type` code

プログラミング言語・Web フレームワーク・ランタイム・IDE の公式マルチカラー `512×512` RGBA PNG アイコンスイート（`drawlib.icons.code`、全 `97` 関数）です。

```python
from drawlib.icons import code
from drawlib.styles import Styles

code.python((30, 25), width=8.0, style=Styles.Neutral)
code.typescript((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `code.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `97` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_code`）。 |
| **代表的なアイコン関数** | `python`, `typescript`, `rust`, `go`, `react`, `angular`, `astro`, `axum` |
| **連携 Enum・キャッシュ** | `CodeIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_code` |

---

## `type` data

リレーショナル／NoSQL データベース・メッセージブローカー・DWH・ETL 基盤の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.data`、全 `70` 関数）です。

```python
from drawlib.icons import data
from drawlib.styles import Styles

data.postgresql((30, 25), width=8.5, style=Styles.Neutral)
data.kafka((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `data.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `70` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_data`）。 |
| **代表的なアイコン関数** | `postgresql`, `mysql`, `redis`, `mongodb`, `kafka`, `airflow`, `clickhouse`, `chromadb` |
| **連携 Enum・キャッシュ** | `DataIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_data` |

---

## `type` devops

CI/CD パイプライン・IaC・ビルドツール・可観測性（Observability）製品の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.devops`、全 `58` 関数）です。

```python
from drawlib.icons import devops
from drawlib.styles import Styles

devops.github_actions((30, 25), width=8.5, style=Styles.Neutral)
devops.terraform((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `devops.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `58` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_devops`）。 |
| **代表的なアイコン関数** | `github_actions`, `gitlab`, `terraform`, `ansible`, `jenkins`, `bazel`, `circleci` |
| **連携 Enum・キャッシュ** | `DevopsIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_devops` |

---

## `type` facility

データセンター・通信キャリア・電源／空調設備・物理ファシリティ企業の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.facility`、全 `49` 関数）です。

```python
from drawlib.icons import facility
from drawlib.styles import Styles

facility.equinix((30, 25), width=8.5, style=Styles.Neutral)
facility.ntt((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `facility.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `49` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_facility`）。 |
| **代表的なアイコン関数** | `equinix`, `ntt`, `at_tokyo`, `apc`, `schneider_electric`, `att`, `colt` |
| **連携 Enum・キャッシュ** | `FacilityIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_facility` |

---

## `def` font_icon(xy, width, code, file, *, style)

任意の外部アイコンフォントファイル（`.ttf` / `.otf`）から指定した Unicode コードポイントのベクターグリフを描画します（`drawlib.icons.font_icon`）。PNG スイートとは異なり、`style.icon_color` によって任意の単色へ自在にティント描画されます。

```python
from drawlib.icons import font_icon
from drawlib.styles import Colors, Styles

icon_style = Styles.Primary.patch(icon_color=Colors.Primary, angle=0)
font_icon((50, 25), width=8.0, code="\ue900", file="_assets/fonts/custom_icons.ttf", style=icon_style)
```

| 引数 | 型 | デフォルト | 説明 |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *必須* | アイコンの中心座標 `(cx, cy)`（`style.halign` / `style.valign` で変更可）。 |
| `width` | `float` | *必須* | アイコンの横幅（キャンバス座標単位、`> 0.0`）。 |
| `code` | `str` | *必須* | 描画するアイコンの Unicode 文字またはコードポイント文字列（例: `"\ue900"`）。 |
| `file` | `str` | *必須* | アイコンフォントファイル（`.ttf` / `.otf`）へのパス。 |
| `style` | `Style` | *必須（キーワード専用）* | `icon_color`・`angle`・`alpha`・`halign`・`valign` を制御する [`Style`](05_styles_and_types.md)。 |
| **戻り値** | `None` | — | アクティブなキャンバスへベクターアイコンを描画します。 |

---

## `type` gcp

Google Cloud 公式アーキテクチャ `512×512` RGBA PNG アイコンスイート（`drawlib.icons.gcp`、全 `250` 関数）です。主要サービスでは標準アイコン（`"default"`）に加えて最新スタイル（`variant="modern"`）を選択できます。

```python
from drawlib.icons import gcp
from drawlib.styles import Styles

gcp.cloud_run((30, 25), width=9.0, style=Styles.Neutral)
gcp.cloud_run((55, 25), width=9.0, style=Styles.Neutral, variant="modern")
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `gcp.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default", "modern"] = "default") -> None` |
| **引数** | `xy`: 中心座標 `(cx, cy)`、`width`: `1:1` 幅、`style`: 必須 `Style`、`variant`: `"default"` または対応サービスの `"modern"`。 |
| **収録数・配色特性** | 全 `250` 個 · 公式マルチカラー Google Cloud RGBA PNG（単色ティント不可）。 |
| **代表的なアイコン関数** | `cloud_run`, `compute_engine`, `google_kubernetes_engine`, `bigquery`, `cloud_sql`, `ai_hypercomputer` |
| **連携 Enum・キャッシュ** | `GcpIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_gcp` |

---

## `type` itservice

グローバル IT コンサルティング・SIer・マネージドサービス企業の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.itservice`、全 `44` 関数）です。

```python
from drawlib.icons import itservice
from drawlib.styles import Styles

itservice.accenture((30, 25), width=8.5, style=Styles.Neutral)
itservice.ntt_data((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `itservice.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `44` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_itservice`）。 |
| **代表的なアイコン関数** | `accenture`, `deloitte`, `ibm`, `ntt_data`, `capgemini`, `bcg`, `bain` |
| **連携 Enum・キャッシュ** | `ItserviceIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_itservice` |

---

## `type` network

ネットワーク機器・リバースプロキシ・DNS・VPN・Cisco トポロジ記号（`cisco_*`）の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.network`、全 `70` 関数）です。Cisco アイコンでは `variant`（`"default"` / `"classic"` / `"modern"`）を切り替え可能です。

```python
from drawlib.icons import network
from drawlib.styles import Styles

network.nginx((30, 25), width=8.5, style=Styles.Neutral)
network.tailscale((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `network.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default", "classic", "modern"] = "default") -> None` |
| **収録数・配色特性** | 全 `70` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_network`）。 |
| **代表的なアイコン関数** | `nginx`, `cloudflare`, `traefik`, `haproxy`, `tailscale`, `apisix`, `arista`, `caddy` |
| **連携 Enum・キャッシュ** | `NetworkIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_network` |

---

## `type` original_ai

フラット 2D パステル調の AI・機械学習 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_ai`、全 `80` 関数）です。`ai.*` 全ブランドの 2D パステルツインに加え、ベンダー中立の AI アーキテクチャ概念アイコン `20` 種を収録します。

```python
from drawlib.icons import original_ai
from drawlib.styles import Styles

original_ai.openai((30, 25), width=8.5, style=Styles.Neutral)
original_ai.ai_agent((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_ai.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `80` 個 · フラット 2D パステルマルチカラー RGBA PNG（`icon_color` 非適用、`image_tint_color` / `image_border_*` / `angle` / `alpha` 対応）。 |
| **代表的なアイコン関数** | ツイン: `openai`, `claude`, `gemini`, `pytorch` · 概念: `ai_agent`, `agent_memory`, `dataset`, `embedding_vector` |
| **連携 Enum・キャッシュ** | `OriginalAiIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_ai` |

---

## `type` original_business

フラット 2D パステル調のビジネス・決済・業務フロー `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_business`、全 `76` 関数: ブランドツイン `48` 種＋汎用業務概念 `28` 種）です。

```python
from drawlib.icons import original_business
from drawlib.styles import Styles

original_business.stripe((30, 25), width=8.5, style=Styles.Neutral)
original_business.approval_workflow((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_business.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `76` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `stripe`, `shopify`, `salesforce` · 概念: `accounting_ledger`, `approval_workflow`, `bank_transfer`, `billing_invoice` |
| **連携 Enum・キャッシュ** | `OriginalBusinessIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_business` |

---

## `type` original_client

フラット 2D パステル調のクライアント端末・ブラウザ・IoT デバイス `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_client`、全 `92` 関数: ブランドツイン `60` 種＋汎用端末概念 `32` 種）です。

```python
from drawlib.icons import original_client
from drawlib.styles import Styles

original_client.desktop_pc((30, 25), width=8.5, style=Styles.Neutral)
original_client.connected_car((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_client.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `92` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `apple`, `android`, `chrome` · 概念: `desktop_pc`, `barcode_scanner`, `connected_car`, `drone` |
| **連携 Enum・キャッシュ** | `OriginalClientIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_client` |

---

## `type` original_cloud

フラット 2D パステル調のクラウド事業者およびベンダー中立クラウドコンポーネント `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_cloud`、全 `147` 関数: 事業者ツイン `45` 種＋汎用クラウド機能 `102` 種）です。

```python
from drawlib.icons import original_cloud
from drawlib.styles import Styles

original_cloud.api_gateway((30, 25), width=8.5, style=Styles.Neutral)
original_cloud.analytics_engine((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_cloud.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `147` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `aws`, `google_cloud`, `cloudflare` · 概念: `api_gateway`, `app_service`, `analytics_engine`, `ai_agent` |
| **連携 Enum・キャッシュ** | `OriginalCloudIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_cloud` |

---

## `type` original_cnative

フラット 2D パステル調の Kubernetes・CNCF クラウドネイティブ `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_cnative`、全 `73` 関数）です。

```python
from drawlib.icons import original_cnative
from drawlib.styles import Styles

original_cnative.kubernetes((30, 25), width=8.5, style=Styles.Neutral)
original_cnative.prometheus((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_cnative.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `73` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | `kubernetes`, `k8s_pod`, `docker`, `helm`, `prometheus`, `argo`, `cilium` |
| **連携 Enum・キャッシュ** | `OriginalCnativeIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_cnative` |

---

## `type` original_code

フラット 2D パステル調のプログラミング言語・フレームワーク・実行成果物 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_code`、全 `121` 関数: ブランドツイン `97` 種＋ソフトウェア概念 `24` 種）です。

```python
from drawlib.icons import original_code
from drawlib.styles import Styles

original_code.python((30, 25), width=8.5, style=Styles.Neutral)
original_code.background_worker((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_code.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `121` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `python`, `typescript`, `rust`, `go` · 概念: `background_worker`, `binary_executable`, `cli_tool`, `compiler_build` |
| **連携 Enum・キャッシュ** | `OriginalCodeIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_code` |

---

## `type` original_data

フラット 2D パステル調のデータベース・レイクハウス・データ基盤 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_data`、全 `86` 関数: ブランドツイン `70` 種＋データ基盤概念 `16` 種）です。

```python
from drawlib.icons import original_data
from drawlib.styles import Styles

original_data.data_lakehouse((30, 25), width=8.5, style=Styles.Neutral)
original_data.cdc_stream((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_data.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `86` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `postgresql`, `redis`, `kafka` · 概念: `data_lakehouse`, `cdc_stream`, `columnar_db`, `data_catalog` |
| **連携 Enum・キャッシュ** | `OriginalDataIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_data` |

---

## `type` original_devops

フラット 2D パステル調の CI/CD・IaC・SRE 運用 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_devops`、全 `78` 関数: ブランドツイン `58` 種＋パイプライン／監視概念 `20` 種）です。

```python
from drawlib.icons import original_devops
from drawlib.styles import Styles

original_devops.cicd_pipeline((30, 25), width=8.5, style=Styles.Neutral)
original_devops.alert_incident((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_devops.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `78` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `github_actions`, `terraform`, `ansible` · 概念: `cicd_pipeline`, `artifact_registry`, `build_runner`, `alert_incident` |
| **連携 Enum・キャッシュ** | `OriginalDevopsIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_devops` |

---

## `type` original_facility

フラット 2D パステル調のデータセンター・拠点ビル・通信施設・物流 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_facility`、全 `86` 関数: ブランドツイン `49` 種＋物理拠点概念 `37` 種）です。

```python
from drawlib.icons import original_facility
from drawlib.styles import Styles

original_facility.branch_office((30, 25), width=8.5, style=Styles.Neutral)
original_facility.cable_landing((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_facility.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `86` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `equinix`, `ntt`, `apc` · 概念: `branch_office`, `cable_landing`, `campus`, `cargo_plane` |
| **連携 Enum・キャッシュ** | `OriginalFacilityIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_facility` |

---

## `type` original_itservice

フラット 2D パステル調の IT コンサルティング・体制図・エンジニアリングロール `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_itservice`、全 `64` 関数: ブランドツイン `44` 種＋組織／ロール概念 `20` 種）です。

```python
from drawlib.icons import original_itservice
from drawlib.styles import Styles

original_itservice.architect_lead((30, 25), width=8.5, style=Styles.Neutral)
original_itservice.dedicated_team((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_itservice.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `64` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `accenture`, `ibm`, `ntt_data` · 概念: `architect_lead`, `bpo_center`, `client_enterprise`, `dedicated_team` |
| **連携 Enum・キャッシュ** | `OriginalItserviceIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_itservice` |

---

## `type` original_network

フラット 2D パステル調のルーター・スイッチ・プロキシ・ネットワーク構成 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_network`、全 `70` 関数）です。

```python
from drawlib.icons import original_network
from drawlib.styles import Styles

original_network.core_router((30, 25), width=8.5, style=Styles.Neutral)
original_network.datacenter_switch((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_network.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `70` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `nginx`, `cloudflare`, `traefik` · 概念: `core_router`, `core_switch`, `datacenter_switch`, `client_pc` |
| **連携 Enum・キャッシュ** | `OriginalNetworkIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_network` |

---

## `type` original_security

フラット 2D パステル調のセキュリティ・IAM・ゼロトラスト防御 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_security`、全 `103` 関数: ブランドツイン `74` 種＋防御機構概念 `29` 種）です。

```python
from drawlib.icons import original_security
from drawlib.styles import Styles

original_security.ddos_protection((30, 25), width=8.5, style=Styles.Neutral)
original_security.directory_service((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_security.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `103` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `auth0`, `okta`, `crowdstrike` · 概念: `ddos_protection`, `casb`, `directory_service`, `dlp` |
| **連携 Enum・キャッシュ** | `OriginalSecurityIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_security` |

---

## `type` original_server

フラット 2D パステル調の Linux ディストリビューション・CPU/GPU・物理サーバー／ストレージ筐体 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_server`、全 `80` 関数）です。

```python
from drawlib.icons import original_server
from drawlib.styles import Styles

original_server.blade_chassis((30, 25), width=8.5, style=Styles.Neutral)
original_server.backup_appliance((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_server.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `80` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `ubuntu`, `debian`, `linux`, `amd` · 概念: `blade_chassis`, `backup_appliance`, `bmc`, `datastore` |
| **連携 Enum・キャッシュ** | `OriginalServerIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_server` |

---

## `type` original_social

フラット 2D パステル調の SNS・動画配信・開発者コミュニティ・AdTech `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_social`、全 `66` 関数: ブランドツイン `50` 種＋チャネル概念 `16` 種）です。

```python
from drawlib.icons import original_social
from drawlib.styles import Styles

original_social.community_forum((30, 25), width=8.5, style=Styles.Neutral)
original_social.chatbot_account((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_social.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `66` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `youtube`, `x`, `linkedin`, `bluesky` · 概念: `ad_targeting`, `chatbot_account`, `community_forum`, `content_moderation` |
| **連携 Enum・キャッシュ** | `OriginalSocialIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_social` |

---

## `type` original_workspace

フラット 2D パステル調のグループウェア・ドキュメント・デザイン・課題管理 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.original_workspace`、全 `57` 関数: ブランドツイン `40` 種＋業務ツール概念 `17` 種）です。

```python
from drawlib.icons import original_workspace
from drawlib.styles import Styles

original_workspace.calendar((30, 25), width=8.5, style=Styles.Neutral)
original_workspace.chat_message((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `original_workspace.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `57` 個 · フラット 2D パステルマルチカラー RGBA PNG。 |
| **代表的なアイコン関数** | ツイン: `slack`, `notion`, `figma`, `jira` · 概念: `announcement`, `calendar`, `chat_message`, `cloud_drive` |
| **連携 Enum・キャッシュ** | `OriginalWorkspaceIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_original_workspace` |

---

## `type` phosphor

単色ティント可能な TrueType ベクターフォントアイコンスイート（`drawlib.icons.phosphor`、全 `1,530` 関数 × `5` ウェイト）です。PNG スイートとは異なり、`style.icon_color` で任意のカラーに染め分けられるほか、`style.icon_style`（`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"` — `Styles.*Thin` / `Styles.*` / `Styles.*Bold` で線幅が自動連動、ベタ塗りは `.patch(icon_style="fill")`）で線の太さや塗りを切り替えられます。

```python
from drawlib.icons import phosphor
from drawlib.styles import Colors, Styles

# 呼び出しシグネチャ: phosphor.<icon_name>(xy, width, *, style) -> None
phosphor.cpu((25, 25), width=7.0, style=Styles.PrimaryBold)
phosphor.shield_check((45, 25), width=7.0, style=Styles.Primary.patch(icon_style="fill"))
phosphor.gear((65, 25), width=7.0, style=Styles.Dark.patch(icon_color=Colors.Teal, icon_style="light", angle=30))
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `phosphor.<icon_name>(xy: tuple[float, float], width: float, *, style: Style) -> None` |
| **引数** | `xy`: 中心座標 `(cx, cy)`、`width`: `1:1` グリフ幅、`style`: `icon_color`・`icon_style`（`"thin"` \| `"light"` \| `"regular"` \| `"bold"` \| `"fill"`）・`angle`・`alpha`・`halign`・`valign` を制御する必須 [`Style`](05_styles_and_types.md)。 |
| **収録数・配色特性** | 全 `1,530` 個 · 単色ティント可能なベクターフォント（任意の解像度で鮮明。濃色カード上では `Styles.WhiteBold` で白抜き描画）。 |
| **代表的なアイコン関数** | `cpu`, `database`, `cloud`, `shield_check`, `git_branch`, `user`, `chart_bar`, `palette`, `sparkle` |
| **連携 Enum・キャッシュ** | `PhosphorIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_phosphor` |

---

## `type` security

認証基盤（IdP）・シークレット管理・脆弱性スキャン・EDR ベンダーの公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.security`、全 `74` 関数）です。

```python
from drawlib.icons import security
from drawlib.styles import Styles

security.auth0((30, 25), width=8.5, style=Styles.Neutral)
security.crowdstrike((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `security.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `74` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_security`）。 |
| **代表的なアイコン関数** | `auth0`, `okta`, `crowdstrike`, `bitwarden`, `aqua_security`, `cerbos`, `burp_suite` |
| **連携 Enum・キャッシュ** | `SecurityIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_security` |

---

## `type` server

Linux OS・CPU/GPU 半導体・ハイパーバイザー・エンタープライズサーバー機器の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.server`、全 `82` 関数）です。

```python
from drawlib.icons import server
from drawlib.styles import Styles

server.ubuntu((30, 25), width=8.5, style=Styles.Neutral)
server.amd((55, 25), width=8.5, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `server.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `82` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_server`）。 |
| **代表的なアイコン関数** | `ubuntu`, `debian`, `redhat`, `linux`, `amd`, `arm`, `alpine_linux`, `arduino` |
| **連携 Enum・キャッシュ** | `ServerIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_server` |

---

## `type` social

SNS・動画配信プラットフォーム・技術コミュニティ・分析／AdTech サービスの公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.social`、全 `50` 関数）です。

```python
from drawlib.icons import social
from drawlib.styles import Styles

social.youtube((30, 25), width=8.0, style=Styles.Neutral)
social.bluesky((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `social.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `50` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_social`）。 |
| **代表的なアイコン関数** | `youtube`, `x`, `linkedin`, `bluesky`, `reddit`, `amplitude`, `dev_to` |
| **連携 Enum・キャッシュ** | `SocialIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_social` |

---

## `type` workspace

チャット・社内 Wiki・デザインツール・プロジェクト管理 SaaS の公式 `512×512` RGBA PNG アイコンスイート（`drawlib.icons.workspace`、全 `40` 関数）です。

```python
from drawlib.icons import workspace
from drawlib.styles import Styles

workspace.slack((30, 25), width=8.0, style=Styles.Neutral)
workspace.notion((55, 25), width=8.0, style=Styles.Neutral)
```

| 項目 / 引数 | 仕様 |
| :--- | :--- |
| **呼び出しシグネチャ** | `workspace.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **収録数・配色特性** | 全 `40` 個 · 公式マルチカラー RGBA PNG（2D パステル版: `original_workspace`）。 |
| **代表的なアイコン関数** | `slack`, `notion`, `figma`, `jira`, `confluence`, `discord`, `dropbox`, `asana` |
| **連携 Enum・キャッシュ** | `WorkspaceIcon`（[`drawlib.diagrams.architecture`](19_diagrams_architecture.md)） · パッケージ名: `icon_workspace` |
