# Chapter 1: System Overview

## Introduction

This chapter provides a high-level overview of the system architecture using Drawlib's core primitive functions.

```drawlib 600px center file:system_overview.png caption:"High-Level System Overview"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle((25, 22.5), width=28, height=18, style=Styles.PrimaryFlat, text="Client App", text_style=Styles.WhiteBold)
rectangle((75, 22.5), width=28, height=18, style=Styles.AccentFlat, text="Cloud Backend", text_style=Styles.WhiteBold)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrow_head="->", style=Styles.PrimaryBold)
```

The client application communicates securely with the cloud backend service.
