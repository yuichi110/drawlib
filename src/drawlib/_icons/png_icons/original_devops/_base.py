# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original DevOps icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_DEVOPS_ALIASES: dict[str, str] = {
    "actions": "github_actions",
    "alert": "alert_incident",
    "artifactory": "jfrog",
    "bb": "bitbucket",
    "cicd": "cicd_pipeline",
    "circle": "circleci",
    "code_review": "pull_request",
    "config": "config_management",
    "dd": "datadog",
    "feature_toggle": "feature_flag",
    "gh": "github",
    "gha": "github_actions",
    "gitops": "gitops_controller",
    "gl": "gitlab",
    "hashicorp_consul": "consul",
    "hashicorp_vault": "vault",
    "iac": "config_management",
    "incident": "alert_incident",
    "k8s": "container_cluster",
    "kubernetes": "container_cluster",
    "kubernetes_cluster": "container_cluster",
    "logs": "logging",
    "metrics": "monitoring",
    "nr": "new_relic",
    "package": "package_dependency",
    "pager": "on_call",
    "pd": "pagerduty",
    "pipeline": "cicd_pipeline",
    "pr": "pull_request",
    "pw": "playwright",
    "qa": "test_automation",
    "registry": "artifact_registry",
    "repo": "git_repository",
    "runner": "build_runner",
    "sbom": "package_dependency",
    "secret": "secret_vault",
    "secret_manager": "secret_vault",
    "sonar": "sonarqube",
    "sonatype_nexus": "nexus",
    "testing": "test_automation",
    "tf": "terraform",
    "tofu": "opentofu",
    "tracing": "distributed_tracing",
    "vulnerability_scan": "security_scan",
}

ORIGINAL_DEVOPS_PROVIDER = PngIconProvider(
    name="original_devops",
    package_name="icon_original_devops",
    asset_subdir="icons/original_devops",
    aliases=ORIGINAL_DEVOPS_ALIASES,
)

_write = ORIGINAL_DEVOPS_PROVIDER.write
