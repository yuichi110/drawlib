# drawlib.icons

Standardized icon system spanning 34 lazy-loaded icon suite submodules (`phosphor` vector font glyphs, `gcp` / `aws` / `azure` + 15 official domain PNG suites, and 15 `original_*` flat 2D pastel twin suites) alongside the custom `font_icon()` renderer. Import suites via `from drawlib.icons import ai, aws, azure, font_icon, gcp, phosphor` and render center-anchored `1:1` icons with a mandatory keyword-only `style` token.

```drawlib align=center code=fold file=08_icons_hero.png caption="34 Standardized Icon Suites Across 3 Visual Tiers — Vector Glyphs, Official Cloud/Vendor Logos, and 2D Pastel Twins"
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

Official AI, LLM, and Machine Learning multi-color `512×512` RGBA PNG icon suite (`drawlib.icons.ai`, `60` icon functions). Multi-color vendor artwork preserves brand colors (`style.icon_color` is ignored; `style.angle`, `style.alpha`, `style.image_tint_color`, and `style.image_border_*` apply).

```python
from drawlib.icons import ai
from drawlib.styles import Styles

# Signature: ai.<icon_name>(xy, width, *, style, variant="default") -> None
ai.openai((30, 25), width=8.0, style=Styles.Neutral)
ai.claude((50, 25), width=8.0, style=Styles.Neutral.patch(angle=15))
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `ai.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Parameters** | `xy`: center `(cx, cy)`; `width`: square `1:1` size in canvas units; `style`: required [`Style`](05_styles_and_types.md) (`angle`, `alpha`, `image_tint_color`, `image_border_*`); `variant`: `"default"`. |
| **Icon Count & Mode** | `60` icons · Multi-color RGBA PNG (preserves official colors; pair with `original_ai` for flat 2D pastel). |
| **Representative Icons** | `openai`, `claude`, `gemini`, `pytorch`, `huggingface`, `autogen`, `crewai`, `arize_phoenix` |
| **Diagram Enum & Cache** | `AiIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_ai` |

---

## `type` aws

Official Amazon Web Services architecture `512×512` RGBA PNG icon suite (`drawlib.icons.aws`, `329` icon functions) covering compute, serverless, storage, database, networking, and analytics services.

```python
from drawlib.icons import aws
from drawlib.styles import Styles

