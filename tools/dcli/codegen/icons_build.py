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
        "apigw": "api_gateway",
        "audit": "audit_compliance",
        "auth": "identity_auth",
        "backup": "backup_archive",
        "batch": "batch_job",
        "bi": "bi_dashboard",
        "browser": "web_browser",
        "bucket": "object_storage",
        "bus": "service_bus",
        "cache": "in_memory_cache",
        "cluster": "container_cluster",
        "cron": "scheduler",
        "db": "database",
        "ddos": "ddos_protection",
        "desktop": "desktop_app",
        "disk": "block_storage",
        "dwh": "data_warehouse",
        "etl": "etl_pipeline",
        "filestore": "file_storage",
        "function": "serverless_function",
        "graph_db": "graph_database",
        "iam": "identity_auth",
        "iap": "zero_trust_proxy",
        "iot": "iot_device",
        "k8s": "container_cluster",
        "kms": "secret_vault",
        "lb": "load_balancer",
        "mesh": "service_mesh",
        "mobile": "mobile_app",
        "mq": "message_queue",
        "nfs": "file_storage",
        "nosql": "nosql_database",
        "on_prem": "on_premises",
        "pubsub": "pub_sub",
        "queue": "message_queue",
        "rdbms": "database",
        "redis": "in_memory_cache",
        "replica": "db_replica",
        "search": "search_engine",
        "stream": "event_stream",
        "tls": "certificate_tls",
        "tsdb": "time_series_db",
        "users": "user_group",
        "vault": "secret_vault",
        "vector_db": "vector_database",
        "vm": "virtual_machine",
        "vpc": "virtual_network",
        "vpn": "vpn_tunnel",
        "worker": "batch_job",
        "workflow": "workflow_orchestrator",
        "zero_trust": "zero_trust_proxy",
    },
    "original_devops": {
        "alert": "alert_incident",
        "cicd": "cicd_pipeline",
        "config": "config_management",
        "git": "git_repository",
        "iac": "config_management",
        "logs": "logging",
        "metrics": "monitoring",
        "pipeline": "cicd_pipeline",
        "registry": "artifact_registry",
        "repo": "git_repository",
        "tracing": "distributed_tracing",
    },
    "original_ai": {
        "agent": "ai_agent",
        "embedding": "embedding_vector",
        "guardrail": "prompt_guardrail",
        "inference": "inference_endpoint",
        "llm": "llm_model",
        "rag": "rag_knowledge_base",
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
