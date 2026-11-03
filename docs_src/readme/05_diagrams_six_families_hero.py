# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Overview of the six domain technical diagram engines."""

from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, GcpIcon, Node, NodeGroup
from drawlib.diagrams.class_diagram import ClassDiagram, ClassNode
from drawlib.diagrams.er import ERDiagram, Entity
from drawlib.diagrams.flow import Decision, FlowDiagram, Process, Start
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.diagrams.state import InitialState, State, StateDiagram
from drawlib.shapes import rectangle
from drawlib.styles import Colors, Styles
from drawlib.text import text

setup(width=130, height=66)

card_style = Styles.Neutral.patch(shape_r=2.0, shape_line_color=Colors.Gray4, shape_fill_color=Colors.White)
title_style = Styles.BlackBold.patch(text_size=10.5, halign="left")

cards = [
    (22.5, 49.0, "1. ArchitectureDiagram"),
    (65.0, 49.0, "2. FlowDiagram"),
    (107.5, 49.0, "3. SequenceDiagram"),
    (22.5, 16.5, "4. ClassDiagram"),
    (65.0, 16.5, "5. ERDiagram"),
    (107.5, 16.5, "6. StateDiagram"),
]
for cx, cy, title in cards:
    rectangle((cx, cy), width=40.0, height=29.5, style=card_style)
    text((cx - 18.0, cy + 12.0), title, style=title_style)

# 1. ArchitectureDiagram (Top-Left, scale=1.0)
arch = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.PrimaryNeutral,
)
grp = arch.add(
    NodeGroup(
        title="VPC",
        width=18.0,
        height=18.5,
        style=Styles.Neutral,
        text_style=Styles.DarkBold.patch(text_size=10.0, halign="left", valign="top"),
    ),
    xy=(18.5, 1.5),
)
n_api = arch.add(Node("Gateway", width=13.0, height=11.5, icon=GcpIcon.CLOUD_RUN, icon_size=4.5), xy=(7.5, 8.7))
n_db = grp.add(
    Node("Cloud SQL", width=13.5, height=11.5, icon=GcpIcon.CLOUD_SQL, icon_size=4.5, card_style=Styles.White),
    xy=(9.0, 7.2),
)
arch.connect(n_api, n_db, padding=0.8)
arch.draw(xy=(3.5, 35.0), scale=1.0)

# 2. FlowDiagram (Top-Center, scale=1.0)
flow = FlowDiagram(
    node_style=Styles.Neutral.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
f_start = flow.add(
    Start("Start", width=10.0, height=7.5, style=Styles.PrimaryNeutral.patch(text_size=10.0)),
    xy=(5.5, 9.5),
)
f_dec = flow.add(
    Decision("Valid?", width=12.5, height=9.5, style=Styles.SecondaryNeutral.patch(text_size=10.0)),
    xy=(19.0, 9.5),
)
f_proc = flow.add(
    Process("Run", width=10.0, height=7.5, style=Styles.PrimaryFlat, text_style=Styles.WhiteBold.patch(text_size=10.0)),
    xy=(32.5, 9.5),
)
f_start.connect(f_dec)
f_dec.connect(f_proc)
flow.draw(xy=(46.0, 35.5), scale=1.0)

# 3. SequenceDiagram (Top-Right, scale=1.0)
seq = SequenceDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
    node_card_style=Styles.PrimaryNeutral,
    col_width=19.5,
    step_y=4.2,
    margin=0.2,
)
p_cli = seq.add(Participant("Client", width=12.5, height=7.2, icon=PhosphorIcon.LAPTOP, icon_size=3.2))
p_srv = seq.add(Participant("Server", width=12.5, height=7.2, icon=PhosphorIcon.CLOUD, icon_size=3.2, card_style=Styles.Neutral))
p_cli.request(p_srv, "POST")
p_srv.reply(p_cli, "200 OK")
seq.draw(xy=(91.0, 33.6), scale=1.0)

# 4. ClassDiagram (Bottom-Left, scale=1.0)
cd = ClassDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
c_base = cd.add(ClassNode(name="Service", width=15.0, style=Styles.PrimaryNeutral), xy=(8.5, 9.5))
c_base.add_method("run", return_type="bool")
c_impl = cd.add(ClassNode(name="Worker", width=15.0, style=Styles.Neutral), xy=(29.5, 9.5))
c_impl.add_attribute("id", type="int")
cd.connect(c_impl, c_base, relationship_type="realization", start_side="left", end_side="right")
cd.draw(xy=(3.5, 3.0), scale=1.0)

# 5. ERDiagram (Bottom-Center, scale=1.0)
er = ERDiagram(
    node_style=Styles.Neutral,
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
e_user = er.add(Entity(name="users", width=15.5, style=Styles.PrimaryNeutral), xy=(8.2, 9.0))
e_user.add_column("id", type="INT", pk=True)
e_user.add_column("name", type="TEXT")
e_ord = er.add(Entity(name="orders", width=18.0, style=Styles.Neutral), xy=(29.2, 9.0))
e_ord.add_column("id", type="INT", pk=True)
e_ord.add_column("uid", type="INT", fk=True)
e_user.connect(e_ord, cardinality="1:*", start_side="right", end_side="left", start_column="id", end_column="uid")
er.draw(xy=(46.0, 3.5), scale=1.0)

# 6. StateDiagram (Bottom-Right, scale=1.0)
sd = StateDiagram(
    node_style=Styles.Neutral.patch(text_size=10.5),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.Dark.patch(text_size=10.0),
)
s_init = sd.add(InitialState(style=Styles.Dark), xy=(3.0, 9.0))
s_idle = sd.add(
    State("Idle", shape="box", width=11.0, height=7.5, style=Styles.PrimaryNeutral.patch(text_size=10.5)),
    xy=(13.0, 9.0),
)
s_run = sd.add(
    State("Active", shape="box", width=12.0, height=7.5, style=Styles.Neutral.patch(text_size=10.5)),
    xy=(30.0, 9.0),
)
sd.connect(s_init, s_idle)
sd.connect(s_idle, s_run, event="start", bend=-0.32, start_side="top_right", end_side="top_left")
sd.connect(
    s_run,
    s_idle,
    event="stop",
    bend=-0.32,
    start_side="bottom_left",
    end_side="bottom_right",
    text_style=Styles.Dark.patch(text_size=10.0, valign="top"),
)
sd.draw(xy=(89.0, 3.5), scale=1.0)

save()
