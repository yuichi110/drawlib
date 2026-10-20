# Icons Overview

Drawlib provides **4,538 canonical icons** organized across **34 icon modules** (`drawlib.icons.*`) in four visual tiers: **Phosphor Vector Glyphs** (`phosphor`), **Cloud Provider Suites** (`gcp`, `aws`, `azure`), **15 Official Brand Suites** (`ai`, `data`, `code`, `cnative`, `devops`, etc.), and **15 Original 2D Pastel Suites** (`original_*`).

```drawlib code=fold align=center file=icons_overview_hero.png caption="Drawlib's 34 Icon Modules Across 4 Visual Tiers (4,538 Canonical Icons)"
from drawlib.canvas import save, setup
from drawlib.icons import (
    ai,
    aws,
    azure,
    cnative,
    code,
    data,
    gcp,
    original_ai,
    original_cloud,
    original_data,
    original_security,
    phosphor,
)
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=70)

tiers = [
    (
        20.0,
        "1. Vector Glyphs",
        "phosphor (1,512)",
        Styles.Neutral,
        [
            ("cpu", phosphor.cpu, Styles.DarkBold),
            ("database", phosphor.database, Styles.PrimaryBold),
            ("shield", phosphor.shield_check, Styles.SecondaryBold),
            ("git", phosphor.git_branch, Styles.DarkBold),
        ],
    ),
    (
        54.5,
        "2. Cloud Providers",
        "gcp · aws · azure (829)",
        Styles.PrimaryNeutral,
        [
            ("GKE", gcp.google_kubernetes_engine, Styles.Primary),
            ("BigQuery", gcp.bigquery, Styles.Primary),
            ("Lambda", aws.aws_lambda, Styles.Primary),
            ("AKS", azure.kubernetes_services, Styles.Primary),
        ],
    ),
    (
        89.5,
        "3. Official Brands",
        "15 Domain Suites (910)",
        Styles.Neutral,
        [
            ("OpenAI", ai.openai, Styles.Primary),
            ("PostgreSQL", data.postgresql, Styles.Primary),
            ("Kubernetes", cnative.kubernetes, Styles.Primary),
            ("Python", code.python, Styles.Primary),
        ],
    ),
    (
        124.0,
        "4. 2D Pastel Suites",
        "15 original_* (1,287)",
        Styles.SecondaryNeutral,
        [
            ("API GW", original_cloud.api_gateway, Styles.Primary),
            ("AI Agent", original_ai.ai_agent, Styles.Primary),
            ("Warehouse", original_data.data_warehouse, Styles.Primary),
            ("DDoS Guard", original_security.ddos_protection, Styles.Primary),
        ],
    ),
]

for cx, title, subtitle, card_style, icons_list in tiers:
    # Column card container
    rectangle((cx, 35), width=32.5, height=62, style=card_style.patch(shape_r=2.5))
    text((cx, 60.0), title, style=Styles.DarkBold.patch(text_size=11.0))
    text((cx, 54.8), subtitle, style=Styles.Muted.patch(text_size=9.5))

    # 2x2 grid of representative icons inside each column
    offsets = [(-7.6, 42.0), (7.6, 42.0), (-7.6, 21.0), (7.6, 21.0)]
    sub_card_style = Styles.White.patch(shape_r=1.5, line_width=0.6)
    for (dx, iy), (lbl, fn, st) in zip(offsets, icons_list, strict=True):
        ix = cx + dx
        rectangle((ix, iy - 2.0), width=13.8, height=17.5, style=sub_card_style)
        fn((ix, iy + 1.2), width=7.5, style=st)
        text((ix, iy - 6.8), lbl, style=Styles.DarkBold.patch(text_size=9.5))

save()
```

---

## 1. Why Three Visual Styles? (Choosing the Right Icon Tier)

Different technical illustrations call for different levels of visual specificity. Drawlib organizes its 4,538 canonical icons into three distinct visual styles across four module groups so you can match the exact fidelity of your document:

| Visual Style | Modules & Canonical Count | Rendering Engine | Best Use Cases |
| :--- | :--- | :--- | :--- |
| **1. Phosphor Vector Icons** | `phosphor` (**1,512** icons) | TrueType vector glyphs (`text()` engine) across 5 weights (`thin`, `light`, `regular`, `bold`, `fill`) | UI wireframes, callouts, flow steps, corner status badges, and generic system concepts tinted with theme colors (`Styles.PrimaryBold`, `Styles.DarkBold`). |
| **2. Official Vendor & Brand Icons** | `gcp`, `aws`, `azure` (**829** cloud icons) + 15 official domain modules (**910** brand icons) = **1,739** total | High-resolution `512×512` RGBA PNGs (`image()` engine) | Vendor-specific cloud architecture topologies (GCP, AWS, Azure) and production tech stack diagrams featuring real-world product logos (OpenAI, PostgreSQL, Kubernetes, Python, Okta). |
| **3. Original 2D Pastel Icons** | 15 `original_*` modules (**1,287** icons) | High-resolution `512×512` RGBA PNGs (`image()` engine) authored in Drawlib's flat 2D pastel aesthetic | Multi-domain diagrams where disparate vendor logos would clash visually, or vendor-neutral reference architectures requiring trademark-free concept and platform illustrations. |

