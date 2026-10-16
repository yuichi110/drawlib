# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Original AI concept icon functions."""

from __future__ import annotations

from typing import Literal

from drawlib._core.l2_types import Coordinate, PosFloat
from drawlib._core.l3_styles import Style
from drawlib._icons.png_icons.original_ai._base import _write


def agent(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing agent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ai_agent", style=style, variant=variant)


def agent_memory(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing agent memory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="agent_memory", style=style, variant=variant)


def agent_swarm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing agent swarm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="multi_agent", style=style, variant=variant)


def ai_agent(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing ai agent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="ai_agent", style=style, variant=variant)


def benchmark(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing benchmark.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="evaluation", style=style, variant=variant)


def dataset(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing dataset.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="dataset", style=style, variant=variant)


def embedding(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing embedding.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="embedding_vector", style=style, variant=variant)


def embedding_vector(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing embedding vector.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="embedding_vector", style=style, variant=variant)


def eval(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing eval.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="evaluation", style=style, variant=variant)


def evaluation(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing evaluation.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="evaluation", style=style, variant=variant)


def feature_store(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing feature store.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="feature_store", style=style, variant=variant)


def fine_tuning(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing fine tuning.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="fine_tuning", style=style, variant=variant)


def function_calling(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing function calling.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="function_calling", style=style, variant=variant)


def gpu(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing gpu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gpu_node", style=style, variant=variant)


def gpu_node(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing gpu node.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="gpu_node", style=style, variant=variant)


def guardrail(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing guardrail.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="prompt_guardrail", style=style, variant=variant)


def inference(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing inference.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="inference_endpoint", style=style, variant=variant)


def inference_endpoint(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing inference endpoint.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="inference_endpoint", style=style, variant=variant)


def jupyter(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing jupyter.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="notebook", style=style, variant=variant)


def llm(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing llm.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="llm_model", style=style, variant=variant)


def llm_model(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing llm model.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="llm_model", style=style, variant=variant)


def lora(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing lora.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="fine_tuning", style=style, variant=variant)


def mcp(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing mcp.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="function_calling", style=style, variant=variant)


def memory(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing memory.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="agent_memory", style=style, variant=variant)


def model_registry(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing model registry.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="model_registry", style=style, variant=variant)


def multi_agent(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing multi agent.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="multi_agent", style=style, variant=variant)


def notebook(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing notebook.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="notebook", style=style, variant=variant)


def npu(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing npu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="npu_node", style=style, variant=variant)


def npu_node(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing npu node.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="npu_node", style=style, variant=variant)


def prompt(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing prompt.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="prompt_template", style=style, variant=variant)


def prompt_guardrail(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing prompt guardrail.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="prompt_guardrail", style=style, variant=variant)


def prompt_template(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing prompt template.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="prompt_template", style=style, variant=variant)


def rag(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing rag.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rag_knowledge_base", style=style, variant=variant)


def rag_knowledge_base(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing rag knowledge base.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="rag_knowledge_base", style=style, variant=variant)


def tool_use(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing tool use.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="function_calling", style=style, variant=variant)


def tpu(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing tpu.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="npu_node", style=style, variant=variant)


def training(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing training.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="training_pipeline", style=style, variant=variant)


def training_data(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing training data.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="dataset", style=style, variant=variant)


def training_pipeline(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing training pipeline.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="training_pipeline", style=style, variant=variant)


def vector_database(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing vector database.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vector_database", style=style, variant=variant)


def vector_db(
    xy: Coordinate,
    width: PosFloat,
    *,
    style: Style,
    variant: Literal["default"] = "default",
) -> None:
    """Draws an Original AI concept icon representing vector db.

    Args:
        xy: Tuple of floats (x, y) representing the coordinates of the icon's center.
            Default alignment is center, center.
        width: Horizontal size of the icon.
        style: Style object (required).
        variant: Visual variant of the icon ('default'). Defaults to "default".

    """
    _write(xy=xy, width=width, name="vector_database", style=style, variant=variant)
