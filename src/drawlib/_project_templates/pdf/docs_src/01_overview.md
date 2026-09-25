# Chapter 1: System Overview

## Introduction

This chapter provides a high-level overview of the system architecture.

```drawlib
config(width=100, height=50)

rectangle((25, 25), width=30, height=20, style=styles.blue_flat, text="Client App", textstyle=styles.white_bold)
rectangle((75, 25), width=30, height=20, style=styles.green_flat, text="Cloud Backend", textstyle=styles.white_bold)

line((40, 25), (60, 25), arrowhead="<->", style=styles.bold)
text((50, 28), "TLS / HTTPS", style=styles.primary)
```

The client application communicates securely with the cloud backend service.
