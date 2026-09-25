# Architecture

This document describes the internal architecture of the system.

## Component Breakdown

```drawlib
config(width=120, height=60)

rectangle((30, 40), width=35, height=20, style="blue_flat", text="Frontend (UI)", textstyle="white_bold")
rectangle((30, 15), width=35, height=20, style="green_flat", text="Auth Service", textstyle="white_bold")
rectangle((90, 27.5), width=35, height=40, style="purple_flat", text="Core Backend", textstyle="white_bold")

line((47.5, 40), (72.5, 35), arrowhead="->", style="bold")
line((47.5, 15), (72.5, 20), arrowhead="->", style="bold")
```
