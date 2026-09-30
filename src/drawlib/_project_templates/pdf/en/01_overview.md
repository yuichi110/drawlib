# Chapter 1: System Overview

## Introduction

This chapter provides a high-level overview of the system architecture using Drawlib's core primitive functions.

```drawlib 600px center caption:"High-Level System Overview"
from drawlib.canvas import setup
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles

setup(width=100, height=45)

# Standard shapes drawn with primitive functions
rectangle((25, 22.5), width=28, height=18, style=Styles.primary_flat, text="Client App", textstyle=Styles.white_bold)
rectangle((75, 22.5), width=28, height=18, style=Styles.accent_flat, text="Cloud Backend", textstyle=Styles.white_bold)

# Connecting line with arrow
line((39, 22.5), (61, 22.5), arrowhead="->", style=Styles.bold)
```

The client application communicates securely with the cloud backend service.
