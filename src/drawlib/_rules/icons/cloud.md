# Drawlib Cloud Icons Guidelines (`lib-icons-cloud`)

API specification and complete catalog for `drawlib.icons.cloud` (`CloudIcon`, **45** official hyperscaler, CDN, VPS, and PaaS brand icons) and `drawlib.icons.original_cloud` (`OriginalCloudIcon`, **147** flat 2D pastel icons: **45** brand twins + **102** vendor-neutral cloud taxonomy icons). See `lib-icons-overview` for cross-tier icon rules, or `lib-icons-gcp`, `lib-icons-aws`, and `lib-icons-azure` for provider-specific service catalogs.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import CloudIcon, Node, OriginalCloudIcon
from drawlib.icons import cloud, cloud_icon, original_cloud, original_cloud_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
cloud.cloudflare((30, 25), width=9.0, style=Styles.Primary)
original_cloud.cloudflare((55, 25), width=9.0, style=Styles.Primary)
original_cloud.load_balancer((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
cloud_icon((30, 10), width=9.0, name="vercel", style=Styles.Primary)
original_cloud_icon((55, 10), width=9.0, name="serverless_function", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
cdn_node = Node("Cloudflare CDN", width=24, height=18, icon=CloudIcon.CLOUDFLARE, icon_size=7.5)
lb_node = Node("Load Balancer", width=24, height=18, icon=OriginalCloudIcon.LOAD_BALANCER, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.cloud` | `CloudIcon` | **45** | `icon_cloud` | Official provider logos for hyperscalers, edge CDNs, modern PaaS/BaaS, and regional cloud hosts. |
| `drawlib.icons.original_cloud` | `OriginalCloudIcon` | **147** (`45` + `102`) | `icon_original_cloud` | Flat 2D pastel twins for all 45 providers plus **102 vendor-neutral cloud architecture taxonomy icons**. |

---

## 2. Complete 45 Shared Cloud Provider Brand Icons (`cloud.*` & `original_cloud.*`)

| Brand Category | Count | Canonical Function Names (`cloud.*` & `original_cloud.*`) |
| :--- | :---: | :--- |
| **Hyperscale Cloud Providers & Parent Companies** | 16 | `alibaba`, `alibaba_cloud`, `amazon`, `aws`, `azure`, `google`, `google_cloud`, `huawei`, `huawei_cloud`, `ibm`, `ibm_cloud`, `microsoft`, `oracle`, `oracle_cloud`, `tencent`, `tencent_cloud` |
| **Global VPS, Bare-Metal, Edge & Object Storage** | 12 | `akamai`, `backblaze`, `cloudflare`, `digitalocean`, `fastly`, `hetzner`, `ionos`, `linode`, `ovhcloud`, `scaleway`, `vultr`, `wasabi` |
| **Modern PaaS, Serverless & BaaS Platforms** | 11 | `coolify`, `deno_deploy`, `firebase`, `fly_io`, `heroku`, `netlify`, `railway`, `render`, `supabase`, `upstash`, `vercel` |
| **Japan Cloud & Hosting Providers** | 6 | `conoha`, `idcf`, `kagoya`, `nifcloud`, `sakura`, `xserver` |

---

## 3. Complete 102 Vendor-Neutral Cloud Taxonomy Icons (`original_cloud.*` Only)

| Taxonomy Category | Count | Canonical Function Names (`original_cloud.*` / `OriginalCloudIcon.*`) |
| :--- | :---: | :--- |
| **Cloud Topologies, Environments & Accounts** | 8 | `cloud`, `external_saas`, `hybrid_cloud`, `multi_cloud`, `on_premises`, `organization_account`, `private_cloud`, `public_cloud` |
| **Compute, Containers, Serverless & Virtualization** | 16 | `app_service`, `autoscaling`, `bare_metal`, `batch_job`, `compute`, `container`, `container_cluster`, `gpu_cluster`, `gpu_node`, `npu_node`, `serverless_function`, `virtual_desktop`, `virtual_machine`, `virtualization_cluster`, `virtualization_controller`, `virtualization_host` |
| **Storage, Backup & Disaster Recovery** | 6 | `backup_archive`, `block_storage`, `data_migration`, `disaster_recovery`, `file_storage`, `object_storage` |
| **Databases, Caching & Search** | 9 | `database`, `db_replica`, `distributed_database`, `graph_database`, `in_memory_cache`, `nosql_database`, `search_engine`, `time_series_database`, `vector_database` |
| **Networking, Edge, Gateways & Service Mesh** | 19 | `api_gateway`, `bastion_host`, `cdn`, `dedicated_interconnect`, `dns`, `edge_location`, `internet_gateway`, `load_balancer`, `nat_gateway`, `network_peering`, `private_endpoint`, `reverse_proxy`, `router`, `service_discovery`, `service_mesh`, `switch`, `transit_hub`, `virtual_network`, `vpn_tunnel` |
| **Security, Identity, Zero-Trust & Governance** | 14 | `audit_compliance`, `certificate_tls`, `ddos_protection`, `directory_service`, `firewall`, `identity_auth`, `ids_ips`, `key_management`, `secret_vault`, `security_center`, `user`, `user_group`, `waf`, `zero_trust_proxy` |
| **Data Analytics, Streaming, Messaging & AI** | 17 | `ai_agent`, `analytics_engine`, `bi_dashboard`, `blockchain_ledger`, `data_catalog`, `data_lake`, `data_warehouse`, `email_service`, `etl_pipeline`, `event_stream`, `llm_model`, `media_streaming`, `message_queue`, `notification`, `scheduler`, `webhook`, `workflow_orchestrator` |
| **DevOps, Observability, FinOps, IoT & Clients** | 13 | `artifact_registry`, `billing`, `cicd_pipeline`, `cost_management`, `desktop_app`, `digital_twin`, `git_repository`, `iot_device`, `iot_hub`, `logging`, `mobile_app`, `monitoring`, `web_browser` |

```drawlib code=fold align=center file=icons_cloud_rules_arch.png caption="Vendor-Neutral Cloud Core & Edge Ingress Using CloudIcon and OriginalCloudIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    CloudIcon,
    Node,
    NodeGroup,
    OriginalCloudIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

edge = d.add(
    Node("Cloudflare\nEdge CDN", width=24, height=18, icon=CloudIcon.CLOUDFLARE, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
vpc = d.add(NodeGroup(title="Vendor-Neutral Cloud Core", padding=4.5), xy=(42, 4))
gw = vpc.add(Node("API Gateway", width=24, height=18, icon=OriginalCloudIcon.API_GATEWAY, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
db = vpc.add(Node("Distributed\nDatabase", width=24, height=18, icon=OriginalCloudIcon.DISTRIBUTED_DATABASE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(edge, gw, label="HTTPS", padding=1.5)
d.connect(gw, db, label="SQL", padding=1.5)
d.draw(xy=(4, 4))
save()
```
