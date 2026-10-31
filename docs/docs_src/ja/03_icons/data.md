# データ・データベースアイコン

Drawlib は、`drawlib.icons.data`（`DataIcon`）に **70 種の公式データ・データベースブランドアイコン**を、`drawlib.icons.original_data`（`OriginalDataIcon`）に **86 種のフラット 2D パステルアイコン**（**70 種のブランドツイン**＋**16 種のベンダー中立データベース・データアーキテクチャコンセプトアイコン**）を提供しています。ティア間の使い分け指針については[アイコン概要](./overview.md)を、トポロジ図への組み込みについては[アーキテクチャ図](../06_diagrams/architecture.md)を参照してください。

```drawlib code=fold align=center file=icons_data_hero.png caption="公式ブランドアイコン (data)、オリジナル 2D パステルブランド (original_data)、オリジナル 2D パステルコンセプト (original_data) の比較"
from drawlib.canvas import save, setup
from drawlib.icons import data, original_data
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=144, height=70)

columns = [
    (
        26.0,
        "1. Official Data Brands",
        "drawlib.icons.data (70)",
        Styles.Neutral,
        [
            ("postgresql", data.postgresql),
            ("redis", data.redis),
            ("kafka", data.kafka),
            ("snowflake", data.snowflake),
        ],
    ),
    (
        72.0,
        "2. 2D Pastel Brands",
        "original_data Twins (70)",
        Styles.PrimaryNeutral,
        [
            ("postgresql", original_data.postgresql),
            ("redis", original_data.redis),
            ("kafka", original_data.kafka),
            ("snowflake", original_data.snowflake),
        ],
    ),
    (
        118.0,
        "3. 2D Pastel Concepts",
        "original_data Exclusive (16)",
        Styles.SecondaryNeutral,
        [
            ("relational_db", original_data.relational_db),
            ("lakehouse", original_data.data_lakehouse),
            ("etl_pipeline", original_data.etl_pipeline),
            ("vector_db", original_data.vector_db),
        ],
    ),
]

for cx, title, subtitle, card_style, icons_list in columns:
    rectangle((cx, 35.0), width=42.0, height=62.0, style=card_style.patch(shape_r=2.5))
    text((cx, 60.0), title, style=Styles.DarkBold.patch(text_size=11.0))
    text((cx, 54.8), subtitle, style=Styles.Muted.patch(text_size=10.0))

    offsets = [(-9.8, 41.5), (9.8, 41.5), (-9.8, 20.5), (9.8, 20.5)]
    sub_card_style = Styles.White.patch(shape_r=1.5, line_width=0.6)
    for (dx, iy), (lbl, fn) in zip(offsets, icons_list, strict=True):
        ix = cx + dx
        rectangle((ix, iy - 1.8), width=17.6, height=17.5, style=sub_card_style)
        fn((ix, iy + 1.5), width=7.5, style=Styles.Primary)
        text((ix, iy - 6.6), lbl, style=Styles.DarkBold.patch(text_size=10.0))

save()
```

---

## 1. API シグネチャとツインモジュール構成

データ・データベースアイコンスイートは、1 対 1 の正規命名規則を共有するツインモジュールペアとして構成されています。

- **`drawlib.icons.data`**（`DataIcon` Enum）: リレーショナルデータベース、NoSQL ストア、ベクトルデータベース、データウェアハウス、Apache レイクハウス形式、ストリーミングブローカ、ETL/BI プラットフォームを網羅する **70 種の公式ベンダーおよび OSS ブランドアイコン**（`512×512` RGBA PNG）。
- **`drawlib.icons.original_data`**（`OriginalDataIcon` Enum）: 全 **70 種の対応するブランドツイン**に加え、**16 種のベンダー中立データアーキテクチャコンセプトアイコン**（`relational_db`、`data_warehouse`、`data_lakehouse`、`etl_pipeline`、`cdc_stream` など）を含む合計 **86 種のフラット 2D パステルアイコン**（`512×512` RGBA PNG）。

