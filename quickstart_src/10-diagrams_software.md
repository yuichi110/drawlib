# 10. Software Design Diagrams

`drawlib.diagrams` provides specialized, declarative diagramming engines tailored for software architecture, API protocols, workflows, and object-oriented modeling.

## 1. Sequence Diagrams (`SequenceDiagram`)

In a `SequenceDiagram`, participants and lifelines are defined as Python objects. Interactions use clear methods (`request()`, `reply()`, `note()`) with automatic timeline layout:

```drawlib 640px center file:diagrams_sequence.png caption:"Figure 10.1: Declarative Sequence Diagram with Phosphor Icons"
from drawlib.canvas import setup
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram
from drawlib.styles import Styles

setup(width=120, height=65)

d = SequenceDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="OAuth 2.0 Token Exchange Sequence",
)

client = d.add(Participant("Client App", icon=PhosphorIcon.DESKTOP, icon_size=7.0))
gateway = d.add(Participant("API Gateway", icon=PhosphorIcon.CLOUD, icon_size=7.0))
auth = d.add(Participant("Auth Server", icon=PhosphorIcon.LOCK, icon_size=7.0))
user_db = d.add(Participant("User DB", icon=PhosphorIcon.DATABASE, icon_size=7.0))

client.request(gateway, "POST /v1/auth/token")
gateway.request(auth, "Validate Client Secret")
auth.request(user_db, "Query User Credentials")
user_db.reply(auth, "Hash Verified")
auth.reply(gateway, "Issued JWT & Refresh Token")
gateway.reply(client, "200 OK (access_token)")

d.draw(xy=(5.0, 5.0))
```

## 2. Decision & Process Flows (`FlowDiagram`)

`FlowDiagram` models logical branching, decision criteria, and workflow stages without manual line coordinate calculations:

```drawlib 640px center file:diagrams_auth_flow.png caption:"Figure 10.2: Request Authentication Flow with Branching Logic"
from drawlib.canvas import setup
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start
from drawlib.styles import Styles

setup(width=120, height=65)

f = FlowDiagram(
    node_style=Styles.PrimaryFlat,
    edge_style=Styles.Primary,
    title="Incoming Request Authorization Gate",
)

start = f.add(Start("HTTP Request"), xy=(15, 32))
parse_jwt = f.add(Process("Parse JWT"), xy=(42, 32))
check_valid = f.add(Decision("Valid?"), xy=(70, 32))
grant = f.add(End("Allow 200"), xy=(100, 46))
deny = f.add(End("Reject 401"), xy=(100, 18))

start.connect(parse_jwt)
parse_jwt.connect(check_valid)
check_valid.connect(grant, label="Yes")
check_valid.connect(deny, label="No")

f.draw()
```

## 3. Class, State & ER Diagrams

- **`ClassDiagram`**: Document classes, attributes, methods, inheritance (`--|>`), implementation (`..|>`), and associations.
- **`StateDiagram`**: Model state machine lifecycles (`InitialState`, `State`, `FinalState`) with event triggers and guard conditions.
- **`ERDiagram`**: Relational database schemas documenting primary keys (`PK`), foreign keys (`FK`), and 1:N cardinalities.
