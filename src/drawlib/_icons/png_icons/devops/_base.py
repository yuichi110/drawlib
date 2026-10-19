# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Official DevOps, CI/CD, IaC, Testing, and Observability icon provider configuration."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

DEVOPS_ALIASES: dict[str, str] = {
    "actions": "github_actions",
    "artifactory": "jfrog",
    "bb": "bitbucket",
    "circle": "circleci",
    "dd": "datadog",
    "fluentbit": "fluent_bit",
    "gh": "github",
    "gha": "github_actions",
    "gl": "gitlab",
    "grafana_mimir": "mimir",
    "grafana_tempo": "tempo",
    "hashicorp_consul": "consul",
    "hashicorp_vault": "vault",
    "nr": "new_relic",
    "pd": "pagerduty",
    "pw": "playwright",
    "sonar": "sonarqube",
    "sonatype_nexus": "nexus",
    "tf": "terraform",
    "tofu": "opentofu",
    "turbo": "turborepo",
    "victoriametrics": "victoria_metrics",
    "vm_metrics": "victoria_metrics",
}

DEVOPS_PROVIDER = PngIconProvider(
    name="devops",
    package_name="icon_devops",
    asset_subdir="icons/devops",
    aliases=DEVOPS_ALIASES,
)

_write = DEVOPS_PROVIDER.write
