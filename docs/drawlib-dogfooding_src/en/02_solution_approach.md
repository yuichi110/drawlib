# Chapter 2: The Solution: Illustrated Documentation as Code

Drawlib delivers **"Illustrated Documentation as Code" (IDaC)** for software engineers and AI coding agents. While traditional Documentation-as-Code focused solely on text, Drawlib elevates architectural diagrams, system designs, and workflows into first-class, version-controlled code.

## 2.1 Core Principles of Illustrated Documentation as Code

Drawlib is built on four pillars:
1. **Declarative Python Scripts**: Define architecture diagrams, flowcharts, quantitative charts, and structured SmartArts using intuitive, high-level Python APIs.
2. **Inline Markdown Embedding**: Embed drawing code directly inside your Markdown documents via ````drawlib```` code fences.
3. **Full Version Control & Git Diffs**: Diagram definitions live as plain text in Git, enabling line-by-line diff reviews in pull requests.
4. **Multi-Format Compilation & Incremental Caching**: A single CLI build (`drawlib build`) compiles your source into multi-page HTML sites (`site`), A4 vector PDFs and linear HTML reports (`doc`), 16:9 widescreen HTML/PDF slide decks (`slide`), and GitHub-flavored Markdown—accelerated by a SQLite incremental build cache (`.drawlib/cache.db`) that only re-renders modified diagrams.

## 2.2 Traditional Approach vs. Drawlib

```drawlib align=center file=fig_solution_comparison.png caption="Figure 2.1: Comparing Traditional Manual Drawing with Drawlib"
from drawlib.canvas import save, setup
from drawlib.icons import phosphor
from drawlib.lines import line
from drawlib.shapes import rectangle
from drawlib.styles import Styles
from drawlib.text import text

setup(width=116, height=44)

# Left: Traditional Approach (Neutral card)
rectangle((28.0, 22.0), width=48, height=36, style=Styles.Neutral.patch(shape_r=2.0))
text((28.0, 35.0), text="Traditional Manual Approach", style=Styles.DarkBold.patch(text_size=11.5))
line((6.0, 30.0), (50.0, 30.0), style=Styles.Muted)
phosphor.file_x(xy=(11.5, 17.0), width=6.5, style=Styles.Secondary)
text((16.5, 17.0), text="• Hand-drawn in Figma / draw.io\n• Binary PNGs stored in Git\n• Out-of-sync docs & diagram rot", style=Styles.Dark.patch(text_size=10.5, halign="left"))

# Right: Drawlib Approach (PrimaryNeutral card + PrimaryFlat header banner)
rectangle((88.0, 22.0), width=48, height=36, style=Styles.PrimaryNeutral.patch(shape_r=2.0))
rectangle((88.0, 35.0), width=48, height=10, style=Styles.PrimaryFlat.patch(shape_r=2.0))
text((88.0, 35.0), text="Illustrated Doc as Code", style=Styles.WhiteBold.patch(text_size=11.5))
phosphor.code(xy=(71.5, 17.0), width=6.5, style=Styles.Primary)
text((76.5, 17.0), text="• Declarative Python code\n• Inline Markdown embedding\n• Git diff reviews & auto-builds", style=Styles.DarkBold.patch(text_size=10.5, halign="left"))

line((53.5, 22.0), (62.5, 22.0), arrow_head="->", style=Styles.DarkBold)

save()
```

## 2.3 Synergy with AI Pair Programming

Expressing diagrams as executable code transforms collaboration with AI coding agents (Claude Code, Cursor, Gemini CLI, GitHub Copilot, etc.):
- **Spec-Driven Generation**: When you implement a new microservice or data model, simply prompt your AI agent to update the architecture diagram, and it generates the corresponding Python block directly.
- **Multimodal Visual Verification**: AI agents render diagrams with a coordinate grid (`drawlib show -g`), visually inspect the output image, and self-correct overlapping labels or routing defects before delivering the result.
- **100% Deterministic Reproducibility**: The same Python code renders pixel-identical diagrams across every machine and CI/CD environment.
