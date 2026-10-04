---
layout: default
header: "Unified Ecosystem"
footer: "Drawlib: Illustration as Code"
paginate: true
---

::: block (80, 140) (1760, 840)
# One Illustration Core, Multiple Targets

Drawlib unifies engineering documentation and technical visualizations as version-controlled code:

| Target | Command | Output | Primary Use Case |
| :--- | :--- | :--- | :--- |
| **Standalone Images** | `drawlib build image` | PNG, WebP, PDF | README graphics, blog posts, whitepapers |
| **Documentation Site** | `drawlib build html` | Static Web Site | Technical specs, API references, architecture docs |
| **Document Book** | `drawlib build pdf` | Merged Vector PDF | Formal RFCs, architecture books, print designs |
| **Presentation Deck** | `drawlib build slide` | HTML Slide Deck | Conference talks, design reviews, team pitches |

---

### Get Started Today

```bash
# Initialize a new presentation project with Google styling
uv run drawlib init slide -s google

# Build presentation slides
uv run drawlib build slide slide_src/ -o slide/

# Start interactive preview server
uv run drawlib serve slide/
```
:::
