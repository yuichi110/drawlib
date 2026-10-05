# AI Agent Instructions & Prompt Engineering

Drawlib was built from the ground up for the era of AI-assisted engineering. Instead of asking Large Language Models (LLMs) to construct thousands of lines of fragile SVG path strings or brittle Matplotlib code, Drawlib gives AI agents a clean, high-level, declarative Python vocabulary designed for zero-shot architectural visualization.

---

## 1. Why Drawlib is Ideal for AI Agents

1. **Deterministic Geometry**: Unlike heuristic layout engines (e.g. Graphviz, PlantUML) that scramble diagrams unexpectedly when a label changes, Drawlib uses a predictable Cartesian coordinate system where `(0, 0)` is anchored at the bottom-left.
2. **High-Level Domain Abstractions**: AI agents can instantiate enterprise architecture topologies, UML class models, and data charts in fewer than 20 lines of Python.
3. **On-Demand Knowledge Retrieval**: Drawlib includes a built-in terminal rules catalog (`drawlib rules show <topic>`). Agents can fetch targeted API specifications on demand without consuming valuable context window space with massive upfront manuals.

---

## 2. Recommended Agent Instruction Template

Copy and paste the following snippet into your repository's AI instruction file (e.g. `.cursorrules`, `.agents/rules/docs.md`, or Claude/Gemini system prompts):

````markdown
# Drawlib Agent Directives

Drawlib is a pure-Python library for "Illustration as Code" and "Documentation as Code".
When tasked with creating diagrams, architectures, flowcharts, or charts, follow these rules:

1. High-Level Over Low-Level:
   Always favor high-level components over assembling raw rectangles and lines:
   - Cloud Topologies: `drawlib.diagrams.architecture.ArchitectureDiagram`
   - Flowcharts & Swimlanes: `drawlib.diagrams.flow.FlowDiagram`
   - API Sequences: `drawlib.diagrams.sequence.SequenceDiagram`
   - UML Class Hierarchies: `drawlib.diagrams.class_diagram.ClassDiagram`
   - Relational Database Schemas: `drawlib.diagrams.er.ERDiagram`
   - State Machines: `drawlib.diagrams.state.StateDiagram`
   - Pipelines & Steps: `drawlib.smartarts.ChevronProcess`
   - Quantitative Charts: `drawlib.charts` (BarChart, LineChart, AreaChart, PieChart, RadarChart, GanttChart)

2. Coordinate System:
   - (0, 0) is the BOTTOM-LEFT corner of the canvas.
   - X increases rightward, Y increases upward.
   - For icons and architecture nodes, coordinates define the CENTER of the icon.

3. The Multimodal Self-Correction Loop:
   - Write diagram prototype in `.drawlib/scratch/test_diagram.py` (ensure `.drawlib/` is in `.gitignore`).
   - Render headless with grid: `uv run drawlib show .drawlib/scratch/test_diagram.py -g -o .drawlib/scratch/test_diagram.png`.
   - Multimodal review: Inspect the image for label clipping, line overlaps, or missing margins.
   - Fix coordinates, re-render, and present to user.

4. Fetch Rules on Demand:
   If you need exact parameter signatures or examples, run:
   `uv run drawlib rules show <topic>` (e.g. `lib-diagrams`, `lib-charts`, `lib-smartarts`, `style-guide`).
````

---

## 3. Dynamic Knowledge Retrieval (`drawlib rules`)

Instead of pasting entire documentation pages into prompts, train your agent to run `drawlib rules`:

```bash
# List all 21 modular rule topics:
uv run drawlib rules list

# Retrieve targeted manuals:
uv run drawlib rules show agent-instruction    # Workflow loop
uv run drawlib rules show lib-diagrams          # Architecture, flow, sequence, class, ER
uv run drawlib rules show lib-charts            # Bar, line, area, pie, radar, gantt
uv run drawlib rules show lib-smartarts         # Tables, trees, mindmaps, cycle loops
uv run drawlib rules show style-guide           # 6-color semantic system & typography
```

---

## 4. Prompting Best Practices

When asking an AI agent to generate a diagram:
- **Provide Context**: Reference the actual code files (e.g., "Look at `src/services/order.py` and draw an `ArchitectureDiagram` showing the services it communicates with").
- **Specify Canvas Dimensions**: Suggest canvas units (e.g., "Use canvas size 100x60").
- **Ask for Multimodal Verification**: Remind the agent to test and inspect the rendered image before delivering the final code.
