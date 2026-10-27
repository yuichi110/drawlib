# Drawlib GCP Icons Guidelines (`lib-icons-gcp`)

API specification and complete service catalog for `drawlib.icons.gcp` (`GcpIcon`, `gcp_icon`). See `lib-icons-overview` for cross-tier icon rules and `lib-diagrams-architecture` for `ArchitectureDiagram`.

---

## 1. Overview & API Signatures

`drawlib.icons.gcp` provides **206 official Google Cloud service icons** (`237` total functions including **31 convenience aliases**) rendered from normalized `512×512` RGBA PNG assets (`icon_gcp` archive).

```python
from drawlib.diagrams.architecture import GcpIcon, Node, NodeGroup
from drawlib.icons import gcp, gcp_icon
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
def gcp_icon(
    xy: tuple[float, float],
    width: float,
    name: str | GcpIcon,
    *,
    style: Style,
    variant: str = "default",
) -> None: ...
```
- **Center Anchor**: `xy=(cx, cy)` is the geometric center; `width` sets the `1:1` square size in canvas units.
- **Required `*, style: Style`**: Always pass `style=Styles.Primary` (or a patched `Style` with `image_tint_color` / `image_border_*`, `alpha`, `angle`).
- **Diagram Enum (`GcpIcon`)**: Pass `icon=GcpIcon.<NAME>` to `ArchitectureDiagram` `Node` or `SequenceDiagram` `add_participant()`.

```drawlib code=fold align=center file=icons_gcp_rules_showcase.png caption="Google Cloud Architecture Using ArchitectureDiagram and GcpIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=140, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

lb = d.add(
    Node("Cloud Armor\n& Load Balancing", width=26, height=18, icon=GcpIcon.CLOUD_ARMOR, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
vpc = d.add(
    NodeGroup(title="Serverless & Data VPC", padding=4.5),
    xy=(44, 4),
)
run = vpc.add(Node("Cloud Run", width=24, height=18, icon=GcpIcon.CLOUD_RUN, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
bq = vpc.add(Node("BigQuery", width=24, height=18, icon=GcpIcon.BIGQUERY, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(lb, run, label="HTTPS", padding=1.5)
d.connect(run, bq, label="Stream", padding=1.5)
d.draw(xy=(4, 4))
save()
```

---

## 2. Convenience Short Aliases (31 Aliases)

For frequently used GCP services, `drawlib.icons.gcp` and `GcpIcon` provide concise aliases alongside the canonical function names:

| Short Alias (`gcp.*` / `GcpIcon.*`) | Canonical Target | Short Alias (`gcp.*` / `GcpIcon.*`) | Canonical Target |
| :--- | :--- | :--- | :--- |
| **`gce`** (`GCE`) | `compute_engine` | **`gar`** (`GAR`) | `artifact_registry` |
| **`gke`** (`GKE`) | `google_kubernetes_engine` | **`gcr`** (`GCR`) | `container_registry` |
| **`gcs`** (`GCS`) | `cloud_storage` | **`cdn`** (`CDN`) | `cloud_cdn` |
| **` vpc`** (`VPC`) | `virtual_private_cloud` | **`dns`** (`DNS`) | `cloud_dns` |
| **`iam`** (`IAM`) | `identity_and_access_management` | **`nat`** (`NAT`) | `cloud_nat` |
| **`kms`** (`KMS`) | `key_management_service` | **`armor`** (`ARMOR`) | `cloud_armor` |
| **`iap`** (`IAP`) | `identity_aware_proxy` | **`lb`** (`LB`) | `cloud_load_balancing` |
| **`scc`** (`SCC`) | `security_command_center` | **` vpn`** (`VPN`) | `cloud_vpn` |
| **`dlp`** (`DLP`) | `data_loss_prevention_api` | **` logging`** (`LOGGING`) | `cloud_logging` |
| **`bq`** (`BQ`) | `bigquery` | **`monitoring`** (`MONITORING`) | `cloud_monitoring` |
| **`bt`** (`BT`) | `bigtable` | **`trace`** (`TRACE`) | `cloud_trace` |
| **`spanner`** (`SPANNER`) | `cloud_spanner` | **`tasks`** (`TASKS`) | `cloud_tasks` |
| **`sql`** (`SQL`) | `cloud_sql` | **`scheduler`** (`SCHEDULER`) | `cloud_scheduler` |
| **`run`** (`RUN`) | `cloud_run` | **`endpoints`** (`ENDPOINTS`) | `cloud_endpoints` |
| **`functions`** (`FUNCTIONS`) | `cloud_functions` | **`interconnect`** (`INTERCONNECT`) | `cloud_interconnect` |
| **`build`** (`BUILD`) | `cloud_build` | | |

---

## 3. Complete Canonical GCP Icons Reference (206 Services)

Every name below is available as `gcp.<name>(xy, width, style=...)` and `GcpIcon.<NAME>`:

