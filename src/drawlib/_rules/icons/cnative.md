# Drawlib Cloud Native Icons Guidelines (`lib-icons-cnative`)

API specification and complete catalog for `drawlib.icons.cnative` (`CnativeIcon`, **73** official CNCF project logos and Kubernetes `k8s_*` resource icons) and `drawlib.icons.original_cnative` (`OriginalCnativeIcon`, **73** matching flat 2D pastel icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Both `cnative` and `original_cnative` share the exact same **73 canonical function names** (**53** CNCF/container ecosystem brands + **20** `k8s_*` Kubernetes resource icons). Every function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import CnativeIcon, Node, OriginalCnativeIcon
from drawlib.icons import cnative, cnative_icon, original_cnative, original_cnative_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
cnative.kubernetes((30, 25), width=9.0, style=Styles.Primary)
original_cnative.kubernetes((55, 25), width=9.0, style=Styles.Primary)
cnative.k8s_pod((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
cnative_icon((30, 10), width=9.0, name="istio", style=Styles.Primary)
original_cnative_icon((55, 10), width=9.0, name="k8s_deployment", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
ing_node = Node("Istio Ingress", width=24, height=18, icon=CnativeIcon.ISTIO, icon_size=7.5)
pod_node = Node("Worker Pod", width=24, height=18, icon=OriginalCnativeIcon.K8S_POD, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.cnative` | `CnativeIcon` | **73** (`53` + `20` `k8s_*`) | `icon_cnative` | Official CNCF project logos and standard blue Kubernetes `k8s_*` resource icons. |
| `drawlib.icons.original_cnative` | `OriginalCnativeIcon` | **73** (`53` + `20` `k8s_*`) | `icon_original_cnative` | Cohesive flat 2D pastel twins for all 53 CNCF projects and 20 `k8s_*` resource icons. |

---

## 2. Complete 53 CNCF & Container Project Icons (`cnative.*` & `original_cnative.*`)

| Category | Count | Canonical Function Names (`cnative.*` & `original_cnative.*`) |
| :--- | :---: | :--- |
| **Kubernetes Distributions, Runtimes & Cluster Management** | 14 | `containerd`, `docker`, `k0s`, `k3s`, `kind`, `kubernetes`, `microk8s`, `minikube`, `okd`, `openshift`, `rancher`, `talos`, `tanzu`, `vcluster` |
| **GitOps, Packaging, Autoscaling & Platform Engineering** | 11 | `argo`, `backstage`, `crossplane`, `flux`, `helm`, `karpenter`, `keda`, `knative`, `kubevirt`, `kustomize`, `temporal` |
| **Service Mesh, CNI Networking & Edge Proxies** | 7 | `calico`, `cilium`, `coredns`, `envoy`, `istio`, `linkerd`, `metallb` |
| **Cloud Native Storage, Databases & Messaging Operators** | 8 | `ceph`, `cloudnative_pg`, `etcd`, `longhorn`, `rook`, `strimzi`, `velero`, `vitess` |
| **Observability, Security, Identity & Policy Engines** | 13 | `cert_manager`, `dapr`, `external_secrets`, `falco`, `fluentd`, `grafana`, `harbor`, `jaeger`, `kyverno`, `opa`, `opentelemetry`, `prometheus`, `spiffe` |

---

## 3. Complete 20 Kubernetes Resource Icons (`k8s_*` in Both Modules)

| Canonical Function (`cnative.*` & `original_cnative.*`) | `CnativeIcon` / `OriginalCnativeIcon` Enum | Kubernetes Resource Kind & Role |
| :--- | :--- | :--- |
| `k8s_api_server` | `K8S_API_SERVER` | `kube-apiserver` control plane gateway |
| `k8s_configmap` | `K8S_CONFIGMAP` | `ConfigMap` non-confidential configuration data |
| `k8s_control_plane` | `K8S_CONTROL_PLANE` | Kubernetes control plane (`scheduler`, `controller-manager`) |
| `k8s_crd` | `K8S_CRD` | `CustomResourceDefinition` operator API extension |
| `k8s_cronjob` | `K8S_CRONJOB` | `CronJob` time-scheduled batch workload |
| `k8s_daemonset` | `K8S_DAEMONSET` | `DaemonSet` node-level background agent |
| `k8s_deployment` | `K8S_DEPLOYMENT` | `Deployment` stateless replica controller |
| `k8s_endpoint` | `K8S_ENDPOINT` | `Endpoints` / `EndpointSlice` network target IP list |
| `k8s_hpa` | `K8S_HPA` | `HorizontalPodAutoscaler` dynamic replica scaling |
| `k8s_ingress` | `K8S_INGRESS` | `Ingress` L7 HTTP/HTTPS routing rules |
| `k8s_job` | `K8S_JOB` | `Job` run-to-completion batch task |
| `k8s_namespace` | `K8S_NAMESPACE` | `Namespace` virtual cluster boundary |
| `k8s_network_policy` | `K8S_NETWORK_POLICY` | `NetworkPolicy` L3/L4 pod firewall rules |
| `k8s_node` | `K8S_NODE` | `Node` worker VM or bare-metal kubelet host |
| `k8s_pod` | `K8S_POD` | `Pod` atomic co-located container group |
| `k8s_pv` | `K8S_PV` | `PersistentVolume` cluster storage volume |
| `k8s_pvc` | `K8S_PVC` | `PersistentVolumeClaim` pod storage mount request |
| `k8s_secret` | `K8S_SECRET` | `Secret` encrypted credentials, TLS keys, and tokens |
| `k8s_service` | `K8S_SERVICE` | `Service` stable ClusterIP / LoadBalancer virtual IP |
| `k8s_statefulset` | `K8S_STATEFULSET` | `StatefulSet` ordered stateful workload controller |

```drawlib code=fold align=center file=icons_cnative_rules_arch.png caption="GitOps & Kubernetes Namespace Topology Using CnativeIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, CnativeIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

argo = d.add(
    Node("Argo CD\nGitOps", width=24, height=18, icon=CnativeIcon.ARGO, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
ns = d.add(NodeGroup(title="Production K8s Namespace", padding=4.5), xy=(42, 4))
svc = ns.add(Node("K8s Service\n(ClusterIP)", width=24, height=18, icon=CnativeIcon.K8S_SERVICE, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
pod = ns.add(Node("App Pod\nReplica", width=24, height=18, icon=CnativeIcon.K8S_POD, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(argo, svc, label="Sync", padding=1.5)
d.connect(svc, pod, label="gRPC", padding=1.5)
d.draw(xy=(4, 4))
save()
```
