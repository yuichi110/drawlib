# Drawlib Data Icons Guidelines (`lib-icons-data`)

API specification and complete catalog for `drawlib.icons.data` (`DataIcon`, **70** official relational, NoSQL, vector, lakehouse, streaming, and BI brand icons) and `drawlib.icons.original_data` (`OriginalDataIcon`, **86** flat 2D pastel icons: **70** brand twins + **16** vendor-neutral database and data platform concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import DataIcon, Node, OriginalDataIcon
from drawlib.icons import data, data_icon, original_data, original_data_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
data.postgresql((30, 25), width=9.0, style=Styles.Primary)
original_data.postgresql((55, 25), width=9.0, style=Styles.Primary)
original_data.data_lakehouse((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
data_icon((30, 10), width=9.0, name="kafka", style=Styles.Primary)
original_data_icon((55, 10), width=9.0, name="vector_db", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
pg_node = Node("PostgreSQL", width=24, height=18, icon=DataIcon.POSTGRESQL, icon_size=7.5)
lake_node = Node("Data Lakehouse", width=24, height=18, icon=OriginalDataIcon.DATA_LAKEHOUSE, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.data` | `DataIcon` | **70** | `icon_data` | Official logos for SQL/NoSQL/Vector databases, data warehouses, lakehouse formats, event brokers, and ETL/BI tools. |
| `drawlib.icons.original_data` | `OriginalDataIcon` | **86** (`70` + `16`) | `icon_original_data` | Flat 2D pastel twins for all 70 data brands plus **16 vendor-neutral database & lakehouse concept icons**. |

---

## 2. Complete 70 Shared Brand Icons (`data.*` & `original_data.*`)

| Category | Count | Canonical Function Names (`data.*` & `original_data.*`) |
| :--- | :---: | :--- |
| **Relational, Distributed SQL & Serverless DBs** | 13 | `cockroachdb`, `mariadb`, `mysql`, `neon`, `oracle_db`, `planetscale`, `postgresql`, `sql_server`, `sqlite`, `supabase`, `tidb`, `turso`, `yugabytedb` |
| **NoSQL, Document, Wide-Column, Graph & Time-Series** | 10 | `cassandra`, `couchbase`, `influxdb`, `memcached`, `mongodb`, `neo4j`, `redis`, `scylladb`, `timescaledb`, `valkey` |
| **Vector Databases & Search Engines** | 9 | `chromadb`, `elasticsearch`, `lancedb`, `meilisearch`, `milvus`, `opensearch`, `pgvector`, `qdrant`, `weaviate` |
| **Cloud Data Warehouses, OLAP & Lakehouse Formats** | 15 | `arrow`, `clickhouse`, `databricks`, `delta_lake`, `doris`, `druid`, `duckdb`, `hadoop`, `hudi`, `iceberg`, `minio`, `parquet`, `snowflake`, `starrocks`, `trino` |
| **Streaming, Event Brokers & CDC Engines** | 9 | `beam`, `debezium`, `flink`, `kafka`, `nats`, `pulsar`, `rabbitmq`, `redpanda`, `spark` |
| **Data Integration, Orchestration, Catalog & BI** | 14 | `airbyte`, `airflow`, `dagster`, `datahub`, `dbt`, `fivetran`, `marimo`, `metabase`, `nifi`, `openmetadata`, `polars`, `prefect`, `redash`, `superset` |

---

## 3. Complete 16 Vendor-Neutral Data Concept Icons (`original_data.*` Only)

| Canonical Function (`original_data.*`) | `OriginalDataIcon` Enum | Architectural Role |
| :--- | :--- | :--- |
| `cdc_stream` | `CDC_STREAM` | Change Data Capture (CDC) log tailing and real-time replication stream |
| `columnar_db` | `COLUMNAR_DB` | Column-oriented analytical database engine (OLAP) |
| `data_catalog` | `DATA_CATALOG` | Enterprise metadata governance, schema discovery, and lineage catalog |
| `data_lakehouse` | `DATA_LAKEHOUSE` | Unified open table format lakehouse combining object storage and ACID SQL |
| `data_warehouse` | `DATA_WAREHOUSE` | Centralized enterprise analytical data warehouse |
| `document_db` | `DOCUMENT_DB` | Schema-flexible JSON/BSON document database |
| `etl_pipeline` | `ETL_PIPELINE` | Extract-Transform-Load (ETL / ELT) batch and incremental data pipeline |
| `graph_db` | `GRAPH_DB` | Property graph or RDF knowledge graph database |
| `in_memory_cache` | `IN_MEMORY_CACHE` | Sub-millisecond in-memory caching tier |
| `key_value_store` | `KEY_VALUE_STORE` | Distributed key-value lookup and session storage engine |
| `message_broker` | `MESSAGE_BROKER` | Asynchronous pub/sub event bus and message queue broker |
| `nosql_db` | `NOSQL_DB` | Partitioned non-relational wide-column or distributed NoSQL store |
| `object_storage` | `OBJECT_STORAGE` | Durable blob and parquet object storage bucket |
| `relational_db` | `RELATIONAL_DB` | ACID-compliant relational SQL transactional database (OLTP) |
| `time_series_db` | `TIME_SERIES_DB` | High-ingest telemetry, metrics, and IoT time-series database |
| `vector_db` | `VECTOR_DB` | High-dimensional vector similarity search database |

```drawlib code=fold align=center file=icons_data_rules_arch.png caption="Real-Time CDC & Lakehouse Analytics Pipeline Using DataIcon and OriginalDataIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    DataIcon,
    Node,
    NodeGroup,
    OriginalDataIcon,
)
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

pg = d.add(
    Node("PostgreSQL\nOLTP", width=24, height=18, icon=DataIcon.POSTGRESQL, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
lake = d.add(NodeGroup(title="Streaming & Lakehouse Platform", padding=4.5), xy=(42, 4))
kafka = lake.add(Node("Apache\nKafka", width=24, height=18, icon=DataIcon.KAFKA, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
lh = lake.add(Node("Iceberg\nLakehouse", width=24, height=18, icon=OriginalDataIcon.DATA_LAKEHOUSE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(pg, kafka, label="CDC", padding=1.5)
d.connect(kafka, lh, label="Parquet", padding=1.5)
d.draw(xy=(4, 4))
save()
```