- **Use `phosphor` Vector Icons** when you need lightweight, single-color icons that inherit your theme palette (`style=Styles.PrimaryBold`, `Styles.WhiteBold`)—such as step indicators, warning badges, or high-level conceptual flowcharts.
- **Use Official Vendor & Brand Icons (`gcp`, `aws`, `azure`, `ai`, `data`, `code`, `cnative`, etc.)** when documenting an exact production deployment where engineers expect to recognize official service and open-source logos at a glance.
- **Use Original 2D Pastel Icons (`original_cloud`, `original_ai`, `original_data`, etc.)** when combining concepts across many domains (e.g., facility hardware, enterprise SaaS, AI agents, and cloud gateways) and you want every icon on the canvas to share a cohesive, calm 2D illustration style.

---

## 2. Unified Icon API & Coordinate Anchor

Every icon function across `phosphor` and all 33 PNG icon modules shares the exact same **center-anchored `(cx, cy)`** call signature:

```python
from drawlib.icons import ai, gcp, original_ai, phosphor
from drawlib.styles import Styles

# All icon modules anchor at the center (cx, cy) with a 1:1 square aspect ratio:
phosphor.robot((20, 25), width=10.0, style=Styles.PrimaryBold)
gcp.vertex_ai((50, 25), width=10.0, style=Styles.Primary, variant="default")
ai.openai((80, 25), width=10.0, style=Styles.Primary)
original_ai.ai_agent((110, 25), width=10.0, style=Styles.Primary)
```

| Parameter / `Style` Attribute | Applies To | Description |
| :--- | :--- | :--- |
| `xy: tuple[float, float]` | All 34 modules | Center coordinate `(cx, cy)` of the icon (`halign="center"`, `valign="center"` by default). |
| `width: float` | All 34 modules | Horizontal width in canvas units; height scales automatically at a `1:1` square aspect ratio. |
| `style: Style` | All 34 modules | Controls `angle` (rotation in degrees), `alpha` (`0.0–1.0` opacity), `halign`, `valign`, and `xy_shift`. |
| `style.icon_style`, `style.icon_color` | `phosphor`, `font_icon` | Selects vector glyph weight (`"thin"`, `"light"`, `"regular"`, `"bold"`, `"fill"`) and stroke/fill color. |
| `style.image_tint_color`, `style.image_border_*` | All 33 PNG modules | Fills transparent PNG background pixels or frames the icon bounding box with a solid/dashed border. |
| `variant: str = "default"` | All 33 PNG modules | Selects `"default"` palette (all modules) or `"modern"` on supported `gcp` and `network` (`cisco_*`) icons. |
| `<Module>Icon` Enums | `ArchitectureDiagram`, `SequenceDiagram` | Strongly typed `StrEnum`/`Enum` classes (`PhosphorIcon`, `GcpIcon`, `AwsIcon`, `AiIcon`, `OriginalAiIcon`, etc.) passed to `Node(icon=...)` or `Participant(icon=...)`. |

### 2.1. Side-by-Side Comparison Across Visual Tiers

The following diagram renders the same five architectural roles (**LLM / AI**, **Database**, **Kubernetes**, **Security / IAM**, and **Client Browser**) across all three visual styles:

