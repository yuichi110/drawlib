# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Post-build 512x512 PNG normalizer and manifest generator for `tools/icons_src/`."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from drawlib._builder._common import BuildImageCache, hash_file

TARGET_SIZE: int = 512
INNER_SIZE: int = 460


def normalize_png_in_place(
    png_path: Path,
    *,
    target_size: int = TARGET_SIZE,
    inner_size: int = INNER_SIZE,
) -> tuple[tuple[int, int, int, int], bool]:
    """Normalize a rendered transparent PNG into a 512x512 canvas (460x460 inner bbox).

    Returns:
        Tuple of (bbox, was_modified).
    """
    with Image.open(png_path) as raw_img:
        rgba = raw_img.convert("RGBA")
        width, height = rgba.size
        bbox = rgba.getbbox()
        if not bbox:
            return (0, 0, target_size, target_size), False

        bx0, by0, bx1, by1 = bbox
        bw, bh = bx1 - bx0, by1 - by0
        margin = (target_size - inner_size) // 2
        if (
            width == target_size
            and height == target_size
            and max(bw, bh) == inner_size
            and bx0 >= margin - 1
            and by0 >= margin - 1
        ):
            return bbox, False

        cropped = rgba.crop(bbox)

    crop_w, crop_h = cropped.size
    scale = inner_size / max(crop_w, crop_h)
    new_w = max(1, int(round(crop_w * scale)))
    new_h = max(1, int(round(crop_h * scale)))
    resized = cropped.resize((new_w, new_h), Image.Resampling.BOX)

    canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    offset_x = (target_size - new_w) // 2
    offset_y = (target_size - new_h) // 2
    canvas.paste(resized, (offset_x, offset_y))

    canvas.save(png_path, format="PNG", optimize=True)
    final_bbox = canvas.getbbox() or (offset_x, offset_y, offset_x + new_w, offset_y + new_h)
    return final_bbox, True


