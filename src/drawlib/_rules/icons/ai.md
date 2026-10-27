# Drawlib AI Icons Guidelines (`lib-icons-ai`)

API specification and complete catalog for `drawlib.icons.ai` (`AiIcon`, **60** official AI/ML brand icons) and `drawlib.icons.original_ai` (`OriginalAiIcon`, **80** flat 2D pastel icons: **60** brand twins + **20** vendor-neutral AI/agent concept icons). See `lib-icons-overview` for cross-tier icon rules.

---

## 1. API Signature & Twin Module Structure

Every icon function is **Center-Anchored at `xy = (cx, cy)`** with a `1:1` square aspect ratio and requires `*, style: Style` as a mandatory keyword-only argument:

```python
from drawlib.diagrams.architecture import AiIcon, Node, OriginalAiIcon
from drawlib.icons import ai, ai_icon, original_ai, original_ai_icon
from drawlib.styles import Styles

# 1. Direct module function calls (center-anchored at (cx, cy); style is required)
ai.openai((30, 25), width=9.0, style=Styles.Primary)
original_ai.openai((55, 25), width=9.0, style=Styles.Primary)
original_ai.rag_knowledge_base((80, 25), width=9.0, style=Styles.Primary)

# 2. Dynamic string/Enum dispatchers
ai_icon((30, 10), width=9.0, name="claude", style=Styles.Primary)
original_ai_icon((55, 10), width=9.0, name="ai_agent", style=Styles.Primary)

# 3. High-level ArchitectureDiagram Node integration via Enum
llm_node = Node("Claude LLM", width=24, height=18, icon=AiIcon.CLAUDE, icon_size=7.5)
rag_node = Node("RAG Store", width=24, height=18, icon=OriginalAiIcon.RAG_KNOWLEDGE_BASE, icon_size=7.5)
```

| Module | Diagram Enum | Canonical Count | Asset Archive | Visual Purpose |
| :--- | :--- | :---: | :--- | :--- |
| `drawlib.icons.ai` | `AiIcon` | **60** | `icon_ai` | Official logos for LLM providers, GPU/inference engines, agent frameworks, and MLOps tools. |
| `drawlib.icons.original_ai` | `OriginalAiIcon` | **80** (`60` + `20`) | `icon_original_ai` | Flat 2D pastel twins for all 60 AI brands plus **20 vendor-neutral AI/RAG/agent concept icons**. |

---

## 2. Complete 60 Shared Brand Icons (`ai.*` & `original_ai.*`)

All 60 canonical names below exist identically in `ai.<name>` (`AiIcon.<NAME>`) and `original_ai.<name>` (`OriginalAiIcon.<NAME>`):

| Category | Count | Canonical Function Names (`ai.*` & `original_ai.*`) |
| :--- | :---: | :--- |
| **Foundation LLM Providers & Model Families** | 10 | `claude`, `cohere`, `deepseek`, `gemini`, `grok`, `meta_llama`, `mistral`, `openai`, `perplexity`, `qwen` |
| **Inference Engines, Routers & GPU Clouds** | 13 | `fireworks_ai`, `groq`, `litellm`, `modal`, `nvidia`, `ollama`, `openrouter`, `replicate`, `runpod`, `sglang`, `together_ai`, `triton`, `vllm` |
| **Agent Frameworks, Protocols & Orchestration** | 14 | `a2a`, `autogen`, `crewai`, `dify`, `haystack`, `langchain`, `langgraph`, `llamaindex`, `mastra`, `mcp`, `n8n`, `openhands`, `pydantic_ai`, `semantic_kernel` |
| **Deep Learning & ML Frameworks** | 8 | `huggingface`, `jax`, `jupyter`, `keras`, `onnx`, `pytorch`, `scikit_learn`, `tensorflow` |
| **Observability, Evals, MLOps & Ingestion** | 8 | `arize_phoenix`, `braintrust`, `firecrawl`, `langfuse`, `mlflow`, `ray`, `tavily`, `wandb` |
| **AI Coding, Multimodal Voice & UI Apps** | 7 | `copilot`, `cursor`, `deepgram`, `elevenlabs`, `gradio`, `livekit`, `streamlit` |

---

## 3. Complete 20 Vendor-Neutral AI Concept Icons (`original_ai.*` Only)

| Canonical Function (`original_ai.*`) | `OriginalAiIcon` Enum | Architectural Role |
| :--- | :--- | :--- |
| `agent_memory` | `AGENT_MEMORY` | Short-term working context and long-term episodic agent memory |
| `ai_agent` | `AI_AGENT` | Autonomous reasoning agent executing planning and tool loops |
| `dataset` | `DATASET` | Curated training, validation, or benchmark data corpus |
| `embedding_vector` | `EMBEDDING_VECTOR` | Dense vector encoder and semantic embedding representation |
| `evaluation` | `EVALUATION` | Automated LLM-as-a-Judge scoring and benchmark evaluation |
| `feature_store` | `FEATURE_STORE` | Centralized online/offline ML feature repository |
| `fine_tuning` | `FINE_TUNING` | Supervised fine-tuning (SFT), LoRA adaptation, and RLHF stages |
| `function_calling` | `FUNCTION_CALLING` | Structured tool invocation and external API execution |
| `gpu_node` | `GPU_NODE` | High-density GPU compute node for training or inference |
| `inference_endpoint` | `INFERENCE_ENDPOINT` | Low-latency model serving gateway and token streaming API |
| `llm_model` | `LLM_MODEL` | Vendor-neutral Large Language Model or foundation model core |
| `model_registry` | `MODEL_REGISTRY` | Versioned model weights, checkpoints, and lineage catalog |
| `multi_agent` | `MULTI_AGENT` | Supervisor and specialist multi-agent orchestration topology |
| `notebook` | `NOTEBOOK` | Interactive data science and ML experimentation notebook |
| `npu_node` | `NPU_NODE` | Neural Processing Unit (NPU) or custom AI ASIC accelerator node |
| `prompt_guardrail` | `PROMPT_GUARDRAIL` | Input/output safety filter, PII redaction, and policy guardrail |
| `prompt_template` | `PROMPT_TEMPLATE` | Parameterized system prompt and few-shot context template |
| `rag_knowledge_base` | `RAG_KNOWLEDGE_BASE` | Indexed document chunks and retrieval-augmented knowledge store |
| `training_pipeline` | `TRAINING_PIPELINE` | Distributed pre-training or continuous model retraining workflow |
| `vector_database` | `VECTOR_DATABASE` | Approximate nearest-neighbor (ANN) semantic vector store |

```drawlib code=fold align=center file=icons_ai_rules_arch.png caption="Agentic RAG & MCP Orchestration Topology Using AiIcon and OriginalAiIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import AiIcon, ArchitectureDiagram, Node, NodeGroup, OriginalAiIcon
from drawlib.styles import Styles

setup(width=136, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

guard = d.add(
    Node("Prompt\nGuardrail", width=24, height=18, icon=OriginalAiIcon.PROMPT_GUARDRAIL, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
cluster = d.add(NodeGroup(title="Agentic Runtime & RAG Pipeline", padding=4.5), xy=(42, 4))
agent = cluster.add(Node("LangGraph\nOrchestrator", width=25, height=18, icon=AiIcon.LANGGRAPH, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
rag = cluster.add(Node("RAG Vector\nKnowledge", width=25, height=18, icon=OriginalAiIcon.RAG_KNOWLEDGE_BASE, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(guard, agent, label="Safe Prompt", padding=1.5)
d.connect(agent, rag, label="Retrieve", padding=1.5)
d.draw(xy=(4, 4))
save()
```
