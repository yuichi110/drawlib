# Drawlib Icons Overview Guidelines (`lib-icons-overview`)

Comprehensive architectural guide and routing catalog for `drawlib.icons`. Drawlib provides **34 icon modules** (**3,500+ total icons**) plus the low-level `font_icon()` renderer, organized into **3 visual tiers** and **19 sub-topic manuals**.

---

## 1. Sub-Topic Routing Table & Complete 34-Module Catalog

Query the specific icon sub-topic for complete function catalogs, enum tokens, and diagram examples:

| Rule Topic | CLI Command | Modules Covered (`drawlib.icons.*`) | Diagram Enums (`drawlib.diagrams.architecture`) | Canonical Icons | Asset Package(s) |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`lib-icons-phosphor`** | `uv run drawlib rules show lib-icons-phosphor` | `phosphor`, `font_icon` | `PhosphorIcon` | 1,512 × 5 weights | `icon_phosphor` |
| **`lib-icons-gcp`** | `uv run drawlib rules show lib-icons-gcp` | `gcp` | `GcpIcon` | 206 (`237` funcs) | `icon_gcp` |
| **`lib-icons-aws`** | `uv run drawlib rules show lib-icons-aws` | `aws` | `AwsIcon` | 80 | `icon_aws` |
| **`lib-icons-azure`** | `uv run drawlib rules show lib-icons-azure` | `azure` | `AzureIcon` | 80 | `icon_azure` |
| **`lib-icons-ai`** | `uv run drawlib rules show lib-icons-ai` | `ai`, `original_ai` | `AiIcon`, `OriginalAiIcon` | 60 / 80 | `icon_ai`, `icon_original_ai` |
| **`lib-icons-business`** | `uv run drawlib rules show lib-icons-business` | `business`, `original_business` | `BusinessIcon`, `OriginalBusinessIcon` | 48 / 76 | `icon_business`, `icon_original_business` |
| **`lib-icons-client`** | `uv run drawlib rules show lib-icons-client` | `client`, `original_client` | `ClientIcon`, `OriginalClientIcon` | 60 / 92 | `icon_client`, `icon_original_client` |
| **`lib-icons-cloud`** | `uv run drawlib rules show lib-icons-cloud` | `cloud`, `original_cloud` | `CloudIcon`, `OriginalCloudIcon` | 45 / 147 | `icon_cloud`, `icon_original_cloud` |
| **`lib-icons-cnative`** | `uv run drawlib rules show lib-icons-cnative` | `cnative`, `original_cnative` | `CnativeIcon`, `OriginalCnativeIcon` | 73 / 73 | `icon_cnative`, `icon_original_cnative` |
| **`lib-icons-code`** | `uv run drawlib rules show lib-icons-code` | `code`, `original_code` | `CodeIcon`, `OriginalCodeIcon` | 97 / 121 | `icon_code`, `icon_original_code` |
| **`lib-icons-data`** | `uv run drawlib rules show lib-icons-data` | `data`, `original_data` | `DataIcon`, `OriginalDataIcon` | 70 / 86 | `icon_data`, `icon_original_data` |
| **`lib-icons-devops`** | `uv run drawlib rules show lib-icons-devops` | `devops`, `original_devops` | `DevopsIcon`, `OriginalDevopsIcon` | 58 / 78 | `icon_devops`, `icon_original_devops` |
| **`lib-icons-facility`** | `uv run drawlib rules show lib-icons-facility` | `facility`, `original_facility` | `FacilityIcon`, `OriginalFacilityIcon` | 49 / 86 | `icon_facility`, `icon_original_facility` |
| **`lib-icons-itservice`** | `uv run drawlib rules show lib-icons-itservice` | `itservice`, `original_itservice` | `ItserviceIcon`, `OriginalItserviceIcon` | 44 / 64 | `icon_itservice`, `icon_original_itservice` |
| **`lib-icons-network`** | `uv run drawlib rules show lib-icons-network` | `network`, `original_network` | `NetworkIcon`, `OriginalNetworkIcon` | 70 / 70 | `icon_network`, `icon_original_network` |
| **`lib-icons-security`** | `uv run drawlib rules show lib-icons-security` | `security`, `original_security` | `SecurityIcon`, `OriginalSecurityIcon` | 74 / 103 | `icon_security`, `icon_original_security` |
| **`lib-icons-server`** | `uv run drawlib rules show lib-icons-server` | `server`, `original_server` | `ServerIcon`, `OriginalServerIcon` | 82 / 80 | `icon_server`, `icon_original_server` |
| **`lib-icons-social`** | `uv run drawlib rules show lib-icons-social` | `social`, `original_social` | `SocialIcon`, `OriginalSocialIcon` | 50 / 66 | `icon_social`, `icon_original_social` |
| **`lib-icons-workspace`** | `uv run drawlib rules show lib-icons-workspace` | `workspace`, `original_workspace` | `WorkspaceIcon`, `OriginalWorkspaceIcon` | 40 / 57 | `icon_workspace`, `icon_original_workspace` |

---

## 2. Three Visual Tiers & Architectural Selection Rules

1. **Tier 1 — Monochrome Vector Font Glyphs (`phosphor`, `font_icon`)**:
   - Rendered as crisp TrueType font glyphs where `style.icon_color` (or `Styles.Primary`, `Styles.Dark`, `Styles.White`) directly colors the vector stroke/fill.
   - Supports 5 weights: `"regular"`, `"bold"`, `"light"`, `"thin"`, and `"fill"`.
   - Best for UI wireframes, generic step badges (`SmartArts`), process flows, and inline status markers.
