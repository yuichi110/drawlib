# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Unit and integration tests for Data & Database ecosystem icons drawing."""

from pathlib import Path

import pytest

from drawlib._icons.png_icons.data._base import DATA_PROVIDER
from drawlib._icons.png_icons.original_data._base import ORIGINAL_DATA_PROVIDER
from drawlib.canvas import clear, save
from drawlib.diagrams.architecture import ArchitectureDiagram, DataIcon, Node, OriginalDataIcon
from drawlib.diagrams.sequence import Participant, SequenceDiagram
from drawlib.icons import data, original_data
from drawlib.styles import Styles
from drawlib.types import Style


class TestDataIcons:
    """Tests for Data icon provider, aliases, and diagram enums."""

    def test_data_db_and_dwh_icons(self, tmp_path: Path) -> None:
        """Verify RDBMS, NoSQL, and DWH icons."""
        clear()
        data.postgresql(xy=(15, 75), width=12, style=Style(), variant="default")
        data.mysql(xy=(35, 75), width=12, style=Style())
        data.sqlite(xy=(55, 75), width=12, style=Style())
        data.duckdb(xy=(75, 75), width=12, style=Style())

        data.mongodb(xy=(15, 50), width=12, style=Style())
        data.redis(xy=(35, 50), width=12, style=Style())
        data.valkey(xy=(55, 50), width=12, style=Style())
        data.neo4j(xy=(75, 50), width=12, style=Style())

        data.snowflake(xy=(15, 25), width=12, style=Style())
        data.databricks(xy=(35, 25), width=12, style=Style())
        data.clickhouse(xy=(55, 25), width=12, style=Style())
        data.trino(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_data_db_dwh.png"
        save(str(out))
        assert out.is_file()

    def test_data_streaming_and_processing_icons(self, tmp_path: Path) -> None:
        """Verify Streaming, Search, Vector, and ETL/Processing icons."""
        clear()
        data.kafka(xy=(15, 75), width=12, style=Style(), variant="default")
        data.rabbitmq(xy=(35, 75), width=12, style=Style())
        data.pulsar(xy=(55, 75), width=12, style=Style())
        data.redpanda(xy=(75, 75), width=12, style=Style())

        data.elasticsearch(xy=(15, 50), width=12, style=Style())
        data.milvus(xy=(35, 50), width=12, style=Style())
        data.qdrant(xy=(55, 50), width=12, style=Style())
        data.weaviate(xy=(75, 50), width=12, style=Style())

        data.spark(xy=(15, 25), width=12, style=Style())
        data.flink(xy=(35, 25), width=12, style=Style())
        data.airflow(xy=(55, 25), width=12, style=Style())
        data.dbt(xy=(75, 25), width=12, style=Style())

        out = tmp_path / "test_data_streaming_proc.png"
        save(str(out))
        assert out.is_file()

    def test_data_aliases(self, tmp_path: Path) -> None:
        """Verify Data shorthand aliases (pg, postgres, mongo, es, mssql, oracle, rabbit, delta)."""
        clear()
        data.pg(xy=(20, 60), width=12, style=Style())
        data.postgres(xy=(40, 60), width=12, style=Style())
        data.mongo(xy=(60, 60), width=12, style=Style())
        data.es(xy=(80, 60), width=12, style=Style())

        data.mssql(xy=(20, 30), width=12, style=Style())
        data.oracle(xy=(40, 30), width=12, style=Style())
        data.rabbit(xy=(60, 30), width=12, style=Style())
        data.delta(xy=(80, 30), width=12, style=Style())

        out = tmp_path / "test_data_aliases.png"
        save(str(out))
        assert out.is_file()

    def test_data_architecture_diagram_enum(self, tmp_path: Path) -> None:
        """Verify DataIcon works inside ArchitectureDiagram nodes."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Kafka", width=20, height=20, icon=DataIcon.KAFKA), (20, 50))
        n2 = diag.add(Node("Flink", width=20, height=20, icon=DataIcon.FLINK), (50, 50))
        n3 = diag.add(Node("Postgres", width=20, height=20, icon=DataIcon.POSTGRESQL), (80, 50))
        diag.connect(n1, n2)
        diag.connect(n2, n3)
        diag.draw((5, 10))
        out = tmp_path / "test_arch_data.png"
        save(str(out))
        assert out.is_file()

    def test_data_sequence_diagram_enum(self, tmp_path: Path) -> None:
        """Verify DataIcon works inside SequenceDiagram participants."""
        clear()
        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("Airflow", icon=DataIcon.AIRFLOW))
        p2 = seq.add(Participant("Snowflake", icon=DataIcon.SNOWFLAKE))
        seq.request(p1, p2, "Run dbt transform")
        seq.draw((10, 10))
        out = tmp_path / "test_seq_data.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_data_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Data icon file."""
        with pytest.raises(FileNotFoundError):
            DATA_PROVIDER.get_icon_path("non_existent_data_icon_xyz")

    def test_original_data_icons_and_aliases(self, tmp_path: Path) -> None:
        """Verify Original Data 2D pastel icons and shorthand aliases."""
        clear()
        original_data.postgresql(xy=(15, 75), width=12, style=Style(), variant="default")
        original_data.redis(xy=(35, 75), width=12, style=Style())
        original_data.kafka(xy=(55, 75), width=12, style=Style())
        original_data.duckdb(xy=(75, 75), width=12, style=Style())

        original_data.pg(xy=(15, 45), width=12, style=Style())
        original_data.mongo(xy=(35, 45), width=12, style=Style())
        original_data.es(xy=(55, 45), width=12, style=Style())
        original_data.delta(xy=(75, 45), width=12, style=Style())

        out = tmp_path / "test_original_data.png"
        save(str(out))
        assert out.is_file()

    def test_original_data_diagram_enums(self, tmp_path: Path) -> None:
        """Verify OriginalDataIcon works inside ArchitectureDiagram and SequenceDiagram."""
        clear()
        diag = ArchitectureDiagram(
            node_style=Styles.PrimaryFlat,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        n1 = diag.add(Node("Kafka", width=20, height=20, icon=OriginalDataIcon.KAFKA), (25, 65))
        n2 = diag.add(Node("Postgres", width=20, height=20, icon=OriginalDataIcon.POSTGRESQL), (75, 65))
        diag.connect(n1, n2)
        diag.draw((5, 45))

        seq = SequenceDiagram(
            node_style=Styles.Neutral,
            node_text_style=Styles.Dark,
            edge_style=Styles.Primary,
            edge_text_style=Styles.Dark,
        )
        p1 = seq.add(Participant("Airflow", icon=OriginalDataIcon.AIRFLOW))
        p2 = seq.add(Participant("Snowflake", icon=OriginalDataIcon.SNOWFLAKE))
        seq.request(p1, p2, "Run dbt")
        seq.draw((10, 5))

        out = tmp_path / "test_original_data_diagrams.png"
        save(str(out))
        assert out.is_file()

    def test_nonexistent_original_data_icon_error(self) -> None:
        """Verify FileNotFoundError when requesting an invalid Original Data icon file."""
        with pytest.raises(FileNotFoundError):
            ORIGINAL_DATA_PROVIDER.get_icon_path("non_existent_original_data_icon_xyz")
