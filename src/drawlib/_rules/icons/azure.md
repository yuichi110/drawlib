# Drawlib Azure Icons Guidelines (`lib-icons-azure`)

API specification and complete 80-service catalog for `drawlib.icons.azure` (`AzureIcon`, `azure_icon`). See `lib-icons-overview` for cross-tier icon rules and `lib-diagrams-architecture` for `ArchitectureDiagram`.

---

## 1. Overview & API Signatures

`drawlib.icons.azure` provides **80 official Microsoft Azure service icons** rendered from normalized `512×512` RGBA PNG assets (`icon_azure` archive).

```python
from drawlib.diagrams.architecture import AzureIcon, Node, NodeGroup
from drawlib.icons import azure, azure_icon
from drawlib.styles import Styles
from drawlib.types import Style

# 1. Direct function call (center-anchored at (cx, cy); style is required keyword-only)
def <service_name>(
    xy: tuple[float, float],
    width: float,
    *,
    style: Style,
    variant: str = "default",
) -> None: ...

# 2. Dynamic string/Enum dispatcher
def azure_icon(
    xy: tuple[float, float],
    width: float,
    name: str | AzureIcon,
    *,
    style: Style,
    variant: str = "default",
) -> None: ...
```
- **Center Anchor & Required `style`**: Anchored at `xy=(cx, cy)` with `1:1` square aspect ratio; `*, style: Style` is mandatory.
- **Diagram Enum (`AzureIcon`)**: Pass `icon=AzureIcon.<NAME>` to `ArchitectureDiagram` `Node` or `SequenceDiagram` `add_participant()`.

```drawlib code=fold align=center file=icons_azure_rules_showcase.png caption="Microsoft Azure Cloud Native Architecture Using ArchitectureDiagram and AzureIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, AzureIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=140, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

fd = d.add(
    Node("Azure\nFront Door", width=24, height=18, icon=AzureIcon.FRONT_DOOR_AND_CDN_PROFILES, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
vnet = d.add(
    NodeGroup(title="Azure Virtual Network (VNet)", padding=4.5),
    xy=(42, 4),
)
aks = vnet.add(Node("AKS Cluster", width=24, height=18, icon=AzureIcon.KUBERNETES_SERVICES, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
cosmos = vnet.add(Node("Azure\nCosmos DB", width=24, height=18, icon=AzureIcon.COSMOS_DB, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(fd, aks, label="HTTPS", padding=1.5)
d.connect(aks, cosmos, label="NoSQL", padding=1.5)
d.draw(xy=(4, 4))
save()
```

---

## 2. Complete Canonical 80 Azure Icons Reference (`azure.*` & `AzureIcon.*`)

Every service below is callable as `azure.<name>(xy, width, style=...)` and `AzureIcon.<NAME>`:

