# Original AI Icons Expansion Plan (`drawlib.icons.original_ai`)

## 1. Objective & Scope

Expand `drawlib.icons.original_ai` (`OriginalAiIcon`) with 40 Drawlib-stylized pastel versions of the official `ai` logos, matching the exact aesthetic and stroke width (`w = 1.9`) of `drawlib.icons.original_data`.
The existing 20 vendor-neutral concept icons in `original_ai` remain untouched, bringing `original_ai` to 60 canonical icons + 32 shorthand aliases (92 functions total).

---

## 2. Mandatory Design & Code Rules (`original_data` Parity)

1. **Stroke Width & Outlines**:
   - Primary / outer stroke width: `w = 1.9` (`border_units=w` or `width_units=w`, color `DARK = "#323A48"`).
   - Inner seam / detail stroke width: `1.5`–`1.8` (`width_units=1.7` or `1.8`, color `DARK`).
2. **Respect Official Color Usage + Unified Drawlib Tone**:
   - Use Drawlib's numbered pastel palette from `from drawlib.styles import Colors` (`Colors.Blue1..6`, `Colors.Teal1..6`, `Colors.Purple1..6`, `Colors.Pink1..6`, `Colors.Orange1..6`, `Colors.Amber1..6`, `Colors.Green1..6`, `Colors.Red1..6`, `Colors.Gray1..6`, plus `WHITE = "#FFFFFF"` and `DARK = "#323A48"`), or softened custom hex codes when an iconic brand hue sits between standard palette steps (just like `original_data/postgresql_default.py` and `original_data/mariadb_default.py`).
   - **Never split a single-color official shape into two contrasting hues**, and **never add artificial black seam lines** across unified shapes or smooth gradients.
   - **Keep white badge details white** (never recolor white glyphs/nodes to teal or blue).
   - Replace continuous pixel gradients (`gemini`, `llamaindex`, `gradio`) with seamless borderless flat pastel bands inside a crisp `w = 1.9` `DARK` outer contour.
   - Replace harsh pure-black (`#000000`) fills (`openai`, `grok`, `mcp`, `autogen`, `openhands` ticks) with calm slate charcoal (`Colors.Gray6`) and `DARK` outlines.
3. **Canvas & Geometry**:
   - Canvas is `100x100` (`setup_icon()`), origin `(0, 0)` at bottom-left, center `(50.0, 50.0)`.
   - Keep all outer borders strictly inside `[9.0, 91.0]` (`82x82` inner box).
   - **Pure Drawlib Primitives Only**: Never call `image()` or `text()`. Use `polygon()`, `circle()`, `rectangle()`, `draw_compound_polygon()`, `draw_round_polyline()`, `draw_round_segment()`, `fill_style()`, and `no_border_fill()`.
   - Imports MUST use `from drawlib.utils import ...` (never `from utils import ...`).
   - Standard Apache 2.0 header + module docstring `"""Original AI concept icon: <name>."""`.

---

## 3. Icon-by-Icon Design Specifications (4 Batches of 10)

### Batch 1: LLM Models & Providers
1. **`openai`**: 6 interlocking rounded knot petals around a central hollow hexagon. All 6 petals in unified `Colors.Gray6` (respecting solid `#000000` official logo), `WHITE` center hole, `w = 1.9` `DARK` borders.
2. **`claude`**: Iconic 12-ray asymmetric sunburst filled in softened terracotta `#E08568` (respecting official `#D97757`) with `w = 1.9` `DARK` outline.
3. **`gemini`**: 4-point concave sparkle star with 4 seamless pastel color zones (`Colors.Blue3` right+center, `Colors.Red3` top, `Colors.Amber3` left, `Colors.Green3` bottom), NO interior black X-lines, and a single united `w = 1.9` `DARK` outer outline.
4. **`meta_llama`**: Continuous twisted infinity loop (`∞`) with both halves in rich `Colors.Blue3` (respecting official Meta blue), `WHITE` loop holes, and `w = 1.9` `DARK` borders showing the over/under crossover.
5. **`mistral`**: Stepped pixel-block "M" tower in all 5 official horizontal color rows from top to bottom (`Colors.Amber2`, `Colors.Amber3`, `Colors.Orange3`, `#EC6E42`, `Colors.Red3`) with no interior black lines and `w = 1.9` `DARK` outer outline.
6. **`deepseek`**: Leaping whale silhouette with body, dorsal fin, and tail fluke in unified `Colors.Blue3` (no black cut seams on fin/tail), `WHITE` belly and eye cutouts, and `w = 1.9` `DARK` borders.
7. **`cohere`**: Three rounded organic pebbles matching official hues: top-wide forest-sage `#4D6E60` (`#39594D`), bottom-left coral `#F2826B` (`#FF7759`), bottom-right lilac `Colors.Purple2` (`#D18EE2`), each with `w = 1.9` `DARK` border.
8. **`grok`**: Circular orbital ring and diagonal slash blade both in unified `Colors.Gray6` (no two-tone blade split or center ridge line), `WHITE` inner circle hole, and `w = 1.9` `DARK` outlines.
9. **`qwen`**: Official 6-pointed woven star with central triangle hole and woven channel cutout in unified `#7A68F0` (softened `#6950EF`) + `WHITE` cutouts + `w = 1.9` `DARK` borders.
10. **`perplexity`**: Hollow crystal wireframe bars filled in unified `Colors.Teal3` (`#22B8CD`) with open `WHITE` window panes inside and crisp `DARK` outlines.

