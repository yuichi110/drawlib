# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud Native (Kubernetes & CNCF ecosystem) icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

CNATIVE_ALIASES: dict[str, str] = {
    "api_server": "k8s_api_server",
    "apiserver": "k8s_api_server",
    "argo_cd": "argo",
    "argo_rollouts": "argo",
    "argo_workflows": "argo",
    "argocd": "argo",
    "autoscaler": "k8s_hpa",
    "ceph": "rook",
    "cj": "k8s_cronjob",
    "cm": "k8s_configmap",
    "configmap": "k8s_configmap",
    "container_runtime": "containerd",
    "control_plane": "k8s_control_plane",
    "crd": "k8s_crd",
    "cronjob": "k8s_cronjob",
    "custom_resource": "k8s_crd",
    "daemonset": "k8s_daemonset",
    "deploy": "k8s_deployment",
    "deployment": "k8s_deployment",
    "ds": "k8s_daemonset",
    "endpoint": "k8s_endpoint",
    "endpoints": "k8s_endpoint",
    "envoy_proxy": "envoy",
    "ep": "k8s_endpoint",
    "fluent_bit": "fluentd",
    "fluentbit": "fluentd",
    "flux_cd": "flux",
    "fluxcd": "flux",
    "gatekeeper": "opa",
    "hpa": "k8s_hpa",
    "ing": "k8s_ingress",
    "ingress": "k8s_ingress",
    "jaeger_tracing": "jaeger",
    "job": "k8s_job",
    "k8s": "kubernetes",
    "k8s_cj": "k8s_cronjob",
    "k8s_cm": "k8s_configmap",
    "k8s_deploy": "k8s_deployment",
    "k8s_ds": "k8s_daemonset",
    "k8s_ep": "k8s_endpoint",
    "k8s_ing": "k8s_ingress",
    "k8s_master": "k8s_control_plane",
    "k8s_netpol": "k8s_network_policy",
    "k8s_ns": "k8s_namespace",
    "k8s_sts": "k8s_statefulset",
    "k8s_svc": "k8s_service",
    "k8s_worker": "k8s_node",
    "kube": "kubernetes",
    "kube_apiserver": "k8s_api_server",
    "master": "k8s_control_plane",
    "namespace": "k8s_namespace",
    "netpol": "k8s_network_policy",
    "network_policy": "k8s_network_policy",
    "node": "k8s_node",
    "ns": "k8s_namespace",
    "open_policy_agent": "opa",
    "open_telemetry": "opentelemetry",
    "otel": "opentelemetry",
    "persistent_volume": "k8s_pv",
    "persistent_volume_claim": "k8s_pvc",
    "po": "k8s_pod",
    "pod": "k8s_pod",
    "prom": "prometheus",
    "pv": "k8s_pv",
    "pvc": "k8s_pvc",
    "rook_ceph": "rook",
    "secret": "k8s_secret",  # noqa: S105
    "service": "k8s_service",
    "statefulset": "k8s_statefulset",
    "sts": "k8s_statefulset",
    "svc": "k8s_service",
    "worker_node": "k8s_node",
}

CNATIVE_PROVIDER = PngIconProvider(
    name="cnative",
    package_name="icon_cnative",
    asset_subdir="icons/cnative",
    aliases=CNATIVE_ALIASES,
)

_write = CNATIVE_PROVIDER.write