```drawlib code=show align=center file=icons_overview_side_by_side.png caption="Comparing Phosphor Vector, Official Brand, and Original 2D Pastel Icons"
from drawlib.canvas import save, setup
from drawlib.icons import (
    ai,
    client,
    cnative,
    data,
    original_ai,
    original_client,
    original_cnative,
    original_data,
    original_security,
    phosphor,
    security,
)
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=78)

columns = [
    ("LLM / AI", phosphor.robot, ai.openai, original_ai.openai),
    ("Database", phosphor.database, data.postgresql, original_data.postgresql),
    ("Kubernetes", phosphor.cube, cnative.kubernetes, original_cnative.kubernetes),
    ("Security / IAM", phosphor.shield_check, security.okta, original_security.okta),
    ("Client Browser", phosphor.browser, client.chrome, original_client.chrome),
]

rows = [
    (56.5, "Tier 1: Phosphor", "Vector Glyph", Styles.Neutral),
    (35.0, "Tier 2: Official", "Vendor / OSS Logo", Styles.PrimaryNeutral),
    (13.5, "Tier 3: Original", "2D Pastel Suite", Styles.SecondaryNeutral),
]

# Column headers
for col_idx, (col_title, _, _, _) in enumerate(columns):
    cx = 46.0 + col_idx * 21.5
    text((cx, 71.0), col_title, style=Styles.DarkBold.patch(text_size=10.5))

# Row labels and icon cells
for row_idx, (cy, row_title, row_sub, card_st) in enumerate(rows):
    rectangle((18.5, cy), width=29.0, height=18.5, style=card_st.patch(shape_r=2))
    text((18.5, cy + 2.5), row_title, style=Styles.DarkBold.patch(text_size=10.0))
    text((18.5, cy - 3.0), row_sub, style=Styles.Muted.patch(text_size=9.5))

    for col_idx, (_, fn_vec, fn_off, fn_orig) in enumerate(columns):
        cx = 46.0 + col_idx * 21.5
        rectangle((cx, cy), width=19.0, height=18.5, style=card_st.patch(shape_r=2))
        if row_idx == 0:
            fn_vec((cx, cy), width=8.5, style=Styles.PrimaryBold)
        elif row_idx == 1:
            fn_off((cx, cy), width=8.5, style=Styles.Primary)
        else:
            fn_orig((cx, cy), width=8.5, style=Styles.Primary)

save()
```

---

## 3. Complete 34 Icon Modules Directory

All 34 icon modules use a strict **1-to-1 canonical naming rule** (zero aliases) and lazy-load their underlying font or PNG archive on first use. To pre-download all icon packages for offline or CI environments, run `uv run drawlib cache download --all`.

| Module (`drawlib.icons.*`) | Diagram Enum (`*Icon`) | Visual Tier | Canonical Icons | Asset Package | Dedicated Documentation Page |
| :--- | :--- | :--- | :---: | :--- | :--- |
| `phosphor` | `PhosphorIcon` | Vector Font (5 weights) | 1,512 | `icon_phosphor` | [Phosphor Vector Icons](./phosphor.md) |
| `gcp` | `GcpIcon` | Cloud Provider (Official) | 253 | `icon_gcp` | [Google Cloud (GCP) Icons](./gcp.md) |
| `aws` | `AwsIcon` | Cloud Provider (Official) | 329 | `icon_aws` | [Amazon Web Services (AWS) Icons](./aws.md) |
| `azure` | `AzureIcon` | Cloud Provider (Official) | 250 | `icon_azure` | [Microsoft Azure Icons](./azure.md) |
| `cloud` | `CloudIcon` | Official Brand | 45 | `icon_cloud` | [Cloud & Original Cloud Icons](./cloud.md) |
| `original_cloud` | `OriginalCloudIcon` | Original 2D Pastel | 147 | `icon_original_cloud` | [Cloud & Original Cloud Icons](./cloud.md) |
| `cnative` | `CnativeIcon` | Official Brand | 73 | `icon_cnative` | [Cloud Native (K8s) Icons](./cnative.md) |
| `original_cnative` | `OriginalCnativeIcon` | Original 2D Pastel | 73 | `icon_original_cnative` | [Cloud Native (K8s) Icons](./cnative.md) |
| `devops` | `DevopsIcon` | Official Brand | 58 | `icon_devops` | [DevOps & Observability Icons](./devops.md) |
| `original_devops` | `OriginalDevopsIcon` | Original 2D Pastel | 78 | `icon_original_devops` | [DevOps & Observability Icons](./devops.md) |
| `network` | `NetworkIcon` | Official Brand & Cisco | 70 | `icon_network` | [Network & Cisco Topology Icons](./network.md) |
| `original_network` | `OriginalNetworkIcon` | Original 2D Pastel | 70 | `icon_original_network` | [Network & Cisco Topology Icons](./network.md) |
| `server` | `ServerIcon` | Official Brand & Dell/VMware | 82 | `icon_server` | [Server, OS & Virtualization Icons](./server.md) |
| `original_server` | `OriginalServerIcon` | Original 2D Pastel | 80 | `icon_original_server` | [Server, OS & Virtualization Icons](./server.md) |
| `security` | `SecurityIcon` | Official Brand | 74 | `icon_security` | [Security & Zero-Trust Icons](./security.md) |
| `original_security` | `OriginalSecurityIcon` | Original 2D Pastel | 103 | `icon_original_security` | [Security & Zero-Trust Icons](./security.md) |
| `facility` | `FacilityIcon` | Official Brand | 49 | `icon_facility` | [Data Center & Facility Icons](./facility.md) |
| `original_facility` | `OriginalFacilityIcon` | Original 2D Pastel | 86 | `icon_original_facility` | [Data Center & Facility Icons](./facility.md) |
| `ai` | `AiIcon` | Official Brand | 60 | `icon_ai` | [AI & Machine Learning Icons](./ai.md) |
| `original_ai` | `OriginalAiIcon` | Original 2D Pastel | 80 | `icon_original_ai` | [AI & Machine Learning Icons](./ai.md) |
| `data` | `DataIcon` | Official Brand | 70 | `icon_data` | [Data & Database Icons](./data.md) |
| `original_data` | `OriginalDataIcon` | Original 2D Pastel | 86 | `icon_original_data` | [Data & Database Icons](./data.md) |
| `code` | `CodeIcon` | Official Brand | 97 | `icon_code` | [Code, Languages & Frameworks Icons](./code.md) |
| `original_code` | `OriginalCodeIcon` | Original 2D Pastel | 121 | `icon_original_code` | [Code, Languages & Frameworks Icons](./code.md) |
| `business` | `BusinessIcon` | Official Brand | 48 | `icon_business` | [Enterprise Business & FinTech Icons](./business.md) |
| `original_business` | `OriginalBusinessIcon` | Original 2D Pastel | 76 | `icon_original_business` | [Enterprise Business & FinTech Icons](./business.md) |
| `itservice` | `ItserviceIcon` | Official Brand | 44 | `icon_itservice` | [IT Services & Consulting Icons](./itservice.md) |
| `original_itservice` | `OriginalItserviceIcon` | Original 2D Pastel | 64 | `icon_original_itservice` | [IT Services & Consulting Icons](./itservice.md) |
| `workspace` | `WorkspaceIcon` | Official Brand | 40 | `icon_workspace` | [Workspace & Collaboration Icons](./workspace.md) |
| `original_workspace` | `OriginalWorkspaceIcon` | Original 2D Pastel | 57 | `icon_original_workspace` | [Workspace & Collaboration Icons](./workspace.md) |
| `social` | `SocialIcon` | Official Brand | 50 | `icon_social` | [Social, Media & Community Icons](./social.md) |
| `original_social` | `OriginalSocialIcon` | Original 2D Pastel | 66 | `icon_original_social` | [Social, Media & Community Icons](./social.md) |
| `client` | `ClientIcon` | Official Brand | 60 | `icon_client` | [Client Devices & Endpoints Icons](./client.md) |
| `original_client` | `OriginalClientIcon` | Original 2D Pastel | 92 | `icon_original_client` | [Client Devices & Endpoints Icons](./client.md) |