| Azure Service Category | Count | Canonical Function Names (`azure.*`) | `AzureIcon` Enum Members |
| :--- | :---: | :--- | :--- |
| **1. Compute, Containers & Serverless** | 12 | `app_services`, `batch_accounts`, `container_apps_environments`, `container_instances`, `container_registries`, `function_apps`, `kubernetes_services`, `service_fabric_clusters`, `spring_apps`, `static_apps`, `vm_scale_sets`, `virtual_machine` | `APP_SERVICES`, `BATCH_ACCOUNTS`, `CONTAINER_APPS_ENVIRONMENTS`, `CONTAINER_INSTANCES`, `CONTAINER_REGISTRIES`, `FUNCTION_APPS`, `KUBERNETES_SERVICES`, `SERVICE_FABRIC_CLUSTERS`, `SPRING_APPS`, `STATIC_APPS`, `VM_SCALE_SETS`, `VIRTUAL_MACHINE` |
| **2. Databases, Caching & Storage** | 14 | `archive_storage`, `blob_storage`, `cache_for_redis`, `cosmos_db`, `data_box`, `data_lake_storage`, `database_for_mysql`, `database_for_postgresql`, `files`, `managed_disks`, `netapp_files`, `sql_database`, `sql_managed_instance`, `storage_accounts` | `ARCHIVE_STORAGE`, `BLOB_STORAGE`, `CACHE_FOR_REDIS`, `COSMOS_DB`, `DATA_BOX`, `DATA_LAKE_STORAGE`, `DATABASE_FOR_MYSQL`, `DATABASE_FOR_POSTGRESQL`, `FILES`, `MANAGED_DISKS`, `NETAPP_FILES`, `SQL_DATABASE`, `SQL_MANAGED_INSTANCE`, `STORAGE_ACCOUNTS` |
| **3. Networking, Edge & Hybrid Delivery** | 15 | `application_gateway`, `bastion`, `cdn`, `ddos_protection`, `dns`, `expressroute`, `firewall`, `front_door`, `load_balancer`, `nat_gateway`, `network_security_groups`, `private_link`, `traffic_manager`, `virtual_network`, `virtual_wan`, `vpn_gateway` | `APPLICATION_GATEWAY`, `BASTION`, `CDN`, `DDOS_PROTECTION`, `DNS`, `EXPRESSROUTE`, `FIREWALL`, `FRONT_DOOR`, `LOAD_BALANCER`, `NAT_GATEWAY`, `NETWORK_SECURITY_GROUPS`, `PRIVATE_LINK`, `TRAFFIC_MANAGER`, `VIRTUAL_NETWORK`, `VIRTUAL_WAN`, `VPN_GATEWAY` |
| **4. Integration, Messaging & APIs** | 7 | `api_management`, `data_factory`, `event_grid`, `event_hubs`, `logic_apps`, `notification_hubs`, `relay`, `service_bus`, `signalr_service` | `API_MANAGEMENT`, `DATA_FACTORY`, `EVENT_GRID`, `EVENT_HUBS`, `LOGIC_APPS`, `NOTIFICATION_HUBS`, `RELAY`, `SERVICE_BUS`, `SIGNALR_SERVICE` |
| **5. Data Analytics, BI & IoT** | 9 | `analysis_services`, `data_explorer`, `databricks`, `digital_twins`, `hdinsight`, `iot_central`, `iot_hub`, `power_bi_embedded`, `purview`, `stream_analytics`, `synapse_analytics` | `ANALYSIS_SERVICES`, `DATA_EXPLORER`, `DATABRICKS`, `DIGITAL_TWINS`, `HDINSIGHT`, `IOT_CENTRAL`, `IOT_HUB`, `POWER_BI_EMBEDDED`, `PURVIEW`, `STREAM_ANALYTICS`, `SYNAPSE_ANALYTICS` |
| **6. AI, Machine Learning & Cognitive Services** | 7 | `ai_search`, `ai_Services`, `ai_studio`, `bot_service`, `document_intelligence`, `machine_learning`, `openai`, `speech_services`, `translator`, `vision` | `AI_SEARCH`, `AI_SERVICES`, `AI_STUDIO`, `BOT_SERVICE`, `DOCUMENT_INTELLIGENCE`, `MACHINE_LEARNING`, `OPENAI`, `SPEECH_SERVICES`, `TRANSLATOR`, `VISION` |
| **7. Security, Identity & Governance** | 8 | `active_directory_b2c`, `confidential_ledger`, `defender_for_cloud`, `entra_id`, `information_protection`, `key_vault`, `managed_identities`, `policy`, `sentinel` | `ACTIVE_DIRECTORY_B2C`, `CONFIDENTIAL_LEDGER`, `DEFENDER_FOR_CLOUD`, `ENTRA_ID`, `INFORMATION_PROTECTION`, `KEY_VAULT`, `MANAGED_IDENTITIES`, `POLICY`, `SENTINEL` |
| **8. DevOps, Management & Hybrid Arc** | 8 | `advisor`, `app_configuration`, `application_insights`, `arc`, `automation`, `backup`, `chaos_studio`, `cost_management`, `devops`, `load_testing`, `log_analytics`, `migrate`, `monitor`, `resource_groups`, `site_recovery`, `subscriptions`, `virtual_desktop` | `ADVISOR`, `APP_CONFIGURATION`, `APPLICATION_INSIGHTS`, `ARC`, `AUTOMATION`, `BACKUP`, `CHAOS_STUDIO`, `COST_MANAGEMENT`, `DEVOPS`, `LOAD_TESTING`, `LOG_ANALYTICS`, `MIGRATE`, `MONITOR`, `RESOURCE_GROUPS`, `SITE_RECOVERY`, `SUBSCRIPTIONS`, `VIRTUAL_DESKTOP` |
