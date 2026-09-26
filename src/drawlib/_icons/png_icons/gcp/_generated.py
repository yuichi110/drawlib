# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""GCP icon functions."""

from __future__ import annotations

from pydantic import validate_call

from drawlib._core.types import Style, TypeAngle, TypeCoordinate, TypePosFloat, TypeStr
from drawlib._icons.png_icons.gcp._base import _write


@validate_call
def access_context_manager(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing access context manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="access_context_manager", angle=angle, style=style)


@validate_call
def administration(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing administration.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="administration", angle=angle, style=style)


@validate_call
def advanced_agent_modeling(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing advanced agent modeling.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="advanced_agent_modeling", angle=angle, style=style)


@validate_call
def advanced_solutions_lab(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing advanced solutions lab.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="advanced_solutions_lab", angle=angle, style=style)


@validate_call
def agent_assist(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing agent assist.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="agent_assist", angle=angle, style=style)


@validate_call
def ai_hub(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing ai hub.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="ai_hub", angle=angle, style=style)


@validate_call
def ai_hypercomputer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing ai hypercomputer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="ai_hypercomputer", angle=angle, style=style)


@validate_call
def ai_platform(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing ai platform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="ai_platform", angle=angle, style=style)


@validate_call
def ai_platform_unified(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing ai platform unified.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="ai_platform_unified", angle=angle, style=style)


@validate_call
def alloydb(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing alloydb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="alloydb", angle=angle, style=style)


@validate_call
def analytics_hub(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing analytics hub.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="analytics_hub", angle=angle, style=style)


@validate_call
def anthos(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing anthos.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="anthos", angle=angle, style=style)


@validate_call
def anthos_config_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing anthos config management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="anthos_config_management", angle=angle, style=style)


@validate_call
def anthos_service_mesh(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing anthos service mesh.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="anthos_service_mesh", angle=angle, style=style)


@validate_call
def api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="api", angle=angle, style=style)


@validate_call
def api_analytics(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing api analytics.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="api_analytics", angle=angle, style=style)


@validate_call
def api_monetization(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing api monetization.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="api_monetization", angle=angle, style=style)


@validate_call
def apigee(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing apigee.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="apigee", angle=angle, style=style)


@validate_call
def apigee_api_platform(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing apigee api platform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="apigee_api_platform", angle=angle, style=style)


@validate_call
def apigee_sense(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing apigee sense.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="apigee_sense", angle=angle, style=style)


@validate_call
def app_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing app engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="app_engine", angle=angle, style=style)


@validate_call
def artifact_registry(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing artifact registry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="artifact_registry", angle=angle, style=style)


@validate_call
def asset_inventory(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing asset inventory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="asset_inventory", angle=angle, style=style)


@validate_call
def assured_workloads(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing assured workloads.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="assured_workloads", angle=angle, style=style)