### Batch 2: Agent Frameworks & Builders
11. **`langchain`**: Parrot + chain link petals all in unified sky-blue `#8AC8FA` (softened `#7FC8FF`) with `w = 1.9` `DARK` borders.
12. **`langgraph`**: Stadium pill badge in deep forest-teal `#2D5252` (`#1C3C3C`) containing `WHITE` bird on left and `WHITE` 4-node diamond graph on right, with `DARK` outlines.
13. **`llamaindex`**: Standing llama profile split into 4 borderless diagonal pastel bands (`Colors.Pink1` head -> `Colors.Pink2` neck -> `Colors.Teal2` chest/belly/front legs -> `Colors.Purple2` rump/back legs) with NO interior black seam lines and `w = 1.9` `DARK` outer contour.
14. **`crewai`**: One continuous C-swirl in softened deep burgundy `#6B2D2B` (`#461816`) with zero interior cut seams, `WHITE` inner crescent space, and `w = 1.9` `DARK` outer/inner outlines.
15. **`autogen`**: Rounded square badge in `Colors.Gray6` (`#2D2D2F`) with BOTH "A" and "G" vector polygons in `WHITE` and `DARK` borders.
16. **`dify`**: Geometric "i" dot and "if" hooked body both in unified `Colors.Blue4` (`#0033FF`) with `w = 1.9` `DARK` outlines.
17. **`openhands`**: Open hands in soft pale yellow `#FFF08A` (`#FFFF8B`) and top 3 celebration rays in `Colors.Gray6` (`#000000`, no orange), all outlined in `DARK`.
18. **`haystack`**: Rounded square badge in `Colors.Blue3` (`#2558FF`) with BOTH "h" stem and bottom-left dot in `WHITE` and `DARK` outlines.
19. **`semantic_kernel`**: Interlocking 45-degree figure-8 loops with upper loop in `#78D2FA` / `Colors.Blue3`, lower loop in `Colors.Purple2` / `Colors.Purple3`, and center sphere in deep indigo `Colors.Blue5`, all with `DARK` borders.
20. **`n8n`**: Connected 4-node workflow graph with all 4 rings AND all 3 bars in unified rose-pink `#EC6888` (`#EA4B71`), `WHITE` node holes, and `w = 1.9` `DARK` borders.

### Batch 3: Protocols, Hubs & ML Libraries
21. **`mcp`**: Rotated double-arch "M" ribbon with BOTH parts in unified `Colors.Gray6` (`#000000`, no blue) and `w = 1.9` `DARK` borders.
22. **`a2a`**: Orbital ring band AND all 3 circular badges ("A", "2", "A") in unified `Colors.Blue3` (`#2874D7`) with `WHITE` inner core and `WHITE` vector glyphs, all outlined in `DARK`.
23. **`huggingface`**: Round face in `Colors.Amber2` (`#FFD21E`), hands and cheeks in `Colors.Amber3` (`#FF9D0B`), tongue in `Colors.Red3` (`#FF323D`), eyes/mouth in `DARK`.
24. **`ollama`**: Fluffy llama front portrait with body, inner ears, and snout in pure `WHITE` and crisp `DARK` outlines/eyes (matching pure B&W official logo).
25. **`vllm`**: Left triangle wing in `Colors.Amber3` (`#FDB515`) and right parallelogram wing in `#58AEFA` (`#30A2FF`) with `w = 1.9` `DARK` outlines.
26. **`litellm`**: Rounded square badge AND train cutouts (cockpit, window, nose, pill) all in unified `Colors.Blue4` (`#0117BE`), train body in `WHITE`, with `DARK` outlines.
27. **`pytorch`**: Flame-loop ring AND top-right dot both in unified vermilion `#EE6A4E` (`#EE4C2C`) with `w = 1.9` `DARK` borders.
28. **`tensorflow`**: Official two flat isometric halves (left "T" and right "F" with vertical center gap) both in unified `Colors.Orange3` (`#FF6F00`), no 3D underside shadows or yellow split, with `w = 1.9` `DARK` outlines.
29. **`keras`**: Rounded square badge in crimson `#D84A52` (`#D00000`) with chamfered `WHITE` "K" polygon and `DARK` borders.
30. **`scikit_learn`**: Official bottom-left tilted blob in `#54A6D4` (`#3499CD`) and top-right tilted blob in `Colors.Orange3` (`#F89939`) with `w = 1.9` `DARK` borders and official vector script polygons in `DARK` and `WHITE`.

