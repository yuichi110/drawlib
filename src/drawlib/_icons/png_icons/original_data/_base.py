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
    "apache_arrow": "arrow",
    "apache_beam": "beam",
    "apache_cassandra": "cassandra",
    "apache_doris": "doris",
    "apache_druid": "druid",
    "apache_flink": "flink",
    "apache_hadoop": "hadoop",
    "apache_hudi": "hudi",
    "apache_iceberg": "iceberg",
    "apache_kafka": "kafka",
    "apache_nifi": "nifi",
    "apache_parquet": "parquet",
    "apache_pulsar": "pulsar",
    "apache_spark": "spark",
    "apache_superset": "superset",
    "bucket": "object_storage",
    "cache": "in_memory_cache",
    "catalog": "data_catalog",
    "cdc": "cdc_stream",
    "chroma": "chromadb",
    "cockroach": "cockroachdb",
    "crdb": "cockroachdb",
    "delta": "delta_lake",
    "deltalake": "delta_lake",
    "doc_db": "document_db",
    "dwh": "data_warehouse",
    "elastic": "elasticsearch",
    "elt": "etl_pipeline",
    "es": "elasticsearch",
    "etl": "etl_pipeline",
    "influx": "influxdb",
    "kv_store": "key_value_store",
    "kvs": "key_value_store",
    "lakehouse": "data_lakehouse",
    "mongo": "mongodb",
    "mq": "message_broker",
    "mssql": "sql_server",
    "nosql": "nosql_db",
    "oracle": "oracle_db",
    "pg": "postgresql",
    "postgres": "postgresql",
    "pubsub": "message_broker",
    "rabbit": "rabbitmq",
    "rdbms": "relational_db",
    "scylla": "scylladb",
    "sql_db": "relational_db",
    "sqlserver": "sql_server",
    "timescale": "timescaledb",
    "tsdb": "time_series_db",
    "yb": "yugabytedb",
    "yugabyte": "yugabytedb",
}

ORIGINAL_DATA_PROVIDER = PngIconProvider(
    name="original_data",
    package_name="icon_original_data",
    asset_subdir="icons/original_data",
    aliases=ORIGINAL_DATA_ALIASES,
)

_write = ORIGINAL_DATA_PROVIDER.write
