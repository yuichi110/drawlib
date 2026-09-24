# Chapter 1: System Overview

## Introduction

This chapter provides a high-level overview of the system architecture.

```drawlib
config(width=100, height=50)

rectangle((25, 25), width=30, height=20, style="blue_flat", text="Client App", textstyle="white_bold")
rectangle((75, 25), width=30, height=20, style="green_flat", text="Cloud Backend", textstyle="white_bold")

line((40, 25), (60, 25), arrowhead="<->", style="bold")
text((50, 28), "TLS / HTTPS")
```

The client application communicates securely with the cloud backend service.
