# Chapter 1: Diagramming & Documentation Challenges in AI Development

As AI-assisted coding and pair programming become standard practice, the primary bottleneck in software engineering has shifted from writing implementation code to **visualizing system architecture and keeping documentation synchronized**.

## 1.1 The Gap Between Design Docs and Implementation (Documentation Rot)

With AI coding agents (Claude Code, Cursor, Gemini CLI, GitHub Copilot, etc.), source code is refactored and expanded at unprecedented speed. However, system architecture diagrams, sequence diagrams, and database schema diagrams are frequently left behind.

This disconnect leads to chronic engineering problems:
- **Stale Documentation**: Engineers can no longer tell whether the documentation or the current codebase represents the truth.
- **Slower Onboarding**: New team members and fresh AI agent sessions cannot quickly grasp the system's macro architecture.
- **Siloed Tribal Knowledge**: Up-to-date design intent remains buried in commit logs and ephemeral chat transcripts.

## 1.2 Limitations of Manual GUI Drawing Tools

Traditionally, engineers have relied on manual GUI tools to create diagrams:
- draw.io / diagrams.net
- Figma / Miro
- PowerPoint / Google Slides

Diagrams produced in these tools are typically exported and committed to repositories as **binary images (PNG or JPEG)**. Managing binary assets introduces three fundamental flaws:
1. **Unreviewable in Git Diffs**: Pull requests cannot track logical or structural changes inside a binary image.
2. **Inaccessible to AI Agents**: AI coding agents cannot directly edit the internals of a binary PNG. Updating a single box requires a human to open an external GUI tool, rearrange shapes manually, and re-export the file.
3. **Inconsistent Visual Design**: Fonts, color palettes, stroke weights, and margins vary wildly across authors, eroding documentation quality across the organization.

## 1.3 Why Raw SVG and Matplotlib Fail for AI Agents

Can we simply ask an AI to generate diagrams as code using existing formats? In practice, having AI generate **raw SVG** or **Matplotlib** code quickly breaks down:

- **Raw SVG Generation**:
  - Computing text wrapping and multilingual (CJK/Latin) font metrics is difficult, causing labels to overflow or clip against box borders.
  - Calculating arrow coordinates and connector routing manually leads to crossed lines and misaligned arrowheads.
  - Hundreds of low-level `<path>` and `<rect>` elements make the resulting files impossible for humans to review or maintain.
- **Repurposing Matplotlib**:
  - Designed for statistical plots rather than system design, Matplotlib lacks high-level primitives for architecture nodes, container groups, connector routing, vector icons, and graph auto-layout.
  - Verbose boilerplate code increases token consumption and frequently causes AI coordinate or syntax errors.

These challenges motivated the creation of **Drawlib**—a pure-Python library built for **"Illustration as Code"** and **"Illustrated Documentation as Code"**.
