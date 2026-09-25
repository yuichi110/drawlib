# Workflow

This document illustrates the execution lifecycle.

## Process Flow

```drawlib
config(width=100, height=40)

circle((20, 20), radius=10, style="blue_flat", text="Start", textstyle="white_bold")
rectangle((50, 20), width=24, height=16, style="green_flat", text="Process", textstyle="white_bold")
circle((80, 20), radius=10, style="red_flat", text="Finish", textstyle="white_bold")

line((30, 20), (38, 20), arrowhead="->", style="bold")
line((62, 20), (70, 20), arrowhead="->", style="bold")
```
