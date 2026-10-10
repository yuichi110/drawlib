# Workflow

This document illustrates the execution lifecycle.

## Process Flow

```drawlib center file:execution_lifecycle.png caption:"Execution Lifecycle Flow"
from drawlib.canvas import setup
from drawlib.shapes import circle
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=100, height=40)

# Process stages
circle((18, 20), radius=9, style=Styles.PrimaryFlat, text="Start", text_style=Styles.WhiteBold)
service_card((50, 20), title="Process", subtitle="Worker Job", width=26, height=16, style=Styles.AccentFlat)
circle((82, 20), radius=9, style=Styles.SecondaryFlat, text="Finish", text_style=Styles.WhiteBold)

# Transitions
connect((27, 20), (37, 20))
connect((63, 20), (73, 20))
```