PROVIDER_ALIASES: dict[str, dict[str, str]] = {
    "gcp": {
        "functions": "cloud_functions",
        "gce": "compute_engine",
        "gcs": "cloud_storage",
        "gke": "google_kubernetes_engine",
        "iam": "identity_and_access_management",
        "kms": "key_management_service",
        "vertexai": "vertex_ai",
        "vpc": "virtual_private_cloud",
        "load_balancing": "cloud_load_balancing",
        "cloud_pubsub": "pubsub",
    },
    "original_cloud": {
        "ad": "directory_service",
        "agent": "ai_agent",
        "apigw": "api_gateway",
        "audit": "audit_compliance",
        "auth": "identity_auth",
        "backup": "backup_archive",
        "bastion": "bastion_host",
        "batch": "batch_job",
        "bi": "bi_dashboard",
        "browser": "web_browser",
        "bucket": "object_storage",
        "cache": "in_memory_cache",
        "cicd": "cicd_pipeline",
        "cluster": "container_cluster",
        "cron": "scheduler",
        "db": "database",
        "ddos": "ddos_protection",
        "desktop": "desktop_app",
        "disk": "block_storage",
        "dr": "disaster_recovery",
        "dwh": "data_warehouse",
        "etl": "etl_pipeline",
        "filestore": "file_storage",
        "function": "serverless_function",
        "git": "git_repository",
        "gpu": "gpu_node",
        "graph_db": "graph_database",
        "iam": "identity_auth",
        "iap": "zero_trust_proxy",
        "ids": "ids_ips",
        "igw": "internet_gateway",
        "iot": "iot_device",
        "ips": "ids_ips",
        "k8s": "container_cluster",
        "kms": "key_management",
        "kubernetes_cluster": "container_cluster",
        "lb": "load_balancer",
        "llm": "llm_model",
        "logs": "logging",
        "mesh": "service_mesh",
        "metrics": "monitoring",
        "mobile": "mobile_app",
        "mq": "message_queue",
        "nat": "nat_gateway",
        "nfs": "file_storage",
        "nosql": "nosql_database",
        "npu": "npu_node",
        "on_prem": "on_premises",
        "peering": "network_peering",
        "pipeline": "cicd_pipeline",
        "queue": "message_queue",
        "rdbms": "database",
        "redis": "in_memory_cache",
        "replica": "db_replica",
        "repo": "git_repository",
        "search": "search_engine",
        "secret_manager": "secret_vault",
        "stream": "event_stream",
        "tls": "certificate_tls",
        "tpu": "npu_node",
        "tsdb": "time_series_database",
        "users": "user_group",
        "vault": "secret_vault",
        "vcenter": "virtualization_controller",
        "vdi": "virtual_desktop",
        "vector_db": "vector_database",
        "vm": "virtual_machine",
        "vnet": "virtual_network",
        "vpc": "virtual_network",
        "vpn": "vpn_tunnel",
        "worker": "batch_job",
        "workflow": "workflow_orchestrator",
        "zero_trust": "zero_trust_proxy",
    },
    "original_devops": {
        "alert": "alert_incident",
        "cicd": "cicd_pipeline",
        "code_review": "pull_request",
        "config": "config_management",
        "feature_toggle": "feature_flag",
        "git": "git_repository",
        "gitops": "gitops_controller",
        "iac": "config_management",
        "incident": "alert_incident",
        "k8s": "container_cluster",
        "kubernetes": "container_cluster",
        "kubernetes_cluster": "container_cluster",
        "logs": "logging",
        "metrics": "monitoring",
        "package": "package_dependency",
        "pager": "on_call",
        "pipeline": "cicd_pipeline",
        "pr": "pull_request",
        "qa": "test_automation",
        "registry": "artifact_registry",
        "repo": "git_repository",
        "runner": "build_runner",
        "sbom": "package_dependency",
        "secret": "secret_vault",
        "secret_manager": "secret_vault",
        "testing": "test_automation",
        "tracing": "distributed_tracing",
        "vault": "secret_vault",
        "vulnerability_scan": "security_scan",
    },
    "original_ai": {
        "agent": "ai_agent",
        "agent_swarm": "multi_agent",
        "benchmark": "evaluation",
        "embedding": "embedding_vector",
        "eval": "evaluation",
        "gpu": "gpu_node",
        "guardrail": "prompt_guardrail",
        "inference": "inference_endpoint",
        "jupyter": "notebook",
        "llm": "llm_model",
        "lora": "fine_tuning",
        "mcp": "function_calling",
        "memory": "agent_memory",
        "npu": "npu_node",
        "prompt": "prompt_template",
        "rag": "rag_knowledge_base",
        "tool_use": "function_calling",
        "tpu": "npu_node",
        "training": "training_pipeline",
        "training_data": "dataset",
        "vector_db": "vector_database",
    },
    "original_network": {
        "aaa_server": "nac_server",
        "access_point": "wireless_ap",
        "access_switch": "l2_switch",
        "adc": "load_balancer",
        "ap": "wireless_ap",
        "branch_router": "router",
        "call_manager": "voice_gateway",
        "carrier_cloud": "wan_cloud",
        "carrier_router": "core_router",
        "chassis_router": "core_router",
        "chassis_switch": "core_switch",
        "desktop_pc": "client_pc",
        "dwdm": "optical_transport",
        "edge_router": "wan_router",
        "fabric_switch": "datacenter_switch",
        "fiber_switch": "optical_transport",
        "ids": "ids_ips",
        "internet_cloud": "wan_cloud",
        "intrusion_prevention": "ids_ips",
        "ips": "ids_ips",
        "ise": "nac_server",
        "isr_router": "router",
        "mpls_cloud": "wan_cloud",
        "multilayer_switch": "l3_switch",
        "network_firewall": "firewall",
        "network_server": "server",
        "ngfw": "firewall",
        "pbx": "voice_gateway",
        "proxy_appliance": "web_security",
        "rack_server": "server",
        "radius_server": "nac_server",
        "roadm": "optical_transport",
        "sd_wan": "wan_router",
        "secure_web_gateway": "web_security",
        "sip_gateway": "voice_gateway",
        "spine_leaf_switch": "datacenter_switch",
        "swg": "web_security",
        "switch": "l2_switch",
        "traffic_manager": "load_balancer",
        "voip_phone": "ip_phone",
        "vpn": "vpn_gateway",
        "vpn_concentrator": "vpn_gateway",
        "wifi_ap": "wireless_ap",
        "wifi_router": "wireless_router",
        "wlan_controller": "wireless_controller",
        "wlc": "wireless_controller",
        "workgroup_switch": "l2_switch",
        "workstation": "client_pc",
    },
    "aws": {
        "acm": "certificate_manager",
        "alb": "elastic_load_balancing",
        "apigw": "api_gateway",
        "cdk": "cloud_development_kit",
        "cli": "command_line_interface",
        "cloudwatch_logs": "cloudwatch",
        "cognito_id": "cognito",
        "dms": "database_migration_service",
        "ebs": "elastic_block_store",
        "ecr": "elastic_container_registry",
        "ecs": "elastic_container_service",
        "eks": "elastic_kubernetes_service",
        "elastic_file_system": "efs",
        "elb": "elastic_load_balancing",
        "eventbridge_bus": "eventbridge",
        "flink": "managed_service_for_apache_flink",
        "iam": "identity_and_access_management",
        "kms": "key_management_service",
        "lambda_function": "aws_lambda",
        "msk": "managed_streaming_for_apache_kafka",
        "nlb": "elastic_load_balancing",
        "opensearch": "opensearch_service",
        "prometheus": "managed_service_for_prometheus",
        "ram": "resource_access_manager",
        "route53": "route_53",
        "s3": "simple_storage_service",
        "s3_glacier": "simple_storage_service_glacier",
        "ses": "simple_email_service",
        "sns": "simple_notification_service",
        "sqs": "simple_queue_service",
        "step_functions_workflow": "step_functions",
        "vpc": "virtual_private_cloud",
    },
    "azure": {
        "aad": "entra_id",
        "aca": "worker_container_app",
        "aci": "container_instances",
        "acr": "container_registries",
        "active_directory": "entra_id",
        "adf": "data_factories",
        "ai_search": "cognitive_search",
        "aks": "kubernetes_services",
        "api_management": "api_management_services",
        "apim": "api_management_services",
        "app_insights": "application_insights",
        "appgw": "application_gateways",
        "application_gateway": "application_gateways",
        "avd": "virtual_desktop",
        "azure_files": "storage_azure_files",
        "bastion": "bastions",
        "blob_storage": "storage_container",
        "cdn": "front_door_and_cdn_profiles",
        "container_apps": "worker_container_app",
        "data_factory": "data_factories",
        "event_grid": "event_grid_topics",
        "expressroute": "expressroute_circuits",
        "front_door": "front_door_and_cdn_profiles",
        "functions": "function_apps",
        "key_vault": "key_vaults",
        "kv": "key_vaults",
        "lb": "load_balancers",
        "log_analytics": "log_analytics_workspaces",
        "nat_gateway": "nat",
        "redis": "cache_redis",
        "synapse": "synapse_analytics",
        "virtual_machines": "virtual_machine",
        "vm": "virtual_machine",
        "vmss": "vm_scale_sets",
        "vnet": "virtual_networks",
        "waf": "web_application_firewall_policies_waf",
    },
    "network": {
        "cisco_aaa_server": "cisco_ise",
        "cisco_access_switch": "cisco_l2_switch",
        "cisco_ap": "cisco_wireless_ap",
        "cisco_asa": "cisco_firewall",
        "cisco_carrier_router": "cisco_core_router",
        "cisco_chassis_router": "cisco_core_router",
        "cisco_chassis_switch": "cisco_core_switch",
        "cisco_content_switch": "cisco_load_balancer",
        "cisco_cucm": "cisco_voice_gateway",
        "cisco_datacenter_switch": "cisco_nexus_switch",
        "cisco_dwdm": "cisco_optical_transport",
        "cisco_edge_router": "cisco_wan_router",
        "cisco_firepower": "cisco_firewall",
        "cisco_internet_cloud": "cisco_wan_cloud",
        "cisco_ips": "cisco_ids_ips",
        "cisco_isr_router": "cisco_router",
        "cisco_mpls_cloud": "cisco_wan_cloud",
        "cisco_multilayer_switch": "cisco_l3_switch",
        "cisco_nac": "cisco_ise",
        "cisco_roadm": "cisco_optical_transport",
        "cisco_sd_wan": "cisco_wan_router",
        "cisco_ucs_server": "cisco_server",
        "cisco_umbrella": "cisco_web_security",
        "cisco_voip_phone": "cisco_ip_phone",
        "cisco_vpn_concentrator": "cisco_vpn_gateway",
        "cisco_wifi_ap": "cisco_wireless_ap",
        "cisco_wlc": "cisco_wireless_controller",
        "cisco_workgroup_switch": "cisco_l2_switch",
        "cisco_workstation": "cisco_client_pc",
        "cisco_wsa": "cisco_web_security",
    },
}


