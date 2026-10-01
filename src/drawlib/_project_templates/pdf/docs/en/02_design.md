# Chapter 2: Technical Design

## Component Architecture

This chapter describes the multi-tier component architecture using reusable drawing helpers defined in `utils.py` and local image assets stored in `_assets/`.

```drawlib 600px center caption:"Detailed Component Architecture"
from drawlib.canvas import setup
from drawlib.images import image
from drawlib.styles import Styles
from drawlib.utils import connect, service_card

setup(width=110, height=52)

# Service nodes drawn using reusable helper from utils.py
service_card((20, 24), title="Web Client", subtitle="Browser / App")
service_card((55, 24), title="Linux Server", subtitle="Ubuntu / Nginx", style=Styles.AccentFlat)
service_card((90, 24), title="Database", subtitle="PostgreSQL", style=Styles.SecondaryFlat)

# Connections with protocol labels
connect((32, 24), (43, 24), label="HTTPS")
connect((67, 24), (78, 24), label="SQL")

# Embedded local image asset from doc_src/_assets/ directory
image((55, 41), width=8, image="_assets/linux.png")
```

The system separates concerns across client access, application logic on the Linux host, and persistent storage.
