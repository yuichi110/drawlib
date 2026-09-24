# Chapter 2: Technical Design

## Data Flow

This chapter describes how data flows through the processing pipeline.

```drawlib
config(width=100, height=45)

circle((20, 22.5), radius=12, style="blue_flat", text="Ingest", textstyle="white_bold")
rectangle((50, 22.5), width=24, height=18, style="green_flat", text="Process", textstyle="white_bold")
rectangle((80, 22.5), width=24, height=18, style="purple_flat", text="Storage", textstyle="white_bold")

line((32, 22.5), (38, 22.5), arrowhead="->", style="bold")
line((62, 22.5), (68, 22.5), arrowhead="->", style="bold")
```
