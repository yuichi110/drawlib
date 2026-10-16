# Official AI & ML Icons Plan (`drawlib.icons.ai` & `drawlib.icons.original_ai`)

## 1. Objective & Scope

Add 40 official AI, LLM, Agent Framework, Protocol, ML Library, and MLOps icons under a new `drawlib.icons.ai` module (`AiIcon`), and subsequently expand `drawlib.icons.original_ai` (`OriginalAiIcon`) with 40 Drawlib-stylized pastel versions of those logos (at stroke width `1.9` to match `original_data`).

- **Core Separation Rule**:
  - **`drawlib.icons.ai`**: Contains ONLY real products, OSS frameworks, and official protocols that have an unmistakable official logo (40 icons + 13 shorthand aliases). Generic concept icons (`ai_agent`, `rag`, `embedding`, etc.) do NOT belong in `ai`.
  - **`drawlib.icons.original_ai`**: Contains both the existing 20 vendor-neutral AI/Agent concept icons AND the 40 Drawlib-stylized pastel versions of the `ai` logos.

---

## 2. The 40 Canonical `ai` Icons

| Row | Category | Canonical Names (10 per row) |
| :- | :--- | :--- |
| **1** | **LLM Models & Providers** | `openai`, `claude`, `gemini`, `meta_llama`, `mistral`, `deepseek`, `cohere`, `grok`, `qwen`, `perplexity` |
| **2** | **Agent Frameworks & Builders** | `langchain`, `langgraph`, `llamaindex`, `crewai`, `autogen`, `dify`, `openhands`, `haystack`, `semantic_kernel`, `n8n` |
| **3** | **Protocols, Hubs & ML Libraries** | `mcp`, `a2a`, `huggingface`, `ollama`, `vllm`, `litellm`, `pytorch`, `tensorflow`, `keras`, `scikit_learn` |
| **4** | **ML Frameworks, MLOps & UI** | `jax`, `onnx`, `ray`, `mlflow`, `wandb`, `langfuse`, `jupyter`, `streamlit`, `gradio`, `nvidia` |

### Shorthand Aliases (`AI_ALIASES` — 13 aliases)
- `anthropic` -> `claude`
- `chatgpt` -> `openai`
- `google_gemini` -> `gemini`
- `hf` -> `huggingface`
- `hugging_face` -> `huggingface`
- `llama` -> `meta_llama`
- `meta` -> `meta_llama`
- `mistral_ai` -> `mistral`
- `open_hands` -> `openhands`
- `sk` -> `semantic_kernel`
- `sklearn` -> `scikit_learn`
- `tf` -> `tensorflow`
- `weights_and_biases` -> `wandb`

---

## 3. Technical & Authoring Rules for `tools/icons_src/ai/`

- **Canvas**: `100x100` (`setup_icon()`), origin `(0,0)` at bottom-left, center `(50,50)`. Keep all geometry inside `[9.0, 91.0]` (`82x82` inner box).
- **Pure Drawlib Primitives Only**: Never call `image()` or `text()`. Use `polygon()`, `circle()`, `rectangle()`, `draw_compound_polygon()`, `fill_style()`, and `stroke_style()`.
- **Reference Assets**: Stored in `tools/original_assets/ai/<name>/<name>.svg` (39 SVGs + `semantic_kernel.png`), with rasterized `512x512` reference PNGs in `.drawlib/scratch/ai_ref/<name>_ref.png`.
- **Gradient & Multi-Color Handling**:
  - `meta_llama`: 15 SVG path segments along the Meta infinity loop, each colored with its exact gradient midpoint (`#0668E1` to `#0082FB`).
  - `qwen`: Official purple-indigo (`#6950EF`) compound polygon.
  - `gradio`: 3 interlocking chevron ribbons (`#F97700`, `#F99F00`, `#F9C400` / clipped gradient bands).
  - `gemini`: 4-point sparkle with smooth clipped color transitions across `#3186FF` (right/center), `#F94543` (top), `#FABC12` (left), and `#08B962` (bottom).
  - `llamaindex`: Llama silhouette polygon with diagonal clipped gradient bands (`#F6DCD9` -> `#FFA5EA` -> `#45DFF8` -> `#BC8DEB`).
  - `semantic_kernel`: Two interlocking `+45°` cyan-blue and `-45°` purple-violet figure-8 ribbons with dark indigo center circle.
  - `jax`: 38 isometric polygons with `.cls-1..9` fills and thin `#DCE0DF` stroke borders.

---

## 4. Wiring & Packaging Checklist (`drawlib.icons.ai`)

1. **Provider Module**:
   - `src/drawlib/_icons/png_icons/ai/__init__.py`
   - `src/drawlib/_icons/png_icons/ai/_base.py` (`AI_ALIASES`, `AI_PROVIDER`)
   - `src/drawlib/_icons/png_icons/ai/_generated.py` (generated via `./dcli codegen icon-ai`)
2. **Facade & Package Exports**:
   - `src/drawlib/_icons/png_icons/__init__.py` (`ai`)
   - `src/drawlib/_icons/__init__.py` (`ai`)
   - `src/drawlib/icons.py` (`ai`, `sys.modules["drawlib.icons.ai"] = ai`)
3. **Architecture & Sequence Diagram Enums**:
   - `src/drawlib/_diagrams/architecture/_icons.py` (`AiIcon`)
   - `src/drawlib/_diagrams/architecture/__init__.py` (`AiIcon`)
   - `src/drawlib/_diagrams/architecture/_types.py` (`AiIcon` in `IconType`)
   - `src/drawlib/_diagrams/_common.py` (`AiIcon` -> `ai_gen` in `_ENUM_ICON_MODULES` and `draw_enum_icon` / `draw_diagram_icon`)
   - `src/drawlib/_diagrams/sequence/_types.py` & `_render_elements.py` (`AiIcon`)
   - `src/drawlib/diagrams/architecture.py` & `sequence.py` (`AiIcon`)
4. **DCLI Codegen & Release Assets**:
   - `tools/dcli/codegen/icons_build.py` (`"ai": AI_ALIASES` in `PROVIDER_ALIASES`)
   - `tools/dcli/codegen/original_cloud_codegen.py` (`"ai": "AI"` in `PROVIDER_LABELS`, `"ai": "AiIcon"` in `PROVIDER_ENUM_NAMES`)
   - `tools/dcli/codegen/cli.py` (`icon-ai` command)
   - `./dcli release-assets build icon_ai --tag v0.3` and `./dcli release-assets sync --tag v0.3`
5. **Tests & Rules**:
   - `tests/drawlib/icons/test_ai.py`
   - `src/drawlib/_rules/api.md`, `lib_icons.md`, `lib_diagrams.md`

---

## 5. Verification Steps

1. Render grid previews for all 40 icons (`-g --no-cache`) and visually compare every `_grid.png` against `.drawlib/scratch/ai_ref/<name>_ref.png` via `view_file`.
2. Render 512x512 PNGs into `tools/release_assets/v0.3/icons/ai/` and `src/drawlib/_cached_assets/icons/ai/`.
3. Run `./dcli codegen icon-ai`, `./dcli release-assets build icon_ai --tag v0.3`, and `./dcli release-assets sync --tag v0.3`.
4. Run `./dcli code-check all` and `./dcli test target icons --no-cov`.
5. Build a 40-icon contact sheet for `ai`, show the user, and proceed to Phase 2 (`original_ai` expansion with `w = 1.9`).