---

## 4. Using Icons in High-Level Diagrams (`ArchitectureDiagram` & `SequenceDiagram`)

Both **[`ArchitectureDiagram`](../06_diagrams/architecture.md)** (`Node(..., icon=...)`) and **[`SequenceDiagram`](../06_diagrams/sequence.md)** (`Participant(..., icon=...)`) natively accept all 34 `*Icon` Enums (`ClientIcon`, `AiIcon`, `GcpIcon`, `AwsIcon`, `DataIcon`, `OriginalAiIcon`, etc.), letting you mix client devices, cloud infrastructure, AI models, and databases in a single connected topology:

```drawlib code=show align=center file=icons_overview_arch_integration.png caption="Mixing Multiple Icon Modules in an ArchitectureDiagram"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    AiIcon,
    ArchitectureDiagram,
    ClientIcon,
    DataIcon,
    GcpIcon,
    Node,
    NodeGroup,
)
from drawlib.styles import Styles

setup(width=132, height=64)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Multi-Domain RAG Pipeline (ClientIcon + GcpIcon + AiIcon + DataIcon)",
)

web = d.add(
    Node("Chrome Client", width=24, height=18, icon=ClientIcon.CHROME, icon_size=7.5),
    xy=(14.0, 22.0),
)

vpc = d.add(NodeGroup(title="Production Cloud VPC", padding=5.0), xy=(40.0, 4.0))
run = vpc.add(
    Node(
        "Cloud Run\nOrchestrator",
        width=25,
        height=18,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(16.0, 18.0),
)
llm = vpc.add(
    Node(
        "OpenAI\nAPI",
        width=24,
        height=18,
        icon=AiIcon.OPENAI,
        icon_size=7.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(60.0, 28.0),
)
pg = vpc.add(
    Node(
        "PostgreSQL\npgvector",
        width=24,
        height=18,
        icon=DataIcon.POSTGRESQL,
        icon_size=7.5,
    ),
    xy=(60.0, 8.0),
)

d.connect(web, run, label="HTTPS", padding=1.5)
d.connect(run, llm, padding=1.5)
d.connect(run, pg, padding=1.5)

d.draw(xy=(6.0, 4.0))
save()
```
