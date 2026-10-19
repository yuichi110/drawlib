# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

ORIGINAL_AI_ALIASES: dict[str, str] = {
    "agent": "ai_agent",
    "agent_swarm": "multi_agent",
    "anthropic": "claude",
    "benchmark": "evaluation",
    "chatgpt": "openai",
    "copilot_ai": "copilot",
    "embedding": "embedding_vector",
    "eval": "evaluation",
    "fireworks": "fireworks_ai",
    "github_copilot": "copilot",
    "google_gemini": "gemini",
    "gpu": "gpu_node",
    "guardrail": "prompt_guardrail",
    "hf": "huggingface",
    "hugging_face": "huggingface",
    "inference": "inference_endpoint",
    "llama": "meta_llama",
    "llm": "llm_model",
    "lora": "fine_tuning",
    "memory": "agent_memory",
    "meta": "meta_llama",
    "mistral_ai": "mistral",
    "npu": "npu_node",
    "nvidia_triton": "triton",
    "open_hands": "openhands",
    "phoenix": "arize_phoenix",
    "prompt": "prompt_template",
    "pydantic": "pydantic_ai",
    "rag": "rag_knowledge_base",
    "sk": "semantic_kernel",
    "sklearn": "scikit_learn",
    "tf": "tensorflow",
    "together": "together_ai",
    "tool_use": "function_calling",
    "tpu": "npu_node",
    "training": "training_pipeline",
    "training_data": "dataset",
    "vector_db": "vector_database",
    "weights_and_biases": "wandb",
}

ORIGINAL_AI_PROVIDER = PngIconProvider(
    name="original_ai",
    package_name="icon_original_ai",
    asset_subdir="icons/original_ai",
    aliases=ORIGINAL_AI_ALIASES,
)

_write = ORIGINAL_AI_PROVIDER.write