```python
from drawlib.diagrams.architecture import DataIcon, Node, OriginalDataIcon
from drawlib.icons import data, original_data
from drawlib.styles import Styles

# 1. Direct canvas rendering (center-anchored at (cx, cy), 1:1 square aspect ratio)
data.postgresql((30, 25), width=9.0, style=Styles.Primary)
original_data.postgresql((60, 25), width=9.0, style=Styles.Primary)
original_data.data_lakehouse((90, 25), width=9.0, style=Styles.Primary)

# 2. High-level ArchitectureDiagram / SequenceDiagram Enums
pg_node = Node("PostgreSQL Primary", width=25, height=18, icon=DataIcon.POSTGRESQL, icon_size=7.5)
dw_node = Node("Enterprise DW", width=25, height=18, icon=OriginalDataIcon.DATA_WAREHOUSE, icon_size=7.5)
```

| 項目 | 公式スイート (`drawlib.icons.data`) | オリジナル 2D パステルスイート (`drawlib.icons.original_data`) |
| :--- | :--- | :--- |
| **関数シグネチャ** | `data.<name>(xy, width, *, style, variant="default")` | `original_data.<name>(xy, width, *, style, variant="default")` |
| **ダイアグラム Enum** | `DataIcon.<NAME>`（例: `DataIcon.POSTGRESQL`） | `OriginalDataIcon.<NAME>`（例: `OriginalDataIcon.DATA_WAREHOUSE`） |
| **正規アイコン数** | ブランドアイコン **70** 種 | 合計 **86** 種（ブランドツイン **70** 種 + コンセプトアイコン **16** 種） |
| **座標アンカー** | 中央基準 `(cx, cy)`（`halign="center"`, `valign="center"`） | 中央基準 `(cx, cy)`（`halign="center"`, `valign="center"`） |
| **アセットアーカイブ** | `icon_data`（`512×512` RGBA PNG） | `icon_original_data`（`512×512` RGBA PNG） |

---

## 2. 公式・パステルブランドアイコン一覧とリファレンス (`data` & `original_data`)

以下に示す **70 種のブランドアイコン名**は、`drawlib.icons.data`（公式ロゴ）と `drawlib.icons.original_data`（対応する 2D パステルブランドツイン）の両方に共通して収録されています。

```drawlib code=fold align=center file=icons_data_brands.png caption="リレーショナル・NoSQL・ベクトル・ストリーミング・レイクハウスにわたる代表的なデータ・DB ブランドアイコン"
from drawlib.canvas import save, setup
from drawlib.icons import data
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=148, height=64)

row1 = [
    ("postgresql", "Relational", data.postgresql, Styles.PrimaryNeutral),
    ("mongodb", "Document DB", data.mongodb, Styles.Neutral),
    ("redis", "In-Memory", data.redis, Styles.SecondaryNeutral),
    ("qdrant", "Vector DB", data.qdrant, Styles.Neutral),
    ("clickhouse", "Columnar OLAP", data.clickhouse, Styles.PrimaryNeutral),
    ("snowflake", "Cloud DW", data.snowflake, Styles.Neutral),
]

row2 = [
    ("databricks", "Lakehouse", data.databricks, Styles.Neutral),
    ("iceberg", "Table Format", data.iceberg, Styles.SecondaryNeutral),
    ("kafka", "Event Stream", data.kafka, Styles.PrimaryNeutral),
    ("flink", "Stream Engine", data.flink, Styles.Neutral),
    ("airflow", "Orchestrator", data.airflow, Styles.SecondaryNeutral),
    ("dbt", "SQL Transform", data.dbt, Styles.Neutral),
]

for row_idx, items in enumerate([row1, row2]):
    cy = 46.5 if row_idx == 0 else 17.5
    for col_idx, (name, cat, icon_fn, card_st) in enumerate(items):
        cx = 15.2 + col_idx * 23.5
        rectangle((cx, cy), width=21.8, height=25.0, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.8), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.4), name, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.2), cat, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 2.1. 共通ブランドアイコン全 70 種一覧 (`data.<name>` & `original_data.<name>`)

| カテゴリ | 数 | 正規関数名 (`data.<name>` & `original_data.<name>`) |
| :--- | :---: | :--- |
| **リレーショナル・分散 SQL・サーバーレス DB** | 13 | `cockroachdb`, `mariadb`, `mysql`, `neon`, `oracle_db`, `planetscale`, `postgresql`, `sql_server`, `sqlite`, `supabase`, `tidb`, `turso`, `yugabytedb` |
| **NoSQL・ドキュメント・ワイドカラム・グラフ・時系列** | 10 | `cassandra`, `couchbase`, `influxdb`, `memcached`, `mongodb`, `neo4j`, `redis`, `scylladb`, `timescaledb`, `valkey` |
| **ベクトルデータベース・検索エンジン** | 9 | `chromadb`, `elasticsearch`, `lancedb`, `meilisearch`, `milvus`, `opensearch`, `pgvector`, `qdrant`, `weaviate` |
| **クラウド DWH・OLAP・レイクハウス形式** | 15 | `arrow`, `clickhouse`, `databricks`, `delta_lake`, `doris`, `druid`, `duckdb`, `hadoop`, `hudi`, `iceberg`, `minio`, `parquet`, `snowflake`, `starrocks`, `trino` |
| **ストリーミング・イベントブローカ・CDC エンジン** | 9 | `beam`, `debezium`, `flink`, `kafka`, `nats`, `pulsar`, `rabbitmq`, `redpanda`, `spark` |
| **データ統合・オーケストレーション・カタログ・BI** | 14 | `airbyte`, `airflow`, `dagster`, `datahub`, `dbt`, `fivetran`, `marimo`, `metabase`, `nifi`, `openmetadata`, `polars`, `prefect`, `redash`, `superset` |

---

## 3. ベンダー中立コンセプトアイコン一覧とリファレンス (`original_data`)

70 種のブランドツインに加え、`drawlib.icons.original_data`（`OriginalDataIcon`）には **16 種の専用ベンダー中立データベース・データ基盤コンセプトアイコン**が収録されており、論理データアーキテクチャやストレージエンジン、ETL/CDC パイプラインを図解できます。

```drawlib code=fold align=center file=icons_data_concepts.png caption="drawlib.icons.original_data に収録された代表的なベンダー中立データ・データベースコンセプトアイコン 12 選"
from drawlib.canvas import save, setup
from drawlib.icons import original_data
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=140, height=88)

