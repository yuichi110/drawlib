# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Data concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.data._base import _write


def airbyte(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing airbyte.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="airbyte", style=style, variant=variant)


def airflow(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing airflow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="airflow", style=style, variant=variant)


def apache_airflow(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache airflow.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="airflow", style=style, variant=variant)


def apache_beam(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache beam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="beam", style=style, variant=variant)


def apache_cassandra(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache cassandra.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cassandra", style=style, variant=variant)


def apache_druid(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache druid.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="druid", style=style, variant=variant)


def apache_flink(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache flink.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="flink", style=style, variant=variant)


def apache_hadoop(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache hadoop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hadoop", style=style, variant=variant)


def apache_iceberg(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache iceberg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="iceberg", style=style, variant=variant)


def apache_kafka(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache kafka.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="kafka", style=style, variant=variant)


def apache_nifi(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache nifi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nifi", style=style, variant=variant)


def apache_pulsar(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache pulsar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="pulsar", style=style, variant=variant)


def apache_spark(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache spark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="spark", style=style, variant=variant)


def apache_superset(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing apache superset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="superset", style=style, variant=variant)


def beam(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing beam.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="beam", style=style, variant=variant)


def cassandra(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing cassandra.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cassandra", style=style, variant=variant)


def clickhouse(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing clickhouse.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="clickhouse", style=style, variant=variant)


def cockroach(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing cockroach.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cockroachdb", style=style, variant=variant)


def cockroachdb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing cockroachdb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cockroachdb", style=style, variant=variant)


def couchbase(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing couchbase.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="couchbase", style=style, variant=variant)


def crdb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing crdb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="cockroachdb", style=style, variant=variant)


def dagster(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing dagster.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="dagster", style=style, variant=variant)


def databricks(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing databricks.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="databricks", style=style, variant=variant)


def dbt(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing dbt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="dbt", style=style, variant=variant)


def debezium(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing debezium.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="debezium", style=style, variant=variant)


def delta(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing delta.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="delta_lake", style=style, variant=variant)


def delta_lake(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing delta lake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="delta_lake", style=style, variant=variant)


def deltalake(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing deltalake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="delta_lake", style=style, variant=variant)


def druid(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing druid.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="druid", style=style, variant=variant)


def duckdb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing duckdb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="duckdb", style=style, variant=variant)


def elastic(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing elastic.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="elasticsearch", style=style, variant=variant)


def elasticsearch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing elasticsearch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="elasticsearch", style=style, variant=variant)


def es(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing es.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="elasticsearch", style=style, variant=variant)


def flink(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing flink.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="flink", style=style, variant=variant)


def hadoop(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing hadoop.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="hadoop", style=style, variant=variant)


def iceberg(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing iceberg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="iceberg", style=style, variant=variant)


def influx(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing influx.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="influxdb", style=style, variant=variant)


def influxdb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing influxdb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="influxdb", style=style, variant=variant)


def kafka(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing kafka.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="kafka", style=style, variant=variant)


def mariadb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing mariadb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="mariadb", style=style, variant=variant)


def meilisearch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing meilisearch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="meilisearch", style=style, variant=variant)


def memcached(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing memcached.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="memcached", style=style, variant=variant)


def milvus(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing milvus.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="milvus", style=style, variant=variant)


def minio(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing minio.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="minio", style=style, variant=variant)


def mongo(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing mongo.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="mongodb", style=style, variant=variant)


def mongodb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing mongodb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="mongodb", style=style, variant=variant)


def mssql(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing mssql.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sql_server", style=style, variant=variant)


def mysql(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing mysql.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="mysql", style=style, variant=variant)


def nats(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing nats.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nats", style=style, variant=variant)


def neo4j(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing neo4j.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="neo4j", style=style, variant=variant)


def nifi(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing nifi.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="nifi", style=style, variant=variant)


def opensearch(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing opensearch.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="opensearch", style=style, variant=variant)


def oracle(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing oracle.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="oracle_db", style=style, variant=variant)


def oracle_db(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing oracle db.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="oracle_db", style=style, variant=variant)


def pg(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing pg.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="postgresql", style=style, variant=variant)


def postgres(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing postgres.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="postgresql", style=style, variant=variant)


def postgresql(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing postgresql.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="postgresql", style=style, variant=variant)


def pulsar(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing pulsar.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="pulsar", style=style, variant=variant)


def qdrant(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing qdrant.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="qdrant", style=style, variant=variant)


def rabbit(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing rabbit.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rabbitmq", style=style, variant=variant)


def rabbitmq(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing rabbitmq.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rabbitmq", style=style, variant=variant)


def redis(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing redis.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="redis", style=style, variant=variant)


def redpanda(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing redpanda.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="redpanda", style=style, variant=variant)


def scylla(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing scylla.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="scylladb", style=style, variant=variant)


def scylladb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing scylladb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="scylladb", style=style, variant=variant)


def snowflake(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing snowflake.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="snowflake", style=style, variant=variant)


def spark(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing spark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="spark", style=style, variant=variant)


def sql_server(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing sql server.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sql_server", style=style, variant=variant)


def sqlite(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing sqlite.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sqlite", style=style, variant=variant)


def sqlserver(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing sqlserver.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="sql_server", style=style, variant=variant)


def supabase(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing supabase.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="supabase", style=style, variant=variant)


def superset(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing superset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="superset", style=style, variant=variant)


def tidb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing tidb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="tidb", style=style, variant=variant)


def timescale(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing timescale.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="timescaledb", style=style, variant=variant)


def timescaledb(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing timescaledb.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="timescaledb", style=style, variant=variant)


def trino(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing trino.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="trino", style=style, variant=variant)


def valkey(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing valkey.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="valkey", style=style, variant=variant)


def weaviate(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Data concept icon representing weaviate.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="weaviate", style=style, variant=variant)
