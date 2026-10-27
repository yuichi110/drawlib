# Drawlib DevOps Icons Guidelines (`lib-icons-devops`)

API specification and complete catalog for `drawlib.icons.devops` (`DevopsIcon`, **58** official CI/CD, IaC, observability, incident management, and DevSecOps brand icons) and `drawlib.icons.original_devops` (`OriginalDevopsIcon`, **78** flat 2D pastel icons: **58** brand twins + **20** vendor-neutral DevOps and SRE concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import DevopsIcon, Node, OriginalDevopsIcon
from drawlib.icons import devops, devops_icon, original_devops, original_devops_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
devops.github_actions((30, 25), width=9.0, style=Styles.Primary)
original_devops.github_actions((55, 25), width=9.0, style=Styles.Primary)
original_devops.cicd_pipeline((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
devops_icon((30, 10), width=9.0, name="terraform", style=Styles.Primary)
original_devops_icon((55, 10), width=9.0, name="monitoring", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
ci_node = Node("GitHub Actions", width=24, height=18, icon=DevopsIcon.GITHUB_ACTIONS, icon_size=7.5)
sre_node = Node("On-Call SRE", width=24, height=18, icon=OriginalDevopsIcon.ON_CALL, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.devops` | `DevopsIcon` | **58** | `icon_devops` | Official logos for Git/CI/CD platforms, IaC tools, APM/logging backends, incident paging, and security scanners. |
| `drawlib.icons.original_devops` | `OriginalDevopsIcon` | **78** (`58` + `20`) | `icon_original_devops` | Flat 2D pastel twins for all 58 brands plus **20 vendor-neutral CI/CD & SRE concept icons**. |

---

## 2. Complete 58 Shared Brand Icons (`devops.*` & `original_devops.*`)

| Category | Count | Canonical Function Names (`devops.*` & `original_devops.*`) |
| :--- | :---: | :--- |
| **Source Control, CI/CD Pipelines & Build Systems** | 14 | `bazel`, `bitbucket`, `buildkite`, `circleci`, `dagger`, `git`, `github`, `github_actions`, `gitlab`, `jenkins`, `nx`, `spinnaker`, `tekton`, `turborepo` |
| **Infrastructure as Code (IaC), Configuration & Containers** | 9 | `ansible`, `consul`, `opentofu`, `packer`, `podman`, `pulumi`, `terraform`, `vagrant`, `vault` |
| **Observability, APM, Logging & Metrics** | 15 | `datadog`, `dynatrace`, `fluent_bit`, `honeycomb`, `kibana`, `loki`, `mimir`, `new_relic`, `sentry`, `signoz`, `splunk`, `tempo`, `thanos`, `vector`, `victoria_metrics` |
| **Incident Management, Feature Flags & ChatOps** | 7 | `incident_io`, `jira`, `launchdarkly`, `opsgenie`, `pagerduty`, `slack`, `unleash` |
| **Testing, API Clients, Artifact Registries & DevSecOps** | 13 | `bruno`, `cypress`, `insomnia`, `jfrog`, `k6`, `keycloak`, `nexus`, `playwright`, `postman`, `selenium`, `snyk`, `sonarqube`, `trivy` |

---

## 3. Complete 20 Vendor-Neutral DevOps & SRE Concept Icons (`original_devops.*` Only)

| Canonical Function (`original_devops.*`) | `OriginalDevopsIcon` Enum | Architectural Role |
| :--- | :--- | :--- |
| `alert_incident` | `ALERT_INCIDENT` | Critical threshold breach or active production incident alert |
| `artifact_registry` | `ARTIFACT_REGISTRY` | Container image, Helm chart, or binary package repository |
| `build_runner` | `BUILD_RUNNER` | Ephemeral CI compilation worker or build agent |
| `cicd_pipeline` | `CICD_PIPELINE` | Automated continuous integration and delivery workflow |
| `config_management` | `CONFIG_MANAGEMENT` | Declarative infrastructure state and host configuration |
| `container` | `CONTAINER` | Standardized OCI application container image/instance |
| `container_cluster` | `CONTAINER_CLUSTER` | Orchestrated multi-node container cluster |
| `dashboard` | `DASHBOARD` | Real-time SLI/SLO operational metrics visualization |
| `distributed_tracing` | `DISTRIBUTED_TRACING` | End-to-end microservice request span & latency trace |
| `feature_flag` | `FEATURE_FLAG` | Runtime progressive delivery toggle & canary release gate |
| `git_repository` | `GIT_REPOSITORY` | Version-controlled source code and IaC repository |
| `gitops_controller` | `GITOPS_CONTROLLER` | Continuous reconciliation loop syncing Git state to clusters |
| `logging` | `LOGGING` | Centralized structured log ingestion and indexing |
| `monitoring` | `MONITORING` | Time-series metric collection, health checks, and probing |
| `on_call` | `ON_CALL` | SRE incident response rotation and paging escalation |
| `package_dependency` | `PACKAGE_DEPENDENCY` | Software Bill of Materials (SBOM) & library dependency tree |
| `pull_request` | `PULL_REQUEST` | Code review, branch merge gate, and automated status checks |
| `secret_vault` | `SECRET_VAULT` | Encrypted secrets manager, KMS key store, and token broker |
| `security_scan` | `SECURITY_SCAN` | SAST/DAST vulnerability & container image scanning stage |
| `test_automation` | `TEST_AUTOMATION` | Automated unit, integration, and E2E regression test suite |

```drawlib code=fold align=center file=icons_devops_rules_arch.png caption="DevSecOps CI/CD & Observability Pipeline Using DevopsIcon and OriginalDevopsIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    DevopsIcon,
    Node,
    NodeGroup,
    OriginalDevopsIcon,
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

gh = d.add(
    Node("GitHub\nRepository", width=24, height=18, icon=DevopsIcon.GITHUB, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
pipe = d.add(NodeGroup(title="DevSecOps & SRE Platform", padding=4.5), xy=(42, 4))
ci = pipe.add(Node("GitHub\nActions CI", width=24, height=18, icon=DevopsIcon.GITHUB_ACTIONS, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
scan = pipe.add(Node("Security\nImage Scan", width=24, height=18, icon=OriginalDevopsIcon.SECURITY_SCAN, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(gh, ci, label="PR Push", padding=1.5)
d.connect(ci, scan, label="SBOM", padding=1.5)
d.draw(xy=(4, 4))
save()
```