aws.aws_lambda((30, 25), width=9.0, style=Styles.Neutral)
aws.simple_storage_service((55, 25), width=9.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `aws.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Parameters** | `xy`: center `(cx, cy)`; `width`: `1:1` icon width; `style`: required `Style` (`angle`, `alpha`, `image_tint_color`, `image_border_*`); `variant`: `"default"`. |
| **Icon Count & Mode** | `329` icons · Official multi-color AWS RGBA PNG (non-tinted artwork). |
| **Representative Icons** | `aws_lambda`, `simple_storage_service`, `ec2`, `rds`, `dynamodb`, `api_gateway`, `app_runner` |
| **Diagram Enum & Cache** | `AwsIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_aws` |

---

## `type` azure

Official Microsoft Azure architecture `512×512` RGBA PNG icon suite (`drawlib.icons.azure`, `250` icon functions) covering Azure compute, containers, databases, AI Foundry, and identity services.

```python
from drawlib.icons import azure
from drawlib.styles import Styles

azure.function_apps((30, 25), width=9.0, style=Styles.Neutral)
azure.cosmos_db((55, 25), width=9.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `azure.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Parameters** | `xy`: center `(cx, cy)`; `width`: `1:1` icon width; `style`: required `Style`; `variant`: `"default"`. |
| **Icon Count & Mode** | `250` icons · Official multi-color Azure RGBA PNG (non-tinted artwork). |
| **Representative Icons** | `function_apps`, `kubernetes_services`, `sql_database`, `cosmos_db`, `storage_accounts`, `ai_foundry` |
| **Diagram Enum & Cache** | `AzureIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_azure` |

---

## `type` business

Official SaaS, FinTech, CRM, e-commerce, and enterprise business platform `512×512` RGBA PNG icon suite (`drawlib.icons.business`, `48` icon functions).

```python
from drawlib.icons import business
from drawlib.styles import Styles

business.stripe((30, 25), width=8.0, style=Styles.Neutral)
business.salesforce((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `business.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `48` icons · Official multi-color RGBA PNG (pastel twin: `original_business`). |
| **Representative Icons** | `stripe`, `shopify`, `salesforce`, `hubspot`, `zendesk`, `adyen`, `algolia` |
| **Diagram Enum & Cache** | `BusinessIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_business` |

---

## `type` client

Official client OS, web browser, mobile platform, and consumer device vendor `512×512` RGBA PNG icon suite (`drawlib.icons.client`, `60` icon functions).

```python
from drawlib.icons import client
from drawlib.styles import Styles

client.apple((30, 25), width=8.0, style=Styles.Neutral)
client.chrome((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `client.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `60` icons · Official multi-color RGBA PNG (pastel twin: `original_client`). |
| **Representative Icons** | `apple`, `android`, `windows`, `chrome`, `firefox`, `app_store`, `arc` |
| **Diagram Enum & Cache** | `ClientIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_client` |

---

## `type` cloud

Official cloud provider, CDN, and PaaS brand logo `512×512` RGBA PNG icon suite (`drawlib.icons.cloud`, `45` icon functions).

```python
from drawlib.icons import cloud
from drawlib.styles import Styles

cloud.cloudflare((30, 25), width=8.0, style=Styles.Neutral)
cloud.vercel((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `cloud.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `45` icons · Official multi-color RGBA PNG (pastel twin: `original_cloud`). |
| **Representative Icons** | `aws`, `google_cloud`, `azure`, `cloudflare`, `vercel`, `akamai`, `alibaba_cloud` |
| **Diagram Enum & Cache** | `CloudIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_cloud` |

---

## `type` cnative

Official CNCF, Kubernetes workload (`k8s_*`), service mesh, and cloud-native ecosystem `512×512` RGBA PNG icon suite (`drawlib.icons.cnative`, `73` icon functions).

```python
from drawlib.icons import cnative
from drawlib.styles import Styles

cnative.kubernetes((30, 25), width=8.5, style=Styles.Neutral)
cnative.k8s_pod((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `cnative.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `73` icons · Official multi-color RGBA PNG (pastel twin: `original_cnative`). |
| **Representative Icons** | `kubernetes`, `k8s_pod`, `docker`, `helm`, `prometheus`, `argo`, `cilium`, `backstage` |
| **Diagram Enum & Cache** | `CnativeIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_cnative` |

---

## `type` code

Official programming language, web framework, runtime, and IDE `512×512` RGBA PNG icon suite (`drawlib.icons.code`, `97` icon functions).

```python
from drawlib.icons import code
from drawlib.styles import Styles

code.python((30, 25), width=8.0, style=Styles.Neutral)
code.typescript((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `code.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `97` icons · Official multi-color RGBA PNG (pastel twin: `original_code`). |
| **Representative Icons** | `python`, `typescript`, `rust`, `go`, `react`, `angular`, `astro`, `axum` |
| **Diagram Enum & Cache** | `CodeIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_code` |

---

## `type` data

Official relational/NoSQL database, streaming broker, data warehouse, and ETL `512×512` RGBA PNG icon suite (`drawlib.icons.data`, `70` icon functions).

```python
from drawlib.icons import data
from drawlib.styles import Styles

data.postgresql((30, 25), width=8.5, style=Styles.Neutral)
data.kafka((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `data.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `70` icons · Official multi-color RGBA PNG (pastel twin: `original_data`). |
| **Representative Icons** | `postgresql`, `mysql`, `redis`, `mongodb`, `kafka`, `airflow`, `clickhouse`, `chromadb` |
| **Diagram Enum & Cache** | `DataIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_data` |

---

## `type` devops

Official CI/CD pipeline, Infrastructure as Code (IaC), build system, and observability `512×512` RGBA PNG icon suite (`drawlib.icons.devops`, `58` icon functions).

```python
from drawlib.icons import devops
from drawlib.styles import Styles

devops.github_actions((30, 25), width=8.5, style=Styles.Neutral)
devops.terraform((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `devops.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `58` icons · Official multi-color RGBA PNG (pastel twin: `original_devops`). |
| **Representative Icons** | `github_actions`, `gitlab`, `terraform`, `ansible`, `jenkins`, `bazel`, `circleci` |
| **Diagram Enum & Cache** | `DevopsIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_devops` |

---

## `type` facility

Official data center colocation, telecom carrier, power/cooling, and physical infrastructure `512×512` RGBA PNG icon suite (`drawlib.icons.facility`, `49` icon functions).

```python
from drawlib.icons import facility
from drawlib.styles import Styles

facility.equinix((30, 25), width=8.5, style=Styles.Neutral)
facility.ntt((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `facility.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `49` icons · Official multi-color RGBA PNG (pastel twin: `original_facility`). |
| **Representative Icons** | `equinix`, `ntt`, `at_tokyo`, `apc`, `schneider_electric`, `att`, `colt` |
| **Diagram Enum & Cache** | `FacilityIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_facility` |

---

## `def` font_icon(xy, width, code, file, *, style)

Render an arbitrary monochrome vector glyph from a custom TrueType/OpenType icon font file (`drawlib.icons.font_icon`). Unlike PNG icon suites, `font_icon` directly tints the vector glyph using `style.icon_color` (defaulting to `Colors.Black` when unset).

```python
from drawlib.icons import font_icon
from drawlib.styles import Colors, Styles

icon_style = Styles.Primary.patch(icon_color=Colors.Primary, angle=0)
font_icon((50, 25), width=8.0, code="\ue900", file="_assets/fonts/custom_icons.ttf", style=icon_style)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `xy` | `tuple[float, float]` | *Required* | Center coordinate `(cx, cy)` of the icon (adjusted by `style.halign` / `style.valign`). |
| `width` | `float` | *Required* | Horizontal icon size (`> 0.0`) in canvas units. |
| `code` | `str` | *Required* | Unicode character or Private Use Area codepoint string (e.g. `"\ue900"`). |
| `file` | `str` | *Required* | File path to the `.ttf` or `.otf` icon font file. |
| `style` | `Style` | *Required (kw-only)* | [`Style`](05_styles_and_types.md) controlling `icon_color`, `angle`, `alpha`, `halign`, and `valign`. |
| **Returns** | `None` | — | Draws the vector glyph onto the active canvas. |

---

## `type` gcp

Official Google Cloud Platform architecture `512×512` RGBA PNG icon suite (`drawlib.icons.gcp`, `250` icon functions). Core GCP services additionally expose `variant="modern"` alongside `"default"`.

```python
from drawlib.icons import gcp
from drawlib.styles import Styles

gcp.cloud_run((30, 25), width=9.0, style=Styles.Neutral)
gcp.cloud_run((55, 25), width=9.0, style=Styles.Neutral, variant="modern")
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `gcp.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default", "modern"] = "default") -> None` |
| **Parameters** | `xy`: center `(cx, cy)`; `width`: `1:1` icon width; `style`: required `Style`; `variant`: `"default"` (all icons) or `"modern"` (supported GCP core services). |
| **Icon Count & Mode** | `250` icons · Official multi-color Google Cloud RGBA PNG (non-tinted artwork). |
| **Representative Icons** | `cloud_run`, `compute_engine`, `google_kubernetes_engine`, `bigquery`, `cloud_sql`, `ai_hypercomputer` |
| **Diagram Enum & Cache** | `GcpIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_gcp` |

---

## `type` itservice

Official global IT consulting, systems integration (SIer), and managed service provider `512×512` RGBA PNG icon suite (`drawlib.icons.itservice`, `44` icon functions).

```python
from drawlib.icons import itservice
from drawlib.styles import Styles

itservice.accenture((30, 25), width=8.5, style=Styles.Neutral)
itservice.ntt_data((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `itservice.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `44` icons · Official multi-color RGBA PNG (pastel twin: `original_itservice`). |
| **Representative Icons** | `accenture`, `deloitte`, `ibm`, `ntt_data`, `capgemini`, `bcg`, `bain` |
| **Diagram Enum & Cache** | `ItserviceIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_itservice` |

---

## `type` network

Official networking hardware, reverse proxy, DNS, VPN, and Cisco topology (`cisco_*`) `512×512` RGBA PNG icon suite (`drawlib.icons.network`, `70` icon functions). Cisco topology icons support `variant` selection (`"default"`, `"classic"`, `"modern"`).

```python
from drawlib.icons import network
from drawlib.styles import Styles

network.nginx((30, 25), width=8.5, style=Styles.Neutral)
network.tailscale((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `network.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default", "classic", "modern"] = "default") -> None` |
| **Icon Count & Mode** | `70` icons · Official multi-color RGBA PNG (pastel twin: `original_network`). |
| **Representative Icons** | `nginx`, `cloudflare`, `traefik`, `haproxy`, `tailscale`, `apisix`, `arista`, `caddy` |
| **Diagram Enum & Cache** | `NetworkIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_network` |

---

## `type` original_ai

Flat 2D pastel AI & ML `512×512` RGBA PNG icon suite (`drawlib.icons.original_ai`, `80` icon functions), containing unified 2D pastel brand twins for every `ai.*` icon plus `20` vendor-neutral AI architecture concept icons.

```python
from drawlib.icons import original_ai
from drawlib.styles import Styles

original_ai.openai((30, 25), width=8.5, style=Styles.Neutral)
original_ai.ai_agent((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_ai.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `80` icons · Flat 2D pastel multi-color RGBA PNG (`style.icon_color` ignored; `image_tint_color` / `image_border_*` / `angle` / `alpha` apply). |
| **Representative Icons** | Brand twins: `openai`, `claude`, `gemini`, `pytorch` · Concepts: `ai_agent`, `agent_memory`, `dataset`, `embedding_vector` |
| **Diagram Enum & Cache** | `OriginalAiIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_ai` |

---

## `type` original_business

Flat 2D pastel business, finance, and enterprise workflow `512×512` RGBA PNG icon suite (`drawlib.icons.original_business`, `76` icon functions: `48` brand twins + `28` white-label business concept icons).

```python
from drawlib.icons import original_business
from drawlib.styles import Styles

original_business.stripe((30, 25), width=8.5, style=Styles.Neutral)
original_business.approval_workflow((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_business.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `76` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `stripe`, `shopify`, `salesforce` · Concepts: `accounting_ledger`, `approval_workflow`, `bank_transfer`, `billing_invoice` |
| **Diagram Enum & Cache** | `OriginalBusinessIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_business` |

---

## `type` original_client

Flat 2D pastel client device, browser, and endpoint `512×512` RGBA PNG icon suite (`drawlib.icons.original_client`, `92` icon functions: `60` brand twins + `32` hardware/IoT device concept icons).

```python
from drawlib.icons import original_client
from drawlib.styles import Styles

original_client.desktop_pc((30, 25), width=8.5, style=Styles.Neutral)
original_client.connected_car((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_client.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `92` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `apple`, `android`, `chrome` · Concepts: `desktop_pc`, `barcode_scanner`, `connected_car`, `drone` |
| **Diagram Enum & Cache** | `OriginalClientIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_client` |

---

## `type` original_cloud

Flat 2D pastel cloud platform and generic cloud architecture `512×512` RGBA PNG icon suite (`drawlib.icons.original_cloud`, `147` icon functions: `45` provider twins + `102` vendor-neutral cloud service icons).

```python
from drawlib.icons import original_cloud
from drawlib.styles import Styles

original_cloud.api_gateway((30, 25), width=8.5, style=Styles.Neutral)
original_cloud.analytics_engine((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_cloud.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `147` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `aws`, `google_cloud`, `cloudflare` · Concepts: `api_gateway`, `app_service`, `analytics_engine`, `ai_agent` |
| **Diagram Enum & Cache** | `OriginalCloudIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_cloud` |

---

## `type` original_cnative

Flat 2D pastel Kubernetes and CNCF cloud-native `512×512` RGBA PNG icon suite (`drawlib.icons.original_cnative`, `73` icon functions matching `cnative.*` in unified pastel styling).

```python
from drawlib.icons import original_cnative
from drawlib.styles import Styles

original_cnative.kubernetes((30, 25), width=8.5, style=Styles.Neutral)
original_cnative.prometheus((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_cnative.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `73` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | `kubernetes`, `k8s_pod`, `docker`, `helm`, `prometheus`, `argo`, `cilium` |
| **Diagram Enum & Cache** | `OriginalCnativeIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_cnative` |

---

## `type` original_code

Flat 2D pastel programming language, framework, and software artifact `512×512` RGBA PNG icon suite (`drawlib.icons.original_code`, `121` icon functions: `97` brand twins + `24` runtime/artifact concepts).

```python
from drawlib.icons import original_code
from drawlib.styles import Styles

original_code.python((30, 25), width=8.5, style=Styles.Neutral)
original_code.background_worker((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_code.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `121` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `python`, `typescript`, `rust`, `go` · Concepts: `background_worker`, `binary_executable`, `cli_tool`, `compiler_build` |
| **Diagram Enum & Cache** | `OriginalCodeIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_code` |

---

## `type` original_data

Flat 2D pastel database, lakehouse, and data engineering `512×512` RGBA PNG icon suite (`drawlib.icons.original_data`, `86` icon functions: `70` brand twins + `16` data architecture concepts).

```python
from drawlib.icons import original_data
from drawlib.styles import Styles

original_data.data_lakehouse((30, 25), width=8.5, style=Styles.Neutral)
original_data.cdc_stream((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_data.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `86` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `postgresql`, `redis`, `kafka` · Concepts: `data_lakehouse`, `cdc_stream`, `columnar_db`, `data_catalog` |
| **Diagram Enum & Cache** | `OriginalDataIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_data` |

---

## `type` original_devops

Flat 2D pastel CI/CD, IaC, and SRE operations `512×512` RGBA PNG icon suite (`drawlib.icons.original_devops`, `78` icon functions: `58` brand twins + `20` pipeline/incident concepts).

```python
from drawlib.icons import original_devops
from drawlib.styles import Styles

original_devops.cicd_pipeline((30, 25), width=8.5, style=Styles.Neutral)
original_devops.alert_incident((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_devops.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `78` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `github_actions`, `terraform`, `ansible` · Concepts: `cicd_pipeline`, `artifact_registry`, `build_runner`, `alert_incident` |
| **Diagram Enum & Cache** | `OriginalDevopsIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_devops` |

---

## `type` original_facility

Flat 2D pastel data center, office building, telecom, and logistics `512×512` RGBA PNG icon suite (`drawlib.icons.original_facility`, `86` icon functions: `49` brand twins + `37` physical site concepts).

```python
from drawlib.icons import original_facility
from drawlib.styles import Styles

original_facility.branch_office((30, 25), width=8.5, style=Styles.Neutral)
original_facility.cable_landing((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_facility.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `86` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `equinix`, `ntt`, `apc` · Concepts: `branch_office`, `cable_landing`, `campus`, `cargo_plane` |
| **Diagram Enum & Cache** | `OriginalFacilityIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_facility` |

---

## `type` original_itservice

Flat 2D pastel IT consulting, organizational role, and delivery team `512×512` RGBA PNG icon suite (`drawlib.icons.original_itservice`, `64` icon functions: `44` brand twins + `20` role/team concepts).

```python
from drawlib.icons import original_itservice
from drawlib.styles import Styles

original_itservice.architect_lead((30, 25), width=8.5, style=Styles.Neutral)
original_itservice.dedicated_team((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_itservice.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `64` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `accenture`, `ibm`, `ntt_data` · Concepts: `architect_lead`, `bpo_center`, `client_enterprise`, `dedicated_team` |
| **Diagram Enum & Cache** | `OriginalItserviceIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_itservice` |

---

## `type` original_network

Flat 2D pastel network router, switch, proxy, and topology `512×512` RGBA PNG icon suite (`drawlib.icons.original_network`, `70` icon functions).

```python
from drawlib.icons import original_network
from drawlib.styles import Styles

original_network.core_router((30, 25), width=8.5, style=Styles.Neutral)
original_network.datacenter_switch((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_network.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `70` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `nginx`, `cloudflare`, `traefik` · Concepts: `core_router`, `core_switch`, `datacenter_switch`, `client_pc` |
| **Diagram Enum & Cache** | `OriginalNetworkIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_network` |

---

## `type` original_security

Flat 2D pastel cybersecurity, IAM, zero-trust, and compliance `512×512` RGBA PNG icon suite (`drawlib.icons.original_security`, `103` icon functions: `74` brand twins + `29` security control concepts).

```python
from drawlib.icons import original_security
from drawlib.styles import Styles

original_security.ddos_protection((30, 25), width=8.5, style=Styles.Neutral)
original_security.directory_service((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_security.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `103` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `auth0`, `okta`, `crowdstrike` · Concepts: `ddos_protection`, `casb`, `directory_service`, `dlp` |
| **Diagram Enum & Cache** | `OriginalSecurityIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_security` |

---

## `type` original_server

Flat 2D pastel Linux distribution, CPU/GPU silicon, bare-metal chassis, and storage appliance `512×512` RGBA PNG icon suite (`drawlib.icons.original_server`, `80` icon functions).

```python
from drawlib.icons import original_server
from drawlib.styles import Styles

original_server.blade_chassis((30, 25), width=8.5, style=Styles.Neutral)
original_server.backup_appliance((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_server.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `80` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `ubuntu`, `debian`, `linux`, `amd` · Concepts: `blade_chassis`, `backup_appliance`, `bmc`, `datastore` |
| **Diagram Enum & Cache** | `OriginalServerIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_server` |

---

## `type` original_social

Flat 2D pastel social platform, developer community, streaming, and AdTech `512×512` RGBA PNG icon suite (`drawlib.icons.original_social`, `66` icon functions: `50` brand twins + `16` engagement concepts).

```python
from drawlib.icons import original_social
from drawlib.styles import Styles

original_social.community_forum((30, 25), width=8.5, style=Styles.Neutral)
original_social.chatbot_account((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_social.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `66` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `youtube`, `x`, `linkedin`, `bluesky` · Concepts: `ad_targeting`, `chatbot_account`, `community_forum`, `content_moderation` |
| **Diagram Enum & Cache** | `OriginalSocialIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_social` |

---

## `type` original_workspace

Flat 2D pastel collaboration, productivity, document, and team messaging `512×512` RGBA PNG icon suite (`drawlib.icons.original_workspace`, `57` icon functions: `40` brand twins + `17` workspace artifact concepts).

```python
from drawlib.icons import original_workspace
from drawlib.styles import Styles

original_workspace.calendar((30, 25), width=8.5, style=Styles.Neutral)
original_workspace.chat_message((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `original_workspace.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `57` icons · Flat 2D pastel multi-color RGBA PNG. |
| **Representative Icons** | Twins: `slack`, `notion`, `figma`, `jira` · Concepts: `announcement`, `calendar`, `chat_message`, `cloud_drive` |
| **Diagram Enum & Cache** | `OriginalWorkspaceIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_original_workspace` |

---

## `type` phosphor

Monochrome-tintable TrueType vector font icon suite (`drawlib.icons.phosphor`, `1,530` icon functions × `5` stroke/fill weights). Unlike PNG icon packages, `phosphor` renders vector font glyphs directly tinted by `style.icon_color` and styled by `style.icon_style` (`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"` — with `"thin"`, `"regular"`, and `"bold"` automatically mapped by `Styles.*Thin`, `Styles.*`, and `Styles.*Bold`).

```python
from drawlib.icons import phosphor
from drawlib.styles import Colors, Styles

# Signature: phosphor.<icon_name>(xy, width, *, style) -> None
phosphor.cpu((25, 25), width=7.0, style=Styles.PrimaryBold)
phosphor.shield_check((45, 25), width=7.0, style=Styles.Primary.patch(icon_style="fill"))
phosphor.gear((65, 25), width=7.0, style=Styles.Dark.patch(icon_color=Colors.Teal, icon_style="light", angle=30))
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `phosphor.<icon_name>(xy: tuple[float, float], width: float, *, style: Style) -> None` |
| **Parameters** | `xy`: center `(cx, cy)`; `width`: `1:1` glyph width in canvas units; `style`: required [`Style`](05_styles_and_types.md) controlling `icon_color`, `icon_style` (`"thin"` \| `"light"` \| `"regular"` \| `"bold"` \| `"fill"`), `angle`, `alpha`, `halign`, `valign`. |
| **Icon Count & Mode** | `1,530` icons · Monochrome-tintable vector font glyphs (crisp at any DPI; white-on-dark via `style=Styles.WhiteBold`). |
| **Representative Icons** | `cpu`, `database`, `cloud`, `shield_check`, `git_branch`, `user`, `chart_bar`, `palette`, `sparkle` |
| **Diagram Enum & Cache** | `PhosphorIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_phosphor` |

---

## `type` security

Official identity (IdP), zero-trust, secret management, vulnerability scanning, and EDR vendor `512×512` RGBA PNG icon suite (`drawlib.icons.security`, `74` icon functions).

```python
from drawlib.icons import security
from drawlib.styles import Styles

security.auth0((30, 25), width=8.5, style=Styles.Neutral)
security.crowdstrike((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `security.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `74` icons · Official multi-color RGBA PNG (pastel twin: `original_security`). |
| **Representative Icons** | `auth0`, `okta`, `crowdstrike`, `bitwarden`, `aqua_security`, `cerbos`, `burp_suite` |
| **Diagram Enum & Cache** | `SecurityIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_security` |

---

## `type` server

Official Linux OS distribution, CPU/GPU silicon vendor, hypervisor, and enterprise server hardware `512×512` RGBA PNG icon suite (`drawlib.icons.server`, `82` icon functions).

```python
from drawlib.icons import server
from drawlib.styles import Styles

server.ubuntu((30, 25), width=8.5, style=Styles.Neutral)
server.amd((55, 25), width=8.5, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `server.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `82` icons · Official multi-color RGBA PNG (pastel twin: `original_server`). |
| **Representative Icons** | `ubuntu`, `debian`, `redhat`, `linux`, `amd`, `arm`, `alpine_linux`, `arduino` |
| **Diagram Enum & Cache** | `ServerIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_server` |

---

## `type` social

Official social network, video streaming, developer community, and analytics/AdTech `512×512` RGBA PNG icon suite (`drawlib.icons.social`, `50` icon functions).

```python
from drawlib.icons import social
from drawlib.styles import Styles

social.youtube((30, 25), width=8.0, style=Styles.Neutral)
social.bluesky((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `social.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `50` icons · Official multi-color RGBA PNG (pastel twin: `original_social`). |
| **Representative Icons** | `youtube`, `x`, `linkedin`, `bluesky`, `reddit`, `amplitude`, `dev_to` |
| **Diagram Enum & Cache** | `SocialIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_social` |

---

## `type` workspace

Official team collaboration, documentation wiki, design tool, and issue tracker `512×512` RGBA PNG icon suite (`drawlib.icons.workspace`, `40` icon functions).

```python
from drawlib.icons import workspace
from drawlib.styles import Styles

workspace.slack((30, 25), width=8.0, style=Styles.Neutral)
workspace.notion((55, 25), width=8.0, style=Styles.Neutral)
```

| Field / Parameter | Specification |
| :--- | :--- |
| **Call Signature** | `workspace.<icon_name>(xy: tuple[float, float], width: float, *, style: Style, variant: Literal["default"] = "default") -> None` |
| **Icon Count & Mode** | `40` icons · Official multi-color RGBA PNG (pastel twin: `original_workspace`). |
| **Representative Icons** | `slack`, `notion`, `figma`, `jira`, `confluence`, `discord`, `dropbox`, `asana` |
| **Diagram Enum & Cache** | `WorkspaceIcon` ([`drawlib.diagrams.architecture`](19_diagrams_architecture.md)) · Cache package: `icon_workspace` |