### Batch 4: ML Frameworks, MLOps & UI
31. **`jax`**: Isometric "JAX" facets in `Colors.Blue2..3` ("J"), `Colors.Teal2..4` ("A"), and `Colors.Purple2..4` ("X") with `w = 1.9` `DARK` outer borders and `1.45` inner seams.
32. **`onnx`**: All 8 crystal polyhedron facets in monochrome gray shades (`Colors.Gray3..6` matching `#3E3E3D`..`#717272`, no blue facets) with `DARK` wireframe chords and vertex dots.
33. **`ray`**: All 5 squares AND all 3 radiating spoke bars in unified cyan-blue `#3DB4D8` (`#02A0CF`) with `w = 1.9` `DARK` outlines.
34. **`mlflow`**: Left crescent arrow in `#45A4E5` (`#0194E2`) and right crescent arrow in `#6AD0EE` (`#43C9ED`) with `w = 1.9` `DARK` outlines.
35. **`wandb`**: All 12 circles of the 3×4 wave grid in unified `Colors.Amber3` (`#FCBC32`) with `1.8` `DARK` borders.
36. **`langfuse`**: Intertwined crossing loops in `Colors.Red3` (`#FF5D5F`) and `Colors.Blue3` (`#4E9CFF`) with `w = 1.9` `DARK` borders.
37. **`jupyter`**: Top and bottom crescents in `Colors.Orange3` (`#F37726`) and ALL 3 satellite moons in gray (`Colors.Gray4` / `Colors.Gray5`, no orange moon) with `w = 1.9` `DARK` borders.
38. **`streamlit`**: 3-peak crown with center peak in `Colors.Red3` (`#FF4B4B`), left wing in `Colors.Red4` (`#BD4043`), and right wing in `#9E353F` (`#7D353B`) so side wings are darker than center, with `DARK` seams and outline.
39. **`gradio`**: Bottom diamond loop (`Colors.Amber3` left -> `Colors.Orange3` right) and top diamond loop (`Colors.Orange3` left -> `Colors.Amber3` right) with seamless interior color transition and `w = 1.9` `DARK` outlines.
40. **`nvidia`**: Left spiral bands AND right rounded badge both in unified lime-green `#7CC242` (`#74B71B`) with `WHITE` right cutouts and `w = 1.9` `DARK` borders.

---

## 4. Workflow & Verification

1. **Phase 2A (Parallel Subagents — 4 Batches of 10)**:
   - Each subagent updates its 10 assigned `tools/icons_src/original_ai/<name>_default.py` scripts.
   - Each subagent runs Ruff check/format (Stage 1) and renders a grid preview (`-g --no-cache`) to `.drawlib/scratch/orig_ai_fix_<name>_grid.png` (Stage 2), inspecting every image via `view_file` against `tools/release_assets/v0.3/icons/ai/<name>_default.png`.
2. **Phase 2B (Parent Orchestrator — Build, Codegen & Visual Verification)**:
   - Render all 40 updated `512x512` PNGs into `tools/release_assets/v0.3/icons/original_ai/`.
   - Run `./dcli codegen icon-original-ai` to normalize all 60 PNGs, update `manifest.json`, and regenerate bindings.
   - Copy normalized PNGs + `manifest.json` to `src/drawlib/_cached_assets/icons/original_ai/`.
   - Run `./dcli release-assets sync --tag v0.3` and `./dcli release-assets build icon_original_ai --tag v0.3`.
   - Render the 40-icon `original_ai_icons_contact_sheet.png` (`--no-cache`) and inspect via `view_file` alongside `ai_icons_contact_sheet.png`.
   - Run `./dcli code-check all`, `./dcli test target icons --no-cov`, and `./dcli release-assets sync --tag v0.3 --check`.
