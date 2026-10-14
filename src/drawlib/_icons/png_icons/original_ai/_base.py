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
    "embedding": "embedding_vector",
    "guardrail": "prompt_guardrail",
    "inference": "inference_endpoint",
    "llm": "llm_model",
    "rag": "rag_knowledge_base",
}

ORIGINAL_AI_PROVIDER = PngIconProvider(
    name="original_ai",
    package_name="icon_original_ai",
    asset_subdir="icons/original_ai",
    aliases=ORIGINAL_AI_ALIASES,
)

_write = ORIGINAL_AI_PROVIDER.write
