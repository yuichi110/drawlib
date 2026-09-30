# Workflow

This document illustrates the execution lifecycle.

## Process Flow

```drawlib 600px center caption:"Execution Lifecycle Flow"
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=100, height=40)

# Process stages
circle((18, 20), radius=9, style=Styles.primary_flat, text="Start", textstyle=Styles.white_bold)
service_card((50, 20), title="Process", subtitle="Worker Job", width=26, height=16, style=Styles.accent_flat)
circle((82, 20), radius=9, style=Styles.secondary_flat, text="Finish", textstyle=Styles.white_bold)

# Transitions
connect((27, 20), (37, 20))
connect((63, 20), (73, 20))
```