def write_provider_manifest(
    provider: str,
    src_subdir: Path,
    dest_subdir: Path,
) -> Path:
    """Write `manifest.json` for normalized PNGs corresponding to `src_subdir/*.py`."""
    py_stems = sorted(p.stem for p in src_subdir.glob("*.py") if not p.name.startswith("_"))
    files_meta: dict[str, Any] = {}

    for stem in py_stems:
        png_path = dest_subdir / f"{stem}.png"
        if not png_path.is_file():
            continue
        bbox, _ = normalize_png_in_place(png_path)
        raw_bytes = png_path.read_bytes()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        icon_name, variant = stem.rsplit("_", 1) if "_" in stem else (stem, "default")
        files_meta[f"{stem}.png"] = {
            "icon_name": icon_name,
            "variant": variant,
            "source_script": f"{provider}/{stem}.py",
            "size_bytes": len(raw_bytes),
            "sha256": sha256,
            "bbox": list(bbox),
        }

    manifest: dict[str, Any] = {
        "format_version": "2.0",
        "provider": provider,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "canvas_size": [TARGET_SIZE, TARGET_SIZE],
        "inner_size": [INNER_SIZE, INNER_SIZE],
        "total_files": len(files_meta),
        "aliases": PROVIDER_ALIASES.get(provider, {}),
        "files": files_meta,
    }
    manifest_path = dest_subdir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path


