# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""DevOps concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.devops._base import _write


def actions(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing actions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="github_actions", style=style, variant=variant)


def ansible(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing ansible.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ansible", style=style, variant=variant)


def artifactory(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing artifactory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="jfrog", style=style, variant=variant)


def bb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing bb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="bitbucket", style=style, variant=variant)


def bitbucket(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing bitbucket.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="bitbucket", style=style, variant=variant)


def buildkite(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing buildkite.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="buildkite", style=style, variant=variant)


def circle(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing circle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="circleci", style=style, variant=variant)


def circleci(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing circleci.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="circleci", style=style, variant=variant)


def consul(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing consul.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="consul", style=style, variant=variant)


def cypress(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing cypress.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cypress", style=style, variant=variant)


def datadog(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing datadog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datadog", style=style, variant=variant)


def dd(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing dd.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="datadog", style=style, variant=variant)


def dynatrace(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing dynatrace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="dynatrace", style=style, variant=variant)


def gh(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing gh.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="github", style=style, variant=variant)


def gha(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing gha.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="github_actions", style=style, variant=variant)


def git(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing git.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="git", style=style, variant=variant)


def github(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing github.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="github", style=style, variant=variant)


def github_actions(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing github actions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="github_actions", style=style, variant=variant)


def gitlab(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing gitlab.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gitlab", style=style, variant=variant)


def gl(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing gl.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gitlab", style=style, variant=variant)


def hashicorp_consul(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing hashicorp consul.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="consul", style=style, variant=variant)


def hashicorp_vault(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing hashicorp vault.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vault", style=style, variant=variant)


def jenkins(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing jenkins.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="jenkins", style=style, variant=variant)


def jfrog(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing jfrog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="jfrog", style=style, variant=variant)


def jira(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing jira.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="jira", style=style, variant=variant)


def k6(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing k6.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="k6", style=style, variant=variant)


def keycloak(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing keycloak.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="keycloak", style=style, variant=variant)


def kibana(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing kibana.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="kibana", style=style, variant=variant)


def loki(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing loki.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="loki", style=style, variant=variant)


def new_relic(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing new relic.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="new_relic", style=style, variant=variant)


def nexus(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing nexus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nexus", style=style, variant=variant)


def nr(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing nr.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="new_relic", style=style, variant=variant)


def opentofu(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing opentofu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="opentofu", style=style, variant=variant)


def packer(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing packer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="packer", style=style, variant=variant)


def pagerduty(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing pagerduty.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="pagerduty", style=style, variant=variant)


def pd(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing pd.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="pagerduty", style=style, variant=variant)


def playwright(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing playwright.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="playwright", style=style, variant=variant)


def podman(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing podman.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="podman", style=style, variant=variant)


def postman(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing postman.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="postman", style=style, variant=variant)


def pulumi(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing pulumi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="pulumi", style=style, variant=variant)


def pw(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing pw.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="playwright", style=style, variant=variant)


def selenium(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing selenium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="selenium", style=style, variant=variant)


def sentry(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing sentry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sentry", style=style, variant=variant)


def slack(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing slack.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="slack", style=style, variant=variant)


def snyk(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing snyk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="snyk", style=style, variant=variant)


def sonar(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing sonar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sonarqube", style=style, variant=variant)


def sonarqube(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing sonarqube.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sonarqube", style=style, variant=variant)


def sonatype_nexus(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing sonatype nexus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nexus", style=style, variant=variant)


def spinnaker(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing spinnaker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="spinnaker", style=style, variant=variant)


def splunk(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing splunk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="splunk", style=style, variant=variant)


def tekton(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing tekton.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tekton", style=style, variant=variant)


def terraform(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing terraform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="terraform", style=style, variant=variant)


def tf(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing tf.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="terraform", style=style, variant=variant)


def tofu(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing tofu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="opentofu", style=style, variant=variant)


def trivy(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing trivy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="trivy", style=style, variant=variant)


def vagrant(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing vagrant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vagrant", style=style, variant=variant)


def vault(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an DevOps concept icon representing vault.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vault", style=style, variant=variant)
