# Architecture

This document describes the internal architecture of the system.

## Component Breakdown

```drawlib center file:component_breakdown.png caption:"Service Component Breakdown"
from drawlib.canvas import setup
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=120, height=60)

# Services drawn using custom helper from utils.py
service_card((30, 42), title="Frontend UI", subtitle="Single Page App", width=34, height=18, style=Styles.PrimaryFlat)
service_card((30, 18), title="Auth Service", subtitle="OAuth 2.0 / JWT", width=34, height=18, style=Styles.AccentFlat)
service_card((90, 30), title="Core Backend", subtitle="Microservices Cluster", width=36, height=36, style=Styles.SecondaryFlat)

# Connections with protocol labels
connect((47, 42), (72, 35), label="HTTPS")
connect((47, 18), (72, 25), label="gRPC")
```
