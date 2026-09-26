# Architecture

This document describes the internal architecture of the system.

## Component Breakdown

```drawlib
setup(width=120, height=60)

rectangle((30, 40), width=35, height=20, style=styles.blue_flat, text="Frontend (UI)", textstyle=styles.white_bold)
rectangle((30, 15), width=35, height=20, style=styles.green_flat, text="Auth Service", textstyle=styles.white_bold)
rectangle((90, 27.5), width=35, height=40, style=styles.purple_flat, text="Core Backend", textstyle=styles.white_bold)

line((47.5, 40), (72.5, 35), arrowhead="->", style=styles.bold)
line((47.5, 15), (72.5, 20), arrowhead="->", style=styles.bold)
```
