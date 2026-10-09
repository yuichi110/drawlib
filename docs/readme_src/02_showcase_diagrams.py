# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Cloud and distributed system architecture showcase."""

from drawlib.canvas import save, setup
from drawlib.icons import gcp, phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=120, height=58, dpi=200, color=Colors.Canvas)

# Outer Cloud Region Boundary (Muted structural container)
rectangle((68, 29), width=96, height=48, style=Styles.MutedDashed.patch(shape_r=3))
text((36, 49.5), "Google Cloud Region (us-central1)", style=Styles.MutedBold.patch(text_size=9.5))

# 1. External Client Entrypoint (Neutral card outside VPC)
rectangle((10, 29), width=16, height=26, style=Styles.Neutral.patch(shape_r=2))
phosphor.devices(xy=(10, 34.5), width=7.5, style=Styles.Accent)
text((10, 22.5), "Web & Mobile\nClients", style=Styles.DarkBold.patch(text_size=8))

line((18, 29), (28, 29), arrow_head="->", style=Styles.DarkBold)
text((23, 32), "HTTPS", style=Styles.DarkBold.patch(text_size=7.5))

# 2. Primary Focal Point: API Gateway on Cloud Run (PrimaryFlat hero node)
rectangle((39, 29), width=22, height=28, style=Styles.PrimaryFlat.patch(shape_r=2.5))
gcp.cloud_run(xy=(39, 35), width=9, style=Styles.White)
text((39, 22), "API Gateway\n(Cloud Run)", style=Styles.WhiteBold.patch(text_size=8.5))

line((50, 29), (60, 29), arrow_head="->", style=Styles.DarkBold)
text((55, 32), "gRPC", style=Styles.DarkBold.patch(text_size=7.5))

# 3. Event Streaming Bus (SecondaryNeutral card)
rectangle((70, 29), width=20, height=28, style=Styles.SecondaryNeutral.patch(shape_r=2))
gcp.pubsub(xy=(70, 35), width=9, style=Styles.Secondary)
text((70, 22), "Event Stream\n(Pub/Sub)", style=Styles.DarkBold.patch(text_size=8))

# Connectors to downstream storage & analytics
line((80, 35), (90, 41), arrow_head="->", style=Styles.DarkBold)
line((80, 23), (90, 17), arrow_head="->", style=Styles.DarkBold)

# 4. Downstream Data Stores (Neutral & SuccessNeutral cards)
rectangle((101, 41), width=22, height=18, style=Styles.Neutral.patch(shape_r=2))
gcp.cloud_sql(xy=(101, 44.5), width=7.5, style=Styles.Primary)
text((101, 35.5), "Cloud SQL (OLTP)", style=Styles.DarkBold.patch(text_size=7.5))

rectangle((101, 17), width=22, height=18, style=Styles.SuccessNeutral.patch(shape_r=2))
gcp.bigquery(xy=(101, 20.5), width=7.5, style=Styles.Success)
text((101, 11.5), "BigQuery (OLAP)", style=Styles.DarkBold.patch(text_size=7.5))

save()
