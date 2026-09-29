# Chapter 1: System Overview

## Introduction

This chapter provides a high-level overview of the system architecture.

```drawlib
setup(width=100, height=50)

rectangle((25, 25), width=30, height=20, style=Styles.blue_flat, text="Client App", textstyle=Styles.white_bold)
rectangle((75, 25), width=30, height=20, style=Styles.green_flat, text="Cloud Backend", textstyle=Styles.white_bold)

line((40, 25), (60, 25), arrowhead="<->", style=Styles.bold)
text((50, 28), "TLS / HTTPS", style=Styles.primary)
```

The client application communicates securely with the cloud backend service.