def postprocess_icons_build(
    icons_src_dir: Path,
    icons_out_dir: Path,
) -> None:
    """Normalize rendered icon PNGs in `icons_out_dir` to 512x512 and update BuildImageCache."""
    s_hash = hash_file(str(icons_src_dir / "styles.py"))
    u_hash = hash_file(str(icons_src_dir / "utils.py"))
    config_hash = f"{s_hash}:{u_hash}"
    cache = BuildImageCache(enabled=True)

    for provider_src in sorted(p for p in icons_src_dir.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        provider = provider_src.name
        provider_out = icons_out_dir / provider
        if not provider_out.is_dir():
            continue

        py_files = sorted(p for p in provider_src.glob("*.py") if not p.name.startswith("_"))
        mod_count = 0
        for py_path in py_files:
            stem = py_path.stem
            png_path = provider_out / f"{stem}.png"
            if not png_path.is_file():
                continue

            _, modified = normalize_png_in_place(png_path)
            if modified:
                mod_count += 1

            # Ensure BuildImageCache stores the 512x512 normalized PNG bytes
            code = py_path.read_text(encoding="utf-8")
            cache_key, code_hash = cache.compute_keys(
                code=code,
                config_hash=config_hash,
                context_dir=str(py_path.parent.resolve()),
                project_root=str(icons_src_dir.resolve()),
                source_file=str(py_path.resolve()),
                target_file=str(png_path.resolve()),
            )
            cache.put(
                cache_key=cache_key,
                code_hash=code_hash,
                config_hash=config_hash,
                image_format="png",
                image_blob=png_path.read_bytes(),
                grid_blob=None,
            )

        manifest_path = write_provider_manifest(provider, provider_src, provider_out)
        print(f"[{provider}] Normalized {len(py_files)} icons ({mod_count} updated) -> {manifest_path}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[3]
    postprocess_icons_build(
        icons_src_dir=repo_root / "tools" / "icons_src",
        icons_out_dir=repo_root / "tools" / "release_assets" / "v0.3" / "icons",
    )
