# 9. Software & Architecture Diagrams

`drawlib.diagrams` provides specialized declarative engines for software engineering and cloud architecture documentation, including **Sequence Diagrams**, **Architecture Diagrams**, **Flow Diagrams**, **Class Diagrams**, **State Diagrams**, and **ER Diagrams**.

## Sequence Diagrams (`drawlib.diagrams.sequence`)

With `SequenceDiagram`, participants and lifelines are defined as Python objects and interactions use expressive methods (`request()`, `reply()`) with automatic timeline spacing:

```drawlib 620px center caption:"Figure 9.1: Declarative Sequence Diagram with Phosphor Icons"
from drawlib import canvas
from drawlib.diagrams.sequence import Participant, PhosphorIcon, SequenceDiagram

canvas.initialize()

d = SequenceDiagram(title="API Gateway & Microservice Authentication")

user = d.add(Participant("Client", icon=PhosphorIcon.USER, icon_size=8.0))
gateway = d.add(Participant("API Gateway", icon=PhosphorIcon.CLOUD, icon_size=8.0))
service = d.add(Participant("Auth Service", icon=PhosphorIcon.CPU, icon_size=8.0))
db = d.add(Participant("User DB", icon=PhosphorIcon.DATABASE, icon_size=8.0))

user.request(gateway, "POST /v1/token")
gateway.request(service, "Verify Credentials")
service.request(db, "SELECT user_hash")
db.reply(service, "Record Matched")
service.reply(gateway, "Signed JWT")
gateway.reply(user, "200 OK (JWT)")

d.draw(xy=(5.0, 5.0))
```