2. **Tier 2 — Official Cloud & Vendor Logos (`gcp`, `aws`, `azure`, + 15 Domain Suites `ai`..`workspace`)**:
   - Multi-color `512×512` RGBA PNG artwork representing official cloud services, CNCF projects (`k8s_*`), Cisco topologies (`cisco_*`), Dell/VMware hardware (`dell_*`, `vmware_*`), and vendor trademarks.
   - Best for cloud architecture diagrams (`ArchitectureDiagram`), vendor stack comparisons, and real-world system blueprints.
3. **Tier 3 — Original 2D Pastel Twin Suites (15 `original_*` Modules)**:
   - Every official domain suite (`ai` through `workspace`) has a paired `original_<domain>` module containing:
     1. **2D Pastel Brand Twins**: Every brand function in `<domain>.<name>()` has a matching `original_<domain>.<name>()` rendered in a unified flat 2D pastel palette.
     2. **Vendor-Neutral Concept Icons**: Additional domain concept icons (`original_ai.rag_pipeline`, `original_data.data_lakehouse`, `original_security.zero_trust`, etc.) for white-label architectures.

---

## 3. Universal Coordinate Geometry (`xy = (cx, cy)`) & Required `*, style: Style`

Every icon function across all 34 modules shares an identical spatial contract:
- **Center Anchor `xy = (cx, cy)`**: Specifies the **exact geometric center** of the icon (matching `drawlib.shapes` and `drawlib.text`).
- **Square `1:1` Aspect Ratio (`width`)**: `width: float` sets the horizontal width in canvas units; height is automatically `1:1` (`height == width`).
- **Required Keyword-Only `*, style: Style`**: `style` is a **mandatory keyword-only argument** on every icon function (`phosphor.*`, `gcp.*`, `aws.*`, `azure.*`, `<domain>.*`, `original_<domain>.*`, and `font_icon`). Never omit `style=...`.

```python
from drawlib.icons import ai, aws, gcp, original_ai, phosphor
from drawlib.styles import Colors, Styles

# 1. Tier 1: Phosphor vector glyph (colored via style.icon_color)
phosphor.cpu((20, 25), width=8.0, style=Styles.Primary, weight="bold")

# 2. Tier 2: Official cloud & vendor PNG icons (512x512 RGBA, center-anchored)
gcp.cloud_run((45, 25), width=9.0, style=Styles.Primary)
aws.aws_lambda((70, 25), width=9.0, style=Styles.Primary)
ai.openai((95, 25), width=9.0, style=Styles.Primary)

# 3. Tier 3: Original 2D pastel brand twin & concept icon with optional container frame
framed = Styles.Primary.patch(
    image_tint_color=Colors.Primary1,
    image_border_color=Colors.Primary,
    image_border_width=1.0,
)
original_ai.rag_pipeline((120, 25), width=9.0, style=framed)
```

### Style Attributes Respected by Icons

| Attribute | Tier 1 (`phosphor` / `font_icon`) | Tier 2 & Tier 3 (RGBA PNG Suites) |
| :--- | :--- | :--- |
| **`icon_color`** | Colors the vector glyph directly (default `Colors.Black`) | Ignored (preserves multi-color PNG artwork) |
| **`image_tint_color`** | Ignored | Fills the square icon background box behind transparent pixels |
| **`image_border_color` / `width` / `style`** | Ignored | Draws a `"solid"`, `"dashed"`, `"dotted"`, or `"dashdot"` frame around the `width × width` box |
| **`alpha`** | Controls glyph opacity (`0.0`–`1.0`) | Controls PNG opacity (`0.0`–`1.0`) |
| **`angle`** | Rotates glyph CCW in degrees around `(cx, cy)` | Rotates PNG CCW in degrees around `(cx, cy)` |
| **`halign` / `valign`** | `"center"` / `"center"` default | `"center"` / `"center"` default |

---

## 4. High-Level Diagram & SmartArt Integration

All 34 icon suites export strongly typed `StrEnum` classes (re-exported by `drawlib.icons` and `drawlib.diagrams.architecture`) that plug directly into:
- **`ArchitectureDiagram`**: `Node(..., icon=GcpIcon.CLOUD_RUN)` or `Node(..., icon=AwsIcon.AWS_LAMBDA)`
- **`SequenceDiagram`**: `sd.add_participant("API", icon=CnativeIcon.K8S_POD)`
- **`FlowDiagram` / `SmartArts`**: Any `PhosphorIcon`, `GcpIcon`, `AwsIcon`, `AzureIcon`, `<Domain>Icon`, or `Original<Domain>Icon` enum member.

---

## 5. Asset Cache Management (`drawlib cache`)

Icon binary archives (`icon_phosphor`, `icon_gcp`, `icon_aws`, `icon_azure`, `icon_<domain>`, `icon_original_<domain>`) are downloaded on demand and cached in `~/.cache/drawlib/`. For offline or CI environments, pre-download all assets:

```bash
uv run drawlib cache list            # Inspect cached font and icon packages
uv run drawlib cache download --all  # Pre-download all 34 icon suites and fonts
uv run drawlib cache clear --all     # Clear cached archives and build DB
```