@validate_call
def automl(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl", angle=angle, style=style)


@validate_call
def automl_natural_language(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl natural language.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl_natural_language", angle=angle, style=style)


@validate_call
def automl_tables(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl tables.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl_tables", angle=angle, style=style)


@validate_call
def automl_translation(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl translation.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl_translation", angle=angle, style=style)


@validate_call
def automl_video_intelligence(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl video intelligence.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl_video_intelligence", angle=angle, style=style)


@validate_call
def automl_vision(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing automl vision.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="automl_vision", angle=angle, style=style)


@validate_call
def bare_metal_solutions(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing bare metal solutions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="bare_metal_solutions", angle=angle, style=style)


@validate_call
def batch(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing batch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="batch", angle=angle, style=style)


@validate_call
def beyondcorp(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing beyondcorp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="beyondcorp", angle=angle, style=style)


@validate_call
def bigquery(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing bigquery.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="bigquery", angle=angle, style=style)


@validate_call
def bigtable(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing bigtable.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="bigtable", angle=angle, style=style)


@validate_call
def billing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing billing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="billing", angle=angle, style=style)


@validate_call
def binary_authorization(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing binary authorization.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="binary_authorization", angle=angle, style=style)


@validate_call
def catalog(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing catalog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="catalog", angle=angle, style=style)


@validate_call
def category_agents(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category agents.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_agents", angle=angle, style=style)


@validate_call
def category_ai_machine_learning(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category ai machine learning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_ai_machine_learning", angle=angle, style=style)


@validate_call
def category_business_intelligence(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category business intelligence.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_business_intelligence", angle=angle, style=style)


@validate_call
def category_collaboration(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category collaboration.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_collaboration", angle=angle, style=style)


@validate_call
def category_compute(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category compute.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_compute", angle=angle, style=style)


@validate_call
def category_containers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category containers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_containers", angle=angle, style=style)


@validate_call
def category_data_analytics(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category data analytics.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_data_analytics", angle=angle, style=style)


@validate_call
def category_databases(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category databases.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_databases", angle=angle, style=style)


@validate_call
def category_developer_tools(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category developer tools.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_developer_tools", angle=angle, style=style)


@validate_call
def category_devops(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category devops.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_devops", angle=angle, style=style)


@validate_call
def category_hybrid_multicloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category hybrid multicloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_hybrid_multicloud", angle=angle, style=style)


@validate_call
def category_integration_services(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category integration services.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_integration_services", angle=angle, style=style)


@validate_call
def category_management_tools(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category management tools.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_management_tools", angle=angle, style=style)


@validate_call
def category_maps_geospatial(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category maps geospatial.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_maps_geospatial", angle=angle, style=style)


@validate_call
def category_marketplace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category marketplace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_marketplace", angle=angle, style=style)


@validate_call
def category_media_services(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category media services.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_media_services", angle=angle, style=style)


@validate_call
def category_migration(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category migration.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_migration", angle=angle, style=style)


@validate_call
def category_mixed_reality(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category mixed reality.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_mixed_reality", angle=angle, style=style)


@validate_call
def category_networking(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category networking.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_networking", angle=angle, style=style)


@validate_call
def category_observability(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category observability.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_observability", angle=angle, style=style)


@validate_call
def category_operations(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category operations.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_operations", angle=angle, style=style)


@validate_call
def category_security_identity(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category security identity.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_security_identity", angle=angle, style=style)


@validate_call
def category_serverless_computing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category serverless computing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_serverless_computing", angle=angle, style=style)


@validate_call
def category_storage(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_storage", angle=angle, style=style)


@validate_call
def category_web3(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category web3.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_web3", angle=angle, style=style)


@validate_call
def category_web_mobile(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing category web mobile.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="category_web_mobile", angle=angle, style=style)


@validate_call
def certificate_authority_service(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing certificate authority service.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="certificate_authority_service", angle=angle, style=style)


@validate_call
def certificate_manager(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing certificate manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="certificate_manager", angle=angle, style=style)


@validate_call
def cloud_api_gateway(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud api gateway.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_api_gateway", angle=angle, style=style)


@validate_call
def cloud_apis(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud apis.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_apis", angle=angle, style=style)


@validate_call
def cloud_armor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud armor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_armor", angle=angle, style=style)


@validate_call
def cloud_asset_inventory(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud asset inventory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_asset_inventory", angle=angle, style=style)


@validate_call
def cloud_audit_logs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud audit logs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_audit_logs", angle=angle, style=style)


@validate_call
def cloud_build(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud build.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_build", angle=angle, style=style)


@validate_call
def cloud_cdn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud cdn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_cdn", angle=angle, style=style)


@validate_call
def cloud_code(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud code.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_code", angle=angle, style=style)


@validate_call
def cloud_composer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud composer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_composer", angle=angle, style=style)


@validate_call
def cloud_data_fusion(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud data fusion.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_data_fusion", angle=angle, style=style)


@validate_call
def cloud_deploy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud deploy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_deploy", angle=angle, style=style)


@validate_call
def cloud_deployment_manager(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud deployment manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_deployment_manager", angle=angle, style=style)


@validate_call
def cloud_dns(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud dns.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_dns", angle=angle, style=style)


@validate_call
def cloud_domains(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud domains.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_domains", angle=angle, style=style)


@validate_call
def cloud_ekm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud ekm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_ekm", angle=angle, style=style)


@validate_call
def cloud_endpoints(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud endpoints.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_endpoints", angle=angle, style=style)


@validate_call
def cloud_external_ip_addresses(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud external ip addresses.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_external_ip_addresses", angle=angle, style=style)


@validate_call
def cloud_firewall_rules(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud firewall rules.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_firewall_rules", angle=angle, style=style)


@validate_call
def cloud_for_marketing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud for marketing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_for_marketing", angle=angle, style=style)


@validate_call
def cloud_functions(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud functions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_functions", angle=angle, style=style)


@validate_call
def cloud_generic(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud generic.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_generic", angle=angle, style=style)


@validate_call
def cloud_gpu(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud gpu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_gpu", angle=angle, style=style)


@validate_call
def cloud_healthcare_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud healthcare api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_healthcare_api", angle=angle, style=style)


@validate_call
def cloud_healthcare_marketplace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud healthcare marketplace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_healthcare_marketplace", angle=angle, style=style)


@validate_call
def cloud_hsm(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud hsm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_hsm", angle=angle, style=style)


@validate_call
def cloud_ids(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud ids.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_ids", angle=angle, style=style)


@validate_call
def cloud_inference_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud inference api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_inference_api", angle=angle, style=style)


@validate_call
def cloud_interconnect(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud interconnect.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_interconnect", angle=angle, style=style)


@validate_call
def cloud_jobs_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud jobs api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_jobs_api", angle=angle, style=style)


@validate_call
def cloud_load_balancing(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud load balancing.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_load_balancing", angle=angle, style=style)


@validate_call
def cloud_logging(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud logging.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_logging", angle=angle, style=style)


@validate_call
def cloud_media_edge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud media edge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_media_edge", angle=angle, style=style)


@validate_call
def cloud_monitoring(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud monitoring.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_monitoring", angle=angle, style=style)


@validate_call
def cloud_nat(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud nat.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_nat", angle=angle, style=style)


@validate_call
def cloud_natural_language_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud natural language api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_natural_language_api", angle=angle, style=style)


@validate_call
def cloud_network(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud network.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_network", angle=angle, style=style)


@validate_call
def cloud_ops(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud ops.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_ops", angle=angle, style=style)


@validate_call
def cloud_optimization_ai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud optimization ai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_optimization_ai", angle=angle, style=style)


@validate_call
def cloud_optimization_ai_fleet_routing_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud optimization ai fleet routing api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_optimization_ai_fleet_routing_api", angle=angle, style=style)


@validate_call
def cloud_router(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud router.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_router", angle=angle, style=style)


@validate_call
def cloud_routes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud routes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_routes", angle=angle, style=style)


@validate_call
def cloud_run(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud run.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_run", angle=angle, style=style)


@validate_call
def cloud_run_for_anthos(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud run for anthos.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_run_for_anthos", angle=angle, style=style)


@validate_call
def cloud_scheduler(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud scheduler.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_scheduler", angle=angle, style=style)


@validate_call
def cloud_security_scanner(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud security scanner.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_security_scanner", angle=angle, style=style)


@validate_call
def cloud_shell(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud shell.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_shell", angle=angle, style=style)


@validate_call
def cloud_spanner(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud spanner.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_spanner", angle=angle, style=style)


@validate_call
def cloud_sql(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud sql.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_sql", angle=angle, style=style)


@validate_call
def cloud_storage(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud storage.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_storage", angle=angle, style=style)


@validate_call
def cloud_tasks(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud tasks.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_tasks", angle=angle, style=style)


@validate_call
def cloud_test_lab(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud test lab.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_test_lab", angle=angle, style=style)


@validate_call
def cloud_tpu(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud tpu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_tpu", angle=angle, style=style)


@validate_call
def cloud_translation_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud translation api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_translation_api", angle=angle, style=style)


@validate_call
def cloud_vision_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud vision api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_vision_api", angle=angle, style=style)


@validate_call
def cloud_vpn(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing cloud vpn.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="cloud_vpn", angle=angle, style=style)


@validate_call
def compute_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing compute engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="compute_engine", angle=angle, style=style)


@validate_call
def configuration_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing configuration management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="configuration_management", angle=angle, style=style)


@validate_call
def connectivity_test(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing connectivity test.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="connectivity_test", angle=angle, style=style)


@validate_call
def connectors(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing connectors.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="connectors", angle=angle, style=style)


@validate_call
def contact_center_ai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing contact center ai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="contact_center_ai", angle=angle, style=style)


@validate_call
def container_optimized_os(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing container optimized os.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="container_optimized_os", angle=angle, style=style)


@validate_call
def container_registry(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing container registry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="container_registry", angle=angle, style=style)


@validate_call
def data_catalog(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data catalog.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_catalog", angle=angle, style=style)


@validate_call
def data_labeling(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data labeling.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_labeling", angle=angle, style=style)


@validate_call
def data_layers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data layers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_layers", angle=angle, style=style)


@validate_call
def data_loss_prevention_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data loss prevention api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_loss_prevention_api", angle=angle, style=style)


@validate_call
def data_qna(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data qna.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_qna", angle=angle, style=style)


@validate_call
def data_studio(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data studio.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_studio", angle=angle, style=style)


@validate_call
def data_transfer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing data transfer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="data_transfer", angle=angle, style=style)


@validate_call
def database_migration_service(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing database migration service.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="database_migration_service", angle=angle, style=style)


@validate_call
def dataflow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dataflow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dataflow", angle=angle, style=style)


@validate_call
def datalab(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing datalab.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="datalab", angle=angle, style=style)


@validate_call
def dataplex(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dataplex.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dataplex", angle=angle, style=style)


@validate_call
def datapol(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing datapol.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="datapol", angle=angle, style=style)


@validate_call
def dataprep(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dataprep.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dataprep", angle=angle, style=style)


@validate_call
def dataproc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dataproc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dataproc", angle=angle, style=style)


@validate_call
def dataproc_metastore(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dataproc metastore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dataproc_metastore", angle=angle, style=style)


@validate_call
def datashare(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing datashare.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="datashare", angle=angle, style=style)


@validate_call
def datastore(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing datastore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="datastore", angle=angle, style=style)


@validate_call
def datastream(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing datastream.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="datastream", angle=angle, style=style)


@validate_call
def debugger(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing debugger.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="debugger", angle=angle, style=style)


@validate_call
def developer_portal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing developer portal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="developer_portal", angle=angle, style=style)


@validate_call
def dialogflow(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dialogflow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dialogflow", angle=angle, style=style)


@validate_call
def dialogflow_cx(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dialogflow cx.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dialogflow_cx", angle=angle, style=style)


@validate_call
def dialogflow_insights(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing dialogflow insights.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="dialogflow_insights", angle=angle, style=style)


@validate_call
def distributed_cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing distributed cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="distributed_cloud", angle=angle, style=style)


@validate_call
def document_ai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing document ai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="document_ai", angle=angle, style=style)


@validate_call
def early_access_center(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing early access center.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="early_access_center", angle=angle, style=style)


@validate_call
def error_reporting(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing error reporting.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="error_reporting", angle=angle, style=style)


@validate_call
def eventarc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing eventarc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="eventarc", angle=angle, style=style)


@validate_call
def filestore(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing filestore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="filestore", angle=angle, style=style)


@validate_call
def financial_services_marketplace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing financial services marketplace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="financial_services_marketplace", angle=angle, style=style)


@validate_call
def firestore(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing firestore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="firestore", angle=angle, style=style)


@validate_call
def fleet_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing fleet engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="fleet_engine", angle=angle, style=style)


@validate_call
def free_trial(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing free trial.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="free_trial", angle=angle, style=style)


@validate_call
def functions(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing functions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="functions", angle=angle, style=style)


@validate_call
def game_servers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing game servers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="game_servers", angle=angle, style=style)


@validate_call
def gce(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing gce.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="gce", angle=angle, style=style)


@validate_call
def gce_systems_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing gce systems management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="gce_systems_management", angle=angle, style=style)


@validate_call
def gcs(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing gcs.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="gcs", angle=angle, style=style)


@validate_call
def genomics(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing genomics.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="genomics", angle=angle, style=style)


@validate_call
def gke(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing gke.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="gke", angle=angle, style=style)


@validate_call
def gke_on_prem(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing gke on prem.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="gke_on_prem", angle=angle, style=style)


@validate_call
def google_cloud_marketplace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing google cloud marketplace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="google_cloud_marketplace", angle=angle, style=style)


@validate_call
def google_kubernetes_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing google kubernetes engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="google_kubernetes_engine", angle=angle, style=style)


@validate_call
def google_maps_platform(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing google maps platform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="google_maps_platform", angle=angle, style=style)


@validate_call
def healthcare_nlp_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing healthcare nlp api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="healthcare_nlp_api", angle=angle, style=style)


@validate_call
def home(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing home.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="home", angle=angle, style=style)


@validate_call
def hyperdisk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing hyperdisk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="hyperdisk", angle=angle, style=style)


@validate_call
def iam(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing iam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="iam", angle=angle, style=style)


@validate_call
def identity_and_access_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing identity and access management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="identity_and_access_management", angle=angle, style=style)


@validate_call
def identity_aware_proxy(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing identity aware proxy.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="identity_aware_proxy", angle=angle, style=style)


@validate_call
def identity_platform(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing identity platform.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="identity_platform", angle=angle, style=style)


@validate_call
def iot_core(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing iot core.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="iot_core", angle=angle, style=style)


@validate_call
def iot_edge(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing iot edge.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="iot_edge", angle=angle, style=style)


@validate_call
def key_access_justifications(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing key access justifications.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="key_access_justifications", angle=angle, style=style)


@validate_call
def key_management_service(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing key management service.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="key_management_service", angle=angle, style=style)


@validate_call
def kms(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing kms.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="kms", angle=angle, style=style)


@validate_call
def kuberun(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing kuberun.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="kuberun", angle=angle, style=style)


@validate_call
def launcher(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing launcher.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="launcher", angle=angle, style=style)


@validate_call
def local_ssd(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing local ssd.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="local_ssd", angle=angle, style=style)


@validate_call
def looker(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing looker.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="looker", angle=angle, style=style)


@validate_call
def managed_service_for_microsoft_active_directory(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing managed service for microsoft active directory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="managed_service_for_microsoft_active_directory", angle=angle, style=style)


@validate_call
def mandiant(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing mandiant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="mandiant", angle=angle, style=style)


@validate_call
def media_translation_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing media translation api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="media_translation_api", angle=angle, style=style)


@validate_call
def memorystore(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing memorystore.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="memorystore", angle=angle, style=style)


@validate_call
def migrate_for_anthos(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing migrate for anthos.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="migrate_for_anthos", angle=angle, style=style)


@validate_call
def migrate_for_compute_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing migrate for compute engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="migrate_for_compute_engine", angle=angle, style=style)


@validate_call
def my_cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing my cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="my_cloud", angle=angle, style=style)


@validate_call
def network_connectivity_center(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing network connectivity center.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="network_connectivity_center", angle=angle, style=style)


@validate_call
def network_intelligence_center(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing network intelligence center.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="network_intelligence_center", angle=angle, style=style)


@validate_call
def network_security(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing network security.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="network_security", angle=angle, style=style)


@validate_call
def network_tiers(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing network tiers.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="network_tiers", angle=angle, style=style)


@validate_call
def network_topology(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing network topology.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="network_topology", angle=angle, style=style)


@validate_call
def onboarding(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing onboarding.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="onboarding", angle=angle, style=style)


@validate_call
def os_configuration_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing os configuration management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="os_configuration_management", angle=angle, style=style)


@validate_call
def os_inventory_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing os inventory management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="os_inventory_management", angle=angle, style=style)


@validate_call
def os_patch_management(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing os patch management.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="os_patch_management", angle=angle, style=style)


@validate_call
def partner_interconnect(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing partner interconnect.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="partner_interconnect", angle=angle, style=style)


@validate_call
def partner_portal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing partner portal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="partner_portal", angle=angle, style=style)


@validate_call
def performance_dashboard(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing performance dashboard.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="performance_dashboard", angle=angle, style=style)


@validate_call
def permissions(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing permissions.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="permissions", angle=angle, style=style)


@validate_call
def persistent_disk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing persistent disk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="persistent_disk", angle=angle, style=style)


@validate_call
def phishing_protection(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing phishing protection.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="phishing_protection", angle=angle, style=style)


@validate_call
def policy_analyzer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing policy analyzer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="policy_analyzer", angle=angle, style=style)


@validate_call
def premium_network_tier(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing premium network tier.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="premium_network_tier", angle=angle, style=style)


@validate_call
def private_connectivity(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing private connectivity.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="private_connectivity", angle=angle, style=style)


@validate_call
def private_service_connect(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing private service connect.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="private_service_connect", angle=angle, style=style)


@validate_call
def producer_portal(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing producer portal.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="producer_portal", angle=angle, style=style)


@validate_call
def profiler(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing profiler.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="profiler", angle=angle, style=style)


@validate_call
def project(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing project.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="project", angle=angle, style=style)


@validate_call
def pubsub(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing pubsub.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="pubsub", angle=angle, style=style)


@validate_call
def quantum_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing quantum engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="quantum_engine", angle=angle, style=style)


@validate_call
def quotas(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing quotas.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="quotas", angle=angle, style=style)


@validate_call
def real_world_insights(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing real world insights.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="real_world_insights", angle=angle, style=style)


@validate_call
def recommendations_ai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing recommendations ai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="recommendations_ai", angle=angle, style=style)


@validate_call
def release_notes(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing release notes.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="release_notes", angle=angle, style=style)


@validate_call
def retail_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing retail api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="retail_api", angle=angle, style=style)


@validate_call
def risk_manager(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing risk manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="risk_manager", angle=angle, style=style)


@validate_call
def runtime_config(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing runtime config.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="runtime_config", angle=angle, style=style)


@validate_call
def secret_manager(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing secret manager.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="secret_manager", angle=angle, style=style)


@validate_call
def security(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing security.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="security", angle=angle, style=style)


@validate_call
def security_command_center(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing security command center.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="security_command_center", angle=angle, style=style)


@validate_call
def security_health_advisor(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing security health advisor.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="security_health_advisor", angle=angle, style=style)


@validate_call
def security_key_enforcement(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing security key enforcement.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="security_key_enforcement", angle=angle, style=style)


@validate_call
def security_operations(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing security operations.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="security_operations", angle=angle, style=style)


@validate_call
def service_discovery(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing service discovery.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="service_discovery", angle=angle, style=style)


@validate_call
def speech_to_text(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing speech to text.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="speech_to_text", angle=angle, style=style)


@validate_call
def stackdriver(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing stackdriver.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="stackdriver", angle=angle, style=style)


@validate_call
def standard_network_tier(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing standard network tier.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="standard_network_tier", angle=angle, style=style)


@validate_call
def stream_suite(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing stream suite.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="stream_suite", angle=angle, style=style)


@validate_call
def support(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing support.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="support", angle=angle, style=style)


@validate_call
def tensorflow_enterprise(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing tensorflow enterprise.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="tensorflow_enterprise", angle=angle, style=style)


@validate_call
def text_to_speech(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing text to speech.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="text_to_speech", angle=angle, style=style)


@validate_call
def threat_intelligence(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing threat intelligence.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="threat_intelligence", angle=angle, style=style)


@validate_call
def tools_for_powershell(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing tools for powershell.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="tools_for_powershell", angle=angle, style=style)


@validate_call
def trace(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing trace.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="trace", angle=angle, style=style)


@validate_call
def traffic_director(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing traffic director.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="traffic_director", angle=angle, style=style)


@validate_call
def transfer(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing transfer.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="transfer", angle=angle, style=style)


@validate_call
def transfer_appliance(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing transfer appliance.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="transfer_appliance", angle=angle, style=style)


@validate_call
def user_preferences(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing user preferences.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="user_preferences", angle=angle, style=style)


@validate_call
def vertex_ai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing vertex ai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="vertex_ai", angle=angle, style=style)


@validate_call
def vertexai(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing vertexai.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="vertexai", angle=angle, style=style)


@validate_call
def video_intelligence_api(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing video intelligence api.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="video_intelligence_api", angle=angle, style=style)


@validate_call
def virtual_private_cloud(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing virtual private cloud.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="virtual_private_cloud", angle=angle, style=style)


@validate_call
def visual_inspection(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing visual inspection.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="visual_inspection", angle=angle, style=style)


@validate_call
def vmware_engine(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing vmware engine.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="vmware_engine", angle=angle, style=style)


@validate_call
def vpc(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing vpc.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="vpc", angle=angle, style=style)


@validate_call
def web_risk(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing web risk.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="web_risk", angle=angle, style=style)


@validate_call
def web_security_scanner(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing web security scanner.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="web_security_scanner", angle=angle, style=style)


@validate_call
def workflows(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing workflows.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="workflows", angle=angle, style=style)


@validate_call
def workload_identity_pool(
    xy: TypeCoordinate,
    width: TypePosFloat,
    angle: TypeAngle = 0.0,
    *,
    style: Style,
) -> None:
    """Draws a GCP icon representing workload identity pool.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        angle: Rotation angle of the icon (0.0 to 360.0 degrees).
        style: Style object (required).

    """
    _write(xy=xy, width=width, name="workload_identity_pool", angle=angle, style=style)