| Domain Category | Count | Canonical Function Names (`gcp.*` / `GcpIcon.*`) |
| :--- | :---: | :--- |
| **Compute, Containers & Serverless** | 21 | `anthos`, `anthos_config_management`, `anthos_service_mesh`, `app_engine`, `bare_metal_solutions`, `batch`, `cloud_functions`, `cloud_gpu`, `cloud_run`, `cloud_Run_for_anthos`, `compute_engine`, `container_optimized_os`, ` fleet_engine`, `gke_on_prem`, `google_kubernetes_engine`, `kuberun`, `migrate_for_anthos`, `migrate_for_compute_engine`, `sole_tenant_nodes`, `tekton`, `vmware_engine` |
| **Storage, Databases & Caching** | 16 | `alloyd_b` / `alloydb` *(use `cloud_sql`, `cloud_spanner`, `bigtable`, `firestore`, `memorystore`)*, `bigtable`, `cloud_generic`, `cloud_hsm`, `cloud_spanner`, `cloud_sql`, `cloud_storage`, `database_migration_service`, `datastore`, `filestore`, `firestore`, `local_ssd`, `memorystore`, `persistent_disk`, `storage_transfer_service`, `transfer_appliance` |
| **Data Analytics, BI & Streaming** | 19 | `analytics_hub`, `bigquery`, `cloud_composer`, `cloud_data_fusion`, `cloud_inference_api`, `data_catalog`, `data_labeling`, `data_layers`, `data_qna`, `data_studio`, `data_transfer`, `dataflow`, `datalab`, `dataplex`, `dataprep`, `dataproc`, `dataproc_metastore`, `datastream`, `looker`, `pub_sub`, `stream_suite` |
| **AI & Machine Learning** | 34 | `advanced_agent_modeling`, `Advanced_solutions_lab`, `agent_assist`, `ai_hub`, `ai_platform`, `ai_platform_unified`, `automl`, `automl_natural_language`, `automl_tables`, `automl_translation`, `automl_video_intelligence`, `automl_vision`, `cloud_natural_language_api`, `cloud_tp_us`, `cloud_translation_api`, `cloud_vision_api`, `contact_center_ai`, `dialogflow`, `dialogflow_cx`, `dialogflow_insights`, `document_ai`, `media_translation_api`, `recommendations_ai`, `retail_api`, `speech_to_text`, `talent_solution`, `tensorflow_enterprise`, `text_to_speech`, `user_preferences`, `vertex_ai`, `video_intelligence_api`, `visual_inspection` |
| **Networking, Edge & Service Mesh** | 25 | `apigee_api_platform`, `apigee_sense`, `cloud_armor`, `cloud_cdn`, `cloud_different_interconnect` / `cloud_interconnect`, `cloud_dns`, `cloud_domains`, `cloud_endpoints`, `cloud_external_ip_addresses`, `cloud_firewall_rules`, `cloud_for_marketing`, `cloud_ids`, `cloud_load_balancing`, `cloud_media_edge`, `cloud_nat`, `cloud_network`, `cloud_router`, `cloud_routes`, `cloud_vpn`, `network_connectivity_center`, `network_intelligence_center`, `network_security`, `network_service_tiers`, `network_tiers`, `network_topology`, `partner_interconnect`, `premium_network_tier`, `standard_network_tier`, `traffic_director`, `virtual_private_cloud` |
| **Security, Identity & Compliance** | 21 | `access_context_manager`, `assured_workloads`, `beyondcorp`, `binary_authorization`, `certificate_authority_service`, `certificate_manager`, `chronicle`, `cloud_asset_inventory`, `cloud_audit_logs`, `cloud_ekm`, `cloud_iam`, `cloud_security_scanner`, `confidential_computing`, `data_loss_prevention_api`, `identity_and_access_management`, `identity_aware_proxy`, `identity_platform`, `key_access_justifications`, `key_management_service`, `managed_service_for_microsoft_active_directory`, `org_policy_service`, `permissions`, `phishing_protection`, `policy_analyzer`, `quotas`, `recaptcha_enterprise`, `risk_manager`, `secret_manager`, `security_command_center`, `security_health_advisor`, `security_key_enforcement`, `web_risk`, `web_security_scanner` |
| **CI/CD, Operations & DevTools** | 27 | `artifact_registry`, `cloud_apis`, `cloud_build`, `cloud_code`, `cloud_deploy`, `cloud_deployment_manager`, `cloud_debugger`, `cloud_error_reporting`, `cloud_healthcare_api`, `cloud_ healthcare_marketplace`, `cloud_iot_core`, `cloud_jobs_api`, `cloud_logging`, `cloud_monitoring`, `cloud_ops`, `cloud_optimizing`, `cloud_profiler`, `cloud_scheduler`, `cloud_shell`, `cloud_source_repositories`, `cloud_tasks`, `cloud_test_lab`, `cloud_trace`, `configuration_management`, `connectors`, `container_registry`, `debugger`, `developer_portal`, `early_access_center`, `error_reporting`, `eventarc`, `firebase`, `free_trial`, `gcloud`, `google_cloud_marketplace`, `ide_plugins`, `iot_core`, `iot_edge`, `kustomize`, `launch_stage`, `onboarding`, `os_config_management`, `os_inventory_management`, `os_patch_management`, `partner_portal`, `private_service_connect`, `producer_portal`, `profiler`, `project`, `quantum_engine`, `release_notes`, ` runtime_config`, `service_catalog`, `service_discovery`, `service_mesh`, `stackdriver`, `support`, `tools_for_powershell`, `trace`, `workflows`, `workload_identity_pool` |
