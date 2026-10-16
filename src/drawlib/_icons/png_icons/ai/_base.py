# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Official AI, LLM, Agent, and ML icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

AI_ALIASES: dict[str, str] = {
    "anthropic": "claude",
    "chatgpt": "openai",
    "google_gemini": "gemini",
    "hf": "huggingface",
    "hugging_face": "huggingface",
    "llama": "meta_llama",
    "meta": "meta_llama",
    "mistral_ai": "mistral",
    "open_hands": "openhands",
    "sk": "semantic_kernel",
    "sklearn": "scikit_learn",
    "tf": "tensorflow",
    "weights_and_biases": "wandb",
}

AI_PROVIDER = PngIconProvider(
    name="ai",
    package_name="icon_ai",
    asset_subdir="icons/ai",
    aliases=AI_ALIASES,
)

_write = AI_PROVIDER.write
