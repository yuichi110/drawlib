# Chapter 2: Technical Design

## Data Flow

This chapter describes how data flows through the processing pipeline.

```drawlib
config(width=100, height=45)

circle((20, 22.5), radius=12, style=styles.blue_flat, text="Ingest", textstyle=styles.white_bold)
rectangle((50, 22.5), width=24, height=18, style=styles.green_flat, text="Process", textstyle=styles.white_bold)
rectangle((80, 22.5), width=24, height=18, style=styles.purple_flat, text="Storage", textstyle=styles.white_bold)

line((32, 22.5), (38, 22.5), arrowhead="->", style=styles.bold)
line((62, 22.5), (68, 22.5), arrowhead="->", style=styles.bold)
```