rows = [
    [
        ("relational_db", "OLTP SQL Store", original_data.relational_db, Styles.PrimaryNeutral),
        ("document_db", "JSON Document DB", original_data.document_db, Styles.Neutral),
        ("key_value_store", "Key-Value Lookup", original_data.key_value_store, Styles.SecondaryNeutral),
        ("in_memory_cache", "Low-Latency Cache", original_data.in_memory_cache, Styles.Neutral),
    ],
    [
        ("graph_db", "Knowledge Graph", original_data.graph_db, Styles.Neutral),
        ("time_series_db", "Metrics & Telemetry", original_data.time_series_db, Styles.PrimaryNeutral),
        ("vector_db", "ANN Similarity Search", original_data.vector_db, Styles.Neutral),
        ("columnar_db", "Columnar OLAP", original_data.columnar_db, Styles.SecondaryNeutral),
    ],
    [
        ("data_warehouse", "Enterprise Analytics", original_data.data_warehouse, Styles.SecondaryNeutral),
        ("data_lakehouse", "Open Table Lakehouse", original_data.data_lakehouse, Styles.Neutral),
        ("etl_pipeline", "Batch & Incremental", original_data.etl_pipeline, Styles.PrimaryNeutral),
        ("cdc_stream", "Change Data Capture", original_data.cdc_stream, Styles.Neutral),
    ],
]

for row_idx, items in enumerate(rows):
    cy = 71.5 - row_idx * 27.5
    for col_idx, (title, sub, icon_fn, card_st) in enumerate(items):
        cx = 20.5 + col_idx * 33.0
        rectangle((cx, cy), width=30.5, height=24.5, style=card_st.patch(shape_r=2))
        icon_fn((cx, cy + 4.6), width=8.0, style=Styles.Primary)
        text((cx, cy - 3.4), title, style=Styles.DarkBold.patch(text_size=10.0))
        text((cx, cy - 8.2), sub, style=Styles.Muted.patch(text_size=10.0))

