::: block xy=(1700, 1008) width=140 height=32
```drawlib file=page.svg
import utils
utils.draw_page_number()
```
:::

::: block xy=(80, 1010) width=900 height=30 font_size=15px
*Drawlib — コードで描く図解と技術ドキュメント*
:::

::: block xy=(80, 36) width=1760 height=72
# ArchitectureDiagram によるクラウド構成図
:::

::: block xy=(80, 130) width=1760 height=815
```drawlib file=cloud_arch_showcase_ja.svg
from drawlib.canvas import clear, save, setup
from drawlib.diagrams.architecture import (
    ArchitectureDiagram,
    GcpIcon,
    Node,
    NodeGroup,
    PhosphorIcon,
)
from drawlib.icons import phosphor
from drawlib.smartarts import Panel
from drawlib.styles import Styles

clear()
setup(width=176, height=82)

panel = Panel(
    "マルチティア本番クラウド基盤トポロジー",
    "GcpIcon + PhosphorIcon + NodeGroup 境界 + 直交バス配線",
    style=Styles.White,
    header_style=Styles.PrimaryNeutral,
    text_style=Styles.DarkBold.patch(text_size=14.5),
    description_style=Styles.Muted.patch(text_size=11.5),
    icon=phosphor.cloud,
    icon_style=Styles.PrimaryBold,
    header_height=8.5,
)
panel.draw((2.0, 2.0), width=172.0, height=78.0)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=11.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=11.0),
    node_card_style=Styles.Neutral,
)

users = d.add(
    Node("外部ユーザー\n・端末", width=21, height=17.5, icon=PhosphorIcon.DEVICES, icon_size=7.0),
    xy=(11.5, 31.0),
)
edge = d.add(
    Node(
        "Cloud CDN\n& Armor WAF",
        width=22,
        height=17.5,
        icon=GcpIcon.CLOUD_ARMOR,
        icon_size=7.0,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(42.5, 31.0),
)

vpc = d.add(
    NodeGroup(
        title="本番 VPC (10.0.0.0/16)",
        width=44.0,
        height=58.0,
        padding=5.0,
        style=Styles.MutedDashed,
        text_style=Styles.DarkBold.patch(text_size=12.0, halign="left"),
    ),
    xy=(66.5, 2.0),
)
gke = vpc.add(
    Node(
        "GKE API\nマイクロサービス",
        width=28,
        height=16.5,
        icon=GcpIcon.GOOGLE_KUBERNETES_ENGINE,
        icon_size=7.0,
        style=Styles.White,
        card_style=Styles.PrimaryFlat,
        text_style=Styles.WhiteBold.patch(text_size=11.5),
    ),
    xy=(22.0, 41.0),
)
run = vpc.add(
    Node(
        "Cloud Run\n非同期ワーカー",
        width=28,
        height=16.5,
        icon=GcpIcon.CLOUD_RUN,
        icon_size=7.0,
        card_style=Styles.PrimaryNeutral,
    ),
    xy=(22.0, 13.5),
)

sql = d.add(
    Node(
        "Cloud SQL\n(本番 DB)",
        width=25,
        height=15.5,
        icon=GcpIcon.CLOUD_SQL,
        icon_size=6.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(150.5, 51.5),
)
pubsub = d.add(
    Node(
        "Pub/Sub\nイベント基盤",
        width=25,
        height=15.5,
        icon=GcpIcon.PUBSUB,
        icon_size=6.5,
        card_style=Styles.Neutral,
    ),
    xy=(150.5, 33.5),
)
bq = d.add(
    Node(
        "BigQuery\nデータ分析基盤",
        width=25,
        height=15.5,
        icon=GcpIcon.BIGQUERY,
        icon_size=6.5,
        card_style=Styles.SecondaryNeutral,
    ),
    xy=(150.5, 15.5),
)

d.connect(users, edge, label="HTTPS", padding=1.2)
edge.fork([gke, run], at_x=60.5, padding=1.2)
d.connect(gke, run, label="gRPC", padding=1.0)
d.connect(gke, sql, label="SQL", padding=1.2)
d.connect(gke, pubsub, label="イベント", padding=1.2)
d.connect(run, bq, label="ストリーム", padding=1.2)

d.draw(xy=(6.0, 4.5))
save()
```
:::

::: note
**`ArchitectureDiagram` によるクラウド基盤構成図の解説**:
- **33種類の公式・ドメインアイコン統合**: `GcpIcon`・`AwsIcon`・`AzureIcon` などの公式クラウドアイコンや `PhosphorIcon` を `Node` カードへ直接指定し、視認性の高い構成図を純粋な Python コードで描画できます。
- **`NodeGroup` による階層ネットワーク境界**: `本番 VPC ネットワーク (10.0.0.0/16)` の内部にローカル座標系で `GKE API マイクロサービス`（主役の `Styles.PrimaryFlat`）と `Cloud Run 非同期ワーカー` を配置し、VPC やサブネットの境界を明確に表現しています。
- **直交バス分岐 (`fork`) と自動ルーティング**: `edge.fork([gke, run], at_x=60.5)` により CDN / WAF から複数コンピュート層への1対N分岐を美しく整列させ、後段の `Cloud SQL`・`Pub/Sub`・`BigQuery` へ交差のない直交配線で接続しています。
:::
