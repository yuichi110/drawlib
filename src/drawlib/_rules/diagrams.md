# Drawlib Diagrams Guidelines

Create software architecture diagrams, flowcharts, sequence diagrams, ER diagrams, and state charts.

## 1. Imports
```python
from drawlib.diagrams import (
    ArchitectureDiagram,
    ClassDiagram,
    ERDiagram,
    FlowDiagram,
    SequenceDiagram,
    StateDiagram,
)
from drawlib.diagrams.flow import Decision, End, Process, Start
```

## 2. Diagram Types & Patterns
- `FlowDiagram(title="")`:
  - Nodes: `start = flow.add(Start("Start"), xy=(50, 80))`
  - Nodes: `proc = flow.add(Process("Task"), xy=(50, 50))`
  - Edges: `flow.connect(start, proc, label="")`
  - `flow.draw()`
- `SequenceDiagram(title="")`:
  - Lifelines: `user = seq.add_lifeline("User")`, `server = seq.add_lifeline("Server")`
  - Messages: `seq.add_message(user, server, "POST /login")`
  - `seq.draw()`
- `StateDiagram(title="")`:
  - States: `idle = state.add_state("Idle")`
  - Transitions: `state.add_transition(idle, active, event="click")`
- `ERDiagram(title="")`, `ClassDiagram(title="")`, `ArchitectureDiagram(title="")`:
  - Specialized UML and system modeling components.

## 3. Minimal Example (FlowDiagram)
```python
from drawlib.canvas import config, save
from drawlib.diagrams.flow import Decision, End, FlowDiagram, Process, Start

config(width=100, height=80)
flow = FlowDiagram(title="Approval Flow")
start = flow.add(Start("Start"), xy=(50, 70))
check = flow.add(Decision("Approved?"), xy=(50, 50))
deploy = flow.add(Process("Deploy"), xy=(50, 30))
finish = flow.add(End("End"), xy=(50, 10))

flow.connect(start, check)
flow.connect(check, deploy, label="Yes")
flow.connect(check, finish, label="No", bend=-0.5)
flow.connect(deploy, finish)
flow.draw()
save()
```