save()
```

### 3.1. ベンダー中立コンセプトアイコン全 16 種一覧 (`original_data.<name>`)

| 正規関数名 (`original_data.*`) | `OriginalDataIcon` Enum メンバー | アーキテクチャ上の役割 |
| :--- | :--- | :--- |
| `cdc_stream` | `OriginalDataIcon.CDC_STREAM` | 変更データキャプチャ（CDC）ログ追跡およびリアルタイムレプリケーションストリーム |
| `columnar_db` | `OriginalDataIcon.COLUMNAR_DB` | 列指向（カラムナ）分析データベースエンジン（OLAP） |
| `data_catalog` | `OriginalDataIcon.DATA_CATALOG` | エンタープライズメタデータガバナンス・スキーマ検索・データリネージカタログ |
| `data_lakehouse` | `OriginalDataIcon.DATA_LAKEHOUSE` | オブジェクトストレージと ACID SQL を統合したオープンテーブル形式レイクハウス |
| `data_warehouse` | `OriginalDataIcon.DATA_WAREHOUSE` | 全社統合型の分析データウェアハウス（DWH） |
| `document_db` | `OriginalDataIcon.DOCUMENT_DB` | スキーマ柔軟性の高い JSON/BSON ドキュメントデータベース |
| `etl_pipeline` | `OriginalDataIcon.ETL_PIPELINE` | バッチおよび増分処理による ETL / ELT データパイプライン |
| `graph_db` | `OriginalDataIcon.GRAPH_DB` | プロパティグラフまたは RDF ナレッジグラフデータベース |
| `in_memory_cache` | `OriginalDataIcon.IN_MEMORY_CACHE` | サブミリ秒応答のインメモリキャッシュ層 |
| `key_value_store` | `OriginalDataIcon.KEY_VALUE_STORE` | 分散 Key-Value ルックアップおよびセッションストレージエンジン |
| `message_broker` | `OriginalDataIcon.MESSAGE_BROKER` | 非同期 Pub/Sub イベントバスおよびメッセージキューブローカ |
| `nosql_db` | `OriginalDataIcon.NOSQL_DB` | パーティション分割された非リレーショナル・ワイドカラム／分散 NoSQL ストア |
| `object_storage` | `OriginalDataIcon.OBJECT_STORAGE` | 高耐久性な Blob・Parquet オブジェクトストレージバケット |
| `relational_db` | `OriginalDataIcon.RELATIONAL_DB` | ACID 準拠のリレーショナル SQL トランザクションデータベース（OLTP） |
| `time_series_db` | `OriginalDataIcon.TIME_SERIES_DB` | 高スループット取り込みに対応したテレメトリ・メトリクス・IoT 時系列データベース |
| `vector_db` | `OriginalDataIcon.VECTOR_DB` | 高次元ベクトル類似度検索データベース |

---

## 4. 実践的なアーキテクチャ図 (`DataIcon` & `OriginalDataIcon`)

以下の例では、[`ArchitectureDiagram`](../06_diagrams/architecture.md) 内で公式 `DataIcon` ロゴ（`PostgreSQL`、`Kafka`、`Iceberg`、`ClickHouse`）を組み合わせ、リアルタイム CDC とレイクハウス分析パイプラインを表現しています。

```drawlib code=show align=center file=icons_data_arch.png caption="DataIcon を用いたリアルタイム CDC ストリーミング＆レイクハウス分析トポロジ"
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    DataIcon,
    Node,
    NodeGroup,
)
from drawlib.styles import Styles

clear()
setup(width=128, height=64)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
    title="Real-Time CDC Streaming & Apache Iceberg Lakehouse Pipeline",
)

platform = d.add(NodeGroup(title="Streaming & Lakehouse Data Platform", padding=5.0), xy=(4.0, 4.0))
oltp = platform.add(
    Node(
        "PostgreSQL\nOLTP",
        width=25,
        height=18,
        icon=DataIcon.POSTGRESQL,
        icon_size=7.5,
    ),
    xy=(12.0, 18.0),
)
kafka_node = platform.add(
    Node(
        "Apache Kafka\nCDC Bus",
        width=25,
        height=18,
        icon=DataIcon.KAFKA,
        icon_size=7.5,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(56.0, 18.0),
)
iceberg_node = platform.add(
    Node(
        "Apache Iceberg\nLakehouse",
        width=25,
        height=18,
        icon=DataIcon.ICEBERG,
        icon_size=7.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(98.0, 28.0),
)
ch_node = platform.add(
    Node(
        "ClickHouse\nReal-Time OLAP",
        width=25,
        height=18,
        icon=DataIcon.CLICKHOUSE,
        icon_size=7.5,
    ),
    xy=(98.0, 8.0),
)

d.connect(oltp, kafka_node, label="Debezium", padding=1.5)
kafka_node.fork([iceberg_node, ch_node], at_x=88.0, padding=1.5)

d.draw(xy=(4.0, 4.0))
save()
```
