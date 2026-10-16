# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original Data & Database icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_DATA_ALIASES: dict[str, str] = {
    "apache_airflow": "airflow",
    "apache_beam": "beam",
    "apache_cassandra": "cassandra",
    "apache_druid": "druid",
    "apache_flink": "flink",
    "apache_hadoop": "hadoop",
    "apache_iceberg": "iceberg",
    "apache_kafka": "kafka",
    "apache_nifi": "nifi",
    "apache_pulsar": "pulsar",
    "apache_spark": "spark",
    "apache_superset": "superset",
    "cockroach": "cockroachdb",
    "crdb": "cockroachdb",
    "delta": "delta_lake",
    "deltalake": "delta_lake",
    "elastic": "elasticsearch",
    "es": "elasticsearch",
    "influx": "influxdb",
    "mongo": "mongodb",
    "mssql": "sql_server",
    "oracle": "oracle_db",
    "pg": "postgresql",
    "postgres": "postgresql",
    "rabbit": "rabbitmq",
    "scylla": "scylladb",
    "sqlserver": "sql_server",
    "timescale": "timescaledb",
}

ORIGINAL_DATA_PROVIDER = PngIconProvider(
    name="original_data",
    package_name="icon_original_data",
    asset_subdir="icons/original_data",
    aliases=ORIGINAL_DATA_ALIASES,
)

_write = ORIGINAL_DATA_PROVIDER.write
